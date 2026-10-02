#!/usr/bin/env python3
"""Auditoria de erros de fato nos posts do investirecocaresocomecar.com.br (SÓ LEITURA).

Etapas:
  python3 auditoria-fatos/auditar.py baixar   # API pública do WP, 1 req/s, cache em auditoria-fatos/cache/
  python3 auditoria-fatos/auditar.py varrer   # varredura automática em todos os posts -> cache/varredura.json
  python3 auditoria-fatos/auditar.py tudo     # baixar + varrer

Nada é enviado ao site: só GET na API pública /wp-json/wp/v2/posts, sem login.
Fontes locais reaproveitadas (não baixa de novo):
  - site-ativos/cache/dados.sqlite: preco_diario (COTAHIST B3 2021-2026: ticker -> nome de pregão),
    empresa (cadastro CVM), macro (SGS do BCB: 11 Selic diária, 12 CDI, 432 meta Selic, 433 IPCA, 13522 IPCA 12m)
  - seo/varredura.json: sitemap e links internos recebidos (proxy de tráfego)
  - site-ativos/saida/: páginas geradas que linkam posts
Regras de IR e fatos de referência conferidos à mão: auditoria-fatos/referencia.py (com link da fonte).
"""
import gzip
import html
import json
import re
import sqlite3
import sys
import time
import urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
CACHE = AQUI / "cache"
API = "https://investirecocaresocomecar.com.br/wp-json/wp/v2/posts"
CAMPOS = "id,link,slug,date,modified,title,content,categories,tags"
UA = "IEC-auditoria-fatos/1.0 (leitura publica da API, 1 req/s)"
INTERVALO = 1.1
DB = RAIZ / "site-ativos" / "cache" / "dados.sqlite"

_ultima = [0.0]


def get(url):
    espera = INTERVALO - (time.time() - _ultima[0])
    if espera > 0:
        time.sleep(espera)
    _ultima[0] = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:
        if r.status in (403, 429):
            raise SystemExit(f"parado: HTTP {r.status} em {url}")
        return r.status, dict(r.headers), r.read()


def baixar():
    CACHE.mkdir(parents=True, exist_ok=True)
    pagina, total_paginas = 1, None
    while True:
        destino = CACHE / f"posts_p{pagina}.json"
        if destino.exists():
            dados = json.loads(destino.read_text())
            meta = json.loads((CACHE / f"posts_p{pagina}.meta.json").read_text())
        else:
            url = f"{API}?per_page=100&page={pagina}&orderby=id&order=asc&_fields={CAMPOS}"
            _, cab, corpo = get(url)
            dados = json.loads(corpo)
            meta = {k.lower(): v for k, v in cab.items() if k.lower() in ("x-wp-total", "x-wp-totalpages", "last-modified")}
            meta["url"] = url
            destino.write_text(json.dumps(dados, ensure_ascii=False))
            (CACHE / f"posts_p{pagina}.meta.json").write_text(json.dumps(meta))
            print(f"página {pagina}: {len(dados)} posts (total {meta.get('x-wp-total')})")
        total_paginas = int(meta.get("x-wp-totalpages", 1))
        if pagina >= total_paginas:
            break
        pagina += 1


def carregar_posts():
    posts = []
    for f in sorted(CACHE.glob("posts_p*.json")):
        if f.name.endswith(".meta.json"):
            continue
        posts.extend(json.loads(f.read_text()))
    return posts


def texto(html_str):
    """HTML do post -> texto plano com quebras de bloco."""
    s = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", html_str)
    s = re.sub(r"(?i)<br\s*/?>", "\n", s)
    s = re.sub(r"(?i)</(p|h[1-6]|li|tr|div|table|blockquote|figcaption)>", "\n", s)
    s = re.sub(r"(?i)</t[dh]>", " | ", s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = html.unescape(s)
    s = re.sub(r"[ \t ]+", " ", s)
    s = re.sub(r"\n\s*\n+", "\n", s)
    return s.strip()


if __name__ == "__main__":
    etapa = sys.argv[1] if len(sys.argv) > 1 else "tudo"
    if etapa in ("baixar", "tudo"):
        baixar()
    if etapa in ("varrer", "tudo"):
        from varredura import varrer  # noqa: E402  (auditoria-fatos/varredura.py)
        varrer(carregar_posts())
