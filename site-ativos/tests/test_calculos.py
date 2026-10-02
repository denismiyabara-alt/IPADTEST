"""Cálculos conferidos contra números publicados nas próprias demonstrações (fixtures reais).

Tolerâncias (as mesmas do DESENHO 8.2): R$ 1 mil para somas contábeis, 3% para LPA, 0,5% para o
valor patrimonial da cota de FII, 0,1% para lucro = controladora + não controladores.
"""
import json
from pathlib import Path

import pytest

from iec_ativos import calcular, normalizar
from iec_ativos.contas import Demonstracoes
from iec_ativos import validar
from iec_ativos.validar import TOL_LPA, TOL_TTM, TOL_VP_FII

PETR, ITUB, BPAC, VALE, AXIA = "33000167000101", "60872504000123", "30306294000145", "33592510000154", "00001180000126"
HGLG = "11728688000147"


def test_escala_mil_e_lpa_sem_escala(ambiente):
    con = ambiente["con"]
    # Receita da Petrobras na DFP 2025: 497.549.000 (em MIL) -> R$ 497.549.000.000
    v = con.execute("""SELECT valor_reais, escala_original FROM conta WHERE cnpj=? AND doc='DFP' AND dt_refer='2025-12-31'
                       AND cd_conta='3.01' AND ordem_exerc='ULTIMO'""", (PETR,)).fetchone()
    assert v[1] == "MIL" and v[0] == 497_549_000_000
    # LPA também vem marcado MIL no arquivo, mas é em reais por ação: 8,54 continua 8,54
    lpa = con.execute("""SELECT valor_reais, escala_original FROM conta WHERE cnpj=? AND doc='DFP' AND dt_refer='2025-12-31'
                         AND cd_conta='3.99.01.01' AND ordem_exerc='ULTIMO'""", (PETR,)).fetchone()
    assert tuple(lpa) == (8.54, "MIL")


def test_fator_escala():
    assert normalizar.fator_escala("MIL", "3.01") == 1000
    assert normalizar.fator_escala("UNIDADE", "3.01") == 1
    assert normalizar.fator_escala("MIL", "3.99.01.01") == 1


def test_maior_versao(ambiente):
    """O ITR 1T26 da Petrobras tem versões 1 e 2 no arquivo; só a 2 pode ficar."""
    con = ambiente["con"]
    vs = {r[0] for r in con.execute("SELECT DISTINCT versao FROM conta WHERE cnpj=? AND doc='ITR' AND dt_refer='2026-03-31'", (PETR,))}
    assert vs == {2}
    doc = con.execute("SELECT versao FROM documento WHERE cnpj=? AND doc='ITR' AND dt_refer='2026-03-31'", (PETR,)).fetchall()
    assert [r[0] for r in doc] == [2]


def test_ttm_bate_com_soma_das_dres(ambiente):
    """Lucro TTM até 30/06/2026 = DFP 2025 + 6M26 − 6M25 = soma dos 4 trimestres (3T25, 4T25, 1T26, 2T26)."""
    d = Demonstracoes(ambiente["con"], PETR)
    ttm = d.ttm("2026-06-30", "DRE", "lucro_controladora")["valor"]
    dfp25, acc26, acc25 = 110_129_000_000, 85_108_000_000, 61_861_000_000   # números das próprias DREs
    assert abs(ttm - (dfp25 + acc26 - acc25)) <= TOL_TTM
    tris = [d.trimestre(r, "DRE", "lucro_controladora") for r in ("2025-09-30", "2025-12-31", "2026-03-31", "2026-06-30")]
    assert tris == [32_705_000_000, 15_563_000_000, 32_663_000_000, 52_445_000_000]
    assert abs(sum(tris) - ttm) <= TOL_TTM


def test_lpa_calculado_bate_com_divulgado(ambiente):
    """Petrobras, DFP 2025: lucro da controladora ÷ ações sem tesouraria ≈ LPA básico divulgado (8,54)."""
    con = ambiente["con"]
    cap = con.execute("SELECT qt_on, qt_pn, qt_on_tesouraria, qt_pn_tesouraria FROM capital WHERE cnpj=? AND doc='DFP' AND dt_refer='2025-12-31'",
                      (PETR,)).fetchone()
    acoes = cap[0] + cap[1] - (cap[2] or 0) - (cap[3] or 0)
    lpa = 110_129_000_000 / acoes
    assert abs(lpa / 8.54 - 1) <= TOL_LPA, f"LPA calculado {lpa:.4f}"


def test_lpa_pela_descricao_e_acoes_em_milhares(ambiente):
    """Vale: 3.99.01.01 é 'PNA' (zerado) e 3.99.01.02 é 'ON' = 3,24. A composição do capital vem em milhares."""
    f = calcular.ficha_acao(ambiente["con"], "VALE3", "comum", VALE)
    assert f["lpa_divulgado"]["lpa_on"] == 3.24
    assert f["acoes"]["escala"] == 1000
    rel = {t["nome"].split(" (")[0]: t for t in validar.testes_acao(ambiente["con"], f)}
    assert rel["LPA calculado × LPA básico divulgado"]["ok"], rel["LPA calculado × LPA básico divulgado"]["detalhe"]


def test_on_pn_valor_de_mercado(ambiente):
    """Petrobras: ON e PN negociadas, cada classe com o seu preço."""
    f = calcular.ficha_acao(ambiente["con"], "PETR4", "comum", PETR)
    partes = {p["classe"]: p for p in f["valor_mercado_partes"]}
    assert partes["ON"]["origem"] == "PETR3" and partes["PN"]["origem"] == "PETR4"
    vm = sum(p["acoes"] * p["preco"] for p in partes.values())
    assert abs(f["ind"]["valor_mercado"]["valor"] - vm) < 1


def test_unit_preco_implicito(ambiente):
    """BTG: ON e PN avulsas sem liquidez; preço de cada ação = BPAC11 ÷ 3 (1 ON + 2 PNA)."""
    f = calcular.ficha_acao(ambiente["con"], "BPAC11", "banco", BPAC)
    assert f["composicao_unit"] == {"ON": 1, "PN": 2}
    preco_unit = f["ind"]["preco"]["valor"]
    for p in f["valor_mercado_partes"]:
        assert abs(p["preco"] - preco_unit / 3) < 1e-9
    assert "estimado" in f["ind"]["valor_mercado"]["nota"]
    # LPA da unit = LPA por ação × 3
    assert abs(f["ind"]["lpa"]["valor"] - f["ttm"]["lucro_controladora"] / f["acoes"]["total"] * 3) < 1e-9


def test_banco_sem_ebitda(ambiente):
    f = calcular.ficha_acao(ambiente["con"], "ITUB4", "banco", ITUB)
    for k in ("ebitda", "margem_ebitda", "div_liq_ebitda", "margem_liquida"):
        assert f["ind"][k]["status"] == "nao_se_aplica", k
    assert f["ind"]["pl"]["status"] == "ok" and f["ind"]["pvp"]["status"] == "ok" and f["ind"]["roe"]["status"] == "ok"
    d = Demonstracoes(ambiente["con"], ITUB)
    assert d.achar("ITR", "2026-06-30", "DRE", "ebit") is None      # banco não tem a conta 3.05 de EBIT
    assert d.achar("ITR", "2026-06-30", "BPP", "pl_total") == "2.08"  # PL do banco é 2.08, não 2.03


def test_controladora_preenchida_com_zero(ambiente):
    """Axia, ITR 3T25: 'Atribuído a Sócios da Empresa Controladora' = 0 e não controladores = 0 -> vale o total."""
    d = Demonstracoes(ambiente["con"], AXIA)
    assert d.trimestre("2025-09-30", "DRE", "lucro_controladora") == -5_448_117_000


def test_balanco_e_ttm_passam_nos_bloqueantes(ambiente):
    for tk, tipo, c in (("PETR4", "comum", PETR), ("ITUB4", "banco", ITUB), ("BPAC11", "banco", BPAC)):
        f = calcular.ficha_acao(ambiente["con"], tk, tipo, c)
        falhas = [t for t in validar.testes_acao(ambiente["con"], f) if t["tipo"] == "bloqueante" and not t["ok"]]
        assert not falhas, falhas


def test_reapresentacao_explicada(ambiente):
    """BTG reapresentou o 1T26 no ITR 2T26: a soma dos trimestres originais difere do TTM em R$ 26,9 milhões,
    e o teste explica a diferença em vez de bloquear."""
    f = calcular.ficha_acao(ambiente["con"], "BPAC11", "banco", BPAC)
    t = next(x for x in validar.testes_acao(ambiente["con"], f) if x["nome"].startswith("TTM até"))
    assert t["ok"] and "reapresentação" in t["detalhe"]


def test_fii_pvp_bate_com_informe(ambiente):
    """HGLG11: patrimônio ÷ cotas ≈ valor patrimonial da cota informado; P/VP = fechamento ÷ esse valor."""
    f = calcular.ficha_fii(ambiente["con"], "HGLG11", HGLG)
    inf = f["informe"]
    assert abs(inf["pl"] / inf["cotas_emitidas"] / inf["vp_cota"] - 1) <= TOL_VP_FII
    assert abs(f["ind"]["pvp"]["valor"] - f["ind"]["preco"]["valor"] / inf["vp_cota"]) < 1e-12
    assert all(t["ok"] for t in validar.testes_fii(ambiente["con"], f) if t["teste"] == 10)


def test_fii_informe_inconsistente_nao_vira_dy(ambiente):
    """XPML11 tem DY negativo e meses copiados no informe: o DY estimado fica 'não disponível'."""
    f = calcular.ficha_fii(ambiente["con"], "XPML11", "28757546000100")
    assert f["ind"]["dy_estimado"]["status"] == "sem_dado"
    assert any("negativo" in p for p in f["informe_problemas"])


def test_receita_zero_nao_se_aplica(tmp_path):
    """Empresa sintética com receita 0: margem líquida e margem EBITDA 'não se aplica'."""
    from iec_ativos import config
    con = normalizar.conectar(tmp_path / "s.sqlite")
    c = "11111111000111"
    con.execute("INSERT INTO empresa VALUES(?,?,?,?,?,?,?,?,?)", (c, "1", "TESTE SA", "TESTE", "Outros", "comum", "ATIVO", 0, ""))
    con.execute("INSERT INTO ativo(ticker,cnpj_emissor,classe,ativo) VALUES('TEST3',?,'ON',1)", (c,))
    hoje = config.HOJE.isoformat()
    con.execute("INSERT INTO preco_diario(ticker,data,fechamento,volume_rs,codbdi) VALUES('TEST3',?,10,5e6,'02')", (hoje,))
    con.execute("INSERT INTO capital VALUES(?,?,?,?,?,?,?,?,?,?)", (c, "DFP", "2025-12-31", 1, 1e6, 0, 1e6, 0, 0, 0))
    linhas = [("DRE", "3.01", "Receita de Venda de Bens e/ou Serviços", 0.0), ("DRE", "3.05", "Resultado Antes do Resultado Financeiro e dos Tributos", -5e5),
              ("DRE", "3.11", "Lucro/Prejuízo Consolidado do Período", -1e6), ("DRE", "3.11.01", "Atribuído a Sócios da Empresa Controladora", -1e6),
              ("BPA", "1", "Ativo Total", 5e6), ("BPP", "2", "Passivo Total", 5e6), ("BPP", "2.03", "Patrimônio Líquido Consolidado", 2e6),
              ("DVA", "7.04.01", "Depreciação, Amortização e Exaustão", -1e5)]
    for dem, cd, ds, v in linhas:
        con.execute("""INSERT INTO conta(cnpj,doc,demonstracao,escopo,dt_refer,dt_ini_exerc,dt_fim_exerc,ordem_exerc,versao,
                       cd_conta,ds_conta,conta_fixa,valor_reais,escala_original,fonte_arquivo_id)
                       VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                    (c, "DFP", dem, "con", "2025-12-31", None if dem.startswith("BP") else "2025-01-01", "2025-12-31",
                     "ULTIMO", 1, cd, ds, "S", v, "MIL", 0))
    f = calcular.ficha_acao(con, "TEST3", "comum", c)
    assert f["ind"]["margem_liquida"]["status"] == "nao_se_aplica"
    assert f["ind"]["margem_ebitda"]["status"] == "nao_se_aplica"
    assert f["ind"]["pl"]["status"] == "nao_se_aplica"            # prejuízo em 12 meses
    assert f["ind"]["div_liq_ebitda"]["status"] in ("nao_se_aplica", "sem_dado")


def test_cotahist_layout():
    """Linha real do COTAHIST (posições fixas de 245 bytes; preços com 2 decimais implícitos)."""
    import gzip
    from conftest import FIX
    linhas = gzip.decompress((FIX / "b3" / "COTAHIST_recorte.txt.gz").read_bytes()).decode("latin-1").splitlines()
    ln = next(x for x in linhas if x[12:24].strip() == "PETR4" and x[2:10] == "20261001")
    assert len(ln) == 245
    r = normalizar.ler_linha_cotahist(ln)
    assert r["ticker"] == "PETR4" and r["data"] == "2026-10-01" and r["codbdi"] == "02" and r["tpmerc"] == "010"
    assert r["fechamento"] == int(ln[108:121]) / 100 and r["isin"].startswith("BRPETR")
    assert r["fatcot"] == 1


def test_composicao_unit_texto_do_fca():
    p = normalizar.parse_composicao_unit
    assert p("1 ON E 2 PNA") == {"ON": 1, "PN": 2}
    assert p("1 KLBN3 + 4 KLBN4") == {"ON": 1, "PN": 4}
    assert p("1 ação ordinária e 4 ações preferenciais") == {"ON": 1, "PN": 4}
    assert p("2 ações preferenciais e 1 ação ordinária") == {"ON": 1, "PN": 2}
    assert p("1 PN + 3 Recibos de Subscrição") is None
