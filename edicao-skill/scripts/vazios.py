#!/usr/bin/env python3
"""Acha vazio pelo SOM, nao pela transcricao nem por gate fixo.
ponytail: RMS 20 ms, piso = percentil 10, limiar = piso + DB. Whisper estica palavra
por cima de silencio e gate -30dB nao ve respiracao/ruido — este pega os dois.
uso: vazios.py arquivo [min_s=0.7] [db=10]"""
import sys, subprocess, numpy as np
f = sys.argv[1]; MIN = float(sys.argv[2]) if len(sys.argv) > 2 else 0.7
DB = float(sys.argv[3]) if len(sys.argv) > 3 else 10
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-map", "0:a:0", "-ac", "1", "-ar", "16000",
                      "-f", "s16le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
H = 320; n = len(x) // H
db = 20 * np.log10(np.sqrt((x[:n*H].reshape(n, H) ** 2).mean(1)) + 1e-9)
piso = np.percentile(db, 10); lim = piso + DB
baixo = db < lim
out, i = [], 0
while i < n:
    if baixo[i]:
        j = i
        while j < n and baixo[j]: j += 1
        if (j - i) * H / 16000 >= MIN: out.append((i * H / 16000, j * H / 16000))
        i = j
    else: i += 1
print(f"piso {piso:.1f} dB  limiar {lim:.1f} dB  vazios>={MIN}s: {len(out)}", file=sys.stderr)
for a, b in out: print(f"{a:9.2f} {b:9.2f} {b-a:5.2f}")
