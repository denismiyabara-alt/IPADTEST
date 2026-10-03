"""Locucao do canal de historia: Qwen3-TTS (mlx_audio, local no Mac) + portao de conferencia (Whisper).
Voz NOVA, desenhada por descricao (VoiceDesign). Nenhum audio de pessoa real entra aqui.

Dois modos (HB_MODO):
  mestra (padrao)  o modelo Base clona a voz-mestra.wav, que e SINTETICA: saiu do VoiceDesign
                   (voz/desenhar_voz.py) e foi escolhida de ouvido. Mesmo timbre em todo episodio.
  design           o VoiceDesign fala direto a partir da descricao (VOZ_DESCRICAO). O timbre varia
                   de frase para frase; serve para testar a descricao, nao para episodio.

O modelo nao e deterministico: gera ate TAKES takes por frase, transcreve cada um com o Whisper
e fica com o que bate com o texto (texto E numeros). Abaixo de MIN_OK a frase e marcada "!!".
Uso: python3 synth_voz.py b0        |  python3 synth_voz.py --teste (autoteste do portao)
"""
import subprocess, os, sys, re, unicodedata, difflib
from fractions import Fraction
import numpy as np, soundfile as sf

AQUI = os.path.dirname(os.path.abspath(globals().get("__file__", "synth_voz.py")))
CANAL = os.path.dirname(AQUI)
PY_GEN = os.path.expanduser(os.environ.get("HB_PY_GEN", "~/.venvs/voice-clone/bin/python"))
MODO = os.environ.get("HB_MODO", "mestra")
# Nomes dos modelos como PARAMETRO: conferidos no pacote mlx-audio 0.5.7 e no Hugging Face em 03/10/2026
# (config.json do VoiceDesign: tts_model_type = voice_design; idiomas incluem "portuguese").
MODELO_DESIGN = os.environ.get("HB_MODELO_DESIGN", "mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16")
MODELO_BASE = os.environ.get("HB_MODELO_BASE", "Qwen/Qwen3-TTS-12Hz-1.7B-Base")
LANG = os.environ.get("HB_LANG", "portuguese")   # "pt" nao e codigo do Qwen3-TTS: cai no automatico
MESTRA = os.environ.get("HB_VOZ_MESTRA", os.path.join(CANAL, "voz", "voz-mestra.wav"))
# A descricao oficial esta em ../voz/descricao.txt (e copiada no VOZ.md). So atributos acusticos.
def _descricao():
    with open(os.path.join(CANAL, "voz", "descricao.txt"), encoding="utf-8") as f:
        return " ".join(l.strip() for l in f if l.strip() and not l.startswith("#"))
SR, TAKES, MIN_OK = 24000, 3, 0.90
ASR = "mlx-community/whisper-large-v3-mlx"
NUMS = {"zero","um","uma","dois","duas","tres","quatro","cinco","seis","sete","oito","nove",
        "dez","onze","doze","treze","quatorze","catorze","quinze","dezesseis","dezessete",
        "dezoito","dezenove","vinte","trinta","quarenta","cinquenta","sessenta","setenta",
        "oitenta","noventa","cem","cento","mil","milhao","milhoes","reais","real"}

def norm(s):
    """Minusculas sem acento. Preserva separadores ENTRE digitos: '.' de milhar e
    ',' de decimal — senao 'R$ 6,00' vira '600' e '31.600,00' vira lixo.
    'por cento' e '%' viram marcador, nao o numeral 'cento'."""
    s = unicodedata.normalize("NFD", s.lower())
    s = s.replace("%", " porcento ")
    # "por cento" so e porcentagem quando NAO e seguido de outro numeral:
    #   "quarenta e tres por cento"        -> porcentagem
    #   "dividido por cento e cinquenta"   -> numeral (cento = 100)
    s = re.sub(r"\bpor\s+cento\b(?!\s+e\s+\w)", " porcento ", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    out = []
    for i, c in enumerate(s):
        if c.isalnum() or c.isspace():
            out.append(c)
        elif c in "-\u2013\u2014/$":            # "$": "R$4,00" -> "r 4,00", senao o r gruda no numero
            out.append(" ")                      # "Mega-Sena" -> "mega sena", como o ASR escreve
        elif c in ",." and 0 < i < len(s)-1 and s[i-1].isdigit() and s[i+1].isdigit():
            out.append(c)                        # '.' milhar e ',' decimal, cada um o seu
    return " ".join("".join(out).split())

VAL = {"zero":0,"um":1,"uma":1,"dois":2,"duas":2,"tres":3,"quatro":4,"cinco":5,"seis":6,
       "sete":7,"oito":8,"nove":9,"dez":10,"onze":11,"doze":12,"treze":13,"quatorze":14,
       "catorze":14,"quinze":15,"dezesseis":16,"dezessete":17,"dezoito":18,"dezenove":19,
       "vinte":20,"trinta":30,"quarenta":40,"cinquenta":50,"sessenta":60,"setenta":70,
       "oitenta":80,"noventa":90,"cem":100,"cento":100,
       "duzentos":200,"trezentos":300,"quatrocentos":400,"quinhentos":500,"seiscentos":600,
       "setecentos":700,"oitocentos":800,"novecentos":900,
       "duzentas":200,"trezentas":300,"quatrocentas":400,"quinhentas":500,"seiscentas":600,
       "setecentas":700,"oitocentas":800,"novecentas":900}
MULT = {"mil":1000, "milhao":10**6, "milhoes":10**6, "bilhao":10**9, "bilhoes":10**9}
PALAVRA_NUM = set(VAL) | set(MULT) | {"reais","real","r","rs","centavos","porcento"}  # "r" = sobra do R$

def so_texto(s):
    """Texto sem os numeros — pega palavra trocada//inventada."""
    return " ".join(w for w in norm(s).split()
                    if not w.replace(",", "").replace(".", "").isdigit()
                    and w not in PALAVRA_NUM and w != "e")   # "e" liga numeral: sai dos dois lados

def _moeda(w):
    """'6,00'->'6' (centavo zerado nao se fala) | '2,60'->'260' | '31.600,00'->'31600'."""
    inteiro, _, cent = w.partition(",")
    inteiro = inteiro.replace(".", "")            # separador de milhar
    return inteiro if set(cent) <= {"0"} or not cent else inteiro + cent

def _e_num(w):
    return w.replace(",", "").replace(".", "").isdigit() or w in VAL or w in MULT

_FIM_DE_FRASE = re.compile(r"[.!?;:]+(?!\d)")   # '.' entre digitos (6.000, 6,71) nao quebra
_VIRGULA = re.compile(r",(?=\s)")                 # virgula + espaco: fronteira MOLE

def _e_num_tok(w):
    return w.replace(",", "").replace(".", "").isdigit() or w in VAL or w in MULT

def _alternativas(s, limite=8):
    """Leituras numericas possiveis da frase. Fim de frase SEMPRE separa numeros
    ('seis. Setenta e um' nao e 6,71). Virgula + espaco entre dois numeros pode separar
    ('R$ 6,00, 71%') ou nao ('dois mil, trezentas e trinta e duas'; 'um, dois, tres'):
    devolve as duas versoes de cada juncao (ate 2**limite combinacoes)."""
    seq, juntas = [], []                    # juntas: indices i em que seq[i] e seq[i+1] podem se juntar
    for trecho in _FIM_DE_FRASE.split(s):
        pedacos = _VIRGULA.split(trecho)
        for k, ped in enumerate(pedacos):
            runs = _corridas_trecho(ped)
            if k and runs and seq and ultimo_num and _e_num_tok((norm(ped).split() or [""])[0]):
                juntas.append(len(seq) - 1)
            seq += runs
            ws = norm(ped).split()
            ultimo_num = bool(ws) and _e_num_tok(ws[-1])
        ultimo_num = False
    juntas = juntas[:limite]
    alts = []
    for mask in range(1 << len(juntas)):
        unir = {j for b, j in enumerate(juntas) if mask >> b & 1}
        alt, atual = [], list(seq[0]) if seq else None
        for i in range(1, len(seq)):
            if i - 1 in unir:
                atual += seq[i]
            else:
                alt.append(atual); atual = list(seq[i])
        if atual is not None:
            alt.append(atual)
        alts.append([_leituras(r) for r in alt])
    return alts or [[]]

def _num_bate_alt(texto, ouvido):
    """Melhor _num_bate entre as leituras possiveis dos dois lados."""
    return max(_num_bate(a, b) for a in _alternativas(texto) for b in _alternativas(ouvido))

def _corridas(s):
    """Fatia a frase em corridas de tokens numericos (o 'e' liga, nao quebra).
    'um real e cinco centavos' fica numa corrida so, com '|' separando reais de centavos.
    Fim de frase QUEBRA a corrida: 'Hoje custa seis. Setenta e um por cento' sao dois numeros
    (6 e 71%), e nao 6,71% -- se o ASR ouviu um decimal, a pausa sumiu e o sentido mudou."""
    corr = []
    for trecho in _FIM_DE_FRASE.split(s):
        corr += _corridas_trecho(trecho)
    return corr

def _corridas_trecho(s):
    corr, atual = [], []
    ws = norm(s).split()
    for i, w in enumerate(ws):
        if _e_num(w):
            atual.append(w)
        elif w == "e" and atual:
            atual.append(w)
        elif (w in ("real", "reais") and atual and "|" not in atual and i + 2 < len(ws) and ws[i + 1] == "e"
              and _e_num(ws[i + 2]) and "centavo" in " ".join(ws[i + 2:i + 6])):
            atual.append("|")
        else:
            if atual: corr.append([x for x in atual if x != "e"]); atual = []
    if atual: corr.append([x for x in atual if x != "e"])
    return corr

def _valor(w, antes_de_escala):
    """Valor de um token em digitos para a leitura composta. Decimal seguido de escala e decimal
    de verdade: '26,6 bilhoes' = 26.600.000.000 (o ASR escreve assim o 'vinte e seis bilhoes e
    seiscentos milhoes' falado). Sem escala, segue o _moeda ('3,50' -> 350, como antes)."""
    inteiro, _, cent = w.partition(",")
    inteiro = inteiro.replace(".", "")
    if antes_de_escala and cent.strip("0"):
        return Fraction(int(inteiro + cent), 10 ** len(cent))
    return int(_moeda(w) or 0)

def _composto(run):
    """So a leitura composta de uma corrida ('sessenta e tres' -> 63, '1' -> 1)."""
    total, parcial = 0, 0
    for w in run:
        if w in MULT:
            parcial = max(parcial, 1) * MULT[w]; total += parcial; parcial = 0
        elif w in VAL:
            parcial += VAL[w]
        else:
            parcial += int(_moeda(w) or 0)
    return total + parcial

def _leituras(run):
    """Uma corrida numerica tem estas leituras legitimas em portugues falado:
      concatenada  — 'tres e quarenta' = R$ 3,40 -> '340'
      composta     — 'cento e cinquenta e seis'  -> '156'
      reais+centavos — 'dois e sessenta e tres' = R$ 2,63 -> '263';
                       'um real e cinco centavos' = R$ 1,05 -> '105'
    Nao da pra escolher uma sem quebrar as outras, entao devolve todas."""
    if "|" in run:
        k = run.index("|")
        return {f"{_composto(run[:k])}{_composto(run[k + 1:]):02d}"}
    leit = _leituras_base(run)
    if len(run) > 1 and all(w in VAL for w in run):
        for k in range(1, len(run)):
            cent = sum(VAL[w] for w in run[k:])
            if cent < 100 and all(VAL[w] < 100 for w in run[k:]):
                leit.add(f"{_composto(run[:k])}{cent:02d}")
    return leit

def _leituras_base(run):
    """Leituras concatenada e composta. Uma corrida numerica tem DUAS leituras legitimas em portugues falado:
      concatenada  — 'tres e quarenta' = R$ 3,40 -> '340'
      composta     — 'cento e cinquenta e seis'  -> '156'
    Nao da pra escolher uma sem quebrar a outra, entao devolve as duas.
    Na composta, escala menor depois de maior soma: 'vinte e seis bilhoes e seiscentos milhoes'
    = 26.600.000.000 = '26,6 bilhoes'."""
    concat, total, parcial = [], 0, 0
    for i, w in enumerate(run):
        if w.replace(",", "").replace(".", "").isdigit():
            prox = run[i + 1] if i + 1 < len(run) else ""
            concat.append(_moeda(w)); parcial += _valor(w, prox in MULT)
        elif w in MULT:
            parcial = max(parcial, 1) * MULT[w]; total += parcial; parcial = 0
        else:
            concat.append(str(VAL[w])); parcial += VAL[w]
    comp = total + parcial
    comp = str(int(comp)) if comp == int(comp) else str(float(comp))
    return {"".join(concat), comp}

def so_numeros(s):
    """Conjunto de leituras por corrida numerica, em ordem.
    NAO pode ser ignorado: o produto do canal e o numero."""
    return [_leituras(run) for run in _corridas(s)]

def _num_bate(a, b):
    """Corridas casam se, uma a uma, alguma leitura coincide.
    Corrida que e so 'um'/'uma'/'1' sai dos dois lados: o ASR poe e tira artigo
    ('viram premio' -> 'vira um premio'), e 'um' sozinho nao e o numero da frase."""
    a = [x for x in a if x != {"1"}]
    b = [x for x in b if x != {"1"}]
    if len(a) != len(b): return 0.0
    if not a: return 1.0
    return sum(1.0 for x, y in zip(a, b) if x & y) / len(a)

def _esperados(txt):
    """Texto original e, se o dicionario tiver a 3a coluna, a forma que o ASR escreve
    ('Segundo a EY' -> 'Segundo a Ernst Young'): a sigla expandida nao reprova sozinha."""
    # o conferir.py executa so o topo deste arquivo, sem __file__: ai a pasta do episodio e o cwd
    aqui = os.path.abspath(globals().get("__file__", "synth_qwen_clone.py"))
    sys.path.insert(0, os.path.dirname(os.path.dirname(aqui)))
    try:
        from pronuncia import textos_esperados
    except ImportError:
        return [txt]
    return textos_esperados(txt)

def nota_portao(txt, ouvido):
    """min(texto, numeros) contra o melhor dos textos esperados."""
    melhor = 0.0
    for alvo in _esperados(txt):
        st = difflib.SequenceMatcher(None, so_texto(alvo), so_texto(ouvido)).ratio()
        sn = _num_bate_alt(alvo, ouvido)
        melhor = max(melhor, min(st, sn))
    return melhor


def _mestra():
    if not os.path.exists(MESTRA):
        raise FileNotFoundError(f"falta {MESTRA}. Gere com: python3 ../voz/desenhar_voz.py (ver COMO-RODAR.md)")
    txt = os.path.splitext(MESTRA)[0] + ".txt"
    return MESTRA, (open(txt, encoding="utf-8").read().strip() if os.path.exists(txt) else None)

def comando(txt, tag, saida_dir="/tmp"):
    """Linha de comando do mlx_audio para uma frase (separada para o teste conferir sem rodar o modelo)."""
    base = [PY_GEN, "-m", "mlx_audio.tts.generate", "--lang_code", LANG, "--text", txt,
            "--file_prefix", tag, "--output_path", saida_dir]
    if MODO == "design":
        return base + ["--model", MODELO_DESIGN, "--instruct", _descricao()]
    ref, ref_txt = _mestra()
    return base + ["--model", MODELO_BASE, "--ref_audio", ref] + (["--ref_text", ref_txt] if ref_txt else [])

def gerar(txt, tag):
    saida = f"/tmp/{tag}_000.wav"
    if os.path.exists(saida):
        os.remove(saida)                       # nao deixa um take velho passar por novo
    p = subprocess.run(comando(txt, tag), capture_output=True, text=True)
    if p.returncode != 0 or not os.path.exists(saida):
        cauda = "\n".join(((p.stderr or "") + (p.stdout or "")).strip().splitlines()[-15:])
        raise RuntimeError(f"mlx_audio nao gerou {saida} (codigo {p.returncode}). Saida do mlx_audio:\n{cauda}")
    a, sr = sf.read(saida)                     # sem deslocar o tom: a voz ja nasce com o timbre do canal
    if a.ndim > 1: a = a.mean(1)
    if sr != SR:
        import scipy.signal as ss; a = ss.resample(a, int(len(a)*SR/sr))
    # limpa ANTES do portao: o ASR julga o som que vai pro video
    from suavizar_bordas import limpar, tirar_estouro
    return tirar_estouro(limpar(a, SR), SR)[0]

def para_voz(txt):
    """Texto que vai pro TTS: o dicionario de pronuncia (../pronuncia.txt) troca a grafia so aqui.
    O portao abaixo compara o ouvido com o texto ORIGINAL ('Zanin'), nao com o da voz ('Zanín')."""
    sys.path.insert(0, CANAL)
    try:
        from pronuncia import aplicar
    except ImportError:
        return txt
    return aplicar(txt)

def melhor_take(txt, i, asr):
    alvo, cands = norm(txt), []
    voz = para_voz(txt)
    for k in range(TAKES):
        a = gerar(voz, f"_q{i}_{k}")
        sf.write(f"/tmp/_qc{i}_{k}.wav", a, SR)
        ouvido = norm(asr(f"/tmp/_qc{i}_{k}.wav"))
        score = nota_portao(txt, ouvido)       # texto E numeros tem que passar: numero errado reprova sozinho
        cands.append((score, a, ouvido))
        if score >= 0.97: break            # ja esta bom, nao gasta mais take
    cands.sort(key=lambda c: -c[0])
    s, a, ouvido = cands[0]
    flag = "OK " if s >= MIN_OK else "!! "
    print(f"  {flag}[{s:.2f}] {txt[:44]:<46} -> {ouvido[:46]}")
    return a, s

PIII = "{PIII}"
def bip(dur=.42):
    """o 'piii' da censura: 1 kHz, fade de 5 ms nas pontas"""
    t = np.arange(int(dur*SR))/SR; b = .32*np.sin(2*np.pi*1000*t)
    n = int(.005*SR); b[:n] *= np.linspace(0, 1, n); b[-n:] *= np.linspace(1, 0, n)
    return b

def falar(txt, i, asr):
    """Frase -> (audio, nota, [instantes do piii relativos ao inicio da frase]).
    '{PIII}' marca o palavrao: gera o antes e o depois separados e poe o bip no meio."""
    if PIII not in txt:
        a, sc = melhor_take(txt, i, asr); return a, sc, []
    pedacos, notas, bips, cur = [], [], [], 0.0
    for j, parte in enumerate(txt.split(PIII)):
        if j:                                   # antes de cada parte (menos a 1a) vem um bip
            b = np.concatenate([np.zeros(int(.06*SR)), bip(), np.zeros(int(.06*SR))])
            bips.append(round(cur + .06, 3)); pedacos.append(b); cur += len(b)/SR
        parte = parte.strip(" ,")
        if parte:
            a, sc = melhor_take(parte, 100*i + j, asr); pedacos.append(a); notas.append(sc); cur += len(a)/SR
    return np.concatenate(pedacos), min(notas), bips

def build(script, out, lead=0.35):
    """Alem do wav, grava <out>.beats.json com o inicio/fim EXATO de cada frase.
    O synth ja sabe onde cada frase comeca — passar whisper por cima seria adivinhar
    o que ja e sabido, e erra em numero por extenso."""
    import mlx_whisper, json
    asr = lambda p: mlx_whisper.transcribe(p, path_or_hf_repo=ASR, language="pt")["text"]
    partes, ruins, marcas = [np.zeros(int(lead*SR))], [], []
    cursor = lead
    for i, (txt, gap) in enumerate(script):
        a, s, bips = falar(txt, i, asr)
        partes.append(a)
        marcas.append({"i": i, "texto": txt, "piii": bips,
                       "ini": round(cursor, 3), "fim": round(cursor + len(a)/SR, 3)})
        cursor += len(a)/SR + gap
        if s < MIN_OK: ruins.append((txt, s))
        if gap: partes.append(np.zeros(int(gap*SR)))
    audio = np.concatenate(partes)
    from suavizar_bordas import desbaquear
    audio, _ = desbaquear(audio, SR)           # o 'bum' da ultima silaba (0,2-0,6 s antes do fim)
    sf.write(out, audio, SR)
    json.dump({"dur": round(len(audio)/SR, 3), "frases": marcas},
              open(out.replace(".wav", ".beats.json"), "w"), ensure_ascii=False, indent=1)
    if ruins:
        print("\n  ATENCAO — frases que nao passaram no portao (reescrever):")
        for t, s in ruins: print(f"    [{s:.2f}] {t}")
    return len(audio)/SR


def _autoteste():
    """Portao de qualidade: metrica por caractere, corte 0.90. Calibrado nestes 6 casos.
    Rodar com: python3 synth_qwen_clone.py --teste"""
    casos = [("Seis reais. É o preço de um café.", "e o preco de um cafe",                 False),
             ("Seis reais. É o preço de um café.", "seis reais e o preco de um cafe",      True),
             ("Os outros três e quarenta",          "os outros 340",                        True),
             ("Mas de cada seis reais, dois e sessenta voltam como prêmio.",
              "precisa mas de cada seis reais dois e 60 voltam como premio",                False),
             ("dois e sessenta",                    "dois e setenta",                       False),
             ("também vão pra algum lugar.",        "tambem vao para algum lugar",          True),
             ("Uma aposta da Mega-Sena custa seis reais.",
              "uma aposta da mega sena custa R$ 6,00",                                       True),
             ("Mas de cada seis reais, dois e sessenta voltam como prêmio.",
              "mas de cada R$ 6,00 R$ 2,60 voltam como premio",                              True),
             ("dois e sessenta",                    "R$ 2,70",                              False),
             ("Comprar todas custaria trezentos milhões de reais.",
              "comprar todas custaria 300 milhoes de reais",                                 True),
             ("Cento e cinquenta e seis chances por ano.",
              "156 chances por ano",                                                         True),
             ("dá trezentos e vinte mil anos.",     "da 320 mil anos",                       True),
             ("O Homo sapiens tem trezentos mil anos de existência.",
              "homo sapiens tem 300 mil anos de existencia",                                 True),
             ("Cinquenta milhões dividido por cento e cinquenta e seis",
              "50 milhoes dividido por 156",                                                 True),
             ("dá trezentos e vinte mil anos.",     "da 420 mil anos",                       False),
             ("vira prêmio: quarenta e três por cento.",
              "vira premio, 43%.",                                                            True),
             ("Trinta e um mil e seiscentos reais.", "R$ 31.600,00.",                         True),
             ("parcelado em duzentas e quarenta vezes",
              "parcelado em 240 vezes",                                                       True),
             ("Trinta e um mil e seiscentos reais.", "R$ 41.600,00.",                        False),
             ("Depois de cem giros, sobram menos de quatro reais.",
              "depois de 100 giros sobram menos de R$4,00",                                  True)]
    for alvo, ouvido, deve in casos:
        st = difflib.SequenceMatcher(None, so_texto(alvo), so_texto(ouvido)).ratio()
        sn = _num_bate(so_numeros(alvo), so_numeros(ouvido))
        assert (min(st, sn) >= MIN_OK) == deve, \
            f"portao errou em: {ouvido!r}  (txt={st:.2f} num={sn:.2f})"
    print(f"autoteste: {len(casos)}/{len(casos)} ok")



CASOS_EPISODIO = [   # numeros deste roteiro, como o Whisper costuma escrever
    ("Em mil novecentos e quatro, o Rio de Janeiro passou uma semana em pé de guerra.",
     "em 1904 o rio de janeiro passou uma semana em pe de guerra", True),
    ("De mil oitocentos e noventa e sete a mil novecentos e seis, uns quatro mil imigrantes morreram na cidade por causa de doença.",
     "de 1897 a 1906 uns 4 mil imigrantes morreram na cidade por causa de doenca", True),
    ("De mil oitocentos e noventa e sete a mil novecentos e seis, uns quatro mil imigrantes morreram na cidade por causa de doença.",
     "de 1897 a 1906 uns 4.000 imigrantes morreram na cidade por causa de doenca", True),
    ("De mil oitocentos e noventa e sete a mil novecentos e seis, uns quatro mil imigrantes morreram na cidade por causa de doença.",
     "de 1897 a 1916 uns 4 mil imigrantes morreram na cidade por causa de doenca", False),
    ("Em trinta e um de outubro de mil novecentos e quatro, saiu a lei: vacinação contra a varíola obrigatória, no país inteiro.",
     "em 31 de outubro de 1904 saiu a lei vacinacao contra a variola obrigatoria no pais inteiro", True),
    ("Aí, entre dez e dezesseis de novembro, o Rio explodiu.", "ai entre 10 e 16 de novembro o rio explodiu", True),
    ("No fim, foram cerca de trinta mortos e mais de novecentas pessoas detidas.",
     "no fim foram cerca de 30 mortos e mais de 900 pessoas detidas", True),
    ("No fim, foram cerca de trinta mortos e mais de novecentas pessoas detidas.",
     "no fim foram cerca de 13 mortos e mais de 900 pessoas detidas", False),
]

def _autoteste_episodio():
    for alvo, ouvido, deve in CASOS_EPISODIO:
        s = nota_portao(alvo, ouvido)
        assert (s >= MIN_OK) == deve, f"portao errou em {ouvido!r} ({s:.2f})"
    print(f"autoteste do episodio: {len(CASOS_EPISODIO)}/{len(CASOS_EPISODIO)} ok")


if __name__ == "__main__":
    if "--teste" in sys.argv:
        _autoteste(); _autoteste_episodio(); raise SystemExit
    if len(sys.argv) > 1 and sys.argv[1].startswith("b"):
        from blocos import BLOCOS
        alvo = sys.argv[1]
        print(f"\nvoz_{alvo}.wav: {build(BLOCOS[alvo], f'voz_{alvo}.wav'):.2f}s")
        raise SystemExit
    sys.exit(__doc__)
