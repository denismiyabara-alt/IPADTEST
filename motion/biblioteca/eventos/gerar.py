"""Eventos no gráfico: marcadores anotados (ex.: decisões do Copom) sobre a linha do grafico_cotacao.
Cada evento é um traço vertical com um ponto na linha e um rótulo curto, que aparece quando a ponta da linha
passa pela data. O resto é o gráfico de cotação, sem mudança (mesmo gerar.py, mesma validação e compliance).

Uso:
  python3 biblioteca/eventos/gerar.py exemplos/eventos-selic-copom-16x9.json -o projetos/copom
  (ou: ./biblioteca/renderizar.sh exemplos/eventos-selic-copom-16x9.json)

Entrada (JSON): a mesma do grafico_cotacao (titulo, kicker, fonte, classe, serie, linha, unidade, variacao,
comparador/aviso, som...) mais:
  peca: "eventos"
  eventos: [{"data": "AAAA-MM-DD", "rotulo": "1º corte: 14,75%"}], 1 a 8, em ordem, dentro do período da série;
           rótulo de até 22 caracteres (curto: lê-se no celular); a altura do rótulo é escolhida para não bater
           na linha nem no rótulo vizinho.
"""
import argparse, datetime as dt, json, os, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MOTION = os.path.dirname(os.path.dirname(AQUI))
sys.path.insert(0, os.path.join(MOTION, "comum"))
from estilo import DadosInvalidos, checar_ativos, esc  # noqa: E402
import projeto  # noqa: E402

G = projeto.grafico_cotacao()
MAX_EVENTOS = 8
MAX_ROTULO = 22
CORPO = 30          # px do rótulo
NIVEL = 44          # px entre níveis de rótulo
ANCORA_SVG = '\n    </svg>\n    <div id="rodape">'
ANCORA_JS = "  // fecha a timeline na duração exata"


def validar(d):
    if not isinstance(d, dict):
        raise DadosInvalidos(["a entrada precisa ser um objeto JSON"])
    d = json.loads(json.dumps(d))
    erros = []
    if d.get("peca", "eventos") != "eventos":
        erros.append(f"'peca' deve ser 'eventos', veio {d.get('peca')!r}")
    d["peca"] = "eventos"
    try:
        g = G.validar(d)
    except G.DadosInvalidos as e:
        erros += list(e.args[0])
        g = None
    ev = d.get("eventos")
    if not isinstance(ev, list) or not 1 <= len(ev) <= MAX_EVENTOS:
        erros.append(f"'eventos' precisa de 1 a {MAX_EVENTOS} marcadores (mais que isso não se lê)")
        ev = []
    datas = []
    serie = d.get("serie") if isinstance(d.get("serie"), list) else []
    try:
        ini, fim = serie[0]["data"], serie[-1]["data"]
    except (IndexError, KeyError, TypeError):
        ini = fim = None
    for k, e in enumerate(ev):
        try:
            x = dt.date.fromisoformat(e["data"])
            r = e["rotulo"]
            if not isinstance(r, str) or not r.strip():
                raise ValueError
        except (KeyError, TypeError, ValueError):
            erros.append(f"eventos[{k}] inválido: {e!r} (esperado {{'data': 'AAAA-MM-DD', 'rotulo': 'texto curto'}})")
            continue
        if len(r) > MAX_ROTULO:
            erros.append(f"eventos[{k}].rotulo com {len(r)} caracteres: no máximo {MAX_ROTULO} ({r!r})")
        if datas and x <= datas[-1]:
            erros.append(f"eventos[{k}] fora de ordem ou repetido: {e['data']}")
        if ini and not ini <= e["data"] <= fim:
            erros.append(f"eventos[{k}] fora do período da série ({ini} a {fim}): {e['data']}")
        datas.append(x)
    checar_ativos(d, [d.get("titulo"), d.get("kicker")] + [e.get("rotulo") for e in ev if isinstance(e, dict)], erros)
    if erros:
        raise DadosInvalidos(erros)
    g["peca"], g["eventos"], g["ativos"] = "eventos", d["eventos"], d["ativos"]
    return g


def posicoes(d):
    """-> [{k, x, y, t, rotulo, lado, nivel, y_rotulo}] de cada evento, na mesma geometria e tempo do gráfico."""
    d = validar(d)
    Gm = G.geometria(d)
    L, pts, xs, ys = Gm["L"], Gm["pts"], Gm["xs"], Gm["ys"]
    t0 = dt.date.fromisoformat(pts[0]["data"]).toordinal()
    t1 = dt.date.fromisoformat(pts[-1]["data"]).toordinal()
    dur = float(d["duracao"])
    t_ini, t_pouso = 0.9, round(dur * G.FRACAO_POUSO, 3)        # os mesmos do grafico_cotacao/gerar.py
    meio = (L["gy0"] + L["gy1"]) / 2
    ocupado = {"cima": [], "baixo": []}                          # (nivel, x0, x1) já usados
    out = []
    for k, e in enumerate(d["eventos"]):
        x = L["gx0"] + (dt.date.fromisoformat(e["data"]).toordinal() - t0) / max(1, t1 - t0) * (L["gx1"] - L["gx0"])
        i = max(j for j, p in enumerate(pts) if p["data"] <= e["data"])
        if d["linha"] == "degrau" or i == len(pts) - 1:
            y = ys[i]
        else:
            f = (x - xs[i]) / max(1e-9, xs[i + 1] - xs[i])
            y = ys[i] + (ys[i + 1] - ys[i]) * f
        lado = "cima" if y > meio else "baixo"                   # o rótulo vai do lado oposto ao da linha
        largura = len(e["rotulo"]) * CORPO * .64 + 20
        direita = x > (L["gx0"] + L["gx1"]) / 2
        x0, x1 = (x - largura, x) if direita else (x, x + largura)
        nivel = 0
        while any(n == nivel and not (x1 < a or x0 > b) for n, a, b in ocupado[lado]):
            nivel += 1
        ocupado[lado].append((nivel, x0, x1))
        y_rot = L["gy0"] + 6 + nivel * NIVEL if lado == "cima" else L["gy1"] - 18 - nivel * NIVEL
        frac = (x - L["gx0"]) / (L["gx1"] - L["gx0"])
        t = t_ini + G.tempo_da_ease(frac) * (t_pouso - t_ini)
        out.append(dict(k=k, x=round(x, 2), y=round(y, 2), t=round(t, 3), rotulo=e["rotulo"], lado=lado,
                        nivel=nivel, y_rotulo=round(y_rot, 1), ancora="end" if direita else "start"))
    return out


def _svg(P):
    s = ""
    for p in P:
        topo = p["y_rotulo"] + (12 if p["lado"] == "cima" else -CORPO)
        y0, y1 = (topo, p["y"]) if topo < p["y"] else (p["y"], topo)
        dx = -10 if p["ancora"] == "end" else 10
        s += (f'<g id="ev{p["k"]}" class="evento">'
              f'<line x1="{p["x"]}" x2="{p["x"]}" y1="{y0:.1f}" y2="{y1:.1f}" class="ev-traco"/>'
              f'<circle cx="{p["x"]}" cy="{p["y"]}" r="9" class="ev-ponto"/>'
              f'<text x="{p["x"] + dx}" y="{p["y_rotulo"] + (CORPO if p["lado"] == "cima" else 0)}" '
              f'text-anchor="{p["ancora"]}" class="ev-texto">{esc(p["rotulo"])}</text></g>')
    return s


TELA = r"""  window.__tela = () => {
    const op = el => { let o = 1; for (let n = el; n && n.nodeType === 1; n = n.parentElement) o *= +getComputedStyle(n).opacity; return o; };
    const ev = [...document.querySelectorAll('.evento')].map(g => {
      const t = g.querySelector('text'), c = g.querySelector('circle'), r = t.getBoundingClientRect();
      return { rotulo: t.textContent, visivel: op(g) > .9, x: +c.getAttribute('cx'), y: +c.getAttribute('cy'),
               caixa: { x0: r.left, x1: r.right, y0: r.top, y1: r.bottom }, cor: getComputedStyle(t).fill };
    });
    const txt = id => { const e = document.getElementById(id); return e ? e.textContent : null; };
    return { eventos: ev, numero: txt('numero'), fonte: txt('fonte'), titulo: txt('titulo'),
             aviso: document.getElementById('aviso') ? txt('aviso') : '', W: innerWidth, H: innerHeight };
  };
"""


def injetar(html, d):
    """Põe a camada de eventos no HTML do grafico_cotacao (SVG, CSS e a entrada na timeline)."""
    P = posicoes(d)
    if html.count(ANCORA_SVG) != 1 or html.count(ANCORA_JS) != 1 or html.count("</style>") != 1:
        raise RuntimeError("o HTML do grafico_cotacao mudou: âncoras da camada de eventos não encontradas")
    C = G.CORES
    css = (f"  .ev-traco {{ stroke:{C['cinza']}; stroke-width:3; stroke-dasharray:6 7; }}\n"
           f"  .ev-ponto {{ fill:{C['tinta']}; stroke:{C['papel']}; stroke-width:4; }}\n"
           f"  .ev-texto {{ font:800 {CORPO}px {G.TEXTO}, sans-serif; fill:{C['tinta']}; paint-order:stroke; "
           f"stroke:{C['papel']}; stroke-width:12px; }}\n")
    js = "".join(f"  tl.set('#ev{p['k']}', {{ opacity: 0 }}, 0);\n"
                 f"  tl.fromTo('#ev{p['k']}', {{ opacity: 0, y: {8 if p['lado'] == 'cima' else -8} }}, "
                 f"{{ opacity: 1, y: 0, duration: .3, ease: 'power2.out', immediateRender: false }}, {p['t']});\n"
                 for p in P)
    html = html.replace("</style>", css + "</style>")
    html = html.replace(ANCORA_SVG, f'\n      <g id="eventos">{_svg(P)}</g>' + ANCORA_SVG)
    html = html.replace(ANCORA_JS, "  // eventos: acendem quando a ponta da linha passa pela data\n" + js + ANCORA_JS)
    return html.replace("</body>", '<script src="assets/tela.js"></script>\n</body>')


def montar_html(d, sfx=None, sfx_dur=1.0):
    d = validar(d)
    return injetar(G.montar_html(d, sfx, sfx_dur), d)


def gerar_projeto(d, destino):
    d = validar(d)
    caminho = G.gerar_projeto(d, destino)       # o gráfico inteiro (fontes, GSAP, som, créditos, meta)
    html = injetar(open(caminho).read(), d)
    open(caminho, "w").write(html)
    projeto.escrever_tela(destino, TELA)
    return caminho


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
    P = posicoes(d)
    print(f"ok: {caminho} (eventos, {len(P)} marcadores: "
          + "; ".join(f"{p['rotulo']} em {p['t']} s" for p in P) + ")")


if __name__ == "__main__":
    main()
