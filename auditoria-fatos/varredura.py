"""Varredura automática (todos os posts, menos cotacao-*). Chamado por auditar.py varrer.

Checagens automáticas (todas geram CANDIDATOS; a classe final vem da checagem manual em checagem_manual.py):
  1. ticker inexistente: código no texto que não aparece no COTAHIST à vista 2021-2026 (site-ativos/cache/raw/b3).
     Limitação conhecida: ETFs de renda fixa (IMAB11, B5P211, FIXA11, IRFM11...) não estão no COTAHIST; ver LISTA_RF.
  2. ticker que parou de negociar antes da data do post (ou desde então): DATADO/CRÍTICO conforme a data.
  3. ticker x empresa: frase com um único ticker e um único nome de empresa (referencia.EMPRESAS) de outra empresa,
     ou par colado "Nome (TICK)" / "TICK (Nome)" trocado.
  4. Selic citada x meta Selic do BCB (SGS 432) na data do post.
  5. Regras de IR (referencia.REGRAS_IR): JCP 15% em post de 2026, 50 cotistas em FII, carência de 90 dias em
     LCI/LCA, isenção de R$ 20 mil sobre "lucro", dividendos "isentos" sem ressalva da Lei 15.270, "imposto sobre
     dividendos de 15%/20%" etc.
  6. Padrões de texto de IA sem revisão e recomendação de compra/venda.
"""
import csv
import json
import re
import sqlite3
import unicodedata
from bisect import bisect_right
from collections import Counter
from datetime import date, timedelta
from pathlib import Path

from auditar import AQUI, CACHE, DB, RAIZ, texto
from referencia import AMBIGUOS, EMPRESAS

RE_TICKER = re.compile(r"\b([A-Z]{4}(?:3|4|5|6|7|8|11|31|32|33|34|35|39))\b")
# ETFs de renda fixa e outros códigos que existem mas não aparecem no COTAHIST à vista (conferido na web).
LISTA_RF = {"IMAB11", "B5P211", "FIXA11", "IRFM11", "IB5M11", "B5MB11", "IMBB11", "LFTS11", "NTNS11", "IDKA11",
            "DEBB11", "SPXB11", "5PRE11", "BNDX11"}
# Códigos que aparecem como índice ou exemplo, não como ativo.
NAO_ATIVO = {"IFIX11"}


def norm(s):
    s = unicodedata.normalize("NFKD", s.lower())
    return "".join(c for c in s if not unicodedata.combining(c))


NOMES = []  # (nome normalizado, raiz)
for raiz, nomes in EMPRESAS.items():
    for n in nomes:
        NOMES.append((norm(n), raiz))
NOMES.sort(key=lambda x: -len(x[0]))


def empresas_no_trecho(t, so_inequivocos=True):
    tn = norm(t)
    achados = set()
    usados = []
    for n, raiz in NOMES:
        if so_inequivocos and n in {norm(a) for a in AMBIGUOS}:
            continue
        for m in re.finditer(r"(?<![a-z0-9])" + re.escape(n) + r"(?![a-z0-9])", tn):
            if any(a <= m.start() < b for a, b in usados):
                continue
            usados.append((m.start(), m.end()))
            achados.add(raiz)
    return achados


def raizes_da_empresa(raiz):
    """Raízes equivalentes (mesma empresa com códigos antigos/novos)."""
    grupos = [{"ELET", "AXIA"}, {"EMBR", "EMBJ"}, {"TRPL", "ISAE"}, {"PETZ", "AUAU"}, {"ARZZ", "AZZA"}]
    for g in grupos:
        if raiz in g:
            return g
    return {raiz}


def carregar_universo():
    return json.loads((CACHE / "universo_b3.json").read_text())


def carregar_selic():
    con = sqlite3.connect(DB)
    rows = con.execute("select data, valor from macro where serie=432 order by data").fetchall()
    return [r[0] for r in rows], [r[1] for r in rows]


def selic_em(datas, valores, d):
    i = bisect_right(datas, d) - 1
    return valores[max(i, 0)]


def trafego():
    """Proxy de tráfego: no sitemap, links internos recebidos (seo/varredura.csv), linkado pelo site-ativos."""
    sitemap, links = set(), {}
    with open(RAIZ / "seo" / "varredura.csv", newline="") as f:
        for r in csv.DictReader(f):
            sitemap.add(r["url"])
            links[r["url"]] = int(r.get("links_recebidos") or 0)
    ativos = Counter()
    saida = RAIZ / "site-ativos" / "saida"
    for f in saida.rglob("*.html"):
        for u in set(re.findall(r"https://investirecocaresocomecar\.com\.br/[a-z0-9%-]+/", f.read_text(errors="ignore"))):
            ativos[u] += 1
    return sitemap, links, ativos


FRASES_IA = ["guia completo", "em resumo", "vale ressaltar", "é importante ressaltar", "é importante lembrar",
             "em conclusão", "conclusão", "descubra", "navegando", "mergulhe", "desvende", "crucial", "robust",
             "sólid", "no cenário atual", "cenário econômico", "em suma", "por fim", "além disso",
             "lembre-se", "não é recomendação", "consulte um profissional", "faça sua própria análise",
             "panorama", "jornada", "potencial de valorização", "oportunidades e riscos"]
RE_FAQ = re.compile(r"perguntas frequentes|\bfaq\b|d[úu]vidas frequentes", re.I)
RE_RECOM = re.compile(r"vale a pena|\bcompr(e|ar|a)\b|qual (a|o) melhor|melhor(es)? (a[çc][ãa]o|a[çc][õo]es|etf|etfs|fii|fiis|fundo|banco|op[çc][õo]es)|"
                      r"hora de (comprar|vender)|carteira recomendada|recomend|\bvend(a|er)\b|oportunidade|aproveitar a queda|"
                      r"comprar a queda|qual escolher|qual comprar|onde investir", re.I)
RE_FONTE = re.compile(r"href=\"https?://(?!(?:www\.)?investirecocaresocomecar)[^\"]*(cvm\.gov|b3\.com|bcb\.gov|gov\.br|"
                      r"\bri\.|/ri/|investidores|tesourodireto|ibge|anbima|fundamentus|statusinvest|sec\.gov|planalto|receita)", re.I)


def padroes_ia(html, txt, titulo):
    t = norm(txt)
    frases = {f: t.count(norm(f)) for f in FRASES_IA if t.count(norm(f))}
    n_tab = len(re.findall(r"<table", html, re.I))
    faq = bool(RE_FAQ.search(txt))
    n_fontes = len(RE_FONTE.findall(html))
    nums = re.findall(r"(?:R\$\s?\d[\d.,]*\s?(?:mil|milh[õo]es|bi|bilh[õo]es|tri)?|\d+(?:,\d+)?\s?%)", txt)
    redondos = [n for n in nums if re.search(r"(^|\D)(\d+)(,0+)?\s?(%|bi|mi)", n) and not re.search(r",[1-9]", n)]
    # perguntas em H2/H3 repetindo o título (FAQ repetitivo)
    hs = [norm(re.sub("<[^>]+>", "", h)) for h in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", html, re.I | re.S)]
    perguntas = [h for h in hs if h.strip().endswith("?")]
    score = (2 if faq else 0) + min(n_tab, 3) + min(sum(frases.values()), 6) // 2 + (2 if n_fontes == 0 and len(nums) >= 10 else 0) \
        + (1 if len(perguntas) >= 5 else 0) + (1 if "guia completo" in norm(titulo) else 0)
    return {"score": score, "faq": faq, "tabelas": n_tab, "frases": frases, "links_fonte": n_fontes,
            "numeros": len(nums), "numeros_redondos": len(redondos), "h_perguntas": len(perguntas)}


def frases_de(txt):
    return [f.strip() for f in re.split(r"(?<=[.!?])\s+|\n", txt) if f.strip()]


def checar_ir(txt, d_post):
    achados = []
    for f in frases_de(txt):
        fn = norm(f)
        if re.search(r"jcp|juros sobre (o )?capital", fn) and re.search(r"\b15\s?%", fn) and "17,5" not in fn:
            classe = "DATADO" if d_post < "2026-01-01" else "CRÍTICO?"
            achados.append(("ir_jcp", f, "JCP com IRRF de 15%: desde 01/01/2026 é 17,5% (LC 224/2025)", classe))
        if re.search(r"\b50 cotistas", fn):
            achados.append(("ir_fii_50", f, "Isenção de FII exige 100 cotistas desde a Lei 14.754/2023 (antes 50)",
                            "DATADO" if d_post < "2023-12-12" else "CRÍTICO?"))
        if re.search(r"\b(lci|lca)", fn) and re.search(r"90 dias|3 meses|tres meses", fn) and re.search(r"car[eê]ncia|prazo m[ií]nimo|resgat", fn):
            achados.append(("lci_90", f, "Carência mínima de LCI/LCA: 9 meses desde fev/2024 e 6 meses desde mai/2025 (sem correção por índice)",
                            "DATADO" if d_post < "2024-02-01" else "CRÍTICO?"))
        if re.search(r"20 mil", fn) and re.search(r"isen", fn) and re.search(r"lucro|ganho", fn) and not re.search(r"vend", fn):
            achados.append(("ir_20mil_lucro", f, "Isenção de R$ 20 mil é sobre o total de VENDAS no mês, não sobre o lucro", "CRÍTICO?"))
        if re.search(r"20 mil", fn) and re.search(r"isen", fn) and re.search(r"\b(fii|fiis|fundos? imobili|etf|bdr)", fn):
            achados.append(("ir_20mil_fii", f, "Isenção de R$ 20 mil em vendas não vale para FII, ETF nem BDR", "CRÍTICO?"))
        if re.search(r"dividend", fn) and re.search(r"isent", fn) and not re.search(r"fii|fundos? imobili|50 mil|15\.270|alta renda|600 mil|10\s?%|lci|lca", fn):
            if d_post < "2025-11-26":
                achados.append(("div_isento_datado", f, "Dividendos deixaram de ser totalmente isentos: Lei 15.270/2025 (IRRF de 10% acima de R$ 50 mil/mês por empresa; IRPF mínimo acima de R$ 600 mil/ano)", "DATADO"))
            elif d_post >= "2026-01-01":
                achados.append(("div_isento_sem_ressalva", f, "Diz que dividendo é isento sem a ressalva da Lei 15.270/2025", "DÚVIDA"))
        if re.search(r"dividend", fn) and re.search(r"tribut|imposto|ir\b", fn) and re.search(r"\b(15|20)\s?%", fn) and not re.search(r"jcp|juros sobre|fii|ganho de capital|day|swing|bdr|eua|americ|30\s?%", fn):
            achados.append(("div_aliquota", f, "Alíquota de imposto sobre dividendos diferente da Lei 15.270/2025 (10% na fonte acima de R$ 50 mil/mês)", "DÚVIDA"))
        if re.search(r"come.cotas", fn) and re.search(r"(janeiro|fevereiro|mar[cç]o|abril|junho|julho|agosto|setembro|outubro|dezembro)", fn) and not re.search(r"maio|novembro", fn):
            achados.append(("come_cotas_mes", f, "Come-cotas é cobrado em maio e novembro", "CRÍTICO?"))
        if re.search(r"come.cotas", fn) and re.search(r"\b(fii|fiis|etf de a[cç][oõ]es|a[cç][oõ]es)\b", fn) and re.search(r"cobra|incide|tem come", fn) and not re.search(r"n[aã]o (tem|ha|incide|cobra|sofre)|sem come|isent|livre", fn):
            achados.append(("come_cotas_fii", f, "FII e ETF de renda variável não têm come-cotas", "DÚVIDA"))
        if re.search(r"fgc", fn) and re.search(r"r\$\s?(\d+)\s?mil", fn):
            v = re.search(r"r\$\s?(\d+)\s?mil", fn).group(1)
            if v not in ("250",) and not re.search(r"1 milh", fn):
                achados.append(("fgc_valor", f, "Garantia do FGC é de R$ 250 mil por CPF por instituição (teto de R$ 1 milhão a cada 4 anos)", "DÚVIDA"))
    return achados


def checar_selic(txt, d_post, datas, valores):
    achados = []
    for f in frases_de(txt):
        for m in re.finditer(r"selic[^.%\n]{0,30}?(\d{1,2}(?:,\d{1,2})?)\s?%", f, re.I):
            ctx = norm(f)
            if re.search(r"proje|expect|deve|devera|focus|pode|cair|chegar|previs|estimat|20(1|2)\d|historic|passado|em 20\d\d|quando|se a|caso", ctx):
                continue
            v = float(m.group(1).replace(",", "."))
            na_data = selic_em(datas, valores, d_post)
            atual = valores[-1]
            if abs(v - na_data) < 0.01:
                if abs(v - atual) > 0.01:
                    achados.append(("selic_datada", f, f"Selic de {m.group(1)}% era a meta na data do post; hoje é {str(atual).replace('.', ',')}% (SGS 432)", "DATADO"))
            else:
                # aceita valor vigente até 60 dias antes (texto escrito antes de publicar)
                d0 = (date.fromisoformat(d_post) - timedelta(days=60)).isoformat()
                if any(abs(v - x) < 0.01 for d, x in zip(datas, valores) if d0 <= d <= d_post):
                    continue
                achados.append(("selic_errada", f, f"Selic de {m.group(1)}% não bate com a meta na data do post ({str(na_data).replace('.', ',')}%, SGS 432)", "DÚVIDA"))
    return achados


def checar_tickers(txt, titulo, d_post, U):
    achados = []
    tickers = Counter(RE_TICKER.findall(txt + " " + titulo))
    dpost = d_post.replace("-", "")
    for t in tickers:
        if t in NAO_ATIVO:
            achados.append(("ticker_indice", t, f"{t} é tratado como ativo, mas IFIX é índice (o ETF é XFIX11)", "DÚVIDA"))
            continue
        u = U.get(t)
        if u is None:
            if t in LISTA_RF:
                continue
            achados.append(("ticker_inexistente", t, f"{t} não aparece no COTAHIST à vista 2021-2026 (B3)", "DÚVIDA"))
        elif u["fim"] < dpost:
            achados.append(("ticker_parado_antes", t, f"{t} ({u['nome']}) parou de negociar em {u['fim'][:4]}-{u['fim'][4:6]}-{u['fim'][6:]}, antes do post", "CRÍTICO?"))
        elif u["fim"] < "20260901":
            achados.append(("ticker_parado_depois", t, f"{t} ({u['nome']}) parou de negociar em {u['fim'][:4]}-{u['fim'][4:6]}-{u['fim'][6:]}", "DATADO"))
        elif u["ini"] > dpost:
            achados.append(("ticker_futuro", t, f"{t} só começou a negociar em {u['ini']}, depois do post", "DÚVIDA"))
    # ticker x empresa
    for f in frases_de(txt):
        ts = set(RE_TICKER.findall(f))
        if len(ts) != 1:
            continue
        t = ts.pop()
        raiz = t[:4]
        emps = empresas_no_trecho(f)
        if len(emps) == 1:
            e = next(iter(emps))
            if e not in raizes_da_empresa(raiz) and raiz in EMPRESAS and not (raiz == "ITUB" and e == "ITSA") and not (raiz == "ITSA" and e == "ITUB"):
                achados.append(("ticker_empresa", f, f"{t} citado junto de {e} (frase sem outro ticker)", "DÚVIDA"))
    # par colado "Nome (TICK)" ou "TICK (Nome)" em qualquer lugar do texto
    vistos = set()
    for t in tickers:
        raiz = t[:4]
        if raiz not in EMPRESAS:
            continue
        pad1 = r"((?:[A-ZÀ-Ú][\wÀ-ú&'.\-]*\s?){1,5})\(\s*" + t + r"\s*\)"
        pad2 = t + r"\s*\(\s*([^)]{3,40})\)"
        for pad in (pad1, pad2):
            for m in re.finditer(pad, txt):
                e2 = empresas_no_trecho(m.group(1), so_inequivocos=False)
                if e2 and not (e2 & raizes_da_empresa(raiz)) and m.group(0) not in vistos:
                    vistos.add(m.group(0))
                    achados.append(("ticker_empresa_par", m.group(0).strip(), f"{t} colado ao nome de outra empresa ({', '.join(sorted(e2))})", "CRÍTICO?"))
    return tickers, achados


def varrer(posts):
    U = carregar_universo()
    datas, valores = carregar_selic()
    sitemap, links, ativos = trafego()
    saida = []
    for p in posts:
        if p["slug"].startswith("cotacao-"):
            continue
        html = p["content"]["rendered"]
        titulo = texto(p["title"]["rendered"])
        txt = texto(html)
        d_post = p["date"][:10]
        tickers, a_t = checar_tickers(txt, titulo, d_post, U)
        a_ir = checar_ir(txt, d_post)
        a_s = checar_selic(txt, d_post, datas, valores)
        ia = padroes_ia(html, txt, titulo)
        recom_titulo = bool(RE_RECOM.search(titulo))
        recom_texto = len(RE_RECOM.findall(txt))
        emp_titulo = empresas_no_trecho(titulo, so_inequivocos=False) | {t[:4] for t in RE_TICKER.findall(titulo)}
        url = p["link"]
        trafego_score = (2 if url in sitemap else 0) + links.get(url, 0) + 3 * ativos.get(url, 0)
        saida.append({
            "id": p["id"], "url": url, "slug": p["slug"], "data": d_post, "modificado": p["modified"][:10],
            "titulo": titulo, "palavras": len(txt.split()), "no_sitemap": url in sitemap,
            "links_recebidos": links.get(url, 0), "linkado_site_ativos": ativos.get(url, 0),
            "trafego": trafego_score, "ativo_no_titulo": sorted(emp_titulo),
            "grupo": "A" if emp_titulo else "B", "tickers": dict(tickers),
            "achados": [dict(zip(("tipo", "trecho", "problema", "classe"), a)) for a in a_t + a_ir + a_s],
            "ia": ia, "recomenda_titulo": recom_titulo, "recomenda_texto": recom_texto,
        })
    saida.sort(key=lambda r: (r["grupo"], -r["trafego"], -len(r["achados"])))
    (CACHE / "varredura.json").write_text(json.dumps(saida, ensure_ascii=False, indent=1))
    c = Counter(a["tipo"] for r in saida for a in r["achados"])
    print(f"{len(saida)} posts; achados automáticos: {dict(c)}")
    print(f"grupo A (ativo no título): {sum(r['grupo'] == 'A' for r in saida)}; no sitemap: {sum(r['no_sitemap'] for r in saida)}")
    return saida
