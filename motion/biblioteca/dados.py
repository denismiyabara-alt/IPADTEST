"""Monta os JSON de exemplo da biblioteca a partir de dado REAL e já conferido, sem digitar número à mão.

  dy-caixa   Ações com maior DY de caixa em 12 meses: tabela `indicador` (dy_caixa) do site-ativos, com os mesmos
             filtros e a mesma ordem da página saida/acoes/ranking/maiores-dy-de-caixa/ (CVM + B3 COTAHIST).
  cotistas   FIIs com mais cotistas, ago/2025 → ago/2026: tabela `fii_mensal` do site-ativos (informe mensal
             entregue à CVM), os 10 FIIs da cobertura do site (cache/selecao.json).
  megasena   "Pra onde vai o seu R$ 6": a divisão da arrecadação da Mega-Sena (Lei 13.756/2018, art. 16), lida do
             fact-check do Faz a Conta (pautas/megasena-factcheck.md) e conferida contra o quadro "Números
             conferidos" do megasena/roteiro.md (prêmio bruto 43,79% = R$ 2,63, status conferido).

Uso (de motion/):
  python3 biblioteca/dados.py dy-caixa  -o exemplos/barras-dy-caixa-16x9.json
  python3 biblioteca/dados.py cotistas  --formato 9:16 -o exemplos/barras-cotistas-9x16.json
  python3 biblioteca/dados.py megasena  --peca rosca --estilo fazaconta -o exemplos/rosca-megasena-fazaconta-16x9.json
"""
import argparse, datetime as dt, json, os, re, sqlite3, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MOTION = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(MOTION, "comum"))
from estilo import fmt_br  # noqa: E402


def _achar(env, candidatos, marca):
    for c in [os.environ.get(env)] + candidatos:
        if c and os.path.exists(os.path.join(c, marca)):
            return c
    return candidatos[0]


SITE_ATIVOS = _achar("IEC_SITE_ATIVOS", [os.path.join(os.path.dirname(MOTION), "site-ativos"),
                                         "/home/user/IPADTEST/site-ativos", os.path.expanduser("~/IPADTEST/site-ativos")],
                     os.path.join("cache", "dados.sqlite"))
FAZ_A_CONTA = _achar("FAZ_A_CONTA", ["/home/user/faz-a-conta", os.path.expanduser("~/faz-a-conta"),
                                     os.path.join(os.path.dirname(os.path.dirname(MOTION)), "faz-a-conta")],
                     os.path.join("megasena", "roteiro.md"))


def _db():
    p = os.path.join(SITE_ATIVOS, "cache", "dados.sqlite")
    if not os.path.exists(p):
        raise SystemExit(f"sem {p}: rode o site-ativos (python3 -m iec_ativos baixar && ... calcular)")
    return sqlite3.connect(p)


def _origem(arquivo):
    return {"arquivo": arquivo, "gerado_em": dt.datetime.now().isoformat(timespec="seconds")}


# ---------------------------------------------------------------- DY de caixa (ações)
def dy_caixa():
    """-> lista [(ticker, dy_em_pct, fonte, data_preco, periodo)] na ordem da página do site."""
    con = _db()
    q = """select i.ticker, i.valor, i.fonte, i.data_preco, i.periodo_contabil from indicador i
           where i.nome='dy_caixa' and i.status='ok' order by i.valor desc, i.ticker"""
    return [(t, v * 100, f, dp, pc) for t, v, f, dp, pc in con.execute(q).fetchall()]


def montar_dy_caixa(a):
    rows = dy_caixa()
    if a.top:
        rows = rows[:a.top]
    data_preco, periodo = rows[0][3], rows[0][4]
    itens = [{"rotulo": t, "valor": round(v, 6)} for t, v, _, _, _ in rows]
    destaque = a.destaque or rows[0][0]
    return {
        "peca": "barras", "estilo": a.estilo, "formato": a.formato, "duracao": a.duracao,
        "titulo": a.titulo or "DY de caixa em 12 meses",
        "kicker": "Ações · dividendos e JCP pagos ÷ valor de mercado",
        "fonte": "Fonte: CVM (DFC, 12 meses até " + _br(periodo) + ") e B3 (COTAHIST, " + _br(data_preco) + ")",
        "unidade": {"prefixo": "", "sufixo": "%", "casas": 1},
        "ordem": "desc", "destaque": destaque, "rotulo_placar": f"{destaque} · DY de caixa",
        "ativos": True,
        "criterio": ("Critério: as 10 ações de maior volume na B3 cobertas pelo site; volume ≥ R$ 1 mi/dia, lucro em "
                     "12 meses, dado com menos de 6 meses. Ordem só pelo número."),
        "som": {"pouso": "impact-bass-1"},
        "itens": itens,
        "_origem": _origem("site-ativos/cache/dados.sqlite (indicador dy_caixa) = saida/acoes/ranking/maiores-dy-de-caixa/"),
    }


# ---------------------------------------------------------------- cotistas (FIIs)
def cotistas(data_ref):
    con = _db()
    selecao = json.load(open(os.path.join(SITE_ATIVOS, "cache", "selecao.json")))
    out = {}
    for f in selecao.get("fiis", []):
        r = con.execute("select cotistas, versao, data_entrega from fii_mensal where cnpj=? and data_ref=?",
                        (f["cnpj"], data_ref)).fetchone()
        if r and r[0]:
            out[f["ticker"]] = (int(r[0]), r[1], r[2])
    return out


def montar_cotistas(a):
    antes, depois = cotistas(a.antes), cotistas(a.depois)
    comuns = [t for t in depois if t in antes]
    comuns.sort(key=lambda t: -depois[t][0])
    comuns = comuns[:a.top or 8]
    destaque = a.destaque or max(comuns, key=lambda t: depois[t][0] / antes[t][0])
    m = lambda iso: f"{['jan','fev','mar','abr','mai','jun','jul','ago','set','out','nov','dez'][int(iso[5:7]) - 1]}/{iso[:4]}"
    return {
        "peca": "barras", "estilo": a.estilo, "formato": a.formato, "duracao": a.duracao,
        "titulo": a.titulo or "FIIs com mais cotistas",
        "kicker": "Fundos imobiliários · número de cotistas",
        "fonte": f"Fonte: CVM (informe mensal de FII, {m(a.antes)} e {m(a.depois)})",
        "unidade": {"prefixo": "", "sufixo": "", "casas": 0},
        "ordem": "desc", "destaque": destaque, "rotulo_placar": f"{destaque} · cotistas",
        "momentos": [m(a.antes), m(a.depois)], "variacao": "pct",
        "ativos": True,
        "criterio": (f"Critério: os {len(comuns)} maiores, em cotistas, dos 10 FIIs de maior volume na B3 cobertos pelo "
                     "site. Ordem só pelo número de cotistas."),
        "som": {"pouso": "impact-bass-1"},
        "itens": [{"rotulo": t, "antes": antes[t][0], "valor": depois[t][0]} for t in comuns],
        "_origem": _origem(f"site-ativos/cache/dados.sqlite (fii_mensal, cotistas, {a.antes} e {a.depois})"),
    }


# ---------------------------------------------------------------- Mega-Sena (Faz a Conta)
# rótulo na tela <- nome no fact-check
MEGA_ROTULOS = [("prêmio", "Prêmio (com IR)"), ("custeio Caixa", "Caixa e lotéricas"),
                ("seguridade", "Seguridade social"), ("FNSP", "Segurança pública"), ("esporte", "Esporte"),
                ("Funpen", "Presídios (Funpen)"), ("FNC", "Cultura (FNC)"), ("COB", "Comitê Olímpico"),
                ("CPB", "Comitê Paralímpico")]


def _num(s):
    return float(s.replace(".", "").replace(",", "."))


def megasena():
    """-> (fatias [(rotulo, pct)], aposta, premio_reais_conferido, fontes). Lê o fact-check e o quadro do roteiro."""
    fc = open(os.path.join(FAZ_A_CONTA, "pautas", "megasena-factcheck.md")).read()
    rot = open(os.path.join(FAZ_A_CONTA, "megasena", "roteiro.md")).read()
    quadro = rot.split("## Números conferidos", 1)[1].split("\n## ", 1)[0]
    linhas = {c[1]: c for c in ([x.strip() for x in l.split("|")] for l in quadro.splitlines() if l.startswith("|")) if len(c) > 4}
    for k in ("aposta", "premio-bruto"):
        if linhas.get(k, [""] * 5)[4].strip() != "conferido":
            raise SystemExit(f"'{k}' não está 'conferido' no quadro do megasena/roteiro.md")
    aposta = _num(re.search(r"R\$ ([\d.,]+)", linhas["aposta"][2]).group(1))
    m = re.search(r"([\d,]+)% = R\$ ([\d,]+)", linhas["premio-bruto"][2])
    premio_pct, premio_reais = _num(m.group(1)), _num(m.group(2))
    m2 = re.search(r"PREMIO BRUTO ([\d,]+)%", fc)
    if _num(m2.group(1)) != premio_pct:
        raise SystemExit("prêmio bruto do fact-check difere do quadro do roteiro")
    dest = re.search(r"Destinacoes: (.+)", fc).group(1)
    pct = {"prêmio": premio_pct}
    for nome in ("seguridade", "FNSP", "esporte", "COB", "CPB", "FNC", "Funpen", "custeio Caixa"):
        pct[nome] = _num(re.search(re.escape(nome) + r" ([\d,]+)%", dest).group(1))
    fatias = [(rotulo, pct[nome]) for nome, rotulo in MEGA_ROTULOS]
    fontes = {"roteiro": "faz-a-conta/megasena/roteiro.md (Números conferidos: aposta, premio-bruto)",
              "factcheck": "faz-a-conta/pautas/megasena-factcheck.md (26/09/2026): Destinacoes"}
    return fatias, aposta, premio_reais, fontes


def montar_megasena(a):
    fatias, aposta, premio_reais, fontes = megasena()
    base = {
        "estilo": a.estilo, "formato": a.formato, "duracao": a.duracao,
        "titulo": a.titulo or f"Pra onde vão os seus R$ {fmt_br(aposta, 0)}",
        "kicker": "Mega-Sena · cada aposta simples",
        "fonte": "Fonte: Lei 13.756/2018, art. 16",
        "som": {"pouso": "impact-bass-1"},
        "_origem": _origem(fontes["roteiro"] + "; " + fontes["factcheck"]),
    }
    if a.peca == "rosca":
        return {"peca": "rosca", **base, "destaque": fatias[0][0], "casas": 2,
                "centro": {"valor": aposta, "unidade": {"prefixo": "R$ ", "sufixo": "", "casas": 2},
                           "rotulo": "a sua aposta", "rotulo_final": "viram prêmio"},
                "_conferido": {"premio_reais": premio_reais},
                "fatias": [{"rotulo": r, "pct": p} for r, p in fatias]}
    return {"peca": "barras", **base, "unidade": {"prefixo": "", "sufixo": "%", "casas": 2},
            "ordem": "desc", "destaque": fatias[0][0], "rotulo_placar": "da aposta viram prêmio",
            "itens": [{"rotulo": r, "valor": p} for r, p in fatias]}


def _br(iso):
    return f"{iso[8:10]}/{iso[5:7]}/{iso[:4]}"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("conjunto", choices=["dy-caixa", "cotistas", "megasena"])
    ap.add_argument("--peca", choices=["barras", "rosca"], default="barras")
    ap.add_argument("--estilo", choices=["iec", "fazaconta"], default="iec")
    ap.add_argument("--formato", choices=["16:9", "9:16"], default="16:9")
    ap.add_argument("--duracao", type=float, default=8.0)
    ap.add_argument("--titulo")
    ap.add_argument("--destaque")
    ap.add_argument("--top", type=int)
    ap.add_argument("--antes", default="2025-08-01")
    ap.add_argument("--depois", default="2026-08-01")
    ap.add_argument("-o", "--saida", required=True)
    a = ap.parse_args(argv)
    d = {"dy-caixa": montar_dy_caixa, "cotistas": montar_cotistas, "megasena": montar_megasena}[a.conjunto](a)
    os.makedirs(os.path.dirname(os.path.abspath(a.saida)), exist_ok=True)
    json.dump(d, open(a.saida, "w"), ensure_ascii=False, indent=1)
    n = len(d.get("itens") or d.get("fatias"))
    print(f"ok: {a.saida} ({d['peca']}, {n} itens; origem: {d['_origem']['arquivo']})")


if __name__ == "__main__":
    main()
