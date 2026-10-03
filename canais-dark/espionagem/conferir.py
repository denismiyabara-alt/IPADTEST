"""Audita blocos JA gravados: fatia pelo beats.json, transcreve com o Whisper e pontua com o portao.
Nao regera nada. Rodar na pasta do episodio:  python3 ../conferir.py b0 b1 ...   (sai 1 se alguma frase reprovar)
"""
import json, os, sys
import soundfile as sf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from portao import MIN_OK, nota_portao  # noqa: E402

ASR = os.environ.get("VOZ_ASR", "mlx-community/whisper-large-v3-mlx")


def auditar(bloco):
    import mlx_whisper
    meta = json.load(open(f"voz_{bloco}.beats.json"))
    a, sr = sf.read(f"voz_{bloco}.wav")
    ruins, ouvidos = [], []
    print(f"\n=== {bloco}  ({meta['dur']:.1f}s, {len(meta['frases'])} frases)")
    for f in meta["frases"]:
        sf.write("/tmp/_esp_aud.wav", a[int(f["ini"] * sr):int(f["fim"] * sr)], sr)
        ouv = mlx_whisper.transcribe("/tmp/_esp_aud.wav", path_or_hf_repo=ASR, language="pt")["text"].strip()
        sc = nota_portao(f["texto"], ouv)
        print(f"  {'OK ' if sc >= MIN_OK else '!! '}[{sc:.2f}] {f['texto'][:50]:<52} -> {ouv[:50]}")
        if sc < MIN_OK:
            ruins.append((f["texto"], sc, ouv))
        ouvidos.append({"texto": f["texto"], "ouvido": ouv, "score": round(sc, 3)})
    json.dump(ouvidos, open(f"ouvido_{bloco}.json", "w"), ensure_ascii=False, indent=1)
    for t, sc, o in ruins:
        print(f"    !! [{sc:.2f}] {t}\n           ouvido: {o}")
    return ruins


if __name__ == "__main__":
    raise SystemExit(1 if sum(len(auditar(b)) for b in sys.argv[1:]) else 0)
