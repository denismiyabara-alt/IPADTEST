"""Número que vira gráfico: o número grande (ex.: a Selic de hoje) pousa no centro, encolhe, vai para o canto do
gráfico e vira o ÚLTIMO PONTO de uma linha histórica, que então se desenha de trás para a frente. HyperFrames.

Uso:
  python3 biblioteca/numero_linha/gerar.py exemplos/numero-linha-selic-16x9.json -o projetos/selic-numero
  (ou: ./biblioteca/renderizar.sh exemplos/numero-linha-selic-16x9.json)

O que acontece na tela:
  1. kicker e título entram; o número grande (o último valor da série) pousa no centro com um pulso e o único som;
  2. o número encolhe e desliza até o lugar do último ponto do gráfico; os eixos aparecem;
  3. o ponto final acende sob o número, e a linha se desenha da direita para a esquerda, do hoje até o começo;
  4. entra a variação ("+9,25 p.p. desde jan/2020"); a fonte fica no rodapé a peça inteira.

Entrada (JSON) — ver biblioteca/README.md:
  peca: "numero_linha"; estilo; formato; duracao (5 a 10 s); titulo; kicker; fonte ("Fonte: BCB/SGS 432")
  serie: [{"data", "valor"}] em ordem (2 ou mais); linha: "linha" | "degrau"; unidade {prefixo, sufixo, casas}
  rotulo_numero: texto sob o número grande (padrão "em 02/out/2026"); variacao: "pp" | "pct" | null
  classe: "indicador" (padrão) | "ativo" (exige "ativos": true, e a tela mostra o aviso); som
"""
import argparse, datetime as dt, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MOTION = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(MOTION, "comum"))
from estilo import (AVISO_ATIVOS, ESTILOS, DadosInvalidos, checar_ativos, esc, fmt_br, numero_ok,  # noqa: E402
                    texto_valor, validar_base)
import projeto  # noqa: E402

G = projeto.grafico_cotacao()


def validar(d):
    if not isinstance(d, dict):
        raise DadosInvalidos(["a entrada precisa ser um objeto JSON"])
    d = json.loads(json.dumps(d))
    erros = []
    if d.get("peca", "numero_linha") != "numero_linha":
        erros.append(f"'peca' deve ser 'numero_linha', veio {d.get('peca')!r}")
    d["peca"] = "numero_linha"
    validar_base(d, erros)
    d.setdefault("linha", "linha")
    d.setdefault("variacao", None)
    d.setdefault("classe", "indicador")
    if d["linha"] not in ("linha", "degrau"):
        erros.append("'linha' deve ser 'linha' ou 'degrau' (Selic: degrau)")
    if d["variacao"] not in (None, "pp", "pct"):
        erros.append("'variacao' deve ser 'pp', 'pct' ou null")
    serie = d.get("serie")
    if not isinstance(serie, list) or len(serie) < 2:
        erros.append("'serie' precisa de pelo menos 2 pontos")
        serie = []
    ultima = None
    for i, p in enumerate(serie):
        try:
            data = dt.date.fromisoformat(p["data"])
            if not numero_ok(p["valor"]):
                raise ValueError
        except (KeyError, TypeError, ValueError):
            erros.append(f"serie[{i}] inválido: {p!r} (esperado {{'data': 'AAAA-MM-DD', 'valor': número}})")
            continue
        if ultima and data <= ultima:
            erros.append(f"serie[{i}] fora de ordem ou repetido: {p['data']}")
        ultima = data
    if d["variacao"] == "pct" and serie and numero_ok(serie[0].get("valor")) and serie[0]["valor"] <= 0:
        erros.append("variação % precisa de primeiro valor positivo")
    if d["classe"] not in ("indicador", "ativo"):
        erros.append("'classe' deve ser 'indicador' (Selic, IPCA, CDI) ou 'ativo' (ação/FII)")
    if d["classe"] == "ativo" and not d.get("ativos"):
        erros.append("série de ativo exige \"ativos\": true (a tela mostra 'Não é recomendação de investimento.')")
    checar_ativos(d, [d.get("titulo"), d.get("kicker"), d.get("rotulo_numero")], erros)
    if erros:
        raise DadosInvalidos(erros)
    return d


def geometria(d):
    """Pontos na tela (mesma escala e layout do grafico_cotacao, sem o placar)."""
    L = dict(G.layout(d["formato"]))
    pts = G.reduzir(d["serie"])
    t0 = dt.date.fromisoformat(pts[0]["data"]).toordinal()
    t1 = dt.date.fromisoformat(pts[-1]["data"]).toordinal()
    vs = [p["valor"] for p in pts]
    lo, hi, marcas = G.escala_y(min(vs), max(vs))
    X = lambda iso: L["gx0"] + (dt.date.fromisoformat(iso).toordinal() - t0) / max(1, t1 - t0) * (L["gx1"] - L["gx0"])
    Y = lambda v: L["gy1"] - (v - lo) / (hi - lo) * (L["gy1"] - L["gy0"])
    xs = [round(X(p["data"]), 2) for p in pts]
    ys = [round(Y(v), 2) for v in vs]
    linha = G._caminho(xs, ys, d["linha"] == "degrau")
    anos = []
    a0, a1 = dt.date.fromordinal(t0).year, dt.date.fromordinal(t1).year
    if a1 - a0 >= 2:
        anos = [(round(X(f"{a}-01-01"), 1), str(a)) for a in range(a0 + 1, a1 + 1)]
    return dict(L=L, pts=pts, xs=xs, ys=ys, linha=linha, area=linha + f"V{L['gy1']}H{xs[0]}Z",
                marcas=[(round(Y(m), 1), m) for m in marcas], anos=anos)


def final_ancora(Gm):
    """Onde o número pousa (canto inferior direito): na faixa entre o título e o gráfico, no x do último ponto.
    Ali ele não cobre a linha; um traço tracejado liga o número ao ponto."""
    return (round(Gm["xs"][-1] + 12, 2), Gm["L"]["gy0"] - 70)


def tamanhos(d):
    """-> (corpo do número grande, corpo do número no ponto final, centro do número grande)."""
    W, H = G.FORMATOS[d["formato"]]
    txt = texto_valor(d["serie"][-1]["valor"], d["unidade"])
    pad = 96 if d["formato"] == "16:9" else 72
    grande = min(320 if d["formato"] == "16:9" else 280, int((W - 2 * pad) / (0.66 * len(txt))))
    pequeno = 84 if d["formato"] == "16:9" else 110
    return grande, pequeno, (W / 2, H * (0.54 if d["formato"] == "16:9" else 0.5))


def tempos(d):
    dur = float(d["duracao"])
    ts0 = round(min(2.2, dur * .27), 3)
    ts1 = round(ts0 + min(1.1, dur * .14), 3)
    return dict(t_entra=.35, tp=.85, ts0=ts0, ts1=ts1, tl1=round(dur * .85, 3), dur=dur)


CSS = """
  #kicker {{ position:absolute; left:{pad}px; top:{kicker_y}px; font:{mono30}; letter-spacing:.14em; text-transform:uppercase; color:var(--cinza); }}
  #titulo {{ position:absolute; left:{pad}px; top:{titulo_y}px; width:{titulo_w}px; font:{titulo}; }}
  #numero {{ position:absolute; left:0; top:0; font:{numero}; font-variant-numeric:tabular-nums; white-space:nowrap;
             color:var(--destaque); will-change:transform; }}
  #rotulo-numero {{ position:absolute; left:0; width:{W}px; text-align:center; top:{rot_y}px; font:{rotulo}; color:var(--cinza); }}
  #variacao {{ position:absolute; font:{rotulo_var}; color:var(--destaque); white-space:nowrap; }}
  #grafico {{ position:absolute; left:0; top:0; }}
  .grade {{ stroke:var(--grade); stroke-width:2; }}
  .marca {{ stroke:var(--cinza); stroke-width:3; }}
  .eixo {{ font:{eixo}; fill:var(--cinza); }}
  #area {{ fill:var(--tinta); opacity:.06; }}
  #linha {{ fill:none; stroke:var(--tinta); stroke-width:7; stroke-linejoin:round; stroke-linecap:round; }}
  #ponta {{ fill:var(--tinta); }}
  .ligacao {{ stroke:var(--destaque); stroke-width:3; stroke-dasharray:5 6; }}
  #ponto-final {{ fill:var(--destaque); }}
  #anel {{ fill:none; stroke:var(--destaque); stroke-width:5; }}
  #rodape {{ position:absolute; left:{pad}px; right:{pad}px; top:{fonte_y}px; display:flex; flex-direction:{rodape_dir};
             justify-content:space-between; gap:8px 32px; font:{mono_fonte}; }}
  #fonte {{ color:var(--cinza); }}
  #aviso {{ color:var(--tinta); white-space:nowrap; }}
"""

JS = r"""
  const tl = gsap.timeline({ paused: true });
  const numero = document.getElementById('numero'), cortina = document.getElementById('cortina'),
        ponta = document.getElementById('ponta');
  const enc = { p: 0 }, rev = { q: 0 }, pop = { s: 1 };
  function naPosicao(x) {
    const xs = D.xs, n = xs.length;
    if (x >= xs[n - 1]) return D.ys[n - 1];
    if (x <= xs[0]) return D.ys[0];
    let lo = 0, hi = n - 1;
    while (hi - lo > 1) { const m = (lo + hi) >> 1; if (xs[m] <= x) lo = m; else hi = m; }
    if (D.degrau) return D.ys[lo];
    return D.ys[lo] + (D.ys[hi] - D.ys[lo]) * (x - xs[lo]) / Math.max(1e-9, xs[hi] - xs[lo]);
  }
  function desenhar() {
    const p = enc.p;
    const px = D.f0 + (D.f1 - D.f0) * p, x = D.c0[0] + (D.c1[0] - D.c0[0]) * p, y = D.c0[1] + (D.c1[1] - D.c0[1]) * p;
    const ax = 50 + 50 * p, ay = 50 + 50 * p;   // âncora: centro do número → canto inferior direito, junto do ponto
    numero.style.fontSize = (px * pop.s).toFixed(2) + 'px';
    numero.style.transform = `translate(${x.toFixed(2)}px, ${y.toFixed(2)}px) translate(-${ax}%, -${ay}%)`;
    const xr = D.gx1 - (D.gx1 - D.gx0) * rev.q;
    cortina.setAttribute('x', (xr - 8).toFixed(2));
    cortina.setAttribute('width', rev.q > 0 ? (D.gx1 + 40 - xr + 8).toFixed(2) : 0);
    ponta.setAttribute('cx', xr); ponta.setAttribute('cy', naPosicao(xr));
  }
  desenhar();
  tl.eventCallback('onUpdate', desenhar);
  tl.from('#kicker', { opacity: 0, y: 24, duration: .4, ease: 'power2.out' }, 0);
  tl.from('#titulo', { opacity: 0, y: 60, duration: .55, ease: 'back.out(1.4)' }, .12);
  tl.from('#rodape', { opacity: 0, duration: .4 }, .6);
  // 1. o número grande pousa no centro (o único som, na trilha de áudio)
  tl.fromTo('#numero', { opacity: 0 }, { opacity: 1, duration: .2 }, D.t_entra);
  tl.fromTo(pop, { s: .55 }, { s: 1, duration: D.tp - D.t_entra, ease: 'back.out(2)' }, D.t_entra);
  tl.from('#rotulo-numero', { opacity: 0, y: 20, duration: .35 }, D.tp + .05);
  // 2. encolhe e vai para o lugar do último ponto; os eixos entram
  tl.to('#rotulo-numero', { opacity: 0, duration: .3 }, D.ts0);
  tl.to(enc, { p: 1, duration: D.ts1 - D.ts0, ease: 'power3.inOut' }, D.ts0);
  tl.from('#eixos', { opacity: 0, duration: .5 }, D.ts0 + .3);
  tl.set(['#ponto-final', '#ponta', '#ligacao'], { opacity: 0 }, 0);
  // 3. vira o último ponto, e a linha se desenha para trás, do hoje até o começo
  tl.set(['#ponto-final', '#ponta', '#ligacao'], { opacity: 1 }, D.ts1);
  tl.fromTo('#anel', { opacity: .9, scale: 1, transformOrigin: 'center' },
            { opacity: 0, scale: 3.2, duration: .7, ease: 'power2.out', immediateRender: false }, D.ts1);
  tl.to(rev, { q: 1, duration: D.tl1 - D.ts1, ease: 'power1.inOut' }, D.ts1);
  tl.set('#ponta', { opacity: 0 }, D.tl1);
  tl.set('#variacao', { opacity: 0 }, 0);
  tl.fromTo('#variacao', { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .4, immediateRender: false }, D.tl1 + .1);
  BOIL
  tl.set({}, {}, D.dur);
  window.__timelines = window.__timelines || {};
  window.__timelines["numero_linha"] = tl;
"""

TELA = r"""  window.__tela = () => {
    const op = el => { let o = 1; for (let n = el; n && n.nodeType === 1; n = n.parentElement) o *= +getComputedStyle(n).opacity; return o; };
    const r = numero.getBoundingClientRect();
    const pf = document.getElementById('ponto-final');
    const txt = id => { const e = document.getElementById(id); return e ? e.textContent : null; };
    return { numero: numero.textContent, corpo: parseFloat(numero.style.fontSize), cor_numero: getComputedStyle(numero).color,
             caixa: { x0: r.left, x1: r.right, y0: r.top, y1: r.bottom, cx: (r.left + r.right) / 2, cy: (r.top + r.bottom) / 2 },
             ponto: { cx: +pf.getAttribute('cx'), cy: +pf.getAttribute('cy'), visivel: op(pf) > .9 },
             revelado_desde: +cortina.getAttribute('x') + 8, gx0: D.gx0, gx1: D.gx1,
             variacao: op(document.getElementById('variacao')) > .9 ? txt('variacao') : '',
             fonte: txt('fonte'), titulo: txt('titulo'), aviso: document.getElementById('aviso') ? txt('aviso') : '',
             W: innerWidth, H: innerHeight };
  };
"""


def montar_html(d, sfx=None, sfx_dur=1.0):
    d = validar(d)
    e = ESTILOS[d["estilo"]]
    Gm = geometria(d)
    L, xs, ys = Gm["L"], Gm["xs"], Gm["ys"]
    W, H = L["W"], L["H"]
    T = tempos(d)
    un = d["unidade"]
    f0, f1, c0 = tamanhos(d)
    vert = d["formato"] == "9:16"
    c1 = final_ancora(Gm)             # canto inferior direito do número: acima do gráfico, no x do último ponto
    tp = lambda papel, px: projeto.tipo(d["estilo"], papel, px)
    css = CSS.format(pad=L["pad"], kicker_y=L["kicker_y"], titulo_y=L["titulo_y"], titulo_w=W - 2 * L["pad"],
                     mono30=tp("mono", 30), titulo=tp("titulo", 76 if not vert else 84), numero=tp("numero", f0), W=W,
                     rot_y=round(c0[1] + f0 * .62), rotulo=tp("rotulo", 40), rotulo_var=tp("rotulo", 34),
                     eixo=tp("mono", L["eixo_px"]), fonte_y=L["fonte_y"], rodape_dir="column" if vert else "row",
                     mono_fonte=tp("mono", 26))
    casas_eixo = 0 if all(abs(m - round(m)) < 1e-9 for _, m in Gm["marcas"]) else min(2, un["casas"])
    grade = "".join(
        f'<line x1="{L["gx0"]}" x2="{L["gx1"]}" y1="{y}" y2="{y}" class="grade"/>'
        f'<text x="{L["gx0"] - 22}" y="{y + 10}" class="eixo" text-anchor="end">{esc(un["prefixo"].strip())}'
        f'{fmt_br(m, casas_eixo)}{esc(un["sufixo"])}</text>' for y, m in Gm["marcas"])
    eixo_x = "".join(f'<line x1="{x}" x2="{x}" y1="{L["gy1"]}" y2="{L["gy1"] + 14}" class="marca"/>'
                     f'<text x="{x}" y="{L["gy1"] + 52}" class="eixo" text-anchor="middle">{a}</text>'
                     for x, a in Gm["anos"] if L["gx0"] + 60 < x < L["gx1"] - 20)
    if not Gm["anos"]:
        eixo_x = (f'<text x="{L["gx0"]}" y="{L["gy1"] + 52}" class="eixo">{G.data_br(Gm["pts"][0]["data"], False)}</text>'
                  f'<text x="{L["gx1"]}" y="{L["gy1"] + 52}" class="eixo" text-anchor="end">{G.data_br(Gm["pts"][-1]["data"], False)}</text>')
    final_txt = texto_valor(d["serie"][-1]["valor"], un)
    rotulo_numero = d.get("rotulo_numero") or f"em {G.data_br(d['serie'][-1]['data'])}"
    variacao = G.texto_variacao(d) if d["variacao"] else ""
    var_y = L["gy0"] - 58             # sob o número final, ainda acima da área do gráfico
    aviso = f'<div id="aviso">{AVISO_ATIVOS}</div>' if d.get("ativos") else ""
    dados = dict(xs=xs, ys=ys, degrau=d["linha"] == "degrau", gx0=L["gx0"], gx1=L["gx1"], f0=f0, f1=f1,
                 c0=[round(c0[0], 2), round(c0[1], 2)], c1=[round(c1[0], 2), round(c1[1], 2)], **T)
    svg = (f'<svg id="grafico" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<defs><clipPath id="revela"><rect id="cortina" x="{L["gx1"]}" y="0" width="0" height="{H}"/></clipPath></defs>'
           f'<g id="eixos">{grade}{eixo_x}</g>'
           f'<g clip-path="url(#revela)"><path id="area" d="{Gm["area"]}"/><path id="linha" d="{Gm["linha"]}"/></g>'
           + (f'<line id="ligacao" x1="{xs[-1]}" x2="{xs[-1]}" y1="{L["gy0"] - 12}" y2="{ys[-1] - 20}" class="ligacao"/>'
              if ys[-1] - 20 > L["gy0"] - 12 else '')
           + f'<circle id="ponta" cx="{xs[-1]}" cy="{ys[-1]}" r="12"/>'
           f'<circle id="anel" cx="{xs[-1]}" cy="{ys[-1]}" r="16" opacity="0"/>'
           f'<circle id="ponto-final" cx="{xs[-1]}" cy="{ys[-1]}" r="15"/></svg>')
    dur = T["dur"]
    return (projeto.cabeca(d, css)
            + f'<div id="root" data-composition-id="numero_linha" data-start="0" data-width="{W}" data-height="{H}" '
              f'data-duration="{dur:.3f}" data-formato="{d["formato"]}" data-estilo="{d["estilo"]}">\n'
            + f'  <section id="cena" class="clip cena" data-start="0" data-duration="{dur:.3f}" data-track-index="1">\n'
            + f'    <div id="kicker">{esc(d["kicker"])}</div>\n    <div id="titulo">{esc(d["titulo"])}</div>\n'
            + f'    {svg}\n'
            + f'    <div id="numero">{esc(final_txt)}</div>\n'
            + f'    <div id="rotulo-numero">{esc(rotulo_numero)}</div>\n'
            + f'    <div id="variacao" style="right:{W - c1[0]:.0f}px; top:{var_y:.0f}px">{esc(variacao)}</div>\n'
            + f'    <div id="rodape"><div id="fonte">{esc(d["fonte"])}</div>{aviso}</div>\n'
            + f'    {projeto.marca(d)}\n  </section>\n  {projeto.audio_pouso(sfx, sfx_dur, T["tp"])}\n</div>\n'
            + "<script>\n  const D = " + json.dumps(dados, ensure_ascii=False) + ";\n" + JS.replace("BOIL", "")
            + '</script>\n<script src="assets/tela.js"></script>\n</body>\n</html>\n')


def gerar_projeto(d, destino):
    d = validar(d)
    os.makedirs(destino, exist_ok=True)
    sfx, sfx_dur = projeto.preparar_assets(d, destino, "numero_linha")
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
    print(f"ok: {caminho} (numero_linha, {d['formato']}, {d['duracao']} s, {len(d['serie'])} pontos, "
          f"número = {texto_valor(d['serie'][-1]['valor'], d['unidade'])})")


if __name__ == "__main__":
    main()
