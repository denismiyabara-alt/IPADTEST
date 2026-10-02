#!/usr/bin/env python3
"""Modelo da meta e do ranking de temas (usado por meta.py, temas.py e calendario_v2.py).

Tudo sai de auditoria-canal/dados/ (Analytics + Studio). Sem rede. As escolhas do modelo estão documentadas
em cada função; os números de referência estão em META.md e TEMAS.md.

Equação da meta (por mês):
    líquidos = ganhos − perdas
    ganhos   = catálogo + Σ_formato Σ_assunto (vídeos novos × inscritos esperados por vídeo)
    inscritos esperados por vídeo = views intencionais medianas × inscritos por mil views intencionais
"catálogo" = inscritos que chegam por vídeos antigos e por fora de vídeos (página do canal, etc.), estimado como
ganhos do canal − inscritos dos vídeos publicados no mesmo trimestre.
"""
import math
import statistics
import sys
from collections import defaultdict
from datetime import date
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "auditoria-canal"))
import analisar as an  # noqa: E402

DADOS = AQUI.parent / "auditoria-canal" / "dados"
META, INICIO = 200_000, date(2026, 10, 1)
PRAZOS = [("31/12/2026", date(2026, 12, 31)), ("30/06/2027", date(2027, 6, 30)), ("31/12/2027", date(2027, 12, 31))]
JANELAS = {"12 meses": (30, 365), "vitalício": (30, 100_000)}
N_MIN = 3                       # assunto com menos vídeos que isso não entra no ranking
RAZAO_INTENC_SHORTS = 0.43      # views intencionais ÷ views dos Shorts em ago/26 (antes do efeito de 27/08)


def quantil(xs, p):
    xs = sorted(x for x in xs if x is not None)
    if not xs:
        return None
    k = (len(xs) - 1) * p
    f = int(math.floor(k))
    c = min(f + 1, len(xs) - 1)
    return xs[f] + (xs[c] - xs[f]) * (k - f)


def meses_ate(fim, ini=INICIO):
    """Meses (fração) entre ini e fim, contando o mês de ini inteiro."""
    return (fim.year - ini.year) * 12 + (fim.month - ini.month) + fim.day / 30.4


def carregar(pasta=DADOS):
    return an.Dados(pasta)


def engajadas(v):
    return v["engajadas"] if v["engajadas"] is not None else v["views"]


def videos(d, formato, janela, ref=None):
    """Vídeos do formato com idade dentro da janela (dias de vida), sem o outlier de Shorts (≥ 40% das views)."""
    ref = ref or d.data_ref
    lo, hi = JANELAS[janela]
    vs = [v for v in d.v.values() if v["formato"] == formato and v["publicado"]
          and lo <= (ref - v["publicado"]).days <= hi and engajadas(v) is not None]
    fora = an.outliers(vs)
    return [v for v in vs if v not in fora], fora


def trafego_por_video(d):
    t = defaultdict(lambda: defaultdict(float))
    for r in d.trafego_video:
        o = "BROWSE" if r["origem"] == "SUBSCRIBER" else r["origem"]
        t[r["video_id"]][o] += an.num(r["views"]) or 0
    return t


def resumo_grupo(vs, trafego=None):
    """n, views intencionais (p25/mediana/p75), inscritos por mil intencionais (somados), esperado por vídeo
    (mediana × taxa) e inscritos reais por vídeo (p25/mediana/p75); origem do tráfego se houver."""
    eng = [engajadas(v) for v in vs]
    g = [an.ganhos(v) for v in vs]
    taxa = an.por_mil(sum(g), sum(eng)) or 0
    r = {"n": len(vs), "eng_p25": quantil(eng, .25), "eng_med": quantil(eng, .5), "eng_p75": quantil(eng, .75),
         "insc_mil": taxa, "insc_p25": quantil(g, .25), "insc_med": quantil(g, .5), "insc_p75": quantil(g, .75),
         "insc_p90": quantil(g, .9), "insc_total": sum(g)}
    r["esperado"] = (r["eng_med"] or 0) * taxa / 1000
    r["esperado_p25"] = (r["eng_p25"] or 0) * taxa / 1000
    r["esperado_p75"] = (r["eng_p75"] or 0) * taxa / 1000
    if trafego is not None:
        cob = [trafego[v["id"]] for v in vs if v["id"] in trafego]
        tot = sum(sum(o.values()) for o in cob)
        r["n_trafego"] = len(cob)
        for k, o in (("busca", "YT_SEARCH"), ("navegacao", "BROWSE"), ("sugeridos", "RELATED_VIDEO")):
            r[f"pct_{k}"] = an.pct(sum(t.get(o, 0) for t in cob), tot) if tot else None
        r["perfil"] = perfil_trafego(r)
    return r


def perfil_trafego(r):
    if r.get("pct_busca") is None:
        return "sem dado"
    if r["pct_busca"] >= 25:
        return "Pesquisa (perene)"
    if (r.get("pct_navegacao") or 0) >= 50:
        return "Navegação (pico)"
    return "misto"


def ranking(d, formato, janela, n_min=N_MIN):
    vs, fora = videos(d, formato, janela)
    tr = trafego_por_video(d)
    grupos = defaultdict(list)
    for v in vs:
        grupos[an.assunto(v["titulo"])].append(v)
    linhas = []
    for nome, l in grupos.items():
        r = resumo_grupo(l, tr)
        r["assunto"] = nome
        r["ranqueado"] = r["n"] >= n_min
        linhas.append(r)
    linhas.sort(key=lambda r: (not r["ranqueado"], -r["esperado"]))
    total = resumo_grupo(vs, tr)
    total["assunto"] = "todos"
    return linhas, total, fora


# ------------------------------------------------------------------------------------------------ base de hoje
def base(d, atual=None):
    """Números de hoje: contador, ritmo líquido, perdas, catálogo, produção histórica e por vídeo."""
    m = an.meta(d) or {}
    atual = atual or m.get("atual") or 165_000
    mes = d.mes
    liq = [(r["mes"], (an.num(r["inscritos_ganhos"]) or 0) - (an.num(r["inscritos_perdidos"]) or 0)) for r in mes]
    perdas6 = statistics.mean(an.num(r["inscritos_perdidos"]) or 0 for r in mes[-6:])
    ganhos3 = statistics.mean(an.num(r["inscritos_ganhos"]) or 0 for r in mes[-3:])
    # catálogo: ganhos do último trimestre fechado − inscritos dos vídeos publicados nele, por mês
    ult = [r["mes"] for r in mes[-3:]]
    novos = sum(an.ganhos(v) for v in d.v.values() if v["publicado"] and f"{v['publicado']:%Y-%m}" in ult)
    catalogo = (sum(an.num(r["inscritos_ganhos"]) or 0 for r in mes[-3:]) - novos) / 3
    pub = defaultdict(lambda: {"longo": 0, "short": 0})
    for v in d.v.values():
        if v["publicado"] and f"{v['publicado']:%Y-%m}" >= "2024-01" and f"{v['publicado']:%Y-%m}" < f"{INICIO:%Y-%m}":
            pub[f"{v['publicado']:%Y-%m}"][v["formato"]] += 1
    lon = [p["longo"] for p in pub.values()]
    sho = [p["short"] for p in pub.values()]
    vl, _ = videos(d, "longo", "12 meses")
    vsh, _ = videos(d, "short", "12 meses")
    return {"atual": atual, "faltam": META - atual, "liq_ult": liq[-1][1], "mes_ult": liq[-1][0],
            "liq_6m": statistics.mean(x for _, x in liq[-6:]), "liq_melhor": max(liq, key=lambda x: x[1]),
            "perdas_6m": perdas6, "ganhos_3m": ganhos3, "catalogo": catalogo, "novos_trimestre": novos,
            "meses_trimestre": ult,
            "longos_mes_med": statistics.median(lon[-12:]), "longos_mes_max": max(lon),
            "shorts_mes_med": statistics.median(sho[-12:]), "shorts_mes_max": max(sho),
            "longo": resumo_grupo(vl), "short": resumo_grupo(vsh), "pub_ultimos": dict(pub)}


def origens_studio_shorts_sem_outlier(d, outlier="aDL4MMF6AnE"):
    """Views mensais de Shorts (Studio, Total.csv) menos as do "1 centavo" (Dados do gráfico.csv)."""
    vm = an.views_mensais_studio(d)
    graf = (d.studio.get("studio_conteudo_shorts") or {}).get("grafico") or []
    if not vm or not graf:
        return {}
    fora = defaultdict(float)
    for r in graf:
        if r.get("video_id", "").strip() == outlier:
            m = an.parse_mes(r.get("data", ""))
            if m:
                fora[m] += an.num(r.get("views")) or 0
    return {m: v - fora.get(m, 0) for m, v in vm["short"].items()}


# ------------------------------------------------------------------------------------------------ cenários
def cenario(b, prazo):
    meses = meses_ate(prazo)
    liq = b["faltam"] / meses
    ganhos = liq + b["perdas_6m"]
    novos = max(0.0, ganhos - b["catalogo"])
    L, S = b["longo"], b["short"]
    out = {"meses": meses, "liquidos": liq, "ganhos": ganhos, "novos": novos,
           "x_ritmo": liq / b["liq_6m"] if b["liq_6m"] else None}
    # produção necessária só com longos, por nível de desempenho por vídeo
    for nivel in ("insc_med", "insc_p75", "insc_p90"):
        out[f"longos_{nivel}"] = novos / L[nivel] if L[nivel] else None
    # inscritos por longo necessários, se a produção for a máxima histórica de longos
    out["insc_por_longo_no_max"] = novos / b["longos_mes_max"]
    # views intencionais necessárias por mês nos vídeos novos, na taxa atual dos longos
    out["views_intenc_novos"] = novos / (L["insc_mil"] / 1000) if L["insc_mil"] else None
    return out


def projecao(b, liq_mes):
    """Data em que chega a 200 mil com um ritmo líquido constante."""
    if liq_mes <= 0:
        return None
    meses = b["faltam"] / liq_mes
    ano, mes = INICIO.year, INICIO.month + int(meses)
    ano += (mes - 1) // 12
    mes = (mes - 1) % 12 + 1
    return date(ano, mes, 1), meses


# ------------------------------------------------------------------------------------------------ plano
def plano(d, b, mix_longos, n_shorts, nivel="esperado"):
    """Ganhos esperados por mês de um plano de produção: mix_longos = {assunto: vídeos por mês}.
    Usa o esperado por vídeo do assunto nos últimos 12 meses (ou o dos longos em geral, se o assunto tiver n < 3).
    Devolve o total e a faixa (p25-p75 das views intencionais × taxa)."""
    rk, tot, _ = ranking(d, "longo", "12 meses")
    por = {r["assunto"]: r for r in rk if r["ranqueado"]}
    ganho, lo, hi, linhas = 0.0, 0.0, 0.0, []
    for assunto, n in mix_longos.items():
        r = por.get(assunto, tot)
        e, e25, e75 = r["esperado"], r["esperado_p25"], r["esperado_p75"]
        ganho += n * e
        lo += n * e25
        hi += n * e75
        linhas.append((assunto, n, e, e25, e75, r["n"]))
    sh = b["short"]
    ganho += n_shorts * sh["esperado"]
    lo += n_shorts * sh["esperado_p25"]
    hi += n_shorts * sh["esperado_p75"]
    return {"novos": ganho, "novos_p25": lo, "novos_p75": hi, "linhas": linhas,
            "novos_shorts": n_shorts * sh["esperado"],
            "liquidos": b["catalogo"] + ganho - b["perdas_6m"],
            "liquidos_p25": b["catalogo"] + lo - b["perdas_6m"], "liquidos_p75": b["catalogo"] + hi - b["perdas_6m"]}
