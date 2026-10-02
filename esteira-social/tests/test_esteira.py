"""Testes da esteira social no contrato do juiz-post (agentes/juiz-post.md) e do leitor-frio (agentes/leitor-frio.md).

Rodar: cd esteira-social && python3 -m pytest -q tests/
Os testes leem os cards gravados em cards/ (o que o juiz-post recebe) e conferem que eles são exatamente o que
gerar_cards.py produz hoje.
"""
import csv
import json
import re
import subprocess
import sys
from collections import Counter
from pathlib import Path

import pytest

AQUI = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(AQUI))
import gerar_cards as g  # noqa: E402

CARDS = AQUI / "cards"
ROWS = g.ler_calendario()
MONTADOS = g.montar_cards(ROWS)
IDS = [c["id"] for c in MONTADOS]
ARQUIVOS = sorted(p.name for p in CARDS.glob("*.md") if p.name not in ("GATE-RELATORIO.md", "AUTOEXAME.md"))


def ler_card(arquivo):
    txt = (CARDS / arquivo).read_text(encoding="utf-8")
    fm = {k: json.loads(v) for k, v in re.findall(r"^(\w+): (.*)$", txt.split("---\n")[1], re.M)}
    js = json.loads(txt.split("---JSON---\n")[1].split("\n---FIM---")[0])
    return txt, fm, js


def textos_do_post(js):
    """O que vai ao ar (sem hashtags): slides, legenda e posts do X."""
    return [s["texto"] for s in js["slides"]] + [js["instagram_caption"]] + [t["texto"] for t in js["tweets"]]


# ---------------------------------------------------------------- cobertura
def test_calendario_v2_tem_21_longos_e_16_shorts():
    assert Counter(r["formato"] for r in ROWS) == {"longo": 21, "short": 16}


def test_todo_video_tem_um_card_com_as_duas_redes():
    """Contrato do juiz-post: um card = carrossel + legenda (Instagram) + 3 a 5 posts (X)."""
    esperados = sorted(f"{r['data']}-{g.slugify(r['titulo'])}.md" for r in ROWS)
    assert ARQUIVOS == esperados
    for a in ARQUIVOS:
        _, _, js = ler_card(a)
        assert js["slides"] and js["instagram_caption"] and 3 <= len(js["tweets"]) <= 5, a


def test_cards_gravados_sao_os_que_o_gerador_produz(tmp_path):
    g.gravar(MONTADOS, tmp_path, gate=None)
    for a in ARQUIVOS:
        assert (tmp_path / a).read_text(encoding="utf-8") == (CARDS / a).read_text(encoding="utf-8"), a


def test_indice_e_a_fila_do_juiz():
    with open(CARDS / "INDICE.csv", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    assert sorted(l["arquivo"] for l in linhas) == ARQUIVOS
    assert all(l["status"] == "rascunho" and l["juiz_post"] == "pendente" and l["leitor_frio"] == "pendente"
               and l["autoexame"] == "OK" for l in linhas)


# ---------------------------------------------------------------- formato de entrada do juiz-post e do leitor-frio
SECOES = ["## PARA O JUIZ-POST", "### CARROSSEL DO INSTAGRAM", "### LEGENDA", "### HASHTAGS", "### POSTS DO X",
          "## PARA O LEITOR-FRIO", "## FONTES E NÚMEROS", "## PENDÊNCIAS", "## PUBLICAÇÃO"]
CAMPOS = ["id", "tipo", "status", "juiz", "depois", "video_data", "video_formato", "video_titulo", "temas",
          "mensagem_capa", "estrutura", "mecanica", "instagram_data", "x_data", "pngs"]


@pytest.mark.parametrize("arquivo", ARQUIVOS)
def test_card_no_formato_do_juiz_post(arquivo):
    txt, fm, js = ler_card(arquivo)
    for c in CAMPOS:
        assert str(fm.get(c, "")).strip() not in ("", "[]"), f"campo vazio: {c}"
    assert fm["tipo"] == "🎬 vídeo do canal" and fm["status"] == js["status"] == "rascunho"
    assert fm["juiz"] == "juiz-post" and fm["depois"] == "leitor-frio"
    for s in SECOES:
        assert s in txt, s
    # card 🎬: capa do carrossel e imagem do post A = thumbnail do YouTube
    assert "thumbnail" in js["slides"][0]["imagem"] and "thumbnail" in js["tweets"][0]["imagem"]
    # prova: print oficial ou nada; nunca foto de banco/IA sugerida como imagem
    for s in js["slides"][1:]:
        assert s["imagem"].startswith(("print legível", "sem imagem")), s["imagem"]
    assert [t["letra"] for t in js["tweets"]] == list("ABCDE"[:len(js["tweets"])])
    assert all(s["png"].endswith(f'slide-{s["numero"]}.png') for s in js["slides"])
    lf = js["leitor_frio"]
    assert lf["pngs"] == [s["png"] for s in js["slides"]] and lf["legenda"] == js["instagram_caption"]
    assert lf["mensagem_pretendida_da_capa"].strip()
    assert not re.search(r"\[(texto|descrição|TODO)\]|\{\w+\}", txt)


@pytest.mark.parametrize("card", MONTADOS, ids=IDS)
def test_autoexame_sem_problema(card):
    """Cada critério do juiz-post e do leitor-frio que dá para medir no texto (ver AUTOEXAME.md)."""
    assert g.autoexame(card) == []


@pytest.mark.parametrize("texto,criterio", [
    ("Isso só vale pra quem tem cota.", "afirmação absoluta"),
    ("Todo mundo recebe todo mês.", "afirmação absoluta"),
    ("O vídeo completo está no link da bio.", "CTA ou link"),
    ("A Selic subiu e o FII caiu.", "jargão"),
    ("Você sabia que o CDB rende?", "palavra proibida"),
])
def test_autoexame_pega_o_que_o_juiz_reprova(texto, criterio):
    c = dict(MONTADOS[0])
    c["posts"] = MONTADOS[0]["posts"][:2] + [{"letra": "C", "texto": texto, "imagem": "", "png": ""}]
    c["texto_gate"] = MONTADOS[0]["texto_gate"] + "\n" + texto
    assert any(criterio in crit for crit, _ in g.autoexame(c)), g.autoexame(c)


def test_checar_nao_elimina_o_card():
    """Decisão do Mac: o [CHECAR] fica para o Denis preencher na publicação e não elimina o card."""
    com = [c for c in MONTADOS if g.pendencias(c)]
    assert {c["video_data"] for c in com} == {"2026-10-28", "2026-11-05"}
    assert all(g.autoexame(c) == [] for c in com)


@pytest.mark.parametrize("arquivo", ARQUIVOS)
def test_sem_cta_link_hashtag_no_texto_julgado(arquivo):
    _, _, js = ler_card(arquivo)
    for t in textos_do_post(js):
        assert not g.RE_CTA.search(g.RE_CHECAR.sub(" ", t)), t
        assert "#" not in t, t


# ---------------------------------------------------------------- X
@pytest.mark.parametrize("arquivo", ARQUIVOS)
def test_x_limites(arquivo):
    _, fm, js = ler_card(arquivo)
    tw = [t["texto"] for t in js["tweets"]]
    assert len(tw) >= (4 if fm["video_formato"] == "longo" else 3)
    for i, t in enumerate(tw):
        assert len(t) <= g.LIMITE_X, f"post {'ABCDE'[i]}: {len(t)} caracteres"
    assert tw[0].startswith("Tanaka, ") and len(tw[0].split("\n")[0].split()) <= 8


def test_x_nenhuma_mecanica_mais_de_5_vezes():
    cont = Counter(c["mecanica"].split(" (")[0] for c in MONTADOS)
    assert max(cont.values()) <= 5, cont.most_common(3)


def test_x_estruturas_equilibradas():
    """Só há 5 estruturas (A-E) para 37 cards: o mínimo possível na mais usada é 8."""
    cont = Counter(c["estrutura"] for c in MONTADOS)
    assert set(cont) == set("ABCDE") and max(cont.values()) <= 8, cont


def test_x_rotacao_de_estrutura_e_mecanica():
    xs = sorted(MONTADOS, key=lambda c: (c["publicacao"]["x"]["data"], c["publicacao"]["x"]["horario"]))
    fam = lambda c, campo: c[campo].split(" (")[0]
    rep = [(a["id"], b["id"], k) for a, b in zip(xs, xs[1:]) for k in ("estrutura", "mecanica") if fam(a, k) == fam(b, k)]
    assert not rep, rep


# ---------------------------------------------------------------- Instagram
@pytest.mark.parametrize("arquivo", ARQUIVOS)
def test_instagram_limites(arquivo):
    _, fm, js = ler_card(arquivo)
    leg = js["instagram_caption"]
    assert leg.startswith("Tanaka, ") and 200 <= len(leg) <= 500
    assert len(leg) + 2 + len(js["hashtags"]) <= 2200
    n = len(js["slides"])
    assert n == 5 if fm["video_formato"] == "longo" else 4 <= n <= 5
    tags = js["hashtags"].split()
    assert 5 <= len(tags) <= 10 and len(set(tags)) == len(tags)


@pytest.mark.parametrize("arquivo", ARQUIVOS)
def test_instagram_hashtags_so_do_tema_do_video(arquivo):
    _, _, js = ler_card(arquivo)
    temas = js["temas"]
    assert temas and all(t in g.HASHTAGS_TEMA for t in temas)
    permitidas = set(g.HASHTAGS_GERAL).union(*(g.HASHTAGS_TEMA[t] for t in temas))
    assert not [h for h in js["hashtags"].split() if h not in permitidas]


def test_card_de_tesouro_nao_leva_hashtag_de_banco():
    for c in MONTADOS:
        if "renda fixa bancária" not in c["temas"]:
            assert not set(c["hashtags"].split()) & {"#CDB", "#LCI", "#LCA", "#LCIeLCA", "#FGC"}, c["id"]


def test_temas_batem_com_o_titulo():
    chaves = {"tesouro": "Tesouro", "fii": "FII", "fundo imobili": "FII", "fundos imobili": "FII", "etf": "ETF",
              "cdb": "renda fixa bancária", "lci": "renda fixa bancária", "fgc": "renda fixa bancária", "bitcoin": "cripto"}
    for r in ROWS:
        for k, tema in chaves.items():
            if k in r["titulo"].lower():
                assert tema in g.conteudo.TEMAS_VIDEO[r["data"]], (r["data"], k)


# ---------------------------------------------------------------- fontes, números e regras do canal
@pytest.mark.parametrize("card", MONTADOS, ids=IDS)
def test_nenhum_numero_inventado_nem_ranking_sem_fonte(card):
    assert g.checar_numeros(card, card["_row"]) == []
    assert g.checar_afirmacoes(card) == []


def test_checadores_pegam_numero_e_ranking_inventados():
    c = dict(MONTADOS[0], texto_gate=MONTADOS[0]["texto_gate"] + "\nA Selic está em 13,4%. Foi o vídeo mais visto do canal.")
    assert any("13,4" in p for p in g.checar_numeros(c, c["_row"]))
    assert g.checar_afirmacoes(c)


@pytest.mark.parametrize("arquivo", ARQUIVOS)
def test_sem_recomendacao_corretora_fonte_ou_disclaimer(arquivo):
    _, _, js = ler_card(arquivo)
    texto = "\n".join(textos_do_post(js))
    assert not [p for p in g.PROIBIDAS if p in texto.lower()]
    assert not g.RE_FONTE.search(texto) and not g.CORRETORAS.search(texto)


def test_publicacao_relativa_ao_video():
    for c in MONTADOS:
        v = c["video_data"]
        assert c["publicacao"]["x"]["data"] == v
        assert c["publicacao"]["instagram"]["data"] >= v


# ---------------------------------------------------------------- gate de qualidade
GATE = g.carregar_gate()


@pytest.mark.skipif(GATE is None, reason="gate_qualidade.py não encontrado (defina IC_GATE)")
def test_gate_sem_bloqueio():
    reprovados = []
    for c in MONTADOS:
        r = g.rodar_gate(GATE, c)
        if r["codigo_saida"] == 2:
            reprovados.append(c["arquivo"] + " -> " + "; ".join(
                f'{p["codigo"]}: {p.get("trecho", "")}' for p in r["problemas"] if p["nivel"] == "BLOQUEANTE"))
    assert not reprovados, "\n" + "\n".join(reprovados)


@pytest.mark.skipif(GATE is None, reason="gate_qualidade.py não encontrado (defina IC_GATE)")
def test_gate_sem_aviso_de_conteudo():
    """Aceitos: DADOS_VELHOS (tabelas do gate mais velhas que a data do card) e 'perfil de investidor', que vem do
    título do Short de 16/11 no calendário."""
    inesperados = []
    for c in MONTADOS:
        for p in g.rodar_gate(GATE, c)["problemas"]:
            if p["codigo"] == "DADOS_VELHOS":
                continue
            if p["codigo"] == "PADRAO_IA" and c["video_data"] == "2026-11-16" and \
                    p["trecho"] == "expressões: perfil de investidor":
                continue
            inesperados.append(f'{c["arquivo"]}: {p["codigo"]} {p.get("trecho", "")}')
    assert not inesperados, inesperados


@pytest.mark.skipif(GATE is None, reason="gate_qualidade.py não encontrado (defina IC_GATE)")
def test_gate_pela_linha_de_comando_da_o_mesmo_resultado():
    c = next(c for c in MONTADOS if c["video_data"] == "2026-10-19")
    p = subprocess.run([sys.executable, GATE.__file__, "-", "--titulo", c["video_titulo"], "--data",
                        c["publicacao"]["instagram"]["data"], "--json"], input=c["texto_gate"], capture_output=True, text=True)
    assert json.loads(p.stdout)["resultado"] == g.rodar_gate(GATE, c)["resultado"]
