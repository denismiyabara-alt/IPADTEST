"""Páginas: testes de HTML (13, 14, 15), ferramentas no modo compacto e o fluxo bloqueante de ponta a ponta."""
import json
import re
import os
import sqlite3
import subprocess
import sys

from iec_ativos import calcular, config, ferramentas, gerar, seo, validar

HTML_OK = """<!doctype html><html><head><title>PETR4: dividendos</title>
<link rel="canonical" href="https://x/acoes/petr4/"><script type="application/ld+json">{"a":1}</script></head>
<body><h1>PETR4</h1><p>Não é recomendação de compra ou venda. Não é preço-alvo nem recomendação.</p>
<span class="n" data-fonte="B3" data-ref="2026-10-01">49,77</span><table><tr><td class="num" data-fonte="CVM" data-ref="2026-06-30">1</td></tr></table>
</body></html>"""


def _falhas(html, nomes=(), titulo="PETR4: dividendos"):
    return {(t["teste"], t["nome"]) for t in seo.verificar_html(html, list(nomes), titulo) if not t["ok"]}


def test_html_ok_passa():
    assert _falhas(HTML_OK) == set()


def test_numero_sem_fonte_bloqueia():
    html = HTML_OK.replace('data-fonte="B3" ', "")
    assert any(t == 13 for t, _ in _falhas(html))


def test_palavras_proibidas_bloqueiam():
    for frase in ("Compre agora", "a ação está barata", "PETR4 vale a pena?", "uma oportunidade", "preço-alvo de R$ 50",
                  "a melhor ação"):
        html = HTML_OK.replace("<h1>PETR4</h1>", f"<h1>PETR4</h1><p>{frase}</p>")
        assert (14, "Sem palavras de recomendação") in _falhas(html), frase


def test_corretora_bloqueia_mas_emissor_nao():
    html = HTML_OK.replace("<h1>PETR4</h1>", "<h1>PETR4</h1><p>Abra sua conta na XP Investimentos</p>")
    assert (14, "Sem citar corretora") in _falhas(html)
    emissor = HTML_OK.replace("<h1>PETR4</h1>", "<h1>BPAC11</h1><p>BANCO BTG PACTUAL S/A</p>")
    assert _falhas(emissor, ["BANCO BTG PACTUAL S/A"]) == set()


def test_estrutura_bloqueia():
    assert any(t == 15 for t, _ in _falhas(HTML_OK.replace("<h1>PETR4</h1>", "<h1>A</h1><h1>B</h1>")))
    assert any(t == 15 for t, _ in _falhas(HTML_OK, titulo="x" * 61))
    assert any(t == 15 for t, _ in _falhas(HTML_OK.replace('<link rel="canonical" href="https://x/acoes/petr4/">', "")))
    dois = HTML_OK.replace("</head>", '<script type="application/ld+json">{}</script></head>')
    assert any(t == 15 for t, _ in _falhas(dois))


def test_preco_justo_compacto_e_so_no_clique():
    f = ferramentas.preco_justo(49.77, 2.97, 10.35, 37.32, "B3; CVM", "/acoes/metodologia/#preco-justo")
    h, js = f["html"], f["js"]
    assert '<section class="explain">' not in h and "Veja a metodologia" in h
    assert 'data-modo="compacto"' in h and 'data-calculo="clique"' in h and 'data-preco="49.77"' in h
    assert re.search(r'id="g-preco"[^>]*value="49.77"', h) and re.search(r'id="g-lpa"[^>]*value="10.35"', h)
    assert 'id="g-calcular"' in h
    assert 'addEventListener("input",calcular)' not in js and 'addEventListener("click",calcular)' in js
    assert not re.search(r"\ncalcular\(\);", js)            # sem conta automática ao abrir
    assert "estar cara" not in js and "pode haver desconto" not in js


def test_renda_fii_preenchida():
    f = ferramentas.renda_fii(0.75, "CVM", "/fiis/metodologia/#renda-fii")
    assert re.search(r'id="f-dy"[^>]*value="0.75"', f["html"]) and '<section class="explain">' not in f["html"]


def _flag_dy_caixa(valor):
    env = {k: v for k, v in os.environ.items() if k != "IEC_ACEITAR_DY_CAIXA"}
    if valor is not None:
        env["IEC_ACEITAR_DY_CAIXA"] = valor
    r = subprocess.run([sys.executable, "-c", "from iec_ativos import gerar; print(gerar.ACEITAR_DY_CAIXA)"],
                       cwd=config.RAIZ, env=env, capture_output=True, text=True, check=True)
    return r.stdout.strip() == "True"


ACAO_COMPLETA = {"ticker": "PETR4", "tipo_pagina": "acao", "n_trimestres_dre": 8, "ind": {"dy_caixa": {"status": "ok"}}}
FII_COMPLETO = {"ticker": "HGLG11", "tipo_pagina": "fii", "n_informes": 12, "ind": {"dy_estimado": {"status": "ok"}}}
VAL_OK = {"ativos": {}}


def test_dy_de_caixa_indexa_por_padrao(monkeypatch):
    assert _flag_dy_caixa(None) and _flag_dy_caixa("1")          # sem variável: exceção do DY de caixa ligada
    monkeypatch.setattr(gerar, "ACEITAR_DY_CAIXA", True)
    assert gerar.indexavel(ACAO_COMPLETA, VAL_OK) == (True, "ok")
    assert gerar.indexavel(FII_COMPLETO, VAL_OK) == (True, "ok")
    # dados incompletos continuam fora
    assert not gerar.indexavel({**ACAO_COMPLETA, "n_trimestres_dre": 7}, VAL_OK)[0]
    assert not gerar.indexavel({**ACAO_COMPLETA, "ind": {"dy_caixa": {"status": "sem"}}}, VAL_OK)[0]
    assert not gerar.indexavel(ACAO_COMPLETA, {"ativos": {"PETR4": {"bloqueado": True}}})[0]


def test_dy_de_caixa_desligado_volta_a_regra_estrita(monkeypatch):
    assert not _flag_dy_caixa("0")
    monkeypatch.setattr(gerar, "ACEITAR_DY_CAIXA", False)
    ok, motivo = gerar.indexavel(ACAO_COMPLETA, VAL_OK)
    assert not ok and "proventos" in motivo
    ok, motivo = gerar.indexavel(FII_COMPLETO, VAL_OK)
    assert not ok and "rendimentos" in motivo


def test_ponta_a_ponta_e_bloqueante_mantem_versao_anterior(ambiente, tmp_path):
    con0 = ambiente["con"]
    con = sqlite3.connect(tmp_path / "copia.sqlite")
    con0.backup(con)
    con.row_factory = sqlite3.Row
    sel = {"acoes": [{"ticker": "PETR4", "cnpj": "33000167000101", "tipo": "comum"},
                     {"ticker": "ITUB4", "cnpj": "60872504000123", "tipo": "banco"},
                     {"ticker": "BPAC11", "cnpj": "30306294000145", "tipo": "banco"}],
           "fiis": [{"ticker": "HGLG11", "cnpj": "11728688000147"}],
           "janela": {"inicio": "2025-10-01", "fim": "2026-10-01"}}
    saida_antiga = config.SAIDA
    config.SAIDA = tmp_path / "saida"
    try:
        calcular.calcular_todos(con, sel, log=lambda *a: None)
        rel = validar.validar_todos(con, sel)
        assert not any(a["bloqueado"] for a in rel["ativos"].values())
        r1 = gerar.gerar_site(con, sel, log=lambda *a: None)
        assert not r1["nao_geradas"]
        petr = config.SAIDA / "acoes" / "petr4" / "index.html"
        html1 = petr.read_text()
        assert "noindex, follow" in html1                      # fixtures têm menos de 8 trimestres de DRE
        assert "trimestres de DRE" in (config.SAIDA / "paginas.csv").read_text()
        assert html1.count("<h1>") == 1 and "Não é recomendação de compra ou venda" in html1
        sitemap = (config.SAIDA / "sitemap-ativos.xml").read_text()
        assert "/acoes/petr4/" not in sitemap and "/acoes/metodologia/" in sitemap
        redirects = (config.SAIDA / "redirects.csv").read_text()
        assert "/cotacao-petr4/,https://investirecocaresocomecar.com.br/acoes/petr4/,301" in redirects
        # estraga o balanço da Petrobras: teste 1 (bloqueante) falha e a página antiga fica
        con.execute("""UPDATE conta SET valor_reais=valor_reais+1e6 WHERE cnpj='33000167000101' AND cd_conta='1'
                       AND dt_refer='2026-06-30' AND ordem_exerc='ULTIMO'""")
        con.execute("UPDATE preco_diario SET fechamento=fechamento+1 WHERE ticker='PETR4'")
        calcular.calcular_todos(con, sel, log=lambda *a: None)
        rel = validar.validar_todos(con, sel)
        assert rel["ativos"]["PETR4"]["bloqueado"] and not rel["ativos"]["ITUB4"]["bloqueado"]
        r2 = gerar.gerar_site(con, sel, log=lambda *a: None)
        assert any("/acoes/petr4/" in x["url"] for x in r2["nao_geradas"])
        assert petr.read_text() == html1                       # versão anterior mantida
        assert "/cotacao-petr4/" not in (config.SAIDA / "redirects.csv").read_text()
    finally:
        config.SAIDA = saida_antiga
        con.close()


def test_publicar_pasta_so_o_que_mudou(tmp_path):
    from iec_ativos import publicar
    origem = tmp_path / "saida"
    (origem / "acoes" / "petr4").mkdir(parents=True)
    (origem / "acoes" / "petr4" / "index.html").write_text("a")
    (origem / "_relatorio.json").write_text("{}")
    antiga, config.SAIDA = config.SAIDA, origem
    try:
        assert publicar.publicar_pasta(str(tmp_path / "pub")) == ["acoes/petr4/index.html"]
        assert publicar.publicar_pasta(str(tmp_path / "pub")) == []          # nada mudou
        assert not (tmp_path / "pub" / "_relatorio.json").exists()
    finally:
        config.SAIDA = antiga
