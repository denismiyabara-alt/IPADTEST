"""Gráficos em SVG gerados no build (DESENHO 5): leves, sem JavaScript, já no HTML.

Regras de desenho: uma série por gráfico (sem eixo duplo), linha de 2 px, barras finas com ponta
arredondada presa à linha de base, grade discreta, rótulo direto só no último ponto, e um <title>
em cada marca para o valor aparecer ao passar o mouse. Toda a tabela com os números fica logo abaixo
do gráfico, na página.
"""
from html import escape
from math import floor, log10

COR = "#123E72"       # mesma cor de destaque do plugin iec-ferramentas
COR2 = "#A9B1BA"
GRADE = "#EBEEF1"
EIXO = "#A3ABB4"
TEXTO = "#5C6570"


def passo_bonito(amplitude: float, alvo: int = 4) -> float:
    if amplitude <= 0:
        return 1
    bruto = amplitude / alvo
    pot = 10 ** floor(log10(bruto))
    n = bruto / pot
    return (1 if n <= 1 else 2 if n <= 2 else 2.5 if n <= 2.5 else 5 if n <= 5 else 10) * pot


def fmt_curto(v: float, moeda=True) -> str:
    a = abs(v)
    pre = "R$ " if moeda else ""
    if a >= 1e9:
        s = f"{v / 1e9:.1f} bi"
    elif a >= 1e6:
        s = f"{v / 1e6:.1f} mi"
    elif a >= 1e3:
        s = f"{v / 1e3:.1f} mil"
    else:
        s = f"{v:.2f}" if a < 100 else f"{v:.0f}"
    return pre + s.replace(".", ",")


def _ticks(vmin, vmax):
    vmin, vmax = min(vmin, 0) if vmin >= 0 else vmin, vmax
    p = passo_bonito(vmax - vmin)
    lo = floor(vmin / p) * p
    hi = -floor(-vmax / p) * p
    if hi == lo:
        hi = lo + p
    t, v = [], lo
    while v <= hi + p / 1e6:
        t.append(round(v, 10))
        v += p
    return lo, hi, t


def barras(itens: list[tuple[str, float | None]], titulo: str, moeda=True, fmt=None, largura=640, altura=240) -> str:
    """Barras verticais (aceita negativos). itens = [(rótulo, valor)]."""
    fmt = fmt or (lambda v: fmt_curto(v, moeda))
    vals = [v for _, v in itens if v is not None]
    if not vals:
        return ""
    lo, hi, ticks = _ticks(min(vals + [0]), max(vals + [0]))
    L, R, T, B = 64, 10, 12, 28
    W, H = largura, altura
    n = len(itens)
    banda = (W - L - R) / n
    bw = max(6, min(28, banda * 0.55))
    y = lambda v: T + (hi - v) / (hi - lo) * (H - T - B)  # noqa: E731
    out = [f'<svg class="graf" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(titulo)}">']
    for t in ticks:
        out.append(f'<line x1="{L}" x2="{W - R}" y1="{y(t):.1f}" y2="{y(t):.1f}" stroke="{EIXO if t == 0 else GRADE}" stroke-width="1"/>')
        out.append(f'<text x="{L - 6}" y="{y(t) + 4:.1f}" text-anchor="end">{escape(fmt(t))}</text>')
    for i, (rot, v) in enumerate(itens):
        cx = L + banda * (i + 0.5)
        if i % max(1, n // 12) == 0 or n <= 12:
            out.append(f'<text x="{cx:.1f}" y="{H - 8}" text-anchor="middle">{escape(rot)}</text>')
        if v is None:
            continue
        y0, y1 = y(0), y(v)
        top, h = min(y0, y1), max(1.5, abs(y1 - y0))
        r = min(4, bw / 2, h)
        # retângulo com cantos arredondados só na ponta oposta à linha de base
        x0 = cx - bw / 2
        if v >= 0:
            d = (f"M{x0:.1f},{y0:.1f} V{top + r:.1f} Q{x0:.1f},{top:.1f} {x0 + r:.1f},{top:.1f} "
                 f"H{x0 + bw - r:.1f} Q{x0 + bw:.1f},{top:.1f} {x0 + bw:.1f},{top + r:.1f} V{y0:.1f} Z")
        else:
            bot = top + h
            d = (f"M{x0:.1f},{y0:.1f} V{bot - r:.1f} Q{x0:.1f},{bot:.1f} {x0 + r:.1f},{bot:.1f} "
                 f"H{x0 + bw - r:.1f} Q{x0 + bw:.1f},{bot:.1f} {x0 + bw:.1f},{bot - r:.1f} V{y0:.1f} Z")
        out.append(f'<path d="{d}" fill="{COR}"><title>{escape(rot)}: {escape(fmt(v))}</title></path>')
    out.append("</svg>")
    return "".join(out)


def linha(pontos: list[tuple[str, float]], titulo: str, moeda=True, fmt=None, rotulo_x=None,
          largura=640, altura=240, base_zero=False, referencia: list[tuple[str, float]] | None = None,
          nome_ref: str = "") -> str:
    """Linha simples. `pontos` = [(data ISO, valor)]. `referencia` = segunda linha cinza (ex.: VP por cota)."""
    fmt = fmt or (lambda v: fmt_curto(v, moeda))
    pontos = [(d, v) for d, v in pontos if v is not None]
    if len(pontos) < 2:
        return ""
    if len(pontos) > 300:  # amostra semanal para o HTML ficar leve
        passo = len(pontos) / 300
        pontos = [pontos[int(i * passo)] for i in range(300)] + [pontos[-1]]
    vals = [v for _, v in pontos] + [v for _, v in (referencia or [])]
    vmin, vmax = (0 if base_zero else min(vals)), max(vals)
    if vmax == vmin:
        vmax = vmin + 1
    p = passo_bonito(vmax - vmin)
    lo, hi = floor(vmin / p) * p, -floor(-vmax / p) * p
    L, R, T, B = 64, 70, 12, 28
    W, H = largura, altura
    xs = {d: i for i, d in enumerate(sorted({d for d, _ in pontos} | {d for d, _ in (referencia or [])}))}
    n = max(1, len(xs) - 1)
    x = lambda d: L + xs[d] / n * (W - L - R)  # noqa: E731
    y = lambda v: T + (hi - v) / (hi - lo) * (H - T - B)  # noqa: E731
    out = [f'<svg class="graf" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(titulo)}">']
    t = lo
    while t <= hi + p / 1e6:
        out.append(f'<line x1="{L}" x2="{W - R}" y1="{y(t):.1f}" y2="{y(t):.1f}" stroke="{GRADE}" stroke-width="1"/>')
        out.append(f'<text x="{L - 6}" y="{y(t) + 4:.1f}" text-anchor="end">{escape(fmt(t))}</text>')
        t += p
    datas = sorted(xs)
    rot = rotulo_x or (lambda d: d[:4])
    vistos = set()
    for d in datas:
        r = rot(d)
        if r not in vistos and (not vistos or xs[d] - max(xs[k] for k in datas if rot(k) in vistos) >= len(datas) / 7):
            vistos.add(r)
            out.append(f'<text x="{x(d):.1f}" y="{H - 8}" text-anchor="middle">{escape(r)}</text>')
    if referencia and len(referencia) >= 2:
        dref = " ".join(("M" if i == 0 else "L") + f"{x(d):.1f},{y(v):.1f}" for i, (d, v) in enumerate(referencia))
        out.append(f'<path d="{dref}" fill="none" stroke="{COR2}" stroke-width="2" stroke-dasharray="5 4"/>')
        dl, vl = referencia[-1]
        out.append(f'<text x="{x(dl) + 6:.1f}" y="{y(vl) + 4:.1f}" class="rot">{escape(nome_ref)}</text>')
    dd = " ".join(("M" if i == 0 else "L") + f"{x(d):.1f},{y(v):.1f}" for i, (d, v) in enumerate(pontos))
    out.append(f'<path d="{dd}" fill="none" stroke="{COR}" stroke-width="2" stroke-linejoin="round"/>')
    for d, v in pontos[:: max(1, len(pontos) // 60)] + [pontos[-1]]:
        out.append(f'<circle cx="{x(d):.1f}" cy="{y(v):.1f}" r="6" fill="transparent"><title>{d[8:10] + "/" if len(d) > 7 else ""}{d[5:7]}/{d[:4]}: {escape(fmt(v))}</title></circle>')
    dl, vl = pontos[-1]
    out.append(f'<circle cx="{x(dl):.1f}" cy="{y(vl):.1f}" r="4" fill="{COR}" stroke="#fff" stroke-width="2"/>')
    out.append(f'<text x="{x(dl) + 8:.1f}" y="{y(vl) + 4:.1f}" class="rot">{escape(fmt(vl))}</text>')
    out.append("</svg>")
    return "".join(out)
