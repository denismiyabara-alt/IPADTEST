#!/usr/bin/env python3
"""Esteira social: gera os cards de X e Instagram de cada vídeo do calendário (rascunhos para o juiz-post).

Lê pautas-canal/CALENDARIO-8-SEMANAS.csv, junta com o texto escrito em conteudo.py e grava, para cada vídeo
(longo e Short), dois cards no formato do ic-copywriter:

    cards/<data do vídeo>-<slug>-x.md     thread do X (5 posts no longo, 3 no Short)
    cards/<data do vídeo>-<slug>-ig.md    Instagram (carrossel de 6 slides no longo, Reels com 4 telas no Short)
    cards/INDICE.csv                      uma linha por card, com o resultado do gate
    cards/GATE-RELATORIO.md               reprovados e avisos do gate de qualidade

Todo card sai com status "rascunho". Nada é publicado: quem decide é o juiz-post e, depois, o Denis.

Só biblioteca padrão. O gate de qualidade (investir-e-cocar/pipeline/gate_qualidade.py) é importado se existir;
sem ele, os cards são gerados e o INDICE marca o gate como "não rodou".

uso:
  python3 gerar_cards.py                      # gera tudo e roda o gate
  python3 gerar_cards.py --sem-gate           # só os cards
  python3 gerar_cards.py --gate CAMINHO/gate_qualidade.py --calendario OUTRO.csv --saida OUTRA_PASTA
  python3 gerar_cards.py --checar             # só confere (números, limites, títulos) e sai com 1 se houver erro
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

CANAL = "Investir e Coçar"
LIMITE_X = 280
LINK = "[LINK DO VÍDEO: preencher na publicação]"

HASHTAGS_BASE = ["#InvestirECocar", "#EducacaoFinanceira", "#Investimentos", "#FinancasPessoais"]
HASHTAGS_ASSUNTO = {
    "tesouro e renda fixa": ["#RendaFixa", "#TesouroDireto", "#CDB", "#LCIeLCA", "#FGC", "#Juros"],
    "renda mensal": ["#RendaMensal", "#DividendosMensais", "#Dividendos", "#ETF", "#FundosImobiliarios", "#RendaPassiva"],
    "crise e macro": ["#Crise", "#Economia", "#MercadoFinanceiro", "#Bolsa", "#Macroeconomia", "#InteligenciaArtificial"],
    "FII": ["#FII", "#FundosImobiliarios", "#RendaMensal", "#Imoveis", "#Aluguel", "#IFIX"],
    "imposto e regras": ["#ImpostoDeRenda", "#IR", "#Dividendos", "#JCP", "#FII", "#Tributacao"],
    "comportamento e família": ["#FinancasDoCasal", "#Planejamento", "#Objetivos", "#Comportamento", "#Familia", "#Dinheiro"],
    "juntar dinheiro e aposentadoria": ["#JurosCompostos", "#Aposentadoria", "#PrimeiroMilhao", "#Poupar", "#LongoPrazo", "#Planejamento"],
    "cripto": ["#Bitcoin", "#Cripto", "#Criptomoedas", "#BTC", "#Risco", "#Volatilidade"],
    "ETF e exterior": ["#ETF", "#TaxaDeAdministracao", "#Dividendos", "#RendaVariavel", "#LongoPrazo", "#Custos"],
}
ESTRUTURAS = {
    "A": "O Choque → A Causa Escondida",
    "B": "O Personagem → O Twist",
    "C": "O Antes / Depois",
    "D": "A Pergunta Que Ninguém Faz",
    "E": "A Linha do Tempo Invertida",
}
RE_CHECAR = re.compile(r"\[CHECAR:[^\]]*\]")
RE_NUM = re.compile(r"(?<![\w])\d+(?:[.,]\d+)*")


# ---------------------------------------------------------------- utilidades
def sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def slugify(titulo, maximo=50):
    s = re.sub(r"[^a-z0-9]+", "-", sem_acento(titulo).lower()).strip("-")
    if len(s) <= maximo:
        return s
    return s[:maximo].rsplit("-", 1)[0]


def ddmm(iso):
    return f"{iso[8:10]}/{iso[5:7]}"


def canon(num):
    """'1.000' -> '1000'; '17,5' -> '175'. Compara número com número, sem se importar com o separador."""
    return re.sub(r"\D", "", num)


def numeros_do_texto(texto):
    return [m.group(0) for m in RE_NUM.finditer(RE_CHECAR.sub(" ", texto))]


def ler_calendario(caminho=CALENDARIO):
    with open(caminho, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------- agenda (relativa ao vídeo)
def agenda(row, rede, extra):
    """(data, horário, texto relativo). Longo sai às 19h; Short no horário do canal."""
    d = date.fromisoformat(row["data"])
    if extra.get("evento_ao_vivo") and row["formato"] == "short":
        return (d.isoformat(), "09:00" if rede == "x" else "10:00",
                "D+0, de manhã, ANTES da decisão do Copom (evento ao vivo)")
    if row["formato"] == "longo":
        if rede == "x":
            return d.isoformat(), "19:30", "D+0, 30 min depois do vídeo (19h)"
        return (d + timedelta(days=1)).isoformat(), "12:00", "D+1, almoço do dia seguinte ao vídeo"
    if rede == "x":
        return d.isoformat(), "12:00", "D+0, no dia do Short"
    return d.isoformat(), "18:00", "D+0, Reels com o mesmo vídeo do Short"


# ---------------------------------------------------------------- números
def checar_numeros(card, row, pautas=PAUTAS):
    """Lista de problemas: número no texto sem origem, ou origem declarada que não confere."""
    probs = []
    permitidos = {canon(n) for n in numeros_do_texto(" ".join(row.values()))}
    cache = {}
    for n in card["numeros"]:
        v = canon(n["valor"])
        if n["fonte"] == "cálculo":
            try:
                r = eval(n["conta"], {"__builtins__": {}}, {})  # só aritmética escrita em conteudo.py
            except Exception as e:  # pragma: no cover
                probs.append(f'conta inválida para {n["valor"]}: {e}')
                continue
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
                probs.append(f'{n["valor"]} não aparece no trecho de {n["fonte"]}: "{n["trecho"]}"')
                continue
        permitidos.add(v)
    for num in numeros_do_texto(card["texto_gate"]):
        if canon(num) not in permitidos:
            probs.append(f'número sem origem no calendário/TEMAS/TERMOS: "{num}"')
    return probs


# ---------------------------------------------------------------- cards
def montar_cards(rows=None):
    rows = rows if rows is not None else ler_calendario()
    cards = []
    faltando = [r["data"] for r in rows if r["data"] not in conteudo.C]
    if faltando:
        raise SystemExit(f"Sem texto em conteudo.py para: {', '.join(faltando)} (não gero template vazio)")
    for row in rows:
        c = conteudo.C[row["data"]]
        if c["titulo"] != row["titulo"]:
            raise SystemExit(f'{row["data"]}: título do calendário mudou ("{row["titulo"]}" x "{c["titulo"]}")')
        slug = slugify(row["titulo"])
        longo = row["formato"] == "longo"
        base = {
            "video_data": row["data"], "video_formato": row["formato"], "video_titulo": row["titulo"],
            "assunto": row["assunto"], "termo_busca": row["termo_busca"] or "—",
            "angulo": row["angulo"], "fontes_a_conferir": row["fontes_a_conferir"],
            "numeros": c.get("numeros", []), "evento_ao_vivo": c.get("evento_ao_vivo", ""),
            "corte_de": c.get("corte_de", ""), "status": "rascunho", "_row": row,
        }
        # X
        tw = c["x"]["tweets"]
        tipos = ["hook"] + ["desenvolvimento"] * (len(tw) - 2) + ["fechamento"]
        d, h, rel = agenda(row, "x", c)
        reply = f"Vídeo completo aqui: {LINK}" if longo else f"O Short: {LINK}"
        if c.get("corte_de"):
            reply += f"\n\nE o vídeo completo de {ddmm(c['corte_de'])}: [LINK DO VÍDEO DE {ddmm(c['corte_de'])}]"
        x = dict(base, rede="x", id=f"{row['data']}-{slug}-x", arquivo=f"{row['data']}-{slug}-x.md",
                 formato=f"thread de {len(tw)} posts", data_publicacao=d, horario=h, relativa_ao_video=rel,
                 gancho=tw[0].split("\n")[0], estrutura=c["x"]["estrutura"], mecanica=c["x"]["mecanica"],
                 tweets=[{"numero": i + 1, "tipo": t, "texto": s} for i, (t, s) in enumerate(zip(tipos, tw))],
                 cta=reply, imagem=c["x"]["imagem"])
        x["texto_gate"] = "\n\n".join(tw) + "\n\n" + reply
        # Instagram
        ig = c["ig"]
        d, h, rel = agenda(row, "ig", c)
        if longo:
            cta = f"O vídeo completo está no YouTube, no canal {CANAL}. Link na bio."
        elif c.get("corte_de"):
            cta = f"Esse é um pedaço do vídeo de {ddmm(c['corte_de'])}. O completo está no YouTube, no canal {CANAL}. Link na bio."
        else:
            cta = f"Mais contas assim no YouTube, no canal {CANAL}. Link na bio."
        tags = HASHTAGS_BASE + HASHTAGS_ASSUNTO[row["assunto"]]
        i_g = dict(base, rede="instagram", id=f"{row['data']}-{slug}-ig", arquivo=f"{row['data']}-{slug}-ig.md",
                   formato=("carrossel" if longo else "reels") + f" ({len(ig['slides'])} {'slides' if longo else 'telas'})",
                   tipo_post="carrossel" if longo else "reels",
                   data_publicacao=d, horario=h, relativa_ao_video=rel, gancho=ig["legenda"].split("\n")[0],
                   legenda=ig["legenda"], cta=cta, hashtags=" ".join(tags),
                   slides=[{"numero": i + 1, "texto": s} for i, s in enumerate(ig["slides"])], imagem=ig["imagem"])
        i_g["texto_gate"] = ig["legenda"] + "\n\n" + cta + "\n\n" + "\n\n".join(ig["slides"])
        cards += [x, i_g]
    return cards


def pendencias(card):
    return sorted(set(RE_CHECAR.findall(card["texto_gate"])))


def _bloco(texto):
    return "\n".join("> " + l if l else ">" for l in texto.split("\n"))


def _fontes_md(card):
    linhas = [f'- Calendário ({ddmm(card["video_data"])}): fontes a conferir: {card["fontes_a_conferir"]}. '
              f'Ângulo: {card["angulo"]}',
              "- Números da própria linha do calendário: liberados (a linha é o briefing)."]
    for n in card["numeros"]:
        if n["fonte"] == "cálculo":
            linhas.append(f'- {n["valor"]}: cálculo `{n["conta"]}` a partir de {n["entradas"]}')
        else:
            linhas.append(f'- {n["valor"]}: pautas-canal/{n["fonte"]}: "{n["trecho"]}"')
    return "\n".join(linhas)


def _json(card):
    comum = {"id": card["id"], "status": card["status"], "topico": card["video_titulo"],
             "video": {"data": card["video_data"], "formato": card["video_formato"], "titulo": card["video_titulo"],
                       "assunto": card["assunto"], "termo_busca": card["termo_busca"]},
             "publicacao": {"data": card["data_publicacao"], "horario": card["horario"],
                            "relativa_ao_video": card["relativa_ao_video"]},
             "gancho": card["gancho"], "cta": card["cta"], "imagem": card["imagem"],
             "numeros": card["numeros"], "pendencias": pendencias(card)}
    if card["rede"] == "x":
        comum.update(rede="x", estrutura=card["estrutura"], mecanica=card["mecanica"], tweets=card["tweets"],
                     reply_com_link=card["cta"])
    else:
        comum.update(rede="instagram", formato=card["tipo_post"], instagram_caption=card["legenda"],
                     slides=card["slides"], hashtags=card["hashtags"])
    return json.dumps(comum, ensure_ascii=False, indent=2)


def _frontmatter(card):
    campos = [("id", card["id"]), ("rede", "X" if card["rede"] == "x" else "Instagram"), ("formato", card["formato"]),
              ("status", card["status"]), ("juiz", "juiz-post"),
              ("data_publicacao", card["data_publicacao"]), ("horario", card["horario"]),
              ("relativa_ao_video", card["relativa_ao_video"]),
              ("video_data", card["video_data"]), ("video_formato", card["video_formato"]),
              ("video_titulo", card["video_titulo"]), ("assunto", card["assunto"]), ("termo_busca", card["termo_busca"]),
              ("gancho", card["gancho"])]
    if card["rede"] == "x":
        campos += [("estrutura", f'{card["estrutura"]} ({ESTRUTURAS[card["estrutura"]]})'), ("mecanica", card["mecanica"])]
    campos.append(("pendencias_checar", len(pendencias(card))))
    linhas = ["---"] + [f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in campos] + ["---"]
    return "\n".join(linhas)


def render(card):
    p = [_frontmatter(card), ""]
    quando = f'{ddmm(card["data_publicacao"])} às {card["horario"]} ({card["relativa_ao_video"]})'
    if card["rede"] == "x":
        p += [f'# 🧵 THREAD — {card["video_titulo"]} ({ddmm(card["video_data"])})',
              "**Status:** rascunho para o juiz-post. Não publicar sem a aprovação do Denis.",
              f"**Publicação sugerida:** {quando}",
              f'**Estrutura:** {card["estrutura"]} ({ESTRUTURAS[card["estrutura"]]}) · **mecanica:** {card["mecanica"]}',
              "", "## GANCHO", _bloco(card["gancho"]), ""]
        nums = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣"]
        for t in card["tweets"]:
            p += [f'## TWEET {nums[t["numero"] - 1]} — {t["tipo"].upper()} ({len(t["texto"])}/{LIMITE_X})',
                  _bloco(t["texto"]), ""]
        p += ["## ↩️ CTA: RESPOSTA COM O LINK (reply depois do último tweet; link nunca no corpo da thread)",
              _bloco(card["cta"]), "",
              "## 🖼️ SUGESTÃO DE IMAGEM (capa da thread, upload nativo)",
              f'- Imagem: {card["imagem"]}',
              f'- Alt text: {card["video_titulo"]}', ""]
    else:
        tipo = "CARROSSEL" if card["tipo_post"] == "carrossel" else "REELS"
        p += [f'# 📸 INSTAGRAM {tipo} — {card["video_titulo"]} ({ddmm(card["video_data"])})',
              "**Status:** rascunho para o juiz-post. Não publicar sem a aprovação do Denis.",
              f"**Publicação sugerida:** {quando}", "",
              "## GANCHO", _bloco(card["gancho"]), "",
              f'## LEGENDA ({len(card["legenda"])} caracteres, sem CTA e hashtags)', _bloco(card["legenda"]), "",
              "## CTA PARA O VÍDEO (última linha da legenda)", _bloco(card["cta"]), "",
              "## 🏷️ HASHTAGS", card["hashtags"], "",
              "## " + ("SLIDES DO CARROSSEL" if card["tipo_post"] == "carrossel" else "TEXTOS NA TELA DO REELS"), ""]
        for s in card["slides"]:
            rot = "capa" if s["numero"] == 1 else ("fechamento" if s["numero"] == len(card["slides"]) else "")
            p += [f'### {"Slide" if card["tipo_post"] == "carrossel" else "Tela"} {s["numero"]}{" (" + rot + ")" if rot else ""}',
                  _bloco(s["texto"]), ""]
        p += ["## 🖼️ SUGESTÃO DE IMAGEM", f'- {card["imagem"]}', ""]
    p += ["## 📌 FONTES E NÚMEROS (para o juiz-post e o Denis; não vão no post)", _fontes_md(card), ""]
    pend = pendencias(card)
    p += ["## ⚠️ PENDÊNCIAS ANTES DE APROVAR"]
    p += [f"- {x}" for x in pend] if pend else ["- nenhuma"]
    if card["evento_ao_vivo"]:
        p += [f'- Evento ao vivo: {card["evento_ao_vivo"]}']
    p += ["", "---JSON---", _json(card), "---FIM---", ""]
    return "\n".join(p)


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
    """O gate recebe post de blog (título + corpo). Aqui: título do vídeo + texto do card (sem hashtags),
    no formato Markdown e com a data de publicação do card."""
    post = gate.Post(card["video_titulo"], card["texto_gate"], "md", card["data_publicacao"])
    return gate.avaliar(post)


# ---------------------------------------------------------------- saída
def gravar(cards, saida, gate=None):
    saida.mkdir(parents=True, exist_ok=True)
    for f in saida.glob("*.md"):
        if f.name != "GATE-RELATORIO.md":
            f.unlink()
    resultados = {}
    for c in cards:
        (saida / c["arquivo"]).write_text(render(c), encoding="utf-8")
        if gate:
            resultados[c["id"]] = rodar_gate(gate, c)
    cols = ["arquivo", "id", "rede", "formato", "status", "video_data", "video_formato", "video_titulo", "assunto",
            "data_publicacao", "horario", "relativa_ao_video", "gancho", "n_posts", "max_chars_post", "estrutura",
            "mecanica", "pendencias_checar", "gate_resultado", "gate_bloqueantes", "gate_avisos", "gate_codigos"]
    with open(saida / "INDICE.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for c in cards:
            textos = [t["texto"] for t in c["tweets"]] if c["rede"] == "x" else [c["legenda"]]
            r = resultados.get(c["id"])
            w.writerow({
                "arquivo": c["arquivo"], "id": c["id"], "rede": c["rede"], "formato": c["formato"], "status": c["status"],
                "video_data": c["video_data"], "video_formato": c["video_formato"], "video_titulo": c["video_titulo"],
                "assunto": c["assunto"], "data_publicacao": c["data_publicacao"], "horario": c["horario"],
                "relativa_ao_video": c["relativa_ao_video"], "gancho": c["gancho"],
                "n_posts": len(c["tweets"]) if c["rede"] == "x" else len(c["slides"]),
                "max_chars_post": max(len(t) for t in textos),
                "estrutura": c.get("estrutura", ""), "mecanica": c.get("mecanica", ""),
                "pendencias_checar": len(pendencias(c)),
                "gate_resultado": r["resultado"] if r else "não rodou",
                "gate_bloqueantes": r["bloqueantes"] if r else "", "gate_avisos": r["avisos"] if r else "",
                "gate_codigos": ";".join(sorted({p["codigo"] for p in r["problemas"]})) if r else "",
            })
    if gate:
        (saida / "GATE-RELATORIO.md").write_text(relatorio_gate(cards, resultados), encoding="utf-8")
    return resultados


def relatorio_gate(cards, res):
    bloq = [c for c in cards if res[c["id"]]["codigo_saida"] == 2]
    avis = [c for c in cards if res[c["id"]]["codigo_saida"] == 1]
    ok = len(cards) - len(bloq) - len(avis)
    L = ["# Gate de qualidade nos cards da esteira social", "",
         "Gerado por `gerar_cards.py` com `investir-e-cocar/pipeline/gate_qualidade.py` (importado, sem alteração).",
         "Entrada de cada card: título do vídeo + texto do post (tweets; ou legenda, CTA e slides), sem hashtags,",
         "com a data de publicação do card.", "",
         f"- Cards: {len(cards)}", f"- OK: {ok}", f"- Só avisos: {len(avis)}", f"- Bloqueados: {len(bloq)}", ""]
    L += ["## Bloqueados", ""] + ([f'- `{c["arquivo"]}`: ' + "; ".join(
        f'{p["codigo"]} ({p["mensagem"]})' for p in res[c["id"]]["problemas"] if p["nivel"] == "BLOQUEANTE")
        for c in bloq] or ["- nenhum"])
    L += ["", "## Avisos", ""]
    for c in avis:
        for p in res[c["id"]]["problemas"]:
            L.append(f'- `{c["arquivo"]}`: {p["codigo"]}: {p["mensagem"]}' + (f' (trecho: "{p["trecho"]}")' if p.get("trecho") else ""))
    if not avis:
        L.append("- nenhum")
    return "\n".join(L) + "\n"


def checar(cards):
    erros = []
    for c in cards:
        for p in checar_numeros(c, c["_row"]):
            erros.append(f'{c["arquivo"]}: {p}')
        if c["rede"] == "x":
            for t in c["tweets"]:
                if len(t["texto"]) > LIMITE_X:
                    erros.append(f'{c["arquivo"]}: tweet {t["numero"]} com {len(t["texto"])} caracteres')
    return erros


def main(argv=None):
    ap = argparse.ArgumentParser(description="Gera os cards de X e Instagram a partir do calendário")
    ap.add_argument("--calendario", default=str(CALENDARIO))
    ap.add_argument("--saida", default=str(AQUI / "cards"))
    ap.add_argument("--gate", help="caminho do gate_qualidade.py (padrão: investir-e-cocar/pipeline/)")
    ap.add_argument("--sem-gate", action="store_true")
    ap.add_argument("--checar", action="store_true", help="só confere números e limites")
    a = ap.parse_args(argv)
    cards = montar_cards(ler_calendario(a.calendario))
    erros = checar(cards)
    if erros:
        print("\n".join(erros))
        return 1
    if a.checar:
        print(f"OK: {len(cards)} cards conferidos")
        return 0
    gate = None if a.sem_gate else carregar_gate(a.gate)
    res = gravar(cards, Path(a.saida), gate)
    nx = sum(c["rede"] == "x" for c in cards)
    print(f"{len(cards)} cards em {a.saida} (X: {nx}, Instagram: {len(cards) - nx}), todos com status rascunho")
    if gate is None:
        print("gate: não encontrado (use --gate CAMINHO); INDICE marca 'não rodou'")
    else:
        cont = {}
        for r in res.values():
            cont[r["resultado"]] = cont.get(r["resultado"], 0) + 1
        print("gate: " + ", ".join(f"{k} {v}" for k, v in sorted(cont.items())))
        if cont.get("BLOQUEADO"):
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
