"""Testes do lote 2 da biblioteca: eventos, barra_linha, numero_linha e manchete.
Rodar de motion/: python3 -m pytest -q biblioteca/tests

Provam, como no lote 1:
  1. a entrada errada é recusada antes de gerar (inclusive acumulado que não bate com a série oficial e texto que
     cita ativo sem o aviso);
  2. o JSON de exemplo é igual ao dado de origem (SGS 432, 433 e 13522 no cache do site-ativos), e o acumulado em
     12 meses calculado do 433 bate com a SGS 13522 (4,22% em ago/2026);
  3. estrutura: o quadro.mjs é JS válido, cada HTML registra a timeline com o id da composição e carrega o
     leitor da tela, sem CDN;
  4. no navegador (Chrome headless, mesmo seek do render), o que está na tela é igual ao dado.
"""
import copy, json, os, re, shutil, subprocess, sys

import pytest

BIB = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTION = os.path.dirname(BIB)
for p in (os.path.join(MOTION, "comum"), BIB):
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


PECAS = ("eventos", "barra_linha", "numero_linha", "manchete")
M = {p: _modulo(f"{p}_gerar", os.path.join(BIB, p, "gerar.py")) for p in PECAS}
eventos, barra_linha, numero_linha, manchete = (M[p] for p in PECAS)
EXEMPLOS = os.path.join(MOTION, "exemplos")
EX = {"eventos": ["eventos-selic-copom-16x9.json"],
      "barra_linha": ["barra-linha-ipca-16x9.json", "barra-linha-ipca-9x16.json"],
      "numero_linha": ["numero-linha-selic-16x9.json", "numero-linha-selic-9x16.json"],
      "manchete": ["manchete-ipca-16x9.json", "manchete-ipca-marcatexto-9x16.json"]}
TODOS = [(p, a) for p, arqs in EX.items() for a in arqs]
precisa_site = pytest.mark.skipif(not os.path.exists(os.path.join(dados.SITE_ATIVOS, "cache", "dados.sqlite")),
                                  reason="sem cache do site-ativos")


def carregar(nome):
    return json.load(open(os.path.join(EXEMPLOS, nome)))


def _rgb(hexa):
    return "rgb(" + ", ".join(str(int(hexa[i:i + 2], 16)) for i in (1, 3, 5)) + ")"


VERMELHO = _rgb(estilo.ESTILOS["iec"]["cores"]["destaque"])


# ------------------------------------------------------------ comum
def test_pecas_novas_sem_cor_fixa_no_codigo():
    for p in PECAS:
        src = open(os.path.join(BIB, p, "gerar.py"), encoding="utf-8").read()
        assert not re.findall(r"#[0-9a-fA-F]{6}\b", src), f"{p}/gerar.py tem cor fixa"


def test_checar_ativos_exige_aviso_quando_o_texto_cita_ticker():
    erros = []
    assert estilo.checar_ativos({}, ["Selic cai para 13,75%", "Fonte: BCB/SGS 432"], erros) is False and erros == []
    estilo.checar_ativos({}, ["PETR4 sobe 3%"], erros)
    assert erros and "PETR4" in erros[0]
    erros = []
    assert estilo.checar_ativos({"ativos": True}, ["HGLG11 paga 0,9%"], erros) is True and erros == []


def test_acumulado_12m_e_composto():
    mensal = [(f"2025-{m:02d}-01", 1.0) for m in range(1, 13)]
    (_, a), = barra_linha.acumulado_12m(mensal)
    assert abs(a - (1.01 ** 12 - 1) * 100) < 1e-12 and round(a, 2) == 12.68     # não é 12,00 (soma simples)


# ------------------------------------------------------------ validação
def _base_serie(n=3):
    return [{"data": f"2026-0{k + 1}-01", "valor": 10 + k} for k in range(n)]


EVENTOS = {"titulo": "T", "fonte": "Fonte: BCB/SGS 432", "classe": "indicador", "serie": _base_serie(),
           "eventos": [{"data": "2026-02-01", "rotulo": "Copom"}]}


@pytest.mark.parametrize("mexer, trecho", [
    (lambda d: d.pop("eventos"), "1 a 8"),
    (lambda d: d.update(eventos=[{"data": "2026-02-01", "rotulo": "x"}] * 9), "1 a 8"),
    (lambda d: d["eventos"].append({"data": "2027-01-01", "rotulo": "depois"}), "fora do período"),
    (lambda d: d["eventos"].insert(0, {"data": "2026-03-01", "rotulo": "antes"}), "fora de ordem"),
    (lambda d: d["eventos"][0].update(rotulo="um rótulo comprido demais para o celular"), "no máximo 22"),
    (lambda d: d["eventos"][0].update(rotulo="PETR4 caiu"), "cita ativo"),
    (lambda d: d.pop("classe"), "'classe' é obrigatória"),          # a validação do grafico_cotacao vale aqui
    (lambda d: d.update(fonte="BCB"), "começar com 'Fonte:'"),
])
def test_eventos_entrada_invalida(mexer, trecho):
    d = copy.deepcopy(EVENTOS)
    mexer(d)
    with pytest.raises(estilo.DadosInvalidos) as e:
        eventos.validar(d)
    assert any(trecho in m for m in e.value.args[0]), e.value.args[0]


def test_eventos_ativo_isolado_segue_a_regra_do_grafico():
    d = {**copy.deepcopy(EVENTOS), "classe": "ativo"}
    with pytest.raises(estilo.DadosInvalidos) as e:
        eventos.validar(d)
    assert any("compliance" in m for m in e.value.args[0])


def _mensal(n, v=0.4, inicio=(2024, 1)):
    a, m = inicio
    out = []
    for _ in range(n):
        out.append({"data": f"{a}-{m:02d}-01", "valor": v})
        a, m = (a + 1, 1) if m == 12 else (a, m + 1)
    return out


BL = {"titulo": "T", "fonte": "Fonte: BCB/SGS 433", "mostrar": 6, "mensal": _mensal(17)}


@pytest.mark.parametrize("mexer, trecho", [
    (lambda d: d.update(mensal=_mensal(16)), "são precisos 17"),
    (lambda d: d["mensal"].pop(5), "seguidos"),
    (lambda d: d.update(mostrar=3), "6 a 24"),
    (lambda d: d["mensal"][0].update(valor="0,4"), "inválido"),
    (lambda d: d.update(referencia_12m=[{"data": r["data"], "valor": 4.89} for r in d["mensal"][-6:]]), "não bate"),
    (lambda d: d.update(referencia_12m=[]), "sem o mês"),
    (lambda d: d.update(titulo="BBAS3 e o IPCA"), "cita ativo"),
])
def test_barra_linha_entrada_invalida(mexer, trecho):
    d = copy.deepcopy(BL)
    mexer(d)
    with pytest.raises(estilo.DadosInvalidos) as e:
        barra_linha.validar(d)
    assert any(trecho in m for m in e.value.args[0]), e.value.args[0]


def test_barra_linha_referencia_que_bate_passa():
    d = copy.deepcopy(BL)
    oficial = round((1.004 ** 12 - 1) * 100, 2)
    d["referencia_12m"] = [{"data": r["data"], "valor": oficial} for r in d["mensal"][-6:]]
    s = barra_linha.series(barra_linha.validar(d))
    assert len(s) == 6 and all(round(a, 2) == oficial for _, _, a in s)


NL = {"titulo": "T", "fonte": "Fonte: BCB/SGS 432", "serie": _base_serie(), "linha": "degrau"}


@pytest.mark.parametrize("mexer, trecho", [
    (lambda d: d.update(serie=d["serie"][:1]), "pelo menos 2"),
    (lambda d: d["serie"].reverse(), "fora de ordem"),
    (lambda d: d.update(linha="curva"), "'linha'"),
    (lambda d: d.update(classe="ativo"), "exige \"ativos\": true"),
    (lambda d: d.update(rotulo_numero="ITUB4 hoje"), "cita ativo"),
    (lambda d: d.update(duracao=4), "'duracao'"),
])
def test_numero_linha_entrada_invalida(mexer, trecho):
    d = copy.deepcopy(NL)
    mexer(d)
    with pytest.raises(estilo.DadosInvalidos) as e:
        numero_linha.validar(d)
    assert any(trecho in m for m in e.value.args[0]), e.value.args[0]


MC = {"frase": "Selic cai para 13,75% hoje", "chave": "13,75%", "fonte": "Fonte: BCB/SGS 432", "duracao": 6}


@pytest.mark.parametrize("mexer, trecho", [
    (lambda d: d.update(chave="13,7"), "palavra(s) inteira(s)"),
    (lambda d: d.update(frase="13,75% e 13,75%"), "uma vez só"),
    (lambda d: d.update(frase="x" * 91), "no máximo 90"),
    (lambda d: d.update(marca="neon"), "'marca'"),
    (lambda d: d.update(palavras=[0.1, 0.2]), "cada uma das 5 palavras"),
    (lambda d: d.update(palavras=[0.5, 0.4, 0.6, 0.7, 0.8]), "em ordem"),
    (lambda d: d.update(t_chave=5.5), "até 0,8 s antes do fim"),
    (lambda d: d.update(palavras=[0.2, 0.4, 0.6, 2.0, 2.4], t_chave=1.0), "antes de a palavra-chave aparecer"),
    (lambda d: d.update(frase="VALE3 sobe para 13,75% hoje"), "cita ativo"),
    (lambda d: d.pop("fonte"), "'fonte' é obrigatório"),
])
def test_manchete_entrada_invalida(mexer, trecho):
    d = copy.deepcopy(MC)
    mexer(d)
    with pytest.raises(estilo.DadosInvalidos) as e:
        manchete.validar(d)
    assert any(trecho in m for m in e.value.args[0]), e.value.args[0]


def test_manchete_chave_no_tempo_da_fala():
    d = manchete.validar({**MC, "palavras": [0.2, 0.5, 0.8, 1.4, 2.0]})
    assert d["t_chave"] == 1.4 and manchete.tempos(d)["tp"] == 1.9      # a chave enche quando é falada
    assert manchete.posicao_chave(d["frase"], "13,75%") == (3, 4)
    d2 = manchete.validar({**MC, "ativos": True, "frase": "VALE3 sobe para 13,75% hoje"})
    assert estilo.AVISO_ATIVOS in manchete.montar_html(d2)


# ------------------------------------------------------------ estrutura (HTML e quadro.mjs)
def test_quadro_mjs_e_js_valido_e_generico():
    if not shutil.which("node"):
        pytest.skip("sem node")
    q = os.path.join(MOTION, "comum", "quadro.mjs")
    subprocess.run(["node", "--check", q], check=True)
    src = open(q).read()
    assert "window.__tela()" in src and "data-composition-id" in src and "tl.seek(t, false)" in src


@pytest.mark.parametrize("peca, arquivo", TODOS)
def test_exemplo_valido_estrutura_e_sem_cdn(peca, arquivo):
    d = carregar(arquivo)
    assert d["peca"] == peca and d["fonte"].startswith("Fonte: BCB/SGS ")
    html = M[peca].montar_html(d)
    comp = re.search(r'data-composition-id="([^"]+)"', html).group(1)
    assert f'window.__timelines["{comp}"] = tl' in html
    assert '<script src="assets/tela.js"></script>' in html and '<script src="assets/gsap.min.js"></script>' in html
    assert "cdn." not in html and "http" not in html.split("<body>")[1]
    assert re.search(r'id="fonte"[^>]*>' + re.escape(estilo.esc(d["fonte"])) + "<", html)
    # só cores da PAL do molde no HTML
    pal, _ = estilo.ler_molde()
    cores_pal = {c.lower() for c in pal.values()} | {estilo.misturar(pal["ink"], pal["faint"], .55).lower()}
    assert {c.lower() for c in re.findall(r"#[0-9a-fA-F]{6}\b", html)} <= cores_pal


# ------------------------------------------------------------ dado real
@precisa_site
def test_ipca_acumulado_do_433_bate_com_a_13522():
    """O acumulado em 12 meses calculado do IPCA mensal (SGS 433) bate com a SGS 13522 em todos os meses do cache
    (até 0,01 p.p.: o BCB arredonda), e o último é 4,22% (ago/2026)."""
    mensal, _ = dados.bcb(433, "2019-01-01")
    oficial = dict(dados.bcb(13522, "2019-01-01")[0])
    calc = barra_linha.acumulado_12m(mensal)
    assert len(calc) >= 60
    for data, v in calc:
        assert abs(round(v, 2) - oficial[data]) <= 0.01 + 1e-9, (data, v, oficial[data])
    data, v = calc[-1]
    assert data == "2026-08-01" and oficial[data] == 4.22 and round(v, 2) == 4.22


@precisa_site
@pytest.mark.parametrize("arquivo", EX["barra_linha"])
def test_exemplo_ipca_igual_ao_sqlite(arquivo):
    d = carregar(arquivo)
    mensal, ref, _ = dados.ipca(d["mostrar"])
    assert [(p["data"], p["valor"]) for p in d["mensal"]] == mensal
    assert [(p["data"], p["valor"]) for p in d["referencia_12m"]] == ref
    s = barra_linha.series(barra_linha.validar(d))
    assert s[-1][0] == "2026-08-01" and round(s[-1][2], 2) == 4.22 and s[-1][1] == -0.32
    assert d["_conferido"]["sgs_13522"] == 4.22


@precisa_site
@pytest.mark.parametrize("arquivo", EX["numero_linha"])
def test_exemplo_selic_igual_ao_sqlite(arquivo):
    d = carregar(arquivo)
    pontos, _ = dados.bcb(432, "2020-01-01")
    assert [(p["data"], p["valor"]) for p in d["serie"]] == dados.S.so_mudancas(pontos)
    assert d["serie"][-1]["valor"] == pontos[-1][1] == 13.75


@precisa_site
def test_eventos_copom_sao_mudancas_reais_da_selic():
    d = carregar("eventos-selic-copom-16x9.json")
    mud = {data: (v, v0) for data, v, v0 in dados.mudancas_selic()}
    assert len(d["eventos"]) == 3
    for e in d["eventos"]:
        v, v0 = mud[e["data"]]                                 # cada evento é uma decisão que mudou a meta
        assert e["rotulo"].endswith(f"{estilo.fmt_br(v, 2)}%")
    assert [e["rotulo"].split(":")[0] for e in d["eventos"]] == ["1ª alta", "Pico", "1º corte"]
    assert max(p["valor"] for p in d["serie"]) == 15.0


@precisa_site
@pytest.mark.parametrize("arquivo", EX["manchete"])
def test_manchete_ipca_igual_a_13522(arquivo):
    d = carregar(arquivo)
    r, _ = dados.bcb(13522, "2019-01-01")
    (_, v0), (d1, v1) = r[-2], r[-1]
    assert d["chave"] == f"{estilo.fmt_br(v1, 2)}%" == "4,22%"
    assert ("cai" if v1 < v0 else "sobe") in d["frase"].split() and "agosto" in d["frase"]


# ------------------------------------------------------------ navegador: a tela é igual ao dado
def _quadros(peca, d, instantes, tmp_path):
    projeto = str(tmp_path / "p")
    M[peca].gerar_projeto(d, projeto)
    r = teste.quadros(projeto, instantes, str(tmp_path / "q"))
    assert r["erros"] == [], r["erros"]
    assert {"Archivo Black 400", "Montserrat 700"} <= set(r["fontes"])
    assert abs(r["quadros"][-1]["duracao"] - float(d["duracao"])) < 1e-6
    return [q["tela"] for q in r["quadros"]]


@teste.precisa_navegador
def test_eventos_na_tela(tmp_path):
    d = eventos.validar(carregar("eventos-selic-copom-16x9.json"))
    P = eventos.posicoes(d)
    antes, fim = _quadros("eventos", d, [P[1]["t"] - .05, d["duracao"]], tmp_path)
    # cada marcador no lugar e com o rótulo do dado; o número final é o último da série
    assert [e["rotulo"] for e in fim["eventos"]] == [e["rotulo"] for e in d["eventos"]]
    for e, p in zip(fim["eventos"], P):
        assert e["visivel"] and abs(e["x"] - p["x"]) < .01 and abs(e["y"] - p["y"]) < .01
        assert 0 <= e["caixa"]["x0"] and e["caixa"]["x1"] <= fim["W"]
    caixas = [e["caixa"] for e in fim["eventos"]]
    for a in range(len(caixas)):                                   # rótulos não se sobrepõem
        for b in range(a + 1, len(caixas)):
            A, B = caixas[a], caixas[b]
            assert A["x1"] <= B["x0"] or B["x1"] <= A["x0"] or A["y1"] <= B["y0"] or B["y1"] <= A["y0"]
    assert fim["numero"] == estilo.texto_valor(d["serie"][-1]["valor"], d["unidade"])
    assert fim["fonte"] == d["fonte"]
    # aparece com a linha: antes de a ponta passar pelo 2º evento, só o 1º está aceso
    assert [e["visivel"] for e in antes["eventos"]] == [True, False, False]


@teste.precisa_navegador
@pytest.mark.parametrize("arquivo", EX["barra_linha"])
def test_barra_linha_na_tela(arquivo, tmp_path):
    d = barra_linha.validar(carregar(arquivo))
    s = barra_linha.series(d)
    G = barra_linha.geometria(d)
    T = barra_linha.tempos(d, len(s))
    barras, fim = _quadros("barra_linha", d, [T["tb"] + .05, d["duracao"]], tmp_path)
    # fase 1: uma barra por mês, altura proporcional ao valor do mês, para baixo se negativo
    for b, (data, m, _), k in zip(barras["barras"], s, range(len(s))):
        assert b["data"] == data
        assert abs(b["h"] - abs(m) * G["escala1"]) < .6
        assert abs((b["y"] if m >= 0 else b["y"] + b["h"]) - G["y_mes"][k]) < .6
        assert abs(b["w"] - G["bw"]) < .01
        if b["rotulo"] is not None:
            assert b["rotulo"] == estilo.fmt_br(m, 2) and b["rotulo_visivel"]
    assert barras["mes_visivel"] and barras["numero_mes"] == f"{estilo.fmt_br(s[-1][1], 2)}%"
    # fim: cada barra virou um ponto na altura do acumulado em 12 meses; o placar pousa no último (4,22%)
    for b, k in zip(fim["barras"], range(len(s))):
        assert abs(b["y"] + b["h"] / 2 - G["y_acum"][k]) < .6 and b["w"] < 20
    assert fim["doze_visivel"] and not fim["mes_visivel"]
    assert fim["numero"] == f"{estilo.fmt_br(s[-1][2], 2)}%" == "4,22%"
    assert fim["cor_numero"] == VERMELHO and fim["barras"][-1]["cor"] == VERMELHO
    assert fim["rotulo_doze"].endswith("ago/2026") and fim["fonte"] == d["fonte"]
    assert fim["revelado"] >= G["L"]["gx1"] - G["L"]["gx0"]


@teste.precisa_navegador
@pytest.mark.parametrize("arquivo", EX["numero_linha"])
def test_numero_linha_na_tela(arquivo, tmp_path):
    d = numero_linha.validar(carregar(arquivo))
    G = numero_linha.geometria(d)
    T = numero_linha.tempos(d)
    f0, f1, c0 = numero_linha.tamanhos(d)
    grande, meio, fim = _quadros("numero_linha", d, [T["ts0"] - .1, (T["ts1"] + T["tl1"]) / 2, d["duracao"]], tmp_path)
    final = estilo.texto_valor(d["serie"][-1]["valor"], d["unidade"])
    # o número grande, no centro, é o último valor da série
    assert grande["numero"] == final and grande["corpo"] == f0
    assert abs(grande["caixa"]["cx"] - c0[0]) < 2 and abs(grande["caixa"]["cy"] - c0[1]) < 2
    assert not grande["ponto"]["visivel"]
    # no fim, pequeno, logo acima do último ponto, que está aceso no lugar do último dado
    assert fim["numero"] == final and fim["corpo"] == f1 and fim["cor_numero"] == VERMELHO
    ax, ay = numero_linha.final_ancora(G)
    assert abs(fim["caixa"]["x1"] - ax) < 2 and abs(fim["caixa"]["y1"] - ay) < 2
    assert fim["ponto"]["visivel"] and (fim["ponto"]["cx"], fim["ponto"]["cy"]) == (G["xs"][-1], G["ys"][-1])
    assert fim["caixa"]["y1"] < G["L"]["gy0"]                      # o número não cobre o gráfico
    # a linha se desenha de trás para a frente: no meio, só a parte da direita
    assert G["L"]["gx0"] < meio["revelado_desde"] < G["L"]["gx1"]
    assert abs(fim["revelado_desde"] - G["L"]["gx0"]) < .01
    assert fim["variacao"] == numero_linha.G.texto_variacao(d) == "+9,25 p.p. desde jan/2020"
    assert fim["fonte"] == d["fonte"] == "Fonte: BCB/SGS 432 (meta Selic)"


@teste.precisa_navegador
@pytest.mark.parametrize("arquivo", EX["manchete"])
def test_manchete_na_tela(arquivo, tmp_path):
    d = manchete.validar(carregar(arquivo))
    T = manchete.tempos(d)
    antes, meio, fim = _quadros("manchete", d, [T["tc"] - .05, T["tc"] + T["dc"] / 2, d["duracao"]], tmp_path)
    assert fim["frase"] == d["frase"] and fim["chave"] == d["chave"]
    assert all(p["visivel"] for p in fim["palavras"])
    assert antes["enchimento"] == 0 and 0 < meio["enchimento"] < 1 and fim["enchimento"] == 1
    assert re.fullmatch(r"inset\(0(px)?( 0(\.0+)?%? 0(px)? 0(px)?)?\)", fim["clip"]), fim["clip"]   # nada recortado
    if d["marca"] == "marca-texto":
        assert fim["faixa"]["cor"] == VERMELHO and fim["faixa"]["escala"] == 1
        assert fim["cor_cheia"] == _rgb(estilo.ESTILOS["iec"]["cores"]["papel"])
    else:
        assert fim["faixa"] is None and fim["cor_cheia"] == VERMELHO
    c = fim["chave_caixa"]
    assert 0 <= c["x"] and c["x"] + c["w"] <= c["W"] and 0 <= c["y"] and c["y"] + c["h"] <= c["H"]
    assert fim["fonte"] == d["fonte"] and fim["fonte_visivel"] and fim["aviso"] == ""
