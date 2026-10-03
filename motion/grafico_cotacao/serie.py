"""Gera o JSON de entrada do gráfico de cotação a partir de dado real e livre.

Fontes, na ordem em que são tentadas:
  bcb <serie>  → BCB SGS. 1) SQLite do site-ativos (tabela macro); 2) JSON cru do site-ativos
                 (cache/raw/bcb/sgs_<n>.json); 3) cache próprio em motion/cache/; 4) API do BCB
                 (api.bcb.gov.br), que grava no cache próprio.
  b3 <TICKER>  → COTAHIST da B3. 1) SQLite do site-ativos (tabela preco_diario); 2) COTAHIST_A<ano>.txt.gz
                 do site-ativos (posições fixas, preço ÷ 100 ÷ FATCOT). Sem rede: o ZIP anual tem ~90 MB e
                 quem baixa é o site-ativos (`python3 -m iec_ativos baixar`).

O preço do COTAHIST é o fechamento do pregão SEM ajuste por proventos, desdobramento ou grupamento.
Uma variação diária acima de 35% é tratada como provável evento societário e impede a geração
(use --aceitar-saltos se conferiu o evento e quer o preço nominal mesmo assim).

Exemplos:
  python3 grafico_cotacao/serie.py bcb 432 --desde 2020-01-01 --destacar-extremos \
      --titulo "Selic: de 2% a 15%" --kicker "Meta da taxa Selic · Copom" -o exemplos/selic-16x9.json
  python3 grafico_cotacao/serie.py b3 PETR4 --desde 2025-10-01 --formato 9:16 --comparador IBOV \
      --titulo "PETR4 × Ibovespa" -o exemplos/petr4-9x16.json
"""
import argparse, datetime as dt, gzip, json, os, sqlite3, sys, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
MOTION = os.path.dirname(AQUI)


def _site_ativos():
    """A pasta site-ativos com cache: $IEC_SITE_ATIVOS, a vizinha desta pasta ou o clone principal."""
    candidatos = [os.environ.get("IEC_SITE_ATIVOS"), os.path.join(os.path.dirname(MOTION), "site-ativos"),
                  os.path.expanduser("~/IPADTEST/site-ativos"), "/home/user/IPADTEST/site-ativos"]
    for c in candidatos:
        if c and os.path.isdir(os.path.join(c, "cache")):
            return c
    return candidatos[1]


SITE_ATIVOS = _site_ativos()
CACHE_PROPRIO = os.path.join(MOTION, "cache")

NOMES_SGS = {432: "Meta da taxa Selic", 11: "Selic diária", 12: "CDI diário", 433: "IPCA mensal",
             13522: "IPCA acumulado em 12 meses"}
LIMITE_SALTO = 0.35


def _sqlite():
    p = os.path.join(SITE_ATIVOS, "cache", "dados.sqlite")
    return p if os.path.exists(p) else None


def _data_br(s):
    d, m, a = s.split("/")
    return f"{a}-{m}-{d}"


def serie_bcb(serie, desde, ate=None):
    """-> (pontos [(iso, valor)], origem)"""
    db = _sqlite()
    if db:
        con = sqlite3.connect(db)
        q = "select data, valor from macro where serie=? and data>=? and data<=? order by data"
        rows = con.execute(q, (serie, desde, ate or "9999")).fetchall()
        if rows:
            return [(d, float(v)) for d, v in rows], f"site-ativos/cache/dados.sqlite (macro {serie})"
    for base in (os.path.join(SITE_ATIVOS, "cache", "raw", "bcb"), CACHE_PROPRIO):
        p = os.path.join(base, f"sgs_{serie}.json")
        if os.path.exists(p):
            rows = [(_data_br(r["data"]), float(r["valor"])) for r in json.load(open(p))]
            rows = [r for r in rows if desde <= r[0] <= (ate or "9999")]
            if rows:
                return rows, os.path.relpath(p, os.path.dirname(MOTION))
    ini = dt.date.fromisoformat(desde).strftime("%d/%m/%Y")
    fim = (dt.date.fromisoformat(ate) if ate else dt.date.today()).strftime("%d/%m/%Y")
    url = (f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie}/dados?formato=json"
           f"&dataInicial={ini}&dataFinal={fim}")
    req = urllib.request.Request(url, headers={"User-Agent": "iec-motion/1.0"})
    bruto = urllib.request.urlopen(req, timeout=60).read()
    os.makedirs(CACHE_PROPRIO, exist_ok=True)
    open(os.path.join(CACHE_PROPRIO, f"sgs_{serie}.json"), "wb").write(bruto)
    rows = [(_data_br(r["data"]), float(r["valor"])) for r in json.loads(bruto)]
    return rows, url


def _cotahist(ticker, desde, ate):
    pasta = os.path.join(SITE_ATIVOS, "cache", "raw", "b3")
    if not os.path.isdir(pasta):
        return []
    rows = []
    for nome in sorted(os.listdir(pasta)):
        if not (nome.startswith("COTAHIST_A") and nome.endswith(".txt.gz")):
            continue
        ano = nome[10:14]
        if ano < desde[:4] or (ate and ano > ate[:4]):
            continue
        with gzip.open(os.path.join(pasta, nome), "rt", encoding="latin-1") as f:
            for linha in f:
                if linha[:2] != "01" or linha[12:24].strip() != ticker or linha[24:27] != "010":
                    continue
                d = f"{linha[2:6]}-{linha[6:8]}-{linha[8:10]}"
                if desde <= d <= (ate or "9999"):
                    fat = int(linha[210:217]) or 1
                    rows.append((d, int(linha[108:121]) / 100 / fat))
    return sorted(rows)


def serie_b3(ticker, desde, ate=None):
    ticker = ticker.upper()
    db = _sqlite()
    if db:
        con = sqlite3.connect(db)
        q = "select data, fechamento from preco_diario where ticker=? and data>=? and data<=? order by data"
        rows = con.execute(q, (ticker, desde, ate or "9999")).fetchall()
        if rows:
            return [(d, float(v)) for d, v in rows], f"site-ativos/cache/dados.sqlite (preco_diario {ticker})"
    rows = _cotahist(ticker, desde, ate)
    if rows:
        return rows, "site-ativos/cache/raw/b3/COTAHIST_A*.txt.gz"
    raise SystemExit(f"sem cotação de {ticker} no cache do site-ativos ({SITE_ATIVOS}). "
                     "Rode lá: python3 -m iec_ativos baixar && python3 -m iec_ativos normalizar")


def saltos(pontos, limite=LIMITE_SALTO):
    """Variações diárias acima do limite (provável desdobramento ou grupamento)."""
    out = []
    for (d0, v0), (d1, v1) in zip(pontos, pontos[1:]):
        if v0 and abs(v1 / v0 - 1) > limite:
            out.append((d1, v0, v1))
    return out


def so_mudancas(pontos):
    """Série em degrau (Selic): guarda o primeiro ponto, cada mudança e o último. Sem perda."""
    out = [pontos[0]]
    for p in pontos[1:-1]:
        if p[1] != out[-1][1]:
            out.append(p)
    if len(pontos) > 1:
        out.append(pontos[-1])
    return out


def fmt_br(v, casas):
    s = f"{abs(v):,.{casas}f}".replace(",", "X").replace(".", ",").replace("X", ".")
    return ("-" if v < 0 and round(abs(v), casas) else "") + s


def montar(args):
    """CLI → especificação → JSON (a regra de compliance mora em especificacao.py)."""
    import especificacao as E
    espec = {"serie": f"{'SGS' if args.fonte == 'bcb' else 'COTAHIST'}:{args.codigo}",
             "periodo": f"{args.desde}:{args.ate or ''}", "rotulo": args.titulo or (args.kicker or args.codigo),
             "formato": args.formato, "cor_final": args.cor_final}
    for k in ("kicker", "comparador"):
        if getattr(args, k):
            espec[k] = getattr(args, k)
    if args.aviso:
        espec["aviso"] = True
    if args.destacar_extremos:
        espec["destaques"] = "extremos"
    if args.aceitar_saltos:
        espec["aceitar_saltos"] = True
    try:
        dados = E.montar_entrada(espec, args.duracao, som=False if args.sem_som else {"pouso": "impact-bass-1"})
    except E.ErroEspecificacao as e:
        raise SystemExit(f"recusado: {e}")
    dados["_origem"]["gerado_em"] = dt.datetime.now().isoformat(timespec="seconds")
    return dados


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("fonte", choices=["bcb", "b3"])
    ap.add_argument("codigo", help="número da série SGS (bcb) ou ticker (b3)")
    ap.add_argument("--desde", required=True, help="AAAA-MM-DD")
    ap.add_argument("--ate", help="AAAA-MM-DD (padrão: último dado)")
    ap.add_argument("--titulo")
    ap.add_argument("--kicker")
    ap.add_argument("--formato", choices=["16:9", "9:16"], default="16:9")
    ap.add_argument("--duracao", type=float, default=8.0)
    ap.add_argument("--cor-final", choices=["vermelho", "ouro"], default="vermelho")
    ap.add_argument("--destacar-extremos", action="store_true")
    ap.add_argument("--aceitar-saltos", action="store_true")
    ap.add_argument("--sem-som", action="store_true")
    ap.add_argument("--comparador", help="IBOV, IFIX, CDI ou SGS:<n> (ativo da B3 exige comparador ou --aviso)")
    ap.add_argument("--aviso", action="store_true", help="escreve 'Não é recomendação de investimento.' na tela")
    ap.add_argument("-o", "--saida", required=True)
    a = ap.parse_args(argv)
    dados = montar(a)
    os.makedirs(os.path.dirname(os.path.abspath(a.saida)), exist_ok=True)
    json.dump(dados, open(a.saida, "w"), ensure_ascii=False, indent=1)
    print(f"ok: {a.saida} ({len(dados['serie'])} pontos, {dados['serie'][0]['data']} → {dados['serie'][-1]['data']}, "
          f"último = {dados['serie'][-1]['valor']}; origem: {dados['_origem']['arquivo']})")


if __name__ == "__main__":
    main()
