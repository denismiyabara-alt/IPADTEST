#!/usr/bin/env python3
"""Monta a fila de respostas: perguntas sem resposta do canal, por prioridade, com rascunho na voz do Denis.

NÃO POSTA NADA. Lê comentarios/dados/threads.csv (do coletar.py) e grava comentarios/fila.csv para o Denis aprovar
em lote. Outra etapa, separada, publica só o que estiver com status "aprovado" ou "editado".

Prioridade (0 a 100) = 100 × (0,50 × likes + 0,30 × vídeo vivo + 0,20 × recência), cada fator entre 0 e 1:
  likes      = log(1 + likes) / log(1 + 50), com teto 1   (50 likes ou mais = nota cheia; 5 likes ≈ 0,46)
  vídeo vivo = log10(1 + views dos últimos 28 dias) / log10(1 + 50.000), com teto 1; se o Analytics não veio,
               usa a idade do vídeo: 1 / (1 + idade_em_dias / 365)   (vídeo de 1 ano = 0,5)
  recência   = 1 / (1 + idade_do_comentário_em_dias / 90)        (comentário de 3 meses = 0,5)
A coluna "peso" mostra a conta de cada linha. Spam/golpe vai para o fim, com status "ocultar".

Status que o script escreve: rascunho | precisa_rascunho (pergunta nova, sem rascunho) | fora_escopo | ocultar.
O Denis troca para: aprovado | editado (e corrige a coluna rascunho) | pular. Ao rodar de novo, as linhas que ele já
marcou mantêm status e rascunho; as threads que o canal respondeu saem da fila sozinhas.

uso:
  python3 comentarios/fila.py                  threads.csv -> fila.csv
  python3 comentarios/fila.py --de-auditoria   usa auditoria-canal/dados/comentarios_top30.csv (sem autor, sem views 28 d)
  python3 comentarios/fila.py --exemplo        regenera fila_exemplo.csv a partir da fixture (dados inventados)
"""
import argparse
import csv
import json
import math
import re
import sys
import tempfile
from datetime import date, datetime
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import regras  # noqa: E402

THREADS = AQUI / "dados" / "threads.csv"
FILA = AQUI / "fila.csv"
EXEMPLO = AQUI / "fila_exemplo.csv"
RASCUNHOS = AQUI / "rascunhos.json"
AUDITORIA = AQUI.parent / "auditoria-canal" / "dados"
FIXTURE = AQUI / "tests" / "fixture_api.json"
RASCUNHOS_FIXTURE = AQUI / "tests" / "rascunhos_fixture.json"

COLUNAS = ["prioridade", "video_id", "video_titulo", "link", "comment_id", "autor", "data", "likes", "texto", "tema",
           "rascunho", "status", "nota_risco", "peso"]
PESOS = {"likes": 0.50, "video": 0.30, "recencia": 0.20}
REF_LIKES, REF_VIEWS, MEIA_VIDA_VIDEO, MEIA_VIDA_COMENT = 50, 50_000, 365, 90
STATUS_DENIS = {"aprovado", "editado", "pular"}


def _data(s):
    s = (s or "")[:10]
    try:
        return date.fromisoformat(s)
    except ValueError:
        return None


def fatores(likes, views_28d, video_publicado, publicado_em, hoje):
    likes = max(0, int(likes or 0))
    f_likes = min(1.0, math.log1p(likes) / math.log1p(REF_LIKES))
    if str(views_28d).strip() != "":
        v = max(0, int(float(views_28d)))
        f_video = min(1.0, math.log10(1 + v) / math.log10(1 + REF_VIEWS))
        txt_video = f"views 28d {v:,}".replace(",", ".")
    else:
        dv = _data(video_publicado)
        idade = (hoje - dv).days if dv else 3650
        f_video = 1 / (1 + max(0, idade) / MEIA_VIDA_VIDEO)
        txt_video = f"vídeo de {dv.isoformat()[:7] if dv else '?'} (sem views 28d)"
    dc = _data(publicado_em)
    f_rec = 1 / (1 + max(0, (hoje - dc).days if dc else 3650) / MEIA_VIDA_COMENT)
    return f_likes, f_video, f_rec, txt_video


def prioridade(likes, views_28d, video_publicado, publicado_em, hoje):
    fl, fv, fr, _ = fatores(likes, views_28d, video_publicado, publicado_em, hoje)
    return round(100 * (PESOS["likes"] * fl + PESOS["video"] * fv + PESOS["recencia"] * fr), 1)


def explicar(likes, views_28d, video_publicado, publicado_em, hoje):
    fl, fv, fr, tv = fatores(likes, views_28d, video_publicado, publicado_em, hoje)
    c = lambda x: f"{x:.2f}".replace(".", ",")  # noqa: E731
    return (f"likes {int(likes or 0)}→{c(fl)}×0,5 + {tv}→{c(fv)}×0,3 + "
            f"comentário de {(publicado_em or '?')[:10]}→{c(fr)}×0,2")


def link(video_id, comment_id):
    return f"https://www.youtube.com/watch?v={video_id}&lc={comment_id}"


def ler_csv(caminho):
    with open(caminho, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def threads_da_auditoria(dados=AUDITORIA):
    """Converte comentarios_top30.csv (auditoria de 01/10/2026) para o formato do threads.csv. Sem autor (a
    auditoria só guarda um hash) e sem views de 28 dias por vídeo (a fila usa a data do vídeo)."""
    vids = {r["id"]: r for r in ler_csv(dados / "videos.csv")}
    cs = ler_csv(dados / "comentarios_top30.csv")
    respondidas = {c["resposta_a"] for c in cs if c.get("eh_do_canal") == "1" and c.get("resposta_a")}
    out = []
    for c in cs:
        if c.get("eh_resposta") != "0" or c.get("eh_do_canal") == "1":
            continue
        v = vids.get(c["video_id"], {})
        resp = c["comentario_id"] in respondidas
        out.append({"video_id": c["video_id"], "video_titulo": v.get("titulo", ""),
                    "video_publicado": (v.get("publicado_em_brt") or "")[:10], "views_28d": "",
                    "comment_id": c["comentario_id"], "autor": "", "publicado_em": c.get("publicado_em", ""),
                    "likes": c.get("likes", 0), "texto": c.get("texto", ""), "respondido_pelo_canal": int(resp),
                    "sem_resposta": int(not resp), "eh_pergunta": int(regras.eh_pergunta(c.get("texto", "")))})
    return out


def ler_rascunhos(caminho=RASCUNHOS):
    p = Path(caminho)
    if not p.exists():
        return {}
    return {k: v for k, v in json.loads(p.read_text(encoding="utf-8")).items() if not k.startswith("_")}


def montar(threads, rascunhos, hoje, anterior=None):
    anterior = anterior or {}
    fila, spam = [], []
    for t in threads:
        if str(t.get("sem_resposta")) != "1":
            continue
        texto = re.sub(r"\s+", " ", t.get("texto") or "").strip()
        risco = regras.nota_risco(texto)
        eh_spam = risco == "spam/golpe"
        if not eh_spam and str(t.get("eh_pergunta")) != "1":
            continue
        tema = regras.tema(texto, t["video_id"])
        cid = t["comment_id"]
        if eh_spam:
            rasc, status = "", "ocultar"
        elif rascunhos.get(cid):
            rasc, status = rascunhos[cid], "rascunho"
        elif regras.fora_do_escopo(tema):
            rasc, status = "", "fora_escopo"
        else:
            rasc, status = "", "precisa_rascunho"
        ant = anterior.get(cid)
        if ant and ant.get("status") in STATUS_DENIS:
            rasc, status = ant.get("rascunho", rasc), ant["status"]
        args = (t.get("likes"), t.get("views_28d", ""), t.get("video_publicado"), t.get("publicado_em"), hoje)
        linha = {"prioridade": prioridade(*args), "video_id": t["video_id"], "video_titulo": t.get("video_titulo", ""),
                 "link": link(t["video_id"], cid), "comment_id": cid, "autor": t.get("autor", ""),
                 "data": (t.get("publicado_em") or "")[:10], "likes": int(t.get("likes") or 0), "texto": texto,
                 "tema": tema, "rascunho": rasc, "status": status, "nota_risco": risco, "peso": explicar(*args)}
        (spam if eh_spam else fila).append(linha)
    chave = lambda r: (-r["prioridade"], -r["likes"], r["comment_id"])  # noqa: E731
    return sorted(fila, key=chave) + sorted(spam, key=chave)


def gravar(caminho, linhas):
    with open(caminho, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS)
        w.writeheader()
        w.writerows(linhas)


def main(argv=None):
    ap = argparse.ArgumentParser(description="Gera a fila de respostas (não posta nada).")
    ap.add_argument("--threads", type=Path, default=THREADS)
    ap.add_argument("--rascunhos", type=Path, default=RASCUNHOS)
    ap.add_argument("--saida", type=Path, default=FILA)
    ap.add_argument("--de-auditoria", action="store_true", help="usa comentarios_top30.csv da auditoria")
    ap.add_argument("--exemplo", action="store_true", help="regenera fila_exemplo.csv a partir da fixture")
    ap.add_argument("--hoje", type=date.fromisoformat, default=None)
    a = ap.parse_args(argv)
    hoje = a.hoje or datetime.now().date()

    if a.exemplo:
        import coletar
        with tempfile.TemporaryDirectory() as tmp:
            arq = Path(tmp) / "threads.csv"
            coletar.main(["--fixture", str(FIXTURE), "--saida", str(arq), "--hoje", "2026-10-03"])
            linhas = montar(ler_csv(arq), ler_rascunhos(RASCUNHOS_FIXTURE), date(2026, 10, 3))
        gravar(EXEMPLO, linhas)
        print(f"{len(linhas)} linhas em {EXEMPLO}")
        return 0

    if a.de_auditoria:
        threads = threads_da_auditoria()
    elif a.threads.exists():
        threads = ler_csv(a.threads)
    else:
        print(f"não achei {a.threads}: rode antes  python3 comentarios/coletar.py  (ou use --de-auditoria)",
              file=sys.stderr)
        return 2
    anterior = {r["comment_id"]: r for r in ler_csv(a.saida)} if a.saida.exists() else {}
    linhas = montar(threads, ler_rascunhos(a.rascunhos), hoje, anterior)
    gravar(a.saida, linhas)
    cont = {}
    for r in linhas:
        cont[r["status"]] = cont.get(r["status"], 0) + 1
    print(f"{len(linhas)} linhas em {a.saida}: " + ", ".join(f"{k} {v}" for k, v in sorted(cont.items())))
    print("Nada foi postado. Marque a coluna status como aprovado, editado ou pular.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
