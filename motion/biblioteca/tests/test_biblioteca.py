"""Testes da biblioteca de animações (barras e rosca). Rodar de motion/: python3 -m pytest -q biblioteca/tests

Provam três coisas:
  1. a entrada errada é recusada antes de gerar (inclusive rosca que não soma 100% e ranking de ativos sem critério);
  2. o JSON de exemplo é igual ao dado de origem (SQLite do site-ativos, fact-check e quadro do Faz a Conta);
  3. no navegador (Chrome headless, mesma `seek` do render), os números NA TELA são iguais aos do JSON.
Os testes de navegador são pulados sem node_modules ou sem Chrome headless; os de dado, sem o cache/repos.
"""
import copy, html, json, os, re, sys

import pytest

BIB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTION = os.path.dirname(BIB)
for p in (os.path.join(MOTION, "comum"), BIB, os.path.join(BIB, "barras")):
    sys.path.insert(0, p)
import estilo  # noqa: E402
import teste  # noqa: E402
import dados  # noqa: E402
import importlib.util  # noqa: E402


def _modulo(nome, caminho):
    spec = importlib.util.spec_from_file_location(nome, caminho)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


barras = _modulo("barras_gerar", os.path.join(BIB, "barras", "gerar.py"))
rosca = _modulo("rosca_gerar", os.path.join(BIB, "rosca", "gerar.py"))
EXEMPLOS = os.path.join(MOTION, "exemplos")
EX_BARRAS = ["barras-dy-caixa-16x9.json", "barras-cotistas-9x16.json", "barras-megasena-fazaconta-9x16.json"]
EX_ROSCA = ["rosca-megasena-9x16.json", "rosca-megasena-fazaconta-16x9.json"]


def carregar(nome):
    return json.load(open(os.path.join(EXEMPLOS, nome)))


# ------------------------------------------------------------ comum: o estilo iec É a PAL do molde Burry
def _pal_do_molde():
    """Lê a PAL do edicao-skill/molde-burry/broll/gerar.py por conta própria (regex, sem o leitor do estilo.py)."""
    src = open(estilo.GERAR_MOLDE, encoding="utf-8").read()
    bloco = re.search(r"^PAL = dict\((.*?)\)\s*$", src, re.S | re.M).group(1)
    return dict(re.findall(r'(\w+)="(#[0-9a-fA-F]{6})"', bloco)), src


def test_estilo_iec_nao_diverge_da_pal_do_molde_burry():
    """FALHA se as cores da variante iec divergirem da PAL do gerar.py do molde Burry (a fonte de verdade)."""
    pal, src = _pal_do_molde()
    c = estilo.ESTILOS["iec"]["cores"]
    assert c == {"papel": pal["bg"], "tinta": pal["ink"], "cinza": pal["gray"], "grade": pal["faint"],
                 "destaque": pal["red"]}
    # as fontes também: só as famílias/pesos que o molde usa (Montserrat e Archivo Black)
    usadas = {(f, int(p)) for p, f in re.findall(r"font:\s*(\d{3})\s+\d+px\s+'?(Montserrat|Archivo Black)'?", src)}
    assert {(fam, peso) for _, fam, peso in estilo.ESTILOS["iec"]["fontes"].values()} == usadas
    assert ("Archivo Black", 400) in usadas and ("Montserrat", 800) in usadas


def test_pecas_sem_cor_fixa_no_codigo():
    for peca in ("barras", "rosca"):
        src = open(os.path.join(BIB, peca, "gerar.py"), encoding="utf-8").read()
        assert not re.findall(r"#[0-9a-fA-F]{6}\b", src), f"{peca}/gerar.py tem cor fixa"


def test_fmt_br_igual_ao_grafico_cotacao():
    g = _modulo("grafico_gerar", os.path.join(MOTION, "grafico_cotacao", "gerar.py"))
    for v, n in ((1234567.891, 2), (13.75, 2), (-0.004, 2), (-3.5, 1), (0, 0)):
        assert estilo.fmt_br(v, n) == g.fmt_br(v, n)


def test_estilo_fazaconta_igual_ao_build_hf():
    """As cores do Faz a Conta saem da PALETA do build_hf.py (lida como texto, sem importar)."""
    p = os.path.join(dados.FAZ_A_CONTA, "megasena", "build_hf.py")
    if not os.path.exists(p):
        pytest.skip("sem o repo faz-a-conta")
    src = open(p).read()
    pal = dict(re.findall(r'(\w+)="(#[0-9a-fA-F]{6})"', src.split("PALETA = dict(", 1)[1].split(")", 1)[0]))
    c = estilo.ESTILOS["fazaconta"]["cores"]
    assert (c["papel"], c["tinta"], c["destaque"], c["cinza"], c["grade"]) == \
           (pal["bg"], pal["ink"], pal["red"], pal["gray"], pal["faint"])
    assert "Archivo Black" in src and "Montserrat" in src


# ------------------------------------------------------------ barras: validação
BARRAS = {"titulo": "T", "fonte": "Fonte: X", "destaque": "A", "duracao": 6,
          "itens": [{"rotulo": "A", "valor": 3}, {"rotulo": "B", "valor": 5}, {"rotulo": "C", "valor": 1}]}


def test_barras_padroes():
    d = barras.validar(BARRAS)
    assert d["estilo"] == "iec" and d["ordem"] == "desc" and d["som"] == {"pouso": "impact-bass-1"}
    assert barras.ordem_final(d) == ["B", "A", "C"]


@pytest.mark.parametrize("mexer, trecho", [
    (lambda d: d.pop("fonte"), "'fonte' é obrigatório"),
    (lambda d: d.update(fonte="CVM"), "começar com 'Fonte:'"),
    (lambda d: d.update(estilo="neon"), "'estilo'"),
    (lambda d: d.update(formato="1:1"), "'formato'"),
    (lambda d: d.update(duracao=20), "'duracao'"),
    (lambda d: d.update(itens=d["itens"][:1]), "2 a 10"),
    (lambda d: d.update(itens=[{"rotulo": str(k), "valor": k} for k in range(11)]), "2 a 10"),
    (lambda d: d["itens"].append({"rotulo": "A", "valor": 1}), "repetido"),
    (lambda d: d["itens"].append({"rotulo": "D", "valor": -1}), "negativo"),
    (lambda d: d["itens"].append({"rotulo": "D", "valor": "1"}), "inválido"),
    (lambda d: d.update(destaque="Z"), "'destaque'"),
    (lambda d: d["itens"][0].update(antes=2), "todos precisam ter"),
    (lambda d: [i.update(antes=1) for i in d["itens"]], "'momentos' é obrigatório"),
    (lambda d: d.update(variacao="pct"), "precisa de dois momentos"),
    (lambda d: d["itens"].append({"rotulo": "PETR4", "valor": 1}), "parece ranking de ativos"),
    (lambda d: d.update(ativos=True), "exige 'criterio'"),
    (lambda d: d.update(som={"x": 1}), "'som'"),
])
def test_barras_entrada_invalida(mexer, trecho):
    d = copy.deepcopy(BARRAS)
    mexer(d)
    with pytest.raises(estilo.DadosInvalidos) as e:
        barras.validar(d)
    assert any(trecho in m for m in e.value.args[0]), e.value.args[0]


def test_barras_reordenacao_e_variacao():
    d = barras.validar({**BARRAS, "momentos": ["2025", "2026"], "destaque": "C",
                        "itens": [{"rotulo": "A", "antes": 9, "valor": 3}, {"rotulo": "B", "antes": 5, "valor": 5},
                                  {"rotulo": "C", "antes": 1, "valor": 8}]})
    pa, pd = barras.posicoes(d)
    assert pa == [0, 1, 2] and pd == [2, 1, 0]
    assert barras.texto_variacao(d) == "subiu do 3º para o 1º lugar"
    d["variacao"] = "pct"
    assert barras.texto_variacao(d) == "+700,0% desde 2025"
    d2 = barras.validar({**BARRAS, "ordem": "asc"})
    assert barras.ordem_final(d2) == ["C", "A", "B"]


# ------------------------------------------------------------ rosca: validação (soma 100%)
ROSCA = {"titulo": "T", "fonte": "Fonte: X", "destaque": "A", "casas": 2,
         "fatias": [{"rotulo": "A", "pct": 50.5}, {"rotulo": "B", "pct": 30.25}, {"rotulo": "C", "pct": 19.25}]}


def test_rosca_valida():
    d = rosca.validar(ROSCA)
    assert rosca.soma_pct(d["fatias"], 2) == 10000
    assert rosca.centro_final(d) == ("50,50%", "A")


@pytest.mark.parametrize("fatias, casas", [
    ([50, 30, 19], 0),                       # soma 99
    ([50.5, 30.25, 19.26], 2),               # soma 100,01
    ([33.33, 33.33, 33.33], 2),              # soma 99,99: o arredondamento não esconde
    ([33.3, 33.3, 33.4, 0.04], 1),           # bruto 100,04: na tela daria 100,0 mas o dado não fecha
    ([33.333, 33.333, 33.334], 1),           # o dado fecha, mas na tela somaria 99,9%
])
def test_rosca_que_nao_soma_100_da_erro(fatias, casas):
    d = {**ROSCA, "casas": casas, "fatias": [{"rotulo": str(k), "pct": p} for k, p in enumerate(fatias)], "destaque": "0"}
    with pytest.raises(estilo.DadosInvalidos) as e:
        rosca.validar(d)
    assert any("não 100%" in m for m in e.value.args[0]), e.value.args[0]


def test_rosca_fatia_que_some_no_arredondamento_da_erro():
    d = {**ROSCA, "casas": 0, "fatias": [{"rotulo": "A", "pct": 99.6}, {"rotulo": "B", "pct": 0.4}]}
    with pytest.raises(estilo.DadosInvalidos) as e:
        rosca.validar(d)
    assert any("apareceria como 0%" in m for m in e.value.args[0]), e.value.args[0]


def test_rosca_que_nao_soma_100_nao_gera_projeto(tmp_path):
    d = {**ROSCA, "fatias": ROSCA["fatias"][:2]}
    with pytest.raises(estilo.DadosInvalidos):
        rosca.gerar_projeto(d, str(tmp_path / "p"))
    assert not (tmp_path / "p" / "index.html").exists()


@pytest.mark.parametrize("mexer, trecho", [
    (lambda d: d["fatias"].append({"rotulo": "D", "pct": 0}), "maior que zero"),
    (lambda d: d.update(destaque="Z"), "'destaque'"),
    (lambda d: d.update(casas=3), "'casas'"),
    (lambda d: d.update(centro={"valor": -1}), "'centro'"),
    (lambda d: d["fatias"][0].update(rotulo="HGLG11"), "parece composição de ativos"),
    (lambda d: d.update(fonte="Lei 13.756"), "começar com 'Fonte:'"),
])
def test_rosca_entrada_invalida(mexer, trecho):
    d = copy.deepcopy(ROSCA)
    mexer(d)
    with pytest.raises(estilo.DadosInvalidos) as e:
        rosca.validar(d)
    assert any(trecho in m for m in e.value.args[0]), e.value.args[0]


@pytest.mark.parametrize("arquivo", EX_BARRAS + EX_ROSCA)
def test_exemplos_validos_e_sem_cdn(arquivo):
    d = carregar(arquivo)
    m = barras if d["peca"] == "barras" else rosca
    d = m.validar(d)
    assert d["fonte"].startswith("Fonte: ")
    html_ = m.montar_html(d)
    assert "cdn." not in html_ and "http" not in html_.split("<body>")[1]


# ------------------------------------------------------------ dado real: o JSON é igual à origem
precisa_site = pytest.mark.skipif(not os.path.exists(os.path.join(dados.SITE_ATIVOS, "cache", "dados.sqlite")),
                                  reason="sem cache do site-ativos")
precisa_fac = pytest.mark.skipif(not os.path.exists(os.path.join(dados.FAZ_A_CONTA, "pautas", "megasena-factcheck.md")),
                                 reason="sem o repo faz-a-conta")


@precisa_site
def test_dy_caixa_igual_ao_sqlite_e_a_pagina_do_site():
    d = carregar("barras-dy-caixa-16x9.json")
    origem = dados.dy_caixa()
    assert [(i["rotulo"], round(i["valor"], 6)) for i in d["itens"]] == [(t, round(v, 6)) for t, v, *_ in origem]
    pagina = os.path.join(dados.SITE_ATIVOS, "saida", "acoes", "ranking", "maiores-dy-de-caixa", "index.html")
    if not os.path.exists(pagina):
        pytest.skip("sem o build do site")
    texto = html.unescape(re.sub(r"<[^>]+>", " ", open(pagina).read()))
    na_pagina = re.findall(r"\b(\d+) ([A-Z]{4}\d{1,2}) .+? (\d+,\d)%", re.sub(r"\s+", " ", texto.split("Tabela", 1)[1]))
    un = d["unidade"]
    assert [(t, v + "%") for _, t, v in na_pagina] == [(i["rotulo"], estilo.texto_valor(i["valor"], un)) for i in d["itens"]]
    assert d["ativos"] and d["criterio"].startswith("Critério:")


@precisa_site
def test_cotistas_igual_ao_informe_da_cvm_no_sqlite():
    d = carregar("barras-cotistas-9x16.json")
    a, b = dados.cotistas("2025-08-01"), dados.cotistas("2026-08-01")
    for it in d["itens"]:
        assert it["antes"] == a[it["rotulo"]][0] and it["valor"] == b[it["rotulo"]][0]
    assert d["momentos"] == ["ago/2025", "ago/2026"]
    # o "depois" é o mesmo número que o site publica (indicador cotistas, informe de 08/2026)
    import sqlite3
    con = sqlite3.connect(os.path.join(dados.SITE_ATIVOS, "cache", "dados.sqlite"))
    site = dict(con.execute("select ticker, valor from indicador where nome='cotistas' and periodo_contabil='2026-08-01'"))
    assert all(site[it["rotulo"]] == it["valor"] for it in d["itens"])


@precisa_fac
@pytest.mark.parametrize("arquivo", ["rosca-megasena-9x16.json", "rosca-megasena-fazaconta-16x9.json",
                                     "barras-megasena-fazaconta-9x16.json"])
def test_megasena_igual_ao_factcheck_e_ao_quadro_conferido(arquivo):
    d = carregar(arquivo)
    fatias, aposta, premio_reais, _ = dados.megasena()
    pares = [(f["rotulo"], f["pct"]) for f in d["fatias"]] if d["peca"] == "rosca" else \
            [(i["rotulo"], i["valor"]) for i in d["itens"]]
    assert pares == fatias
    fc = open(os.path.join(dados.FAZ_A_CONTA, "pautas", "megasena-factcheck.md")).read()
    for nome, v in (("seguridade", "17,32"), ("FNSP", "6,8"), ("esporte", "4,36"), ("COB", "1,73"), ("CPB", "0,96"),
                    ("FNC", "2,91"), ("Funpen", "3"), ("custeio Caixa", "19,13")):
        assert f"{nome} {v}%" in fc
    rot = open(os.path.join(dados.FAZ_A_CONTA, "megasena", "roteiro.md")).read()
    assert "| premio-bruto | 43,79% = R$ 2,63 |" in rot and "| aposta | R$ 6,00 |" in rot
    assert aposta == 6.0 and premio_reais == 2.63
    if d["peca"] == "rosca":
        assert rosca.centro_final(rosca.validar(d))[0] == "R$ 2,63"   # 6 × 43,79% = 2,6274 → igual ao quadro


@pytest.mark.parametrize("arquivo", EX_ROSCA)
def test_rosca_dos_exemplos_soma_100(arquivo):
    d = rosca.validar(carregar(arquivo))
    assert rosca.soma_pct(d["fatias"], d["casas"]) == 100 * 10 ** d["casas"]


# ------------------------------------------------------------ navegador: a tela é igual ao dado
FONTES_ESPERADAS = {e: {f"{fam} {peso}" for _, fam, peso in v["fontes"].values()} for e, v in estilo.ESTILOS.items()}


def _rgb(hexa):
    return "rgb(" + ", ".join(str(int(hexa[i:i + 2], 16)) for i in (1, 3, 5)) + ")"


@teste.precisa_navegador
@pytest.mark.parametrize("arquivo", EX_BARRAS)
def test_barras_na_tela_iguais_ao_dado(arquivo, tmp_path):
    d = barras.validar(carregar(arquivo))
    projeto = str(tmp_path / "p")
    barras.gerar_projeto(d, projeto)
    T = barras.tempos(d)
    instantes = [T["t2"] - .15, d["duracao"]] if d["momentos"] else [d["duracao"]]
    r = teste.quadros(projeto, instantes, str(tmp_path / "q"))
    assert r["erros"] == [], r["erros"]
    assert FONTES_ESPERADAS[d["estilo"]] <= set(r["fontes"])
    fim = r["quadros"][-1]
    assert abs(fim["duracao"] - d["duracao"]) < 1e-6
    tela, un = fim["tela"], d["unidade"]
    por_rotulo = {i["rotulo"]: i for i in d["itens"]}
    # ordem de cima para baixo e cada valor igual ao do dado
    assert [b["rotulo"] for b in tela["barras"]] == barras.ordem_final(d)
    for b in tela["barras"]:
        assert b["valor"] == estilo.texto_valor(por_rotulo[b["rotulo"]]["valor"], un)
        assert b["visivel"]
    # largura proporcional ao valor (mesma escala para todas)
    vmax = max(max(i["valor"], i.get("antes", 0)) for i in d["itens"])
    for b in tela["barras"]:
        assert abs(b["largura"] - por_rotulo[b["rotulo"]]["valor"] / vmax * tela["bw"]) < 0.6
    # barra-chave na cor de destaque; número grande = valor dela
    chave = next(b for b in tela["barras"] if b["rotulo"] == d["destaque"])
    destaque = estilo.ESTILOS[d["estilo"]]["cores"]["destaque"]
    assert chave["cor"] == _rgb(destaque) and tela["cor_numero"] == _rgb(destaque)
    assert tela["numero"] == estilo.texto_valor(por_rotulo[d["destaque"]]["valor"], un)
    assert tela["fonte"] == d["fonte"]
    assert tela["variacao"] == barras.texto_variacao(d)
    # compliance: ranking de ativos com critério e aviso na tela
    if d["ativos"]:
        assert tela["criterio"] == d["criterio"] and tela["aviso"] == estilo.AVISO_ATIVOS
    else:
        assert tela["aviso"] == ""
    if d["momentos"]:
        # antes da troca: os valores e a ordem do 1º momento
        meio = r["quadros"][0]["tela"]
        assert meio["momento"] == d["momentos"][0] and fim["tela"]["momento"] == d["momentos"][1]
        esperado = [d["itens"][k]["rotulo"] for k in barras.ranking([i["antes"] for i in d["itens"]], d["ordem"])]
        assert [b["rotulo"] for b in meio["barras"]] == esperado
        for b in meio["barras"]:
            assert b["valor"] == estilo.texto_valor(por_rotulo[b["rotulo"]]["antes"], un)
        assert esperado != barras.ordem_final(d), "o exemplo de dois momentos deve trocar a ordem"
    assert os.path.getsize(str(tmp_path / f"q-{fim['t']}.png")) > 20_000


@teste.precisa_navegador
@pytest.mark.parametrize("arquivo", EX_ROSCA)
def test_rosca_na_tela_igual_ao_dado(arquivo, tmp_path):
    d = rosca.validar(carregar(arquivo))
    projeto = str(tmp_path / "p")
    rosca.gerar_projeto(d, projeto)
    T = rosca.tempos(d)
    meio = T["t0"] + 2.5 * T["s"]            # 2 fatias prontas, a 3ª no meio, o resto por fazer
    r = teste.quadros(projeto, [meio, d["duracao"]], str(tmp_path / "q"))
    assert r["erros"] == [], r["erros"]
    assert FONTES_ESPERADAS[d["estilo"]] <= set(r["fontes"])
    tela = r["quadros"][-1]["tela"]
    casas = d["casas"]
    assert [f["rotulo"] for f in tela["fatias"]] == [f["rotulo"] for f in d["fatias"]]
    for na_tela, f in zip(tela["fatias"], d["fatias"]):
        assert na_tela["pct"] == rosca.texto_pct(f["pct"], casas)
        assert abs(na_tela["arco"] - (f["pct"] - rosca.FOLGA)) < 1e-3     # o arco mede o percentual
        assert na_tela["legenda_visivel"]
    # o que a tela mostra soma 100%
    soma = sum(round(float(f["pct"].rstrip("%").replace(".", "").replace(",", ".")) * 10 ** casas) for f in tela["fatias"])
    assert soma == 100 * 10 ** casas
    assert tela["soma"] == "soma: " + rosca.texto_pct(100, casas)
    k = [f["rotulo"] for f in d["fatias"]].index(d["destaque"])
    destaque = _rgb(estilo.ESTILOS[d["estilo"]]["cores"]["destaque"])
    assert tela["fatias"][k]["cor"] == destaque and tela["cor_centro"] == destaque
    cfin, rfin = rosca.centro_final(d)
    assert tela["centro"] == cfin and tela["centro_rotulo"] == rfin
    assert tela["fonte"] == d["fonte"]
    # uma por vez: no meio, 2 fatias completas, a 3ª parcial e as outras zeradas
    m = r["quadros"][0]["tela"]["fatias"]
    assert abs(m[0]["arco"] - (d["fatias"][0]["pct"] - rosca.FOLGA)) < 1e-3
    assert abs(m[1]["arco"] - (d["fatias"][1]["pct"] - rosca.FOLGA)) < 1e-3
    assert 0 < m[2]["arco"] < d["fatias"][2]["pct"] - rosca.FOLGA
    assert all(x["arco"] == 0 for x in m[3:]) and not any(x["legenda_visivel"] for x in m[4:])
    assert r["quadros"][0]["tela"]["centro"] == rosca.texto_valor(d["centro"]["valor"], d["centro"]["unidade"])
