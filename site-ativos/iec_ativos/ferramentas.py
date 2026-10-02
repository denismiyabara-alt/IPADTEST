"""Ferramentas do plugin iec-ferramentas embutidas no modo compacto (DESENHO 5.6).

O plugin publicado (1.2.0) ainda não tem atributos de preenchimento nem `modo="compacto"`. Para não
mexer nele, o build lê os arquivos do plugin (fonte única: markup.html, style.css e app.js) e aplica
aqui, de forma verificável, o que a versão 1.3.0 fará:

1. preenchimento: os valores do ativo entram como `data-*` no contêiner e no `value` dos campos;
2. modo compacto: as seções "Como funcionam..." e "Premissas" saem e viram um link para a
   metodologia (o mesmo texto não se repete em 20 ou 300 páginas);
3. preco-justo só calcula no clique (decisão do Denis): sai o recálculo a cada tecla e a conta
   inicial; entra um botão "Calcular". Os textos de conclusão da ferramenta ("pode haver desconto",
   "pode estar cara") são trocados por frases neutras, porque nas páginas de ativo o resultado ficaria
   colado num ticker.

Cada troca confere se o trecho original existe. Se o plugin mudar, o build para com erro em vez de
publicar uma ferramenta quebrada.
"""
import re
from html import escape

from . import config


class PluginMudou(RuntimeError):
    pass


def _ler(id_):
    p = config.PLUGIN / "ferramentas" / id_
    return ((p / "markup.html").read_text(), (p / "style.css").read_text(), (p / "app.js").read_text())


def _trocar(txt: str, antigo: str, novo: str, onde: str) -> str:
    if antigo not in txt:
        raise PluginMudou(f"{onde}: trecho esperado não encontrado no plugin: {antigo[:70]!r}")
    return txt.replace(antigo, novo)


def _compactar(markup: str, id_: str, link: str, texto_link: str) -> str:
    novo, n = re.subn(r'\s*<section class="explain">.*?</section>',
                      f'\n  <p class="iec-compacto">{escape(texto_link)} <a href="{escape(link)}">Veja a metodologia</a>.</p>',
                      markup, flags=re.S)
    if n != 1:
        raise PluginMudou(f"{id_}: esperava 1 <section class=\"explain\">, achei {n}")
    return novo


def _valor(markup: str, campo: str, valor: float, casas: int = 2) -> str:
    padrao = rf'(<input id="{campo}"[^>]*?value=")[^"]*(")'
    novo, n = re.subn(padrao, rf"\g<1>{valor:.{casas}f}\g<2>", markup)
    if n != 1:
        raise PluginMudou(f"campo {campo} não encontrado")
    return novo


def _data_attrs(markup: str, id_: str, attrs: dict) -> str:
    alvo = f'<div id="{id_}" class="iec-ferramenta">'
    extra = " ".join(f'data-{k}="{escape(str(v))}"' for k, v in attrs.items())
    return _trocar(markup, alvo, f'<div id="{id_}" class="iec-ferramenta" {extra}>', id_)


def preco_justo(preco: float, dpa: float | None, lpa: float | None, vpa: float | None, fonte: str, link: str) -> dict:
    markup, css, js = _ler("preco-justo")
    markup = _data_attrs(markup, "preco-justo", {"modo": "compacto", "calculo": "clique", "preco": f"{preco:.2f}",
                                                 "dpa": f"{dpa or 0:.2f}", "lpa": f"{lpa or 0:.2f}",
                                                 "vpa": f"{vpa or 0:.2f}", "fonte": fonte})
    markup = _compactar(markup, "preco-justo", link, "Como funcionam Bazin e Graham, e os limites dos dois métodos:")
    markup = re.sub(r'(<h2 class="titulo">.*?</h2>\s*)<p>.*?</p>',
                    r'\1<p>Conta matemática com os dados desta página. Os campos já vêm preenchidos; a taxa mínima '
                    r'é escolha sua. Não é preço-alvo nem recomendação.</p>', markup, count=1, flags=re.S)
    for campo, v in (("g-preco", preco), ("g-dpa", dpa or 0), ("g-lpa", lpa or 0), ("g-vpa", vpa or 0)):
        markup = _valor(markup, campo, v)
    markup = _trocar(markup, "Valores de exemplo, não de uma empresa real. Use os dados do último balanço e dos proventos pagos nos últimos 12 meses.",
                     escape(f"Preenchido com: {fonte}. Você pode trocar qualquer número."), "preco-justo")
    markup = _trocar(markup, '<div class="err" id="g-err" hidden></div>',
                     '<div class="err" id="g-err" hidden></div>\n      <button type="button" id="g-calcular" class="iec-botao">Calcular</button>',
                     "preco-justo")
    # JS: só no clique, e conclusões neutras
    js = _trocar(js, '["g-preco","g-dpa","g-taxa","g-lpa","g-vpa"].forEach(function(id){ $(id).addEventListener("input",calcular); });\ncalcular();',
                 '''function limpar(){ ["g-bazin","g-graham","g-dy","g-pl","g-pvp"].forEach(function(id){ $(id).textContent="—"; });
  $("g-bazin-m").textContent=""; $("g-graham-m").textContent=""; $("g-story").hidden=true; $("g-err").hidden=true; }
["g-preco","g-dpa","g-taxa","g-lpa","g-vpa"].forEach(function(id){ $(id).addEventListener("input",limpar); });
$("g-calcular").addEventListener("click",calcular);
limpar();''', "preco-justo app.js")
    js = _trocar(js, "Pelos métodos que se aplicam, a cotação está abaixo do preço calculado. Isso indica que pode haver desconto, não que a ação vai subir: confira dívida, setor e se o lucro é recorrente.",
                 "Pelos métodos que se aplicam, a cotação está abaixo do número calculado. É só o resultado da conta com esses dados: não diz nada sobre o preço futuro.", "app.js")
    js = _trocar(js, "Pelos métodos que se aplicam, a cotação está acima do preço calculado. O mercado pode estar pagando por um crescimento que esses métodos não enxergam, ou a ação pode estar cara.",
                 "Pelos métodos que se aplicam, a cotação está acima do número calculado. Esses métodos não enxergam crescimento, dívida nem qualidade da gestão.", "app.js")
    return {"html": markup, "css": css + CSS_EXTRA, "js": js}


def renda_fii(dy_mensal_pct: float | None, fonte: str, link: str) -> dict:
    markup, css, js = _ler("renda-fii")
    attrs = {"modo": "compacto", "fonte": fonte}
    if dy_mensal_pct:
        attrs["dy"] = f"{dy_mensal_pct:.2f}"
        markup = _valor(markup, "f-dy", dy_mensal_pct)
        markup = _trocar(markup, "Todos os valores são exemplos. Troque pelos seus. O dividend yield muda de fundo para fundo e de mês para mês.",
                         escape(f"Dividend yield mensal preenchido com a média estimada dos últimos 12 meses ({fonte}). "
                                "Os outros campos são exemplos. O rendimento muda de mês para mês."), "renda-fii")
    markup = _data_attrs(markup, "renda-fii", attrs)
    markup = _compactar(markup, "renda-fii", link, "Por que reinvestir muda o resultado, e as premissas do simulador:")
    return {"html": markup, "css": css + CSS_EXTRA.replace("#preco-justo", "#renda-fii"), "js": js}


CSS_EXTRA = """
#preco-justo .iec-compacto { margin: 16px 0 0; font-size: 15px; color: var(--muted); }
#preco-justo .iec-botao { margin-top: 14px; padding: 10px 22px; font: 600 15px/1.2 var(--font-body);
  color: #fff; background: var(--accent); border: 0; border-radius: var(--radius); cursor: pointer; }
#preco-justo .iec-botao:focus-visible { outline: 3px solid var(--amber); outline-offset: 2px; }
"""
