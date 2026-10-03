"""Testes da fila de comentários. Sem rede: a API é a fixture (tests/fixture_api.json, dados inventados)."""
import csv
import json
import re
import sys
from datetime import date
from pathlib import Path

import pytest

AQUI = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AQUI))
import coletar as co  # noqa: E402
import fila as fi  # noqa: E402
import regras as rg  # noqa: E402
import voz as vz  # noqa: E402

FIXTURE = AQUI / "tests" / "fixture_api.json"
HOJE = date(2026, 10, 3)

# Gate de qualidade do blog (repo investir-e-cocar), só por import. Se não estiver nesta máquina, usa as regras locais.
GATE = Path("/home/user/investir-e-cocar/pipeline")
try:
    sys.path.insert(0, str(GATE))
    import gate_qualidade as gq  # noqa: E402
except Exception:  # pragma: no cover
    gq = None


@pytest.fixture(scope="module")
def coleta():
    col = co.Coletor(co.ClienteFixture(FIXTURE), "UCcanalExemplo000000000", hoje=HOJE)
    regs, interrompido = col.coletar()
    return {r["comment_id"]: r for r in regs}, col, interrompido


# ------------------------------------------------------------------------------------------- coleta
def test_sem_resposta_do_canal(coleta):
    regs, _, interrompido = coleta
    assert interrompido == ""
    assert regs["UgxEx01"]["sem_resposta"] == 1                 # ninguém respondeu
    assert regs["UgxEx02"]["sem_resposta"] == 0                 # o canal respondeu dentro da thread
    assert regs["UgxEx07"]["sem_resposta"] == 0                 # resposta do canal só em comments.list (7 respostas)
    assert regs["UgxEx07"]["respostas_total"] == 7
    assert "UgxEx04" not in regs                                # comentário do próprio canal não entra


def test_resposta_de_outro_usuario_nao_conta():
    col = co.Coletor(co.ClienteFixture(FIXTURE), "UCcanalExemplo000000000", hoje=HOJE, respostas_extras=False)
    regs, _ = col.coletar()
    r = {x["comment_id"]: x for x in regs}
    # sem buscar as respostas extras, só vieram 5 respostas de outro usuário: fica como sem resposta
    assert r["UgxEx07"]["sem_resposta"] == 1


def test_guarda_respostas_do_canal(coleta):
    _, col, _ = coleta
    ids = {r["reply_id"] for r in col.respostas_canal}
    assert ids == {"UgxEx02.r1", "UgxEx07.r9"}
    assert all(set(r) == set(co.COLUNAS_RESPOSTAS) for r in col.respostas_canal)


def test_views_28d_e_comentarios_desativados(coleta):
    regs, col, _ = coleta
    assert regs["UgxEx01"]["views_28d"] == 42000
    assert any("comentários indisponíveis" in n for n in col.notas)


def test_sem_analytics_views_vazias():
    cli = co.ClienteFixture(FIXTURE)
    cli.d["analytics_negado"] = True
    regs, _ = co.Coletor(cli, "UCcanalExemplo000000000", hoje=HOJE).coletar()
    assert all(r["views_28d"] == "" for r in regs)


def test_limite_de_cota_para_a_coleta():
    cli = co.ClienteFixture(FIXTURE)
    regs, interrompido = co.Coletor(cli, "UCcanalExemplo000000000", max_unidades=4, hoje=HOJE).coletar()
    assert interrompido.startswith("limite")
    assert cli.unidades_data <= 4


def test_paginacao_e_parametros(coleta):
    _, col, _ = coleta
    ct = [p for r, p in col.c.chamadas if r == "commentThreads" and p["videoId"] == "vidExemplo01"]
    assert len(ct) == 2 and ct[1]["pageToken"] == "1"
    assert all(p["order"] == "time" and p["maxResults"] == 100 and p["part"] == "snippet,replies" for p in ct)


def test_estimativa_de_cota():
    e = co.estimar([0, 50, 250, 1000])
    assert e["playlistItems"] == 1 and e["commentThreads"] == 1 + 1 + 2 + 5
    assert e["total"] == e["canal"] + e["playlistItems"] + e["commentThreads"] + e["comments"]


# ------------------------------------------------------------------------------------------- regras
@pytest.mark.parametrize("texto", ["Quanto rende 1000 reais no CDB?", "como faço pra declarar", "Vale a pena a LCI",
                                   "Devo vender agora", "pode abrir conta com 16 anos", "Onde invisto minha reserva",
                                   "gostaria de saber qual a taxa"])
def test_detecta_pergunta(texto):
    assert rg.eh_pergunta(texto)


@pytest.mark.parametrize("texto", ["Ótimo vídeo, valeu!", "Top demais japa", "kkkkkk"])
def test_nao_e_pergunta(texto):
    assert not rg.eh_pergunta(texto)


@pytest.mark.parametrize("texto", [
    "Me chama no WhatsApp 11 91234-5678",
    "Comecei com US$ 500 e saquei US$ 19.000 em duas semanas, tudo graças à coach Fulana.",
    "Incrível ver outro investindo com a Sra. Fulana Tal, meu portfólio cresceu",
    "Ofereço mentoria gratuita, chama no privado",
    "Alguém pode me orientar sobre a abordagem certa para investir e obter um bom lucro em cripto?",
    "Ela está principalmente no Telegram 👇"])
def test_detecta_spam(texto):
    assert rg.eh_spam(texto)
    assert rg.nota_risco(texto) == "spam/golpe"


@pytest.mark.parametrize("texto", [
    "Tentei falar com eles pelo WhatsApp do SAC e ninguém responde",       # reclamação, não spam
    "Tem um grupo no Telegram pedindo depósito de 400, isso é golpe?",      # pergunta sobre golpe, merece resposta
    "nem Sr Carlos acredita kkkk",                                          # personagem do vídeo
    "esses caras só querem vender curso de mentoria"])
def test_nao_e_spam(texto):
    assert not rg.eh_spam(texto)


def test_riscos():
    assert "pede_recomendacao" in rg.riscos("Devo comprar ABCD3 agora?")
    assert "pede_recomendacao" in rg.riscos("qual a melhor ação pra dividendos?")
    assert "tributario" in rg.riscos("Preciso declarar no imposto de renda?")
    assert "tributario" in rg.riscos("E o IR disso?")
    assert "tributario" not in rg.riscos("se eu ir dobrando todo dia")       # "ir" verbo
    assert "reclamacao" in rg.riscos("Vídeo péssimo, só enrolação")
    assert rg.riscos("Como funciona a liquidez diária?") == []


# ------------------------------------------------------------------------------------------- fila
def test_ordem_de_prioridade():
    p = lambda likes, views, pub: fi.prioridade(likes, views, "2025-01-01", pub, HOJE)  # noqa: E731
    assert p(40, 1000, "2026-09-01") > p(2, 1000, "2026-09-01")              # mais likes, mais prioridade
    assert p(5, 30000, "2026-09-01") > p(5, 10, "2026-09-01")                # vídeo que ainda recebe views
    assert p(5, 1000, "2026-09-30") > p(5, 1000, "2023-01-01")               # comentário recente
    # sem views de 28 dias, usa a data do vídeo
    assert (fi.prioridade(5, "", "2026-09-01", "2026-09-10", HOJE) > fi.prioridade(5, "", "2019-01-01", "2026-09-10", HOJE))


def test_fila_da_fixture():
    with open(AQUI / "fila_exemplo.csv", newline="", encoding="utf-8") as f:
        linhas = list(csv.DictReader(f))
    assert list(linhas[0]) == fi.COLUNAS
    ids = [l["comment_id"] for l in linhas]
    assert "UgxEx02" not in ids and "UgxEx07" not in ids and "UgxEx05" not in ids   # respondidas e não-pergunta
    nao_spam = [float(l["prioridade"]) for l in linhas if l["status"] != "ocultar"]
    assert nao_spam == sorted(nao_spam, reverse=True)
    assert linhas[-1]["status"] == "ocultar" and linhas[-1]["rascunho"] == ""        # spam no fim, sem resposta
    l1 = next(l for l in linhas if l["comment_id"] == "UgxEx01")
    assert l1["link"] == "https://www.youtube.com/watch?v=vidExemplo01&lc=UgxEx01" and l1["status"] == "rascunho"
    assert next(l for l in linhas if l["comment_id"] == "UgxEx10")["status"] == "precisa_rascunho"


def test_fila_mantem_decisao_do_denis(tmp_path):
    threads = [{"video_id": "v", "video_titulo": "t", "video_publicado": "2026-01-01", "views_28d": 10,
                "comment_id": "c1", "autor": "", "publicado_em": "2026-09-01", "likes": 3, "texto": "Como funciona?",
                "sem_resposta": 1, "eh_pergunta": 1}]
    anterior = {"c1": {"status": "editado", "rascunho": "texto do Denis"}}
    [l] = fi.montar(threads, {"c1": "rascunho novo"}, HOJE, anterior)
    assert (l["status"], l["rascunho"]) == ("editado", "texto do Denis")


# ------------------------------------------------------------------------------------------- rascunhos
def rascunhos():
    return json.loads((AQUI / "rascunhos.json").read_text(encoding="utf-8"))


PROMESSA = re.compile(r"(retorno|lucro|rendimento|ganho) (garantid|cert)|garant\w+ (de )?(lucro|retorno)|vai (te )?render|"
                      r"vai (subir|dobrar|valorizar|disparar|explodir)|sem risco|fica(r)? rico|enriquecer r[aá]pido", re.I)
COMPRA_VENDA = re.compile(r"\b(compr\w*|vend\w*)\b", re.I)


def test_rascunhos_quantidade_e_formato():
    r = rascunhos()
    assert len(r) >= 30
    for cid, t in r.items():
        assert re.fullmatch(r"Ug[\w-]+", cid)
        frases = [f for f in re.split(r"(?<=[.!?])\s+(?=[A-ZÀ-Ú\"“(])", t) if f.strip()]
        assert 1 <= len(frases) <= 4, (cid, t)
        assert len(t) <= 260, (cid, len(t))
        assert "Taná" not in t.replace("Tanaka", "")


def test_rascunhos_sem_nome_de_autor():
    autores = {"Tanaka Exemplo"}  # a fixture; os dados reais não têm autor no git
    for t in rascunhos().values():
        assert "@" not in t
        assert not any(a in t for a in autores)


def test_rascunhos_sem_corretora_ticker_ou_promessa():
    for cid, t in rascunhos().items():
        assert not rg.INSTITUICAO.search(rg.norm(t)), (cid, t)
        assert not rg.TICKER.search(t), (cid, t)
        assert not (rg.TICKER.search(t) and COMPRA_VENDA.search(t)), (cid, t)
        assert not PROMESSA.search(t), (cid, t)
        assert not re.search(r"\b(compre|venda j[aá]|compra agora)\b", t, re.I), (cid, t)
        if gq:
            assert not gq.RE_CORRETORA.search(t), (cid, t)
            assert not gq.RE_RECOM_TEXTO.search(t), (cid, t)
            assert not gq.RE_TICKER.search(t), (cid, t)


def test_rascunho_so_para_quem_existe_e_nao_e_spam():
    """Todo rascunho aponta para uma pergunta sem resposta da auditoria, e nenhuma é spam."""
    dados = AQUI.parent / "auditoria-canal" / "dados" / "comentarios_top30.csv"
    if not dados.exists():
        pytest.skip("dados da auditoria fora do repositório")
    sem = {t["comment_id"]: t for t in fi.threads_da_auditoria() if t["sem_resposta"] == 1}
    for cid in rascunhos():
        assert cid in sem, cid
        assert not rg.eh_spam(sem[cid]["texto"]), cid


# ------------------------------------------------------------------------------------------- voz
def test_voz_tira_nome_do_comeco():
    assert vz.limpar("Fulano San / Eh pq não rendeu") == "/ Eh pq não rendeu"
    assert vz.limpar("@alguem123 Tem que seguir no aporte ^^") == "Tem que seguir no aporte ^^"
    assert vz.abertura("Fala, Fulano san tudo bem") == "nome de quem comentou + San/chuan"
    assert vz.fechamento("Tem que seguir no aporte ^^") == "^^"


def test_voz_md_tem_bloco_automatico_e_sem_arroba():
    t = (AQUI / "voz_denis.md").read_text(encoding="utf-8")
    assert vz.INI in t and vz.FIM in t
    assert not re.search(r"@[\w.\-]{3,}", t)
