#!/usr/bin/env python3
"""Sugere links internos para as páginas órfãs, a partir do HTML já baixado pela varredura.

Não faz nenhuma requisição ao site. Lê seo/varredura.json e seo/_html/ (gerados por varredura.py).
Para cada página órfã, procura as 3 páginas com texto mais parecido (TF-IDF + cosseno) que ainda
não linkam para ela, e sugere um texto âncora. No fim, acrescenta os links das ferramentas do plugin.

Páginas duplicadas que devem receber 301 ficam de fora, como origem e como destino.

Saída: seo/sugestoes-links.csv
"""
import csv
import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup

AQUI = Path(__file__).resolve().parent
SUFIXO = re.compile(r"\s*[-|–]\s*Investir e Coçar\s*$")
FORA = re.compile(r"/(category|author)/|/(termos-de-uso|politica-de-privacidade|links|llms-txt|sobre|artigos)"
                  r"|-vale-a-pena-2/|-vale-a-pena-investir-2/|/como-funciona-um-fundo-imobiliario-entenda-agora/")
STOP = set("""a o os as um uma uns umas de da do das dos em no na nos nas por para pra com sem sob sobre e ou
que se seu sua seus suas ao aos à às é ser são foi era como mais menos muito muita muitos muitas já não sim
isso esse essa este esta isto ele ela eles elas você vocês nós eu me te lhe mas porque quando onde qual quais
há ter tem têm tinha pode podem vai vão também só ainda entre até depois antes então assim cada todo toda todos
todas outro outra outros outras mesmo mesma bem quem sua nosso nossa ano anos hoje investir coçar""".split())


def arquivo(url):
    p = re.sub(r"[^a-z0-9]+", "-", urlparse(url).path.lower()).strip("-") or "home"
    return AQUI / "_html" / f"{p}.html"


def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


def tokens(texto):
    return [w for w in re.findall(r"[a-z0-9]{3,}", sem_acento(texto.lower())) if w not in STOP]


def texto_conteudo(html):
    s = BeautifulSoup(html, "lxml")
    corpo = s.select_one(".entry-content") or s.select_one("article") or s.body
    for t in corpo.find_all(["script", "style", "nav", "aside", "form", "noscript"]):
        t.decompose()
    titulo = s.title.get_text(strip=True) if s.title else ""
    return titulo, corpo.get_text(" ")


def main():
    dados = json.load(open(AQUI / "varredura.json", encoding="utf-8"))["resultados"]
    pags = {}
    for r in dados:
        f = arquivo(r["url"])
        if not f.exists():
            continue
        titulo, texto = texto_conteudo(f.read_bytes())
        tit = SUFIXO.sub("", titulo)
        pags[r["url"]] = {"r": r, "titulo": tit, "tf": Counter(tokens(tit + " " + tit + " " + texto)), "links": set(r["_links"])}

    n = len(pags)
    df = Counter(w for p in pags.values() for w in p["tf"])
    for p in pags.values():
        vec = {w: (1 + math.log(c)) * math.log(n / df[w]) for w, c in p["tf"].items()}
        norma = math.sqrt(sum(v * v for v in vec.values())) or 1
        p["vec"] = {w: v / norma for w, v in vec.items()}

    def cos(a, b):
        if len(a) > len(b):
            a, b = b, a
        return sum(v * b.get(w, 0) for w, v in a.items())

    def norm(u):
        return "https://investirecocaresocomecar.com.br" + urlparse(u).path

    alvos = [u for u, p in pags.items() if p["r"]["links_recebidos"] == 0 and not p["r"]["noindex"]
             and not FORA.search(u) and p["r"]["palavras"] >= 400]
    fontes = [u for u, p in pags.items() if p["r"]["palavras"] >= 400 and not p["r"]["noindex"] and not FORA.search(u)]

    linhas = []
    for alvo in alvos:
        pa = pags[alvo]
        cands = sorted(((cos(pa["vec"], pags[f]["vec"]), f) for f in fontes
                        if f != alvo and norm(alvo) not in pags[f]["links"]), reverse=True)[:3]
        for pos, (sim, f) in enumerate(cands, 1):
            if sim < 0.08:
                continue
            linhas.append({"tipo": "orfao", "destino": urlparse(alvo).path, "titulo_destino": pa["titulo"],
                           "origem": urlparse(f).path, "titulo_origem": pags[f]["titulo"], "ordem": pos,
                           "similaridade": round(sim, 3), "ancora_sugerida": pa["titulo"].split("?")[0].split(":")[0].strip()})

    ferramentas = {
        "/simulador-ntnb/": ("simulador de marcação a mercado da NTN-B", ["tesouro-ipca", "ntn-b", "ntnb", "marcacao-a-mercado", "tesouro-direto"]),
        "(nova página) renda-fii": ("simulador de renda mensal com FIIs", ["fundo-imobiliario", "fundos-imobiliarios", "fii", "ifix", "dividendos-mensais"]),
        "/calculadora-lci/ (após fundir com LCA)": ("calculadora LCI e LCA × CDB", ["lci", "lca", "cdb", "renda-fixa", "fgc"]),
        "/calculadora-juros-anual-para-mensal/": ("conversor de juros anual para mensal", ["selic", "cdi", "juros", "inflacao", "poupanca"]),
        "/calculadora-renda-fixa/": ("comparador de renda fixa", ["renda-fixa", "cdb", "tesouro", "prefixado", "ipca", "selic"]),
        "/perfil-de-investidor/": ("quiz de perfil de investidor", ["perfil", "comecar", "iniciante", "reserva-de-emergencia", "onde-investir"]),
        "(nova página) preco-justo": ("calculadora de preço justo (Bazin e Graham)", ["preco-justo", "bazin", "graham", "valuation", "pl-acoes", "pvp", "dividend"]),
    }
    for destino, (ancora, chaves) in ferramentas.items():
        origens = [u for u in fontes if any(k in urlparse(u).path for k in chaves)]
        origens.sort(key=lambda u: -pags[u]["r"]["links_recebidos"])
        for pos, u in enumerate(origens[:8], 1):
            linhas.append({"tipo": "ferramenta", "destino": destino, "titulo_destino": ancora, "origem": urlparse(u).path,
                           "titulo_origem": pags[u]["titulo"], "ordem": pos, "similaridade": "", "ancora_sugerida": ancora})

    with open(AQUI / "sugestoes-links.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    orfaos = len({l["destino"] for l in linhas if l["tipo"] == "orfao"})
    print(f"{len(alvos)} órfãos elegíveis, {orfaos} com sugestão, {len(linhas)} linhas no CSV")


if __name__ == "__main__":
    main()
