#!/usr/bin/env python3
"""Auditoria do render pela ONDA. uso: python3 auditar.py FINAL-corte.mp4 cuts.json
1) pausas: toda pausa (envelope < limiar Otsu) > 0.5 s no render
2) emendas: transcreve 2.5 s de cada lado de CADA emenda sozinha — pato vazado ou palavra comida
   aparece aqui mesmo quando a transcricao do video inteiro engole."""
import sys, json, subprocess, numpy as np, mlx_whisper, re
f, cj = sys.argv[1], sys.argv[2]
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-map", "0:a:0", "-ac", "1", "-ar", "16000",
                      "-f", "s16le", "-"], capture_output=True).stdout
x = np.frombuffer(raw, np.int16).astype(np.float32) / 32768
H = 160; n = len(x) // H
db = 20 * np.log10(np.sqrt((x[:n*H].reshape(n, H) ** 2).mean(1)) + 1e-9)
h, e = np.histogram(db[db > -60], bins=120); c = (e[:-1] + e[1:]) / 2
LIM = max(c[1:], key=lambda t: h[c < t].sum() * h[c >= t].sum() *
          (((h * c)[c >= t].sum() / h[c >= t].sum()) - ((h * c)[c < t].sum() / h[c < t].sum())) ** 2)
q = db < LIM; pausas, j = [], 0
while j < n:
    if q[j]:
        k = j
        while k < n and q[k]: k += 1
        if (k - j) * H / 16000 > 0.5: pausas.append((j * H / 16000, (k - j) * H / 16000))
        j = k
    else: j += 1
print(f"LIM {LIM:.1f} dB · pausas > 0.5 s: {len(pausas)}")
for t, d in pausas: print(f"  PAUSA {int(t//60)}:{t%60:05.2f}  {d:.2f}s")
keep = json.load(open(cj))["keep"]; t, emendas = 0, []
for s, a, b, m in keep[:-1]:
    t += round((b - a) * 30) / 30; emendas.append((t, m))
PATO = re.compile(r"\bp[ai]t[oa]s?\b|\b(vermelh|amarel)[oa]s?\b", re.I)
for t, m in emendas:
    seg = x[int(max(0, t - 2.5) * 16000): int((t + 2.5) * 16000)]
    tx = mlx_whisper.transcribe(seg, path_or_hf_repo="mlx-community/whisper-large-v3-turbo",
                                language="pt", condition_on_previous_text=False)["text"].strip()
    print(f"{'!!PATO ' if PATO.search(tx) else ''}{int(t//60)}:{t%60:05.2f} [{m[:28]}] {tx}", flush=True)
