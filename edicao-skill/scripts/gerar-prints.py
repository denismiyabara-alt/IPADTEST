#!/usr/bin/env python3
# ponytail: peca de matérias — print real + push-in + sublinhado desenhado no trecho citado
import os

W, H = 1920, 1080
INK, DIM, GOLD, DANGER, BG = "#0E0E0E", "#4A4A4A", "#B58200", "#C8261D", "#F4F1EA"

# janela do print dentro do papel
JW, JH = 1560, 800           # janela maior: o texto precisa ser lido em 1080p
JX, JY = (W - JW) // 2, 168

CENAS = [
 # id, arquivo, w, h, alvo_y, alvo_x0, alvo_x1, dur, rotulo, legenda, zoom
 ("m0-nota093", "nota-tecnica-093.png", 1075, 1521, 0.663, 0.09, 0.92, 10.0,
  "NOTA TÉCNICA · RELATÓRIO GERENCIAL 31/07/2026", "o que ela escreveu que ia pagar", 1.1),
 ("m7-grafico", "grafico-i10.png", 1300, 1200, 0.45, 0.5, 0.5, 9.0,
  "INVESTIDOR10 · COTAÇÃO TRXF11", "o degrau no fim do gráfico é a queda", 1.15),
 ("m1-fatos", "site-fatos-relevantes.png", 2200, 1800, 0.912, 0.06, 0.62, 9.9,
  "TRXF11.COM.BR · FATOS RELEVANTES", "cinco anúncios em oito dias", 1.9),
 ("m2-iguatemi", "fr-iguatemi.png", 1075, 1521, 0.781, 0.08, 0.92, 11.0,
  "FATO RELEVANTE · 07 AGO 2026", "o preço dos cinco shoppings", 2.1),
 ("m3-guarulhos", "fr-guarulhos.png", 1075, 1521, 0.124, 0.08, 0.92, 11.0,
  "FATO RELEVANTE · 20 JUL 2026", "a maior compra da história do fundo", 2.1),
 ("m4-keleti-08", "tweet-keleti-08ago.png", 1240, 1800, 0.710, 0.12, 0.81, 11.0,
  "@CCKELETI · 08 AGO 2026", "o comunicado da Iguatemi, no post do gestor", 2.3),
 ("m5-nota", "nota-tecnica-taxa.png", 1075, 1521, 0.336, 0.10, 0.91, 11.0,
  "NOTA TÉCNICA DA 13ª EMISSÃO · PÁG. 14", "a taxa de performance, com todas as letras", 2.1),
 ("m6-keleti-14", "tweet-keleti-14ago.png", 1240, 1800, 0.122, 0.03, 0.79, 10.3,
  "@CCKELETI · 14 AGO 2026", "o mesmo alerta, uma semana depois", 1.35),
]

def cena(cid, arq, iw, ih, alvo, ax0, ax1, dur, rotulo, legenda, zoom):
    zoom = min(2.6, 0.92 / max(0.05, ax1 - ax0))   # a linha citada ocupa ~92% da janela
    iw_esc = JW * zoom
    ih_esc = ih * (iw_esc / iw)
    cx = (ax0 + ax1) / 2
    tx = -(cx * iw_esc - JW / 2)
    ty = -(alvo * ih_esc - JH / 2)
    x0 = max(JX + 24, JX + ax0 * iw_esc + tx)
    x1 = min(JX + JW - 24, JX + ax1 * iw_esc + tx)
    sub_x, sub_w = x0, max(120, x1 - x0)
    svg_sub = "" if abs(ax1 - ax0) < 1e-6 else (
        f'<svg class="sub" id="sub" viewBox="0 0 {sub_w:.0f} 14" preserveAspectRatio="none">'
        f'<path d="M2 9 Q {sub_w*0.25:.0f} 3, {sub_w*0.5:.0f} 8 T {sub_w-2:.0f} 7" /></svg>')
    sub_y = JY + JH / 2 + 12
    return f"""<template>
  <div id="root" data-composition-id="{cid}" data-start="0" data-duration="{dur}" data-width="{W}" data-height="{H}">
    <style>
      #root {{ position:absolute; inset:0; width:{W}px; height:{H}px; overflow:hidden;
               font-family:"IC-Inter",sans-serif; background:{BG}; }}
      @font-face {{ font-family:"IC-Inter"; src:url("assets/fonts/Inter-600.woff2") format("woff2"); font-weight:600; }}
      @font-face {{ font-family:"IC-Mono";  src:url("assets/fonts/JetBrainsMono-400.woff2") format("woff2"); font-weight:400; }}
      #root .fade {{ position:absolute; inset:0; opacity:0; }}
      #root .bg {{ position:absolute; inset:0; background:{BG}; }}
      #root .janela {{ position:absolute; left:{JX}px; top:{JY}px; width:{JW}px; height:{JH}px;
        overflow:hidden; background:#fff; box-shadow:0 18px 60px rgba(14,14,14,0.16); }}
      #root .janela img {{ position:absolute; left:0; top:0; width:{iw_esc:.0f}px; height:{ih_esc:.0f}px;
        transform:translate({tx:.0f}px, {ty:.0f}px); filter:grayscale(1) contrast(1.06); }}
      #root .lupa {{ position:absolute; inset:0; transform-origin:50% 50%; }}
      #root .duotone {{ position:absolute; inset:0; background:{INK}; opacity:0.07; mix-blend-mode:multiply; }}
      #root .veu {{ position:absolute; inset:0;
        background:linear-gradient(180deg, rgba(244,241,234,0.55) 0%, rgba(244,241,234,0) 22%,
                   rgba(244,241,234,0) 78%, rgba(244,241,234,0.55) 100%); }}
      #root .sub {{ position:absolute; left:{sub_x:.0f}px; top:{sub_y:.0f}px; width:{sub_w:.0f}px; height:14px; }}
      #root .sub path {{ fill:none; stroke:{DANGER}; stroke-width:5; stroke-linecap:round; }}
      #root .rotulo {{ position:absolute; top:104px; left:{JX}px;
        font-family:"IC-Mono",monospace; font-size:24px; letter-spacing:5px; text-transform:uppercase;
        color:{DIM}; opacity:0; }}
      #root .legenda {{ position:absolute; top:{JY + JH + 34}px; left:{JX}px; width:{JW}px;
        font-family:"IC-Inter",sans-serif; font-size:34px; color:{INK}; opacity:0; }}
    </style>

    <div id="cena-{cid}-fade" class="clip fade" data-start="0" data-duration="{dur}" data-track-index="0">
      <div class="bg"></div>
      <div class="rotulo" id="rot">{rotulo}</div>
      <div class="janela">
        <div class="lupa" id="lupa"><img id="print" src="assets/fontes/{arq}" alt="" /></div>
        <div class="duotone"></div>
        <div class="veu"></div>
      </div>
      {svg_sub}
      <div class="legenda" id="leg">{legenda}</div>
    </div>

    <script>
      (function () {{
        const tl = gsap.timeline({{ paused: true }});
        const DUR = {dur};
        tl.to("#cena-{cid}-fade", {{ opacity: 1, duration: 0.4, ease: "power2.out" }}, 0);
        tl.to("#cena-{cid}-fade", {{ opacity: 0, duration: 0.4, ease: "power2.in" }}, DUR - 0.4);
        tl.to("#rot", {{ opacity: 1, duration: 0.5, ease: "power2.out" }}, 0.25);
        // ken burns lento no print
        tl.fromTo("#lupa", {{ scale: 1.0 }}, {{ scale: 1.06, duration: DUR, ease: "none" }}, 0);
        // sublinhado desenhado no trecho citado
        const p = document.querySelector("#sub path");
        if (p) {{
          const len = p.getTotalLength();
          gsap.set(p, {{ strokeDasharray: len, strokeDashoffset: len }});
          tl.to(p, {{ strokeDashoffset: 0, duration: 0.8, ease: "power2.inOut" }}, 1.5);
        }}
        tl.fromTo("#leg", {{ y: 16 }}, {{ y: 0, opacity: 1, duration: 0.5, ease: "power2.out" }}, 2.1);
        window.__timelines["{cid}"] = tl;
      }})();
    </script>
  </div>
</template>
"""

os.makedirs("compositions/frames", exist_ok=True)
hosts, t, OVER = [], 0.0, 0.3
for i, c in enumerate(CENAS):
    open(f"compositions/frames/{c[0]}.html", "w").write(cena(*c))
    hosts.append(f"""      <div id="el-{c[0]}" class="scene" data-composition-id="{c[0]}"
        data-composition-src="compositions/frames/{c[0]}.html"
        data-start="{t:.2f}" data-duration="{c[7]}" data-track-index="{i % 3}"
        data-width="{W}" data-height="{H}"></div>""")
    t += c[7] - OVER
total = round(t + OVER, 2)

open("index.html", "w").write(f"""<!doctype html>
<html lang="pt-BR">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <title>TRXF11 — B-roll de matérias</title>
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
print(f"{len(CENAS)} cenas · total {total}s")
