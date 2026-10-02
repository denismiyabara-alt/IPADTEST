#!/usr/bin/env python3
"""Lê os CSVs de dados/ (e, se houver, as exportações do YouTube Studio em dados/studio/) e calcula as tabelas
do RELATORIO.md. Só biblioteca padrão; não acessa a rede.

uso:
  python3 analisar.py                    gera analise/RESULTADOS.md, analise/temas_por_video.csv e a lista abaixo
  python3 analisar.py --lista-retencao   só imprime os 10 longos top e os 10 fracos (IDs) para anotar a
                                         retenção em 30 s no Studio (grava analise/lista_retencao_30s.csv)

Ajustes fáceis (no topo deste arquivo): TEMAS e ENTIDADES (classificação de tema pelo título), POPULACAO_*
(quais vídeos entram em top × fracos) e as datas das hipóteses. Para corrigir o tema de um vídeo à mão, crie
dados/temas_manual.csv com as colunas video_id,tema.

Exportações do Studio (opcionais; o script segue sem elas). Em dados/studio/, cada uma como ZIP ou pasta com
Tabela.csv / Totais.csv / Gráfico.csv (ou Table data.csv / Totals.csv / Chart data.csv), cabeçalhos em PT ou EN:
  studio_conteudo_longos, studio_conteudo_shorts       por vídeo: impressões, CTR, views, views engajadas, ...
  studio_origem_trafego_mensal[_longos|_shorts]        origem × mês
  studio_ctr_por_origem_top30, studio_publico_mensal   opcionais
  retencao_30s.csv (video_id,pct_30s) e ask_studio.txt opcionais
"""
import argparse
import csv
import io
import math
import re
import statistics
import sys
import unicodedata
import zipfile
from collections import Counter, defaultdict
from datetime import date, datetime, timedelta
from pathlib import Path

AQUI = Path(__file__).resolve().parent

# ------------------------------------------------------------------------------------------- ajustes fáceis
# Datas das hipóteses (a confirmar ou derrubar, não verdades).
DATA_INFLACAO = date(2026, 8, 27)       # "desde 27/08 o contador público está inflado 2,5 a 2,8x"
DATA_SHORTS_FIM = date(2026, 7, 28)     # "os Shorts foram encerrados em 28/07"
DATA_SHORTS_NOVA_CONTAGEM = date(2025, 3, 31)  # YouTube passou a contar toda reprodução de Short como view
JANELA_DIAS = 28                        # dias antes × depois de DATA_INFLACAO na série diária

# População de top × fracos: só longos, publicados nos últimos N dias e com pelo menos M dias de vida
# (para um vídeo de ontem não cair entre os "fracos" e um de 3 anos atrás não dominar os "top").
POPULACAO_DIAS, POPULACAO_MIN_VIDA = 540, 14

# Entidades que, no título, fazem o vídeo ser "caso com nome". Minúsculas, sem acento. Acrescente à vontade.
ENTIDADES = [
    "americanas", "petrobras", "vale3", "itau", "bradesco", "santander", "banco do brasil", "caixa economica",
    "nubank", "banco inter", "c6 bank", "xp", "btg", "banco master", "magalu", "magazine luiza",
    "casas bahia", "embraer", "ambev", "jbs", "weg", "eletrobras", "sabesp", "taesa",
    "irb", "hapvida", "rede d'or", "raizen", "braskem", "cvc", "mercado livre", "binance", "ftx", "evergrande",
    "lehman", "silicon valley bank", "credit suisse", "warren buffett", "buffett", "barsi", "luiz barsi",
    "primo rico", "thiago nigro", "nath financas", "bastter", "elon musk", "musk", "tesla", "apple", "nvidia",
    "eike", "eike batista", "123 milhas", "hurb", "unimed", "correios",
]
# Fora da lista de propósito por serem palavras comuns: vale (a pena), oi, via, inter, gol, azul, light, master.
# Palavras com inicial maiúscula que NÃO são nome de pessoa/empresa (termos de finanças, meses, etc.).
NAO_NOMES = set("""tesouro selic ipca cdi cdb lci lca fii fiis fundos fundo imobiliario imobiliarios renda fixa variavel
direto prefixado poupanca bolsa ibovespa dolar real reais brasil brasileiro brasileiros governo banco central copom
previdencia aposentadoria imposto ir etf etfs bdr acoes acao dividendos janeiro fevereiro marco abril maio junho julho
agosto setembro outubro novembro dezembro natal ano novo black friday youtube shorts lula bolsonaro haddad""".split())

# Temas: o primeiro que casar leva o vídeo ("caso com nome" é testado antes, pela função caso_com_nome).
TEMAS = [
    ("alerta macro", r"crise|colapso|quebr|recess|inflac|\bselic\b|juros|dolar|governo|fiscal|divida publica|bolha|"
                     r"calote|alerta|urgente|cuidado|perigo|economia|copom|banco central|\bpib\b|desemprego|"
                     r"taxac|confisco|imposto|tribut|o que vai acontecer|vai cair|vai subir"),
    ("plano de renda", r"renda passiva|viver de renda|por mes|mensa(l|is)|salario|aposentad|independencia financeira|"
                       r"liberdade financeira|milhao|r\$ ?\d|\d+ ?mil\b|carteira|quanto (preciso|investir|rende)|"
                       r"\brenda\b"),
    ("produto / comparativo", r"tesouro|\bcdb|\blci|\blca|\bfiis?\b|fundos? imobiliari|poupanca|\bacoes\b|\betf|"
                              r"previdencia|\bcdi\b|ipca|\bvs\.?\b|\bx\b|melhor investimento|onde investir|"
                              r"renda fixa|dividendo"),
    ("educativo / iniciante", r"\bcomo\b|comecar|iniciante|passo a passo|\berros?\b|aprenda|entenda|o que e\b|guia|"
                              r"\bdicas?\b|nunca|segredo"),
]
TEMA_CASO, TEMA_OUTROS = "caso com nome", "outros"

PERGUNTA = re.compile(r"\?|^(como|qual|quais|quando|onde|quanto|quantos|por que|porque|o que|vale a pena|devo|"
                      r"compensa|alguem sabe|sera que|tem como|da pra|da para|voce acha|faz um video|faca um video)\b")
STOP = set("""a o e de da do das dos que em um uma para pra por com no na nos nas se eu voce vc meu minha isso esse essa
como qual quais quando onde quanto quantos porque por que o que mais mas ou ja nao sim tem ter ser vai faz fazer e
ao aos as os sobre tambem muito bom boa ai entao seu sua ele ela isso so ate pode posso devo vale pena alguem sabe
dia ano anos hoje agora tipo bem aqui la cara pessoal video videos obrigado parabens canal""".split())


# ------------------------------------------------------------------------------------------------ utilidades
def sem_acento(t):
    return "".join(c for c in unicodedata.normalize("NFD", t or "") if unicodedata.category(c) != "Mn")


def norm(t):
    return re.sub(r"\s+", " ", sem_acento(t).lower()).strip()


def num(v):
    """Converte '1.234', '1,234.5', '1.234,5', '12,5%', '0:03:21' (vira segundos) e '' (None)."""
    if v is None:
        return None
    s = str(v).strip().replace("%", "").replace(" ", "").replace(" ", "")
    if s in ("", "-", "—"):
        return None
    if re.fullmatch(r"\d+:\d{1,2}(:\d{1,2})?", s):
        partes = [int(p) for p in s.split(":")]
        seg = 0
        for p in partes:
            seg = seg * 60 + p
        return float(seg)
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        s = s.replace(",", "") if re.fullmatch(r"-?\d{1,3}(,\d{3})+", s) else s.replace(",", ".")
    elif s.count(".") > 1:
        s = s.replace(".", "")
    try:
        return float(s)
    except ValueError:
        return None


def soma(rs, campo):
    return sum(num(r.get(campo)) or 0 for r in rs)


def mediana(vs):
    vs = [v for v in vs if v is not None]
    return statistics.median(vs) if vs else None


def por_mil(a, b):
    return 1000 * a / b if b else None


def pct(a, b):
    return 100 * a / b if b else None


def f(v, casas=1):
    if v is None:
        return "—"
    if isinstance(v, str):
        return v
    s = f"{v:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def ler_csv(p):
    if not p.exists():
        return []
    with p.open(newline="", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def tabela_md(cab, linhas):
    out = ["| " + " | ".join(cab) + " |", "|" + "|".join("---" for _ in cab) + "|"]
    out += ["| " + " | ".join(str(c) for c in l) + " |" for l in linhas]
    return "\n".join(out)


# ------------------------------------------------------------------------------------------------ temas
def caso_com_nome(titulo):
    t = " " + norm(titulo) + " "
    if any(re.search(r"(?<![a-z0-9])" + re.escape(e) + r"(?![a-z0-9])", t) for e in ENTIDADES):
        return True
    if re.search(r"\b(o caso|a historia d|caso d[aoe]s?)\b", t):
        return True
    # Duas palavras seguidas com inicial maiúscula (não tudo em caixa alta), fora do começo do título e fora
    # de NAO_NOMES: "... com Luiz Barsi", "... da Banco Master".
    palavras = re.findall(r"[\wÀ-ÿ'’]+", titulo or "")
    iniciais = [p[0].isupper() for p in palavras if len(p) > 3]
    if iniciais and sum(iniciais) / len(iniciais) > 0.6:  # Título Em Caixa De Título: a regra não serve
        return False
    cap = [len(p) > 1 and p[0].isupper() and not p.isupper() and norm(p) not in NAO_NOMES for p in palavras]
    return any(cap[i] and cap[i + 1] for i in range(1, len(cap) - 1))


def tema(titulo, manual=None):
    if manual:
        return manual
    if caso_com_nome(titulo):
        return TEMA_CASO
    t = norm(titulo)
    for nome, rx in TEMAS:
        if re.search(rx, t):
            return nome
    return TEMA_OUTROS


# ------------------------------------------------------------------------------------------------ Studio
# Cabeçalhos do Studio (PT e EN) → nomes internos. A chave é o cabeçalho normalizado, sem o que está entre ().
CABECALHOS = {
    "conteudo": "video_id", "content": "video_id", "video": "video_id", "id do video": "video_id", "video id": "video_id",
    "video_id": "video_id",
    "titulo do video": "titulo", "video title": "titulo", "titulo": "titulo", "title": "titulo",
    "horario de publicacao do video": "publicado", "video publish time": "publicado",
    "duracao": "duracao_s", "duration": "duracao_s",
    "impressoes": "impressoes", "impressions": "impressoes",
    "taxa de cliques de impressoes": "ctr", "impressions click-through rate": "ctr",
    "taxa de cliques das impressoes": "ctr", "ctr das impressoes": "ctr", "ctr": "ctr",
    "visualizacoes": "views", "views": "views",
    "visualizacoes engajadas": "views_engajadas", "engaged views": "views_engajadas",
    "tempo de exibicao": "horas", "watch time": "horas",
    "duracao media da visualizacao": "duracao_media", "average view duration": "duracao_media",
    "porcentagem visualizada media": "pct_media", "average percentage viewed": "pct_media",
    "% media visualizada": "pct_media", "porcentagem media visualizada": "pct_media",
    "inscritos": "inscritos", "subscribers": "inscritos",
    "inscritos ganhos": "inscritos_ganhos", "subscribers gained": "inscritos_ganhos",
    "inscritos perdidos": "inscritos_perdidos", "subscribers lost": "inscritos_perdidos",
    "espectadores unicos": "espectadores_unicos", "unique viewers": "espectadores_unicos",
    "origem do trafego": "origem", "traffic source": "origem",
    "mes": "mes", "month": "mes", "data": "data", "date": "data",
    "pct_30s": "pct_30s",
}
MESES = {"jan": 1, "fev": 2, "feb": 2, "mar": 3, "abr": 4, "apr": 4, "mai": 5, "may": 5, "jun": 6, "jul": 7,
         "ago": 8, "aug": 8, "set": 9, "sep": 9, "out": 10, "oct": 10, "nov": 11, "dez": 12, "dec": 12}
ORIGEM_PARA_API = {  # nomes do Studio → códigos da API, para comparar com trafego_por_mes.csv
    "videos sugeridos": "RELATED_VIDEO", "suggested videos": "RELATED_VIDEO",
    "recursos de navegacao": "BROWSE", "browse features": "BROWSE",
    "pesquisa do youtube": "YT_SEARCH", "youtube search": "YT_SEARCH", "feed do shorts": "SHORTS",
    "shorts feed": "SHORTS", "externo": "EXT_URL", "external": "EXT_URL",
    "direto ou desconhecido": "NO_LINK_OTHER", "direct or unknown": "NO_LINK_OTHER",
    "paginas do canal": "YT_CHANNEL", "channel pages": "YT_CHANNEL", "playlists": "PLAYLIST",
    "notificacoes": "NOTIFICATION", "notifications": "NOTIFICATION", "telas finais": "END_SCREEN",
    "end screens": "END_SCREEN", "outros recursos do youtube": "YT_OTHER_PAGE", "other youtube features": "YT_OTHER_PAGE",
}


def chave_cab(c):
    return CABECALHOS.get(re.sub(r"\s*\(.*?\)\s*", " ", norm(c)).strip())


def parse_mes(v):
    """'2025-09', '2025-09-14', 'Sep 2025', 'set. de 2025', 'setembro 2025' → '2025-09'."""
    s = norm(v)
    m = re.match(r"(\d{4})-(\d{2})", s)
    if m:
        return f"{m.group(1)}-{m.group(2)}"
    m = re.search(r"([a-z]{3})[a-z]*\.?\s*(?:de\s+)?(\d{4})", s)
    if m and m.group(1) in MESES:
        return f"{m.group(2)}-{MESES[m.group(1)]:02d}"
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)  # dd/mm/aaaa
    if m:
        return f"{m.group(3)}-{int(m.group(2)):02d}"
    return None


def _ler_texto_csv(texto):
    rs = list(csv.reader(io.StringIO(texto.lstrip("﻿"))))
    if not rs:
        return []
    cab = [chave_cab(c) or norm(c) for c in rs[0]]
    out = []
    for r in rs[1:]:
        d = dict(zip(cab, r))
        if norm(d.get("video_id", "")) == "total" or norm(next(iter(d.values()), "")) == "total":
            continue
        out.append(d)
    return out


def _papel(nome_arquivo):
    n = norm(Path(nome_arquivo).stem)
    if n.startswith(("tabela", "table")):
        return "tabela"
    if n.startswith(("totais", "totals")):
        return "totais"
    if n.startswith(("grafico", "chart")):
        return "grafico"
    return None


def ler_exportacao_studio(caminho):
    """Lê uma exportação do Studio (ZIP ou pasta) → {'tabela': [...], 'totais': [...], 'grafico': [...]}."""
    caminho = Path(caminho)
    out = {}
    if caminho.is_file() and caminho.suffix.lower() == ".zip":
        with zipfile.ZipFile(caminho) as z:
            for nome in z.namelist():
                papel = _papel(nome)
                if papel and nome.lower().endswith(".csv"):
                    out[papel] = _ler_texto_csv(z.read(nome).decode("utf-8-sig", errors="replace"))
    elif caminho.is_dir():
        for arq in caminho.iterdir():
            papel = _papel(arq.name)
            if papel and arq.suffix.lower() == ".csv":
                out[papel] = _ler_texto_csv(arq.read_text(encoding="utf-8-sig", errors="replace"))
    elif caminho.is_file() and caminho.suffix.lower() == ".csv":
        out["tabela"] = _ler_texto_csv(caminho.read_text(encoding="utf-8-sig", errors="replace"))
    return out


def achar_studio(pasta, base):
    """Procura dados/studio/<base>.zip, <base>/ ou <base>.csv (nomes comparados sem acento e sem caixa)."""
    if not pasta.exists():
        return None
    for p in sorted(pasta.iterdir()):
        nome = norm(p.stem if p.is_file() else p.name)
        if nome == norm(base):
            return p
    return None


def carregar_studio(pasta):
    st = {}
    for base in ("studio_conteudo_longos", "studio_conteudo_shorts", "studio_origem_trafego_mensal",
                 "studio_origem_trafego_mensal_longos", "studio_origem_trafego_mensal_shorts",
                 "studio_ctr_por_origem_top30", "studio_publico_mensal"):
        p = achar_studio(pasta, base)
        if p:
            st[base] = ler_exportacao_studio(p)
    p = pasta / "retencao_30s.csv"
    if p.exists():
        st["retencao_30s"] = _ler_texto_csv(p.read_text(encoding="utf-8-sig"))
    p = pasta / "ask_studio.txt"
    if p.exists():
        st["ask_studio"] = p.read_text(encoding="utf-8", errors="replace")
    return st


def linhas_origem_mes(exp):
    """Origem × mês de uma exportação do Studio: usa a tabela se tiver mês; senão o gráfico (diário → mês)."""
    for papel in ("tabela", "grafico"):
        rs = exp.get(papel) or []
        if rs and "origem" in rs[0] and ("mes" in rs[0] or "data" in rs[0]):
            agg = defaultdict(lambda: defaultdict(float))
            for r in rs:
                m = parse_mes(r.get("mes") or r.get("data") or "")
                if not m:
                    continue
                k = (m, r["origem"])
                for c in ("views", "impressoes", "horas"):
                    agg[k][c] += num(r.get(c)) or 0
                if num(r.get("ctr")) is not None and num(r.get("impressoes")):
                    agg[k]["_cliques"] += num(r["ctr"]) / 100 * num(r["impressoes"])
            out = []
            for (m, o), d in sorted(agg.items()):
                out.append({"mes": m, "origem": o, "origem_api": ORIGEM_PARA_API.get(norm(o), ""),
                            "views": d["views"], "impressoes": d["impressoes"], "horas": d["horas"],
                            "ctr": pct(d["_cliques"], d["impressoes"]) if d["impressoes"] else None})
            return out
    return []


# ------------------------------------------------------------------------------------------------ dados
class Dados:
    def __init__(self, pasta):
        self.pasta = Path(pasta)
        self.videos = ler_csv(self.pasta / "videos.csv")
        self.analytics = {r["video_id"]: r for r in ler_csv(self.pasta / "analytics_por_video.csv")}
        self.mes = ler_csv(self.pasta / "canal_por_mes.csv")
        self.dia = ler_csv(self.pasta / "canal_por_dia.csv")
        self.trafego_mes = ler_csv(self.pasta / "trafego_por_mes.csv")
        self.trafego_video = ler_csv(self.pasta / "trafego_por_video.csv")
        self.inscritos_video = ler_csv(self.pasta / "inscritos_por_video.csv")
        self.comentarios = ler_csv(self.pasta / "comentarios_top30.csv")
        manual = {r["video_id"]: r["tema"] for r in ler_csv(self.pasta / "temas_manual.csv")}
        self.studio = carregar_studio(self.pasta / "studio")
        self.casamento = {"por_id": 0, "por_titulo": 0, "sem_par": 0}
        self.v = self._montar(manual)

    def _montar(self, manual):
        """Uma linha por vídeo, juntando videos.csv, Analytics e (se houver) Studio."""
        out = {}
        for r in self.videos:
            a = self.analytics.get(r["id"], {})
            pub = datetime.strptime(r["publicado_em_brt"][:10], "%Y-%m-%d").date() if r.get("publicado_em_brt") else None
            out[r["id"]] = {
                "id": r["id"], "titulo": r["titulo"], "formato": r["formato"], "publicado": pub,
                "dia_semana": r.get("dia_semana"), "hora": num(r.get("hora")), "duracao_s": num(r.get("duracao_s")),
                "views_publico": num(r.get("views")), "views": num(a.get("views")) if a else num(r.get("views")),
                "minutos": num(a.get("estimatedMinutesWatched")), "pct_media": num(a.get("averageViewPercentage")),
                "ganhos": num(a.get("subscribersGained")), "perdidos": num(a.get("subscribersLost")),
                "engajadas": num(a.get("engagedViews")), "impressoes": num(a.get("impressions")),
                "ctr": num(a.get("impressionsClickThroughRate")), "pct_30s": None, "inscritos_studio": None,
                "tema": tema(r["titulo"], manual.get(r["id"])), "fonte_ctr": "API" if num(a.get("impressions")) else "",
            }
        por_titulo = {norm(v["titulo"]): k for k, v in out.items()}
        for base in ("studio_conteudo_longos", "studio_conteudo_shorts"):
            for r in (self.studio.get(base) or {}).get("tabela", []):
                vid = r.get("video_id", "").strip()
                if vid not in out:
                    vid = por_titulo.get(norm(r.get("titulo", "")))
                    self.casamento["por_titulo" if vid else "sem_par"] += 1
                else:
                    self.casamento["por_id"] += 1
                if not vid:
                    continue
                v = out[vid]
                for campo_st, campo in (("impressoes", "impressoes"), ("ctr", "ctr"), ("views_engajadas", "engajadas")):
                    if num(r.get(campo_st)) is not None:
                        v[campo] = num(r.get(campo_st))
                        if campo != "engajadas":
                            v["fonte_ctr"] = "Studio"
                if v["pct_media"] is None:
                    v["pct_media"] = num(r.get("pct_media"))
                v["inscritos_studio"] = num(r.get("inscritos"))
        for r in self.studio.get("retencao_30s", []):
            if r.get("video_id", "").strip() in out:
                out[r["video_id"].strip()]["pct_30s"] = num(r.get("pct_30s"))
        return out

    @property
    def data_ref(self):
        datas = [r["dia"] for r in self.dia] + [str(v["publicado"]) for v in self.v.values() if v["publicado"]]
        return date.fromisoformat(max(datas)[:10]) if datas else date.today()


# ------------------------------------------------------------------------------------------------ análises
def conversao(vs):
    """inscritos por mil views (ganhos do Analytics; senão os líquidos do Studio)."""
    g = sum(v["ganhos"] or 0 for v in vs)
    if not any(v["ganhos"] is not None for v in vs):
        g = sum(v["inscritos_studio"] or 0 for v in vs)
    return por_mil(g, sum(v["views"] or 0 for v in vs))


def por_grupo(vs, chave):
    g = defaultdict(list)
    for v in vs:
        g[v[chave]].append(v)
    total = sum(v["views"] or 0 for v in vs)
    out = []
    for k, l in sorted(g.items(), key=lambda kv: -sum(v["views"] or 0 for v in kv[1])):
        out.append({"grupo": k, "n": len(l), "views": sum(v["views"] or 0 for v in l),
                    "pct_views": pct(sum(v["views"] or 0 for v in l), total),
                    "mediana_views": mediana([v["views"] for v in l]), "insc_mil": conversao(l),
                    "engajadas_mil": por_mil(sum(v["ganhos"] or 0 for v in l), sum(v["engajadas"] or 0 for v in l))
                    if any(v["engajadas"] for v in l) else None,
                    "pct_media": mediana([v["pct_media"] for v in l]), "ctr": mediana([v["ctr"] for v in l])})
    return out


def concentracao(vs):
    views = sorted((v["views"] or 0 for v in vs), reverse=True)
    total = sum(views)
    if not total:
        return {}
    acum, n50, n80 = 0, None, None
    for i, x in enumerate(views, 1):
        acum += x
        if n50 is None and acum >= 0.5 * total:
            n50 = i
        if n80 is None and acum >= 0.8 * total:
            n80 = i
    n = len(views)
    cres = sorted(views)
    gini = (2 * sum(i * x for i, x in enumerate(cres, 1)) / (n * total)) - (n + 1) / n
    return {"n": n, "top1": pct(sum(views[:1]), total), "top5": pct(sum(views[:5]), total),
            "top10": pct(sum(views[:10]), total), "top10pct": pct(sum(views[:max(1, n // 10)]), total),
            "n50": n50, "n80": n80, "gini": gini}


def populacao_longos(d):
    ref = d.data_ref
    return [v for v in d.v.values() if v["formato"] == "longo" and v["publicado"]
            and POPULACAO_MIN_VIDA <= (ref - v["publicado"]).days <= POPULACAO_DIAS and v["views"] is not None]


def top_fracos(d, n=None):
    pop = sorted(populacao_longos(d), key=lambda v: -(v["views"] or 0))
    if n is None:
        n = max(1, len(pop) // 4)
    n = min(n, len(pop) // 2)
    return pop[:n], pop[-n:] if n else []


def perfil(vs):
    if not vs:
        return {}
    tit = [v["titulo"] for v in vs]
    temas = Counter(v["tema"] for v in vs)
    dias = Counter(v["dia_semana"] for v in vs)
    return {
        "n": len(vs), "mediana_views": mediana([v["views"] for v in vs]), "insc_mil": conversao(vs),
        "tema_principal": ", ".join(f"{t} {100 * c / len(vs):.0f}%" for t, c in temas.most_common(3)),
        "caso_com_nome": pct(sum(v["tema"] == TEMA_CASO for v in vs), len(vs)),
        "duracao_min": (mediana([v["duracao_s"] for v in vs]) or 0) / 60,
        "titulo_chars": mediana([len(t) for t in tit]),
        "titulo_com_numero": pct(sum(bool(re.search(r"\d", t)) for t in tit), len(tit)),
        "titulo_com_pergunta": pct(sum("?" in t for t in tit), len(tit)),
        "titulo_caixa_alta": pct(sum(_caixa_alta(t) for t in tit), len(tit)),
        "dia_mais_comum": dias.most_common(1)[0][0] if dias else None,
        "hora_mediana": mediana([v["hora"] for v in vs]),
        "pct_media": mediana([v["pct_media"] for v in vs]), "ctr": mediana([v["ctr"] for v in vs]),
        "impressoes": mediana([v["impressoes"] for v in vs]), "pct_30s": mediana([v["pct_30s"] for v in vs]),
    }


def _caixa_alta(t):
    letras = [c for c in t if c.isalpha()]
    return bool(letras) and sum(c.isupper() for c in letras) / len(letras) > 0.5


def curva_mensal(d):
    out = []
    for r in d.mes:
        views = num(r.get("views")) or 0
        g, p = num(r.get("inscritos_ganhos")) or 0, num(r.get("inscritos_perdidos")) or 0
        gs = num(r.get("inscritos_ganhos_shorts"))
        out.append({"mes": r["mes"], "views": views, "minutos": num(r.get("minutos")), "liquidos": g - p,
                    "insc_mil": por_mil(g, views), "engajadas_pct": pct(num(r.get("engagedViews")) or 0, views)
                    if num(r.get("engagedViews")) else None,
                    "pct_views_shorts": pct(num(r.get("views_shorts")) or 0, views) if r.get("views_shorts") else None,
                    "pct_insc_shorts": pct(gs, g) if gs is not None and g else None})
    return out


def origem_por_mes(d):
    tab = defaultdict(dict)
    for r in d.trafego_mes:
        tab[r["mes"]][r["origem"]] = num(r.get("pct_views_mes"))
    return dict(sorted(tab.items()))


def comparar_periodos(serie, data_corte, dias, campo_a, campo_b):
    """Razão campo_a/campo_b nos `dias` antes × depois da data de corte (série diária)."""
    antes = [r for r in serie if data_corte - timedelta(days=dias) <= r["_d"] < data_corte]
    depois = [r for r in serie if data_corte <= r["_d"] < data_corte + timedelta(days=dias)]

    def razao(rs):
        b = sum(num(r.get(campo_b)) or 0 for r in rs)
        return (sum(num(r.get(campo_a)) or 0 for r in rs) / b) if b else None
    ra, rd = razao(antes), razao(depois)
    return ra, rd, (rd / ra if ra and rd else None), len(antes), len(depois)


def razao_mediana(vs, a, b):
    return mediana([v[a] / v[b] for v in vs if v.get(a) and v.get(b)])


# ------------------------------------------------------------------------------------------------ hipóteses
def veredito(cond_confirma, cond_parcial, tem_dados):
    if not tem_dados:
        return "SEM DADOS"
    return "CONFIRMA" if cond_confirma else "PARCIAL" if cond_parcial else "DERRUBA"


def hipoteses(d):
    H = []
    # H1: contador público inflado desde 27/08.
    serie = [dict(r, _d=date.fromisoformat(r["dia"])) for r in d.dia]
    _, _, fator_min, na, nd = comparar_periodos(serie, DATA_INFLACAO, JANELA_DIAS, "views", "minutos")
    _, _, fator_eng, _, _ = comparar_periodos(serie, DATA_INFLACAO, JANELA_DIAS, "views", "engagedViews")
    longos = [v for v in d.v.values() if v["formato"] == "longo" and v["publicado"]]
    antes = [v for v in longos if DATA_INFLACAO - timedelta(days=120) <= v["publicado"] < DATA_INFLACAO]
    depois = [v for v in longos if v["publicado"] >= DATA_INFLACAO]
    ra, rd = razao_mediana(antes, "views_publico", "engajadas"), razao_mediana(depois, "views_publico", "engajadas")
    fator_vid = rd / ra if ra and rd else None
    shorts = [v for v in d.v.values() if v["formato"] == "short" and v["publicado"]]
    sa = razao_mediana([v for v in shorts if v["publicado"] < DATA_SHORTS_NOVA_CONTAGEM], "views_publico", "engajadas")
    sd = razao_mediana([v for v in shorts if v["publicado"] >= DATA_SHORTS_NOVA_CONTAGEM], "views_publico", "engajadas")
    fator = fator_eng or fator_vid or fator_min
    H.append({
        "id": "H1", "texto": f"Desde {DATA_INFLACAO:%d/%m/%Y} o contador público de views está inflado 2,5 a 2,8x",
        "numeros": [
            f"views por minuto assistido, {JANELA_DIAS} dias depois ÷ antes (canal_por_dia, {na}+{nd} dias): {f(fator_min, 2)}x",
            f"views ÷ views engajadas, depois ÷ antes: {f(fator_eng, 2)}x",
            f"longos: mediana de contador público ÷ engajadas, publicados depois ({len(depois)}) ÷ 120 dias antes "
            f"({len(antes)}): {f(fator_vid, 2)}x (antes {f(ra, 2)}, depois {f(rd, 2)})",
            f"Shorts: contador público ÷ engajadas antes de {DATA_SHORTS_NOVA_CONTAGEM:%d/%m/%Y}: {f(sa, 2)}; "
            f"depois: {f(sd, 2)} (a contagem de Shorts mudou nessa data; não confundir com o efeito de 27/08)",
        ],
        "veredito": veredito(fator is not None and 2.2 <= fator <= 3.2, fator is not None and fator >= 1.3,
                             fator is not None),
        "regra": "CONFIRMA se o fator (engajadas; senão vídeos; senão minutos) ficar entre 2,2x e 3,2x; "
                 "PARCIAL se ≥ 1,3x; DERRUBA abaixo disso.",
    })
    # H2: conversão por tema.
    g = {r["grupo"]: r for r in por_grupo([v for v in d.v.values() if v["formato"] == "longo"], "tema")}
    caso = (g.get(TEMA_CASO) or {}).get("insc_mil")
    outros = [x for x in ((g.get("alerta macro") or {}).get("insc_mil"), (g.get("plano de renda") or {}).get("insc_mil"))
              if x is not None]
    ref = statistics.mean(outros) if outros else None
    H.append({
        "id": "H2", "texto": "Vídeos de caso com nome convertem 6 a 8 inscritos por mil views; alerta macro e plano de renda ~2",
        "numeros": [f"{k}: {f(v.get('insc_mil'), 2)} por mil ({v['n']} longos)" for k, v in g.items()],
        "veredito": veredito(caso is not None and 5 <= caso <= 9 and ref is not None and 1 <= ref <= 3,
                             caso is not None and ref and caso / ref >= 2, caso is not None and ref is not None),
        "regra": "CONFIRMA se caso ∈ [5; 9] e a média de alerta macro/plano de renda ∈ [1; 3]; PARCIAL se caso ≥ 2× "
                 "a média dos outros dois; DERRUBA abaixo disso. Confira a classificação em temas_por_video.csv.",
    })
    # H3: Recomendados (RELATED_VIDEO) de 29% para 2%.
    om = origem_por_mes(d)
    meses = list(om)
    ini = mediana([om[m].get("RELATED_VIDEO", 0) for m in meses[:3]]) if meses else None
    fim = mediana([om[m].get("RELATED_VIDEO", 0) for m in meses[-2:]]) if meses else None
    pico = max(((om[m].get("RELATED_VIDEO", 0), m) for m in meses), default=(None, None))
    H.append({
        "id": "H3", "texto": "A origem Recomendados (vídeos sugeridos) caiu de 29% para 2% das views",
        "numeros": [f"RELATED_VIDEO, mediana dos 3 primeiros meses: {f(ini)}%; dos 2 últimos: {f(fim)}%",
                    f"pico: {f(pico[0])}% em {pico[1]}",
                    f"BROWSE nos mesmos recortes: {f(mediana([om[m].get('BROWSE', 0) for m in meses[:3]]) if meses else None)}% → "
                    f"{f(mediana([om[m].get('BROWSE', 0) for m in meses[-2:]]) if meses else None)}%"],
        "veredito": veredito(ini is not None and ini >= 20 and fim is not None and fim <= 5,
                             ini and fim is not None and fim <= ini / 2, bool(meses)),
        "regra": "CONFIRMA se começa ≥ 20% e termina ≤ 5%; PARCIAL se caiu pela metade ou mais; DERRUBA se não caiu.",
    })
    # H4: tema explica 20-50x; abertura quase não separa.
    pop = populacao_longos(d)
    gt = [r for r in por_grupo(pop, "tema") if r["n"] >= 3 and r["mediana_views"]]
    razao_tema = (max(r["mediana_views"] for r in gt) / min(r["mediana_views"] for r in gt)) if len(gt) >= 2 else None
    eta = eta2([math.log10((v["views"] or 0) + 1) for v in pop], [v["tema"] for v in pop])
    top, fr = top_fracos(d)
    a30t, a30f = mediana([v["pct_30s"] for v in top]), mediana([v["pct_30s"] for v in fr])
    pmt, pmf = mediana([v["pct_media"] for v in top]), mediana([v["pct_media"] for v in fr])
    dif_abertura = (a30t - a30f) if a30t is not None and a30f is not None else None
    H.append({
        "id": "H4", "texto": "O tema explica 20 a 50x da diferença de views; a abertura quase não separa top de fracos",
        "numeros": [f"mediana de views do melhor tema ÷ pior tema (longos, temas com ≥ 3 vídeos): {f(razao_tema)}x",
                    f"parte da variação de log(views) explicada pelo tema (eta²): {f(100 * eta if eta is not None else None)}%",
                    f"retenção aos 30 s, top × fracos: {f(a30t)}% × {f(a30f)}% (diferença {f(dif_abertura)} p.p.; "
                    "vem de retencao_30s.csv)",
                    f"proxy sem os 30 s: % média assistida, top × fracos: {f(pmt)}% × {f(pmf)}%"],
        "veredito": veredito(razao_tema is not None and 20 <= razao_tema <= 50 and (dif_abertura is None or dif_abertura <= 5),
                             razao_tema is not None and razao_tema >= 5, razao_tema is not None),
        "regra": "CONFIRMA se a razão de temas ∈ [20; 50]x e a abertura difere ≤ 5 p.p. (ou não foi medida); "
                 "PARCIAL se a razão ≥ 5x; DERRUBA abaixo. Sem retencao_30s.csv a parte da abertura fica em aberto.",
    })
    # H5: Shorts davam 40% dos inscritos e foram encerrados em 28/07.
    meses_antes = [r for r in d.mes if r["mes"] < f"{DATA_SHORTS_FIM:%Y-%m}"][-6:]
    gs = sum(num(r.get("inscritos_ganhos_shorts")) or 0 for r in meses_antes)
    gt_ = sum(num(r.get("inscritos_ganhos")) or 0 for r in meses_antes)
    share_mes = pct(gs, gt_) if any(r.get("inscritos_ganhos_shorts") for r in meses_antes) else None
    sv = [v for v in d.v.values() if v["formato"] == "short"]
    share_vid = pct(sum(v["ganhos"] or 0 for v in sv), sum(v["ganhos"] or 0 for v in d.v.values())) \
        if any(v["ganhos"] is not None for v in d.v.values()) else None
    ultimo = max((v["publicado"] for v in sv if v["publicado"]), default=None)
    depois_fim = sum(1 for v in sv if v["publicado"] and v["publicado"] > DATA_SHORTS_FIM)
    share = share_mes if share_mes is not None else share_vid
    H.append({
        "id": "H5", "texto": f"Os Shorts davam 40% dos inscritos e foram encerrados em {DATA_SHORTS_FIM:%d/%m/%Y}",
        "numeros": [f"% dos inscritos ganhos vindos de Shorts nos 6 meses antes de {DATA_SHORTS_FIM:%m/%Y} "
                    f"(canal_por_mes): {f(share_mes)}%",
                    f"% dos inscritos ganhos em Shorts no período todo (por vídeo): {f(share_vid)}%",
                    f"último Short publicado: {ultimo or '—'}; Shorts publicados depois de {DATA_SHORTS_FIM:%d/%m}: {depois_fim}"],
        "veredito": veredito(share is not None and 30 <= share <= 50 and depois_fim == 0,
                             share is not None and share >= 20, share is not None),
        "regra": "CONFIRMA se a fatia ∈ [30; 50]% e não houve Short depois de 28/07; PARCIAL se a fatia ≥ 20%; "
                 "DERRUBA abaixo.",
    })
    return H


def eta2(y, grupos):
    if len(y) < 3:
        return None
    m = statistics.mean(y)
    sst = sum((v - m) ** 2 for v in y)
    if not sst:
        return None
    g = defaultdict(list)
    for v, k in zip(y, grupos):
        g[k].append(v)
    ssb = sum(len(l) * (statistics.mean(l) - m) ** 2 for l in g.values())
    return ssb / sst


# ------------------------------------------------------------------------------------------------ comentários
def analise_comentarios(d):
    cs = d.comentarios
    if not cs:
        return None
    publico = [c for c in cs if c.get("eh_do_canal") != "1"]
    perguntas = [c for c in publico if c.get("eh_resposta") == "0" and PERGUNTA.search(norm(c.get("texto", "")))]
    respondidos = {c["resposta_a"] for c in cs if c.get("eh_do_canal") == "1" and c.get("resposta_a")}
    termos = Counter()
    for c in perguntas:
        ws = [w for w in re.findall(r"[a-z0-9]+", norm(c["texto"])) if len(w) > 2 and w not in STOP]
        termos.update(set(ws))
        termos.update({f"{a} {b}" for a, b in zip(ws, ws[1:])})
    temas = Counter(tema(c["texto"]) for c in perguntas)
    return {"total": len(cs), "publico": len(publico), "perguntas": len(perguntas),
            "pct_perguntas": pct(len(perguntas), sum(c.get("eh_resposta") == "0" for c in publico)),
            "pct_perguntas_respondidas": pct(sum(c["comentario_id"] in respondidos for c in perguntas), len(perguntas)),
            "termos": termos.most_common(25), "temas": temas.most_common(),
            "mais_curtidas": sorted(perguntas, key=lambda c: -(num(c.get("likes")) or 0))[:15]}


# ------------------------------------------------------------------------------------------------ saída
def relatorio(d):
    L = ["# Resultados da auditoria (gerado por analisar.py)", "",
         f"Dados até {d.data_ref}. {len(d.v)} vídeos; {sum(v['formato'] == 'short' for v in d.v.values())} Shorts. "
         f"Exportações do Studio: {', '.join(k for k in d.studio) or 'nenhuma'}.", ""]
    if any(d.casamento.values()):
        L += [f"Studio casado com videos.csv: {d.casamento['por_id']} por ID, {d.casamento['por_titulo']} por título, "
              f"{d.casamento['sem_par']} sem par.", ""]
    todos = list(d.v.values())
    L += ["## 1. Conversão por formato (inscritos ganhos por mil views)", "",
          tabela_md(["formato", "vídeos", "views", "% views", "mediana views", "insc./mil views",
                     "insc./mil engajadas", "% média assistida", "CTR mediano"],
                    [[r["grupo"], r["n"], f(r["views"], 0), f(r["pct_views"]), f(r["mediana_views"], 0),
                      f(r["insc_mil"], 2), f(r["engajadas_mil"], 2), f(r["pct_media"]), f(r["ctr"], 2)]
                     for r in por_grupo(todos, "formato")]), ""]
    for fmt in ("longo", "short"):
        vs = [v for v in todos if v["formato"] == fmt]
        if vs:
            L += [f"## 2{'a' if fmt == 'longo' else 'b'}. Por tema ({fmt}s)", "",
                  tabela_md(["tema", "vídeos", "views", "% views", "mediana views", "insc./mil views", "CTR mediano",
                             "% média assistida"],
                            [[r["grupo"], r["n"], f(r["views"], 0), f(r["pct_views"]), f(r["mediana_views"], 0),
                              f(r["insc_mil"], 2), f(r["ctr"], 2), f(r["pct_media"])] for r in por_grupo(vs, "tema")]), ""]
    L += ["## 3. Concentração das views", ""]
    linhas = []
    for nome, vs in (("todos", todos), ("longos", [v for v in todos if v["formato"] == "longo"]),
                     ("shorts", [v for v in todos if v["formato"] == "short"])):
        c = concentracao(vs)
        if c:
            linhas.append([nome, c["n"], f(c["top1"]), f(c["top5"]), f(c["top10"]), f(c["top10pct"]), c["n50"], c["n80"],
                           f(c["gini"], 2)])
    L += [tabela_md(["grupo", "vídeos", "% top 1", "% top 5", "% top 10", "% top 10% dos vídeos", "vídeos p/ 50%",
                     "vídeos p/ 80%", "Gini"], linhas), ""]
    top, fr = top_fracos(d)
    pt, pf = perfil(top), perfil(fr)
    if pt:
        L += [f"## 4. Top × fracos (longos de {POPULACAO_MIN_VIDA} a {POPULACAO_DIAS} dias de vida; quartil de cima × de baixo)", ""]
        rotulos = [("n", "vídeos", 0), ("mediana_views", "mediana de views", 0), ("insc_mil", "inscritos por mil views", 2),
                   ("tema_principal", "temas", None), ("caso_com_nome", "% caso com nome", 0),
                   ("duracao_min", "duração mediana (min)", 1), ("titulo_chars", "título: caracteres", 0),
                   ("titulo_com_numero", "% título com número", 0), ("titulo_com_pergunta", "% título com ?", 0),
                   ("titulo_caixa_alta", "% título em caixa alta", 0), ("dia_mais_comum", "dia mais comum", None),
                   ("hora_mediana", "hora mediana (Brasília)", 0), ("ctr", "CTR mediano (%)", 2),
                   ("impressoes", "impressões medianas", 0), ("pct_media", "% média assistida", 1),
                   ("pct_30s", "retenção aos 30 s (%)", 1)]
        L += [tabela_md(["", "top", "fracos"], [[r, f(pt.get(k), c) if c is not None else (pt.get(k) or "—"),
                                                  f(pf.get(k), c) if c is not None else (pf.get(k) or "—")]
                                                 for k, r, c in rotulos]), ""]
    curva = curva_mensal(d)
    if curva:
        L += ["## 5. Mês a mês", "", tabela_md(
            ["mês", "views", "minutos", "inscritos líquidos", "insc./mil views", "% engajadas", "% views Shorts",
             "% inscritos de Shorts"],
            [[r["mes"], f(r["views"], 0), f(r["minutos"], 0), f(r["liquidos"], 0), f(r["insc_mil"], 2),
              f(r["engajadas_pct"]), f(r["pct_views_shorts"]), f(r["pct_insc_shorts"])] for r in curva]), ""]
    om = origem_por_mes(d)
    if om:
        principais = [o for o, _ in Counter({o: p for m in om.values() for o, p in m.items()}).most_common()]
        foco = [o for o in ("RELATED_VIDEO", "BROWSE", "YT_SEARCH", "SUBSCRIBER", "SHORTS", "EXT_URL", "NO_LINK_OTHER")
                if o in principais]
        L += ["## 6. Origem do tráfego (% das views do mês, API)", "",
              "RELATED_VIDEO = vídeos sugeridos (\"Recomendados\"); BROWSE = Início/Inscrições.", "",
              tabela_md(["mês"] + foco, [[m] + [f(om[m].get(o)) for o in foco] for m in om]), ""]
    for base in ("studio_origem_trafego_mensal", "studio_origem_trafego_mensal_longos", "studio_origem_trafego_mensal_shorts"):
        ls = linhas_origem_mes(d.studio.get(base) or {})
        if ls:
            L += [f"### 6b. {base} (Studio: views, impressões e CTR por origem)", "", tabela_md(
                ["mês", "origem", "views", "impressões", "CTR (%)", "horas"],
                [[r["mes"], r["origem"], f(r["views"], 0), f(r["impressoes"], 0), f(r["ctr"], 2), f(r["horas"], 0)]
                 for r in ls]), ""]
    L += ["## 7. Hipóteses (a confirmar ou derrubar)", ""]
    for h in hipoteses(d):
        L += [f"### {h['id']}. {h['texto']} → **{h['veredito']}**", ""] + [f"- {n}" for n in h["numeros"]] + \
             [f"- Regra: {h['regra']}", ""]
    c = analise_comentarios(d)
    if c:
        L += ["## 8. O que o público pergunta", "",
              f"{c['total']} comentários; {c['perguntas']} perguntas ({f(c['pct_perguntas'])}% dos comentários de topo do "
              f"público); {f(c['pct_perguntas_respondidas'])}% das perguntas têm resposta do canal.", "",
              "Temas das perguntas: " + ", ".join(f"{t} ({n})" for t, n in c["temas"]), "",
              "Termos mais frequentes nas perguntas: " + ", ".join(f"{t} ({n})" for t, n in c["termos"]), "",
              "Perguntas mais curtidas:", ""]
        L += [f"- ({c_['likes']} likes, {c_['video_id']}) {c_['texto'][:200].replace(chr(10), ' ')}" for c_ in c["mais_curtidas"]]
        L.append("")
    if d.studio.get("ask_studio"):
        L += ["## 9. Anotações do Ask Studio (texto colado pelo Denis)", "", "> " +
              d.studio["ask_studio"][:4000].replace("\n", "\n> "), ""]
    return "\n".join(L)


def lista_retencao(d, n=10):
    top, fr = top_fracos(d, n)
    return [{"grupo": g, "video_id": v["id"], "titulo": v["titulo"], "views": int(v["views"] or 0),
             "publicado": v["publicado"], "pct_30s": "",
             "studio": f"https://studio.youtube.com/video/{v['id']}/analytics/tab-overview/period-default"}
            for g, l in (("top", top), ("fraco", fr)) for v in l]


def gravar(p, cab, regs):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cab, extrasaction="ignore")
        w.writeheader()
        w.writerows(regs)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Calcula as tabelas do relatório a partir de dados/.")
    ap.add_argument("--dados", type=Path, default=AQUI / "dados")
    ap.add_argument("--saida", type=Path, default=AQUI / "analise")
    ap.add_argument("--lista-retencao", action="store_true", help="só a lista de 10 top e 10 fracos (IDs)")
    args = ap.parse_args(argv)
    d = Dados(args.dados)
    if not d.v:
        print(f"não achei {args.dados / 'videos.csv'}: rode o exportar.py primeiro", file=sys.stderr)
        return 2
    lr = lista_retencao(d)
    gravar(args.saida / "lista_retencao_30s.csv", ["grupo", "video_id", "titulo", "views", "publicado", "pct_30s", "studio"], lr)
    if args.lista_retencao:
        for r in lr:
            print(f"{r['grupo']:5} {r['video_id']}  {r['views']:>9}  {r['titulo'][:70]}")
        print(f"\nPreencha pct_30s em {args.saida / 'lista_retencao_30s.csv'} e salve só video_id,pct_30s "
              f"como dados/studio/retencao_30s.csv.", file=sys.stderr)
        return 0
    gravar(args.saida / "temas_por_video.csv", ["id", "tema", "formato", "views", "titulo"],
           sorted(d.v.values(), key=lambda v: (v["tema"], -(v["views"] or 0))))
    (args.saida / "RESULTADOS.md").write_text(relatorio(d), encoding="utf-8")
    print(f"ok: {args.saida / 'RESULTADOS.md'}, temas_por_video.csv e lista_retencao_30s.csv")
    return 0


if __name__ == "__main__":
    sys.exit(main())
