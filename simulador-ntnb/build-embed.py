#!/usr/bin/env python3
"""Gera embed-wordpress.html a partir de index.html.

O resultado é um trecho único (sem <html>/<head>/<body>) para colar num bloco
"HTML personalizado" do WordPress ou num widget HTML do Elementor. Todo o CSS
fica preso dentro de #sim-ntnb, para não interferir no tema do site, e o modo
escuro é removido para o simulador seguir o visual claro da página.

Uso: python3 simulador-ntnb/build-embed.py
"""
import re
from pathlib import Path

AQUI = Path(__file__).parent
ROOT = "#sim-ntnb"

src = (AQUI / "index.html").read_text(encoding="utf-8")
css = re.search(r"<style>(.*?)</style>", src, re.S).group(1)
corpo = re.search(r"<body>(.*?)<script>", src, re.S).group(1)
js = re.search(r"<script>(.*?)</script>", src, re.S).group(1)


def blocos(texto):
    """Divide CSS em (prelúdio, conteúdo) respeitando chaves aninhadas."""
    out, i = [], 0
    while i < len(texto):
        a = texto.find("{", i)
        if a < 0:
            break
        nivel, j = 1, a + 1
        while nivel:
            nivel += {"{": 1, "}": -1}.get(texto[j], 0)
            j += 1
        out.append((texto[i:a].strip(), texto[a + 1:j - 1]))
        i = j
    return out


def escopo(sel):
    sel = sel.strip()
    if sel in (":root", "body"):
        return ROOT
    if sel == "*":
        return f"{ROOT},{ROOT} *"
    return f"{ROOT} {sel}"


def converter(texto):
    regras = []
    for pre, conteudo in blocos(texto):
        if pre.startswith("@media"):
            if "prefers-color-scheme" in pre:
                continue  # sem modo escuro no embed
            regras.append(f"{pre}{{{converter(conteudo)}}}")
        elif pre.startswith(":root[") or pre == "html,body":
            continue
        else:
            sels = ",".join(escopo(s) for s in pre.split(","))
            regras.append(f"{sels}{{{conteudo.strip()}}}")
    return "\n".join(regras)


css_novo = converter(css)
# Fundo transparente para herdar o fundo da página do site
css_novo = css_novo.replace(f"{ROOT}{{background:var(--bg);", f"{ROOT}{{background:transparent;", 1)
# Reforça contra estilos genéricos de temas (botões, tabelas, inputs)
css_novo += (
    f"\n{ROOT} button,{ROOT} input,{ROOT} select{{box-shadow:none;text-transform:none;letter-spacing:normal;min-height:0;margin:0}}"
    f"\n{ROOT} table{{margin:0;border:0;background:transparent}}{ROOT} th,{ROOT} td{{border-left:0;border-right:0;border-top:0;background:transparent}}"
    f"\n{ROOT} h1,{ROOT} h2,{ROOT} h3{{font-family:inherit;color:var(--text)}}"
)

corpo = corpo.replace("<h1>", '<h2 class="titulo">').replace("</h1>", "</h2>")
css_novo = css_novo.replace(f"{ROOT} header h1{{", f"{ROOT} header h2.titulo{{")

js_novo = (
    js.replace('document.querySelectorAll(".tab")', 'document.getElementById("sim-ntnb").querySelectorAll(".tab")')
      .replace('document.querySelectorAll(".panel")', 'document.getElementById("sim-ntnb").querySelectorAll(".panel")')
      .replace("getComputedStyle(document.documentElement)", 'getComputedStyle(document.getElementById("sim-ntnb"))')
)
assert 'document.querySelectorAll' not in js_novo

saida = (
    "<!-- Simulador de marcação a mercado NTN-B · Investir e Coçar -->\n"
    "<!-- Arquivo gerado por build-embed.py a partir de index.html. Não edite à mão. -->\n"
    f"<style>\n{css_novo}\n</style>\n"
    f'<div id="sim-ntnb">\n{corpo.strip()}\n</div>\n'
    f"<script>{js_novo}</script>\n"
)
# Sem linhas em branco: evita que o WordPress insira <p> no meio do código
saida = "\n".join(l for l in saida.splitlines() if l.strip()) + "\n"
(AQUI / "embed-wordpress.html").write_text(saida, encoding="utf-8")
print(f"embed-wordpress.html gerado ({len(saida):,} bytes)")
