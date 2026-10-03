"""Dados de teste do OUTLIER → ENCAIXE: saída falsa do radar, canal do Denis, calendário de exemplo e gerador falso.
Nenhum teste usa a rede: o urlopen é trocado por um que explode."""
import csv
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AQUI))
import comum as c  # noqa: E402

AGORA = datetime(2026, 10, 5, 11, 0, tzinfo=timezone.utc)      # segunda 05/10, 8h em Brasília
HOJE = AGORA.date()


def iso(dt):
    return c.iso(dt)


def video(vid, titulo, idade_h, views, dur=600, obs=None, desc=""):
    pub = AGORA - timedelta(hours=idade_h)
    return {"video_id": vid, "titulo": titulo, "descricao": desc, "publicado": iso(pub), "views": views,
            "duracao_s": dur, "obs": obs if obs is not None else [[iso(AGORA), views]]}


def pares(prefixo, n, views=2000, idade0_h=120, passo_h=72, dur=600):
    return [video(f"{prefixo}{i:02d}", f"Vídeo antigo {i} sobre investimentos", idade0_h + i * passo_h, views, dur)
            for i in range(n)]


def snapshot():
    """Canal pequeno de FII com outlier; canal grande com outlier de dívida; canal médio com notícia quente;
    canal com histórico curto; outlier com poucas views."""
    return {"gerado_em": iso(AGORA), "fonte": "fixture", "canais": [
        {"nome": "Canal FII Pequeno", "channel_id": "UCfiiPequeno0000000000aa", "inscritos": 20_000,
         "videos": [video("fiiOUT00001", "MXRF11 reduziu o rendimento: a conta do cotista", 30, 9000,
                          desc="Link do cartão de crédito parceiro na descrição")] + pares("fii", 12)},
        {"nome": "Canal Dívida Grande", "channel_id": "UCdividaGrande00000000aa", "inscritos": 2_000_000,
         "videos": [video("divOUT00001", "Como sair das dívidas do cartão em 6 meses", 20, 400_000)]
         + pares("div", 12, views=40_000)},
        {"nome": "Canal Notícia Médio", "channel_id": "UCnoticiaMedio000000000a", "inscritos": 200_000,
         "videos": [video("newsOUT0001", "Copom corta a Selic: o que muda no Tesouro IPCA+", 10, 30_000)]
         + pares("nws", 12, views=4000)},
        {"nome": "Canal Novo", "channel_id": "UCcanalNovo0000000000000", "inscritos": 8_000,
         "videos": [video("novoOUT0001", "Fundos imobiliários: minha carteira de FII", 24, 20_000)] + pares("nov", 4)},
        {"nome": "Canal Minúsculo", "channel_id": "UCminusculo0000000000000", "inscritos": 3_000,
         "videos": [video("miniOUT0001", "Tesouro Selic: quanto rende hoje", 24, 1500)] + pares("min", 12, views=100)},
    ]}


VIDEOS_DENIS = [
    ("XOqLAz3dkV4", "MXRF11: o rendimento caiu? A conta do cotista de FII", "2026-08-26 19:00:00", "longo", 8000),
    ("Q1WMbZZn2Ik", "O QUE RENDE MAIS CDB ou LCI/LCA? #investimentos", "2025-04-28 12:00:00", "short", 50000),
    ("abcdefghijk", "Banco digital: como funciona", "2024-01-10 12:00:00", "longo", 3000),
]
ANALYTICS_DENIS = [("XOqLAz3dkV4", 5200, 410), ("Q1WMbZZn2Ik", 21000, 90)]

CAL_COLS = ["data", "dia", "formato", "assunto", "assunto_pelo_titulo", "titulo", "status_titulo", "serie_ep", "origem",
            "trocas_aplicadas", "termo_busca", "views_pesquisa_6m", "views_pesquisa_vitalicio", "demanda",
            "continuacao_de", "angulo", "inscritos_esperados", "faixa_p25_p75", "base_do_esperado", "fontes_a_conferir"]
CALENDARIO = [
    # data, formato, titulo, serie_ep, origem, esperado
    ("2026-10-04", "longo", "Pauta de ontem", "", "v2", 1.0),
    ("2026-10-06", "longo", "FII ou imóvel alugado: a conta", "", "v2", 45.3),
    ("2026-10-07", "short", "Short de renda", "", "v2", 2.2),
    ("2026-10-08", "longo", "Tesouro IPCA+ a 7%: quanto ganhou", "", "v2", 195.5),
    ("2026-10-13", "longo", "Episódio da série", "Ep. 1", "série de renda mensal", 5.0),
    ("2026-10-15", "longo", "Tesouro Direto antes do Copom", "", "Copom (versão pré)", 3.0),
    ("2026-10-16", "longo", "Copom hoje: o que olhar", "", "v2 (ângulo ajustado ao pré)", 4.0),
    ("2026-10-20", "longo", "Dividendos mensais: o calendário", "", "v2", 30.0),
    ("2026-10-22", "longo", "LCI e LCA ou CDB: a conta de 2026", "", "v2", 31.0),
    ("2026-10-27", "longo", "Fora da janela de 3 semanas", "", "v2", 0.5),
]
TROCAS_ORIGINAL = """{
  "descricao": "Trocas aprovadas (fixture).",
  "trocas": [
    {
      "id": "T01", "aprovada_em": "2026-10-03", "aprovada_por": "Denis Miyabara", "motivo": "fixture",
      "op": "move", "pauta": {"data": "2026-11-03", "formato": "longo", "titulo": "X"}, "para": "2026-11-05"
    }
  ]
}
"""
GERADOR_OK = """import json, pathlib
aqui = pathlib.Path(__file__).parent
n = len(json.loads((aqui / "trocas.json").read_text(encoding="utf-8"))["trocas"])
(aqui / "gerado.txt").write_text(str(n))
print(f"ok: calendário regenerado com {n} trocas")
"""
GERADOR_FALHA = "import sys\nprint('TrocaInvalida: pauta não encontrada')\nsys.exit(1)\n"


def escrever(p, texto):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(texto, encoding="utf-8")
    return p


def escrever_csv(p, cols, linhas):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(cols)
        w.writerows(linhas)
    return p


def montar_calendario(raiz, linhas=CALENDARIO):
    rows = []
    for data, fmt, tit, ep, origem, e in linhas:
        r = dict.fromkeys(CAL_COLS, "")
        r.update(data=data, dia="ter", formato=fmt, titulo=tit, serie_ep=ep, origem=origem, inscritos_esperados=e,
                 assunto="FII")
        rows.append([r[k] for k in CAL_COLS])
    escrever_csv(raiz / "pautas-canal" / "CALENDARIO.csv", CAL_COLS, rows)


