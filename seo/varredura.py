#!/usr/bin/env python3
"""Varredura de SEO só leitura do investirecocaresocomecar.com.br.

Regras: no máximo 1 requisição por segundo, sem login, para na primeira resposta 429 ou 403.
Saída: seo/varredura.csv, seo/varredura.json e o HTML bruto em seo/_html/ (fora do git).

Uso: python3 seo/varredura.py
"""
import csv
import json
import re
import sys
import time
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urldefrag, urljoin, urlparse

from bs4 import BeautifulSoup

SITE = "https://investirecocaresocomecar.com.br"
HOSTS = {"investirecocaresocomecar.com.br", "www.investirecocaresocomecar.com.br"}
UA = "Mozilla/5.0 (compatible; IEC-auditoria-SEO/1.0; leitura publica, 1 req/s)"
AQUI = Path(__file__).resolve().parent
HTML_DIR = AQUI / "_html"
INTERVALO = 1.1

_ultima = [0.0]


class Parar(Exception):
    pass


def baixar(url):
    espera = INTERVALO - (time.time() - _ultima[0])
    if espera > 0:
        time.sleep(espera)
    _ultima[0] = time.time()
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "pt-BR"})
    try:
        r = urllib.request.urlopen(req, timeout=30)
        return r.status, r.geturl(), r.read(), dict(r.headers)
    except urllib.error.HTTPError as e:
        if e.code in (403, 429):
            raise Parar(f"{e.code} em {url}")
        return e.code, url, e.read(), dict(e.headers)


def locs(xml):
    return re.findall(r"<loc>\s*(.*?)\s*</loc>", xml.decode("utf-8", "replace"))


def norm(u):
    u = urldefrag(u)[0]
    p = urlparse(u)
    if p.netloc not in HOSTS:
        return None
    path = p.path or "/"
    if not path.endswith("/") and "." not in path.rsplit("/", 1)[-1]:
        path += "/"
    return f"https://investirecocaresocomecar.com.br{path}"


def conteudo(soup):
    for sel in (".entry-content", "article", "main"):
        el = soup.select_one(sel)
        if el:
            return el
    return soup.body or soup


def analisar(url, status, final, html, headers):
    soup = BeautifulSoup(html, "lxml")
    meta = lambda **a: soup.find_all("meta", attrs=a)
    canon = [l.get("href", "") for l in soup.find_all("link", rel="canonical")]
    robots = [m.get("content", "") for m in meta(name=re.compile("^robots$", re.I))]
    desc = [m.get("content", "") for m in meta(name=re.compile("^description$", re.I))]
    title = soup.title.get_text(strip=True) if soup.title else ""
    corpo = conteudo(soup)
    for t in corpo.find_all(["script", "style", "noscript", "nav", "aside", "form"]):
        t.decompose()
    palavras = len(re.findall(r"\w+", corpo.get_text(" "), re.U))
    links_conteudo = {n for a in corpo.find_all("a", href=True) if (n := norm(urljoin(final, a["href"])))}
    ldjson = soup.find_all("script", type="application/ld+json")
    texto_ld = " ".join(s.get_text() for s in ldjson)
    upload_sem_fuso = re.findall(r'"uploadDate"\s*:\s*"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)"', texto_ld)
    imgs = soup.find_all("img")
    return {
        "url": url,
        "status": status,
        "final": final,
        "canonical": canon[0] if canon else "",
        "n_canonical": len(canon),
        "canonical_ok": bool(canon) and norm(canon[0]) == norm(final),
        "robots": " | ".join(robots),
        "n_meta_robots": len(robots),
        "noindex": any("noindex" in r.lower() for r in robots) or "noindex" in headers.get("X-Robots-Tag", "").lower(),
        "title": title,
        "title_len": len(title),
        "n_title": len(soup.find_all("title")),
        "desc_len": len(desc[0]) if desc else 0,
        "n_desc": len(desc),
        "n_h1": len(soup.find_all("h1")),
        "palavras": palavras,
        "links_saida_conteudo": len(links_conteudo),
        "n_og_title": len(meta(property="og:title")),
        "n_og_url": len(meta(property="og:url")),
        "n_og_image": len(meta(property="og:image")),
        "n_twitter_card": len(meta(name="twitter:card")),
        "n_ldjson": len(ldjson),
        "yoast_schema": bool(soup.select("script.yoast-schema-graph")),
        "wpsso": "wpsso" in html.decode("utf-8", "replace").lower(),
        "upload_sem_fuso": len(upload_sem_fuso),
        "html_kb": round(len(html) / 1024, 1),
        "n_scripts": len(soup.find_all("script", src=True)),
        "n_css": len(soup.find_all("link", rel="stylesheet")),
        "n_img": len(imgs),
        "img_sem_dim": sum(1 for i in imgs if not (i.get("width") and i.get("height"))),
        "wpo_min": len(re.findall(r"/wpo-minify/", html.decode("utf-8", "replace"))),
        "_links": sorted(links_conteudo),
    }


def main():
    HTML_DIR.mkdir(exist_ok=True)
    log = []
    try:
        st, _, idx, _ = baixar(SITE + "/sitemap_index.xml")
        filhos = locs(idx)
        log.append(f"sitemap_index.xml: {st}, {len(filhos)} sitemaps")
        urls, por_mapa = [], {}
        for f in filhos:
            st, _, xml, _ = baixar(f)
            lista = locs(xml)
            por_mapa[f] = {"status": st, "urls": len(lista)}
            urls += lista
        urls = list(dict.fromkeys(urls))
        log.append(f"{len(urls)} URLs nos sitemaps")
        resultados = []
        for i, u in enumerate(urls, 1):
            st, final, html, hd = baixar(u)
            (HTML_DIR / (re.sub(r"[^a-z0-9]+", "-", urlparse(u).path.lower()).strip("-") or "home")).with_suffix(".html").write_bytes(html)
            resultados.append(analisar(u, st, final, html, hd))
            if i % 50 == 0:
                print(f"{i}/{len(urls)}", flush=True)
        cotacoes_links = sorted({l for r in resultados for l in r["_links"] if "/cotacao-" in l})
        amostra = []
        for u in cotacoes_links[:5]:
            st, final, html, hd = baixar(u)
            amostra.append(analisar(u, st, final, html, hd))
        parado = None
    except Parar as e:
        parado = str(e)
        print("PAROU:", parado, flush=True)
        resultados = locals().get("resultados", [])
        por_mapa = locals().get("por_mapa", {})
        cotacoes_links, amostra = [], []

    recebidos = Counter()
    origens = defaultdict(set)
    for r in resultados:
        for l in r["_links"]:
            if l != norm(r["url"]):
                origens[l].add(r["url"])
    for r in resultados:
        r["links_recebidos"] = len(origens.get(norm(r["url"]), ()))

    campos = [k for k in resultados[0] if not k.startswith("_")] if resultados else []
    with open(AQUI / "varredura.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        w.writerows(resultados)
    json.dump({"log": log, "parado": parado, "sitemaps": por_mapa, "cotacoes_linkadas": cotacoes_links,
               "amostra_cotacoes": amostra, "resultados": resultados},
              open(AQUI / "varredura.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("\n".join(log), f"\nresultados: {len(resultados)}  parado: {parado}")


if __name__ == "__main__":
    sys.exit(main())
