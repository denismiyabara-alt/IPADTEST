"""Escolha dos ativos do MVP (DESENHO 8.1). Critério objetivo, não é recomendação.

Ações: maior volume financeiro médio diário em 12 meses (COTAHIST, CODBDI 02, TPMERC 010), um
ticker por empresa (o mais negociado), só entre os tickers válidos que já têm página cotacao-*.
FIIs: maior volume médio diário em 12 meses (CODBDI 12), com pelo menos 24 meses de negociação e
informe mensal recente na CVM.
"""
import json
import re
from datetime import timedelta

from . import config

INVALIDO = re.compile(r"^[a-z0-9]{4}\d{1,2}l$")  # ex.: b8in8l, poly8l (lixo de importação)


def tickers_cotacao(caminho=None) -> tuple[list[str], list[str]]:
    """Lê seo/varredura.json (chave cotacoes_linkadas). Devolve (válidos, inválidos)."""
    caminho = caminho or config.SEO_VARREDURA
    if not caminho.exists():
        return [], []
    urls = json.loads(caminho.read_text()).get("cotacoes_linkadas", [])
    validos, invalidos = [], []
    for u in urls:
        m = re.search(r"/cotacao-([a-z0-9]+)/?$", u)
        if not m:
            continue
        t = m.group(1)
        (validos if re.fullmatch(r"[a-z0-9]{3}[a-z]\d{1,2}", t) and not INVALIDO.match(t) else invalidos).append(t)
    return sorted(set(validos)), sorted(set(invalidos))


def fii_por_isin_unico(con) -> tuple[dict, list]:
    """ISIN -> CNPJ. Achado: o informe mensal tem ISIN repetido em CNPJs diferentes (ex.: um fundo novo
    declarando o ISIN de outro). Fica o CNPJ com mais informes; empate, o de nome parecido com o ticker."""
    por_isin: dict[str, list] = {}
    for r in con.execute("""SELECT f.isin, f.cnpj, f.nome, (SELECT COUNT(*) FROM fii_mensal m WHERE m.cnpj=f.cnpj)
                            FROM fii f WHERE f.isin LIKE 'BR__________'"""):
        por_isin.setdefault(r[0], []).append((r[3], r[1], r[2]))
    mapa, colisoes = {}, []
    for isin, cands in por_isin.items():
        prefixo = isin[2:6]
        cands.sort(key=lambda c: (c[0], prefixo in (c[2] or "").upper().replace(" ", "")), reverse=True)
        mapa[isin] = cands[0][1]
        if len(cands) > 1:
            colisoes.append({"isin": isin, "escolhido": cands[0][1],
                             "candidatos": [{"cnpj": c[1], "nome": c[2], "informes": c[0]} for c in cands]})
    return mapa, colisoes


def volume_medio(con, codbdi: str, inicio: str) -> dict[str, float]:
    """Volume financeiro total na janela ÷ número de pregões da janela (dias sem negócio contam como zero)."""
    n_pregoes = con.execute("SELECT COUNT(DISTINCT data) FROM preco_diario WHERE data>=?", (inicio,)).fetchone()[0] or 1
    return {r[0]: r[1] / n_pregoes for r in con.execute(
        "SELECT ticker, SUM(volume_rs) FROM preco_diario WHERE codbdi=? AND data>=? GROUP BY ticker", (codbdi, inicio))}


def selecionar(con, n_acoes=10, n_fiis=10) -> dict:
    ultimo = con.execute("SELECT MAX(data) FROM preco_diario").fetchone()[0]
    from datetime import date
    fim = date.fromisoformat(ultimo)
    inicio = (fim - timedelta(days=365)).isoformat()
    validos, invalidos = tickers_cotacao()
    tem_lista = bool(validos)
    universo = {t.upper() for t in validos}

    vol = volume_medio(con, "02", inicio)
    emissor = {r[0]: r[1] for r in con.execute("SELECT ticker, cnpj_emissor FROM ativo")}
    tipo = {r[0]: r[1] for r in con.execute("SELECT cnpj, tipo FROM empresa")}
    classe = {r[0]: r[1] for r in con.execute("SELECT ticker, classe FROM ativo")}

    ranking = sorted(((v, t) for t, v in vol.items() if (not tem_lista or t in universo) and t in emissor),
                     reverse=True)
    acoes, vistos = [], set()
    for v, t in ranking:
        c = emissor[t]
        if c in vistos:
            continue
        vistos.add(c)
        acoes.append({"ticker": t, "cnpj": c, "volume_medio": round(v, 2), "tipo": tipo.get(c, "comum"),
                      "classe": classe.get(t)})
    top = acoes[:n_acoes]
    notas = []
    colisoes = []
    if not any(a["tipo"] == "banco" for a in top):
        banco = next(a for a in acoes if a["tipo"] == "banco")
        notas.append(f"Nenhum banco no top {n_acoes}: {banco['ticker']} entrou no lugar de {top[-1]['ticker']}.")
        top[-1] = banco
    unit_teste = None
    if not any(a["classe"] == "UNIT" for a in top):
        unit_teste = next((a for a in acoes if a["classe"] == "UNIT"), None)
        if unit_teste:
            notas.append(f"Nenhuma unit no top {n_acoes}: {unit_teste['ticker']} (a unit mais negociada da lista) "
                         "entra só nos testes, não no MVP publicado (DESENHO 8.1).")

    # FIIs
    volf = volume_medio(con, "12", inicio)
    inicio24 = (fim - timedelta(days=730)).isoformat()
    primeiro = {r[0]: r[1] for r in con.execute("SELECT ticker, MIN(data) FROM preco_diario WHERE codbdi='12' GROUP BY ticker")}
    isin = {r[0]: r[1] for r in con.execute("SELECT ticker, isin FROM preco_diario WHERE codbdi='12' AND data=(SELECT MAX(data) FROM preco_diario p2 WHERE p2.ticker=preco_diario.ticker)")}
    fii_por_isin, colisoes = fii_por_isin_unico(con)
    ultimo_informe = {r[0]: r[1] for r in con.execute("SELECT cnpj, MAX(data_ref) FROM fii_mensal GROUP BY cnpj")}
    corte_informe = (fim.replace(day=1) - timedelta(days=62)).replace(day=1).isoformat()
    fiis, descartados = [], []
    for v, t in sorted(((v, t) for t, v in volf.items()), reverse=True):
        c = fii_por_isin.get(isin.get(t))
        motivo = None
        if not c:
            motivo = "sem informe mensal de FII na CVM (pode ser Fiagro ou FI-Infra)"
        elif primeiro.get(t, "9999") > inicio24:
            motivo = "menos de 24 meses de negociação"
        elif ultimo_informe.get(c, "") < corte_informe:
            motivo = f"último informe mensal antes de {corte_informe}"
        if motivo:
            descartados.append({"ticker": t, "volume_medio": round(v, 2), "motivo": motivo})
            continue
        fiis.append({"ticker": t, "cnpj": c, "volume_medio": round(v, 2)})
        if len(fiis) == n_fiis:
            break
    return {
        "janela": {"inicio": inicio, "fim": ultimo},
        "lista_cotacao": {"existe": tem_lista, "validos": len(validos), "invalidos": invalidos},
        "acoes": top, "acoes_ranking_completo": acoes[:30], "unit_teste": unit_teste,
        "fiis": fiis, "isin_repetido_no_informe": colisoes, "fiis_descartados_no_caminho": descartados[:15], "notas": notas,
        "aviso": "Escolha pelo volume negociado na B3 nos últimos 12 meses. A escolha não é recomendação.",
    }
