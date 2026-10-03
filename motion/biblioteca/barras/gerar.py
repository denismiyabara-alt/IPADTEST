"""Barras que crescem e se reordenam (ranking), em HyperFrames, a partir de um JSON de dado real.

Uso:
  python3 biblioteca/barras/gerar.py exemplos/barras-dy-caixa-16x9.json -o projetos/barras-dy
  cd projetos/barras-dy && npx hyperframes render -o ../../renders/barras-dy.mp4
  (ou: ./biblioteca/renderizar.sh exemplos/barras-dy-caixa-16x9.json)

O que acontece na tela:
  1. título e kicker entram; as barras crescem a partir do zero, de cima para baixo, com o valor contando junto;
  2. se houver dois momentos (cada item com "antes"), as barras crescem até o "antes", param um instante com o
     selo do 1º momento, e depois os valores vão para o "depois" enquanto as barras trocam de lugar;
  3. pouso: a barra-chave ganha a cor de destaque, o número grande pousa com um pulso e um único som grave;
  4. entra a variação da barra-chave (posição ou %), e a fonte, o critério e o aviso ficam na tela.

Entrada (JSON) — ver biblioteca/README.md:
  peca: "barras"; estilo: "iec" | "fazaconta"; formato: "16:9" | "9:16"; duracao: 5 a 10 s
  titulo, kicker, fonte ("Fonte: ..."), unidade {prefixo, sufixo, casas}
  itens: [{"rotulo", "valor", "antes"?, "detalhe"?}], 2 a 10
  destaque: rótulo da barra-chave; ordem: "desc" | "asc"; momentos: ["ago/2025", "ago/2026"] (com "antes")
  variacao: null | "posicao" | "pct"; ativos: true para ranking de FII/ação (exige "criterio")
  rotulo_placar, criterio, som
"""
import argparse, json, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MOTION = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(MOTION, "comum"))
from estilo import (AVISO_ATIVOS, ESTILOS, FORMATOS, DadosInvalidos, esc, fmt_br, misturar, numero_ok,  # noqa: E402
                    texto_valor, validar_base)
import projeto  # noqa: E402

MAX_ITENS = 10
TICKER = re.compile(r"^[A-Z]{4}\d{1,2}$")


# ---------------------------------------------------------------- dados
def validar(d):
    """Levanta DadosInvalidos com todos os problemas de uma vez. Devolve a entrada com padrões."""
    if not isinstance(d, dict):
        raise DadosInvalidos(["a entrada precisa ser um objeto JSON"])
    d = json.loads(json.dumps(d))
    erros = []
    if d.get("peca", "barras") != "barras":
        erros.append(f"'peca' deve ser 'barras', veio {d.get('peca')!r}")
    d["peca"] = "barras"
    validar_base(d, erros)
    d.setdefault("ordem", "desc")
    d.setdefault("momentos", None)
    d.setdefault("ativos", False)
    d.setdefault("criterio", "")
    itens = d.get("itens")
    if not isinstance(itens, list) or not 2 <= len(itens) <= MAX_ITENS:
        erros.append(f"'itens' precisa de 2 a {MAX_ITENS} barras (mais que isso não se lê no celular)")
        itens = []
    rotulos = []
    for i, it in enumerate(itens):
        if not isinstance(it, dict) or not isinstance(it.get("rotulo"), str) or not it["rotulo"].strip():
            erros.append(f"itens[{i}] sem 'rotulo'")
            continue
        if it["rotulo"] in rotulos:
            erros.append(f"itens[{i}]: rótulo repetido {it['rotulo']!r}")
        rotulos.append(it["rotulo"])
        for campo in ("valor", "antes"):
            if campo == "antes" and campo not in it:
                continue
            v = it.get(campo)
            if not numero_ok(v):
                erros.append(f"itens[{i}].{campo} inválido: {v!r} (esperado número)")
            elif v < 0:
                erros.append(f"itens[{i}].{campo} negativo: a barra cresce a partir do zero")
    com_antes = [("antes" in it) for it in itens if isinstance(it, dict)]
    dois = any(com_antes)
    if dois and not all(com_antes):
        erros.append("se um item tem 'antes', todos precisam ter (dois momentos: antes → depois)")
    if dois:
        m = d["momentos"]
        if not (isinstance(m, list) and len(m) == 2 and all(isinstance(x, str) and x.strip() for x in m)):
            erros.append("com 'antes', 'momentos' é obrigatório: [\"rótulo do antes\", \"rótulo do depois\"]")
    elif d["momentos"] is not None:
        erros.append("'momentos' só vale com 'antes' em cada item")
    d.setdefault("variacao", "posicao" if dois else None)
    if d["variacao"] not in (None, "posicao", "pct"):
        erros.append("'variacao' deve ser 'posicao', 'pct' ou null")
    elif d["variacao"] and not dois:
        erros.append("'variacao' precisa de dois momentos ('antes' em cada item)")
    if d["ordem"] not in ("desc", "asc"):
        erros.append("'ordem' deve ser 'desc' (maior em cima) ou 'asc'")
    if d.get("destaque") not in rotulos:
        erros.append(f"'destaque' deve ser o rótulo de uma barra (a barra-chave), veio {d.get('destaque')!r}")
    if d["variacao"] == "pct" and dois:
        k = rotulos.index(d["destaque"]) if d.get("destaque") in rotulos else None
        if k is not None and not (numero_ok(itens[k].get("antes")) and itens[k]["antes"] > 0):
            erros.append("variação % precisa de 'antes' positivo na barra-chave")
    # compliance: ranking de ativos mostra o critério e o aviso
    parece_ativo = [r for r in rotulos if TICKER.match(r)]
    if parece_ativo and not d["ativos"]:
        erros.append(f"parece ranking de ativos ({', '.join(parece_ativo[:3])}): use \"ativos\": true e informe o "
                     "'criterio' (a tela mostra o critério e 'Não é recomendação de investimento')")
    if d["ativos"]:
        if not isinstance(d["criterio"], str) or not d["criterio"].startswith("Critério:"):
            erros.append("ranking de ativos exige 'criterio' começando com 'Critério:' (como a lista foi montada)")
    if erros:
        raise DadosInvalidos(erros)
    return d


def ranking(valores, ordem):
    """Índices dos itens na ordem do ranking (empate: ordem da entrada)."""
    sinal = -1 if ordem == "desc" else 1
    return sorted(range(len(valores)), key=lambda k: (sinal * valores[k], k))


def posicoes(d):
    """-> (pos_antes, pos_depois): posição (0 = topo) de cada item em cada momento."""
    itens = d["itens"]
    depois = ranking([it["valor"] for it in itens], d["ordem"])
    pd = [0] * len(itens)
    for p, k in enumerate(depois):
        pd[k] = p
    if d["momentos"]:
        antes = ranking([it["antes"] for it in itens], d["ordem"])
        pa = [0] * len(itens)
        for p, k in enumerate(antes):
            pa[k] = p
        return pa, pd
    return pd, pd


def texto_variacao(d):
    if not d["variacao"]:
        return ""
    k = [it["rotulo"] for it in d["itens"]].index(d["destaque"])
    pa, pd = posicoes(d)
    if d["variacao"] == "posicao":
        a, b = pa[k] + 1, pd[k] + 1
        if b < a:
            return f"subiu do {a}º para o {b}º lugar"
        if b > a:
            return f"caiu do {a}º para o {b}º lugar"
        return f"manteve o {b}º lugar"
    it = d["itens"][k]
    x = (it["valor"] / it["antes"] - 1) * 100
    return f"{'+' if x >= 0 else '−'}{fmt_br(abs(x), 1)}% desde {d['momentos'][0]}"


def ordem_final(d):
    """Rótulos de cima para baixo no fim da animação (o que o teste espera ver na tela)."""
    return [d["itens"][k]["rotulo"] for k in ranking([it["valor"] for it in d["itens"]], d["ordem"])]


# ---------------------------------------------------------------- layout
def layout(d):
    W, H = FORMATOS[d["formato"]]
    n = len(d["itens"])
    un = d["unidade"]
    vert = d["formato"] == "9:16"
    if not vert:
        L = dict(W=W, H=H, pad=96, kicker_y=92, titulo_y=140, titulo_px=64, titulo_w=W - 2 * 96 - 640,
                 placar_x=96, placar_lado="right", placar_y=78, num_px=130, y0=340, y1=880 if d["criterio"] else 930,
                 criterio_y=H - 140, fonte_y=H - 64, aviso_y=H - 64, mono_px=26)
    else:
        L = dict(W=W, H=H, pad=72, kicker_y=200, titulo_y=246, titulo_px=84, titulo_w=W - 2 * 72,
                 placar_x=72, placar_lado="left", placar_y=460, num_px=150, y0=830, y1=1430,
                 criterio_y=1462, fonte_y=1548, aviso_y=1600, mono_px=24)
    rowh = min(112 if not vert else 96, (L["y1"] - L["y0"]) / n)
    L["rowh"] = rowh
    L["barra_h"] = round(rowh * .62)
    L["rot_px"] = round(min(46 if not vert else 42, rowh * .5))
    L["val_px"] = round(min(64 if not vert else 56, rowh * .7))
    L["rank_px"] = round(L["rot_px"] * .7)
    maxrot = max(len(it["rotulo"]) for it in d["itens"])
    L["rank_w"] = round(L["rank_px"] * 2.2)
    L["rot_w"] = round(min(max(maxrot * L["rot_px"] * .62, 140), 520 if not vert else 330))
    L["bx0"] = L["pad"] + L["rank_w"] + L["rot_w"] + 28
    vmax_txt = max((texto_valor(v, un) for it in d["itens"] for v in (it["valor"], it.get("antes", 0))), key=len)
    L["val_w"] = round(len(vmax_txt) * L["val_px"] * .56 + 28)
    L["bw"] = W - L["pad"] - L["bx0"] - L["val_w"]
    return L


# ---------------------------------------------------------------- página
CSS = """
  #kicker {{ position:absolute; left:{pad}px; top:{kicker_y}px; font:{mono30}; letter-spacing:.12em; text-transform:uppercase; color:var(--cinza); }}
  #titulo {{ position:absolute; left:{pad}px; top:{titulo_y}px; width:{titulo_w}px; font:{titulo}; letter-spacing:{titulo_espaco}; }}
  #placar {{ position:absolute; {placar_lado}:{placar_x}px; top:{placar_y}px; text-align:{placar_lado}; }}
  #numero {{ font:{numero}; font-variant-numeric:tabular-nums; display:inline-block; transform-origin:{placar_lado} center; white-space:nowrap; }}
  #rotulo-placar {{ font:{mono_placar}; letter-spacing:.08em; text-transform:uppercase; color:var(--cinza); margin-top:10px; }}
  #momento {{ display:inline-block; margin-top:12px; font:{mono_placar}; letter-spacing:.06em; color:var(--tinta);
              border:3px solid var(--tinta); border-radius:8px; padding:4px 14px; }}
  #variacao {{ display:inline-block; margin-top:12px; margin-{margem_var}:12px; font:{rotulo_var}; color:var(--destaque);
               border:4px solid var(--destaque); border-radius:10px; padding:4px 16px; }}
  .rank {{ position:absolute; left:{pad}px; width:{rank_w}px; font:{mono_rank}; color:var(--cinza); line-height:{rowh}px; }}
  .linha {{ position:absolute; left:0; top:0; width:{W}px; height:{rowh}px; will-change:transform; }}
  .rot {{ position:absolute; left:{rot_x}px; width:{rot_w}px; top:0; height:{rowh}px; display:flex; flex-direction:column;
          justify-content:center; align-items:flex-end; text-align:right; font:{rotulo}; white-space:nowrap; }}
  .rot .det {{ font:{mono_det}; color:var(--cinza); margin-top:2px; }}
  .barra {{ position:absolute; left:{bx0}px; top:{barra_top}px; height:{barra_h}px; width:0; background:var(--cinza-barra); border:5px solid var(--tinta); {boil} }}
  .barra.chave {{ background:var(--tinta); }}
  .val {{ position:absolute; left:{bx0}px; top:0; height:{rowh}px; line-height:{rowh}px; font:{numero_val};
          font-variant-numeric:tabular-nums; white-space:nowrap; }}
  #rodape {{ position:absolute; left:{pad}px; right:{pad}px; }}
  #criterio {{ position:absolute; left:{pad}px; top:{criterio_y}px; width:{criterio_w}px; font:{mono_crit}; color:var(--cinza); }}
  #fonte {{ position:absolute; left:{pad}px; top:{fonte_y}px; font:{mono_fonte}; color:var(--cinza); background:var(--papel);
            padding:4px 10px; margin-left:-10px; }}
  #aviso {{ position:absolute; {aviso_pos}; top:{aviso_y}px; font:{rotulo_aviso}; color:var(--tinta); }}
"""

JS = r"""
  const tl = gsap.timeline({ paused: true });
  const linhas = D.itens.map((it, k) => ({ el: document.getElementById('L' + k), barra: document.getElementById('B' + k),
                                           val: document.getElementById('V' + k) }));
  const numero = document.getElementById('numero'), momento = document.getElementById('momento');
  const cresce = D.itens.map(() => ({ p: 0 }));   // fase 1: cada barra de 0 até o 1º valor
  const troca = { p: 0 };                           // fase 2: do antes para o depois, trocando de lugar
  const slotY = i => D.y0 + i * D.rowh;
  function valorEm(k) {
    const it = D.itens[k];
    if (troca.p > 0) return troca.p >= 1 ? it.valor : it.base + (it.valor - it.base) * troca.p;
    return cresce[k].p >= 1 ? it.base : it.base * cresce[k].p;
  }
  function desenhar() {
    D.itens.forEach((it, k) => {
      const v = valorEm(k), w = D.vmax > 0 ? v / D.vmax * D.bw : 0;
      const y = slotY(D.pa[k]) + (slotY(D.pd[k]) - slotY(D.pa[k])) * troca.p;
      linhas[k].el.style.transform = `translateY(${y.toFixed(2)}px)`;
      linhas[k].el.style.zIndex = k === D.chave ? 3 : (D.pd[k] < D.pa[k] ? 2 : 1);   // quem sobe passa por cima
      linhas[k].barra.style.width = w.toFixed(2) + 'px';
      linhas[k].val.style.left = (D.bx0 + w + 18).toFixed(2) + 'px';
      linhas[k].val.textContent = D.pre + fmtBR(v, D.casas) + D.suf;
      if (k === D.chave) numero.textContent = D.pre + fmtBR(v, D.casas) + D.suf;
    });
    if (momento) momento.textContent = D.momentos[tl.time() >= D.t2 - .02 ? 1 : 0];
  }
  desenhar();
  tl.eventCallback('onUpdate', desenhar);

  // 1. entrada do texto
  tl.from('#kicker', { opacity: 0, y: 24, duration: .4, ease: 'power2.out' }, 0);
  tl.from('#titulo', { opacity: 0, y: 60, duration: .55, ease: 'back.out(1.4)' }, .12);
  tl.from('#placar', { opacity: 0, y: 40, duration: .5, ease: 'power2.out' }, .35);
  tl.from('.rot, .rank', { opacity: 0, x: -30, duration: .4, stagger: .04, ease: 'power2.out' }, .4);
  tl.from(['#fonte', '#criterio', '#aviso'], { opacity: 0, duration: .4 }, .6);
  tl.set('.val', { opacity: 0 }, 0);
  tl.set('#variacao', { opacity: 0 }, 0);
  // 2. as barras crescem do zero, de cima para baixo (na ordem do 1º momento), com o valor contando junto
  D.ordemA.forEach((k, i) => {
    tl.set('#V' + k, { opacity: 1 }, D.t0 + i * D.s);
    tl.to(cresce[k], { p: 1, duration: D.g, ease: 'power2.out' }, D.t0 + i * D.s);
  });
  // 3. dois momentos: o selo troca e as barras vão para o "depois", trocando de lugar
  if (D.dois) {
    tl.to('#momento', { opacity: 0, y: -14, duration: .18, ease: 'power1.in' }, D.t2 - .2);
    tl.fromTo('#momento', { opacity: 0, y: 14 }, { opacity: 1, y: 0, duration: .25, ease: 'power2.out', immediateRender: false }, D.t2);
    tl.to(troca, { p: 1, duration: D.tp - D.t2, ease: 'power2.inOut' }, D.t2);
  }
  // 4. pouso: a barra-chave ganha a cor, o número pousa com um pulso (e o único som, na trilha de áudio)
  tl.to('#B' + D.chave, { backgroundColor: D.cor_destaque, duration: .15 }, D.tp);
  tl.to(['#V' + D.chave, '#numero', '#R' + D.chave], { color: D.cor_destaque, duration: .15 }, D.tp);
  tl.fromTo('#numero', { scale: 1 }, { scale: 1.12, duration: .14, ease: 'power2.out', yoyo: true, repeat: 1, immediateRender: false }, D.tp);
  tl.fromTo('#B' + D.chave, { scaleY: 1 }, { scaleY: 1.25, duration: .14, ease: 'power2.out', yoyo: true, repeat: 1, immediateRender: false }, D.tp);
  if (D.variacao) tl.fromTo('#variacao', { opacity: 0, y: 16 }, { opacity: 1, y: 0, duration: .4, ease: 'power2.out', immediateRender: false }, D.tp + .35);
  BOIL
  tl.set({}, {}, D.dur);
  window.__timelines = window.__timelines || {};
  window.__timelines["barras"] = tl;

"""


# leitor da tela, em assets/tela.js (fora da timeline: só o teste chama; não roda no render)
TELA = r"""  window.__tela = () => {
    const cor = el => getComputedStyle(el).backgroundColor;
    const op = el => +getComputedStyle(el).opacity;
    const barras = D.itens.map((it, k) => {
      const r = linhas[k].el.getBoundingClientRect();
      return { rotulo: it.rotulo, valor: linhas[k].val.textContent, y: r.top,
               largura: parseFloat(linhas[k].barra.style.width), cor: cor(linhas[k].barra),
               visivel: op(linhas[k].val) > .5 };
    }).sort((a, b) => a.y - b.y);
    const txt = id => { const e = document.getElementById(id); return e ? e.textContent : null; };
    const vis = id => { const e = document.getElementById(id); return e ? op(e) > .5 : false; };
    return { barras, numero: txt('numero'), cor_numero: getComputedStyle(numero).color, momento: txt('momento'),
             variacao: vis('variacao') ? txt('variacao') : '', titulo: txt('titulo'), fonte: txt('fonte'),
             criterio: txt('criterio'), aviso: vis('aviso') ? txt('aviso') : '', bw: D.bw };
  };
"""


def tempos(d):
    dur = float(d["duracao"])
    n = len(d["itens"])
    t0 = 0.8
    if d["momentos"]:
        g = 1.0
        fim1 = dur * .40
        s = min(.3, max(.06, (fim1 - t0 - g) / max(1, n - 1)))
        fim1 = t0 + (n - 1) * s + g
        t2 = fim1 + .55
        tp = t2 + 1.5
    else:
        g = 1.3
        s = min(.3, max(.06, (dur * .55 - t0 - g) / max(1, n - 1)))
        t2 = None
        tp = t0 + (n - 1) * s + g
    return dict(t0=t0, g=g, s=round(s, 4), t2=None if t2 is None else round(t2, 3), tp=round(tp, 3), dur=dur)


def montar_html(d, sfx=None, sfx_dur=1.0):
    d = validar(d)
    e = ESTILOS[d["estilo"]]
    L = layout(d)
    T = tempos(d)
    un = d["unidade"]
    itens = d["itens"]
    pa, pd = posicoes(d)
    chave = [it["rotulo"] for it in itens].index(d["destaque"])
    vmax = max(max(it["valor"], it.get("antes", 0)) for it in itens)
    ordemA = sorted(range(len(itens)), key=lambda k: pa[k])
    tp = lambda papel, px: projeto.tipo(d["estilo"], papel, px)
    vert = d["formato"] == "9:16"
    css = CSS.format(
        **{k: L[k] for k in ("pad", "kicker_y", "titulo_y", "titulo_w", "placar_x", "placar_lado", "placar_y", "rowh",
                             "rank_w", "rot_w", "bx0", "barra_h", "criterio_y", "fonte_y", "aviso_y", "W")},
        mono30=tp("mono", 30), titulo=tp("titulo", L["titulo_px"]), titulo_espaco=e["titulo_espaco"],
        numero=tp("numero", L["num_px"]), mono_placar=tp("mono", 28), rotulo_var=tp("rotulo", 34),
        margem_var="left" if L["placar_lado"] == "right" else "right",
        mono_rank=tp("mono", L["rank_px"]), rot_x=L["pad"] + L["rank_w"], rotulo=tp("rotulo", L["rot_px"]),
        mono_det=tp("mono", max(18, round(L["rot_px"] * .5))), barra_top=round((L["rowh"] - L["barra_h"]) / 2),
        boil="filter:url(#boil);" if e["boil"] else "",
        numero_val=tp("numero", L["val_px"]), criterio_w=L["W"] - 2 * L["pad"], mono_crit=tp("mono", 24 if not vert else 22),
        mono_fonte=tp("mono", 28 if not vert else 26), rotulo_aviso=tp("rotulo", 28 if not vert else 30),
        aviso_pos=f"right:{L['pad']}px" if not vert else f"left:{L['pad']}px",
    ).replace("var(--cinza-barra)", misturar(e["cores"]["tinta"], e["cores"]["grade"], .55))
    if e["marca"] and d["ativos"] and not vert:   # o aviso sobe para não bater na marca-d'água
        css += f"\n  #aviso {{ top:{L['H'] - 120}px; }}"
    ranks = "".join(f'<div class="rank" style="top:{L["y0"] + i * L["rowh"]:.2f}px">{i + 1}º</div>' for i in range(len(itens)))
    linhas = ""
    for k, it in enumerate(itens):
        det = f'<span class="det">{esc(it["detalhe"])}</span>' if it.get("detalhe") and L["rowh"] >= 80 else ""
        linhas += (f'<div class="linha" id="L{k}"><div class="rot" id="R{k}">{esc(it["rotulo"])}{det}</div>'
                   f'<div class="barra{" chave" if k == chave else ""}" id="B{k}"></div>'
                   f'<div class="val" id="V{k}">{esc(texto_valor(0, un))}</div></div>')
    rot_placar = d.get("rotulo_placar") or d["destaque"]
    momento = f'<div><span id="momento">{esc(d["momentos"][0])}</span></div>' if d["momentos"] else ""
    variacao = texto_variacao(d)
    var_html = f'<div><span id="variacao">{esc(variacao)}</span></div>' if variacao else ""
    criterio = f'<div id="criterio">{esc(d["criterio"])}</div>' if d["criterio"] else ""
    aviso = f'<div id="aviso">{AVISO_ATIVOS}</div>' if d["ativos"] else ""
    W, H, dur = L["W"], L["H"], T["dur"]
    dados = dict(itens=[dict(rotulo=it["rotulo"], valor=it["valor"], base=it.get("antes", it["valor"])) for it in itens],
                 pa=pa, pd=pd, ordemA=ordemA, chave=chave, vmax=vmax, bw=L["bw"], bx0=L["bx0"], y0=L["y0"],
                 rowh=L["rowh"], pre=un["prefixo"], suf=un["sufixo"], casas=un["casas"], dois=bool(d["momentos"]),
                 momentos=d["momentos"] or [], variacao=bool(variacao), cor_destaque=e["cores"]["destaque"],
                 t0=T["t0"], g=T["g"], s=T["s"], t2=T["t2"], tp=T["tp"], dur=dur)
    js = JS.replace("BOIL", projeto.js_boil(d))
    return (projeto.cabeca(d, css)
            + f'<div id="root" data-composition-id="barras" data-start="0" data-width="{W}" data-height="{H}" '
              f'data-duration="{dur:.3f}" data-formato="{d["formato"]}" data-estilo="{d["estilo"]}">\n'
            + projeto.filtro_boil(d)
            + f'  <section id="cena" class="clip cena" data-start="0" data-duration="{dur:.3f}" data-track-index="1">\n'
            + f'    <div id="kicker">{esc(d["kicker"])}</div>\n    <div id="titulo">{esc(d["titulo"])}</div>\n'
            + f'    <div id="placar"><div><span id="numero">{esc(texto_valor(0, un))}</span></div>'
              f'<div id="rotulo-placar">{esc(rot_placar)}</div>{momento}{var_html}</div>\n'
            + f'    {ranks}\n    {linhas}\n    {criterio}\n    <div id="fonte">{esc(d["fonte"])}</div>\n    {aviso}\n'
            + f'    {projeto.marca(d)}\n  </section>\n  {projeto.audio_pouso(sfx, sfx_dur, T["tp"])}\n</div>\n'
            + "<script>\n  const D = " + json.dumps(dados, ensure_ascii=False) + ";\n" + projeto.JS_FMT + js
            + '</script>\n<script src="assets/tela.js"></script>\n</body>\n</html>\n')


def gerar_projeto(d, destino):
    d = validar(d)
    os.makedirs(destino, exist_ok=True)
    sfx, sfx_dur = projeto.preparar_assets(d, destino, "barras")
    open(os.path.join(destino, "index.html"), "w").write(montar_html(d, sfx, sfx_dur))
    open(os.path.join(destino, "assets", "tela.js"), "w").write("// lido pelo teste (comum/quadro.mjs)\n(() => {\n" + TELA + "})();\n")
    return os.path.join(destino, "index.html")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada", help="JSON de entrada (ver biblioteca/README.md)")
    ap.add_argument("-o", "--saida", required=True, help="pasta do projeto HyperFrames a criar")
    a = ap.parse_args(argv)
    try:
        d = json.load(open(a.entrada))
        caminho = gerar_projeto(d, a.saida)
    except DadosInvalidos as e:
        raise SystemExit("entrada inválida:\n  - " + "\n  - ".join(e.args[0]))
    d = validar(d)
    print(f"ok: {caminho} (barras, {d['estilo']}, {d['formato']}, {d['duracao']} s, {len(d['itens'])} itens, "
          f"ordem final: {', '.join(ordem_final(d))}; pouso em {tempos(d)['tp']} s)")


if __name__ == "__main__":
    main()
