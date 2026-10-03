"""Especificação simples de um gráfico (a que vai no plano de edição) → JSON de entrada do gerar.py.

    {"serie": "SGS:432" | "COTAHIST:PETR4",
     "periodo": "2020-01-01:" | "2025-10-01:2026-10-01" | "12m" | "5a",
     "rotulo": "Selic: de 2% a 15%",           # título na tela
     "unidade": "%" | "R$" | "pontos",           # opcional: sai da fonte (SGS → %, COTAHIST → R$)
     "comparador": "CDI" | "IBOV" | "IFIX" | "SGS:<n>",   # opcional
     "aviso": true,                              # opcional: "Não é recomendação de investimento" na tela
     "formato": "16:9" | "9:16",                 # opcional (padrão 16:9)
     "kicker": "...", "destaques": "extremos" | [...], "cor_final": "vermelho" | "ouro"}   # opcionais

REGRA DE COMPLIANCE (no código, não só na documentação):
  ativo isolado (COTAHIST: ação ou FII) EXIGE um comparador (IBOV, IFIX ou CDI) desenhado junto,
  OU o aviso explícito na tela. Sem nenhum dos dois → ErroCompliance. Séries do BCB (Selic, IPCA, CDI)
  podem ir sozinhas. A mesma regra é conferida de novo no gerar.validar(), para um JSON escrito à mão
  não passar por fora.

De onde vem cada comparador (nada é inventado; faltou dado → erro):
  CDI   BCB SGS 12 (CDI diário, % a.d.), acumulado dia a dia a partir da 1ª data do gráfico.
  IBOV  BOVA11 (ETF do Ibovespa) no COTAHIST da B3. O COTAHIST não traz o índice; o ETF segue o índice
        menos a taxa de administração (0,10% a.a.). Fonte na tela: "Ibovespa via BOVA11".
  IFIX  XFIX11 (ETF do IFIX) no COTAHIST da B3, preço de fechamento SEM os rendimentos distribuídos
        (subestima o retorno total do IFIX). Fonte na tela: "IFIX via XFIX11, sem rendimentos".
  SGS:n outra série do BCB, no mesmo eixo, para comparar taxa com taxa (Selic × IPCA 12 meses).

Base 100: ativo (R$) com comparador é sempre desenhado em base 100 na 1ª data (as unidades são
diferentes: R$ × índice). Taxa com taxa (% com %) fica no mesmo eixo, com os valores reais.
Taxa (SGS em %) com CDI/IBOV/IFIX é recusado: comparar uma taxa com um índice acumulado não tem leitura.
"""
import datetime as dt, re

import serie as S

AVISO_PADRAO = "Não é recomendação de investimento."
COMPARADORES = {
    "CDI": dict(rotulo="CDI", fonte="BCB (SGS 12)"),
    "IBOV": dict(rotulo="Ibovespa", fonte="B3 (COTAHIST, via BOVA11)", ticker="BOVA11"),
    "IFIX": dict(rotulo="IFIX", fonte="B3 (COTAHIST, via XFIX11, sem rendimentos)", ticker="XFIX11"),
}
UNIDADES = {"%": {"prefixo": "", "sufixo": "%", "casas": 2},
            "R$": {"prefixo": "R$ ", "sufixo": "", "casas": 2},
            "pontos": {"prefixo": "", "sufixo": " pts", "casas": 0}}
FOLGA_DIAS = 7   # o comparador pode começar/terminar até 7 dias corridos fora da série (feriado, fim de semana)


class ErroEspecificacao(ValueError):
    pass


class ErroCompliance(ErroEspecificacao):
    pass


def _periodo(txt, hoje=None):
    txt = (txt or "").strip()
    m = re.fullmatch(r"(\d+)\s*([ma])", txt)
    if m:
        hoje = hoje or dt.date.today()
        n = int(m.group(1))
        meses = n if m.group(2) == "m" else 12 * n
        a, mm = divmod(hoje.year * 12 + hoje.month - 1 - meses, 12)
        return dt.date(a, mm + 1, min(hoje.day, 28)).isoformat(), None
    m = re.fullmatch(r"(\d{4}-\d{2}-\d{2})\s*:\s*(\d{4}-\d{2}-\d{2})?", txt)
    if not m:
        raise ErroEspecificacao(f"periodo {txt!r}: use 'AAAA-MM-DD:', 'AAAA-MM-DD:AAAA-MM-DD', '12m' ou '5a'")
    return m.group(1), m.group(2)


def _fonte_serie(cod):
    m = re.fullmatch(r"(SGS|COTAHIST):([A-Za-z0-9]+)", (cod or "").strip())
    if not m:
        raise ErroEspecificacao(f"serie {cod!r}: use 'SGS:<número>' (BCB) ou 'COTAHIST:<TICKER>' (B3)")
    if m.group(1) == "SGS" and not m.group(2).isdigit():
        raise ErroEspecificacao(f"serie {cod!r}: o código SGS é um número (ex.: SGS:432)")
    return m.group(1), m.group(2).upper()


def checar_compliance(classe, comparador, aviso, rotulo=""):
    """A regra, num lugar só. classe: 'ativo' (COTAHIST) ou 'indicador' (SGS)."""
    if classe == "ativo" and not comparador and not aviso:
        raise ErroCompliance(
            f"gráfico '{rotulo}': ativo isolado (ação ou FII) precisa de um comparador desenhado junto "
            f"(comparador: IBOV, IFIX ou CDI) OU do aviso na tela (aviso: true → '{AVISO_PADRAO}'). "
            "Regra de compliance do canal: preço de um ativo sozinho na tela parece recomendação.")


def _cdi_indice(desde, ate):
    pontos, origem = S.serie_bcb(12, desde, ate)
    if not pontos:
        raise ErroEspecificacao(f"sem CDI (SGS 12) de {desde} a {ate or 'hoje'} no cache")
    idx, v = [], 100.0
    for k, (d, r) in enumerate(pontos):
        if k:
            v *= 1 + r / 100
        idx.append((d, v))
    return idx, origem


def _comparador(nome, desde, ate, classe_principal):
    nome = nome.strip().upper()
    if nome.startswith("SGS:"):
        if classe_principal == "ativo":
            raise ErroEspecificacao("ativo (COTAHIST) se compara com IBOV, IFIX ou CDI, não com uma taxa SGS")
        _, cod = _fonte_serie(nome)
        pontos, origem = S.serie_bcb(int(cod), desde, ate)
        return dict(rotulo=S.NOMES_SGS.get(int(cod), f"SGS {cod}"), fonte=f"BCB (SGS {cod})",
                    linha="degrau" if int(cod) == 432 else "linha"), pontos, origem
    if nome not in COMPARADORES:
        raise ErroEspecificacao(f"comparador {nome!r}: use IBOV, IFIX, CDI ou SGS:<número>")
    if classe_principal == "indicador":
        raise ErroEspecificacao(f"comparador {nome} com uma taxa do BCB: taxa (%) × índice acumulado não tem "
                                "leitura no mesmo gráfico. Compare taxa com taxa (comparador: 'SGS:<n>').")
    info = dict(COMPARADORES[nome], linha="linha")
    if nome == "CDI":
        pontos, origem = _cdi_indice(desde, ate)
    else:
        pontos, origem = S.serie_b3(info["ticker"], desde, ate)
        s = S.saltos(pontos)
        if s:
            raise ErroEspecificacao(f"comparador {info['ticker']} com salto diário acima de 35% em {s[0][0]}: "
                                    "confira o evento antes de usar")
    return info, pontos, origem


def _alinhar(comp, ini, fim, rotulo):
    """Recorta o comparador no período da série principal; falta de dado → erro, nunca extrapola."""
    d_ini, d_fim = dt.date.fromisoformat(ini), dt.date.fromisoformat(fim)
    if not comp:
        raise ErroEspecificacao(f"comparador {rotulo}: sem dado no período {ini} a {fim}")
    c_ini, c_fim = dt.date.fromisoformat(comp[0][0]), dt.date.fromisoformat(comp[-1][0])
    if (c_ini - d_ini).days > FOLGA_DIAS:
        raise ErroEspecificacao(f"comparador {rotulo}: o dado começa em {comp[0][0]}, a série em {ini}")
    if (d_fim - c_fim).days > FOLGA_DIAS:
        raise ErroEspecificacao(f"comparador {rotulo}: o dado termina em {comp[-1][0]}, a série em {fim} "
                                "(atualize o cache do site-ativos)")
    antes = [p for p in comp if p[0] <= ini]
    dentro = [p for p in comp if ini < p[0] <= fim]
    return ([(ini, antes[-1][1])] if antes else []) + dentro


def montar_entrada(espec, duracao=8.0, som=False):
    """espec (dict do plano) → dados para o gerar.py. Levanta ErroEspecificacao/ErroCompliance."""
    if not isinstance(espec, dict):
        raise ErroEspecificacao("a especificação do gráfico é um dict")
    for c in ("serie", "periodo", "rotulo"):
        if not espec.get(c):
            raise ErroEspecificacao(f"gráfico sem '{c}' (obrigatório: serie, periodo, rotulo)")
    fonte, cod = _fonte_serie(espec["serie"])
    classe = "ativo" if fonte == "COTAHIST" else "indicador"
    # a regra vem ANTES de buscar dado: plano errado é recusado mesmo sem cache
    checar_compliance(classe, espec.get("comparador"), espec.get("aviso"), espec["rotulo"])
    desde, ate = _periodo(espec["periodo"])
    if fonte == "SGS":
        pontos, origem = S.serie_bcb(int(cod), desde, ate)
        linha = "degrau" if int(cod) == 432 else "linha"
        unidade = UNIDADES[espec.get("unidade", "%")]
        kicker = espec.get("kicker") or S.NOMES_SGS.get(int(cod), f"SGS {cod}")
        texto_fonte = f"Fonte: BCB (SGS {cod})"
        variacao = "pp" if unidade["sufixo"] == "%" else "pct"
    else:
        pontos, origem = S.serie_b3(cod, desde, ate)
        s = S.saltos(pontos)
        if s and not espec.get("aceitar_saltos"):
            raise ErroEspecificacao(f"{cod}: salto diário acima de 35% em {s[0][0]} ({s[0][1]:.2f} → {s[0][2]:.2f}); "
                                    "provável desdobramento/grupamento, o COTAHIST não ajusta")
        linha = "linha"
        unidade = UNIDADES[espec.get("unidade", "R$")]
        kicker = espec.get("kicker") or f"{cod} · fechamento diário"
        texto_fonte = "Fonte: B3 (COTAHIST, fechamento sem ajuste)"
        variacao = "pct"
    if len(pontos) < 2:
        raise ErroEspecificacao(f"{espec['serie']}: menos de 2 pontos no período {desde} a {ate or 'hoje'}")
    if linha == "degrau":
        pontos = S.so_mudancas(pontos)
    dados = {
        "titulo": espec["rotulo"], "kicker": kicker,
        "nome_serie": cod if fonte == "COTAHIST" else S.NOMES_SGS.get(int(cod), f"SGS {cod}"), "fonte": texto_fonte, "classe": classe,
        "formato": espec.get("formato", "16:9"), "duracao": float(duracao), "linha": linha,
        "unidade": dict(unidade), "variacao": variacao, "cor_final": espec.get("cor_final", "vermelho"),
        "som": som, "destaques": [],
        "serie": [{"data": d, "valor": round(v, 6)} for d, v in pontos],
        "_origem": {"arquivo": origem, "espec": espec},
    }
    if espec.get("aviso"):
        dados["aviso"] = AVISO_PADRAO if espec["aviso"] is True else str(espec["aviso"])
    if espec.get("comparador"):
        info, comp, origem_c = _comparador(espec["comparador"], desde, ate, classe)
        comp = _alinhar(comp, pontos[0][0], pontos[-1][0], info["rotulo"])
        dados["comparador"] = {"rotulo": info["rotulo"], "fonte": info["fonte"], "linha": info["linha"],
                               "serie": [{"data": d, "valor": round(v, 6)} for d, v in comp]}
        dados["base100"] = classe == "ativo"
        dados["fonte"] = f"{texto_fonte} · {info['rotulo']}: {info['fonte']}"
        dados["_origem"]["comparador"] = origem_c
    dq = espec.get("destaques")
    if dq == "extremos":
        c, pre, suf = unidade["casas"], unidade["prefixo"], unidade["sufixo"]
        vmin, vmax = min(pontos, key=lambda p: p[1]), max(pontos, key=lambda p: p[1])
        for nome, (d, v), pos in (("Mínima", vmin, "acima"), ("Máxima", vmax, "abaixo")):
            if d != pontos[-1][0]:
                dados["destaques"].append({"data": d, "rotulo": f"{nome}: {pre}{S.fmt_br(v, c)}{suf}", "posicao": pos})
    elif isinstance(dq, list):
        dados["destaques"] = dq
    return dados
