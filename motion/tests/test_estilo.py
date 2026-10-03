"""O estilo do gráfico vem da PAL do molde Burry (broll/gerar.py), e de nenhum outro lugar.
Estes testes FALHAM se uma cor do gráfico sair da PAL, se a PAL deixar de ser lida do gerar.py,
ou se a ressalva "Preço sem dividendos." sumir da tela num gráfico de ação."""
import json, os, re, subprocess, sys

import pytest

MOTION = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(MOTION, "comum"))
sys.path.insert(0, os.path.join(MOTION, "grafico_cotacao"))
import estilo  # noqa: E402  (motion/comum/estilo.py, o módulo comum com a biblioteca)
import gerar  # noqa: E402
from test_grafico import carregar, precisa_navegador, quadro  # noqa: E402


def rgb(hexa):
    h = hexa.lstrip("#")
    return f"rgb({int(h[0:2], 16)}, {int(h[2:4], 16)}, {int(h[4:6], 16)})"


def test_pal_do_grafico_e_a_do_molde_burry():
    pal, fontes = estilo.ler_molde()
    src = open(estilo.GERAR_MOLDE, encoding="utf-8").read()
    assert "PAL = dict(" in src
    for k, v in pal.items():
        assert re.search(rf"\b{k}\s*=\s*\"{re.escape(v)}\"", src), (k, v)
    assert gerar.CORES == {p: pal[k] for p, k in gerar.PAPEIS.items()}
    assert {"Montserrat", "Archivo Black"} <= {f for f, _ in fontes}
    assert (gerar.TEXTO, gerar.NUMERO) == ("Montserrat", "Archivo Black")


def test_pal_muda_junto_quando_o_gerar_py_muda(tmp_path):
    falso = tmp_path / "gerar.py"
    falso.write_text('PAL = dict(bg="#000001", ink="#000002", red="#000003", gray="#000004", faint="#000005", '
                     'verde="#000006", cobre="#000007", paper="#000008")\n'
                     'CSS = "font:800 30px Montserrat, sans-serif; font:400 90px \'Archivo Black\', sans-serif;"\n')
    r = subprocess.run([sys.executable, "-c", "import gerar; print(gerar.CORES['papel'], gerar.CORES['vermelho'])"],
                       cwd=os.path.join(MOTION, "grafico_cotacao"),
                       env={**os.environ, "IEC_MOLDE_BURRY_GERAR": str(falso)}, capture_output=True, text=True)
    assert r.stdout.split() == ["#000001", "#000003"], r.stderr


@pytest.mark.parametrize("arquivo", ["selic-16x9.json", "petr4-9x16.json", "petr4-cdi-16x9.json"])
def test_toda_cor_do_grafico_esta_na_pal(arquivo):
    html = gerar.montar_html(carregar(arquivo)).lower()
    usadas = set(re.findall(r"#[0-9a-f]{6}\b", html))
    fora = usadas - {v.lower() for v in estilo.ler_molde()[0].values()}
    assert not fora, f"cores fora da PAL do molde Burry: {sorted(fora)}"
    assert not re.search(r"rgba?\(", html.split("<script")[0]), "cor em rgb() escapa da PAL"
    assert "'Archivo Black'" in gerar.montar_html(carregar(arquivo))


def test_ressalva_so_em_ativo():
    assert gerar.RESSALVA_PRECO in gerar.montar_html(carregar("petr4-cdi-16x9.json"))
    assert gerar.RESSALVA_PRECO not in gerar.montar_html(carregar("selic-16x9.json"))


@precisa_navegador
def test_na_tela_as_cores_sao_da_pal_e_a_ressalva_aparece(tmp_path):
    d = carregar("petr4-cdi-16x9.json")
    projeto = str(tmp_path / "proj")
    gerar.gerar_projeto(d, projeto)
    r = quadro(projeto, d["duracao"])
    P = estilo.ler_molde()[0]
    assert r["cores"]["fundo"] == rgb(P["bg"])
    assert r["cores"]["numero"] == rgb(P["red"])          # cor_final vermelho, depois do pouso
    assert r["cores"]["linha"] == rgb(P["ink"])
    assert r["cores"]["comp"] == rgb(P["gray"])
    assert gerar.NUMERO in r["familias"]["numero"] and gerar.TEXTO in r["familias"]["titulo"]
    assert r["ressalva"] == "Preço sem dividendos." and r["ressalvaVisivel"]
