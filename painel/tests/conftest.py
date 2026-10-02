"""Fixtures pequenas: uma árvore falsa com IPADTEST, stock-signal-bot e investir-e-cocar dentro de tmp_path."""
import json
import os
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import gerar_painel as gp  # noqa: E402

# Segunda-feira, 05/10/2026, 8h50 em Brasília
AGORA = datetime(2026, 10, 5, 8, 50, tzinfo=gp.BRT)


def escrever(p, texto):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8")
    return p


def wjson(p, d):
    return escrever(p, json.dumps(d, ensure_ascii=False))


def tocar(p, quando):
    ts = quando.timestamp()
    os.utime(p, (ts, ts))


def montar_canal(raiz, exportado="2026-10-05 10:00", dias_out=0):
    dados = raiz / "auditoria-canal" / "dados"
    escrever(dados / "LEIAME_DADOS.md",
             f"- Exportação: {exportado} UTC (modo: completo)\n- Canal: X, inscritos no contador público: 165000\n")
    linhas = ["dia,views,minutos,inscritos_ganhos,inscritos_perdidos,engagedViews"]
    for d in range(1, 31):
        linhas.append(f"2026-09-{d:02d},1000,500,10,5,400")
    for d in range(1, dias_out + 1):
        linhas.append(f"2026-10-{d:02d},1000,500,30,5,400")
    escrever(dados / "canal_por_dia.csv", "\n".join(linhas) + "\n")
    escrever(dados / "videos.csv",
             "id,titulo,publicado_em_utc,publicado_em_brt,dia_semana,hora,duracao_s,formato,views,likes,comentarios,"
             "tags,descricao_tamanho,thumbnail_url\n"
             "v1,Vídeo novo,2026-10-01 22:00:00,2026-10-01 19:00:00,quinta,19,600,longo,8805,1,1,,1,u\n"
             "v0,Vídeo velho,2026-09-01 22:00:00,2026-09-01 19:00:00,terça,19,30,short,100,1,1,,1,u\n")
    escrever(dados / "analytics_por_video.csv", "video_id,averageViewPercentage\nv1,41.5\n")
    escrever(dados / "studio" / "retencao_30s.csv", "video_id,pct_30s\nv1,70.2\n")
    pautas = raiz / "pautas-canal"
    escrever(pautas / "meta.csv", "tipo,periodo,inscritos_liquidos\nmes,2026-10,573\nmes,2026-11,925\n")
    escrever(pautas / "META.md", "e os 200 mil em\n    **mai/29** (faixa)\n")
    escrever(pautas / "CALENDARIO-8-SEMANAS.csv",
             "data,dia,formato,assunto,titulo\n2026-10-05,seg,short,renda fixa,LCI ou CDB?\n"
             "2026-10-06,ter,longo,renda mensal,ETFs mensais\n")


def montar_posts(raiz):
    for pasta, lote, ids in (("auditoria-fatos", "A", [1, 2]), ("links-internos", "L1", [2, 3, 4])):
        p = raiz / pasta / "patches"
        wjson(p / f"LOTE_{lote}.json", {"lote": lote, "descricao": f"lote {lote}", "post_ids": ids})
        for i in ids:
            wjson(p / f"{i}.json", {"post_id": i, "trocas": [{"de": f"{pasta}-{i}", "para": "x"}]})


def montar_trader(raiz, gerado="2026-10-02", sinais=None, aprovadas=0, aviso_reb="", entram=None):
    t = raiz / "trader"
    wjson(t / "swing_v2_resultado.json", {"gerado_em": gerado, "sinais_hoje": sinais or [],
                                          "setups": {"a": {"fora_da_amostra": {"liberado": bool(sinais)}}, "b": None}})
    wjson(t / "radar_puts_resultado.json", {"gerado_em": gerado, "n_aprovadas_total": aprovadas, "n_reprovadas": 9,
                                            "fonte_cotacoes": "cotahist"})
    wjson(t / "carteira_longo_resultado.json", {"gerado_em": gerado, "carteira": [{}] * 18,
                                                "rebalanceamento": {"aviso": aviso_reb, "entram": entram or [], "saem": []}})
    wjson(t / "ai_portfolio.json", {"paper": True, "capital_inicial_brl": 50000, "positions": {"A": {}, "B": {}},
                                    "trade_log": [{"ts": "2026-09-11T09:03:59.1"}],
                                    "nav_history": [{"date": gerado, "nav": 49640.53}]})
    for f in t.glob("*.json"):
        tocar(f, datetime.fromisoformat(gerado + "T19:15").replace(tzinfo=gp.BRT))
    return t


def montar_site(raiz, gerado="2026-10-05T07:00:00", cotahist="2026-10-02"):
    s = raiz / "site-ativos"
    wjson(s / "saida" / "_relatorio.json", {"gerado_em": gerado, "paginas": [{"indexavel": True}, {"indexavel": False}],
                                            "nao_geradas": []})
    escrever(s / "saida" / "paginas.csv", "url,indexavel,motivo,bytes\na,sim,ok,1\nb,não,x,1\nc,sim,ok,1\n")
    db = s / "cache" / "dados.sqlite"
    db.parent.mkdir(parents=True, exist_ok=True)
    if db.exists():
        db.unlink()
    con = sqlite3.connect(db)
    con.execute("create table preco_diario (ticker text, data text)")
    con.execute("insert into preco_diario values ('PETR4', ?)", (cotahist,))
    con.commit()
    con.close()


CARD = {"name": "Radar de comentários · semana de 05/10", "idList": "", "pos": "top",
        "desc": "**As 3 dúvidas mais pedidas**\n\n### 1. Tesouro Direto — 7 pessoas perguntaram\nCanais: X\n\n"
                "### 2. FIIs — 4 pessoas perguntaram\n\n### 3. Juros e Selic — 3 pessoas perguntaram\n\n"
                "_Base: 812 comentários de 5 canais. Só entram..._"}

VIDEO_RADAR = """---
updated: 2026-10-04
---
| # | Score | Views | Projetada | Base | Canal | Título | Dias | Link |
|---|---|---|---|---|---|---|---|---|
| 1 | **28.2x** | 195,000 | 1 | 1 | Canal A | LULA NÃO É FAVORITO | 4d | https://youtu.be/a |
| 2 | **16.0x** | 12,000 | 1 | 1 | Canal B | PETROBRAS ACHA PETRÓLEO | Entenda | 13d | https://youtu.be/b |
"""


@pytest.fixture
def arvore(tmp_path):
    montar_canal(tmp_path)
    montar_posts(tmp_path)
    montar_trader(tmp_path)
    montar_site(tmp_path)
    radar = wjson(tmp_path / "radar.json", CARD)
    tocar(radar, datetime(2026, 10, 5, 8, 5, tzinfo=gp.BRT))
    escrever(tmp_path / "iec" / "vault" / "Concorrentes" / "video-radar-2026-10-04.md", VIDEO_RADAR)
    return tmp_path


def args(raiz, **extra):
    a = ["--ipadtest", str(raiz), "--iec", str(raiz / "iec"), "--trader", str(raiz / "trader"),
         "--gate-dir", str(raiz / "gate"), "--radar-json", str(raiz / "radar.json"),
         "--saida", str(raiz / "saida"), "--agora", "2026-10-05T08:50"]
    for k, v in extra.items():
        a += [f"--{k.replace('_', '-')}", str(v)]
    return gp.config(a, env={})
