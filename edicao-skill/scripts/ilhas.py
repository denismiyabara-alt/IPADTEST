#!/usr/bin/env python3
"""Pato pela ONDA: parte o audio em ilhas de fala (vazio >= 0.35 s pelo envelope) e
transcreve cada ilha CURTA sozinha. Pato costuma ser ilha propria ("...pato vermelho" entre
pausas); sozinho num clipe de 1-4 s o Whisper nao tem como engolir no meio de frase longa.
uso: ~/Library/Python/3.9/bin/python3 ilhas.py audio.wav saida.json [max_s=6]"""
import sys, json, subprocess, numpy as np, mlx_whisper, re
f, out = sys.argv[1], sys.argv[2]; MAX = float(sys.argv[3]) if len(sys.argv) > 3 else 6
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-map", "0:a:0", "-ac", "1", "-ar", "16000",
                      "-f", "s16le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
H = 320; n = len(x) // H
db = 20 * np.log10(np.sqrt((x[:n*H].reshape(n, H) ** 2).mean(1)) + 1e-9)
lim = np.percentile(db, 10) + 10
fala = db >= lim
# fecha buracos < 0.35 s (pausa dentro de frase)
ilhas, i = [], 0
while i < n:
    if fala[i]:
        j = i
        while True:
            while j < n and fala[j]: j += 1
            k = j
            while k < n and not fala[k]: k += 1
            if k < n and (k - j) * H / 16000 < 0.35: j = k; continue
            break
        ilhas.append((i * H / 16000, j * H / 16000)); i = j
    else: i += 1
PATO = re.compile(r"\bp[ai]t[oa]s?\b|\b(vermelh|amarel)[oa]s?\b", re.I)
res = []
for a, b in ilhas:
    if b - a > MAX or b - a < 0.3: continue
    seg = x[int(max(0, a - 0.15) * 16000): int((b + 0.15) * 16000)]
    t = mlx_whisper.transcribe(seg, path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
                               language="pt", condition_on_previous_text=False)["text"].strip()
    hit = bool(PATO.search(t))
    res.append({"a": round(a, 2), "b": round(b, 2), "t": t, "pato": hit})
    if hit: print(f"PATO {a:8.2f}-{b:8.2f}  {t}", flush=True)
json.dump({"ilhas": ilhas, "curtas": res}, open(out, "w"), ensure_ascii=False, indent=0)
print(f"{len(ilhas)} ilhas, {len(res)} curtas transcritas, {sum(r['pato'] for r in res)} com pato")
