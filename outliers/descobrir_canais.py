#!/usr/bin/env python3
"""Descoberta de canais candidatos para o radar (roda NO MAC, UMA vez; usa a API do YouTube).

1. search.list (type=video, regionCode=BR, relevanceLanguage=pt, últimos 180 dias, 50 resultados) para cada termo que
   mais traz views da Pesquisa ao Denis (auditoria-canal/dados/termos_busca_*.csv e pautas-canal/TERMOS.md):
   trxf11, dividendos mensais, tesouro ipca, lci e lca, fundos imobiliarios e os de --termos. 100 unidades POR BUSCA
   (aceitável só aqui: o radar diário nunca usa search).
2. Opcional, --sugeridos-csv: vídeos de onde vem o tráfego de "Vídeos sugeridos" do canal (coluna video_id) ->
   videos.list (1 unidade por 50) -> canal. O CSV sai do Analytics (ver OUTLIERS.md: o export atual NÃO guarda o
   detalhe; --sugeridos-analytics faz a consulta com o OAuth do auditoria-canal/exportar.py).
3. channels.list (snippet, statistics) em lotes de 50: inscritos, país e descrição.
4. Filtra: país BR (ou sem país), 5 mil+ inscritos, nicho do canal pelas regras de config.json (nome + descrição).
5. Junta no outliers/canais_candidatos.csv: atualiza linha existente (mesmo channel_id, ou mesmo nome sem ID) com os
   inscritos e a faixa medidos, sem tocar na coluna "aprovado"; acrescenta os novos com aprovado vazio.

Custo: termos × 100 + ceil(vídeos sugeridos ÷ 50) + ceil(canais ÷ 50). Com os 10 termos padrão e ~300 canais:
1.000 + 6 ≈ 1.006 unidades (10% da cota diária de 10.000), uma vez só.

uso:
  python3 descobrir_canais.py --dry-run                  # mostra termos e custo, sem rede
  python3 descobrir_canais.py [--termos "x,y"] [--max-termos 10] [--sugeridos-csv sugeridos.csv]
  python3 descobrir_canais.py --sugeridos-analytics      # Analytics (OAuth: YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN)
"""
from __future__ import annotations

import argparse
import csv
import math
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import comum as c

TERMOS_PADRAO = ["trxf11", "dividendos mensais", "tesouro ipca", "lci e lca", "fundos imobiliarios",
                 "fii", "dividendos", "renda passiva", "tesouro direto", "etf dividendos mensais"]
COLUNAS = ["nome", "channel_id", "inscritos", "faixa", "nicho", "link", "fonte_da_descoberta", "aprovado"]
CSV_PADRAO = c.AQUI / "canais_candidatos.csv"


def ler_csv(p):
    if not Path(p).is_file():
        return []
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def gravar_csv(p, linhas):
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUNAS, extrasaction="ignore")
        w.writeheader()
        w.writerows(linhas)


def buscar(yt, termo, desde):
    d = yt.chamar("search", part="snippet", q=termo, type="video", regionCode="BR", relevanceLanguage="pt",
                  maxResults=50, publishedAfter=desde)
    return [it["snippet"]["channelId"] for it in d.get("items", []) if (it.get("snippet") or {}).get("channelId")]


def sugeridos_analytics(desde, ate):
    """Vídeos de outros canais que mandam tráfego de Sugeridos para o canal do Denis (Analytics, top 25 por mês)."""
    sys.path.insert(0, str(c.RAIZ / "auditoria-canal"))
    import exportar  # OAuth e cache do export do canal
    cli = exportar.Cliente(c.AQUI / "estado" / "cache_analytics")
    ids, m = [], desde.replace(day=1)
    while m <= ate:
        fim = (m.replace(day=28) + timedelta(days=4)).replace(day=1) - timedelta(days=1)
        rs = cli.analytics_tabela(startDate=str(m), endDate=str(min(fim, ate)),
                                  dimensions="insightTrafficSourceDetail", metrics="views",
                                  filters="insightTrafficSourceType==RELATED_VIDEO", sort="-views", maxResults=25)
        ids += [r["insightTrafficSourceDetail"] for r in rs]
        m = fim + timedelta(days=1)
    return list(dict.fromkeys(ids))


def descobrir(cfg, yt, termos, sugeridos=(), existentes=(), agora=None):
    agora = agora or datetime.now(timezone.utc)
    desde = c.iso(agora - timedelta(days=180))
    origem = {}
    for t in termos:
        for cid in buscar(yt, t, desde):
            origem.setdefault(cid, set()).add(f"busca API: {t}")
    for it in yt.em_lotes("videos", list(sugeridos), "snippet"):
        cid = (it.get("snippet") or {}).get("channelId")
        if cid:
            origem.setdefault(cid, set()).add("sugeridos do Analytics")
    ids = list(origem) + [r["channel_id"] for r in existentes if r.get("channel_id")]
    canais = {it["id"]: it for it in yt.em_lotes("channels", ids, "snippet,statistics")}
    linhas = {r["channel_id"] or "nome:" + c.norm(r["nome"]): dict(r) for r in existentes}
    por_nome = {c.norm(r["nome"]): k for k, r in linhas.items()}
    novos = 0
    for cid, it in canais.items():
        sn, st = it.get("snippet") or {}, it.get("statistics") or {}
        n = None if st.get("hiddenSubscriberCount") else int(st.get("subscriberCount") or 0)
        nome = sn.get("title", cid)
        onde, nicho = c.classificar_nicho(nome, sn.get("description"), cfg["nichos"])
        chave = cid if cid in linhas else por_nome.get(c.norm(nome))
        medido = {"channel_id": cid, "inscritos": "" if n is None else str(n), "faixa": c.faixa_por_inscritos(n),
                  "link": f"https://www.youtube.com/channel/{cid}"}
        if chave:                                   # já estava (radar, web ou comentários): corrige com o medido
            r = linhas.pop(chave)
            r.update(medido)
            if "conferido na API" not in r.get("fonte_da_descoberta", ""):
                r["fonte_da_descoberta"] = (r.get("fonte_da_descoberta", "") + "; conferido na API").lstrip("; ")
            linhas[cid] = r
            continue
        pais = sn.get("country")
        if (pais and pais != "BR") or n is None or n < 5000 or onde == "fora":
            continue
        linhas[cid] = {"nome": nome, **medido, "nicho": nicho, "aprovado": "",
                       "fonte_da_descoberta": "; ".join(sorted(origem.get(cid, [])))}
        novos += 1
    return list(linhas.values()), novos


def main(argv=None):
    ap = argparse.ArgumentParser(description="Descobre canais candidatos (API do YouTube, uma vez, no Mac).")
    ap.add_argument("--config")
    ap.add_argument("--termos", help="termos extras, separados por vírgula")
    ap.add_argument("--max-termos", type=int, default=10)
    ap.add_argument("--sugeridos-csv", help="CSV com a coluna video_id (vídeos que mandam tráfego de Sugeridos)")
    ap.add_argument("--sugeridos-analytics", action="store_true", help="consulta o Analytics (OAuth) dos últimos 6 meses")
    ap.add_argument("--csv", default=str(CSV_PADRAO))
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args(argv)
    cfg = c.carregar_config(a.config)
    termos = TERMOS_PADRAO + [t.strip() for t in (a.termos or "").split(",") if t.strip()]
    termos = list(dict.fromkeys(termos))[: a.max_termos]
    existentes = ler_csv(a.csv)
    sug = []
    if a.sugeridos_csv:
        sug += [r["video_id"] for r in ler_csv(a.sugeridos_csv) if r.get("video_id")]
    n_ch = len(existentes) + 50 * len(termos)
    custo = 100 * len(termos) + math.ceil(len(sug) / 50) + math.ceil(n_ch / 50)
    if a.dry_run:
        print(f"termos ({len(termos)}): {', '.join(termos)}")
        print(f"custo estimado: {100 * len(termos)} (search) + {math.ceil(len(sug) / 50)} (videos.list dos sugeridos) + "
              f"até {math.ceil(n_ch / 50)} (channels.list) = ~{custo} unidades de 10.000/dia. Nada foi chamado.")
        return 0
    ycfg = cfg.get("youtube") or {}
    chave = c.credencial("YOUTUBE_API_KEY", None, [c.caminho(x) for x in ycfg.get("credenciais", [])])
    if not chave:
        print("ERRO: falta YOUTUBE_API_KEY", file=sys.stderr)
        return 2
    if a.sugeridos_analytics:
        hoje = datetime.now(timezone.utc).date()
        sug += sugeridos_analytics(hoje - timedelta(days=180), hoje)
    yt = c.YouTube(chave)
    linhas, novos = descobrir(cfg, yt, termos, sug, existentes)
    ordem = {"grande": 0, "médio": 1, "pequeno": 2}
    linhas.sort(key=lambda r: (ordem.get(r["faixa"].split(" ")[0], 3), r["nome"].lower()))
    gravar_csv(a.csv, linhas)
    print(f"ok: {len(linhas)} candidatos ({novos} novos) em {a.csv}; {yt.unidades} unidades gastas ({yt.chamadas})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
