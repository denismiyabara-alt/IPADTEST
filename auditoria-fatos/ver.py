#!/usr/bin/env python3
"""Mostra os nós de texto de um post (rendered, com entidades convertidas) que casam com um padrão.
Uso: python3 auditoria-fatos/ver.py <post_id> <regex> [<regex> ...]
Ajuda a escolher 'de' seguros: marca com ⚠ os nós que têm caracteres que o WordPress transforma."""
import html
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auditar import carregar_posts  # noqa: E402
from patchlib import PROIBIDOS, nos_de_texto  # noqa: E402


def main():
    pid = int(sys.argv[1])
    pads = [re.compile(p, re.I) for p in sys.argv[2:]] or [re.compile(".")]
    post = next(p for p in carregar_posts() if p["id"] == pid)
    r = post["content"]["rendered"]
    for i, (a, b) in enumerate(nos_de_texto(r)):
        t = html.unescape(r[a:b])
        if not t.strip():
            continue
        if any(p.search(t) for p in pads):
            ruins = "".join(sorted({c for c in t if c in PROIBIDOS and c not in "\n"}))
            print(f"#{i}{' ⚠' + repr(ruins) if ruins else ''}: {t.strip()}")


if __name__ == "__main__":
    main()
