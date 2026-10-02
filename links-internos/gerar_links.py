#!/usr/bin/env python3
"""Gera patches de links internos (lotes L1, L2 e L3) no formato do auditoria-fatos/aplicar_patches.py.

Só leitura: usa o cache dos posts (auditoria-fatos/cache/posts_p*.json), o cache das páginas
(links-internos/cache/pages_p1.json, baixado da API pública), a varredura de SEO (seo/varredura.json,
seo/sugestoes-links.csv) e os achados da auditoria (auditoria-fatos/achados.csv). Não altera nada na
auditoria-fatos: importa o patchlib.py e o carregar_posts() de lá.

Uso: python3 links-internos/gerar_links.py
Saída: links-internos/patches/<post_id>.json, patches/LOTE_L1.json, LOTE_L2.json, LOTE_L3.json e resumo.csv
(uma linha por link, com a situação de órfão do destino antes e depois).

Regras de cada troca (as mesmas do gerar_patches.py, mais as de link):
- o "de" é um trecho seguro (patchlib.problemas_do_de) e está dentro de UM nó de texto do rendered;
- o "de" aparece 1 vez no texto do post todo, inclusive dentro de <script> (o "para" tem aspas duplas no href e
  não pode cair num JSON-LD);
- o nó de texto está num <p>, <li>, <td> ou <blockquote>, fora de <a>, títulos, botões, FAQ e índice;
- a âncora é um termo que já está na frase (nada é reescrito, o termo só vira link);
- no máximo 3 links novos por post, nenhum destino repetido no post, nenhum destino que o post já linka;
- nenhum link para post que vai ser redirecionado ou despublicado, para cotacao-* ou para post com achado CRÍTICO
  (exceto os corrigidos nos lotes A/B);
- para os posts que também estão nos lotes A/B, o "de" continua único depois de aplicar as trocas de lá
  (a ordem de aplicação no Mac não importa).
"""
import csv
import html
import json
import math
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent
AF = RAIZ / "auditoria-fatos"
sys.path.insert(0, str(AF))
from auditar import carregar_posts  # noqa: E402
from patchlib import localizar_no_rendered, problemas_do_de  # noqa: E402

SITE = "https://investirecocaresocomecar.com.br"
SAIDA = AQUI / "patches"
MAX_POR_POST = 3

# posts que o RELATORIO da auditoria-fatos manda redirecionar (301) ou despublicar: nem origem nem destino
REDIRECIONADOS = {1033, 998, 1073, 1083, 1113, 1178, 1183,
                  983, 1003, 1013, 1038, 1063, 1068, 1078, 1098, 1128, 1168, 1188, 1193}
# duplicados exatos do seo/RELATORIO.md (vão para 301)
DUPLICADOS = ("-vale-a-pena-2/", "-vale-a-pena-investir-2/", "-vale-a-pena-investir-3/",
              "/como-funciona-um-fundo-imobiliario-entenda-agora/")

# posts que o RELATORIO manda reescrever: um patch de link se perderia na reescrita
REESCREVER = {1008, 1043, 1158, 4816}
# sem link em frase que cita o JEPQ39 (produto que não existe na B3; vai sair dos posts)
# nem em aviso legal ("não é recomendação de compra ou venda")
FRASE_RUIM = re.compile(r"JEPQ39|recomendação de compra ou venda|não é recomendação", re.I)
FII = r"\bFIIs?\b|\bcotas?\b|fundos? imobiliários?"

# ---------------------------------------------------------------- destinos
# ancoras: regex, em ordem de preferência (a primeira que casar num nó elegível vira link)
# tema: regex que mede se o post fala do assunto (mínimo "min_tema" ocorrências no texto)
FERRAMENTAS = [
    dict(id="simulador-ntnb", url=f"{SITE}/simulador-ntnb/", nome="Simulador de marcação a mercado do Tesouro IPCA+",
         ancoras=[r"marcação a mercado", r"Tesouro IPCA\+ ?20[0-9]{2}", r"NTN-Bs?"],
         tema=r"tesouro ipca|ntn-b|marcação a mercado", min_tema=3),
    dict(id="renda-fii", url=f"{SITE}/simulador-renda-fii/", nome="Simulador de renda mensal com FIIs",
         ancoras=[r"renda (?:mensal|passiva) com (?:FIIs|fundos imobiliários)",
                  (r"rendimentos? mensa(?:l|is)", FII), (r"renda (?:mensal|passiva)", FII)],
         tema=r"fundos? imobiliários?|\bFIIs?\b", min_tema=6),
    dict(id="lci-lca-cdb", url=f"{SITE}/calculadora-lci-lca-cdb/", nome="Calculadora LCI/LCA × CDB",
         ancoras=[r"LCIs? e LCAs?", r"LCAs? e LCIs?", r"LCIs? ou LCAs?", r"\bLCIs?\b", r"\bLCAs?\b"],
         tema=r"\bLC[IA]s?\b", min_tema=3),
    dict(id="juros-anual-mensal", url=f"{SITE}/calculadora-juros-anual-para-mensal/",
         nome="Calculadora de juros anual para mensal",
         ancoras=[r"taxa (?:equivalente )?mensal", r"juros (?:ao mês|mensais)", r"taxa ao mês"],
         tema=r"ao mês|ao ano|a\.m\.|a\.a\.|mensal", min_tema=4),
    dict(id="renda-fixa-comparador", url=f"{SITE}/calculadora-cdb-lci-prefixado-ipca/",
         nome="Comparador de renda fixa (CDB, LCI, prefixado e IPCA+)",
         ancoras=[r"tabela regressiva(?: do (?:Imposto de Renda|IR))?", r"CDBs? prefixados?", r"Tesouro Prefixado",
                  r"títulos? prefixados?", r"prefixados?"],
         tema=r"\bCDBs?\b|prefixad|tesouro|renda fixa", min_tema=5),
    dict(id="perfil-investidor", url=f"{SITE}/quiz-perfil-de-investidor/", nome="Quiz de perfil de investidor",
         ancoras=[r"perfil de investidor", r"seu perfil(?: de risco)?", r"perfil (?:conservador|moderado|arrojado)",
                  r"tolerância (?:a|ao) risco"],
         tema=r"perfil|iniciante|conservador|arrojad", min_tema=2),
    dict(id="preco-justo", url=f"{SITE}/calculadora-preco-justo/", nome="Calculadora de preço justo (Bazin e Graham)",
         ancoras=[r"preço justo", r"preço[- ]teto", r"(?:método|fórmula|modelo) (?:de )?(?:Bazin|Graham)",
                  r"Décio Bazin", r"Benjamin Graham"],
         tema=r"preço justo|preço[- ]teto|bazin|graham|valuation|P/L|P/VP", min_tema=2),
    dict(id="um-milhao", url=f"{SITE}/calculadora-1-milhao/", nome="Calculadora: quanto falta para juntar 1 milhão",
         ancoras=[r"primeiro milhão", r"(?:juntar|acumular|chegar (?:a|ao|em)) (?:R\$ ?)?(?:1|um) milhão",
                  r"aportes? mensa(?:l|is)", r"juros compostos"],
         tema=r"milhão|aporte|juros compostos|patrimônio", min_tema=3),
    dict(id="jcp-liquido", url=f"{SITE}/calculadora-jcp-liquido/", nome="Calculadora de JCP líquido",
         ancoras=[r"juros sobre (?:o )?capital próprio", r"\bJCP\b"],
         tema=r"\bJCP\b|juros sobre (?:o )?capital próprio", min_tema=2),
    dict(id="aposentadoria-renda", url=f"{SITE}/calculadora-aposentadoria-renda-passiva/",
         nome="Calculadora de aposentadoria com renda passiva e INSS",
         ancoras=[r"independência financeira", r"aposentadoria", r"se aposentar", r"viver de renda"],
         tema=r"aposentad|aposentar|INSS|independência financeira|viver de", min_tema=3),
    dict(id="ir-fii-venda", url=f"{SITE}/calculadora-ir-venda-fii/", nome="Calculadora de IR na venda de FII",
         ancoras=[(r"ganho de capital", FII), (r"venda (?:das|de) (?:suas )?cotas", FII), (r"\bDARF\b", FII),
                  (r"imposto na venda", FII)],
         tema=r"fundos? imobiliários?|\bFIIs?\b", min_tema=4),
]
GUIAS = [
    dict(id=4873, nome="Dividendos e dividend yield (guia)",
         ancoras=[r"dividend yield", r"\bDY\b"], tema=r"dividend", min_tema=4),
    dict(id=4874, nome="Fundos imobiliários (guia completo)",
         ancoras=[r"fundos imobiliários", r"fundo imobiliário"], tema=r"fundos? imobiliários?|\bFIIs?\b", min_tema=4),
    dict(id=5091, nome="O que é BOVA11",
         ancoras=[r"\bBOVA11\b"], tema=r"BOVA11|Ibovespa|\bETFs?\b", min_tema=3),
    dict(id=1053, nome="Itaúsa × Itaú (ITSA4 × ITUB4)",
         ancoras=[r"ITSA4 (?:ou|e|x|vs\.?) ITUB4", r"ITUB4 (?:ou|e|x|vs\.?) ITSA4", r"Itaúsa e (?:o )?Itaú\b",
                  r"Itaú e (?:a )?Itaúsa", (r"\bITUB4\b", r"Itaúsa|ITSA4")], tema=r"Itaúsa|ITSA4|ITUB4|Itaú", min_tema=3),
    dict(id=993, nome="Quem a Itaúsa controla (as 7 empresas)",
         ancoras=[r"empresas (?:da|que a) Itaúsa", r"holding do Itaú", r"\bItaúsa\b", r"\bITSA4\b"],
         tema=r"Itaúsa|ITSA4|holding", min_tema=3),
    dict(id=4537, nome="ETFs de dividendos mensais (JEPI39)",
         ancoras=[r"\bJEPI39\b", r"ETFs? (?:que pagam|de) dividendos mensais", r"ETFs? de dividendos"],
         tema=r"\bETFs?\b|JEPI|dividendos mensais", min_tema=3),
]
QUOTA_FERRAMENTA = 8
QUOTA_GUIA = 10
QUOTA_ORFAO = 2

# âncoras ruins (genéricas) e palavras de ligação para as âncoras do L3
ANCORA_RUIM = re.compile(r"(?i)^(clique aqui|aqui|leia mais|saiba mais|este post|neste link)$")


# ---------------------------------------------------------------- utilidades
def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")


STOP = set("""a o os as um uma de da do das dos em no na nos nas por para pra com sem sobre e ou que se seu sua
seus suas ao aos a as e ser sao foi como mais menos muito ja nao sim isso esse essa este esta ele ela voce mas
porque quando onde qual quais ha ter tem pode vai tambem so ainda entre ate depois antes entao assim cada todo
toda todos todas outro outra mesmo bem ano anos hoje investir cocar""".split())


def tokens(t):
    return [w for w in re.findall(r"[a-z0-9]{3,}", sem_acento(t.lower())) if w not in STOP]


def sem_scripts(h):
    return re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", h)


def texto_plano(h):
    return html.unescape(re.sub(r"<[^>]+>", " ", sem_scripts(h)))


VAZIAS = {"br", "img", "hr", "input", "meta", "link", "source", "wbr", "col", "area", "embed", "param", "track"}
BLOCOS_OK = {"p", "li", "blockquote"}
PROIBIDO_ANCESTRAL = {"a", "h1", "h2", "h3", "h4", "h5", "h6", "button", "summary", "script", "style", "nav",
                      "figcaption", "th", "code", "pre", "label", "select", "option", "textarea", "svg", "title"}
CLASSE_RUIM = re.compile(r"faq|toc|indice|table-of-contents|lwptoc|ez-toc|wp-block-buttons|cta|related|leia-tambem",
                         re.I)


def nos_elegiveis(rendered):
    """(inicio, fim, texto_sem_entidades) dos nós de texto onde dá para pôr um link."""
    out, pilha, pos = [], [], 0
    padrao = re.compile(r"<!--.*?-->|<(/?)([a-zA-Z][a-zA-Z0-9-]*)([^>]*)>", re.S)
    i = 0
    while True:
        m = padrao.search(rendered, i)
        fim_txt = m.start() if m else len(rendered)
        if fim_txt > pos:
            tags = [t for t, _ in pilha]
            classes = " ".join(c for _, c in pilha)
            blocos = [t for t in tags if t in BLOCOS_OK]
            if blocos and not (set(tags) & PROIBIDO_ANCESTRAL) and not CLASSE_RUIM.search(classes):
                out.append((pos, fim_txt, html.unescape(rendered[pos:fim_txt])))
        if not m:
            break
        i = pos = m.end()
        if m.group(0).startswith("<!--"):
            continue
        fecha, tag, attrs = m.group(1), m.group(2).lower(), m.group(3) or ""
        if tag in ("script", "style") and not fecha:
            f = re.search(r"(?is)</%s\s*>" % tag, rendered[m.end():])
            i = pos = m.end() + (f.end() if f else len(rendered))
            continue
        if fecha:
            for k in range(len(pilha) - 1, -1, -1):
                if pilha[k][0] == tag:
                    del pilha[k:]
                    break
        elif tag not in VAZIAS and not attrs.rstrip().endswith("/"):
            if tag == "p":  # <p> não aninha: fecha o anterior
                while pilha and pilha[-1][0] == "p":
                    pilha.pop()
            c = re.search(r'class="([^"]*)"', attrs)
            pilha.append((tag, c.group(1) if c else ""))
    return out


SEGURO = re.compile(r"[^\"'“”‘’«»–—…×&<>\n\r\t ]")


def montar_de(txt_total, no, a, b, alvo_rendered=None):
    """Recorta em volta de no[a:b] um 'de' seguro e único no post. Devolve (de, ini_ancora, fim_ancora) ou None."""
    # limite do trecho seguro em volta da âncora (sem caracteres que o WordPress mexe), dentro da frase
    esq = a
    while esq > 0 and SEGURO.match(no[esq - 1]) and not (no[esq - 1] in ".!?;:" and no[esq:esq + 1] == " "):
        esq -= 1
    dirt = b
    while dirt < len(no) and SEGURO.match(no[dirt]) and no[dirt] not in "!?;":
        if no[dirt] == "." and (dirt + 1 >= len(no) or no[dirt + 1] == " "):
            dirt += 1  # inclui o ponto final
            break
        dirt += 1
    # cresce de 15 em 15 caracteres até ficar único
    for lado in range(15, 200, 15):
        i = max(esq, a - lado)
        j = min(dirt, b + lado)
        if i > esq:  # começa no início de uma palavra
            k = no.find(" ", i)
            i = k + 1 if 0 <= k < a else i
        if j < dirt:  # termina no fim de uma palavra
            k = no.rfind(" ", b, j)
            j = k if k >= b else j
        de = no[i:j].strip(" ,")
        off = no[i:j].find(de)
        ini = a - i - off
        if ini < 0 or de[ini:ini + (b - a)] != no[a:b]:
            continue
        if problemas_do_de(de) or re.search(r"\d\s*x\s*\d", de):
            if i == esq and j == dirt:
                return None
            continue
        if txt_total.count(de) == 1:
            return de, ini, ini + (b - a)
        if i == esq and j == dirt:
            return None
    return None


def carregar():
    posts = {p["id"]: p for p in carregar_posts()}
    arqs = sorted((AQUI / "cache").glob("pages_p*.json"))
    if not arqs:
        raise SystemExit("sem cache das páginas: rode python3 links-internos/baixar_paginas.py")
    paginas = [x for f in arqs for x in json.loads(f.read_text(encoding="utf-8"))]
    varr = {r["url"]: r for r in json.loads((RAIZ / "seo" / "varredura.json").read_text(encoding="utf-8"))["resultados"]}
    achados = list(csv.DictReader(open(AF / "achados.csv", encoding="utf-8")))
    corrigidos = {int(p.stem) for p in (AF / "patches").glob("*.json") if p.stem.isdigit()}
    criticos = {int(a["post_id"]) for a in achados if a["classe"] == "CRÍTICO"} - corrigidos
    trocas_ab = {}
    for pid in corrigidos:
        trocas_ab[pid] = json.loads((AF / "patches" / f"{pid}.json").read_text(encoding="utf-8"))["trocas"]
    return posts, paginas, varr, criticos, corrigidos, trocas_ab


def caminho(url):
    return re.sub(r"^https?://[^/]+", "", url)


def ja_linka(rendered, url):
    p = re.escape(caminho(url).rstrip("/"))
    return re.search(r'href="(?:https?://(?:www\.)?investirecocaresocomecar\.com\.br)?%s/?(?:[#?][^"]*)?"' % p,
                     rendered) is not None


class Vetores:
    def __init__(self, textos):
        tf = {k: Counter(tokens(t)) for k, t in textos.items()}
        n = len(tf)
        df = Counter(w for c in tf.values() for w in c)
        self.v = {}
        for k, c in tf.items():
            vec = {w: (1 + math.log(x)) * math.log(n / df[w]) for w, x in c.items()}
            nr = math.sqrt(sum(x * x for x in vec.values())) or 1
            self.v[k] = {w: x / nr for w, x in vec.items()}

    def cos(self, a, b):
        a, b = self.v[a], self.v[b]
        if len(a) > len(b):
            a, b = b, a
        return sum(x * b.get(w, 0) for w, x in a.items())


# ---------------------------------------------------------------- candidatos
def achar_troca(post, url, ancoras, trocas_ab, ja_usados, trechos_achados=()):
    """Primeira âncora (na ordem de preferência) num nó elegível que dá um 'de' seguro e único."""
    r = post["content"]["rendered"]
    txt_total = html.unescape(r)
    nos = nos_elegiveis(r)
    for padrao in ancoras:
        padrao, ctx = padrao if isinstance(padrao, tuple) else (padrao, None)
        rx = re.compile(r"(?<![\w/-])(?:%s)(?![\w-])" % padrao, re.I)
        for _, _, no in nos:
            if FRASE_RUIM.search(no) or (ctx and not re.search(ctx, no, re.I)):
                continue
            if any(t in no or no.strip() in t for t in trechos_achados if len(no.strip()) > 20):
                continue
            for m in rx.finditer(no):
                if ANCORA_RUIM.match(m.group(0)):
                    continue
                res = montar_de(txt_total, no, m.start(), m.end())
                if not res:
                    continue
                de, ia, fa = res
                if any(de in u or u in de for u in ja_usados):
                    continue
                _, de_r = localizar_no_rendered(r, de)
                if de_r is None:
                    continue
                # continua único depois dos lotes A/B e não encosta nas trocas de lá
                para = de[:ia] + f'<a href="{url}">' + de[ia:fa] + "</a>" + de[fa:]
                if not compativel_com_ab(txt_total, de, para, trocas_ab.get(post["id"], [])):
                    continue
                return {"de": de, "para": para, "de_rendered": de_r, "ancora": de[ia:fa]}
    return None


def compativel_com_ab(txt_total, de, para, trocas_ab_post):
    """O link e as trocas dos lotes A/B do mesmo post não se atrapalham, em qualquer ordem de aplicação."""
    depois_ab = txt_total
    for t in trocas_ab_post:
        alvo = html.unescape(t["de"])
        if alvo in de or de in alvo:
            return False
        depois_ab = depois_ab.replace(alvo, html.unescape(t["para"]))
    if depois_ab.count(de) != 1:
        return False
    depois_link = txt_total.replace(de, para)
    for t in trocas_ab_post:
        alvo = html.unescape(t["de"])
        if depois_link.count(alvo) != txt_total.count(alvo):
            return False
    return True


def main():
    posts, paginas, varr, criticos, corrigidos, trocas_ab = carregar()
    # trechos com achado da auditoria (qualquer classe): o link não entra nessas frases, que ainda vão mudar
    trechos = defaultdict(list)
    for a in csv.DictReader(open(AF / "achados.csv", encoding="utf-8")):
        for parte in re.split(r"\s*\|\s*|\.\.\.|…", a["trecho"]):
            if len(parte.strip()) >= 15:
                trechos[int(a["post_id"])].append(parte.strip())
    pag_por_slug = {p["slug"]: p for p in paginas}
    for f in FERRAMENTAS:
        cont = [p for p in paginas if re.search(r'<div id="[a-z0-9_-]+" class="iec-ferramenta', p["content"]["rendered"])
                and caminho(p["link"]) == caminho(f["url"])]
        if not cont:
            raise SystemExit(f"ferramenta {f['id']} sem página publicada em {f['url']} (rode links-internos/baixar_paginas.py)")
    # origens: posts do sitemap, fora dos que vão sair do ar
    def excluido(p):
        return (p["id"] in REDIRECIONADOS or p["id"] in REESCREVER or "elementor" in p["slug"] or p["slug"].startswith("cotacao") or any(d in p["link"] for d in DUPLICADOS)
                or p["link"] not in varr or varr[p["link"]]["noindex"])
    origens = {pid: p for pid, p in posts.items() if not excluido(p) and varr[p["link"]]["palavras"] >= 300}

    textos = {("post", pid): texto_plano(p["content"]["rendered"]) + " " + html.unescape(p["title"]["rendered"]) * 2
              for pid, p in posts.items() if not p["slug"].startswith("cotacao")}
    for f in FERRAMENTAS:
        pg = pag_por_slug[caminho(f["url"]).strip("/")]
        textos[("ferr", f["id"])] = texto_plano(pg["content"]["rendered"]) + (" " + f["nome"]) * 3
    vet = Vetores(textos)

    def trafego(pid):
        return varr[posts[pid]["link"]]["links_recebidos"]

    def tema_ok(pid, d):
        return len(re.findall(d["tema"], textos[("post", pid)], re.I)) >= d["min_tema"]

    destinos = []
    for f in FERRAMENTAS:
        destinos.append(dict(lote="L1", chave=("ferr", f["id"]), url=f["url"], nome=f["nome"], ancoras=f["ancoras"],
                             tema=f["tema"], min_tema=f["min_tema"], quota=QUOTA_FERRAMENTA, post_id=None))
    for g in GUIAS:
        if g["id"] in criticos or g["id"] in REDIRECIONADOS:
            raise SystemExit(f"guia {g['id']} tem CRÍTICO sem patch")
        destinos.append(dict(lote="L2", chave=("post", g["id"]), url=posts[g["id"]]["link"], nome=g["nome"],
                             ancoras=g["ancoras"], tema=g["tema"], min_tema=g["min_tema"], quota=QUOTA_GUIA,
                             post_id=g["id"]))

    # L3: órfãos do seo/sugestoes-links.csv que ainda são órfãos, com as origens sugeridas lá
    orfaos = defaultdict(list)
    for l in csv.DictReader(open(RAIZ / "seo" / "sugestoes-links.csv", encoding="utf-8")):
        if l["tipo"] == "orfao":
            orfaos[l["destino"]].append(l["origem"])
    por_caminho = {caminho(p["link"]): p for p in posts.values()}
    ja_destino = {d["post_id"] for d in destinos if d["post_id"]}
    for cam, srcs in orfaos.items():
        p = por_caminho.get(cam)
        if not p or p["id"] in criticos or p["id"] in REDIRECIONADOS or p["id"] in ja_destino or excluido(p):
            continue
        anc = ancoras_do_titulo(html.unescape(p["title"]["rendered"]), p["slug"])
        if not anc:
            continue
        destinos.append(dict(lote="L3", chave=("post", p["id"]), url=p["link"], nome=html.unescape(p["title"]["rendered"]),
                             ancoras=anc, tema=None, min_tema=0, quota=QUOTA_ORFAO, post_id=p["id"],
                             sugeridas=[por_caminho[s]["id"] for s in srcs if s in por_caminho]))

    # pares candidatos por destino, ordenados por relevância (similaridade × tráfego provável da origem)
    cands = {}
    for d in destinos:
        lista = []
        pool = d.get("sugeridas") if d["lote"] == "L3" else origens
        for pid in pool:
            if pid not in origens or pid == d["post_id"] or caminho(posts[pid]["link"]) == caminho(d["url"]):
                continue
            p = origens[pid]
            if ja_linka(p["content"]["rendered"], d["url"]):
                continue
            if d["tema"] and not tema_ok(pid, d):
                continue
            sim = vet.cos(("post", pid), d["chave"])
            if sim < {"L1": 0.04, "L2": 0.08, "L3": 0.05}[d["lote"]]:
                continue
            score = sim * (1 + 0.25 * math.log1p(trafego(pid)))
            lista.append((score, sim, pid))
        lista.sort(reverse=True)
        cands[id(d)] = lista

    # rodízio: em cada rodada cada destino pega a melhor origem livre; um post fica num lote só
    escolha = defaultdict(list)       # pid -> [trocas]
    lote_do_post = {}
    recebidos = defaultdict(list)     # url destino -> [pid]
    for lote in ("L2", "L1", "L3"):  # guias primeiro: as âncoras deles são mais raras
        ds = [d for d in destinos if d["lote"] == lote]
        pos = {id(d): 0 for d in ds}
        mudou = True
        while mudou:
            mudou = False
            for d in ds:
                if len(recebidos[d["url"]]) >= d["quota"]:
                    continue
                lista = cands[id(d)]
                while pos[id(d)] < len(lista):
                    score, sim, pid = lista[pos[id(d)]]
                    pos[id(d)] += 1
                    if lote_do_post.get(pid, lote) != lote or len(escolha[pid]) >= MAX_POR_POST:
                        continue
                    if any(t["url"] == d["url"] for t in escolha[pid]):
                        continue
                    t = achar_troca(posts[pid], d["url"], d["ancoras"], trocas_ab, [x["de"] for x in escolha[pid]],
                                    trechos[pid])
                    if not t:
                        continue
                    t.update(url=d["url"], destino=d["nome"], sim=round(sim, 3))
                    escolha[pid].append(t)
                    lote_do_post[pid] = lote
                    recebidos[d["url"]].append(pid)
                    mudou = True
                    break

    gravar(posts, escolha, lote_do_post, destinos, recebidos, varr, trocas_ab)
    resumir(posts, paginas, escolha, lote_do_post, destinos)


def resumir(posts, paginas, escolha, lote_do_post, destinos):
    """resumo.csv: um link por linha; diz se o destino era órfão (nenhum link no conteúdo de outro post/página)."""
    conteudos = [(x["id"], x["content"]["rendered"]) for x in list(posts.values()) + paginas
                 if not x["slug"].startswith("cotacao")]
    nome = {d["url"]: (d["lote"], d["nome"]) for d in destinos}
    linhas = []
    for pid, trocas in sorted(escolha.items()):
        if not (SAIDA / f"{pid}.json").exists():
            continue
        for t in trocas:
            linhas.append({"lote": lote_do_post[pid], "origem_id": pid, "origem": caminho(posts[pid]["link"]),
                           "destino": caminho(t["url"]), "destino_nome": nome[t["url"]][1], "ancora": t["ancora"],
                           "similaridade": t["sim"], "de": t["de"], "para": t["para"]})
    orfao = {}
    for url in {l["destino"] for l in linhas}:
        alvo_id = next((d["post_id"] for d in destinos if caminho(d["url"]) == url), None)
        orfao[url] = not any(ja_linka(c, SITE + url) for i, c in conteudos if i != alvo_id)
    for l in linhas:
        l["destino_era_orfao"] = "sim" if orfao[l["destino"]] else "não"
    with open(AQUI / "resumo.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    resolvidos = sorted(u for u, o in orfao.items() if o)
    print(f"órfãos que passam a receber link: {len(resolvidos)}")
    for u in resolvidos:
        print("   ", u)


def ancoras_do_titulo(titulo, slug):
    """Âncoras para um órfão: os tickers do título (com o verbo do tema, quando houver) e o nome antes do ':'."""
    tickers = re.findall(r"\b[A-Z]{4}(?:3|4|5|6|11|33|34|39)\b", titulo)
    anc = []
    for t in tickers:
        anc.append(re.escape(t))
    return anc


def validar(rendered, trocas, trocas_ab_post):
    """Mesmas regras do gerar_patches.validar, para o conjunto final de trocas do post."""
    erros = []
    txt_total = html.unescape(rendered)
    simulado = txt_total
    for t in trocas:
        de = t["de"]
        p = problemas_do_de(de)
        if p:
            erros.append(f"de inseguro ({'; '.join(p)}): {de}")
        if re.search(r"[\\\n]", t["para"]):
            erros.append(f"para com barra/quebra: {t['para']}")
        if txt_total.count(de) != 1:
            erros.append(f"de aparece {txt_total.count(de)}x: {de}")
        n, de_r = localizar_no_rendered(rendered, de)
        if de_r is None or de_r != t["de_rendered"]:
            erros.append(f"de fora de um nó de texto: {de}")
        if simulado.count(de) != 1:
            erros.append(f"de alterado por troca anterior: {de}")
        simulado = simulado.replace(de, t["para"])
        if html.unescape(re.sub(r"<[^>]+>", "", t["para"])) != de:
            erros.append(f"para muda o texto visível: {t['para']}")
    return erros


def gravar(posts, escolha, lote_do_post, destinos, recebidos, varr, trocas_ab):
    SAIDA.mkdir(exist_ok=True)
    for f in SAIDA.glob("*.json"):
        f.unlink()
    lotes = defaultdict(list)
    erros_total = 0
    for pid, trocas in sorted(escolha.items()):
        if not trocas:
            continue
        p = posts[pid]
        erros = validar(p["content"]["rendered"], trocas, trocas_ab.get(pid, []))
        if erros:
            erros_total += len(erros)
            print(f"post {pid}:", *erros, sep="\n    ")
            continue
        lote = lote_do_post[pid]
        lotes[lote].append(pid)
        dados = {"post_id": pid, "url": p["link"], "lote": lote,
                 "motivo": "Links internos: " + "; ".join(f"{t['ancora']} -> {caminho(t['url'])}" for t in trocas),
                 "trocas": [{"de": t["de"], "para": t["para"], "de_rendered": t["de_rendered"]} for t in trocas],
                 "fonte": "links-internos/gerar_links.py (seo/sugestoes-links.csv, similaridade TF-IDF e varredura)",
                 "links": [{"url": t["url"], "destino": t["destino"], "ancora": t["ancora"], "similaridade": t["sim"]}
                           for t in trocas]}
        (SAIDA / f"{pid}.json").write_text(json.dumps(dados, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    desc = {"L1": "Links contextuais para as 11 ferramentas do plugin iec-ferramentas 1.3.0 (páginas publicadas).",
            "L2": "Links contextuais para os 6 guias corrigidos ou reescritos: 4873, 4874, 5091, 1053, 993 e 4537.",
            "L3": "Links contextuais para posts órfãos (seo/sugestoes-links.csv), pelo ticker do título."}
    for lote, ids in sorted(lotes.items()):
        (SAIDA / f"LOTE_{lote}.json").write_text(json.dumps(
            {"lote": lote, "descricao": desc[lote], "post_ids": ids}, ensure_ascii=False, indent=1) + "\n",
            encoding="utf-8")
        print(f"lote {lote}: {len(ids)} posts, {sum(len(escolha[i]) for i in ids)} links")
    for d in destinos:
        if d["lote"] != "L3":
            print(f"  {d['lote']} {caminho(d['url']):58s} {len(recebidos[d['url']])} links")
    if erros_total:
        raise SystemExit(f"{erros_total} erros")


if __name__ == "__main__":
    main()
