#!/usr/bin/env python3
"""Monta o video final: FINAL-corte + as cartelas por cima, nos pontos do EDL.

ponytail: corta tudo em pedacos e concatena por copia — 24 overlays encadeados
davam 0,08x (4h de render) porque cada trim redecodifica o input inteiro.

⚠️ CONTABILIDADE EM FRAMES INTEIROS, NUNCA EM SEGUNDOS.
A versao anterior cortava com `-ss X -to Y` e avancava o cursor pelo valor *pedido*.
Cada peca sai com numero inteiro de frames, entao a duracao real caia num multiplo
de 1/30 — em media meio frame a mais. Com 53 pecas isso virou +0,84s de deriva
monotonica (medido no TRXF11 DESISTIU), sempre no mesmo sentido: video atrasando,
audio "adiantado". `-frames:v N` fixa a duracao de cada peca por construcao e o
acumulador em frames garante que a soma bata com o audio no fim E no meio.
"""
import subprocess, os, glob, json

BASE = "FINAL-corte.mp4"
FPS = 30
def ultimo(d): return sorted(glob.glob(f"videos/{d}/renders/*.mp4"))[-1]
PECA = {"A": ultimo("broll-cartelas"),
        "B": ultimo("broll-prints")}
TMP = "montagem"
APARA = 0.25   # corta o miolo do fade da cartela pra nao entrar em papel vazio
DUR_BASE = 1093.97
N_BASE = round(DUR_BASE * FPS)

ordem = [(c["peca"], c["ini"], c["fim"], c["entra"]) for c in json.load(open("cartelas.json"))]
for x, y in zip(ordem, ordem[1:]):
    assert x[3] + (x[2] - x[1]) <= y[3] + 0.01, f"colisao entre {x} e {y}"

os.makedirs(TMP, exist_ok=True)
V = ["-c:v", "h264_videotoolbox", "-b:v", "20M", "-an", "-r", str(FPS),
     "-pix_fmt", "yuv420p", "-video_track_timescale", str(FPS * 1000)]

def corta(src, ini_f, n_f, saida):
    """Corta n_f frames a partir do frame ini_f. -frames:v e o que trava a duracao."""
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", f"{ini_f/FPS:.5f}",
                    "-i", src, "-frames:v", str(n_f), *V, saida], check=True)
    got = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                              "-show_entries", "stream=nb_read_frames", "-of", "default=nw=1:nk=1",
                              saida], capture_output=True, text=True).stdout.strip())
    assert got == n_f, f"{saida}: pedi {n_f} frames, saiu {got}"
    return got

pedacos, out_f, base_f = [], 0, 0
for i, (peca, ini, fim, entra) in enumerate(ordem):
    entra_f = round((entra + APARA) * FPS)          # onde a cartela entra, em frame
    cart_f  = round((fim - ini - 2 * APARA) * FPS)  # quantos frames de cartela
    ini_c_f = round((ini + APARA) * FPS)
    if entra_f > out_f:                              # trecho do Denis antes da cartela
        n = entra_f - out_f
        p = f"{TMP}/base-{i:02d}.mp4"; corta(BASE, base_f, n, p); pedacos.append(p)
        out_f += n; base_f += n
    p = f"{TMP}/cart-{i:02d}.mp4"; corta(PECA[peca], ini_c_f, cart_f, p); pedacos.append(p)
    out_f += cart_f; base_f += cart_f
    print(f"  {i+1:2d}/{len(ordem)}  {peca} frame {entra_f:6d} → {out_f:6d} "
          f"({entra_f/FPS:7.2f}s → {out_f/FPS:7.2f}s)", flush=True)
if out_f < N_BASE:
    n = N_BASE - out_f
    p = f"{TMP}/base-fim.mp4"; corta(BASE, base_f, n, p); pedacos.append(p)
    out_f += n

assert out_f == N_BASE, f"total {out_f} frames, esperado {N_BASE}"
print(f"  ✓ {out_f} frames = {out_f/FPS:.3f}s, casa com o audio")

with open(f"{TMP}/lista.txt", "w") as fh:
    for p in pedacos: fh.write(f"file '{os.path.basename(p)}'\n")

subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0",
                "-i", f"{TMP}/lista.txt", "-c", "copy", f"{TMP}/video-mudo.mp4"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{TMP}/video-mudo.mp4", "-i", BASE,
                "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "copy",   # copia: reencodar geraria 2a geracao de AAC
                "-shortest", "VIDEO-FINAL.mp4"], check=True)
d = subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                    "-show_entries", "stream=nb_read_frames,duration", "-of", "default=nw=1",
                    "VIDEO-FINAL.mp4"], capture_output=True, text=True).stdout.strip()
print(f"VIDEO-FINAL.mp4 · {d.replace(chr(10),' · ')} (base {DUR_BASE}s / {N_BASE} frames)")
