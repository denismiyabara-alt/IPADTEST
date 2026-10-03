"""Prova de que a voz do canal nao imita ninguem: semelhanca de locutor (resemblyzer, local, nada sai do Mac)
entre a voz-mestra.wav do canal e cada voz de comparacao. Os caminhos das vozes de comparacao vem de
variavel de ambiente (nunca gravados no repositorio):
    VOZ_COMPARAR="/caminho/voz_pessoal.wav,/caminho/voz_outro_canal.wav" python3 comparar_voz.py
Sai 1 se alguma semelhanca passar do LIMIAR (calibrar no 1o teste e anotar em VOZ.md).
"""
import os, sys
import numpy as np

LIMIAR = float(os.environ.get("VOZ_LIMIAR_PARECIDA", "0.75"))


def main():
    from resemblyzer import VoiceEncoder, preprocess_wav
    enc = VoiceEncoder()
    mestra = enc.embed_utterance(preprocess_wav(os.path.join(os.path.dirname(os.path.abspath(__file__)), "voz-mestra.wav")))
    ruim = 0
    for k, p in enumerate(x for x in os.environ.get("VOZ_COMPARAR", "").split(",") if x):
        s = float(np.dot(mestra, enc.embed_utterance(preprocess_wav(p))))
        ok = s < LIMIAR
        ruim += not ok
        print(f"  comparacao {k + 1}: semelhanca {s:.3f} {'ok (diferente)' if ok else '!! PARECIDA DEMAIS: trocar de semente/descricao'}")
    return ruim


if __name__ == "__main__":
    raise SystemExit(1 if main() else 0)
