"""Testes da esteira social: cobertura do calendário, limites, voz, regras do canal, números e gate.

Rodar: cd esteira-social && python3 -m pytest -q tests/
Os testes leem os cards gravados em cards/ (o que o juiz-post vai receber) e conferem que eles são
exatamente o que gerar_cards.py produz hoje.
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
POR_ID = {c["id"]: c for c in MONTADOS}


def ler_card(arquivo):
    txt = (CARDS / arquivo).read_text(encoding="utf-8")
    fm = dict(re.findall(r"^(\w+): (.*)$", txt.split("---\n")[1], re.M))
    fm = {k: json.loads(v) for k, v in fm.items()}
    js = json.loads(txt.split("---JSON---\n")[1].split("\n---FIM---")[0])
    return txt, fm, js


ARQUIVOS = sorted(p.name for p in CARDS.glob("*.md") if p.name != "GATE-RELATORIO.md")
X = [a for a in ARQUIVOS if a.endswith("-x.md")]
IG = [a for a in ARQUIVOS if a.endswith("-ig.md")]


def textos_do_post(js):
    """Tudo o que vai ao ar (sem hashtags)."""
    if js["rede"] == "x":
        return [t["texto"] for t in js["tweets"]] + [js["reply_com_link"]]
    return [js["instagram_caption"], js["cta"]] + [s["texto"] for s in js["slides"]]


# ---------------------------------------------------------------- cobertura
def test_calendario_v2_tem_21_longos_e_16_shorts():
    c = Counter(r["formato"] for r in ROWS)
    assert c == {"longo": 21, "short": 16}


def test_todo_video_tem_card_nas_duas_redes():
    faltam = []
    for r in ROWS:
        slug = g.slugify(r["titulo"])
        for rede in ("x", "ig"):
            if f"{r['data']}-{slug}-{rede}.md" not in ARQUIVOS:
                faltam.append(f"{r['data']} {rede}")
    assert not faltam, faltam
    assert len(X) == len(IG) == len(ROWS) == 37


def test_cards_gravados_sao_os_que_o_gerador_produz(tmp_path):
    g.gravar(MONTADOS, tmp_path, gate=None)
    for a in ARQUIVOS:
        assert (tmp_path / a).read_text(encoding="utf-8") == (CARDS / a).read_text(encoding="utf-8"), a


def test_indice_bate_com_os_arquivos():
    with open(CARDS / "INDICE.csv", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    assert sorted(l["arquivo"] for l in linhas) == ARQUIVOS
    assert Counter(l["rede"] for l in linhas) == {"x": 37, "instagram": 37}
    assert all(l["status"] == "rascunho" for l in linhas)


# ---------------------------------------------------------------- formato para o juiz-post
CAMPOS = ["id", "rede", "formato", "status", "juiz", "data_publicacao", "horario", "relativa_ao_video",
          "video_data", "video_formato", "video_titulo", "assunto", "termo_busca", "gancho", "pendencias_checar"]


@pytest.mark.parametrize("arquivo", ARQUIVOS)
def test_card_completo_e_rascunho(arquivo):
    txt, fm, js = ler_card(arquivo)
    for c in CAMPOS + (["estrutura", "mecanica"] if arquivo.endswith("-x.md") else []):
        assert str(fm.get(c, "")).strip() != "", f"campo vazio: {c}"
    assert fm["status"] == js["status"] == "rascunho"
    assert fm["juiz"] == "juiz-post"
    assert js["cta"].strip() and js["gancho"].strip() and js["imagem"].strip()
    assert "## 📌 FONTES E NÚMEROS" in txt and "## ⚠️ PENDÊNCIAS" in txt
    # nada de template vazio
    assert not re.search(r"\[(texto|descrição|TODO)\]|\{\w+\}", txt)
    # data de publicação relativa ao vídeo: nunca antes do vídeo, no máximo D+1
    d, v = fm["data_publicacao"], fm["video_data"]
    assert v <= d and (d == v or fm["relativa_ao_video"].startswith("D+1"))


# ---------------------------------------------------------------- X
@pytest.mark.parametrize("arquivo", X)
def test_x_limites_e_regras_do_brief(arquivo):
    _, fm, js = ler_card(arquivo)
    tw = [t["texto"] for t in js["tweets"]]
    assert 3 <= len(tw) <= 5
    assert len(tw) == (5 if fm["video_formato"] == "longo" else 3)
    for i, t in enumerate(tw, 1):
        assert len(t) <= g.LIMITE_X, f"tweet {i}: {len(t)} caracteres"
        assert not re.search(r"https?://|www\.|#\w", t), f"tweet {i}: link ou hashtag no corpo"
        assert not re.search(r"[\U0001F300-\U0001FAFF☀-➿]", t), f"tweet {i}: emoji"
    # capa "Tanaka, ..." (memória feedback_persona_tanaka_voice: thread abre com "Tanaka,", não "Fala, Tanaka")
    assert tw[0].startswith("Tanaka, ")
    primeira = tw[0].split("\n")[0]
    assert len(primeira.split()) <= 8, f'1ª linha com {len(primeira.split())} palavras: "{primeira}"'
    assert js["estrutura"] in "ABCDE" and js["mecanica"]
    # o link vai na reply, nunca no corpo (X-COPYWRITER-BRIEF, algoritmo)
    assert "LINK" in js["reply_com_link"] and not any("LINK" in t for t in tw)


def test_x_nenhuma_mecanica_mais_de_5_vezes():
    """Piada/formato (mecânica): no máximo 5 threads cada, para não virar molde."""
    cont = Counter(c["mecanica"].split(" (")[0] for c in MONTADOS if c["rede"] == "x")
    assert max(cont.values()) <= 5, cont.most_common(3)


def test_x_estruturas_equilibradas():
    """O brief só tem 5 estruturas (A-E) para 37 threads: o mínimo possível é 8 na mais usada.
    O limite de 5 vale para a mecânica; aqui, nenhuma estrutura passa de 8."""
    cont = Counter(c["estrutura"] for c in MONTADOS if c["rede"] == "x")
    assert set(cont) == set("ABCDE") and max(cont.values()) <= 8, cont


def test_x_rotacao_de_estrutura_e_mecanica():
    """X-COPYWRITER-BRIEF: nunca a mesma estrutura nem a mesma mecânica duas threads seguidas."""
    xs = sorted((c for c in MONTADOS if c["rede"] == "x"), key=lambda c: (c["data_publicacao"], c["horario"]))
    fam = lambda c, campo: c[campo].split(" (")[0]  # "eco-do-gatilho (cair)" e "(preso)" são a mesma mecânica
    repetidas = [(a["id"], b["id"], campo) for a, b in zip(xs, xs[1:])
                 for campo in ("estrutura", "mecanica") if fam(a, campo) == fam(b, campo)]
    assert not repetidas, repetidas


# ---------------------------------------------------------------- Instagram
@pytest.mark.parametrize("arquivo", IG)
def test_instagram_limites(arquivo):
    _, fm, js = ler_card(arquivo)
    leg = js["instagram_caption"]
    assert 200 <= len(leg) <= 500, f"legenda com {len(leg)} caracteres (brief: 200-500)"
    total = len(leg) + 2 + len(js["cta"]) + 2 + len(js["hashtags"])
    assert total <= 2200, "limite do Instagram"
    tags = js["hashtags"].split()
    assert 5 <= len(tags) <= 10 and all(t.startswith("#") for t in tags) and len(set(tags)) == len(tags)
    n = len(js["slides"])
    assert n == (6 if fm["video_formato"] == "longo" else 4)
    assert js["formato"] == ("carrossel" if fm["video_formato"] == "longo" else "reels")
    for s in js["slides"]:
        assert 0 < len(s["texto"]) <= 120, f'slide {s["numero"]} com {len(s["texto"])} caracteres'
    assert "link na bio" in js["cta"].lower()


@pytest.mark.parametrize("arquivo", IG)
def test_instagram_hashtags_so_do_tema_do_video(arquivo):
    """Nenhuma hashtag de outro tema: só as gerais da marca e as dos temas do próprio vídeo."""
    _, fm, js = ler_card(arquivo)
    temas = js["temas"]
    assert temas and all(t in g.HASHTAGS_TEMA for t in temas)
    permitidas = set(g.HASHTAGS_GERAL).union(*(g.HASHTAGS_TEMA[t] for t in temas))
    fora = [h for h in js["hashtags"].split() if h not in permitidas]
    assert not fora, f"hashtags de outro tema em {temas}: {fora}"


def test_card_de_tesouro_nao_leva_hashtag_de_banco():
    for c in MONTADOS:
        if c["rede"] == "instagram" and "renda fixa bancária" not in c["temas"]:
            assert not set(c["hashtags"].split()) & {"#CDB", "#LCI", "#LCA", "#LCIeLCA", "#FGC"}, c["id"]


def test_temas_batem_com_o_titulo():
    """Sanidade do mapa: título que fala de Tesouro, FII, ETF, CDB/LCI ou bitcoin tem o tema correspondente."""
    chaves = {"tesouro": "Tesouro", "fii": "FII", "fundo imobili": "FII", "fundos imobili": "FII", "etf": "ETF",
              "cdb": "renda fixa bancária", "lci": "renda fixa bancária", "fgc": "renda fixa bancária", "bitcoin": "cripto"}
    for r in ROWS:
        t = r["titulo"].lower()
        temas = g.conteudo.TEMAS_VIDEO[r["data"]]
        for k, tema in chaves.items():
            if k in t:
                assert tema in temas, (r["data"], k, temas)


# ---------------------------------------------------------------- regras do canal
PROIBIDAS = [
    # IC-COPYWRITER SKILL.md + anti-ai-writing-style + feedback_brand_anti_ai_words
    "ecossistema", "jornada", "protagonista", "navegar", "empoderar", "disruptiv", "mindset", "ressignificar",
    "curadoria", "potencializar", "otimizar", "entregar valor", "construir pontes", "visão holística", "sinergia",
    "você sabia", "já pensou se", "sua melhor versão", "você merece", "me siga", "salva esse", "compartilha",
    "marque um amigo", "plot twist", "fala, tanaka", "taná ", "taná,",
    # recomendação (pedido do Denis e gate)
    "vale a pena", "melhor ação", "melhores ações", "qual a melhor", "qual é a melhor", "quais as melhores",
    "hora de comprar", "hora de vender", "recomendo", "carteira recomendada", "compre já", "compre agora",
    # disclaimer e fonte (feedback_copywriter_sem_fonte_sem_disclaimer)
    "não é recomendação", "nao e recomendacao", "conteúdo educativo", "segundo a ", "segundo o ", "de acordo com",
    "levantamento",
]
RE_FONTE = re.compile(r"(^|\n)\s*fontes?:", re.I)  # "Fonte: X" no post (e não "retido na fonte: 17,5%")
CORRETORAS = re.compile(r"\b(XP|Rico|Clear|BTG|Nu ?Invest|Easynvest|Inter|Toro|Modal|Genial|Órama|Warren|Avenue|Nomad|"
                        r"C6|Itaú|Bradesco|Santander|Safra|Ágora|Mirae|Guide|Ativa|Necton|Terra)\b")


@pytest.mark.parametrize("arquivo", ARQUIVOS)
def test_sem_palavra_proibida_recomendacao_corretora_fonte(arquivo):
    _, _, js = ler_card(arquivo)
    texto = "\n".join(textos_do_post(js))
    baixo = texto.lower()
    achadas = [p for p in PROIBIDAS if p in baixo]
    assert not achadas, achadas
    assert not RE_FONTE.search(texto)
    assert not CORRETORAS.search(texto), CORRETORAS.search(texto).group(0)


@pytest.mark.parametrize("card", MONTADOS, ids=[c["id"] for c in MONTADOS])
def test_nenhum_numero_inventado(card):
    """Todo número vem da linha do calendário ou está declarado com trecho literal/conta que confere."""
    assert g.checar_numeros(card, card["_row"]) == []


@pytest.mark.parametrize("card", MONTADOS, ids=[c["id"] for c in MONTADOS])
def test_ranking_e_superlativo_so_com_fonte_literal(card):
    """'top 10', '3º melhor', 'mais buscado', 'campeão', 'recorde'... só se estiver escrito no calendário,
    nos TEMAS/TERMOS ou no RELATORIO da auditoria (trecho conferido no arquivo)."""
    assert g.checar_afirmacoes(card) == []


def test_checador_pega_ranking_sem_fonte():
    c = dict(MONTADOS[0], texto_gate=MONTADOS[0]["texto_gate"] + "\nFoi o vídeo mais visto do canal, recorde do ano.")
    assert g.checar_afirmacoes(c)


def test_checador_de_numeros_pega_numero_inventado():
    c = dict(MONTADOS[0], texto_gate=MONTADOS[0]["texto_gate"] + " A Selic está em 13,4% e o CDB paga 112%.")
    probs = g.checar_numeros(c, c["_row"])
    assert any("13,4" in p for p in probs) and any("112" in p for p in probs)


def test_pendencias_checar_sao_poucas_e_listadas():
    """[CHECAR] só onde o número depende do dia (Tesouro Selic do dia e decisão do Copom)."""
    com = {c["video_data"] for c in MONTADOS if g.pendencias(c)}
    assert com == {"2026-10-28", "2026-11-05"}


# ---------------------------------------------------------------- gate de qualidade
GATE = g.carregar_gate()


@pytest.mark.skipif(GATE is None, reason="gate_qualidade.py não encontrado (defina IC_GATE)")
def test_gate_passa_em_todos_os_cards():
    reprovados = []
    for c in MONTADOS:
        r = g.rodar_gate(GATE, c)
        if r["codigo_saida"] == 2:
            motivos = "; ".join(f'{p["codigo"]}: {p["mensagem"]} ("{p.get("trecho", "")}")'
                                for p in r["problemas"] if p["nivel"] == "BLOQUEANTE")
            reprovados.append(f'{c["arquivo"]} -> {motivos}')
    assert not reprovados, "\n" + "\n".join(reprovados)


@pytest.mark.skipif(GATE is None, reason="gate_qualidade.py não encontrado (defina IC_GATE)")
def test_gate_sem_aviso_de_conteudo():
    """Avisos aceitos: DADOS_VELHOS (tabelas do gate mais velhas que a data do card) e o título
    'Perfil de investidor' do Short de 16/11, que o gate conta como expressão de IA (vem do calendário)."""
    inesperados = []
    for c in MONTADOS:
        for p in g.rodar_gate(GATE, c)["problemas"]:
            if p["codigo"] == "DADOS_VELHOS":
                continue
            if p["codigo"] == "PADRAO_IA" and c["video_data"] == "2026-11-16" and "perfil de investidor" in p["trecho"] \
                    and "descubra" not in p["trecho"]:
                continue
            inesperados.append(f'{c["arquivo"]}: {p["codigo"]} {p.get("trecho", "")}')
    assert not inesperados, inesperados


@pytest.mark.skipif(GATE is None, reason="gate_qualidade.py não encontrado (defina IC_GATE)")
def test_gate_pela_linha_de_comando_da_o_mesmo_resultado():
    """O gate aceita texto solto pelo stdin; o import usado na esteira tem de dar o mesmo veredito."""
    c = next(c for c in MONTADOS if c["video_data"] == "2026-10-19" and c["rede"] == "x")
    p = subprocess.run([sys.executable, GATE.__file__, "-", "--titulo", c["video_titulo"], "--data",
                        c["data_publicacao"], "--json"], input=c["texto_gate"], capture_output=True, text=True)
    assert json.loads(p.stdout)["resultado"] == g.rodar_gate(GATE, c)["resultado"]
