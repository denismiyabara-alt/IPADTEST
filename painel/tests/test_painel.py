import json
import shutil
from datetime import date, datetime

import pytest

from conftest import AGORA, CARD, args, escrever, gp, montar_canal, montar_site, montar_trader, tocar, wjson

H = 36


# ------------------------------------------------------------------------------------------- utilidades
def test_horas_uteis_ignora_fim_de_semana():
    sexta = datetime(2026, 10, 2, 19, 10, tzinfo=gp.BRT)
    assert gp.horas_uteis(sexta, AGORA) == pytest.approx(4 + 50 / 60 + 8 + 50 / 60)  # sexta 19h10 → seg 8h50
    assert gp.estado_por_idade(sexta, AGORA, H) == gp.OK
    assert gp.estado_por_idade(datetime(2026, 10, 1, 8, 0, tzinfo=gp.BRT), AGORA, H) == gp.VELHO
    assert gp.estado_por_idade(None, AGORA, H) == gp.SEM


def test_formatos_brasileiros():
    assert gp.num(165000) == "165.000"
    assert gp.num(49640.53, 2) == "49.640,53"
    assert gp.pct(-0.72, 1, True) == "-0,7%"
    assert gp.dmy(gp.ler_data("2026-10-01")) == "01/10/2026"
    assert gp.ultimo_pregao_antes(date(2026, 10, 5)) == date(2026, 10, 2)


# ------------------------------------------------------------------------------------------- CANAL
def test_canal_presente(arvore):
    b = gp.bloco_canal(arvore, AGORA, H)
    assert b["estado"] == gp.OK
    kp = {r: (v, n) for r, v, n in b["kpis"]}
    assert kp["Inscritos (contador público)"][0] == "165.000"
    assert "Vídeo do calendário HOJE" in kp and kp["Próximo do calendário"][0].startswith("06/10/2026")
    videos = [t for t in b["tabelas"] if t["titulo"] == "Últimos vídeos"][0]
    assert videos["linhas"][0][2] == "Vídeo novo" and videos["linhas"][0][4] == "3.100" and videos["linhas"][0][5] == "42%" and videos["linhas"][0][6] == "70%"
    r = b["fatos"]["ritmo"]
    assert r["base"] == "30d" and r["feito"] == 150 and r["abaixo"]
    assert any("mai/29" in n for n in b["notas"])


def test_canal_ritmo_com_dias_do_mes(tmp_path):
    montar_canal(tmp_path, dias_out=4)  # 4 dias de outubro, 25 líquidos por dia = 100 > 573*4/31 ≈ 74
    r = gp.bloco_canal(tmp_path, AGORA, H)["fatos"]["ritmo"]
    assert r["base"] == "mes" and r["feito"] == 100 and not r["abaixo"]


def test_canal_faltando(tmp_path):
    b = gp.bloco_canal(tmp_path, AGORA, H)
    assert b["estado"] == gp.SEM and "sem dado" in b["aviso"]
    assert b["fatos"]["calendario"] is None


def test_canal_velho(tmp_path):
    montar_canal(tmp_path, exportado="2026-09-29 10:00")
    b = gp.bloco_canal(tmp_path, AGORA, H)
    assert b["estado"] == gp.VELHO and b["aviso"].startswith("dado de 29/09/2026")
    assert b["kpis"]  # mostra o dado velho, com aviso


# ------------------------------------------------------------------------------------------- POSTS
def test_posts_presente_e_log_de_aplicacao(arvore):
    backup = arvore / "auditoria-fatos" / "backup"
    log = [{"acao": "aplicar", "post_id": 1, "trocas": [{"de": "auditoria-fatos-1", "para": "x"}]},
           # post 2 está nos dois lotes: a troca aplicada é a do lote de links, então só conta lá
           {"acao": "aplicar", "post_id": 2, "trocas": [{"de": "links-internos-2", "para": "x"}]},
           {"acao": "aplicar", "post_id": 3, "trocas": [{"de": "links-internos-3", "para": "x"}]},
           {"acao": "desfazer", "post_id": 3}]
    escrever(backup / "log_20261002.jsonl", "\n".join(json.dumps(x) for x in log) + "\nlixo\n")
    b = gp.bloco_posts(arvore, backup, arvore / "gate", AGORA, H)
    assert b["estado"] == gp.OK
    lotes = {x["lote"]: x for x in b["fatos"]["lotes"]}
    assert (lotes["A"]["aplicados"], lotes["A"]["pendentes"]) == (1, 1)
    assert (lotes["L1"]["aplicados"], lotes["L1"]["pendentes"]) == (1, 2)


def test_posts_faltando(tmp_path):
    b = gp.bloco_posts(tmp_path, tmp_path / "backup", tmp_path / "gate", AGORA, H)
    assert b["estado"] == gp.SEM and "sem dado" in b["aviso"]


def test_posts_gate_recente_e_velho(arvore):
    g = arvore / "gate"
    s = wjson(g / "gate_4873.saida.json", {"resultado": "BLOQUEADO", "titulo": "T", "bloqueantes": 1, "avisos": 2,
                                           "problemas": [{"codigo": "TICKER_PARADO", "nivel": "BLOQUEANTE"}]})
    e = escrever(g / "gate_estado.jsonl", '{"resultado": "OK"}\n{"resultado": "BLOQUEADO"}\n')
    tocar(s, datetime(2026, 10, 5, 7, 0, tzinfo=gp.BRT))
    tocar(e, datetime(2026, 10, 1, 7, 0, tzinfo=gp.BRT))
    b = gp.bloco_posts(arvore, arvore / "x", g, AGORA, H)
    tab = [t for t in b["tabelas"] if t["titulo"].startswith("Últimas saídas do gate")][0]
    assert tab["titulo"] == "Últimas saídas do gate"
    assert tab["linhas"][0][1] == "post 4873" and "TICKER_PARADO" in tab["linhas"][0][3]
    assert "1 bloqueados" in tab["linhas"][1][3]
    itens = gp.o_que_fazer([b], AGORA)
    assert itens[0][1].startswith("Post 4873 bloqueado no gate")

    tocar(s, datetime(2026, 9, 28, 7, 0, tzinfo=gp.BRT))
    b = gp.bloco_posts(arvore, arvore / "x", g, AGORA, H)
    tab = [t for t in b["tabelas"] if t["titulo"].startswith("Últimas saídas do gate")][0]
    assert "dado de" in tab["titulo"]
    assert not any("bloqueado no gate" in t for _, t in gp.o_que_fazer([b], AGORA))


def test_posts_wp_rest_opcional(arvore):
    falso = lambda url: [{"id": 9, "date": "2026-10-04T10:00:00", "title": {"rendered": "A &amp; B"}}]
    wp = gp.wp_recentes(transporte=falso)
    assert wp[0]["titulo"] == "A & B"

    def quebra(url):
        raise OSError("sem rede")

    assert gp.wp_recentes(transporte=quebra) is None
    b = gp.bloco_posts(arvore, arvore / "x", arvore / "gate", AGORA, H, wp)
    assert any(t["titulo"].startswith("Posts recentes") for t in b["tabelas"])
    b = gp.bloco_posts(arvore, arvore / "x", arvore / "gate", AGORA, H, [])
    assert any("sem resposta" in n for n in b["notas"])


# ------------------------------------------------------------------------------------------- TRADER
def test_trader_presente_com_sinal(tmp_path):
    t = montar_trader(tmp_path, sinais=[{"ticker": "AAAA3", "data_sinal": "2026-10-02", "setup": "x", "fechamento": 10}],
                      aprovadas=2)
    b = gp.bloco_trader(t, AGORA, H)
    assert b["estado"] == gp.OK  # sexta 19h15 → segunda 8h50: menos de 36 h úteis
    assert "SIMULAÇÃO" in b["titulo"]
    assert b["tabelas"][0]["titulo"].startswith("Sinais do dia (simulação")
    assert b["fatos"]["sinais"] == 1 and b["fatos"]["puts"] == 2
    kp = {r: (v, n) for r, v, n in b["kpis"]}
    papel = [v for r, v in kp.items() if r.startswith("Carteira de papel")][0]
    assert papel[0] == "R$ 49.640,53" and "-0,7%" in papel[1]
    item = gp.o_que_fazer([b], AGORA)[0][1]
    assert "1 sinal(is) de swing" in item and "simulação" in item


def test_trader_faltando(tmp_path):
    b = gp.bloco_trader(tmp_path / "nada", AGORA, H)
    assert b["estado"] == gp.SEM and "sem dado" in b["aviso"]
    assert "SIMULAÇÃO" not in gp.html_bloco(b).split("</h2>")[1]


def test_trader_velho(tmp_path):
    t = montar_trader(tmp_path, gerado="2026-09-30", aprovadas=3)
    b = gp.bloco_trader(t, AGORA, H)
    assert b["estado"] == gp.VELHO and "dado de 30/09/2026" in b["aviso"]
    itens = gp.o_que_fazer([b], AGORA)
    assert len(itens) == 1 and "sem rodada nova" in itens[0][1]  # sinal velho não vira tarefa


# ------------------------------------------------------------------------------------------- SITE
def test_site_presente(arvore):
    b = gp.bloco_site(arvore, AGORA, H)
    kp = {r: (v, n) for r, v, n in b["kpis"]}
    assert b["estado"] == gp.OK
    assert kp["Páginas geradas"] == ("3", "2 indexáveis")
    assert kp["COTAHIST (preços da B3) até"][0] == "02/10/2026" and b["fatos"]["cotahist_atrasado"] is False


def test_site_cotahist_atrasado(tmp_path):
    montar_site(tmp_path, cotahist="2026-09-30")
    b = gp.bloco_site(tmp_path, AGORA, H)
    assert b["fatos"]["cotahist_atrasado"] is True
    assert any("COTAHIST parado" in t for _, t in gp.o_que_fazer([b], AGORA))


def test_site_faltando_e_sem_sqlite(tmp_path):
    b = gp.bloco_site(tmp_path, AGORA, H)
    assert b["estado"] == gp.SEM
    montar_site(tmp_path)
    (tmp_path / "site-ativos" / "cache" / "dados.sqlite").unlink()
    b = gp.bloco_site(tmp_path, AGORA, H)
    assert b["estado"] == gp.OK and b["fatos"]["cotahist_atrasado"] is None


def test_site_velho(tmp_path):
    montar_site(tmp_path, gerado="2026-09-25T07:00:00")
    b = gp.bloco_site(tmp_path, AGORA, H)
    assert b["estado"] == gp.VELHO and b["aviso"].startswith("dado de 25/09/2026")
    assert any("Dado do site velho" in t for _, t in gp.o_que_fazer([b], AGORA))


# ------------------------------------------------------------------------------------------- RADAR
def test_radar_presente(arvore):
    b = gp.bloco_radar(arvore / "radar.json", arvore / "iec", AGORA, H)
    assert b["estado"] == gp.OK
    duvidas, videos = b["tabelas"]
    assert duvidas["linhas"][0] == ["1", "Tesouro Direto", "7"]
    assert [l[1] for l in videos["linhas"]] == ["Canal B"]  # o título sobre eleição fica de fora
    assert "Entenda" in videos["linhas"][0][2]
    assert any("Tesouro Direto" in t for _, t in gp.o_que_fazer([b], AGORA))


def test_radar_pouca_duvida(tmp_path):
    card = {"name": "Radar de comentários · semana de 05/10 · pouca dúvida",
            "desc": "**Semana com pouca dúvida**\n\n- **FIIs** — 2 pessoas perguntaram (X)\n"}
    wjson(tmp_path / "r.json", card)
    b = gp.bloco_radar(tmp_path / "r.json", tmp_path / "iec", AGORA, H)
    assert "pouca dúvida" in b["tabelas"][0]["titulo"]
    assert gp.o_que_fazer([b], AGORA) == []


def test_radar_faltando(tmp_path):
    b = gp.bloco_radar(tmp_path / "radar.json", tmp_path / "iec", AGORA, H)
    assert b["estado"] == gp.SEM and "radar_comentarios.py" in b["aviso"]


def test_radar_velho(arvore):
    tocar(arvore / "radar.json", datetime(2026, 9, 28, 8, 0, tzinfo=gp.BRT))
    (arvore / "iec" / "vault" / "Concorrentes" / "video-radar-2026-10-04.md").rename(
        arvore / "iec" / "vault" / "Concorrentes" / "video-radar-2026-09-20.md")
    b = gp.bloco_radar(arvore / "radar.json", arvore / "iec", AGORA, H)
    assert b["estado"] == gp.VELHO and b["aviso"].startswith("dado de 28/09/2026")
    assert b["tabelas"]  # continua mostrando, com a data
    assert gp.o_que_fazer([b], AGORA) == []  # radar velho não vira tarefa


# ------------------------------------------------------------------------------------------- O QUE FAZER HOJE
def test_o_que_fazer_ordem_e_limite(arvore):
    montar_trader(arvore, sinais=[{"ticker": "AAAA3", "data_sinal": "2026-10-02", "setup": "x"}])
    montar_site(arvore, cotahist="2026-09-29")
    wjson(arvore / "gate" / "gate_1.saida.json", {"resultado": "BLOQUEADO", "problemas": []})
    blocos, itens, _ = gp.gerar(args(arvore))
    assert len(itens) == gp.MAX_ITENS_HOJE
    assert [n for n, _ in itens] == ["CANAL", "POSTS", "POSTS", "CANAL", "TRADER"]
    assert itens[0][1].startswith("Vídeo do calendário para hoje (short): LCI ou CDB?")
    assert "Lote A de patches esperando: 2 posts" in itens[2][1] and "mais 1 lote" in itens[2][1]
    assert "abaixo do ritmo" in itens[3][1]


def test_o_que_fazer_nada(tmp_path):
    blocos, itens, pagina = gp.gerar(args(tmp_path))
    assert itens == [] and "Nada urgente" in pagina
    assert all(b["estado"] == gp.SEM for b in blocos)


def test_o_que_fazer_trader_sem_novidade_nao_aparece(tmp_path):
    t = montar_trader(tmp_path)
    assert gp.o_que_fazer([gp.bloco_trader(t, AGORA, H)], AGORA) == []
    t = montar_trader(tmp_path, aviso_reb="Rebalanceamento devido hoje (trimestral).", entram=["X"])
    assert "rebalanceamento" in gp.o_que_fazer([gp.bloco_trader(t, AGORA, H)], AGORA)[0][1]


# ------------------------------------------------------------------------------------------- HTML e main
def test_html_um_arquivo_sem_js_com_modo_escuro(arvore):
    escrever(arvore / "pautas-canal" / "CALENDARIO-8-SEMANAS.csv",
             "data,formato,titulo\n2026-10-05,short,<script>alert(1)</script>\n")
    _, _, pagina = gp.gerar(args(arvore))
    assert "<script" not in pagina and "&lt;script&gt;" in pagina
    assert "prefers-color-scheme:dark" in pagina and 'name="viewport"' in pagina
    assert "http" not in pagina.split("<style>")[1].split("</style>")[0]  # nada de CSS externo
    for nome in ("CANAL", "POSTS", "TRADER", "SITE", "RADAR"):
        assert f'<span class="tag">{nome}</span>' in pagina


def test_main_grava_arquivo_do_dia(arvore, capsys):
    a = ["--ipadtest", str(arvore), "--iec", str(arvore / "iec"), "--trader", str(arvore / "trader"),
         "--gate-dir", str(arvore / "gate"), "--radar-json", str(arvore / "radar.json"),
         "--saida", str(arvore / "saida"), "--agora", "2026-10-05T08:50"]
    assert gp.main(a) == 0
    assert (arvore / "saida" / "painel-2026-10-05.html").exists()
    assert "CANAL" in capsys.readouterr().out


def test_config_por_variavel_de_ambiente(tmp_path):
    a = gp.config(["--agora", "2026-10-05T08:50"], env={"PAINEL_IPADTEST": str(tmp_path), "PAINEL_TRADER": "/t",
                                                        "PAINEL_MAX_HORAS": "48"})
    assert a.ipadtest == str(tmp_path) and a.trader == "/t" and a.max_horas == 48
    assert a.backup == str(tmp_path / "auditoria-fatos" / "backup") and a.radar_json == "/tmp/radar.json"
    assert a.agora.tzinfo is not None and not a.wp_rest


def test_canal_usa_views_intencionais(arvore):
    """Desde 27/08 o contador infla; o painel compara pelas intencionais (engagedViews)."""
    b = gp.bloco_canal(arvore, AGORA, H)
    kp = {r: (v, n) for r, v, n in b["kpis"]}
    rot = [r for r in kp if r.startswith("Views intencionais em 7 dias")]
    assert rot and kp[rot[0]][0] == "2.800"  # 7 × 400, não 7 × 1000
    dias = [t for t in b["tabelas"] if t["titulo"] == "Últimos dias"][0]
    assert dias["cab"][1] == "views intencionais"


def test_canal_sem_intencionais_avisa_contador(tmp_path):
    montar_canal(tmp_path)
    p = tmp_path / "auditoria-canal" / "dados" / "canal_por_dia.csv"
    p.write_text("\n".join(l.rsplit(",", 1)[0] for l in p.read_text().splitlines()) + "\n")
    kp = [r for r, _, _ in gp.bloco_canal(tmp_path, AGORA, H)["kpis"]]
    assert any(r.startswith("Views (contador, inflado desde 27/08)") for r in kp)
