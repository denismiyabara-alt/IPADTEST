#!/usr/bin/env python3
"""ENTREGA: um card por proposta na lista Ideias do Trello (POST /1/cards), sem duplicar pelo id do vídeo.

Duplicata: o vídeo já está em outliers/estado/cards.json (cards criados por este script) OU algum card aberto da
lista Ideias já tem "video_id: <id>" na descrição.

Lista Ideias, em ordem: TRELLO_LIST_IDEIAS (ambiente) > trello.lista_ideias_id (config) > busca pelo nome
(trello.lista_ideias_nome) no board da lista de referência (ENTRADA, id do ic-health-monitor). Sem achar, sai com
erro e diz o que configurar.

--dry-run imprime os cards e NÃO chama a rede (nem para resolver a lista nem para checar duplicata).

uso:
  python3 entregar.py [--propostas outliers/saida/propostas.json] [--dry-run]
Credenciais: TRELLO_KEY e TRELLO_TOKEN (ambiente ou trello.credenciais).
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.parse
import urllib.request

import comum as c
import propor

TRELLO_API = "https://api.trello.com/1"


def _http(metodo, url, dados=None, timeout=15):
    req = urllib.request.Request(url, data=dados, method=metodo,
                                 headers={"Accept": "application/json", "User-Agent": "IEC-outliers/1.0"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


class Trello:
    def __init__(self, key, token, transporte=None, timeout=15):
        self.key, self.token = key, token
        self.t = transporte or (lambda m, u, d=None: _http(m, u, d, timeout))

    def _auth(self):
        return urllib.parse.urlencode({"key": self.key, "token": self.token})

    def get(self, caminho, **q):
        q = urllib.parse.urlencode(q)
        try:
            return self.t("GET", f"{TRELLO_API}{caminho}?{q}&{self._auth()}")
        except Exception as e:
            raise RuntimeError(str(e).replace(self.key, "***").replace(self.token, "***")) from None

    def post(self, caminho, campos):
        dados = urllib.parse.urlencode({**campos, "key": self.key, "token": self.token}).encode()
        try:
            return self.t("POST", f"{TRELLO_API}{caminho}", dados)
        except Exception as e:
            raise RuntimeError(str(e).replace(self.key, "***").replace(self.token, "***")) from None


def lista_ideias(cfg_t, trello, env):
    if env.get("TRELLO_LIST_IDEIAS"):
        return env["TRELLO_LIST_IDEIAS"]
    if cfg_t.get("lista_ideias_id"):
        return cfg_t["lista_ideias_id"]
    ref = cfg_t.get("lista_referencia_id")
    if not ref:
        raise RuntimeError("sem id da lista Ideias: defina TRELLO_LIST_IDEIAS ou trello.lista_ideias_id")
    board = trello.get(f"/lists/{ref}/board", fields="id")["id"]
    alvo = c.norm(cfg_t.get("lista_ideias_nome", "Ideias"))
    for l in trello.get(f"/boards/{board}/lists", fields="name", filter="open"):
        if alvo in c.norm(l.get("name")):
            return l["id"]
    raise RuntimeError(f"não achei a lista '{cfg_t.get('lista_ideias_nome', 'Ideias')}' no board da lista {ref}: "
                       "defina TRELLO_LIST_IDEIAS ou trello.lista_ideias_id")


def entregar(r, cfg, env=None, transporte=None, dry_run=False, saida=print):
    import os
    env = os.environ if env is None else env
    estado_p = c.caminho(cfg["caminhos"]["estado"]) / "cards.json"
    estado = c.ler_json(estado_p, {}) or {}
    novas = [p for p in r.get("propostas", []) if p["video_id"] not in estado]
    pulados = len(r.get("propostas", [])) - len(novas)
    if dry_run:
        for p in novas:
            nome, desc = propor.card(p)
            saida(f"[dry-run] card na lista Ideias:\n{nome}\n{desc}\n")
        saida(f"[dry-run: nada enviado · {len(novas)} card(s) novo(s), {pulados} já entregue(s)]")
        return {"criados": [], "pulados": pulados, "dry_run": len(novas)}
    cfg_t = cfg.get("trello") or {}
    arqs = [c.caminho(x) for x in cfg_t.get("credenciais") or []]
    key, token = c.credencial("TRELLO_KEY", env, arqs), c.credencial("TRELLO_TOKEN", env, arqs)
    if not key or not token:
        raise RuntimeError("faltam TRELLO_KEY e TRELLO_TOKEN")
    tr = Trello(key, token, transporte, float(cfg_t.get("timeout_s", 15)))
    lid = lista_ideias(cfg_t, tr, env)
    existentes = " ".join(x.get("desc", "") for x in tr.get(f"/lists/{lid}/cards", fields="desc"))
    criados = []
    for p in novas:
        if f"video_id: {p['video_id']}" in existentes:
            estado[p["video_id"]] = {"card": None, "nota": "já existia na lista"}
            pulados += 1
            continue
        nome, desc = propor.card(p)
        d = tr.post("/cards", {"idList": lid, "name": nome, "desc": desc, "pos": "top"})
        estado[p["video_id"]] = {"card": d.get("id"), "url": d.get("shortUrl"), "proposta": p["id"],
                                 "quando": r.get("gerado_em")}
        criados.append(d.get("shortUrl") or d.get("id"))
        saida(f"card criado: {nome} -> {d.get('shortUrl', '')}")
    c.gravar_json(estado_p, estado)
    return {"criados": criados, "pulados": pulados}


def main(argv=None):
    ap = argparse.ArgumentParser(description="Cria os cards das propostas na lista Ideias do Trello.")
    ap.add_argument("--config")
    ap.add_argument("--propostas")
    ap.add_argument("--dry-run", action="store_true", help="só imprime; não chama a rede")
    a = ap.parse_args(argv)
    cfg = c.carregar_config(a.config)
    p = c.caminho(a.propostas) if a.propostas else c.caminho(cfg["caminhos"]["saida"]) / "propostas.json"
    r = c.ler_json(p)
    if r is None:
        print(f"ERRO: não li {p} (rode propor.py antes)", file=sys.stderr)
        return 2
    try:
        res = entregar(r, cfg, dry_run=a.dry_run)
    except Exception as e:
        print(f"ERRO no Trello: {e}", file=sys.stderr)
        return 1
    if not a.dry_run:
        print(f"{len(res['criados'])} card(s) criado(s), {res['pulados']} já entregue(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
