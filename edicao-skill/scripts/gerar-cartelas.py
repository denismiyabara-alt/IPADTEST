#!/usr/bin/env python3
# ponytail: gera as 18 cartelas a partir de uma tabela — mesma estrutura da peca aprovada (Prudential)
import json, os

W, H = 1920, 1080
INK, DIM, GOLD, DANGER, BG = "#0E0E0E", "#4A4A4A", "#B58200", "#C8261D", "#F4F1EA"

# icones stroke-only, geometricos — viewBox 0 0 100 100
ICONS = {
 "galpao":   "M8 62 L50 30 L92 62 M16 62 L16 88 L84 88 L84 62 M38 88 L38 64 L62 64 L62 88",
 "shopping": "M14 40 L86 40 L86 88 L14 88 Z M14 40 L24 18 L76 18 L86 40 M34 88 L34 60 L66 60 L66 88 M34 60 L66 60",
 "torre":    "M28 92 L28 20 L72 20 L72 92 M40 32 L40 40 M60 32 L60 40 M40 52 L40 60 M60 52 L60 60 M40 72 L40 80 M60 72 L60 80",
 "sala":     "M12 84 L12 34 L88 34 L88 84 Z M12 34 L50 12 L88 34 M42 84 L42 58 L58 58 L58 84",
 "moeda":    "M50 12 A38 38 0 1 1 49.9 12 M36 34 L36 66 M36 34 L58 34 A11 11 0 0 1 58 56 L36 56 M48 56 L64 66",
 "seta":     "M50 14 L50 82 M28 60 L50 84 L72 60",
 "regua":    "M8 40 L92 40 L92 68 L8 68 Z M24 40 L24 56 M40 40 L40 62 M56 40 L56 56 M72 40 L72 62",
 "documento":"M24 8 L64 8 L80 26 L80 92 L24 92 Z M64 8 L64 26 L80 26 M36 44 L68 44 M36 58 L68 58 M36 72 L56 72",
 "balanca":  "M50 14 L50 88 M22 88 L78 88 M18 34 L82 34 M18 34 L6 60 A16 12 0 0 0 30 60 Z M82 34 L70 60 A16 12 0 0 0 94 60 Z",
 "relogio":  "M50 10 A40 40 0 1 1 49.9 10 M50 28 L50 52 L68 62",
}

FR = [
 # id, tipo, dur, icone, dados
 ("01-1960","countup",11.0,"moeda", dict(rot="ANUNCIADO NA TELA DO APP", val=19.60, dec=2, suf="%", sub="AO ANO", pe="VENDA DE IMÓVEL — UMA VEZ SÓ", cor=INK)),
 ("02-093","kinetic",10.9,"documento", dict(rot="O MESMO RELATÓRIO, NO RODAPÉ", l1="R$ 0,93", l2="por cota, até dez/2026", pe="NOTA TÉCNICA DA 13ª EMISSÃO")),
 ("03-queda","comparison",11.0,"seta", dict(rot="A COTA, NÃO O DIVIDENDO", ea="R$ 91,10", eal="fim de julho", eb="R$ 70,13", ebl="hoje", delta="−23%", cor=DANGER)),
 ("04-iguatemi","countup",5.0,"shopping", dict(rot="5 SHOPPINGS DA IGUATEMI", val=876.1, dec=1, suf=" MI", pre="R$ ", sub="R$ 876.148.751,69", pe="FATO RELEVANTE · 07 AGO 2026", cor=INK)),
 ("05-guarulhos","countup",10.0,"galpao", dict(rot="GUARULHOS — A MAIOR DA HISTÓRIA DO FUNDO", val=1.435, dec=3, suf=" BI", pre="R$ ", sub="3 GALPÕES · 2 COM MERCADO LIVRE · 1 EM OBRA (K300)", pe="FATO RELEVANTE · 20 JUL 2026", cor=INK)),
 ("06-abl","countup",10.1,"galpao", dict(rot="UMA COMPRA SÓ", val=19, dec=0, suf="%", pre="+", sub="DE ÁREA ALUGÁVEL DO FUNDO INTEIRO", pe="", cor=GOLD)),
 ("07-caprate","kinetic",11.0,"regua", dict(rot="GUARDA ESSE NÚMERO", l1="7,30", l2="cap rate da compra dos shoppings", pe="VOLTA NO FIM DO VÍDEO")),
 ("08-degraus","grid",10.3,"seta", dict(rot="OS DEGRAUS DA QUEDA", linhas=[("12 de agosto","R$ 81,35"),("1 semana depois","R$ 70,13"),("no ano","−25%")], pe="", destaque=2, icone_bottom=520)),
 ("09-preco-emissao","grid",9.2,"documento", dict(rot="O PREÇO DA EMISSÃO", linhas=[("preço de emissão","R$ 94,25"),("custo da oferta","R$ 0,14"),("total por cota","R$ 94,39")], pe="NOTA TÉCNICA DA 13ª EMISSÃO", destaque=0, cor_destaque=GOLD, icone_bottom=520)),
 ("10-tela-vs-oferta","comparison",10.2,"balanca", dict(rot="MESMA COTA, MESMO DIVIDENDO", ea="15,7%", eal="comprando na tela", eb="11,8%", ebl="entrando na oferta", delta="+32% DE RENDA", cor=GOLD)),
 ("11-ocupacao","grid",7.5,"shopping", dict(rot="TAXA DE OCUPAÇÃO DOS CINCO", linhas=[("Iguatemi Alphaville","97,8%"),("Outlet Novo Hamburgo","97,7%"),("Praia de Belas","93,9%"),("Iguatemi Ribeirão Preto","90,4%"),("Iguatemi S. J. Rio Preto","85,7%")], pe="FATO RELEVANTE · 07 AGO 2026", destaque=4, icone_bottom=560)),
 ("12-taxas","grid",11.0,"moeda", dict(rot="TRÊS TAXAS", linhas=[("1% administração","sobre o TAMANHO"),("20% performance","sobre a RENDA distribuída"),("4% desenvolvimento","sobre o CAPEX")], pe="NENHUMA SOBRE O PREÇO DO IMÓVEL", destaque=-1, valor_texto=True, icone_bottom=520)),
 ("13-performance","comparison",11.0,"regua", dict(rot="A TAXA DE PERFORMANCE PASSOU", ea="11,5%", eal="R$ 11,16 sobre a cota patrimonial", eb="10,71%", ebl="IPCA + 6 com a inflação de hoje", delta="PASSOU", cor=GOLD)),
 ("14-escala-taxa","comparison",11.0,"sala", dict(rot="1% AO ANO, SÓ DE ADMINISTRAÇÃO", ea="R$ 50 mi", eal="com 5 bilhões", eb="R$ 100 mi", ebl="com 10 bilhões", delta="POR ANO", cor=INK)),
 ("15-cdi","comparison",6.7,"relogio", dict(rot="NA MESMA RÉGUA", ea="12,06%", eal="shopping, já com inflação", eb="13,90%", ebl="CDI, sem vacância e sem obra", delta="−1,84 PONTO", cor=DANGER)),
 ("16-13a","kinetic",10.6,"documento", dict(rot="NÃO É A PRIMEIRA", l1="13ª emissão", l2="a décima terceira vez que o fundo pede pra você acreditar", pe="")),
 ("17-ntnb","comparison",10.4,"balanca", dict(rot="O NÚMERO QUE VOCÊ GUARDOU", ea="7,30%", eal="cap rate do shopping", eb="7,32%", ebl="NTN-B 2050, o governo", delta="EMPATE TÉCNICO · 0,02", cor=DANGER)),
 ("18-veredito","comparison",8.2,"balanca", dict(rot="A MESMA COTA, DOIS PREÇOS", ea="R$ 70,13", eal="a bolsa cobra", eb="R$ 94,25", ebl="a oferta cobra", delta="", cor=INK)),
]

FONTS = """
      @font-face { font-family:"IC-Anton"; src:url("assets/fonts/Anton-400.woff2") format("woff2"); font-weight:400; }
      @font-face { font-family:"IC-Inter"; src:url("assets/fonts/Inter-600.woff2") format("woff2"); font-weight:600; }
      @font-face { font-family:"IC-Mono";  src:url("assets/fonts/JetBrainsMono-400.woff2") format("woff2"); font-weight:400; }
"""

def base_css(fid, d):
    return f"""
      #root {{ position:absolute; inset:0; width:{W}px; height:{H}px; overflow:hidden;
               font-family:"IC-Inter",sans-serif; background:{BG}; }}
{FONTS}
      #root .fade {{ position:absolute; inset:0; opacity:0; }}
      #root .bg {{ position:absolute; inset:0; background:{BG}; }}
      #root .vinheta {{ position:absolute; inset:0;
        background:radial-gradient(ellipse at 50% 45%, rgba(0,0,0,0) 55%, rgba(0,0,0,0.10) 100%); }}
      #root .icone {{ position:absolute; right:120px; bottom:{d.get("icone_bottom",96)}px; width:300px; height:300px; opacity:0.13; }}
      #root .icone path {{ fill:none; stroke:{INK}; stroke-width:2.2; stroke-linecap:round; stroke-linejoin:round; }}
      #root .rotulo {{ position:absolute; top:132px; left:0; width:100%; text-align:center;
        font-family:"IC-Mono",monospace; font-size:26px; letter-spacing:6px; text-transform:uppercase;
        color:{DIM}; opacity:0; }}
      #root .pe {{ position:absolute; bottom:96px; left:0; width:100%; text-align:center;
        font-family:"IC-Mono",monospace; font-size:22px; letter-spacing:5px; text-transform:uppercase;
        color:{DIM}; opacity:0; }}
"""

def icone_svg(nome):
    if not nome: return ""
    return f'<svg class="icone" viewBox="0 0 100 100"><path id="ico" d="{ICONS[nome]}"/></svg>'

def wrap(fid, dur, css, corpo, js):
    return f"""<template>
  <div id="root" data-composition-id="{fid}" data-start="0" data-duration="{dur}" data-width="{W}" data-height="{H}">
    <style>{css}    </style>

    <div id="cena-{fid}-fade" class="clip fade" data-start="0" data-duration="{dur}" data-track-index="0">
      <div class="bg"></div>
      <div class="vinheta"></div>
{corpo}
    </div>

    <script>
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
        const DUR = {dur};
        tl.to("#cena-{fid}-fade", {{ opacity: 1, duration: 0.35, ease: "power2.out" }}, 0);
        tl.to("#cena-{fid}-fade", {{ opacity: 0, duration: 0.35, ease: "power2.in" }}, DUR - 0.35);
        const ico = document.getElementById("ico");
        if (ico) {{
          const len = 900;
          gsap.set(ico, {{ strokeDasharray: len, strokeDashoffset: len }});
          tl.to(ico, {{ strokeDashoffset: 0, duration: 1.6, ease: "power2.out" }}, 0.3);
        }}
{js}
        window.__timelines["{fid}"] = tl;
      }})();
    </script>
  </div>
</template>
"""

def cena_countup(fid, dur, d):
    css = base_css(fid, d) + f"""
      #root .num-wrap {{ position:absolute; top:352px; left:0; width:100%;
        display:flex; align-items:baseline; justify-content:center; }}
      #root .num {{ font-family:"IC-Anton",sans-serif; font-variant-numeric:tabular-nums;
        display:inline-block; font-size:300px; line-height:1; color:{d['cor']}; transform-origin:center center; }}
      #root .suf {{ font-family:"IC-Anton",sans-serif; font-size:210px; line-height:1;
        margin-left:18px; color:{d['cor']}; opacity:0; }}
      #root .sub {{ position:absolute; top:730px; left:0; width:100%; text-align:center;
        font-family:"IC-Inter",sans-serif; font-size:38px; letter-spacing:1px; color:{DIM}; opacity:0; }}
"""
    pre = d.get("pre", "")
    corpo = f"""      <div class="rotulo" id="rot">{d['rot']}</div>
      <div class="num-wrap"><span class="num" id="num">{pre}0</span><span class="suf" id="suf">{d['suf']}</span></div>
      <div class="sub" id="sub">{d['sub']}</div>
      <div class="pe" id="pe">{d['pe']}</div>
{icone_svg(d.get('icone',''))}"""
    js = f"""
        const st = {{ v: 0 }};
        const num = document.getElementById("num");
        const DEC = {d['dec']}, ALVO = {d['val']}, PRE = "{pre}";
        tl.to(st, {{ v: ALVO, duration: 1.7, ease: "power3.out", onUpdate: () => {{
          num.textContent = PRE + st.v.toFixed(DEC).replace(".", ",");
        }} }}, 0.5);
        tl.fromTo("#num", {{ scale: 0.55 }}, {{ scale: 1, duration: 1.7, ease: "power3.out" }}, 0.5);
        tl.to("#rot", {{ opacity: 1, duration: 0.5, ease: "power2.out" }}, 0.15);
        tl.to("#suf", {{ opacity: 1, duration: 0.35, ease: "back.out(1.6)" }}, 2.1);
        tl.fromTo("#sub", {{ y: 18 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power2.out" }}, 1.6);
        tl.to("#pe", {{ opacity: 1, duration: 0.5, ease: "power2.out" }}, 2.3);
"""
    return wrap(fid, dur, css, corpo, js)

def cena_kinetic(fid, dur, d):
    css = base_css(fid, d) + f"""
      #root .l1 {{ position:absolute; top:368px; left:0; width:100%; text-align:center;
        font-family:"IC-Anton",sans-serif; font-size:280px; line-height:1; color:{INK}; opacity:0; }}
      #root .l2 {{ position:absolute; top:788px; left:0; width:100%; text-align:center;
        font-family:"IC-Inter",sans-serif; font-size:44px; letter-spacing:1px; color:{DIM}; opacity:0; }}
"""
    corpo = f"""      <div class="rotulo" id="rot">{d['rot']}</div>
      <div class="l1" id="l1">{d['l1']}</div>
      <div class="l2" id="l2">{d['l2']}</div>
      <div class="pe" id="pe">{d['pe']}</div>
{icone_svg(d.get('icone',''))}"""
    js = """
        tl.to("#rot", { opacity: 1, duration: 0.5, ease: "power2.out" }, 0.15);
        tl.fromTo("#l1", { scale: 0.86, y: 24 }, { scale: 1, y: 0, opacity: 1, duration: 0.7, ease: "power3.out" }, 0.5);
        tl.fromTo("#l2", { y: 20 }, { y: 0, opacity: 1, duration: 0.5, ease: "power2.out" }, 1.15);
        tl.to("#pe", { opacity: 1, duration: 0.5, ease: "power2.out" }, 1.9);
"""
    return wrap(fid, dur, css, corpo, js)

def cena_comparison(fid, dur, d):
    css = base_css(fid, d) + f"""
      #root .col {{ position:absolute; top:330px; width:760px; text-align:center; opacity:0; }}
      #root .col-a {{ left:110px; }}
      #root .col-b {{ right:110px; }}
      #root .val {{ font-family:"IC-Anton",sans-serif; font-size:180px; line-height:1; color:{INK}; padding-bottom:18px;
        font-variant-numeric:tabular-nums; }}
      #root .val-b {{ color:{DIM}; }}
      #root .cap {{ margin-top:96px; font-family:"IC-Inter",sans-serif; font-size:34px; color:{DIM}; }}
      #root .eixo {{ position:absolute; top:340px; left:960px; width:2px; height:280px;
        background:{DIM}; opacity:0; transform-origin:top center; }}
      #root .delta {{ position:absolute; top:706px; left:0; width:100%; text-align:center;
        font-family:"IC-Anton",sans-serif; font-size:112px; line-height:1; color:{d['cor']}; opacity:0; }}
"""
    corpo = f"""      <div class="rotulo" id="rot">{d['rot']}</div>
      <div class="col col-a" id="ca"><div class="val">{d['ea']}</div><div class="cap">{d['eal']}</div></div>
      <div class="eixo" id="eixo"></div>
      <div class="col col-b" id="cb"><div class="val val-b">{d['eb']}</div><div class="cap">{d['ebl']}</div></div>
      <div class="delta" id="delta">{d['delta']}</div>
      <div class="pe" id="pe"></div>
{icone_svg(d.get('icone',''))}"""
    js = """
        tl.to("#rot", { opacity: 1, duration: 0.5, ease: "power2.out" }, 0.15);
        tl.fromTo("#ca", { x: -70 }, { x: 0, opacity: 1, duration: 0.7, ease: "power3.out" }, 0.45);
        tl.fromTo("#cb", { x: 70 }, { x: 0, opacity: 1, duration: 0.7, ease: "power3.out" }, 0.65);
        tl.fromTo("#eixo", { scaleY: 0 }, { scaleY: 1, opacity: 0.35, duration: 0.6, ease: "power2.out" }, 0.9);
        tl.fromTo("#delta", { scale: 0.8 }, { scale: 1, opacity: 1, duration: 0.5, ease: "back.out(1.5)" }, 1.7);
"""
    return wrap(fid, dur, css, corpo, js)

def cena_grid(fid, dur, d):
    linhas = d["linhas"]
    css = base_css(fid, d) + f"""
      #root .lista {{ position:absolute; top:300px; left:300px; width:1320px; }}
      #root .linha {{ display:flex; align-items:baseline; justify-content:space-between;
        padding:16px 0; border-bottom:1.5px solid rgba(14,14,14,0.14); opacity:0; }}
      #root .rot-l {{ font-family:"IC-Inter",sans-serif; font-size:42px; color:{DIM}; }}
      #root .val-l {{ font-family:"IC-Anton",sans-serif; font-size:78px; line-height:1; color:{INK};
        font-variant-numeric:tabular-nums; }}
      #root .lista.texto .val-l {{ font-family:"IC-Inter",sans-serif; font-size:44px; letter-spacing:0.5px; }}
      #root .linha.hot .val-l {{ color:{d.get("cor_destaque", DANGER)}; }}
      #root .linha.hot .rot-l {{ color:{INK}; }}
"""
    cls_lista = " texto" if d.get("valor_texto") else ""
    itens = "\n".join(
        f'        <div class="linha{" hot" if i == d.get("destaque", -1) else ""}" id="ln{i}">'
        f'<span class="rot-l">{a}</span><span class="val-l">{b}</span></div>'
        for i, (a, b) in enumerate(linhas))
    corpo = f"""      <div class="rotulo" id="rot">{d['rot']}</div>
      <div class="lista{cls_lista}">
{itens}
      </div>
      <div class="pe" id="pe">{d['pe']}</div>
{icone_svg(d.get('icone',''))}"""
    passo = round(min(0.55, (dur - 2.3) / max(len(linhas), 1)), 2)
    js = f"""
        tl.to("#rot", {{ opacity: 1, duration: 0.5, ease: "power2.out" }}, 0.15);
        const PASSO = {passo};
        for (let i = 0; i < {len(linhas)}; i++) {{
          tl.fromTo("#ln" + i, {{ x: -28 }},
            {{ x: 0, opacity: 1, duration: 0.45, ease: "power2.out" }}, 0.55 + i * PASSO);
        }}
        tl.to("#pe", {{ opacity: 1, duration: 0.5, ease: "power2.out" }}, 0.6 + {len(linhas)} * PASSO);
"""
    return wrap(fid, dur, css, corpo, js)

GER = {"countup": cena_countup, "kinetic": cena_kinetic, "comparison": cena_comparison, "grid": cena_grid}

os.makedirs("compositions/frames", exist_ok=True)
hosts, t = [], 0.0
OVER = 0.3   # sobreposicao do crossfade
for i, (fid, tipo, dur, ico, d) in enumerate(FR):
    d["icone"] = ico
    open(f"compositions/frames/{fid}.html", "w").write(GER[tipo](fid, dur, d))
    hosts.append(f"""      <div id="el-{fid}" class="scene" data-composition-id="{fid}"
        data-composition-src="compositions/frames/{fid}.html"
        data-start="{t:.2f}" data-duration="{dur}" data-track-index="{i % 4}"
        data-width="{W}" data-height="{H}"></div>""")
    t += dur - OVER
total = round(t + OVER, 2)

open("index.html", "w").write(f"""<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>TRXF11 — B-roll de dados</title>
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
    <style>
      * {{ margin:0; padding:0; box-sizing:border-box; }}
      html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:{BG}; }}
      #root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; background:{BG}; }}
      .scene {{ position:absolute; inset:0; width:100%; height:100%; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{total}"
         data-width="{W}" data-height="{H}">
{chr(10).join(hosts)}
    </div>
    <script>
      window.__timelines["main"] = gsap.timeline({{ paused: true }});
    </script>
  </body>
</html>
""")
print(f"{len(FR)} cenas · total {total}s")
