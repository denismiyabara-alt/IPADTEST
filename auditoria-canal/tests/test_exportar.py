"""Testes do exportador com uma API falsa: nada vai para a rede."""
import csv
import json
import sys
import urllib.parse
from datetime import date, datetime, timezone
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import exportar as ex  # noqa: E402

ENV = {"YOUTUBE_API_KEY": "CHAVE-API-SECRETA-111", "YT_CLIENT_ID": "CLIENTE-ID-222",
       "YT_CLIENT_SECRET": "SEGREDO-CLIENTE-333", "YT_REFRESH_TOKEN": "REFRESH-TOKEN-444"}
ACCESS = "ACCESS-TOKEN-555"
CANAL = "UCcanalTeste"


def video_item(i, dur, titulo=None, pub="2025-03-10T21:30:00Z", views=1000, desc="descrição"):
    return {"id": f"v{i}", "snippet": {"title": titulo or f"Vídeo {i}", "publishedAt": pub, "description": desc,
                                       "tags": ["a", "b"], "thumbnails": {"high": {"url": f"https://i/{i}.jpg"}}},
            "contentDetails": {"duration": dur}, "statistics": {"viewCount": str(views), "likeCount": "10",
                                                                 "commentCount": "2"}}


class FakeAPI:
    """Roteia pela URL. `falhas` é uma lista de (trecho_da_url, ErroHTTP) consumida na ordem."""

    def __init__(self, n_videos=120, recusar=("videoThumbnailImpressions", "impressions",
                                               "videoThumbnailImpressionsClickRate", "impressionsClickThroughRate")):
        self.n = n_videos
        self.recusar = set(recusar)
        self.chamadas = []
        self.falhas = []
        self.headers = []
        self.max_lote = 200          # maior lote de IDs que a API "aceita"
        self.aceita_duas = True      # aceita dimensions=video,<outra> com vários vídeos

    def __call__(self, url, data=None, headers=None):
        self.chamadas.append(url)
        self.headers.append(headers or {})
        for i, (trecho, erro) in enumerate(self.falhas):
            if trecho in url:
                del self.falhas[i]
                raise erro
        if url.startswith(ex.URL_TOKEN):
            assert b"REFRESH-TOKEN-444" in data
            return {"access_token": ACCESS, "expires_in": 3600}
        base, _, qs = url.partition("?")
        q = dict(urllib.parse.parse_qsl(qs))
        if base.endswith("/channels"):
            if q.get("mine"):
                assert headers["Authorization"] == "Bearer " + ACCESS
                return {"items": [{"id": CANAL}]}
            assert q["key"] == ENV["YOUTUBE_API_KEY"]
            return {"items": [{"id": CANAL, "snippet": {"title": "Canal", "publishedAt": "2022-05-01T00:00:00Z"},
                               "contentDetails": {"relatedPlaylists": {"uploads": "UUcanalTeste"}},
                               "statistics": {"subscriberCount": "100000"}}]}
        if base.endswith("/playlistItems"):
            pagina = int(q.get("pageToken", "0"))
            ids = list(range(pagina * 50, min(self.n, pagina * 50 + 50)))
            d = {"items": [{"contentDetails": {"videoId": f"v{i}"}} for i in ids]}
            if (pagina + 1) * 50 < self.n:
                d["nextPageToken"] = str(pagina + 1)
            return d
        if base.endswith("/videos"):
            itens = []
            for vid in q["id"].split(","):
                i = int(vid[1:])
                dur = "PT45S" if i % 3 == 0 else "PT12M3S"
                itens.append(video_item(i, dur, views=10000 - i))
            return {"items": itens}
        if base.endswith("/commentThreads"):
            if q["videoId"] == "v1":
                raise ex.ErroHTTP(403, "commentsDisabled", "comments disabled")
            return {"items": [{"snippet": {"totalReplyCount": 1, "topLevelComment": {
                "id": "c-" + q["videoId"], "snippet": {"authorChannelId": {"value": "UCautor"},
                                                       "authorDisplayName": "Fulano de Tal",
                                                       "textOriginal": "Como faço?", "likeCount": 3,
                                                       "publishedAt": "2026-01-01T00:00:00Z"}}},
                "replies": {"comments": [{"id": "r-" + q["videoId"], "snippet": {
                    "authorChannelId": {"value": CANAL}, "authorDisplayName": "Canal", "textOriginal": "Assim.",
                    "likeCount": 1, "publishedAt": "2026-01-02T00:00:00Z"}}]}}]}
        if base == ex.API_ANALYTICS:
            assert headers["Authorization"] == "Bearer " + ACCESS
            assert q["ids"] == "channel==MINE"
            return self.analytics(q)
        raise AssertionError("URL inesperada: " + base)

    def analytics(self, q):
        mets = q["metrics"].split(",")
        for m in mets:
            if m in self.recusar:
                raise ex.ErroHTTP(400, "badRequest", f"Unknown identifier ({m}) given in field parameters.metrics.")
        dims = q.get("dimensions", "").split(",")
        if dims[0] == "month":
            # Como a API real: com a dimensão month, startDate e endDate têm de cair no dia 1.
            for campo in ("startDate", "endDate"):
                if not q.get(campo, "").endswith("-01"):
                    raise ex.ErroHTTP(400, "badRequest", f"Date range ({q.get(campo)}) in field parameters."
                                      f"{'end' if campo == 'endDate' else 'start'}-date does not align to chosen date dimension.")
        cab = [{"name": d} for d in dims] + [{"name": m} for m in mets]
        filtro = q.get("filters", "")
        ids = filtro[len("video=="):].split(",") if filtro.startswith("video==") else []
        if dims[0] == "video":
            # Como a API real: o "top vídeos" com sort=-views não passa de startIndex=200.
            if int(q.get("startIndex", 1)) > 200:
                raise ex.ErroHTTP(400, "badRequest", "The query is not supported.")
            if not ids and "sort" in q:
                fatia = [f"v{i}" for i in range(self.n)][:min(200, int(q.get("maxResults", 200)))]
            else:
                assert ids and "sort" not in q, "consulta por vídeo deve ir em lote de IDs, sem sort"
                if len(ids) > self.max_lote:
                    raise ex.ErroHTTP(400, "badRequest", "The query is not supported.")
                fatia = ids
            if dims == ["video"]:
                rows = [[v] + [100 + k for k in range(len(mets))] for v in fatia]
            else:
                if not self.aceita_duas:
                    raise ex.ErroHTTP(400, "badRequest", "The query is not supported.")
                seg = {"insightTrafficSourceType": [("RELATED_VIDEO", 3, 5), ("YT_SEARCH", 7, 9)],
                       "subscribedStatus": [("SUBSCRIBED", 4, 8), ("UNSUBSCRIBED", 6, 9)]}[dims[1]]
                rows = [[v, a, b, c] for v in fatia for a, b, c in seg]
        elif dims == ["month"]:
            rows = [["2025-05", 10, 20, 3, 1], ["2025-06", 11, 21, 4, 1]] if len(mets) == 4 else \
                   [["2025-05", 10, 7], ["2025-06", 11, 8]]
        elif dims == ["month", "creatorContentType"]:
            rows = [["2025-05", "SHORTS"] + [5] * len(mets), ["2025-05", "VIDEO_ON_DEMAND"] + [5] * len(mets)]
        elif dims == ["day"]:
            rows = [["2026-08-26", 10, 20, 1, 0], ["2026-08-27", 30, 20, 1, 0]] if len(mets) == 4 else \
                   [["2026-08-26", 10, 9], ["2026-08-27", 30, 9]]
        elif dims == ["month", "insightTrafficSourceType"]:
            rows = [["2025-05", "RELATED_VIDEO", 29, 50], ["2025-05", "BROWSE", 71, 90]]
        elif dims == ["insightTrafficSourceDetail"]:
            assert int(q["maxResults"]) <= 25 and q["sort"] == "-views"
            assert "insightTrafficSourceType==YT_SEARCH" in q["filters"]
            if getattr(self, "recusar_termos", False):
                raise ex.ErroHTTP(400, "badRequest", "The query is not supported.")
            alvo = q["filters"].split(";")[0] if q["filters"].startswith("video==") else q["startDate"][:7]
            rows = [[f"termo {k} {alvo}", 100 - k, 200 - k] for k in range(int(q["maxResults"]))]
        elif dims == ["insightTrafficSourceType"]:
            rows = [["RELATED_VIDEO", 3, 5], ["YT_SEARCH", 7, 9]]
        elif dims == ["subscribedStatus"]:
            rows = [["SUBSCRIBED", 4, 8], ["UNSUBSCRIBED", 6, 9]]
        else:
            raise AssertionError(dims)
        return {"columnHeaders": cab, "rows": rows}


def novo(tmp_path, api, hoje=date(2026, 10, 2), **kw):
    logs = []
    cli = ex.Cliente(tmp_path / ".cache", env=dict(ENV), transporte=api, dormir=lambda s: None, pausa=0,
                     log=logs.append)
    exp = ex.Exportador(cli, tmp_path, hoje=hoje, **kw)
    return cli, exp, logs


def ler(p):
    with open(p, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def rodar_tudo(exp):
    exp.canal()
    exp.exportar_videos()
    ids = exp.exportar_analytics_por_video()
    exp.exportar_canal_por_mes()
    exp.exportar_canal_por_dia()
    exp.exportar_trafego_por_mes()
    exp.exportar_por_video(ids)
    exp.exportar_comentarios()
    exp.salvar_estado()
    exp.leiame("completo")


# ------------------------------------------------------------------------------------------------ unidades
def test_formato_short_e_longo():
    antes = datetime(2023, 5, 1, tzinfo=timezone.utc)
    depois = datetime(2025, 5, 1, tzinfo=timezone.utc)
    assert ex.formato(59, antes) == "short"
    assert ex.formato(60, antes) == "short"
    assert ex.formato(120, antes) == "longo"          # 2 min em 2023 não podia ser Short
    assert ex.formato(120, depois) == "short"         # depois de 15/10/2024 o limite é 3 min
    assert ex.formato(180, depois) == "short"
    assert ex.formato(181, depois) == "longo"
    assert ex.formato(900, depois, "Dica rápida #Shorts") == "short"
    assert ex.formato(900, depois, "t", "veja #short") == "short"
    assert ex.formato(900, depois, "#shortstop") == "longo"


def test_duracao():
    assert ex.duracao_s("PT1H2M3S") == 3723
    assert ex.duracao_s("PT45S") == 45
    assert ex.duracao_s("P1DT1S") == 86401
    assert ex.duracao_s(None) == 0


def test_meses():
    assert ex.fim_do_mes(date(2024, 2, 10)) == date(2024, 2, 29)
    assert ex.meses_para_tras(date(2026, 9, 30), 18) == date(2025, 4, 1)


# ------------------------------------------------------------------------------------------------ fluxo
def test_paginacao_playlist_e_videos(tmp_path):
    api = FakeAPI(n_videos=120)
    cli, exp, _ = novo(tmp_path, api)
    exp.canal()
    exp.exportar_videos()
    vs = ler(tmp_path / "videos.csv")
    assert len(vs) == 120
    assert sum("/playlistItems" in u for u in api.chamadas) == 3     # 50 + 50 + 20
    assert sum("/videos?" in u for u in api.chamadas) == 3
    assert cli.unidades_data == 2 + 3 + 3                             # mine + channels + 3 + 3
    v0 = next(v for v in vs if v["id"] == "v0")
    assert v0["formato"] == "short" and v0["duracao_s"] == "45"
    v1 = next(v for v in vs if v["id"] == "v1")
    assert v1["formato"] == "longo"
    assert v1["publicado_em_utc"] == "2025-03-10 21:30:00"
    assert v1["publicado_em_brt"] == "2025-03-10 18:30:00"
    assert v1["dia_semana"] == "segunda" and v1["hora"] == "18"
    assert v1["tags"] == "a|b" and v1["thumbnail_url"] == "https://i/1.jpg"


def _q(u):
    return dict(urllib.parse.parse_qsl(u.split("?")[1]))


def test_api_real_recusa_startindex_201_e_codigo_novo_nao_pagina(tmp_path):
    api = FakeAPI(n_videos=450)
    cli, exp, _ = novo(tmp_path, api)
    # O mock reproduz o bug visto no Mac: top vídeos com sort=-views dá 400 a partir de startIndex=201.
    cli.analytics_tabela(dimensions="video", metrics="views", sort="-views", maxResults=200, startIndex=1)
    with pytest.raises(ex.ErroHTTP) as e:
        cli.analytics_tabela(dimensions="video", metrics="views", sort="-views", maxResults=200, startIndex=201)
    assert e.value.status == 400 and "not supported" in e.value.mensagem
    api.chamadas.clear()
    exp.canal()
    exp.exportar_videos()
    ids = exp.exportar_analytics_por_video()
    assert len(ids) == 450
    an = [_q(u) for u in api.chamadas if u.startswith(ex.API_ANALYTICS)]
    assert an and not any("startIndex" in q or "sort" in q for q in an)


def test_analytics_por_video_em_lotes_de_200_e_metricas_indisponiveis(tmp_path):
    api = FakeAPI(n_videos=450)
    cli, exp, _ = novo(tmp_path, api)
    exp.canal()
    exp.exportar_videos()
    exp.exportar_analytics_por_video()
    principais = [_q(u) for u in api.chamadas if "subscribersGained" in u and u.startswith(ex.API_ANALYTICS)]
    tamanhos = [len(q["filters"][len("video=="):].split(",")) for q in principais]
    assert tamanhos == [200, 200, 50] and all(q["dimensions"] == "video" for q in principais)
    assert principais[0]["filters"].startswith("video==v0,v1,")          # do mais visto ao menos visto
    rs = ler(tmp_path / "analytics_por_video.csv")
    assert len(rs) == 450
    assert rs[0]["engagedViews"] == "101"                 # métrica opcional que a API aceitou
    assert rs[0]["impressions"] == "" and rs[0]["impressionsClickThroughRate"] == ""
    notas = exp.notas["analytics_por_video.csv"]
    assert any("impressions vazia" in n for n in notas)
    assert any("lotes de até 200 IDs" in n for n in notas)
    # métrica recusada não divide o lote: só a sonda de 1 vídeo por nome tentado
    recusadas = [u for u in api.chamadas if "Impressions" in u or "impressions" in u]
    assert len(recusadas) == 4
    exp.leiame("completo")
    leia = (tmp_path / "LEIAME_DADOS.md").read_text(encoding="utf-8")
    assert "impressionsClickThroughRate" in leia and "Colunas vazias" in leia and "lotes de até 200" in leia


def test_lote_recusado_e_dividido_ao_meio(tmp_path):
    api = FakeAPI(n_videos=120)
    api.max_lote = 60
    cli, exp, logs = novo(tmp_path, api)
    exp.canal()
    exp.exportar_videos()
    exp.exportar_analytics_por_video()
    principais = [_q(u) for u in api.chamadas if "subscribersGained" in u and u.startswith(ex.API_ANALYTICS)]
    tamanhos = [len(q["filters"].split(",")) for q in principais]
    assert tamanhos == [120, 60, 60]              # 120 recusado → divide ao meio → 60 passa e segue com 60
    assert len(ler(tmp_path / "analytics_por_video.csv")) == 120
    assert any("lotes de até 60 IDs" in n for n in exp.notas["analytics_por_video.csv"])
    assert any("tentando 60" in l for l in logs)
    # Retomada: nova execução não repete nenhum lote (nem o recusado, cujo 400 ficou no cache).
    exp.salvar_estado()
    api.chamadas.clear()
    cli2, exp2, _ = novo(tmp_path, api)
    exp2.exportar_analytics_por_video()
    assert not any(u.startswith(ex.API_ANALYTICS) for u in api.chamadas)


def test_trafego_e_inscritos_em_lote(tmp_path):
    api = FakeAPI(n_videos=250)
    cli, exp, _ = novo(tmp_path, api)
    exp.canal()
    exp.exportar_videos()
    ids = exp.exportar_analytics_por_video()
    api.chamadas.clear()
    exp.exportar_por_video(ids)
    qs = [_q(u) for u in api.chamadas if u.startswith(ex.API_ANALYTICS)]
    assert [q["dimensions"] for q in qs] == ["video,insightTrafficSourceType"] * 2 + ["video,subscribedStatus"] * 2
    assert all(q["filters"].startswith("video==") and "sort" not in q for q in qs)
    assert len(ler(tmp_path / "trafego_por_video.csv")) == 500
    ins = ler(tmp_path / "inscritos_por_video.csv")
    assert len(ins) == 250 and ins[0] == {"video_id": "v0", "views_inscritos": "4", "views_nao_inscritos": "6",
                                          "minutos_inscritos": "8", "minutos_nao_inscritos": "9"}


def test_fallback_por_video_quando_api_recusa_duas_dimensoes(tmp_path):
    api = FakeAPI(n_videos=5)
    api.aceita_duas = False
    cli, exp, _ = novo(tmp_path, api)
    exp.canal()
    exp.exportar_videos()
    ids = exp.exportar_analytics_por_video()
    api.chamadas.clear()
    exp.exportar_por_video(ids)
    qs = [_q(u) for u in api.chamadas if u.startswith(ex.API_ANALYTICS)]
    duas = [q for q in qs if q["dimensions"].startswith("video,")]
    # 5 → 2 → 1 recusados para cada dimensão; depois 1 consulta por vídeo, filters=video==ID e só a dimensão secundária
    assert [len(q["filters"].split(",")) for q in duas] == [5, 2, 1] * 2
    uma = [q for q in qs if not q["dimensions"].startswith("video")]
    assert len(uma) == 10 and all("," not in q["filters"] for q in uma)
    assert {q["dimensions"] for q in uma} == {"insightTrafficSourceType", "subscribedStatus"}
    assert len(ler(tmp_path / "trafego_por_video.csv")) == 10
    assert len(ler(tmp_path / "inscritos_por_video.csv")) == 5
    assert any("vídeo a vídeo" in n for n in exp.notas["trafego_por_video.csv"])
    assert any("vídeo a vídeo" in n for n in exp.notas["inscritos_por_video.csv"])


def test_so_analytics_pula_o_passo_1(tmp_path, monkeypatch):
    api = FakeAPI(n_videos=8)
    _, exp, _ = novo(tmp_path, api)
    exp.canal()
    exp.exportar_videos()          # simula o passo 1 já feito (videos.csv + cache)
    exp.salvar_estado()
    api.chamadas.clear()
    monkeypatch.setattr(ex.Cliente.__init__, "__defaults__", (None, api, lambda s: None, 0.3, 6, 2.0, None))
    for k, v in ENV.items():
        monkeypatch.setenv(k, v)
    assert ex.main(["--saida", str(tmp_path), "--pausa", "0", "--so-analytics"]) == 0
    assert not any("/playlistItems" in u or "/videos?" in u or "/commentThreads" in u or "/channels" in u
                   for u in api.chamadas)
    assert len(ler(tmp_path / "analytics_por_video.csv")) == 8


def test_impressoes_com_nome_alternativo(tmp_path):
    api = FakeAPI(n_videos=10, recusar=("videoThumbnailImpressions", "videoThumbnailImpressionsClickRate"))
    _, exp, _ = novo(tmp_path, api)
    exp.canal()
    exp.exportar_videos()
    exp.exportar_analytics_por_video()
    rs = ler(tmp_path / "analytics_por_video.csv")
    assert rs[0]["impressions"] == "101" and rs[0]["impressionsClickThroughRate"] == "101"


def test_formato_por_mes_recusado_fica_vazio_com_nota(tmp_path):
    api = FakeAPI(n_videos=5, recusar=("engagedViews",))
    orig = api.analytics

    def sem_formato(q):
        if "creatorContentType" in q.get("dimensions", ""):
            raise ex.ErroHTTP(400, "badRequest", "The query is not supported.")
        return orig(q)
    api.analytics = sem_formato
    _, exp, _ = novo(tmp_path, api)
    exp.exportar_canal_por_mes()
    rs = ler(tmp_path / "canal_por_mes.csv")
    assert [r["mes"] for r in rs] == ["2025-05", "2025-06"]
    assert rs[0]["views_shorts"] == "" and rs[0]["engagedViews"] == ""
    notas = " ".join(exp.notas["canal_por_mes.csv"])
    assert "creatorContentType" in notas and "engagedViews" in notas


def test_canal_por_mes_e_trafego(tmp_path):
    api = FakeAPI(n_videos=5)
    _, exp, _ = novo(tmp_path, api)
    exp.exportar_canal_por_mes()
    exp.exportar_trafego_por_mes()
    m = ler(tmp_path / "canal_por_mes.csv")
    assert m[0]["views_shorts"] == "5" and m[0]["inscritos_ganhos_longos"] == "5" and m[0]["engagedViews"] == "7"
    q = dict(urllib.parse.parse_qsl(next(u for u in api.chamadas if "dimensions=month&" in u).split("?")[1]))
    assert q["startDate"] == "2025-04-01" and q["endDate"] == "2026-09-01"   # 18 meses fechados; month exige dia 1
    t = ler(tmp_path / "trafego_por_mes.csv")
    assert t[0]["origem"] == "BROWSE" and t[0]["pct_views_mes"] == "71.0"
    assert t[1]["origem_pt"].startswith("Vídeos sugeridos")


def test_trafego_por_mes_cai_para_consulta_mes_a_mes(tmp_path):
    api = FakeAPI(n_videos=5)
    orig = api.analytics

    def recusa(q):
        if q.get("dimensions") == "month,insightTrafficSourceType":
            raise ex.ErroHTTP(400, "badRequest", "not supported")
        return orig(q)
    api.analytics = recusa
    _, exp, _ = novo(tmp_path, api, meses=3)
    exp.exportar_trafego_por_mes()
    t = ler(tmp_path / "trafego_por_mes.csv")
    assert sorted({r["mes"] for r in t}) == ["2026-07", "2026-08", "2026-09"]
    assert t[0]["pct_views_mes"] == "70.0"


def test_retry_em_429_e_5xx_com_backoff(tmp_path):
    api = FakeAPI(n_videos=3)
    api.falhas = [("/channels", ex.ErroHTTP(503, "backendError", "x")),
                  ("/channels", ex.ErroHTTP(429, "", "too many")),
                  ("/playlistItems", ex.ErroHTTP(403, "rateLimitExceeded", "slow down"))]
    esperas = []
    cli = ex.Cliente(tmp_path / ".cache", env=dict(ENV), transporte=api, dormir=esperas.append, pausa=0,
                     log=lambda m: None)
    exp = ex.Exportador(cli, tmp_path, hoje=date(2026, 10, 2))
    exp.estado["canal_id"] = CANAL
    exp.canal()
    exp.exportar_videos()
    assert esperas == [2.0, 4.0, 2.0]
    assert len(ler(tmp_path / "videos.csv")) == 3


def test_retry_desiste_e_400_nao_repete(tmp_path):
    api = FakeAPI(n_videos=3)
    api.falhas = [("/channels", ex.ErroHTTP(500, "", "x"))] * 3
    cli = ex.Cliente(tmp_path / ".cache", env=dict(ENV), transporte=api, dormir=lambda s: None, pausa=0,
                     tentativas=3, log=lambda m: None)
    with pytest.raises(ex.ErroHTTP) as e:
        cli.data_api("channels", part="id", id="x")
    assert e.value.status == 500 and len(api.chamadas) == 3
    api.falhas = [("/videos", ex.ErroHTTP(400, "badRequest", "ruim"))]
    for _ in range(2):  # a segunda vem do cache de erro, sem nova chamada
        with pytest.raises(ex.ErroHTTP):
            cli.data_api("videos", part="id", id="x")
    assert sum("/videos" in u for u in api.chamadas) == 1


def test_401_renova_token(tmp_path):
    api = FakeAPI(n_videos=3)
    api.falhas = [(ex.API_ANALYTICS, ex.ErroHTTP(401, "authError", "expired"))]
    cli, exp, _ = novo(tmp_path, api)
    exp.exportar_canal_por_dia()
    assert sum(u.startswith(ex.URL_TOKEN) for u in api.chamadas) == 2


def test_quota_esgotada_e_retomada_pelo_cache(tmp_path):
    api = FakeAPI(n_videos=120)
    api.falhas = [("pageToken=2", ex.ErroHTTP(403, "quotaExceeded", "The request cannot be completed"))]
    cli, exp, _ = novo(tmp_path, api)
    exp.canal()
    with pytest.raises(ex.QuotaEsgotada):
        exp.exportar_videos()
    exp.salvar_estado()
    feitas = len(api.chamadas)
    # Segunda execução (outro dia): o que já veio sai do cache; só as chamadas que faltavam vão para a rede.
    api.chamadas.clear()
    cli2, exp2, _ = novo(tmp_path, api, hoje=date(2026, 10, 3))
    assert exp2.data_fim == exp.data_fim                     # período ficou fixo no estado
    exp2.canal()
    exp2.exportar_videos()
    assert not any("/channels" in u for u in api.chamadas)
    assert sum("/playlistItems" in u for u in api.chamadas) == 1     # só a página 3
    assert cli2.do_cache == 2 and feitas == 6  # token, mine, channels, 3 páginas
    assert len(ler(tmp_path / "videos.csv")) == 120


def test_main_quota_grava_leiame_e_sai_3(tmp_path, monkeypatch, capsys):
    api = FakeAPI(n_videos=3)
    api.falhas = [("/playlistItems", ex.ErroHTTP(403, "quotaExceeded", "quota"))]
    monkeypatch.setattr(ex, "transporte_urllib", api)
    monkeypatch.setattr(ex.Cliente.__init__, "__defaults__",
                        (None, api, lambda s: None, 0.3, 6, 2.0, None))
    for k, v in ENV.items():
        monkeypatch.setenv(k, v)
    assert ex.main(["--saida", str(tmp_path), "--pausa", "0"]) == 3
    leia = (tmp_path / "LEIAME_DADOS.md").read_text(encoding="utf-8")
    assert "INCOMPLETA" in leia


def test_comentarios_hash_e_sem_nome(tmp_path):
    api = FakeAPI(n_videos=5)
    _, exp, _ = novo(tmp_path, api, top_comentarios=3)
    exp.canal()
    exp.exportar_videos()
    exp.exportar_comentarios()
    rs = ler(tmp_path / "comentarios_top30.csv")
    assert {r["video_id"] for r in rs} == {"v0", "v2"}           # v1 tem comentários desativados
    assert any("v1" in n for n in exp.notas["comentarios_top30.csv"])
    topo = next(r for r in rs if r["comentario_id"] == "c-v0")
    resp = next(r for r in rs if r["comentario_id"] == "r-v0")
    assert topo["autor_canal_id"] == ex.hash_autor("UCautor") and len(topo["autor_canal_id"]) == 16
    assert topo["eh_resposta"] == "0" and resp["eh_resposta"] == "1" and resp["resposta_a"] == "c-v0"
    assert resp["eh_do_canal"] == "1" and topo["eh_do_canal"] == "0"
    texto = (tmp_path / "comentarios_top30.csv").read_text(encoding="utf-8")
    assert "Fulano" not in texto and "UCautor" not in texto


def test_respostas_alem_das_cinco_buscam_comments_list(tmp_path):
    api = FakeAPI(n_videos=1)
    orig = api.__call__

    def chamada(url, data=None, headers=None):
        if "/commentThreads" in url:
            return {"items": [{"snippet": {"totalReplyCount": 7, "topLevelComment": {
                "id": "c1", "snippet": {"textOriginal": "oi"}}}, "replies": {"comments": []}}]}
        if "/comments?" in url:
            q = dict(urllib.parse.parse_qsl(url.split("?")[1]))
            if "pageToken" not in q:
                return {"items": [{"id": f"r{i}", "snippet": {"textOriginal": "x"}} for i in range(5)],
                        "nextPageToken": "p2"}
            return {"items": [{"id": "r5", "snippet": {}}, {"id": "r6", "snippet": {}}]}
        return orig(url, data, headers)
    _, exp, _ = novo(tmp_path, chamada, top_comentarios=1)
    exp.canal()
    exp.exportar_videos()
    exp.exportar_comentarios()
    rs = ler(tmp_path / "comentarios_top30.csv")
    assert len(rs) == 8 and sum(r["eh_resposta"] == "1" for r in rs) == 7


def test_fluxo_completo_e_nenhum_segredo_em_arquivo_ou_log(tmp_path):
    api = FakeAPI(n_videos=60)
    # erro com a key na mensagem: tem de sair limpo no log
    api.falhas = [("/videos", ex.ErroHTTP(503, "", "falhou url ?key=CHAVE-API-SECRETA-111&x=1 Bearer " + ACCESS))]
    cli, exp, logs = novo(tmp_path, api)
    rodar_tudo(exp)
    for nome in ["videos.csv", "analytics_por_video.csv", "trafego_por_video.csv", "inscritos_por_video.csv",
                 "canal_por_mes.csv", "canal_por_dia.csv", "trafego_por_mes.csv", "comentarios_top30.csv",
                 "LEIAME_DADOS.md"]:
        assert (tmp_path / nome).exists(), nome
    ins = ler(tmp_path / "inscritos_por_video.csv")
    assert ins[0] == {"video_id": "v0", "views_inscritos": "4", "views_nao_inscritos": "6",
                      "minutos_inscritos": "8", "minutos_nao_inscritos": "9"}
    tr = ler(tmp_path / "trafego_por_video.csv")
    assert len(tr) == 120 and any(r["origem_pt"].startswith("Vídeos sugeridos") for r in tr)
    # Nenhuma credencial (nem o access token) em nenhum arquivo gerado, inclusive o cache, nem no log.
    segredos = list(ENV.values()) + [ACCESS]
    for arq in tmp_path.rglob("*"):
        if arq.is_file():
            conteudo = arq.read_text(encoding="utf-8", errors="replace")
            for s in segredos:
                assert s not in conteudo, f"{s} vazou em {arq}"
    log = "\n".join(logs)
    assert "aviso: HTTP 503" in log
    for s in segredos:
        assert s not in log
    # A key vai na URL da Data API, mas nunca na chave do cache.
    assert any("key=CHAVE-API-SECRETA-111" in u for u in api.chamadas)


def test_main_sem_vazar_no_stderr_e_no_log(tmp_path, monkeypatch, capsys):
    api = FakeAPI(n_videos=4)
    api.falhas = [(ex.API_ANALYTICS, ex.ErroHTTP(500, "", "Bearer " + ACCESS + " key=" + ENV["YOUTUBE_API_KEY"]))]
    monkeypatch.setattr(ex.Cliente.__init__, "__defaults__", (None, api, lambda s: None, 0.3, 6, 2.0, None))
    for k, v in ENV.items():
        monkeypatch.setenv(k, v)
    assert ex.main(["--saida", str(tmp_path), "--pausa", "0", "--top-comentarios", "2"]) == 0
    saida = capsys.readouterr()
    log = (tmp_path / ".cache" / "exportar.log").read_text(encoding="utf-8")
    for s in list(ENV.values()) + [ACCESS]:
        assert s not in saida.out + saida.err + log
    assert "LEIAME_DADOS.md" in [p.name for p in tmp_path.iterdir()]


def test_dry_run_sem_rede_e_sem_credenciais(tmp_path, monkeypatch, capsys):
    def proibido(*a, **k):
        raise AssertionError("dry-run foi para a rede")
    monkeypatch.setattr(ex, "transporte_urllib", proibido)
    monkeypatch.setattr(ex.Cliente.__init__, "__defaults__", (None, proibido, lambda s: None, 0.3, 6, 2.0, None))
    for k in ENV:
        monkeypatch.delenv(k, raising=False)
    monkeypatch.setenv("YOUTUBE_API_KEY", ENV["YOUTUBE_API_KEY"])
    assert ex.main(["--dry-run", "--saida", str(tmp_path)]) == 0
    out = capsys.readouterr().out
    assert "PLANO" in out and "YOUTUBE_API_KEY=sim" in out and "YT_REFRESH_TOKEN=NÃO" in out
    assert ENV["YOUTUBE_API_KEY"] not in out
    assert not (tmp_path / ".cache").exists()


def test_main_sem_credenciais_sai_2(tmp_path, monkeypatch):
    for k in ENV:
        monkeypatch.delenv(k, raising=False)
    assert ex.main(["--saida", str(tmp_path)]) == 2


def test_cache_nao_guarda_key(tmp_path):
    api = FakeAPI(n_videos=1)
    cli, _, _ = novo(tmp_path, api)
    cli.data_api("channels", part="id", id="x")
    a = cli._arquivo("data", "channels", {"part": "id", "id": "x", "key": "OUTRA"})
    assert a.exists()                                       # a key não entra na chave do cache
    conteudo = json.loads(a.read_text(encoding="utf-8"))
    assert "items" in conteudo


def test_termos_de_busca_canal_e_videos(tmp_path):
    api = FakeAPI(n_videos=8)
    cli, exp, _ = novo(tmp_path, api)
    exp.canal()
    exp.exportar_videos()
    ids = exp.exportar_analytics_por_video()
    exp.exportar_por_video(ids)          # gera trafego_por_video.csv (YT_SEARCH vem no mock)
    exp.leiame("completo")
    api.chamadas.clear()
    exp.exportar_termos_busca(meses=3, n_videos=5)
    qs = [_q(u) for u in api.chamadas if u.startswith(ex.API_ANALYTICS)]
    assert len(qs) == 3 + 1 + 5
    assert all(q["dimensions"] == "insightTrafficSourceDetail" and q["maxResults"] == "25" for q in qs)
    canal = ler(tmp_path / "termos_busca_canal.csv")
    assert {r["periodo"] for r in canal} == {"2026-07", "2026-08", "2026-09", "total"}
    assert len(canal) == 4 * 25 and canal[0]["posicao"] == "1"
    vids = ler(tmp_path / "termos_busca_por_video.csv")
    assert len({r["video_id"] for r in vids}) == 5 and vids[0]["termo"].startswith("termo 0 video==")
    exp.leiame_termos()
    exp.leiame_termos()                  # idempotente: uma seção só
    leia = (tmp_path / "LEIAME_DADOS.md").read_text(encoding="utf-8")
    assert leia.count("<!-- termos-busca -->") == 1 and "videos.csv" in leia
    # retomada: tudo do cache
    exp.salvar_estado()
    api.chamadas.clear()
    _, exp2, _ = novo(tmp_path, api)
    exp2.exportar_termos_busca(meses=3, n_videos=5)
    assert not any(u.startswith(ex.API_ANALYTICS) for u in api.chamadas)


def test_termos_de_busca_400_vira_nota(tmp_path):
    api = FakeAPI(n_videos=3)
    api.recusar_termos = True
    _, exp, _ = novo(tmp_path, api)
    exp.canal()
    exp.exportar_videos()
    exp.exportar_termos_busca(meses=2, n_videos=3)
    assert ler(tmp_path / "termos_busca_canal.csv") == []
    assert any("recusou" in n for n in exp.notas["termos_busca_canal.csv"])
    assert any("recusou" in n for n in exp.notas["termos_busca_por_video.csv"])


def test_main_termos_busca_so_analytics_e_sem_segredo(tmp_path, monkeypatch, capsys):
    api = FakeAPI(n_videos=4)
    monkeypatch.setattr(ex.Cliente.__init__, "__defaults__", (None, api, lambda s: None, 0.3, 6, 2.0, None))
    for k, v in ENV.items():
        monkeypatch.setenv(k, v)
    assert ex.main(["--saida", str(tmp_path), "--pausa", "0", "--so-videos", "--top-comentarios", "1"]) == 0
    api.chamadas.clear()
    assert ex.main(["--saida", str(tmp_path), "--pausa", "0", "--termos-busca", "--termos-meses", "2",
                    "--termos-videos", "2"]) == 0
    assert not any(u.startswith(ex.API_DATA) for u in api.chamadas)
    assert (tmp_path / "termos_busca_canal.csv").exists()
    out = capsys.readouterr()
    for s_ in list(ENV.values()) + [ACCESS]:
        assert s_ not in out.out + out.err + (tmp_path / "LEIAME_DADOS.md").read_text(encoding="utf-8")


def test_termos_recentes(tmp_path):
    api = FakeAPI(n_videos=6)
    orig = api.__call__

    def chamada(url, data=None, headers=None):
        if "/videos?" in url:
            d = orig(url, data, headers)
            for it in d["items"]:
                if it["id"] in ("v0", "v1"):
                    it["snippet"]["publishedAt"] = "2026-08-10T21:00:00Z"
            return d
        return orig(url, data, headers)
    cli, exp, _ = novo(tmp_path, chamada)
    exp.canal()
    exp.exportar_videos()
    ids = exp.exportar_analytics_por_video()
    exp.exportar_por_video(ids)
    api.chamadas.clear()
    exp.exportar_termos_recentes(dias=180, n_busca=2)
    qs = [_q(u) for u in api.chamadas if u.startswith(ex.API_ANALYTICS)]
    alvos = [q["filters"].split(";")[0] for q in qs]
    assert alvos[:2] == ["video==v0", "video==v1"] and len(set(alvos)) == len(alvos)
    assert all(q["startDate"] == "2026-04-04" and q["maxResults"] == "25" for q in qs)
    rs = ler(tmp_path / "termos_busca_recentes.csv")
    assert rs[0]["desde"] == "2026-04-04" and rs[0]["publicado"] == "2026-08-10"
    exp.leiame_termos()
    assert "termos_busca_recentes.csv" in (tmp_path / "LEIAME_DADOS.md").read_text(encoding="utf-8")
