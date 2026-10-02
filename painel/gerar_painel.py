#!/usr/bin/env python3
"""Painel único diário do Investir e Coçar: CANAL, POSTS, TRADER, SITE e RADAR numa página só.

Só biblioteca padrão. Só LEITURA de arquivos locais (nada é escrito fora de painel/saida/).
Rede só se você pedir: --wp-rest lê os posts recentes na API pública do WordPress (GET, sem login).

uso:
  python3 gerar_painel.py                      gera saida/painel-AAAA-MM-DD.html
  python3 gerar_painel.py --saida-arquivo x.html
  python3 gerar_painel.py --agora 2026-10-05T08:50   (reproduzir um dia; horário de Brasília)
  python3 gerar_painel.py --wp-rest            inclui os 5 posts mais recentes do blog (rede, opcional)

Caminhos (argumento > variável de ambiente > padrão do Mac do Denis). Veja PAINEL.md.
  --ipadtest   PAINEL_IPADTEST   repositório IPADTEST (auditoria-canal, pautas-canal, auditoria-fatos,
                                 links-internos, site-ativos). Padrão: a pasta acima de painel/.
  --iec        PAINEL_IEC        repositório investir-e-cocar.        Padrão: ~/investir-e-cocar
  --trader     PAINEL_TRADER     stock-signal-bot.                     Padrão: ~/stock-signal-bot
  --gate-dir   PAINEL_GATE_DIR   onde ficam gate_<id>.saida.json e gate_estado*.jsonl. Padrão: /tmp
  --radar-json PAINEL_RADAR_JSON card do radar de comentários (--saida do radar). Padrão: /tmp/radar.json
  --backup     PAINEL_BACKUP     auditoria-fatos/backup (log dos patches aplicados). Padrão: <ipadtest>/auditoria-fatos/backup
  --saida      PAINEL_SAIDA      pasta do HTML.                        Padrão: painel/saida
  --max-horas  PAINEL_MAX_HORAS  idade máxima de um dado, em horas úteis (sábado e domingo não contam). Padrão: 36

Saída: 0 = painel gerado (mesmo com blocos sem dado).
"""
from __future__ import annotations

import argparse
import calendar
import csv
import html
import json
import os
import re
import sqlite3
import subprocess
import sys
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
BRT = timezone(timedelta(hours=-3))  # Brasília, sem horário de verão desde 2019
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
DIAS = ["segunda", "terça", "quarta", "quinta", "sexta", "sábado", "domingo"]
WP_BASE = "https://investirecocaresocomecar.com.br"
MAX_ITENS_HOJE = 5
OK, VELHO, SEM = "ok", "velho", "sem"

# Títulos de concorrentes fora do escopo do canal (política), para o radar de vídeos
FORA_ESCOPO_TITULO = re.compile(
    r"\b(lula|bolsonaro|fl[aá]vio|elei[çc][aãoõ]\w*|trump|haddad|stf|moraes|partido|voto|petista)\b", re.I)


# --------------------------------------------------------------------------------------------- utilidades
def num(n, casas=0):
    """Número no formato brasileiro: 165.000 / 3,5."""
    if n is None:
        return "—"
    s = f"{n:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def pct(n, casas=1, sinal=False):
    if n is None:
        return "—"
    s = num(n, casas) + "%"
    return ("+" + s) if sinal and n > 0 else s


def dmy(d):
    if d is None:
        return "—"
    if isinstance(d, datetime):
        d = d.astimezone(BRT)
        return f"{d:%d/%m/%Y}" if (d.hour, d.minute, d.second) == (0, 0, 0) else f"{d:%d/%m/%Y %H:%M}"
    return f"{d:%d/%m/%Y}"


def para_brt(dt):
    if dt is None:
        return None
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=BRT)
    return dt.astimezone(BRT)


def ler_data(texto):
    """Lê '2026-10-02', '2026-10-02T17:19:47', '...Z' ou '+00:00'. Sem fuso = Brasília."""
    if not texto:
        return None
    t = str(texto).strip().replace("Z", "+00:00")
    try:
        if len(t) == 10:
            return datetime.strptime(t, "%Y-%m-%d").replace(tzinfo=BRT)
        return para_brt(datetime.fromisoformat(t))
    except ValueError:
        return None


def mtime(p):
    try:
        return datetime.fromtimestamp(Path(p).stat().st_mtime, BRT)
    except OSError:
        return None


def momento(texto_data, arquivo=None):
    """Data de um JSON; se ela só tem o dia, usa a hora do arquivo quando o arquivo é do mesmo dia."""
    d = ler_data(texto_data)
    if d is not None and texto_data and len(str(texto_data).strip()) == 10 and arquivo:
        m = mtime(arquivo)
        if m and m.date() == d.date():
            return m
    return d if d is not None else (mtime(arquivo) if arquivo else None)


def horas_uteis(desde, ate):
    """Horas entre dois instantes sem contar sábado e domingo (o trader e as exportações não rodam no fim de semana)."""
    desde, ate = para_brt(desde), para_brt(ate)
    if desde >= ate:
        return 0.0
    total, t = 0.0, desde
    while t < ate:
        prox = min(ate, datetime.combine(t.date() + timedelta(days=1), datetime.min.time(), BRT))
        if t.weekday() < 5:
            total += (prox - t).total_seconds() / 3600
        t = prox
    return total


def estado_por_idade(dado_de, agora, max_horas):
    if dado_de is None:
        return SEM
    return VELHO if horas_uteis(dado_de, agora) > max_horas else OK


def ler_json(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return None


def ler_csv(p):
    try:
        with open(p, encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))
    except OSError:
        return None


def inteiro(v, padrao=0):
    try:
        return int(float(v))
    except (TypeError, ValueError):
        return padrao


def real(v):
    try:
        return float(v)
    except (TypeError, ValueError):
        return None


def ultimo_pregao_antes(d):
    """Último dia útil (seg a sex) antes de d. Feriados da B3 não entram: num feriado o painel pode acusar atraso."""
    d = d - timedelta(days=1)
    while d.weekday() >= 5:
        d -= timedelta(days=1)
    return d


def bloco(nome, titulo):
    return {"nome": nome, "titulo": titulo, "estado": SEM, "dado_de": None, "aviso": "", "kpis": [],
            "tabelas": [], "notas": [], "fatos": {}}


# --------------------------------------------------------------------------------------------- CANAL
def bloco_canal(ipadtest, agora, max_horas):
    b = bloco("CANAL", "Canal no YouTube")
    dados = Path(ipadtest) / "auditoria-canal" / "dados"
    pautas = Path(ipadtest) / "pautas-canal"

    leiame = ""
    try:
        leiame = (dados / "LEIAME_DADOS.md").read_text(encoding="utf-8")
    except OSError:
        pass
    m = re.search(r"Exporta[çc][ãa]o:\s*(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}) UTC", leiame)
    exportado = (datetime.fromisoformat(f"{m.group(1)}T{m.group(2)}").replace(tzinfo=timezone.utc).astimezone(BRT)
                 if m else mtime(dados / "canal_por_dia.csv"))
    m = re.search(r"inscritos no contador p[úu]blico:\s*([\d.]+)", leiame)
    inscritos = inteiro(m.group(1).replace(".", "")) if m else None

    dias = ler_csv(dados / "canal_por_dia.csv")
    videos = ler_csv(dados / "videos.csv")
    if not dias and not videos:
        b["aviso"] = f"sem dado: não achei {dados}/canal_por_dia.csv nem videos.csv (rode o exportar.py)"
        b["fatos"]["calendario"] = calendario(pautas, agora)
        _notas_calendario(b)
        return b

    b["dado_de"] = exportado
    b["estado"] = estado_por_idade(exportado, agora, max_horas)
    if inscritos:
        b["kpis"].append(("Inscritos (contador público)", num(inscritos), f"faltam {num(200000 - inscritos)} para 200 mil"))

    if dias:
        dias.sort(key=lambda r: r["dia"])
        ult7, ant7 = dias[-7:], dias[-14:-7]
        # views intencionais (engagedViews): desde 27/08 o contador público infla (auditoria-canal, H1)
        col = "engagedViews" if all((r.get("engagedViews") or "").strip() for r in ult7 + ant7) else "views"
        v7 = sum(inteiro(r[col]) for r in ult7)
        va = sum(inteiro(r[col]) for r in ant7)
        liq7 = sum(inteiro(r["inscritos_ganhos"]) - inteiro(r["inscritos_perdidos"]) for r in ult7)
        var = (v7 / va - 1) * 100 if va else None
        rot = "Views intencionais" if col == "engagedViews" else "Views (contador, inflado desde 27/08)"
        b["kpis"].append((f"{rot} em 7 dias (até {dmy(ler_data(dias[-1]['dia']))})", num(v7),
                          f"{pct(var, 1, True)} contra os 7 anteriores" if var is not None else ""))
        b["kpis"].append(("Inscritos líquidos em 7 dias", num(liq7), "ganhos − perdidos"))
        b["fatos"]["ritmo"] = ritmo_meta(dias, pautas, agora)
        r = b["fatos"]["ritmo"]
        if r:
            b["kpis"].append((r["rotulo"], num(r["feito"]), r["nota"]))
        b["tabelas"].append({
            "titulo": "Últimos dias",
            "cab": ["dia", "views intencionais" if col == "engagedViews" else "views", "ganhos", "perdidos", "líquidos"],
            "linhas": [[dmy(ler_data(x["dia"])), num(inteiro(x[col])), num(inteiro(x["inscritos_ganhos"])),
                        num(inteiro(x["inscritos_perdidos"])),
                        num(inteiro(x["inscritos_ganhos"]) - inteiro(x["inscritos_perdidos"]))] for x in reversed(dias[-5:])],
        })

    if videos:
        analytics = {r["video_id"]: r for r in (ler_csv(dados / "analytics_por_video.csv") or [])}
        r30 = {r["video_id"]: r.get("pct_30s") for r in (ler_csv(dados / "studio" / "retencao_30s.csv") or [])}
        videos.sort(key=lambda r: r.get("publicado_em_utc", ""), reverse=True)
        linhas = []
        for v in videos[:5]:
            a = analytics.get(v["id"], {})
            linhas.append([dmy(ler_data(v.get("publicado_em_brt", "")[:10])), v.get("formato", ""),
                           _curto(v.get("titulo", ""), 70), num(inteiro(v.get("views"))),
                           num(inteiro(a.get("engagedViews"))) if a.get("engagedViews") else "—",
                           pct(real(a.get("averageViewPercentage")), 0) if a.get("averageViewPercentage") else "—",
                           pct(real(r30.get(v["id"])), 0) if r30.get(v["id"]) else "—"])
        b["tabelas"].append({"titulo": "Últimos vídeos", "cab": ["publicado", "formato", "título", "views", "intencionais",
                                                                 "% média assistida", "fica aos 30 s"],
                             "linhas": linhas})
        b["notas"].append("Views = contador público na exportação; desde 27/08 ele infla cerca de 3x nos longos novos, "
                          "então compare vídeos pelas intencionais (Analytics, período todo). Retenção = Analytics (período todo); "
                          "“fica aos 30 s” vem do export do Studio, quando existe. Vídeo novo demais ainda não tem retenção.")

    meta_txt = ""
    try:
        meta_txt = (pautas / "META.md").read_text(encoding="utf-8")
    except OSError:
        pass
    m = re.search(r"os 200 mil em\s+\*\*([a-z]{3}/\d{2})\*\*", meta_txt)
    if m:
        b["notas"].append(f"Meta (META.md): cenário recomendado chega a 200 mil em {m.group(1)}.")
    b["fatos"]["calendario"] = calendario(pautas, agora)
    _notas_calendario(b)
    if b["estado"] == VELHO:
        b["aviso"] = f"dado de {dmy(exportado)}: rode o exportar.py"
    return b


def _curto(t, n):
    t = re.sub(r"\s+", " ", t or "").strip()
    return t if len(t) <= n else t[: n - 1].rstrip() + "…"


def metas_mensais(pautas):
    out = {}
    for r in ler_csv(Path(pautas) / "meta.csv") or []:
        if r.get("tipo") == "mes":
            out[r["periodo"]] = inteiro(r["inscritos_liquidos"])
    return out


def ritmo_meta(dias, pautas, agora):
    """Inscritos líquidos do mês contra o ritmo da meta do mês (meta.csv). Sem dia do mês nos dados: últimos 30 dias."""
    metas = metas_mensais(pautas)
    mes = f"{agora:%Y-%m}"
    meta = metas.get(mes)
    if meta is None or not dias:
        return None
    dias_mes = calendar.monthrange(agora.year, agora.month)[1]
    do_mes = [r for r in dias if r["dia"].startswith(mes)]
    liq = lambda rs: sum(inteiro(r["inscritos_ganhos"]) - inteiro(r["inscritos_perdidos"]) for r in rs)
    if do_mes:
        feito = liq(do_mes)
        esperado = meta * len(do_mes) / dias_mes
        rot = f"Líquidos no mês ({len(do_mes)} dias com dado)"
        nota = f"ritmo da meta: {num(esperado)} até aqui (meta de {MESES[agora.month - 1]}: {num(meta)})"
    else:
        ult = dias[-30:]
        feito = liq(ult)
        esperado = meta * len(ult) / 30
        rot = "Líquidos nos últimos 30 dias"
        nota = f"o mês ainda não tem dado; meta de {MESES[agora.month - 1]}: {num(meta)}"
    prox = metas.get(f"{(agora.replace(day=1) + timedelta(days=32)):%Y-%m}")
    if prox:
        nota += f"; próximo mês: {num(prox)}"
    return {"feito": feito, "esperado": esperado, "meta": meta, "abaixo": feito < esperado, "rotulo": rot, "nota": nota,
            "base": "mes" if do_mes else "30d"}


def calendario(pautas, agora):
    linhas = ler_csv(Path(pautas) / "CALENDARIO-8-SEMANAS.csv")
    if not linhas:
        return None
    hoje = agora.date().isoformat()
    linhas.sort(key=lambda r: r.get("data", ""))
    de_hoje = [r for r in linhas if r.get("data") == hoje]
    futuros = [r for r in linhas if r.get("data", "") > hoje]
    return {"hoje": de_hoje, "proximo": futuros[0] if futuros else None}


def _notas_calendario(b):
    c = b["fatos"].get("calendario")
    if not c:
        b["notas"].append("Calendário: sem dado (não achei pautas-canal/CALENDARIO-8-SEMANAS.csv).")
        return
    for r in c["hoje"]:
        b["kpis"].append(("Vídeo do calendário HOJE", r.get("formato", ""), _curto(r.get("titulo", ""), 90)))
    p = c["proximo"]
    if p:
        b["kpis"].append(("Próximo do calendário", f"{dmy(ler_data(p['data']))} ({p.get('formato', '')})",
                          _curto(p.get("titulo", ""), 90)))
    elif not c["hoje"]:
        b["notas"].append("Calendário: acabou. Hora de montar as próximas 8 semanas.")


# --------------------------------------------------------------------------------------------- POSTS
def aplicados_do_log(backup):
    """{post_id: [trocas da última aplicação]} a partir de backup/log_*.jsonl (desfazer tira o post)."""
    estado = {}
    for arq in sorted(Path(backup).glob("log_*.jsonl")) if Path(backup).is_dir() else []:
        try:
            linhas = arq.read_text(encoding="utf-8").splitlines()
        except OSError:
            continue
        for l in linhas:
            try:
                e = json.loads(l)
            except ValueError:
                continue
            pid = inteiro(e.get("post_id"), None)
            if pid is None:
                continue
            if e.get("acao") == "aplicar":
                estado[pid] = e.get("trocas")
            elif e.get("acao") == "desfazer":
                estado.pop(pid, None)
    return estado


def lotes(pastas, aplicados):
    out = []
    for nome_pasta, pasta in pastas:
        for arq in sorted(Path(pasta).glob("LOTE_*.json")) if Path(pasta).is_dir() else []:
            d = ler_json(arq) or {}
            ids = [inteiro(x) for x in d.get("post_ids", [])]
            feitos = 0
            for pid in ids:
                if pid not in aplicados:
                    continue
                patch = ler_json(Path(pasta) / f"{pid}.json") or {}
                # O mesmo post pode estar num lote de fatos e num de links: só conta se as trocas do log são as deste patch.
                if aplicados[pid] is None or patch.get("trocas") is None or aplicados[pid] == patch.get("trocas"):
                    feitos += 1
            out.append({"lote": d.get("lote") or arq.stem[5:], "pasta": nome_pasta, "total": len(ids),
                        "aplicados": feitos, "pendentes": len(ids) - feitos,
                        "descricao": _curto(d.get("descricao", ""), 90), "mtime": mtime(arq)})
    return out


def saidas_gate(gate_dir):
    """Últimas saídas do gate: gate_<id>.saida.json (--json) e gate_estado*.jsonl (--wp-todos)."""
    g = Path(gate_dir)
    if not g.is_dir():
        return []
    out = []
    for arq in g.glob("gate_*.saida.json"):
        d = ler_json(arq)
        if not isinstance(d, dict) or "resultado" not in d:
            continue
        m = re.match(r"gate_(\d+)\.saida\.json$", arq.name)
        out.append({"tipo": "post", "post_id": m.group(1) if m else arq.stem, "resultado": d.get("resultado"),
                    "titulo": d.get("titulo") or "", "bloqueantes": d.get("bloqueantes", 0), "avisos": d.get("avisos", 0),
                    "codigos": sorted({p.get("codigo", "") for p in d.get("problemas", []) if p.get("nivel") == "BLOQUEANTE"}),
                    "quando": mtime(arq), "arquivo": arq.name})
    for arq in g.glob("gate_estado*.jsonl"):
        cont = {}
        try:
            for l in arq.read_text(encoding="utf-8").splitlines():
                if l.strip():
                    r = json.loads(l).get("resultado", "?")
                    cont[r] = cont.get(r, 0) + 1
        except (OSError, ValueError):
            continue
        out.append({"tipo": "site", "resultado": cont, "quando": mtime(arq), "arquivo": arq.name})
    out.sort(key=lambda x: x["quando"] or datetime.min.replace(tzinfo=BRT), reverse=True)
    return out


def wp_recentes(base=WP_BASE, transporte=None, n=5):
    """Posts recentes pela API pública do WP (só GET, sem credencial). Falha vira None."""
    url = f"{base.rstrip('/')}/wp-json/wp/v2/posts?per_page={n}&_fields=id,date,title"

    def _padrao(u):
        req = urllib.request.Request(u, headers={"User-Agent": "IEC-painel/1.0 (leitura publica)",
                                                 "Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as r:
            return json.loads(r.read().decode("utf-8"))

    try:
        d = (transporte or _padrao)(url)
        return [{"id": p["id"], "data": ler_data(p.get("date")), "titulo": html.unescape(re.sub(r"<[^>]+>", "",
                 (p.get("title") or {}).get("rendered", "")))} for p in d]
    except Exception:  # rede é opcional: qualquer falha só some com a lista
        return None


def bloco_posts(ipadtest, backup, gate_dir, agora, max_horas, wp=None):
    b = bloco("POSTS", "Posts do blog (WordPress)")
    ipadtest = Path(ipadtest)
    aplicados = aplicados_do_log(backup)
    ls = lotes([("auditoria-fatos", ipadtest / "auditoria-fatos" / "patches"),
                ("links-internos", ipadtest / "links-internos" / "patches")], aplicados)
    gate = saidas_gate(gate_dir)
    b["fatos"].update({"lotes": ls, "gate": gate})
    if not ls and not gate and not wp:
        b["aviso"] = "sem dado: não achei os lotes de patches nem saídas do gate"
        return b
    datas = [x["mtime"] for x in ls if x["mtime"]] + [g["quando"] for g in gate if g["quando"]]
    b["dado_de"] = max(datas) if datas else None
    b["estado"] = OK
    if ls:
        pend = sum(x["pendentes"] for x in ls)
        b["kpis"].append(("Patches esperando aplicar (1 por post em cada lote)", num(pend),
                          f"em {sum(1 for x in ls if x['pendentes'])} de {len(ls)} lotes"))
        b["tabelas"].append({"titulo": "Lotes de patches", "cab": ["lote", "pasta", "posts", "aplicados", "pendentes", "o que é"],
                             "linhas": [[x["lote"], x["pasta"], num(x["total"]), num(x["aplicados"]), num(x["pendentes"]),
                                         x["descricao"]] for x in ls]})
        if not Path(backup).is_dir():
            b["notas"].append(f"Sem log de aplicação em {backup}: contei tudo como pendente. "
                              "O aplicar_patches.py grava esse log no Mac.")
    if gate:
        ult = gate[0]["quando"]
        velho = ult is not None and horas_uteis(ult, agora) > max_horas
        linhas = []
        for g in gate[:5]:
            if g["tipo"] == "post":
                linhas.append([dmy(g["quando"]), f"post {g['post_id']}", g["resultado"],
                               f"{g['bloqueantes']} bloq., {g['avisos']} avisos" +
                               (f" ({', '.join(g['codigos'][:3])})" if g["codigos"] else "")])
            else:
                r = g["resultado"]
                linhas.append([dmy(g["quando"]), "site inteiro", "resumo",
                               f"{r.get('BLOQUEADO', 0)} bloqueados, {r.get('AVISOS', 0)} só avisos, {r.get('OK', 0)} OK"])
        b["tabelas"].append({"titulo": "Últimas saídas do gate" + (f" (dado de {dmy(ult)})" if velho else ""),
                             "cab": ["quando", "o quê", "resultado", "detalhe"], "linhas": linhas})
        b["fatos"]["gate_velho"] = velho
    else:
        b["notas"].append(f"Gate: nenhuma saída em {gate_dir} (gate_<id>.saida.json ou gate_estado.jsonl). "
                          "No Mac elas ficam em /tmp e somem ao reiniciar.")
    if wp is not None:
        if wp:
            b["tabelas"].append({"titulo": "Posts recentes no site (API pública)", "cab": ["data", "id", "título"],
                                 "linhas": [[dmy(p["data"]), str(p["id"]), _curto(p["titulo"], 80)] for p in wp]})
        else:
            b["notas"].append("API pública do WordPress: sem resposta agora (opcional).")
    return b


# --------------------------------------------------------------------------------------------- TRADER
def bloco_trader(trader, agora, max_horas):
    b = bloco("TRADER", "Trader (stock-signal-bot) — SIMULAÇÃO")
    t = Path(trader)
    swing = ler_json(t / "swing_v2_resultado.json")
    puts = ler_json(t / "radar_puts_resultado.json")
    longo = ler_json(t / "carteira_longo_resultado.json")
    papel = ler_json(t / "ai_portfolio.json")
    if not any(isinstance(x, dict) for x in (swing, puts, longo, papel)):
        b["aviso"] = f"sem dado: não achei os JSON do trader em {t}"
        return b
    momentos = []
    if isinstance(swing, dict):
        momentos.append(momento(swing.get("gerado_em"), t / "swing_v2_resultado.json"))
    if isinstance(puts, dict):
        momentos.append(momento(puts.get("gerado_em"), t / "radar_puts_resultado.json"))
    if isinstance(longo, dict):
        momentos.append(momento(longo.get("gerado_em"), t / "carteira_longo_resultado.json"))
    momentos = [m for m in momentos if m]
    b["dado_de"] = min(momentos) if momentos else None
    b["estado"] = estado_por_idade(b["dado_de"], agora, max_horas) if momentos else SEM

    sinais = []
    if isinstance(swing, dict):
        sinais = swing.get("sinais_hoje") or []
        setups = swing.get("setups") or {}
        lib = sum(1 for s in setups.values() if isinstance(s, dict) and (s.get("fora_da_amostra") or {}).get("liberado"))
        b["kpis"].append(("Swing v2: sinais registrados hoje", num(len(sinais)),
                          f"{lib} de {len(setups)} setups liberados no teste fora da amostra"))
        if sinais:
            b["tabelas"].append({"titulo": "Sinais do dia (simulação: o bot registrou, ninguém executou)",
                                 "cab": ["data do sinal", "ativo", "setup", "fechamento"],
                                 "linhas": [[dmy(ler_data(s.get("data_sinal"))), s.get("ticker", ""), s.get("setup", ""),
                                             num(real(s.get("fechamento")), 2)] for s in sinais[:10]]})
    n_puts = 0
    if isinstance(puts, dict):
        n_puts = inteiro(puts.get("n_aprovadas_total"))
        b["kpis"].append(("Radar de puts: aprovadas pelos filtros", num(n_puts),
                          f"prêmio: {puts.get('fonte_cotacoes', '?')}; reprovadas: {num(inteiro(puts.get('n_reprovadas')))}"))
    entram, saem, aviso_reb = [], [], ""
    if isinstance(longo, dict):
        reb = longo.get("rebalanceamento") or {}
        entram, saem, aviso_reb = reb.get("entram") or [], reb.get("saem") or [], reb.get("aviso") or ""
        b["kpis"].append(("Carteira de longo prazo (estudo)", f"{len(longo.get('carteira') or [])} ações",
                          (aviso_reb + " " if aviso_reb else "") + f"entram {len(entram)}, saem {len(saem)}"))
    if isinstance(papel, dict):
        nav = (papel.get("nav_history") or [{}])[-1]
        cap = real(papel.get("capital_inicial_brl"))
        v = real(nav.get("nav"))
        var = (v / cap - 1) * 100 if v and cap else None
        trades = papel.get("trade_log") or []
        ult_trade = ler_data((trades[-1].get("ts") or "")[:19]) if trades else None
        b["kpis"].append((f"Carteira de papel (paper trading) em {dmy(ler_data(nav.get('date')))}",
                          f"R$ {num(v, 2)}" if v else "—",
                          f"{pct(var, 1, True)} desde o início (R$ {num(cap)}); {len(papel.get('positions') or {})} posições; "
                          f"última operação simulada: {dmy(ult_trade)}"))
    novo_reb = bool(entram or saem) and "hoje" in aviso_reb.lower()
    b["fatos"].update({"sinais": len(sinais), "puts": n_puts, "rebalanceou": novo_reb,
                       "entram": len(entram), "saem": len(saem)})
    b["notas"].append("Tudo aqui é simulação: nenhuma ordem é criada ou enviada e nada disto é recomendação. "
                      "Detalhe no placar.html do bot.")
    if b["estado"] == VELHO:
        b["aviso"] = f"dado de {dmy(b['dado_de'])}: o rodar_trader_novo.sh não rodou desde então"
    return b


# --------------------------------------------------------------------------------------------- SITE
def bloco_site(ipadtest, agora, max_horas, db=None):
    b = bloco("SITE", "Site de ativos (iec-ativos)")
    s = Path(ipadtest) / "site-ativos"
    rel = ler_json(s / "saida" / "_relatorio.json")
    paginas = ler_csv(s / "saida" / "paginas.csv")
    if not isinstance(rel, dict) and not paginas:
        b["aviso"] = f"sem dado: não achei {s}/saida/_relatorio.json (rode python3 -m iec_ativos tudo)"
        return b
    gerado = momento((rel or {}).get("gerado_em"), s / "saida" / "_relatorio.json") if isinstance(rel, dict) \
        else mtime(s / "saida" / "paginas.csv")
    b["dado_de"] = gerado
    b["estado"] = estado_por_idade(gerado, agora, max_horas)
    pags = (rel or {}).get("paginas") or []
    total = len(paginas) if paginas else len(pags)
    idx = sum(1 for p in paginas if p.get("indexavel") == "sim") if paginas else sum(1 for p in pags if p.get("indexavel"))
    b["kpis"].append(("Última geração", dmy(gerado), ""))
    b["kpis"].append(("Páginas geradas", num(total), f"{num(idx)} indexáveis"))
    nao = (rel or {}).get("nao_geradas") or []
    if nao:
        b["kpis"].append(("Não geradas (bloqueio na validação)", num(len(nao)), ""))
    cot = cotahist_ate(db or (s / "cache" / "dados.sqlite"))
    esperado = ultimo_pregao_antes(agora.date())
    if cot is None:
        b["kpis"].append(("COTAHIST (preços da B3)", "sem dado", "não achei cache/dados.sqlite"))
        b["fatos"]["cotahist_atrasado"] = None
    else:
        atrasado = cot < esperado
        b["kpis"].append(("COTAHIST (preços da B3) até", dmy(cot),
                          ("ATRASADO: " if atrasado else "em dia: ") + f"último pregão esperado {dmy(esperado)}"))
        b["fatos"]["cotahist_atrasado"] = atrasado
        b["fatos"]["cotahist_ate"] = cot
    b["notas"].append("O pregão esperado ignora feriados da B3: num dia depois de feriado o aviso pode ser falso.")
    if b["estado"] == VELHO:
        b["aviso"] = f"dado de {dmy(gerado)}"
    return b


def cotahist_ate(db):
    if not Path(db).is_file():
        return None
    try:
        con = sqlite3.connect(f"file:{db}?mode=ro", uri=True)
        try:
            r = con.execute("select max(data) from preco_diario").fetchone()
        finally:
            con.close()
        return date.fromisoformat(r[0]) if r and r[0] else None
    except (sqlite3.Error, ValueError):
        return None


# --------------------------------------------------------------------------------------------- RADAR
def ler_card_radar(p):
    """Card do radar_comentarios.py (--saida): nome + desc em markdown. Devolve [(tema, pessoas)] e se é 'pouca dúvida'."""
    d = ler_json(p)
    if not isinstance(d, dict) or "desc" not in d:
        return None
    desc = d.get("desc") or ""
    top = [(t.strip(), inteiro(n)) for t, n in re.findall(r"^### \d+\. (.+?) — (\d+) pessoas? pergunt", desc, re.M)]
    pouca = "pouca dúvida" in (d.get("name") or "").lower()
    if not top:
        top = [(t.strip(), inteiro(n)) for t, n in re.findall(r"^- \*\*(.+?)\*\* — (\d+) pessoas? pergunt", desc, re.M)]
    base = re.search(r"Base: (\d+) comentários de (\d+) canais", desc)
    return {"nome": d.get("name", ""), "top": top, "pouca": pouca,
            "base": (inteiro(base.group(1)), inteiro(base.group(2))) if base else None}


def ler_video_radar(iec):
    """Último vault/Concorrentes/video-radar-AAAA-MM-DD.md (vídeos de concorrentes acima da média). Lê do disco;
    se não houver no disco, lê do git (git show), sem mexer no checkout do vault."""
    pasta = Path(iec) / "vault" / "Concorrentes"
    arqs = sorted(pasta.glob("video-radar-*.md")) if pasta.is_dir() else []
    texto, nome = None, None
    if arqs:
        nome = arqs[-1].name
        try:
            texto = arqs[-1].read_text(encoding="utf-8")
        except OSError:
            texto = None
    elif (Path(iec) / ".git").exists():
        try:
            ls = subprocess.run(["git", "-C", str(iec), "ls-tree", "--name-only", "HEAD", "vault/Concorrentes/"],
                                capture_output=True, text=True, timeout=20).stdout.split()
            cand = sorted(x for x in ls if re.search(r"video-radar-\d{4}-\d{2}-\d{2}\.md$", x))
            if cand:
                nome = Path(cand[-1]).name
                texto = subprocess.run(["git", "-C", str(iec), "show", f"HEAD:{cand[-1]}"],
                                       capture_output=True, text=True, timeout=20).stdout
        except (OSError, subprocess.SubprocessError):
            texto = None
    if not texto:
        return None
    m = re.search(r"video-radar-(\d{4}-\d{2}-\d{2})", nome or "")
    quando = ler_data(m.group(1)) if m else None
    itens = []
    for l in texto.splitlines():
        c = [x.strip() for x in l.strip().strip("|").split("|")]
        if len(c) >= 9 and c[0].isdigit():
            titulo = " | ".join(c[6:-2])
            if FORA_ESCOPO_TITULO.search(titulo):
                continue
            itens.append({"score": c[1].strip("*"), "canal": c[5], "titulo": titulo, "link": c[-1]})
    return {"quando": quando, "itens": itens, "arquivo": nome}


def bloco_radar(radar_json, iec, agora, max_horas):
    b = bloco("RADAR", "Radar de pautas")
    card = ler_card_radar(radar_json) if radar_json else None
    vr = ler_video_radar(iec) if iec else None
    if not card and not vr:
        b["aviso"] = (f"sem dado: não achei o card do radar ({radar_json}) nem o video-radar no vault. "
                      "Rode: python3 pipeline/radar_comentarios.py --saida /tmp/radar.json")
        return b
    datas = []
    if card:
        q = mtime(radar_json)
        datas.append(q)
        fresco = q is not None and horas_uteis(q, agora) <= max_horas
        b["fatos"]["card"] = {**card, "fresco": fresco}
        if card["top"]:
            b["tabelas"].append({
                "titulo": ("Dúvidas dos comentários" + (" (semana com pouca dúvida, sem ranking)" if card["pouca"] else "")
                           + f" — card de {dmy(q)}"),
                "cab": ["#", "tema", "pessoas"],
                "linhas": [[str(i), t, num(n)] for i, (t, n) in enumerate(card["top"][:5], 1)]})
        else:
            b["notas"].append(f"Radar de comentários ({dmy(q)}): nenhum tema com pergunta suficiente.")
        if card["base"]:
            b["notas"].append(f"Base do radar: {num(card['base'][0])} comentários de {card['base'][1]} canais. "
                              "Fora do escopo: dívida pessoal, cartão e política.")
    else:
        b["notas"].append(f"Radar de comentários: sem card em {radar_json} (ele roda às segundas e grava com --saida).")
    if vr:
        datas.append(vr["quando"])
        b["fatos"]["video_radar"] = vr
        b["tabelas"].append({"titulo": f"Vídeos de concorrentes acima da média — {vr['arquivo']}",
                             "cab": ["score", "canal", "título"],
                             "linhas": [[x["score"], x["canal"], _curto(x["titulo"], 80)] for x in vr["itens"][:5]]})
        b["notas"].append("Títulos sobre política e eleição ficam de fora (fora do escopo do canal).")
    datas = [d for d in datas if d]
    b["dado_de"] = max(datas) if datas else None
    b["estado"] = estado_por_idade(b["dado_de"], agora, max_horas)
    if b["estado"] == VELHO:
        b["aviso"] = f"dado de {dmy(b['dado_de'])} (o radar de comentários roda 1x por semana)"
    return b


# --------------------------------------------------------------------------------------------- O QUE FAZER HOJE
def o_que_fazer(blocos, agora):
    """Até 5 itens, na ordem de prioridade. Cada item: (bloco, texto)."""
    bl = {b["nome"]: b for b in blocos}
    itens = []
    c = bl.get("CANAL")
    if c:
        cal = c["fatos"].get("calendario") or {}
        for r in cal.get("hoje") or []:
            itens.append(("CANAL", f"Vídeo do calendário para hoje ({r.get('formato', '')}): {_curto(r.get('titulo', ''), 80)}"))
    p = bl.get("POSTS")
    if p:
        for g in p["fatos"].get("gate") or []:
            if g["tipo"] == "post" and g["resultado"] == "BLOQUEADO" and not p["fatos"].get("gate_velho"):
                itens.append(("POSTS", f"Post {g['post_id']} bloqueado no gate: corrigir antes de publicar "
                                       f"({', '.join(g['codigos'][:3]) or 'ver a saída'})."))
                break
        pend = [x for x in p["fatos"].get("lotes") or [] if x["pendentes"]]
        if pend:
            x = pend[0]
            resto = len(pend) - 1
            pasta = "" if x["pasta"] == "auditoria-fatos" else " --pasta ../links-internos/patches"
            itens.append(("POSTS", f"Lote {x['lote']} de patches esperando: {x['pendentes']} posts. Conferir e aplicar "
                                   f"(aplicar_patches.py{pasta} --checar --lote {x['lote']})"
                                   + (f"; mais {resto} lote(s) na fila." if resto else ".")))
    if c and c["estado"] == OK:
        r = c["fatos"].get("ritmo")
        if r and r["abaixo"]:
            base = "no mês" if r["base"] == "mes" else "nos últimos 30 dias"
            itens.append(("CANAL", f"Inscritos abaixo do ritmo da meta: {num(r['feito'])} líquidos {base}, "
                                   f"contra {num(r['esperado'])} pedidos (meta do mês: {num(r['meta'])})."))
    t = bl.get("TRADER")
    if t and t["estado"] == OK:
        f = t["fatos"]
        partes = []
        if f.get("sinais"):
            partes.append(f"{f['sinais']} sinal(is) de swing")
        if f.get("puts"):
            partes.append(f"{f['puts']} put(s) aprovada(s) no radar")
        if f.get("rebalanceou"):
            partes.append(f"rebalanceamento da carteira de estudo (entram {f['entram']}, saem {f['saem']})")
        if partes:
            itens.append(("TRADER", "Trader registrou: " + "; ".join(partes) + ". Só olhar: é simulação."))
    elif t and t["estado"] == VELHO:
        itens.append(("TRADER", f"Trader sem rodada nova desde {dmy(t['dado_de'])}: ver o log do launchd."))
    for nome, cmd in (("CANAL", "rodar o exportar.py"), ("SITE", "rodar python3 -m iec_ativos tudo")):
        b = bl.get(nome)
        if b and b["estado"] == VELHO:
            itens.append((nome, f"Dado do {nome.lower()} velho (de {dmy(b['dado_de'])}): {cmd}."))
    s = bl.get("SITE")
    if s and s["fatos"].get("cotahist_atrasado") and s["estado"] == OK:
        itens.append(("SITE", f"COTAHIST parado em {dmy(s['fatos']['cotahist_ate'])}: atualizar os preços do site "
                              "(python3 -m iec_ativos tudo)."))
    rd = bl.get("RADAR")
    if rd:
        card = rd["fatos"].get("card")
        if card and card["fresco"] and card["top"] and not card["pouca"]:
            tema, n = card["top"][0]
            itens.append(("RADAR", f"Dúvida nº 1 do radar: {tema} ({n} pessoas). Vale pauta?"))
    return itens[:MAX_ITENS_HOJE]


# --------------------------------------------------------------------------------------------- HTML
CSS = """
:root{--bg:#f6f7f9;--card:#fff;--tx:#1b1f24;--mu:#5d6670;--bd:#e3e6ea;--ac:#0b6bcb;--ok:#1a7f37;--ok-bg:#e6f4ea;
--warn:#9a6700;--warn-bg:#fff4d6;--bad:#b42318;--bad-bg:#fde8e7;--hl:#eef4fc}
@media (prefers-color-scheme:dark){:root{--bg:#0f1216;--card:#181c22;--tx:#e6e9ed;--mu:#9aa4ae;--bd:#2b313a;--ac:#5ea8ff;
--ok:#56d364;--ok-bg:#12261a;--warn:#e3b341;--warn-bg:#2b230f;--bad:#ff7b72;--bad-bg:#2d1615;--hl:#16243a}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--tx);font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif}
main{max-width:980px;margin:0 auto;padding:16px}
h1{font-size:1.4rem;margin:.2rem 0}h2{font-size:1.1rem;margin:0}h3{font-size:.95rem;margin:1rem 0 .4rem;color:var(--mu)}
.sub{color:var(--mu);font-size:.9rem;margin:0 0 1rem}
.card{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:16px;margin:0 0 16px}
.hoje{border-color:var(--ac);background:var(--hl)}.hoje ol{margin:.5rem 0 0;padding-left:1.3rem}.hoje li{margin:.35rem 0}
.tag{display:inline-block;font-size:.72rem;font-weight:600;letter-spacing:.03em;padding:1px 7px;border-radius:999px;
border:1px solid var(--bd);color:var(--mu);margin-right:6px;vertical-align:1px}
.cab{display:flex;flex-wrap:wrap;gap:8px;align-items:center;justify-content:space-between}
.st{font-size:.78rem;font-weight:600;padding:2px 9px;border-radius:999px;white-space:nowrap}
.st.ok{color:var(--ok);background:var(--ok-bg)}.st.velho{color:var(--warn);background:var(--warn-bg)}
.st.sem{color:var(--bad);background:var(--bad-bg)}
.aviso{margin:.6rem 0 0;padding:8px 10px;border-radius:8px;background:var(--warn-bg);color:var(--warn);font-size:.9rem}
.aviso.sem{background:var(--bad-bg);color:var(--bad)}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:10px;margin-top:12px}
.kpi{border:1px solid var(--bd);border-radius:10px;padding:10px}
.kpi .r{font-size:.8rem;color:var(--mu)}.kpi .v{font-size:1.25rem;font-weight:650;font-variant-numeric:tabular-nums;
overflow-wrap:anywhere}.kpi .n{font-size:.8rem;color:var(--mu)}
.tw{overflow-x:auto;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%;font-size:.88rem}
th,td{text-align:left;padding:6px 8px;border-bottom:1px solid var(--bd);vertical-align:top}
th{color:var(--mu);font-weight:600;white-space:nowrap}td{font-variant-numeric:tabular-nums}
.notas{margin:.8rem 0 0;padding-left:1.1rem;color:var(--mu);font-size:.83rem}
.sim{display:inline-block;background:var(--warn-bg);color:var(--warn);font-weight:700;font-size:.75rem;padding:2px 8px;
border-radius:6px;letter-spacing:.04em}
footer{color:var(--mu);font-size:.8rem;text-align:center;padding:8px 0 24px}
@media (max-width:520px){body{font-size:15px}main{padding:12px}.card{padding:12px}.kpis{grid-template-columns:1fr 1fr}
.kpi .v{font-size:1.05rem}}
"""

ROTULO_ESTADO = {OK: "em dia", VELHO: "dado velho", SEM: "sem dado"}


def e(t):
    return html.escape(str(t if t is not None else ""), quote=True)


def html_bloco(b):
    p = [f'<section class="card" id="{e(b["nome"].lower())}">',
         f'<div class="cab"><h2><span class="tag">{e(b["nome"])}</span>{e(b["titulo"])}</h2>'
         f'<span class="st {b["estado"]}">{ROTULO_ESTADO[b["estado"]]}'
         + (f' · {e(dmy(b["dado_de"]))}' if b["dado_de"] else "") + "</span></div>"]
    if b["nome"] == "TRADER" and b["estado"] != SEM:
        p.append('<p style="margin:.5rem 0 0"><span class="sim">SIMULAÇÃO</span> nada aqui é ordem real nem recomendação</p>')
    if b["aviso"]:
        p.append(f'<p class="aviso {"sem" if b["estado"] == SEM else ""}">{e(b["aviso"])}</p>')
    if b["kpis"]:
        p.append('<div class="kpis">')
        for r, v, n in b["kpis"]:
            p.append(f'<div class="kpi"><div class="r">{e(r)}</div><div class="v">{e(v)}</div>'
                     + (f'<div class="n">{e(n)}</div>' if n else "") + "</div>")
        p.append("</div>")
    for t in b["tabelas"]:
        p.append(f'<h3>{e(t["titulo"])}</h3><div class="tw"><table><thead><tr>'
                 + "".join(f"<th>{e(c)}</th>" for c in t["cab"]) + "</tr></thead><tbody>")
        for l in t["linhas"]:
            p.append("<tr>" + "".join(f"<td>{e(c)}</td>" for c in l) + "</tr>")
        p.append("</tbody></table></div>")
    if b["notas"]:
        p.append('<ul class="notas">' + "".join(f"<li>{e(n)}</li>" for n in b["notas"]) + "</ul>")
    p.append("</section>")
    return "\n".join(p)


def montar_html(blocos, itens, agora):
    dia = f"{DIAS[agora.weekday()]}, {agora:%d}/{agora:%m}/{agora:%Y}"
    hoje = ['<section class="card hoje"><h2>O que fazer hoje</h2>']
    if itens:
        hoje.append("<ol>" + "".join(f'<li><span class="tag">{e(n)}</span>{e(t)}</li>' for n, t in itens) + "</ol>")
    else:
        hoje.append('<p class="sub" style="margin:.4rem 0 0">Nada urgente pelas regras do painel.</p>')
    hoje.append("</section>")
    return f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="color-scheme" content="light dark">
<title>Painel diário {agora:%d/%m/%Y}</title>
<style>{CSS}</style></head>
<body><main>
<h1>Painel do dia</h1>
<p class="sub">{e(dia)} · gerado às {agora:%H:%M} (Brasília) · Investir e Coçar</p>
{"".join(hoje)}
{chr(10).join(html_bloco(b) for b in blocos)}
<footer>Gerado por painel/gerar_painel.py, só com leitura de arquivos locais. Dado com mais de 36 horas úteis aparece como “dado velho”.</footer>
</main></body></html>
"""


# --------------------------------------------------------------------------------------------- main
def config(argv=None, env=None):
    env = os.environ if env is None else env
    home = Path.home()
    ap = argparse.ArgumentParser(description="Gera o painel único diário (HTML estático).")
    ap.add_argument("--ipadtest", default=env.get("PAINEL_IPADTEST") or str(AQUI.parent))
    ap.add_argument("--iec", default=env.get("PAINEL_IEC") or str(home / "investir-e-cocar"))
    ap.add_argument("--trader", default=env.get("PAINEL_TRADER") or str(home / "stock-signal-bot"))
    ap.add_argument("--gate-dir", default=env.get("PAINEL_GATE_DIR") or "/tmp")
    ap.add_argument("--radar-json", default=env.get("PAINEL_RADAR_JSON") or "/tmp/radar.json")
    ap.add_argument("--backup", default=env.get("PAINEL_BACKUP"))
    ap.add_argument("--saida", default=env.get("PAINEL_SAIDA") or str(AQUI / "saida"))
    ap.add_argument("--saida-arquivo", help="caminho exato do HTML (senão: <saida>/painel-AAAA-MM-DD.html)")
    ap.add_argument("--max-horas", type=float, default=float(env.get("PAINEL_MAX_HORAS") or 36))
    ap.add_argument("--agora", help="AAAA-MM-DDTHH:MM em Brasília (padrão: agora)")
    ap.add_argument("--wp-rest", action="store_true", default=env.get("PAINEL_WP_REST") == "1",
                    help="lê os posts recentes na API pública do WordPress (rede; opcional)")
    ap.add_argument("--wp-base", default=env.get("PAINEL_WP_BASE") or WP_BASE)
    a = ap.parse_args(argv)
    a.backup = a.backup or str(Path(a.ipadtest) / "auditoria-fatos" / "backup")
    a.agora = para_brt(datetime.fromisoformat(a.agora)) if a.agora else datetime.now(BRT)
    return a


def gerar(a, wp_transporte=None):
    wp = wp_recentes(a.wp_base, wp_transporte) if a.wp_rest else None
    blocos = [
        bloco_canal(a.ipadtest, a.agora, a.max_horas),
        bloco_posts(a.ipadtest, a.backup, a.gate_dir, a.agora, a.max_horas, wp),
        bloco_trader(a.trader, a.agora, a.max_horas),
        bloco_site(a.ipadtest, a.agora, a.max_horas),
        bloco_radar(a.radar_json, a.iec, a.agora, a.max_horas),
    ]
    itens = o_que_fazer(blocos, a.agora)
    return blocos, itens, montar_html(blocos, itens, a.agora)


def main(argv=None):
    a = config(argv)
    blocos, itens, pagina = gerar(a)
    destino = Path(a.saida_arquivo) if a.saida_arquivo else Path(a.saida) / f"painel-{a.agora:%Y-%m-%d}.html"
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text(pagina, encoding="utf-8")
    print(f"painel: {destino}")
    for b in blocos:
        print(f"  {b['nome']:<7} {ROTULO_ESTADO[b['estado']]:<11} {dmy(b['dado_de']) if b['dado_de'] else ''}")
    print(f"  o que fazer hoje: {len(itens)} item(ns)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
