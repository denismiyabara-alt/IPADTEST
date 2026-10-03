#!/usr/bin/env python3
"""Mede a voz do Denis nas RESPOSTAS DO CANAL e atualiza a parte automática do comentarios/voz_denis.md.

Entrada (sem rede):
  comentarios/dados/respostas_canal.csv   gerado pelo coletar.py no Mac (padrão)
  --de-auditoria                          usa as replies do canal em auditoria-canal/dados/comentarios_top30.csv

Saída:
  voz_denis.md, só o trecho entre <!-- auto:inicio --> e <!-- auto:fim --> (números agregados, sem nome de ninguém);
  comentarios/dados/voz_exemplos_candidatos.txt (no .gitignore): respostas curtas, com @menções e o "Fulano San" do
  começo tirados, para o Denis escolher exemplos novos e colar à mão na parte curada do voz_denis.md.

uso: python3 comentarios/voz.py [--de-auditoria] [--desde 2023-01-01]
"""
import argparse
import csv
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import regras  # noqa: E402

RESPOSTAS = AQUI / "dados" / "respostas_canal.csv"
AUDITORIA = AQUI.parent / "auditoria-canal" / "dados" / "comentarios_top30.csv"
VOZ = AQUI / "voz_denis.md"
CANDIDATOS = AQUI / "dados" / "voz_exemplos_candidatos.txt"
INI, FIM = "<!-- auto:inicio -->", "<!-- auto:fim -->"

# "Fulano San", "Fala, Fulano san", "Fulana chuan": vocativo com nome de quem comentou. Sai dos exemplos.
VOCATIVO = re.compile(r"^\s*(fala,?\s+)?([@\w.\-]+\s+){1,2}(san+|sama|chuan+|chan)\b[\s,!.]*", re.I)
ARROBA = re.compile(r"@[\w.\-]+")
MARCAS = [("s2", r"\bs2\b"), ("^^", r"\^\^"), ("lol", r"\blol\b"), ("risada escrita (hahaha, kkk, hauhau)",
          r"(ha){2,}|(hau|hua|ah){2,}|k{3,}"), ("😂/🤣", r"[😂🤣]"), ("💛/❤", r"[💛❤]"), ("arigatou", r"arigat"),
          ("\"eh\" no lugar de \"é\"", r"\beh\b"), ("neh", r"\bneh\b"), ("mto/msm/tbm/vc", r"\b(mto|msm|tbm|vc)\b"),
          ("vrau", r"vrau"), ("Tanaka/Tanakão no texto", r"tanaka"), ("San/sama/chuan (nome de quem comentou)",
          r"\b(san+|sama|chuan+)\b"), ("link para vídeo (youtu)", r"youtu"), ("pergunta de volta (termina em ?)", r"\?\s*$")]


def ler(args):
    if args.de_auditoria:
        cs = list(csv.DictReader(open(AUDITORIA, newline="", encoding="utf-8")))
        pais = {c["comentario_id"]: c for c in cs}
        return [{"publicado_em": c["publicado_em"], "texto": c["texto"],
                 "pai": pais.get(c["resposta_a"], {}).get("texto", "")}
                for c in cs if c.get("eh_do_canal") == "1" and c.get("eh_resposta") == "1"]
    if not args.respostas.exists():
        raise SystemExit(f"não achei {args.respostas}: rode antes o coletar.py (ou use --de-auditoria)")
    return [dict(r, pai="") for r in csv.DictReader(open(args.respostas, newline="", encoding="utf-8"))]


def limpar(texto):
    t = ARROBA.sub("", texto or "")
    return VOCATIVO.sub("", t).strip()


def abertura(texto):
    t = regras.norm(ARROBA.sub("", texto or ""))
    if re.match(r"^(fala,?\s+)?([\w.\-]+\s+){1,2}(san+|sama|chuan+|chan)\b", t):
        return "nome de quem comentou + San/chuan"
    for nome, rx in [("Fala, ...", r"^fala\b"), ("Tanaka/Tanakão/Tanakaooo", r"^tanaka"), ("risada", r"^(ha|hau|hua|ah|k){2,}"),
                     ("sim/não esticado (simmm, naooo)", r"^(sim+|nao+|isso+|exato+)\b"), ("arigatou/valeu", r"^(arigat|valeu|obrigad)"),
                     ("emoji", r"^[^\w\s]")]:
        if re.search(rx, t):
            return nome
    return "direto no assunto"


def fechamento(texto):
    t = (texto or "").strip()
    for nome, rx in [("s2", r"s2+\s*$"), ("^^", r"\^\^\s*$"), ("lol", r"lol\s*$"), ("emoji", r"[^\w\s?!.,)\]=(:]\s*$"),
                     ("risada", r"((ha|hau|hua|ah){2,}|k{3,})\s*$"), ("pergunta de volta", r"\?\s*$"), ("link", r"https?://\S+\s*$")]:
        if re.search(rx, t, re.I):
            return nome
    return "ponto final ou nada"


def pct(n, tot):
    return f"{100 * n / tot:.0f}%" if tot else "-"


def resumo(rs, rotulo):
    if not rs:
        return [f"**{rotulo}:** nenhuma resposta."]
    c = [len(r["texto"]) for r in rs]
    p = [len(r["texto"].split()) for r in rs]
    q = sorted(c)
    linhas = [f"**{rotulo}:** {len(rs)} respostas. Tamanho: mediana de {statistics.median(c):.0f} caracteres "
              f"({statistics.median(p):.0f} palavras); metade fica entre {q[len(q) // 4]} e {q[3 * len(q) // 4]} caracteres; "
              f"{pct(sum(1 for r in rs if chr(10) not in r['texto'].strip()), len(rs))} cabem numa linha só.", ""]
    ab, fe = Counter(abertura(r["texto"]) for r in rs), Counter(fechamento(r["texto"]) for r in rs)
    linhas.append("| abre com | % |  | fecha com | % |")
    linhas.append("|---|---|---|---|---|")
    a, f = ab.most_common(7), fe.most_common(7)
    for i in range(max(len(a), len(f))):
        x = a[i] if i < len(a) else ("", 0)
        y = f[i] if i < len(f) else ("", 0)
        linhas.append(f"| {x[0]} | {pct(x[1], len(rs)) if x[0] else ''} |  | {y[0]} | {pct(y[1], len(rs)) if y[0] else ''} |")
    linhas += ["", "| marca | aparece em |", "|---|---|"]
    for nome, rx in MARCAS:
        n = sum(1 for r in rs if re.search(rx, r["texto"], re.I) or re.search(rx, regras.norm(r["texto"])))
        linhas.append(f"| {nome} | {pct(n, len(rs))} |")
    return linhas


def recomendacao(rs):
    alvo = [r for r in rs if r.get("pai") and "pede_recomendacao" in regras.riscos(r["pai"])]
    if not alvo:
        return ["Sem o texto da pergunta original nesta base (o respostas_canal.csv guarda só a resposta); rode com "
                "--de-auditoria para medir isso."]
    tick = sum(1 for r in alvo if regras.TICKER.search(r["texto"]))
    link = sum(1 for r in alvo if "youtu" in r["texto"])
    inst = sum(1 for r in alvo if regras.INSTITUICAO.search(regras.norm(r["texto"])))
    med = statistics.median(len(r["texto"]) for r in alvo)
    return [f"{len(alvo)} respostas a perguntas do tipo \"qual comprar / vale a pena / ticker\" (mediana de {med:.0f} "
            f"caracteres). Em {pct(tick, len(alvo))} a resposta cita ticker, em {pct(inst, len(alvo))} cita banco, corretora "
            f"ou exchange pelo nome, e em {pct(link, len(alvo))} manda um link de vídeo. **Os rascunhos não copiam "
            f"o nome do ativo nem o da instituição** (regra do canal: nada de call de ativo nominal, nada de corretora); "
            f"copiam o tamanho e o tom."]


def main(argv=None):
    ap = argparse.ArgumentParser(description="Mede a voz das respostas do canal e atualiza voz_denis.md.")
    ap.add_argument("--respostas", type=Path, default=RESPOSTAS)
    ap.add_argument("--de-auditoria", action="store_true")
    ap.add_argument("--desde", default="2023-01-01", help="corte da fase recente (padrão 2023-01-01)")
    ap.add_argument("--voz", type=Path, default=VOZ)
    a = ap.parse_args(argv)
    rs = [r for r in ler(a) if (r.get("texto") or "").strip()]
    rec = [r for r in rs if r["publicado_em"][:10] >= a.desde]
    fonte = ("auditoria-canal/dados/comentarios_top30.csv (30 vídeos com mais views)" if a.de_auditoria
             else "comentarios/dados/respostas_canal.csv (coletar.py)")
    datas = sorted(r["publicado_em"][:10] for r in rs)
    bloco = [INI, f"_Gerado por `python3 comentarios/voz.py{' --de-auditoria' if a.de_auditoria else ''}` a partir de "
             f"{fonte}: {len(rs)} respostas do canal, de {datas[0] if datas else '-'} a {datas[-1] if datas else '-'}. "
             f"Só números agregados; nenhum nome._", ""]
    bloco += resumo(rec, f"Fase recente (desde {a.desde}), a que vale para os rascunhos") + [""]
    bloco += resumo(rs, "Todas as respostas (inclui 2018 a 2022, fase de bancos digitais)") + [""]
    bloco += ["**Como ele responde a \"qual comprar\":** " + " ".join(recomendacao(rs)), "", FIM]
    texto = a.voz.read_text(encoding="utf-8") if a.voz.exists() else f"# Voz do Denis nas respostas\n\n{INI}\n{FIM}\n"
    i, j = texto.index(INI), texto.index(FIM) + len(FIM)
    a.voz.write_text(texto[:i] + "\n".join(bloco) + texto[j:], encoding="utf-8")
    cand = sorted({limpar(r["texto"]) for r in rec if 15 <= len(limpar(r["texto"])) <= 160}, key=len)
    CANDIDATOS.parent.mkdir(parents=True, exist_ok=True)
    CANDIDATOS.write_text("\n".join(cand) + "\n", encoding="utf-8")
    print(f"{a.voz} atualizado ({len(rs)} respostas; {len(rec)} desde {a.desde}); {len(cand)} candidatos a exemplo em "
          f"{CANDIDATOS} (fora do git; confira se não sobrou nome antes de colar)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
