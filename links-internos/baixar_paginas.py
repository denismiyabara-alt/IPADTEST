#!/usr/bin/env python3
"""Baixa as páginas publicadas pela API pública do WordPress para links-internos/cache/pages_p<N>.json.

Só leitura, sem login, 1 requisição por segundo. É daqui que o gerar_links.py tira em que URL cada ferramenta do
plugin está publicada (o shortcode [iec_ferramenta id=...] aparece no rendered como <div id="..." class="iec-ferramenta">).

Uso: python3 links-internos/baixar_paginas.py
"""
import json
import time
import urllib.request
from pathlib import Path

CACHE = Path(__file__).resolve().parent / "cache"
URL = ("https://investirecocaresocomecar.com.br/wp-json/wp/v2/pages?per_page=100&page={}"
       "&_fields=id,link,slug,status,modified,title,content")


def main():
    CACHE.mkdir(exist_ok=True)
    pagina, total = 1, 1
    while pagina <= total:
        req = urllib.request.Request(URL.format(pagina), headers={"User-Agent": "IEC-links-internos/1.0"})
        with urllib.request.urlopen(req, timeout=60) as r:
            total = int(r.headers.get("X-WP-TotalPages", "1"))
            dados = json.loads(r.read())
        (CACHE / f"pages_p{pagina}.json").write_text(json.dumps(dados, ensure_ascii=False), encoding="utf-8")
        print(f"página {pagina}/{total}: {len(dados)} páginas")
        pagina += 1
        time.sleep(1)


if __name__ == "__main__":
    main()
