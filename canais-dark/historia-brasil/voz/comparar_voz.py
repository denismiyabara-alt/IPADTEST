"""Mede a semelhança de locutor (ECAPA, SpeechBrain, local) entre a voz-mestra e outras gravações.
Serve para provar que a voz do canal NÃO é a voz do dono nem a do canal irmão.

    python3 voz/comparar_voz.py voz/voz-mestra.wav <referência do canal irmão> <um trecho já publicado do canal irmão> ...

Saída: similaridade de cosseno (−1 a 1). Critério do VOZ.md: abaixo de 0,50 contra cada referência
(ECAPA costuma dar > 0,70 para a mesma pessoa e < 0,40 para pessoas diferentes; o limiar de 0,50 é
uma margem, a calibrar no 1º uso comparando dois trechos da MESMA referência, que devem dar > 0,70).
Não baixe voz de famoso para comparar. Requer: pip install speechbrain torchaudio (no Mac, uma vez).
"""
import sys


def embedding(modelo, caminho):
    import torchaudio
    sinal, sr = torchaudio.load(caminho)
    if sr != 16000:
        sinal = torchaudio.functional.resample(sinal, sr, 16000)
    return modelo.encode_batch(sinal.mean(0, keepdim=True)).squeeze()


def main(args):
    if len(args) < 2:
        sys.exit(__doc__)
    import torch
    from speechbrain.inference.speaker import EncoderClassifier
    modelo = EncoderClassifier.from_hparams(source="speechbrain/spkrec-ecapa-voxceleb", savedir="/tmp/ecapa")
    base = embedding(modelo, args[0])
    pior = -1.0
    for outro in args[1:]:
        s = float(torch.nn.functional.cosine_similarity(base, embedding(modelo, outro), dim=0))
        pior = max(pior, s)
        print(f"{s:+.3f}  {outro}")
    print("OK: abaixo de 0,50 contra todas" if pior < .5 else "ATENÇÃO: perto demais de alguma referência; gere outra voz")
    return 0 if pior < .5 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
