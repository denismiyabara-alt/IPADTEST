"""Gráfico de cotação animado (HyperFrames) a partir de um JSON de dado real.

Uso:
  python3 grafico_cotacao/gerar.py exemplos/selic-16x9.json -o projetos/selic
  cd projetos/selic && npx hyperframes@0.8.78 render -o ../../renders/selic.mp4

O projeto gerado é uma pasta HyperFrames autocontida: index.html + assets/ (fontes OFL do molde Burry, GSAP e o
efeito de pouso). Nada vem de CDN na hora do render.

Entrada (JSON):
  titulo, kicker, fonte          textos. "fonte" é obrigatória e vai no canto ("Fonte: BCB (SGS 432)").
  formato                        "16:9" (1920x1080) ou "9:16" (1080x1920).
  duracao                        5 a 10 s (padrão 8).
  linha                          "linha" (cotação) ou "degrau" (Selic: o valor vale até a próxima decisão).
  unidade                        {"prefixo": "R$ ", "sufixo": "", "casas": 2}.
  variacao                       "pct" (variação %), "pp" (pontos percentuais) ou null.
  cor_final                      "vermelho", "verde" ou "cobre" (cores da PAL do molde Burry): número e ponto final.
  destaques                      [{"data": "AAAA-MM-DD", "rotulo": "...", "posicao": "acima"|"abaixo"}], até 3.
  som                            false, ou {"pouso": "impact-bass-1" | "caminho/arquivo.mp3" | "sintetico"}.
  serie                          [{"data": "AAAA-MM-DD", "valor": número}], em ordem, 2 pontos ou mais.
  rotulo_final (opcional)        texto sob o número; padrão "em 02/out/2026" (data do último ponto).
"""
import argparse, datetime as dt, json, math, os, re, shutil, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MOTION = os.path.dirname(AQUI)
NODE_MODULES = os.path.join(MOTION, "node_modules")
SFX_DIR = os.path.join(NODE_MODULES, "hyperframes", "dist", "skills", "media-use", "audio", "assets", "sfx")

sys.path.insert(0, os.path.join(MOTION, "comum"))
import estilo    # noqa: E402  — motion/comum/estilo.py: PAL e fontes lidas do molde Burry (broll/gerar.py)
import projeto   # noqa: E402  — motion/comum/projeto.py: CSS das fontes e busca no node_modules

PAL, _ = estilo.ler_molde()   # a PAL inteira (o gráfico usa também verde, cobre e paper)
FONTES_IEC = estilo.ESTILOS["iec"]["fontes"]

# papel de cada cor no gráfico → chave da PAL. Nenhum valor de cor mora aqui.
PAPEIS = dict(papel="bg", folha="paper", tinta="ink", cinza="gray", grade="faint",
              vermelho="red", verde="verde", cobre="cobre")
CORES = {papel: PAL[chave] for papel, chave in PAPEIS.items()}
CORES_FINAIS = ("vermelho", "verde", "cobre")   # cor do número final; os destaques usam cobre (ou tinta)
_familia = lambda papel_tipo: re.search(r"px(?:/[\d.]+)? '?([A-Za-z ]+?)'?,", estilo.TIPO[papel_tipo]).group(1)
TEXTO, NUMERO = _familia("rotulo"), _familia("numero")   # Montserrat, Archivo Black (do TIPO do módulo comum)
FORMATOS = {"16:9": (1920, 1080), "9:16": (1080, 1920)}
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
RESSALVA_PRECO = "Preço sem dividendos."   # COTAHIST: fechamento sem proventos; vai na TELA, não só no README
FRACAO_POUSO = 0.62   # a linha chega no último ponto (e o número "pousa") em 62% da duração
MAX_PONTOS = 600   # acima disso o SVG fica pesado; reduz guardando mínimo e máximo de cada faixa


# ---------------------------------------------------------------- dados
class DadosInvalidos(ValueError):
    pass


def validar(d):
    """Levanta DadosInvalidos com todos os problemas de uma vez. Devolve a entrada com padrões."""
    erros = []
    if not isinstance(d, dict):
        raise DadosInvalidos(["a entrada precisa ser um objeto JSON"])
    d = dict(d)
    d.setdefault("formato", "16:9")
    d.setdefault("duracao", 8.0)
    d.setdefault("linha", "linha")
    d.setdefault("unidade", {})
    d["unidade"] = {"prefixo": "", "sufixo": "", "casas": 2, **(d["unidade"] or {})}
    d.setdefault("variacao", None)
    d.setdefault("cor_final", "vermelho")
    d.setdefault("destaques", [])
    d.setdefault("som", False)
    d.setdefault("kicker", "")
    for campo in ("titulo", "fonte"):
        if not isinstance(d.get(campo), str) or not d[campo].strip():
            erros.append(f"'{campo}' é obrigatório (texto)")
    if isinstance(d.get("fonte"), str) and d["fonte"].strip() and not d["fonte"].lower().startswith("fonte"):
        erros.append("'fonte' deve começar com 'Fonte:' (regra do canal), ex.: 'Fonte: B3'")
    if d["formato"] not in FORMATOS:
        erros.append(f"'formato' deve ser 16:9 ou 9:16, veio {d['formato']!r}")
    if not isinstance(d["duracao"], (int, float)) or not 5 <= d["duracao"] <= 10:
        erros.append(f"'duracao' deve estar entre 5 e 10 s, veio {d['duracao']!r}")
    if d["linha"] not in ("linha", "degrau"):
        erros.append("'linha' deve ser 'linha' ou 'degrau'")
    if d["variacao"] not in (None, "pct", "pp"):
        erros.append("'variacao' deve ser 'pct', 'pp' ou null")
    if d["cor_final"] not in CORES_FINAIS:
        erros.append(f"'cor_final' deve ser um de {CORES_FINAIS} (cores da PAL; no máximo 2 cores de destaque)")
    casas = d["unidade"]["casas"]
    if not isinstance(casas, int) or not 0 <= casas <= 4:
        erros.append("'unidade.casas' deve ser inteiro de 0 a 4")
    serie = d.get("serie")
    if not isinstance(serie, list) or len(serie) < 2:
        erros.append("'serie' precisa de pelo menos 2 pontos")
        serie = []
    datas = []
    for i, p in enumerate(serie):
        try:
            data = dt.date.fromisoformat(p["data"])
            v = p["valor"]
            if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
                raise ValueError
        except (KeyError, TypeError, ValueError):
            erros.append(f"serie[{i}] inválido: {p!r} (esperado {{'data': 'AAAA-MM-DD', 'valor': número}})")
            continue
        if datas and data <= datas[-1]:
            erros.append(f"serie[{i}] fora de ordem ou repetido: {p['data']}")
        datas.append(data)
    if d["variacao"] == "pct" and serie and isinstance(serie[0].get("valor"), (int, float)) and serie[0]["valor"] <= 0:
        erros.append("variação % precisa de primeiro valor positivo")
    if not isinstance(d["destaques"], list) or len(d["destaques"]) > 3:
        erros.append("'destaques' é uma lista de no máximo 3 (mais que isso polui o celular)")
    else:
        for k, h in enumerate(d["destaques"]):
            try:
                hd = dt.date.fromisoformat(h["data"])
                if not h.get("rotulo"):
                    raise ValueError
            except (KeyError, TypeError, ValueError):
                erros.append(f"destaques[{k}] inválido: {h!r}")
                continue
            if datas and not datas[0] <= hd <= datas[-1]:
                erros.append(f"destaques[{k}] fora do período da série: {h['data']}")
            if h.get("posicao", "acima") not in ("acima", "abaixo"):
                erros.append(f"destaques[{k}].posicao deve ser 'acima' ou 'abaixo'")
    # classe + comparador/aviso: a regra de compliance (ver especificacao.py) vale também para JSON à mão
    if d.get("classe") not in ("ativo", "indicador"):
        erros.append("'classe' é obrigatória: 'ativo' (ação/FII, COTAHIST) ou 'indicador' (Selic, IPCA, CDI)")
    comp = d.get("comparador")
    if comp is not None:
        if not isinstance(comp, dict) or not comp.get("rotulo") or not comp.get("fonte"):
            erros.append("'comparador' precisa de rotulo, fonte e serie")
        else:
            cs = comp.get("serie")
            if not isinstance(cs, list) or len(cs) < 2:
                erros.append("'comparador.serie' precisa de pelo menos 2 pontos")
            else:
                cd = []
                for i, p in enumerate(cs):
                    try:
                        x = dt.date.fromisoformat(p["data"])
                        v = p["valor"]
                        if isinstance(v, bool) or not isinstance(v, (int, float)) or not math.isfinite(v):
                            raise ValueError
                    except (KeyError, TypeError, ValueError):
                        erros.append(f"comparador.serie[{i}] inválido: {p!r}")
                        continue
                    if cd and x <= cd[-1]:
                        erros.append(f"comparador.serie[{i}] fora de ordem: {p['data']}")
                    cd.append(x)
                if d.get("base100") and cs and isinstance(cs[0].get("valor"), (int, float)) and cs[0]["valor"] <= 0:
                    erros.append("base 100 precisa de primeiro valor positivo no comparador")
            comp.setdefault("linha", "linha")
    if d.get("base100") and serie and isinstance(serie[0].get("valor"), (int, float)) and serie[0]["valor"] <= 0:
        erros.append("base 100 precisa de primeiro valor positivo na série")
    if d.get("classe") == "ativo" and not comp and not (isinstance(d.get("aviso"), str) and d["aviso"].strip()):
        erros.append("compliance: ativo isolado precisa de 'comparador' (IBOV, IFIX ou CDI) desenhado junto "
                     "OU de 'aviso' na tela ('Não é recomendação de investimento.')")
    som = d["som"]
    if som not in (False, None) and not (isinstance(som, dict) and isinstance(som.get("pouso"), str)):
        erros.append("'som' deve ser false ou {'pouso': 'impact-bass-1' | caminho | 'sintetico'}")
    if erros:
        raise DadosInvalidos(erros)
    return d


def fmt_br(v, casas):
    """1234567.891, 2 -> '1.234.567,89' (igual ao fmtBR do JS da página)."""
    s = f"{abs(v):,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-" if v < 0 and round(abs(v), casas) else "") + s


def texto_valor(v, unidade):
    return f"{unidade['prefixo']}{fmt_br(v, unidade['casas'])}{unidade['sufixo']}"


def data_br(iso, dia=True):
    d = dt.date.fromisoformat(iso)
    return (f"{d.day:02d}/" if dia else "") + f"{MESES[d.month - 1]}/{d.year}"


def texto_variacao(d):
    s = d["serie"]
    a, b = s[0]["valor"], s[-1]["valor"]
    desde = data_br(s[0]["data"], dia=False)
    if d["variacao"] == "pp":
        x = b - a
        return f"{'+' if x >= 0 else '−'}{fmt_br(abs(x), 2)} p.p. desde {desde}"
    if d["variacao"] == "pct":
        x = (b / a - 1) * 100
        return f"{'+' if x >= 0 else '−'}{fmt_br(abs(x), 1)}% desde {desde}"
    return ""


def reduzir(pontos, n=MAX_PONTOS):
    """Mantém primeiro, último e o mínimo e o máximo de cada faixa (o pico nunca some)."""
    if len(pontos) <= n:
        return list(pontos)
    faixas = n // 2 - 1
    miolo = pontos[1:-1]
    tam = len(miolo) / faixas
    out = [pontos[0]]
    for k in range(faixas):
        fatia = miolo[int(k * tam):int((k + 1) * tam)]
        if not fatia:
            continue
        lo = min(fatia, key=lambda p: p["valor"])
        hi = max(fatia, key=lambda p: p["valor"])
        out += sorted({id(lo): lo, id(hi): hi}.values(), key=lambda p: p["data"])
    out.append(pontos[-1])
    return out


def escala_y(vmin, vmax, marcas=4):
    """Limites 'redondos' do eixo e as marcas da grade."""
    if vmax == vmin:
        vmin, vmax = vmin - 1, vmax + 1
    bruto = (vmax - vmin) / (marcas - 1)
    mag = 10 ** math.floor(math.log10(bruto))
    passo = next(m * mag for m in (1, 2, 2.5, 5, 10) if m * mag >= bruto)
    lo = math.floor(vmin / passo) * passo
    hi = math.ceil(vmax / passo) * passo
    if hi - lo < passo * 2:
        hi = lo + passo * 2
    n = int(round((hi - lo) / passo))
    return lo, hi, [lo + k * passo for k in range(n + 1)]


def tempo_da_ease(p):
    """Inverso de power1.inOut (GSAP): em que fração do tempo a ponta chega na fração p do eixo x."""
    p = min(max(p, 0.0), 1.0)
    return math.sqrt(p / 2) if p < 0.5 else 1 - math.sqrt((1 - p) * 2) / 2


# ---------------------------------------------------------------- layout
def layout(formato):
    W, H = FORMATOS[formato]
    if formato == "16:9":
        return dict(W=W, H=H, pad=96, kicker_y=92, titulo_y=136, titulo_px=84, num_px=190, num_x=W - 96, num_y=92,
                    num_alinha="right", num_largura=860, gx0=200, gx1=W - 140, gy0=480, gy1=930, fonte_y=H - 64, eixo_px=30)
    return dict(W=W, H=H, pad=72, kicker_y=200, titulo_y=246, titulo_px=88, num_px=230, num_x=72, num_y=470,
                num_alinha="left", num_largura=W - 2 * 72, gx0=170, gx1=W - 90, gy0=980, gy1=1500, fonte_y=1600, eixo_px=30)


def _caminho(xs, ys, degrau):
    c = [f"M{xs[0]},{ys[0]}"]
    for k in range(1, len(xs)):
        c.append(f"H{xs[k]}V{ys[k]}" if degrau else f"L{xs[k]},{ys[k]}")
    return "".join(c)


def plotados(pontos, base100):
    """Valores desenhados: os reais, ou base 100 na 1ª data (quando as unidades são diferentes)."""
    if not base100:
        return [p["valor"] for p in pontos]
    b = pontos[0]["valor"]
    return [100 * p["valor"] / b for p in pontos]


def geometria(d):
    L = layout(d["formato"])
    b100 = bool(d.get("base100"))
    pts = reduzir(d["serie"])
    comp = d.get("comparador")
    ini, fim = pts[0]["data"], pts[-1]["data"]
    cpts = reduzir([p for p in comp["serie"] if ini <= p["data"] <= fim]) if comp else []
    if comp and len(cpts) < 2:
        raise DadosInvalidos([f"comparador {comp['rotulo']}: menos de 2 pontos dentro de {ini} a {fim}"])
    t0 = dt.date.fromisoformat(ini).toordinal()
    t1 = dt.date.fromisoformat(fim).toordinal()
    vp, vc = plotados(pts, b100), plotados(cpts, b100) if comp else []
    lo, hi, marcas = escala_y(min(vp + vc), max(vp + vc))
    X = lambda iso: L["gx0"] + (dt.date.fromisoformat(iso).toordinal() - t0) / max(1, t1 - t0) * (L["gx1"] - L["gx0"])
    Y = lambda v: L["gy1"] - (v - lo) / (hi - lo) * (L["gy1"] - L["gy0"])
    xs = [round(X(p["data"]), 2) for p in pts]
    ys = [round(Y(v), 2) for v in vp]
    linha = _caminho(xs, ys, d["linha"] == "degrau")
    G = dict(L=L, pts=pts, xs=xs, ys=ys, linha=linha, area=linha + f"V{L['gy1']}H{xs[0]}Z",
             marcas=[(round(Y(m), 1), m) for m in marcas], anos=[], b100=b100, comp=None)
    if comp:
        cx = [round(X(p["data"]), 2) for p in cpts]
        cy = [round(Y(v), 2) for v in vc]
        G["comp"] = dict(linha=_caminho(cx, cy, comp.get("linha") == "degrau"), x_fim=cx[-1], y_fim=cy[-1],
                         rotulo=comp["rotulo"], fim_plot=vc[-1], fim_real=cpts[-1]["valor"], ini_real=cpts[0]["valor"])
    a0, a1 = dt.date.fromordinal(t0).year, dt.date.fromordinal(t1).year
    if a1 - a0 >= 2:
        G["anos"] = [(round(X(f"{ano}-01-01"), 1), str(ano)) for ano in range(a0 + 1, a1 + 1)]
    return G


def texto_comparador(d, G):
    """Rótulo da ponta do comparador: variação % em base 100; valor na unidade no mesmo eixo."""
    c = G["comp"]
    if G["b100"]:
        x = (c["fim_real"] / c["ini_real"] - 1) * 100
        return f"{c['rotulo']} {'+' if x >= 0 else '−'}{fmt_br(abs(x), 1)}%"
    return f"{c['rotulo']} {texto_valor(c['fim_real'], d['unidade'])}"


# ---------------------------------------------------------------- página
def montar_html(d, sfx_arquivo=None, sfx_duracao=1.0):
    d = validar(d)
    G = geometria(d)
    L, pts, xs, ys, linha, area, marcas, anos = (G[k] for k in ("L", "pts", "xs", "ys", "linha", "area", "marcas", "anos"))
    W, H, dur = L["W"], L["H"], float(d["duracao"])
    un = d["unidade"]
    cor_final = CORES[d["cor_final"]]
    t_desenho0 = 0.9
    t_pouso = round(dur * FRACAO_POUSO, 3)                # a linha chega no último ponto aqui
    t_variacao = round(t_pouso + 0.35, 3)
    destaques = []
    for k, h in enumerate(d["destaques"]):
        # ponto da série mais próximo (para trás) da data pedida
        i = max(j for j, p in enumerate(pts) if p["data"] <= h["data"]) if any(p["data"] <= h["data"] for p in pts) else 0
        hx, hy = xs[i], ys[i]
        frac = (hx - L["gx0"]) / (L["gx1"] - L["gx0"])
        t = t_desenho0 + tempo_da_ease(frac) * (t_pouso - t_desenho0)
        destaques.append(dict(k=k, x=hx, y=hy, t=round(t, 3), rotulo=h["rotulo"], acima=h.get("posicao", "acima") == "acima"))
    casas_eixo = 0 if all(abs(m - round(m)) < 1e-9 for _, m in marcas) else min(2, un["casas"])
    pre_eixo, suf_eixo = ("", "") if G["b100"] else (un["prefixo"].strip(), un["sufixo"])
    grade = "".join(
        f'<line x1="{L["gx0"]}" x2="{L["gx1"]}" y1="{y}" y2="{y}" class="grade"/>'
        f'<text x="{L["gx0"] - 22}" y="{y + 10}" class="eixo" text-anchor="end">{pre_eixo}{fmt_br(m, casas_eixo)}{suf_eixo}</text>'
        for y, m in marcas)
    # comparador: 2ª linha tracejada em cinza (cor discreta: não conta como cor de destaque) + legenda
    comp_svg = legenda = ""
    if G["comp"]:
        c = G["comp"]
        acima = c["y_fim"] < ys[-1]
        comp_svg = (f'<path id="linha-comp" d="{c["linha"]}"/>')
        comp_fim = (f'<g id="comp-fim"><circle cx="{c["x_fim"]}" cy="{c["y_fim"]}" r="9" class="comp-ponto"/>'
                    f'<text x="{c["x_fim"] - 20}" y="{c["y_fim"] + (-24 if acima else 46)}" text-anchor="end" '
                    f'class="comp-texto">{esc(texto_comparador(d, G))}</text></g>')
        comp_svg_fim = comp_fim
        ly = L["gy0"] - 70
        nome = d.get("nome_serie") or (d["kicker"].split("·")[0].strip() or "Série")
        legenda = (f'<g id="legenda"><line x1="{L["gx0"]}" x2="{L["gx0"] + 48}" y1="{ly}" y2="{ly}" class="leg-princ"/>'
                   f'<text x="{L["gx0"] + 62}" y="{ly + 11}" class="leg-texto">{esc(nome)}</text>'
                   f'<line x1="{L["gx0"] + 90 + 22 * len(nome)}" x2="{L["gx0"] + 138 + 22 * len(nome)}" y1="{ly}" y2="{ly}" class="leg-comp"/>'
                   f'<text x="{L["gx0"] + 152 + 22 * len(nome)}" y="{ly + 11}" class="leg-texto">{esc(c["rotulo"])}</text></g>')
        if G["b100"]:
            xb, yb = L["gx0"] + 200 + 22 * (len(nome) + len(c["rotulo"])), ly + 10
            if d["formato"] == "9:16":   # não cabe na mesma linha: vai para a linha de cima
                xb, yb = L["gx0"], ly - 40
            legenda = legenda[:-4] + (f'<text x="{xb}" y="{yb}" class="eixo">'
                                      f'base 100 = {data_br(pts[0]["data"])}</text></g>')
    else:
        comp_svg_fim = ""
    eixo_x = "".join(f'<line x1="{x}" x2="{x}" y1="{L["gy1"]}" y2="{L["gy1"] + 14}" class="marca"/>'
                     f'<text x="{x}" y="{L["gy1"] + 52}" class="eixo" text-anchor="middle">{a}</text>'
                     for x, a in anos if L["gx0"] + 60 < x < L["gx1"] - 20)
    if not anos:
        eixo_x = (f'<text x="{L["gx0"]}" y="{L["gy1"] + 52}" class="eixo" text-anchor="start">{data_br(pts[0]["data"], False)}</text>'
                  f'<text x="{L["gx1"]}" y="{L["gy1"] + 52}" class="eixo" text-anchor="end">{data_br(pts[-1]["data"], False)}</text>')
    marcadores = ""
    for h in destaques:
        dy = -46 if h["acima"] else 74
        anc = "end" if h["x"] > (L["gx0"] + L["gx1"]) / 2 else "start"
        dx = 18 if anc == "start" else -18
        marcadores += (f'<g id="dq{h["k"]}" class="destaque" style="transform-origin:{h["x"]}px {h["y"]}px">'
                       f'<circle cx="{h["x"]}" cy="{h["y"]}" r="11" class="dq-ponto"/>'
                       f'<text x="{h["x"] + dx}" y="{h["y"] + dy}" text-anchor="{anc}" class="dq-texto">{esc(h["rotulo"])}</text></g>')
    final_txt = texto_valor(pts[-1]["valor"], un)
    # Archivo Black é larga (~0,6 em por caractere): o corpo do número cabe na largura do placar no pior caso
    # (o texto mais longo que a contagem mostra). 0,66 em/caractere dá folga sobre os ~0,6 medidos no render.
    mais_longo = max(len(texto_valor(p["valor"], un)) for p in pts)
    num_px = min(L["num_px"], int(L["num_largura"] / (0.66 * mais_longo)))
    rotulo_final = d.get("rotulo_final") or f"em {data_br(pts[-1]['data'])}"
    variacao = texto_variacao(d)
    fontes_css = projeto.css_fontes("iec")
    audio = ""
    if sfx_arquivo:
        audio = (f'<audio id="sfx-pouso" src="assets/{sfx_arquivo}" data-start="{max(0, t_pouso - 0.03):.3f}" '
                 f'data-duration="{sfx_duracao:.3f}" data-track-index="91" data-volume="0.6"></audio>')
    js_dados = json.dumps(dict(xs=xs, ys=ys, vs=[p["valor"] for p in pts], degrau=d["linha"] == "degrau",
                               gx0=L["gx0"], gx1=L["gx1"], pre=un["prefixo"], suf=un["sufixo"], casas=un["casas"],
                               t0=t_desenho0, t1=t_pouso, tv=t_variacao, dur=dur,
                               dq=[dict(k=h["k"], t=h["t"]) for h in destaques]), ensure_ascii=False)
    return TEMPLATE.format(
        W=W, H=H, dur=f"{dur:.3f}", fontes_css=fontes_css, **CORES, cor_final=cor_final,
        cor_dq=CORES["tinta"] if d["cor_final"] == "cobre" else CORES["cobre"], texto=TEXTO, numero=NUMERO,
        ressalva=(f'<div id="ressalva">{esc(RESSALVA_PRECO)}</div>' if d.get("classe") == "ativo" else ""),
        titulo=esc(d["titulo"]), kicker=esc(d["kicker"]), fonte=esc(d["fonte"]),
        titulo_px=L["titulo_px"], num_px=num_px, pad=L["pad"], kicker_y=L["kicker_y"], titulo_y=L["titulo_y"],
        num_x=L["num_x"] if L["num_alinha"] == "left" else W - L["num_x"], num_lado="left" if L["num_alinha"] == "left" else "right",
        num_y=L["num_y"], num_alinha=L["num_alinha"], fonte_y=L["fonte_y"], eixo_px=L["eixo_px"],
        titulo_largura=W - 2 * L["pad"] - (760 if d["formato"] == "16:9" else 0),
        gx0=L["gx0"], gx1=L["gx1"], gy0=L["gy0"] - 40, gy1=L["gy1"] + 10, gh=L["gy1"] - L["gy0"] + 60,
        linhas_grade=grade, eixo_x=eixo_x, linha=linha, area=area, marcadores=marcadores,
        comp_svg=comp_svg, comp_fim=comp_svg_fim, legenda=legenda,
        aviso=f'<div id="aviso">{esc(d["aviso"])}</div>' if d.get("aviso") else "",
        rodape_dir="column" if d["formato"] == "9:16" else "row",
        x_fim=xs[-1], y_fim=ys[-1], final_txt=esc(final_txt), inicial_txt=esc(texto_valor(pts[0]["valor"], un)),
        rotulo_final=esc(rotulo_final), variacao=esc(variacao), audio=audio, dados=js_dados,
        formato=d["formato"])


def esc(s):
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
            .replace("{", "&#123;").replace("}", "&#125;"))


# ---------------------------------------------------------------- som
def preparar_som(d, assets):
    """-> (nome do arquivo em assets/, duração) ou (None, 0)."""
    som = d.get("som")
    if not som:
        return None, 0
    pedido = som["pouso"]
    origem = None
    if pedido == "sintetico":
        destino = os.path.join(assets, "pouso.wav")
        sintetizar_pouso(destino)
        return "pouso.wav", 0.6
    if os.path.exists(pedido):
        origem = pedido
    elif os.path.exists(os.path.join(SFX_DIR, pedido + ".mp3")):
        origem = os.path.join(SFX_DIR, pedido + ".mp3")
    else:
        for base in (os.path.expanduser("~/.claude/skills/media-use/audio/assets/sfx"),):
            if os.path.exists(os.path.join(base, pedido + ".mp3")):
                origem = os.path.join(base, pedido + ".mp3")
    if not origem:
        print(f"aviso: efeito '{pedido}' não encontrado (rode npm install); usando o sintético", file=sys.stderr)
        destino = os.path.join(assets, "pouso.wav")
        sintetizar_pouso(destino)
        return "pouso.wav", 0.6
    nome = "pouso" + os.path.splitext(origem)[1]
    shutil.copy(origem, os.path.join(assets, nome))
    return nome, duracao_audio(origem)


def duracao_audio(caminho):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", caminho],
                             capture_output=True, text=True, check=True).stdout
        return min(float(out), 3.0)
    except Exception:
        return 1.5


def sintetizar_pouso(destino):
    """'Tum' grave curto feito no ffmpeg (seno 70 Hz com queda rápida + clique filtrado). Só reserva:
    o Denis achou SFX sintetizado 'muito ruim' no TRXF11; o padrão é a biblioteca (impact-bass-1)."""
    filtro = ("sine=f=70:d=0.6,volume=0.9,afade=t=out:st=0.02:d=0.55:curve=exp[a];"
              "anoisesrc=d=0.05:c=pink:a=0.5,lowpass=f=1800,afade=t=out:st=0:d=0.05[b];"
              "[a][b]amix=inputs=2:normalize=0,alimiter=limit=0.9")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-filter_complex", filtro, "-ar", "48000", "-ac", "2", destino], check=True)


# ---------------------------------------------------------------- projeto
def gerar_projeto(d, destino):
    d = validar(d)
    assets = os.path.join(destino, "assets")
    os.makedirs(os.path.join(assets, "fonts"), exist_ok=True)
    for arq, _, _ in FONTES_IEC.values():
        o = projeto.achar(arq)
        if not o:
            raise SystemExit(f"falta a fonte {arq} em node_modules. Rode: cd motion && npm install")
        shutil.copy(o, os.path.join(assets, "fonts", os.path.basename(arq)))
    faltando = []
    gsap = os.path.join(NODE_MODULES, "gsap", "dist", "gsap.min.js")
    if os.path.exists(gsap):
        shutil.copy(gsap, os.path.join(assets, "gsap.min.js"))
    else:
        faltando.append("gsap/dist/gsap.min.js")
    if faltando:
        raise SystemExit(f"faltam dependências em {NODE_MODULES}: {faltando}. Rode: cd motion && npm install")
    sfx, sfx_dur = preparar_som(d, assets)
    open(os.path.join(destino, "index.html"), "w").write(montar_html(d, sfx, sfx_dur))
    W, H = FORMATOS[d["formato"]]
    json.dump({"id": "grafico-cotacao", "name": d["titulo"], "width": W, "height": H}, open(os.path.join(destino, "meta.json"), "w"),
              ensure_ascii=False)
    json.dump(d, open(os.path.join(destino, "entrada.json"), "w"), ensure_ascii=False, indent=1)
    open(os.path.join(assets, "CREDITOS.txt"), "w").write(
        "Fontes: " + ", ".join(sorted({fam for _, fam, _ in FONTES_IEC.values()}))
        + " (SIL Open Font License 1.1), via @fontsource no npm; escolhidas pelo broll/gerar.py do molde Burry.\n"
        "GSAP 3.14.2 (licença padrão sem custo da GreenSock/Webflow), via npm.\n"
        + ("Efeito de pouso: biblioteca media-use do HyperFrames, Pixabay Content License (uso comercial, sem atribuição).\n"
           if sfx and not sfx.endswith(".wav") else "Efeito de pouso: sintetizado localmente com ffmpeg.\n" if sfx else ""))
    return os.path.join(destino, "index.html")


TEMPLATE = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<script src="assets/gsap.min.js"></script>
<style>
  {fontes_css}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{papel}; }}
  #root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; color:{tinta};
           background:{papel}; font-family:{texto}, sans-serif; }}
  #grain {{ position:absolute; inset:0; opacity:.08; pointer-events:none; }}
  .cena {{ position:absolute; inset:0; }}
  #kicker {{ position:absolute; left:{pad}px; top:{kicker_y}px; font:800 30px {texto}, sans-serif;
             letter-spacing:.14em; text-transform:uppercase; color:{cinza}; }}
  #titulo {{ position:absolute; left:{pad}px; top:{titulo_y}px; width:{titulo_largura}px; font:800 {titulo_px}px/1.08 {texto}, sans-serif;
             letter-spacing:-.02em; }}
  #placar {{ position:absolute; {num_lado}:{num_x}px; top:{num_y}px; text-align:{num_alinha}; }}
  #numero {{ font:400 {num_px}px/1 '{numero}', sans-serif; font-variant-numeric:tabular-nums; letter-spacing:.01em;
             display:inline-block; transform-origin:{num_alinha} center; white-space:nowrap; }}
  #rotulo-final {{ font:800 34px {texto}, sans-serif; color:{cinza}; margin-top:14px; }}
  #variacao {{ display:inline-block; margin-top:16px; font:800 38px {texto}, sans-serif; color:{cor_final};
               border:4px solid {cor_final}; border-radius:10px; padding:6px 18px; }}
  #grafico {{ position:absolute; left:0; top:0; }}
  .grade {{ stroke:{grade}; stroke-width:2; }}
  .marca {{ stroke:{cinza}; stroke-width:3; }}
  .eixo {{ font:700 {eixo_px}px {texto}, sans-serif; fill:{cinza}; }}
  #area {{ fill:{tinta}; opacity:.06; }}
  #linha {{ fill:none; stroke:{tinta}; stroke-width:7; stroke-linejoin:round; stroke-linecap:round; }}
  #ponta {{ fill:{tinta}; }}
  #ponto-final {{ fill:{cor_final}; }}
  #anel {{ fill:none; stroke:{cor_final}; stroke-width:5; }}
  .dq-ponto {{ fill:{cor_dq}; stroke:{papel}; stroke-width:4; }}
  .dq-texto {{ font:800 36px {texto}, sans-serif; fill:{cor_dq}; paint-order:stroke; stroke:{papel}; stroke-width:14px; }}
  #rodape {{ position:absolute; left:{pad}px; right:{pad}px; top:{fonte_y}px; display:flex; flex-direction:{rodape_dir};
             justify-content:space-between; gap:8px 32px; font:700 26px/1.3 {texto}, sans-serif; }}
  #avisos {{ display:flex; gap:24px; white-space:nowrap; color:{tinta}; }}
  #fonte {{ color:{cinza}; }}
  #aviso {{ color:{tinta}; white-space:nowrap; }}
  #linha-comp {{ fill:none; stroke:{cinza}; stroke-width:5; stroke-dasharray:16 10; stroke-linejoin:round; }}
  .comp-ponto {{ fill:{cinza}; }}
  .comp-texto {{ font:800 34px {texto}, sans-serif; fill:{cinza}; paint-order:stroke; stroke:{papel}; stroke-width:12px; }}
  .leg-princ {{ stroke:{tinta}; stroke-width:7; }}
  .leg-comp {{ stroke:{cinza}; stroke-width:5; stroke-dasharray:16 10; }}
  .leg-texto {{ font:800 32px {texto}, sans-serif; fill:{tinta}; }}
</style>
</head>
<body>
<div id="root" data-composition-id="grafico" data-start="0" data-width="{W}" data-height="{H}" data-duration="{dur}" data-formato="{formato}">
  <svg width="0" height="0" style="position:absolute"><filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="7"/><feColorMatrix type="saturate" values="0"/></filter></svg>
  <svg id="grain" width="{W}" height="{H}"><rect width="100%" height="100%" filter="url(#noise)"/></svg>
  <section id="cena" class="clip cena" data-start="0" data-duration="{dur}" data-track-index="1">
    <div id="kicker">{kicker}</div>
    <div id="titulo">{titulo}</div>
    <div id="placar">
      <div><span id="numero">{inicial_txt}</span></div>
      <div id="rotulo-final">{rotulo_final}</div>
      <div id="variacao">{variacao}</div>
    </div>
    <svg id="grafico" width="{W}" height="{H}" viewBox="0 0 {W} {H}">
      <defs><clipPath id="revela"><rect id="cortina" x="{gx0}" y="0" width="0" height="{H}"/></clipPath></defs>
      <g id="eixos">{linhas_grade}{eixo_x}</g>
      <g clip-path="url(#revela)">
        <path id="area" d="{area}"/>
        {comp_svg}
        <path id="linha" d="{linha}"/>
      </g>
      {legenda}
      <circle id="ponta" cx="{gx0}" cy="0" r="12"/>
      <circle id="anel" cx="{x_fim}" cy="{y_fim}" r="16" opacity="0"/>
      <circle id="ponto-final" cx="{x_fim}" cy="{y_fim}" r="15" opacity="0"/>
      {comp_fim}
      {marcadores}
    </svg>
    <div id="rodape"><div id="fonte">{fonte}</div><div id="avisos">{ressalva}{aviso}</div></div>
  </section>
  {audio}
</div>
<script>
  const D = {dados};
  window.__grafico = D;
  const tl = gsap.timeline({{ paused: true }});
  // 1234567.8 -> "1.234.567,8" sem depender do locale do Chrome (igual ao fmt_br do gerar.py)
  function fmtBR(v, casas) {{
    const neg = v < 0 && Math.abs(v).toFixed(casas) !== (0).toFixed(casas);
    const [i, d] = Math.abs(v).toFixed(casas).split('.');
    return (neg ? '-' : '') + i.replace(/\B(?=(\d{{3}})+(?!\d))/g, '.') + (d ? ',' + d : '');
  }}
  // valor e altura da linha na posição x (degrau: vale o último ponto; linha: interpola)
  function naPosicao(x) {{
    const xs = D.xs, n = xs.length;
    if (x >= xs[n - 1]) return {{ y: D.ys[n - 1], v: D.vs[n - 1] }};
    let lo = 0, hi = n - 1;
    while (hi - lo > 1) {{ const m = (lo + hi) >> 1; if (xs[m] <= x) lo = m; else hi = m; }}
    if (D.degrau) return {{ y: D.ys[lo], v: D.vs[lo] }};
    const f = (x - xs[lo]) / Math.max(1e-9, xs[hi] - xs[lo]);
    return {{ y: D.ys[lo] + (D.ys[hi] - D.ys[lo]) * f, v: D.vs[lo] + (D.vs[hi] - D.vs[lo]) * f }};
  }}
  const cortina = document.getElementById('cortina'), ponta = document.getElementById('ponta'),
        numero = document.getElementById('numero');
  const prog = {{ p: 0 }};
  function desenhar() {{
    const x = D.gx0 + (D.gx1 - D.gx0) * prog.p;
    const r = prog.p >= 1 ? {{ y: D.ys[D.ys.length - 1], v: D.vs[D.vs.length - 1] }} : naPosicao(x);
    cortina.setAttribute('width', prog.p > 0 ? x - D.gx0 + 8 : 0);
    ponta.setAttribute('cx', x); ponta.setAttribute('cy', r.y);
    numero.textContent = D.pre + fmtBR(r.v, D.casas) + D.suf;
  }}
  desenhar();

  // 1. entrada do texto
  tl.from('#kicker', {{ opacity: 0, y: 24, duration: .4, ease: 'power2.out' }}, 0);
  tl.from('#titulo', {{ opacity: 0, y: 60, duration: .55, ease: 'back.out(1.4)' }}, .12);
  tl.from('#placar', {{ opacity: 0, y: 40, duration: .5, ease: 'power2.out' }}, .35);
  tl.from('#eixos', {{ opacity: 0, duration: .5, ease: 'power1.out' }}, .45);
  tl.set('#ponta', {{ opacity: 0 }}, 0);
  tl.set('#ponta', {{ opacity: 1 }}, D.t0 - .2);
  tl.from('#rodape', {{ opacity: 0, duration: .4 }}, .6);
  if (document.getElementById('legenda')) tl.from('#legenda', {{ opacity: 0, duration: .4 }}, .55);
  if (document.getElementById('comp-fim')) tl.fromTo('#comp-fim', {{ opacity: 0 }}, {{ opacity: 1, duration: .35 }}, D.t1 + .2);
  tl.set(['#variacao', '#rotulo-final'], {{ opacity: 0 }}, 0);
  // 2. a linha se desenha e o número acompanha a ponta (é o valor real da série naquele ponto)
  tl.to(prog, {{ p: 1, duration: D.t1 - D.t0, ease: 'power1.inOut', onUpdate: desenhar }}, D.t0);
  // 3. destaques acendem quando a ponta passa por eles
  D.dq.forEach(h => tl.from('#dq' + h.k, {{ opacity: 0, scale: .4, duration: .4, ease: 'back.out(2.2)' }}, h.t));
  // 4. pouso: o número final ganha a cor e um pulso; o anel abre uma vez
  tl.set('#ponta', {{ opacity: 0 }}, D.t1);
  tl.to('#ponto-final', {{ opacity: 1, duration: .01 }}, D.t1);
  tl.fromTo('#anel', {{ opacity: .9, scale: 1, transformOrigin: 'center' }},
            {{ opacity: 0, scale: 3.2, duration: .7, ease: 'power2.out', immediateRender: false }}, D.t1);
  tl.to('#numero', {{ color: '{cor_final}', duration: .15 }}, D.t1);
  tl.fromTo('#numero', {{ scale: 1 }}, {{ scale: 1.12, duration: .14, ease: 'power2.out', yoyo: true, repeat: 1, immediateRender: false }}, D.t1);
  tl.to('#rotulo-final', {{ opacity: 1, duration: .3 }}, D.t1 + .1);
  tl.fromTo('#variacao', {{ opacity: 0, y: 16 }}, {{ opacity: 1, y: 0, duration: .4, ease: 'power2.out' }}, D.tv);
  // fecha a timeline na duração exata
  tl.set({{}}, {{}}, D.dur);
  window.__timelines = window.__timelines || {{}};
  window.__timelines["grafico"] = tl;
</script>
</body>
</html>
"""


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("entrada", help="JSON de entrada (ver serie.py)")
    ap.add_argument("-o", "--saida", required=True, help="pasta do projeto HyperFrames a criar")
    a = ap.parse_args(argv)
    try:
        d = json.load(open(a.entrada))
        caminho = gerar_projeto(d, a.saida)
    except DadosInvalidos as e:
        raise SystemExit("entrada inválida:\n  - " + "\n  - ".join(e.args[0]))
    d = validar(d)
    print(f"ok: {caminho} ({d['formato']}, {d['duracao']} s, {len(d['serie'])} pontos, "
          f"final = {texto_valor(d['serie'][-1]['valor'], d['unidade'])})")


if __name__ == "__main__":
    main()
