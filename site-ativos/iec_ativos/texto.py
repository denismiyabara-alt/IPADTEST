"""Texto gerado a partir dos números (DESENHO 6.4). Cada frase só existe se o dado existir.

Proibido: adjetivo de valor, verbo de ação, frase genérica. As frases dizem o que o número é,
de onde vem e contra o que se compara.
"""
from .formato import brl_curto, data_br, inteiro, mes_br, numero, pct, vezes


def _v(f, k):
    i = f["ind"].get(k) or {}
    return i.get("valor") if i.get("status") == "ok" else None


def resumo_acao(f: dict) -> list[str]:
    fr = []
    nome = f["nome_curto"]
    ttm = f.get("ttm") or {}
    ref = ttm.get("fim")
    lc, la = ttm.get("lucro_controladora"), ttm.get("lucro_controladora_ano_anterior")
    if lc is not None and ref:
        verbo = "lucrou" if lc >= 0 else "teve prejuízo de"
        s = f"Nos 12 meses até {data_br(ref)}, a {nome} {verbo} {brl_curto(abs(lc))} (parte da controladora)"
        if la and la > 0 and lc > 0:
            s += f", {pct(lc / la - 1)} em relação aos 12 meses anteriores"
        fr.append(s + ".")
    ml = _v(f, "margem_liquida")
    anos = [a for a in f.get("anual", []) if a.get("margem_liquida") is not None]
    if ml is not None and len(anos) >= 5:
        media = sum(a["margem_liquida"] for a in anos) / len(anos)
        lado = "acima" if ml > media else "abaixo" if ml < media else "igual à"
        fr.append(f"A margem líquida em 12 meses foi de {pct(ml)}, {lado} da média dos últimos 5 exercícios ({pct(media)}).")
    elif ml is not None:
        fr.append(f"A margem líquida em 12 meses foi de {pct(ml)}.")
    if f.get("tipo") not in ("banco", "seguradora"):
        d = _v(f, "div_liq_ebitda")
        if d is not None:
            if d < 0:
                fr.append("Sem contar arrendamentos, a empresa tinha mais caixa e aplicações do que empréstimos e "
                          f"financiamentos em {data_br(ref)}.")
            else:
                fr.append(f"A dívida líquida (sem arrendamentos) era {vezes(d)} o EBITDA calculado de 12 meses.")
    else:
        fr.append("Como é " + ("um banco" if f["tipo"] == "banco" else "uma seguradora") +
                  ", a página não mostra margens, EBITDA nem dívida: esses números não se comparam com os de "
                  "outras empresas.")
    pp = ttm.get("proventos_pagos")
    dy = _v(f, "dy_caixa")
    if pp is not None and dy is not None:
        if pp > 0:
            fr.append(f"Pelo fluxo de caixa, a empresa pagou {brl_curto(pp)} em dividendos e juros sobre capital "
                      f"próprio nos 12 meses até {data_br(ref)}, {pct(dy)} do valor de mercado atual.")
        else:
            fr.append(f"O fluxo de caixa não registra pagamento de dividendos ou juros sobre capital próprio nos "
                      f"12 meses até {data_br(ref)}.")
    var = _v(f, "variacao_12m")
    if var is not None:
        fr.append(f"A cotação variou {pct(var)} em 12 meses, sem contar os proventos.")
    return fr


def resumo_fii(f: dict) -> list[str]:
    fr = []
    I = f["ind"]
    inf = f.get("informe") or {}
    preco, pvp = _v(f, "preco"), _v(f, "pvp")
    if preco and pvp and inf:
        lado = "acima" if pvp > 1 else "abaixo" if pvp < 1 else "igual ao"
        fr.append(f"A cota fechou a R$ {numero(preco)} em {data_br(I['preco']['ref'])}, {lado} do valor "
                  f"patrimonial de R$ {numero(inf['vp_cota'])} informado para {inf['mes']} (P/VP de {numero(pvp)}).")
    meses = f.get("meses") or []
    if len(meses) >= 13 and meses[-1]["cotistas"] and meses[-13]["cotistas"]:
        dif = meses[-1]["cotistas"] - meses[-13]["cotistas"]
        fr.append(f"O fundo tinha {inteiro(meses[-1]['cotistas'])} cotistas em {inf['mes']}, "
                  f"{'mais' if dif >= 0 else 'menos'} {inteiro(abs(dif))} do que 12 meses antes.")
    vs = f.get("vacancia_serie") or []
    if vs:
        u = vs[-1]
        s = f"A vacância física ponderada pela área era de {pct(u['vacancia'])} no trimestre encerrado em {data_br(u['ref'])}"
        ano = [x for x in vs if x["ref"][:4] == str(int(u["ref"][:4]) - 1) and x["ref"][5:] == u["ref"][5:]]
        if ano:
            s += f", contra {pct(ano[0]['vacancia'])} um ano antes"
        fr.append(s + ".")
    elif I.get("vacancia", {}).get("status") == "nao_se_aplica":
        fr.append("O informe trimestral não lista imóveis prontos para renda, então a vacância não se aplica.")
    dy = _v(f, "dy_estimado")
    if dy is not None:
        fr.append(f"Pelo DY que o administrador informa à CVM, os rendimentos dos últimos 12 informes somam cerca de "
                  f"{pct(dy)} da cotação atual (estimativa, ver nota).")
    var = _v(f, "variacao_12m")
    if var is not None:
        fr.append(f"A cotação variou {pct(var)} em 12 meses, sem contar os rendimentos.")
    return fr


def descricao_acao(f: dict, data_geracao: str) -> str:
    partes = []
    for k, rot, fm in (("pl", "P/L", lambda v: numero(v, 1)), ("pvp", "P/VP", lambda v: numero(v, 1)),
                       ("roe", "ROE", pct), ("dy_caixa", "DY de caixa", pct)):
        v = _v(f, k)
        if v is not None:
            partes.append(f"{rot} {fm(v)}")
    lc = (f.get("ttm") or {}).get("lucro_controladora")
    ref = (f.get("ttm") or {}).get("fim")
    s = ", ".join(partes)
    if lc is not None and ref:
        s += f" e lucro de {brl_curto(lc)} em 12 meses até {mes_br(ref)}"
    return (s[:1].upper() + s[1:] + f". Dados da CVM e da B3, atualizados em {data_br(data_geracao)}.").strip()


def descricao_fii(f: dict, data_geracao: str) -> str:
    partes = []
    v = _v(f, "pvp")
    if v is not None:
        partes.append(f"P/VP {numero(v)}")
    v = _v(f, "dy_estimado")
    if v is not None:
        partes.append(f"DY estimado de {pct(v)} em 12 meses")
    v = _v(f, "vacancia")
    if v is not None:
        partes.append(f"vacância de {pct(v)}")
    v = _v(f, "cotistas")
    if v is not None:
        partes.append(f"{inteiro(v)} cotistas")
    s = ", ".join(partes)
    return (s[:1].upper() + s[1:] + f". Dados da CVM e da B3, atualizados em {data_br(data_geracao)}.").strip()
