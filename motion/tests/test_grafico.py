"""Testes do gráfico de cotação: dados validados, frame renderiza sem erro e o número final na tela
bate com o último valor da série. Rodar de motion/: python3 -m pytest -q tests

Os testes de navegador precisam de `npm install` e de um Chrome headless
(PRODUCER_HEADLESS_SHELL_PATH ou `npx hyperframes browser ensure`); sem isso, são pulados.
"""
import copy, json, os, shutil, subprocess, sys

import pytest

MOTION = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(MOTION, "grafico_cotacao"))
import gerar  # noqa: E402
import serie  # noqa: E402

EXEMPLOS = os.path.join(MOTION, "exemplos")


def carregar(nome):
    return json.load(open(os.path.join(EXEMPLOS, nome)))


BASE = {
    "titulo": "Teste", "fonte": "Fonte: BCB", "formato": "16:9", "duracao": 6,
    "unidade": {"prefixo": "", "sufixo": "%", "casas": 2}, "variacao": "pp",
    "serie": [{"data": "2024-01-01", "valor": 10.0}, {"data": "2024-06-01", "valor": 11.5},
              {"data": "2024-12-31", "valor": 12.25}],
}


# ------------------------------------------------------------ validação
def test_entrada_valida_recebe_padroes():
    d = gerar.validar(BASE)
    assert d["linha"] == "linha" and d["cor_final"] == "vermelho" and d["som"] is False


@pytest.mark.parametrize("mexer, trecho", [
    (lambda d: d.pop("fonte"), "'fonte' é obrigatório"),
    (lambda d: d.update(fonte="BCB"), "começar com 'Fonte:'"),
    (lambda d: d.update(formato="4:3"), "'formato'"),
    (lambda d: d.update(duracao=30), "'duracao'"),
    (lambda d: d.update(serie=d["serie"][:1]), "pelo menos 2 pontos"),
    (lambda d: d["serie"].reverse(), "fora de ordem"),
    (lambda d: d["serie"].append({"data": "2025-01-01", "valor": "12"}), "serie[3] inválido"),
    (lambda d: d["serie"].append({"data": "2025-13-01", "valor": 1}), "serie[3] inválido"),
    (lambda d: d["serie"].append({"data": "2025-02-01", "valor": float("nan")}), "serie[3] inválido"),
    (lambda d: d.update(cor_final="azul"), "'cor_final'"),
    (lambda d: d.update(destaques=[{"data": "2030-01-01", "rotulo": "x"}]), "fora do período"),
    (lambda d: d.update(destaques=[{"data": "2024-06-01", "rotulo": "x"}] * 4), "no máximo 3"),
    (lambda d: d.update(som={"outro": 1}), "'som'"),
])
def test_entrada_invalida_explica_o_erro(mexer, trecho):
    d = copy.deepcopy(BASE)
    mexer(d)
    with pytest.raises(gerar.DadosInvalidos) as e:
        gerar.validar(d)
    assert any(trecho in m for m in e.value.args[0]), e.value.args[0]


@pytest.mark.parametrize("arquivo", ["selic-16x9.json", "petr4-9x16.json"])
def test_exemplos_do_repo_sao_validos(arquivo):
    d = gerar.validar(carregar(arquivo))
    assert d["fonte"].startswith("Fonte: ")


# ------------------------------------------------------------ contas
def test_formato_brasileiro():
    assert gerar.fmt_br(1234567.891, 2) == "1.234.567,89"
    assert gerar.fmt_br(13.75, 2) == "13,75"
    assert gerar.fmt_br(-0.004, 2) == "0,00"
    assert gerar.fmt_br(-3.5, 1) == "-3,5"
    assert gerar.texto_valor(49.77, {"prefixo": "R$ ", "sufixo": "", "casas": 2}) == "R$ 49,77"


def test_variacao():
    assert gerar.texto_variacao(gerar.validar(BASE)) == "+2,25 p.p. desde jan/2024"
    d = gerar.validar({**BASE, "variacao": "pct"})
    assert gerar.texto_variacao(d) == "+22,5% desde jan/2024"


def test_reducao_guarda_extremos_e_ultimo():
    pts = [{"data": f"2020-01-01", "valor": 0}]
    import datetime as dt
    pts = [{"data": (dt.date(2020, 1, 1) + dt.timedelta(days=k)).isoformat(), "valor": (k * 37) % 101}
           for k in range(3000)]
    pts[1234]["valor"] = 999
    pts[2222]["valor"] = -50
    r = gerar.reduzir(pts)
    assert len(r) <= gerar.MAX_PONTOS
    assert r[0] == pts[0] and r[-1] == pts[-1]
    assert max(p["valor"] for p in r) == 999 and min(p["valor"] for p in r) == -50
    assert [p["data"] for p in r] == sorted(p["data"] for p in r)


def test_escala_cobre_a_serie():
    lo, hi, marcas = gerar.escala_y(2.0, 15.0)
    assert lo <= 2.0 and hi >= 15.0 and len(marcas) >= 3


def test_inverso_da_ease_power1_inout():
    for t in (0.1, 0.3, 0.5, 0.7, 0.95):
        p = 2 * t * t if t < .5 else 1 - (-2 * t + 2) ** 2 / 2
        assert abs(gerar.tempo_da_ease(p) - t) < 1e-9


def test_html_traz_o_numero_final_e_a_fonte():
    html = gerar.montar_html(carregar("selic-16x9.json"))
    assert "Fonte: BCB (SGS 432)" in html
    assert 'window.__timelines["grafico"]' in html
    assert "cdn." not in html  # nada de CDN na hora do render


# ------------------------------------------------------------ dado real (cache do site-ativos)
@pytest.mark.skipif(not serie._sqlite(), reason="sem cache do site-ativos")
def test_serie_bcb_vem_do_cache_e_termina_no_ultimo_dado():
    import sqlite3
    pontos, origem = serie.serie_bcb(432, "2020-01-01")
    con = sqlite3.connect(serie._sqlite())
    ultimo = con.execute("select data, valor from macro where serie=432 order by data desc limit 1").fetchone()
    assert pontos[-1] == (ultimo[0], ultimo[1])
    assert serie.so_mudancas(pontos)[-1] == pontos[-1]


@pytest.mark.skipif(not serie._sqlite(), reason="sem cache do site-ativos")
def test_b3_sqlite_e_cotahist_cru_concordam():
    pontos, _ = serie.serie_b3("PETR4", "2026-09-01")
    crus = serie._cotahist("PETR4", "2026-09-01", None)
    if not crus:
        pytest.skip("sem COTAHIST cru")
    assert [round(v, 2) for _, v in pontos] == [round(v, 2) for _, v in crus]


def test_salto_de_desdobramento_e_detectado():
    assert serie.saltos([("2024-01-01", 40.0), ("2024-01-02", 41.0), ("2024-01-03", 4.1)]) == [("2024-01-03", 41.0, 4.1)]


# ------------------------------------------------------------ navegador
def _chrome():
    if os.environ.get("PRODUCER_HEADLESS_SHELL_PATH"):
        return True
    bin_ = os.path.join(MOTION, "node_modules", ".bin", "hyperframes")
    if not os.path.exists(bin_):
        return False
    r = subprocess.run([bin_, "browser", "path"], capture_output=True, text=True)
    return r.returncode == 0 and os.path.exists(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "")


precisa_navegador = pytest.mark.skipif(
    not (shutil.which("node") and os.path.isdir(os.path.join(MOTION, "node_modules", "puppeteer-core")) and _chrome()),
    reason="sem node_modules (npm install) ou sem Chrome headless")


def quadro(projeto, t, png=None):
    cmd = ["node", os.path.join(MOTION, "grafico_cotacao", "quadro.mjs"), projeto, str(t)] + ([png] if png else [])
    out = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=120).stdout
    return json.loads(out.strip().splitlines()[-1])


@precisa_navegador
@pytest.mark.parametrize("arquivo", ["selic-16x9.json", "petr4-9x16.json"])
def test_frame_renderiza_e_numero_final_bate_com_a_serie(arquivo, tmp_path):
    d = carregar(arquivo)
    projeto = str(tmp_path / "proj")
    gerar.gerar_projeto(d, projeto)
    png = str(tmp_path / "final.png")
    r = quadro(projeto, d["duracao"], png)
    assert r["erros"] == [], r["erros"]
    assert abs(r["duracao"] - d["duracao"]) < 1e-6
    esperado = gerar.texto_valor(d["serie"][-1]["valor"], gerar.validar(d)["unidade"])
    assert r["numero"] == esperado
    assert r["fonte"] == d["fonte"]
    assert {"Anton 400", "Inter 900", "JetBrains Mono 500"} <= set(r["fontes"])
    assert os.path.getsize(png) > 20_000


@precisa_navegador
def test_numero_no_meio_e_um_valor_real_da_serie(tmp_path):
    d = carregar("selic-16x9.json")  # degrau: o número no meio tem que ser exatamente um valor da série
    projeto = str(tmp_path / "proj")
    gerar.gerar_projeto(d, projeto)
    r = quadro(projeto, 3.0)
    validos = {gerar.texto_valor(p["valor"], d["unidade"]) for p in d["serie"]}
    assert r["numero"] in validos and r["numero"] != gerar.texto_valor(d["serie"][-1]["valor"], d["unidade"])
