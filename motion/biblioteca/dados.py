"""Monta os JSON de exemplo da biblioteca a partir de dado REAL e já conferido, sem digitar número à mão.

  dy-caixa   Ações com maior DY de caixa em 12 meses: tabela `indicador` (dy_caixa) do site-ativos, com os mesmos
             filtros e a mesma ordem da página saida/acoes/ranking/maiores-dy-de-caixa/ (CVM + B3 COTAHIST).
  cotistas   FIIs com mais cotistas, ago/2025 → ago/2026: tabela `fii_mensal` do site-ativos (informe mensal
             entregue à CVM), os 10 FIIs da cobertura do site (cache/selecao.json).
  megasena   "Pra onde vai o seu R$ 6": a divisão da arrecadação da Mega-Sena (Lei 13.756/2018, art. 16), lida do
             fact-check do Faz a Conta (pautas/megasena-factcheck.md) e conferida contra o quadro "Números
             conferidos" do megasena/roteiro.md (prêmio bruto 43,79% = R$ 2,63, status conferido).

Lote 2 (séries do BCB, lidas pelo grafico_cotacao/serie.py: SQLite do site-ativos → JSON cru do site-ativos →
cache próprio → API do BCB; o JSON guarda de onde saiu em `_origem`):
  copom      Selic (SGS 432) com os eventos do ciclo: a 1ª alta, o pico e o 1º corte, achados nas mudanças da
             própria série (cada mudança da meta é uma decisão do Copom). Peça: eventos.
  ipca       IPCA mensal (SGS 433) que vira o acumulado em 12 meses, CALCULADO do 433 e conferido mês a mês
             contra a SGS 13522 (diferença máxima 0,01 p.p.; senão, para). Peça: barra_linha.
  selic      a meta Selic de hoje (SGS 432), que vira o último ponto da série desde jan/2020. Peça: numero_linha.
  manchete-ipca  "Inflação em 12 meses cai para 4,22% em agosto": verbo, número e mês saem da SGS 13522.
             Peça: manchete.

Uso (de motion/):
  python3 biblioteca/dados.py dy-caixa  -o exemplos/barras-dy-caixa-16x9.json
  python3 biblioteca/dados.py cotistas  --formato 9:16 -o exemplos/barras-cotistas-9x16.json
  python3 biblioteca/dados.py megasena  --peca rosca --estilo fazaconta -o exemplos/rosca-megasena-fazaconta-16x9.json
  python3 biblioteca/dados.py copom     -o exemplos/eventos-selic-copom-16x9.json
  python3 biblioteca/dados.py ipca      -o exemplos/barra-linha-ipca-16x9.json
  python3 biblioteca/dados.py selic     --formato 9:16 -o exemplos/numero-linha-selic-9x16.json
  python3 biblioteca/dados.py manchete-ipca --formato 9:16 -o exemplos/manchete-ipca-9x16.json
"""
import argparse, datetime as dt, json, os, re, sqlite3, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
MOTION = os.path.dirname(AQUI)
sys.path.insert(0, os.path.join(MOTION, "comum"))
sys.path.insert(0, os.path.join(MOTION, "grafico_cotacao"))
from estilo import MESES, fmt_br  # noqa: E402
import serie as S  # noqa: E402  — leitura das séries do BCB (mesma do grafico_cotacao)


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


# ---------------------------------------------------------------- lote 2: séries do BCB
MESES_EXTENSO = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro",
                 "novembro", "dezembro"]


def _mes(iso):
    return f"{MESES[int(iso[5:7]) - 1]}/{iso[:4]}"


def bcb(serie, desde="2020-01-01", ate=None):
    """-> ([(iso, valor)], origem). Mesma leitura do grafico_cotacao/serie.py (sem rede se houver cache)."""
    return S.serie_bcb(serie, desde, ate)


def mudancas_selic(desde="2020-01-01"):
    """Cada mudança da meta (SGS 432) = uma decisão do Copom. -> [(data de vigência, nova meta, anterior)]."""
    pontos, _ = bcb(432, desde)
    out = []
    for (d0, v0), (d1, v1) in zip(pontos, pontos[1:]):
        if v1 != v0:
            out.append((d1, v1, v0))
    return out


def eventos_ciclo(desde, ate=None):
    """1ª alta e 1º corte de cada ciclo (mudança de sentido) e o início do pico, dentro do período."""
    mud = mudancas_selic("2020-01-01")
    ev, sentido = [], 0
    for d, v, v0 in mud:
        s = 1 if v > v0 else -1
        if s != sentido and desde <= d <= (ate or "9999"):
            ev.append({"data": d, "rotulo": f"{'1ª alta' if s > 0 else '1º corte'}: {fmt_br(v, 2)}%"})
        sentido = s
    pontos, _ = bcb(432, desde, ate)
    pico = max(v for _, v in pontos)
    inicio_pico = next(d for d, v, _ in mud if v == pico and desde <= d)
    ev.append({"data": inicio_pico, "rotulo": f"Pico: {fmt_br(pico, 2)}%"})
    return sorted(ev, key=lambda e: e["data"])


def montar_copom(a):
    import especificacao as E
    desde = a.desde or "2024-01-01"
    espec = {"serie": "SGS:432", "periodo": f"{desde}:", "rotulo": a.titulo or "Selic: da alta ao 1º corte",
             "kicker": "Meta da taxa Selic · decisões do Copom", "formato": a.formato}
    d = E.montar_entrada(espec, a.duracao, som={"pouso": "impact-bass-1"})
    d["fonte"] = "Fonte: BCB/SGS 432 (meta Selic; data de vigência de cada decisão)"
    d["peca"] = "eventos"
    d["eventos"] = eventos_ciclo(desde)
    d["_origem"]["gerado_em"] = dt.datetime.now().isoformat(timespec="seconds")
    d["_origem"]["eventos"] = "mudanças da própria SGS 432 (1ª alta, pico, 1º corte)"
    return d


def ipca(mostrar=12):
    """-> (mensal [(iso, %)], referência 13522 [(iso, %)], origens). Os meses mostrados terminam no último mês que
    as DUAS séries têm."""
    m, o1 = bcb(433, "2019-01-01")
    r, o2 = bcb(13522, "2019-01-01")
    fim = min(m[-1][0], r[-1][0])
    m = [p for p in m if p[0] <= fim]
    return m[-(mostrar + 11):], [p for p in r if p[0] <= fim][-mostrar:], (o1, o2)


def conferir_ipca(mensal, ref):
    """-> [(mês, calculado, oficial)]. Para (SystemExit) se algum mês diferir mais de 0,01 p.p."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("barra_linha_gerar", os.path.join(AQUI, "barra_linha", "gerar.py"))
    bl = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bl)
    oficial = dict(ref)
    out = [(d, v, oficial.get(d)) for d, v in bl.acumulado_12m(mensal)[-len(ref):]]
    ruins = [x for x in out if x[2] is None or abs(round(x[1], 2) - x[2]) > 0.01 + 1e-9]
    if ruins:
        raise SystemExit(f"acumulado do 433 não bate com a SGS 13522: {ruins}")
    return out


def montar_ipca(a):
    n = a.top or 12
    mensal, ref, (o1, o2) = ipca(n)
    conf = conferir_ipca(mensal, ref)
    ult = conf[-1]
    return {
        "peca": "barra_linha", "estilo": a.estilo, "formato": a.formato, "duracao": a.duracao if a.duracao != 8.0 else 9.0,
        "titulo": a.titulo or "IPCA: o mês e os 12 meses",
        "kicker": "Inflação oficial (IBGE) · mês a mês",
        "fonte": "Fonte: BCB/SGS 433 (IPCA mensal) · 12 meses calculado e conferido com a SGS 13522",
        "unidade": {"prefixo": "", "sufixo": "%", "casas": 2}, "mostrar": n,
        "rotulos": {"mes": "IPCA no mês", "doze": "IPCA em 12 meses"},
        "som": {"pouso": "impact-bass-1"},
        "mensal": [{"data": d, "valor": v} for d, v in mensal],
        "referencia_12m": [{"data": d, "valor": v} for d, v in ref],
        "_conferido": {"mes": ult[0], "calculado_433": round(ult[1], 6), "sgs_13522": ult[2],
                       "maior_diferenca_pp": round(max(abs(round(c, 2) - o) for _, c, o in conf), 4)},
        "_origem": _origem(f"{o1}; referência: {o2}"),
    }


def montar_selic(a):
    desde = a.desde or "2020-01-01"
    pontos, origem = bcb(432, desde)
    pontos = S.so_mudancas(pontos)
    return {
        "peca": "numero_linha", "estilo": a.estilo, "formato": a.formato, "duracao": a.duracao,
        "titulo": a.titulo or f"Selic: {fmt_br(pontos[-1][1], 2)}%, e o caminho até aqui",
        "kicker": "Meta da taxa Selic · Copom",
        "fonte": "Fonte: BCB/SGS 432 (meta Selic)",
        "classe": "indicador", "linha": "degrau", "variacao": "pp",
        "unidade": {"prefixo": "", "sufixo": "%", "casas": 2},
        "rotulo_numero": f"meta Selic em {pontos[-1][0][8:10]}/{_mes(pontos[-1][0])}",
        "som": {"pouso": "impact-bass-1"},
        "serie": [{"data": d, "valor": v} for d, v in pontos],
        "_origem": _origem(origem),
    }


def montar_manchete_ipca(a):
    r, origem = bcb(13522, "2019-01-01")
    (d0, v0), (d1, v1) = r[-2], r[-1]
    verbo = "cai" if v1 < v0 else "sobe" if v1 > v0 else "fica"
    numero = f"{fmt_br(v1, 2)}%"
    frase = f"Inflação em 12 meses {verbo} {'em' if verbo == 'fica' else 'para'} {numero} em {MESES_EXTENSO[int(d1[5:7]) - 1]}"
    return {
        "peca": "manchete", "estilo": a.estilo, "formato": a.formato, "duracao": a.duracao if a.duracao != 8.0 else 6.0,
        "kicker": "IPCA · acumulado em 12 meses",
        "frase": frase, "chave": numero, "marca": a.marca, "palavras": None,
        "fonte": f"Fonte: BCB/SGS 13522 (IPCA em 12 meses, {_mes(d1)}; {_mes(d0)}: {fmt_br(v0, 2)}%)",
        "som": {"pouso": "impact-bass-1"},
        "_conferido": {"mes": d1, "valor": v1, "mes_anterior": d0, "valor_anterior": v0},
        "_origem": _origem(origem),
    }


def _br(iso):
    return f"{iso[8:10]}/{iso[5:7]}/{iso[:4]}"


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("conjunto", choices=["dy-caixa", "cotistas", "megasena", "copom", "ipca", "selic", "manchete-ipca"])
    ap.add_argument("--peca", choices=["barras", "rosca"], default="barras")
    ap.add_argument("--estilo", choices=["iec", "fazaconta"], default="iec")
    ap.add_argument("--formato", choices=["16:9", "9:16"], default="16:9")
    ap.add_argument("--duracao", type=float, default=8.0)
    ap.add_argument("--titulo")
    ap.add_argument("--destaque")
    ap.add_argument("--top", type=int)
    ap.add_argument("--antes", default="2025-08-01")
    ap.add_argument("--depois", default="2026-08-01")
    ap.add_argument("--desde", help="AAAA-MM-DD (copom, selic)")
    ap.add_argument("--marca", choices=["preencher", "marca-texto"], default="preencher", help="manchete")
    ap.add_argument("-o", "--saida", required=True)
    a = ap.parse_args(argv)
    d = {"dy-caixa": montar_dy_caixa, "cotistas": montar_cotistas, "megasena": montar_megasena,
         "copom": montar_copom, "ipca": montar_ipca, "selic": montar_selic,
         "manchete-ipca": montar_manchete_ipca}[a.conjunto](a)
    os.makedirs(os.path.dirname(os.path.abspath(a.saida)), exist_ok=True)
    json.dump(d, open(a.saida, "w"), ensure_ascii=False, indent=1)
    n = len(d.get("itens") or d.get("fatias") or d.get("eventos") or d.get("mensal") or d.get("serie") or [d.get("frase")])
    print(f"ok: {a.saida} ({d['peca']}, {n} itens; origem: {d['_origem']['arquivo']})"
          + (f"; conferido: {d['_conferido']}" if "_conferido" in d else ""))


if __name__ == "__main__":
    main()
