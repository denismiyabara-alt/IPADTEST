#!/usr/bin/env python3
"""Gera o video_radar_channels.json novo a partir dos candidatos APROVADOS em outliers/canais_candidatos.csv.

O Denis marca a coluna "aprovado" com sim ou não. Este comando:
- monta "channels" só com as linhas "sim" (nome, id, faixa, nicho, inscritos);
- mantém as chaves de topo do JSON atual (outlier_multiplier, window_days, desativados, notas...);
- manda para "desativados" os canais que estavam no JSON e foram marcados "não", com o motivo e a data;
- guarda o JSON antigo ao lado, como video_radar_channels.json.bak-AAAAMMDD-HHMMSS, antes de gravar;
- recusa "sim" sem channel_id (rode descobrir_canais.py no Mac para achar o ID; handle @ nunca, é mutável).

uso:
  python3 canais_aprovados.py --dry-run                 # mostra o que entra, sai e falta; não grava
  python3 canais_aprovados.py [--destino caminho.json]  # padrão: o primeiro de caminhos.canais_radar que existir
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from datetime import datetime
from pathlib import Path

import comum as c
import descobrir_canais as dc

SIM = {"sim", "s", "yes", "y", "x", "ok", "1"}
NAO = {"não", "nao", "n", "no", "0"}


def gerar(linhas, atual, agora=None):
    agora = agora or datetime.now()
    sim = [r for r in linhas if c.norm(r.get("aprovado")) in SIM]
    nao = {r.get("channel_id") for r in linhas if c.norm(r.get("aprovado")) in {c.norm(x) for x in NAO} and r.get("channel_id")}
    sem_id = [r["nome"] for r in sim if not re.fullmatch(r"UC[\w-]{22}", r.get("channel_id") or "")]
    canais = []
    for r in sim:
        if r["nome"] in sem_id:
            continue
        ch = {"name": r["nome"], "id": r["channel_id"], "faixa": (r.get("faixa") or "").split(" ")[0],
              "nicho": r.get("nicho", ""), "origem": "canais_candidatos.csv (aprovado)"}
        if (r.get("inscritos") or "").isdigit():
            ch["inscritos"] = int(r["inscritos"])
        canais.append(ch)
    novo = {k: v for k, v in (atual or {}).items() if k != "channels"}
    desat = list(novo.get("desativados") or [])
    ids_novos = {ch["id"] for ch in canais}
    saem = [ch for ch in (atual or {}).get("channels", []) if ch.get("id") not in ids_novos]
    for ch in saem:
        if ch.get("id") in nao:
            desat.append({**ch, "disabled": True, "motivo": f"reprovado na lista de candidatos em {agora:%d/%m/%Y}"})
    novo["desativados"] = desat
    novo["_nota_aprovacao"] = (f"channels gerado por outliers/canais_aprovados.py em {agora:%d/%m/%Y %H:%M} a partir "
                               "das linhas aprovado=sim de outliers/canais_candidatos.csv.")
    novo["channels"] = canais
    antigos = {ch.get("id") for ch in (atual or {}).get("channels", [])}
    return novo, {"entram": [ch["name"] for ch in canais if ch["id"] not in antigos],
                  "saem": [ch.get("name") for ch in saem], "sem_id": sem_id, "total": len(canais)}


def main(argv=None):
    ap = argparse.ArgumentParser(description="video_radar_channels.json a partir dos candidatos aprovados.")
    ap.add_argument("--config")
    ap.add_argument("--csv", default=str(dc.CSV_PADRAO))
    ap.add_argument("--destino")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    cfg = c.carregar_config(a.config)
    dest = c.caminho(a.destino) if a.destino else c.primeiro_existente(cfg["caminhos"]["canais_radar"])
    if dest is None:
        print("ERRO: não achei o video_radar_channels.json; use --destino", file=sys.stderr)
        return 2
    atual = c.ler_json(dest, {}) or {}
    novo, res = gerar(dc.ler_csv(a.csv), atual)
    print(f"{res['total']} canal(is) aprovado(s) com ID -> {dest}")
    print(f"  entram ({len(res['entram'])}): {', '.join(res['entram']) or '—'}")
    print(f"  saem ({len(res['saem'])}): {', '.join(res['saem']) or '—'}")
    if res["sem_id"]:
        print(f"  ATENÇÃO, aprovados SEM channel_id (ficam de fora): {', '.join(res['sem_id'])}")
    if not res["total"]:
        print("ERRO: nenhum aprovado com ID: o radar não pode ficar vazio. Nada gravado.", file=sys.stderr)
        return 2
    if a.dry_run:
        print("[dry-run] nada gravado.")
        return 0
    if Path(dest).is_file():
        bak = Path(f"{dest}.bak-{datetime.now():%Y%m%d-%H%M%S}")
        shutil.copy2(dest, bak)
        print(f"  antigo guardado em {bak}")
    c.gravar_json(dest, novo)
    print("ok: gravado")
    return 0


if __name__ == "__main__":
    sys.exit(main())
