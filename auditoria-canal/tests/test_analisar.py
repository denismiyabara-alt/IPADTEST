"""Testes do analisar.py com dados falsos pequenos (inclui exportações falsas do Studio, em ZIP e em pasta)."""
import csv
import sys
import zipfile
from datetime import date, timedelta
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import analisar as an  # noqa: E402


def escrever(p, cab, linhas):
    p.parent.mkdir(parents=True, exist_ok=True)
    with p.open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cab)
        w.writerows(linhas)


# 12 longos (4 por tema) + 4 shorts. Views e inscritos escolhidos para dar números fáceis de conferir.
VIDEOS = [
    # id, título, formato, publicado (Brasília), views, ganhos, engajadas
    ("c1", "O que aconteceu com a Americanas", "longo", "2026-05-01", 100000, 700, 40000),
    ("c2", "A história de Luiz Barsi", "longo", "2026-05-10", 80000, 560, 32000),
    ("c3", "Banco Master quebrou: e agora?", "longo", "2026-06-01", 60000, 420, 24000),
    ("c4", "O caso Petrobras", "longo", "2026-09-01", 50000, 350, 8000),
    ("m1", "Crise fiscal: alerta para 2027", "longo", "2026-05-05", 5000, 10, 2000),
    ("m2", "Juros vão subir de novo", "longo", "2026-05-20", 4000, 8, 1600),
    ("m3", "Inflação e o dólar", "longo", "2026-06-10", 3000, 6, 1200),
    ("m4", "Selic a 15%: o que muda", "longo", "2026-09-05", 2000, 4, 300),
    ("r1", "Quanto preciso para viver de renda", "longo", "2026-05-03", 3000, 6, 1200),
    ("r2", "Renda passiva de R$ 5 mil por mês", "longo", "2026-05-25", 2500, 5, 1000),
    ("r3", "Minha carteira de dividendos", "longo", "2026-06-15", 2000, 4, 800),
    ("r4", "Plano de aposentadoria", "longo", "2026-09-10", 1000, 2, 150),
    ("s1", "Dica #shorts", "short", "2025-01-10", 20000, 60, 18000),
    ("s2", "CDB ou Tesouro? #shorts", "short", "2025-06-10", 30000, 90, 10000),
    ("s3", "Poupança perde #shorts", "short", "2026-03-10", 30000, 90, 10000),
    ("s4", "LCI isenta #shorts", "short", "2026-07-20", 30000, 90, 10000),
]


@pytest.fixture
def dados(tmp_path):
    d = tmp_path / "dados"
    escrever(d / "videos.csv", ["id", "titulo", "publicado_em_utc", "publicado_em_brt", "dia_semana", "hora",
                                "duracao_s", "formato", "views", "likes", "comentarios", "tags", "descricao_tamanho",
                                "thumbnail_url"],
             [[i, t, p + " 21:00:00", p + " 18:00:00", "terça", 18, 900 if fm == "longo" else 40, fm,
               int(v * (2.5 if p >= "2026-08-27" and fm == "longo" else 1.0)), 1, 1, "", 10, ""]
              for i, t, fm, p, v, g, e in VIDEOS])
    escrever(d / "analytics_por_video.csv", ["video_id", "views", "estimatedMinutesWatched", "averageViewPercentage",
                                             "subscribersGained", "subscribersLost", "engagedViews", "impressions",
                                             "impressionsClickThroughRate"],
             [[i, v, v * 3, 40 if i.startswith("c") else 30, g, 0, "", "", ""] for i, t, fm, p, v, g, e in VIDEOS])
    meses = ["2025-04", "2025-05", "2025-06", "2026-01", "2026-02", "2026-03", "2026-04", "2026-05", "2026-06",
             "2026-07", "2026-08", "2026-09"]
    escrever(d / "canal_por_mes.csv", ["mes", "views", "minutos", "inscritos_ganhos", "inscritos_perdidos",
                                       "engagedViews", "views_shorts", "inscritos_ganhos_shorts"],
             [[m, 10000, 30000, 100, 10, 5000, 3000, 40] for m in meses])
    linhas = []
    for k, m in enumerate(meses):
        rel = 29 if k < 3 else 2 if k >= len(meses) - 2 else 15
        linhas += [[m, "RELATED_VIDEO", "Vídeos sugeridos", rel * 10, rel, rel],
                   [m, "BROWSE", "Navegação", (100 - rel) * 10, 1, 100 - rel]]
    escrever(d / "trafego_por_mes.csv", ["mes", "origem", "origem_pt", "views", "minutos", "pct_views_mes"], linhas)
    dias = []
    ini = date(2026, 7, 1)
    for n in range(90):
        dia = ini + timedelta(days=n)
        views = 2600 if dia >= an.DATA_INFLACAO else 1000
        dias.append([dia.isoformat(), views, 3000, 10, 1, 500])
    escrever(d / "canal_por_dia.csv", ["dia", "views", "minutos", "inscritos_ganhos", "inscritos_perdidos",
                                       "engagedViews"], dias)
    escrever(d / "comentarios_top30.csv", ["video_id", "comentario_id", "resposta_a", "autor_canal_id", "eh_do_canal",
                                           "texto", "likes", "publicado_em", "eh_resposta"],
             [["c1", "k1", "", "h1", "0", "Como declarar FII no imposto de renda?", "9", "", "0"],
              ["c1", "k2", "", "h2", "0", "Vale a pena tesouro IPCA?", "5", "", "0"],
              ["c1", "k3", "", "h3", "0", "Ótimo vídeo", "2", "", "0"],
              ["c1", "k4", "k1", "hc", "1", "Assim: ...", "1", "", "1"]])
    # Studio: longos em ZIP com cabeçalhos em PT (e linha Total); shorts em pasta com cabeçalhos em EN.
    st = d / "studio"
    st.mkdir()
    cab_pt = ["Conteúdo", "Título do vídeo", "Horário de publicação do vídeo", "Duração", "Impressões",
              "Taxa de cliques de impressões (%)", "Visualizações", "Visualizações engajadas", "Tempo de exibição (horas)",
              "Duração média da visualização", "Porcentagem visualizada média (%)", "Inscritos", "Espectadores únicos"]
    linhas_pt = [["Total", "", "", "", "999999", "5", "", "", "", "", "", "", ""]]
    for i, t, fm, p, v, g, e in VIDEOS:
        if fm != "longo":
            continue
        ctr = "8,5" if i.startswith("c") else "3,1"
        vid = "" if i == "c2" else i            # c2 sem ID: tem de casar pelo título
        linhas_pt.append([vid, t, p, "900", str(v * 10), ctr, str(v), str(e), "100", "0:04:30", "40", str(g), "1"])
    texto = ",".join(cab_pt) + "\n" + "\n".join(",".join(f'"{c}"' for c in l) for l in linhas_pt)
    with zipfile.ZipFile(st / "studio_conteudo_longos.zip", "w") as z:
        z.writestr("Tabela.csv", texto)
        z.writestr("Totais.csv", "Data,Visualizações\n2026-09-30,1\n")
    pasta = st / "studio_conteudo_shorts"
    escrever(pasta / "Table data.csv", ["Content", "Video title", "Impressions", "Impressions click-through rate (%)",
                                        "Views", "Engaged views", "Subscribers"],
             [["Total", "", "", "", "", "", ""]] +
             [[i, t, "1000", "2.0", str(v), str(e), str(g)] for i, t, fm, p, v, g, e in VIDEOS if fm == "short"])
    escrever(pasta / "Chart data.csv", ["Date", "Views"], [["2026-01-01", "1"]])
    escrever(st / "studio_origem_trafego_mensal" / "Tabela.csv",
             ["Origem do tráfego", "Mês", "Impressões", "Taxa de cliques de impressões (%)", "Visualizações"],
             [["Total", "", "", "", ""],
              ["Vídeos sugeridos", "set. de 2026", "1000", "4.0", "100"],
              ["Vídeos sugeridos", "Sep 2026", "1000", "2.0", "100"],
              ["Recursos de navegação", "2026-09", "5000", "6", "900"]])
    escrever(st / "retencao_30s.csv", ["video_id", "pct_30s"], [["c1", "62"], ["c2", "61"], ["r4", "60"], ["m4", "59"]])
    (st / "ask_studio.txt").write_text("O público pergunta muito sobre FIIs.", encoding="utf-8")
    return d


# ------------------------------------------------------------------------------------------------ unidades
def test_num_formatos():
    assert an.num("1.234") == 1.234
    assert an.num("1.234.567") == 1234567
    assert an.num("1,234") == 1234
    assert an.num("12,5") == 12.5
    assert an.num("1.234,5") == 1234.5
    assert an.num("1,234.5") == 1234.5
    assert an.num("4.5%") == 4.5
    assert an.num("0:04:30") == 270
    assert an.num("") is None and an.num(None) is None


def test_temas():
    assert an.tema("O que aconteceu com a Americanas") == an.TEMA_CASO
    assert an.tema("Entrevista com Luiz Barsi") == an.TEMA_CASO
    assert an.tema("Se você é JOVEM DEVERIA INVESTIR em AÇÕES | Como investe Nicolas Agnez") == an.TEMA_CASO
    assert an.tema("BBAS3: VALE A PENA?") == "produto / comparativo"
    assert an.tema("Crise fiscal: alerta para 2027") == "alerta macro"
    assert an.tema("Renda passiva de R$ 5 mil por mês") == "plano de renda"
    assert an.tema("CDB ou Tesouro Direto?") == "produto / comparativo"
    assert an.tema("Vale a pena investir?") != an.TEMA_CASO        # "vale" não é a Vale
    assert an.tema("Como Investir No Tesouro Direto Em 2026") != an.TEMA_CASO  # título em caixa de título
    assert an.tema("qualquer coisa", manual="meu tema") == "meu tema"


def test_cabecalhos_pt_en_e_mes():
    assert an.chave_cab("Taxa de cliques de impressões (%)") == "ctr"
    assert an.chave_cab("Impressions click-through rate (%)") == "ctr"
    assert an.chave_cab("Visualizações engajadas") == "views_engajadas"
    assert an.chave_cab("Engaged views") == "views_engajadas"
    assert an.chave_cab("Tempo de exibição (horas)") == "horas"
    assert an.parse_mes("set. de 2026") == an.parse_mes("Sep 2026") == an.parse_mes("2026-09-14") == "2026-09"


def test_concentracao():
    vs = [{"views": x} for x in (50, 30, 10, 5, 5)]
    c = an.concentracao(vs)
    assert c["top1"] == 50 and c["n50"] == 1 and c["n80"] == 2


# ------------------------------------------------------------------------------------------------ com dados
def test_studio_lido_e_casado(dados):
    d = an.Dados(dados)
    assert set(d.studio) >= {"studio_conteudo_longos", "studio_conteudo_shorts", "studio_origem_trafego_mensal",
                             "retencao_30s", "ask_studio"}
    assert d.casamento == {"por_id": 15, "por_titulo": 1, "sem_par": 0}
    assert d.v["c2"]["ctr"] == 8.5 and d.v["c2"]["impressoes"] == 800000      # casou pelo título
    assert d.v["s1"]["ctr"] == 2.0 and d.v["s1"]["engajadas"] == 18000
    assert d.v["c1"]["pct_30s"] == 62
    ls = an.linhas_origem_mes(d.studio["studio_origem_trafego_mensal"])
    sug = next(r for r in ls if r["origem_api"] == "RELATED_VIDEO")
    assert sug["mes"] == "2026-09" and sug["impressoes"] == 2000 and sug["ctr"] == pytest.approx(3.0)


def test_conversao_por_formato_e_tema(dados):
    d = an.Dados(dados)
    g = {r["grupo"]: r for r in an.por_grupo([v for v in d.v.values() if v["formato"] == "longo"], "tema")}
    assert g[an.TEMA_CASO]["insc_mil"] == pytest.approx(7.0)
    assert g["alerta macro"]["insc_mil"] == pytest.approx(2.0)
    assert g["plano de renda"]["insc_mil"] == pytest.approx(2.0)
    f = {r["grupo"]: r for r in an.por_grupo(list(d.v.values()), "formato")}
    assert f["short"]["insc_mil"] == pytest.approx(3.0)


def test_hipoteses(dados):
    d = an.Dados(dados)
    H = {h["id"]: h for h in an.hipoteses(d)}
    assert H["H1"]["veredito"] == "CONFIRMA"      # views/engajadas 2,6x depois de 27/08
    assert H["H2"]["veredito"] == "CONFIRMA"      # 7 por mil × 2 por mil
    assert H["H3"]["veredito"] == "CONFIRMA"      # 29% → 2%
    assert H["H5"]["veredito"] == "CONFIRMA"      # 40% dos inscritos, nenhum Short depois de 28/07
    assert H["H4"]["veredito"] in ("CONFIRMA", "PARCIAL")
    assert "Shorts" in " ".join(H["H1"]["numeros"])


def test_hipoteses_sem_dados_nao_quebram(tmp_path):
    escrever(tmp_path / "videos.csv", ["id", "titulo", "publicado_em_brt", "formato", "views"],
             [["a", "Vídeo", "2026-01-01 10:00:00", "longo", "10"]])
    d = an.Dados(tmp_path)
    assert {h["veredito"] for h in an.hipoteses(d)} == {"SEM DADOS"}
    assert "Resultados" in an.relatorio(d)


def test_relatorio_e_lista_retencao(dados, tmp_path, capsys):
    saida = tmp_path / "analise"
    assert an.main(["--dados", str(dados), "--saida", str(saida)]) == 0
    md = (saida / "RESULTADOS.md").read_text(encoding="utf-8")
    for trecho in ("Conversão por formato", "Por tema", "Concentração", "Top × fracos", "Mês a mês",
                   "Origem do tráfego", "Hipóteses", "O que o público pergunta", "CTR mediano", "studio_origem_trafego_mensal",
                   "Ask Studio"):
        assert trecho in md, trecho
    temas = list(csv.DictReader((saida / "temas_por_video.csv").open(encoding="utf-8")))
    assert len(temas) == 16
    assert an.main(["--dados", str(dados), "--saida", str(saida), "--lista-retencao"]) == 0
    lista = list(csv.DictReader((saida / "lista_retencao_30s.csv").open(encoding="utf-8")))
    top = [r["video_id"] for r in lista if r["grupo"] == "top"]
    fracos = [r["video_id"] for r in lista if r["grupo"] == "fraco"]
    assert top[0] == "c1" and len(top) == len(fracos) and not set(top) & set(fracos)
    assert all(r["video_id"].startswith(("c", "m", "r")) for r in lista)   # só longos


def test_comentarios(dados):
    c = an.analise_comentarios(an.Dados(dados))
    assert c["perguntas"] == 2 and c["pct_perguntas_respondidas"] == 50
    assert c["mais_curtidas"][0]["comentario_id"] == "k1"


def test_formato_real_do_studio_so_studio_totais_e_outlier(tmp_path):
    """Cabeçalhos como os do Studio em pt-BR de 2026, ID com espaço antes, Total.csv, e nenhum videos.csv."""
    st = tmp_path / "studio"
    st.mkdir(parents=True)
    cab = ("Conteúdo,Título do vídeo,Horário de publicação do vídeo,Duração,Impressões de miniaturas,"
           "Taxa de cliques na miniatura (%),Visualizações,Visualizações intencionais,Tempo de exibição (horas),"
           "Duração média da visualização,Porcentagem visualizada média (%),Inscrições obtidas")
    linhas = ["Total,,,,4000,5.5,10100,4600,10.0,0:00:28,100,40",
              ' -abc,Pra ficar rico você só precisa de 1 centavo #investimentos,"Oct 30, 2023",20,3000,6,8000,3000,7.0,0:00:28,140,20',
              'b1,Dica #shorts,"Jan 10, 2025",30,500,4,1000,900,1.5,0:00:20,90,10',
              'b2,Outra #shorts,"Jun 10, 2025",30,300,5,600,400,1.0,0:00:20,90,6',
              'b3,Mais uma #shorts,"Jul 10, 2025",30,100,5,300,200,0.3,0:00:20,90,3',
              'b4,Última #shorts,"Aug 10, 2025",30,100,5,200,100,0.2,0:00:20,90,1']
    with zipfile.ZipFile(st / "studio_conteudo_shorts.zip", "w") as z:
        z.writestr("Dados da tabela.csv", "﻿" + cab + "\n" + "\n".join(linhas))
        z.writestr("Dados do gráfico.csv", "Data,Conteúdo,Visualizações\n2025-01-01,b1,1\n")
        z.writestr("Total.csv", "Data,Visualizações\n2025-01-01,1\n")
    d = an.Dados(tmp_path)
    assert d.so_studio and set(d.v) == {"-abc", "b1", "b2", "b3", "b4"}
    v = d.v["-abc"]
    assert v["formato"] == "short" and v["engajadas"] == 3000 and v["inscritos_studio"] == 20
    assert v["ctr"] == 6 and v["impressoes"] == 3000 and v["publicado"] == date(2023, 10, 30)
    conf = {c["metrica"]: c for c in an.conferencia_studio(d)}
    assert conf["views"]["total_studio"] == 10100 and conf["views"]["soma_linhas"] == 10100
    assert conf["views intencionais"]["dif_pct"] == 0 and conf["inscritos"]["soma_linhas"] == 40
    assert conf["CTR (%)"]["soma_linhas"] == pytest.approx((3000 * 6 + 500 * 4 + 500 * 5) / 4000)
    assert [x["id"] for x in an.outliers(list(d.v.values()))] == ["-abc"]
    grupos = {r["grupo"]: r for r in an.studio_por_formato(d)}
    assert grupos["sem outlier"]["views"] == 2100
    assert grupos["publicados a partir de 31/03/2025"]["razao"] == pytest.approx(1100 / 700)
    md = an.relatorio(d)
    assert "Conferência do Studio" in md and "sem outlier" in md and "só o Studio" in md


def test_studio_conferencia_com_totais_vitalicios_do_canal():
    """Confere, quando o ZIP real está no repositório, os totais vitalícios informados pelo Denis."""
    pasta = Path(__file__).resolve().parents[1] / "dados"
    if not (pasta / "studio" / "studio_conteudo_longos.zip").exists():
        pytest.skip("exportações reais do Studio ausentes")
    conf = {(c["exportacao"], c["metrica"]): c["total_studio"] for c in an.conferencia_studio(an.Dados(pasta))}
    assert conf[("longos", "impressões")] == pytest.approx(46.7e6, rel=0.01)
    assert conf[("longos", "CTR (%)")] == pytest.approx(7.1, abs=0.05)
    assert conf[("longos", "views")] == pytest.approx(13.07e6, rel=0.01)
    assert conf[("longos", "views intencionais")] == pytest.approx(12.92e6, rel=0.01)
    assert conf[("longos", "horas")] == pytest.approx(918.7e3, rel=0.01)
    assert conf[("shorts", "impressões")] == pytest.approx(23.7e6, rel=0.01)
    assert conf[("shorts", "views")] == pytest.approx(11.22e6, rel=0.01)
    assert conf[("shorts", "views intencionais")] == pytest.approx(5.75e6, rel=0.01)


def _zip_origem(p, tabela, grafico):
    with zipfile.ZipFile(p, "w") as z:
        z.writestr("Dados da tabela.csv", "﻿Origem do tráfego,Impressões de miniaturas,Taxa de cliques na miniatura (%),"
                   "Visualizações,Tempo de exibição (horas)\n" + tabela)
        z.writestr("Dados do gráfico.csv", "﻿Data,Origem do tráfego,Visualizações\n" + grafico)
        z.writestr("Total.csv", "Data,Visualizações\n2026-01,1\n")


def test_origem_mensal_do_studio_e_h3_com_os_dois_significados(tmp_path, monkeypatch):
    monkeypatch.setattr(an, "HOJE", date(2026, 10, 2))
    st = tmp_path / "studio"
    st.mkdir()
    meses = [f"{a}-{m:02d}" for a in (2025, 2026) for m in range(1, 13)][:21] + ["2026-10"]  # até 2026-09 + mês aberto
    g_todos, g_longos = [], []
    for k, m in enumerate(meses):
        sug = 29 if k < 6 else 2                     # Sugeridos: 29% → 2% nos longos
        g_longos += [f"{m},Vídeos sugeridos,{sug}", f"{m},Recursos de navegação,{100 - sug}"]
        g_todos += [f"{m},Vídeos sugeridos,{sug}", f"{m},Recursos de navegação,{100 - sug}", f"{m},Feed dos Shorts,100"]
    _zip_origem(st / "studio_origem_trafego_mensal.zip",
                "Total,300,6.5,1000,10\nPesquisa do YouTube,100,8.53,600,5\nFeed dos Shorts,,,400,1\n", "\n".join(g_todos))
    _zip_origem(st / "studio_origem_trafego_mensal_longos.zip", "Total,100,7,500,9\nRecursos de navegação,100,7.18,500,9\n",
                "\n".join(g_longos))
    escrever(tmp_path / "videos.csv", ["id", "titulo", "publicado_em_brt", "formato", "views"],
             [["a", "Vídeo", "2026-01-01 10:00:00", "longo", "10"]])
    d = an.Dados(tmp_path)
    s = an.origens_studio(d)
    assert set(s) == {"todos", "longos", "shorts (todos − longos)"}
    assert "2026-10" not in s["longos"]                                  # mês aberto fica fora
    assert s["shorts (todos − longos)"]["2026-09"] == {"RELATED_VIDEO": 0, "BROWSE": 0, "SHORTS": 100}
    H3 = next(h for h in an.hipoteses(d) if h["id"] == "H3")
    assert H3["veredito"] == "CONFIRMA"
    txt = " ".join(H3["numeros"])
    assert "Studio, longos · Sugeridos" in txt and "Navegação" in txt
    assert "mais se aproxima de 29% → 2%: Studio, longos · Sugeridos" in txt
    md = an.relatorio(d)
    assert "6b. Origem do tráfego, vitalício (todos" in md and "6c." in md


def test_conferencia_e3_real():
    pasta = Path(__file__).resolve().parents[1] / "dados" / "studio"
    if not (pasta / "studio_origem_trafego_mensal_longos.zip").exists():
        pytest.skip("E3 real ausente")
    def tab(nome):
        return {r["origem"]: r for r in an.ler_exportacao_studio(pasta / nome)["tabela"]}
    t, lo = tab("studio_origem_trafego_mensal.zip"), tab("studio_origem_trafego_mensal_longos.zip")
    assert an.num(t["Pesquisa do YouTube"]["views"]) == pytest.approx(7.64e6, rel=0.01)
    assert an.num(t["Pesquisa do YouTube"]["ctr"]) == 8.53
    assert an.num(t["Feed dos Shorts"]["views"]) == pytest.approx(6.42e6, rel=0.01)
    assert an.num(t["Recursos de navegação"]["views"]) == pytest.approx(5.45e6, rel=0.01)
    assert an.num(t["Recursos de navegação"]["ctr"]) == 6.92
    assert an.num(t["Vídeos sugeridos"]["views"]) == pytest.approx(1.33e6, rel=0.01)
    assert an.num(t["Vídeos sugeridos"]["ctr"]) == 3.51
    assert an.num(lo["Recursos de navegação"]["views"]) == pytest.approx(5.14e6, rel=0.01)
    assert an.num(lo["Recursos de navegação"]["ctr"]) == 7.18
    assert an.num(lo["Pesquisa do YouTube"]["views"]) == pytest.approx(3.26e6, rel=0.01)
    assert an.num(lo["Pesquisa do YouTube"]["ctr"]) == 12.32
