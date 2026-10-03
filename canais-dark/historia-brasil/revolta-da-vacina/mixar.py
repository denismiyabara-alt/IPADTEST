"""Mixa voz + efeitos (+ trilha opcional) de todos os blocos e troca o audio do master, sem re-renderizar.
Uso: python3 mixar.py [trilha.mp3]   -> <PASTA>-final.mp4
A trilha entra em loop, abaixa sob a voz (sidechain) e o total sai em -14 LUFS (padrao YouTube).
"""
import sys, subprocess, numpy as np, soundfile as sf

SR = 48000
import os
from blocos import BLOCOS as _R
BLOCOS = list(_R)
NOME = os.path.basename(os.getcwd()).upper()

def ler(p):
    raw = subprocess.run(["ffmpeg", "-v", "error", "-i", p, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).astype(np.float64)

def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", p],
                                capture_output=True, text=True).stdout)

import json
from blocos import BLOCOS as ROTEIRO
voz, fx, silencios, ofs = [], [], [], 0.0
for b in BLOCOS:
    n = int(round(dur(f"render_{b}.mp4") * SR))      # cada bloco ocupa exatamente o tempo do seu video
    fr = json.load(open(f"voz_{b}.beats.json"))["frases"]
    for k, f in enumerate(fr):                        # punchline = pausa longa depois
        gap = ROTEIRO[b][k][1]
        prox = ofs + (fr[k+1]["ini"] if k + 1 < len(fr) else n / SR + .35)   # fecho de bloco: volta no proximo
        if gap >= 0.9:
            silencios.append((ofs + f["fim"] - .05, prox + .3, 0.0))    # corta seco
        elif gap >= 0.7:
            silencios.append((ofs + f["fim"] - .05, prox + .2, 0.25))   # afunda
    ofs += n / SR
    for lista, arq in ((voz, f"voz_{b}.wav"), (fx, f"sfx_{b}.wav")):
        a = ler(arq)[:n]
        lista.append(np.pad(a, (0, n - len(a))))
sf.write("/tmp/_voz.wav", np.concatenate(voz), SR)
sf.write("/tmp/_fx.wav", np.concatenate(fx) * 0.5, SR)   # efeitos ~6 dB abaixo da voz

trilha = sys.argv[1] if len(sys.argv) > 1 else None
if trilha:
    total_n = len(np.concatenate(voz))
    m = ler(trilha); m = np.tile(m, total_n // len(m) + 1)[:total_n]
    env = np.ones(total_n)
    for a, b, nivel in silencios:                     # entra seco, volta em 0,8s
        i, j = int(a*SR), min(int(b*SR), total_n)
        env[i:j] = np.minimum(env[i:j], nivel)
        k = min(int(.8*SR), total_n - j); env[j:j+k] = np.minimum(env[j:j+k], np.linspace(nivel, 1, k))
    sf.write("/tmp/_bgm.wav", m * env, SR)
    print(f"  musica: {sum(1 for x in silencios if x[2] == 0)} cortes secos, {sum(1 for x in silencios if x[2] > 0)} afundadas")
    trilha = "/tmp/_bgm.wav"
    # base -18 dB, e o sidechain da voz abaixa mais quando ela fala
    filtro = ("[2:a]volume=0.12,afade=t=in:d=1.5[bgm];"
              "[0:a]asplit=2[v][vsc];"
              "[bgm][vsc]sidechaincompress=threshold=0.02:ratio=6:attack=40:release=500[bgmd];"
              "[v][1:a][bgmd]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[out]")
    entradas = ["-i", "/tmp/_voz.wav", "-i", "/tmp/_fx.wav", "-i", trilha]
else:
    filtro = "[0:a][1:a]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=11[out]"
    entradas = ["-i", "/tmp/_voz.wav", "-i", "/tmp/_fx.wav"]
subprocess.run(["ffmpeg", "-v", "error", "-y", *entradas, "-filter_complex", filtro, "-map", "[out]",
                "-ar", "48000", "/tmp/_mix.wav"], check=True)
# fade final de 1,5s na trilha toda (o calendario segura em silencio de voz)
total = dur("/tmp/_mix.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{NOME}-video.mp4", "-i", "/tmp/_mix.wav",
                "-af", f"afade=t=out:st={total-1.5:.2f}:d=1.5", "-map", "0:v", "-map", "1:a",
                "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", f"{NOME}-final.mp4"], check=True)
# acerta o volume em -14 LUFS (o loudnorm de 1 passada fica ~2 dB abaixo) com limitador nos picos
med = subprocess.run(["ffmpeg", "-i", f"{NOME}-final.mp4", "-af", "ebur128", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
lufs = float([l for l in med.splitlines() if l.strip().startswith("I:")][-1].split()[1])
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", f"{NOME}-final.mp4", "-c:v", "copy",
                "-af", f"volume={-14 - lufs:.1f}dB,alimiter=limit=0.84:level=false", "-c:a", "aac", "-b:a", "192k",
                "/tmp/_v.mp4"], check=True)
import shutil; shutil.move("/tmp/_v.mp4", f"{NOME}-final.mp4")
print(f"  volume: {lufs:.1f} -> -14 LUFS")
print(f"ok: {NOME}-final.mp4  ({total:.1f}s, trilha: {trilha or 'nenhuma'})")
