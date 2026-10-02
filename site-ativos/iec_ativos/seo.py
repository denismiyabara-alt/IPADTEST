"""SEO (DESENHO 6): JSON-LD, sitemap, redirecionamentos e testes de HTML (13, 14 e 15)."""
import csv
import json
import re
from html.parser import HTMLParser

from . import config


def jsonld(canonical: str, nome: str, data_mod: str, migalhas: list[tuple[str, str]], sobre: dict | None = None) -> str:
    """Um único bloco: WebPage (+ about) e BreadcrumbList. Sem FAQPage, Review, Product ou NewsArticle."""
    site = {"@type": "WebSite", "@id": config.SITE_URL + "/#website", "url": config.SITE_URL + "/", "name": config.SITE_NOME}
    org = {"@type": "Organization", "@id": config.SITE_URL + "/#organization", "name": config.SITE_NOME, "url": config.SITE_URL + "/"}
    pagina = {"@type": "WebPage", "@id": canonical + "#webpage", "url": canonical, "name": nome, "inLanguage": "pt-BR",
              "dateModified": data_mod, "isPartOf": {"@id": site["@id"]}, "publisher": {"@id": org["@id"]},
              "breadcrumb": {"@id": canonical + "#breadcrumb"}}
    if sobre:
        pagina["about"] = sobre
    trilha = {"@type": "BreadcrumbList", "@id": canonical + "#breadcrumb",
              "itemListElement": [{"@type": "ListItem", "position": i + 1, "name": n, "item": u}
                                  for i, (n, u) in enumerate(migalhas)]}
    grafo = {"@context": "https://schema.org", "@graph": [pagina, trilha, site, org]}
    return json.dumps(grafo, ensure_ascii=False).replace("</", "<\\/")


def sitemap(paginas: list[dict]) -> str:
    linhas = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for p in paginas:
        if p["indexavel"]:
            linhas.append(f"  <url><loc>{p['url']}</loc><lastmod>{p['lastmod']}</lastmod></url>")
    linhas.append("</urlset>")
    return "\n".join(linhas) + "\n"


def redirecionamentos(pasta, acoes_mvp: list[str], invalidos: list[str], base_ativos: str) -> None:
    """Mapa 301/410 das cotacao-* (DESENHO 6.6). Só gera os arquivos; nada é aplicado no site."""
    origem = config.SITE_URL
    linhas = [("de", "para", "codigo", "motivo")]
    for t in sorted(acoes_mvp):
        linhas.append((f"/cotacao-{t.lower()}/", f"{base_ativos}/acoes/{t.lower()}/", "301", "página nova do MVP"))
    for t in sorted(invalidos):
        linhas.append((f"/cotacao-{t}/", "", "410", "ticker inválido (lixo de importação)"))
    with open(pasta / "redirects.csv", "w", newline="") as f:
        csv.writer(f).writerows(linhas)
    absoluto = not base_ativos.startswith(origem)
    ht = ["# Exemplo para o .htaccess do WordPress. NÃO APLICADO. Gerado pelo iec-ativos.",
          "# Colocar ANTES do bloco '# BEGIN WordPress'. Conferir antes: exportar o Search Console das cotacao-*.",
          "# Só os tickers que já têm página nova; os demais cotacao-* continuam como estão (noindex).",
          "<IfModule mod_alias.c>"]
    for t in sorted(acoes_mvp):
        destino = f"{base_ativos}/acoes/{t.lower()}/" if absoluto else f"/acoes/{t.lower()}/"
        ht.append(f"  Redirect 301 /cotacao-{t.lower()}/ {destino}")
    for t in sorted(invalidos):
        ht.append(f"  Redirect gone /cotacao-{t}/")
    ht += ["</IfModule>",
           "# Quando TODOS os tickers estiverem cobertos, a lista pode virar uma regra só:",
           "# RedirectMatch 301 ^/cotacao-([a-z0-9]+)/?$ /acoes/$1/"]
    (pasta / "htaccess-exemplo.txt").write_text("\n".join(ht) + "\n")


# ------------------------------------------------------------------------- testes de HTML

PROIBIDAS = [r"\bcompre\b", r"\bvenda já\b", r"\bvender agora\b", r"vale a pena", r"\bbarat[ao]s?\b",
             r"\bcar[ao]s?\b", r"oportunidade", r"pre[çc]o[- ]alvo", r"melhor(es)? a[çc](ão|ões)", r"\baproveite\b",
             r"\brecomendamos\b", r"hora de (comprar|vender)"]
# frases de aviso exigidas pelo desenho (seção 7) que contêm palavras da lista
PERMITIDAS = [r"não é recomendação de compra ou venda", r"não é preço-alvo nem recomendação",
              r"não é preço-alvo", r"nem preço-alvo"]
CORRETORAS = [r"\bXP Investimentos\b", r"\bcorretora\b", r"\bRico\b", r"\bClear\b", r"\bBTG Pactual\b", r"\bÁgora\b",
              r"\bNuInvest\b", r"\bNubank\b", r"\bBanco Inter\b", r"\bInter Invest\b", r"\bModal\b", r"\bGenial\b",
              r"\bToro\b", r"\bAvenue\b", r"\bÓrama\b", r"\bEasynvest\b", r"\bWarren\b", r"\bC6\b", r"abra (sua )?conta"]


class _Leitor(HTMLParser):
    VAZIAS = {"meta", "link", "br", "img", "input", "hr", "source", "area", "base", "col", "wbr", "path", "line",
              "circle", "rect", "stop"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.pilha, self.erros, self.texto = [], [], []
        self.h1 = 0
        self.title = ""
        self._em_title = self._em_script = False
        self.jsonld = 0
        self.canonical = []
        self.numeros_sem_fonte = []
        self.n_numeros = 0

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "h1":
            self.h1 += 1
        if tag == "title":
            self._em_title = True
        if tag == "script":
            self._em_script = True
            if a.get("type") == "application/ld+json":
                self.jsonld += 1
        if tag == "link" and a.get("rel") == "canonical":
            self.canonical.append(a.get("href"))
        cls = (a.get("class") or "").split()
        if "n" in cls or "nd" in cls or (tag == "td" and "num" in cls):
            self.n_numeros += 1
            if not a.get("data-fonte") or not a.get("data-ref"):
                self.numeros_sem_fonte.append(f"<{tag} class={a.get('class')}>")
        if tag not in self.VAZIAS:
            self.pilha.append(tag)

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        if tag not in self.VAZIAS and self.pilha and self.pilha[-1] == tag:
            self.pilha.pop()

    def handle_endtag(self, tag):
        if tag == "title":
            self._em_title = False
        if tag == "script":
            self._em_script = False
        if tag in self.VAZIAS:
            return
        if tag in self.pilha:
            while self.pilha and self.pilha[-1] != tag:
                aberta = self.pilha.pop()
                if aberta not in ("p", "li", "td", "th", "tr", "option"):
                    self.erros.append(f"<{aberta}> não fechada antes de </{tag}>")
            self.pilha.pop()
        else:
            self.erros.append(f"</{tag}> sem abertura")

    def handle_data(self, data):
        if self._em_title:
            self.title += data
        if not self._em_script:
            self.texto.append(data)


def verificar_html(html: str, nomes_emissores: list[str], titulo_base: str) -> list[dict]:
    """Testes 13, 14 e 15 sobre o HTML pronto. Devolve a lista de resultados."""
    p = _Leitor()
    p.feed(html)
    p.close()
    out = []
    out.append({"teste": 13, "nome": "Todo número tem data-fonte e data-ref", "tipo": "bloqueante",
                "ok": not p.numeros_sem_fonte, "tolerancia": "100%",
                "detalhe": f"{p.n_numeros} números; sem fonte: {p.numeros_sem_fonte[:3]}"})
    # 14: palavras proibidas e corretoras, no texto visível, nos atributos e nos scripts (que montam texto)
    texto = " ".join(p.texto) + " " + " ".join(re.findall(r'(?:title|alt|aria-label|content)="([^"]*)"', html))
    scripts = " ".join(re.findall(r"<script(?![^>]*ld\+json)[^>]*>(.*?)</script>", html, flags=re.S))
    alvo = (texto + " " + scripts)
    for frase in PERMITIDAS:
        alvo = re.sub(frase, " ", alvo, flags=re.I)
    for nome in nomes_emissores:  # o emissor pode aparecer como emissor (ex.: Banco BTG Pactual, XP Malls)
        if nome:
            alvo = re.sub(re.escape(nome), " ", alvo, flags=re.I)
    achados = [m.group(0) for pat in PROIBIDAS for m in re.finditer(pat, alvo, flags=re.I)]
    out.append({"teste": 14, "nome": "Sem palavras de recomendação", "tipo": "bloqueante", "ok": not achados,
                "tolerancia": "zero", "detalhe": f"achadas: {sorted(set(achados))}" if achados else "ok"})
    corr = [m.group(0) for pat in CORRETORAS for m in re.finditer(pat, alvo)]
    out.append({"teste": 14, "nome": "Sem citar corretora", "tipo": "bloqueante", "ok": not corr, "tolerancia": "zero",
                "detalhe": f"achadas: {sorted(set(corr))}" if corr else "ok"})
    erros15 = []
    if p.h1 != 1:
        erros15.append(f"{p.h1} h1")
    if len(titulo_base) > 60:
        erros15.append(f"title com {len(titulo_base)} caracteres (sem o sufixo do site)")
    if p.jsonld != 1:
        erros15.append(f"{p.jsonld} blocos JSON-LD")
    if len(p.canonical) != 1:
        erros15.append(f"{len(p.canonical)} canonical")
    if p.erros or p.pilha:
        erros15.append(f"HTML: {(p.erros + ['abertas no fim: ' + ','.join(p.pilha)] if p.pilha else p.erros)[:3]}")
    try:
        bloco = re.search(r'<script type="application/ld\+json">(.*?)</script>', html, flags=re.S).group(1)
        json.loads(bloco)
    except Exception as e:  # noqa: BLE001
        erros15.append(f"JSON-LD inválido: {e}")
    out.append({"teste": 15, "nome": "HTML válido, um H1, title ≤ 60, um JSON-LD, canonical", "tipo": "bloqueante",
                "ok": not erros15, "tolerancia": "100%", "detalhe": "; ".join(erros15) or "ok"})
    return out
