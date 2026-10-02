"""Etapa 2: normalizar. Lê os arquivos do cache e grava tudo no SQLite (`cache/dados.sqlite`).

Regras (DESENHO 2 e 4.1):
- CSV da CVM: latin-1, separador `;`.
- ESCALA_MOEDA = MIL vira x1000. Exceção: as linhas de LPA (`3.99...`) já vêm em reais por ação
  e não são multiplicadas (achado do primeiro download: o arquivo marca MIL também nelas).
- Para cada (CNPJ, documento, DT_REFER), só fica a maior VERSAO.
- COTAHIST: posições fixas de 245 bytes; preço dividido por 100 e por FATCOT.
"""
import csv
import gzip
import io
import json
import re
import sqlite3
import zipfile
from pathlib import Path

from . import config
from .rede import meta_de

csv.field_size_limit(10_000_000)

ESQUEMA = """
CREATE TABLE IF NOT EXISTS fonte_arquivo (
  id INTEGER PRIMARY KEY, fonte TEXT, url TEXT, arquivo TEXT, etag TEXT, last_modified TEXT,
  baixado_em TEXT, sha256 TEXT, linhas INTEGER, UNIQUE(fonte, arquivo));
CREATE TABLE IF NOT EXISTS empresa (
  cnpj TEXT PRIMARY KEY, cd_cvm TEXT, nome TEXT, nome_comercial TEXT, setor_cvm TEXT, tipo TEXT,
  situacao TEXT, fonte_arquivo_id INTEGER, data_ref TEXT);
CREATE TABLE IF NOT EXISTS ativo (
  ticker TEXT PRIMARY KEY, cnpj_emissor TEXT, isin TEXT, classe TEXT, composicao_unit TEXT,
  composicao_fonte TEXT, listado_desde TEXT, ativo INTEGER, fonte_arquivo_id INTEGER);
CREATE TABLE IF NOT EXISTS documento (
  cnpj TEXT, doc TEXT, dt_refer TEXT, versao INTEGER, id_doc TEXT, dt_receb TEXT, link TEXT,
  fonte_arquivo_id INTEGER, PRIMARY KEY(cnpj, doc, dt_refer, versao));
CREATE TABLE IF NOT EXISTS conta (
  id INTEGER PRIMARY KEY, cnpj TEXT, doc TEXT, demonstracao TEXT, escopo TEXT, dt_refer TEXT,
  dt_ini_exerc TEXT, dt_fim_exerc TEXT, ordem_exerc TEXT, versao INTEGER, cd_conta TEXT,
  ds_conta TEXT, conta_fixa TEXT, valor_reais REAL, escala_original TEXT, fonte_arquivo_id INTEGER);
CREATE INDEX IF NOT EXISTS conta_busca ON conta(cnpj, demonstracao, escopo, cd_conta, dt_fim_exerc);
CREATE INDEX IF NOT EXISTS conta_versao ON conta(cnpj, doc, dt_refer, versao);
CREATE TABLE IF NOT EXISTS capital (
  cnpj TEXT, doc TEXT, dt_refer TEXT, versao INTEGER, qt_on REAL, qt_pn REAL, qt_total REAL,
  qt_on_tesouraria REAL, qt_pn_tesouraria REAL, fonte_arquivo_id INTEGER,
  PRIMARY KEY(cnpj, doc, dt_refer, versao));
CREATE TABLE IF NOT EXISTS preco_diario (
  ticker TEXT, data TEXT, abertura REAL, maxima REAL, minima REAL, fechamento REAL, medio REAL,
  negocios INTEGER, quantidade REAL, volume_rs REAL, fatcot INTEGER, isin TEXT, codbdi TEXT,
  especificacao TEXT, nome_pregao TEXT, fonte_arquivo_id INTEGER, PRIMARY KEY(ticker, data));
CREATE TABLE IF NOT EXISTS evento_societario (
  ticker TEXT, tipo TEXT, fator REAL, data_ex TEXT, doc_url TEXT, conferido_por TEXT, conferido_em TEXT);
CREATE TABLE IF NOT EXISTS provento (
  ticker TEXT, tipo TEXT, valor_bruto_por_acao REAL, data_aprovacao TEXT, data_com TEXT,
  data_ex TEXT, data_pagamento TEXT, doc_url TEXT, origem TEXT, status TEXT,
  aprovado_por TEXT, aprovado_em TEXT);
CREATE TABLE IF NOT EXISTS fii (
  cnpj TEXT PRIMARY KEY, nome TEXT, isin TEXT, segmento TEXT, mandato TEXT, tipo_gestao TEXT,
  publico_alvo TEXT, administrador TEXT, data_ref TEXT, fonte_arquivo_id INTEGER);
CREATE TABLE IF NOT EXISTS fii_mensal (
  cnpj TEXT, data_ref TEXT, versao INTEGER, cotistas INTEGER, pl REAL, cotas_emitidas REAL,
  vp_cota REAL, dy_mes_informado REAL, rentab_efetiva_mes REAL, rendimentos_distribuir REAL,
  data_entrega TEXT, fonte_arquivo_id INTEGER, PRIMARY KEY(cnpj, data_ref));
CREATE TABLE IF NOT EXISTS fii_imovel_trim (
  cnpj TEXT, data_ref TEXT, versao INTEGER, imovel TEXT, classe TEXT, area_m2 REAL,
  vacancia_pct REAL, inadimplencia_pct REAL, pct_receita REAL, fonte_arquivo_id INTEGER);
CREATE TABLE IF NOT EXISTS macro (serie INTEGER, data TEXT, valor REAL, fonte_arquivo_id INTEGER,
  PRIMARY KEY(serie, data));
CREATE TABLE IF NOT EXISTS indicador (
  ticker TEXT, nome TEXT, valor REAL, status TEXT, data_preco TEXT, periodo_contabil TEXT,
  formula_versao TEXT, insumos TEXT, fonte TEXT, calculado_em TEXT, PRIMARY KEY(ticker, nome));
CREATE TABLE IF NOT EXISTS pagina (
  url TEXT PRIMARY KEY, tipo TEXT, indexavel INTEGER, hash_conteudo TEXT, lastmod_dados TEXT,
  publicado_em TEXT);
"""

DEMONSTRACOES = ["BPA", "BPP", "DRE", "DFC_MI", "DFC_MD", "DVA"]


def conectar(caminho: Path | None = None) -> sqlite3.Connection:
    caminho = caminho or config.DB
    caminho.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(caminho)
    con.row_factory = sqlite3.Row
    con.executescript(ESQUEMA)
    return con


def so_digitos(cnpj: str) -> str:
    return re.sub(r"\D", "", cnpj or "").zfill(14)


def num(txt: str) -> float | None:
    txt = (txt or "").strip()
    if not txt:
        return None
    try:
        return float(txt.replace(",", ".")) if txt.count(",") == 1 and "." not in txt else float(txt)
    except ValueError:
        return None


def registrar_fonte(con, fonte: str, caminho: Path, membro: str | None = None, linhas: int | None = None) -> int:
    meta = meta_de(caminho)
    arquivo = caminho.name + (f"!{membro}" if membro else "")
    con.execute(
        """INSERT INTO fonte_arquivo(fonte,url,arquivo,etag,last_modified,baixado_em,sha256,linhas)
           VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(fonte,arquivo) DO UPDATE SET
           url=excluded.url, etag=excluded.etag, last_modified=excluded.last_modified,
           baixado_em=excluded.baixado_em, sha256=excluded.sha256, linhas=excluded.linhas""",
        (fonte, meta.get("url"), arquivo, meta.get("etag"), meta.get("last_modified"),
         meta.get("baixado_em"), meta.get("sha256"), linhas))
    return con.execute("SELECT id FROM fonte_arquivo WHERE fonte=? AND arquivo=?", (fonte, arquivo)).fetchone()[0]


def fmt_cnpj(c: str) -> str:
    c = so_digitos(c)
    return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}"


def ler_csv_filtrado(f, cnpjs: set[str]):
    """Como ler_csv_cvm, mas só decodifica as linhas que começam com um dos CNPJs (filtro em bytes).
    Os CSVs de DFP/ITR somam alguns GB por ano; assim a leitura cai de minutos para segundos."""
    prefixos = {fmt_cnpj(c).encode("latin-1") for c in cnpjs}
    cab = next(csv.reader([f.readline().decode("latin-1").rstrip("\r\n")], delimiter=";"))
    for linha in f:
        if linha[:18] in prefixos:
            valores = next(csv.reader([linha.decode("latin-1").rstrip("\r\n")], delimiter=";"))
            yield dict(zip(cab, valores))


def ler_csv_cvm(f) -> csv.DictReader:
    """`f` é um arquivo binário (de dentro do ZIP, em streaming)."""
    return csv.DictReader(io.TextIOWrapper(f, encoding="latin-1", newline=""), delimiter=";")


# --------------------------------------------------------------------------- cadastro e FCA

def tipo_por_setor(setor: str) -> str:
    """Só o setor "Bancos" e o de seguradoras viram tipo especial. "Emp. Adm. Part." (holding no nome do
    setor) é usado pela CVM até para WEG e Axia, então holding só vem da lista manual."""
    s = (setor or "").lower()
    if s.startswith("bancos") or s == "intermediação financeira":
        return "banco"
    if s.startswith("seguradoras"):
        return "seguradora"
    return "comum"


# Correções manuais (DESENHO 4.6): o setor da CVM nem sempre basta.
TIPO_MANUAL = {
    "60872504000123": "banco",    # Itaú Unibanco Holding (setor CVM: Bancos)
    "60746948000112": "banco",    # Bradesco
    "00000000000191": "banco",    # Banco do Brasil
    "90400888000142": "banco",    # Santander Brasil
    "30306294000145": "banco",    # BTG Pactual
    "92702067000196": "banco",    # Banrisul
    "61532644000115": "holding",  # Itaúsa
    "17344597000194": "seguradora",  # BB Seguridade
    "22543331000100": "seguradora",  # Caixa Seguridade
}


def normalizar_cadastro(con) -> None:
    caminho = config.RAW / "cvm" / "cad_cia_aberta.csv"
    with open(caminho, "rb") as f:
        linhas = list(ler_csv_cvm(f))
    fid = registrar_fonte(con, "CVM-CAD", caminho, linhas=len(linhas))
    # Uma empresa pode ter mais de um registro (cancelado e ativo): fica o ativo, senão o mais recente.
    melhor: dict[str, dict] = {}
    for r in linhas:
        c = so_digitos(r["CNPJ_CIA"])
        atual = melhor.get(c)
        ativo = r["SIT"].startswith("ATIVO")
        if atual is None or (ativo and not atual["SIT"].startswith("ATIVO")) or \
           (ativo == atual["SIT"].startswith("ATIVO") and r["DT_INI_SIT"] > atual["DT_INI_SIT"]):
            melhor[c] = r
    for c, r in melhor.items():
        tipo = TIPO_MANUAL.get(c) or tipo_por_setor(r["SETOR_ATIV"])
        con.execute("INSERT OR REPLACE INTO empresa VALUES(?,?,?,?,?,?,?,?,?)",
                    (c, r["CD_CVM"].lstrip("0"), r["DENOM_SOCIAL"], r["DENOM_COMERC"], r["SETOR_ATIV"],
                     tipo, r["SIT"], fid, r["DT_INI_SIT"]))


CLASSE_POR_VM = {"Ações Ordinárias": "ON", "Ações Preferenciais": "PN", "Units": "UNIT"}


def parse_composicao_unit(txt: str) -> dict | None:
    """'1 ON E 2 PNA' -> {'ON':1,'PN':2}; '1 KLBN3 + 4 KLBN4' -> {'ON':1,'PN':4}."""
    t = (txt or "").upper().replace("AÇÃO ORDINÁRIA", "ON").replace("AÇÕES ORDINÁRIAS", "ON")
    t = t.replace("AÇÕES PREFERENCIAIS", "PN").replace("AÇÃO PREFERENCIAL", "PN")
    t = re.sub(r"\b[A-Z]{4}3\b", "ON", t)
    t = re.sub(r"\b[A-Z]{4}[4-8]\b", "PN", t)
    comp: dict[str, int] = {}
    for qtd, cls in re.findall(r"(\d+)\s*(ON|PN)[A-Z]*S?\b", t):
        comp[cls] = comp.get(cls, 0) + int(qtd)
    if "RECIBO" in t or not comp:
        return None
    return comp


def normalizar_fca(con) -> None:
    caminho = config.RAW / "cvm" / f"fca_cia_aberta_{config.HOJE.year}.zip"
    membro = f"fca_cia_aberta_valor_mobiliario_{config.HOJE.year}.csv"
    with zipfile.ZipFile(caminho) as z, z.open(membro) as f:
        linhas = list(ler_csv_cvm(f))
    fid = registrar_fonte(con, "CVM-FCA", caminho, membro, len(linhas))
    # Maior versão por CNPJ
    maxv: dict[str, int] = {}
    for r in linhas:
        c = so_digitos(r["CNPJ_Companhia"])
        maxv[c] = max(maxv.get(c, 0), int(r["Versao"] or 0))
    for r in linhas:
        c = so_digitos(r["CNPJ_Companhia"])
        if int(r["Versao"] or 0) != maxv[c]:
            continue
        classe = CLASSE_POR_VM.get(r["Valor_Mobiliario"])
        tk = (r["Codigo_Negociacao"] or "").strip().upper()
        if not classe or not re.fullmatch(r"[A-Z]{4}\d{1,2}", tk) or r["Mercado"] != "Bolsa":
            continue
        comp = parse_composicao_unit(r["Composicao_BDR_Unit"]) if classe == "UNIT" else None
        con.execute("INSERT OR REPLACE INTO ativo VALUES(?,?,?,?,?,?,?,?,?)",
                    (tk, c, None, classe, json.dumps(comp) if comp else None,
                     f"FCA {config.HOJE.year}: \"{r['Composicao_BDR_Unit']}\"" if comp else None,
                     r["Data_Inicio_Negociacao"], 0 if r["Data_Fim_Negociacao"] else 1, fid))


# Units cuja linha no FCA está incompleta (ex.: BTG com código "000000"). Composição digitada à mão,
# com a fonte. Conferir no estatuto antes de publicar.
UNITS_MANUAIS = {
    "BPAC11": ("30306294000145", {"ON": 1, "PN": 2}, "FCA 2026: \"1 ON E 2 PNA\" (linha sem ticker; ticker pelo prefixo BPAC)"),
}


def completar_ativos(con) -> None:
    """Liga ao emissor os tickers do COTAHIST que o FCA não traz, pelo prefixo de 4 letras."""
    for tk, (cnpj, comp, fonte) in UNITS_MANUAIS.items():
        con.execute("INSERT OR REPLACE INTO ativo(ticker,cnpj_emissor,classe,composicao_unit,composicao_fonte,ativo)"
                    " VALUES(?,?,?,?,?,1)", (tk, cnpj, "UNIT", json.dumps(comp), fonte))
    prefixos: dict[str, set] = {}
    for r in con.execute("SELECT ticker, cnpj_emissor FROM ativo"):
        prefixos.setdefault(r["ticker"][:4], set()).add(r["cnpj_emissor"])
    faltam = con.execute("""SELECT DISTINCT p.ticker, p.isin, p.especificacao FROM preco_diario p
                            LEFT JOIN ativo a ON a.ticker=p.ticker WHERE a.ticker IS NULL AND p.codbdi='02'""").fetchall()
    for r in faltam:
        cands = prefixos.get(r["ticker"][:4], set())
        if len(cands) == 1:
            esp = (r["especificacao"] or "").upper()
            classe = "UNIT" if esp.startswith("UNT") else "ON" if esp.startswith("ON") else "PN" if esp.startswith("PN") else None
            if classe:
                con.execute("INSERT OR IGNORE INTO ativo(ticker,cnpj_emissor,isin,classe,ativo) VALUES(?,?,?,?,1)",
                            (r["ticker"], next(iter(cands)), r["isin"], classe))
    # ISIN a partir do COTAHIST
    con.execute("""UPDATE ativo SET isin=(SELECT p.isin FROM preco_diario p WHERE p.ticker=ativo.ticker
                   ORDER BY p.data DESC LIMIT 1) WHERE isin IS NULL""")


# --------------------------------------------------------------------------- COTAHIST

def ler_linha_cotahist(linha: str) -> dict:
    """Layout B3 (SeriesHistoricas_Layout.pdf). Preços com 2 decimais implícitos."""
    fat = int(linha[210:217] or 1) or 1
    p = lambda a, b: int(linha[a:b]) / 100 / fat  # noqa: E731
    return {
        "data": f"{linha[2:6]}-{linha[6:8]}-{linha[8:10]}",
        "codbdi": linha[10:12],
        "ticker": linha[12:24].strip(),
        "tpmerc": linha[24:27],
        "nome_pregao": linha[27:39].strip(),
        "especificacao": linha[39:49].strip(),
        "abertura": p(56, 69), "maxima": p(69, 82), "minima": p(82, 95),
        "medio": p(95, 108), "fechamento": p(108, 121),
        "negocios": int(linha[147:152]), "quantidade": int(linha[152:170]),
        "volume_rs": int(linha[170:188]) / 100,
        "fatcot": fat, "isin": linha[230:242],
    }


def normalizar_cotahist(con, bdis=("02", "12")) -> None:
    for gz in sorted((config.RAW / "b3").glob("COTAHIST_*.txt.gz")):
        meta_nome = gz.name.replace(".txt.gz", ".ZIP")
        fid = registrar_fonte(con, "B3-COTAHIST", gz.with_name(meta_nome))
        n = 0
        with gzip.open(gz, "rt", encoding="latin-1") as f:
            lote = []
            for linha in f:
                if linha[10:12] not in bdis:
                    continue
                r = ler_linha_cotahist(linha)
                lote.append((r["ticker"], r["data"], r["abertura"], r["maxima"], r["minima"], r["fechamento"],
                             r["medio"], r["negocios"], r["quantidade"], r["volume_rs"], r["fatcot"], r["isin"],
                             r["codbdi"], r["especificacao"], r["nome_pregao"], fid))
                n += 1
            con.executemany("INSERT OR REPLACE INTO preco_diario VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", lote)
        con.execute("UPDATE fonte_arquivo SET linhas=? WHERE id=?", (n, fid))


# --------------------------------------------------------------------------- DFP / ITR

def normalizar_demonstracoes(con, cnpjs: set[str]) -> None:
    """Carrega as contas dos CNPJs escolhidos (DFP e ITR, con e ind) e fica só com a maior VERSAO."""
    con.execute("DELETE FROM conta")
    con.execute("DELETE FROM capital")
    con.execute("DELETE FROM documento")
    for doc, anos in (("DFP", config.ANOS_DFP), ("ITR", config.ANOS_ITR)):
        for ano in anos:
            caminho = config.RAW / "cvm" / f"{doc.lower()}_cia_aberta_{ano}.zip"
            if not caminho.exists():
                continue
            with zipfile.ZipFile(caminho) as z:
                nomes = set(z.namelist())
                _carregar_zip_doc(con, z, nomes, doc, ano, caminho, cnpjs)
    manter_maior_versao(con)


def _carregar_zip_doc(con, z, nomes, doc, ano, caminho, cnpjs) -> None:
    p = doc.lower()
    indice = f"{p}_cia_aberta_{ano}.csv"
    if indice in nomes:
        fid = registrar_fonte(con, f"CVM-{doc}", caminho, indice)
        with z.open(indice) as f:
            for r in ler_csv_cvm(f):
                c = so_digitos(r["CNPJ_CIA"])
                if c in cnpjs:
                    con.execute("INSERT OR REPLACE INTO documento VALUES(?,?,?,?,?,?,?,?)",
                                (c, doc, r["DT_REFER"], int(r["VERSAO"]), r["ID_DOC"], r["DT_RECEB"], r["LINK_DOC"], fid))
    cap = f"{p}_cia_aberta_composicao_capital_{ano}.csv"
    if cap in nomes:
        fid = registrar_fonte(con, f"CVM-{doc}", caminho, cap)
        with z.open(cap) as f:
            for r in ler_csv_filtrado(f, cnpjs):
                c = so_digitos(r["CNPJ_CIA"])
                if c in cnpjs:
                    con.execute("INSERT OR REPLACE INTO capital VALUES(?,?,?,?,?,?,?,?,?,?)",
                                (c, doc, r["DT_REFER"], int(r["VERSAO"]), num(r["QT_ACAO_ORDIN_CAP_INTEGR"]),
                                 num(r["QT_ACAO_PREF_CAP_INTEGR"]), num(r["QT_ACAO_TOTAL_CAP_INTEGR"]),
                                 num(r["QT_ACAO_ORDIN_TESOURO"]), num(r["QT_ACAO_PREF_TESOURO"]), fid))
    for dem in DEMONSTRACOES:
        for escopo in ("con", "ind"):
            membro = f"{p}_cia_aberta_{dem}_{escopo}_{ano}.csv"
            if membro not in nomes:
                continue
            fid = registrar_fonte(con, f"CVM-{doc}", caminho, membro)
            with z.open(membro) as f:
                lote = [linha_conta(r, doc, dem, escopo, fid) for r in ler_csv_filtrado(f, cnpjs)]
            con.executemany("""INSERT INTO conta(cnpj,doc,demonstracao,escopo,dt_refer,dt_ini_exerc,dt_fim_exerc,
                               ordem_exerc,versao,cd_conta,ds_conta,conta_fixa,valor_reais,escala_original,fonte_arquivo_id)
                               VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""", lote)


def fator_escala(escala: str, cd_conta: str) -> int:
    """MIL = x1000. LPA (3.99...) é em reais por ação mesmo quando o arquivo diz MIL."""
    if cd_conta.startswith("3.99"):
        return 1
    return 1000 if (escala or "").upper() == "MIL" else 1


def linha_conta(r: dict, doc: str, dem: str, escopo: str, fid: int) -> tuple:
    cd = r["CD_CONTA"]
    v = num(r["VL_CONTA"])
    v = None if v is None else v * fator_escala(r["ESCALA_MOEDA"], cd)
    return (so_digitos(r["CNPJ_CIA"]), doc, dem, escopo, r["DT_REFER"], r.get("DT_INI_EXERC") or None,
            r["DT_FIM_EXERC"], r["ORDEM_EXERC"].replace("Ú", "U"), int(r["VERSAO"]), cd, r["DS_CONTA"],
            r["ST_CONTA_FIXA"], v, r["ESCALA_MOEDA"], fid)


def manter_maior_versao(con) -> int:
    """Apaga linhas de versões antigas: para cada (CNPJ, doc, DT_REFER) fica só a maior VERSAO."""
    apagadas = 0
    for tabela in ("conta", "capital", "documento"):
        cur = con.execute(f"""DELETE FROM {tabela} WHERE versao < (SELECT MAX(t2.versao) FROM {tabela} t2
                              WHERE t2.cnpj={tabela}.cnpj AND t2.doc={tabela}.doc AND t2.dt_refer={tabela}.dt_refer)""")
        apagadas += cur.rowcount
    return apagadas


# --------------------------------------------------------------------------- FII

def _membro(nomes, prefixo):
    for n in nomes:
        if n.startswith(prefixo):
            return n
    return None


def normalizar_fii(con, cnpjs: set[str] | None = None) -> None:
    """Informe mensal (geral + complemento + ativo_passivo) e trimestral (imóveis)."""
    con.execute("DELETE FROM fii_mensal")
    con.execute("DELETE FROM fii_imovel_trim")
    cadastro_fii: dict[str, tuple] = {}
    for ano in config.ANOS_FII:
        caminho = config.RAW / "cvm" / f"inf_mensal_fii_{ano}.zip"
        if not caminho.exists():
            continue
        with zipfile.ZipFile(caminho) as z:
            nomes = z.namelist()
            geral = _membro(nomes, "inf_mensal_fii_geral_")
            comp = _membro(nomes, "inf_mensal_fii_complemento_")
            ap = _membro(nomes, "inf_mensal_fii_ativo_passivo_")
            fid = registrar_fonte(con, "CVM-FII-MENSAL", caminho, comp)
            versoes = {}
            if geral:
                fidg = registrar_fonte(con, "CVM-FII-MENSAL", caminho, geral)
                with z.open(geral) as f:
                    for r in ler_csv_cvm(f):
                        c = so_digitos(r.get("CNPJ_Fundo_Classe") or r.get("CNPJ_Fundo"))
                        if cnpjs is not None and c not in cnpjs:
                            continue
                        v = int(r.get("Versao") or 1)
                        if v >= versoes.get((c, r["Data_Referencia"]), (0, None))[0]:
                            versoes[(c, r["Data_Referencia"])] = (v, r.get("Data_Entrega"))
                        if c not in cadastro_fii or r["Data_Referencia"] >= cadastro_fii[c][8]:
                            cadastro_fii[c] = (c, r.get("Nome_Fundo_Classe") or r.get("Nome_Fundo"), r.get("Codigo_ISIN"),
                                               r.get("Segmento_Atuacao"), r.get("Mandato"), r.get("Tipo_Gestao"),
                                               r.get("Publico_Alvo"), r.get("Nome_Administrador"),
                                               r["Data_Referencia"], fidg)
            rend = {}
            if ap:
                with z.open(ap) as f:
                    for r in ler_csv_cvm(f):
                        c = so_digitos(r.get("CNPJ_Fundo_Classe") or r.get("CNPJ_Fundo"))
                        if cnpjs is None or c in cnpjs:
                            rend[(c, r["Data_Referencia"])] = num(r.get("Rendimentos_Distribuir"))
            melhor = {}
            with z.open(comp) as f:
                for r in ler_csv_cvm(f):
                    c = so_digitos(r.get("CNPJ_Fundo_Classe") or r.get("CNPJ_Fundo"))
                    if cnpjs is not None and c not in cnpjs:
                        continue
                    chave = (c, r["Data_Referencia"])
                    if chave not in melhor or int(r.get("Versao") or 1) >= int(melhor[chave].get("Versao") or 1):
                        melhor[chave] = r
            for (c, dref), r in melhor.items():
                v = int(r.get("Versao") or 1)
                entrega = versoes.get((c, dref), (v, None))[1]
                con.execute("""INSERT OR REPLACE INTO fii_mensal VALUES(?,?,?,?,?,?,?,?,?,?,?,?)""",
                            (c, dref, v, int(num(r.get("Total_Numero_Cotistas")) or 0),
                             num(r.get("Patrimonio_Liquido")), num(r.get("Cotas_Emitidas")),
                             num(r.get("Valor_Patrimonial_Cotas")), num(r.get("Percentual_Dividend_Yield_Mes")),
                             num(r.get("Percentual_Rentabilidade_Efetiva_Mes")), rend.get((c, dref)),
                             entrega, fid))
    con.executemany("INSERT OR REPLACE INTO fii VALUES(?,?,?,?,?,?,?,?,?,?)", list(cadastro_fii.values()))
    for ano in config.ANOS_FII[-2:]:
        caminho = config.RAW / "cvm" / f"inf_trimestral_fii_{ano}.zip"
        if not caminho.exists():
            continue
        with zipfile.ZipFile(caminho) as z:
            membro = _membro(z.namelist(), "inf_trimestral_fii_imovel_")
            if not membro or membro.startswith("inf_trimestral_fii_imovel_renda"):
                membro = next((n for n in z.namelist() if re.match(r"inf_trimestral_fii_imovel_\d{4}", n)), membro)
            if not membro:
                continue
            fid = registrar_fonte(con, "CVM-FII-TRIMESTRAL", caminho, membro)
            with z.open(membro) as f:
                for r in ler_csv_cvm(f):
                    c = so_digitos(r.get("CNPJ_Fundo_Classe") or r.get("CNPJ_Fundo"))
                    if cnpjs is not None and c not in cnpjs:
                        continue
                    con.execute("INSERT INTO fii_imovel_trim VALUES(?,?,?,?,?,?,?,?,?,?)",
                                (c, r["Data_Referencia"], int(r.get("Versao") or 1), r.get("Nome_Imovel"),
                                 r.get("Classe"), num(r.get("Area")), num(r.get("Percentual_Vacancia")),
                                 num(r.get("Percentual_Inadimplencia")), num(r.get("Percentual_Receitas_FII")), fid))
    con.execute("""DELETE FROM fii_imovel_trim WHERE versao < (SELECT MAX(t.versao) FROM fii_imovel_trim t
                   WHERE t.cnpj=fii_imovel_trim.cnpj AND t.data_ref=fii_imovel_trim.data_ref)""")


# --------------------------------------------------------------------------- BCB

def normalizar_bcb(con) -> None:
    for p in sorted((config.RAW / "bcb").glob("sgs_*.json")):
        if p.name.endswith(".meta.json"):
            continue
        serie = int(p.stem.split("_")[1])
        fid = registrar_fonte(con, "BCB-SGS", p)
        dados = json.loads(p.read_text())
        con.executemany("INSERT OR REPLACE INTO macro VALUES(?,?,?,?)",
                        [(serie, f"{d['data'][6:]}-{d['data'][3:5]}-{d['data'][:2]}", float(d["valor"]), fid)
                         for d in dados])
