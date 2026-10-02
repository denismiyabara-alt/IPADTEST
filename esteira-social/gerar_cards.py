#!/usr/bin/env python3
"""Esteira social: gera um card 🎬 por vídeo do calendário, no contrato do juiz-post (agentes/juiz-post.md).

Lê pautas-canal/CALENDARIO-8-SEMANAS.csv, junta com o texto de conteudo.py e grava:

    cards/<data do vídeo>-<slug>.md   card 🎬: carrossel do Instagram (capa = thumbnail do YouTube + slides),
                                      legenda, posts do X (A, B, C...), PNGs esperados, fontes e publicação
    cards/INDICE.csv                  a fila do juiz-post: uma linha por card, com gate e autoexame
    cards/GATE-RELATORIO.md           bloqueados e avisos do gate de qualidade
    cards/AUTOEXAME.md                cada critério do juiz-post e do leitor-frio que dá para medir no texto,
                                      mais o risco de pauta/voz que só o juiz decide

Todo card sai com status "rascunho". Nada é publicado: juiz-post -> leitor-frio -> Denis.

Só biblioteca padrão. O gate (investir-e-cocar/pipeline/gate_qualidade.py) é importado se existir.

uso:
  python3 gerar_cards.py                 # gera tudo e roda o gate
  python3 gerar_cards.py --sem-gate
  python3 gerar_cards.py --checar        # só o autoexame; sai com 1 se algum card falhar
  python3 gerar_cards.py --gate CAMINHO/gate_qualidade.py --calendario OUTRO.csv --saida OUTRA_PASTA
"""
import argparse
import csv
import importlib.util
import json
import os
import re
import sys
import unicodedata
from datetime import date, timedelta
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import conteudo  # noqa: E402

PAUTAS = AQUI.parent / "pautas-canal"
CALENDARIO = PAUTAS / "CALENDARIO-8-SEMANAS.csv"
GATE_PADRAO = [
    Path(os.environ["IC_GATE"]) if os.environ.get("IC_GATE") else None,
    Path("/home/user/investir-e-cocar/pipeline/gate_qualidade.py"),
    Path("/home/user/investir-e-cocar/gate_qualidade.py"),
    Path.home() / "investir-e-cocar" / "pipeline" / "gate_qualidade.py",
]
RENDER = "esteira-social/render"   # onde o renderizador do Mac deve gravar os PNGs (ainda não existe aqui)

CANAL = "Investir e Coçar"
LIMITE_X = 280
LETRAS = "ABCDE"

# ---------------------------------------------------------------- hashtags por tema do vídeo
HASHTAGS_GERAL = ["#InvestirECocar", "#EducacaoFinanceira"]
HASHTAGS_TEMA = {
    "Tesouro": ["#TesouroDireto", "#TesouroIPCA", "#TesouroSelic", "#TitulosPublicos", "#RendaFixa"],
    "renda fixa bancária": ["#CDB", "#LCI", "#LCA", "#FGC", "#RendaFixa"],
    "FII": ["#FII", "#FundosImobiliarios", "#IFIX", "#RendaMensal"],
    "ações e dividendos": ["#Dividendos", "#Acoes", "#DividendosMensais", "#RendaMensal"],
    "ETF": ["#ETF", "#ETFs", "#TaxaDeAdministracao", "#DividendosMensais", "#RendaMensal"],
    "IR": ["#ImpostoDeRenda", "#IR", "#Tributacao", "#JCP"],
    "juros": ["#Copom", "#Selic", "#Juros"],
    "crise": ["#Crise", "#CriseFinanceira", "#Recessao", "#MercadoFinanceiro"],
    "IA": ["#BolhaDaIA", "#InteligenciaArtificial", "#Tecnologia", "#MercadoFinanceiro"],
    "cripto": ["#Bitcoin", "#Cripto", "#Criptomoedas", "#BTC"],
    "juntar dinheiro": ["#JurosCompostos", "#PrimeiroMilhao", "#Aposentadoria", "#LongoPrazo"],
    "comportamento": ["#FinancasDoCasal", "#Planejamento", "#Objetivos", "#FinancasPessoais"],
}
MAX_HASHTAGS = 10


def hashtags_do_video(temas):
    tags = list(HASHTAGS_GERAL)
    for t in temas:
        for h in HASHTAGS_TEMA[t]:
            if h not in tags and len(tags) < MAX_HASHTAGS:
                tags.append(h)
    return tags


ESTRUTURAS = {
    "A": "O Choque → A Causa Escondida",
    "B": "O Personagem → O Twist",
    "C": "O Antes / Depois",
    "D": "A Pergunta Que Ninguém Faz",
    "E": "A Linha do Tempo Invertida",
}

# ---------------------------------------------------------------- regras do juiz-post e do leitor-frio
RE_CHECAR = re.compile(r"\[CHECAR:[^\]]*\]")
RE_NUM = re.compile(r"(?<![\w])\d+(?:[.,]\d+)*")
# eliminatório do juiz-post: afirmação absoluta ("só", "nunca", "todo", "ninguém", "sempre")
RE_ABSOLUTO = re.compile(r"(?<![\wÀ-ú])(só|somente|apenas|nunca|jamais|todo|toda|todos|todas|tudo|ninguém|sempre|"
                         r"nenhum|nenhuma)(?![\wÀ-ú])", re.I)
# eliminatório: CTA e link
RE_CTA = re.compile(r"https?://|www\.|\blink\b|\bbio\b|\bsiga\b|\bsegue a gente|\bcomenta(?:e|r)?\b|\bsalv[ae]\b|"
                    r"compartilh|inscrev|\bclique\b|ative o sininho|@\w", re.I)
PROIBIDAS = [
    "ecossistema", "jornada", "protagonista", "navegar", "empoderar", "disruptiv", "mindset", "ressignificar",
    "curadoria", "potencializar", "otimizar", "entregar valor", "construir pontes", "visão holística", "sinergia",
    "você sabia", "já pensou se", "sua melhor versão", "você merece", "plot twist", "fala, tanaka", "taná ",
    "vale a pena", "melhor ação", "melhores ações", "qual a melhor", "qual é a melhor", "quais as melhores",
    "hora de comprar", "hora de vender", "recomendo", "carteira recomendada", "compre já", "compre agora",
    "não é recomendação", "conteúdo educativo", "segundo a ", "segundo o ", "de acordo com", "levantamento",
    "✅", "🚀", "💡",
]
RE_FONTE = re.compile(r"(^|\n)\s*fontes?:", re.I)
CORRETORAS = re.compile(r"\b(XP|Rico|Clear|BTG|Nu ?Invest|Easynvest|Inter|Toro|Modal|Genial|Órama|Warren|Avenue|Nomad|"
                        r"C6|Itaú|Bradesco|Santander|Safra|Ágora|Mirae|Guide|Ativa|Necton|Terra)\b")
# leitor-frio: o leitor leigo não conhece estes termos; cada slide ou post que usar um deles explica ali mesmo,
# entre parênteses logo depois (ou com "Tradução:").
JARGAO = {
    "LCI": r"\bLCI\b", "LCA": r"\bLCA\b", "IOF": r"\bIOF\b", "FII": r"\bFIIs?\b", "ETF": r"\bETFs?\b",
    "JCP": r"\bJCP\b", "IPCA": r"\bIPCA\+?", "CDI": r"\bCDI\b", "Selic": r"\bSelic\b", "Copom": r"\bCopom\b",
    "FGC": r"\bFGC\b", "RendA+": r"RendA\+", "TRXF11": r"\bTRXF11\b", "IR": r"\bIR\b", "IA": r"\bIA\b",
    "marcação a mercado": r"marcação a mercado", "isenção": r"\bisen[çt]", "alíquota": r"al[íi]quota",
    "liquidez": r"\bliquidez\b", "carência": r"\bcar[êe]ncia\b", "prefixado": r"\bprefixado\b",
    "pós-fixado": r"\bpós-fixado\b", "taxa de administração": r"taxa de administração", "cotista": r"\bcotistas?\b",
    "alavancagem": r"\balavancagem\b", "vacância": r"\bvacância\b", "opções de compra": r"opções de compra",
    "data com": r"\bdata com\b", "juros semestrais": r"juros semestrais", "juro real": r"juro real",
    "tabela progressiva/regressiva": r"\b(progressiva|regressiva)\b",
}
RE_RANKING = re.compile(
    r"top ?\d+|campe[ãa]|recorde|l[ií]der\w*|\d+º|mais buscad\w*|mais trouxe\w*|mais vist\w*|"
    r"\b(?:o|a|os|as) (?:melhor|pior)(?:es)?\b|\bmelhor(?:es)? d[oa]\b|\bpior(?:es)? d[oa]\b|"
    r"\b(?:o|a|os|as) maior(?:es)? (?:\w+ )?d[oa]s? (?:canal|ano|brasil|mercado|bolsa|hist[oó]ria)\b|"
    r"\b(?:primeiro|segundo|terceiro) (?:que|mais|melhor|lugar)\b|\bnº", re.I)


# ---------------------------------------------------------------- utilidades
def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def slugify(titulo, maximo=50):
    s = re.sub(r"[^a-z0-9]+", "-", sem_acento(titulo).lower()).strip("-")
    return s if len(s) <= maximo else s[:maximo].rsplit("-", 1)[0]


def ddmm(iso):
    return f"{iso[8:10]}/{iso[5:7]}"


def canon(num):
    return re.sub(r"\D", "", num)


def numeros_do_texto(texto):
    return [m.group(0) for m in RE_NUM.finditer(RE_CHECAR.sub(" ", texto))]


def n_numeros(texto):
    return len({canon(n) for n in numeros_do_texto(texto)})


def frases(texto):
    t = RE_CHECAR.sub("X", texto)
    return [f.strip() for f in re.split(r"(?<=[.!?:])\s+|\n+", t) if f.strip()]


def jargao_sem_explicacao(texto):
    t = RE_CHECAR.sub(" ", texto)
    faltam = []
    for nome, rx in JARGAO.items():
        ocorr = list(re.finditer(rx, t))
        if not ocorr:
            continue
        explicado = "Tradução:" in t or any("(" in t[m.end():m.end() + 30] for m in ocorr)
        if not explicado:
            faltam.append(nome)
    return faltam


def ler_calendario(caminho=CALENDARIO):
    with open(caminho, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def agenda(row, extra):
    """{rede: (data, horário, relativo)}. Longo sai às 19h; Short no horário do canal."""
    d = date.fromisoformat(row["data"])
    if extra.get("evento_ao_vivo") and row["formato"] == "short":
        rel = "D+0, de manhã, ANTES da decisão do Copom (evento ao vivo)"
        return {"x": (d.isoformat(), "09:00", rel), "instagram": (d.isoformat(), "10:00", rel)}
    if row["formato"] == "longo":
        return {"x": (d.isoformat(), "19:30", "D+0, 30 min depois do vídeo (19h)"),
                "instagram": ((d + timedelta(days=1)).isoformat(), "12:00", "D+1, almoço do dia seguinte ao vídeo")}
    return {"x": (d.isoformat(), "12:00", "D+0, no dia do Short"),
            "instagram": (d.isoformat(), "18:00", "D+0, no dia do Short")}


def prova_slide2(row):
    f = row["fontes_a_conferir"].strip()
    if not f or f == "—":
        return "sem imagem (slide só de texto)"
    return f"print legível e do dia da publicação de fonte oficial: {f} (nada de foto de banco ou imagem de IA)"


# ---------------------------------------------------------------- cards
def montar_cards(rows=None):
    rows = rows if rows is not None else ler_calendario()
    faltando = [r["data"] for r in rows if r["data"] not in conteudo.C]
    if faltando:
        raise SystemExit(f"Sem texto em conteudo.py para: {', '.join(faltando)} (não gero template vazio)")
    cards = []
    for row in rows:
        c = conteudo.C[row["data"]]
        if c["titulo"] != row["titulo"]:
            raise SystemExit(f'{row["data"]}: título do calendário mudou ("{row["titulo"]}" x "{c["titulo"]}")')
        slug = slugify(row["titulo"])
        cid = f"{row['data']}-{slug}"
        slides = [c["capa"]] + c["slides"]
        posts = c["posts"]
        ag = agenda(row, c)
        card = {
            "id": cid, "arquivo": f"{cid}.md", "tipo": "🎬 vídeo do canal", "status": "rascunho",
            "video_data": row["data"], "video_formato": row["formato"], "video_titulo": row["titulo"],
            "assunto": row["assunto"], "termo_busca": row["termo_busca"] or "—", "angulo": row["angulo"],
            "fontes_a_conferir": row["fontes_a_conferir"], "temas": conteudo.TEMAS_VIDEO[row["data"]],
            "estrutura": c["estrutura"], "mecanica": c["mecanica"], "mensagem_capa": c["mensagem_capa"],
            "slides": [{"numero": i + 1, "texto": s,
                        "imagem": ("thumbnail do vídeo no YouTube (regra do card 🎬)" if i == 0
                                   else prova_slide2(row) if i == 1 else "sem imagem (slide só de texto)"),
                        "png": f"{RENDER}/{cid}/slide-{i + 1}.png"} for i, s in enumerate(slides)],
            "legenda": c["legenda"], "hashtags": " ".join(hashtags_do_video(conteudo.TEMAS_VIDEO[row["data"]])),
            "posts": [{"letra": LETRAS[i], "texto": t,
                       "imagem": "thumbnail do vídeo no YouTube" if i == 0 else "só texto",
                       "png": f"{RENDER}/{cid}/post-A.png" if i == 0 else ""} for i, t in enumerate(posts)],
            "numeros": c.get("numeros", []), "afirmacoes": conteudo.AFIRMACOES.get(row["data"], []),
            "evento_ao_vivo": c.get("evento_ao_vivo", ""), "corte_de": c.get("corte_de", ""),
            "risco": {"nivel": c["risco"][0], "nota": c["risco"][1]},
            "publicacao": {rede: {"data": d, "horario": h, "relativa_ao_video": r} for rede, (d, h, r) in ag.items()},
            "_row": row,
        }
        card["texto_gate"] = "\n\n".join(slides + [c["legenda"]] + posts)
        cards.append(card)
    return cards


def pendencias(card):
    return sorted(set(RE_CHECAR.findall(card["texto_gate"])))


# ---------------------------------------------------------------- checagens de fonte
def checar_numeros(card, row, pautas=PAUTAS):
    probs = []
    permitidos = {canon(n) for n in numeros_do_texto(" ".join(row.values()))}
    cache = {}
    for n in card["numeros"]:
        v = canon(n["valor"])
        if n["fonte"] == "cálculo":
            r = eval(n["conta"], {"__builtins__": {}}, {})  # só aritmética escrita em conteudo.py
            alvo = float(n["valor"].replace(".", "").replace(",", "."))
            casas = len(n["valor"].split(",")[1]) if "," in n["valor"] else 0
            if abs(r - alvo) > 0.5 * 10 ** -casas + 1e-9:
                probs.append(f'conta de {n["valor"]} dá {r:.4f} ({n["conta"]})')
                continue
        else:
            if n["fonte"] not in cache:
                cache[n["fonte"]] = (pautas / n["fonte"]).read_text(encoding="utf-8")
            if n["trecho"] not in cache[n["fonte"]]:
                probs.append(f'trecho não está em {n["fonte"]}: "{n["trecho"]}"')
                continue
            if v not in {canon(x) for x in numeros_do_texto(n["trecho"])}:
                probs.append(f'{n["valor"]} não aparece no trecho de {n["fonte"]}')
                continue
        permitidos.add(v)
    for num in numeros_do_texto(card["texto_gate"]):
        if canon(num) not in permitidos:
            probs.append(f'número sem origem no calendário/TEMAS/TERMOS: "{num}"')
    return probs


def checar_afirmacoes(card, raiz=AQUI.parent):
    probs, texto = [], card["texto_gate"]
    for a in card["afirmacoes"]:
        if a["trecho"] not in (raiz / a["arquivo"]).read_text(encoding="utf-8"):
            probs.append(f'trecho não está em {a["arquivo"]}: "{a["trecho"]}"')
    cobertos = [a["texto"] for a in card["afirmacoes"] if a["texto"] in texto]
    for m in RE_RANKING.finditer(texto):
        ini = texto.rfind("\n", 0, m.start()) + 1
        fim = texto.find("\n", m.end())
        linha = texto[ini:fim if fim >= 0 else None]
        if not any(c in linha for c in cobertos):
            probs.append(f'afirmação de ranking sem fonte literal: "{linha.strip()}"')
    return probs


# ---------------------------------------------------------------- autoexame (critérios do juiz-post e do leitor-frio)
def autoexame(card):
    """Lista de (critério, problema). Vazia = nenhum critério mensurável no texto reprova o card.
    Pauta (item 1), voz/piada (item 2) e imagem (item 4) são do juiz; o risco deles está em card['risco']."""
    P = []
    pecas = ([(f'slide {s["numero"]}', s["texto"]) for s in card["slides"]] + [("legenda", card["legenda"])]
             + [(f'post {p["letra"]}', p["texto"]) for p in card["posts"]])
    texto = card["texto_gate"]
    sem_checar = RE_CHECAR.sub(" ", texto)
    # eliminatórios do juiz-post
    for onde, t in pecas:
        for m in RE_ABSOLUTO.finditer(RE_CHECAR.sub(" ", t)):
            P.append(("eliminatório: afirmação absoluta", f'{onde}: "{m.group(0)}"'))
        m = RE_CTA.search(RE_CHECAR.sub(" ", t))
        if m:
            P.append(("eliminatório: CTA ou link", f'{onde}: "{m.group(0)}"'))
    baixo = sem_checar.lower()
    for w in PROIBIDAS:
        if w in baixo:
            P.append(("eliminatório: palavra proibida ou recomendação", w))
    if RE_FONTE.search(sem_checar):
        P.append(("regra do canal: fonte no corpo", "Fonte:"))
    m = CORRETORAS.search(sem_checar)
    if m:
        P.append(("regra do canal: corretora", m.group(0)))
    for p in checar_numeros(card, card["_row"]) + checar_afirmacoes(card):
        P.append(("eliminatório: número ou afirmação sem fonte", p))
    # capa (juiz: entende em 1 segundo e diz UMA coisa; leitor-frio: 1 ideia, até 1 número, zero trava)
    capa = card["slides"][0]["texto"]
    if n_numeros(capa) > 1:
        P.append(("capa: mais de 1 número", capa))
    if jargao_sem_explicacao(capa) or any(re.search(rx, capa) for rx in JARGAO.values()):
        P.append(("capa: palavra técnica", capa))
    if len(capa.split()) > 10 or len(frases(capa)) > 2:
        P.append(("capa: longa demais pra 1 segundo", capa))
    # leitor-frio nos slides: até 3 números, frase de até 25 palavras, jargão explicado no próprio slide
    for s in card["slides"][1:]:
        if n_numeros(s["texto"]) > 3:
            P.append(("leitor-frio: mais de 3 números no slide", f'slide {s["numero"]}'))
        for j in jargao_sem_explicacao(s["texto"]):
            P.append(("leitor-frio: jargão sem explicação", f'slide {s["numero"]}: {j}'))
        for f in frases(s["texto"]):
            if len(f.split()) > 25:
                P.append(("leitor-frio: frase com mais de 25 palavras", f'slide {s["numero"]}: {f}'))
        if len(s["texto"]) > 140:
            P.append(("PNG: texto pode estourar o slide", f'slide {s["numero"]} ({len(s["texto"])} caracteres)'))
    # posts do X: cada um funciona sozinho no feed
    if not 3 <= len(card["posts"]) <= 5:
        P.append(("X: precisa de 3 a 5 posts", str(len(card["posts"]))))
    for p in card["posts"]:
        t = p["texto"]
        if len(t) > LIMITE_X:
            P.append(("X: mais de 280 caracteres", f'post {p["letra"]} ({len(t)})'))
        if re.search(r"#\w|[\U0001F300-\U0001FAFF☀-➿]", t):
            P.append(("X: hashtag ou emoji no post", f'post {p["letra"]}'))
        lim = 1 if p["letra"] == "A" else 4
        if n_numeros(t) > lim:
            P.append(("X: números demais num post", f'post {p["letra"]} ({n_numeros(t)} números, máximo {lim})'))
        for j in jargao_sem_explicacao(t):
            P.append(("X: jargão sem explicação (post lido sozinho)", f'post {p["letra"]}: {j}'))
        for f in frases(t):
            if len(f.split()) > 25:
                P.append(("X: frase com mais de 25 palavras", f'post {p["letra"]}: {f}'))
    a = card["posts"][0]["texto"]
    if not a.startswith("Tanaka, ") or len(a.split("\n")[0].split()) > 8:
        P.append(("voz: post A abre com \"Tanaka,\" e até 8 palavras na 1ª linha", a.split("\n")[0]))
    if not card["legenda"].startswith("Tanaka, "):
        P.append(("voz: legenda abre com \"Tanaka,\"", card["legenda"][:40]))
    if not 200 <= len(card["legenda"]) <= 500:
        P.append(("legenda: fora de 200-500 caracteres", str(len(card["legenda"]))))
    n_sl = len(card["slides"])
    if not (n_sl == 5 if card["video_formato"] == "longo" else 4 <= n_sl <= 5):
        P.append(("carrossel: número de slides", str(n_sl)))
    return P


# ---------------------------------------------------------------- render
def _bloco(texto):
    return "\n".join("> " + l if l else ">" for l in texto.split("\n"))


def _json(card):
    d = {k: card[k] for k in ("id", "tipo", "status", "temas", "estrutura", "mecanica", "mensagem_capa", "slides",
                              "legenda", "hashtags", "numeros", "afirmacoes", "publicacao", "risco")}
    d["topico"] = card["video_titulo"]
    d["video"] = {"data": card["video_data"], "formato": card["video_formato"], "titulo": card["video_titulo"],
                  "assunto": card["assunto"], "termo_busca": card["termo_busca"]}
    d["instagram_caption"] = card["legenda"]
    # chave "tweets": é por ela que o pipeline reconhece um card de thread válido (ic-copywriter)
    d["tweets"] = [{"numero": i + 1, "letra": p["letra"], "texto": p["texto"], "imagem": p["imagem"]}
                   for i, p in enumerate(card["posts"])]
    d["pendencias"] = pendencias(card)
    d["leitor_frio"] = {"pngs": [s["png"] for s in card["slides"]], "legenda": card["legenda"],
                        "mensagem_pretendida_da_capa": card["mensagem_capa"]}
    return json.dumps(d, ensure_ascii=False, indent=2)


def render(card):
    pub = card["publicacao"]
    fm = [("id", card["id"]), ("tipo", card["tipo"]), ("status", card["status"]), ("juiz", "juiz-post"),
          ("depois", "leitor-frio"), ("video_data", card["video_data"]), ("video_formato", card["video_formato"]),
          ("video_titulo", card["video_titulo"]), ("assunto", card["assunto"]), ("temas", card["temas"]),
          ("termo_busca", card["termo_busca"]), ("mensagem_capa", card["mensagem_capa"]),
          ("estrutura", f'{card["estrutura"]} ({ESTRUTURAS[card["estrutura"]]})'), ("mecanica", card["mecanica"]),
          ("instagram_data", pub["instagram"]["data"]), ("instagram_horario", pub["instagram"]["horario"]),
          ("x_data", pub["x"]["data"]), ("x_horario", pub["x"]["horario"]),
          ("pendencias_checar", len(pendencias(card))), ("pngs", "pendente (renderizar antes do juiz-post)")]
    L = ["---"] + [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in fm] + ["---", ""]
    L += [f'# 🎬 {card["video_titulo"]} ({ddmm(card["video_data"])})',
          "**Status:** rascunho para o juiz-post. Depois do APROVADO, vai pro leitor-frio. Não publicar sem o Denis.",
          "", "## PARA O JUIZ-POST", "",
          f'### CARROSSEL DO INSTAGRAM ({len(card["slides"])} slides)', ""]
    for s in card["slides"]:
        rot = " (capa)" if s["numero"] == 1 else ""
        L += [f'#### Slide {s["numero"]}{rot}', f'- imagem: {s["imagem"]}', f'- png: `{s["png"]}`', _bloco(s["texto"]), ""]
    L += [f'### LEGENDA ({len(card["legenda"])} caracteres)', _bloco(card["legenda"]), "",
          "### HASHTAGS (no fim da legenda)", card["hashtags"], "",
          f'### POSTS DO X ({len(card["posts"])})', ""]
    for p in card["posts"]:
        L += [f'#### Post {p["letra"]} ({len(p["texto"])}/{LIMITE_X})', f'- imagem: {p["imagem"]}'
              + (f' · png: `{p["png"]}`' if p["png"] else ""), _bloco(p["texto"]), ""]
    L += ["## PARA O LEITOR-FRIO (depois do APROVADO do juiz)",
          "Recebe só os PNGs dos slides, em ordem, e a legenda. Quem chama compara \"a capa quer me dizer\" com:",
          f'- **mensagem pretendida da capa:** {card["mensagem_capa"]}',
          "- PNGs: " + ", ".join(f'`{s["png"]}`' for s in card["slides"]), ""]
    L += ["## FONTES E NÚMEROS (para conferir; não vão no post)",
          f'- Calendário ({ddmm(card["video_data"])}): fontes a conferir: {card["fontes_a_conferir"]}. '
          f'Ângulo: {card["angulo"]}',
          "- Números da própria linha do calendário: liberados (a linha é o briefing)."]
    for n in card["numeros"]:
        if n["fonte"] == "cálculo":
            L.append(f'- {n["valor"]}: cálculo `{n["conta"]}` a partir de {n["entradas"]}')
        else:
            L.append(f'- {n["valor"]}: pautas-canal/{n["fonte"]}: "{n["trecho"]}"')
    for a in card["afirmacoes"]:
        L.append(f'- "{a["texto"]}": {a["arquivo"]}: "{a["trecho"]}"')
    L += ["", "## PENDÊNCIAS"]
    pend = pendencias(card)
    L += [f"- {x} (o Denis preenche na publicação; decisão do Mac: não elimina o card)" for x in pend] or []
    if not pend:
        L.append("- nenhuma de texto")
    L.append("- PNGs dos slides e do post A: renderizar antes do juiz-post")
    if card["evento_ao_vivo"]:
        L.append(f'- Evento ao vivo: {card["evento_ao_vivo"]}')
    L += ["", "## PUBLICAÇÃO (fora do julgamento; não é texto do post)",
          f'- Instagram: {ddmm(pub["instagram"]["data"])} às {pub["instagram"]["horario"]} ({pub["instagram"]["relativa_ao_video"]})',
          f'- X: {ddmm(pub["x"]["data"])} às {pub["x"]["horario"]} ({pub["x"]["relativa_ao_video"]})',
          f"- Link do vídeo: nenhum no texto (o juiz-post elimina CTA e link). O link fica na bio do Instagram e no "
          f"canal {CANAL}; no X, se o Denis quiser, numa resposta publicada à parte, depois da aprovação."]
    if card["corte_de"]:
        L.append(f'- Este Short é um corte do longo de {ddmm(card["corte_de"])}.')
    L += [f'- Risco no juiz-post (autoexame): {card["risco"]["nivel"]}. {card["risco"]["nota"]}',
          "", "---JSON---", _json(card), "---FIM---", ""]
    return "\n".join(L)


# ---------------------------------------------------------------- gate
def carregar_gate(caminho=None):
    for c in ([Path(caminho)] if caminho else [g for g in GATE_PADRAO if g]):
        if c.exists():
            spec = importlib.util.spec_from_file_location("gate_qualidade", c)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    return None


def rodar_gate(gate, card):
    """Título do vídeo + texto inteiro do card (slides, legenda e posts), sem hashtags, na data do Instagram."""
    post = gate.Post(card["video_titulo"], card["texto_gate"], "md", card["publicacao"]["instagram"]["data"])
    return gate.avaliar(post)


# ---------------------------------------------------------------- saída
def gravar(cards, saida, gate=None):
    saida.mkdir(parents=True, exist_ok=True)
    for f in saida.glob("*.md"):
        if f.name not in ("GATE-RELATORIO.md", "AUTOEXAME.md"):
            f.unlink()
    res = {}
    for c in cards:
        (saida / c["arquivo"]).write_text(render(c), encoding="utf-8")
        if gate:
            res[c["id"]] = rodar_gate(gate, c)
    cols = ["arquivo", "id", "tipo", "status", "video_data", "video_formato", "video_titulo", "temas",
            "instagram_data", "instagram_horario", "x_data", "x_horario", "mensagem_capa", "n_slides", "n_posts",
            "max_chars_post", "estrutura", "mecanica", "pendencias_checar", "autoexame", "risco_juiz",
            "gate_resultado", "gate_bloqueantes", "gate_avisos", "gate_codigos", "juiz_post", "leitor_frio"]
    with open(saida / "INDICE.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for c in cards:
            r = res.get(c["id"])
            w.writerow({
                "arquivo": c["arquivo"], "id": c["id"], "tipo": c["tipo"], "status": c["status"],
                "video_data": c["video_data"], "video_formato": c["video_formato"], "video_titulo": c["video_titulo"],
                "temas": "; ".join(c["temas"]),
                "instagram_data": c["publicacao"]["instagram"]["data"], "instagram_horario": c["publicacao"]["instagram"]["horario"],
                "x_data": c["publicacao"]["x"]["data"], "x_horario": c["publicacao"]["x"]["horario"],
                "mensagem_capa": c["mensagem_capa"], "n_slides": len(c["slides"]), "n_posts": len(c["posts"]),
                "max_chars_post": max(len(p["texto"]) for p in c["posts"]),
                "estrutura": c["estrutura"], "mecanica": c["mecanica"], "pendencias_checar": len(pendencias(c)),
                "autoexame": "OK" if not autoexame(c) else f"{len(autoexame(c))} problema(s)",
                "risco_juiz": c["risco"]["nivel"],
                "gate_resultado": r["resultado"] if r else "não rodou",
                "gate_bloqueantes": r["bloqueantes"] if r else "", "gate_avisos": r["avisos"] if r else "",
                "gate_codigos": ";".join(sorted({p["codigo"] for p in r["problemas"]})) if r else "",
                "juiz_post": "pendente", "leitor_frio": "pendente",
            })
    if gate:
        (saida / "GATE-RELATORIO.md").write_text(relatorio_gate(cards, res), encoding="utf-8")
    (saida / "AUTOEXAME.md").write_text(relatorio_autoexame(cards), encoding="utf-8")
    return res


def relatorio_gate(cards, res):
    bloq = [c for c in cards if res[c["id"]]["codigo_saida"] == 2]
    avis = [c for c in cards if res[c["id"]]["codigo_saida"] == 1]
    L = ["# Gate de qualidade nos cards da esteira social", "",
         "Gerado por `gerar_cards.py` com `investir-e-cocar/pipeline/gate_qualidade.py` (importado, sem alteração).",
         "Entrada: título do vídeo + slides, legenda e posts do card, sem hashtags, na data do Instagram.", "",
         f"- Cards: {len(cards)}", f"- OK: {len(cards) - len(bloq) - len(avis)}", f"- Só avisos: {len(avis)}",
         f"- Bloqueados: {len(bloq)}", "", "## Bloqueados", ""]
    L += [f'- `{c["arquivo"]}`: ' + "; ".join(f'{p["codigo"]} ({p["mensagem"]})' for p in res[c["id"]]["problemas"]
                                               if p["nivel"] == "BLOQUEANTE") for c in bloq] or ["- nenhum"]
    L += ["", "## Avisos", ""]
    for c in avis:
        for p in res[c["id"]]["problemas"]:
            L.append(f'- `{c["arquivo"]}`: {p["codigo"]}: {p["mensagem"]}' + (f' (trecho: "{p["trecho"]}")' if p.get("trecho") else ""))
    if not avis:
        L.append("- nenhum")
    return "\n".join(L) + "\n"


def relatorio_autoexame(cards):
    niveis = {"baixo": [], "médio": [], "alto": []}
    for c in cards:
        niveis[c["risco"]["nivel"]].append(c)
    falhas = [(c, autoexame(c)) for c in cards if autoexame(c)]
    L = ["# Autoexame dos cards contra o juiz-post e o leitor-frio", "",
         "Gerado por `gerar_cards.py`. Duas partes:", "",
         "1. **O que dá para medir no texto** (eliminatórios e travas mecânicas). Isso inclui afirmação absoluta, CTA "
         "ou link, palavra proibida, número ou ranking sem fonte e capa com mais de 1 número ou com palavra técnica. "
         "Também confere jargão sem explicação, mais de 3 números por slide, frase com mais de 25 palavras e post A "
         "com \"Tanaka,\". Os testes exigem zero problemas.",
         "2. **O que só o juiz decide:** pauta (item 1), voz e piada (item 2) e a imagem real (item 4). O risco vem "
         "abaixo, por card.", "",
         f"## Parte 1: problemas mensuráveis: {sum(len(p) for _, p in falhas)} em {len(falhas)} card(s)", ""]
    for c, ps in falhas:
        for crit, det in ps:
            L.append(f'- `{c["arquivo"]}`: {crit}: {det}')
    if not falhas:
        L.append("- nenhum")
    L += ["", "## Parte 2: risco no juiz-post (estimativa)", "",
          f'- **baixo** ({len(niveis["baixo"])}): pauta com bolso ou nome conhecido; deve passar se o PNG da '
          "thumbnail for legível.",
          f'- **médio** ({len(niveis["médio"])}): pauta ok, mas o carrossel mais explica que reage (item 2 vale no '
          "máximo 1), ou há uma regra que o juiz vai querer inteira.",
          f'- **alto** ({len(niveis["alto"])}): pauta que o juiz lista como eliminatória (finança pessoal básica) ou '
          "tema gringo sem ponte. O texto não salva: \"PAUTA MORTA, descartar\".", ""]
    for nivel in ("alto", "médio", "baixo"):
        L += [f"### {nivel}", ""]
        L += [f'- {ddmm(c["video_data"])} {c["video_titulo"]}: {c["risco"]["nota"]}' for c in niveis[nivel]]
        L.append("")
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Gera os cards 🎬 (Instagram + X) a partir do calendário")
    ap.add_argument("--calendario", default=str(CALENDARIO))
    ap.add_argument("--saida", default=str(AQUI / "cards"))
    ap.add_argument("--gate")
    ap.add_argument("--sem-gate", action="store_true")
    ap.add_argument("--checar", action="store_true", help="só o autoexame")
    a = ap.parse_args(argv)
    cards = montar_cards(ler_calendario(a.calendario))
    erros = [f'{c["arquivo"]}: {crit}: {det}' for c in cards for crit, det in autoexame(c)]
    if erros:
        print("\n".join(erros))
        return 1
    if a.checar:
        print(f"OK: {len(cards)} cards passam no autoexame")
        return 0
    gate = None if a.sem_gate else carregar_gate(a.gate)
    res = gravar(cards, Path(a.saida), gate)
    print(f"{len(cards)} cards 🎬 em {a.saida} (carrossel + legenda + posts do X), todos com status rascunho")
    if gate is None:
        print("gate: não encontrado (use --gate CAMINHO)")
        return 0
    cont = {}
    for r in res.values():
        cont[r["resultado"]] = cont.get(r["resultado"], 0) + 1
    print("gate: " + ", ".join(f"{k} {v}" for k, v in sorted(cont.items())))
    return 2 if cont.get("BLOQUEADO") else 0


if __name__ == "__main__":
    sys.exit(main())
