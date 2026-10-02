"""Etapa 4: validar (DESENHO 8.2). Testes com os dados reais, a cada execução.

"bloqueante": se falhar, a página do ativo não é gerada (fica a versão anterior, se houver).
"alerta": vai para o relatório e para a página de metodologia, mas não impede a página.
Os testes de HTML (13, 14 e 15) rodam no gerar, sobre o HTML pronto.
"""
import json
from datetime import date, timedelta

from . import config
from .calcular import refs_trimestrais
from .contas import Demonstracoes, fim_trimestre_anterior, menos_um_ano

TOL_BALANCO = 1000.0        # teste 1: R$ 1 mil
TOL_LUCRO_PARTES = 0.001    # teste 2: 0,1%
TOL_TTM = 1000.0            # teste 3: R$ 1 mil
FATOR_ESCALA = 500          # teste 4: variação de mais de 500x = erro de escala
TOL_LPA = 0.03              # teste 5: 3%
TOL_ACOES = 0.01            # teste 6: 1%
SALTO_PRECO = 0.30          # teste 9: 30% num dia
TOL_VP_FII = 0.005          # teste 10: 0,5%


def r(num, nome, tipo, ok, detalhe, tolerancia=""):
    return {"teste": num, "nome": nome, "tipo": tipo, "ok": bool(ok), "detalhe": detalhe, "tolerancia": tolerancia}


def zerou_controladora(d, refs) -> bool:
    """Algum trimestre com a linha da controladora preenchida com zero e lucro total diferente de zero."""
    for x in refs:
        dd = d.doc_em(x)
        if not dd:
            continue
        cd = d.achar(*dd, "DRE", "lucro_controladora")
        if cd and any(l.cd == cd and l.valor == 0 for l in d._linhas(*dd, "DRE")):
            return True
    return False


def testes_acao(con, ficha: dict) -> list[dict]:
    d = Demonstracoes(con, ficha["cnpj"])
    out = []
    u = d.ultimo_doc()
    if not u:
        return [r(0, "existe demonstração", "bloqueante", False, "nenhum DFP/ITR")]
    doc, ref = u
    # 1. Ativo = Passivo + PL
    at = d.saldo(ref, "BPA", "ativo_total")[0]
    pa = d.saldo(ref, "BPP", "passivo_total")[0]
    ok = at is not None and pa is not None and abs(at - pa) <= TOL_BALANCO
    out.append(r(1, "Ativo total = Passivo total + PL", "bloqueante", ok,
                 f"{d.rotulo_curto(doc, ref)}: ativo {at:,.0f}, passivo+PL {pa:,.0f}" if ok or at else "conta ausente", "R$ 1 mil"))
    # 2. lucro total = controladora + não controladores
    if d.escopo == "con":
        lt = d.acumulado(doc, ref, "DRE", "lucro_total")[0]
        lc = d.acumulado(doc, ref, "DRE", "lucro_controladora")[0]
        ln = d.acumulado(doc, ref, "DRE", "lucro_nao_controladores")[0] or 0
        ok = lt is not None and lc is not None and abs(lt - (lc + ln)) <= abs(lt) * TOL_LUCRO_PARTES + 1
        out.append(r(2, "Lucro consolidado = controladora + não controladores", "bloqueante", ok,
                     f"{lt} = {lc} + {ln}", "0,1%"))
    # 3. soma de 4 trimestres = anual da DFP; TTM = soma dos 4 últimos trimestres
    dfps = sorted(x for (dd, x) in d.docs if dd == "DFP")
    financeira = ficha.get("tipo") in ("banco", "seguradora")
    contas = ["lucro_controladora"] + ([] if financeira else ["receita", "ebit"])
    if dfps:
        y = dfps[-1]
        for regra in contas:
            anual = d.acumulado("DFP", y, "DRE", regra)[0]
            tris = [d.trimestre(x, "DRE", regra) for x in refs_trimestrais(y, 4)]
            tol, nota = TOL_TTM, ""
            if regra == "lucro_controladora" and zerou_controladora(d, refs_trimestrais(y, 4)):
                nc = abs(d.acumulado("DFP", y, "DRE", "lucro_nao_controladores")[0] or 0)
                tol, nota = TOL_TTM + nc, (f". A empresa preencheu a parte da controladora com zero em algum trimestre; "
                                          f"usado o lucro total, e a tolerância sobe pelo lucro de não controladores do ano ({nc:,.0f})")
            ok = anual is not None and None not in tris and abs(sum(tris) - anual) <= tol
            out.append(r(3, f"Soma dos 4 trimestres de {y[:4]} = DFP {y[:4]} ({regra})", "bloqueante", ok,
                         f"trimestres {[round(t or 0) for t in tris]} soma {sum(t or 0 for t in tris):,.0f}; DFP {anual:,.0f}{nota}",
                         "R$ 1 mil" + (" + não controladores" if nota else "")))
    for regra in contas:
        ttm = d.ttm(ref, "DRE", regra).get("valor")
        tris = [d.trimestre(x, "DRE", regra) for x in refs_trimestrais(ref, 4)]
        dif = None if ttm is None or None in tris else sum(tris) - ttm
        tol = TOL_TTM
        if regra == "lucro_controladora" and zerou_controladora(d, refs_trimestrais(ref, 4)):
            tol += abs(d.ttm(ref, "DRE", "lucro_nao_controladores").get("valor") or 0)
        ok = dif is not None and abs(dif) <= tol
        detalhe = f"TTM {ttm:,.0f}; soma dos trimestres {sum(t or 0 for t in tris):,.0f}" if ttm is not None else "sem TTM"
        tipo = "bloqueante"
        if dif is not None and not ok and doc == "ITR":
            # A diferença pode ser só reapresentação: o TTM usa sempre o acumulado mais recente (DESENHO 4.1),
            # e os trimestres antigos vêm dos ITRs originais. Soma das reapresentações encontradas:
            # (a) acumulado do ano anterior: original × coluna PENÚLTIMO do ITR atual;
            # (b) trimestres anteriores do ano corrente: acumulado original × (acumulado atual − trimestre atual).
            deltas = []
            ant = menos_um_ano(ref)
            if d.doc_em(ant):
                orig = d.acumulado(*d.doc_em(ant), "DRE", regra)[0]
                reap = d.acumulado(doc, ref, "DRE", regra, "PENULTIMO")[0]
                if None not in (orig, reap) and abs(orig - reap) > TOL_TTM:
                    deltas.append((f"acumulado de {ant}", orig, reap))
            ant_tri = fim_trimestre_anterior(ref)
            if d.doc_em(ant_tri) and d.doc_em(ant_tri)[0] == "ITR" and ant_tri[:4] == ref[:4]:
                orig = d.acumulado(*d.doc_em(ant_tri), "DRE", regra)[0]
                agora = d.acumulado(doc, ref, "DRE", regra)[0]
                q = d.trimestre(ref, "DRE", regra)
                if None not in (orig, agora, q) and abs(orig - (agora - q)) > TOL_TTM:
                    deltas.append((f"acumulado até {ant_tri}", orig, agora - q))
            explicado = sum(abs(o - n) for _, o, n in deltas)
            if deltas and abs(abs(dif) - explicado) <= TOL_TTM:
                ok = True
                detalhe += ". Diferença explicada por reapresentação: " + "; ".join(
                    f"{nome} original {o:,.0f}, reapresentado {n:,.0f}" for nome, o, n in deltas) + ". Vale o reapresentado"
        out.append(r(3, f"TTM até {ref} = soma dos 4 últimos trimestres ({regra})", tipo, ok, detalhe, "R$ 1 mil"))
    # 4. escala: nenhum trimestre ±500x o anterior (receita, ou lucro em banco)
    regra = "lucro_controladora" if financeira else "receita"
    tris = [(t["rotulo"], t.get("receita" if not financeira else "lucro")) for t in ficha.get("trimestres", [])]
    ruins = [f"{a[0]}→{b[0]}" for a, b in zip(tris, tris[1:])
             if a[1] and b[1] and (abs(b[1] / a[1]) > FATOR_ESCALA or abs(b[1] / a[1]) < 1 / FATOR_ESCALA)]
    out.append(r(4, f"Escala: {regra} trimestral sem salto de {FATOR_ESCALA}x", "bloqueante", not ruins,
                 "ok" if not ruins else "salto em " + ", ".join(ruins), f"{FATOR_ESCALA}x"))
    # 5. LPA calculado x divulgado (DFP)
    lp = ficha.get("lpa_divulgado") or {}
    cap = con.execute("SELECT qt_on, qt_pn, qt_on_tesouraria, qt_pn_tesouraria FROM capital WHERE cnpj=? AND doc='DFP' AND dt_refer=?",
                      (ficha["cnpj"], lp.get("dt_refer"))).fetchone()
    k = (ficha.get("acoes") or {}).get("escala", 1)
    if cap and lp.get("lucro_controladora") and (lp.get("lpa_on") or lp.get("lpa_pn")):
        on, pn = ((cap[0] or 0) - (cap[2] or 0)) * k, ((cap[1] or 0) - (cap[3] or 0)) * k
        div_med = ((lp.get("lpa_on") or 0) * on + (lp.get("lpa_pn") or 0) * pn) / (on + pn)
        calc = lp["lucro_controladora"] / (on + pn)
        dif = abs(calc / div_med - 1) if div_med else 1
        out.append(r(5, f"LPA calculado × LPA básico divulgado (DFP {lp['dt_refer'][:4]})", "alerta", dif <= TOL_LPA,
                     f"calculado {calc:.4f}; divulgado (média ON/PN) {div_med:.4f}; diferença {dif:.2%}"
                     + (" (ações informadas em milhares)" if k == 1000 else ""), "3%"))
    else:
        out.append(r(5, "LPA calculado × divulgado", "alerta", True, "LPA não divulgado por classe na DFP: não conferido", "3%"))
    # 6 (adaptado). Ações em circulação: último documento × anterior (o FRE não entrou no MVP)
    caps = con.execute("""SELECT dt_refer, qt_on+qt_pn-COALESCE(qt_on_tesouraria,0)-COALESCE(qt_pn_tesouraria,0)
                          FROM capital WHERE cnpj=? ORDER BY dt_refer DESC LIMIT 2""", (ficha["cnpj"],)).fetchall()
    if len(caps) == 2 and caps[1][1]:
        dif = caps[0][1] / caps[1][1] - 1
        out.append(r(6, "Ações em circulação: último documento × anterior", "alerta", abs(dif) <= TOL_ACOES,
                     f"{caps[1][0]}: {caps[1][1]:,.0f}; {caps[0][0]}: {caps[0][1]:,.0f} ({dif:+.2%}). "
                     "Diferença grande: desdobramento, grupamento, recompra ou conversão. Conferir no FRE.", "1%"))
    out += testes_preco(con, ficha)
    return out


def testes_preco(con, ficha) -> list[dict]:
    t = ficha["ticker"]
    ini = (config.HOJE - timedelta(days=365)).isoformat()
    pregoes = [x[0] for x in con.execute("SELECT DISTINCT data FROM preco_diario WHERE data>=? AND codbdi IN ('02','12')", (ini,))]
    dias = {x[0] for x in con.execute("SELECT data FROM preco_diario WHERE ticker=? AND data>=?", (t, ini))}
    faltam = [d for d in pregoes if d not in dias]
    out = [r(9, "Preço: nenhum pregão sem negócio em 12 meses", "alerta", not faltam,
             f"{len(faltam)} pregões sem negócio" + (f" (ex.: {faltam[0]})" if faltam else ""), "exato")]
    from .calcular import saltos_de_preco
    s = saltos_de_preco(con, t, ini)
    out.append(r(9, f"Preço: variação diária acima de {SALTO_PRECO:.0%} só com evento conhecido", "alerta", not s,
                 "ok" if not s else f"{s[0]['data']}: {s[0]['de']:.2f} → {s[0]['para']:.2f} (evento não cadastrado)", "exato"))
    return out


def testes_fii(con, ficha) -> list[dict]:
    out = []
    inf = ficha.get("informe")
    if not inf:
        return [r(0, "existe informe mensal", "bloqueante", False, "sem informe")]
    calc = inf["pl"] / inf["cotas_emitidas"] if inf.get("cotas_emitidas") else None
    vp = inf.get("vp_cota")
    dif = abs(calc / vp - 1) if calc and vp else 1
    out.append(r(10, "FII: Patrimônio ÷ cotas emitidas = valor patrimonial da cota", "bloqueante", dif <= TOL_VP_FII,
                 f"informe {inf['mes']}: {calc:.4f} × {vp:.4f} ({dif:.3%})" if calc and vp else "campo vazio", "0,5%"))
    prob = ficha.get("informe_problemas") or []
    out.append(r(12, "FII: DY mensal informado coerente (sem negativos, saltos ou meses copiados)", "alerta", not prob,
                 "ok" if not prob else "; ".join(prob[:4]), "DY entre 0% e 3% ao mês"))
    out += testes_preco(con, ficha)
    return out


def validar_todos(con, selecao) -> dict:
    rel = {"data": config.HOJE.isoformat(), "ativos": {}}
    for a in selecao["acoes"] + selecao["fiis"]:
        p = config.CACHE / "fichas" / f"{a['ticker']}.json"
        ficha = json.loads(p.read_text())
        ts = testes_fii(con, ficha) if ficha["tipo_pagina"] == "fii" else testes_acao(con, ficha)
        bloq = [t for t in ts if t["tipo"] == "bloqueante" and not t["ok"]]
        rel["ativos"][a["ticker"]] = {"bloqueado": bool(bloq), "testes": ts}
    (config.CACHE / "validacao.json").write_text(json.dumps(rel, ensure_ascii=False, indent=1))
    return rel
