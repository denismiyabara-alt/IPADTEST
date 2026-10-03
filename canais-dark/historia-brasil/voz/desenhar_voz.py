"""Desenha a voz do canal com o Qwen3-TTS VoiceDesign (mlx_audio, no Mac) e fixa a voz-mestra.
Nenhum áudio de pessoa real entra aqui: a voz nasce da descrição em voz/descricao.txt.

Rode com o Python do ambiente do mlx_audio (o mesmo que o synth usa), de dentro de canais-dark/historia-brasil:

    ~/.venvs/voice-clone/bin/python voz/desenhar_voz.py candidatas --n 20    # ~20 amostras, sementes 0..19
    ~/.venvs/voice-clone/bin/python voz/desenhar_voz.py mestra --semente 7   # fixa a escolhida
    ~/.venvs/voice-clone/bin/python voz/desenhar_voz.py mestra --de-candidata 7   # alternativa: usa a amostra tal como saiu

`candidatas` grava voz/candidatas/cand_SS.wav e um ouvido.tsv (o que o Whisper entendeu e a nota do
mesmo portão do synth). Ouça, escolha UMA e rode `mestra`. A voz-mestra é o que o modelo Base clona em
todo episódio (HB_MODO=mestra): o timbre fica igual de um vídeo para o outro.
Variáveis: HB_MODELO_DESIGN (padrão mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16), HB_LANG (portuguese).
"""
import argparse
import hashlib
import os
import shutil
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
CANAL = os.path.dirname(AQUI)
MODELO = os.environ.get("HB_MODELO_DESIGN", "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16")
LANG = os.environ.get("HB_LANG", "portuguese")
ASR = "mlx-community/whisper-large-v3-mlx"

# frase de teste: tem pergunta, ironia, pausa e um número por extenso (o que o canal faz o tempo todo)
AMOSTRA = ("Em mil novecentos e quatro, o governo resolveu vacinar a cidade inteira. "
           "Sem explicar nada pra ninguém. O que poderia dar errado?")
# texto da voz-mestra (~25 s): neutro, sem número difícil, com frase curta e frase longa
MESTRA_TXT = ("Boa noite. Hoje a gente vai abrir uma pasta velha do arquivo. "
              "Tem carimbo, tem assinatura e tem muita coisa que ninguém te contou na escola. "
              "A gente lê o documento, confere a data e só depois conta a história. "
              "Combinado? Então pega um café, que essa é comprida.")


def descricao():
    with open(os.path.join(AQUI, "descricao.txt"), encoding="utf-8") as f:
        return " ".join(l.strip() for l in f if l.strip() and not l.lstrip().startswith("#"))


def gerar(modelo, texto, semente, saida):
    import mlx.core as mx
    import numpy as np
    import soundfile as sf
    mx.random.seed(semente)
    partes = [np.array(r.audio) for r in modelo.generate_voice_design(text=texto, instruct=descricao(), language=LANG)]
    audio = np.concatenate(partes)
    sf.write(saida, audio, modelo.sample_rate)
    return len(audio) / modelo.sample_rate


def nota(texto, wav):
    """Mesmo portão do synth (texto e números), para descartar amostra embolada."""
    import mlx_whisper
    sys.path.insert(0, os.path.join(CANAL, "revolta-da-vacina"))
    ns = {}
    exec(open(os.path.join(CANAL, "revolta-da-vacina", "synth_voz.py"), encoding="utf-8").read().split("def gerar")[0], ns)
    ouvido = mlx_whisper.transcribe(wav, path_or_hf_repo=ASR, language="pt")["text"].strip()
    return ns["nota_portao"](texto, ouvido), ouvido


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("acao", choices=["candidatas", "mestra"])
    ap.add_argument("--n", type=int, default=20)
    ap.add_argument("--semente", type=int)
    ap.add_argument("--de-candidata", type=int)
    a = ap.parse_args()
    dest = os.path.join(AQUI, "candidatas")
    os.makedirs(dest, exist_ok=True)
    mestra = os.path.join(AQUI, "voz-mestra.wav")

    if a.acao == "mestra" and a.de_candidata is not None:
        orig = os.path.join(dest, f"cand_{a.de_candidata:02d}.wav")
        shutil.copy(orig, mestra)
        open(os.path.join(AQUI, "voz-mestra.txt"), "w", encoding="utf-8").write(AMOSTRA)
        print(f"voz-mestra.wav = {orig}\nsha256 {sha256(mestra)}\nAnote no VOZ.md: modelo {MODELO}, semente {a.de_candidata}, texto = AMOSTRA")
        return

    from mlx_audio.tts.utils import load_model
    modelo = load_model(MODELO)
    if a.acao == "candidatas":
        linhas = ["semente\tnota\tsegundos\touvido"]
        for s in range(a.n):
            wav = os.path.join(dest, f"cand_{s:02d}.wav")
            dur = gerar(modelo, AMOSTRA, s, wav)
            sc, ouvido = nota(AMOSTRA, wav)
            linhas.append(f"{s}\t{sc:.2f}\t{dur:.1f}\t{ouvido}")
            print(f"  cand_{s:02d}.wav  [{sc:.2f}] {dur:4.1f}s  {ouvido[:60]}")
        open(os.path.join(dest, "ouvido.tsv"), "w", encoding="utf-8").write("\n".join(linhas) + "\n")
        print(f"\nOuça as de nota >= 0.90 em {dest} e escolha UMA (critérios no VOZ.md).")
    else:
        if a.semente is None:
            sys.exit("use --semente N (a candidata escolhida) ou --de-candidata N")
        dur = gerar(modelo, MESTRA_TXT, a.semente, mestra)
        sc, ouvido = nota(MESTRA_TXT, mestra)
        open(os.path.join(AQUI, "voz-mestra.txt"), "w", encoding="utf-8").write(MESTRA_TXT)
        print(f"voz-mestra.wav: {dur:.1f}s, portão {sc:.2f}\nouvido: {ouvido}\nsha256 {sha256(mestra)}")
        print("Compare de ouvido com a candidata: o timbre tem de ser o mesmo. Se mudou, use --de-candidata.")
        print(f"Anote no VOZ.md: modelo {MODELO}, semente {a.semente}, data, sha256.")


if __name__ == "__main__":
    main()
