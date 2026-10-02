#!/usr/bin/env python3
"""Desdobra a meta de 200 mil inscritos: árvore, cenários de prazo, plano recomendado, metas mensais e semanais
e sensibilidade das alavancas. Gera META.md e meta.csv. Sem rede; dados de auditoria-canal/dados/.

uso: python3 meta.py
"""
import csv
import statistics
from datetime import date, timedelta
from pathlib import Path

import modelo as mo
from modelo import an

AQUI = Path(__file__).resolve().parent

# Plano recomendado (vídeos por mês), escolhido pelo ranking de inscritos esperados por vídeo (TEMAS.md):
# 12 longos/mês = o máximo que o canal já publicou num mês (fev e set/2024); 8 Shorts/mês.
PLANO_LONGOS = {"renda mensal": 4.3, "tesouro e renda fixa": 2, "crise e macro": 1.5, "cripto": 1,
                "FII": 1.2, "ações e empresas": 2}
PLANO_SHORTS = 8
RAMPA = {"2026-10": 0.75, "2026-11": 1.0}       # out/26 começa com 9 longos (calendário v2), depois 12
DEFASAGEM = (0.6, 0.25, 0.15)                    # parte dos inscritos de um vídeo no mês de publicação, +1, +2
MESES_PLANO = 15                                 # out/26 a dez/27


def mes_seq(n, ini=mo.INICIO):
    out, a, m = [], ini.year, ini.month
    for _ in range(n):
        out.append(f"{a}-{m:02d}")
        m += 1
        if m > 12:
            a, m = a + 1, 1
    return out


def metas_mensais(b, p, meses=MESES_PLANO, rampa=RAMPA, defasagem=DEFASAGEM):
    """Inscritos líquidos esperados por mês com o plano p (de modelo.plano), com rampa de produção e defasagem."""
    seq = mes_seq(meses)
    prod = [rampa.get(m, 1.0) for m in seq]          # a rampa vale para os longos; Shorts já começam em 8
    novos = [0.0] * meses
    shorts = p.get("novos_shorts", 0.0)
    for i, f in enumerate(prod):
        for k, w in enumerate(defasagem):
            if i + k < meses:
                novos[i + k] += (f * (p["novos"] - shorts) + shorts) * w
    out, acum = [], b["atual"]
    for i, m in enumerate(seq):
        liq = b["catalogo"] + novos[i] - b["perdas_6m"]
        acum += liq
        out.append({"mes": m, "fator_producao": prod[i], "ganhos": b["catalogo"] + novos[i], "perdas": b["perdas_6m"],
                    "liquidos": liq, "inscritos_fim_mes": acum,
                    "longos": round(sum(PLANO_LONGOS.values()) * prod[i]), "shorts": PLANO_SHORTS})
    return out


def data_meta(b, mensal, liq_regime):
    """Mês em que passa de 200 mil: usa as metas mensais e, depois delas, o regime constante."""
    acum = b["atual"]
    for r in mensal:
        acum = r["inscritos_fim_mes"]
        if acum >= mo.META:
            return r["mes"]
    if liq_regime <= 0:
        return None
    falta = mo.META - acum
    extra = int(-(-falta // liq_regime))
    ult = mensal[-1]["mes"]
    a, m = int(ult[:4]), int(ult[5:]) + extra
    a += (m - 1) // 12
    m = (m - 1) % 12 + 1
    return f"{a}-{m:02d}"


def alavancas(d, b):
    """Inscritos por mês que cada alavanca acrescenta (central, mínimo, máximo), com a base de cada número."""
    rk, tot, _ = mo.ranking(d, "longo", "12 meses")
    por = {r["assunto"]: r for r in rk if r["ranqueado"]}
    rm, te, ac = por["renda mensal"], por["tesouro e renda fixa"], por["ações e empresas"]
    sh = b["short"]
    vm = an.views_mensais_studio(d)
    # Shorts: views de Shorts SEM o "1 centavo" (Studio, Total − gráfico do outlier) caíram com a produção
    so = mo.origens_studio_shorts_sem_outlier(d)
    perda_views = (statistics.mean([so.get("2026-06", 0), so.get("2026-07", 0)])
                   - statistics.mean([so.get("2026-08", 0), so.get("2026-09", 0)])) if so else 0
    mod = an.modelo_inscritos(d)
    shorts_hoje = statistics.mean([b["pub_ultimos"]["2026-08"]["short"], b["pub_ultimos"]["2026-09"]["short"]])
    extra_sh = max(0.0, mo_plano_shorts() - shorts_hoje)
    st = an.origens_studio(d)
    busca_longos = statistics.mean(st["longos"][m].get("YT_SEARCH", 0) for m in mes_seq(6, date(2026, 4, 1)))
    ref = d.data_ref
    old = [v for v in d.v.values() if v["publicado"] and (ref - v["publicado"]).days > 365]
    rendimento_catalogo = b["catalogo"] / sum(an.ganhos(v) for v in old)
    fora = sorted((r for r in d.fora_do_publico if r["formato"] == "longo"),
                  key=lambda r: -(an.num(r.get("inscritos_ganhos")) or 0))
    insc30 = sum(an.num(r.get("inscritos_ganhos")) or 0 for r in fora[:30])
    L = [
        {"alavanca": "+1 longo por semana da série de renda mensal (+4,3 por mês)",
         "central": 4.3 * rm["esperado"], "min": 4.3 * rm["esperado_p25"], "max": 4.3 * rm["esperado_p75"],
         "base": f"renda mensal, longos dos últimos 12 meses (n = {rm['n']}): {br(rm['eng_med'])} views intencionais "
                 f"medianas × {br(rm['insc_mil'], 1)} inscritos por mil = {br(rm['esperado'])} por vídeo "
                 f"(faixa p25–p75: {br(rm['esperado_p25'])}–{br(rm['esperado_p75'])})"},
        {"alavanca": "+1 longo por mês de Tesouro e renda fixa (Copom e marcação)",
         "central": te["esperado"], "min": te["esperado_p25"], "max": te["esperado_p75"],
         "base": f"tesouro e renda fixa, 12 meses (n = {te['n']}): {br(te['esperado'])} por vídeo "
                 f"({br(te['esperado_p25'])}–{br(te['esperado_p75'])}); amostra pequena, puxada por 2 vídeos top"},
        {"alavanca": "Trocar 2 longos/mês de 'ações e empresas' por renda mensal",
         "central": 2 * (rm["esperado"] - ac["esperado"]), "min": 2 * (rm["esperado_p25"] - ac["esperado_p75"]),
         "max": 2 * (rm["esperado_p75"] - ac["esperado_p25"]),
         "base": f"ações e empresas é o assunto mais produzido (n = {ac['n']} em 12 meses) e rende {br(ac['esperado'])} "
                 f"por vídeo, contra {br(rm['esperado'])} da renda mensal"},
        {"alavanca": "Republicar (ou regravar) os 30 maiores dos 285 longos fora do ar",
         "central": 0.75 * insc30 * rendimento_catalogo, "min": 0.5 * insc30 * rendimento_catalogo,
         "max": insc30 * rendimento_catalogo,
         "base": f"os 30 maiores somam {br(insc30)} inscritos vitalícios; o catálogo público rende "
                 f"{br(100 * rendimento_catalogo, 2)}% dos inscritos vitalícios por mês ({br(b['catalogo'])}/mês); faixa "
                 "de 50% a 100% desse rendimento (o conteúdo é de 2019-2022 e pode estar desatualizado)"},
        {"alavanca": f"Voltar a {mo_plano_shorts()} Shorts por mês (hoje {br(shorts_hoje, 1)})",
         "central": extra_sh * sh["esperado"], "min": extra_sh * sh["esperado_p25"],
         "max": max(extra_sh * sh["esperado_p75"], perda_views * (mod["b"] / 1000 if mod else 0)),
         "base": f"por vídeo, um Short novo traz {br(sh['esperado'], 1)} inscrito (n = {sh['n']}, 12 meses, sem o "
                 f"'1 centavo'); o máximo usa a regressão mensal ({br(mod['b'], 2)} por mil) sobre as "
                 f"{br(perda_views)} views de Shorts (sem o '1 centavo') que sumiram de jun-jul para ago-set"},
        {"alavanca": "Reduzir as perdas em 10%",
         "central": 0.10 * b["perdas_6m"], "min": 0.0, "max": 0.20 * b["perdas_6m"],
         "base": f"perdas médias de {br(b['perdas_6m'])}/mês (6 meses); quase nada é atribuível a vídeo "
                 "(3.959 perdas por vídeo no vitalício), então a alavanca é fraca e incerta"},
        {"alavanca": "Subir o CTR da Pesquisa nos longos em 1 p.p. (12,3% → 13,3%)",
         "central": busca_longos / 12.32 * (tot["insc_mil"] / 1000),
         "min": busca_longos / 12.32 * (tot["insc_mil"] / 1000) * 0.5,
         "max": busca_longos / 12.32 * 0.015,
         "base": f"longos recebem {br(busca_longos)} views/mês da Pesquisa (abr a set/26, Studio); +1 p.p. sobre "
                 f"12,32% = +8%, a {br(tot['insc_mil'], 1)} inscritos por mil"},
    ]
    L.sort(key=lambda r: -r["central"])
    return L


def mo_plano_shorts():
    return PLANO_SHORTS


def semanas(mensal, ini=date(2026, 10, 5), fim=date(2026, 11, 29)):
    out, s = [], ini
    por_mes = {r["mes"]: r for r in mensal}
    while s <= fim:
        r = por_mes[f"{s:%Y-%m}"]
        out.append({"semana": f"{s:%d/%m}–{(s + timedelta(days=6)):%d/%m}", "liquidos": r["liquidos"] / 4.33,
                    "ganhos": r["ganhos"] / 4.33, "longos": 3 if s >= date(2026, 10, 26) else 2,
                    "shorts": 2})
        s += timedelta(days=7)
    return out


def br(x, casas=0):
    if x is None:
        return "—"
    s = f"{x:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def gerar(d=None):
    d = d or mo.carregar()
    b = mo.base(d)
    cen = [(nome, prazo, mo.cenario(b, prazo)) for nome, prazo in mo.PRAZOS]
    p = mo.plano(d, b, PLANO_LONGOS, PLANO_SHORTS)
    mensal = metas_mensais(b, p)
    quando = data_meta(b, mensal, p["liquidos"])
    p25 = dict(p, novos=p["novos_p25"])
    p75 = dict(p, novos=p["novos_p75"])
    m25, m75 = metas_mensais(b, p25), metas_mensais(b, p75)
    quando25, quando75 = data_meta(b, m25, p["liquidos_p25"]), data_meta(b, m75, p["liquidos_p75"])
    hoje_liq = mo.projecao(b, b["liq_6m"])
    lav = alavancas(d, b)
    sem = semanas(mensal)
    return {"b": b, "cen": cen, "p": p, "mensal": mensal, "quando": quando, "quando25": quando25,
            "quando75": quando75, "hoje": hoje_liq, "alavancas": lav, "semanas": sem, "d": d}


def escrever_csv(r, caminho):
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["tipo", "periodo", "inscritos_liquidos", "ganhos", "perdas", "longos", "shorts",
                    "inscritos_acumulados"])
        for m in r["mensal"]:
            w.writerow(["mes", m["mes"], round(m["liquidos"]), round(m["ganhos"]), round(m["perdas"]), m["longos"],
                        m["shorts"], round(m["inscritos_fim_mes"])])
        for s in r["semanas"]:
            w.writerow(["semana", s["semana"], round(s["liquidos"]), round(s["ganhos"]), "", s["longos"], s["shorts"], ""])
        for nome, prazo, c in r["cen"]:
            w.writerow(["cenario", nome, round(c["liquidos"]), round(c["ganhos"]), round(r["b"]["perdas_6m"]),
                        round(c["longos_insc_p75"]), "", ""])


if __name__ == "__main__":
    import meta_md
    r = gerar()
    escrever_csv(r, AQUI / "meta.csv")
    (AQUI / "META.md").write_text(meta_md.markdown(r), encoding="utf-8")
    print(f"ok: META.md e meta.csv · plano: {r['p']['liquidos']:.0f} líquidos/mês · 200 mil em {r['quando']} "
          f"(faixa {r['quando25']} a {r['quando75']})")
