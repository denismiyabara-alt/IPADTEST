#!/usr/bin/env python3
"""Renderiza FINAL-corte.mp4 com contabilidade em frames inteiros.

ponytail: o concat por trim deu 6 frames a mais que a soma dos trechos (bruto e VFR, 29,99 fps
com frames dropados) e o checa_sync perdeu o mapa. Aqui cada trecho de video sai com
`-frames:v N` (N = round(dur*30)) e assert; o audio sai numa passada so, sample-exato,
com atrim de a ate a+N/30. Video e audio batem por construcao, trecho a trecho.
"""
import json, os, subprocess

FPS = 30
SRC = {0: "Cotista-recusou-a-cota-20260929-180245.MOV"}
keep = json.load(open("cuts.json"))["keep"]
os.makedirs("pecas", exist_ok=True)
V = ["-c:v", "h264_videotoolbox", "-b:v", "20M", "-an", "-r", str(FPS),
     "-pix_fmt", "yuv420p", "-video_track_timescale", str(FPS * 1000)]

def nframes(p):
    return int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0",
                               "-show_entries", "stream=nb_read_frames", "-of", "default=nw=1:nk=1", p],
                              capture_output=True, text=True).stdout.strip())

lista, total = [], 0
for i, (src, a, b, rot) in enumerate(keep):
    n = round((b - a) * FPS)
    p = f"pecas/v-{i:02d}.mp4"
    if not (os.path.exists(p) and nframes(p) == n):
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-hwaccel", "videotoolbox", "-ss", f"{a:.5f}",
                        "-i", SRC[src], "-frames:v", str(n), *V, p], check=True)
        got = nframes(p)
        if got < n:   # acabou o arquivo/keyframe antes: clona o ultimo frame
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-hwaccel", "videotoolbox", "-ss", f"{a:.5f}",
                            "-i", SRC[src], "-vf", f"tpad=stop_mode=clone:stop_duration={(n-got)/FPS+0.5:.3f}",
                            "-frames:v", str(n), *V, p], check=True)
            got = nframes(p)
        assert got == n, f"{p}: pedi {n} frames, saiu {got}"
    lista.append(p); total += n
    print(f"  {i+1:2d}/{len(keep)} src{src} {a:8.2f}-{b:8.2f} {n:5d} frames {rot}", flush=True)

with open("pecas/lista.txt", "w") as fh:
    for p in lista: fh.write(f"file '{os.path.basename(p)}'\n")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "pecas/lista.txt",
                "-c", "copy", "pecas/video-mudo.mp4"], check=True)
assert nframes("pecas/video-mudo.mp4") == total, "concat perdeu frame"

# audio: uma passada, sample-exato, mesma duracao N/30 de cada trecho
with open("filter_audio.txt", "w") as f:
    parts = []
    for i, (src, a, b, rot) in enumerate(keep):
        n = round((b - a) * FPS)
        f.write(f"[{src}:a]atrim=start={a:.5f}:end={a + n / FPS:.5f},asetpts=PTS-STARTPTS[a{i}];\n")
        parts.append(f"[a{i}]")
    f.write(f"{''.join(parts)}concat=n={len(keep)}:v=0:a=1[aout]")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", SRC[0], "-/filter_complex", "filter_audio.txt",
                "-map", "[aout]", "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "pecas/audio.m4a"], check=True)
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "pecas/video-mudo.mp4", "-i", "pecas/audio.m4a",
                "-map", "0:v", "-map", "1:a", "-c", "copy", "FINAL-corte.mp4"], check=True)
import shutil; shutil.rmtree("pecas")   # ponytail: apaga na hora (Denis, 11/09) — 5,6 GB de peca nao fica esperando a faxina
d = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,nb_frames,duration",
                    "-of", "compact", "FINAL-corte.mp4"], capture_output=True, text=True).stdout
print(f"\n{total} frames = {total/FPS:.3f}s esperado\n{d}")
