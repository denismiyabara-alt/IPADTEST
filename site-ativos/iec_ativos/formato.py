"""Formatação em português do Brasil."""


def _milhar(s: str) -> str:
    inteiro, _, dec = s.partition(".")
    neg = inteiro.startswith("-")
    inteiro = inteiro.lstrip("-")
    grupos = []
    while len(inteiro) > 3:
        grupos.insert(0, inteiro[-3:])
        inteiro = inteiro[:-3]
    grupos.insert(0, inteiro)
    return ("-" if neg else "") + ".".join(grupos) + ("," + dec if dec else "")


def numero(v, casas=2) -> str:
    if v is None:
        return "—"
    return _milhar(f"{v:.{casas}f}")


def brl(v, casas=2) -> str:
    return "—" if v is None else "R$ " + numero(v, casas)


def brl_curto(v) -> str:
    if v is None:
        return "—"
    a = abs(v)
    if a >= 1e9:
        return f"R$ {numero(v / 1e9, 1)} bi"
    if a >= 1e6:
        return f"R$ {numero(v / 1e6, 1)} mi"
    if a >= 1e3:
        return f"R$ {numero(v / 1e3, 1)} mil"
    return brl(v)


def pct(v, casas=1) -> str:
    return "—" if v is None else numero(v * 100, casas) + "%"


def vezes(v, casas=1) -> str:
    return "—" if v is None else numero(v, casas) + "x"


def data_br(iso) -> str:
    if not iso:
        return "—"
    return f"{iso[8:10]}/{iso[5:7]}/{iso[:4]}"


def mes_br(iso) -> str:
    meses = ["jan", "fev", "mar", "abr", "mai", "jun", "jul", "ago", "set", "out", "nov", "dez"]
    return f"{meses[int(iso[5:7]) - 1]}/{iso[2:4]}" if iso else "—"


def inteiro(v) -> str:
    return "—" if v is None else numero(v, 0)
