#!/usr/bin/env python3
"""Corte do 'Cotista recusou a cota nova do TRXF11' (gravado 29/09).
Na edicao manda a fala: ad-libs ficam, so saem patos, partidas falsas e takes repetidos.
Borda de corte e vazio saem da ONDA (envelope RMS), nao da transcricao.
"""
import json, subprocess, numpy as np

# (fim da ultima palavra boa, inicio da primeira palavra do take bom, motivo) — master.json
CORTES = [
    (None,     26.02, "pre-roll + 2 'Fala Tanaka e o T...' + patos"),
    (127.22,  141.84, "'E se voce comprou em julho' 2 takes + patos (fica o 3o, chorando no banho)"),
    (190.68,  199.22, "'ninguem cancelou ainda' take 1 + pato"),
    (211.56,  218.26, "'Enquanto a cota escorregava...' + vazio + pato"),
    (249.04,  281.94, "'Se voce chega no caixa' 4 takes + patos (Whisper esticou as palavras, borda pela re-transcricao da janela)"),
    (335.74,  360.08, "'A oferta continua aberta / papel de 10/09' 2 takes + patos"),
    (451.16,  462.56, "'Como e que quem vende o predio' 2 takes + patos"),
    (484.42,  491.12, "'cada cota contada a 94, o preco' + pato"),
    (563.32,  585.64, "'um dos negocios que ja fechou' 2 takes + patos"),
    (591.56,  604.74, "'escritorios na Berrini... quem vendeu foi' + pato (fica o take de 604)"),
    (692.04,  695.98, "'A segunda, pato vermelho'"),
    (778.28,  781.78, "'Nenhuma das tres...' + pato"),
    (935.70,  948.16, "'O fundo tem argumentar...' + vazio + pato"),
    (981.20,  987.18, "'So que quem tem essa conta...' + pato"),
    (1026.02, 1033.26, "'77 centavos entram 90' + vazio"),
    (1064.30, 1068.02, "pato"),
    (1080.02, 1084.42, "'no galpao do ES, Cat Rate' + pato"),
    (1121.62, 1131.98, "'o fundo tem a resposta... uma parcela' + pato"),
    (1270.70, 1275.26, "'Pergunta para quem pagou' + pato"),
    (1323.54, 1328.88, "'Isso aqui...' + pato"),
    (1342.14, 1350.28, "'E 72 a cota sai abaixo... de todos' + pato"),
    (1646.52, None,   "fim"),
]

# ---------- a onda ----------
SR, H = 16000, 160                      # envelope de 10 ms
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", "master.wav", "-f", "s16le", "-ac", "1",
                      "-ar", str(SR), "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
n = len(x) // H
db = 20 * np.log10(np.sqrt((x[:n*H].reshape(n, H) ** 2).mean(1)) + 1e-9)
# limiar fala/ruido por Otsu no histograma: aqui o ruido do motorhome fica em -25 dB e a fala em -12,
# entao gate fixo de -30 dB (o do Calote) nunca ve pausa nenhuma. ponytail: Otsu basta com 2 modas.
_h, _e = np.histogram(db[db > -60], bins=120); _c = (_e[:-1] + _e[1:]) / 2
LIM = max(_c[1:], key=lambda t: _h[_c < t].sum() * _h[_c >= t].sum() *
          (((_h * _c)[_c >= t].sum() / _h[_c >= t].sum()) - ((_h * _c)[_c < t].sum() / _h[_c < t].sum())) ** 2)
DUR = len(x) / SR
fr = lambda t: int(round(t * SR / H)); tt = lambda i: i * H / SR

def vale(t0, t1):
    """meio da MAIOR pausa (abaixo do LIM) entre t0 e t1; sem pausa, o ponto mais baixo.
    ponytail: o ponto mais baixo sozinho caiu dentro do 'vermelho' em 1050 s e deixou meio pato."""
    i0, i1 = fr(max(0, t0)), fr(min(DUR, t1))
    q = db[i0:i1] < LIM
    best, j = (0, 0, 0), 0
    while j < len(q):
        if q[j]:
            k = j
            while k < len(q) and q[k]: k += 1
            if k - j > best[0]: best = (k - j, j, k)
            j = k
        else: j += 1
    if best[0]: return tt(i0 + (best[1] + best[2]) // 2)
    s = np.convolve(db[i0:i1], np.ones(5) / 5, mode="same")
    return tt(i0 + int(np.argmin(s)))

# 1) bordas dos cortes no vale da onda (Whisper erra a palavra em 0.3-0.5 s)
keep, cur = [], 0.0
for a, b, m, *ex in CORTES:   # "exato": borda conferida no ouvido, nao encaixa no vale
    if a is not None:
        keep.append([cur, a if ex else vale(a - 0.2, a + 0.6), m])
    cur = (b if ex else vale(b - 0.6, b + 0.5)) if b is not None else DUR
if cur < DUR: keep.append([cur, DUR, "ate o fim"])

# 2) vazio pela onda: dentro de cada trecho, pausa > MAXP vira RESP; nas pontas sobra BORDA
MAXP, RESP, BORDA = 0.45, 0.30, 0.12
out = []
for a, b, m in keep:
    i0, i1 = fr(a), fr(b)
    fala = db[i0:i1] >= LIM
    idx = np.flatnonzero(fala)
    if len(idx) == 0: continue
    s0 = max(a, tt(i0 + idx[0]) - BORDA); s1 = min(b, tt(i0 + idx[-1] + 1) + BORDA)
    # pausas internas
    pedacos, ini = [], s0
    j = idx[0]
    while j < idx[-1]:
        if not fala[j]:
            k = j
            while k < len(fala) and not fala[k]: k += 1
            if (k - j) * H / SR > MAXP:
                pa, pb = tt(i0 + j), tt(i0 + k)
                pedacos.append([ini, pa + RESP / 2, m]); ini = pb - RESP / 2; m = "vazio"
            j = k
        else: j += 1
    pedacos.append([ini, s1, m])
    out += pedacos

keep = [[0, round(a, 3), round(b, 3), m] for a, b, m in out if b - a > 0.08]
json.dump({"keep": keep}, open("cuts.json", "w"), ensure_ascii=False, indent=0)
tot = sum(k[2] - k[1] for k in keep)
print(f"LIM {LIM:.1f} dB · {len(keep)} trechos · {tot//60:.0f}:{tot%60:05.2f} de {DUR//60:.0f}:{DUR%60:05.2f}")
