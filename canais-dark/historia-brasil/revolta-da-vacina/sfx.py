"""Trilha de efeitos do bloco, no tempo exato das animações. TODOS os sons são sintetizados aqui
(papel, carimbo, máquina de escrever, campainha da máquina, guincho de rato, clique de projetor):
sem biblioteca de terceiros, sem licença envolvida e sem som em comum com o canal irmão.
Uso: python3 sfx.py b0 b1 ...   -> sfx_<bloco>.wav (mesma duração do render do bloco)
Os tempos saem por regex do JS das cenas; peça nova fica muda até ganhar regra aqui.
"""
import json
import re
import sys

import numpy as np
import soundfile as sf

SR = 48000
rng = np.random.default_rng(1904)   # semente fixa: mesma trilha a cada build


def env(n, ataque=.002, queda=.1):
    t = np.arange(n) / SR
    return np.minimum(1, t / ataque) * np.exp(-t / queda)


def ruido(n, suave=1):
    r = rng.normal(0, 1, n)
    return np.convolve(r, np.ones(suave) / suave, "same") if suave > 1 else r


def papel():                       # folha caindo na mesa: chiado curto e abafado
    n = int(.28 * SR)
    return .35 * ruido(n, 9) * env(n, .03, .07)


def carimbo():                     # baque de madeira + tapa no papel
    n = int(.4 * SR); t = np.arange(n) / SR
    return .9 * np.sin(2 * np.pi * (110 - 50 * t / .4) * t) * env(n, .001, .08) + .5 * ruido(n, 5) * env(n, .0005, .02)


def tecla():                       # máquina de escrever
    n = int(.05 * SR); t = np.arange(n) / SR
    return (.6 * ruido(n, 2) * env(n, .0003, .006) + .3 * np.sin(2 * np.pi * 1800 * t) * env(n, .0005, .01))


def campainha():                   # o "plim" do fim da linha
    n = int(.6 * SR); t = np.arange(n) / SR
    return .25 * (np.sin(2 * np.pi * 2093 * t) + .5 * np.sin(2 * np.pi * 4186 * t)) * env(n, .001, .18)


def guincho():                     # rato
    n = int(.12 * SR); t = np.arange(n) / SR
    f = 3200 + 900 * np.sin(2 * np.pi * 18 * t)
    return .18 * np.sin(2 * np.pi * np.cumsum(f) / SR) * env(n, .005, .05)


def projetor():                    # clique da íris
    n = int(.03 * SR)
    return .3 * ruido(n) * env(n, .0002, .004)


def tique():
    n = int(.012 * SR); t = np.arange(n) / SR
    return .5 * np.sin(2 * np.pi * 2900 * t) * env(n, .0003, .003)


class Pista:
    def __init__(self, dur):
        self.a = np.zeros(int(dur * SR) + SR)

    def add(self, som, t, gan=1.0):
        i = int(max(0, t) * SR); j = min(len(self.a), i + len(som))
        if j > i:
            self.a[i:j] += gan * som[:j - i]


def avaliar(expr, T, D):
    e = expr.replace("Math.min", "min").replace("Math.max", "max")
    return float(eval(e, {"min": min, "max": max, "T": T, "D": D}))


def sonorizar(bloco):
    import build_hf
    from blocos import BLOCOS
    meta = json.load(open(f"voz_{bloco}.beats.json"))
    cenas, _, cauda = build_hf.registro(bloco)
    dur = meta["dur"] + cauda
    P = Pista(dur)
    fr = meta["frases"]
    for k, f in enumerate(fr):
        html, js = cenas.get(k, ("", ""))
        T, D = f["ini"], f["fim"] - f["ini"]
        m = re.search(r"\}\)\(T \+ ([\d.]+)\*D\);$", js)          # cena atrasada até a palavra
        if m:
            T = T + float(m.group(1)) * D
        ev = lambda x: avaliar(x, T, D)
        for _ in re.finditer(r"\{y:-70, rotation:", js):
            P.add(papel(), T, .8)
        if "tl.to('#stage'" in js:
            P.add(carimbo(), T + .41, .9)
        for m in re.finditer(r"from\('#(\w+) span', \{opacity:0, y:-24, duration:\.08, stagger:\.11", js):   # ano
            n = len(re.findall(r"<span>", html))
            for i in range(n):
                P.add(tecla(), T + i * .11, .9)
            P.add(campainha(), T + n * .11 + .05, .8)
        m = re.search(r"from\('#\w+ li', \{opacity:0, x:-30, duration:\.3, stagger:Math\.min\(\.7, D/(\d+)\)", js)
        if m:
            st = min(.7, D / int(m.group(1)))
            for i in range(html.count("<li")):
                for j in range(4):
                    P.add(tecla(), T + i * st + j * .05, .7)
        for m in re.finditer(r"countTo\('[^']+', [^,]+, [^,]+, ([^,]+), (Math\.min\([^)]*\)|[^,)]+)", js):
            t0, d = ev(m.group(1)), ev(m.group(2))
            for i in range(int(8 + 10 * d)):
                u = i / (8 + 10 * d)
                P.add(tique(), t0 + d * (1 - (1 - u) ** 2), .5)
        if "bounce.out'}}, T)" in js or "ease:'bounce.out'}, T)" in js:   # placa pregada
            P.add(carimbo()[: int(.2 * SR)], T + .45, .5)
        if "rato-m" in html:
            n = html.count("rato-m")
            st = min(.18, (D - .4) / n)
            for i in range(0, n, 3):
                P.add(guincho(), T + i * st, .7)
    gaps = [g for _, g in BLOCOS[bloco]]
    for k, f in enumerate(fr[:-1]):                           # íris de punchline
        if gaps[k] >= .75:
            P.add(projetor(), f["fim"] + .02, .8)
    a = P.a[:int(dur * SR)]
    sf.write(f"sfx_{bloco}.wav", a, SR)
    print(f"sfx_{bloco}.wav  {dur:.1f}s  pico {np.abs(a).max():.2f}")


if __name__ == "__main__":
    for b in sys.argv[1:]:
        sonorizar(b)
