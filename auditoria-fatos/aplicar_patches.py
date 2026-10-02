#!/usr/bin/env python3
"""Aplica os patches de auditoria-fatos/patches/ no WordPress (rodar no Mac, com credenciais).

Credenciais SÓ por variável de ambiente (Application Password do WP):
    export WP_USER='usuario'
    export WP_APP_PASSWORD='xxxx xxxx xxxx xxxx xxxx xxxx'
    export WP_BASE='https://investirecocaresocomecar.com.br'   # opcional

Uso:
    python3 aplicar_patches.py                       # = --checar em todos os patches (não escreve nada)
    python3 aplicar_patches.py --checar --lote A     # só os posts do patches/LOTE_A.json
    python3 aplicar_patches.py --checar --so 4873
    python3 aplicar_patches.py --aplicar --lote A    # aplica só posts em que TODAS as trocas casam 1 vez no raw
    python3 aplicar_patches.py --aplicar --lote A --so 4873
    python3 aplicar_patches.py --desfazer 4873       # restaura o backup mais recente do post

Cada troca casa exatamente 1 vez, ou exatamente "n" vezes quando o patch diz "n" (ex.: n=2 quando a mesma frase
do FAQ está no texto visível e no bloco JSON-LD de FAQ dentro do post; as duas são trocadas).
--checar: lê content.raw (context=edit) e diz, por troca, quantas vezes o "de" aparece exatamente. Se não aparece,
tenta o casamento tolerante (aspas, travessões, espaços, entidades) e MOSTRA o trecho do raw que casaria; nunca aplica.
--aplicar: antes de cada escrita grava backup/<post_id>_<AAAAmmdd-HHMMSS>.json com o raw; envia só o campo content;
anota o que mudou em backup/log_<AAAAmmdd>.jsonl.
"""
import argparse
import base64
import datetime as dt
import json
import os
import sys
import urllib.error
import urllib.request
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from patchlib import casar_tolerante, escolher_de  # noqa: E402

PATCHES = AQUI / "patches"
BACKUP = AQUI / "backup"


class WP:
    """Cliente mínimo da API REST do WordPress (Basic auth com Application Password)."""

    def __init__(self, base=None, user=None, senha=None):
        self.base = (base or os.environ.get("WP_BASE") or "https://investirecocaresocomecar.com.br").rstrip("/")
        user = user or os.environ.get("WP_USER")
        senha = senha or os.environ.get("WP_APP_PASSWORD")
        if not user or not senha:
            raise SystemExit("defina WP_USER e WP_APP_PASSWORD (Application Password do WordPress) no ambiente")
        self.auth = "Basic " + base64.b64encode(f"{user}:{senha}".encode()).decode()

    def _req(self, metodo, caminho, corpo=None):
        dados = json.dumps(corpo).encode() if corpo is not None else None
        req = urllib.request.Request(self.base + caminho, data=dados, method=metodo, headers={
            "Authorization": self.auth, "Content-Type": "application/json", "Accept": "application/json",
            "User-Agent": "IEC-auditoria-fatos/1.0"})
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read())
        except urllib.error.HTTPError as e:
            raise SystemExit(f"HTTP {e.code} em {metodo} {caminho}: {e.read()[:300]!r}")

    def ler(self, post_id):
        d = self._req("GET", f"/wp-json/wp/v2/posts/{post_id}?context=edit&_fields=id,modified,status,content")
        return {"raw": d["content"]["raw"], "modified": d.get("modified"), "status": d.get("status")}

    def gravar(self, post_id, content):
        d = self._req("POST", f"/wp-json/wp/v2/posts/{post_id}", {"content": content})
        return {"modified": d.get("modified")}


def carregar_patch(post_id, pasta=PATCHES):
    return json.loads((Path(pasta) / f"{post_id}.json").read_text(encoding="utf-8"))


def ids_do_lote(lote, pasta=PATCHES):
    return json.loads((Path(pasta) / f"LOTE_{lote}.json").read_text(encoding="utf-8"))["post_ids"]


def todos_ids(pasta=PATCHES):
    return sorted(int(p.stem) for p in Path(pasta).glob("*.json") if p.stem.isdigit())


def checar_post(wp, patch):
    """Devolve (ok_para_aplicar, linhas_de_relatorio, raw, meta)."""
    meta = wp.ler(patch["post_id"])
    raw = meta["raw"]
    linhas, ok = [], True
    if "elementor" in raw.lower():
        linhas.append("  ATENÇÃO: o raw menciona elementor; a página pode não usar content.raw")
    for i, t in enumerate(patch["trocas"], 1):
        _, n = escolher_de(raw, t)
        esperado = t.get("n", 1)
        if n == esperado:
            linhas.append(f"  [{i}] OK ({n}x): {t['de'][:70]}")
            continue
        ok = False
        if n > esperado:
            linhas.append(f"  [{i}] AMBÍGUO ({n}x, esperado {esperado}x): {t['de'][:70]}")
            continue
        if n:
            linhas.append(f"  [{i}] CASA {n}x, esperado {esperado}x: {t['de'][:70]}")
            continue
        tol = casar_tolerante(raw, t["de"])
        if tol:
            linhas.append(f"  [{i}] NÃO CASA exato; tolerante achou {len(tol)}x. Trecho do raw: {tol[0][:120]!r}")
        else:
            linhas.append(f"  [{i}] NÃO CASA (nem tolerante): {t['de'][:70]}")
    return ok, linhas, raw, meta


def aplicar_trocas(raw, trocas):
    novo = raw
    for t in trocas:
        esperado = t.get("n", 1)
        de, n = escolher_de(novo, t)
        if n != esperado:
            raise ValueError(f"'de' mudou de contagem durante a aplicação: {t['de'][:60]}")
        novo = novo.replace(de, t["para"])
    return novo


def gravar_backup(post_id, raw, meta, pasta=BACKUP, agora=None):
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    agora = agora or dt.datetime.now()
    arq = pasta / f"{post_id}_{agora:%Y%m%d-%H%M%S}.json"
    arq.write_text(json.dumps({"post_id": post_id, "raw": raw, "modified": meta.get("modified"),
                               "salvo_em": agora.isoformat()}, ensure_ascii=False), encoding="utf-8")
    return arq


def ultimo_backup(post_id, pasta=BACKUP):
    arqs = sorted(Path(pasta).glob(f"{post_id}_*.json"))
    return arqs[-1] if arqs else None


def logar(evento, pasta=BACKUP, agora=None):
    pasta = Path(pasta)
    pasta.mkdir(parents=True, exist_ok=True)
    agora = agora or dt.datetime.now()
    with open(pasta / f"log_{agora:%Y%m%d}.jsonl", "a", encoding="utf-8") as f:
        f.write(json.dumps({**evento, "em": agora.isoformat()}, ensure_ascii=False) + "\n")


def cmd_checar(wp, ids, pasta=PATCHES, saida=print):
    resumo = {"ok": [], "falha": []}
    for pid in ids:
        patch = carregar_patch(pid, pasta)
        ok, linhas, _, _ = checar_post(wp, patch)
        saida(f"post {pid}: {'PRONTO' if ok else 'PRECISA REVISAR'} ({len(patch['trocas'])} trocas)")
        for l in linhas:
            saida(l)
        for m in patch.get("manual", []):
            saida(f"  MANUAL (fazer no editor): {m}")
        resumo["ok" if ok else "falha"].append(pid)
    saida(f"\nprontos: {len(resumo['ok'])}  precisam revisar: {len(resumo['falha'])} {resumo['falha']}")
    return resumo


def cmd_aplicar(wp, ids, pasta=PATCHES, backup=BACKUP, saida=print):
    feitos, pulados = [], []
    for pid in ids:
        patch = carregar_patch(pid, pasta)
        ok, linhas, raw, meta = checar_post(wp, patch)
        if not ok:
            saida(f"post {pid}: PULADO (nem todas as trocas casam 1x)")
            for l in linhas:
                saida(l)
            pulados.append(pid)
            continue
        novo = aplicar_trocas(raw, patch["trocas"])
        arq = gravar_backup(pid, raw, meta, backup)
        r = wp.gravar(pid, novo)
        logar({"acao": "aplicar", "post_id": pid, "backup": arq.name, "trocas": patch["trocas"],
               "modified_antes": meta.get("modified"), "modified_depois": r.get("modified")}, backup)
        saida(f"post {pid}: APLICADO ({len(patch['trocas'])} trocas; backup {arq.name})")
        feitos.append(pid)
    saida(f"\naplicados: {len(feitos)}  pulados: {len(pulados)} {pulados}")
    return {"aplicados": feitos, "pulados": pulados}


def cmd_desfazer(wp, pid, backup=BACKUP, saida=print):
    arq = ultimo_backup(pid, backup)
    if not arq:
        raise SystemExit(f"sem backup para o post {pid} em {backup}")
    dados = json.loads(arq.read_text(encoding="utf-8"))
    r = wp.gravar(pid, dados["raw"])
    logar({"acao": "desfazer", "post_id": pid, "backup": arq.name, "modified_depois": r.get("modified")}, backup)
    saida(f"post {pid}: restaurado de {arq.name}")
    return arq


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    modo = ap.add_mutually_exclusive_group()
    modo.add_argument("--checar", action="store_true", help="padrão: só confere, não escreve")
    modo.add_argument("--aplicar", action="store_true")
    modo.add_argument("--desfazer", type=int, metavar="POST_ID")
    ap.add_argument("--lote", choices=["A", "B", "C"])
    ap.add_argument("--so", type=int, metavar="POST_ID")
    a = ap.parse_args(argv)
    wp = WP()
    if a.desfazer:
        cmd_desfazer(wp, a.desfazer)
        return
    if a.aplicar and not a.lote:
        raise SystemExit("--aplicar exige --lote A|B|C")
    ids = ids_do_lote(a.lote) if a.lote else todos_ids()
    if a.so:
        if a.so not in ids:
            raise SystemExit(f"post {a.so} não está {'no lote ' + a.lote if a.lote else 'nos patches'}")
        ids = [a.so]
    if a.aplicar:
        cmd_aplicar(wp, ids)
    else:
        cmd_checar(wp, ids)


if __name__ == "__main__":
    main()
