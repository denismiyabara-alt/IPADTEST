#!/usr/bin/env python3
"""TROCA POR COMANDO: aprova (ou desfaz) a troca proposta e regenera o calendário oficial.

  python3 outliers/encaixar.py aprovar OUT-<video_id> [--quem Denis] [--dry-run]
  python3 outliers/encaixar.py desfazer OUT-<video_id> [--quem Denis] [--dry-run]     (ou o id da troca, T18)
  python3 outliers/encaixar.py listar                                                 (propostas e trocas de outlier)

aprovar:
1. acha a proposta (outliers/estado/propostas.json guarda todas; a saída do dia também serve);
2. confere de novo, no CALENDARIO.csv atual, que a vaga existe, é futura e não é série nem Copom;
3. acrescenta ao FIM de pautas-canal/trocas.json (formato do calendario_v3.py) duas trocas com o mesmo "proposta":
   - op "titulo": a pauta (data + formato + título) recebe o título novo; também leva data, sai, entra, motivo,
     aprovado_por e quando, legíveis por gente;
   - op "edita": ângulo, fontes, continuação e origem da pauta nova;
4. roda o calendario_v3.py, que regenera CALENDARIO.md e .csv. Se ele falhar, o trocas.json volta como estava;
5. grava a ação em outliers/estado/historico_trocas.jsonl (o histórico não é apagado nem no desfazer).

desfazer: tira do trocas.json as trocas daquela proposta, regenera e registra no histórico.
--dry-run: mostra o que seria gravado; não grava nada e não roda o gerador.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import comum as c
import propor


def caminhos(cfg):
    cc = cfg["calendario"]
    est = c.caminho(cfg["caminhos"]["estado"])
    return {"csv": c.caminho(cc["csv"]), "trocas": c.caminho(cc["trocas"]), "gerador": c.caminho(cc["gerador"]),
            "arquivo": est / "propostas.json", "historico": est / "historico_trocas.jsonl",
            "saida": c.caminho(cfg["caminhos"]["saida"]) / "propostas.json"}


def achar_proposta(pid, cam):
    arq = c.ler_json(cam["arquivo"], {}) or {}
    if pid in arq:
        return arq[pid]
    for p in (c.ler_json(cam["saida"], {}) or {}).get("propostas", []):
        if p["id"] == pid:
            return p
    return None


def ler_trocas_doc(p):
    d = c.ler_json(p, None)
    if d is None:
        return {"descricao": "Trocas aprovadas no calendário oficial (v3).", "trocas": []}
    if isinstance(d, list):
        return {"trocas": d}
    d.setdefault("trocas", [])
    return d


def _linha(t):
    return "    " + json.dumps(t, ensure_ascii=False)


def texto_com(texto, novas):
    """Acrescenta as trocas no fim do array SEM reformatar o resto do arquivo (cada troca nova em uma linha)."""
    if texto is None:
        return None
    i = texto.rstrip().rfind("]")
    antes = texto[:i].rstrip()
    sep = "" if antes.endswith("[") else ","
    novo = antes + sep + "\n" + ",\n".join(_linha(t) for t in novas) + "\n  " + texto[i:]
    try:
        ok = json.loads(novo)["trocas"] == json.loads(texto)["trocas"] + novas
    except (ValueError, KeyError):
        ok = False
    return novo if ok else None


def texto_sem(texto, pid, esperado):
    """Tira as linhas das trocas da proposta (as que este script gravou), sem reformatar o resto."""
    linhas = [l for l in texto.split("\n") if not (l.strip().startswith("{") and f'"proposta": "{pid}"' in l)]
    novo = re.sub(r",(\s*\n\s*\])", r"\1", "\n".join(linhas))
    try:
        ok = json.loads(novo)["trocas"] == esperado
    except (ValueError, KeyError):
        ok = False
    return novo if ok else None


def gravar_trocas(p, doc, texto):
    if texto is not None:
        Path(p).write_text(texto, encoding="utf-8")
    else:
        c.gravar_json(p, doc)


def proximo_id(trocas):
    ns = [int(m.group(1)) for t in trocas for m in [re.fullmatch(r"T(\d+)", str(t.get("id", "")))] if m]
    return max(ns, default=0) + 1


def registrar(cam, ev):
    cam["historico"].parent.mkdir(parents=True, exist_ok=True)
    with open(cam["historico"], "a", encoding="utf-8") as f:
        f.write(json.dumps(ev, ensure_ascii=False) + "\n")


def regenerar(cam, timeout=600):
    g = cam["gerador"]
    if not g or not g.is_file():
        return False, f"gerador não encontrado: {g}"
    r = subprocess.run([sys.executable, str(g)], cwd=str(g.parent), capture_output=True, text=True, timeout=timeout)
    saida = (r.stdout + r.stderr).strip().splitlines()
    return r.returncode == 0, (saida[-1] if saida else f"código {r.returncode}")


def trocas_da_proposta(p, quem, agora, n0):
    o, e = p["outlier"], p["encaixe"]
    pauta = {"data": e["data"], "formato": e["formato"], "titulo": e["sai"]}
    motivo = (f"Outlier: \"{o['titulo']}\" ({o['canal']}, {o['multiplo']:g}x, {o['url']}). Ampliar o outlier, não "
              f"contradizer. Sai a pauta de menor inscritos esperados nas próximas semanas ({e.get('sai_esperado')}), "
              f"fora da série e do Copom. Proposta {p['id']}.")
    base = {"aprovada_em": agora.date().isoformat(), "aprovada_por": quem, "motivo": motivo, "proposta": p["id"]}
    t1 = {"id": f"T{n0:02d}", **base, "op": "titulo", "pauta": pauta, "novo": e["entra"],
          "data": e["data"], "sai": e["sai"], "entra": e["entra"], "aprovado_por": quem, "quando": c.iso(agora)}
    t2 = {"id": f"T{n0 + 1:02d}", **base, "op": "edita",
          "pauta": {"data": e["data"], "formato": e["formato"], "titulo": e["entra"]},
          "campos": {"angulo": "RASCUNHO do outlier (revisar): " + p["angulo"],
                     "fontes_a_conferir": f"{p['dado_chave']['dado']}: {p['dado_chave']['fonte_primaria']}",
                     "continuacao_de": f"outlier {o['url']}",
                     "status_titulo": "rascunho do outlier (passa pelo empacotador)",
                     "origem": f"outlier {p['id']} (no lugar de \"{e['sai']}\")"}}
    return [t1, t2]


def conferir_vaga(p, cam, hoje, cfg):
    e = p["encaixe"]
    if e.get("tipo") != "troca":
        return f"a proposta {p['id']} não é troca ({e.get('tipo')}): {e.get('texto', '')}"
    linhas = propor.ler_calendario(cam["csv"])
    alvo = [r for r in linhas if (r.get("data"), r.get("formato"), r.get("titulo")) == (e["data"], e["formato"], e["sai"])]
    if not alvo:
        return (f"a pauta de {e['data']} (\"{e['sai']}\") não está mais no CALENDARIO.csv: o calendário mudou. "
                "Rode propor.py de novo.")
    if propor.protegida(alvo[0], cfg["calendario"].get("protegidas_regex", "copom")):
        return "a vaga é da série ou do Copom: nunca troca"
    if date.fromisoformat(e["data"]) <= hoje:
        return f"a data {e['data']} já passou (ou é hoje)"
    return None


def aprovar(pid, cfg, quem="Denis", dry_run=False, agora=None, saida=print):
    agora = agora or datetime.now(timezone.utc)
    cam = caminhos(cfg)
    p = achar_proposta(pid, cam)
    if p is None:
        saida(f"ERRO: proposta {pid} não encontrada")
        return 2
    doc = ler_trocas_doc(cam["trocas"])
    if any(t.get("proposta") == pid for t in doc["trocas"]):
        saida(f"ERRO: a proposta {pid} já foi aprovada (use desfazer antes)")
        return 2
    erro = conferir_vaga(p, cam, agora.astimezone(timezone(timedelta(hours=-3))).date(), cfg)
    if erro:
        saida(f"ERRO: {erro}")
        return 2
    novas = trocas_da_proposta(p, quem, agora, proximo_id(doc["trocas"]))
    if dry_run:
        saida(f"[dry-run] acrescentaria a {cam['trocas']}:\n" + json.dumps(novas, ensure_ascii=False, indent=2))
        saida(f"[dry-run] e rodaria {cam['gerador']}. Nada foi gravado.")
        return 0
    antes = cam["trocas"].read_text(encoding="utf-8") if cam["trocas"].is_file() else None
    texto = texto_com(antes, novas)
    doc["trocas"] += novas
    gravar_trocas(cam["trocas"], doc, texto)
    ok, msg = regenerar(cam)
    if not ok:
        if antes is None:
            cam["trocas"].unlink()
        else:
            cam["trocas"].write_text(antes, encoding="utf-8")
        saida(f"ERRO: o calendario_v3.py falhou ({msg}); trocas.json voltou como estava")
        registrar(cam, {"acao": "aprovar (falhou)", "proposta": pid, "quem": quem, "quando": c.iso(agora), "erro": msg})
        return 1
    registrar(cam, {"acao": "aprovar", "proposta": pid, "quem": quem, "quando": c.iso(agora),
                    "trocas": novas, "gerador": msg})
    e = p["encaixe"]
    saida(f"ok: {e['data']} \"{e['sai']}\" -> \"{e['entra']}\" ({novas[0]['id']} e {novas[1]['id']}); {msg}")
    return 0


def desfazer(ident, cfg, quem="Denis", dry_run=False, agora=None, saida=print):
    agora = agora or datetime.now(timezone.utc)
    cam = caminhos(cfg)
    doc = ler_trocas_doc(cam["trocas"])
    alvo = next((t for t in doc["trocas"] if ident in (t.get("proposta"), t.get("id"))), None)
    if alvo is None or not alvo.get("proposta"):
        saida(f"ERRO: nenhuma troca de outlier com id {ident} em {cam['trocas']}")
        return 2
    pid = alvo["proposta"]
    sai = [t for t in doc["trocas"] if t.get("proposta") == pid]
    if dry_run:
        saida(f"[dry-run] tiraria de {cam['trocas']}: {', '.join(t['id'] for t in sai)} (proposta {pid}) e rodaria o "
              "gerador. Nada foi gravado.")
        return 0
    antes = cam["trocas"].read_text(encoding="utf-8")
    doc["trocas"] = [t for t in doc["trocas"] if t.get("proposta") != pid]
    gravar_trocas(cam["trocas"], doc, texto_sem(antes, pid, doc["trocas"]))
    ok, msg = regenerar(cam)
    if not ok:
        cam["trocas"].write_text(antes, encoding="utf-8")
        saida(f"ERRO: o calendario_v3.py falhou ao desfazer ({msg}); trocas.json voltou como estava. Alguma troca "
              "posterior usa a pauta nova?")
        return 1
    registrar(cam, {"acao": "desfazer", "proposta": pid, "quem": quem, "quando": c.iso(agora), "trocas": sai,
                    "gerador": msg})
    saida(f"ok: desfeita a proposta {pid} ({', '.join(t['id'] for t in sai)}); {msg}")
    return 0


def listar(cfg, saida=print):
    cam = caminhos(cfg)
    arq = c.ler_json(cam["arquivo"], {}) or {}
    feitas = {t.get("proposta") for t in ler_trocas_doc(cam["trocas"])["trocas"] if t.get("proposta")}
    for pid, p in sorted(arq.items(), key=lambda x: x[1].get("gerada_em", ""), reverse=True)[:20]:
        marca = "APROVADA" if pid in feitas else p["encaixe"]["tipo"]
        saida(f"{pid}  [{marca}]  {propor.linha_resumo(p)}")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description="Aprova ou desfaz a troca proposta para um outlier.")
    ap.add_argument("acao", choices=["aprovar", "desfazer", "listar"])
    ap.add_argument("id", nargs="?")
    ap.add_argument("--quem", default="Denis")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--config")
    a = ap.parse_args(argv)
    cfg = c.carregar_config(a.config)
    if a.acao == "listar":
        return listar(cfg)
    if not a.id:
        ap.error("informe o id (OUT-<video_id> ou o id da troca)")
    f = aprovar if a.acao == "aprovar" else desfazer
    return f(a.id, cfg, a.quem, a.dry_run)


if __name__ == "__main__":
    sys.exit(main())
