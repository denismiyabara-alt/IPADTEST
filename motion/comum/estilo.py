"""Estilo, formato de número e validação comuns às peças da biblioteca de motion.

Dois estilos:
  "iec"        Investir e Coçar. Fonte de verdade ÚNICA: a PAL e as fontes do molde Burry
               (edicao-skill/molde-burry/broll/gerar.py). Nada é copiado: este módulo lê o arquivo (sem executá-lo,
               pois ele abre o plano.json ao ser importado) e extrai o dict PAL e as famílias/pesos usados no CSS.
               Hoje: bg #f6f2e8, ink #1c1a17, red #d6362b, gray #79756c, faint #d9d4c7; Montserrat (700/800) nos
               rótulos e Archivo Black nos números e títulos; traço que "ferve" (filtro boil).
               Caminho: $IEC_MOLDE_BURRY_GERAR, senão ../edicao-skill/molde-burry/broll/gerar.py a partir de motion/.
  "fazaconta"  Faz a Conta (faz-a-conta/*/build_hf.py, PALETA): mesmas famílias, traço que ferve e a marca-d'água
               FAZ A CONTA no canto. O teste confere as cores contra o build_hf.py do repo faz-a-conta.

As peças (barras, rosca) não têm cor fixa no código: tudo vem de ESTILOS[estilo]["cores"].
"""
import ast, math, os, re

COMUM = os.path.dirname(os.path.abspath(__file__))
MOTION = os.path.dirname(COMUM)
GERAR_MOLDE = os.environ.get("IEC_MOLDE_BURRY_GERAR") or os.path.join(
    os.path.dirname(MOTION), "edicao-skill", "molde-burry", "broll", "gerar.py")

# arquivo de cada família/peso no @fontsource (o @fontsource só dá o arquivo; família e peso vêm do molde)
ARQUIVO_FONTE = {
    ("Archivo Black", 400): "@fontsource/archivo-black/files/archivo-black-latin-400-normal.woff2",
    ("Montserrat", 700): "@fontsource/montserrat/files/montserrat-latin-700-normal.woff2",
    ("Montserrat", 800): "@fontsource/montserrat/files/montserrat-latin-800-normal.woff2",
}


def ler_molde(caminho=GERAR_MOLDE):
    """-> (PAL, {(família, peso)}) lidos do gerar.py do molde Burry, sem executá-lo."""
    if not os.path.exists(caminho):
        raise FileNotFoundError(f"não achei o gerar.py do molde Burry ({caminho}), a fonte de verdade do estilo iec. "
                                "Aponte IEC_MOLDE_BURRY_GERAR para ele.")
    src = open(caminho, encoding="utf-8").read()
    pal = None
    for no in ast.parse(src).body:
        if isinstance(no, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "PAL" for t in no.targets):
            v = no.value
            if isinstance(v, ast.Call) and getattr(v.func, "id", "") == "dict":
                pal = {k.arg: ast.literal_eval(k.value) for k in v.keywords}
            else:
                pal = ast.literal_eval(v)
    if not pal:
        raise ValueError(f"PAL não encontrada em {caminho}")
    fontes = {(fam, int(peso)) for peso, fam in
              re.findall(r"font:\s*(\d{3})\s+\d+px(?:/[\d.]+)?\s+'?(Montserrat|Archivo Black)'?", src)}
    return pal, fontes


def _estilo_iec():
    pal, fontes = ler_molde()
    faltam = sorted(f for f in fontes if f not in ARQUIVO_FONTE)
    if faltam:
        raise ValueError(f"o molde usa fontes sem arquivo mapeado em ARQUIVO_FONTE: {faltam}")
    return {
        "nome": "Investir e Coçar",
        "cores": dict(papel=pal["bg"], tinta=pal["ink"], cinza=pal["gray"], grade=pal["faint"], destaque=pal["red"]),
        "fontes": {f"{fam}-{peso}": (ARQUIVO_FONTE[(fam, peso)], fam, peso) for fam, peso in sorted(fontes)},
        "tipo": dict(TIPO),
        "titulo_espaco": "0",
        "marca": None,
        "boil": True,
    }


# papel tipográfico -> declaração CSS (o tamanho entra na página). Igual nos dois estilos: é o traço do molde
# Burry (.head/.big/.bv em Archivo Black, .rot/.bl em Montserrat 800, .card-f/.cap em Montserrat 700).
TIPO = {
    "titulo": "400 {px}px/1.08 'Archivo Black', sans-serif",
    "numero": "400 {px}px/1 'Archivo Black', sans-serif",
    "rotulo": "800 {px}px/1.1 Montserrat, sans-serif",
    "mono": "700 {px}px/1.25 Montserrat, sans-serif",
}

ESTILOS = {
    "iec": _estilo_iec(),
    "fazaconta": {
        "nome": "Faz a Conta",
        # PALETA do faz-a-conta/megasena/build_hf.py (o teste confere contra o arquivo)
        "cores": dict(papel="#f6f2e8", tinta="#1c1a17", cinza="#79756c", grade="#d9d4c7", destaque="#d6362b"),
        "fontes": {f"{fam}-{peso}": (arq, fam, peso) for (fam, peso), arq in ARQUIVO_FONTE.items()},
        "tipo": dict(TIPO),
        "titulo_espaco": "0",
        "marca": "FAZ A CONTA",
        "boil": True,
    },
}

FORMATOS = {"16:9": (1920, 1080), "9:16": (1080, 1920)}
MESES = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
AVISO_ATIVOS = "Não é recomendação de investimento."


class DadosInvalidos(ValueError):
    """Entrada errada. args[0] é a lista com todos os problemas encontrados."""


def fmt_br(v, casas):
    """1234567.891, 2 -> '1.234.567,89' (igual ao fmtBR do JS da página e ao do grafico_cotacao)."""
    s = f"{abs(v):,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-" if v < 0 and round(abs(v), casas) else "") + s


def texto_valor(v, unidade):
    return f"{unidade.get('prefixo', '')}{fmt_br(v, unidade.get('casas', 2))}{unidade.get('sufixo', '')}"


def esc(s):
    """Escapa para HTML e para o str.format do template."""
    return (str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
            .replace("{", "&#123;").replace("}", "&#125;"))


def misturar(c1, c2, f):
    """Cor entre c1 e c2 (hex #RRGGBB), f=0 -> c1, f=1 -> c2."""
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]
    b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x + (y - x) * f):02X}" for x, y in zip(a, b))


def rampa_cinza(estilo, n):
    """n tons entre a tinta e a grade, para as fatias/barras que não são a chave (sem cor nova)."""
    c = ESTILOS[estilo]["cores"]
    if n <= 1:
        return [misturar(c["tinta"], c["grade"], .35)]
    return [misturar(c["tinta"], c["grade"], .12 + .78 * k / (n - 1)) for k in range(n)]


def validar_base(d, erros, duracao=(5, 10)):
    """Campos comuns a todas as peças. Preenche os padrões em d (dict) e acumula problemas em erros."""
    d.setdefault("estilo", "iec")
    d.setdefault("formato", "16:9")
    d.setdefault("duracao", 8.0)
    d.setdefault("kicker", "")
    d.setdefault("som", {"pouso": "impact-bass-1"})
    d["unidade"] = {"prefixo": "", "sufixo": "", "casas": 2, **(d.get("unidade") or {})}
    for campo in ("titulo", "fonte"):
        if not isinstance(d.get(campo), str) or not d[campo].strip():
            erros.append(f"'{campo}' é obrigatório (texto)")
    if isinstance(d.get("fonte"), str) and d["fonte"].strip() and not d["fonte"].startswith("Fonte:"):
        erros.append("'fonte' deve começar com 'Fonte:' (regra do canal), ex.: 'Fonte: CVM'")
    if d["estilo"] not in ESTILOS:
        erros.append(f"'estilo' deve ser 'iec' ou 'fazaconta', veio {d['estilo']!r}")
    if d["formato"] not in FORMATOS:
        erros.append(f"'formato' deve ser 16:9 ou 9:16, veio {d['formato']!r}")
    lo, hi = duracao
    if isinstance(d["duracao"], bool) or not isinstance(d["duracao"], (int, float)) or not lo <= d["duracao"] <= hi:
        erros.append(f"'duracao' deve estar entre {lo} e {hi} s, veio {d['duracao']!r}")
    casas = d["unidade"]["casas"]
    if isinstance(casas, bool) or not isinstance(casas, int) or not 0 <= casas <= 4:
        erros.append("'unidade.casas' deve ser inteiro de 0 a 4")
    som = d["som"]
    if som not in (False, None) and not (isinstance(som, dict) and isinstance(som.get("pouso"), str)):
        erros.append("'som' deve ser false ou {'pouso': 'impact-bass-1' | caminho de arquivo}")
    return d


def numero_ok(v):
    return not isinstance(v, bool) and isinstance(v, (int, float)) and math.isfinite(v)
