#!/usr/bin/env python3
"""Coleta os comentários do canal Investir e Coçar e marca os que estão SEM RESPOSTA do canal.

SÓ LEITURA. Este script não posta, não responde, não oculta e não apaga nada: ele só chama endpoints .list.
Roda no Mac do Denis, com a mesma autorização do auditoria-canal/exportar.py (a classe Cliente de lá é
reaproveitada por import: troca do refresh token, retry, cache e filtro de segredos). Nenhum segredo fica neste
arquivo nem nos arquivos que ele grava.

Credenciais (variáveis de ambiente, as mesmas do exportar.py):
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN   OAuth; o token precisa do escopo youtube.force-ssl
                                                     (commentThreads/comments) e yt-analytics.readonly (views 28 d)
  YT_CHANNEL_ID (opcional)                           se faltar, sai de channels?mine=true
  YOUTUBE_API_KEY (só com --api-key)                 lê os comentários públicos com a chave, sem OAuth

Passos:
  1. canal: channels (1 unidade) -> playlist de uploads;
  2. vídeos: playlistItems part=snippet,contentDetails (1 unidade por página de 50);
  3. views dos últimos 28 dias por vídeo: YouTube Analytics (quota própria, não gasta a da Data API); se a
     autorização não permitir, a coluna fica vazia e a fila usa a data do vídeo;
  4. comentários: commentThreads part=snippet,replies, order=time, maxResults=100, com paginação (1 unidade por
     página). A thread traz só parte das respostas; se tiver mais respostas que as que vieram e nenhuma delas for do
     canal, busca as demais em comments.list (1 unidade por página de 100), a não ser com --sem-respostas-extras.

Saída (as duas no .gitignore):
  comentarios/dados/threads.csv          um comentário de topo por linha; tem nome de autor (dado de terceiros)
  comentarios/dados/respostas_canal.csv  as respostas do próprio canal (texto, data, thread); base do voz_denis.md

uso:
  python3 comentarios/coletar.py                     tudo
  python3 comentarios/coletar.py --dry-run           estimativa de cota, sem rede e sem credenciais
  python3 comentarios/coletar.py --max-unidades 3000 teto de unidades da Data API nesta execução (padrão 4000)
  python3 comentarios/coletar.py --dias 365          só comentários dos últimos N dias (para de paginar ao passar)
  python3 comentarios/coletar.py --fixture tests/fixture_api.json --saida /tmp/x.csv   teste, sem rede

Saída do processo: 0 = ok; 2 = faltou credencial; 3 = cota da API esgotada; 4 = parou no --max-unidades (o CSV
sai com o que deu tempo de coletar; rode de novo no dia seguinte, com o cache do dia ele retoma).
"""
import argparse
import csv
import json
import math
import os
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
sys.path.insert(0, str(AQUI.parent / "auditoria-canal"))
import regras  # noqa: E402
import exportar as ex  # noqa: E402  (Cliente, ErroHTTP, QuotaEsgotada, CANAL_PADRAO, BRT)

DADOS = AQUI / "dados"
THREADS = DADOS / "threads.csv"
RESPOSTAS = DADOS / "respostas_canal.csv"   # replies do canal: base do voz_denis.md (no .gitignore)
COLUNAS_RESPOSTAS = ["video_id", "thread_id", "reply_id", "publicado_em", "texto"]
COLUNAS = ["video_id", "video_titulo", "video_publicado", "views_28d", "comment_id", "autor", "publicado_em",
           "likes", "texto", "respostas_total", "respondido_pelo_canal", "sem_resposta", "eh_pergunta", "coletado_em"]
LIMITE_PADRAO = 4000


class LimiteCota(Exception):
    pass


# ---------------------------------------------------------------------------------------------- fixture (testes)
class ClienteFixture:
    """Responde como a API a partir de um JSON (ver tests/fixture_api.json). Conta unidades como a real."""

    def __init__(self, caminho):
        self.d = json.loads(Path(caminho).read_text(encoding="utf-8"))
        self.unidades_data = 0
        self.chamadas = []

    def log(self, msg):
        print(msg, file=sys.stderr)

    def _pagina(self, paginas, token):
        i = int(token or 0)
        out = {"items": paginas[i] if i < len(paginas) else []}
        if i + 1 < len(paginas):
            out["nextPageToken"] = str(i + 1)
        return out

    def data_api(self, recurso, oauth=False, custo=1, **p):
        self.unidades_data += custo
        self.chamadas.append((recurso, p))
        if recurso == "channels":
            return {"items": [{"id": self.d["canal_id"],
                               "contentDetails": {"relatedPlaylists": {"uploads": "UU" + self.d["canal_id"][2:]}}}]}
        if recurso == "playlistItems":
            itens = [{"snippet": {"title": v["titulo"]},
                      "contentDetails": {"videoId": v["id"], "videoPublishedAt": v["publicado_em"]}}
                     for v in self.d["videos"]]
            return self._pagina([itens[i:i + 50] for i in range(0, len(itens), 50)] or [[]], p.get("pageToken"))
        if recurso == "commentThreads":
            vid = p["videoId"]
            if vid in self.d.get("comentarios_desativados", []):
                raise ex.ErroHTTP(403, "commentsDisabled", "comentários desativados")
            return self._pagina(self.d["threads"].get(vid, [[]]), p.get("pageToken"))
        if recurso == "comments":
            return self._pagina([self.d.get("respostas", {}).get(p["parentId"], [])], p.get("pageToken"))
        raise ValueError(recurso)

    def analytics_tabela(self, **p):
        if self.d.get("analytics_negado"):
            raise ex.ErroHTTP(403, "forbidden", "escopo insuficiente")
        ids = p["filters"].split("==", 1)[1].split(",")
        return [{"video": v, "views": n} for v, n in self.d.get("views_28d", {}).items() if v in ids]


# ------------------------------------------------------------------------------------------------- coleta
class Coletor:
    def __init__(self, cliente, canal_id=None, max_unidades=LIMITE_PADRAO, dias=0, max_paginas=50,
                 respostas_extras=True, oauth=True, hoje=None):
        self.c, self.canal_id = cliente, canal_id
        self.max_unidades, self.dias, self.max_paginas = max_unidades, dias, max_paginas
        self.respostas_extras, self.oauth = respostas_extras, oauth
        self.hoje = hoje or datetime.now(ex.BRT).date()
        self.notas = []
        self.respostas_canal, self.vistas = [], set()

    def nota(self, t):
        self.notas.append(t)
        self.c.log("  nota: " + t)

    def api(self, recurso, oauth=None, **p):
        if self.c.unidades_data + 1 > self.max_unidades:
            raise LimiteCota(f"chegou ao teto de {self.max_unidades} unidades")
        return self.c.data_api(recurso, oauth=self.oauth if oauth is None else oauth, **p)

    def canal(self):
        if not self.canal_id:
            try:
                self.canal_id = self.api("channels", oauth=True, part="id", mine="true")["items"][0]["id"]
            except (ex.ErroHTTP, KeyError, IndexError) as e:
                self.canal_id = ex.CANAL_PADRAO
                self.nota(f"channels?mine=true falhou ({e}); usei o canal padrão")
        d = self.api("channels", part="contentDetails", id=self.canal_id)
        return d["items"][0]["contentDetails"]["relatedPlaylists"]["uploads"]

    def videos(self, uploads):
        out, token = [], None
        while True:
            p = {"part": "snippet,contentDetails", "playlistId": uploads, "maxResults": 50}
            if token:
                p["pageToken"] = token
            d = self.api("playlistItems", **p)
            for i in d.get("items", []):
                cd = i.get("contentDetails", {})
                out.append({"id": cd["videoId"], "titulo": i.get("snippet", {}).get("title", ""),
                            "publicado": (cd.get("videoPublishedAt") or "")[:10]})
            token = d.get("nextPageToken")
            if not token:
                return list({v["id"]: v for v in out}.values())

    def views_28d(self, ids):
        """{video_id: views} dos últimos 28 dias fechados; {} se a autorização não permitir (a fila usa a data)."""
        fim = self.hoje - timedelta(days=1)
        ini = fim - timedelta(days=27)
        out = {}
        try:
            for i in range(0, len(ids), 200):
                lote = ids[i:i + 200]
                for r in self.c.analytics_tabela(startDate=str(ini), endDate=str(fim), metrics="views",
                                                 dimensions="video", filters="video==" + ",".join(lote)):
                    out[r["video"]] = int(r.get("views") or 0)
        except (ex.ErroHTTP, SystemExit) as e:
            self.nota(f"Analytics indisponível ({e}); views_28d fica vazio e a fila usa a data do vídeo")
            return {}
        for v in ids:
            out.setdefault(v, 0)
        return out

    def do_canal(self, c):
        return (c.get("snippet", {}).get("authorChannelId") or {}).get("value", "") == self.canal_id

    def guardar_do_canal(self, itens, video_id, thread_id):
        """Guarda as respostas do próprio canal (texto, data, thread): é a base do voz_denis.md."""
        achou = False
        for r in itens:
            if self.do_canal(r) and r.get("id") not in self.vistas:
                self.vistas.add(r.get("id"))
                sn = r.get("snippet", {})
                self.respostas_canal.append({"video_id": video_id, "thread_id": thread_id, "reply_id": r.get("id", ""),
                                             "publicado_em": sn.get("publishedAt", ""),
                                             "texto": sn.get("textOriginal") or sn.get("textDisplay", "")})
            achou = achou or self.do_canal(r)
        return achou

    def respondida(self, thread):
        topo = thread["snippet"]["topLevelComment"]
        vid = topo.get("snippet", {}).get("videoId", "") or thread.get("snippet", {}).get("videoId", "")
        vieram = (thread.get("replies") or {}).get("comments", [])
        if self.guardar_do_canal(vieram, vid, topo["id"]):
            return True
        total = thread["snippet"].get("totalReplyCount", 0)
        if total > len(vieram) and self.respostas_extras:
            token = None
            while True:
                p = {"part": "snippet", "parentId": topo["id"], "maxResults": 100, "textFormat": "plainText"}
                if token:
                    p["pageToken"] = token
                d = self.api("comments", **p)
                if self.guardar_do_canal(d.get("items", []), vid, topo["id"]):
                    return True
                token = d.get("nextPageToken")
                if not token:
                    break
        return False

    def threads_do_video(self, v, views, coletado_em):
        regs, token, paginas = [], None, 0
        corte = (self.hoje - timedelta(days=self.dias)).isoformat() if self.dias else ""
        while paginas < self.max_paginas:
            p = {"part": "snippet,replies", "videoId": v["id"], "order": "time", "maxResults": 100,
                 "textFormat": "plainText"}
            if token:
                p["pageToken"] = token
            try:
                d = self.api("commentThreads", **p)
            except ex.ErroHTTP as e:
                if e.status in (403, 404):
                    self.nota(f"{v['id']}: comentários indisponíveis ({e.motivo or e.status})")
                    return regs
                raise
            paginas += 1
            velho = False
            for t in d.get("items", []):
                topo = t["snippet"]["topLevelComment"]
                sn = topo["snippet"]
                pub = sn.get("publishedAt", "")
                if corte and pub[:10] < corte:
                    velho = True  # order=time: daqui para frente só fica mais velho
                    break
                if self.do_canal(topo):
                    continue  # comentário do próprio canal (fixado, aviso): não é pergunta do público
                t["snippet"].setdefault("videoId", v["id"])
                resp = self.respondida(t)
                texto = sn.get("textOriginal") or sn.get("textDisplay", "")
                regs.append({"video_id": v["id"], "video_titulo": v["titulo"], "video_publicado": v["publicado"],
                             "views_28d": "" if views is None else views.get(v["id"], 0),
                             "comment_id": topo["id"], "autor": sn.get("authorDisplayName", ""), "publicado_em": pub,
                             "likes": sn.get("likeCount", 0), "texto": texto,
                             "respostas_total": t["snippet"].get("totalReplyCount", 0),
                             "respondido_pelo_canal": int(resp), "sem_resposta": int(not resp),
                             "eh_pergunta": int(regras.eh_pergunta(texto)), "coletado_em": coletado_em})
            token = d.get("nextPageToken")
            if velho or not token:
                break
        if token and paginas >= self.max_paginas:
            self.nota(f"{v['id']}: parei em {paginas} páginas (--max-paginas)")
        return regs

    def coletar(self):
        coletado_em = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        regs, interrompido = [], ""
        try:
            uploads = self.canal()
            vids = sorted(self.videos(uploads), key=lambda v: v["publicado"], reverse=True)
            self.c.log(f"{len(vids)} vídeos; views dos últimos 28 dias no Analytics")
            views = self.views_28d([v["id"] for v in vids]) or None
            for n, v in enumerate(vids, 1):
                regs += self.threads_do_video(v, views, coletado_em)
                if n % 50 == 0:
                    self.c.log(f"  {n}/{len(vids)} vídeos, {len(regs)} comentários, {self.c.unidades_data} unidades")
        except LimiteCota as e:
            interrompido = f"limite: {e}"
        except ex.QuotaEsgotada as e:
            interrompido = f"cota esgotada: {e}"
        return regs, interrompido


def gravar(caminho, regs, colunas=COLUNAS):
    caminho = Path(caminho)
    caminho.parent.mkdir(parents=True, exist_ok=True)
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=colunas)
        w.writeheader()
        w.writerows(regs)
    return len(regs)


def estimar(comentarios_por_video, frac_topo=0.5, frac_extras=0.03):
    """Unidades da Data API para uma coleta completa, a partir do total de comentários de cada vídeo (videos.csv).
    canal (2) + playlistItems (1 por 50 vídeos) + commentThreads (1 por página de 100 threads, mínimo 1 por vídeo)
    + comments.list (1 por thread com mais respostas do que as que vêm junto: ~3% das threads no top 30 de hoje).
    Na auditoria de 01/10/2026, metade dos comentários era de topo (6.039 de 12.318)."""
    n = len(comentarios_por_video)
    pl = math.ceil(n / 50)
    ct = sum(max(1, math.ceil(c * frac_topo / 100)) for c in comentarios_por_video)
    cm = math.ceil(sum(comentarios_por_video) * frac_topo * frac_extras)
    return {"videos": n, "canal": 2, "playlistItems": pl, "commentThreads": ct, "comments": cm,
            "total": 2 + pl + ct + cm}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Coleta comentários sem resposta do canal (só leitura; não posta nada).")
    ap.add_argument("--saida", type=Path, default=THREADS)
    ap.add_argument("--max-unidades", type=int, default=LIMITE_PADRAO, help="teto de unidades da Data API (padrão 4000)")
    ap.add_argument("--max-paginas", type=int, default=50, help="páginas de 100 threads por vídeo (padrão 50)")
    ap.add_argument("--dias", type=int, default=0, help="só comentários dos últimos N dias (0 = todos)")
    ap.add_argument("--sem-respostas-extras", action="store_true",
                    help="não busca respostas além das que vêm na thread (economiza cota; pode marcar como sem "
                         "resposta uma thread que o canal respondeu lá no fim)")
    ap.add_argument("--respostas", type=Path, default=None,
                    help="CSV das respostas do canal (padrão: respostas_canal.csv ao lado do --saida)")
    ap.add_argument("--api-key", action="store_true", help="lê comentários com YOUTUBE_API_KEY em vez do OAuth")
    ap.add_argument("--fixture", type=Path, help="JSON de exemplo no lugar da API (testes, sem rede)")
    ap.add_argument("--hoje", type=date.fromisoformat, help="data de referência (testes)")
    ap.add_argument("--dry-run", action="store_true", help="só a estimativa de cota")
    ap.add_argument("--pausa", type=float, default=0.3)
    a = ap.parse_args(argv)

    if a.dry_run:
        vcsv = AQUI.parent / "auditoria-canal" / "dados" / "videos.csv"
        coms = ([int(r.get("comentarios") or 0) for r in csv.DictReader(open(vcsv, encoding="utf-8"))]
                if vcsv.exists() else [50] * 1200)
        e = estimar(coms)
        print(f"PLANO (sem rede): {e['videos']} vídeos, {sum(coms)} comentários no contador público. Data API ~"
              f"{e['total']} unidades (canal {e['canal']} + playlistItems {e['playlistItems']} + commentThreads "
              f"~{e['commentThreads']} + comments ~{e['comments']}); teto desta execução: {a.max_unidades}; cota do "
              f"projeto: 10.000/dia. Analytics: ~{math.ceil(e['videos'] / 200)} consultas (quota separada).")
        return 0

    if a.fixture:
        cli = ClienteFixture(a.fixture)
        canal = cli.d["canal_id"]
    else:
        precisa = ["YOUTUBE_API_KEY"] if a.api_key else []
        precisa += ["YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN"]
        faltam = [v for v in precisa if not os.environ.get(v)]
        if faltam:
            print("faltam variáveis de ambiente: " + ", ".join(faltam)
                  + "\n(carregue o .env com set -a; source ...; set +a)", file=sys.stderr)
            return 2
        # cache por dia: retoma no mesmo dia sem gastar cota de novo; no dia seguinte, coleta fresca
        cache = DADOS / ".cache" / datetime.now(ex.BRT).date().isoformat()
        cli = ex.Cliente(cache, pausa=a.pausa)
        canal = os.environ.get("YT_CHANNEL_ID")
    col = Coletor(cli, canal, a.max_unidades, a.dias, a.max_paginas, not a.sem_respostas_extras,
                  oauth=not a.api_key, hoje=a.hoje)
    regs, interrompido = col.coletar()
    n = gravar(a.saida, regs)
    arq_resp = a.respostas or a.saida.with_name("respostas_canal.csv")
    nr = gravar(arq_resp, col.respostas_canal, COLUNAS_RESPOSTAS)
    print(f"{nr} respostas do canal em {arq_resp} (base do voz_denis.md: python3 comentarios/voz.py)", file=sys.stderr)
    sem = sum(1 for r in regs if r["sem_resposta"] and r["eh_pergunta"])
    print(f"{n} comentários de topo gravados em {a.saida}; {sem} perguntas sem resposta do canal; "
          f"{cli.unidades_data} unidades da Data API" + (f"; INTERROMPIDO ({interrompido})" if interrompido else ""),
          file=sys.stderr)
    if interrompido.startswith("cota"):
        return 3
    return 4 if interrompido else 0


if __name__ == "__main__":
    sys.exit(main())
