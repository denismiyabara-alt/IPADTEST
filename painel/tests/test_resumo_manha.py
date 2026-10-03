"""Testes do resumo_manha.py: sem rede, sem launchctl de verdade e sem Telegram."""
import json
from datetime import datetime, timedelta
from pathlib import Path

import pytest

from conftest import AGORA, escrever, gp, montar_trader, tocar, wjson

import resumo_manha as rm  # noqa: E402  (o conftest já pôs painel/ no sys.path)

# Saída realista do `launchctl list` no Mac (tabulada; PID "-" = parado; status negativo = sinal)
LAUNCHCTL = """PID\tStatus\tLabel
-\t0\tcom.apple.SafariHistoryServiceAgent
412\t0\tcom.apple.Finder
-\t0\tcom.denal.trader-novo
-\t1\tcom.denis.milhasrss
-\t0\tcom.denal.painel
-\t-9\tcom.denal.stocksignal
-\t0\tcom.denal.resumo-manha
731\t0\tcom.denal.extra-sem-config
-\t78\tcom.denis.milhasradar
-\t0\tcom.openssh.ssh-agent
"""

MILHAS_MD = """# Radar de milhas — posts de promoção

Gerado em 05/10/2026 10:40 · fonte: rss · 42 post(s) lido(s), 3 relevante(s)

Regra: programa E (destino OU palavra-chave forte), sem exclusão. ⭐ = número de milhas no texto abaixo do limite.

| | Data | Fonte | Post | Programa | Destino | Milhas | Cabine | Limite | Motivo |
|---|---|---|---|---|---|---|---|---|---|
| ⭐ novo | 05/10/2026 | Passageiro de Primeira | [Lisboa em executiva por 45 mil \\| ida](https://x/1) | smiles | LIS | 45.000 | executiva | 60.000 | destino |
| novo | 04/10/2026 | Melhores Destinos | [Smiles com bônus de 100%](https://x/2) | smiles | — | — | — | — | resgate |
| | 01/10/2026 | Pontos pra Voar | [Post antigo](https://x/3) | avios | — | — | — | — | resgate |

## Cobertura por programa

- **smiles**: 2 post(s)
"""

TERMO_LOG = """🌡️ Velho · 2,0 h no ar
Views 10 vs mediana 20
👉 Dentro do normal: não mexer agora.
🌡️ Selic a 15% · 2,1 h no ar
Views 900 vs mediana 2.010
CTR: informe com --ctr (o número só existe no Studio)
Retenção: o Analytics ainda não liberou o dado deste vídeo
👉 Views abaixo da mediana e sem CTR informado: confira o CTR no Studio; se estiver baixo, troque a thumb/título.
"""


def brt(*a):
    return datetime(*a, tzinfo=gp.BRT)


class TrelloFalso:
    """Responde como a API do Trello; guarda as URLs pedidas."""

    def __init__(self, por_lista=None, corpo=None, erro=None):
        self.por_lista, self.corpo, self.erro, self.urls = por_lista or {}, corpo, erro, []

    def __call__(self, url):
        self.urls.append(url)
        if self.erro:
            raise self.erro
        if self.corpo is not None:
            return self.corpo
        lid = url.split("/lists/")[1].split("/")[0]
        return json.dumps(self.por_lista.get(lid, []))


TRELLO_OK = TrelloFalso({
    "L1": [{"id": "a" * 24, "name": "💡 Thread DY do BTG", "dateLastActivity": "2026-09-29T12:00:00.000Z"},
           {"id": "b" * 24, "name": "🧵 Tesouro IPCA+", "dateLastActivity": "2026-10-04T12:00:00.000Z"},
           {"id": "c" * 24, "name": "🧵 FII de papel", "dateLastActivity": "2026-10-02T12:00:00.000Z"}],
    "L2": [{"id": "d" * 24, "name": "Carrossel Selic", "dateLastActivity": "2026-09-30T09:00:00.000Z"}],
    "L3": [],
})

ENV_TRELLO = {"TRELLO_KEY": "kkk-falsa", "TRELLO_TOKEN": "ttt-falso"}


def montar_extras(raiz):
    """Saídas dos radares e dos jobs, todas frescas para segunda 05/10 8h50."""
    m = escrever(raiz / "milhas" / "milhas_relatorio.md", MILHAS_MD)
    tocar(m, brt(2026, 10, 5, 7, 41))
    t = escrever(raiz / "iec" / "termometro.log", TERMO_LOG)
    tocar(t, brt(2026, 10, 4, 21, 5))
    escrever(raiz / "iec" / "termometro_historico.jsonl",
             json.dumps({"video": "abc", "medido_em": "2026-10-04T23:05+00:00", "horas": 2.1, "views": 900,
                         "ctr": None, "retencao": None}) + "\n")
    for nome, quando in (("painel-2026-10-02.html", brt(2026, 10, 2, 8, 51)),
                         ("resumo.log", brt(2026, 10, 2, 8, 51))):
        tocar(escrever(raiz / "jobs" / nome, "x"), quando)


def config(raiz, **troca):
    cfg = {
        "painel": {"ipadtest": str(raiz), "iec": str(raiz / "iec"), "trader": str(raiz / "trader"),
                   "gate_dir": str(raiz / "gate"), "radar_json": str(raiz / "radar.json"), "max_horas": 36},
        "painel_html": str(raiz / "saida" / "painel-{data}.html"),
        "milhas": {"relatorio": str(raiz / "milhas" / "milhas_relatorio.md"), "max_horas": 26},
        "comentarios": {"novas_horas": 24, "max_horas": 192},
        "termometro": {"log": str(raiz / "iec" / "termometro.log"),
                       "historico": str(raiz / "iec" / "termometro_historico.jsonl"), "max_horas": 24},
        "trello": {"listas": [{"nome": "Aprovar X", "id": "L1"}, {"nome": "Aprovar Instagram", "id": "L2"},
                              {"nome": "Aprovar Blog", "id": "L3"}], "credenciais": [str(raiz / "nada.env")]},
        "jobs": {"tolerancia_min": 30, "esperados": [
            {"label": "com.denis.milhasrss", "horario": "07:40", "dias": "todos",
             "saida": str(raiz / "milhas" / "milhas_relatorio.md")},
            {"label": "com.denal.painel", "horario": "08:50", "dias": "uteis",
             "saida": str(raiz / "jobs" / "painel-{data}.html")},
            {"label": "com.denal.resumo-manha", "horario": "08:50", "dias": "uteis",
             "saida": str(raiz / "jobs" / "resumo.log")},
            {"label": "com.denal.trader-novo", "horario": "19:10", "dias": "uteis",
             "saida": str(raiz / "trader" / "swing_v2_resultado.json"), "tolerancia_min": 90},
            {"label": "com.denal.termometro", "a_cada_min": 60, "opcional": True},
            {"label": "com.denal.stocksignal", "horario": "09:15", "dias": "todos", "opcional": True},
            {"label": "com.denis.milhasradar", "horario": "03:00", "opcional": True},
        ]},
    }
    cfg.update(troca)
    return cfg


@pytest.fixture
def completo(arvore):
    montar_extras(arvore)
    return arvore


def coletar(raiz, cfg=None, lc=LAUNCHCTL, trello=TRELLO_OK, env=ENV_TRELLO, agora=AGORA):
    return rm.coletar(cfg or config(raiz), agora, env=dict(env), ler_launchctl=lambda: lc,
                      trello_transporte=trello)


# ------------------------------------------------------------------------------------------- mensagem inteira
def test_mensagem_completa_na_ordem(completo):
    d = coletar(completo)
    txt = rm.montar_mensagem(d)
    pos = [txt.index(s) for s in ("🎯 Decidir hoje", "📋 Trello", "📡 Radares", "✈️ Milhas", "💬 Comentários",
                                  "🌡️ Termômetro", "📈 Trader [SIMULAÇÃO]", "⚙️ Jobs")]
    assert pos == sorted(pos)
    assert rm.tamanho_telegram(txt) <= rm.LIMITE_TELEGRAM
    assert "kkk-falsa" not in txt and "ttt-falso" not in txt
    assert 1 <= len(d["decidir"]) <= 5
    assert d["decidir"][0].startswith("Vídeo do calendário para hoje")  # 1º item do painel
    assert d["decidir"][1].startswith("Aprovar no Trello: 4 card(s)")
    assert any(x.startswith("Promo de milhas ⭐ 45.000 mi") for x in d["decidir"])
    assert any(x.startswith("Job com problema: milhasrss (saiu com 1)") for x in d["decidir"])


def test_reaproveita_o_que_fazer_do_painel(completo):
    d = coletar(completo)
    a = gp.config(["--ipadtest", str(completo), "--iec", str(completo / "iec"), "--trader", str(completo / "trader"),
                   "--gate-dir", str(completo / "gate"), "--radar-json", str(completo / "radar.json"),
                   "--agora", "2026-10-05T08:50"], env={})
    _, itens, _ = gp.gerar(a)
    assert [t for _, t in d["itens_painel"]] == [t for _, t in itens]


def test_tudo_faltando_nao_quebra(tmp_path):
    cfg = config(tmp_path, trello={"listas": [{"nome": "Aprovar X", "id": "L1"}],
                                   "credenciais": [str(tmp_path / "nada.env")]})
    d = rm.coletar(cfg, AGORA, env={}, ler_launchctl=lambda: None, trello_transporte=TRELLO_OK)
    txt = rm.montar_mensagem(d)
    for linha in ("📋 Trello: sem dado (faltam TRELLO_KEY e TRELLO_TOKEN)", "✈️ Milhas: sem dado",
                  "💬 Comentários: sem dado", "🌡️ Termômetro: sem dado", "📈 Trader [SIMULAÇÃO]: sem dado"):
        assert linha in txt
    assert "(sem launchctl: só a idade das saídas)" in txt


# ------------------------------------------------------------------------------------------- milhas
def test_milhas_presente(completo):
    m = rm.ler_milhas(config(completo)["milhas"], AGORA)
    assert m["estado"] == gp.OK and (m["relevantes"], m["estrelas"], m["novos"]) == (3, 1, 2)
    assert m["destaque"][0]["titulo"] == "Lisboa em executiva por 45 mil | ida"  # \| desfeito
    linhas = rm.linhas_milhas(m, AGORA)
    assert linhas[0] == "✈️ Milhas: 1 ⭐ e 2 novo(s)"
    assert linhas[1].startswith("  • ⭐ 45.000 mi · Lisboa") and "Post antigo" not in "\n".join(linhas)


def test_milhas_faltando(tmp_path):
    m = rm.ler_milhas({"relatorio": str(tmp_path / "x.md")}, AGORA)
    assert m["estado"] == gp.SEM and rm.linhas_milhas(m, AGORA)[0].startswith("✈️ Milhas: sem dado (não achei")


def test_milhas_velho(completo):
    tocar(completo / "milhas" / "milhas_relatorio.md", brt(2026, 10, 3, 7, 40))
    m = rm.ler_milhas(config(completo)["milhas"], AGORA)
    assert rm.linhas_milhas(m, AGORA) == ["✈️ Milhas: sem dado (relatório de sáb 03/10 07:40)"]


def test_milhas_sem_novidade(completo):
    m = escrever(completo / "milhas" / "milhas_relatorio.md",
                 MILHAS_MD.replace("⭐ novo |", " |").replace("| novo |", "| |"))
    tocar(m, brt(2026, 10, 5, 7, 41))
    m = rm.ler_milhas(config(completo)["milhas"], AGORA)
    assert rm.linhas_milhas(m, AGORA)[0].startswith("✈️ Milhas: nada novo (3 relevante(s)")


# ------------------------------------------------------------------------------------------- comentários
def test_comentarios_presente(completo):
    d = coletar(completo)
    assert rm.linhas_comentarios(d["comentarios"], AGORA) == [
        "💬 Comentários: Tesouro Direto (7), FIIs (4), Juros e Selic (3)"]


def test_comentarios_faltando(tmp_path):
    c = rm.ler_comentarios(None, tmp_path / "radar.json", {}, AGORA)
    assert rm.linhas_comentarios(c, AGORA)[0].startswith("💬 Comentários: sem dado (sem card em")


def test_comentarios_sem_pergunta_nova_e_velho(completo):
    radar = completo / "radar.json"
    bloco = {"fatos": {"card": {"top": [("FIIs", 4)], "pouca": False}}}
    tocar(radar, brt(2026, 10, 1, 8, 0))  # quinta: não é novo, mas está na semana
    c = rm.ler_comentarios(bloco, radar, {"novas_horas": 24, "max_horas": 192}, AGORA)
    assert rm.linhas_comentarios(c, AGORA) == ["💬 Comentários: nenhuma pergunta nova (card de qui 01/10 08:00)"]
    tocar(radar, brt(2026, 9, 20, 8, 0))
    c = rm.ler_comentarios(bloco, radar, {"novas_horas": 24, "max_horas": 192}, AGORA)
    assert rm.linhas_comentarios(c, AGORA) == ["💬 Comentários: sem dado (card de dom 20/09 08:00)"]


# ------------------------------------------------------------------------------------------- termômetro
def test_termometro_presente_pelo_log(completo):
    t = rm.ler_termometro(config(completo)["termometro"], AGORA)
    linhas = rm.linhas_termometro(t)
    assert linhas[0] == "🌡️ Termômetro: Selic a 15% · 2,1 h no ar · Views 900 vs mediana 2.010"
    assert linhas[1].startswith("  👉 Views abaixo da mediana")


def test_termometro_pelo_historico_quando_nao_ha_log(completo):
    cfg = dict(config(completo)["termometro"], log=str(completo / "nao-existe.log"))
    t = rm.ler_termometro(cfg, AGORA)
    assert rm.linhas_termometro(t) == ["🌡️ Termômetro: vídeo abc · 900 views com 2,1 h"]


def test_termometro_faltando_e_velho(completo, tmp_path):
    t = rm.ler_termometro({"log": str(tmp_path / "a"), "historico": str(tmp_path / "b")}, AGORA)
    assert rm.linhas_termometro(t) == ["🌡️ Termômetro: sem dado (nenhuma medição recente)"]
    tocar(completo / "iec" / "termometro.log", brt(2026, 10, 1, 21, 0))
    escrever(completo / "iec" / "termometro_historico.jsonl",
             json.dumps({"video": "abc", "medido_em": "2026-10-01T21:00", "horas": 2, "views": 1}) + "\n")
    t = rm.ler_termometro(config(completo)["termometro"], AGORA)
    assert rm.linhas_termometro(t) == ["🌡️ Termômetro: sem dado (última medição qui 01/10 21:00)"]


# ------------------------------------------------------------------------------------------- trader
def test_trader_presente_com_rotulo_simulacao(completo):
    d = coletar(completo)
    l = rm.linhas_trader(d["trader"])[0]
    assert l.startswith("📈 Trader [SIMULAÇÃO], rodada de 02/10/2026 19:15: 0 sinal(is) de swing · 0 put(s)")
    assert "papel R$ 49.640,53 (-0,7%)" in l


def test_trader_faltando_e_velho(tmp_path):
    assert rm.linhas_trader(gp.bloco_trader(tmp_path, AGORA, 36)) == [
        "📈 Trader [SIMULAÇÃO]: sem dado (não achei os JSON do trader)"]
    montar_trader(tmp_path, gerado="2026-09-29")
    assert rm.linhas_trader(gp.bloco_trader(tmp_path / "trader", AGORA, 36)) == [
        "📈 Trader [SIMULAÇÃO]: sem dado (rodada de 29/09/2026 19:15)"]


# ------------------------------------------------------------------------------------------- Trello
def test_trello_resposta_falsa(completo):
    t = rm.ler_trello(config(completo)["trello"], ENV_TRELLO, TRELLO_OK)
    assert t["estado"] == gp.OK and t["total"] == 4
    assert t["contagem"] == [("Aprovar X", 3), ("Aprovar Instagram", 1), ("Aprovar Blog", 0)]
    assert [c["nome"] for c in t["antigos"]] == ["💡 Thread DY do BTG", "Carrossel Selic", "🧵 FII de papel"]
    linhas = rm.linhas_trello(t, AGORA)
    assert linhas[0] == "📋 Trello: 4 esperando aprovação (Aprovar X 3 · Aprovar Instagram 1 · Aprovar Blog 0)"
    assert linhas[1] == "  • 💡 Thread DY do BTG (Aprovar X, há 5 d)"
    assert all("key=kkk-falsa" in u and u.startswith("https://api.trello.com/1/lists/") for u in TRELLO_OK.urls)


def test_trello_invalid_key_em_texto_puro(completo):
    t = rm.ler_trello(config(completo)["trello"], ENV_TRELLO, TrelloFalso(corpo="invalid key"))
    assert t["estado"] == gp.SEM and "invalid key" in t["motivo"] and "TRELLO_KEY" in t["motivo"]


def test_trello_rede_falha_sem_vazar_token(completo):
    erro = OSError("falhou em https://api.trello.com/1/lists/L1/cards?key=kkk-falsa&token=ttt-falso")
    t = rm.ler_trello(config(completo)["trello"], ENV_TRELLO, TrelloFalso(erro=erro))
    assert t["estado"] == gp.SEM and "kkk-falsa" not in t["motivo"] and "ttt-falso" not in t["motivo"]


def test_trello_credencial_do_arquivo_e_lista_por_nome(tmp_path):
    env_arq = escrever(tmp_path / "credentials.env", "# x\nexport TRELLO_KEY='k2'\nTRELLO_TOKEN=\"t2\"\n")
    falso = TrelloFalso()

    def transporte(url):
        falso.urls.append(url)
        if "/boards/" in url:
            return json.dumps([{"id": "LX", "name": "Aprovar X"}])
        return json.dumps([{"id": "e" * 24, "name": "c1"}])  # sem dateLastActivity: data vem do id

    t = rm.ler_trello({"board_id": "B", "listas": [{"nome": "Aprovar X"}], "credenciais": [str(env_arq)]}, {},
                      transporte)
    assert t["estado"] == gp.OK and t["contagem"] == [("Aprovar X", 1)] and t["antigos"][0]["desde"] is not None
    assert "key=k2&token=t2" in falso.urls[0]


# ------------------------------------------------------------------------------------------- jobs
def test_parse_launchctl():
    lc = rm.parse_launchctl(LAUNCHCTL)
    assert lc["com.denal.trader-novo"] == {"pid": None, "status": 0}
    assert lc["com.apple.Finder"] == {"pid": 412, "status": 0}
    assert lc["com.denal.stocksignal"]["status"] == -9 and lc["com.denis.milhasradar"]["status"] == 78
    assert "Label" not in lc and len(lc) == 10


def test_jobs_presente(completo):
    j = rm.avaliar_jobs(config(completo)["jobs"], AGORA, LAUNCHCTL)
    r = {n: (ok, m) for n, ok, m in j["jobs"]}
    assert r["milhasrss"] == (False, "saiu com 1")
    assert r["stocksignal"] == (False, "saiu com -9")
    assert r["milhasradar"] == (False, "saiu com 78")
    assert r["painel"] == (True, "") and r["resumo-manha"] == (True, "")  # 8h50 de hoje ainda no prazo: vale sexta
    assert r["trader-novo"] == (True, "") and r["extra-sem-config"] == (True, "")
    assert "termometro" not in r  # opcional e fora do launchctl
    linha = rm.linha_jobs(j)
    assert linha.startswith("⚙️ Jobs: ❌ milhasrss (saiu com 1) · ❌ stocksignal (saiu com -9)")
    assert "✅ painel, resumo-manha, trader-novo, extra-sem-config" in linha and "\n" not in linha


def test_jobs_nao_rodou_no_horario_e_nao_carregado(completo):
    tocar(completo / "trader" / "swing_v2_resultado.json", brt(2026, 10, 1, 19, 20))  # parou na quinta
    lc = LAUNCHCTL.replace("-\t0\tcom.denal.painel\n", "")
    j = rm.avaliar_jobs(config(completo)["jobs"], AGORA, lc)
    r = {n: (ok, m) for n, ok, m in j["jobs"]}
    assert r["trader-novo"] == (False, "não rodou sex 02/10 19:10")
    assert r["painel"] == (False, "não carregado")


def test_jobs_saida_faltando_e_sem_launchctl(tmp_path):
    cfg = {"esperados": [{"label": "com.denal.x", "horario": "07:00", "saida": str(tmp_path / "nada.log")},
                         {"label": "com.denal.opc", "horario": "07:00", "saida": str(tmp_path / "n"), "opcional": True},
                         {"label": "com.denal.sem-saida", "a_cada_min": 60}]}
    j = rm.avaliar_jobs(cfg, AGORA, None)
    assert j["jobs"] == [("x", False, "sem saída")] and not j["launchctl"]
    assert rm.linha_jobs(rm.avaliar_jobs({}, AGORA, None)).startswith("⚙️ Jobs: sem dado")


def test_execucao_esperada():
    seg = AGORA
    assert rm.execucao_esperada({"horario": "07:40"}, seg, 30) == brt(2026, 10, 5, 7, 40)
    assert rm.execucao_esperada({"horario": "08:50", "dias": "uteis"}, seg, 30) == brt(2026, 10, 2, 8, 50)
    assert rm.execucao_esperada({"horario": "08:00", "dias": ["seg"]}, seg, 30) == brt(2026, 10, 5, 8, 0)
    assert rm.execucao_esperada({"a_cada_min": 60}, seg, 30) == seg - timedelta(minutes=90)
    assert rm.execucao_esperada({}, seg, 30) is None


# ------------------------------------------------------------------------------------------- corte e envio
def test_corte_em_4096(completo):
    d = coletar(completo)
    d["decidir"] = ["x" * 160] * 5
    d["trello"]["antigos"] = [{"nome": "card " + "y" * 300, "lista": "Aprovar X", "desde": None}] * 40
    txt = rm.montar_mensagem(d, "painel-2026-10-05.html")
    assert rm.tamanho_telegram(txt) <= 4096
    assert txt.endswith("✂️ Cortado: ver painel (painel-2026-10-05.html)")
    assert txt.startswith("☀️ Resumo da manhã · seg 05/10 · 08:50")


def test_corte_conta_emoji_como_dois_e_linha_gigante():
    assert rm.tamanho_telegram("☀️") == 2 and rm.tamanho_telegram("🎯") == 2
    txt = rm.cortar("🎯" * 3000)
    assert rm.tamanho_telegram(txt) <= 4096 and "ver painel" in txt
    assert rm.cortar("curto") == "curto"


def test_dry_run_nao_envia(completo, monkeypatch, capsys):
    cfg = completo / "cfg.json"
    wjson(cfg, config(completo))
    lc = escrever(completo / "lc.txt", LAUNCHCTL)

    def proibido(*a, **k):
        raise AssertionError("dry-run tentou usar a rede")

    monkeypatch.setattr(rm, "_telegram_post", proibido)
    monkeypatch.setattr(rm, "_trello_get", proibido)
    monkeypatch.setattr(rm.urllib.request, "urlopen", proibido)
    env = {"TELEGRAM_BOT_TOKEN": "tok", "TELEGRAM_CHAT_ID": "1"}
    assert rm.main(["--config", str(cfg), "--dry-run", "--agora", "2026-10-05T08:50", "--sem-trello",
                    "--launchctl-arquivo", str(lc)], env=env) == 0
    out = capsys.readouterr().out
    assert out.startswith("☀️ Resumo da manhã · seg 05/10 · 08:50") and "[dry-run: nada enviado" in out
    assert "📋 Trello: sem dado (desligado com --sem-trello)" in out


def test_envio_usa_variaveis_e_texto_puro():
    pedidos = []

    def transporte(url, dados):
        pedidos.append((url, dados))
        return {"ok": True}

    rm.enviar_telegram("oi_*x*", env={"TELEGRAM_BOT_TOKEN": "TK", "TELEGRAM_HOME_CHANNEL": "99"}, arquivos=[],
                       transporte=transporte)
    url, dados = pedidos[0]
    assert url == "https://api.telegram.org/botTK/sendMessage"
    assert b"chat_id=99" in dados and b"parse_mode" not in dados


def test_envio_sem_credencial_e_falha_sem_vazar(tmp_path):
    with pytest.raises(RuntimeError, match="faltam TELEGRAM_BOT_TOKEN"):
        rm.enviar_telegram("x", env={}, arquivos=[str(tmp_path / "nada.env")])

    def cai(url, dados):
        raise OSError(f"erro em {url}")

    with pytest.raises(RuntimeError) as e:
        rm.enviar_telegram("x", env={"TELEGRAM_BOT_TOKEN": "SEGREDO", "TELEGRAM_CHAT_ID": "1"}, transporte=cai)
    assert "SEGREDO" not in str(e.value)


def test_main_envio_falho_sai_com_1(completo, monkeypatch, capsys):
    cfg = completo / "cfg.json"
    wjson(cfg, config(completo))
    monkeypatch.setattr(rm, "_telegram_post", lambda u, d: {"ok": False, "description": "chat not found"})
    r = rm.main(["--config", str(cfg), "--agora", "2026-10-05T08:50", "--sem-trello",
                 "--launchctl-arquivo", str(completo / "nao-existe.txt")],
                env={"TELEGRAM_BOT_TOKEN": "tok", "TELEGRAM_CHAT_ID": "1"})
    assert r == 1 and "chat not found" in capsys.readouterr().err


def test_config_do_repositorio_e_valida_e_sem_segredo():
    p = Path(rm.__file__).with_name("resumo_manha.json")
    texto = p.read_text(encoding="utf-8")
    cfg = json.loads(texto)
    assert [l["nome"] for l in cfg["trello"]["listas"]] == ["Aprovar X", "Aprovar Instagram", "Aprovar Blog"]
    labels = [j["label"] for j in cfg["jobs"]["esperados"]]
    assert "com.denal.resumo-manha" in labels and "com.denis.milhasrss" in labels
    for proibido in ("TOKEN=", "KEY=", "telegram.org/bot", "claude-"):
        assert proibido not in texto.replace("TELEGRAM_BOT_TOKEN", "").replace("TRELLO_TOKEN", "")


# --------------------------------------------------------------------------------------------- outliers
LINHA_FII = "🔥 Outlier: MXRF11 corta o rendimento: o que muda na sua cota (Canal FII, 8.4x) → proposta: trocar o de 13/10"
LINHA_SHORT = "🔥 Outlier: Parecer da CVM muda FII (Canal Y, 5x) → Short rápido"


def _propostas(raiz, gerado="2026-10-05T10:15:00Z", linhas=(LINHA_FII, LINHA_SHORT)):
    return wjson(raiz / "outliers" / "propostas.json",
                 {"gerado_em": gerado, "propostas": [{"id": f"OUT-{i}", "linha_resumo": l} for i, l in enumerate(linhas)]})


def test_outlier_aparece_depois_do_decidir_hoje(completo):
    p = _propostas(completo)
    d = coletar(completo, config(completo, outliers={"propostas": str(p), "max_horas": 26, "max_linhas": 2}))
    txt = rm.montar_mensagem(d)
    assert LINHA_FII in txt and LINHA_SHORT in txt
    assert txt.index("🎯 Decidir hoje") < txt.index(LINHA_FII) < txt.index("📋 Trello")


def test_outlier_respeita_max_linhas(completo):
    p = _propostas(completo)
    d = coletar(completo, config(completo, outliers={"propostas": str(p), "max_linhas": 1}))
    txt = rm.montar_mensagem(d)
    assert LINHA_FII in txt and LINHA_SHORT not in txt


def test_sem_outlier_a_linha_nao_aparece(completo):
    sem = _propostas(completo, linhas=())
    for cfg_o in ({}, {"propostas": str(completo / "nao-existe.json")}, {"propostas": str(sem)}):
        txt = rm.montar_mensagem(coletar(completo, config(completo, outliers=cfg_o)))
        assert "🔥" not in txt


def test_outlier_velho_nao_aparece(completo):
    p = _propostas(completo, gerado="2026-10-03T08:00:00Z")
    txt = rm.montar_mensagem(coletar(completo, config(completo, outliers={"propostas": str(p), "max_horas": 26})))
    assert "🔥" not in txt


def test_config_tem_outliers():
    cfg = json.loads(Path(rm.__file__).with_name("resumo_manha.json").read_text(encoding="utf-8"))
    assert cfg["outliers"]["propostas"].endswith("outliers/saida/propostas.json")
