"""Testes do OUTLIER → ENCAIXE (pytest, sem rede)."""
import json
from datetime import date, timedelta

import pytest

from dados_teste import AGORA, HOJE, TROCAS_ORIGINAL, GERADOR_FALHA, escrever, iso, montar_calendario, pares, video

import comum as c
import coletar
import canais_aprovados as ca
import descobrir_canais as dc
import detectar
import diagnosticar as dg
import encaixar
import entregar
import propor


# ------------------------------------------------------------------------------------------------ nicho
@pytest.mark.parametrize("titulo, desc, esperado", [
    ("MXRF11 reduziu o rendimento", "abra seu cartão de crédito no link", ("dentro", "FII")),
    ("Como sair das dívidas em 2026", "", ("fora", "dívida")),
    ("O rotativo do cartão subiu", "", ("fora", "cartão")),
    ("6 dicas para economizar e juntar dinheiro", "", ("fora", "finanças pessoais básicas")),
    ("LULA NÃO É FAVORITO", "", ("fora", "política")),
    ("O Brasil pode dar calote? O risco da dívida pública", "", ("dentro", "Tesouro e renda fixa")),
    ("Bitcoin vai a 200 mil?", "", ("fora", "cripto puro")),
    ("Viva de Renda está ao vivo!", "", ("fora", "live")),
    ("Quanto ganha o dono de uma lotérica?", "", ("fora", "finanças pessoais básicas")),
])
def test_classificar_nicho(cfg, titulo, desc, esperado):
    assert c.classificar_nicho(titulo, desc, cfg["nichos"]) == esperado


# ------------------------------------------------------------------------------------------------ detecção
def test_detecta_fii_filtra_divida_e_ruido(cfg):
    r = detectar.detectar(cfg, agora=AGORA)
    ids = [o["video_id"] for o in r["outliers"]]
    assert set(ids) == {"fiiOUT00001", "newsOUT0001"}
    fii = next(o for o in r["outliers"] if o["video_id"] == "fiiOUT00001")
    assert fii["nicho"] == "FII" and fii["multiplo"] >= 10 and fii["n_comparacao"] == 12 and fii["base"] == "curva"
    motivos = {d["video_id"]: d["motivo"] for d in r["descartes"]}
    assert motivos["divOUT00001"] == "fora do nicho: dívida"
    assert motivos["novoOUT0001"].startswith("histórico curto: 4")
    assert "mínimo 3000" in motivos["miniOUT0001"]


def test_mesma_idade_pelo_historico_interpolado(cfg):
    """Com observações que cercam a idade do outlier, a comparação é exata (base 'histórico')."""
    snap = {"canais": [{"nome": "X", "channel_id": "UCx", "inscritos": 50_000, "videos": [
        video("alvo", "Tesouro IPCA+ a 7%: a conta", 24, 6000)] + [
        video(f"p{i}", f"FII {i}", 200 + i, 50_000, obs=[[iso(AGORA - timedelta(hours=200 + i - 12)), 500],
                                                         [iso(AGORA - timedelta(hours=200 + i - 36)), 1500],
                                                         [iso(AGORA), 50_000]]) for i in range(10)]}]}
    ach, _ = detectar.detectar_snapshot(snap, cfg, AGORA)
    assert len(ach) == 1 and ach[0]["base"] == "histórico"
    assert ach[0]["mediana_mesma_idade"] == 1000 and ach[0]["multiplo"] == 6.0


def test_curva_nao_usa_video_mais_novo_que_a_idade(cfg):
    v = video("novo", "x", 5, 100)
    assert detectar.views_na_idade(v, 24, AGORA, 72) is None


def test_shorts_comparam_com_shorts(cfg):
    snap = {"canais": [{"nome": "X", "channel_id": "UCx", "inscritos": 50_000, "videos": [
        video("alvo", "FII em 40 segundos #shorts", 24, 9000, dur=40)] + pares("lg", 12, views=100)}]}
    ach, desc = detectar.detectar_snapshot(snap, cfg, AGORA)
    assert not ach and desc[0]["motivo"].startswith("histórico curto: 0")


def test_pontuacao_canal_pequeno_10x_pesa_mais_que_grande_2x(cfg):
    p = cfg["deteccao"]
    assert detectar.pontuacao(10, 20_000, p) > detectar.pontuacao(2, 2_000_000, p)
    assert detectar.pontuacao(10, 20_000, p) > detectar.pontuacao(10, 2_000_000, p)
    assert detectar.pontuacao(3, None, p) == round(__import__("math").log2(3), 2)


def test_adaptador_md_do_vault(cfg, raiz):
    md = escrever(raiz / "video-radar-2026-10-04.md", """---
updated: 2026-10-04
---
| # | Score | Comp. | Canal | Título | Dias | Link |
|---|-------|-------|-------|--------|------|------|
| 1 | **12.2x** | 79 | Tiago Reis | SNEL11 capta R$ 1 bilhão: o que muda no fundo? | 2d | https://youtu.be/xvIivgulpGk |
| 2 | **28.2x** | 80 | Canal A | LULA NÃO É FAVORITO | 1d | https://youtu.be/aaaaaaaaaaa |
| 3 | **9.0x** | 70 | Canal B | PETROBRAS ACHA PETRÓLEO \\| Entenda | 13d | https://youtu.be/bbbbbbbbbbb |
| 4 | **2.0x** | 70 | Canal C | FII qualquer | 1d | https://youtu.be/ccccccccccc |
""")
    r = detectar.detectar(cfg, str(md), AGORA)
    assert [o["video_id"] for o in r["outliers"]] == ["xvIivgulpGk"]
    assert r["outliers"][0]["base"].startswith("aproximação")
    assert {d["video_id"]: d["motivo"] for d in r["descartes"]}["aaaaaaaaaaa"] == "fora do nicho: política"


def test_sem_entrada_nao_quebra(cfg, raiz):
    r = detectar.detectar(cfg, str(raiz / "nao-existe.json"), AGORA)
    assert r["outliers"] == [] and r["erro"]


# ------------------------------------------------------------------------------------------------ diagnóstico
def test_diagnostico_acha_video_parecido_do_denis(cfg):
    o = next(x for x in detectar.detectar(cfg, agora=AGORA)["outliers"] if x["video_id"] == "fiiOUT00001")
    d = dg.diagnosticar(o, dg.carregar_denis(cfg), cfg, AGORA)
    par = d["parecidos_no_canal"]
    assert par and par[0]["video_id"] == "XOqLAz3dkV4"
    assert par[0]["views_intencionais"] == 5200 and par[0]["inscritos"] == 410
    assert d["tema"]["tickers"] == ["MXRF11"] and not d["timing"]["quente"]
    assert any("tema de FII com MXRF11" in x for x in d["por_que_estourou"])


def test_noticia_quente_e_data_de_evento(cfg):
    o = {"titulo": "Copom corta a Selic hoje", "descricao": "", "publicado": iso(AGORA - timedelta(hours=60))}
    assert not dg.timing(o, cfg, AGORA)["quente"]                          # 60 h: passou do prazo de 48 h
    o["data_evento"] = iso(AGORA - timedelta(hours=5))
    t = dg.timing(o, cfg, AGORA)
    assert t["quente"] and t["evento"] == "copom"


# ------------------------------------------------------------------------------------------------ proposta e encaixe
def test_proposta_fii_troca_a_menor_vaga_fora_de_serie_e_copom(cfg):
    r = propor.propor(cfg, agora=AGORA, hoje=HOJE, usar_modelo=False)
    p = next(x for x in r["propostas"] if x["video_id"] == "fiiOUT00001")
    e = p["encaixe"]
    assert e["tipo"] == "troca" and e["data"] == "2026-10-20" and e["sai"] == "Dividendos mensais: o calendário"
    assert len(p["titulos"]) == 3 and all(len(t) <= 60 for t in p["titulos"])
    assert e["entra"] == p["titulos"][0]
    assert "Ampliar, não contradizer" in p["angulo"] and "MXRF11" in p["angulo"]
    assert p["dado_chave"]["fonte_primaria"]
    assert p["linha_resumo"] == ("🔥 Outlier: MXRF11 reduziu o rendimento: a conta do cotista (Canal FII Pequeno, "
                                 "13.4x) → proposta: trocar o de 20/10")


def test_noticia_quente_vira_short_rapido(cfg):
    r = propor.propor(cfg, agora=AGORA, hoje=HOJE, usar_modelo=False)
    p = next(x for x in r["propostas"] if x["video_id"] == "newsOUT0001")
    assert p["encaixe"]["tipo"] == "short_rapido"
    assert p["linha_resumo"].endswith("→ Short rápido")
    assert r["propostas"][0]["video_id"] == "newsOUT0001"            # maior pontuação primeiro


def test_encaixe_nunca_toca_serie_nem_copom(cfg, raiz):
    so_protegidas = [("2026-10-13", "longo", "Ep.", "Ep. 1", "série de renda mensal", 0.1),
                     ("2026-10-15", "longo", "Tesouro Direto antes do Copom", "", "Copom (versão pré)", 0.2),
                     ("2026-10-16", "longo", "Copom hoje", "", "v2", 0.3),
                     ("2026-10-21", "short", "Short do Ep. 2", "Ep. 2 (Short)", "série", 0.1)]
    linhas = [{"data": d, "formato": f, "titulo": t, "serie_ep": ep, "origem": o, "inscritos_esperados": str(e)}
              for d, f, t, ep, o, e in so_protegidas]
    for fmt in ("longo", "short"):
        assert propor.escolher_vaga(linhas, fmt, HOJE) is None
    montar_calendario(raiz, so_protegidas)
    r = propor.propor(cfg, agora=AGORA, hoje=HOJE, usar_modelo=False)
    assert all(p["encaixe"]["tipo"] in ("sem_vaga", "short_rapido", "ideia") for p in r["propostas"])


def test_vaga_ja_trocada_por_outlier_nao_e_escolhida_de_novo(cfg):
    linhas = [{"data": "2026-10-20", "formato": "longo", "titulo": "A", "serie_ep": "", "origem": "",
               "inscritos_esperados": "1", "trocas_aplicadas": "T18 T19"},
              {"data": "2026-10-22", "formato": "longo", "titulo": "B", "serie_ep": "", "origem": "",
               "inscritos_esperados": "9"}]
    trocas = [{"id": "T18", "proposta": "OUT-x"}, {"id": "T19", "proposta": "OUT-x"}]
    assert propor.escolher_vaga(linhas, "longo", HOJE, 3, trocas)["titulo"] == "B"


def test_titulos_passam_no_gate_ou_na_checagem_minima(cfg):
    gate = c.importar_gate(cfg)
    o = {"nicho": "ações", "titulo": "Vale a pena comprar BBAS3?"}
    diag = {"tema": {"tickers": ["BBAS3"], "entidades": []}, "angulo": {"tipo": "pergunta"}}
    ts, _ = propor.titulos(o, diag, gate)
    assert len(ts) == 3
    for t in ts:
        assert len(t) <= 60 and propor.titulo_passa(t, gate)[0]
        assert "vale a pena" not in t.lower()
    assert not propor.titulo_passa("Vale a pena comprar BBAS3 agora?", gate)[0]
    assert not propor.titulo_passa("x" * 61, gate)[0]


def test_card_marca_rascunho_e_id_do_video(cfg):
    r = propor.propor(cfg, agora=AGORA, hoje=HOJE, usar_modelo=False)
    nome, desc = propor.card(r["propostas"][1])
    assert nome.startswith("🔥 Outlier:")
    assert "RASCUNHO" in desc and "video_id: fiiOUT00001" in desc and "encaixar.py aprovar OUT-fiiOUT00001" in desc
    assert "MXRF11: o rendimento caiu?" in desc                       # o parecido do canal aparece no card


def test_main_grava_saida_e_arquivo(cfg, raiz, monkeypatch):
    p = raiz / "cfg.json"
    p.write_text(json.dumps(cfg, ensure_ascii=False))
    assert propor.main(["--config", str(p), "--agora", "2026-10-05T11:00:00+00:00", "--sem-modelo"]) == 0
    r = json.loads((raiz / "saida" / "propostas.json").read_text())
    assert len(r["propostas"]) == 2 and (raiz / "saida" / "propostas.md").is_file()
    assert set(json.loads((raiz / "estado" / "propostas.json").read_text())) == {"OUT-fiiOUT00001", "OUT-newsOUT0001"}


# ------------------------------------------------------------------------------------------------ Trello
def _gerar(cfg, raiz):
    r = propor.propor(cfg, agora=AGORA, hoje=HOJE, usar_modelo=False)
    c.gravar_json(raiz / "saida" / "propostas.json", r)
    arq = {p["id"]: p for p in r["propostas"]}
    c.gravar_json(raiz / "estado" / "propostas.json", arq)
    return r


def test_entregar_dry_run_nao_chama_a_rede(cfg, raiz):
    r = _gerar(cfg, raiz)
    saida = []
    res = entregar.entregar(r, cfg, env={}, dry_run=True, saida=saida.append)
    assert res["dry_run"] == 2 and "[dry-run: nada enviado" in saida[-1]
    assert not (raiz / "estado" / "cards.json").exists()


class TrelloFalso:
    def __init__(self, existentes=""):
        self.chamadas, self.existentes = [], existentes

    def __call__(self, metodo, url, dados=None):
        self.chamadas.append((metodo, url, dados))
        if "/lists/REF/board" in url:
            return {"id": "BOARD"}
        if "/boards/BOARD/lists" in url:
            return [{"id": "L0", "name": "ENTRADA"}, {"id": "LIDEIAS", "name": "💡 Ideias"}]
        if "/lists/LIDEIAS/cards" in url:
            return [{"desc": self.existentes}]
        if metodo == "POST":
            return {"id": "C1", "shortUrl": "https://trello.com/c/x"}
        raise AssertionError(url)


def test_entregar_acha_ideias_pelo_nome_e_nao_duplica(cfg, raiz):
    r = _gerar(cfg, raiz)
    cfg["trello"]["lista_referencia_id"] = "REF"
    env = {"TRELLO_KEY": "k" * 32, "TRELLO_TOKEN": "t" * 64}
    tr = TrelloFalso(existentes="video_id: newsOUT0001")
    res = entregar.entregar(r, cfg, env=env, transporte=tr, saida=lambda *_: None)
    posts = [x for x in tr.chamadas if x[0] == "POST"]
    assert len(posts) == 1 and b"idList=LIDEIAS" in posts[0][2] and b"fiiOUT00001" in posts[0][2]
    assert res["pulados"] == 1
    tr2 = TrelloFalso()
    res2 = entregar.entregar(r, cfg, env=env, transporte=tr2, saida=lambda *_: None)
    assert not [x for x in tr2.chamadas if x[0] == "POST"] and res2["pulados"] == 2


def test_entregar_usa_lista_do_ambiente_e_esconde_token(cfg, raiz):
    r = _gerar(cfg, raiz)
    env = {"TRELLO_KEY": "chave-secreta", "TRELLO_TOKEN": "token-secreto", "TRELLO_LIST_IDEIAS": "LENV"}

    def falha(m, u, d=None):
        raise OSError(f"HTTP 500 em {u}")
    with pytest.raises(RuntimeError) as e:
        entregar.entregar(r, cfg, env=env, transporte=falha, saida=lambda *_: None)
    assert "token-secreto" not in str(e.value) and "chave-secreta" not in str(e.value) and "LENV" in str(e.value)


# ------------------------------------------------------------------------------------------------ troca por comando
def test_aprovar_dry_run_nao_grava_nem_regenera(cfg, raiz):
    _gerar(cfg, raiz)
    out = []
    assert encaixar.aprovar("OUT-fiiOUT00001", cfg, dry_run=True, agora=AGORA, saida=out.append) == 0
    assert (raiz / "pautas-canal" / "trocas.json").read_text() == TROCAS_ORIGINAL
    assert not (raiz / "pautas-canal" / "gerado.txt").exists() and not (raiz / "estado" / "historico_trocas.jsonl").exists()
    assert '"op": "titulo"' in out[0]


def test_aprovar_grava_troca_regenera_e_desfazer_volta(cfg, raiz):
    _gerar(cfg, raiz)
    out = []
    assert encaixar.aprovar("OUT-fiiOUT00001", cfg, quem="Denis", agora=AGORA, saida=out.append) == 0
    texto = (raiz / "pautas-canal" / "trocas.json").read_text()
    assert texto.startswith(TROCAS_ORIGINAL.rsplit("\n  ]", 1)[0])           # o resto do arquivo não foi reformatado
    trocas = json.loads(texto)["trocas"]
    t1, t2 = trocas[-2:]
    assert (t1["id"], t2["id"]) == ("T02", "T03")
    assert t1["op"] == "titulo" and t1["pauta"] == {"data": "2026-10-20", "formato": "longo",
                                                    "titulo": "Dividendos mensais: o calendário"}
    for k in ("data", "sai", "entra", "motivo", "aprovado_por", "quando"):
        assert t1[k]
    assert t1["aprovado_por"] == "Denis" and "Ampliar" in t1["motivo"]
    assert t2["op"] == "edita" and t2["pauta"]["titulo"] == t1["novo"] and t2["campos"]["angulo"].startswith("RASCUNHO")
    assert (raiz / "pautas-canal" / "gerado.txt").read_text() == "3"
    assert encaixar.aprovar("OUT-fiiOUT00001", cfg, agora=AGORA, saida=out.append) == 2          # não aprova 2 vezes
    assert encaixar.desfazer("OUT-fiiOUT00001", cfg, agora=AGORA, saida=out.append) == 0
    assert (raiz / "pautas-canal" / "trocas.json").read_text() == TROCAS_ORIGINAL
    assert (raiz / "pautas-canal" / "gerado.txt").read_text() == "1"
    hist = [json.loads(l) for l in (raiz / "estado" / "historico_trocas.jsonl").read_text().splitlines()]
    assert [h["acao"] for h in hist] == ["aprovar", "desfazer"] and hist[0]["quem"] == "Denis"


def test_gerador_falha_e_trocas_volta(cfg, raiz):
    _gerar(cfg, raiz)
    escrever(raiz / "pautas-canal" / "calendario_v3.py", GERADOR_FALHA)
    out = []
    assert encaixar.aprovar("OUT-fiiOUT00001", cfg, agora=AGORA, saida=out.append) == 1
    assert (raiz / "pautas-canal" / "trocas.json").read_text() == TROCAS_ORIGINAL
    assert "voltou como estava" in out[-1]


def test_aprovar_recusa_short_rapido_e_vaga_sumida(cfg, raiz):
    _gerar(cfg, raiz)
    out = []
    assert encaixar.aprovar("OUT-newsOUT0001", cfg, agora=AGORA, saida=out.append) == 2
    assert "não é troca" in out[-1]
    montar_calendario(raiz, [("2026-10-22", "longo", "Outra", "", "v2", 3.0)])
    assert encaixar.aprovar("OUT-fiiOUT00001", cfg, agora=AGORA, saida=out.append) == 2
    assert "não está mais no CALENDARIO.csv" in out[-1]


def test_aprovar_cria_trocas_json_se_nao_existir(cfg, raiz):
    _gerar(cfg, raiz)
    (raiz / "pautas-canal" / "trocas.json").unlink()
    assert encaixar.aprovar("OUT-fiiOUT00001", cfg, agora=AGORA, saida=lambda *_: None) == 0
    assert [t["id"] for t in json.loads((raiz / "pautas-canal" / "trocas.json").read_text())["trocas"]] == ["T01", "T02"]


# ------------------------------------------------------------------------------------------------ coleta (cota)
class YTFalso:
    def __init__(self, n_videos=30):
        self.urls, self.n = [], n_videos

    def __call__(self, url):
        self.urls.append(url)
        if "/channels?" in url:
            ids = url.split("id=")[1].split("&")[0].split("%2C")
            return {"items": [{"id": i, "statistics": {"subscriberCount": "12345"}} for i in ids]}
        if "/playlistItems?" in url:
            pl = url.split("playlistId=")[1].split("&")[0]
            return {"items": [{"snippet": {"title": f"FII {pl} {k}", "description": ""},
                               "contentDetails": {"videoId": f"{pl}-{k}",
                                                  "videoPublishedAt": iso(AGORA - timedelta(days=k))}}
                              for k in range(self.n)]}
        if "/videos?" in url:
            ids = url.split("id=")[1].split("&")[0].split("%2C")
            return {"items": [{"id": i, "statistics": {"viewCount": "1000"}, "contentDetails": {"duration": "PT10M"}}
                              for i in ids]}
        raise AssertionError(url)


def test_coleta_nunca_usa_search_e_conta_unidades(cfg):
    canais = [{"nome": f"C{i}", "channel_id": f"UC{i:022d}"} for i in range(80)]
    tr = YTFalso()
    yt = c.YouTube("CHAVE", tr)
    snap, hist = coletar.coletar(cfg, yt, canais, agora=AGORA)
    assert not any("/search?" in u for u in tr.urls)
    assert yt.chamadas == {"channels": 2, "playlistItems": 80, "videos": 48} and yt.unidades == 130
    assert len(snap["canais"]) == 80 and snap["canais"][0]["inscritos"] == 12345
    tr2 = YTFalso()
    yt2 = c.YouTube("CHAVE", tr2)
    coletar.coletar(cfg, yt2, canais, agora=AGORA + timedelta(hours=6), historico=hist)
    assert yt2.chamadas["videos"] == 23 and yt2.unidades == 105      # só os de até 14 dias (14 por canal)
    assert len(hist["videos"]["UU0000000000000000000000-0"]["obs"]) == 2
    assert coletar.custo_estimado(80, 30, 100) == {"primeira_rodada": 130, "rodada_normal": 84}


def test_canais_ativos_ignora_desativado_e_id_invalido(raiz):
    p = escrever(raiz / "ch.json", json.dumps({"channels": [
        {"name": "A", "id": "UC" + "a" * 22}, {"name": "B", "id": "@handle"},
        {"name": "C", "id": "UC" + "c" * 22, "disabled": True}]}))
    assert [x["nome"] for x in coletar.canais_ativos(p)] == ["A"]


# ------------------------------------------------------------------------------------------------ descoberta e aprovação de canais
class DescobertaFalsa:
    def __call__(self, url):
        if "/search?" in url:
            return {"items": [{"snippet": {"channelId": "UC" + "n" * 22}}, {"snippet": {"channelId": "UC" + "d" * 22}},
                              {"snippet": {"channelId": "UC" + "u" * 22}}]}
        if "/channels?" in url:
            return {"items": [
                {"id": "UC" + "n" * 22, "snippet": {"title": "Renda com FII", "description": "fundos imobiliários",
                                                    "country": "BR"}, "statistics": {"subscriberCount": "12000"}},
                {"id": "UC" + "d" * 22, "snippet": {"title": "Saia das Dívidas", "description": ""},
                 "statistics": {"subscriberCount": "90000"}},
                {"id": "UC" + "u" * 22, "snippet": {"title": "US dividends", "description": "dividend", "country": "US"},
                 "statistics": {"subscriberCount": "90000"}},
                {"id": "UC" + "p" * 22, "snippet": {"title": "Primo Rico"}, "statistics": {"subscriberCount": "9000000"}}]}
        raise AssertionError(url)


def test_descoberta_junta_e_preserva_aprovado(cfg):
    existentes = [{"nome": "Primo Rico", "channel_id": "UC" + "p" * 22, "inscritos": "a conferir",
                   "faixa": "grande (estimada)", "nicho": "investimento geral", "link": "", "aprovado": "sim",
                   "fonte_da_descoberta": "radar atual"}]
    yt = c.YouTube("CHAVE", DescobertaFalsa())
    linhas, novos = dc.descobrir(cfg, yt, ["trxf11", "lci e lca"], [], existentes, agora=AGORA)
    por_id = {r["channel_id"]: r for r in linhas}
    assert novos == 1 and set(por_id) == {"UC" + "p" * 22, "UC" + "n" * 22}
    assert por_id["UC" + "p" * 22]["aprovado"] == "sim" and por_id["UC" + "p" * 22]["inscritos"] == "9000000"
    assert por_id["UC" + "p" * 22]["faixa"] == "grande" and "conferido na API" in por_id["UC" + "p" * 22]["fonte_da_descoberta"]
    n = por_id["UC" + "n" * 22]
    assert n["faixa"] == "pequeno" and n["aprovado"] == "" and "busca API: trxf11" in n["fonte_da_descoberta"]
    assert yt.chamadas["search"] == 2 and yt.unidades == 201


def test_canais_aprovados_gera_json_com_backup_de_chaves(cfg):
    linhas = [{"nome": "A", "channel_id": "UC" + "a" * 22, "aprovado": "sim", "faixa": "pequeno (estimada)",
               "nicho": "FII", "inscritos": "12000"},
              {"nome": "B", "channel_id": "", "aprovado": "Sim", "faixa": "médio", "nicho": "FII", "inscritos": ""},
              {"nome": "C", "channel_id": "UC" + "c" * 22, "aprovado": "não", "faixa": "", "nicho": "", "inscritos": ""}]
    atual = {"outlier_multiplier": 4.0, "channels": [{"name": "C", "id": "UC" + "c" * 22}], "desativados": []}
    novo, res = ca.gerar(linhas, atual)
    assert [ch["name"] for ch in novo["channels"]] == ["A"] and novo["channels"][0]["inscritos"] == 12000
    assert novo["outlier_multiplier"] == 4.0 and res["sem_id"] == ["B"] and res["saem"] == ["C"]
    assert novo["desativados"][0]["id"] == "UC" + "c" * 22 and "reprovado" in novo["desativados"][0]["motivo"]


def test_canais_aprovados_dry_run_nao_grava(cfg, raiz, capsys):
    dest = escrever(raiz / "video_radar_channels.json", json.dumps({"channels": []}))
    csvp = raiz / "cand.csv"
    dc.gravar_csv(csvp, [{"nome": "A", "channel_id": "UC" + "a" * 22, "aprovado": "sim", "faixa": "", "nicho": "",
                          "inscritos": "", "link": "", "fonte_da_descoberta": ""}])
    cp = raiz / "cfg.json"
    cp.write_text(json.dumps(cfg))
    assert ca.main(["--config", str(cp), "--csv", str(csvp), "--destino", str(dest), "--dry-run"]) == 0
    assert json.loads(dest.read_text()) == {"channels": []} and not list(raiz.glob("video_radar_channels.json.bak-*"))
    assert ca.main(["--config", str(cp), "--csv", str(csvp), "--destino", str(dest)]) == 0
    assert len(json.loads(dest.read_text())["channels"]) == 1 and list(raiz.glob("video_radar_channels.json.bak-*"))


def test_lista_candidata_do_repositorio():
    linhas = dc.ler_csv(dc.CSV_PADRAO)
    assert 40 <= len(linhas) <= 80
    assert list(linhas[0].keys()) == dc.COLUNAS
    faixas = [r["faixa"].split(" ")[0] for r in linhas]
    assert faixas.count("pequeno") + faixas.count("médio") >= len(linhas) / 2
    assert all(r["aprovado"] == "" for r in linhas)
    nomes = {c.norm(r["nome"]) for r in linhas}
    assert not nomes & {"nath financas", "me poupe!", "berman trader"}           # fora do nicho
