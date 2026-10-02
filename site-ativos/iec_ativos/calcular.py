"""Etapa 3: calcular. Monta a "ficha" de cada ativo: indicadores com valor, status, fonte e data.

Cada indicador é um dict:
  {"valor": float|None, "status": "ok"|"nao_se_aplica"|"sem_dado"|"negativo",
   "fonte": "CVM, ITR 2T26 ...; B3, COTAHIST, pregão de ...", "ref": "AAAA-MM-DD", "nota": "...",
   "insumos": [ids de conta/preco], "formula": "..."}
A ficha vai para cache/fichas/<ticker>.json e para a tabela `indicador`.
"""
import json
from datetime import date, datetime, timedelta

from . import config
from .contas import Demonstracoes, _br, menos_um_ano

FORMULA_VERSAO = "2026-10-mvp1"
LIQUIDEZ_MIN = 1_000_000  # R$/dia em 3 meses (DESENHO 5.4)


def ind(valor, status="ok", fonte="", ref="", nota="", insumos=None, formula=""):
    return {"valor": valor, "status": status, "fonte": fonte, "ref": ref, "nota": nota,
            "insumos": insumos or [], "formula": formula}


def sem(motivo, fonte="", ref="", status="sem_dado"):
    return ind(None, status, fonte, ref, motivo)


def div(a, b):
    return None if a is None or b in (None, 0) else a / b


# ---------------------------------------------------------------------------- preços

def ultimo_preco(con, ticker, ate=None):
    ate = ate or config.HOJE.isoformat()
    r = con.execute("""SELECT data, fechamento, rowid FROM preco_diario WHERE ticker=? AND data<=?
                       ORDER BY data DESC LIMIT 1""", (ticker, ate)).fetchone()
    return (r[0], r[1], r[2]) if r else (None, None, None)


def volume_3m(con, ticker, fim):
    ini = (date.fromisoformat(fim) - timedelta(days=91)).isoformat()
    n = con.execute("SELECT COUNT(DISTINCT data) FROM preco_diario WHERE data>? AND data<=?", (ini, fim)).fetchone()[0] or 1
    v = con.execute("SELECT SUM(volume_rs) FROM preco_diario WHERE ticker=? AND data>? AND data<=?",
                    (ticker, ini, fim)).fetchone()[0] or 0
    return v / n


def saltos_de_preco(con, ticker, desde) -> list[dict]:
    """Teste 9: variação diária acima de 30% sem evento societário conferido."""
    eventos = {r[0] for r in con.execute("SELECT data_ex FROM evento_societario WHERE ticker=?", (ticker,))}
    rows = con.execute("SELECT data, fechamento FROM preco_diario WHERE ticker=? AND data>=? ORDER BY data",
                       (ticker, desde)).fetchall()
    out = []
    for (d0, p0), (d1, p1) in zip(rows, rows[1:]):
        if p0 and abs(p1 / p0 - 1) > 0.30 and d1 not in eventos:
            out.append({"data": d1, "de": p0, "para": p1})
    return out


def serie_precos(con, ticker, anos=5):
    ini = (config.HOJE - timedelta(days=365 * anos + 2)).isoformat()
    return [(r[0], r[1]) for r in con.execute(
        "SELECT data, fechamento FROM preco_diario WHERE ticker=? AND data>=? ORDER BY data", (ticker, ini))]


def variacao_12m(con, ticker, data, preco):
    alvo = (date.fromisoformat(data) - timedelta(days=365)).isoformat()
    r = con.execute("SELECT data, fechamento FROM preco_diario WHERE ticker=? AND data<=? ORDER BY data DESC LIMIT 1",
                    (ticker, alvo)).fetchone()
    if not r:
        return sem("menos de 12 meses de pregões no arquivo")
    saltos = saltos_de_preco(con, ticker, r[0])
    if saltos:
        return sem(f"variação diária acima de 30% em {_br(saltos[0]['data'])} sem desdobramento ou grupamento "
                   "conferido; a variação nominal pode enganar", f"B3, COTAHIST, pregões de {_br(r[0])} e {_br(data)}", data)
    return ind(preco / r[1] - 1, fonte=f"B3, COTAHIST, pregões de {_br(r[0])} e {_br(data)} (preço sem ajuste)",
               ref=data, formula="fechamento atual ÷ fechamento de 12 meses antes − 1")


# ---------------------------------------------------------------------------- ações

def classes_da_empresa(con, cnpj, fim):
    """Tickers da empresa no COTAHIST, com classe, preço e liquidez."""
    out = []
    for r in con.execute("SELECT ticker, classe, composicao_unit, composicao_fonte FROM ativo WHERE cnpj_emissor=?", (cnpj,)):
        data, preco, pid = ultimo_preco(con, r[0], fim)
        if preco is None or (date.fromisoformat(fim) - date.fromisoformat(data)).days > 10:
            continue
        out.append({"ticker": r[0], "classe": r[1], "comp": json.loads(r[2]) if r[2] else None,
                    "comp_fonte": r[3], "data": data, "preco": preco, "preco_id": pid,
                    "volume_3m": volume_3m(con, r[0], fim)})
    return out


def acoes_por_unit(comp: dict | None) -> int:
    return sum(comp.values()) if comp else 1


def valor_de_mercado(con, cnpj, qt_on, qt_pn, fim):
    """Σ por classe (preço da classe × ações em circulação). DESENHO 4.4."""
    cls = classes_da_empresa(con, cnpj, fim)
    liquidos = {c["classe"]: c for c in sorted(cls, key=lambda c: c["volume_3m"]) if c["volume_3m"] >= LIQUIDEZ_MIN}
    unit = next((c for c in cls if c["classe"] == "UNIT" and c["comp"]), None)
    partes, notas, estimado = [], [], False
    for classe, qt in (("ON", qt_on), ("PN", qt_pn)):
        if not qt:
            continue
        if classe in liquidos:
            c = liquidos[classe]
            partes.append((classe, qt, c["preco"], c["ticker"]))
        elif unit:
            p = unit["preco"] / acoes_por_unit(unit["comp"])
            partes.append((classe, qt, p, f"{unit['ticker']} ÷ {acoes_por_unit(unit['comp'])}"))
            notas.append(f"{classe} sem liquidez: preço implícito da unit {unit['ticker']} ÷ "
                         f"{acoes_por_unit(unit['comp'])} ações ({unit['comp_fonte']})")
            estimado = True
        elif liquidos:
            c = max(liquidos.values(), key=lambda c: c["volume_3m"])
            partes.append((classe, qt, c["preco"], c["ticker"]))
            notas.append(f"{classe} sem negociação líquida: usado o preço de {c['ticker']}")
            estimado = True
        else:
            return None, [], ["nenhuma classe com liquidez"], True
    vm = sum(qt * p for _, qt, p, _ in partes)
    return vm, partes, notas, estimado


def ficha_acao(con, ticker: str, tipo: str, cnpj: str) -> dict:
    emp = con.execute("SELECT nome, nome_comercial, setor_cvm, cd_cvm FROM empresa WHERE cnpj=?", (cnpj,)).fetchone()
    at = con.execute("SELECT classe, composicao_unit, composicao_fonte, isin FROM ativo WHERE ticker=?", (ticker,)).fetchone()
    comp = json.loads(at[1]) if at and at[1] else None
    equiv = acoes_por_unit(comp) if at and at[0] == "UNIT" else 1
    d = Demonstracoes(con, cnpj)
    u = d.ultimo_doc()
    data, preco, pid = ultimo_preco(con, ticker)
    fonte_preco = f"B3, COTAHIST, pregão de {_br(data)}"
    f = {"ticker": ticker, "tipo_pagina": "acao", "tipo": tipo, "cnpj": cnpj, "nome": emp[0],
         "nome_curto": nome_curto(emp[1] or emp[0]), "setor": emp[2], "cd_cvm": emp[3], "classe": at[0] if at else None,
         "isin": at[3] if at else None, "composicao_unit": comp, "composicao_fonte": at[2] if at else None,
         "acoes_por_titulo": equiv, "escopo": d.escopo, "calculado_em": datetime.now().isoformat(timespec="seconds"),
         "formula_versao": FORMULA_VERSAO, "avisos": [], "ind": {}}
    I = f["ind"]
    I["preco"] = ind(preco, fonte=fonte_preco, ref=data, insumos=[pid]) if preco else sem("sem pregão")
    I["variacao_12m"] = variacao_12m(con, ticker, data, preco) if preco else sem("sem pregão")
    I["volume_3m"] = ind(volume_3m(con, ticker, data), fonte=f"B3, COTAHIST, 3 meses até {_br(data)}", ref=data)
    if u is None:
        f["avisos"].append("Sem demonstrações na CVM.")
        return f
    doc, ref = u
    f["doc"] = {"doc": doc, "dt_refer": ref, "rotulo": d.rotulo_doc(doc, ref), "curto": d.rotulo_curto(doc, ref),
                **d.documentos.get((doc, ref), {})}
    fonte_bal = d.rotulo_doc(doc, ref)
    fonte_ttm = f"CVM, 12 meses até {_br(ref)} ({d.rotulo_curto(doc, ref)} + DFP anterior), {('consolidado' if d.escopo == 'con' else 'individual')}"
    if d.escopo == "ind":
        f["avisos"].append("A empresa não publica demonstração consolidada: os números são da demonstração individual.")

    # ações em circulação (capital do último documento)
    cap = con.execute("""SELECT qt_on, qt_pn, qt_on_tesouraria, qt_pn_tesouraria, doc, dt_refer FROM capital
                         WHERE cnpj=? ORDER BY dt_refer DESC LIMIT 1""", (cnpj,)).fetchone()
    if cap:
        qt_on = (cap[0] or 0) - (cap[2] or 0)
        qt_pn = (cap[1] or 0) - (cap[3] or 0)
        f["acoes"] = {"on": qt_on, "pn": qt_pn, "total": qt_on + qt_pn,
                      "fonte": f"CVM, composição do capital, {cap[4]} de {_br(cap[5])} (sem ações em tesouraria)",
                      "ref": cap[5]}
    else:
        qt_on = qt_pn = 0
        f["avisos"].append("Sem composição do capital no último documento.")
    total_acoes = qt_on + qt_pn

    vm, partes, notas_vm, estimado = valor_de_mercado(con, cnpj, qt_on, qt_pn, data)
    fonte_vm = f"{fonte_preco}; {f['acoes']['fonte'] if cap else ''}"
    I["valor_mercado"] = (ind(vm, fonte=fonte_vm, ref=data, nota="; ".join(notas_vm) + (" (estimado)" if estimado else ""),
                              formula="Σ por classe (fechamento × ações em circulação)")
                          if vm else sem("sem preço ou sem número de ações", fonte_vm, data))
    f["valor_mercado_partes"] = [{"classe": c, "acoes": q, "preco": p, "origem": o} for c, q, p, o in partes]

    # resultados TTM
    lc = d.ttm(ref, "DRE", "lucro_controladora")
    lt = d.ttm(ref, "DRE", "lucro_total")
    rec = d.ttm(ref, "DRE", "receita")
    ttm_ant_ref = menos_um_ano(ref)
    lc_ant = d.ttm(ttm_ant_ref, "DRE", "lucro_controladora") if d.doc_em(ttm_ant_ref) else {"valor": None}
    f["ttm"] = {"lucro_controladora": lc.get("valor"), "lucro_total": lt.get("valor"), "receita": rec.get("valor"),
                "lucro_controladora_ano_anterior": lc_ant.get("valor"), "pecas": lc.get("pecas"), "fim": ref}
    pl, pl_ids = d.saldo(ref, "BPP", "pl_total")
    pl_nc = d.saldo(ref, "BPP", "pl_nao_controladores")[0] or 0
    pl_contr = None if pl is None else pl - pl_nc
    pl_ant, _ = d.saldo(ttm_ant_ref, "BPP", "pl_total")
    pl_nc_ant = d.saldo(ttm_ant_ref, "BPP", "pl_nao_controladores")[0] or 0
    pl_contr_ant = None if pl_ant is None else pl_ant - pl_nc_ant
    f["balanco"] = {"pl_total": pl, "pl_nao_controladores": pl_nc, "pl_controladora": pl_contr,
                    "pl_controladora_12m_antes": pl_contr_ant, "ref": ref}

    # P/L
    v = lc.get("valor")
    if vm is None:
        I["pl"] = sem("sem valor de mercado")
    elif v is None:
        I["pl"] = sem(lc.get("motivo", "lucro não encontrado"))
    elif v <= 0:
        I["pl"] = sem("não se aplica (prejuízo em 12 meses)", fonte_ttm, ref, "nao_se_aplica")
    else:
        I["pl"] = ind(vm / v, fonte=f"{fonte_preco}; {fonte_ttm}", ref=ref, insumos=lc.get("insumos"),
                      formula="valor de mercado ÷ lucro da controladora em 12 meses")
    # P/VP
    if vm is None or pl_contr is None:
        I["pvp"] = sem("sem valor de mercado ou sem patrimônio")
    elif pl_contr <= 0:
        I["pvp"] = sem("não se aplica (patrimônio líquido negativo)", fonte_bal, ref, "nao_se_aplica")
    else:
        I["pvp"] = ind(vm / pl_contr, fonte=f"{fonte_preco}; {fonte_bal}", ref=ref, insumos=pl_ids,
                       formula="valor de mercado ÷ (patrimônio líquido − participação de não controladores)")
    # ROE
    if v is None or pl_contr is None:
        I["roe"] = sem("sem lucro ou patrimônio")
    elif pl_contr_ant is None:
        I["roe"] = sem("sem o balanço de 12 meses antes")
    elif (pl_contr + pl_contr_ant) / 2 <= 0:
        I["roe"] = sem("não se aplica (patrimônio médio negativo)", status="nao_se_aplica")
    else:
        I["roe"] = ind(v / ((pl_contr + pl_contr_ant) / 2), fonte=f"{fonte_ttm}; balanços de {_br(ref)} e {_br(ttm_ant_ref)}",
                       ref=ref, formula="lucro da controladora em 12 meses ÷ média do patrimônio da controladora (hoje e 12 meses antes)")
    # DY de caixa (DFC)
    prov = d.ttm(ref, "DFC", "soma:proventos_pagos")
    pv = prov.get("valor")
    f["ttm"]["proventos_pagos"] = None if pv is None else -pv
    if vm is None:
        I["dy_caixa"] = sem("sem valor de mercado")
    elif pv is None:
        I["dy_caixa"] = sem("linhas de dividendos/JCP pagos não encontradas na DFC")
    else:
        I["dy_caixa"] = ind(-pv / vm, fonte=f"{fonte_ttm} (fluxo de caixa); {fonte_preco}", ref=ref,
                            insumos=prov.get("insumos"),
                            nota="Dividendos e JCP pagos pela empresa em 12 meses (fluxo de caixa) ÷ valor de mercado. "
                                 "Não é a soma dos proventos por ação com data ex nos últimos 12 meses: essa tabela "
                                 "ainda não foi aprovada.",
                            formula="proventos pagos em 12 meses (DFC, 6.03, sinal invertido) ÷ valor de mercado")
    I["dy_12m"] = sem("tabela de proventos por ação ainda não aprovada (fila de Avisos aos Acionistas). "
                      "Veja o DY de caixa da empresa.")
    # por ação (para o preco-justo): LPA, VPA, DPA de caixa
    if total_acoes:
        I["lpa"] = (ind(v / total_acoes * equiv, fonte=f"{fonte_ttm}; {f['acoes']['fonte']}", ref=ref,
                        formula="lucro da controladora em 12 meses ÷ ações em circulação" + (f" × {equiv} (ações por unit)" if equiv > 1 else ""))
                    if v is not None else sem("sem lucro"))
        I["vpa"] = (ind(pl_contr / total_acoes * equiv, fonte=f"{fonte_bal}; {f['acoes']['fonte']}", ref=ref,
                        formula="patrimônio da controladora ÷ ações em circulação" + (f" × {equiv}" if equiv > 1 else ""))
                    if pl_contr is not None else sem("sem patrimônio"))
        I["dpa_caixa"] = (ind(-pv / total_acoes * equiv, fonte=f"{fonte_ttm} (fluxo de caixa); {f['acoes']['fonte']}", ref=ref,
                              formula="proventos pagos em 12 meses (DFC) ÷ ações em circulação" + (f" × {equiv}" if equiv > 1 else ""))
                          if pv is not None else sem("sem proventos pagos na DFC"))
    financeira = tipo in ("banco", "seguradora")
    motivo_fin = ("não se aplica a banco: a receita de intermediação e a dívida são a matéria-prima do negócio"
                  if tipo == "banco" else "não se aplica a seguradora: o plano de contas é diferente")
    # margens, EBITDA, dívida
    if financeira:
        for k in ("margem_liquida", "ebitda", "margem_ebitda", "div_liq_ebitda", "div_liq_ebitda_arrend"):
            I[k] = sem(motivo_fin, status="nao_se_aplica")
    else:
        r_v = rec.get("valor")
        lt_v = lt.get("valor")
        if r_v is None or lt_v is None:
            I["margem_liquida"] = sem("receita ou lucro não encontrados")
        elif r_v <= 0:
            I["margem_liquida"] = sem("não se aplica (receita menor ou igual a zero)", status="nao_se_aplica")
        else:
            I["margem_liquida"] = ind(lt_v / r_v, fonte=fonte_ttm, ref=ref, formula="lucro líquido total ÷ receita líquida, 12 meses")
        eb = ebitda_ttm(d, ref)
        f["ttm"]["ebit"] = eb.get("ebit")
        f["ttm"]["da"] = eb.get("da")
        f["ttm"]["ebitda"] = eb.get("valor")
        nota_eb = ("EBITDA calculado (lucro antes do resultado financeiro e dos tributos + depreciação e amortização, "
                   "conceito da Resolução CVM 156/2022). Não é o EBITDA ajustado do release da empresa. "
                   + ("D&A da DVA." if eb.get("origem_da") == "DVA" else "D&A somada das linhas do fluxo de caixa."))
        if eb.get("valor") is None:
            I["ebitda"] = sem(eb.get("motivo", "EBIT ou D&A não encontrados"))
        else:
            I["ebitda"] = ind(eb["valor"], fonte=fonte_ttm, ref=ref, nota=nota_eb, formula="EBIT (3.05) + D&A, 12 meses")
        if eb.get("valor") is None or r_v is None:
            I["margem_ebitda"] = sem("sem EBITDA ou receita")
        elif r_v <= 0:
            I["margem_ebitda"] = sem("não se aplica (receita menor ou igual a zero)", status="nao_se_aplica")
        else:
            I["margem_ebitda"] = ind(eb["valor"] / r_v, fonte=fonte_ttm, ref=ref, formula="EBITDA ÷ receita líquida, 12 meses")
        dv = divida(d, ref)
        f["divida"] = dv
        if dv.get("liquida") is None or eb.get("valor") is None:
            I["div_liq_ebitda"] = sem("sem dívida ou EBITDA")
            I["div_liq_ebitda_arrend"] = sem("sem dívida ou EBITDA")
        elif eb["valor"] <= 0:
            I["div_liq_ebitda"] = sem("não se aplica (EBITDA menor ou igual a zero)", status="nao_se_aplica")
            I["div_liq_ebitda_arrend"] = sem("não se aplica (EBITDA menor ou igual a zero)", status="nao_se_aplica")
        else:
            I["div_liq_ebitda"] = ind(dv["liquida"] / eb["valor"], fonte=f"{fonte_bal}; {fonte_ttm}", ref=ref,
                                      formula="(empréstimos e financiamentos sem arrendamento − caixa − aplicações) ÷ EBITDA 12 meses")
            if dv.get("arrendamento"):
                I["div_liq_ebitda_arrend"] = ind(dv["liquida_com_arrend"] / eb["valor"], fonte=f"{fonte_bal}; {fonte_ttm}",
                                                 ref=ref, formula="mesma conta, somando os arrendamentos (IFRS 16)")
            else:
                I["div_liq_ebitda_arrend"] = sem("conta de arrendamento não encontrada no balanço")
    if tipo == "holding":
        f["avisos"].append("Holding: o lucro vem principalmente das participações (equivalência patrimonial), "
                           "então EBITDA e dívida/EBITDA dizem pouco.")
    # séries para gráficos e tabelas
    f["trimestres"] = serie_trimestral(d, ref, financeira)
    f["anual"] = serie_anual(d, financeira)
    if not financeira:
        f["divida_serie"] = serie_divida(d, ref)
    f["precos"] = serie_precos(con, ticker)
    f["n_trimestres_dre"] = sum(1 for t in f["trimestres"] if t.get("lucro") is not None)
    f["lpa_divulgado"] = lpa_divulgado(d)
    return f


def nome_curto(nome: str) -> str:
    n = (nome or "").strip()
    for suf in (" S.A.", " S/A", " SA", " S.A", " HOLDING"):
        if n.upper().endswith(suf):
            n = n[: -len(suf)]
    return n.title() if n.isupper() else n


def ebitda_ttm(d: Demonstracoes, ref: str) -> dict:
    ebit = d.ttm(ref, "DRE", "ebit")
    if ebit.get("valor") is None:
        return {"valor": None, "motivo": "EBIT (3.05) não encontrado"}
    da = d.ttm(ref, "DVA", "da")
    origem = "DVA"
    if da.get("valor") is None:
        da = d.ttm(ref, "DFC", "soma:da_dfc")
        origem = "DFC"
    if da.get("valor") is None:
        return {"valor": None, "motivo": "depreciação e amortização não encontradas (DVA e DFC)", "ebit": ebit["valor"]}
    return {"valor": ebit["valor"] + abs(da["valor"]), "ebit": ebit["valor"], "da": abs(da["valor"]), "origem_da": origem}


def divida(d: Demonstracoes, ref: str) -> dict:
    bruta, _ = d.saldo(ref, "BPP", "soma:divida_bruta")
    arr_dentro = d.saldo(ref, "BPP", "soma:arrendamento_dentro_da_divida")[0] or 0
    arr_total = d.saldo(ref, "BPP", "soma:arrendamento")[0] or 0
    caixa = d.saldo(ref, "BPA", "caixa")[0] or 0
    aplic = d.saldo(ref, "BPA", "aplicacoes")[0] or 0
    if bruta is None:
        return {"bruta": None, "liquida": None}
    sem_arr = bruta - arr_dentro
    liq = sem_arr - caixa - aplic
    return {"bruta": sem_arr, "arrendamento": arr_total, "caixa": caixa, "aplicacoes": aplic,
            "liquida": liq, "liquida_com_arrend": liq + arr_total, "ref": ref}


def refs_trimestrais(ref: str, n: int) -> list[str]:
    out, d = [], date.fromisoformat(ref)
    for _ in range(n):
        out.append(d.isoformat())
        d = d.replace(day=1) - timedelta(days=62)
        d = (d.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
    return list(reversed(out))


def serie_trimestral(d: Demonstracoes, ref: str, financeira: bool, n=12) -> list[dict]:
    out = []
    for r in refs_trimestrais(ref, n):
        item = {"ref": r, "rotulo": f"{(int(r[5:7]) - 1) // 3 + 1}T{r[2:4]}",
                "lucro": d.trimestre(r, "DRE", "lucro_controladora")}
        if not financeira:
            item["receita"] = d.trimestre(r, "DRE", "receita")
        out.append(item)
    return out


def serie_anual(d: Demonstracoes, financeira: bool) -> list[dict]:
    """5 exercícios. O ano Y vem da DFP Y+1 (coluna do ano anterior, já reapresentada) quando existe."""
    dfps = sorted(r for (doc, r) in d.docs if doc == "DFP")
    out = []
    for r in dfps:
        prox = f"{int(r[:4]) + 1}{r[4:]}"
        fonte_doc, ordem = (("DFP", prox), "PENULTIMO") if ("DFP", prox, "DRE") in d.linhas else (("DFP", r), "ULTIMO")
        g = lambda dem, regra: d.acumulado(*fonte_doc, dem, regra, ordem)[0]  # noqa: E731
        item = {"ano": r[:4], "lucro": g("DRE", "lucro_controladora"), "lucro_total": g("DRE", "lucro_total"),
                "fonte": d.rotulo_curto(*fonte_doc) + (" (coluna do ano anterior)" if ordem == "PENULTIMO" else "")}
        if not financeira:
            item["receita"] = g("DRE", "receita")
            ebit = g("DRE", "ebit")
            da = g("DVA", "da")
            item["ebitda"] = None if ebit is None or da is None else ebit + abs(da)
            item["margem_liquida"] = div(item["lucro_total"], item["receita"]) if (item["receita"] or 0) > 0 else None
            item["margem_ebitda"] = div(item["ebitda"], item["receita"]) if (item["receita"] or 0) > 0 else None
        out.append(item)
    return out[-5:]


def serie_divida(d: Demonstracoes, ref: str, n=8) -> list[dict]:
    out = []
    for r in refs_trimestrais(ref, n):
        if d.doc_em(r) is None:
            continue
        dv = divida(d, r)
        eb = ebitda_ttm(d, r).get("valor")
        out.append({"ref": r, "rotulo": f"{(int(r[5:7]) - 1) // 3 + 1}T{r[2:4]}", **dv, "ebitda_ttm": eb,
                    "div_liq_ebitda": div(dv.get("liquida"), eb) if eb and eb > 0 else None})
    return out


def lpa_divulgado(d: Demonstracoes) -> dict | None:
    """LPA básico divulgado na última DFP (3.99.01.01/02) e o lucro da controladora do mesmo ano (teste 5)."""
    dfps = sorted(r for (doc, r) in d.docs if doc == "DFP")
    if not dfps:
        return None
    r = dfps[-1]
    on = d.acumulado("DFP", r, "DRE", "lpa_on")[0]
    pn = d.acumulado("DFP", r, "DRE", "lpa_pn")[0]
    lucro = d.acumulado("DFP", r, "DRE", "lucro_controladora")[0]
    return {"dt_refer": r, "lpa_on": on, "lpa_pn": pn, "lucro_controladora": lucro}


# ---------------------------------------------------------------------------- FIIs

def ficha_fii(con, ticker: str, cnpj: str) -> dict:
    fii = con.execute("SELECT nome, segmento, mandato, tipo_gestao, administrador, isin FROM fii WHERE cnpj=?", (cnpj,)).fetchone()
    data, preco, pid = ultimo_preco(con, ticker)
    fonte_preco = f"B3, COTAHIST, pregão de {_br(data)}"
    meses = [dict(r) for r in con.execute("""SELECT data_ref, versao, cotistas, pl, cotas_emitidas, vp_cota, dy_mes_informado,
                                             rendimentos_distribuir, data_entrega FROM fii_mensal WHERE cnpj=?
                                             ORDER BY data_ref""", (cnpj,))]
    f = {"ticker": ticker, "tipo_pagina": "fii", "cnpj": cnpj, "nome": fii[0], "nome_curto": nome_curto(fii[0]),
         "segmento": fii[1] or "não informado", "mandato": fii[2] or "não informado", "tipo_gestao": fii[3],
         "administrador": fii[4], "isin": fii[5], "calculado_em": datetime.now().isoformat(timespec="seconds"),
         "formula_versao": FORMULA_VERSAO, "avisos": [], "ind": {}, "meses": meses}
    I = f["ind"]
    I["preco"] = ind(preco, fonte=fonte_preco, ref=data, insumos=[pid]) if preco else sem("sem pregão")
    I["variacao_12m"] = variacao_12m(con, ticker, data, preco) if preco else sem("sem pregão")
    I["volume_3m"] = ind(volume_3m(con, ticker, data), fonte=f"B3, COTAHIST, 3 meses até {_br(data)}", ref=data)
    if not meses:
        f["avisos"].append("Sem informe mensal na CVM.")
        return f
    u = meses[-1]
    mes = f"{u['data_ref'][5:7]}/{u['data_ref'][:4]}"
    fonte_inf = f"CVM, informe mensal de FII de {mes}, versão {u['versao']}" + (
        f", entregue em {_br(u['data_entrega'])}" if u.get("data_entrega") else "")
    f["informe"] = {"mes": mes, "fonte": fonte_inf, **u}
    I["vp_cota"] = ind(u["vp_cota"], fonte=fonte_inf, ref=u["data_ref"])
    I["pvp"] = (ind(preco / u["vp_cota"], fonte=f"{fonte_preco}; {fonte_inf}", ref=u["data_ref"],
                    formula="fechamento ÷ valor patrimonial da cota do último informe mensal",
                    nota=f"O valor patrimonial é de {mes}; o preço é de {_br(data)}.")
                if preco and u["vp_cota"] else sem("sem valor patrimonial da cota"))
    I["cotistas"] = ind(u["cotistas"], fonte=fonte_inf, ref=u["data_ref"])
    I["pl"] = ind(u["pl"], fonte=fonte_inf, ref=u["data_ref"])
    # DY estimado pelo informe mensal: Σ (DY do mês informado × VP da cota do mês) nos 12 últimos informes ÷ preço
    ult12 = meses[-12:]
    if len(ult12) == 12 and preco and all(m["dy_mes_informado"] is not None and m["vp_cota"] for m in ult12):
        rend = sum(m["dy_mes_informado"] * m["vp_cota"] for m in ult12)
        f["rendimento_12m_estimado"] = rend
        I["dy_estimado"] = ind(rend / preco, fonte=f"CVM, informes mensais de {ult12[0]['data_ref'][5:7]}/{ult12[0]['data_ref'][:4]} "
                               f"a {mes}; {fonte_preco}", ref=u["data_ref"],
                               formula="Σ (DY do mês informado à CVM × valor patrimonial da cota do mês), 12 meses ÷ fechamento",
                               nota="Estimativa a partir do DY sobre o patrimônio que o administrador informa à CVM. "
                                    "Não é a soma dos rendimentos por cota com data com nos últimos 12 meses: essa "
                                    "tabela (Fundos.NET) ainda não foi aprovada.")
        I["dy_mensal_medio"] = ind(rend / 12 / preco, fonte=I["dy_estimado"]["fonte"], ref=u["data_ref"])
    else:
        I["dy_estimado"] = sem("menos de 12 informes mensais com DY e valor patrimonial")
    I["dy_12m"] = sem("tabela de rendimentos por cota ainda não aprovada (Fundos.NET em análise)")
    I["ultimo_rendimento"] = sem("tabela de rendimentos por cota ainda não aprovada")
    # vacância (informe trimestral, imóveis para renda acabados)
    trims = [r[0] for r in con.execute("SELECT DISTINCT data_ref FROM fii_imovel_trim WHERE cnpj=? ORDER BY data_ref", (cnpj,))]
    vac_serie = []
    for t in trims:
        rows = con.execute("""SELECT area_m2, vacancia_pct FROM fii_imovel_trim WHERE cnpj=? AND data_ref=?
                              AND classe LIKE 'Imóveis para renda acabados%' AND area_m2>0 AND vacancia_pct IS NOT NULL""",
                           (cnpj, t)).fetchall()
        if rows:
            a = sum(r[0] for r in rows)
            vac_serie.append({"ref": t, "vacancia": sum(r[0] * r[1] for r in rows) / a, "area": a, "n": len(rows)})
    f["vacancia_serie"] = vac_serie
    if vac_serie:
        v = vac_serie[-1]
        I["vacancia"] = ind(v["vacancia"], fonte=f"CVM, informe trimestral de FII, trimestre encerrado em {_br(v['ref'])}",
                            ref=v["ref"], formula="Σ (área × vacância) ÷ Σ área, imóveis para renda acabados",
                            nota="Vacância física ponderada pela área. A vacância financeira não está no informe estruturado.")
        f["imoveis"] = [dict(r) for r in con.execute(
            """SELECT imovel, classe, area_m2, vacancia_pct, inadimplencia_pct, pct_receita FROM fii_imovel_trim
               WHERE cnpj=? AND data_ref=? ORDER BY area_m2 DESC""", (cnpj, v["ref"]))]
    elif trims:
        I["vacancia"] = sem("não se aplica: o informe trimestral não lista imóveis para renda acabados "
                            "(fundo de papel ou de outros ativos)", status="nao_se_aplica")
    else:
        I["vacancia"] = sem("não se aplica: o fundo não informa imóveis no informe trimestral "
                            "(fundo de papel ou de outros ativos)", status="nao_se_aplica")
    f["precos"] = serie_precos(con, ticker)
    f["n_informes"] = len(meses)
    return f


# ---------------------------------------------------------------------------- execução

def calcular_todos(con, selecao: dict, log=print) -> list[dict]:
    pasta = config.CACHE / "fichas"
    pasta.mkdir(parents=True, exist_ok=True)
    fichas = []
    for a in selecao["acoes"]:
        fichas.append(ficha_acao(con, a["ticker"], a["tipo"], a["cnpj"]))
    for a in selecao["fiis"]:
        fichas.append(ficha_fii(con, a["ticker"], a["cnpj"]))
    con.execute("DELETE FROM indicador")
    for f in fichas:
        (pasta / f"{f['ticker']}.json").write_text(json.dumps(f, ensure_ascii=False, indent=1, default=str))
        for nome, i in f["ind"].items():
            con.execute("INSERT OR REPLACE INTO indicador VALUES(?,?,?,?,?,?,?,?,?,?)",
                        (f["ticker"], nome, i["valor"], i["status"], f["ind"]["preco"].get("ref"), i.get("ref"),
                         FORMULA_VERSAO, json.dumps(i.get("insumos", [])), i.get("fonte"), f["calculado_em"]))
        log(f"calculado {f['ticker']}")
    con.commit()
    return fichas
