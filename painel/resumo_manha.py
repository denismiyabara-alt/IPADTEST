#!/usr/bin/env python3
"""Resumo único da manhã no Telegram: uma mensagem curta, lida em 30 segundos no celular.

Junta o que hoje chega de vários lugares, sem refazer nenhum radar. Só LÊ as saídas que já existem:
- "O que fazer hoje" e os blocos TRADER e RADAR vêm das funções do gerar_painel.py (importadas);
- Trello: cards pendentes nas listas de aprovação (API REST, só GET, TRELLO_KEY e TRELLO_TOKEN);
- milhas: milhas_relatorio.md do milhas_radar.py (só os ⭐ e os novos);
- termômetro: log do termometro_2h.py --auto ou o termometro_historico.jsonl;
- jobs: `launchctl list` (código de saída) e a idade da saída de cada job.

Seções, nesta ordem: Decidir hoje (até 5), Trello, Radares, Jobs. Fonte faltando ou velha vira "sem dado".
Acima de 4096 caracteres (limite do Telegram) a mensagem é cortada e termina com "ver painel".

uso:
  python3 resumo_manha.py --dry-run            imprime a mensagem e NÃO envia
  python3 resumo_manha.py                      envia pelo bot do Telegram
  python3 resumo_manha.py --config outro.json  (padrão: RESUMO_CONFIG ou painel/resumo_manha.json)
  python3 resumo_manha.py --agora 2026-10-05T08:50 --launchctl-arquivo lista.txt --sem-trello

Credenciais (nunca no código nem na config): primeiro o ambiente, depois os arquivos da config, na mesma
ordem do notifier.py do stock-signal-bot. Telegram: TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID (ou
TELEGRAM_HOME_CHANNEL). Trello: TRELLO_KEY e TRELLO_TOKEN.

Saída: 0 = enviado (ou dry-run); 1 = o envio falhou (a mensagem vai para o stdout, e o launchctl
registra o código, que aparece como ❌ no resumo do dia seguinte).
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import urllib.parse
import urllib.request
from datetime import datetime, time, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import gerar_painel as gp  # noqa: E402  (reaproveita os blocos do painel, não copia)

LIMITE_TELEGRAM = 4096
MAX_DECIDIR = 5
SEM_DADO = "sem dado"
CONFIG_PADRAO = AQUI / "resumo_manha.json"
# Mesma ordem de busca do notifier.py: o primeiro arquivo que tiver a chave ganha.
TELEGRAM_ARQUIVOS = ["~/.hermes/.env", "~/.config/investirecocar/credentials.env", "~/.claude/credentials.env"]
CHAT_ID_KEYS = ("TELEGRAM_HOME_CHANNEL", "TELEGRAM_CHAT_ID")
TRELLO_ARQUIVOS = ["~/.config/investirecocar/credentials.env"]
TRELLO_API = "https://api.trello.com/1"
DIAS_CURTOS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]


# --------------------------------------------------------------------------------------------- utilidades
def caminho(p):
    return Path(str(p)).expanduser() if p not in (None, "") else None


def carregar_config(p):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"AVISO: config {p} ilegível ({e}); usando só os padrões", file=sys.stderr)
        return {}


def ler_env_arquivo(p):
    """chave=valor, # comenta (mesmo formato do notifier.py e do credentials.env)."""
    out = {}
    try:
        for linha in Path(p).expanduser().read_text(encoding="utf-8").splitlines():
            linha = linha.strip()
            if "=" in linha and not linha.startswith("#"):
                k, _, v = linha.partition("=")
                k = k.strip()
                if k.startswith("export "):
                    k = k[7:].strip()
                out[k] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    return out


def credencial(nomes, env, arquivos):
    """Primeiro o ambiente, depois os arquivos (o primeiro que tiver ganha). Nunca imprime o valor."""
    nomes = (nomes,) if isinstance(nomes, str) else tuple(nomes)
    for n in nomes:
        if env.get(n):
            return env[n]
    for arq in arquivos:
        d = ler_env_arquivo(arq)
        for n in nomes:
            if d.get(n):
                return d[n]
    return ""


def horas(desde, agora):
    return (agora - desde).total_seconds() / 3600


def quando_curto(dt, agora):
    """'hoje 07:40', 'ontem 19:10' ou 'sex 02/10 19:10'."""
    dt = gp.para_brt(dt)
    if dt.date() == agora.date():
        return f"hoje {dt:%H:%M}"
    if dt.date() == agora.date() - timedelta(days=1):
        return f"ontem {dt:%H:%M}"
    return f"{DIAS_CURTOS[dt.weekday()]} {dt:%d/%m %H:%M}"


def sem_dado(motivo=""):
    return SEM_DADO + (f" ({motivo})" if motivo else "")


# --------------------------------------------------------------------------------------------- painel
def blocos_do_painel(cfg, agora, env):
    """Roda as funções de bloco do gerar_painel.py com os caminhos da config. Um bloco que quebrar vira 'sem dado'."""
    p = cfg.get("painel") or {}
    argv = []
    for chave, opc in (("ipadtest", "--ipadtest"), ("iec", "--iec"), ("trader", "--trader"),
                       ("gate_dir", "--gate-dir"), ("radar_json", "--radar-json"), ("backup", "--backup")):
        if p.get(chave):
            argv += [opc, str(caminho(p[chave]))]
    if p.get("max_horas"):
        argv += ["--max-horas", str(p["max_horas"])]
    a = gp.config(argv, env=env)
    a.agora = agora
    chamadas = [
        ("CANAL", lambda: gp.bloco_canal(a.ipadtest, agora, a.max_horas)),
        ("POSTS", lambda: gp.bloco_posts(a.ipadtest, a.backup, a.gate_dir, agora, a.max_horas, None)),
        ("TRADER", lambda: gp.bloco_trader(a.trader, agora, a.max_horas)),
        ("SITE", lambda: gp.bloco_site(a.ipadtest, agora, a.max_horas)),
        ("RADAR", lambda: gp.bloco_radar(a.radar_json, a.iec, agora, a.max_horas)),
    ]
    blocos = []
    for nome, f in chamadas:
        try:
            blocos.append(f())
        except Exception as e:  # o resumo nunca quebra por causa de um bloco
            b = gp.bloco(nome, nome)
            b["aviso"] = f"sem dado: o bloco falhou ({type(e).__name__})"
            blocos.append(b)
    try:
        itens = gp.o_que_fazer(blocos, agora)
    except Exception:
        itens = []
    return {b["nome"]: b for b in blocos}, itens, a


# --------------------------------------------------------------------------------------------- milhas
def _celulas(linha):
    return [c.strip().replace("\\|", "|") for c in re.split(r"(?<!\\)\|", linha.strip())[1:-1]]


def ler_milhas(cfg_m, agora):
    """milhas_relatorio.md do milhas_radar.py: só os ⭐ e os 'novo' da última rodada."""
    rel = caminho(cfg_m.get("relatorio"))
    max_h = float(cfg_m.get("max_horas", 26))
    if rel is None or not rel.is_file():
        return {"estado": gp.SEM, "motivo": f"não achei {rel}" if rel else "caminho não configurado"}
    try:
        texto = rel.read_text(encoding="utf-8")
    except OSError as e:
        return {"estado": gp.SEM, "motivo": f"não li {rel.name}: {e.strerror}"}
    quando = gp.mtime(rel)
    if quando is None:
        m = re.search(r"Gerado em (\d{2})/(\d{2})/(\d{4}) (\d{2}):(\d{2})", texto)
        if m:  # o milhas_radar.py escreve a hora em UTC
            d, mo, y, h, mi = (int(x) for x in m.groups())
            quando = datetime(y, mo, d, h, mi, tzinfo=timezone.utc).astimezone(gp.BRT)
    if quando is None or horas(quando, agora) > max_h:
        return {"estado": gp.SEM, "motivo": f"relatório de {quando_curto(quando, agora)}" if quando else "sem data"}
    itens = []
    for l in texto.splitlines():
        c = _celulas(l) if l.lstrip().startswith("|") else []
        if len(c) < 10 or c[1] in ("Data", "---", "—"):  # cabeçalho, separador e "nenhum post relevante"
            continue
        marca = c[0]
        m = re.match(r"\[(.*)\]\((.*)\)$", c[3])
        itens.append({"estrela": "⭐" in marca, "novo": "novo" in marca, "titulo": m.group(1) if m else c[3],
                      "link": m.group(2) if m else "", "programa": c[4], "milhas": c[6] if c[6] != "—" else "",
                      "fonte": c[2]})
    relevantes = [x for x in itens if x["titulo"] != "nenhum post relevante"]
    destaque = [x for x in relevantes if x["estrela"] or x["novo"]]
    destaque.sort(key=lambda x: (not x["estrela"], not x["novo"]))
    return {"estado": gp.OK, "quando": quando, "relevantes": len(relevantes), "destaque": destaque,
            "estrelas": sum(1 for x in relevantes if x["estrela"]), "novos": sum(1 for x in relevantes if x["novo"])}


def linhas_milhas(m, agora):
    if m["estado"] != gp.OK:
        return [f"✈️ Milhas: {sem_dado(m.get('motivo', ''))}"]
    if not m["destaque"]:
        return [f"✈️ Milhas: nada novo ({m['relevantes']} relevante(s) no relatório de {quando_curto(m['quando'], agora)})"]
    out = [f"✈️ Milhas: {m['estrelas']} ⭐ e {m['novos']} novo(s)"]
    for x in m["destaque"][:3]:
        mi = f"{x['milhas']} mi · " if x["milhas"] else ""
        out.append(f"  • {'⭐ ' if x['estrela'] else ''}{mi}{gp._curto(x['titulo'], 70)}")
    return out


# --------------------------------------------------------------------------------------------- comentários
def ler_comentarios(bloco_radar, radar_json, cfg_c, agora):
    """Reaproveita o card que o bloco RADAR do painel já leu (radar_comentarios.py --saida)."""
    card = (bloco_radar or {}).get("fatos", {}).get("card")
    if not card:
        return {"estado": gp.SEM, "motivo": f"sem card em {radar_json}"}
    q = gp.mtime(radar_json)
    if q is None:
        return {"estado": gp.SEM, "motivo": "card sem data"}
    h = horas(q, agora)
    if h <= float(cfg_c.get("novas_horas", 24)):
        return {"estado": gp.OK, "novo": True, "quando": q, "top": card["top"], "pouca": card["pouca"]}
    if h <= float(cfg_c.get("max_horas", 192)):
        return {"estado": gp.OK, "novo": False, "quando": q, "top": card["top"], "pouca": card["pouca"]}
    return {"estado": gp.SEM, "motivo": f"card de {quando_curto(q, agora)}"}


def linhas_comentarios(c, agora):
    if c["estado"] != gp.OK:
        return [f"💬 Comentários: {sem_dado(c.get('motivo', ''))}"]
    if not c["novo"]:
        return [f"💬 Comentários: nenhuma pergunta nova (card de {quando_curto(c['quando'], agora)})"]
    if not c["top"]:
        return [f"💬 Comentários: card novo sem tema com pergunta suficiente"]
    temas = ", ".join(f"{t} ({n})" for t, n in c["top"][:3])
    return [f"💬 Comentários{' (pouca dúvida)' if c['pouca'] else ''}: {temas}"]


# --------------------------------------------------------------------------------------------- termômetro
def ler_termometro(cfg_t, agora):
    """Último veredito do termometro_2h.py: do log do --auto (texto pronto) ou do histórico (só números)."""
    max_h = float(cfg_t.get("max_horas", 24))
    log = caminho(cfg_t.get("log"))
    q = gp.mtime(log) if log else None
    if q is not None and horas(q, agora) <= max_h:
        try:
            linhas = log.read_text(encoding="utf-8").splitlines()
        except OSError:
            linhas = []
        inicio = max((i for i, l in enumerate(linhas) if l.startswith("🌡️")), default=None)
        if inicio is not None:
            bloco = linhas[inicio:]
            fim = next((i for i, l in enumerate(bloco) if l.startswith("👉")), len(bloco) - 1)
            bloco = bloco[: fim + 1]
            acao = bloco[-1] if bloco[-1].startswith("👉") else ""
            return {"estado": gp.OK, "quando": q, "titulo": bloco[0].replace("🌡️", "").strip(),
                    "views": next((l for l in bloco if l.startswith("Views")), ""), "acao": acao}
    hist = caminho(cfg_t.get("historico"))
    ult = None
    if hist and hist.is_file():
        try:
            for l in hist.read_text(encoding="utf-8").splitlines():
                try:
                    ult = json.loads(l) if l.strip() else ult
                except ValueError:
                    continue
        except OSError:
            ult = None
    if ult:
        quando = gp.ler_data(ult.get("medido_em"))
        if quando and horas(quando, agora) <= max_h:
            partes = [f"{gp.num(gp.inteiro(ult.get('views')))} views com {gp.num(gp.real(ult.get('horas')) or 0, 1)} h"]
            if ult.get("ctr") is not None:
                partes.append(f"CTR {gp.num(gp.real(ult['ctr']), 1)}%")
            if ult.get("retencao") is not None:
                partes.append(f"retenção {gp.num(gp.real(ult['retencao']), 1)}%")
            return {"estado": gp.OK, "quando": quando, "titulo": f"vídeo {ult.get('video', '?')}",
                    "views": ", ".join(partes), "acao": ""}
        if quando:
            return {"estado": gp.SEM, "motivo": f"última medição {quando_curto(quando, agora)}"}
    return {"estado": gp.SEM, "motivo": "nenhuma medição recente"}


def linhas_termometro(t):
    if t["estado"] != gp.OK:
        return [f"🌡️ Termômetro: {sem_dado(t.get('motivo', ''))}"]
    out = [f"🌡️ Termômetro: {gp._curto(t['titulo'], 60)}" + (f" · {t['views']}" if t["views"] else "")]
    if t["acao"]:
        out.append(f"  {gp._curto(t['acao'], 140)}")
    return out


# --------------------------------------------------------------------------------------------- trader
def linhas_trader(b):
    rot = "📈 Trader [SIMULAÇÃO]"
    if not b or b["estado"] == gp.SEM:
        return [f"{rot}: {sem_dado('não achei os JSON do trader')}"]
    if b["estado"] == gp.VELHO:
        return [f"{rot}: {sem_dado('rodada de ' + gp.dmy(b['dado_de']))}"]
    f = b["fatos"]
    partes = [f"{f.get('sinais', 0)} sinal(is) de swing", f"{f.get('puts', 0)} put(s) aprovada(s)"]
    if f.get("rebalanceou"):
        partes.append(f"rebalanceou (entram {f['entram']}, saem {f['saem']})")
    for r, v, n in b["kpis"]:
        if r.startswith("Carteira de papel") and v != "—":
            var = n.split(" desde")[0] if " desde" in n else ""
            partes.append(f"papel {v}" + (f" ({var})" if var else ""))
    return [f"{rot}, rodada de {gp.dmy(b['dado_de'])}: " + " · ".join(partes)]


# --------------------------------------------------------------------------------------------- Trello
def _trello_get(url, timeout):
    req = urllib.request.Request(url, headers={"Accept": "application/json", "User-Agent": "IEC-resumo-manha/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return r.read().decode("utf-8", errors="replace")


def _data_card(c):
    d = gp.ler_data(c.get("dateLastActivity"))
    if d is None and re.fullmatch(r"[0-9a-f]{24}", c.get("id") or ""):
        d = datetime.fromtimestamp(int(c["id"][:8], 16), gp.BRT)  # o id do Trello começa com a data de criação
    return d


def ler_trello(cfg_t, env, transporte=None):
    """Cards nas listas de aprovação. transporte(url) -> texto (os testes trocam por uma resposta falsa)."""
    listas = [dict(l) for l in (cfg_t.get("listas") or []) if l.get("nome")]
    if not listas:
        return {"estado": gp.SEM, "motivo": "nenhuma lista na config"}
    arquivos = cfg_t.get("credenciais") or TRELLO_ARQUIVOS
    key, token = credencial("TRELLO_KEY", env, arquivos), credencial("TRELLO_TOKEN", env, arquivos)
    if not key or not token:
        return {"estado": gp.SEM, "motivo": "faltam TRELLO_KEY e TRELLO_TOKEN"}
    timeout = float(cfg_t.get("timeout_s", 15))
    get = transporte or (lambda u: _trello_get(u, timeout))
    auth = urllib.parse.urlencode({"key": key, "token": token})

    def pedir(caminho_api, campos):
        texto = get(f"{TRELLO_API}{caminho_api}?fields={campos}&{auth}")
        try:
            return json.loads(texto)
        except ValueError:
            # A API responde "invalid key" em texto puro com HTTP 200 quando a variável está errada.
            raise RuntimeError(f"Trello respondeu {texto.strip()[:40]!r}: confira TRELLO_KEY/TRELLO_TOKEN")

    def limpo(e):
        return str(e).replace(key, "***").replace(token, "***")

    try:
        sem_id = [l for l in listas if not l.get("id")]
        if sem_id and cfg_t.get("board_id"):
            ids = {x.get("name"): x.get("id") for x in pedir(f"/boards/{cfg_t['board_id']}/lists", "name")}
            for l in sem_id:
                l["id"] = ids.get(l["nome"])
        contagem, cards = [], []
        for l in listas:
            if not l.get("id"):
                contagem.append((l["nome"], None))
                continue
            cs = pedir(f"/lists/{l['id']}/cards", "name,dateLastActivity")
            contagem.append((l["nome"], len(cs)))
            cards += [{"nome": c.get("name", ""), "lista": l["nome"], "desde": _data_card(c)} for c in cs]
    except Exception as e:  # rede, HTTP, JSON: vira "sem dado"
        return {"estado": gp.SEM, "motivo": gp._curto(limpo(e), 90)}
    cards.sort(key=lambda c: c["desde"] or datetime.max.replace(tzinfo=gp.BRT))
    return {"estado": gp.OK, "contagem": contagem, "total": sum(n or 0 for _, n in contagem), "antigos": cards[:3]}


def linhas_trello(t, agora):
    if t["estado"] != gp.OK:
        return [f"📋 Trello: {sem_dado(t.get('motivo', ''))}"]
    listas = " · ".join(f"{n} {c if c is not None else '?'}" for n, c in t["contagem"])
    out = [f"📋 Trello: {t['total']} esperando aprovação ({listas})"]
    for c in t["antigos"]:
        idade = f"há {max(0, (agora - c['desde']).days)} d" if c["desde"] else "sem data"
        out.append(f"  • {gp._curto(c['nome'], 60)} ({c['lista']}, {idade})")
    return out


# --------------------------------------------------------------------------------------------- jobs
def rodar_launchctl():
    try:
        r = subprocess.run(["launchctl", "list"], capture_output=True, text=True, timeout=15)
        return r.stdout if r.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def parse_launchctl(texto):
    """`launchctl list`: 'PID<tab>Status<tab>Label'. PID '-' = não está rodando; Status = código da última saída
    (negativo = morto por sinal). Devolve {label: {'pid': int|None, 'status': int|None}}."""
    out = {}
    for l in (texto or "").splitlines():
        partes = l.strip().split(None, 2)
        if len(partes) != 3 or partes[0] == "PID":
            continue
        pid, st, label = partes
        try:
            st_i = int(st)
        except ValueError:
            st_i = None
        out[label.strip()] = {"pid": int(pid) if pid.isdigit() else None, "status": st_i}
    return out


def _dia_vale(dias, d):
    if dias in (None, "todos"):
        return True
    if dias == "uteis":
        return d.weekday() < 5
    lista = [dias] if isinstance(dias, str) else list(dias)
    return DIAS_CURTOS[d.weekday()] in lista or (d.weekday() == 5 and "sab" in lista)


def execucao_esperada(job, agora, tol_min):
    """Último horário agendado cujo prazo (horário + tolerância) já passou. None se o job não tem horário."""
    tol = timedelta(minutes=tol_min)
    if job.get("a_cada_min"):
        return agora - timedelta(minutes=float(job["a_cada_min"])) - tol
    if not job.get("horario"):
        return None
    h, m = (int(x) for x in job["horario"].split(":"))
    for atras in range(0, 9):
        d = agora.date() - timedelta(days=atras)
        t = datetime.combine(d, time(h, m), gp.BRT)
        if _dia_vale(job.get("dias", "todos"), d) and t + tol <= agora:
            return t
    return None


def nome_curto(label, prefixos):
    for p in prefixos:
        if label.startswith(p):
            return label[len(p):]
    return label


def avaliar_jobs(cfg_j, agora, texto_launchctl):
    prefixos = cfg_j.get("prefixos") or ["com.denal.", "com.denis."]
    tol_padrao = float(cfg_j.get("tolerancia_min", 30))
    lc = parse_launchctl(texto_launchctl) if texto_launchctl else None
    esperados = [j for j in (cfg_j.get("esperados") or []) if j.get("label")]
    conhecidos = {j["label"] for j in esperados}
    if lc:
        esperados += [{"label": l} for l in sorted(lc) if l.startswith(tuple(prefixos)) and l not in conhecidos]
    res = []
    for j in esperados:
        label, curto = j["label"], nome_curto(j["label"], prefixos)
        if lc is not None and label not in lc:
            if not j.get("opcional"):
                res.append((curto, False, "não carregado"))
            continue
        if lc is None and (j.get("opcional") or not j.get("saida")):
            continue  # sem launchctl não dá para saber se o job opcional existe, nem o código de quem não tem saída
        st = lc[label]["status"] if lc is not None else None
        if st not in (None, 0):
            res.append((curto, False, f"saiu com {st}"))
            continue
        esp = execucao_esperada(j, agora, float(j.get("tolerancia_min", tol_padrao)))
        if j.get("saida") and esp is not None:
            p = caminho(str(j["saida"]).replace("{data}", f"{esp:%Y-%m-%d}"))
            m = gp.mtime(p)
            if m is None:
                res.append((curto, False, "sem saída"))
                continue
            if m < esp - timedelta(minutes=2):
                rot = f"a cada {j['a_cada_min']} min" if j.get("a_cada_min") else quando_curto(esp, agora)
                res.append((curto, False, f"não rodou {rot}"))
                continue
        res.append((curto, True, ""))
    return {"launchctl": lc is not None, "jobs": res}


def linha_jobs(j):
    if not j["jobs"]:
        return f"⚙️ Jobs: {sem_dado('launchctl indisponível e nenhum job na config')}"
    ruins = [f"❌ {n} ({m})" for n, ok, m in j["jobs"] if not ok]
    bons = [n for n, ok, _ in j["jobs"] if ok]
    partes = ruins + ([f"✅ {', '.join(bons)}"] if bons else [])
    extra = "" if j["launchctl"] else " (sem launchctl: só a idade das saídas)"
    return "⚙️ Jobs: " + " · ".join(partes) + extra


# --------------------------------------------------------------------------------------------- montagem
def decidir_hoje(itens_painel, trello, milhas, termometro, jobs):
    """Até 5 itens. Ordem: 1º do painel, Trello, promo ⭐ nova, job com falha, resto do painel, termômetro."""
    cand = []
    textos = [t for _, t in itens_painel]
    if textos:
        cand.append(textos[0])
    if trello.get("estado") == gp.OK and trello["total"]:
        com = "; ".join(f"{n} {c}" for n, c in trello["contagem"] if c)
        velho = trello["antigos"][0]["desde"] if trello["antigos"] else None
        cand.append(f"Aprovar no Trello: {trello['total']} card(s) ({com})"
                    + (f", o mais antigo de {gp.dmy(velho)[:5]}." if velho else "."))
    if milhas.get("estado") == gp.OK:
        for x in milhas["destaque"]:
            if x["estrela"] and x["novo"]:
                cand.append(f"Promo de milhas ⭐ {x['milhas'] + ' mi: ' if x['milhas'] else ''}{gp._curto(x['titulo'], 70)}")
                break
    ruins = [f"{n} ({m})" for n, ok, m in jobs["jobs"] if not ok]
    if ruins:
        cand.append("Job com problema: " + ", ".join(ruins[:3]) + ". Ver o log.")
    cand += textos[1:]
    if termometro.get("estado") == gp.OK and termometro.get("acao") and "não mexer" not in termometro["acao"] \
            and "Sem base" not in termometro["acao"]:
        cand.append("Termômetro: " + termometro["acao"].replace("👉", "").strip())
    return [gp._curto(c, 170) for c in cand[:MAX_DECIDIR]]


def tamanho_telegram(s):
    """O Telegram conta em unidades UTF-16 (emoji fora do BMP vale 2)."""
    return len(s.encode("utf-16-le")) // 2


def cortar(texto, limite=LIMITE_TELEGRAM, ref_painel=""):
    if tamanho_telegram(texto) <= limite:
        return texto
    sufixo = "\n…\n✂️ Cortado: ver painel" + (f" ({ref_painel})" if ref_painel else "")
    linhas = texto.split("\n")
    while linhas and tamanho_telegram("\n".join(linhas) + sufixo) > limite:
        linhas.pop()
    corpo = "\n".join(linhas)
    if not corpo:  # uma linha gigante: corta no caractere
        corpo = texto
        while tamanho_telegram(corpo + sufixo) > limite:
            corpo = corpo[: -max(1, (tamanho_telegram(corpo + sufixo) - limite))]
    return corpo + sufixo


def coletar(cfg, agora, env=None, ler_launchctl=rodar_launchctl, trello_transporte=None, usar_trello=True):
    env = os.environ if env is None else env
    blocos, itens, a = blocos_do_painel(cfg, agora, env)
    trello = ler_trello(cfg.get("trello") or {}, env, trello_transporte) if usar_trello \
        else {"estado": gp.SEM, "motivo": "desligado com --sem-trello"}
    milhas = ler_milhas(cfg.get("milhas") or {}, agora)
    coment = ler_comentarios(blocos.get("RADAR"), a.radar_json, cfg.get("comentarios") or {}, agora)
    termo = ler_termometro(cfg.get("termometro") or {}, agora)
    jobs = avaliar_jobs(cfg.get("jobs") or {}, agora, ler_launchctl())
    return {"agora": agora, "itens_painel": itens, "trader": blocos.get("TRADER"), "trello": trello,
            "milhas": milhas, "comentarios": coment, "termometro": termo, "jobs": jobs,
            "decidir": decidir_hoje(itens, trello, milhas, termo, jobs)}


def montar_mensagem(d, ref_painel=""):
    agora = d["agora"]
    l = [f"☀️ Resumo da manhã · {DIAS_CURTOS[agora.weekday()]} {agora:%d/%m} · {agora:%H:%M}", "", "🎯 Decidir hoje"]
    l += [f"{i}. {t}" for i, t in enumerate(d["decidir"], 1)] or ["Nada urgente."]
    l += [""] + linhas_trello(d["trello"], agora)
    l += ["", "📡 Radares"] + linhas_milhas(d["milhas"], agora) + linhas_comentarios(d["comentarios"], agora) \
        + linhas_termometro(d["termometro"]) + linhas_trader(d["trader"])
    l += ["", linha_jobs(d["jobs"])]
    return cortar("\n".join(l), LIMITE_TELEGRAM, ref_painel)


# --------------------------------------------------------------------------------------------- envio
def _telegram_post(url, dados, timeout=20):
    req = urllib.request.Request(url, data=dados, method="POST")
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def enviar_telegram(texto, env=None, arquivos=None, transporte=None):
    """Envio mínimo, igual ao notifier.py (mesmas variáveis e arquivos), mas em texto puro: o parse_mode
    Markdown do notifier recusa títulos com '_' ou '*', que aparecem em nome de card e de post."""
    env = os.environ if env is None else env
    arquivos = arquivos or TELEGRAM_ARQUIVOS
    token = credencial("TELEGRAM_BOT_TOKEN", env, arquivos)
    chat = credencial(CHAT_ID_KEYS, env, arquivos)
    if not token or not chat:
        raise RuntimeError("faltam TELEGRAM_BOT_TOKEN e TELEGRAM_CHAT_ID (ou TELEGRAM_HOME_CHANNEL) "
                           "no ambiente ou em: " + ", ".join(arquivos))
    dados = urllib.parse.urlencode({"chat_id": chat, "text": texto, "disable_web_page_preview": "true"}).encode()
    try:
        r = (transporte or _telegram_post)(f"https://api.telegram.org/bot{token}/sendMessage", dados)
    except Exception as e:
        raise RuntimeError(str(e).replace(token, "***")) from None
    if not (isinstance(r, dict) and r.get("ok")):
        raise RuntimeError(f"Telegram recusou: {str((r or {}).get('description', r))[:120]}")
    return r


# --------------------------------------------------------------------------------------------- main
def main(argv=None, env=None):
    env = os.environ if env is None else env
    ap = argparse.ArgumentParser(description="Resumo único da manhã no Telegram.")
    ap.add_argument("--config", default=env.get("RESUMO_CONFIG") or str(CONFIG_PADRAO))
    ap.add_argument("--dry-run", action="store_true", help="imprime a mensagem e não envia")
    ap.add_argument("--agora", help="AAAA-MM-DDTHH:MM em Brasília (padrão: agora)")
    ap.add_argument("--launchctl-arquivo", help="lê a saída do `launchctl list` deste arquivo (teste)")
    ap.add_argument("--sem-trello", action="store_true", help="não consulta o Trello (sem rede)")
    a = ap.parse_args(argv)
    cfg = carregar_config(a.config)
    agora = gp.para_brt(datetime.fromisoformat(a.agora)) if a.agora else datetime.now(gp.BRT)
    if a.launchctl_arquivo:
        def ler_lc():
            try:
                return Path(a.launchctl_arquivo).read_text(encoding="utf-8")
            except OSError:
                return None
    else:
        ler_lc = rodar_launchctl
    d = coletar(cfg, agora, env, ler_lc, usar_trello=not a.sem_trello)
    ref = (cfg.get("painel_html") or "").replace("{data}", f"{agora:%Y-%m-%d}")
    texto = montar_mensagem(d, ref)
    if a.dry_run:
        print(texto)
        print(f"\n[dry-run: nada enviado · {tamanho_telegram(texto)} de {LIMITE_TELEGRAM} caracteres]")
        return 0
    try:
        enviar_telegram(texto, env, (cfg.get("telegram") or {}).get("credenciais"))
    except Exception as e:
        print(f"ERRO no envio: {e}", file=sys.stderr)
        print(texto)
        return 1
    print(f"{agora:%Y-%m-%d %H:%M} resumo enviado ({tamanho_telegram(texto)} caracteres)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
