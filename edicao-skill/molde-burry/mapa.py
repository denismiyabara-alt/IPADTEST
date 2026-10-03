#!/usr/bin/env python3
"""Mapa de insercao: onde cada cartela entra no FINAL e que janela dela usar.

ponytail: as janelas saem do index.html que cada peca ja gerou (data-start/duration),
nao de um exec no gerar.py — o meu le plano.json por caminho relativo e quebraria.
As entradas saem do plano.json (ancoradas em frase). Nada de timecode a mao.
"""
import json, re, os, sys

MIN_JANELA = 1.5   # cartela mais curta que isso nao le; melhor remover a ancora

import subprocess
# ponytail: nb_frames do container basta — o corte_frames ja garantiu (assert por peca)
# que o mp4 tem exatamente a soma dos trechos. -count_frames decodificava 2,5 GB por nada.
DUR_VIDEO = int(subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
    "-show_entries","stream=nb_frames","-of","default=nw=1:nk=1","FINAL-corte.mp4"],
    capture_output=True, text=True).stdout.strip()) / 30.0
# ponytail: peca unica (cartelas + prints no mesmo render); janelas.json sai do gerar.py
janelas = {cid: ("A", round(ini, 2), round(ini + dur, 2), dur)
           for cid, (ini, dur) in json.load(open("videos/broll/janelas.json")).items()} \
    if os.path.exists("videos/broll/janelas.json") else {}
# 4a peca: cada grafico e um mp4 proprio (videos/broll/grafico.py → graficos.json), janela [0, dur]
GRAF = json.load(open("videos/broll/graficos.json")) if os.path.exists("videos/broll/graficos.json") else {}
for gid, g in GRAF.items():
    janelas[gid] = ("G", 0.0, g["dur"], g["dur"])

plano = json.load(open("plano.json"))
base = lambda c: c.split("@")[0]
falta = [c for c in plano if base(c) not in janelas]
if falta:
    raise SystemExit("sem janela renderizada: " + ", ".join(falta))

cart = []
for cid, p in plano.items():
    pc, ini, fim, dur = janelas[base(cid)]
    cart.append([pc, ini, min(fim, ini + p["dur"]), p["entra"], cid, min(dur, p["dur"])])
cart.sort(key=lambda c: c[3])

# nao pode invadir a proxima nem passar do fim
for i, c in enumerate(cart):
    lim = cart[i+1][3] if i + 1 < len(cart) else DUR_VIDEO
    sobra = (c[3] + c[5]) - (lim - 0.5)
    if sobra > 0:
        # ponytail: PISO. sem ele o aparo passava de zero e o montar.py pedia -15 frames
        # (esc-4 e 23-socio ancoradas na MESMA frase, 3,3s de distancia). Estourou a montagem.
        nova_dur = round(c[5] - sobra, 2)
        if c[0] == "G" and nova_dur < GRAF[base(c[4])]["pouso"] + 0.8:
            raise SystemExit(f"\n✗ grafico {c[4]} seria cortado em {nova_dur:.1f}s, antes do numero pousar "
                             f"({GRAF[base(c[4])]['pouso']:.1f}s + 0,8s). Afaste a peca seguinte em pecas.py.")
        if nova_dur < MIN_JANELA:
            raise SystemExit(
                f"\n✗ {c[4]} sobraria {nova_dur:.2f}s (minimo {MIN_JANELA}s): a peca seguinte "
                f"entra {lim - c[3]:.1f}s depois dela.\n"
                f"  Duas pecas na mesma frase — mude a ancora de uma das duas em pecas.py.")
        cart[i][2] = round(c[2] - sobra, 2); cart[i][5] = nova_dur
        print(f"  aparado: {c[4]} -{sobra:.1f}s (encostava na proxima)")

# PORTAO: a cartela nao pode sair enquanto ele ainda fala do assunto
segs = json.load(open("final.json"))["segments"]
reprovas = []
for i, c in enumerate(cart):
    entra, sai = c[3], c[3] + c[5]
    lim = cart[i+1][3] if i + 1 < len(cart) else DUR_VIDEO
    fim_fala = max([s["end"] for s in segs
                    if entra - 2 <= s["start"] <= min(lim - 0.8, entra + 9)] or [0])
    buraco = min(lim, fim_fala) - sai
    if buraco > 2.5:
        reprovas.append(f"  {c[4]}: sai em {sai:.1f}s, fala ate {min(lim, fim_fala):.1f}s (buraco {buraco:.1f}s)")
if reprovas:
    print(f"(aviso) {len(reprovas)} cartelas saem antes da fala acabar — regra nova, so informativo")

json.dump([{"peca": c[0], "ini": c[1], "fim": c[2], "entra": c[3], "id": c[4]} for c in cart],
          open("cartelas.json", "w"), indent=1, ensure_ascii=False)
cob = sum(c[5] for c in cart)
print(f"{len(cart)} pecas · {cob:.0f}s de imagem = {cob/DUR_VIDEO*100:.1f}% do video")
