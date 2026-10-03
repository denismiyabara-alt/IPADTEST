#!/usr/bin/env python3
"""Recalcula a duracao de cada cartela pela fala e escreve de volta nos geradores.
ponytail: uma fonte de verdade (a transcricao), tres geradores atualizados sozinhos."""
import json, re, importlib.util

TETO = 14.0
GER = {"A": ("videos/trxf11-broll-dados/gerar.py", "FR", 2),
       "B": ("videos/trxf11-broll-materias/gerar.py", "CENAS", 7),
       "C": ("videos/trxf11-broll-frases/gerar.py", "FR", 2)}

segs = json.load(open("final.json"))["segments"]
ns = {}; exec(open("mapa.py").read().split("janelas = {}")[0], ns)
ENTRA = ns["ENTRA"]
ordem = sorted(ENTRA.items(), key=lambda kv: kv[1])

novas = {}
for i, (cid, entra) in enumerate(ordem):
    prox = ordem[i+1][1] if i+1 < len(ordem) else 1344.34
    fim_fala = max([s["end"] for s in segs
                    if entra - 2 <= s["start"] <= min(prox - 0.8, entra + 9)] or [entra + 5])
    dur = min(fim_fala - entra + 0.4, prox - entra - 0.5, TETO)
    novas[cid] = round(max(dur, 4.0), 1)

for peca, (caminho, var, idx) in GER.items():
    s = open(caminho).read(); n = 0
    for cid, nova in novas.items():
        m = re.search(r'\("' + re.escape(cid) + r'",(.*?)\)\s*,\s*\n', s, re.S)
        if not m: continue
        partes = m.group(1).split(",")
        antigo = partes[idx-1].strip()
        if not re.match(r'^[\d.]+$', antigo): continue
        partes[idx-1] = partes[idx-1].replace(antigo, str(nova))
        s = s[:m.start(1)] + ",".join(partes) + s[m.end(1):]; n += 1
    open(caminho, "w").write(s)
    print(f"{peca}: {n} cartelas")
print(f"cobertura: {sum(novas.values()):.0f}s = {sum(novas.values())/1344.34*100:.1f}%")
