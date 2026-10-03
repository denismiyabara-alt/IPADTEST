"""Manchete que se enche: a frase entra e a palavra-chave se preenche de vermelho (ou ganha o marca-texto)
no instante em que é falada. HyperFrames, a partir de um JSON.

Uso:
  python3 biblioteca/manchete/gerar.py exemplos/manchete-ipca-16x9.json -o projetos/manchete
  (ou: ./biblioteca/renderizar.sh exemplos/manchete-ipca-16x9.json)

O que acontece na tela:
  1. kicker e frase entram: palavra por palavra no tempo da fala (se vier "palavras" com o instante de cada uma,
     tirado da transcrição) ou em cascata rápida;
  2. em "t_chave" (o instante em que a palavra-chave é falada), a chave se preenche da esquerda para a direita:
     "preencher" = o texto vira vermelho; "marca-texto" = uma faixa vermelha passa por trás e o texto fica claro;
  3. pouso: fim do preenchimento, um pulso e o único som; a fonte fica no rodapé a peça inteira.

Entrada (JSON) — ver biblioteca/README.md:
  peca: "manchete"; estilo; formato; duracao (5 a 10 s); kicker; fonte ("Fonte: ...")
  frase: o texto (até 90 caracteres); chave: palavra(s) inteiras da frase, uma vez só
  marca: "preencher" | "marca-texto"; t_chave: instante da fala da chave (s); dur_chave: duração do preenchimento
  palavras: null | [instante de cada palavra da frase, em s] (da transcrição, ex.: Whisper com word timestamps)
  ativos: true se a frase cita ativo (a tela mostra "Não é recomendação de investimento."); som
"""
import argparse, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MOTION = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(MOTION, "comum"))
from estilo import AVISO_ATIVOS, ESTILOS, FORMATOS, DadosInvalidos, checar_ativos, esc, numero_ok, validar_base  # noqa: E402
import projeto  # noqa: E402

MAX_CARACTERES = 90
MARCAS = ("preencher", "marca-texto")


def palavras_da_frase(frase):
    return frase.split()


def posicao_chave(frase, chave):
    """-> (i, j): a chave são as palavras i..j-1 da frase. None se não estiver lá exatamente uma vez."""
    p, c = palavras_da_frase(frase), palavras_da_frase(chave)
    achou = [i for i in range(len(p) - len(c) + 1) if c and p[i:i + len(c)] == c]
    return (achou[0], achou[0] + len(c)) if len(achou) == 1 else None


def validar(d):
    if not isinstance(d, dict):
        raise DadosInvalidos(["a entrada precisa ser um objeto JSON"])
    d = json.loads(json.dumps(d))
    erros = []
    if d.get("peca", "manchete") != "manchete":
        erros.append(f"'peca' deve ser 'manchete', veio {d.get('peca')!r}")
    d["peca"] = "manchete"
    frase = d.get("frase")
    if not isinstance(frase, str) or not frase.strip():
        erros.append("'frase' é obrigatória (texto)")
        frase = ""
    elif len(frase) > MAX_CARACTERES:
        erros.append(f"'frase' com {len(frase)} caracteres: no máximo {MAX_CARACTERES} (manchete, não parágrafo)")
    d["frase"] = " ".join(frase.split())
    d.setdefault("titulo", d["frase"])
    validar_base(d, erros)
    d.setdefault("marca", "preencher")
    d.setdefault("palavras", None)
    d.setdefault("dur_chave", 0.5)
    if d["marca"] not in MARCAS:
        erros.append(f"'marca' deve ser 'preencher' ou 'marca-texto', veio {d['marca']!r}")
    pos = posicao_chave(d["frase"], d.get("chave") or "") if isinstance(d.get("chave"), str) else None
    if pos is None:
        erros.append("'chave' deve ser palavra(s) inteira(s) da frase, presente(s) uma vez só")
    n = len(palavras_da_frase(d["frase"]))
    dur = d["duracao"] if numero_ok(d["duracao"]) else 8.0
    pal = d["palavras"]
    if pal is not None:
        if not (isinstance(pal, list) and len(pal) == n and all(numero_ok(t) for t in pal)):
            erros.append(f"'palavras' deve ter o instante (s) de cada uma das {n} palavras da frase")
        elif any(b < a for a, b in zip(pal, pal[1:])) or pal[0] < 0 or pal[-1] > dur - 1:
            erros.append("'palavras': instantes em ordem, de 0 até 1 s antes do fim")
    if "t_chave" not in d and pos is not None:
        d["t_chave"] = pal[pos[0]] if isinstance(pal, list) and len(pal) == n and all(numero_ok(t) for t in pal) \
            else round(0.3 + 0.07 * n + 0.6, 3)
    if not numero_ok(d.get("t_chave")) or not numero_ok(d["dur_chave"]) or not 0.15 <= d["dur_chave"] <= 1.5:
        erros.append("'t_chave' (s) e 'dur_chave' (0,15 a 1,5 s) devem ser números")
    elif not 0.3 <= d["t_chave"] <= dur - d["dur_chave"] - 0.8:
        erros.append(f"'t_chave' = {d['t_chave']} s: a chave precisa terminar de encher até 0,8 s antes do fim ({dur} s)")
    if pos is not None and isinstance(pal, list) and len(pal) == n and numero_ok(d.get("t_chave")) \
            and d["t_chave"] + 1e-9 < pal[pos[0]]:
        erros.append("'t_chave' antes de a palavra-chave aparecer na tela")
    checar_ativos(d, [d["frase"], d.get("kicker")], erros)
    if erros:
        raise DadosInvalidos(erros)
    return d


def tempos(d):
    n = len(palavras_da_frase(d["frase"]))
    entrada = d["palavras"] or [round(0.3 + 0.07 * k, 3) for k in range(n)]
    tp = round(d["t_chave"] + d["dur_chave"], 3)
    return dict(entrada=entrada, tc=d["t_chave"], dc=d["dur_chave"], tp=tp, dur=float(d["duracao"]))


def layout(d):
    W, H = FORMATOS[d["formato"]]
    n = len(d["frase"])
    if d["formato"] == "16:9":
        px = 132 if n <= 40 else 112 if n <= 60 else 96
        return dict(W=W, H=H, pad=120, kicker_y=150, px=px, fonte_y=H - 80, largura=W - 240)
    px = 128 if n <= 30 else 110 if n <= 55 else 92
    return dict(W=W, H=H, pad=80, kicker_y=420, px=px, fonte_y=1600, largura=W - 160)


CSS = """
  #kicker {{ position:absolute; left:{pad}px; top:{kicker_y}px; font:{mono}; letter-spacing:.14em; text-transform:uppercase; color:var(--cinza); }}
  #frase {{ position:absolute; left:{pad}px; top:0; bottom:0; width:{largura}px; display:flex; align-items:center; }}
  #frase p {{ font:{titulo}; letter-spacing:-.01em; }}
  .pal {{ display:inline-block; }}
  #chave {{ position:relative; display:inline-block; white-space:nowrap; }}
  #chave .base {{ position:relative; color:var(--tinta); }}
  #faixa {{ position:absolute; left:-.08em; right:-.08em; top:.06em; bottom:.02em; background:var(--destaque);
            transform-origin:left center; transform:scaleX(0); }}
  #cheia {{ position:absolute; left:0; top:0; white-space:nowrap; color:var(--COR_CHEIA); clip-path:inset(0 100% 0 0); }}
  #rodape {{ position:absolute; left:{pad}px; right:{pad}px; top:{fonte_y}px; display:flex; flex-direction:{rodape_dir};
             justify-content:space-between; gap:8px 32px; font:{mono_fonte}; }}
  #fonte {{ color:var(--cinza); }}
  #aviso {{ color:var(--tinta); white-space:nowrap; }}
"""

JS = r"""
  const tl = gsap.timeline({ paused: true });
  const enche = { p: 0 };
  const cheia = document.getElementById('cheia'), faixa = document.getElementById('faixa');
  function desenhar() {
    cheia.style.clipPath = `inset(0 ${(100 - 100 * enche.p).toFixed(3)}% 0 0)`;
    if (faixa) faixa.style.transform = `scaleX(${enche.p.toFixed(4)})`;
  }
  desenhar();
  tl.from('#kicker', { opacity: 0, y: 24, duration: .4, ease: 'power2.out' }, 0);
  tl.from('#rodape', { opacity: 0, duration: .4 }, .5);
  // as palavras entram no tempo da fala
  D.entrada.forEach((t, k) => tl.from('#P' + k, { opacity: 0, y: 26, duration: .28, ease: 'power2.out' }, t));
  // a chave se enche da esquerda para a direita no instante em que é falada
  tl.to(enche, { p: 1, duration: D.dc, ease: 'power1.inOut', onUpdate: desenhar }, D.tc);
  // pouso: pulso (e o único som, na trilha de áudio)
  tl.fromTo('#chave', { scale: 1 }, { scale: 1.08, duration: .14, ease: 'power2.out', yoyo: true, repeat: 1,
                                       immediateRender: false, transformOrigin: 'center center' }, D.tp);
  BOIL
  tl.set({}, {}, D.dur);
  window.__timelines = window.__timelines || {};
  window.__timelines["manchete"] = tl;
"""

TELA = r"""  window.__tela = () => {
    const op = el => { let o = 1; for (let n = el; n && n.nodeType === 1; n = n.parentElement) o *= +getComputedStyle(n).opacity; return o; };
    const pal = D.palavras.map((_, k) => { const e = document.getElementById('P' + k); return { texto: e.textContent, visivel: op(e) > .9 }; });
    const r = document.getElementById('chave').getBoundingClientRect();
    const txt = id => { const e = document.getElementById(id); return e ? e.textContent : null; };
    return { palavras: pal, frase: pal.map(p => p.texto).join(' '), chave: document.querySelector('#chave .base').textContent,
             enchimento: enche.p, clip: cheia.style.clipPath, cor_cheia: getComputedStyle(cheia).color,
             faixa: faixa ? { escala: enche.p, cor: getComputedStyle(faixa).backgroundColor } : null,
             chave_caixa: { x: r.left, y: r.top, w: r.width, h: r.height, W: innerWidth, H: innerHeight },
             fonte: txt('fonte'), fonte_visivel: op(document.getElementById('fonte')) > .9,
             aviso: document.getElementById('aviso') ? txt('aviso') : '' };
  };
"""


def montar_html(d, sfx=None, sfx_dur=1.0):
    d = validar(d)
    e = ESTILOS[d["estilo"]]
    L = layout(d)
    T = tempos(d)
    i, j = posicao_chave(d["frase"], d["chave"])
    pal = palavras_da_frase(d["frase"])
    tp = lambda papel, px: projeto.tipo(d["estilo"], papel, px)
    vert = d["formato"] == "9:16"
    cor_cheia = "papel" if d["marca"] == "marca-texto" else "destaque"
    css = CSS.format(pad=L["pad"], kicker_y=L["kicker_y"], largura=L["largura"], fonte_y=L["fonte_y"],
                     mono=tp("mono", 30), titulo=tp("titulo", L["px"]), mono_fonte=tp("mono", 28 if not vert else 26),
                     rodape_dir="column" if vert else "row").replace("COR_CHEIA", cor_cheia)
    chave_txt = " ".join(pal[i:j])
    faixa = '<span id="faixa"></span>' if d["marca"] == "marca-texto" else ""
    partes = []
    for k, w in enumerate(pal):
        if k == i:
            ids = "".join(f'<span class="pal" id="P{m}">{esc(pal[m])}</span>{" " if m < j - 1 else ""}' for m in range(i, j))
            partes.append(f'<span id="chave">{faixa}<span class="base">{ids}</span>'
                          f'<span id="cheia" aria-hidden="true">{esc(chave_txt)}</span></span>')
        elif i < k < j:
            continue
        else:
            partes.append(f'<span class="pal" id="P{k}">{esc(w)}</span>')
    aviso = f'<div id="aviso">{AVISO_ATIVOS}</div>' if d["ativos"] else ""
    W, H, dur = L["W"], L["H"], T["dur"]
    dados = dict(palavras=pal, entrada=T["entrada"], tc=T["tc"], dc=T["dc"], tp=T["tp"], dur=dur)
    return (projeto.cabeca(d, css)
            + f'<div id="root" data-composition-id="manchete" data-start="0" data-width="{W}" data-height="{H}" '
              f'data-duration="{dur:.3f}" data-formato="{d["formato"]}" data-estilo="{d["estilo"]}">\n'
            + f'  <section id="cena" class="clip cena" data-start="0" data-duration="{dur:.3f}" data-track-index="1">\n'
            + f'    <div id="kicker">{esc(d["kicker"])}</div>\n'
            + f'    <div id="frase"><p>{" ".join(partes)}</p></div>\n'
            + f'    <div id="rodape"><div id="fonte">{esc(d["fonte"])}</div>{aviso}</div>\n'
            + f'    {projeto.marca(d)}\n  </section>\n  {projeto.audio_pouso(sfx, sfx_dur, T["tp"])}\n</div>\n'
            + "<script>\n  const D = " + json.dumps(dados, ensure_ascii=False) + ";\n" + JS.replace("BOIL", "")
            + '</script>\n<script src="assets/tela.js"></script>\n</body>\n</html>\n')


def gerar_projeto(d, destino):
    d = validar(d)
    os.makedirs(destino, exist_ok=True)
    sfx, sfx_dur = projeto.preparar_assets(d, destino, "manchete")
    open(os.path.join(destino, "index.html"), "w").write(montar_html(d, sfx, sfx_dur))
    projeto.escrever_tela(destino, TELA)
    return os.path.join(destino, "index.html")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada")
    ap.add_argument("-o", "--saida", required=True)
    a = ap.parse_args(argv)
    try:
        d = json.load(open(a.entrada))
        caminho = gerar_projeto(d, a.saida)
    except DadosInvalidos as e:
        raise SystemExit("entrada inválida:\n  - " + "\n  - ".join(e.args[0]))
    d = validar(d)
    print(f"ok: {caminho} (manchete, {d['estilo']}, {d['formato']}, {d['duracao']} s; chave {d['chave']!r} "
          f"enche em {d['t_chave']} s, pouso em {tempos(d)['tp']} s)")


if __name__ == "__main__":
    main()
