"""Testes de pautas-canal (sem rede). Os que dependem dos dados reais pulam se eles não estiverem no repositório."""
import csv
from collections import Counter
import re
import sys
from datetime import date, timedelta
from pathlib import Path

import pytest

AQUI = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AQUI))
import modelo as mo  # noqa: E402
import meta as me  # noqa: E402
import calendario_v2 as cal  # noqa: E402
import perguntas as pg  # noqa: E402
from modelo import an  # noqa: E402

DADOS_REAIS = (mo.DADOS / "videos.csv").exists() and (mo.DADOS / "canal_por_mes.csv").exists()


def test_quantil_e_meses():
    assert mo.quantil([1, 2, 3, 4, 5], .5) == 3
    assert mo.quantil([0, 10], .25) == 2.5
    assert mo.quantil([], .5) is None
    assert mo.meses_ate(date(2026, 12, 31)) == pytest.approx(2 + 31 / 30.4)


def base_falsa():
    longo = {"insc_med": 25, "insc_p75": 60, "insc_p90": 150, "insc_mil": 9.0, "esperado": 40, "esperado_p25": 20,
             "esperado_p75": 70}
    return {"atual": 165_000, "faltam": 35_000, "perdas_6m": 350, "catalogo": 450, "liq_6m": 400,
            "longos_mes_max": 12, "longo": longo, "short": {"esperado": 1.5}}


def test_cenario_fecha_a_conta():
    b = base_falsa()
    c = mo.cenario(b, date(2027, 12, 31))
    assert c["liquidos"] * c["meses"] == pytest.approx(35_000)
    assert c["ganhos"] == pytest.approx(c["liquidos"] + 350)
    assert c["novos"] == pytest.approx(c["ganhos"] - 450)
    assert c["longos_insc_med"] == pytest.approx(c["novos"] / 25)
    assert c["insc_por_longo_no_max"] == pytest.approx(c["novos"] / 12)
    assert c["views_intenc_novos"] == pytest.approx(c["novos"] / 0.009)
    assert c["x_ritmo"] == pytest.approx(c["liquidos"] / 400)


def test_projecao():
    quando, meses = mo.projecao(base_falsa(), 1000)
    assert meses == 35 and quando == date(2029, 9, 1)
    assert mo.projecao(base_falsa(), 0) is None


def test_metas_mensais_rampa_e_defasagem():
    b = base_falsa()
    p = {"novos": 1000.0, "novos_shorts": 0.0}
    m = me.metas_mensais(b, p, meses=4, rampa={"2026-10": 0.5}, defasagem=(0.6, 0.25, 0.15))
    # out: 0,5 × 1000 × 0,6; nov: 1000 × 0,6 + 500 × 0,25; dez: 600 + 250 + 75; jan: regime 1000
    assert [round(x["ganhos"] - 450) for x in m] == [300, 725, 925, 1000]
    assert m[-1]["liquidos"] == pytest.approx(450 + 1000 - 350)
    assert m[0]["inscritos_fim_mes"] == pytest.approx(165_000 + 450 + 300 - 350)
    assert me.data_meta(b, m, 1100) is not None


def test_calendario_v2_assunto_sai_do_titulo_e_regras():
    longos = [p for p in cal.PAUTAS if p[1] == cal.L]
    shorts = [p for p in cal.PAUTAS if p[1] == cal.S]
    assert len(longos) == 21 and len(shorts) == 16
    for data_, fmt, assunto, titulo, *_ in cal.PAUTAS:
        assert an.assunto(titulo) == assunto, titulo
        assert date(2026, 10, 5) <= date.fromisoformat(data_) <= date(2026, 11, 29)
        t = an.norm(titulo)
        assert not re.search(r"cartao|divida pessoal|lula|bolsonaro|eleic|corretora|compre\b", t), titulo
    assert any(p[0] == "2026-11-05" and "Copom" in p[3] for p in longos)
    # 2 longos por semana até 25/10 e 3 depois (9 em outubro, 12 em novembro)
    out = sum(1 for p in longos if p[0] < "2026-11-01")
    assert out == 9 and len(longos) - out == 12


def test_perguntas_criterio(tmp_path):
    arq = tmp_path / "c.csv"
    cab = ["video_id", "comentario_id", "resposta_a", "autor_canal_id", "eh_do_canal", "texto", "likes", "publicado_em",
           "eh_resposta"]
    linhas = [["v", "a", "", "h", "0", "Como declarar FII?", "3", "", "0"],
              ["v", "b", "", "h", "0", "Ótimo vídeo", "1", "", "0"],
              ["v", "c", "", "h", "0", "Qual a taxa?", "0", "", "0"],
              ["v", "r1", "a", "hc", "1", "Assim", "0", "", "1"],           # canal respondeu a "a"
              ["v", "r2", "c", "h2", "0", "Não sei", "0", "", "1"]]          # resposta de usuário não conta
    with open(arq, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cab)
        w.writerows(linhas)
    perg, sem = pg.perguntas_sem_resposta(arq)
    assert [c["comentario_id"] for c in perg] == ["a", "c"]
    assert [c["comentario_id"] for c in sem] == ["c"]
    assert pg.tema("O cartão tem anuidade?").endswith("(fora do escopo)")
    assert pg.tema("Como declarar no imposto de renda?").startswith("Imposto")
    assert pg.tema("dobra como?", pg.SHORT_1_CENTAVO) == pg.GRUPO_1_CENTAVO


@pytest.mark.skipif(not DADOS_REAIS, reason="dados reais ausentes")
def test_modelo_com_dados_reais_calibra_com_o_ritmo_de_hoje():
    d = mo.carregar()
    b = mo.base(d)
    # a árvore com a produção de hoje (8 longos e 5,5 Shorts) tem de dar perto do ritmo real (±25%)
    hoje = b["catalogo"] + 8 * b["longo"]["esperado"] + 5.5 * b["short"]["esperado"] - b["perdas_6m"]
    assert hoje == pytest.approx(b["liq_6m"], rel=0.25)
    r = me.gerar(d)
    assert r["quando"] > "2027-12"                     # 200 mil em 2027 não sai do plano recomendado
    assert [a["central"] for a in r["alavancas"]] == sorted((a["central"] for a in r["alavancas"]), reverse=True)
    rk, tot, _ = mo.ranking(d, "longo", "12 meses")
    assert sum(r_["n"] for r_ in rk) == tot["n"]


import termos as tm  # noqa: E402


def test_titulos_longos_ate_62_caracteres_e_termo_no_titulo():
    for data_, fmt, assunto, titulo, *_ in cal.PAUTAS:
        if fmt == cal.L:
            assert len(titulo) <= 62, titulo
        termo = cal.TERMOS.get(data_, (None, ""))[0]
        if termo and fmt == cal.L:
            # o termo (ou a sua palavra principal) aparece no título
            vazias = {"o", "e", "que", "como", "qual", "melhor", "para", "de", "do", "da", "por"}
            palavras = [w for w in an.norm(termo).split() if len(w) >= 3 and w not in vazias]
            assert any(w[:4] in an.norm(titulo) for w in palavras), (termo, titulo)


def test_classificacao_dos_termos():
    T = tm.Termos.__new__(tm.Termos)
    T.origem = {"como ganhar dinheiro": {tm.SHORT_1_CENTAVO: 10}}
    T.origem = {k: __import__("collections").Counter(v) for k, v in T.origem.items()}
    T.origem_rec, T.videos = {}, {}
    assert T.categoria("como ganhar dinheiro") == "amplo (1 centavo)"
    assert T.categoria("renda extra") == "amplo (1 centavo)"
    assert T.categoria("banco next vale a pena") == "bancos, apps e outros (catálogo)"
    assert T.categoria("caixinha turbo nubank") == "bancos, apps e outros (catálogo)"
    assert T.categoria("lci e lca") == "investimento"
    assert T.categoria("etfs que pagam dividendos mensais") == "investimento"
    assert tm.Termos.assunto("hash11") == "cripto" and tm.Termos.assunto("spyi11") == "ETF e exterior"


@pytest.mark.skipif(not (tm.DADOS / "termos_busca_canal.csv").exists(), reason="termos reais ausentes")
def test_termos_reais():
    T = tm.Termos()
    assert set(T.corte) >= set(tm.MESES_6)
    soma, pres, teto = T.seis_meses(["como ganhar dinheiro na internet"])
    assert pres == 6 and soma > 50_000
    soma, pres, teto = T.seis_meses(["lci e lca"])
    assert pres == 0 and teto == sum(T.corte[m] for m in tm.MESES_6)
    assert T.vitalicio(["lci e lca"]) == 3544
    linhas = cal.montar(mo.carregar())
    assert all(k in linhas[0] for k in ("termo_busca", "views_pesquisa_6m", "views_pesquisa_vitalicio"))
    por_data = {r["data"]: r for r in linhas}
    if T.recentes:
        assert int(por_data["2026-10-31"]["views_pesquisa_6m"].replace(".", "")) >= 1516  # trxf11, o nº 1 do período
        assert por_data["2026-11-05"]["termo_busca"] == "tesouro direto"
        top = sorted((r for r in T.linhas() if r["categoria"] == "investimento"), key=lambda r: -r["recente"])
        assert top[0]["termo"] == "trxf11" and top[0]["assunto"] == "FII"
    assert por_data["2026-10-22"]["views_pesquisa_vitalicio"] > 0


# ------------------------------------------------------------------ calendário oficial (v3)
import calendario_v3 as cal3  # noqa: E402
import os  # noqa: E402

CAL3_CSV = AQUI / "CALENDARIO.csv"
GATE_DIR = Path(os.environ.get("GATE_DIR", "/home/user/investir-e-cocar/pipeline"))


def linhas_v3():
    with open(CAL3_CSV, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def test_calendario_v3_no_maximo_3_longos_por_semana():
    longos = [r for r in linhas_v3() if r["formato"] == "longo"]
    por_semana = Counter((date.fromisoformat(r["data"]) - cal3.INICIO).days // 7 for r in longos)
    assert set(por_semana) == set(range(8))
    assert max(por_semana.values()) <= 3, por_semana
    for r in linhas_v3():
        assert cal3.INICIO <= date.fromisoformat(r["data"]) <= cal3.FIM


def test_calendario_v3_sem_as_7_pautas_fora_do_nicho():
    assert len(cal3.FORA_DO_NICHO) == 7
    titulos = {an.norm(r["titulo"]) for r in linhas_v3()}
    for data_, titulo in cal3.FORA_DO_NICHO.items():
        assert an.norm(titulo) not in titulos, titulo
        assert any(p[0] == data_ and p[3] == titulo for p in cal.PAUTAS), (data_, titulo)   # existia no v2
    t = " ".join(titulos)
    assert not re.search(r"bolha da ia|perfil de investidor|casal que investe|1 centavo dobrando|reserva de emergencia", t)


def test_calendario_v3_serie_copom_e_titulos_provisorios():
    ls = linhas_v3()
    eps = sorted((r["data"], r["serie_ep"]) for r in ls if r["formato"] == "longo" and r["serie_ep"])
    assert eps == [("2026-10-14", "Ep. 1"), ("2026-10-21", "Ep. 2"), ("2026-10-28", "Ep. 3"), ("2026-11-11", "Ep. 4"),
                   ("2026-11-18", "Ep. 5"), ("2026-11-25", "Ep. 6")]
    for r in ls:
        assert (r["status_titulo"] == cal3.PROVISORIO) == bool(r["serie_ep"]), r["titulo"]
        assert an.assunto(r["titulo"], cal3.SERIE if r["serie_ep"] else None) == r["assunto"], r["titulo"]
    copom = [r for r in ls if r["formato"] == "longo" and "Copom" in r["titulo"]]
    assert [r["data"] for r in copom] == ["2026-11-03"] and copom[0]["assunto"] == "tesouro e renda fixa"
    assert not any(r["data"] == "2026-11-02" and r["formato"] == "longo" for r in ls)   # feriado de Finados
    assert sum(1 for r in ls if r["formato"] == "short") == 16


def _tema_etf_dividendos_mensais(titulo):
    """O longo é SOBRE ETF de dividendos mensais (uma comparação com outra classe, como "ETF ... ou FII", não é)."""
    t = an.norm(titulo)
    return bool(re.search(r"\betfs?\b.*dividendos? mensa|dividendos? mensa.*\betfs?\b", t)) and " ou " not in t


def test_calendario_v3_etf_de_dividendos_mensais_so_no_ep1():
    ls = linhas_v3()
    tema = [r for r in ls if r["formato"] == "longo" and _tema_etf_dividendos_mensais(r["titulo"])]
    assert [(r["data"], r["serie_ep"]) for r in tema] == [("2026-10-14", "Ep. 1")], [r["titulo"] for r in tema]
    for r in ls:
        if not r["serie_ep"]:
            assert "o que sobra" not in an.norm(r["titulo"]), r["titulo"]            # promessa do Ep. 1
    assert _tema_etf_dividendos_mensais("ETFs que pagam dividendos mensais: o que mudou em 2026")
    assert not _tema_etf_dividendos_mensais("ETF de dividendos mensais ou FII: imposto e renda de cada um")
    ep1 = next(r for r in ls if r["serie_ep"] == "Ep. 1")
    assert "BLOCOS ABSORVIDOS" in ep1["angulo"] and "opções" in ep1["angulo"] and "taxa" in ep1["angulo"]


@pytest.mark.skipif(not DADOS_REAIS, reason="dados reais ausentes")
def test_calendario_v3_fila_de_dezembro_e_regra_nas_trocas():
    linhas, decisoes, fila, log = cal3.montar(mo.carregar())
    assert decisoes == []                                    # as trocas já deixam no máximo 3 longos por semana
    assert [r["titulo"] for r in fila] == ["ETFs que pagam dividendos mensais: o que mudou em 2026"]
    for x in log:
        t = x["troca"]
        if t.get("regra_3_longos"):
            sem = x["semana_antes"]
            assert len(sem) == 4
            fraco = min((r for r in sem if not cal3.fixa(r)), key=lambda r: r["_e"])
            assert [(p["data"], p["titulo"]) for p in t["pautas"]] == [(fraco["data"], fraco["titulo"])]


def test_trocas_json_versionado():
    trocas = cal3.carregar_trocas()
    ids = [t["id"] for t in trocas]
    assert len(ids) == len(set(ids)) and ids == sorted(ids)
    for t in trocas:
        assert t["aprovada_em"] and t["aprovada_por"] and t["motivo"], t["id"]
        assert t["op"] in {"sai", "entra", "move", "titulo", "edita", "absorve"}, t["id"]
    assert len(cal3.FORA_DO_NICHO) == 7
    # uma troca inválida é recusada, não ignorada
    with pytest.raises(cal3.TrocaInvalida):
        cal3.aplicar_trocas([{"id": "X", "op": "move", "para": "2026-10-20",
                              "pauta": {"data": "2026-10-06", "formato": "longo", "titulo": "não existe"}}],
                            cal3.pautas_v2())
    ls, fila, _ = cal3.aplicar_trocas(trocas, cal3.pautas_v2())
    assert [(r["data"], r["titulo"]) for r in ls] == [(r["data"], r["titulo"]) for r in linhas_v3()]


def test_calendario_v3_todo_titulo_passa_no_gate():
    sys.path.insert(0, str(GATE_DIR))
    g = pytest.importorskip("gate_qualidade")
    titulos = [r["titulo"] for r in linhas_v3()]
    assert len(titulos) == len(set(titulos))
    for t in titulos:
        post = g.Post(t, "", "md")
        probs = g.checar_recomendacao(post) + g.checar_corretora(post) + g.checar_tickers(post)
        assert not probs, (t, probs)
        r = g.avaliar(post)
        assert r["bloqueantes"] == 0, (t, r["problemas"])


def test_regra_dos_3_longos_tira_o_mais_fraco_ou_empurra():
    def p(data_, e, ep=""):
        return {"data": data_, "formato": "longo", "_e": e, "serie_ep": ep, "origem": "v2", "titulo": data_,
                "assunto": "x"}
    # semana de 12/10 com 4 longos: o episódio (10) é fixo; o mais fraco dos outros é o de 13/10 (30)
    ls = [p("2026-10-12", 91), p("2026-10-13", 30), p("2026-10-14", 10, "Ep. 1"), p("2026-10-15", 195),
          p("2026-10-20", 91)]
    out, dec = cal3.aplicar_limite(ls)
    # a terça 20/10 já tem longo: vai para a terça seguinte com vaga, 27/10
    assert len(dec) == 1 and dec[0]["sai"] == "2026-10-13" and dec[0]["acao"] == "empurrado para 27/10"
    assert [r["data"] for r in out if r["titulo"] == "2026-10-13"] == ["2026-10-27"]
    # sem vaga em nenhuma semana seguinte: sai da janela
    cheio = [p(f"2026-11-{d:02d}", 50) for d in (23, 24, 25)] + [p("2026-11-26", 40), p("2026-11-27", 45)]
    out, dec = cal3.aplicar_limite(cheio)
    assert [d["sai"] for d in dec] == ["2026-11-26", "2026-11-27"]          # 5 longos: saem os 2 mais fracos
    assert all("fila de dezembro" in d["acao"] for d in dec) and len(out) == 3


@pytest.mark.skipif(not DADOS_REAIS, reason="dados reais ausentes")
def test_calendario_v3_csv_e_o_que_o_script_gera():
    linhas, *_ = cal3.montar(mo.carregar())
    assert [(r["data"], r["titulo"]) for r in linhas] == [(r["data"], r["titulo"]) for r in linhas_v3()]
