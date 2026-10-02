"""Funções comuns aos patches de texto (sem rede).

O WordPress guarda o post em content.raw (texto do editor) e a API pública devolve content.rendered (raw passado por
wpautop + wptexturize: <p> automáticos, aspas curvas, travessões, reticências, entidades HTML). Para um "de" funcionar
nos dois, ele precisa ser um trecho "seguro": dentro de um só nó de texto e sem os caracteres que o wptexturize mexe.
"""
import html
import re

# caracteres que o wptexturize cria/troca, ou que viram entidade
PROIBIDOS = set("\"'“”‘’«»–—…×&<>\n\r\t ")
TRADUCAO = {
    "“": '"', "”": '"', "„": '"', "″": '"', "«": '"', "»": '"',
    "‘": "'", "’": "'", "′": "'",
    "–": "-", "—": "-", "−": "-",
    "…": "...", "×": "x", " ": " ",
}


def normalizar(s):
    """Entidades -> caracteres, aspas/travessões/reticências -> ASCII, espaços colapsados (casamento tolerante)."""
    s = html.unescape(s)
    s = "".join(TRADUCAO.get(c, c) for c in s)
    s = s.replace("--", "-")
    return re.sub(r"\s+", " ", s)


def normalizar_com_mapa(s):
    """Como normalizar(), devolvendo também, para cada caractere da saída, o índice de origem em s."""
    out, mapa = [], []
    i = 0
    while i < len(s):
        m = re.match(r"&(#\d+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]*);", s[i:])
        if m:
            ch = html.unescape(m.group(0))
            largura = len(m.group(0))
        else:
            ch, largura = s[i], 1
        ch = "".join(TRADUCAO.get(c, c) for c in ch)
        for c in ch:
            if c.isspace():
                if out and out[-1] == " ":
                    continue
                c = " "
            if c == "-" and out and out[-1] == "-":
                continue
            out.append(c)
            mapa.append(i)
        i += largura
    mapa.append(len(s))
    return "".join(out), mapa


# '>' é aceito: o raw pode ter '>' ou '&gt;'; o gerador grava as duas formas (campo "alternativas")
PERMITIDOS_COM_ALTERNATIVA = set(">")


def problemas_do_de(de):
    """Lista de motivos que tornam o 'de' inseguro para casar com o raw."""
    p = []
    ruins = sorted({c for c in de if c in PROIBIDOS and c not in PERMITIDOS_COM_ALTERNATIVA})
    if ruins:
        p.append("caracteres que o WordPress transforma: " + " ".join(repr(c) for c in ruins))
    if "--" in de or "..." in de:
        p.append("contém -- ou ...")
    if re.search(r"\d\s*x\s*\d", de):
        p.append("contém NxN (vira ×)")
    if de != de.strip():
        p.append("espaço nas pontas")
    if len(de) < 12:
        p.append("curto demais (menos de 12 caracteres)")
    if "[" in de and "]" in de:
        p.append("parece shortcode")
    return p


def nos_de_texto(rendered):
    """Lista de (inicio, fim) dos nós de texto do HTML (fora das tags)."""
    nos = []
    pos = 0
    for m in re.finditer(r"<[^>]*>", rendered):
        if m.start() > pos:
            nos.append((pos, m.start()))
        pos = m.end()
    if pos < len(rendered):
        nos.append((pos, len(rendered)))
    return nos


def localizar_no_rendered(rendered, de):
    """Procura 'de' (texto real) dentro de UM nó de texto do rendered.
    Devolve (n_ocorrencias_no_texto_todo, de_rendered_da_primeira_ou_None)."""
    total = html.unescape(rendered).count(de)
    primeira = None
    for a, b in nos_de_texto(rendered):
        trecho = rendered[a:b]
        txt, mapa = _unescape_com_mapa(trecho)
        k = txt.find(de)
        if k >= 0:
            primeira = trecho[mapa[k]:mapa[k + len(de)]]
            break
    return total, primeira


def _unescape_com_mapa(s):
    out, mapa = [], []
    i = 0
    while i < len(s):
        m = re.match(r"&(#\d+|#x[0-9a-fA-F]+|[a-zA-Z][a-zA-Z0-9]*);", s[i:])
        if m:
            ch, largura = html.unescape(m.group(0)), len(m.group(0))
        else:
            ch, largura = s[i], 1
        for c in ch:
            out.append(c)
            mapa.append(i)
        i += largura
    mapa.append(len(s))
    return "".join(out), mapa


def casar_exato(raw, de):
    return raw.count(de)


def casar_tolerante(raw, de):
    """Procura de normalizado no raw normalizado. Devolve lista de trechos do raw original que casariam."""
    alvo = normalizar(de)
    norm, mapa = normalizar_com_mapa(raw)
    achados = []
    k = norm.find(alvo)
    while k >= 0:
        achados.append(raw[mapa[k]:mapa[k + len(alvo)]])
        k = norm.find(alvo, k + 1)
    return achados


def alternativas(de):
    """Formas do 'de' com entidade, para o raw que guardou '&gt;' em vez de '>'."""
    alt = de.replace(">", "&gt;")
    return [alt] if alt != de else []


def escolher_de(raw, troca):
    """Devolve (de_que_casa, contagem). Tenta o 'de' e as alternativas; prefere a que casa o número esperado."""
    esperado = troca.get("n", 1)
    opcoes = [troca["de"]] + troca.get("alternativas", [])
    contagens = [(o, raw.count(o)) for o in opcoes]
    for o, n in contagens:
        if n == esperado:
            return o, n
    return max(contagens, key=lambda x: x[1])
