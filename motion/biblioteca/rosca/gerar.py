"""Rosca que se divide em fatias (composição), em HyperFrames, a partir de um JSON de dado real.

Uso:
  python3 biblioteca/rosca/gerar.py exemplos/rosca-megasena-9x16.json -o projetos/rosca
  cd projetos/rosca && npx hyperframes render -o ../../renders/rosca.mp4
  (ou: ./biblioteca/renderizar.sh exemplos/rosca-megasena-9x16.json)

O que acontece na tela:
  1. título e kicker entram; o anel vazio aparece, com o total no centro ("R$ 6,00 · a sua aposta");
  2. as fatias se desenham UMA POR VEZ, no sentido horário a partir do topo, e a linha da legenda de cada uma
     entra junto, com o percentual contando de 0 até o valor;
  3. pouso: a fatia-chave engrossa e ganha a cor de destaque; o centro pousa na parte dela ("R$ 2,63 · viram
     prêmio") com um pulso e um único som grave;
  4. a soma das fatias ("soma: 100,00%") fecha a legenda.

Os percentuais têm de somar 100%: se não somarem (no número de casas mostrado), validar() levanta
DadosInvalidos e nada é gerado.

Entrada (JSON) — ver biblioteca/README.md:
  peca: "rosca"; estilo: "iec" | "fazaconta"; formato: "16:9" | "9:16"; duracao: 5 a 10 s
  titulo, kicker, fonte ("Fonte: ..."), casas (casas do percentual, padrão 1)
  fatias: [{"rotulo", "pct"}], 2 a 10, na ordem do desenho; destaque: rótulo da fatia-chave
  centro (opcional): {"valor", "unidade", "rotulo", "rotulo_final"}: o total; no pouso, vira a parte da fatia-chave
  ativos / criterio: como nas barras (composição de carteira de FII/ação exige critério e aviso)
  som
"""
import argparse, json, math, os, re, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MOTION = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(MOTION, "comum"))
from estilo import (AVISO_ATIVOS, ESTILOS, FORMATOS, DadosInvalidos, esc, fmt_br, numero_ok, rampa_cinza,  # noqa: E402
                    texto_valor, validar_base)
import projeto  # noqa: E402

MAX_FATIAS = 10
TICKER = re.compile(r"^[A-Z]{4}\d{1,2}$")
FOLGA = 0.28   # espaço entre fatias, em pontos percentuais do anel


def soma_pct(fatias, casas):
    """Soma dos percentuais como aparecem na tela (arredondados), em inteiros de 10^-casas: sem erro de float."""
    return sum(round(f["pct"] * 10 ** casas) for f in fatias)


def validar(d):
    """Levanta DadosInvalidos com todos os problemas de uma vez. Devolve a entrada com padrões."""
    if not isinstance(d, dict):
        raise DadosInvalidos(["a entrada precisa ser um objeto JSON"])
    d = json.loads(json.dumps(d))
    erros = []
    if d.get("peca", "rosca") != "rosca":
        erros.append(f"'peca' deve ser 'rosca', veio {d.get('peca')!r}")
    d["peca"] = "rosca"
    validar_base(d, erros)
    d.setdefault("casas", 1)
    d.setdefault("ativos", False)
    d.setdefault("criterio", "")
    d.setdefault("centro", None)
    casas = d["casas"]
    if isinstance(casas, bool) or not isinstance(casas, int) or not 0 <= casas <= 2:
        erros.append("'casas' (do percentual) deve ser 0, 1 ou 2")
        casas = 1
    fatias = d.get("fatias")
    if not isinstance(fatias, list) or not 2 <= len(fatias) <= MAX_FATIAS:
        erros.append(f"'fatias' precisa de 2 a {MAX_FATIAS} fatias")
        fatias = []
    rotulos, ok = [], True
    for i, f in enumerate(fatias):
        if not isinstance(f, dict) or not isinstance(f.get("rotulo"), str) or not f["rotulo"].strip():
            erros.append(f"fatias[{i}] sem 'rotulo'")
            ok = False
            continue
        if f["rotulo"] in rotulos:
            erros.append(f"fatias[{i}]: rótulo repetido {f['rotulo']!r}")
        rotulos.append(f["rotulo"])
        if not numero_ok(f.get("pct")) or f["pct"] <= 0:
            erros.append(f"fatias[{i}].pct inválido: {f.get('pct')!r} (esperado número maior que zero)")
            ok = False
    if fatias and ok:
        s = soma_pct(fatias, casas)
        bruto = sum(f["pct"] for f in fatias)
        if abs(bruto - 100) > 1e-6:
            erros.append(f"os percentuais somam {fmt_br(bruto, casas + 2)}%, não 100%: confira o dado")
        elif s != 100 * 10 ** casas:
            erros.append(f"arredondados em {casas} casa(s), os percentuais somam {fmt_br(s / 10 ** casas, casas)}% "
                         "na tela, não 100%: passe o dado já com as casas que vão aparecer")
        for i, f in enumerate(fatias):
            if round(f["pct"] * 10 ** casas) == 0:
                erros.append(f"fatias[{i}] ({f['rotulo']}) apareceria como 0%: use mais casas ou junte com outra")
    if d.get("destaque") not in rotulos:
        erros.append(f"'destaque' deve ser o rótulo de uma fatia (a fatia-chave), veio {d.get('destaque')!r}")
    c = d["centro"]
    if c is not None:
        if not isinstance(c, dict) or not numero_ok(c.get("valor")) or c["valor"] <= 0:
            erros.append("'centro' deve ser {'valor': número > 0, 'unidade': {...}, 'rotulo': ..., 'rotulo_final': ...}")
        else:
            c["unidade"] = {"prefixo": "", "sufixo": "", "casas": 2, **(c.get("unidade") or {})}
            c.setdefault("rotulo", "")
            c.setdefault("rotulo_final", "")
    parece_ativo = [r for r in rotulos if TICKER.match(r)]
    if parece_ativo and not d["ativos"]:
        erros.append(f"parece composição de ativos ({', '.join(parece_ativo[:3])}): use \"ativos\": true e informe o 'criterio'")
    if d["ativos"] and not (isinstance(d["criterio"], str) and d["criterio"].startswith("Critério:")):
        erros.append("composição de ativos exige 'criterio' começando com 'Critério:'")
    if erros:
        raise DadosInvalidos(erros)
    return d


def texto_pct(p, casas):
    return fmt_br(p, casas) + "%"


def centro_final(d):
    """Texto do centro no pouso: a parte da fatia-chave no total (ex.: R$ 6 × 43,79% = R$ 2,63)."""
    k = [f["rotulo"] for f in d["fatias"]].index(d["destaque"])
    pct = d["fatias"][k]["pct"]
    c = d["centro"]
    if not c:
        return texto_pct(pct, d["casas"]), d["destaque"]
    return texto_valor(c["valor"] * pct / 100, c["unidade"]), c.get("rotulo_final") or d["destaque"]


# ---------------------------------------------------------------- layout
def layout(d):
    W, H = FORMATOS[d["formato"]]
    n = len(d["fatias"])
    if d["formato"] == "16:9":
        L = dict(W=W, H=H, pad=96, kicker_y=92, titulo_y=136, titulo_px=76, titulo_w=W - 2 * 96,
                 cx=520, cy=640, R=262, w=112, leg_x=1000, leg_w=W - 96 - 1000, leg_y=300, colunas=1,
                 fonte_y=H - 64, criterio_y=H - 112, aviso_y=H - 64)
        L["leg_rowh"] = min(72, 600 / (n + 1))
    else:
        L = dict(W=W, H=H, pad=72, kicker_y=200, titulo_y=246, titulo_px=84, titulo_w=W - 2 * 72,
                 cx=540, cy=730, R=228, w=100, leg_x=72, leg_w=W - 2 * 72, leg_y=1050, colunas=1,
                 fonte_y=1590, criterio_y=1630, aviso_y=1680)
        L["leg_rowh"] = min(56, 520 / (n + 1))
    L["rot_px"] = round(min(36, L["leg_rowh"] * .56))
    L["pct_px"] = round(min(50, L["leg_rowh"] * .72))
    L["sw"] = round(L["rot_px"] * .8)
    L["centro_px"] = round(L["R"] * .5)
    return L


CSS = """
  #kicker {{ position:absolute; left:{pad}px; top:{kicker_y}px; font:{mono30}; letter-spacing:.12em; text-transform:uppercase; color:var(--cinza); }}
  #titulo {{ position:absolute; left:{pad}px; top:{titulo_y}px; width:{titulo_w}px; font:{titulo}; letter-spacing:{titulo_espaco}; }}
  #rosca {{ position:absolute; left:0; top:0; }}
  #trilho {{ fill:none; stroke:var(--grade); }}
  .fatia {{ fill:none; }}
  .contorno {{ fill:none; stroke:var(--tinta); stroke-width:6; }}
  #centro {{ position:absolute; left:{c_x}px; top:{c_y}px; width:{c_w}px; height:{c_h}px; display:flex; flex-direction:column;
             align-items:center; justify-content:center; text-align:center; }}
  #centro-numero {{ font:{numero_centro}; font-variant-numeric:tabular-nums; white-space:nowrap; display:inline-block; }}
  #centro-rotulo {{ font:{mono_centro}; letter-spacing:.06em; text-transform:uppercase; color:var(--cinza); margin-top:12px; max-width:{c_w}px; }}
  .leg {{ position:absolute; height:{rowh}px; width:{col_w}px; display:flex; align-items:center; gap:14px; }}
  .leg .sw {{ width:{sw}px; height:{sw}px; flex:none; }}
  .leg .rot {{ font:{rotulo}; white-space:nowrap; flex:1; overflow:hidden; text-overflow:ellipsis; }}
  .leg .pct {{ font:{numero_pct}; font-variant-numeric:tabular-nums; white-space:nowrap; }}
  #soma {{ position:absolute; font:{mono_soma}; color:var(--cinza); }}
  #criterio {{ position:absolute; left:{pad}px; top:{criterio_y}px; width:{crit_w}px; font:{mono_crit}; color:var(--cinza); }}
  #fonte {{ position:absolute; left:{pad}px; top:{fonte_y}px; font:{mono_fonte}; color:var(--cinza); background:var(--papel);
            padding:4px 10px; margin-left:-10px; }}
  #aviso {{ position:absolute; {aviso_pos}; top:{aviso_y}px; font:{rotulo_aviso}; color:var(--tinta); }}
"""

JS = r"""
  const tl = gsap.timeline({ paused: true });
  const arcos = D.fatias.map((f, k) => document.getElementById('F' + k));
  const pcts = D.fatias.map((f, k) => document.getElementById('P' + k));
  const prog = D.fatias.map(() => ({ p: 0 }));
  const pouso = { p: 0 };
  const cn = document.getElementById('centro-numero'), cr = document.getElementById('centro-rotulo');
  function desenhar() {
    D.fatias.forEach((f, k) => {
      const p = prog[k].p, len = Math.max(0, f.pct * p - D.folga);
      arcos[k].setAttribute('stroke-dasharray', `${len.toFixed(4)} ${(100 - len).toFixed(4)}`);
      pcts[k].textContent = fmtBR(p >= 1 ? f.pct : f.pct * p, D.casas) + '%';
    });
    const fim = pouso.p > 0;
    cn.textContent = fim ? D.centro_final : D.centro_ini;
    cr.textContent = fim ? D.rotulo_final : D.rotulo_ini;
  }
  desenhar();
  tl.eventCallback('onUpdate', desenhar);

  // 1. entrada
  tl.from('#kicker', { opacity: 0, y: 24, duration: .4, ease: 'power2.out' }, 0);
  tl.from('#titulo', { opacity: 0, y: 60, duration: .55, ease: 'back.out(1.4)' }, .12);
  tl.from('#trilho', { opacity: 0, duration: .45, ease: 'power1.out' }, .35);
  tl.from('#centro', { opacity: 0, scale: .85, duration: .45, ease: 'back.out(1.6)' }, .45);
  tl.from(['#fonte', '#criterio', '#aviso'], { opacity: 0, duration: .4 }, .6);
  tl.set('.leg', { opacity: 0 }, 0);
  tl.set('#soma', { opacity: 0 }, 0);
  // 2. uma fatia por vez: o arco se desenha e a linha da legenda entra, com o percentual contando
  D.fatias.forEach((f, k) => {
    const t = D.t0 + k * D.s;
    tl.to(prog[k], { p: 1, duration: D.g, ease: 'power2.out' }, t);
    tl.fromTo('#G' + k, { opacity: 0, x: -24 }, { opacity: 1, x: 0, duration: .3, ease: 'power2.out', immediateRender: false }, t);
  });
  // 3. pouso: a fatia-chave engrossa e ganha a cor; o centro pousa na parte dela (o único som, na trilha de áudio)
  tl.to(pouso, { p: 1, duration: .01 }, D.tp);
  tl.to('#F' + D.chave, { attr: { 'stroke-width': D.w * 1.3 }, stroke: D.cor_destaque, duration: .25, ease: 'back.out(2)' }, D.tp);
  tl.to(['#S' + D.chave], { backgroundColor: D.cor_destaque, duration: .15 }, D.tp);
  tl.to(['#P' + D.chave, '#R' + D.chave, '#centro-numero'], { color: D.cor_destaque, duration: .15 }, D.tp);
  tl.fromTo('#centro-numero', { scale: 1 }, { scale: 1.14, duration: .14, ease: 'power2.out', yoyo: true, repeat: 1, immediateRender: false }, D.tp);
  tl.fromTo('#soma', { opacity: 0, y: 12 }, { opacity: 1, y: 0, duration: .35, ease: 'power2.out', immediateRender: false }, D.tp + .35);
  BOIL
  tl.set({}, {}, D.dur);
  window.__timelines = window.__timelines || {};
  window.__timelines["rosca"] = tl;

"""


# leitor da tela, em assets/tela.js (fora da timeline: só o teste chama; não roda no render)
TELA = r"""  window.__tela = () => {
    const op = el => +getComputedStyle(el).opacity;
    const fatias = D.fatias.map((f, k) => ({
      rotulo: document.getElementById('R' + k).textContent, pct: pcts[k].textContent,
      arco: parseFloat(arcos[k].getAttribute('stroke-dasharray')), cor: getComputedStyle(arcos[k]).stroke,
      largura: parseFloat(arcos[k].getAttribute('stroke-width')), legenda_visivel: op(document.getElementById('G' + k)) > .5 }));
    const txt = id => { const e = document.getElementById(id); return e ? e.textContent : null; };
    return { fatias, centro: cn.textContent, centro_rotulo: cr.textContent, cor_centro: getComputedStyle(cn).color,
             soma: op(document.getElementById('soma')) > .5 ? txt('soma') : '', titulo: txt('titulo'), fonte: txt('fonte'),
             criterio: txt('criterio'), aviso: txt('aviso') };
  };
"""


def tempos(d):
    dur = float(d["duracao"])
    n = len(d["fatias"])
    t0 = 0.9
    tp = round(dur * .62, 3)
    s = (tp - .35 - t0) / n
    return dict(t0=t0, s=round(s, 4), g=round(min(.6, s * 1.05), 4), tp=tp, dur=dur)


def montar_html(d, sfx=None, sfx_dur=1.0):
    d = validar(d)
    e = ESTILOS[d["estilo"]]
    L = layout(d)
    T = tempos(d)
    fatias = d["fatias"]
    n = len(fatias)
    chave = [f["rotulo"] for f in fatias].index(d["destaque"])
    cinzas = iter(rampa_cinza(d["estilo"], n - 1))
    cores = [e["cores"]["tinta"] if k == chave else next(cinzas) for k in range(n)]
    tp = lambda papel, px: projeto.tipo(d["estilo"], papel, px)
    vert = d["formato"] == "9:16"
    raio_int = L["R"] - L["w"] / 2
    c_w = round(raio_int * 2 * .86)
    col_w = (L["leg_w"] - (40 if L["colunas"] == 2 else 0)) / L["colunas"]
    centro_ini = texto_valor(d["centro"]["valor"], d["centro"]["unidade"]) if d["centro"] else "100%"
    rotulo_ini = d["centro"]["rotulo"] if d["centro"] else "o total"
    cfin, rfin = centro_final(d)
    num_px = round(min(L["centro_px"], c_w / max(len(cfin), len(centro_ini)) * 1.55))
    css = CSS.format(
        **{k: L[k] for k in ("pad", "kicker_y", "titulo_y", "titulo_w", "sw", "fonte_y", "criterio_y", "aviso_y")},
        mono30=tp("mono", 30), titulo=tp("titulo", L["titulo_px"]), titulo_espaco=e["titulo_espaco"],
        c_x=round(L["cx"] - c_w / 2), c_y=round(L["cy"] - c_w / 2), c_w=c_w, c_h=c_w,
        numero_centro=tp("numero", num_px), mono_centro=tp("mono", 26 if not vert else 26),
        rowh=round(L["leg_rowh"]), col_w=round(col_w), rotulo=tp("rotulo", L["rot_px"]), numero_pct=tp("numero", L["pct_px"]),
        mono_soma=tp("mono", 26), crit_w=L["W"] - 2 * L["pad"], mono_crit=tp("mono", 22),
        mono_fonte=tp("mono", 28 if not vert else 26), rotulo_aviso=tp("rotulo", 28),
        aviso_pos=f"right:{L['pad']}px" if not vert else f"left:{L['pad']}px")
    # anel: cada fatia é um círculo com pathLength=100; o traço começa no topo e anda no sentido horário
    W, H, dur = L["W"], L["H"], T["dur"]
    acum, arcos = 0.0, ""
    for k, f in enumerate(fatias):
        arcos += (f'<circle id="F{k}" class="fatia" cx="{L["cx"]}" cy="{L["cy"]}" r="{L["R"]}" pathLength="100" '
                  f'stroke="{cores[k]}" stroke-width="{L["w"]}" stroke-dasharray="0 100" '
                  f'stroke-dashoffset="{-(acum + FOLGA / 2):.4f}" transform="rotate(-90 {L["cx"]} {L["cy"]})"/>')
        acum += f["pct"]
    contorno = ""
    if e["boil"]:
        contorno = "".join(f'<circle class="contorno" cx="{L["cx"]}" cy="{L["cy"]}" r="{r}" filter="url(#boil)"/>'
                           for r in (L["R"] + L["w"] / 2 + 4, L["R"] - L["w"] / 2 - 4))
    svg = (f'<svg id="rosca" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<circle id="trilho" cx="{L["cx"]}" cy="{L["cy"]}" r="{L["R"]}" stroke-width="{L["w"]}"/>{contorno}{arcos}</svg>')
    leg = ""
    linhas_col = math.ceil((n + 1) / L["colunas"])
    for k, f in enumerate(fatias):
        col, lin = divmod(k, linhas_col) if L["colunas"] == 2 else (0, k)
        x = L["leg_x"] + col * (col_w + 40)
        y = L["leg_y"] + lin * L["leg_rowh"]
        leg += (f'<div class="leg" id="G{k}" style="left:{x:.1f}px; top:{y:.1f}px">'
                f'<div class="sw" id="S{k}" style="background:{cores[k]}"></div>'
                f'<div class="rot" id="R{k}">{esc(f["rotulo"])}</div><div class="pct" id="P{k}">0%</div></div>')
    k = n
    col, lin = divmod(k, linhas_col) if L["colunas"] == 2 else (0, k)
    soma_txt = "soma: " + texto_pct(soma_pct(fatias, d["casas"]) / 10 ** d["casas"], d["casas"])
    leg += (f'<div id="soma" style="left:{L["leg_x"] + col * (col_w + 40):.1f}px; '
            f'top:{L["leg_y"] + lin * L["leg_rowh"] + 10:.1f}px">{soma_txt}</div>')
    criterio = f'<div id="criterio">{esc(d["criterio"])}</div>' if d["criterio"] else ""
    aviso = f'<div id="aviso">{AVISO_ATIVOS}</div>' if d["ativos"] else ""
    dados = dict(fatias=[dict(rotulo=f["rotulo"], pct=f["pct"]) for f in fatias], chave=chave, casas=d["casas"],
                 folga=FOLGA, w=L["w"], centro_ini=centro_ini, rotulo_ini=rotulo_ini, centro_final=cfin, rotulo_final=rfin,
                 cor_destaque=e["cores"]["destaque"], t0=T["t0"], s=T["s"], g=T["g"], tp=T["tp"], dur=dur)
    js = JS.replace("BOIL", projeto.js_boil(d))
    return (projeto.cabeca(d, css)
            + f'<div id="root" data-composition-id="rosca" data-start="0" data-width="{W}" data-height="{H}" '
              f'data-duration="{dur:.3f}" data-formato="{d["formato"]}" data-estilo="{d["estilo"]}">\n'
            + projeto.filtro_boil(d)
            + f'  <section id="cena" class="clip cena" data-start="0" data-duration="{dur:.3f}" data-track-index="1">\n'
            + f'    <div id="kicker">{esc(d["kicker"])}</div>\n    <div id="titulo">{esc(d["titulo"])}</div>\n'
            + f'    {svg}\n    <div id="centro"><div id="centro-numero">{esc(centro_ini)}</div>'
              f'<div id="centro-rotulo">{esc(rotulo_ini)}</div></div>\n'
            + f'    {leg}\n    {criterio}\n    <div id="fonte">{esc(d["fonte"])}</div>\n    {aviso}\n'
            + f'    {projeto.marca(d)}\n  </section>\n  {projeto.audio_pouso(sfx, sfx_dur, T["tp"])}\n</div>\n'
            + "<script>\n  const D = " + json.dumps(dados, ensure_ascii=False) + ";\n" + projeto.JS_FMT + js
            + '</script>\n<script src="assets/tela.js"></script>\n</body>\n</html>\n')


def gerar_projeto(d, destino):
    d = validar(d)
    os.makedirs(destino, exist_ok=True)
    sfx, sfx_dur = projeto.preparar_assets(d, destino, "rosca")
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
    cfin, rfin = centro_final(d)
    print(f"ok: {caminho} (rosca, {d['estilo']}, {d['formato']}, {d['duracao']} s, {len(d['fatias'])} fatias, "
          f"soma {fmt_br(soma_pct(d['fatias'], d['casas']) / 10 ** d['casas'], d['casas'])}%, centro final {cfin} · {rfin})")


if __name__ == "__main__":
    main()
