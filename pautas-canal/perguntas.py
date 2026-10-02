#!/usr/bin/env python3
"""Separa as perguntas SEM resposta do canal em auditoria-canal/dados/comentarios_top30.csv e agrupa por tema.

Critério (o mesmo do analisar.py, seção 8):
  pergunta  = comentário de topo (eh_resposta = 0), do público (eh_do_canal = 0), cujo texto normalizado casa a regra
              PERGUNTA do analisar.py: tem "?" ou começa com como/qual/quando/onde/quanto/por que/o que/vale a pena/
              devo/compensa/alguém sabe/será que/tem como/dá pra/você acha/faz um vídeo...
  sem resposta = nenhum comentário do próprio canal (eh_do_canal = 1) com resposta_a = id da pergunta.
              Resposta de outro usuário não conta como resposta do canal.

Tema: regras de palavras-chave (TEMAS abaixo; o primeiro que casar leva, então a ordem importa: imposto e cripto
vêm antes de conta digital). Temas fora do escopo do canal (cartão de
crédito, dívida pessoal, política) são separados e não recebem rascunho de resposta.

Saída: perguntas.csv (uma linha por pergunta, sem autor e sem @menções) e o resumo no terminal.
uso: python3 perguntas.py [--json]
"""
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI.parent / "auditoria-canal"))
import analisar as an  # noqa: E402

FORA = "fora do escopo"
TEMAS = [
    (f"Cartão de crédito ({FORA})", r"cartao|cartoes|fatura|anuidade|rotativo|limite do cartao|\bcredito\b"),
    (f"Dívida pessoal ({FORA})", r"divida|dividas|emprestimo|consignado|serasa|nome sujo|negativad"),
    (f"Política ({FORA})", r"\blula\b|bolsonaro|eleic|partido|\bvoto\b|\bstf\b|presidente|governo lula"),
    ("Imposto de renda e declaração", r"imposto|\bir\b|declar|tribut|isent|darf|come.?cotas|receita federal"),
    ("Cripto", r"bitcoin|\bbtc\b|cripto|ethereum"),
    ("Menor de idade e filhos", r"menor de idade|de menor|contas? de menor|meu filho|minha filha|meus filhos|crianca|\b1[0-7] anos\b"),
    ("Rendimento: quanto rende, CDB, LCI, poupança, Tesouro", r"quanto rende|rendimento|render|rende\b|\bcdb|\blci|\blca|"
     r"poupanca|tesouro|selic|\bcdi\b|ipca|renda fixa|caixinha|fgc"),
    ("ETFs, BDRs e exterior", r"\betf|\bbdr|exterior|dolar|s&p|nasdaq"),
    ("Ações, dividendos e FIIs", r"\b[a-z]{4}(3|4|5|6|11)\b|\bacao\b|\bacoes\b|dividendo|provento|\bfii|fundo imobiliario|"
     r"fundos imobiliarios|bolsa|barsi|corretora|home broker"),
    ("Conta digital: tarifas, transferências e funcionamento", r"\bconta\b|\bnext\b|nubank|banco inter|\binter\b|bradesco|"
     r"santander|itau|\bpix\b|\bted\b|\bdoc\b|transferen|tarifa|\bcobra|agencia|saque|boleto|deposit|debito|"
     r"mercado pago|picpay|\bc6\b|banco digital|abrir conta|app\b|aplicativo"),
    ("Começar a investir e juros compostos", r"centavo|comecar|iniciante|pouco dinheiro|primeiro investimento|juros composto|"
     r"1 milhao|um milhao|dobrar"),
    ("Aposentadoria e previdência", r"aposentad|previdencia|pgbl|vgbl|\binss"),
]


SHORT_1_CENTAVO = "aDL4MMF6AnE"   # o Short "Pra ficar rico você só precisa de 1 centavo"
GRUPO_1_CENTAVO = "Short do 1 centavo: como dobra? é possível? (dúvida e ironia sobre a conta)"


def tema(texto, video_id=""):
    t = an.norm(texto)
    for nome, rx in TEMAS:
        if re.search(rx, t):
            return nome
    if video_id == SHORT_1_CENTAVO or re.search(r"dobr|centavo|10 milh|matematica|calculo", t):
        return GRUPO_1_CENTAVO
    return "Outros (sem palavra-chave de tema)"


def perguntas_sem_resposta(caminho=AQUI.parent / "auditoria-canal" / "dados" / "comentarios_top30.csv"):
    cs = list(csv.DictReader(open(caminho, newline="", encoding="utf-8")))
    respondidas = {c["resposta_a"] for c in cs if c.get("eh_do_canal") == "1" and c.get("resposta_a")}
    perg = [c for c in cs if c.get("eh_do_canal") != "1" and c.get("eh_resposta") == "0"
            and an.PERGUNTA.search(an.norm(c.get("texto", "")))]
    sem = [c for c in perg if c["comentario_id"] not in respondidas]
    return perg, sem


def main():
    perg, sem = perguntas_sem_resposta()
    titulos = {r["id"]: r["titulo"] for r in csv.DictReader(open(AQUI.parent / "auditoria-canal" / "dados" / "videos.csv",
                                                                encoding="utf-8"))}
    linhas = []
    for c in sem:
        linhas.append({"tema": tema(c["texto"], c["video_id"]), "video_id": c["video_id"], "video_titulo": titulos.get(c["video_id"], ""),
                       "comentario_id": c["comentario_id"], "likes": int(c.get("likes") or 0),
                       "publicado_em": c.get("publicado_em", "")[:10], "texto": an.sem_arroba(c["texto"])})
    linhas.sort(key=lambda r: (r["tema"], -r["likes"]))
    with open(AQUI / "perguntas.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    grupos = defaultdict(list)
    for r in linhas:
        grupos[r["tema"]].append(r)
    resumo = {"perguntas": len(perg), "sem_resposta": len(sem),
              "grupos": [{"tema": t, "n": len(l), "likes": sum(r["likes"] for r in l),
                          "exemplos": [r["texto"][:140] for r in sorted(
                              (r for r in l if 15 <= len(r["texto"]) <= 200 and "@" not in r["texto"]),
                              key=lambda r: -r["likes"])[:2]]}
                         for t, l in sorted(grupos.items(), key=lambda kv: -len(kv[1]))]}
    if "--json" in sys.argv:
        print(json.dumps(resumo, ensure_ascii=False, indent=1))
    else:
        print(f"{resumo['perguntas']} perguntas; {resumo['sem_resposta']} sem resposta do canal")
        for g in resumo["grupos"]:
            print(f"{g['n']:4}  {g['likes']:5} likes  {g['tema']}")


if __name__ == "__main__":
    main()
