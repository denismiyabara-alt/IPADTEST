"""Regera UMA frase de um bloco ja gerado e remonta wav + beats, sem refazer o resto.
Uso: python3 trocar_frase.py b2 13   (o texto novo vem do blocos.py)"""
import sys, json, numpy as np, soundfile as sf, mlx_whisper
import synth_voz as S
from blocos import BLOCOS

bloco, idx = sys.argv[1], int(sys.argv[2])
meta = json.load(open(f"voz_{bloco}.beats.json")); a, sr = sf.read(f"voz_{bloco}.wav")
asr = lambda p: mlx_whisper.transcribe(p, path_or_hf_repo=S.ASR, language="pt")["text"]
novo, _, bips_novo = S.falar(BLOCOS[bloco][idx][0], 900 + idx, asr)
partes, marcas, cursor = [a[:int(meta["frases"][0]["ini"]*sr)]], [], meta["frases"][0]["ini"]
for k, f in enumerate(meta["frases"]):
    seg = novo if k == idx else a[int(f["ini"]*sr):int(f["fim"]*sr)]
    gap = BLOCOS[bloco][k][1]
    marcas.append({"i": k, "texto": BLOCOS[bloco][k][0], "piii": bips_novo if k == idx else f.get("piii", []),
                   "ini": round(cursor, 3), "fim": round(cursor + len(seg)/sr, 3)})
    partes += [seg, np.zeros(int(gap*sr))]; cursor += len(seg)/sr + gap
audio = np.concatenate(partes)
from suavizar_bordas import suavizar
for m_ in marcas: suavizar(audio, sr, m_["ini"], m_["fim"])
sf.write(f"voz_{bloco}.wav", audio, sr)
json.dump({"dur": round(len(audio)/sr, 3), "frases": marcas}, open(f"voz_{bloco}.beats.json", "w"), ensure_ascii=False, indent=1)
print(f"voz_{bloco}.wav remontado: {len(audio)/sr:.2f}s")
