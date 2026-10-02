"""Etapa 5: gerar o HTML estático em saida/ (DESENHO 5 e 6).

Para cada ativo: se algum teste bloqueante (dados ou HTML) falhar, a página nova não é gravada;
se já existir uma versão anterior em saida/, ela fica. Também gera hubs, rankings, comparador,
calendário (esqueleto), metodologia, sitemap, redirecionamentos e um relatório da geração.
"""
import csv
import hashlib
import json
import os
import re
from datetime import date, datetime, timedelta

from jinja2 import Environment, FileSystemLoader, select_autoescape

from . import config, ferramentas, formato as fm, graficos, seo, texto
from .selecionar import tickers_cotacao

# Indexação (DESENHO 6.7): só com 8 trimestres de DRE (12 informes no FII), proventos de 12 meses revisados
# e todos os testes bloqueantes aprovados. IEC_ACEITAR_DY_CAIXA=1 aceita o DY de caixa (ações) e o DY
# estimado pelo informe (FIIs) no lugar dos proventos revisados. Padrão: regra do desenho, sem exceção.
ACEITAR_DY_CAIXA = os.environ.get("IEC_ACEITAR_DY_CAIXA") == "1"
# Títulos dos posts do canal: muitos têm "vale a pena" ou "melhor" (palavras proibidas pela seção 7).
# Padrão: rótulo neutro. IEC_POSTS_COM_TITULO=1 mostra o título do post.
POSTS_COM_TITULO = os.environ.get("IEC_POSTS_COM_TITULO") == "1"
MIN_ATIVOS_RANKING_INDEXAVEL = 30
BASE = os.environ.get("IEC_BASE_ATIVOS", config.SITE_URL).rstrip("/")   # subpasta (padrão) ou subdomínio


def _env():
    env = Environment(loader=FileSystemLoader(config.TEMPLATES), autoescape=select_autoescape(["html"]),
                      trim_blocks=False, lstrip_blocks=False)
    env.globals.update(brl=fm.brl, brl_curto=fm.brl_curto, pct=fm.pct, pct2=lambda v: fm.pct(v, 2), vezes=fm.vezes,
                       numero1=lambda v: fm.numero(v, 1), numero2=lambda v: fm.numero(v, 2), inteiro=fm.inteiro,
                       data_br=fm.data_br, mes_br=fm.mes_br, site_url=config.SITE_URL, site_nome=config.SITE_NOME,
                       base=BASE, aviso_curto=config.AVISO_CURTO, aviso_completo=config.AVISO_COMPLETO,
                       email_erros=config.EMAIL_ERROS, adsense=os.environ.get("IEC_ADSENSE_CLIENT", ""))
    return env


def cnpj_fmt(c):
    return f"{c[:2]}.{c[2:5]}.{c[5:8]}/{c[8:12]}-{c[12:]}"


def url_ativo(f):
    return f"{BASE}/{'acoes' if f['tipo_pagina'] == 'acao' else 'fiis'}/{f['ticker'].lower()}/"


def posts_do_canal(ticker: str) -> list[dict]:
    caminho = config.SEO_VARREDURA.with_name("varredura.csv")
    if not caminho.exists():
        return []
    out = []
    with open(caminho) as f:
        for r in csv.DictReader(f):
            if ticker.lower() in r["url"].lower() and "/cotacao-" not in r["url"] and r.get("noindex") != "True":
                titulo = re.sub(r"\s*-\s*Investir e Coçar$", "", r["title"])
                out.append({"url": r["url"], "titulo": titulo})
    for i, p in enumerate(out, 1):
        p["rotulo"] = p["titulo"] if POSTS_COM_TITULO else f"Análise do canal sobre {ticker} ({i})"
    return out


def _lastmod(f):
    """Muda só com dado contábil ou informe novo, não com o preço do dia (DESENHO 6.7)."""
    if f["tipo_pagina"] == "acao":
        return (f.get("doc") or {}).get("dt_receb") or (f.get("doc") or {}).get("dt_refer") or config.HOJE.isoformat()
    inf = f.get("informe") or {}
    return inf.get("data_entrega") or inf.get("data_ref") or config.HOJE.isoformat()


def cdi_12m(con):
    fim = con.execute("SELECT MAX(data) FROM macro WHERE serie=12").fetchone()[0]
    if not fim:
        return {"valor": None, "fonte": "BCB, SGS 12", "ref": config.HOJE.isoformat()}
    ini = (date.fromisoformat(fim) - timedelta(days=365)).isoformat()
    acum = 1.0
    for (v,) in con.execute("SELECT valor FROM macro WHERE serie=12 AND data>? AND data<=?", (ini, fim)):
        acum *= 1 + v / 100
    return {"valor": acum - 1, "fonte": f"Banco Central, SGS série 12 (CDI), 12 meses até {fm.data_br(fim)}", "ref": fim}


def _alertas(val, ticker):
    return [f"{t['nome']}: {t['detalhe']}" for t in val["ativos"].get(ticker, {}).get("testes", [])
            if t["tipo"] == "alerta" and not t["ok"]]


def indexavel(f, val) -> tuple[bool, str]:
    if val["ativos"].get(f["ticker"], {}).get("bloqueado"):
        return False, "teste bloqueante falhou"
    if f["tipo_pagina"] == "acao":
        if f.get("n_trimestres_dre", 0) < 8:
            return False, f"só {f.get('n_trimestres_dre', 0)} trimestres de DRE (mínimo 8)"
        if not ACEITAR_DY_CAIXA:
            return False, "proventos dos últimos 12 meses ainda não revisados (tabela por ação não aprovada)"
        if f["ind"]["dy_caixa"]["status"] != "ok":
            return False, "sem DY de caixa"
    else:
        if f.get("n_informes", 0) < 12:
            return False, f"só {f.get('n_informes', 0)} informes mensais (mínimo 12)"
        if not ACEITAR_DY_CAIXA:
            return False, "rendimentos dos últimos 12 meses ainda não revisados (Fundos.NET não aprovado)"
        if f["ind"]["dy_estimado"]["status"] != "ok":
            return False, "DY estimado indisponível (informe inconsistente)"
    return True, "ok"


def _base_ctx(titulo, descricao, canonical, migalhas, indexavel_, data_mod, sobre=None, **kw):
    ctx = {"titulo": titulo, "descricao": descricao, "canonical": canonical, "migalhas": migalhas,
           "indexavel": indexavel_, "jsonld": seo.jsonld(canonical, titulo, data_mod, migalhas, sobre),
           "gerado_em": fm.data_br(config.HOJE.isoformat()), "ref_pagina": config.HOJE.isoformat(),
           "css_extra": "", "scripts": [], "anuncio_final": ""}
    ctx.update(kw)
    return ctx


def _gravar(caminho_rel: str, html: str, gravadas: list):
    p = config.SAIDA / caminho_rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html)
    gravadas.append(caminho_rel)


def _anuncio_final(env):
    return env.from_string('{% from "_macros.html" import anuncio with context %}{{ anuncio(3) }}').render()


# --------------------------------------------------------------------------------------- páginas

def pagina_acao(env, con, f, fichas, val, cdi):
    I = f["ind"]
    t = f["ticker"]
    url = url_ativo(f)
    migalhas = [("Início", config.SITE_URL + "/"), ("Ações", f"{BASE}/acoes/"), (f"{f['nome_curto']} ({t})", url)]
    financeira = f["tipo"] in ("banco", "seguradora")
    titulo = f"{t}: dividendos, P/L e resultados da {f['nome_curto']}"
    if len(titulo) > 60:
        titulo = f"{t}: dividendos, P/L e resultados"
    precos = f.get("precos") or []
    graf_preco = graficos.linha(precos, f"Fechamento diário de {t}")
    tris = f.get("trimestres") or []
    graf_receita = graficos.barras([(x["rotulo"], x.get("receita")) for x in tris], f"Receita líquida trimestral de {t}")
    graf_lucro = graficos.barras([(x["rotulo"], x.get("lucro")) for x in tris], f"Lucro da controladora por trimestre, {t}")
    esc = "consolidados" if f.get("escopo") == "con" else "individuais"
    fonte_tri = f"CVM, ITRs e DFPs {esc}, até {f['doc']['curto']}"
    preco_i = I["preco"]
    ferr = ferramentas.preco_justo(preco_i["valor"], (I.get("dpa_caixa") or {}).get("valor"),
                                   (I.get("lpa") or {}).get("valor"), (I.get("vpa") or {}).get("valor"),
                                   f"B3, pregão de {fm.data_br(preco_i['ref'])}; CVM, {f['doc']['curto']} (12 meses); proventos pelo fluxo de caixa",
                                   f"{BASE}/acoes/metodologia/#preco-justo")
    alerta_preco = None
    if I["variacao_12m"]["status"] != "ok" and "30%" in (I["variacao_12m"].get("nota") or ""):
        alerta_preco = ("O gráfico tem um salto de preço que parece desdobramento ou grupamento. Até o evento ser "
                        "conferido e cadastrado, o preço não é ajustado e a variação de 12 meses não é mostrada.")
    outras = [x for x in fichas if x["tipo_pagina"] == "acao" and x["ticker"] != t]
    mesmo = [x for x in outras if x.get("setor") == f.get("setor") or (financeira and x.get("tipo") == f["tipo"])]
    parecidas = (mesmo + [x for x in outras if x not in mesmo])[:6]
    criterio = ("Primeiro as do mesmo setor da CVM, depois as demais da cobertura." if mesmo
                else "Nenhuma outra empresa do mesmo setor na cobertura; mostrando as demais.")
    idx, motivo = indexavel(f, val)
    classe_txt = {"ON": "ação ordinária (ON)", "PN": "ação preferencial (PN)",
                  "UNIT": f"unit ({' + '.join(f'{v} {k}' for k, v in (f.get('composicao_unit') or {}).items())})"}.get(f["classe"], f["classe"])
    sobre = {"@type": "Corporation", "name": f["nome_curto"], "legalName": f["nome"], "tickerSymbol": f"BVMF:{t}",
             "identifier": {"@type": "PropertyValue", "propertyID": "CNPJ", "value": cnpj_fmt(f["cnpj"])}}
    ctx = _base_ctx(titulo, texto.descricao_acao(f, config.HOJE.isoformat()), url, migalhas, idx, _lastmod(f), sobre,
                    f=f, h1=f"{t}: indicadores, dividendos e resultados da {f['nome_curto']}", cnpj_fmt=cnpj_fmt(f["cnpj"]),
                    classe_txt=classe_txt, resumo=texto.resumo_acao(f), graf_preco=graf_preco, graf_receita=graf_receita,
                    graf_lucro=graf_lucro, financeira=financeira, fonte_trimestres=fonte_tri, escopo_txt=esc,
                    texto_financeira=("Em banco, a dívida é matéria-prima do negócio (depósitos e captações), então "
                                      "dívida líquida e dívida/EBITDA não fazem sentido. Por isso este bloco não tem números."
                                      if f["tipo"] == "banco" else "Em seguradora, o plano de contas é diferente; o bloco não se aplica."),
                    ferramenta=ferr["html"], parecidas=[{"url": url_ativo(x), "ticker": x["ticker"], "nome": x["nome_curto"]} for x in parecidas],
                    parecidas_criterio=criterio, posts=posts_do_canal(t), eventos=False, alerta_preco=alerta_preco,
                    testes_alerta=_alertas(val, t))
    ctx["css_extra"] = ferr["css"]
    ctx["scripts"] = [ferr["js"]]
    ctx["anuncio_final"] = _anuncio_final(env)
    return env.get_template("acao.html").render(**ctx), idx, motivo, titulo


def pagina_fii(env, con, f, fichas, val, cdi):
    I = f["ind"]
    t = f["ticker"]
    url = url_ativo(f)
    migalhas = [("Início", config.SITE_URL + "/"), ("FIIs", f"{BASE}/fiis/"), (t, url)]
    titulo = f"{t}: dividendos, P/VP e vacância"
    meses = f.get("meses") or []
    meses24 = meses[-24:]
    precos = f.get("precos") or []
    ini_vp = meses[0]["data_ref"] if meses else None
    graf_pvp = graficos.linha([p for p in precos if not ini_vp or p[0] >= ini_vp], f"Cotação e valor patrimonial de {t}",
                              referencia=[(m["data_ref"], m["vp_cota"]) for m in meses if m["vp_cota"]],
                              nome_ref="VP/cota", rotulo_x=lambda d: fm.mes_br(d))
    graf_cot = graficos.linha([(m["data_ref"], m["cotistas"]) for m in meses], f"Cotistas de {t}", moeda=False,
                              fmt=lambda v: fm.inteiro(v) if v < 1e5 else fm.numero(v / 1e3, 0) + " mil",
                              rotulo_x=lambda d: fm.mes_br(d))
    graf_dy = None
    if not f.get("informe_problemas"):
        graf_dy = graficos.barras([(fm.mes_br(m["data_ref"]), m["dy_mes_informado"] * m["vp_cota"]
                                    if m["dy_mes_informado"] is not None and m["vp_cota"] else None) for m in meses24],
                                  f"Rendimento mensal estimado por cota de {t}", fmt=lambda v: fm.brl(v))
    dym = (I.get("dy_mensal_medio") or {}).get("valor")
    ferr = ferramentas.renda_fii(dym * 100 if dym else None,
                                 f"CVM, informes mensais até {f['informe']['mes']}; B3, pregão de {fm.data_br(I['preco']['ref'])}",
                                 f"{BASE}/fiis/metodologia/#renda-fii")
    alerta_preco = None
    if I["variacao_12m"]["status"] != "ok" and "30%" in (I["variacao_12m"].get("nota") or ""):
        alerta_preco = "Salto de preço sem evento conferido: a variação de 12 meses não é mostrada."
    outras = [x for x in fichas if x["tipo_pagina"] == "fii" and x["ticker"] != t]
    mesmo = [x for x in outras if x.get("segmento") == f.get("segmento")]
    parecidas = (mesmo + [x for x in outras if x not in mesmo])[:6]
    idx, motivo = indexavel(f, val)
    sobre = {"@type": "Organization", "name": f["nome"], "legalName": f["nome"], "alternateName": t,
             "identifier": {"@type": "PropertyValue", "propertyID": "CNPJ", "value": cnpj_fmt(f["cnpj"])}}
    ctx = _base_ctx(titulo, texto.descricao_fii(f, config.HOJE.isoformat()), url, migalhas, idx, _lastmod(f), sobre,
                    f=f, h1=f"{t}: dividendos, P/VP e vacância do fundo", cnpj_fmt=cnpj_fmt(f["cnpj"]),
                    resumo=texto.resumo_fii(f), graf_pvp=graf_pvp, graf_cotistas=graf_cot, graf_dy=graf_dy,
                    meses24=meses24, ferramenta=ferr["html"], cdi=cdi,
                    parecidas=[{"url": url_ativo(x), "ticker": x["ticker"], "nome": x["nome_curto"]} for x in parecidas],
                    parecidas_criterio=("Primeiro os do mesmo segmento informado à CVM." if mesmo else "Demais FIIs da cobertura."),
                    posts=posts_do_canal(t), alerta_preco=alerta_preco, testes_alerta=_alertas(val, t))
    ctx["css_extra"] = ferr["css"]
    ctx["scripts"] = [ferr["js"]]
    ctx["anuncio_final"] = _anuncio_final(env)
    return env.get_template("fii.html").render(**ctx), idx, motivo, titulo


RANKINGS_ACOES = [
    ("menores-p-vp", "Ações com menor P/VP", "pvp", "P/VP", lambda v: fm.numero(v, 2), False,
     ["P/VP compara o valor de mercado com o patrimônio da empresa. Abaixo de 1, o mercado paga menos do que o "
      "patrimônio contábil; acima de 1, paga mais. Leia o <a href=\"{site}/o-que-e-pvp-acoes/\">verbete de P/VP</a>."]),
    ("maiores-roe", "Ações com maior ROE em 12 meses", "roe", "ROE", fm.pct, True,
     ["ROE é o lucro de 12 meses dividido pelo patrimônio médio: quanto a empresa lucrou para cada real de "
      "patrimônio. Lucro não recorrente infla o número. Leia o <a href=\"{site}/o-que-e-roe/\">verbete de ROE</a>."]),
    ("maiores-valores-de-mercado", "Ações com maior valor de mercado", "valor_mercado", "Valor de mercado", fm.brl_curto, True,
     ["Valor de mercado é o preço de cada classe de ação vezes a quantidade de ações em circulação."]),
    ("maiores-dy-de-caixa", "Ações com maior DY de caixa em 12 meses", "dy_caixa", "DY de caixa", fm.pct, True,
     ["DY de caixa é o total de dividendos e JCP pagos pela empresa em 12 meses (fluxo de caixa) dividido pelo "
      "valor de mercado atual. Não é a soma dos proventos por ação com data ex no período. Leia o "
      "<a href=\"{site}/dividendos-o-que-sao-dividend-yield/\">verbete de dividend yield</a>."]),
]
RANKINGS_FIIS = [
    ("maiores-dy-estimados", "FIIs com maior DY estimado em 12 meses", "dy_estimado", "DY estimado", fm.pct, True,
     ["DY estimado: soma do DY mensal que o administrador informa à CVM, convertido pela cotação. Fundos com "
      "informe inconsistente ficam fora."]),
    ("mais-cotistas", "FIIs com mais cotistas", "cotistas", "Cotistas", fm.inteiro, True,
     ["Número total de cotistas no último informe mensal entregue à CVM."]),
    ("menor-vacancia", "FIIs com menor vacância física", "vacancia", "Vacância", fm.pct, False,
     ["Vacância física ponderada pela área dos imóveis prontos para renda, no último informe trimestral. Fundos "
      "de papel ficam fora (não se aplica)."]),
]


def pagina_ranking(env, fichas, tipo, slug, titulo, k, rotulo, fmt, desc, explic, janela):
    base_url = f"{BASE}/{'acoes' if tipo == 'acao' else 'fiis'}/ranking/{slug}/"
    hoje = config.HOJE.isoformat()
    linhas, fora = [], []
    corte_dado = (config.HOJE - timedelta(days=183)).isoformat()
    for f in fichas:
        if f["tipo_pagina"] != tipo:
            continue
        i = f["ind"].get(k) or {}
        vol = (f["ind"].get("volume_3m") or {}).get("valor") or 0
        if i.get("status") != "ok":
            fora.append((f["ticker"], "não se aplica" if i.get("status") == "nao_se_aplica" else "sem dado"))
            continue
        if vol < 1_000_000:
            fora.append((f["ticker"], "volume médio abaixo de R$ 1 milhão por dia"))
            continue
        if tipo == "acao" and (f.get("ttm") or {}).get("lucro_controladora", 0) <= 0:
            fora.append((f["ticker"], "prejuízo em 12 meses"))
            continue
        if (i.get("ref") or hoje) < corte_dado:
            fora.append((f["ticker"], "dado com mais de 6 meses"))
            continue
        engano = []
        if tipo == "acao" and k == "dy_caixa":
            engano.append("pagamento extraordinário entra inteiro; é por empresa, não por ação")
        if tipo == "acao" and k in ("roe", "pvp") and f.get("tipo") == "banco":
            engano.append("banco: patrimônio regulado, compare com outros bancos")
        if f.get("acoes", {}).get("escala") == 1000:
            engano.append("quantidade de ações informada em milhares (corrigida)")
        if (f.get("ind", {}).get("valor_mercado") or {}).get("nota", "").endswith("(estimado)"):
            engano.append("valor de mercado estimado pelo preço da unit")
        f2 = dict(f, url=url_ativo(f), engano="; ".join(engano) or "—")
        linhas.append(f2)
    linhas.sort(key=lambda x: x["ind"][k]["valor"], reverse=desc)
    linhas = linhas[:30]
    migalhas = [("Início", config.SITE_URL + "/"), ("Ações" if tipo == "acao" else "FIIs", f"{BASE}/{'acoes' if tipo == 'acao' else 'fiis'}/"),
                (titulo, base_url)]
    n_cob = sum(1 for f in fichas if f["tipo_pagina"] == tipo)
    idx = n_cob >= MIN_ATIVOS_RANKING_INDEXAVEL
    ferr_html, ferr_css, ferr_js = "", "", []
    if tipo == "fii":
        fr = ferramentas.renda_fii(None, "valores de exemplo", f"{BASE}/fiis/metodologia/#renda-fii")
        ferr_html = '<h2>Simule a renda mensal</h2><p>Simulador sem preenchimento: coloque os seus números.</p>' + fr["html"]
        ferr_css, ferr_js = fr["css"], [fr["js"]]
    else:
        ferr_html = (f'<p>Para fazer contas com os números de uma ação, use a calculadora de preço justo na página '
                     f'da ação (exemplo: <a href="{url_ativo(linhas[0])}">{linhas[0]["ticker"]}</a>).</p>' if linhas else "")
    filtros = ("volume médio diário em 3 meses de pelo menos R$ 1 milhão, lucro positivo em 12 meses e dado com menos de 6 meses"
               if tipo == "acao" else "volume médio diário em 3 meses de pelo menos R$ 1 milhão e dado com menos de 6 meses")
    ctx = _base_ctx(titulo, f"{titulo}, entre os ativos da cobertura do Investir e Coçar. Dados da CVM e da B3 até {fm.data_br(hoje)}.",
                    base_url, migalhas, idx, hoje, None, h1=titulo,
                    explicacao=[e.replace("{site}", config.SITE_URL) for e in explic] +
                               [f"A cobertura ainda tem só {n_cob} {'ações' if tipo == 'acao' else 'FIIs'}, escolhidos pelo volume "
                                "negociado; por isso a tabela é curta."],
                    filtros=filtros, corte=hoje, aviso_escolha="A escolha dos ativos não é recomendação.",
                    linhas=linhas, k=k, fmt=fmt, rotulo=rotulo, fora=fora, ferramenta=ferr_html)
    ctx["css_extra"] = ferr_css
    ctx["scripts"] = ferr_js
    ctx["anuncio_final"] = _anuncio_final(env)
    return env.get_template("ranking.html").render(**ctx), idx, ("ok" if idx else f"menos de {MIN_ATIVOS_RANKING_INDEXAVEL} ativos na cobertura"), titulo


JS_COMPARAR = r"""(function(){
"use strict";
var D=JSON.parse(document.getElementById("cmp-dados").textContent);
var LIN=[["preco","Fechamento"],["variacao_12m","Variação 12 meses"],["valor_mercado","Valor de mercado"],["pl","P/L"],["pvp","P/VP"],["roe","ROE"],["dy_caixa","DY de caixa"],["margem_liquida","Margem líquida"],["margem_ebitda","Margem EBITDA"],["div_liq_ebitda","Dív. líq./EBITDA"]];
var sel=[0,1,2,3].map(function(i){return document.getElementById("cmp-"+i);});
function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c];});}
function celula(x){ if(!x||x.t==null) return '<td class="num" data-fonte="não se aplica" data-ref="'+esc(D.hoje)+'">'+(x&&x.s==="nao_se_aplica"?"não se aplica":"não disponível")+"</td>";
  return '<td class="num" data-fonte="'+esc(x.f)+'" data-ref="'+esc(x.r)+'" title="Fonte: '+esc(x.f)+'">'+esc(x.t)+"</td>"; }
function montar(){
  var ts=sel.map(function(s){return s.value;}).filter(function(v,i,a){return v && a.indexOf(v)===i;});
  var th=document.querySelector("#cmp-tabela thead"), tb=document.querySelector("#cmp-tabela tbody"), dif=document.getElementById("cmp-diferencas");
  if(ts.length<2){ th.innerHTML=""; tb.innerHTML='<tr><td>Escolha pelo menos 2 ações.</td></tr>'; dif.textContent=""; return; }
  th.innerHTML="<tr><th>Indicador</th>"+ts.map(function(t){return '<th class="num"><a href="'+esc(D.a[t].url)+'">'+esc(t)+"</a></th>";}).join("")+"</tr>";
  tb.innerHTML=LIN.map(function(l){return "<tr><td>"+l[1]+"</td>"+ts.map(function(t){return celula(D.a[t].i[l[0]]);}).join("")+"</tr>";}).join("");
  var frases=[];
  [["margem_liquida","margem líquida maior"],["div_liq_ebitda","dívida líquida/EBITDA menor",true],["roe","ROE maior"]].forEach(function(c){
    var v=ts.map(function(t){var x=D.a[t].i[c[0]];return x&&x.t!=null?[t,x.v]:null;}).filter(Boolean);
    if(v.length<2) return; v.sort(function(a,b){return c[2]?a[1]-b[1]:b[1]-a[1];}); frases.push(v[0][0]+" tem "+c[1]);
  });
  dif.textContent=frases.length?"Diferenças objetivas: "+frases.join("; ")+".":"";
  try{ history.replaceState(null,"","?"+ts.map(function(t,i){return "abcd"[i]+"="+t.toLowerCase();}).join("&")); }catch(e){}
}
var q=new URLSearchParams(location.search), ini=["a","b","c","d"].map(function(k){return (q.get(k)||"").toUpperCase();});
if(!ini[0]){ini=D.padrao;}
sel.forEach(function(s,i){ if(ini[i] && D.a[ini[i]]) s.value=ini[i]; s.addEventListener("change",montar); });
montar();
})();"""


def pagina_comparar(env, fichas):
    url = f"{BASE}/comparar/acoes/"
    acoes = [f for f in fichas if f["tipo_pagina"] == "acao"]
    fmts = {"preco": fm.brl, "variacao_12m": fm.pct, "valor_mercado": fm.brl_curto, "pl": lambda v: fm.numero(v, 1),
            "pvp": lambda v: fm.numero(v, 2), "roe": fm.pct, "dy_caixa": fm.pct, "margem_liquida": fm.pct,
            "margem_ebitda": fm.pct, "div_liq_ebitda": fm.vezes}
    dados = {"hoje": config.HOJE.isoformat(), "padrao": [a["ticker"] for a in acoes[:2]], "a": {}}
    for f in acoes:
        dados["a"][f["ticker"]] = {"url": url_ativo(f), "i": {
            k: ({"v": i["valor"], "t": fmt(i["valor"]), "f": i["fonte"], "r": i["ref"]} if i.get("status") == "ok"
                else {"t": None, "s": i.get("status")}) for k, fmt in fmts.items() for i in [f["ind"].get(k) or {}]}}
    migalhas = [("Início", config.SITE_URL + "/"), ("Ações", f"{BASE}/acoes/"), ("Comparar ações", url)]
    n_cob = len(acoes)
    idx = n_cob >= MIN_ATIVOS_RANKING_INDEXAVEL
    ctx = _base_ctx("Comparar ações: P/L, P/VP, ROE e margens", "Compare de 2 a 4 ações lado a lado, com dados da CVM e da B3 e fonte em cada número.",
                    url, migalhas, idx, config.HOJE.isoformat(), None, h1="Comparar ações lado a lado",
                    tickers=[f["ticker"] for f in acoes], dados=json.dumps(dados, ensure_ascii=False).replace("</", "<\\/"))
    ctx["scripts"] = [JS_COMPARAR]
    ctx["css_extra"] = ".cmp-form{display:flex;flex-wrap:wrap;gap:10px;margin:12px 0}.cmp-form select{font:inherit;padding:6px}"
    ctx["anuncio_final"] = _anuncio_final(env)
    return env.get_template("comparar.html").render(**ctx), idx, ("ok" if idx else f"menos de {MIN_ATIVOS_RANKING_INDEXAVEL} ações na cobertura"), ctx["titulo"]


def pagina_lista(env, fichas, tipo, selecao, rankings):
    url = f"{BASE}/{'acoes' if tipo == 'acao' else 'fiis'}/"
    fs = []
    for f in fichas:
        if f["tipo_pagina"] != tipo:
            continue
        fs.append(dict(f, url=url_ativo(f), grupo=(f.get("setor") if tipo == "acao" else f.get("segmento")) or "—"))
    if tipo == "acao":
        titulo, h1 = "Ações: indicadores e resultados com dados da CVM", "Ações: indicadores, dividendos e resultados"
        cols = [{"k": "preco", "rotulo": "Fechamento", "fmt": fm.brl}, {"k": "pl", "rotulo": "P/L", "fmt": lambda v: fm.numero(v, 1)},
                {"k": "pvp", "rotulo": "P/VP", "fmt": lambda v: fm.numero(v, 2)}, {"k": "roe", "rotulo": "ROE", "fmt": fm.pct},
                {"k": "dy_caixa", "rotulo": "DY de caixa", "fmt": fm.pct}]
        intro = "Cada página reúne cotação, resultados trimestrais, endividamento e proventos, com a fonte e a data de cada número."
        col_grupo = "Setor (CVM)"
    else:
        titulo, h1 = "FIIs: P/VP, vacância e cotistas com dados da CVM", "Fundos imobiliários: P/VP, vacância e cotistas"
        cols = [{"k": "preco", "rotulo": "Fechamento", "fmt": fm.brl}, {"k": "pvp", "rotulo": "P/VP", "fmt": lambda v: fm.numero(v, 2)},
                {"k": "dy_estimado", "rotulo": "DY estimado", "fmt": fm.pct}, {"k": "vacancia", "rotulo": "Vacância", "fmt": fm.pct},
                {"k": "cotistas", "rotulo": "Cotistas", "fmt": fm.inteiro}]
        intro = "Cada página reúne cotação, valor patrimonial, vacância, cotistas e uma estimativa de rendimentos, com fonte e data."
        col_grupo = "Segmento (CVM)"
    migalhas = [("Início", config.SITE_URL + "/"), ("Ações" if tipo == "acao" else "FIIs", url)]
    ctx = _base_ctx(titulo, intro, url, migalhas, True, config.HOJE.isoformat(), None, h1=h1, intro=intro,
                    aviso_escolha="Os primeiros ativos foram escolhidos pelo volume negociado na B3 nos últimos 12 meses. A escolha não é recomendação.",
                    fichas=fs, colunas=cols, col_grupo=col_grupo, janela=selecao["janela"], rankings=rankings,
                    metodologia=f"{BASE}/{'acoes' if tipo == 'acao' else 'fiis'}/metodologia/", largo=True)
    ctx["anuncio_final"] = _anuncio_final(env)
    return env.get_template("lista.html").render(**ctx), True, "ok", titulo


FORMULAS_ACOES = [
    ("P/L", "Valor de mercado ÷ lucro da controladora em 12 meses. Com prejuízo: não se aplica."),
    ("P/VP", "Valor de mercado ÷ (patrimônio líquido − participação de não controladores). Com patrimônio negativo: não se aplica."),
    ("ROE", "Lucro da controladora em 12 meses ÷ média do patrimônio da controladora (último balanço e 12 meses antes)."),
    ("DY de caixa", "Dividendos e JCP pagos em 12 meses (fluxo de caixa, atividades de financiamento, sem os pagos a não controladores) ÷ valor de mercado."),
    ("DY 12 meses", "Soma dos proventos por ação com data ex nos últimos 365 dias ÷ fechamento. Só com proventos aprovados (ainda não publicado)."),
    ("Margem líquida", "Lucro líquido total em 12 meses ÷ receita líquida em 12 meses. Receita ≤ 0: não se aplica. Bancos: não se aplica."),
    ("EBITDA calculado", "Resultado antes do resultado financeiro e dos tributos (3.05) + depreciação e amortização (DVA; se faltar, linhas do fluxo de caixa). Conceito da Resolução CVM 156/2022, sem ajustes."),
    ("Margem EBITDA", "EBITDA calculado ÷ receita líquida, 12 meses."),
    ("Dívida líquida / EBITDA", "(Empréstimos e financiamentos 2.01.04 + 2.02.01, sem arrendamentos − caixa 1.01.01 − aplicações 1.01.02) ÷ EBITDA de 12 meses. Segunda linha: somando os arrendamentos. EBITDA ≤ 0: não se aplica."),
    ("Valor de mercado", "Soma, por classe (ON e PN), de fechamento × ações em circulação (sem tesouraria), do último ITR ou DFP. Classe sem liquidez: preço implícito da unit ÷ ações por unit (marcado como estimado)."),
    ("12 meses (TTM)", "DFP do ano anterior + acumulado do ano no ITR atual − mesmo período do ano anterior (coluna do ITR atual, já reapresentada). No 4º trimestre, a DFP."),
    ("LPA e VPA", "Lucro da controladora em 12 meses e patrimônio da controladora ÷ ações em circulação (× ações por unit, na unit)."),
]
FORMULAS_FIIS = [
    ("P/VP", "Fechamento ÷ valor patrimonial da cota do último informe mensal. Conferência: patrimônio ÷ cotas emitidas."),
    ("DY estimado", "Σ (DY do mês informado à CVM × valor patrimonial da cota do mês) nos 12 últimos informes ÷ fechamento. Não é a soma dos rendimentos por cota com data com; fica indisponível se o informe tiver DY negativo, acima de 3% no mês ou meses copiados."),
    ("DY 12 meses", "Soma dos rendimentos por cota com data com nos últimos 365 dias ÷ fechamento. Só com rendimentos aprovados (ainda não publicado). Amortização não entra."),
    ("Vacância física", "Σ (área × vacância) ÷ Σ área dos imóveis para renda acabados, no último informe trimestral. Sem imóveis: não se aplica."),
    ("Cotistas", "Total de cotistas do informe mensal."),
]


def _explicacao_ferramenta(id_):
    markup = (config.PLUGIN / "ferramentas" / id_ / "markup.html").read_text()
    m = re.search(r'<section class="explain">(.*?)</section>', markup, flags=re.S)
    if not m:
        return ""
    # o texto do plugin aparece uma vez só, aqui; os h2 viram h3 para caber na página
    corpo = m.group(1).replace("<h2", "<h3").replace("</h2>", "</h3>")
    corpo = re.sub(r"Não é recomendação de compra ou venda de nenhum ativo\.", "Não é recomendação de compra ou venda.", corpo)
    corpo = re.sub(r"É um filtro de empresa sólida e barata, não uma previsão de preço\.",
                   "É um filtro de lucro e patrimônio, não uma previsão de preço.", corpo)
    corpo = corpo.replace("href=\"/", f"href=\"{config.SITE_URL}/")
    return corpo


def pagina_metodologia(env, tipo, val):
    url = f"{BASE}/{'acoes' if tipo == 'acao' else 'fiis'}/metodologia/"
    nomes = {}
    alertas = []
    for t, a in val["ativos"].items():
        for x in a["testes"]:
            nomes.setdefault((x["teste"], x["nome"].split(" (")[0].split(" de 20")[0], x["tipo"], x["tolerancia"]), []).append(x["ok"])
            if not x["ok"] and x["tipo"] == "alerta":
                alertas.append(f"{t}: {x['nome']} — {x['detalhe']}")
    testes = [{"teste": k[0], "nome": k[1], "tipo": k[2], "tolerancia": k[3], "resumo": f"{sum(v)}/{len(v)} ok"}
              for k, v in sorted(nomes.items(), key=lambda kv: kv[0][0])]
    testes += [{"teste": 13, "nome": "Todo número tem fonte e data no HTML", "tipo": "bloqueante", "tolerancia": "100%", "resumo": "no gerar"},
               {"teste": 14, "nome": "Sem palavras de recomendação nem corretoras", "tipo": "bloqueante", "tolerancia": "zero", "resumo": "no gerar"},
               {"teste": 15, "nome": "HTML válido, um H1, title ≤ 60, um JSON-LD, canonical", "tipo": "bloqueante", "tolerancia": "100%", "resumo": "no gerar"}]
    regras = (["Demonstração consolidada; se a empresa não publica, a individual, com aviso na página. Para cada documento, vale a maior versão entregue à CVM.",
               "Valores em milhares (ESCALA_MOEDA = MIL) são multiplicados por 1.000, menos o lucro por ação, que já vem em reais por ação.",
               "As contas são achadas pela descrição, não só pelo código: em bancos, o patrimônio é 2.08 e o lucro 3.11 com outra estrutura.",
               "Bancos e seguradoras: só P/L, P/VP, ROE e DY. Holding: aviso de que o lucro vem das participações.",
               "A quantidade de ações da composição do capital não tem coluna de escala. Quando o lucro ÷ LPA divulgado mostra que veio em milhares, ela é multiplicada por 1.000."]
              if tipo == "acao" else
              ["Para cada fundo e mês vale a maior versão do informe. O valor patrimonial da cota é de 1 a 2 meses atrás; a página mostra o mês.",
               "O ticker é ligado ao CNPJ pelo código ISIN. Quando dois CNPJs informam o mesmo ISIN, vale o de histórico mais longo."])
    id_f = "preco-justo" if tipo == "acao" else "renda-fii"
    migalhas = [("Início", config.SITE_URL + "/"), ("Ações" if tipo == "acao" else "FIIs", f"{BASE}/{'acoes' if tipo == 'acao' else 'fiis'}/"),
                ("Metodologia", url)]
    titulo = f"Metodologia: como calculamos os indicadores de {'ações' if tipo == 'acao' else 'FIIs'}"
    sobre = None
    ctx = _base_ctx(titulo, "Fórmulas, fontes oficiais (CVM, B3 e Banco Central) e testes automáticos de cada indicador.", url, migalhas,
                    True, config.HOJE.isoformat(), sobre, h1=titulo, tipo=tipo,
                    formulas=FORMULAS_ACOES if tipo == "acao" else FORMULAS_FIIS, regras=regras,
                    explicacao_ferramenta=_explicacao_ferramenta(id_f), id_ferramenta=id_f, testes=testes,
                    alertas=alertas if tipo == "acao" or True else [], hoje=config.HOJE.isoformat())
    ctx["anuncio_final"] = ""
    return env.get_template("metodologia.html").render(**ctx), True, "ok", titulo


def pagina_calendario(env):
    url = f"{BASE}/dividendos/calendario/"
    migalhas = [("Início", config.SITE_URL + "/"), ("Calendário de proventos", url)]
    titulo = "Calendário de dividendos e rendimentos"
    ctx = _base_ctx(titulo, "Datas com, ex e de pagamento de proventos de ações e FIIs, com link para o documento oficial.",
                    url, migalhas, False, config.HOJE.isoformat(), None, h1=titulo)
    return env.get_template("calendario.html").render(**ctx), False, "sem proventos aprovados (esqueleto)", titulo


# --------------------------------------------------------------------------------------- execução

def gerar_site(con, selecao, log=print) -> dict:
    env = _env()
    val = json.loads((config.CACHE / "validacao.json").read_text())
    fichas = []
    for a in selecao["acoes"] + selecao["fiis"]:
        fichas.append(json.loads((config.CACHE / "fichas" / f"{a['ticker']}.json").read_text()))
    cdi = cdi_12m(con)
    nomes_emissores = sorted({x for f in fichas for x in (f["nome"], f["nome_curto"])}, key=len, reverse=True)
    config.SAIDA.mkdir(parents=True, exist_ok=True)
    relatorio = {"gerado_em": datetime.now().isoformat(timespec="seconds"), "paginas": [], "nao_geradas": []}
    paginas_sitemap = []
    gravadas = []

    def registrar(rel_path, url, html, idx, motivo, titulo_base, ticker=None, lastmod=None):
        testes_html = seo.verificar_html(html, nomes_emissores, titulo_base)
        falhou = [t for t in testes_html if not t["ok"]]
        if ticker and val["ativos"].get(ticker, {}).get("bloqueado"):
            falhou.append({"teste": "dados", "detalhe": "teste bloqueante de dados"})
        if falhou:
            relatorio["nao_geradas"].append({"url": url, "falhas": falhou})
            log(f"NÃO GERADA {url}: " + "; ".join(f"{t['teste']}: {t['detalhe']}" for t in falhou))
            return
        _gravar(rel_path, html, gravadas)
        h = hashlib.sha256(html.encode()).hexdigest()[:16]
        relatorio["paginas"].append({"url": url, "arquivo": rel_path, "indexavel": idx, "motivo": motivo, "hash": h,
                                     "bytes": len(html.encode()), "testes_html": testes_html})
        paginas_sitemap.append({"url": url, "indexavel": idx, "lastmod": lastmod or config.HOJE.isoformat()})

    for f in fichas:
        gerar_fn = pagina_acao if f["tipo_pagina"] == "acao" else pagina_fii
        html, idx, motivo, tb = gerar_fn(env, con, f, fichas, val, cdi)
        pasta = "acoes" if f["tipo_pagina"] == "acao" else "fiis"
        registrar(f"{pasta}/{f['ticker'].lower()}/index.html", url_ativo(f), html, idx, motivo, tb, f["ticker"], _lastmod(f))
    rk_acoes, rk_fiis = [], []
    for tipo, lista, dest in (("acao", RANKINGS_ACOES, rk_acoes), ("fii", RANKINGS_FIIS, rk_fiis)):
        for slug, titulo, k, rotulo, fmt_, desc, explic in lista:
            html, idx, motivo, tb = pagina_ranking(env, fichas, tipo, slug, titulo, k, rotulo, fmt_, desc, explic, selecao["janela"])
            pasta = "acoes" if tipo == "acao" else "fiis"
            url = f"{BASE}/{pasta}/ranking/{slug}/"
            registrar(f"{pasta}/ranking/{slug}/index.html", url, html, idx, motivo, tb)
            dest.append({"url": url, "titulo": titulo})
    for tipo, rks in (("acao", rk_acoes), ("fii", rk_fiis)):
        html, idx, motivo, tb = pagina_lista(env, fichas, tipo, selecao, rks)
        pasta = "acoes" if tipo == "acao" else "fiis"
        registrar(f"{pasta}/index.html", f"{BASE}/{pasta}/", html, idx, motivo, tb)
        html, idx, motivo, tb = pagina_metodologia(env, tipo, val)
        registrar(f"{pasta}/metodologia/index.html", f"{BASE}/{pasta}/metodologia/", html, idx, motivo, tb)
    html, idx, motivo, tb = pagina_comparar(env, fichas)
    registrar("comparar/acoes/index.html", f"{BASE}/comparar/acoes/", html, idx, motivo, tb)
    html, idx, motivo, tb = pagina_calendario(env)
    registrar("dividendos/calendario/index.html", f"{BASE}/dividendos/calendario/", html, idx, motivo, tb)

    (config.SAIDA / "sitemap-ativos.xml").write_text(seo.sitemap(paginas_sitemap))
    (config.SAIDA / "robots-trecho.txt").write_text(f"# Acrescentar ao robots.txt do domínio (não aplicado):\nSitemap: {BASE}/sitemap-ativos.xml\n")
    _, invalidos = tickers_cotacao()
    seo.redirecionamentos(config.SAIDA, [f["ticker"] for f in fichas if f["tipo_pagina"] == "acao"
                                          and not any(p["url"] == url_ativo(f) for p in relatorio["nao_geradas"])],
                          invalidos, BASE)
    with open(config.SAIDA / "paginas.csv", "w", newline="") as fcsv:
        w = csv.writer(fcsv)
        w.writerow(["url", "indexavel", "motivo", "bytes"])
        for p in relatorio["paginas"]:
            w.writerow([p["url"], "sim" if p["indexavel"] else "não (noindex, fora do sitemap)", p["motivo"], p["bytes"]])
    (config.SAIDA / "_relatorio.json").write_text(json.dumps(relatorio, ensure_ascii=False, indent=1))
    n_idx = sum(1 for p in relatorio["paginas"] if p["indexavel"])
    log(f"geradas {len(relatorio['paginas'])} páginas ({n_idx} indexáveis), {len(relatorio['nao_geradas'])} não geradas")
    return relatorio
