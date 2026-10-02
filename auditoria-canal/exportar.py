#!/usr/bin/env python3
"""Exportador de dados do canal "Investir e Coçar" para a auditoria.

Só LEITURA e só biblioteca padrão. Roda no Mac do Denis, que tem as credenciais; grava CSVs em dados/.

Credenciais (variáveis de ambiente, as mesmas do radar de comentários e do termômetro de 2 h):
  YOUTUBE_API_KEY                          Data API v3 (vídeos e comentários públicos)
  YT_CLIENT_ID, YT_CLIENT_SECRET,          trocadas por um access token em oauth2.googleapis.com/token,
  YT_REFRESH_TOKEN                         usado na YouTube Analytics API v2 (ids=channel==MINE)
  YT_CHANNEL_ID (opcional)                 se faltar, o canal sai de channels?mine=true com o OAuth

Nenhuma credencial é impressa ou gravada: o cache guarda só as respostas, com a chave sem a API key, e todo
texto que vai para a tela ou para o log passa por um filtro que troca os segredos por ***.

uso:
  python3 exportar.py                      tudo (Data API + Analytics)
  python3 exportar.py --so-videos          só Data API: videos.csv e comentarios_top30.csv
  python3 exportar.py --so-analytics       só Analytics: os demais CSVs
  python3 exportar.py --desde 2023-01-01   início do período por vídeo (padrão: criação do canal)
  python3 exportar.py --dry-run            mostra o plano e a quota estimada, sem rede e sem credenciais
  python3 exportar.py --recomecar          apaga o cache e começa do zero (senão, retoma de onde parou)

Saída: 0 = ok; 2 = faltou credencial; 3 = quota da Data API esgotada (rode de novo amanhã: retoma do cache).
"""
import argparse
import csv
import hashlib
import json
import math
import os
import re
import shutil
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
DADOS = AQUI / "dados"
API_DATA = "https://www.googleapis.com/youtube/v3"
API_ANALYTICS = "https://youtubeanalytics.googleapis.com/v2/reports"
URL_TOKEN = "https://oauth2.googleapis.com/token"
CANAL_PADRAO = "UCWA0o8iZl2xbPXRopKu5A5Q"  # Investir e Coçar (o mesmo do radar e do termômetro)
SEGREDOS = ("YOUTUBE_API_KEY", "YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN")
BRT = timezone(timedelta(hours=-3))  # Brasília: sem horário de verão desde 2019
DIAS = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]

# Critério de formato. O YouTube aceita Shorts de até 60 s e, desde 15/10/2024, de até 3 min (180 s).
# short = duração ≤ 60 s; OU duração ≤ 180 s e publicado a partir de 15/10/2024; OU "#shorts"/"#short" no
# título ou na descrição. O resto é "longo". (Um vídeo horizontal de 2 min de 2023 não vira short à toa.)
SHORT_MAX_ANTIGO, SHORT_MAX, SHORT_DESDE = 60, 180, date(2024, 10, 15)
CRITERIO_FORMATO = ("short = duração ≤ 60 s; ou ≤ 180 s publicado a partir de 15/10/2024 (quando o limite dos "
                    "Shorts subiu para 3 min); ou com #shorts/#short no título ou na descrição. O resto é longo.")

RETRY_STATUS = {429, 500, 502, 503, 504}
RETRY_MOTIVOS = {"rateLimitExceeded", "userRateLimitExceeded", "backendError", "internalError"}
QUOTA_MOTIVOS = {"quotaExceeded", "dailyLimitExceeded"}

METRICAS_VIDEO = ["views", "estimatedMinutesWatched", "averageViewDuration", "averageViewPercentage",
                  "subscribersGained", "subscribersLost", "likes", "shares", "comments"]
# Métricas que podem não existir na API: cada uma vai numa consulta separada; se der 400, a coluna fica vazia
# com nota no LEIAME. Para impressões e CTR tentamos os nomes conhecidos, na ordem.
OPCIONAIS_VIDEO = [
    ("engagedViews", ["engagedViews"]),
    ("impressions", ["videoThumbnailImpressions", "impressions"]),
    ("impressionsClickThroughRate", ["videoThumbnailImpressionsClickRate", "impressionsClickThroughRate"]),
]
METRICAS_MES = ["views", "estimatedMinutesWatched", "subscribersGained", "subscribersLost"]
FORMATOS_API = {"SHORTS": "shorts", "VIDEO_ON_DEMAND": "longos", "LIVE_STREAM": "lives"}
ORIGENS_PT = {
    "RELATED_VIDEO": "Vídeos sugeridos (Recomendados)", "BROWSE": "Recursos de navegação (Início/Inscrições)",
    "YT_SEARCH": "Pesquisa do YouTube", "SUBSCRIBER": "Recursos de navegação (na API: Início, Inscrições)", "EXT_URL": "Externo",
    "NO_LINK_OTHER": "Direto ou desconhecido", "SHORTS": "Feed do Shorts", "PLAYLIST": "Playlists",
    "YT_CHANNEL": "Página do canal", "NOTIFICATION": "Notificações", "END_SCREEN": "Tela final",
    "ANNOTATION": "Cards/anotações", "YT_OTHER_PAGE": "Outras páginas do YouTube", "CAMPAIGN_CARD": "Campanha",
    "ADVERTISING": "Anúncios", "HASHTAGS": "Hashtags", "SOUND_PAGE": "Página de áudio", "LIVE_REDIRECT": "Redirecionamento de live",
    "VIDEO_REMIXES": "Remixes", "PRODUCT_PAGE": "Página de produto", "IMMERSIVE_LIVE": "Live imersiva",
}


# ----------------------------------------------------------------------------------------------- rede e cache
class ErroHTTP(Exception):
    def __init__(self, status, motivo="", mensagem=""):
        super().__init__(f"HTTP {status} {motivo}: {mensagem}".strip())
        self.status, self.motivo, self.mensagem = status, motivo, mensagem


class QuotaEsgotada(Exception):
    pass


def transporte_urllib(url, data=None, headers=None):
    """Única porta de saída para a rede (os testes trocam por uma falsa). Erros não carregam a URL com a key."""
    req = urllib.request.Request(url, data=data, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        corpo = e.read().decode("utf-8", errors="replace")
        motivo, msg = "", corpo[:300]
        try:
            err = json.loads(corpo).get("error", {})
            if isinstance(err, dict):
                msg = err.get("message", msg)
                motivo = (err.get("errors") or [{}])[0].get("reason", "") or err.get("status", "")
            else:
                motivo = str(err)
        except (ValueError, AttributeError):
            pass
        raise ErroHTTP(e.code, motivo, msg) from None
    except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
        raise ErroHTTP(0, "rede", str(getattr(e, "reason", e))) from None


class Cliente:
    """Faz as chamadas com cache em disco, contagem de quota, pausa entre chamadas e retry com backoff."""

    def __init__(self, cache_dir, env=None, transporte=transporte_urllib, dormir=time.sleep, pausa=0.3,
                 tentativas=6, backoff=2.0, log=None):
        self.cache_dir = Path(cache_dir)
        (self.cache_dir / "respostas").mkdir(parents=True, exist_ok=True)
        self.env = os.environ if env is None else env
        self.transporte, self.dormir, self.pausa = transporte, dormir, pausa
        self.tentativas, self.backoff = tentativas, backoff
        self._log = log or (lambda m: print(m, file=sys.stderr))
        self._token = None
        self.unidades_data = 0      # unidades da quota da Data API (10.000/dia por projeto)
        self.consultas_analytics = 0
        self.do_cache = 0

    # -- segredos
    def segredos(self):
        vals = [self.env.get(n) for n in SEGREDOS] + [self._token]
        return [v for v in vals if v and len(v) >= 4]

    def limpar(self, texto):
        texto = str(texto)
        for s in self.segredos():
            texto = texto.replace(s, "***")
        texto = re.sub(r"(key|access_token|refresh_token|client_secret)=[^&\s]+", r"\1=***", texto)
        return re.sub(r"Bearer\s+\S+", "Bearer ***", texto)

    def log(self, msg):
        self._log(self.limpar(msg))

    def exigir(self, nome):
        v = self.env.get(nome)
        if not v:
            raise SystemExit(f"faltou a variável de ambiente {nome}")
        return v

    # -- cache
    def _arquivo(self, tipo, recurso, params):
        limpo = {k: v for k, v in params.items() if k != "key"}
        chave = json.dumps([tipo, recurso, sorted(limpo.items())], ensure_ascii=False, default=str)
        return self.cache_dir / "respostas" / (hashlib.sha256(chave.encode()).hexdigest()[:32] + ".json")

    def _de_cache(self, arq):
        if not arq.exists():
            return None
        self.do_cache += 1
        d = json.loads(arq.read_text(encoding="utf-8"))
        if isinstance(d, dict) and "__erro__" in d:  # erro 400/403/404 é determinístico: não repete a chamada
            e = d["__erro__"]
            raise ErroHTTP(e["status"], e["motivo"], e["mensagem"])
        return d

    def _gravar(self, arq, d):
        tmp = arq.with_suffix(".tmp")
        tmp.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        tmp.replace(arq)

    # -- chamada com retry
    def _pedir(self, url, data=None, headers=None, oauth=False):
        renovou = False
        for n in range(self.tentativas):
            h = dict(headers or {})
            if oauth:
                h["Authorization"] = "Bearer " + self.token()
            try:
                if self.pausa:
                    self.dormir(self.pausa)
                return self.transporte(url, data, h)
            except ErroHTTP as e:
                if e.motivo in QUOTA_MOTIVOS:
                    raise QuotaEsgotada(self.limpar(e.mensagem)) from None
                if e.status == 401 and oauth and not renovou:
                    self._token, renovou = None, True
                    continue
                if (e.status in RETRY_STATUS or e.status == 0 or e.motivo in RETRY_MOTIVOS) and n < self.tentativas - 1:
                    espera = min(self.backoff * 2 ** n, 120)
                    self.log(f"  aviso: HTTP {e.status} {e.motivo} em {url.split('?')[0]}; nova tentativa em {espera:.0f} s")
                    self.dormir(espera)
                    continue
                raise ErroHTTP(e.status, e.motivo, self.limpar(e.mensagem)) from None
        raise ErroHTTP(0, "rede", "esgotou as tentativas")

    def token(self):
        if self._token is None:
            corpo = urllib.parse.urlencode({
                "client_id": self.exigir("YT_CLIENT_ID"), "client_secret": self.exigir("YT_CLIENT_SECRET"),
                "refresh_token": self.exigir("YT_REFRESH_TOKEN"), "grant_type": "refresh_token"}).encode()
            try:
                d = self.transporte(URL_TOKEN, corpo, {"Content-Type": "application/x-www-form-urlencoded"})
            except ErroHTTP as e:
                raise SystemExit(self.limpar(f"não consegui trocar o refresh token por um access token: {e}")) from None
            self._token = d["access_token"]
        return self._token

    def _chamar(self, tipo, recurso, params, url, oauth, custo):
        arq = self._arquivo(tipo, recurso, params)
        d = self._de_cache(arq)
        if d is not None:
            return d
        try:
            if tipo == "data":
                self.unidades_data += custo
            else:
                self.consultas_analytics += 1
            d = self._pedir(url, oauth=oauth)
        except ErroHTTP as e:
            if e.status in (400, 403, 404):
                self._gravar(arq, {"__erro__": {"status": e.status, "motivo": e.motivo, "mensagem": e.mensagem}})
            raise
        self._gravar(arq, d)
        return d

    def data_api(self, recurso, oauth=False, custo=1, **params):
        q = dict(params)
        if not oauth:
            q["key"] = self.exigir("YOUTUBE_API_KEY")
        url = f"{API_DATA}/{recurso}?{urllib.parse.urlencode(q)}"
        return self._chamar("data", recurso, params, url, oauth, custo)

    def analytics(self, **params):
        q = {"ids": "channel==MINE", **params}
        url = f"{API_ANALYTICS}?{urllib.parse.urlencode(q)}"
        return self._chamar("analytics", "reports", q, url, True, 0)

    def analytics_tabela(self, **params):
        """Resposta do Analytics como lista de dicts. Sem paginação: o relatório por vídeo não passa de 200
        linhas (startIndex=201 dá 400), então o exportador consulta por lotes de IDs."""
        return linhas(self.analytics(**params))


def linhas(d):
    nomes = [c["name"] for c in d.get("columnHeaders", [])]
    return [dict(zip(nomes, r)) for r in d.get("rows") or []]


# ------------------------------------------------------------------------------------------------ utilidades
def duracao_s(iso):
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso or "")
    if not m:
        return 0
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def formato(dur, publicado_utc, titulo="", descricao=""):
    if re.search(r"#shorts?\b", f"{titulo} {descricao}", re.I):
        return "short"
    if dur <= SHORT_MAX_ANTIGO:
        return "short"
    if dur <= SHORT_MAX and publicado_utc.date() >= SHORT_DESDE:
        return "short"
    return "longo"


def hash_autor(canal_id):
    if not canal_id:
        return ""
    return hashlib.sha256(("iec-auditoria:" + canal_id).encode()).hexdigest()[:16]


def iso_utc(s):
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def fim_do_mes(d):
    prox = (d.replace(day=28) + timedelta(days=4)).replace(day=1)
    return prox - timedelta(days=1)


def meses_para_tras(fim_mes, n):
    """Primeiro dia do mês n-1 meses antes do mês de fim_mes."""
    a, m = fim_mes.year, fim_mes.month - (n - 1)
    while m <= 0:
        a, m = a - 1, m + 12
    return date(a, m, 1)


def gravar_csv(caminho, colunas, registros):
    caminho.parent.mkdir(parents=True, exist_ok=True)
    tmp = caminho.with_suffix(".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=colunas, extrasaction="ignore")
        w.writeheader()
        for r in registros:
            w.writerow({c: ("" if r.get(c) is None else r.get(c)) for c in colunas})
    tmp.replace(caminho)
    return len(registros)


def ler_csv(caminho):
    if not caminho.exists():
        return []
    with caminho.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


# ------------------------------------------------------------------------------------------------ colunas
COLUNAS = {
    "videos.csv": [
        ("id", "id do vídeo"), ("titulo", "título atual"),
        ("publicado_em_utc", "data e hora da publicação em UTC"),
        ("publicado_em_brt", "data e hora da publicação em Brasília (UTC-3)"),
        ("dia_semana", "dia da semana em Brasília"), ("hora", "hora cheia em Brasília (0-23)"),
        ("duracao_s", "duração em segundos"), ("formato", "short ou longo (critério abaixo)"),
        ("views", "contador público de views (Data API, no momento da exportação)"),
        ("likes", "likes públicos"), ("comentarios", "total de comentários públicos"),
        ("tags", "tags separadas por |"), ("descricao_tamanho", "nº de caracteres da descrição"),
        ("thumbnail_url", "maior thumbnail disponível"),
    ],
    "analytics_por_video.csv": [
        ("video_id", "id do vídeo"), ("titulo", "título (de videos.csv)"), ("formato", "short ou longo"),
        ("publicado_em_brt", "publicação em Brasília"),
        ("views", "views no período (Analytics)"), ("estimatedMinutesWatched", "minutos assistidos"),
        ("averageViewDuration", "duração média da visualização (s)"),
        ("averageViewPercentage", "% média assistida"), ("subscribersGained", "inscritos ganhos"),
        ("subscribersLost", "inscritos perdidos"), ("likes", "likes"), ("shares", "compartilhamentos"),
        ("comments", "comentários"), ("engagedViews", "views engajadas (se a API tiver a métrica)"),
        ("impressions", "impressões da thumbnail (se a API devolver)"),
        ("impressionsClickThroughRate", "CTR das impressões, % (se a API devolver)"),
    ],
    "trafego_por_video.csv": [
        ("video_id", "id do vídeo"), ("origem", "insightTrafficSourceType"), ("origem_pt", "nome no Studio"),
        ("views", "views"), ("minutos", "estimatedMinutesWatched"),
    ],
    "inscritos_por_video.csv": [
        ("video_id", "id do vídeo"), ("views_inscritos", "views de quem é inscrito"),
        ("views_nao_inscritos", "views de quem não é inscrito"), ("minutos_inscritos", "minutos de inscritos"),
        ("minutos_nao_inscritos", "minutos de não inscritos"),
    ],
    "canal_por_mes.csv": [
        ("mes", "AAAA-MM"), ("views", "views"), ("minutos", "minutos assistidos"),
        ("inscritos_ganhos", "inscritos ganhos"), ("inscritos_perdidos", "inscritos perdidos"),
        ("engagedViews", "views engajadas (se a API tiver)"),
        ("views_shorts", "views de Shorts (creatorContentType=SHORTS)"),
        ("views_longos", "views de vídeos longos (VIDEO_ON_DEMAND)"), ("views_lives", "views de lives"),
        ("minutos_shorts", "minutos de Shorts"), ("minutos_longos", "minutos de longos"),
        ("minutos_lives", "minutos de lives"),
        ("inscritos_ganhos_shorts", "inscritos ganhos em Shorts"), ("inscritos_ganhos_longos", "inscritos ganhos em longos"),
        ("inscritos_ganhos_lives", "inscritos ganhos em lives"),
        ("inscritos_perdidos_shorts", "inscritos perdidos em Shorts"),
        ("inscritos_perdidos_longos", "inscritos perdidos em longos"),
        ("inscritos_perdidos_lives", "inscritos perdidos em lives"),
    ],
    "canal_por_dia.csv": [
        ("dia", "AAAA-MM-DD"), ("views", "views"), ("minutos", "minutos assistidos"),
        ("inscritos_ganhos", "inscritos ganhos"), ("inscritos_perdidos", "inscritos perdidos"),
        ("engagedViews", "views engajadas (se a API tiver)"),
    ],
    "trafego_por_mes.csv": [
        ("mes", "AAAA-MM"), ("origem", "insightTrafficSourceType"), ("origem_pt", "nome no Studio"),
        ("views", "views"), ("minutos", "minutos"), ("pct_views_mes", "% das views do mês"),
    ],
    "termos_busca_canal.csv": [
        ("periodo", "AAAA-MM, ou 'total' para o período inteiro"), ("posicao", "posição do termo no período (1 = mais views)"),
        ("termo", "termo buscado no YouTube (insightTrafficSourceDetail com origem YT_SEARCH)"),
        ("views", "views que vieram desse termo"), ("minutos", "minutos assistidos vindos desse termo"),
    ],
    "termos_busca_por_video.csv": [
        ("video_id", "id do vídeo"), ("titulo", "título"), ("posicao", "posição do termo no vídeo"),
        ("termo", "termo buscado"), ("views", "views desse termo no vídeo (período inteiro)"), ("minutos", "minutos"),
    ],
    "termos_busca_recentes.csv": [
        ("video_id", "id do vídeo"), ("titulo", "título"), ("publicado", "data de publicação (Brasília)"),
        ("desde", "início do período (fim = data de corte da exportação)"), ("posicao", "posição do termo no vídeo"),
        ("termo", "termo buscado"), ("views", "views desse termo no vídeo, no período"), ("minutos", "minutos"),
    ],
    "comentarios_top30.csv": [
        ("video_id", "id do vídeo"), ("comentario_id", "id do comentário"),
        ("resposta_a", "id do comentário-pai (vazio se não for resposta)"),
        ("autor_canal_id", "hash SHA-256 (16 hex) do id do canal do autor; o nome NÃO é gravado"),
        ("eh_do_canal", "1 se quem escreveu foi o próprio canal"), ("texto", "texto do comentário"),
        ("likes", "likes"), ("publicado_em", "data e hora UTC"), ("eh_resposta", "1 se é resposta"),
    ],
}


def cols(arquivo):
    return [c for c, _ in COLUNAS[arquivo]]


# ------------------------------------------------------------------------------------------------ exportador
class Exportador:
    def __init__(self, cliente, saida=DADOS, desde=None, hoje=None, top_comentarios=30, max_paginas_coment=20,
                 meses=18, dias=180, max_videos_detalhe=0):
        self.c, self.saida = cliente, Path(saida)
        self.desde_arg, self.top_comentarios, self.max_paginas_coment = desde, top_comentarios, max_paginas_coment
        self.meses, self.dias, self.max_videos_detalhe = meses, dias, max_videos_detalhe
        self.estado_arq = self.c.cache_dir / "estado.json"
        self.estado = json.loads(self.estado_arq.read_text(encoding="utf-8")) if self.estado_arq.exists() else {}
        hoje = hoje or datetime.now(BRT).date()
        # O fim do período fica fixo na primeira execução: uma retomada no dia seguinte reaproveita o cache.
        self.estado.setdefault("data_fim", (hoje - timedelta(days=1)).isoformat())
        self.estado.setdefault("exportado_em", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"))
        self.data_fim = date.fromisoformat(self.estado["data_fim"])
        self.notas = {}
        self.contagens = {}
        self.lote_ok = {}
        self.videos = {r["id"]: r for r in ler_csv(self.saida / "videos.csv")}

    def nota(self, arquivo, texto):
        self.notas.setdefault(arquivo, [])
        if texto not in self.notas[arquivo]:
            self.notas[arquivo].append(texto)
        self.c.log(f"  nota ({arquivo}): {texto}")

    def salvar_estado(self):
        self.estado["unidades_data_total"] = self.estado.get("unidades_data_total", 0) + self.c.unidades_data
        self.estado["consultas_analytics_total"] = (self.estado.get("consultas_analytics_total", 0)
                                                    + self.c.consultas_analytics)
        self.estado_arq.write_text(json.dumps(self.estado, ensure_ascii=False, indent=1), encoding="utf-8")

    def gravar(self, arquivo, registros):
        n = gravar_csv(self.saida / arquivo, cols(arquivo), registros)
        self.contagens[arquivo] = n
        self.c.log(f"  {arquivo}: {n} linhas")

    # -- canal
    def canal(self):
        cid = self.c.env.get("YT_CHANNEL_ID") or self.estado.get("canal_id")
        if not cid:
            try:
                d = self.c.data_api("channels", oauth=True, part="id", mine="true")
                cid = d["items"][0]["id"]
            except (ErroHTTP, KeyError, IndexError) as e:
                cid = CANAL_PADRAO
                self.nota("videos.csv", f"channels?mine=true falhou ({e}); usei o canal padrão {CANAL_PADRAO}")
        self.estado["canal_id"] = cid
        if "canal_criado" not in self.estado:
            d = self.c.data_api("channels", part="snippet,contentDetails,statistics", id=cid)
            item = d["items"][0]
            self.estado["canal_titulo"] = item["snippet"]["title"]
            self.estado["canal_criado"] = item["snippet"]["publishedAt"][:10]
            self.estado["uploads"] = item["contentDetails"]["relatedPlaylists"]["uploads"]
            self.estado["inscritos_publico"] = item["statistics"].get("subscriberCount")
        return cid

    @property
    def desde(self):
        if self.desde_arg:
            return self.desde_arg
        return date.fromisoformat(self.estado.get("canal_criado") or "2023-01-01")

    # -- 1. vídeos
    def exportar_videos(self):
        self.c.log("1/7 vídeos (playlist de uploads)")
        ids, token = [], None
        while True:
            p = {"part": "contentDetails", "playlistId": self.estado["uploads"], "maxResults": 50}
            if token:
                p["pageToken"] = token
            d = self.c.data_api("playlistItems", **p)
            ids += [i["contentDetails"]["videoId"] for i in d.get("items", [])]
            token = d.get("nextPageToken")
            if not token:
                break
        ids = list(dict.fromkeys(ids))
        regs = []
        for i in range(0, len(ids), 50):
            d = self.c.data_api("videos", part="snippet,contentDetails,statistics", id=",".join(ids[i:i + 50]))
            for v in d.get("items", []):
                sn, st = v["snippet"], v.get("statistics", {})
                pub = iso_utc(sn["publishedAt"])
                brt = pub.astimezone(BRT)
                dur = duracao_s(v.get("contentDetails", {}).get("duration"))
                thumbs = sn.get("thumbnails", {})
                thumb = next((thumbs[k]["url"] for k in ("maxres", "standard", "high", "medium", "default")
                              if k in thumbs), "")
                regs.append({
                    "id": v["id"], "titulo": sn.get("title", ""),
                    "publicado_em_utc": pub.strftime("%Y-%m-%d %H:%M:%S"),
                    "publicado_em_brt": brt.strftime("%Y-%m-%d %H:%M:%S"),
                    "dia_semana": DIAS[brt.weekday()], "hora": brt.hour, "duracao_s": dur,
                    "formato": formato(dur, pub, sn.get("title", ""), sn.get("description", "")),
                    "views": st.get("viewCount", ""), "likes": st.get("likeCount", ""),
                    "comentarios": st.get("commentCount", ""), "tags": "|".join(sn.get("tags", [])),
                    "descricao_tamanho": len(sn.get("description", "")), "thumbnail_url": thumb})
        faltando = len(ids) - len(regs)
        if faltando:
            self.nota("videos.csv", f"{faltando} vídeo(s) da playlist não voltaram em videos.list (privados ou removidos)")
        regs.sort(key=lambda r: r["publicado_em_utc"], reverse=True)
        self.gravar("videos.csv", regs)
        self.videos = {r["id"]: {k: str(v) for k, v in r.items()} for r in regs}

    # -- consultas em lote de IDs
    # O relatório de "top vídeos" (dimensions=video, sort=-views) NÃO pagina além de 200: com startIndex=201 a
    # API devolve 400 "The query is not supported". Por isso consultamos por lotes de IDs (filters=video==a,b,...),
    # sem sort. Se a API recusar o lote, ele é dividido ao meio até funcionar (ou até 1 vídeo).
    LOTE_INICIAL = 200

    def ids_videos(self):
        """IDs de videos.csv, do mais visto ao menos visto (contador público)."""
        return [v["id"] for v in sorted(self.videos.values(), key=lambda v: -int(v.get("views") or 0))]

    def _lote(self, ids, dims, metrics):
        q = {"startDate": str(self.desde), "endDate": str(self.data_fim), "dimensions": dims, "metrics": metrics,
             "filters": "video==" + ",".join(ids)}
        return self.c.analytics_tabela(**q)

    def consulta_em_lotes(self, ids, dims, metrics, arquivo):
        """Roda a consulta em lotes; devolve (linhas, tamanho_que_funcionou). Erro de métrica não divide o lote.
        Se nem 1 vídeo funcionar, levanta o ErroHTTP (quem chamou decide o fallback)."""
        tam = self.lote_ok.get(dims, self.LOTE_INICIAL)
        out, i = [], 0
        while i < len(ids):
            lote = ids[i:i + tam]
            try:
                out += self._lote(lote, dims, metrics)
                i += len(lote)
            except ErroHTTP as e:
                if e.status != 400 or len(lote) == 1 or "identifier" in e.mensagem.lower():
                    raise
                tam = max(1, len(lote) // 2)
                self.c.log(f"  lote de {len(lote)} vídeos recusado ({dims}): tentando {tam}")
        self.lote_ok[dims] = tam
        self.nota(arquivo, f"consulta por lotes de até {tam} IDs (filters=video==...; dimensions={dims})")
        return out

    # -- 2. analytics por vídeo
    def exportar_analytics_por_video(self):
        arq = "analytics_por_video.csv"
        ids = self.ids_videos()
        if not ids:
            raise SystemExit("videos.csv ausente ou vazio: rode antes `python3 exportar.py --so-videos`")
        self.c.log(f"2/7 Analytics por vídeo ({self.desde} a {self.data_fim}; {len(ids)} vídeos em lotes)")
        por_id = {}
        for r in self.consulta_em_lotes(ids, "video", ",".join(METRICAS_VIDEO), arq):
            por_id[r["video"]] = {"video_id": r["video"], **{m: r.get(m) for m in METRICAS_VIDEO}}
        for coluna, nomes in OPCIONAIS_VIDEO:
            erros = []
            for nome in nomes:
                try:
                    self._lote(ids[:1], "video", f"views,{nome}")  # sonda barata: 1 vídeo
                    rs = self.consulta_em_lotes(ids, "video", f"views,{nome}", arq)
                except ErroHTTP as e:
                    if e.status not in (400, 403):
                        raise
                    erros.append(f"{nome}: HTTP {e.status} {e.mensagem[:120]}")
                    continue
                for r in rs:
                    if r["video"] in por_id:
                        por_id[r["video"]][coluna] = r.get(nome)
                if nome != coluna:
                    self.nota(arq, f"coluna {coluna} veio da métrica {nome}")
                break
            else:
                self.nota(arq, f"coluna {coluna} vazia: a API recusou ({'; '.join(erros)}). "
                               "Exporte pelo YouTube Studio (Análises > Modo avançado > Conteúdo) para dados/studio/.")
        regs = sorted(por_id.values(), key=lambda r: -float(r.get("views") or 0))
        for r in regs:
            v = self.videos.get(r["video_id"], {})
            r.update(titulo=v.get("titulo", ""), formato=v.get("formato", ""), publicado_em_brt=v.get("publicado_em_brt", ""))
        sem = len(set(self.videos) - set(por_id))
        if sem:
            self.nota(arq, f"{sem} vídeo(s) de videos.csv sem linha no Analytics (sem views no período ou recentes demais)")
        self.gravar(arq, regs)
        return [r["video_id"] for r in regs]  # ordem: -views

    # -- 3 e 4. tráfego e inscritos por vídeo
    def inicio_video(self, vid):
        pub = self.videos.get(vid, {}).get("publicado_em_brt", "")
        d = date.fromisoformat(pub[:10]) if pub else self.desde
        return max(d, self.desde)

    def _por_video_ou_lote(self, ids, dim, arquivo):
        """Linhas {video, dim, views, estimatedMinutesWatched}: em lote com dimensions=video,<dim>; se a API não
        aceitar duas dimensões com vários vídeos, uma consulta por vídeo (filters=video==ID, só <dim>)."""
        met = "views,estimatedMinutesWatched"
        try:
            return self.consulta_em_lotes(ids, f"video,{dim}", met, arquivo)
        except ErroHTTP as e:
            if e.status != 400:
                raise
            self.nota(arquivo, f"a API recusou video,{dim} em lote ({e.mensagem[:100]}); consultei vídeo a vídeo")
        out = []
        for n, vid in enumerate(ids, 1):
            if n % 50 == 0:
                self.c.log(f"  {dim}: {n}/{len(ids)}")
            ini = str(self.inicio_video(vid))
            if ini > str(self.data_fim):
                continue
            try:
                rs = self.c.analytics_tabela(startDate=ini, endDate=str(self.data_fim), filters=f"video=={vid}",
                                             metrics=met, dimensions=dim)
            except ErroHTTP as e:
                if e.status != 400:
                    raise
                self.nota(arquivo, f"a API recusou {dim} por vídeo ({e.mensagem[:100]})")
                return out
            out += [dict(r, video=vid) for r in rs]
        return out

    def exportar_por_video(self, ids):
        if self.max_videos_detalhe:
            ids = ids[:self.max_videos_detalhe]
            self.nota("trafego_por_video.csv", f"só os {len(ids)} vídeos com mais views (--max-videos-detalhe)")
            self.nota("inscritos_por_video.csv", f"só os {len(ids)} vídeos com mais views (--max-videos-detalhe)")
        self.c.log(f"3-4/7 tráfego e inscritos por vídeo ({len(ids)} vídeos; retoma do cache)")
        traf = []
        for r in self._por_video_ou_lote(ids, "insightTrafficSourceType", "trafego_por_video.csv"):
            o = r["insightTrafficSourceType"]
            traf.append({"video_id": r["video"], "origem": o, "origem_pt": ORIGENS_PT.get(o, o),
                         "views": r["views"], "minutos": r["estimatedMinutesWatched"]})
        insc = {}
        for r in self._por_video_ou_lote(ids, "subscribedStatus", "inscritos_por_video.csv"):
            reg = insc.setdefault(r["video"], {"video_id": r["video"]})
            suf = "inscritos" if r["subscribedStatus"] == "SUBSCRIBED" else "nao_inscritos"
            reg[f"views_{suf}"] = r["views"]
            reg[f"minutos_{suf}"] = r["estimatedMinutesWatched"]
        ordem = {v: k for k, v in enumerate(ids)}
        traf.sort(key=lambda r: (ordem.get(r["video_id"], 1e9), -float(r["views"] or 0)))
        self.gravar("trafego_por_video.csv", traf)
        self.gravar("inscritos_por_video.csv", sorted(insc.values(), key=lambda r: ordem.get(r["video_id"], 1e9)))

    # -- 5. canal por mês (e por dia, para datas exatas como 27/08)
    def periodo_meses(self):
        fim = self.data_fim if self.data_fim == fim_do_mes(self.data_fim) else self.data_fim.replace(day=1) - timedelta(days=1)
        return meses_para_tras(fim, self.meses), fim

    def periodo_meses_api(self):
        """Datas para consultas com dimensions=month: a API exige startDate e endDate no dia 1
        (endDate = 1º dia do último mês, que entra inteiro). Com o último dia do mês dá
        HTTP 400 "does not align to chosen date dimension" (visto no Mac em 02/10/2026)."""
        ini, fim = self.periodo_meses()
        return ini, fim.replace(day=1)

    def exportar_canal_por_mes(self):
        arq = "canal_por_mes.csv"
        ini, fim = self.periodo_meses()
        self.c.log(f"5/7 canal por mês ({ini:%Y-%m} a {fim:%Y-%m}; o mês corrente, incompleto, fica fora)")
        q = {"startDate": str(ini), "endDate": str(self.periodo_meses_api()[1]), "dimensions": "month", "sort": "month"}
        regs = {}
        for r in self.c.analytics_tabela(metrics=",".join(METRICAS_MES), **q):
            regs[r["month"]] = {"mes": r["month"], "views": r["views"], "minutos": r["estimatedMinutesWatched"],
                                "inscritos_ganhos": r["subscribersGained"], "inscritos_perdidos": r["subscribersLost"]}
        self._opcional_engaged(arq, q, regs, "month")
        # Por formato: tenta todas as métricas; se recusar, só views e minutos; se recusar de novo, fica vazio.
        nomes = {"views": "views", "estimatedMinutesWatched": "minutos", "subscribersGained": "inscritos_ganhos",
                 "subscribersLost": "inscritos_perdidos"}
        q2 = dict(q, dimensions="month,creatorContentType")
        erros = []
        for mets in (METRICAS_MES, ["views", "estimatedMinutesWatched"]):
            try:
                rs = self.c.analytics_tabela(metrics=",".join(mets), **q2)
            except ErroHTTP as e:
                if e.status not in (400, 403):
                    raise
                erros.append(f"{','.join(mets)}: HTTP {e.status} {e.mensagem[:120]}")
                continue
            for r in rs:
                fmt = FORMATOS_API.get(r["creatorContentType"])
                if not fmt or r["month"] not in regs:
                    continue
                for m in mets:
                    regs[r["month"]][f"{nomes[m]}_{fmt}"] = r[m]
            if mets != METRICAS_MES:
                self.nota(arq, "inscritos por formato vazios: a API não aceitou subscribersGained/Lost com creatorContentType")
            break
        else:
            self.nota(arq, f"colunas por formato vazias: a API recusou creatorContentType ({'; '.join(erros)}). "
                           "No Studio: Análises > Modo avançado > Tipo de conteúdo, por mês.")
        self.gravar(arq, sorted(regs.values(), key=lambda r: r["mes"]))

    def _opcional_engaged(self, arq, q, regs, dim):
        try:
            for r in self.c.analytics_tabela(metrics="views,engagedViews", **q):
                if r[dim] in regs:
                    regs[r[dim]]["engagedViews"] = r["engagedViews"]
        except ErroHTTP as e:
            if e.status not in (400, 403):
                raise
            self.nota(arq, f"engagedViews vazia: a API recusou a métrica (HTTP {e.status} {e.mensagem[:120]}). "
                           "Compare com minutos assistidos.")

    def exportar_canal_por_dia(self):
        arq = "canal_por_dia.csv"
        ini = self.data_fim - timedelta(days=self.dias - 1)
        self.c.log(f"5b/7 canal por dia ({ini} a {self.data_fim}: para testar datas como 27/08 e 28/07)")
        q = {"startDate": str(ini), "endDate": str(self.data_fim), "dimensions": "day", "sort": "day"}
        regs = {}
        for r in self.c.analytics_tabela(metrics=",".join(METRICAS_MES), **q):
            regs[r["day"]] = {"dia": r["day"], "views": r["views"], "minutos": r["estimatedMinutesWatched"],
                              "inscritos_ganhos": r["subscribersGained"], "inscritos_perdidos": r["subscribersLost"]}
        self._opcional_engaged(arq, q, regs, "day")
        self.gravar(arq, sorted(regs.values(), key=lambda r: r["dia"]))

    # -- 6. tráfego por mês
    def exportar_trafego_por_mes(self):
        arq = "trafego_por_mes.csv"
        ini, fim = self.periodo_meses()
        self.c.log("6/7 origem do tráfego por mês")
        met = "views,estimatedMinutesWatched"
        regs = []
        try:
            rs = self.c.analytics_tabela(startDate=str(ini), endDate=str(self.periodo_meses_api()[1]), metrics=met,
                                         dimensions="month,insightTrafficSourceType", sort="month")
            regs = [{"mes": r["month"], "origem": r["insightTrafficSourceType"], "views": r["views"],
                     "minutos": r["estimatedMinutesWatched"]} for r in rs]
        except ErroHTTP as e:
            if e.status != 400:
                raise
            self.nota(arq, "a API não aceitou month+origem juntos; consultei mês a mês")
            m = ini
            while m <= fim:
                fm = fim_do_mes(m)
                for r in self.c.analytics_tabela(startDate=str(m), endDate=str(fm), metrics=met,
                                                 dimensions="insightTrafficSourceType", sort="-views"):
                    regs.append({"mes": f"{m:%Y-%m}", "origem": r["insightTrafficSourceType"], "views": r["views"],
                                 "minutos": r["estimatedMinutesWatched"]})
                m = fm + timedelta(days=1)
        total = {}
        for r in regs:
            total[r["mes"]] = total.get(r["mes"], 0) + float(r["views"] or 0)
        for r in regs:
            r["origem_pt"] = ORIGENS_PT.get(r["origem"], r["origem"])
            t = total.get(r["mes"]) or 0
            r["pct_views_mes"] = round(100 * float(r["views"] or 0) / t, 2) if t else ""
        self.gravar(arq, sorted(regs, key=lambda r: (r["mes"], -float(r["views"] or 0))))

    # -- 7. comentários
    def exportar_comentarios(self):
        arq = "comentarios_top30.csv"
        top = sorted(self.videos.values(), key=lambda v: -int(v.get("views") or 0))[:self.top_comentarios]
        self.c.log(f"7/7 comentários dos {len(top)} vídeos com mais views (contador público)")
        cid = self.estado.get("canal_id", "")
        regs = []

        def reg(c, vid, pai=""):
            sn = c["snippet"]
            autor = (sn.get("authorChannelId") or {}).get("value", "")
            return {"video_id": vid, "comentario_id": c["id"], "resposta_a": pai, "autor_canal_id": hash_autor(autor),
                    "eh_do_canal": int(bool(autor) and autor == cid),
                    "texto": sn.get("textOriginal") or sn.get("textDisplay", ""), "likes": sn.get("likeCount", 0),
                    "publicado_em": sn.get("publishedAt", ""), "eh_resposta": int(bool(pai))}

        for v in top:
            vid, token, paginas = v["id"], None, 0
            try:
                while paginas < self.max_paginas_coment:
                    p = {"part": "snippet,replies", "videoId": vid, "maxResults": 100, "textFormat": "plainText"}
                    if token:
                        p["pageToken"] = token
                    d = self.c.data_api("commentThreads", **p)
                    paginas += 1
                    for t in d.get("items", []):
                        topo = t["snippet"]["topLevelComment"]
                        regs.append(reg(topo, vid))
                        resp = (t.get("replies") or {}).get("comments", [])
                        if t["snippet"].get("totalReplyCount", 0) > len(resp):
                            resp = self.respostas(topo["id"])
                        regs += [reg(r, vid, topo["id"]) for r in resp]
                    token = d.get("nextPageToken")
                    if not token:
                        break
                if token:
                    self.nota(arq, f"{vid}: parei em {paginas} páginas de comentários (--max-paginas-comentarios)")
            except ErroHTTP as e:
                if e.status not in (403, 404):
                    raise
                self.nota(arq, f"{vid}: comentários indisponíveis ({e.motivo or e.status})")
        self.gravar(arq, regs)

    def respostas(self, pai):
        out, token = [], None
        while True:
            p = {"part": "snippet", "parentId": pai, "maxResults": 100, "textFormat": "plainText"}
            if token:
                p["pageToken"] = token
            d = self.c.data_api("comments", **p)
            out += d.get("items", [])
            token = d.get("nextPageToken")
            if not token:
                return out

    # -- termos de busca (opcional: --termos-busca)
    # A dimensão insightTrafficSourceDetail só aceita maxResults ≤ 25 e exige sort; com origem YT_SEARCH ela devolve
    # os termos buscados. Período: cada um dos últimos `meses_termos` meses fechados + o período inteiro; e, por vídeo,
    # os `n_videos_termos` vídeos com mais views da Pesquisa (de trafego_por_video.csv).
    def _termos(self, filtros, ini, fim):
        return self.c.analytics_tabela(startDate=str(ini), endDate=str(fim), dimensions="insightTrafficSourceDetail",
                                       metrics="views,estimatedMinutesWatched", filters=filtros, sort="-views",
                                       maxResults=25)

    def exportar_termos_busca(self, meses=12, n_videos=50):
        arq_c, arq_v = "termos_busca_canal.csv", "termos_busca_por_video.csv"
        self.c.log(f"termos de busca: canal ({meses} meses + total) e {n_videos} vídeos com mais views da Pesquisa")
        regs = []
        _, fim = self.periodo_meses()
        periodos = []
        m = meses_para_tras(fim, meses)
        while m <= fim:
            periodos.append((f"{m:%Y-%m}", m, fim_do_mes(m)))
            m = fim_do_mes(m) + timedelta(days=1)
        periodos.append(("total", self.desde, self.data_fim))
        for nome, ini, f_ in periodos:
            try:
                rs = self._termos("insightTrafficSourceType==YT_SEARCH", ini, f_)
            except ErroHTTP as e:
                if e.status != 400:
                    raise
                self.nota(arq_c, f"{nome}: a API recusou a consulta de termos ({e.mensagem[:120]})")
                continue
            regs += [{"periodo": nome, "posicao": k, "termo": r["insightTrafficSourceDetail"], "views": r["views"],
                      "minutos": r["estimatedMinutesWatched"]} for k, r in enumerate(rs, 1)]
        self.gravar(arq_c, regs)
        trafego = ler_csv(self.saida / "trafego_por_video.csv")
        busca = sorted(((float(r["views"] or 0), r["video_id"]) for r in trafego if r["origem"] == "YT_SEARCH"),
                       reverse=True)
        ids = [vid for _, vid in busca][:n_videos]
        if not ids:
            ids = self.ids_videos()[:n_videos]
            self.nota(arq_v, "trafego_por_video.csv ausente: usei os vídeos com mais views no contador público")
        out = []
        for vid in ids:
            try:
                rs = self._termos(f"video=={vid};insightTrafficSourceType==YT_SEARCH", self.desde, self.data_fim)
            except ErroHTTP as e:
                if e.status != 400:
                    raise
                self.nota(arq_v, f"a API recusou termos por vídeo ({e.mensagem[:120]})")
                break
            out += [{"video_id": vid, "titulo": self.videos.get(vid, {}).get("titulo", ""), "posicao": k,
                     "termo": r["insightTrafficSourceDetail"], "views": r["views"],
                     "minutos": r["estimatedMinutesWatched"]} for k, r in enumerate(rs, 1)]
        self.gravar(arq_v, out)
        self.nota(arq_c, "a API devolve no máximo 25 termos por consulta (maxResults ≤ 25 para insightTrafficSourceDetail)")

    def exportar_termos_recentes(self, dias=180, n_busca=50):
        """Termos dos últimos `dias` dias: todos os vídeos publicados no período e os `n_busca` com mais views da
        Pesquisa no vitalício (para ver quais termos antigos ainda trazem gente). Um arquivo só, sem o vitalício."""
        arq = "termos_busca_recentes.csv"
        ini = self.data_fim - timedelta(days=dias)
        novos = [v["id"] for v in sorted(self.videos.values(), key=lambda v: -int(v.get("views") or 0))
                 if v.get("publicado_em_brt", "")[:10] >= str(ini)]
        trafego = ler_csv(self.saida / "trafego_por_video.csv")
        busca = [vid for _, vid in sorted(((float(r["views"] or 0), r["video_id"]) for r in trafego
                                           if r["origem"] == "YT_SEARCH"), reverse=True)][:n_busca]
        ids = list(dict.fromkeys(novos + busca))
        self.c.log(f"termos recentes: {len(novos)} vídeos publicados desde {ini} + {len(busca)} com mais busca "
                   f"({len(ids)} consultas)")
        out = []
        for vid in ids:
            try:
                rs = self._termos(f"video=={vid};insightTrafficSourceType==YT_SEARCH", ini, self.data_fim)
            except ErroHTTP as e:
                if e.status != 400:
                    raise
                self.nota(arq, f"a API recusou termos por vídeo ({e.mensagem[:120]})")
                break
            v = self.videos.get(vid, {})
            out += [{"video_id": vid, "titulo": v.get("titulo", ""), "publicado": v.get("publicado_em_brt", "")[:10],
                     "desde": str(ini), "posicao": k, "termo": r["insightTrafficSourceDetail"], "views": r["views"],
                     "minutos": r["estimatedMinutesWatched"]} for k, r in enumerate(rs, 1)]
        self.gravar(arq, out)

    def leiame_termos(self):
        """No modo --termos-busca, só troca a seção dos termos no LEIAME_DADOS.md (o resto fica como estava)."""
        p = self.saida / "LEIAME_DADOS.md"
        txt = p.read_text(encoding="utf-8") if p.exists() else "# Dados exportados do canal (auditoria)\n"
        ini, fim = "<!-- termos-busca -->", "<!-- /termos-busca -->"
        if ini in txt:
            txt = txt[:txt.index(ini)] + txt[txt.index(fim) + len(fim):]
        L = [ini, f"## Termos de busca (exportados em {datetime.now(timezone.utc):%Y-%m-%d %H:%M UTC}; "
                  f"quota da Data API: {self.c.unidades_data}; consultas ao Analytics: {self.c.consultas_analytics})", ""]
        arqs = [a for a in ("termos_busca_canal.csv", "termos_busca_por_video.csv", "termos_busca_recentes.csv")
                if a in self.contagens or (self.saida / a).exists()]
        for arq in arqs:
            n = self.contagens.get(arq, len(ler_csv(self.saida / arq)))
            L += [f"### {arq} ({n} linhas)", ""] + [f"- `{c}`: {d}" for c, d in COLUNAS[arq]]
            L += [f"- Nota: {n}" for n in self.notas.get(arq, [])] + [""]
        L.append(fim)
        p.write_text(txt.rstrip("\n") + "\n\n" + "\n".join(L) + "\n", encoding="utf-8")

    # -- LEIAME
    def leiame(self, modo, interrompido=""):
        e = self.estado
        ini_m, fim_m = self.periodo_meses()
        L = ["# Dados exportados do canal (auditoria)", "",
             "Gerado por `exportar.py`. Não edite à mão: rode o exportador de novo.", "",
             f"- Exportação: {e.get('exportado_em')} (modo: {modo})",
             f"- Canal: {e.get('canal_titulo', '?')} (`{e.get('canal_id', '?')}`), criado em {e.get('canal_criado', '?')}; "
             f"inscritos no contador público: {e.get('inscritos_publico', '?')}",
             f"- Período por vídeo (Analytics): {self.desde} a {self.data_fim}",
             f"- Período mensal: {ini_m:%Y-%m} a {fim_m:%Y-%m} ({self.meses} meses fechados); diário: últimos {self.dias} dias",
             f"- Quota da Data API nesta execução: {self.c.unidades_data} unidades "
             f"(acumulado: {e.get('unidades_data_total', 0)}; limite do projeto: 10.000/dia)",
             f"- Consultas ao Analytics nesta execução: {self.c.consultas_analytics} "
             f"(acumulado: {e.get('consultas_analytics_total', 0)}); respostas vindas do cache: {self.c.do_cache}",
             f"- Fuso: horários em UTC e em Brasília (UTC-3). Formato: {CRITERIO_FORMATO}",
             "- Privacidade: os comentários não trazem nome do autor; `autor_canal_id` é um hash do id do canal.",
             "- Atenção: `views` de videos.csv é o contador público de hoje; `views` do Analytics é do período e "
             "pode diferir (o contador público conta views que o Analytics filtra, e vice-versa).", ""]
        if interrompido:
            L += [f"**EXPORTAÇÃO INCOMPLETA:** {interrompido} Rode o mesmo comando de novo (retoma do cache).", ""]
        for arq, colunas in COLUNAS.items():
            if arq.startswith("termos_busca"):
                continue
            n = self.contagens.get(arq)
            existe = (self.saida / arq).exists()
            st = f"{n} linhas" if n is not None else ("de uma execução anterior" if existe else "não gerado nesta execução")
            L += [f"## {arq} ({st})", ""]
            L += [f"- `{c}`: {d}" for c, d in colunas]
            vazias = self._colunas_vazias(arq) if existe else []
            if vazias:
                L.append(f"- **Colunas vazias:** {', '.join(vazias)}")
            for nt in self.notas.get(arq, []):
                L.append(f"- Nota: {nt}")
            L.append("")
        L += ["## Métricas que a API pode não entregar", "",
              "- Impressões e CTR das impressões: em geral só no YouTube Studio. Se as colunas vierem vazias, "
              "exporte em Studio > Análises > Modo avançado > Conteúdo (todo o período), com Impressões e Taxa de "
              "cliques, e salve o ZIP como `dados/studio/studio_conteudo_longos.zip` (e `..._shorts.zip`): "
              "o analisar.py lê esses arquivos.",
              "- Retenção nos primeiros 30 s (abertura): não existe por API para lista de vídeos; o proxy é "
              "averageViewPercentage.", ""]
        (self.saida / "LEIAME_DADOS.md").write_text("\n".join(L), encoding="utf-8")

    def _colunas_vazias(self, arq):
        rs = ler_csv(self.saida / arq)
        if not rs:
            return []
        return [c for c in rs[0] if all(not r.get(c) for r in rs)]


# ------------------------------------------------------------------------------------------------ plano / CLI
def plano(args, exp_dir=DADOS):
    vids = ler_csv(exp_dir / "videos.csv")
    n = len(vids) or 500
    base = "videos.csv já existe" if vids else "estimativa com 500 vídeos (ainda não há videos.csv)"
    pags = math.ceil(n / 50)
    data = 2 + 2 * pags
    coment = args.top_comentarios * 3
    det = min(n, args.max_videos_detalhe or n)
    print("PLANO (dry-run: nada vai para a rede, nenhuma credencial é lida)")
    print(f"  variáveis presentes: " + ", ".join(f"{v}={'sim' if os.environ.get(v) else 'NÃO'}"
                                                  for v in SEGREDOS + ("YT_CHANNEL_ID",)))
    print(f"  saída: {exp_dir}  (cache: {exp_dir / '.cache'})")
    print(f"  {base}: N = {n}")
    if not args.so_analytics:
        print(f"  Data API: channels (1-2) + playlistItems ({pags}) + videos ({pags}) = {data} unidades")
        print(f"            comentários de {args.top_comentarios} vídeos: ~{coment} unidades (1 por página de 100; "
              f"até {args.max_paginas_comentarios} páginas por vídeo, + respostas longas)")
    if not args.so_videos:
        print(f"  Analytics: por vídeo ~{4 * math.ceil(n / 200) + 6} consultas (lotes de 200 IDs); tráfego e inscritos "
              f"~{2 * math.ceil(det / 200)} em lote (ou {2 * det} vídeo a vídeo, se a API recusar o lote); "
              f"mês/dia/origem ~10  (não gasta a quota da Data API)")
        print(f"  período por vídeo: desde {args.desde or 'a criação do canal'}")
    total = (0 if args.so_analytics else data + coment)
    print(f"  TOTAL Data API estimado: ~{total} de 10.000 unidades/dia")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Exporta os dados do canal para a auditoria (só leitura).")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--so-videos", action="store_true", help="só Data API: videos.csv e comentarios_top30.csv")
    g.add_argument("--so-analytics", action="store_true", help="só YouTube Analytics")
    ap.add_argument("--desde", type=date.fromisoformat, help="AAAA-MM-DD; padrão: criação do canal")
    ap.add_argument("--dry-run", action="store_true", help="mostra o plano, sem rede")
    ap.add_argument("--recomecar", action="store_true", help="apaga o cache antes de começar")
    ap.add_argument("--pausa", type=float, default=0.3, help="segundos entre chamadas (padrão 0,3)")
    ap.add_argument("--top-comentarios", type=int, default=30)
    ap.add_argument("--max-paginas-comentarios", type=int, default=20, help="páginas de 100 por vídeo")
    ap.add_argument("--max-videos-detalhe", type=int, default=0, help="limita tráfego/inscritos por vídeo (0 = todos)")
    ap.add_argument("--meses", type=int, default=18)
    ap.add_argument("--saida", type=Path, default=DADOS)
    ap.add_argument("--termos-busca", action="store_true",
                    help="só a etapa opcional dos termos de busca (precisa de videos.csv e trafego_por_video.csv)")
    ap.add_argument("--termos-meses", type=int, default=12)
    ap.add_argument("--termos-recentes", type=int, default=0, metavar="DIAS",
                    help="só os termos dos últimos DIAS dias, por vídeo (publicados no período + 50 com mais busca)")
    ap.add_argument("--termos-videos", type=int, default=50)
    args = ap.parse_args(argv)

    if args.dry_run:
        plano(args, args.saida)
        if args.termos_busca:
            print(f"  --termos-busca: {args.termos_meses + 1} consultas no canal (1 por mês + total) e "
                  f"{args.termos_videos} por vídeo, todas no Analytics (maxResults = 25)")
        return 0
    faltam = [v for v in SEGREDOS if not os.environ.get(v)]
    if faltam:
        print("faltam variáveis de ambiente: " + ", ".join(faltam) + "\n(carregue o .env com set -a; source ...; set +a)",
              file=sys.stderr)
        return 2
    cache = args.saida / ".cache"
    if args.recomecar and cache.exists():
        shutil.rmtree(cache)
    cache.mkdir(parents=True, exist_ok=True)
    logf = (cache / "exportar.log").open("a", encoding="utf-8")

    def log(m):
        print(m, file=sys.stderr)
        logf.write(f"{datetime.now():%H:%M:%S} {m}\n")
        logf.flush()

    cli = Cliente(cache, pausa=args.pausa, log=log)
    exp = Exportador(cli, args.saida, args.desde, top_comentarios=args.top_comentarios,
                     max_paginas_coment=args.max_paginas_comentarios, meses=args.meses,
                     max_videos_detalhe=args.max_videos_detalhe)
    modo = "só vídeos" if args.so_videos else "só analytics" if args.so_analytics else "completo"
    interrompido, codigo = "", 0
    if args.termos_busca or args.termos_recentes:
        try:
            if args.termos_recentes:
                exp.exportar_termos_recentes(args.termos_recentes, args.termos_videos)
            else:
                exp.exportar_termos_busca(args.termos_meses, args.termos_videos)
        except QuotaEsgotada as e:
            interrompido, codigo = f"quota esgotada ({e}).", 3
        except ErroHTTP as e:
            interrompido, codigo = f"erro da API: {cli.limpar(e)}.", 1
            cli.log(f"ERRO: {e}")
        finally:
            exp.salvar_estado()
            exp.leiame_termos()
            cli.log(f"fim (termos de busca): {cli.consultas_analytics} consultas ao Analytics, {cli.do_cache} do cache"
                    + (f"; {interrompido}" if interrompido else ""))
            logf.close()
        return codigo
    try:
        exp.canal()
        if not args.so_analytics:
            exp.exportar_videos()
        if not args.so_videos:
            ids = exp.exportar_analytics_por_video()
            exp.exportar_canal_por_mes()
            exp.exportar_canal_por_dia()
            exp.exportar_trafego_por_mes()
            exp.exportar_por_video(ids)
        if not args.so_analytics:
            exp.exportar_comentarios()
    except QuotaEsgotada as e:
        interrompido, codigo = f"quota esgotada ({e}).", 3
        cli.log("QUOTA ESGOTADA: o que já veio está no cache; rode de novo amanhã (a quota zera à meia-noite do Pacífico).")
    except ErroHTTP as e:
        interrompido, codigo = f"erro da API: {cli.limpar(e)}.", 1
        cli.log(f"ERRO: {e}")
    finally:
        exp.salvar_estado()
        exp.leiame(modo, interrompido)
        cli.log(f"fim: {cli.unidades_data} unidades da Data API, {cli.consultas_analytics} consultas ao Analytics, "
            f"{cli.do_cache} do cache. Arquivos em {args.saida}")
        logf.close()
    return codigo


if __name__ == "__main__":
    sys.exit(main())
