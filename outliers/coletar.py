#!/usr/bin/env python3
"""Coleta do radar de outliers pela API do YouTube, SEM search (roda no Mac, que tem a chave e acesso ao YouTube).

Por rodada, para N canais:
- channels.list (statistics) em lotes de 50 ............ ceil(N/50) unidades (inscritos, para o peso da pontuação)
- playlistItems.list da playlist de uploads (UU...) ..... N unidades (1 por canal; até 50 uploads por chamada)
- videos.list (statistics, contentDetails) em lotes de 50  ceil(V/50) unidades, V = vídeos a atualizar

V = os uploads com até `atualizar_ate_dias` dias + os que ainda não estão no histórico (na 1ª rodada, todos).
Com 80 canais e 30 uploads por canal: 1ª rodada ≈ 2 + 80 + 48 = 130 unidades; rodadas seguintes ≈ 2 + 80 + 4 a 8
≈ 86 a 90 unidades. Quatro rodadas por dia ≈ 360 unidades, 3,6% da cota padrão de 10.000 por dia.

Grava:
- outliers/dados/historico.json: as observações (hora, views) de cada vídeo, que dão as views NA MESMA IDADE;
- outliers/dados/radar_snapshot.json: o que o detectar.py lê (canais, inscritos, uploads e as observações).

uso:
  python3 coletar.py                  # canais do video_radar_channels.json (config caminhos.canais_radar)
  python3 coletar.py --completo       # atualiza as views de todos os uploads (≈ 130 unidades com 80 canais)
  python3 coletar.py --canais outro.json --dry-run   # só diz o custo estimado, sem rede
"""
from __future__ import annotations

import argparse
import math
import sys
from datetime import datetime, timedelta, timezone

import comum as c


def canais_ativos(arquivo):
    d = c.ler_json(arquivo, {}) or {}
    out = []
    for ch in d.get("channels", []):
        cid = (ch.get("id") or "").strip()
        if ch.get("disabled") or not (cid.startswith("UC") and len(cid) == 24):
            continue
        out.append({"nome": ch.get("name") or cid, "channel_id": cid})
    return out


def custo_estimado(n_canais, uploads, atualizar):
    lotes_ch = math.ceil(n_canais / 50)
    return {"primeira_rodada": lotes_ch + n_canais + math.ceil(n_canais * uploads / 50),
            "rodada_normal": lotes_ch + n_canais + math.ceil(max(1, atualizar) / 50)}


def coletar(cfg, yt, canais, agora=None, completo=False, historico=None):
    agora = agora or datetime.now(timezone.utc)
    ycfg = cfg.get("youtube") or {}
    n_up = min(50, int(ycfg.get("uploads_por_canal", 30)))
    ate = timedelta(days=float(ycfg.get("atualizar_ate_dias", 14)))
    guardar = timedelta(days=float(ycfg.get("guardar_historico_dias", 60)))
    hist = historico if historico is not None else {"videos": {}}
    hv = hist.setdefault("videos", {})

    inscritos = {}
    for it in yt.em_lotes("channels", [ch["channel_id"] for ch in canais], "statistics"):
        s = it.get("statistics") or {}
        inscritos[it["id"]] = None if s.get("hiddenSubscriberCount") else int(s.get("subscriberCount") or 0)

    uploads, falhas = {}, []
    for ch in canais:
        pl = "UU" + ch["channel_id"][2:]
        try:
            d = yt.chamar("playlistItems", part="snippet,contentDetails", playlistId=pl, maxResults=n_up)
        except Exception as e:  # canal sem playlist ou removido: segue com os outros
            falhas.append((ch["nome"], str(e)[:120]))
            continue
        lista = []
        for it in d.get("items", []):
            sn, cd = it.get("snippet") or {}, it.get("contentDetails") or {}
            vid = cd.get("videoId") or (sn.get("resourceId") or {}).get("videoId")
            pub = cd.get("videoPublishedAt")
            if not vid or not pub:          # privado ou excluído
                continue
            lista.append({"video_id": vid, "titulo": sn.get("title", ""), "descricao": (sn.get("description") or "")[:500],
                          "publicado": pub})
        uploads[ch["channel_id"]] = lista

    precisa = []
    for lista in uploads.values():
        for v in lista:
            pub = c.ler_data(v["publicado"])
            if completo or v["video_id"] not in hv or (pub and agora - pub <= ate):
                precisa.append(v["video_id"])
    stats = {}
    for it in yt.em_lotes("videos", precisa, "statistics,contentDetails"):
        stats[it["id"]] = {"views": int((it.get("statistics") or {}).get("viewCount") or 0),
                           "duracao_s": c.duracao_s((it.get("contentDetails") or {}).get("duration"))}

    ts = c.iso(agora)
    saida = []
    for ch in canais:
        lista = uploads.get(ch["channel_id"])
        if lista is None:
            continue
        vids = []
        for v in lista:
            h = hv.setdefault(v["video_id"], {"canal": ch["channel_id"], "publicado": v["publicado"], "obs": []})
            h["titulo"] = v["titulo"]
            if v["video_id"] in stats:
                h["duracao_s"] = stats[v["video_id"]]["duracao_s"]
                h["obs"].append([ts, stats[v["video_id"]]["views"]])
            if not h["obs"]:
                continue
            vids.append({**v, "views": h["obs"][-1][1], "duracao_s": h.get("duracao_s"), "obs": h["obs"]})
        saida.append({"nome": ch["nome"], "channel_id": ch["channel_id"], "inscritos": inscritos.get(ch["channel_id"]),
                      "videos": vids})

    # poda: vídeo publicado há mais de guardar_historico_dias e que saiu da lista de uploads
    vivos = {v["video_id"] for lista in uploads.values() for v in lista}
    for vid in list(hv):
        pub = c.ler_data(hv[vid].get("publicado"))
        if vid not in vivos and pub and agora - pub > guardar:
            del hv[vid]
    snapshot = {"gerado_em": ts, "fonte": "coletar.py (API: playlistItems + videos, sem search)",
                "unidades_gastas": yt.unidades, "chamadas": yt.chamadas, "falhas": falhas, "canais": saida}
    return snapshot, hist


def main(argv=None):
    ap = argparse.ArgumentParser(description="Coleta do radar de outliers (API do YouTube, sem search).")
    ap.add_argument("--config")
    ap.add_argument("--canais", help="video_radar_channels.json (padrão: caminhos.canais_radar da config)")
    ap.add_argument("--completo", action="store_true", help="atualiza as views de todos os uploads")
    ap.add_argument("--dry-run", action="store_true", help="só imprime o custo estimado (sem rede)")
    a = ap.parse_args(argv)
    cfg = c.carregar_config(a.config)
    arq = c.caminho(a.canais) if a.canais else c.primeiro_existente(cfg["caminhos"]["canais_radar"])
    if not arq or not arq.is_file():
        print("ERRO: não achei o video_radar_channels.json (use --canais)", file=sys.stderr)
        return 2
    canais = canais_ativos(arq)
    if not canais:
        print(f"ERRO: nenhum canal ativo em {arq}: o radar não roda vazio", file=sys.stderr)
        return 2
    ycfg = cfg.get("youtube") or {}
    est = custo_estimado(len(canais), int(ycfg.get("uploads_por_canal", 30)), 5 * len(canais) // 4)
    if a.dry_run:
        print(f"{len(canais)} canais em {arq}. Custo estimado: 1ª rodada {est['primeira_rodada']} unidades; "
              f"rodada normal ~{est['rodada_normal']} unidades (cota padrão: 10.000/dia). Nada foi chamado.")
        return 0
    chave = c.credencial("YOUTUBE_API_KEY", None, [c.caminho(x) for x in ycfg.get("credenciais", [])])
    if not chave:
        print("ERRO: falta YOUTUBE_API_KEY (ambiente ou credentials.env)", file=sys.stderr)
        return 2
    hist_p = c.caminho(cfg["caminhos"]["historico"])
    hist = c.ler_json(hist_p, {"videos": {}})
    snap, hist = coletar(cfg, c.YouTube(chave), canais, completo=a.completo, historico=hist)
    c.gravar_json(hist_p, hist)
    snap_p = c.caminho("outliers/dados/radar_snapshot.json")
    c.gravar_json(snap_p, snap)
    nv = sum(len(ch["videos"]) for ch in snap["canais"])
    print(f"ok: {len(snap['canais'])} canais, {nv} vídeos, {snap['unidades_gastas']} unidades "
          f"({snap['chamadas']}); {len(snap['falhas'])} falha(s) -> {snap_p}")
    for nome, erro in snap["falhas"]:
        print(f"  falhou: {nome}: {erro}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
