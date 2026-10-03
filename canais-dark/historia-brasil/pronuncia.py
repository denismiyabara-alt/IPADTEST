"""Dicionário de pronúncia da voz: pronuncia.txt na raiz (palavra<TAB>grafia_pra_voz[<TAB>como_o_asr_escreve]).

Só o texto que vai para o TTS passa por aqui. Roteiro, legenda, cartela e conferência
continuam com a grafia original, e o conferir.py compara o ouvido com ela.
"""
import re
from pathlib import Path

ARQ = Path(__file__).resolve().parent / "pronuncia.txt"


def carregar_ouvido(arq=ARQ):
    """3ª coluna opcional: como o ASR escreve a palavra falada ('EY' falado 'Érnest Iângue'
    vira 'Ernst Young' na transcrição). {palavra minúscula: forma_ouvida}."""
    mapa = {}
    try:
        linhas = Path(arq).read_text(encoding="utf-8").splitlines()
    except OSError:
        return mapa
    for l in linhas:
        if not l.strip() or l.lstrip().startswith("#"):
            continue
        partes = [p.strip() for p in l.split("\t")]
        if len(partes) >= 3 and partes[0] and partes[2]:
            mapa[partes[0].lower()] = partes[2]
    return mapa


def textos_esperados(texto, mapa_ouvido=None):
    """O que o portão aceita ouvir: o texto original e, se o dicionário tiver a 3ª coluna,
    o original com a palavra trocada pela forma ouvida ('Segundo a EY' e 'Segundo a Ernst Young')."""
    mapa_ouvido = carregar_ouvido() if mapa_ouvido is None else mapa_ouvido
    alt = aplicar(texto, mapa_ouvido) if mapa_ouvido else texto
    return [texto] if alt == texto else [texto, alt]


def carregar(arq=ARQ):
    """{palavra minúscula: grafia_pra_voz}. Linha com # ou sem as duas colunas é ignorada."""
    mapa = {}
    try:
        linhas = Path(arq).read_text(encoding="utf-8").splitlines()
    except OSError:
        return mapa
    for l in linhas:
        if not l.strip() or l.lstrip().startswith("#"):
            continue
        partes = [p.strip() for p in l.split("\t")]
        if len(partes) >= 2 and partes[0] and partes[1] and "?" not in partes[1]:
            mapa[partes[0].lower()] = partes[1]
    return mapa


def _caixa(original, nova):
    if original.isupper() and len(original) > 1:
        # sigla soletrada ("bê ene dê ésse") fica como escrita: em CAIXA ALTA a voz poderia soletrar de novo
        return nova if " " in nova else nova.upper()
    if original[:1].isupper():
        return nova[:1].upper() + nova[1:]
    return nova[:1].lower() + nova[1:]


def aplicar(texto, mapa=None):
    """Troca cada palavra do dicionário (inteira, sem caixa, com ou sem 's' de plural) pela grafia da voz."""
    mapa = carregar() if mapa is None else mapa
    if not mapa:
        return texto
    alternativas = "|".join(sorted((re.escape(p) for p in mapa), key=len, reverse=True))
    padrao = re.compile(rf"(?<![\wÀ-ÿ])({alternativas})(s?)(?![\wÀ-ÿ])", re.IGNORECASE)
    return padrao.sub(lambda m: _caixa(m.group(1), mapa[m.group(1).lower()]) + m.group(2), texto)
