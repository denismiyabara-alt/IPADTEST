#!/usr/bin/env python3
"""DETECÇÃO: vídeos de concorrentes que estouraram, normalizados pela idade e pelo próprio canal, só no nicho.

Regra (parâmetros em config.json, bloco "deteccao"):
  múltiplo  = views do vídeo na idade a  ÷  mediana das views dos outros vídeos do MESMO canal e do MESMO formato
              (longo ou Short, corte em short_max_s) quando eles tinham a mesma idade a.
              Como a idade é a mesma, isso é a mesma razão das views por hora.
  outlier   = múltiplo ≥ multiplo_min (3×), views ≥ views_min (3.000), pelo menos historico_min (10) vídeos de
              comparação, idade entre idade_min_h (6 h) e idade_max_h (72 h), e nicho do canal (nichos.dentro,
              sem nichos.fora).

Views de um vídeo de comparação na idade a, em ordem de preferência:
  1. HISTÓRICO: interpolação linear entre duas observações do coletar.py que cercam a idade a (exata);
  2. CURVA (aproximação, enquanto o histórico não cobre a idade): views atuais × g(a) / g(idade atual), com
     g(t) = t / (t + T) e T = curva_meia_vida_h (72 h: metade das views dos primeiros dias chega nas primeiras 72 h).
     Só usa vídeos MAIS VELHOS que a (nunca extrapola para a frente).
  Cada outlier diz qual base usou ("histórico", "curva" ou "misto").

Pontuação (ordena as propostas):
  pontuação = log2(múltiplo) × peso_do_canal
  peso_do_canal = 1 + peso_k × log10(peso_ref_inscritos ÷ inscritos), limitado a [peso_min, peso_max]
  Com k = 0,3 e ref = 500 mil: canal de 20 mil com 10× = 3,32 × 1,42 = 4,7; canal de 2 milhões com 2× = 1 × 0,82 = 0,8.
  O log2 faz 10× valer 3,3 vezes o 2×, e o peso dá até +60% ao canal pequeno (a escala do Denis), até −30% ao grande.
  Inscritos desconhecidos: peso 1.

Adaptadores (quando não há o snapshot do coletar.py):
  - .md do vault (video-radar-AAAA-MM-DD.md): "Score Nx" = views ÷ mediana dos últimos 30 vídeos do canal, SEM idade.
    Aproximação documentada: o múltiplo é o do radar, a idade vem da coluna Dias (dias × 24 h), o mínimo de
    histórico não é verificável (o radar usa 30 vídeos) e views abaixo do mínimo só são cortadas se a tabela tiver Views.
  - JSON do video_radar.py antigo (API): ratio = views ÷ média dos uploads 4 a 20; idade = detail.hours_old.

uso:
  python3 detectar.py [--entrada arquivo] [--agora 2026-10-05T08:00] [--json]
"""
from __future__ import annotations

import argparse
import json
import math
import re
import statistics
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import comum as c


# ------------------------------------------------------------------------------------------------ idade e curva
def horas(a, b):
    return (a - b).total_seconds() / 3600


def g(t, meia_vida):
    return t / (t + meia_vida) if t > 0 else 0.0


def views_na_idade(video, idade_h, agora, meia_vida):
    """(views na idade, 'histórico'|'curva') ou None. idade_h em horas desde a publicação."""
    pub = c.ler_data(video.get("publicado"))
    if pub is None:
        return None
    obs = sorted(((horas(c.ler_data(ts), pub), v) for ts, v in video.get("obs") or [] if c.ler_data(ts)),
                 key=lambda x: x[0])
    for (h0, v0), (h1, v1) in zip(obs, obs[1:]):
        if h0 <= idade_h <= h1:
            if h1 == h0:
                return v1, "histórico"
            return v0 + (v1 - v0) * (idade_h - h0) / (h1 - h0), "histórico"
    if obs and abs(obs[-1][0] - idade_h) <= 1.0:
        return obs[-1][1], "histórico"
    idade_atual = horas(agora, pub)
    if idade_atual < idade_h:
        return None                      # mais novo que a idade de comparação: não serve
    v_atual = video.get("views")
    if v_atual is None:
        return None
    return v_atual * g(idade_h, meia_vida) / g(idade_atual, meia_vida), "curva"


def formato(video, short_max_s):
    d = video.get("duracao_s")
    if d is None:
        return "short" if "#short" in c.norm(video.get("titulo")) else "longo"
    return "short" if d <= short_max_s else "longo"


def peso_canal(inscritos, p):
    if not inscritos:
        return 1.0
    w = 1 + p.get("peso_k", 0.3) * math.log10(p.get("peso_ref_inscritos", 500_000) / max(1, inscritos))
    return max(p.get("peso_min", 0.7), min(p.get("peso_max", 1.6), w))


def pontuacao(multiplo, inscritos, p):
    return round(math.log2(max(multiplo, 1.0)) * peso_canal(inscritos, p), 2)


# ------------------------------------------------------------------------------------------------ snapshot (coletar.py)
def detectar_snapshot(snap, cfg, agora):
    p = cfg["deteccao"]
    regras = cfg["nichos"]
    achados, descartes = [], []
    for ch in snap.get("canais", []):
        vids = ch.get("videos") or []
        for v in vids:
            pub = c.ler_data(v.get("publicado"))
            if pub is None:
                continue
            a = horas(agora, pub)
            if not (p["idade_min_h"] <= a <= p["idade_max_h"]):
                continue
            base = {"video_id": v["video_id"], "titulo": v.get("titulo", ""), "canal": ch.get("nome", ""),
                    "views": v.get("views"), "idade_h": round(a, 1)}
            fmt = formato(v, p["short_max_s"])
            pares = []
            fontes = set()
            for o in vids:
                if o["video_id"] == v["video_id"] or formato(o, p["short_max_s"]) != fmt:
                    continue
                r = views_na_idade(o, a, agora, p["curva_meia_vida_h"])
                if r is not None:
                    pares.append(r[0])
                    fontes.add(r[1])
            if len(pares) < p["historico_min"]:
                descartes.append({**base, "motivo": f"histórico curto: {len(pares)} vídeo(s) de comparação "
                                                    f"(mínimo {p['historico_min']})"})
                continue
            mediana = statistics.median(pares)
            mult = (v.get("views") or 0) / mediana if mediana > 0 else 0.0
            if mult < p["multiplo_min"]:
                continue
            if (v.get("views") or 0) < p["views_min"]:
                descartes.append({**base, "motivo": f"{mult:.1f}×, mas só {v.get('views')} views (mínimo {p['views_min']})"})
                continue
            onde, nicho = c.classificar_nicho(v.get("titulo"), v.get("descricao"), regras)
            if onde == "fora":
                descartes.append({**base, "multiplo": round(mult, 1), "motivo": f"fora do nicho: {nicho}"})
                continue
            achados.append({**base, "channel_id": ch.get("channel_id"), "inscritos": ch.get("inscritos"),
                            "publicado": v.get("publicado"), "descricao": v.get("descricao", ""),
                            "formato": fmt, "nicho": nicho, "multiplo": round(mult, 1),
                            "mediana_mesma_idade": round(mediana), "n_comparacao": len(pares),
                            "base": "histórico" if fontes == {"histórico"} else "curva" if fontes == {"curva"} else "misto",
                            "data_evento": v.get("data_evento"),
                            "pontuacao": pontuacao(mult, ch.get("inscritos"), p),
                            "url": f"https://youtu.be/{v['video_id']}"})
    return achados, descartes


# ------------------------------------------------------------------------------------------------ adaptadores
def _celulas(linha):
    return [x.strip() for x in re.split(r"(?<!\\)\|", linha.strip())[1:-1]]


def _num(s):
    s = re.sub(r"[*\s]", "", str(s or ""))
    m = re.search(r"\d[\d.,]*", s)
    if not m:
        return None
    t = m.group(0)
    if re.fullmatch(r"\d{1,3}([.,]\d{3})+", t):
        return float(re.sub(r"[.,]", "", t))
    return float(t.replace(",", "."))


def ler_md(texto, agora):
    """Tabelas do video-radar-*.md (as colunas mudaram entre as rodadas: acha pelo cabeçalho)."""
    itens, cab = [], None
    data_nota = re.search(r"updated:\s*(\d{4}-\d{2}-\d{2})", texto)
    ref = datetime.fromisoformat(data_nota.group(1) + "T08:00:00+00:00") if data_nota else agora
    for l in texto.splitlines():
        if not l.lstrip().startswith("|"):
            cab = None if not l.strip() else cab
            continue
        cel = _celulas(l)
        low = [c.norm(x) for x in cel]
        if "canal" in low and any(x in low for x in ("titulo", "title")):
            cab = low
            continue
        if cab is None or set("".join(cel)) <= set("-: "):
            continue
        if len(cel) != len(cab):          # título com '|' dentro: junta o excesso no título
            extra = len(cel) - len(cab)
            if extra > 0 and "titulo" in cab:
                i = cab.index("titulo")
                cel = cel[:i] + [" | ".join(cel[i:i + extra + 1])] + cel[i + extra + 1:]
            else:
                continue
        r = dict(zip(cab, cel))
        link = r.get("link", "")
        m = re.search(r"(?:youtu\.be/|v=)([\w-]{6,})", link)
        if not m:
            continue
        dias = _num(r.get("dias"))
        views = _num(r.get("views"))
        itens.append({"video_id": m.group(1), "titulo": r.get("titulo", ""), "canal": r.get("canal", ""),
                      "views": int(views) if views is not None else None, "multiplo": _num(r.get("score")),
                      "idade_h": (dias * 24 + 12) if dias is not None else None,
                      "publicado": c.iso(ref - timedelta(days=dias or 0)) if dias is not None else None,
                      "url": f"https://youtu.be/{m.group(1)}"})
    vistos, out = set(), []
    for it in itens:
        if it["video_id"] not in vistos:
            vistos.add(it["video_id"])
            out.append(it)
    return out


def ler_json_api(lista):
    out = []
    for o in lista:
        det = (o.get("score_breakdown") or {}).get("detail") or {}
        out.append({"video_id": o.get("video_id"), "titulo": o.get("title", ""), "canal": o.get("channel", ""),
                    "channel_id": o.get("channel_id"), "views": o.get("views"), "multiplo": o.get("ratio"),
                    "idade_h": det.get("hours_old") or ((o.get("days_ago") or 0) * 24 + 12),
                    "publicado": o.get("published"), "url": o.get("url")})
    return out


def detectar_aproximado(itens, cfg, base, idade_max_h=None):
    """Para o .md e o JSON antigo: o múltiplo é o do radar (sem a mesma idade). Mesmos cortes de views e nicho."""
    p = cfg["deteccao"]
    idade_max_h = idade_max_h or p["idade_max_h"]
    achados, descartes = [], []
    for it in itens:
        mult = it.get("multiplo") or 0
        if mult < p["multiplo_min"]:
            continue
        if it.get("idade_h") is not None and it["idade_h"] > idade_max_h:
            continue
        if it.get("views") is not None and it["views"] < p["views_min"]:
            descartes.append({**it, "motivo": f"{mult:.1f}×, mas só {it['views']} views (mínimo {p['views_min']})"})
            continue
        onde, nicho = c.classificar_nicho(it.get("titulo"), it.get("descricao"), cfg["nichos"])
        if onde == "fora":
            descartes.append({**it, "motivo": f"fora do nicho: {nicho}"})
            continue
        achados.append({**it, "inscritos": it.get("inscritos"), "descricao": it.get("descricao", ""),
                        "formato": "short" if "#short" in c.norm(it.get("titulo")) else "longo", "nicho": nicho,
                        "multiplo": round(mult, 1), "mediana_mesma_idade": None, "n_comparacao": None,
                        "base": base, "pontuacao": pontuacao(mult, it.get("inscritos"), p)})
    return achados, descartes


# ------------------------------------------------------------------------------------------------ entrada
def detectar(cfg, entrada=None, agora=None):
    agora = agora or datetime.now(timezone.utc)
    arq = c.caminho(entrada) if entrada else c.primeiro_existente(cfg["caminhos"]["entrada_radar"])
    if not arq or not Path(arq).is_file():
        return {"entrada": str(arq) if arq else None, "erro": "não achei a saída do radar", "outliers": [],
                "descartes": []}
    texto = Path(arq).read_text(encoding="utf-8")
    if arq.suffix == ".md":
        # a nota é semanal: a janela de idade vira a da tabela "últimos 7 dias"
        ach, desc = detectar_aproximado(ler_md(texto, agora), cfg,
                                        "aproximação: Nx do radar (views ÷ mediana dos 30 últimos), sem idade",
                                        idade_max_h=8 * 24)
        fonte = "video-radar .md (adaptador)"
    else:
        d = json.loads(texto)
        if isinstance(d, dict) and "canais" in d:
            ach, desc = detectar_snapshot(d, cfg, agora)
            fonte = d.get("fonte", "snapshot")
        else:
            ach, desc = detectar_aproximado(ler_json_api(d if isinstance(d, list) else d.get("outliers", [])), cfg,
                                            "aproximação: ratio do video_radar.py (views ÷ média do canal)")
            fonte = "video_radar.py JSON (adaptador)"
    ach.sort(key=lambda o: (-o["pontuacao"], -o["multiplo"]))
    return {"entrada": str(arq), "fonte": fonte, "agora": c.iso(agora), "outliers": ach, "descartes": desc}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Detecta outliers de concorrentes no nicho do canal.")
    ap.add_argument("--config")
    ap.add_argument("--entrada")
    ap.add_argument("--agora", help="AAAA-MM-DDTHH:MM (UTC se não tiver fuso)")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    cfg = c.carregar_config(a.config)
    agora = c.ler_data(a.agora) if a.agora else None
    r = detectar(cfg, a.entrada, agora)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
        return 0
    print(f"entrada: {r['entrada']} ({r.get('fonte', '?')})")
    if r.get("erro"):
        print("ERRO:", r["erro"])
        return 1
    for o in r["outliers"]:
        print(f"  {o['pontuacao']:>5}  {o['multiplo']}×  [{o['nicho']}] {o['canal']}: {o['titulo']}  ({o['base']})")
    for d in r["descartes"]:
        print(f"  fora: {d['canal']}: {d['titulo']} -> {d['motivo']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
