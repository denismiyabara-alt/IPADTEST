"""Audita um bloco JA gerado: fatia pelo beats.json, transcreve e pontua com o portao.
Barato — nao regera nada. Use antes de renderizar, e depois de qualquer edicao de roteiro.
"""
import sys, json, difflib, numpy as np, soundfile as sf, mlx_whisper
ns = {}
exec(open("synth_voz.py").read().split("def gerar")[0], ns)
so_texto, so_numeros, _num_bate, MIN_OK = ns["so_texto"], ns["so_numeros"], ns["_num_bate"], ns["MIN_OK"]
nota_portao = ns["nota_portao"]
ASR = "mlx-community/whisper-large-v3-mlx"

def auditar(bloco):
    meta = json.load(open(f"voz_{bloco}.beats.json"))
    a, sr = sf.read(f"voz_{bloco}.wav")
    ruins, ouvidos = [], []
    print(f"\n=== {bloco}  ({meta['dur']:.1f}s, {len(meta['frases'])} frases)")
    for f in meta["frases"]:
        seg = a[int(f["ini"]*sr):int(f["fim"]*sr)]
        sf.write("/tmp/_aud.wav", seg, sr)
        ouv = mlx_whisper.transcribe("/tmp/_aud.wav", path_or_hf_repo=ASR, language="pt")["text"]
        alvo = f["texto"].replace("{PIII}", " ")          # o bip nao e palavra
        sc = nota_portao(alvo, ouv)
        flag = "OK " if sc >= MIN_OK else "!! "
        print(f"  {flag}[{sc:.2f}] {f['texto'][:50]:<52} -> {ouv.strip()[:50]}")
        if sc < MIN_OK: ruins.append((f["texto"], sc, ouv.strip()))
        ouvidos.append({"texto": f["texto"], "ouvido": ouv.strip(), "score": round(sc, 3)})
    # o que o ASR ouviu, inteiro: o reconferir.py repontua sem rodar o Whisper de novo
    json.dump(ouvidos, open(f"ouvido_{bloco}.json", "w"), ensure_ascii=False, indent=1)
    if ruins:
        print(f"\n  {len(ruins)} frase(s) reprovada(s) — regerar ou reescrever:")
        for t, sc, o in ruins: print(f"    [{sc:.2f}] {t}\n           ouvido: {o}")
    else:
        print("  todas passaram")
    return ruins

if __name__ == "__main__":
    total = sum(len(auditar(b)) for b in sys.argv[1:])
    raise SystemExit(1 if total else 0)
