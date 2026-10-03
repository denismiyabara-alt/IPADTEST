#!/usr/bin/env python3
"""Trilha de efeitos do VIDEO-FINAL: cada som que o gerar.py previu pra cena (eventos.json, tempo
relativo a cena) cai no tempo em que a cena entra no video (cartelas.json). Saida: sfx.wav (48 kHz,
mono, duracao do FINAL-corte). Sons: biblioteca media-use (Pixabay) + sintetizados do Faz a Conta.
ponytail: evento depois da janela aparada nao toca (a cena ja saiu).
"""
import json, subprocess, numpy as np, soundfile as sf, sys
sys.path.insert(0, "/Users/denal/Downloads/faz-a-conta/bets")
import sfx as FAC                       # carimbo, tique, moeda, lib, env, SR

SR = FAC.SR
rng = np.random.default_rng(11)

def papel():                            # folha batendo na mesa
    n = int(.22 * SR); r = rng.normal(0, 1, n) * FAC.env(n, .001, .05)
    return np.convolve(r, np.ones(10) / 10, "same") * .8

def marca_texto():                      # caneta riscando: ruido em faixa, modulado em "vai-e-vem"
    n = int(.5 * SR); t = np.arange(n) / SR
    r = rng.normal(0, 1, n)
    r = r - np.convolve(r, np.ones(40) / 40, "same")          # tira o grave
    r = np.convolve(r, np.ones(3) / 3, "same")                # tira o chiado mais agudo
    am = .55 + .45 * np.abs(np.sin(2 * np.pi * 7 * t))
    return r * am * np.minimum(1, t / .03) * np.minimum(1, (t[-1] - t) / .08) * .5

SONS = dict(pop=FAC.lib("pop"), whoosh=FAC.lib("whoosh"), **{"whoosh-curto": FAC.lib("whoosh-short")},
            impacto=FAC.lib("impact-bass-1"), riser=FAC.lib("riser")[:int(.9 * SR)] * np.linspace(1, 0, int(.9 * SR)),
            click=FAC.lib("click-soft"), carimbo=FAC.carimbo(), moeda=FAC.moeda(), papel=papel(),
            **{"marca-texto": marca_texto()})

def som(nome):
    if nome.startswith("tique:"): return FAC.tique(float(nome[6:]), vol=.8)
    return SONS[nome]

dur = float(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a:0", "-show_entries", "stream=duration",
                            "-of", "default=nw=1:nk=1", "FINAL-corte.mp4"], capture_output=True, text=True).stdout)
a = np.zeros(int(dur * SR) + SR)
import os
ev = json.load(open("videos/broll/eventos.json")) if os.path.exists("videos/broll/eventos.json") else {}
# graficos (4a peca): um som so, o "impacto" no pouso do numero (Denis: so o numero aterrissando)
if os.path.exists("videos/broll/graficos.json"):
    ev.update({gid: g["eventos"] for gid, g in json.load(open("videos/broll/graficos.json")).items()})
n = 0
for c in json.load(open("cartelas.json")):
    janela = c["fim"] - c["ini"]
    for t, nome, g in ev.get(c["id"].split("@")[0], []):
        if t >= janela - .05: continue
        s = som(nome); i = int((c["entra"] + t) * SR); j = min(len(a), i + len(s))
        a[i:j] += g * s[:j - i]; n += 1
a = a[:int(dur * SR)]
pico = np.abs(a).max()
if pico > .95: a *= .95 / pico
sf.write("sfx.wav", a.astype(np.float32), SR)
print(f"sfx.wav · {dur:.1f}s · {n} sons · pico {pico:.2f}")
