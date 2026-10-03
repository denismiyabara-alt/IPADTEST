"""Portao de conferencia da voz: compara o que o Whisper ouviu com o texto pretendido.
Texto E numeros tem que bater (min das duas notas >= MIN_OK). Puro Python: roda e testa sem Mac.
Datas e numeros por extenso no roteiro; o ASR escreve em algarismos ("mil novecentos e sessenta" -> "1960"):
as leituras composta e concatenada cobrem os dois lados.
    python3 portao.py --teste
"""
import os, re, sys, unicodedata, difflib
from fractions import Fraction

MIN_OK = 0.90

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
            out.append(" ")                      # "Mercedes-Benz" -> "mercedes benz", como o ASR escreve
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
MULT = {"mil":1000, "milhao":10**6, "milhoes":10**6, "bilhao":10**9, "bilhoes":10**9, "trilhao":10**12, "trilhoes":10**12}
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
    """Texto original e, se o pronuncia.txt tiver a 3a coluna, a forma que o ASR escreve."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
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


def _autoteste():
    """Casos do episodio 1 (datas por extenso x algarismos do Whisper). Corte 0,90."""
    casos = [
        ("Onze de maio de mil novecentos e sessenta.", "11 de maio de 1960.", True),
        ("Onze de maio de mil novecentos e sessenta.", "11 de maio de 1961.", False),
        ("Onze de maio de mil novecentos e sessenta.", "onze de maio de mil novecentos e sessenta", True),
        ("Em vinte e três de junho de mil novecentos e sessenta, o Conselho aprovou a Resolução cento e trinta e oito.",
         "Em 23 de junho de 1960, o Conselho aprovou a Resolução 138.", True),
        ("Em vinte e três de junho de mil novecentos e sessenta, o Conselho aprovou a Resolução cento e trinta e oito.",
         "Em 23 de junho de 1960, o Conselho aprovou a Resolução 139.", False),
        ("Foram oito votos a favor, nenhum contra e duas abstenções.", "Foram 8 votos a favor, nenhum contra e 2 abstenções.", True),
        ("Foram oito votos a favor, nenhum contra e duas abstenções.", "Foram 9 votos a favor, nenhum contra e 2 abstenções.", False),
        ("Em cerca de oito semanas, mais de quatrocentas mil pessoas foram deportadas, quase todas para Auschwitz.",
         "Em cerca de 8 semanas, mais de 400 mil pessoas foram deportadas, quase todas para Auschwitz.", True),
        ("Em cerca de oito semanas, mais de quatrocentas mil pessoas foram deportadas, quase todas para Auschwitz.",
         "Em cerca de 8 semanas, mais de 40 mil pessoas foram deportadas, quase todas para Auschwitz.", False),
        ("Eram bodas de prata.", "Eram bodas de prata.", True),
        # limite conhecido: troca de UMA letra em frase curta ("bodas" -> "bolas") passa (0,95). Frase curta: ouvir no Mac.
        ("Os documentos dele dizem que ele se chama Ricardo Klement.",
         "Os documentos dele dizem que ele se chama Ricardo Clement.", True),
        ("Adolf Eichmann foi enforcado na prisão de Ramla, na noite de trinta e um de maio para primeiro de junho de mil novecentos e sessenta e dois.",
         "Adolf Eichmann foi enforcado na prisão de Ramla, na noite de 31 de maio para primeiro de junho de 1962.", True),
    ]
    for alvo, ouvido, deve in casos:
        st = difflib.SequenceMatcher(None, so_texto(alvo), so_texto(ouvido)).ratio()
        sn = _num_bate_alt(alvo, ouvido)
        assert (min(st, sn) >= MIN_OK) == deve, f"portao errou em: {ouvido!r}  (txt={st:.2f} num={sn:.2f})"
    print(f"autoteste do portao: {len(casos)}/{len(casos)} ok")


if __name__ == "__main__":
    if "--teste" in sys.argv:
        _autoteste()
