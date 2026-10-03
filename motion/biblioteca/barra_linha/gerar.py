"""Barra vira linha: a taxa do mês em barras (ex.: IPCA mensal, SGS 433) que se transformam na linha do
acumulado em 12 meses. HyperFrames, a partir de um JSON de dado real.

Uso:
  python3 biblioteca/barra_linha/gerar.py exemplos/barra-linha-ipca-16x9.json -o projetos/ipca
  (ou: ./biblioteca/renderizar.sh exemplos/barra-linha-ipca-16x9.json)

O que acontece na tela:
  1. kicker e título entram; as barras do mês crescem do zero (para baixo, se negativo), da esquerda para a
     direita, com o valor de cada uma em cima; o placar mostra o valor do mês da barra que acabou de entrar;
  2. cada barra se encolhe num ponto, na altura do acumulado em 12 meses daquele mês; a escala troca junto;
  3. a linha liga os pontos da esquerda para a direita, o placar acompanha (o acumulado do último ponto
     alcançado, sempre um valor da série) e pousa no último com o único som;
  4. a fonte fica no rodapé a peça inteira.

O acumulado é CALCULADO aqui, a partir do mensal: prod(1 + m/100) dos 12 meses − 1. Se a entrada trouxer
"referencia_12m" (a série oficial, ex.: SGS 13522), cada mês mostrado tem de bater com ela em até 0,01 p.p.;
senão, validar() recusa e nada é gerado.

Entrada (JSON) — ver biblioteca/README.md:
  peca: "barra_linha"; estilo; formato; duracao (5 a 10 s); titulo; kicker; fonte ("Fonte: BCB/SGS 433 ...")
  mensal: [{"data", "valor"}] em ordem, mês a mês, com pelo menos 11 meses ANTES do 1º mês mostrado
  mostrar: quantos meses mostrar (6 a 24, padrão 12), os últimos da série
  referencia_12m: [{"data", "valor"}] (opcional, mas o dados.py sempre põe): a série oficial do acumulado
  rotulos: {"mes": "no mês", "doze": "em 12 meses"}; casas (padrão 2); som
"""
import argparse, datetime as dt, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MOTION = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(MOTION, "comum"))
from estilo import (AVISO_ATIVOS, ESTILOS, MESES, DadosInvalidos, checar_ativos, esc, fmt_br, misturar,  # noqa: E402
                    numero_ok, validar_base)
import projeto  # noqa: E402

G = projeto.grafico_cotacao()
TOLERANCIA = 0.01 + 1e-9   # p.p.: o BCB publica o acumulado com 2 casas


def acumulado_12m(mensal):
    """[(data, % no mês)] -> [(data, % em 12 meses)] a partir do 12º mês. Composto, não somado."""
    out = []
    for k in range(11, len(mensal)):
        p = 1.0
        for _, v in mensal[k - 11:k + 1]:
            p *= 1 + v / 100
        out.append((mensal[k][0], (p - 1) * 100))
    return out


def _mes_seguinte(a, b):
    return (b.year * 12 + b.month) - (a.year * 12 + a.month) == 1


def validar(d):
    if not isinstance(d, dict):
        raise DadosInvalidos(["a entrada precisa ser um objeto JSON"])
    d = json.loads(json.dumps(d))
    erros = []
    if d.get("peca", "barra_linha") != "barra_linha":
        erros.append(f"'peca' deve ser 'barra_linha', veio {d.get('peca')!r}")
    d["peca"] = "barra_linha"
    d.setdefault("duracao", 9.0)
    d.setdefault("unidade", {"prefixo": "", "sufixo": "%", "casas": d.get("casas", 2)})
    validar_base(d, erros)
    d.setdefault("mostrar", 12)
    d.setdefault("referencia_12m", None)
    d["rotulos"] = {"mes": "no mês", "doze": "em 12 meses", **(d.get("rotulos") or {})}
    n = d["mostrar"]
    if isinstance(n, bool) or not isinstance(n, int) or not 6 <= n <= 24:
        erros.append("'mostrar' deve ser inteiro de 6 a 24 meses")
        n = 12
    mensal = d.get("mensal")
    ok = isinstance(mensal, list)
    if not ok:
        erros.append("'mensal' é obrigatório: [{'data': 'AAAA-MM-01', 'valor': % no mês}]")
        mensal = []
    datas = []
    for i, p in enumerate(mensal):
        try:
            x = dt.date.fromisoformat(p["data"])
            if not numero_ok(p["valor"]):
                raise ValueError
        except (KeyError, TypeError, ValueError):
            erros.append(f"mensal[{i}] inválido: {p!r}")
            ok = False
            continue
        if datas and not _mes_seguinte(datas[-1], x):
            erros.append(f"mensal[{i}] ({p['data']}): os meses têm de ser seguidos, sem buraco nem repetição")
            ok = False
        datas.append(x)
    if ok and len(mensal) < n + 11:
        erros.append(f"'mensal' com {len(mensal)} meses: para mostrar {n} com o acumulado em 12 meses, são precisos "
                     f"{n + 11} (11 antes do 1º mostrado)")
    ref = d["referencia_12m"]
    if ok and len(mensal) >= n + 11 and ref is not None:
        if not isinstance(ref, list):
            erros.append("'referencia_12m' deve ser uma lista [{'data', 'valor'}]")
        else:
            oficial = {r.get("data"): r.get("valor") for r in ref if isinstance(r, dict)}
            calc = acumulado_12m([(p["data"], p["valor"]) for p in mensal])[-n:]
            for data, v in calc:
                o = oficial.get(data)
                if not numero_ok(o):
                    erros.append(f"referencia_12m sem o mês {data} (cada mês mostrado precisa da conferência)")
                elif abs(round(v, 2) - o) > TOLERANCIA:
                    erros.append(f"acumulado de {data} calculado = {fmt_br(v, 4)}%, oficial = {fmt_br(o, 2)}%: "
                                 "não bate (dado mensal errado ou fora de ordem)")
    checar_ativos(d, [d.get("titulo"), d.get("kicker")], erros)
    if erros:
        raise DadosInvalidos(erros)
    return d


def series(d):
    """-> [(data, mensal, acumulado)] dos meses mostrados."""
    mensal = [(p["data"], p["valor"]) for p in d["mensal"]]
    acum = acumulado_12m(mensal)[-d["mostrar"]:]
    por_data = dict(mensal)
    return [(data, por_data[data], a) for data, a in acum]


def mes_br(iso):
    return f"{MESES[int(iso[5:7]) - 1]}/{iso[:4]}"


def geometria(d):
    L = dict(G.layout(d["formato"]))
    s = series(d)
    n = len(s)
    ms, ac = [m for _, m, _ in s], [a for _, _, a in s]
    lo1, hi1, marcas1 = G.escala_y(min(0, min(ms)), max(0, max(ms)))
    lo2, hi2, marcas2 = G.escala_y(min(ac), max(ac))
    gx0, gx1, gy0, gy1 = L["gx0"], L["gx1"], L["gy0"], L["gy1"]
    Y1 = lambda v: gy1 - (v - lo1) / (hi1 - lo1) * (gy1 - gy0)
    Y2 = lambda v: gy1 - (v - lo2) / (hi2 - lo2) * (gy1 - gy0)
    sw = (gx1 - gx0) / n
    xs = [round(gx0 + sw * (k + .5), 2) for k in range(n)]
    return dict(L=L, s=s, n=n, sw=sw, bw=round(sw * .62, 2), xs=xs,
                y_zero=round(Y1(0), 2), y_mes=[round(Y1(m), 2) for m in ms], y_acum=[round(Y2(a), 2) for a in ac],
                marcas1=[(round(Y1(m), 1), m) for m in marcas1], marcas2=[(round(Y2(m), 1), m) for m in marcas2],
                escala1=(gy1 - gy0) / (hi1 - lo1))


def tempos(d, n):
    dur = float(d["duracao"])
    t0, g = 0.8, 0.5
    s = round(min(.2, max(.03, (dur * .33 - t0 - g) / max(1, n - 1))), 4)
    tb = t0 + (n - 1) * s + g
    tm0 = round(tb + .35, 3)
    tm1 = round(tm0 + .8, 3)
    tp = round(max(tm1 + 1.0, dur * .75), 3)
    return dict(t0=t0, g=g, s=s, tb=round(tb, 3), tm0=tm0, tm1=tm1, tp=tp, dur=dur)


CSS = """
  #kicker {{ position:absolute; left:{pad}px; top:{kicker_y}px; font:{mono30}; letter-spacing:.14em; text-transform:uppercase; color:var(--cinza); }}
  #titulo {{ position:absolute; left:{pad}px; top:{titulo_y}px; width:{titulo_w}px; font:{titulo}; }}
  #placar {{ position:absolute; {lado}:{num_x}px; top:{num_y}px; text-align:{lado}; }}
  .num {{ font:{numero}; font-variant-numeric:tabular-nums; white-space:nowrap; display:inline-block; transform-origin:{lado} center; }}
  #numero {{ color:var(--tinta); }}
  .rot-placar {{ font:{rotulo}; color:var(--cinza); margin-top:12px; }}
  #placar-mes, #placar-doze {{ position:absolute; {lado}:0; top:0; white-space:nowrap; }}
  #grafico {{ position:absolute; left:0; top:0; }}
  .grade {{ stroke:var(--grade); stroke-width:2; }}
  .zero {{ stroke:var(--cinza); stroke-width:3; }}
  .eixo {{ font:{eixo}; fill:var(--cinza); }}
  .barra {{ fill:var(--cinza-barra); stroke:var(--tinta); stroke-width:4; }}
  .vbar {{ font:{vbar}; fill:var(--tinta); }}
  #linha {{ fill:none; stroke:var(--tinta); stroke-width:7; stroke-linejoin:round; stroke-linecap:round; }}
  #anel {{ fill:none; stroke:var(--destaque); stroke-width:5; }}
  #rodape {{ position:absolute; left:{pad}px; right:{pad}px; top:{fonte_y}px; display:flex; flex-direction:{rodape_dir};
             justify-content:space-between; gap:8px 32px; font:{mono_fonte}; }}
  #fonte {{ color:var(--cinza); }}
  #aviso {{ color:var(--tinta); white-space:nowrap; }}
"""

JS = r"""
  const tl = gsap.timeline({ paused: true });
  const cresce = D.ms.map(() => ({ p: 0 })), morf = { m: 0 }, rev = { q: 0 };
  const barras = D.ms.map((_, k) => document.getElementById('B' + k));
  const numMes = document.getElementById('numero-mes'), num = document.getElementById('numero'),
        cortina = document.getElementById('cortina');
  const r = D.r;
  function desenhar() {
    let ultima = -1;
    D.ms.forEach((v, k) => {
      const g = cresce[k].p, m = morf.m;
      if (g > 0) ultima = k;
      const yv = D.y_zero + (D.y_mes[k] - D.y_zero) * g;
      const top = Math.min(yv, D.y_zero), bot = Math.max(yv, D.y_zero);
      const t = top + (D.y_acum[k] - r - top) * m, b = bot + (D.y_acum[k] + r - bot) * m;
      const w = D.bw + (2 * r - D.bw) * m;
      const e = barras[k];
      e.setAttribute('x', (D.xs[k] - w / 2).toFixed(2)); e.setAttribute('width', w.toFixed(2));
      e.setAttribute('y', t.toFixed(2)); e.setAttribute('height', Math.max(0, b - t).toFixed(2));
      e.setAttribute('rx', (r * m).toFixed(2));
    });
    // placar do mês: o valor real da última barra que entrou
    if (ultima >= 0) numMes.textContent = D.txt_mes[ultima];
    // linha: revela da esquerda para a direita; o placar mostra o acumulado do último ponto alcançado
    const x = D.gx0 + (D.gx1 - D.gx0) * rev.q;
    cortina.setAttribute('width', rev.q > 0 ? (x - D.gx0 + 10).toFixed(2) : 0);
    let k = -1;
    D.xs.forEach((xk, i) => { if (xk <= x + 1e-6) k = i; });
    if (rev.q >= 1) k = D.xs.length - 1;
    num.textContent = k >= 0 ? D.txt_acum[k] : D.txt_acum[0];
  }
  desenhar();
  tl.eventCallback('onUpdate', desenhar);
  tl.from('#kicker', { opacity: 0, y: 24, duration: .4, ease: 'power2.out' }, 0);
  tl.from('#titulo', { opacity: 0, y: 60, duration: .55, ease: 'back.out(1.4)' }, .12);
  tl.from('#rodape', { opacity: 0, duration: .4 }, .6);
  tl.from('#eixos1', { opacity: 0, duration: .45 }, .45);
  tl.set(['#placar-doze', '#eixos2', '.vbar'], { opacity: 0 }, 0);
  tl.set('#placar-mes', { opacity: 0 }, 0);
  tl.set('#placar-mes', { opacity: 1 }, D.t0);
  // 1. barras do mês, da esquerda para a direita
  D.ms.forEach((_, k) => {
    tl.to(cresce[k], { p: 1, duration: D.g, ease: 'power2.out' }, D.t0 + k * D.s);
    tl.to('#VB' + k, { opacity: 1, duration: .2 }, D.t0 + k * D.s + D.g * .6);
  });
  // 2. cada barra vira um ponto na altura do acumulado em 12 meses; a escala troca
  tl.to('.vbar', { opacity: 0, duration: .25 }, D.tm0 - .1);
  tl.to(morf, { m: 1, duration: D.tm1 - D.tm0, ease: 'power2.inOut' }, D.tm0);
  tl.to('#eixos1', { opacity: 0, duration: .4 }, D.tm0);
  tl.to('#eixos2', { opacity: 1, duration: .4 }, D.tm0 + .3);
  tl.to('#placar-mes', { opacity: 0, y: -20, duration: .3 }, D.tm0);
  tl.fromTo('#placar-doze', { opacity: 0, y: 20 }, { opacity: 1, y: 0, duration: .35, immediateRender: false }, D.tm0 + .25);
  // 3. a linha liga os pontos; pouso no último (o único som, na trilha de áudio)
  tl.to(rev, { q: 1, duration: D.tp - D.tm1, ease: 'power1.inOut' }, D.tm1);
  tl.to('#B' + (D.ms.length - 1), { fill: D.cor_destaque, stroke: D.cor_destaque, duration: .15 }, D.tp);
  tl.to('#numero', { color: D.cor_destaque, duration: .15 }, D.tp);
  tl.fromTo('#numero', { scale: 1 }, { scale: 1.12, duration: .14, ease: 'power2.out', yoyo: true, repeat: 1, immediateRender: false }, D.tp);
  tl.fromTo('#anel', { opacity: .9, scale: 1, transformOrigin: 'center' },
            { opacity: 0, scale: 3.2, duration: .7, ease: 'power2.out', immediateRender: false }, D.tp);
  BOIL
  tl.set({}, {}, D.dur);
  window.__timelines = window.__timelines || {};
  window.__timelines["barra_linha"] = tl;
"""

TELA = r"""  window.__tela = () => {
    const op = el => { let o = 1; for (let n = el; n && n.nodeType === 1; n = n.parentElement) o *= +getComputedStyle(n).opacity; return o; };
    const b = barras.map((e, k) => ({ data: D.datas[k], x: +e.getAttribute('x'), w: +e.getAttribute('width'),
      y: +e.getAttribute('y'), h: +e.getAttribute('height'), cor: getComputedStyle(e).fill,
      rotulo: document.getElementById('VB' + k) ? document.getElementById('VB' + k).textContent : null,
      rotulo_visivel: document.getElementById('VB' + k) ? op(document.getElementById('VB' + k)) > .9 : false }));
    const txt = id => { const e = document.getElementById(id); return e ? e.textContent : null; };
    return { barras: b, numero_mes: txt('numero-mes'), mes_visivel: op(document.getElementById('placar-mes')) > .9,
             numero: txt('numero'), doze_visivel: op(document.getElementById('placar-doze')) > .9,
             rotulo_doze: txt('rotulo-doze'), cor_numero: getComputedStyle(num).color,
             revelado: +cortina.getAttribute('width'), eixos2: op(document.getElementById('eixos2')),
             fonte: txt('fonte'), titulo: txt('titulo'), aviso: document.getElementById('aviso') ? txt('aviso') : '' };
  };
"""


def montar_html(d, sfx=None, sfx_dur=1.0):
    d = validar(d)
    e = ESTILOS[d["estilo"]]
    Gm = geometria(d)
    L, s, n = Gm["L"], Gm["s"], Gm["n"]
    W, H = L["W"], L["H"]
    T = tempos(d, n)
    un = d["unidade"]
    casas = un["casas"]
    vert = d["formato"] == "9:16"
    tv = lambda v: f"{un['prefixo']}{fmt_br(v, casas)}{un['sufixo']}"
    txt_mes, txt_acum = [tv(m) for _, m, _ in s], [tv(a) for _, _, a in s]
    mais_longo = max(len(t) for t in txt_mes + txt_acum)
    num_px = min(L["num_px"], int(L["num_largura"] / (0.66 * mais_longo)))
    tp = lambda papel, px: projeto.tipo(d["estilo"], papel, px)
    css = CSS.format(pad=L["pad"], kicker_y=L["kicker_y"], titulo_y=L["titulo_y"],
                     titulo_w=W - 2 * L["pad"] - (760 if not vert else 0), mono30=tp("mono", 30),
                     titulo=tp("titulo", 72 if not vert else 80), lado=L["num_alinha"],
                     num_x=L["num_x"] if L["num_alinha"] == "left" else W - L["num_x"], num_y=L["num_y"],
                     numero=tp("numero", num_px), rotulo=tp("rotulo", 34), eixo=tp("mono", L["eixo_px"]),
                     vbar=tp("mono", 26 if Gm["sw"] >= 100 else 20), fonte_y=L["fonte_y"],
                     rodape_dir="column" if vert else "row", mono_fonte=tp("mono", 26)
                     ).replace("var(--cinza-barra)", misturar(e["cores"]["tinta"], e["cores"]["grade"], .55))
    def grade(marcas, zero):
        return "".join(
            f'<line x1="{L["gx0"]}" x2="{L["gx1"]}" y1="{y}" y2="{y}" class="{"zero" if zero and abs(m) < 1e-12 else "grade"}"/>'
            f'<text x="{L["gx0"] - 22}" y="{y + 10}" class="eixo" text-anchor="end">'
            f'{fmt_br(m, 0 if all(abs(x - round(x)) < 1e-9 for _, x in marcas) else (1 if all(abs(x * 10 - round(x * 10)) < 1e-9 for _, x in marcas) else 2))}'
            f'{esc(un["sufixo"])}</text>' for y, m in marcas)
    # meses no eixo x: o último e, para trás, de 3 em 3
    passo = 3 if n <= 12 else 6
    meses = "".join(f'<text x="{Gm["xs"][k]}" y="{L["gy1"] + 52}" class="eixo" text-anchor="middle">{mes_br(s[k][0])}</text>'
                    for k in range(n - 1, -1, -passo))
    rotulos_barras = ""
    if Gm["sw"] >= 60:
        for k, (_, m, _) in enumerate(s):
            y = Gm["y_mes"][k] - 14 if m >= 0 else Gm["y_mes"][k] + 34
            rotulos_barras += (f'<text id="VB{k}" class="vbar" x="{Gm["xs"][k]}" y="{y}" text-anchor="middle">'
                               f'{fmt_br(m, casas)}</text>')
    barras = "".join(f'<rect id="B{k}" class="barra" x="{Gm["xs"][k]}" y="{Gm["y_zero"]}" width="0" height="0"/>'
                     for k in range(n))
    aviso = f'<div id="aviso">{AVISO_ATIVOS}</div>' if d.get("ativos") else ""
    ult = s[-1][0]
    rot = d["rotulos"]
    dados = dict(ms=[m for _, m, _ in s], datas=[x for x, _, _ in s], xs=Gm["xs"], bw=Gm["bw"], r=9,
                 y_zero=Gm["y_zero"], y_mes=Gm["y_mes"], y_acum=Gm["y_acum"], gx0=L["gx0"], gx1=L["gx1"],
                 txt_mes=txt_mes, txt_acum=txt_acum, cor_destaque=e["cores"]["destaque"], **T)
    linha = "M" + "L".join(f"{x},{y}" for x, y in zip(Gm["xs"], Gm["y_acum"]))
    svg = (f'<svg id="grafico" width="{W}" height="{H}" viewBox="0 0 {W} {H}">'
           f'<defs><clipPath id="revela"><rect id="cortina" x="{L["gx0"] - 10}" y="0" width="0" height="{H}"/></clipPath></defs>'
           f'<g id="eixos1">{grade(Gm["marcas1"], True)}</g><g id="eixos2">{grade(Gm["marcas2"], False)}</g>'
           f'<g id="meses">{meses}</g>'
           f'<g clip-path="url(#revela)"><path id="linha" d="{linha}"/></g>'
           f'<g id="barras">{barras}</g>{rotulos_barras}'
           f'<circle id="anel" cx="{Gm["xs"][-1]}" cy="{Gm["y_acum"][-1]}" r="16" opacity="0"/></svg>')
    placar = (f'<div id="placar"><div id="placar-mes"><span class="num" id="numero-mes">{esc(txt_mes[0])}</span>'
              f'<div class="rot-placar" id="rotulo-mes">{esc(rot["mes"])}</div></div>'
              f'<div id="placar-doze"><span class="num" id="numero">{esc(txt_acum[0])}</span>'
              f'<div class="rot-placar" id="rotulo-doze">{esc(rot["doze"])} até {mes_br(ult)}</div></div></div>')
    dur = T["dur"]
    return (projeto.cabeca(d, css)
            + f'<div id="root" data-composition-id="barra_linha" data-start="0" data-width="{W}" data-height="{H}" '
              f'data-duration="{dur:.3f}" data-formato="{d["formato"]}" data-estilo="{d["estilo"]}">\n'
            + f'  <section id="cena" class="clip cena" data-start="0" data-duration="{dur:.3f}" data-track-index="1">\n'
            + f'    <div id="kicker">{esc(d["kicker"])}</div>\n    <div id="titulo">{esc(d["titulo"])}</div>\n'
            + f'    {placar}\n    {svg}\n'
            + f'    <div id="rodape"><div id="fonte">{esc(d["fonte"])}</div>{aviso}</div>\n'
            + f'    {projeto.marca(d)}\n  </section>\n  {projeto.audio_pouso(sfx, sfx_dur, T["tp"])}\n</div>\n'
            + "<script>\n  const D = " + json.dumps(dados, ensure_ascii=False) + ";\n" + JS.replace("BOIL", "")
            + '</script>\n<script src="assets/tela.js"></script>\n</body>\n</html>\n')


def gerar_projeto(d, destino):
    d = validar(d)
    os.makedirs(destino, exist_ok=True)
    sfx, sfx_dur = projeto.preparar_assets(d, destino, "barra_linha")
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
    s = series(d)
    print(f"ok: {caminho} (barra_linha, {d['formato']}, {d['duracao']} s, {len(s)} meses; "
          f"último: {fmt_br(s[-1][1], 2)}% no mês, {fmt_br(s[-1][2], 2)}% em 12 meses; pouso em {tempos(d, len(s))['tp']} s)")


if __name__ == "__main__":
    main()
