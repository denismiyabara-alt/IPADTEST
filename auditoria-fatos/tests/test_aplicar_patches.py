"""Testes do aplicar_patches.py com um WordPress falso (sem rede)."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import aplicar_patches as AP  # noqa: E402
from patchlib import casar_tolerante, localizar_no_rendered, problemas_do_de  # noqa: E402


class FakeWP:
    def __init__(self, posts):
        self.posts = dict(posts)
        self.gravacoes = []

    def ler(self, pid):
        return {"raw": self.posts[pid], "modified": "2026-10-01T00:00:00", "status": "publish"}

    def gravar(self, pid, content):
        self.gravacoes.append((pid, content))
        self.posts[pid] = content
        return {"modified": "2026-10-02T00:00:00"}


def escrever_patch(pasta, pid, trocas):
    (pasta / f"{pid}.json").write_text(json.dumps({"post_id": pid, "motivo": "t", "trocas": trocas, "fonte": "f"}))


@pytest.fixture
def ambiente(tmp_path):
    p = tmp_path / "patches"
    b = tmp_path / "backup"
    p.mkdir()
    return p, b


def test_casa_exato_aplica_e_faz_backup_antes(ambiente):
    p, b = ambiente
    wp = FakeWP({1: "<p>JCP tem retenção de 15% na fonte.</p>"})
    escrever_patch(p, 1, [{"de": "retenção de 15% na fonte", "para": "retenção de 17,5% na fonte"}])
    ordem = []
    gravar_orig = wp.gravar

    def gravar(pid, c):
        ordem.append(("gravar", len(list(b.glob("1_*.json")))))
        return gravar_orig(pid, c)
    wp.gravar = gravar
    r = AP.cmd_aplicar(wp, [1], p, b, saida=lambda *_: None)
    assert r["aplicados"] == [1]
    assert wp.posts[1] == "<p>JCP tem retenção de 17,5% na fonte.</p>"
    assert ordem == [("gravar", 1)]  # backup já existia quando gravou
    bk = json.loads(next(b.glob("1_*.json")).read_text())
    assert bk["raw"] == "<p>JCP tem retenção de 15% na fonte.</p>"
    assert list(b.glob("log_*.jsonl"))


def test_nao_casa_nao_aplica(ambiente):
    p, b = ambiente
    wp = FakeWP({2: "<p>outro texto</p>"})
    escrever_patch(p, 2, [{"de": "retenção de 15% na fonte", "para": "x"}])
    r = AP.cmd_aplicar(wp, [2], p, b, saida=lambda *_: None)
    assert r["pulados"] == [2] and not wp.gravacoes and not b.exists()


def test_casa_duas_vezes_nao_aplica(ambiente):
    p, b = ambiente
    wp = FakeWP({3: "Selic em 14,75% ao ano. E de novo: Selic em 14,75% ao ano."})
    escrever_patch(p, 3, [{"de": "Selic em 14,75% ao ano", "para": "Selic atual"}])
    saidas = []
    r = AP.cmd_checar(wp, [3], p, saida=saidas.append)
    assert r["falha"] == [3] and any("AMBÍGUO (2x" in s for s in saidas)
    assert AP.cmd_aplicar(wp, [3], p, b, saida=lambda *_: None)["pulados"] == [3]
    assert not wp.gravacoes


def test_n_esperado_troca_as_duas(ambiente):
    p, b = ambiente
    wp = FakeWP({7: '<p>JCP tem 15% retido na fonte.</p><script>{"text": "JCP tem 15% retido na fonte."}</script>'})
    escrever_patch(p, 7, [{"de": "JCP tem 15% retido na fonte", "para": "JCP tem 17,5% retido na fonte", "n": 2}])
    assert AP.cmd_aplicar(wp, [7], p, b, saida=lambda *_: None)["aplicados"] == [7]
    assert wp.posts[7].count("17,5%") == 2
    wp2 = FakeWP({8: "<p>JCP tem 15% retido na fonte.</p>"})
    escrever_patch(p, 8, [{"de": "JCP tem 15% retido na fonte", "para": "x", "n": 2}])
    assert AP.cmd_aplicar(wp2, [8], p, b, saida=lambda *_: None)["pulados"] == [8]


def test_alternativa_com_entidade(ambiente):
    p, b = ambiente
    wp = FakeWP({9: "<td>Isento (cotas em bolsa, &gt; 50 cotistas)</td>"})
    escrever_patch(p, 9, [{"de": "> 50 cotistas)", "para": "100 ou mais cotistas)", "alternativas": ["&gt; 50 cotistas)"]}])
    assert AP.cmd_aplicar(wp, [9], p, b, saida=lambda *_: None)["aplicados"] == [9]
    assert wp.posts[9] == "<td>Isento (cotas em bolsa, 100 ou mais cotistas)</td>"


def test_um_patch_ruim_trava_o_post_inteiro(ambiente):
    p, b = ambiente
    wp = FakeWP({4: "<p>A primeira frase certa aqui.</p><p>Segunda.</p>"})
    escrever_patch(p, 4, [{"de": "primeira frase certa", "para": "primeira frase nova"},
                          {"de": "frase que não existe no raw", "para": "x"}])
    assert AP.cmd_aplicar(wp, [4], p, b, saida=lambda *_: None)["pulados"] == [4]
    assert not wp.gravacoes


def test_tolerante_so_no_checar(ambiente):
    p, b = ambiente
    raw = "<p>Quando voce ouve “o Banco Central subiu os juros” &#8211; e hoje</p>"
    wp = FakeWP({5: raw})
    escrever_patch(p, 5, [{"de": 'ouve "o Banco Central subiu os juros" - e hoje', "para": "x"}])
    saidas = []
    AP.cmd_checar(wp, [5], p, saida=saidas.append)
    assert any("tolerante achou 1x" in s for s in saidas)
    assert AP.cmd_aplicar(wp, [5], p, b, saida=lambda *_: None)["pulados"] == [5]
    assert not wp.gravacoes
    assert casar_tolerante(raw, 'ouve "o Banco Central subiu os juros" - e hoje')[0].startswith("ouve “")


def test_desfazer_restaura_backup(ambiente):
    p, b = ambiente
    original = "<p>Prazo mínimo de 90 dias para a LCI.</p>"
    wp = FakeWP({6: original})
    escrever_patch(p, 6, [{"de": "Prazo mínimo de 90 dias", "para": "Prazo mínimo de 6 meses"}])
    AP.cmd_aplicar(wp, [6], p, b, saida=lambda *_: None)
    assert "6 meses" in wp.posts[6]
    AP.cmd_desfazer(wp, 6, b, saida=lambda *_: None)
    assert wp.posts[6] == original
    linhas = [json.loads(l) for f in b.glob("log_*.jsonl") for l in f.read_text().splitlines()]
    assert [l["acao"] for l in linhas] == ["aplicar", "desfazer"]


def test_validacoes_do_de():
    assert problemas_do_de("o JCP tem retenção de 15%") == []
    assert problemas_do_de("“Rendimentos Isentos”")
    assert problemas_do_de("curto")
    html_ = "<p>Quando voc&#234; ouve a Selic em 14,75% ao ano.</p><p>Outra Selic em 14,75% ao ano.</p>"
    n, r = localizar_no_rendered(html_, "Quando você ouve a Selic")
    assert n == 1 and r == "Quando voc&#234; ouve a Selic"
    assert localizar_no_rendered(html_, "Selic em 14,75% ao ano")[0] == 2


def test_patches_versionados_sao_validos():
    """Todo patch versionado tem 'de' seguro e 'de_rendered' registrado."""
    pasta = Path(__file__).resolve().parent.parent / "patches"
    for f in pasta.glob("*.json"):
        if not f.stem.isdigit():
            continue
        d = json.loads(f.read_text())
        assert d["post_id"] == int(f.stem) and d["trocas"]
        for t in d["trocas"]:
            assert problemas_do_de(t["de"]) == [], (f.name, t["de"])
            assert t["de"] != t["para"] and t.get("de_rendered")


def test_opcao_pasta_usa_lotes_de_outra_pasta(tmp_path, monkeypatch):
    """--pasta lê patches e LOTE_<X>.json de outra pasta (ex.: links-internos/patches), com lote de qualquer nome."""
    p = tmp_path / "outra"
    p.mkdir()
    escrever_patch(p, 11, [{"de": "o dividend yield da ação", "para": 'o <a href="https://x/dy/">dividend yield</a> da ação'}])
    (p / "LOTE_L1.json").write_text(json.dumps({"lote": "L1", "post_ids": [11]}))
    wp = FakeWP({11: "<p>Veja o dividend yield da ação antes.</p>"})
    monkeypatch.setattr(AP, "WP", lambda: wp)
    monkeypatch.setattr(AP, "BACKUP", tmp_path / "backup")
    monkeypatch.setattr(AP.cmd_aplicar, "__defaults__", (AP.PATCHES, tmp_path / "backup", print))
    AP.main(["--pasta", str(p), "--checar", "--lote", "L1"])
    assert not wp.gravacoes
    AP.main(["--pasta", str(p), "--aplicar", "--lote", "L1"])
    assert wp.posts[11] == '<p>Veja o <a href="https://x/dy/">dividend yield</a> da ação antes.</p>'
    with pytest.raises(SystemExit, match="lote L9 não existe"):
        AP.main(["--pasta", str(p), "--checar", "--lote", "L9"])
    with pytest.raises(SystemExit, match="não existe"):
        AP.main(["--pasta", str(tmp_path / "nada"), "--checar"])


def test_sem_pasta_continua_na_pasta_padrao(monkeypatch):
    """Sem --pasta, --lote A lê auditoria-fatos/patches/LOTE_A.json, como antes."""
    vistos = {}
    monkeypatch.setattr(AP, "WP", lambda: object())
    monkeypatch.setattr(AP, "cmd_checar", lambda wp, ids, pasta=None: vistos.update(ids=ids, pasta=pasta))
    AP.main(["--checar", "--lote", "A"])
    assert vistos["pasta"] == AP.PATCHES.resolve()
    assert vistos["ids"] == AP.ids_do_lote("A")
