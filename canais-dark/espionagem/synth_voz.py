"""Locucao do canal com Qwen3-TTS VoiceDesign: a voz nasce de uma DESCRICAO em texto.
Nao usa audio de referencia de ninguem (nada de clone). Ver VOZ.md.

O modelo e nao-deterministico entre textos: cada frase gera TAKES, cada take e transcrito pelo
Whisper e passa pelo portao (portao.py: texto E numeros >= 0,90). Opcional: portao de timbre
(semelhanca com a voz-mestra.wav do proprio canal, se o resemblyzer estiver instalado).

    python3 ../synth_voz.py --candidatas          # 12 vozes candidatas (sementes 1..12) do mesmo paragrafo
    python3 ../synth_voz.py --mestra              # gera voz-mestra.wav com a SEMENTE escolhida (VOZ.md)
    python3 ../synth_voz.py b0 [b1 ...]           # grava voz_bN.wav + voz_bN.beats.json (rodar NA pasta do episodio)

Tudo que pode mudar no Mac esta em variaveis de ambiente (nomes abaixo). CONFERIR NO MAC:
  - MODELO: nome do repo MLX do VoiceDesign (o README do mlx-audio em 03/10/2026 cita
    mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16, com model.generate_voice_design(text, language, instruct)).
  - IDIOMA: a string de idioma que o modelo aceita para portugues ("Portuguese" no padrao do Qwen3-TTS).
"""
import json, os, sys
import numpy as np
import soundfile as sf

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
from portao import MIN_OK, norm, nota_portao  # noqa: E402

MODELO = os.environ.get("VOZ_MODELO", "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16")
IDIOMA = os.environ.get("VOZ_IDIOMA", "Portuguese")
SEMENTE = int(os.environ.get("VOZ_SEMENTE", "7"))          # trocar pela escolhida no --candidatas (anotar em VOZ.md)
ASR = os.environ.get("VOZ_ASR", "mlx-community/whisper-large-v3-mlx")
SR, TAKES = 24000, int(os.environ.get("VOZ_TAKES", "3"))
TIMBRE_MIN = float(os.environ.get("VOZ_TIMBRE_MIN", "0.80"))  # calibrar no 1o teste (VOZ.md)

# Texto EXATO da instrucao (copiado em VOZ.md; se mudar aqui, mudar la e regravar tudo).
INSTRUCAO = (
    "Adult male narrator, about 55 years old, native Brazilian Portuguese speaker with a neutral accent "
    "(no regional accent, not European Portuguese). Low, grave, warm voice with a slightly husky texture "
    "and medium-low pitch. Calm, serious documentary delivery at a slow, measured pace, with clear pauses "
    "between sentences. Precise diction, restrained emotion, steady volume. Not a movie-trailer voice, "
    "not a radio announcer, no dramatic emphasis, no whispering, no sarcasm, no smile in the voice."
)

PARAGRAFO_TESTE = ("Onze de maio de mil novecentos e sessenta. Já é noite em San Fernando, nos arredores de "
                   "Buenos Aires. Os documentos dele dizem que ele se chama Ricardo Klement.")

_modelo = None


def _carregar():
    global _modelo
    if _modelo is None:
        from mlx_audio.tts.utils import load_model
        _modelo = load_model(MODELO)
    return _modelo


def para_voz(txt):
    """So o texto do TTS passa pelo pronuncia.txt; o portao compara com o original."""
    try:
        from pronuncia import aplicar
    except ImportError:
        return txt
    return aplicar(txt)


def gerar(txt, semente):
    import mlx.core as mx
    mx.random.seed(semente)
    partes = [np.array(r.audio, dtype=np.float32)
              for r in _carregar().generate_voice_design(text=txt, language=IDIOMA, instruct=INSTRUCAO)]
    a = np.concatenate(partes) if partes else np.zeros(1, np.float32)
    sr = getattr(_modelo, "sample_rate", SR)
    if sr != SR:
        import scipy.signal as ss
        a = ss.resample(a, int(len(a) * SR / sr)).astype(np.float32)
    from suavizar_bordas import limpar, tirar_estouro
    return tirar_estouro(limpar(a, SR), SR)[0]


def _timbre():
    """Semelhanca com a voz-mestra.wav (resemblyzer). Sem mestra ou sem a lib: portao de timbre desligado."""
    mestra = os.path.join(AQUI, "voz-mestra.wav")
    try:
        from resemblyzer import VoiceEncoder, preprocess_wav
    except ImportError:
        return None
    if not os.path.exists(mestra):
        return None
    enc = VoiceEncoder()
    ref = enc.embed_utterance(preprocess_wav(mestra))
    return lambda a: float(np.dot(ref, enc.embed_utterance(preprocess_wav(a, source_sr=SR))))


def melhor_take(txt, asr, timbre):
    voz, cands = para_voz(txt), []
    for k in range(TAKES):
        a = gerar(voz, SEMENTE + 1000 * k)
        sf.write("/tmp/_esp_take.wav", a, SR)
        ouvido = norm(asr("/tmp/_esp_take.wav"))
        nota = nota_portao(txt, ouvido)
        tim = timbre(a) if timbre else 1.0
        cands.append((min(nota, 1.0 if tim >= TIMBRE_MIN else 0.0), nota, tim, a, ouvido))
        if nota >= 0.97 and tim >= TIMBRE_MIN:
            break
    cands.sort(key=lambda c: -c[0])
    s, nota, tim, a, ouvido = cands[0]
    print(f"  {'OK ' if s >= MIN_OK else '!! '}[{nota:.2f} timbre {tim:.2f}] {txt[:44]:<46} -> {ouvido[:46]}")
    return a, s


def build(frases, out, lead=0.35):
    """frases = [(texto, pausa)]. Grava out (.wav) e out.beats.json com inicio/fim EXATO de cada frase."""
    import mlx_whisper
    asr = lambda p: mlx_whisper.transcribe(p, path_or_hf_repo=ASR, language="pt")["text"]
    timbre = _timbre()
    if timbre is None:
        print("  (portao de timbre desligado: falta voz-mestra.wav ou o pacote resemblyzer)")
    partes, ruins, marcas, cursor = [np.zeros(int(lead * SR))], [], [], lead
    for i, (txt, gap) in enumerate(frases):
        a, s = melhor_take(txt, asr, timbre)
        partes.append(a)
        marcas.append({"i": i, "texto": txt, "ini": round(cursor, 3), "fim": round(cursor + len(a) / SR, 3)})
        cursor += len(a) / SR + gap
        partes.append(np.zeros(int(gap * SR)))
        if s < MIN_OK:
            ruins.append((txt, s))
    from suavizar_bordas import desbaquear
    audio, _ = desbaquear(np.concatenate(partes), SR)
    sf.write(out, audio, SR)
    json.dump({"dur": round(len(audio) / SR, 3), "frases": marcas},
              open(out.replace(".wav", ".beats.json"), "w"), ensure_ascii=False, indent=1)
    if ruins:
        print("\n  ATENCAO: frases que nao passaram no portao (regerar ou reescrever):")
        for t, s in ruins:
            print(f"    [{s:.2f}] {t}")
    return len(audio) / SR


if __name__ == "__main__":
    args = sys.argv[1:]
    if args[:1] == ["--candidatas"]:
        os.makedirs("candidatas", exist_ok=True)
        for s in range(1, 13):
            SEMENTE = s
            sf.write(f"candidatas/semente_{s:02d}.wav", gerar(para_voz(PARAGRAFO_TESTE), s), SR)
            print(f"candidatas/semente_{s:02d}.wav")
    elif args[:1] == ["--mestra"]:
        # 3 a 5 min de fala neutra do proprio canal: o roteiro do ep. 1 inteiro serve de texto
        import roteiro
        r = roteiro.ler(os.environ.get("VOZ_TEXTO_MESTRA", "ep01-eichmann/roteiro.md"))
        txt = " ".join(t for t, _ in r.blocos[r.ordem[0]] + r.blocos[r.ordem[1]])
        sf.write(os.path.join(AQUI, "voz-mestra.wav"), gerar(para_voz(txt), SEMENTE), SR)
        print(f"voz-mestra.wav (semente {SEMENTE})")
    elif args:
        from blocos import BLOCOS
        for b in args:
            print(f"\nvoz_{b}.wav: {build(BLOCOS[b], f'voz_{b}.wav'):.1f}s")
    else:
        sys.exit(__doc__)
