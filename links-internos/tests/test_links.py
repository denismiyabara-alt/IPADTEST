"""Testes dos patches de links internos (sem rede).

- todo patch segue as regras (de seguro, único no rendered em cache, link único por destino, no máximo 3 por post,
  nenhum destino proibido, cada post num lote só);
- o aplicar_patches.py da auditoria-fatos, com um WordPress falso, confere e aplica 2 desses patches (um do L1 e um
  do L2) e, pela opção --pasta, confere os lotes inteiros.
"""
import html
import json
import re
import sys
from pathlib import Path

import pytest

LI = Path(__file__).resolve().parent.parent
AF = LI.parent / "auditoria-fatos"
sys.path.insert(0, str(AF))
sys.path.insert(0, str(LI))
import aplicar_patches as AP  # noqa: E402
import gerar_links as G  # noqa: E402
from auditar import carregar_posts  # noqa: E402
from patchlib import localizar_no_rendered, problemas_do_de  # noqa: E402

if not list((AF / "cache").glob("posts_p*.json")):
    pytest.skip("sem o cache dos posts (auditoria-fatos/cache/)", allow_module_level=True)

PASTA = LI / "patches"
POSTS = {p["id"]: p for p in carregar_posts()}
LOTES = {f.stem[5:]: json.loads(f.read_text())["post_ids"] for f in PASTA.glob("LOTE_*.json")}
PATCHES = {int(f.stem): json.loads(f.read_text()) for f in PASTA.glob("*.json") if f.stem.isdigit()}
PROIBIDOS = {1033, 998, 1073, 1083, 1113, 1178, 1183}
LINK = re.compile(r'<a href="([^"]+)">([^<]+)</a>')


class FakeWP:
    def __init__(self, posts):
        self.posts = dict(posts)
        self.gravacoes = []

    def ler(self, pid):
        return {"raw": self.posts[pid], "modified": "2026-10-02T00:00:00", "status": "publish"}

    def gravar(self, pid, content):
        self.gravacoes.append(pid)
        self.posts[pid] = content
        return {"modified": "2026-10-03T00:00:00"}


def test_lotes_existem_e_cada_post_esta_num_lote_so():
    assert {"L1", "L2"} <= set(LOTES)
    todos = [i for ids in LOTES.values() for i in ids]
    assert len(todos) == len(set(todos)), "post em dois lotes"
    assert set(todos) == set(PATCHES)


@pytest.mark.parametrize("pid", sorted(PATCHES))
def test_patch_valido(pid):
    d = PATCHES[pid]
    assert d["post_id"] == pid and d["motivo"] and d["fonte"] and 1 <= len(d["trocas"]) <= 3
    rendered = POSTS[pid]["content"]["rendered"]
    txt = html.unescape(rendered)
    urls = []
    for t in d["trocas"]:
        assert problemas_do_de(t["de"]) == [], t["de"]
        assert txt.count(t["de"]) == 1, t["de"]
        assert localizar_no_rendered(rendered, t["de"])[1] == t["de_rendered"]
        links = LINK.findall(t["para"])
        assert len(links) == 1, t["para"]
        url, ancora = links[0]
        assert LINK.sub(r"\2", t["para"]) == t["de"], "o texto visível mudou"
        assert not G.ANCORA_RUIM.match(ancora) and len(ancora) >= 3
        assert url.startswith(G.SITE + "/") and "/cotacao-" not in url
        alvo = next((p for p in POSTS.values() if p["link"] == url), None)
        if alvo:
            assert alvo["id"] not in PROIBIDOS and alvo["id"] != pid
        assert not G.ja_linka(rendered, url), "o post já linka esse destino"
        urls.append(url)
    assert len(urls) == len(set(urls)), "destino repetido no post"


def _raw(pid):
    """O content.raw não está no cache; o rendered serve de raw para o teste (o 'de' é igual nos dois)."""
    return POSTS[pid]["content"]["rendered"]


def test_aplicar_patches_aplica_dois_patches(tmp_path):
    p1, p2 = LOTES["L1"][0], LOTES["L2"][0]
    wp = FakeWP({p1: _raw(p1), p2: _raw(p2)})
    saidas = []
    r = AP.cmd_checar(wp, [p1, p2], PASTA, saida=saidas.append)
    assert r["ok"] == [p1, p2], saidas
    r = AP.cmd_aplicar(wp, [p1, p2], PASTA, tmp_path / "backup", saida=lambda *_: None)
    assert r["aplicados"] == [p1, p2] and wp.gravacoes == [p1, p2]
    for pid in (p1, p2):
        novo = wp.posts[pid]
        for t in PATCHES[pid]["trocas"]:
            assert novo.count(t["para"]) == 1
        # tirando os links novos, o post fica igual ao original
        sem = novo
        for t in PATCHES[pid]["trocas"]:
            sem = sem.replace(t["para"], t["de"])
        assert sem == _raw(pid)
        assert list((tmp_path / "backup").glob(f"{pid}_*.json"))
    # reaplicar não faz nada: o "de" sumiu
    assert AP.cmd_aplicar(wp, [p1], PASTA, tmp_path / "backup", saida=lambda *_: None)["pulados"] == [p1]


@pytest.mark.parametrize("lote", ["L1", "L2", "L3"])
def test_opcao_pasta_confere_o_lote_inteiro(lote, monkeypatch, capsys):
    if lote not in LOTES:
        pytest.skip("lote não gerado")
    wp = FakeWP({pid: _raw(pid) for pid in LOTES[lote]})
    monkeypatch.setattr(AP, "WP", lambda: wp)
    AP.main(["--pasta", str(PASTA), "--checar", "--lote", lote])
    out = capsys.readouterr().out
    assert f"prontos: {len(LOTES[lote])}  precisam revisar: 0" in out
    assert not wp.gravacoes


def test_links_sobrevivem_aos_lotes_a_b():
    """Nos posts que também têm patch nos lotes A/B, os dois patches se aplicam em qualquer ordem."""
    comuns = [pid for pid in PATCHES if (AF / "patches" / f"{pid}.json").exists()]
    assert comuns, "esperado algum post em comum (ex.: 4873)"
    for pid in comuns:
        ab = json.loads((AF / "patches" / f"{pid}.json").read_text())["trocas"]
        li = PATCHES[pid]["trocas"]
        for ordem in ((ab, li), (li, ab)):
            raw = _raw(pid)
            for trocas in ordem:
                raw = AP.aplicar_trocas(raw, trocas)
            for t in li:
                assert raw.count(t["para"]) == 1


def _destinos_dos_patches():
    for pid, d in PATCHES.items():
        for t in d["trocas"]:
            yield pid, LINK.findall(t["para"])[0][0]


def test_nenhum_link_para_titulo_bloqueado_ou_refresh():
    """Nenhum 'para' aponta para post cujo título (ou endereço) o gate barra por RECOMENDACAO_TITULO,
    nem para post do site-ativos/posts-para-refresh.csv."""
    refresh = G.urls_refresh()
    por_url = {p["link"]: p for p in POSTS.values()}
    for pid, url in _destinos_dos_patches():
        assert url not in refresh, (pid, url)
        assert not G.slug_bloqueado(url), (pid, url)
        if url in por_url:
            assert not G.titulo_bloqueado(html.unescape(por_url[url]["title"]["rendered"])), (pid, url)
    # e a regra pega os casos que motivaram a mudança
    assert G.titulo_bloqueado("O Melhor ETF de Bitcoin da B3: HODL11")
    assert G.slug_bloqueado(G.SITE + "/ambev-abev3-resultado-1t26-vale-a-pena-investir/")
    assert not G.titulo_bloqueado("O que é BOVA11? ETF do Ibovespa explicado")


def test_regra_igual_a_do_gate():
    """A regex copiada é a mesma do gate (pipeline/gate_qualidade.py, branch gate-qualidade), quando ele está aqui."""
    import subprocess
    try:
        fonte = subprocess.run(["git", "-C", "/home/user/investir-e-cocar", "show",
                                "gate-qualidade:pipeline/gate_qualidade.py"], capture_output=True, text=True,
                               check=True).stdout
    except (OSError, subprocess.CalledProcessError):
        pytest.skip("gate de qualidade não está nesta máquina")
    ns = {}
    bloco = re.search(r"RE_RECOM_TITULO = re\.compile\(.*?, re\.I\)", fonte, re.S).group(0)
    exec("import re\n" + bloco, ns)
    assert ns["RE_RECOM_TITULO"].pattern == G.RE_RECOM_TITULO.pattern


def test_rascunhos_fora_dos_patches():
    """1198 e 2649 viraram rascunho: sem patch e sem link para eles; o endereço da calculadora de juros é da página."""
    assert 1198 not in PATCHES and 2649 not in PATCHES
    urls = {u for _, u in _destinos_dos_patches()}
    assert G.SITE + "/carteira-recomendada-fundos-imobiliarios-agosto-2025/" not in urls
    assert G.SITE + "/calculadora-juros-anual-para-mensal/" in urls  # agora é a página 19504 (ferramenta)
