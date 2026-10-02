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

# População de top × fracos (e da lista de retenção aos 30 s): só longos, publicados nos últimos 365 dias, com pelo
# menos 30 dias de vida e pelo menos 500 views intencionais. Ordem: inscritos ganhos (o que a meta pede), que não
# sofre com as views infladas depois de 27/08.
POPULACAO_DIAS, POPULACAO_MIN_VIDA, POPULACAO_MIN_INTENC = 365, 30, 500

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
agosto setembro outubro novembro dezembro natal ano novo black friday youtube shorts lula bolsonaro haddad
imoveis imovel perigo oculto grafico mercado bolsa valores renda passiva mensal mensais""".split())

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
                              r"renda fixa|dividendo|\b[a-z]{4}\d{1,2}\b"),  # ticker (BBAS3, CASA11) = produto, não "caso"
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
    palavras = [p for p in re.findall(r"[\wÀ-ÿ'’]+", titulo or "") if p[0].isalpha()]
    iniciais = [p[0].isupper() for p in palavras if len(p) > 3 and not p.isupper()]
    if iniciais and sum(iniciais) / len(iniciais) > 0.6:  # Título Em Caixa De Título: a regra não serve
        return False
    # Pares só dentro do mesmo trecho (":" "?" "|" etc. quebram), e nunca a primeira palavra do trecho.
    for trecho in re.split(r"[:;|?!.,()\[\]–—…-]", titulo or ""):
        ps = [p for p in re.findall(r"[\wÀ-ÿ'’]+", trecho) if p[0].isalpha()]
        cap = [len(p) > 1 and p[0].isupper() and not p.isupper() and norm(p) not in NAO_NOMES for p in ps]
        if any(cap[i] and cap[i + 1] for i in range(1, len(cap) - 1)):
            return True
    return False


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
    "impressoes": "impressoes", "impressions": "impressoes", "impressoes de miniaturas": "impressoes",
    "thumbnail impressions": "impressoes",
    "taxa de cliques na miniatura": "ctr", "thumbnail click-through rate": "ctr",
    "visualizacoes intencionais": "views_engajadas", "intentional views": "views_engajadas",
    "inscricoes obtidas": "inscritos_ganhos", "inscricoes": "inscritos",
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
    "feed dos shorts": "SHORTS", "notificacoes": "NOTIFICATION",
    "shorts feed": "SHORTS", "externo": "EXT_URL", "external": "EXT_URL",
    "direto ou desconhecido": "NO_LINK_OTHER", "direct or unknown": "NO_LINK_OTHER",
    "paginas do canal": "YT_CHANNEL", "channel pages": "YT_CHANNEL", "playlists": "PLAYLIST",
    "notificacoes": "NOTIFICATION", "notifications": "NOTIFICATION", "telas finais": "END_SCREEN",
    "end screens": "END_SCREEN", "outros recursos do youtube": "YT_OTHER_PAGE", "other youtube features": "YT_OTHER_PAGE",
    "externa": "EXT_URL", "origem direta ou desconhecida": "NO_LINK_OTHER", "publicidade no youtube": "ADVERTISING",
    "youtube advertising": "ADVERTISING", "anotacoes e cards de video": "ANNOTATION", "paginas de hashtag": "HASHTAGS",
    "shorts relacionados": "RELATED_SHORTS", "related shorts": "RELATED_SHORTS",
}
NOME_ORIGEM = {"RELATED_VIDEO": "Sugeridos", "BROWSE": "Navegação", "YT_SEARCH": "Pesquisa", "SHORTS": "Feed Shorts",
               "NOTIFICATION": "Notificações", "EXT_URL": "Externa", "YT_CHANNEL": "Pág. do canal"}
HOJE = None  # para testes; None = date.today(). O mês corrente (incompleto) sai das séries mensais do Studio.


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


def parse_data(v):
    """'2018-08-28', 'Aug 28, 2018', '28 de ago. de 2018', '28/08/2018' → date (ou None)."""
    s = norm(v)
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})", s)
    if m:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    m = re.match(r"([a-z]{3})[a-z]*\.? (\d{1,2}),? (\d{4})", s)
    if m and m.group(1) in MESES:
        return date(int(m.group(3)), MESES[m.group(1)], int(m.group(2)))
    m = re.match(r"(\d{1,2}) (?:de )?([a-z]{3})[a-z]*\.? (?:de )?(\d{4})", s)
    if m and m.group(2) in MESES:
        return date(int(m.group(3)), MESES[m.group(2)], int(m.group(1)))
    m = re.match(r"(\d{1,2})/(\d{1,2})/(\d{4})", s)
    if m:
        return date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
    return None


def _ler_texto_csv(texto):
    rs = list(csv.reader(io.StringIO(texto.lstrip("﻿"))))
    if not rs:
        return []
    cab = [chave_cab(c) or norm(c) for c in rs[0]]
    out = []
    for r in rs[1:]:
        d = {k: v.strip() for k, v in zip(cab, r)}  # o Studio põe espaço antes de IDs que começam com "-"
        if norm(d.get("video_id", "")) == "total" or norm(next(iter(d.values()), "")) == "total":
            TOTAIS[id(out)] = d
            continue
        out.append(d)
    return out


TOTAIS = {}  # id(lista de linhas) -> linha "Total" da Tabela do Studio


def linha_total(rs):
    return TOTAIS.get(id(rs))


def _papel(nome_arquivo):
    n = norm(Path(nome_arquivo).stem)
    if n.startswith(("tabela", "table", "dados da tabela")):
        return "tabela"
    if n.startswith(("totais", "totals", "total")):
        return "totais"
    if n.startswith(("grafico", "chart", "dados do grafico")):
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
        self.so_studio = not out
        self.fora_do_publico = []   # linhas do Studio cujo vídeo não está na playlist pública (privado/excluído)
        self.formato_corrigido = 0
        for base in ("studio_conteudo_longos", "studio_conteudo_shorts"):
            for r in (self.studio.get(base) or {}).get("tabela", []):
                vid = r.get("video_id", "").strip()
                if "views" not in r:      # "Mostrando os primeiros 500 resultados"
                    continue
                if self.so_studio and vid:
                    # Sem videos.csv: a base vem do próprio Studio (formato = de qual exportação veio).
                    out[vid] = {"id": vid, "titulo": r.get("titulo", ""), "publicado": parse_data(r.get("publicado")),
                                "formato": "short" if base.endswith("shorts") else "longo", "dia_semana": None,
                                "hora": None, "duracao_s": num(r.get("duracao_s")), "views_publico": num(r.get("views")),
                                "views": num(r.get("views")), "minutos": (num(r.get("horas")) or 0) * 60,
                                "pct_media": None, "ganhos": None, "perdidos": None, "engajadas": None,
                                "impressoes": None, "ctr": None, "pct_30s": None, "inscritos_studio": None,
                                "tema": tema(r.get("titulo", ""), manual.get(vid)), "fonte_ctr": ""}
                if vid not in out:
                    vid = por_titulo.get(norm(r.get("titulo", "")))
                    self.casamento["por_titulo" if vid else "sem_par"] += 1
                else:
                    self.casamento["por_id"] += 1
                if not vid:
                    self.fora_do_publico.append(dict(r, formato="short" if base.endswith("shorts") else "longo"))
                    continue
                v = out[vid]
                fmt = "short" if base.endswith("shorts") else "longo"  # o Studio sabe o formato real
                if v["formato"] != fmt:
                    v["formato"] = fmt
                    self.formato_corrigido += 1
                for campo_st, campo in (("impressoes", "impressoes"), ("ctr", "ctr"), ("views_engajadas", "engajadas")):
                    if campo == "engajadas" and v["engajadas"] is not None:
                        continue
                    if num(r.get(campo_st)) is not None:
                        v[campo] = num(r.get(campo_st))
                        if campo != "engajadas":
                            v["fonte_ctr"] = "Studio"
                if v["pct_media"] is None:
                    v["pct_media"] = num(r.get("pct_media"))
                v["inscritos_studio"] = num(r.get("inscritos_ganhos")) if num(r.get("inscritos_ganhos")) is not None \
                    else num(r.get("inscritos"))
        for r in self.studio.get("retencao_30s", []):
            if r.get("video_id", "").strip() in out:
                out[r["video_id"].strip()]["pct_30s"] = num(r.get("pct_30s"))
        return out

    @property
    def data_ref(self):
        datas = [r["dia"] for r in self.dia] + [str(v["publicado"]) for v in self.v.values() if v["publicado"]]
        return date.fromisoformat(max(datas)[:10]) if datas else date.today()


# ------------------------------------------------------------------------------------------------ análises
def ganhos(v):
    """Inscritos ganhos do Analytics; sem ele, os do Studio ("Inscrições obtidas")."""
    return (v["ganhos"] if v["ganhos"] is not None else v["inscritos_studio"]) or 0


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
                    "engajadas_mil": por_mil(sum((v["ganhos"] if v["ganhos"] is not None else v["inscritos_studio"]) or 0
                                                 for v in l), sum(v["engajadas"] or 0 for v in l))
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
            and POPULACAO_MIN_VIDA <= (ref - v["publicado"]).days <= POPULACAO_DIAS and v["views"] is not None
            and (v["engajadas"] if v["engajadas"] is not None else v["views"]) >= POPULACAO_MIN_INTENC]


def metrica_rank(v):
    return (ganhos(v), v["engajadas"] or v["views"] or 0)


def top_fracos(d, n=None):
    pop = sorted(populacao_longos(d), key=lambda v: tuple(-x for x in metrica_rank(v)))
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
        "mediana_insc": mediana([ganhos(v) for v in vs]), "mediana_intenc": mediana([v["engajadas"] for v in vs]),
        "insc_mil_intenc": por_mil(sum(ganhos(v) for v in vs), sum(v["engajadas"] or 0 for v in vs)),
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
    vm, mod = views_mensais_studio(d), modelo_inscritos(d)
    for r in d.mes:
        views = num(r.get("views")) or 0
        g, p = num(r.get("inscritos_ganhos")) or 0, num(r.get("inscritos_perdidos")) or 0
        gs = num(r.get("inscritos_ganhos_shorts"))
        out.append({"mes": r["mes"], "views": views, "minutos": num(r.get("minutos")), "liquidos": g - p,
                    "insc_mil": por_mil(g, views), "engajadas_pct": pct(num(r.get("engagedViews")) or 0, views)
                    if num(r.get("engagedViews")) else None,
                    "pct_views_shorts": pct(num(r.get("views_shorts")) or 0, views) if r.get("views_shorts") else None,
                    "pct_insc_shorts": pct(gs, g) if gs is not None and g else None, "ganhos": g, "perdidos": p,
                    "views_longos": vm["longo"].get(r["mes"]) if vm else None,
                    "views_shorts_st": vm["short"].get(r["mes"]) if vm else None, "est": False})
        o = out[-1]
        if o["pct_views_shorts"] is None and vm:
            t = (o["views_longos"] or 0) + (o["views_shorts_st"] or 0)
            o["pct_views_shorts"] = pct(o["views_shorts_st"] or 0, t) if t else None
        if o["pct_insc_shorts"] is None and mod and r["mes"] in mod["por_mes"]:
            pm = mod["por_mes"][r["mes"]]
            o["pct_insc_shorts"] = pct(pm["est_shorts"], pm["est_shorts"] + pm["est_longos"])
            o["est"] = True
    return out


def _mes_fechado(m):
    hoje = HOJE or date.today()
    return m < f"{hoje:%Y-%m}"


def origem_mensal_studio(exp):
    """{mes: {origem (código da API se conhecido): views}} de uma exportação de origem × mês do Studio."""
    out = defaultdict(lambda: defaultdict(float))
    for r in linhas_origem_mes(exp):
        if _mes_fechado(r["mes"]):
            out[r["mes"]][r["origem_api"] or r["origem"]] += r["views"]
    return dict(sorted(out.items()))


def origens_studio(d):
    """Séries do Studio por formato: todos, longos e shorts (exportação própria ou todos − longos)."""
    series = {}
    for nome, base in (("todos", "studio_origem_trafego_mensal"), ("longos", "studio_origem_trafego_mensal_longos"),
                       ("shorts", "studio_origem_trafego_mensal_shorts")):
        if d.studio.get(base):
            series[nome] = origem_mensal_studio(d.studio[base])
    if "shorts" not in series and "todos" in series and "longos" in series:
        sh = {}
        for m, o in series["todos"].items():
            lo = series["longos"].get(m, {})
            sh[m] = {k: max(0.0, v - lo.get(k, 0)) for k, v in o.items()}
        series["shorts (todos − longos)"] = sh
    return series


def pct_mes(serie):
    out = {}
    for m, o in serie.items():
        t = sum(o.values())
        out[m] = {k: 100 * v / t for k, v in o.items()} if t else {}
        out[m]["_total"] = t
    return out


def queda(pcts, origem, n_meses=18):
    """Mediana dos 3 primeiros meses da janela, pico na janela e mediana dos 2 últimos (meses fechados)."""
    ms = list(pcts)[-n_meses:]
    if len(ms) < 5:
        return None
    s = [pcts[m].get(origem, 0) for m in ms]
    pico = max(zip(s, ms))
    todos = [(pcts[m].get(origem, 0), m) for m in pcts if pcts[m].get("_total", 0) >= 1000]
    hist = max(todos) if todos else (None, None)
    return {"inicio": mediana(s[:3]), "pico": pico[0], "mes_pico": pico[1], "fim": mediana(s[-2:]),
            "ultimo": s[-1], "de": ms[0], "ate": ms[-1], "pico_hist": hist[0], "mes_pico_hist": hist[1]}


def origem_por_mes(d):
    """% das views por origem e mês (API). Na Analytics API, "SUBSCRIBER" é o que o Studio chama de Recursos de
    navegação (Início, Inscrições, Assistir mais tarde): aqui vira BROWSE."""
    tab = defaultdict(lambda: defaultdict(float))
    for r in d.trafego_mes:
        o = "BROWSE" if r["origem"] == "SUBSCRIBER" else r["origem"]
        tab[r["mes"]][o] += num(r.get("pct_views_mes")) or 0
    return {m: dict(v) for m, v in sorted(tab.items())}


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


def outliers(vs, limite=0.4):
    """Vídeos que sozinhos têm ≥ 40% das views do grupo (ex.: o Short "1 centavo"): tratados à parte."""
    total = sum(v["views"] or 0 for v in vs)
    if len(vs) < 5 or not total:
        return []
    return [v for v in vs if (v["views"] or 0) >= limite * total]


CAMPOS_TOTAL = [("impressoes", "impressões", 0), ("ctr", "CTR (%)", 2), ("views", "views", 0),
                ("views_engajadas", "views intencionais", 0), ("horas", "horas", 1), ("inscritos_ganhos", "inscritos", 0)]


def conferencia_studio(d):
    """Soma as linhas da Tabela do Studio e compara com a linha Total (o CTR é ponderado pelas impressões)."""
    out = []
    for base in ("studio_conteudo_longos", "studio_conteudo_shorts"):
        rs = (d.studio.get(base) or {}).get("tabela") or []
        if not rs:
            continue
        tot = linha_total(rs) or {}
        for campo, rotulo, casas in CAMPOS_TOTAL:
            if campo not in rs[0] and not (campo == "inscritos_ganhos" and "inscritos" in rs[0]):
                continue
            c = campo if campo in rs[0] else "inscritos"
            if c == "ctr":
                imp = soma(rs, "impressoes")
                calc = sum((num(r.get("ctr")) or 0) * (num(r.get("impressoes")) or 0) for r in rs) / imp if imp else None
            else:
                calc = soma(rs, c)
            t = num(tot.get(c))
            dif = pct(calc - t, t) if t and calc is not None else None
            out.append({"exportacao": base.replace("studio_conteudo_", ""), "metrica": rotulo, "total_studio": t,
                        "soma_linhas": calc, "dif_pct": dif, "casas": casas, "n": len(rs)})
    return out


def studio_por_formato(d):
    """Views ÷ views intencionais por formato e período de publicação, com e sem outliers."""
    out = []
    for fmt in ("longo", "short"):
        vs = [v for v in d.v.values() if v["formato"] == fmt and v["engajadas"]]
        if not vs:
            continue
        fora = outliers(vs)
        grupos = [("todos", vs)]
        if fora:
            grupos.append(("sem outlier", [v for v in vs if v not in fora]))
        if fmt == "short":
            grupos += [(f"publicados antes de {DATA_SHORTS_NOVA_CONTAGEM:%d/%m/%Y}",
                        [v for v in vs if v not in fora and v["publicado"] and v["publicado"] < DATA_SHORTS_NOVA_CONTAGEM]),
                       (f"publicados a partir de {DATA_SHORTS_NOVA_CONTAGEM:%d/%m/%Y}",
                        [v for v in vs if v not in fora and v["publicado"] and v["publicado"] >= DATA_SHORTS_NOVA_CONTAGEM])]
        else:
            grupos += [(f"publicados antes de {DATA_INFLACAO:%d/%m/%Y}",
                        [v for v in vs if v["publicado"] and v["publicado"] < DATA_INFLACAO]),
                       (f"publicados a partir de {DATA_INFLACAO:%d/%m/%Y}",
                        [v for v in vs if v["publicado"] and v["publicado"] >= DATA_INFLACAO])]
        for nome, g in grupos:
            if not g:
                continue
            vw, en = sum(v["views"] or 0 for v in g), sum(v["engajadas"] or 0 for v in g)
            imp = sum(v["impressoes"] or 0 for v in g)
            ctr = sum((v["ctr"] or 0) * (v["impressoes"] or 0) for v in g) / imp if imp else None
            out.append({"formato": fmt, "grupo": nome, "n": len(g), "views": vw, "intencionais": en,
                        "razao": vw / en if en else None, "razao_mediana": razao_mediana(g, "views", "engajadas"),
                        "insc_mil": conversao(g), "insc_mil_intenc": por_mil(sum(v["inscritos_studio"] or v["ganhos"] or 0
                                                                                for v in g), en),
                        "ctr": ctr, "impressoes": imp,
                        "outliers": ", ".join(f"{v['id']} ({v['titulo'][:40]})" for v in fora) if nome == "sem outlier" else ""})
    return out


def views_mensais_studio(d):
    """{'longo': {mes: views}, 'short': {...}} a partir do Total.csv (série diária) das exportações de conteúdo."""
    out = {}
    for fmt, base in (("longo", "studio_conteudo_longos"), ("short", "studio_conteudo_shorts")):
        rs = (d.studio.get(base) or {}).get("totais") or []
        if rs and "views" in rs[0]:
            m = defaultdict(float)
            for r in rs:
                k = parse_mes(r.get("data", ""))
                if k:
                    m[k] += num(r.get("views")) or 0
            out[fmt] = dict(m)
    return out if len(out) == 2 else {}


def modelo_inscritos(d):
    """Inscritos ganhos no mês ≈ a·views de longos + b·views de Shorts (mínimos quadrados, sem intercepto), nos
    meses fechados de canal_por_mes ANTES do mês de DATA_INFLACAO+1 (setembro tem views infladas e distorceria)."""
    vm = views_mensais_studio(d)
    if not vm or not d.mes:
        return None
    corte = f"{(DATA_INFLACAO.replace(day=28) + timedelta(days=4)):%Y-%m}"
    pts = [(vm["longo"].get(r["mes"], 0), vm["short"].get(r["mes"], 0), num(r["inscritos_ganhos"]) or 0, r["mes"])
           for r in d.mes if r["mes"] < corte]
    if len(pts) < 6:
        return None
    a11 = sum(l * l for l, s_, y, m in pts); a12 = sum(l * s_ for l, s_, y, m in pts)
    a22 = sum(s_ * s_ for l, s_, y, m in pts)
    b1 = sum(l * y for l, s_, y, m in pts); b2 = sum(s_ * y for l, s_, y, m in pts)
    det = a11 * a22 - a12 * a12
    if not det:
        return None
    a, b = (b1 * a22 - b2 * a12) / det, (a11 * b2 - a12 * b1) / det
    ys = [y for *_, y, m in pts]
    sst = sum((y - statistics.mean(ys)) ** 2 for y in ys)
    sse = sum((y - a * l - b * s_) ** 2 for l, s_, y, m in pts)

    def share(ini, fim):
        sel = [(l, s_) for l, s_, y, m in pts if (ini is None or m >= ini) and (fim is None or m <= fim)]
        tot = sum(a * l + b * s_ for l, s_ in sel)
        return pct(sum(b * s_ for l, s_ in sel), tot) if tot else None
    out = {"a": 1000 * a, "b": 1000 * b, "r2": 1 - sse / sst if sst else None, "n": len(pts), "share": share,
           "por_mes": {m: {"longo": l, "short": s_, "ganhos": y, "est_shorts": b * s_, "est_longos": a * l}
                       for l, s_, y, m in pts}}
    mes_check = corte
    linha = next((r for r in d.mes if r["mes"] == mes_check), None)
    ant = f"{(date.fromisoformat(mes_check + '-01') - timedelta(days=1)):%Y-%m}"
    if linha and vm["longo"].get(mes_check):
        out["check"] = {"mes": mes_check, "views_longos": vm["longo"][mes_check],
                        "x_mes_anterior": vm["longo"][mes_check] / vm["longo"][ant] if vm["longo"].get(ant) else None,
                        "ganhos": num(linha["inscritos_ganhos"]),
                        "esperado": a * vm["longo"][mes_check] + b * vm["short"].get(mes_check, 0)}
    return out


# ------------------------------------------------------------------------------------------------ hipóteses
def veredito(cond_confirma, cond_parcial, tem_dados):
    if not tem_dados:
        return "SEM DADOS"
    return "CONFIRMA" if cond_confirma else "PARCIAL" if cond_parcial else "DERRUBA"


def hipoteses(d):
    H = []
    # H1: contador público inflado desde 27/08.
    serie = [dict(r, _d=date.fromisoformat(r["dia"])) for r in d.dia]
    ra_c, rd_c, fator_eng, na, nd = comparar_periodos(serie, DATA_INFLACAO, JANELA_DIAS, "views", "engagedViews")
    _, _, fator_min, _, _ = comparar_periodos(serie, DATA_INFLACAO, JANELA_DIAS, "views", "minutos")
    longos = [v for v in d.v.values() if v["formato"] == "longo" and v["publicado"]]
    antes = [v for v in longos if DATA_INFLACAO - timedelta(days=120) <= v["publicado"] < DATA_INFLACAO]
    depois = [v for v in longos if v["publicado"] >= DATA_INFLACAO]

    def razao_soma(vs, a="views", b="engajadas"):
        vs = [v for v in vs if v.get(a) and v.get(b)]
        bb = sum(v[b] for v in vs)
        return (sum(v[a] for v in vs) / bb if bb else None), len(vs)
    (ra, n_a), (rd, n_d) = razao_soma(antes), razao_soma(depois)
    fator_vid = rd / ra if ra and rd else None
    shorts = [v for v in d.v.values() if v["formato"] == "short" and v["publicado"]]
    shorts = [v for v in shorts if v not in outliers(shorts)]
    sa, _ = razao_soma([v for v in shorts if v["publicado"] < DATA_SHORTS_NOVA_CONTAGEM])
    sd, _ = razao_soma([v for v in shorts if v["publicado"] >= DATA_SHORTS_NOVA_CONTAGEM])
    # Cada vídeo longo novo é o teste mais direto; sem eles, a série diária do canal (que mistura Shorts).
    fator = fator_vid if n_d >= 3 else fator_eng or fator_min
    mod = modelo_inscritos(d)
    numeros = [
        f"longos publicados a partir de {DATA_INFLACAO:%d/%m} (n = {n_d}): views ÷ views intencionais = {f(rd, 2)}; "
        f"longos dos 120 dias anteriores (n = {n_a}): {f(ra, 2)} → fator {f(fator_vid, 2)}x (Analytics por vídeo)",
        f"canal inteiro, {JANELA_DIAS} dias antes × depois (canal_por_dia, {na}+{nd} dias): views ÷ intencionais "
        f"{f(ra_c, 2)} → {f(rd_c, 2)} ({f(fator_eng, 2)}x); views por minuto assistido {f(fator_min, 2)}x. "
        "O canal mistura Shorts, cuja razão já era ~2.",
        f"Shorts: views ÷ intencionais {f(sa, 2)} nos publicados antes de {DATA_SHORTS_NOVA_CONTAGEM:%d/%m/%Y} e "
        f"{f(sd, 2)} depois, sem o outlier (mudança de contagem dos Shorts, outro efeito)",
    ]
    if mod and mod.get("check"):
        c = mod["check"]
        numeros.append(f"{c['mes']}: views de longos {f(c['views_longos'], 0)} ({f(c['x_mes_anterior'], 1)}x o mês "
                       f"anterior), mas inscritos ganhos {f(c['ganhos'], 0)}; pelo modelo de conversão seriam "
                       f"{f(c['esperado'], 0)}. As views a mais não trouxeram inscritos.")
    H.append({
        "id": "H1", "texto": f"Desde {DATA_INFLACAO:%d/%m/%Y} o contador público de views está inflado 2,5 a 2,8x",
        "numeros": numeros,
        "veredito": veredito(fator is not None and fator >= 2.2, fator is not None and fator >= 1.3,
                             fator is not None) + (" (inflação maior que a hipótese)" if fator and fator > 3.2 else "")
                    + (f" — amostra pequena: {n_d} longos" if 0 < n_d < 15 else ""),
        "regra": "Fator = (views ÷ intencionais dos longos publicados depois) ÷ (o mesmo nos 120 dias antes); sem "
                 "longos novos, a série diária do canal. CONFIRMA se ≥ 2,2x; PARCIAL se ≥ 1,3x; DERRUBA abaixo.",
    })
    # H2: conversão por tema, em duas janelas: vitalício e longos publicados nos últimos 12 meses.
    ref = d.data_ref
    janelas = [("últimos 12 meses", [v for v in d.v.values() if v["formato"] == "longo" and v["publicado"]
                                     and (ref - v["publicado"]).days <= 365]),
               ("vitalício", [v for v in d.v.values() if v["formato"] == "longo"])]
    numeros, res = [], {}
    for nome, vs in janelas:
        g = {r["grupo"]: r for r in por_grupo(vs, "tema")}
        res[nome] = g
        numeros.append(f"{nome}: " + "; ".join(
            f"{k} {f(v['insc_mil'], 1)}/mil (n = {v['n']})"
            for k, v in sorted(g.items(), key=lambda kv: -(kv[1]["insc_mil"] or 0))))
    g = res["últimos 12 meses"]
    caso = (g.get(TEMA_CASO) or {}).get("insc_mil")
    outros = [x for x in ((g.get("alerta macro") or {}).get("insc_mil"), (g.get("plano de renda") or {}).get("insc_mil"))
              if x is not None]
    ref_o = statistics.mean(outros) if outros else None
    n_caso = (g.get(TEMA_CASO) or {}).get("n", 0)
    H.append({
        "id": "H2", "texto": "Vídeos de caso com nome convertem 6 a 8 inscritos por mil views; alerta macro e plano de renda ~2",
        "numeros": numeros + [f"razão caso ÷ (alerta macro, plano de renda), últimos 12 meses: "
                              f"{f(caso / ref_o if caso and ref_o else None, 2)}x"],
        "veredito": veredito(caso is not None and 5 <= caso <= 9 and ref_o is not None and 1 <= ref_o <= 3,
                             caso is not None and ref_o and caso / ref_o >= 1.5, caso is not None and ref_o is not None)
                    + (f" — amostra pequena: {n_caso} vídeos de caso" if 0 < n_caso < 10 else ""),
        "regra": "Inscritos ganhos ÷ views (Analytics) × 1000, longos publicados nos últimos 12 meses. CONFIRMA se caso "
                 "∈ [5; 9] e a média de alerta macro/plano de renda ∈ [1; 3]; PARCIAL se caso ≥ 1,5× essa média; "
                 "DERRUBA abaixo. Tema por regra sobre o título: confira temas_por_video.csv.",
    })
    # H3: "Recomendados" de 29% para 2%. Em pt-BR pode ser Sugeridos (RELATED_VIDEO) ou Navegação (BROWSE,
    # a página inicial): testamos os dois, em cada formato, na API (se houver) e no Studio.
    series = {}
    if d.trafego_mes:
        series["API, todos"] = origem_por_mes(d)
    for nome, sr in origens_studio(d).items():
        series[f"Studio, {nome}"] = pct_mes(sr)
    resultados, numeros = [], []
    for nome, pc in series.items():
        for origem in ("RELATED_VIDEO", "BROWSE"):
            q = queda(pc, origem)
            if not q:
                continue
            ok = q["inicio"] >= 20 and q["fim"] <= 5 or (q["pico"] >= 20 and q["fim"] <= 5)
            meio = q["fim"] <= max(q["inicio"], q["pico"]) / 2
            dist = abs(max(q["inicio"], q["pico"]) - 29) + abs(q["fim"] - 2)
            resultados.append((dist, ok, meio, nome, origem, q))
            numeros.append(f"{nome} · {NOME_ORIGEM[origem]} ({origem}), {q['de']} a {q['ate']}: início {f(q['inicio'])}% · "
                           f"pico {f(q['pico'])}% em {q['mes_pico']} · fim (2 últimos) {f(q['fim'])}% · último mês {f(q['ultimo'])}% "
                           f"· pico histórico (meses com ≥ 1.000 views) {f(q['pico_hist'])}% em {q['mes_pico_hist'] or '—'}")
    if resultados:
        melhor = min(resultados, key=lambda r: r[0])
        numeros.append(f"A leitura que mais se aproxima de 29% → 2%: {melhor[3]} · {NOME_ORIGEM[melhor[4]]} "
                       f"({f(max(melhor[5]['inicio'], melhor[5]['pico']))}% → {f(melhor[5]['fim'])}%)")
    H.append({
        "id": "H3", "texto": "A origem \"Recomendados\" caiu de 29% para 2% das views",
        "numeros": numeros or ["sem série mensal de origem (trafego_por_mes.csv ou studio_origem_trafego_mensal)"],
        "veredito": veredito(any(r[1] for r in resultados), any(r[2] for r in resultados), bool(resultados)),
        "regra": "Testa Sugeridos (RELATED_VIDEO) e Navegação (BROWSE) em cada formato, nos últimos 18 meses fechados. "
                 "CONFIRMA se alguma série começa (ou tem pico) ≥ 20% e termina ≤ 5%; PARCIAL se caiu pela metade ou "
                 "mais; DERRUBA se não caiu.",
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
    # H5: Shorts davam ~40% dos inscritos e foram encerrados em 28/07.
    mod = modelo_inscritos(d)
    fim_m = f"{DATA_SHORTS_FIM:%Y-%m}"
    ini_m = f"{(DATA_SHORTS_FIM.replace(day=1) - timedelta(days=150)):%Y-%m}"   # 6 meses: fev a jul
    direto = [r for r in d.mes if r.get("inscritos_ganhos_shorts")]
    if direto:
        sel = [r for r in direto if ini_m <= r["mes"] <= fim_m]
        share6 = pct(sum(num(r["inscritos_ganhos_shorts"]) for r in sel), sum(num(r["inscritos_ganhos"]) for r in sel))
        share_all, fonte = None, "canal_por_mes (API, creatorContentType)"
    elif mod:
        share6, share_all = mod["share"](ini_m, fim_m), mod["share"](None, None)
        fonte = (f"estimativa: regressão dos inscritos ganhos do mês sobre as views de longos e de Shorts "
                 f"(Studio, {mod['n']} meses, R² = {f(mod['r2'], 2)}): {f(mod['a'], 1)} inscritos por mil views de "
                 f"longos e {f(mod['b'], 2)} por mil de Shorts")
    else:
        share6 = share_all = None
        fonte = "sem dados"
    sv = [v for v in d.v.values() if v["formato"] == "short" and v["publicado"]]
    pub = Counter(f"{v['publicado']:%Y-%m}" for v in sv)
    antes_pub = sum(pub[m] for m in pub if ini_m <= m <= fim_m)
    depois = sorted((v for v in sv if v["publicado"] > DATA_SHORTS_FIM), key=lambda v: v["publicado"])
    meses_depois = sorted({f"{v['publicado']:%Y-%m}" for v in depois})
    g_antes = [num(r["inscritos_ganhos"]) for r in d.mes if ini_m <= r["mes"] <= fim_m]
    g_depois = [num(r["inscritos_ganhos"]) for r in d.mes if r["mes"] > fim_m]
    vm = views_mensais_studio(d)
    vs_antes = [vm["short"].get(m, 0) for m in sorted(vm.get("short", {})) if ini_m <= m <= fim_m] if vm else []
    vs_depois = [vm["short"].get(m, 0) for m in sorted(vm.get("short", {})) if m > fim_m and _mes_fechado(m)] if vm else []
    numeros = [f"fatia dos inscritos ganhos vinda de Shorts, {ini_m} a {fim_m}: {f(share6)}%; "
               f"em toda a janela de {len(d.mes)} meses: {f(share_all)}% ({fonte})",
               f"Shorts publicados: {antes_pub} de {ini_m} a {fim_m} ({f(antes_pub / 6, 1)}/mês); depois de "
               f"{DATA_SHORTS_FIM:%d/%m}: {len(depois)} ({', '.join(f'{m}: {pub[m]}' for m in meses_depois)}). "
               "Os Shorts foram reduzidos, não encerrados." if depois else
               f"Shorts publicados depois de {DATA_SHORTS_FIM:%d/%m}: 0",
               f"inscritos ganhos por mês: média {f(statistics.mean(g_antes) if g_antes else None, 0)} de {ini_m} a "
               f"{fim_m} → {f(statistics.mean(g_depois) if g_depois else None, 0)} depois "
               f"({', '.join(f(x, 0) for x in g_depois)}); views de Shorts por mês: "
               f"{f(statistics.mean(vs_antes) if vs_antes else None, 0)} → "
               f"{f(statistics.mean(vs_depois) if vs_depois else None, 0)}"]
    share = share6 if share6 is not None else share_all
    parou = not depois
    H.append({
        "id": "H5", "texto": f"Os Shorts davam 40% dos inscritos e foram encerrados em {DATA_SHORTS_FIM:%d/%m/%Y}",
        "numeros": numeros,
        "veredito": veredito(share is not None and 30 <= max(share, share_all or 0) <= 50 and parou,
                             share is not None and max(share, share_all or 0) >= 20, share is not None),
        "regra": "CONFIRMA se a fatia ∈ [30; 50]% e não houve Short depois de 28/07; PARCIAL se a fatia ≥ 20% (ou os "
                 "Shorts só diminuíram); DERRUBA abaixo. Sem creatorContentType na API, a fatia é estimada.",
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


# Temas dos comentários (regras simples, como no radar de comentários). O primeiro que casar leva.
TEMAS_COMENTARIO = [
    ("Bancos digitais, contas e cartões", r"\bconta\b|cartao|cartoes|\bnext\b|nubank|banco inter|\binter\b|bradesco|"
                                         r"santander|itau|\bpix\b|debito|credito|anuidade|tarifa|agencia|abrir conta"),
    ("Menor de idade e filhos", r"menor de idade|de menor|\bmenor\b|meu filho|minha filha|meus filhos|crianca|\b1[0-7] anos\b"),
    ("Fundos imobiliários (FIIs)", r"\bfii|fiis|fundo imobiliario|fundos imobiliarios|ifix|\b[a-z]{4}11\b"),
    ("ETFs, BDRs e exterior", r"\betf|\bbdr|exterior|ivvb|s&p|nasdaq|dolar|cambio|\bjepi"),
    ("Tesouro Direto e renda fixa", r"tesouro|ipca|ntn|prefixad|\bcdb|\blci|\blca|renda fixa|selic|\bcdi\b|poupanca"),
    ("Dividendos e renda passiva", r"dividendo|provento|\bjcp|renda passiva|viver de renda|por mes|mensal"),
    ("Ações (empresas e tickers)", r"\b[a-z]{4}[3-6]\b|\bacao\b|\bacoes\b|bolsa|ibovespa|barsi"),
    ("Cripto", r"bitcoin|\bbtc\b|cripto|ethereum"),
    ("Aposentadoria e previdência", r"aposentad|previdencia|pgbl|vgbl|\binss"),
    ("Imposto de renda e tributação", r"imposto|\bir\b|tribut|isent|declara|darf|come.?cotas"),
    ("Começar com pouco / centavos", r"centavo|comecar|iniciante|pouco dinheiro|primeiro investimento|\b1 real\b"),
    ("Crise, governo e macro", r"crise|governo|calote|inflacao|juros|recessao|guerra|bolha|eleic"),
    ("Elogio ou agradecimento", r"parabens|obrigad|otimo video|excelente|top demais|muito bom|show|conteudo bom"),
    ("Crítica, dúvida sobre o conteúdo ou ironia", r"clickbait|caca.?clique|mentira|errado|golpe|kkk|enganad"),
]


def sem_arroba(texto):
    """Tira @menções (são nomes de usuários) e quebras de linha dos textos citados no relatório."""
    return re.sub(r"\s+", " ", re.sub(r"@[\w.\-]+", "@…", texto or "")).strip()


def tema_comentario(texto):
    t = norm(texto)
    for nome, rx in TEMAS_COMENTARIO:
        if re.search(rx, t):
            return nome
    return "outros"


def comentarios_por_tema(d):
    cs = [c for c in d.comentarios if c.get("eh_do_canal") != "1"]
    if not cs:
        return None
    por_video = Counter(c["video_id"] for c in cs)
    grupos = defaultdict(list)
    for c in cs:
        grupos[tema_comentario(c.get("texto", ""))].append(c)
    linhas = []
    for nome, l in sorted(grupos.items(), key=lambda kv: -len(kv[1])):
        perg = [c for c in l if PERGUNTA.search(norm(c.get("texto", "")))]
        base = l if nome.startswith(("Elogio", "Crítica")) else (perg or l)
        ex = sorted((c for c in base if 15 <= len(c.get("texto", "")) <= 160 and "@" not in c.get("texto", "")),
                    key=lambda c: -(num(c.get("likes")) or 0))[:2]
        linhas.append({"tema": nome, "n": len(l), "pct": pct(len(l), len(cs)), "perguntas": len(perg),
                       "exemplos": [sem_arroba(c["texto"])[:120] for c in ex]})
    return {"total": len(cs), "videos": len(por_video), "maior": por_video.most_common(1)[0], "linhas": linhas}


# ------------------------------------------------------------------------------------------------ saída
def relatorio(d):
    L = ["# Resultados da auditoria (gerado por analisar.py)", "",
         f"Dados até {d.data_ref}. {len(d.v)} vídeos; {sum(v['formato'] == 'short' for v in d.v.values())} Shorts. "
         f"Exportações do Studio: {', '.join(k for k in d.studio) or 'nenhuma'}.", ""]
    if any(d.casamento.values()):
        L += [f"Studio casado com videos.csv: {d.casamento['por_id']} por ID, {d.casamento['por_titulo']} por título, "
              f"{d.casamento['sem_par']} sem par.", ""]
    if d.so_studio:
        L += ["**Atenção:** sem videos.csv e sem Analytics: a base é só o Studio (formato = de qual exportação veio; "
              "dia e hora vazios). Rode o exportar.py no Mac para completar.", ""]
    conf = conferencia_studio(d)
    if conf:
        L += ["## 0. Conferência do Studio (soma das linhas × linha Total)", "", tabela_md(
            ["exportação", "vídeos", "métrica", "Total do Studio", "soma das linhas", "diferença %"],
            [[c["exportacao"], c["n"], c["metrica"], f(c["total_studio"], c["casas"]), f(c["soma_linhas"], c["casas"]),
              f(c["dif_pct"], 2)] for c in conf]), ""]
        cortadas = sorted({c["exportacao"] for c in conf if c["n"] >= 499 and c["dif_pct"] is not None
                           and abs(c["dif_pct"]) > 1 and c["metrica"] == "views"})
        if cortadas:
            L += [f"**A tabela do Studio de {', '.join(cortadas)} parou em ~500 linhas** (limite da exportação): a soma "
                  "das linhas não fecha com o Total, e as tabelas abaixo cobrem só esses vídeos. Para ter todos, exporte "
                  "em partes (filtrando por data de publicação) ou use o exportar.py (Analytics, sem esse limite).", ""]
    if getattr(d, "fora_do_publico", None):
        fp = d.fora_do_publico
        tot_l = num((linha_total((d.studio.get("studio_conteudo_longos") or {}).get("tabela") or []) or {}).get("views"))
        tot_i = num((linha_total((d.studio.get("studio_conteudo_longos") or {}).get("tabela") or []) or {}).get("inscritos_ganhos"))
        lo = [r for r in fp if r["formato"] == "longo"]
        L += ["## 0b. Vídeos do Studio fora da playlist pública (privados, não listados ou excluídos)", "",
              f"{len(fp)} vídeos do Studio não estão em videos.csv ({len(lo)} longos). Só entre os 500 longos da "
              f"exportação, eles somam {f(soma(lo, 'views'), 0)} views ({f(pct(soma(lo, 'views'), tot_l))}% das views "
              f"vitalícias de longos) e {f(soma(lo, 'inscritos_ganhos'), 0)} inscritos ganhos "
              f"({f(pct(soma(lo, 'inscritos_ganhos'), tot_i))}% dos inscritos vindos de longos). Os 5 maiores:", ""]
        L += [f"- `{r['video_id']}` {r.get('publicado', '')}: {r.get('titulo', '')[:80]} — {f(num(r.get('views')), 0)} views, "
              f"{f(num(r.get('inscritos_ganhos')), 0)} inscritos" for r in sorted(lo, key=lambda r: -(num(r.get('views')) or 0))[:5]]
        L.append("")
    spf = studio_por_formato(d)
    if spf:
        L += ["## 0c. Views ÷ views intencionais (engajadas), por formato", "",
              "Se o contador de views estiver inflado em relação às views intencionais, a razão sobe. Em Shorts, a "
              f"contagem mudou em {DATA_SHORTS_NOVA_CONTAGEM:%d/%m/%Y}. Os outliers (um vídeo com ≥ 40% das views do "
              "grupo) ficam de fora das linhas por período.", "", tabela_md(
                  ["formato", "grupo", "vídeos", "views", "intencionais", "views ÷ intenc. (soma)", "mediana por vídeo",
                   "insc./mil views", "insc./mil intenc.", "CTR (%)", "impressões"],
                  [[r["formato"], r["grupo"] + (f" — fora: {r['outliers']}" if r["outliers"] else ""), r["n"],
                    f(r["views"], 0), f(r["intencionais"], 0), f(r["razao"], 2), f(r["razao_mediana"], 2),
                    f(r["insc_mil"], 2), f(r["insc_mil_intenc"], 2), f(r["ctr"], 2), f(r["impressoes"], 0)] for r in spf]), ""]
    todos = list(d.v.values())
    L += ["## 1. Conversão por formato (inscritos ganhos por mil views)", "",
          tabela_md(["formato", "vídeos", "views", "% views", "mediana views", "insc./mil views",
                     "insc./mil engajadas", "% média assistida", "CTR mediano"],
                    [[r["grupo"], r["n"], f(r["views"], 0), f(r["pct_views"]), f(r["mediana_views"], 0),
                      f(r["insc_mil"], 2), f(r["engajadas_mil"], 2), f(r["pct_media"]), f(r["ctr"], 2)]
                     for r in por_grupo(todos, "formato")]
                    + [[f"{r['grupo']} sem outlier", r["n"], f(r["views"], 0), f(r["pct_views"]), f(r["mediana_views"], 0),
                        f(r["insc_mil"], 2), f(r["engajadas_mil"], 2), f(r["pct_media"]), f(r["ctr"], 2)]
                       for fmt in ("longo", "short")
                       for fora in [outliers([v for v in todos if v["formato"] == fmt])] if fora
                       for r in por_grupo([v for v in todos if v["formato"] == fmt and v not in fora], "formato")]), ""]
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
        L += [f"## 4. Top × fracos (quartil de cima × de baixo)", "", f"População: {CRITERIO_LISTA}.", ""]
        rotulos = [("n", "vídeos", 0), ("mediana_insc", "inscritos ganhos (mediana)", 0),
                   ("mediana_intenc", "views intencionais (mediana)", 0), ("mediana_views", "views (mediana)", 0),
                   ("insc_mil_intenc", "inscritos por mil views intencionais", 2), ("insc_mil", "inscritos por mil views", 2),
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
    lr = lista_retencao(d)
    if lr:
        L += ["### 4b. Lista para anotar a retenção aos 30 s (10 top e 10 fracos)", "", f"Critério: {CRITERIO_LISTA}.", "",
              tabela_md(["grupo", "vídeo", "título", "publicado", "inscritos", "views intenc.", "insc./mil intenc.", "Studio"],
                        [[r["grupo"], f"`{r['video_id']}`", r["titulo"][:60].replace("|", "/"), r["publicado"], r["inscritos"],
                          f(r["views_intencionais"], 0), f(r["insc_mil_intenc"], 1), f"[abrir]({r['studio']})"] for r in lr]), ""]
    curva = curva_mensal(d)
    if curva:
        L += ["## 5. Mês a mês", "", "Views e minutos: Analytics (canal). Views de longos e de Shorts: Studio (Total.csv). "
              "% de inscritos de Shorts marcada com * é estimativa do modelo (ver H5).", "", tabela_md(
            ["mês", "views", "views intenc.", "% intenc.", "minutos", "views longos", "views Shorts", "ganhos",
             "perdidos", "líquidos", "insc./mil views", "% inscritos de Shorts"],
            [[r["mes"], f(r["views"], 0), f((r["engajadas_pct"] or 0) * r["views"] / 100 if r["engajadas_pct"] else None, 0),
              f(r["engajadas_pct"]), f(r["minutos"], 0), f(r["views_longos"], 0), f(r["views_shorts_st"], 0),
              f(r["ganhos"], 0), f(r["perdidos"], 0), f(r["liquidos"], 0), f(r["insc_mil"], 2),
              f(r["pct_insc_shorts"]) + ("*" if r["est"] and r["pct_insc_shorts"] is not None else "")]
             for r in curva]), ""]
    om = origem_por_mes(d)
    if om:
        principais = [o for o, _ in Counter({o: p for m in om.values() for o, p in m.items()}).most_common()]
        foco = [o for o in ("RELATED_VIDEO", "BROWSE", "YT_SEARCH", "SUBSCRIBER", "SHORTS", "EXT_URL", "NO_LINK_OTHER")
                if o in principais]
        L += ["## 6. Origem do tráfego (% das views do mês, API)", "",
              "RELATED_VIDEO = vídeos sugeridos (\"Recomendados\"); BROWSE = Início/Inscrições.", "",
              tabela_md(["mês"] + foco, [[m] + [f(om[m].get(o)) for o in foco] for m in om]), ""]
    for base, nome in (("studio_origem_trafego_mensal", "todos"), ("studio_origem_trafego_mensal_longos", "longos"),
                       ("studio_origem_trafego_mensal_shorts", "shorts")):
        tab = (d.studio.get(base) or {}).get("tabela") or []
        if tab and "origem" in tab[0] and "mes" not in tab[0]:
            tot = sum(num(r.get("views")) or 0 for r in tab)
            L += [f"### 6b. Origem do tráfego, vitalício ({nome}, Studio)", "", tabela_md(
                ["origem", "views", "% views", "impressões", "CTR (%)", "horas"],
                [[r["origem"], f(num(r.get("views")), 0), f(pct(num(r.get("views")) or 0, tot)),
                  f(num(r.get("impressoes")), 0), f(num(r.get("ctr")), 2), f(num(r.get("horas")), 0)] for r in tab]), ""]
    for nome, sr in origens_studio(d).items():
        pc = pct_mes(sr)
        ms = list(pc)[-24:]
        cols = ["RELATED_VIDEO", "BROWSE", "YT_SEARCH", "SHORTS", "NOTIFICATION", "EXT_URL"]
        L += [f"### 6c. % das views por origem, mês a mês ({nome}, Studio, últimos 24 meses fechados)", "", tabela_md(
            ["mês", "views"] + [NOME_ORIGEM[c] for c in cols],
            [[m, f(pc[m]["_total"], 0)] + [f(pc[m].get(c, 0)) for c in cols] for m in ms]), ""]
    L += ["## 7. Hipóteses (a confirmar ou derrubar)", ""]
    for h in hipoteses(d):
        L += [f"### {h['id']}. {h['texto']} → **{h['veredito']}**", ""] + [f"- {n}" for n in h["numeros"]] + \
             [f"- Regra: {h['regra']}", ""]
    c = analise_comentarios(d)
    if c:
        L += ["## 8. O que o público pergunta", "",
              f"{c['total']} comentários; {c['perguntas']} perguntas ({f(c['pct_perguntas'])}% dos comentários de topo do "
              f"público); {f(c['pct_perguntas_respondidas'])}% das perguntas têm resposta do canal.", "",
              "Termos mais frequentes nas perguntas: " + ", ".join(f"{t} ({n})" for t, n in c["termos"]), "",
              "Perguntas mais curtidas:", ""]
        L += [f"- ({c_['likes']} likes, {c_['video_id']}) {sem_arroba(c_['texto'])[:200]}" for c_ in c["mais_curtidas"]]
        L.append("")
        ct = comentarios_por_tema(d)
        if ct:
            L += [f"### 8b. Todos os comentários do público por tema ({ct['total']} em {ct['videos']} vídeos; "
                  f"{ct['maior'][1]} deles, {f(pct(ct['maior'][1], ct['total']))}%, são do vídeo `{ct['maior'][0]}`)", "",
                  tabela_md(["tema", "comentários", "%", "perguntas", "exemplos (sem autor)"],
                            [[r["tema"], r["n"], f(r["pct"]), r["perguntas"],
                              " · ".join(f"“{e.replace('|', '/')}”" for e in r["exemplos"])] for r in ct["linhas"]]), ""]
    m = meta(d)
    if m:
        L += ["## 10. Conta da meta (200 mil inscritos até 31/12/2026)", "",
              f"- Inscritos hoje: {f(m['atual'], 0)} ({m['fonte']}).",
              f"- Faltam {f(m['faltam'], 0)} em {m['dias']} dias: {f(m['por_mes'], 0)} líquidos por mês "
              f"({f(m['por_dia'], 0)} por dia).",
              f"- Ritmo real: {f(m['ult'], 0)} líquidos no último mês fechado; média de {f(m['media6'], 0)} por mês nos "
              f"últimos 6 meses; melhor mês dos últimos {m['n_meses']}: {f(m['melhor'][1], 0)} ({m['melhor'][0]}).",
              f"- O necessário é {f(m['x_media6'], 0)}x a média dos últimos 6 meses e {f(m['x_melhor'], 1)}x o melhor mês.",
              f"- No ritmo dos últimos 6 meses, o canal chega a 31/12/2026 com cerca de {f(m['proj'], 0)} inscritos; "
              f"200 mil chegariam em {m['quando']}.", ""]
    if d.studio.get("ask_studio"):
        L += ["## 9. Anotações do Ask Studio (texto colado pelo Denis)", "", "> " +
              d.studio["ask_studio"][:4000].replace("\n", "\n> "), ""]
    return "\n".join(L)


META, DATA_META = 200_000, date(2026, 12, 31)


def meta(d):
    leia = d.pasta / "LEIAME_DADOS.md"
    m = re.search(r"inscritos no contador público: (\d+)", leia.read_text(encoding="utf-8")) if leia.exists() else None
    if not m or not d.mes:
        return None
    atual = int(m.group(1))
    ref = d.data_ref
    liq = [(r["mes"], (num(r["inscritos_ganhos"]) or 0) - (num(r["inscritos_perdidos"]) or 0)) for r in d.mes]
    dias = (DATA_META - ref).days
    faltam = META - atual
    media6 = statistics.mean(x for _, x in liq[-6:])
    melhor = max(liq, key=lambda x: x[1])
    por_mes = faltam / (dias / 30.4)
    meses_ate = faltam / media6 if media6 > 0 else None
    quando = (f"{(ref + timedelta(days=30.4 * meses_ate)):%m/%Y} (daqui a ~{meses_ate / 12:.0f} anos)"
              if meses_ate else "nunca, no ritmo atual")
    return {"atual": atual, "fonte": "contador público arredondado do YouTube, LEIAME_DADOS.md", "faltam": faltam,
            "dias": dias, "por_mes": por_mes, "por_dia": faltam / dias, "ult": liq[-1][1], "media6": media6,
            "melhor": melhor, "n_meses": len(liq), "x_media6": por_mes / media6 if media6 else None,
            "x_melhor": por_mes / melhor[1] if melhor[1] else None, "proj": atual + media6 * dias / 30.4,
            "quando": quando}


CRITERIO_LISTA = (f"longos publicados nos últimos {POPULACAO_DIAS} dias, com ≥ {POPULACAO_MIN_VIDA} dias de vida e "
                  f"≥ {POPULACAO_MIN_INTENC} views intencionais; ordem por inscritos ganhos (empate: views intencionais)")


def lista_retencao(d, n=10):
    top, fr = top_fracos(d, n)
    return [{"grupo": g, "video_id": v["id"], "titulo": v["titulo"], "publicado": v["publicado"],
             "inscritos": int(ganhos(v)), "views_intencionais": int(v["engajadas"] or 0),
             "insc_mil_intenc": round(por_mil(ganhos(v), v["engajadas"] or 0) or 0, 2),
             "views": int(v["views"] or 0), "pct_30s": "",
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
    gravar(args.saida / "lista_retencao_30s.csv", ["grupo", "video_id", "titulo", "publicado", "inscritos",
                                                   "views_intencionais", "insc_mil_intenc", "views", "pct_30s", "studio"], lr)
    if args.lista_retencao:
        print(f"Critério: {CRITERIO_LISTA}.")
        for r in lr:
            print(f"{r['grupo']:5} {r['video_id']}  {r['inscritos']:>5} insc.  {r['views_intencionais']:>7} intenc.  "
                  f"{r['titulo'][:60]}")
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
