"""Testes do pacote da semana (sem rede). Os que leem os repos vizinhos pulam se eles não existirem."""
import sys
from datetime import date
from pathlib import Path

import pytest

AQUI = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(AQUI))
import gerar_semana as gs  # noqa: E402

DOMINGO = date(2026, 10, 4)


def test_semana_vai_de_segunda_a_domingo():
    seg, dom = gs.semana(DOMINGO)
    assert (seg, dom) == (date(2026, 10, 5), date(2026, 10, 11))
    assert gs.dia(seg) == "seg 05/10" and gs.dia(dom) == "dom 11/10"


def test_versao_pega_a_maior():
    assert gs.versao_num("v1.5 (v1.0 → v1.7 conserto)") == (1, 7)
    assert gs.versao_num("v5 (v4 ← v3)") == (5,)
    assert gs.versao_num("sem versão") is None


def test_curto_limpa_markdown_e_corta():
    assert gs.curto("**Lei** `x` [a](b)") == "Lei x a"
    assert len(gs.curto("a" * 400)) == gs.MAX and gs.curto("a" * 400).endswith("…")


TEXTO = """---
versao: v1.3
pendente_do_denis:
  - "[ ] Pronúncia do código: confirmar"
---
Fala, Tanaka.

## Validações do Denis (antes de gravar)

1. **Resolvida (Denis, 03/10):** piada aprovada.
2. **Lei X:** conferir o artigo 3º
   na primária.
3. Rodar no Mac: o portão.
4. Rodar ouvinte novo na v1.1.

Texto. **Denis valida:** (a) a regra do carnê-leão;
(b) o IR zero.

### Ouvinte-frio cego (v1.2) e correções v1.3

Média 7,4, REPROVA (bloco 4).

## Juiz-roteiro (rubrica 9/10)
"""


def test_pendencias_extrai_e_classifica():
    p = gs.pendencias(TEXTO, (1, 3))
    textos = [t for _, t in p]
    assert any("Pronúncia" in t for t in textos)                  # frontmatter
    assert any("Lei X" in t and "na primária" in t for t in textos)  # continuação de linha
    assert any("carnê-leão" in t and "IR zero" in t for t in textos)  # "Denis valida:" solto
    assert not any("Resolvida" in t for t in textos)               # resolvidas saem
    assert not any("v1.1" in t for t in textos)                    # tarefa de versão superada sai
    assert ("tarefa", "Rodar no Mac: o portão.") in p


def test_ouvinte_usa_a_versao_ouvida_e_juiz():
    assert gs.ouvinte(TEXTO) == ((1, 2), "reprovou", "7,4")
    assert gs.juiz(TEXTO) == "9"


def test_barsi_e_louise_sem_agenda(tmp_path):
    (tmp_path / "agenda_lote1.tsv").write_text(
        "04/10 12h\tAAAAAAAAAAA\tfora da semana\n05/10 12h\tBBBBBBBBBBB\tBarsi: um #shorts\n"
        "05/10 18h\tfonte@1:00\tBarsi: dois #shorts\n06/10 12h\tPENDENTE\t\n", encoding="utf-8")
    bl, lou = gs.barsi(date(2026, 10, 5), date(2026, 10, 11), tmp_path, None)
    assert bl[0].startswith("- **seg 05/10** ⏳ 12h Barsi: um · 18h Barsi: dois")
    assert bl[1].startswith("- **ter 06/10** ❌")
    assert not any("fora da semana" in l for l in bl)
    assert lou == ["- agenda não encontrada no repo — onde fica?"]


def test_faz_a_conta_status(tmp_path):
    (tmp_path / "banco-central").mkdir()
    (tmp_path / "banco-central" / "TITULO.md").write_text("1. **Título BC** (recomendado)\n", encoding="utf-8")
    (tmp_path / "banco-central" / "descricao.txt").write_text("Resumo.\n", encoding="utf-8")
    (tmp_path / "emendas").mkdir()
    (tmp_path / "emendas" / "roteiro.md").write_text("| x | 1 | fonte | a conferir |\n", encoding="utf-8")
    linhas = gs.faz_a_conta(date(2026, 10, 5), date(2026, 10, 11), tmp_path, None)
    assert any("Título BC" in l and "✅ agendado 18h" in l for l in linhas)
    em = [l for l in linhas if "emendas" in l and "dom 11/10" in l][0]
    assert "❌ pendente" in em and "1 números a conferir" in em and "título" in em
    assert linhas[-1].startswith("- Semana seguinte: ter 13/10 espanha")
    assert gs.faz_a_conta(date(2026, 10, 5), date(2026, 10, 11), None, None)[0].startswith("- ❌ repo faz-a-conta")


def test_canais_dark_em_producao_ou_lido(tmp_path, monkeypatch):
    monkeypatch.setattr(gs, "RAIZ", tmp_path)
    out = gs.canais_dark()
    assert all("em produção" in l for l in out) and len(out) == 2
    p = tmp_path / "canais-dark" / "espionagem"
    p.mkdir(parents=True)
    (p / "COMO-RODAR.md").write_text("```bash\npython3 fazer.py ep1\n```\n", encoding="utf-8")
    (p / "CONFERIR-NO-MAC.md").write_text("- [ ] voz\n- [ ] música\n", encoding="utf-8")
    out = gs.canais_dark()
    esp = [l for l in out if "Eichmann" in l][0]
    assert "falta roteiro, VOZ" in esp and "2 itens a conferir no Mac" in esp and "python3 fazer.py ep1" in esp


def test_pacote_real_2026_10_04():
    fac, bar = gs.achar_repo("faz-a-conta"), gs.achar_repo("barsi-cortes")
    if not (gs.RAIZ / "pautas-canal" / "CALENDARIO.csv").exists():
        pytest.skip("calendário ausente")
    txt = gs.montar(DOMINGO, fac, "faz-a-conta-cenas", bar, None)
    secoes = ["## DECIDIR ANTES DE GRAVAR", "## Investir e Coçar", "## Faz a Conta", "## Shorts Barsi Perene",
              "## Shorts Louise", "## Cards Instagram e X", "## Canais dark"]
    pos = [txt.index(s) for s in secoes]
    assert pos == sorted(pos)
    assert "guarda esse número" in txt and "rotativo" in txt and "R$ 740" in txt
    assert txt.count("guarda esse") == 1          # a decisão fixa abafa as cópias dos roteiros
    assert "seg 05/10 · Short" in txt and "qui 08/10 · Longo" in txt and "12/10" not in txt.split("## Faz a Conta")[0]
    assert "ouvinte reprovou a v1.7 (7,8): falta ouvir a v1.8" in txt
    assert "Shorts Louise\n\n- agenda não encontrada no repo — onde fica?" in txt
    if fac:
        assert "banco Central não gastou".lower() in txt.lower() and "dom 11/10** — Parabéns, o dinheiro é seu" in txt
    if bar:
        assert "**dom 11/10** ✅" in txt
