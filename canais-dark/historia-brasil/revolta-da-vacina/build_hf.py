"""Gera hf-<bloco>/index.html (HyperFrames) a partir de voz_<bloco>.beats.json e do cenas_hf.py.
Uso: python3 build_hf.py b0
Mesmo contrato do canal irmão (fazer.py chama isto e depois `npx hyperframes render`), com a
identidade visual deste canal: papel de arquivo, tinta azul-escura, carimbo vermelho-tijolo,
Alfa Slab One + Courier Prime (OFL, locais via @fontsource) e o palito O Cronista (palito.py).
GSAP e fontes vão copiados para hf-<b>/assets: o render não depende de CDN nem de Google Fonts.
"""
import json
import os
import random
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CANAL = os.path.dirname(HERE)
sys.path.insert(0, CANAL)
import palito as PL  # noqa: E402

PALETA = dict(papel="#ecdfc0", papel2="#f7efdc", tinta="#1e2b4a", carimbo="#a8402b",
              sepia="#7a5c3a", desbotado="#cdb991", sombra="#2a2016")
MARCA = "TEM DOCUMENTO"          # nome de trabalho do canal (IDENTIDADE.md); troque aqui
DOSSIE = "DOSSIÊ Nº 001 · 1904"   # rótulo do episódio no canto
FONTES = {  # arquivo em node_modules -> nome no CSS
    "@fontsource/alfa-slab-one/files/alfa-slab-one-latin-400-normal.woff2": ("Alfa Slab One", 400),
    "@fontsource/courier-prime/files/courier-prime-latin-400-normal.woff2": ("Courier Prime", 400),
    "@fontsource/courier-prime/files/courier-prime-latin-700-normal.woff2": ("Courier Prime", 700),
    "@fontsource/courier-prime/files/courier-prime-latin-ext-400-normal.woff2": ("Courier Prime", 400),
    "@fontsource/courier-prime/files/courier-prime-latin-ext-700-normal.woff2": ("Courier Prime", 700),
    "@fontsource/alfa-slab-one/files/alfa-slab-one-latin-ext-400-normal.woff2": ("Alfa Slab One", 400),
}
GSAP = "gsap/dist/gsap.min.js"

X_E, X_D, X_C = 300, 1620, 960     # onde o palito fica (centro dos pés)
ESCALA = 1.3                        # tamanho do palito na cena
CHAO = 962                          # y do chão


def node_modules():
    """node_modules do canal (npm install em canais-dark/historia-brasil) ou HB_NODE_MODULES."""
    for p in (os.environ.get("HB_NODE_MODULES"), os.path.join(CANAL, "node_modules"), os.path.join(HERE, "node_modules")):
        if p and os.path.exists(os.path.join(p, GSAP)):
            return p
    raise SystemExit("falta node_modules com gsap e @fontsource: rode `npm install` em canais-dark/historia-brasil")


def copiar_assets(proj):
    nm = node_modules()
    os.makedirs(f"{proj}/assets/fonts", exist_ok=True)
    shutil.copy(os.path.join(nm, GSAP), f"{proj}/assets/gsap.min.js")
    css = []
    for rel, (fam, peso) in FONTES.items():
        nome = os.path.basename(rel)
        shutil.copy(os.path.join(nm, rel), f"{proj}/assets/fonts/{nome}")
        css.append(f"@font-face {{ font-family:'{fam}'; font-weight:{peso}; font-style:normal; font-display:block; "
                   f"src:url('assets/fonts/{nome}') format('woff2'); }}")
    return "\n".join(css)


# ---------------------------------------------------------------- direção do palito

def lado_x(lado):
    return {"E": X_E, "D": X_D, "C": X_C}[lado]


def estado(k, palito):
    """(pose, lado) na frase k: herda o último definido até k."""
    chaves = [c for c in sorted(palito) if c <= k]
    return palito[chaves[-1]] if chaves else ("idle", "E")


def reacoes(code, T, pose="idle"):
    r = []
    if "tl.to('#stage'" in code:                         # carimbo: susto
        r.append(PL.pose_js("susto", "T+.43", .12, "power2.out") + PL.boca_js("o", "T+.43")
                 + PL.sobrancelha_js(True, "T+.43")
                 + "tl.to('#pl-pulo', {y:-40, duration:.14, yoyo:true, repeat:1, ease:'power2.out'}, T+.43);"
                 + PL.sobrancelha_js(False, "T+1.1") + PL.pose_js(pose, "T+1.0", .35))
    if "countTo(" in code:                               # olha o número subir
        r.append("tl.to('#pl-cabeca', {rotation:10, svgOrigin:'0 -122', duration:.3}, T+.1);"
                 "tl.to('#pl-cabeca', {rotation:0, svgOrigin:'0 -122', duration:.4}, T+Math.max(.8, D*.8));")
    if not r:                                            # aceno leve
        r.append("tl.to('#pl-cabeca', {rotation:5, svgOrigin:'0 -122', duration:.2, yoyo:true, repeat:1, ease:'sine.inOut'}, T+.1);")
    return "".join(r)


def direcao(fr, cenas, palito, dur, gaps):
    js, ant = [PL.piscar_js(dur), PL.respirar_js(dur)], None
    js.append(PL.pose_js("idle", 0, .01))
    for k, f in enumerate(fr):
        T = f["ini"]
        pose, lado = estado(k, palito)
        x = lado_x(lado)
        if ant is None:
            js.append(f"tl.set('#pl-wrap', {{x:{x - X_E}, scale:{ESCALA}}}, 0);"
                      f"tl.set('#pl-vira', {{scaleX:{-1 if x > X_C else 1}, svgOrigin:'0 0'}}, 0);")
            if k == 0:
                js.append(PL.chapeu_js(.1))       # abre o bloco tirando o chapéu (o gesto do canal)
                T = max(T, 1.75)                  # a 1ª pose entra depois do gesto
        elif ant[1] != lado:                             # anda até o outro lado (com joelho)
            px = lado_x(ant[1])
            d = .5 + abs(x - px) / 1600
            js.append(f"tl.to('#pl-vira', {{scaleX:{1 if x > px else -1}, svgOrigin:'0 0', duration:.12}}, {T:.3f});"
                      f"tl.to('#pl-wrap', {{x:{x - X_E}, duration:{d:.2f}, ease:'none'}}, {T:.3f});"
                      + PL.andar_js(T, d)
                      + f"tl.to('#pl-vira', {{scaleX:{-1 if x > X_C else 1}, svgOrigin:'0 0', duration:.12}}, {T + d:.3f});")
        if ant is None or ant[0] != pose or ant[1] != lado:
            js.append(PL.pose_js(pose, (T + .5 + abs(x - lado_x(ant[1])) / 1600) if ant and ant[1] != lado else T))
        ant = (pose, lado)
        code = cenas.get(k, ("", ""))[1]
        js.append(f"{{ const T={T:.3f}, D={f['fim'] - f['ini']:.3f}; {reacoes(code, T, pose)} }}")
        js.append(PL.falar_js(f["ini"], f["fim"], semente=k, repouso="sorriso" if pose in ("vitoria",) else "fechada"))
        # pausa de punchline (>= 0,75 s): íris de cinema mudo fecha no rosto e reabre na frase seguinte
        if gaps[k] >= .75 and k + 1 < len(fr):
            hx, hy = x, round(CHAO - 278 * ESCALA)
            t0, t1 = f["fim"] + .02, fr[k + 1]["ini"]
            js.append(f"tl.set('#iris', {{opacity:1, '--x':'{hx}px', '--y':'{hy}px'}}, {t0:.3f});"
                      f"tl.fromTo('#iris', {{'--r':'1500px'}}, {{'--r':'210px', duration:.32, ease:'power2.out'}}, {t0:.3f});"
                      f"tl.to('#iris', {{'--r':'1500px', duration:.3, ease:'power2.in'}}, {max(t0 + .35, t1 - .25):.3f});"
                      f"tl.set('#iris', {{opacity:0}}, {max(t0 + .66, t1 + .05):.3f});"
                      + PL.sobrancelha_js(True, t0) + PL.sobrancelha_js(False, t1))
    return js


def tremor_filme(dur, semente=3):
    """Cintilação de projetor (8 por segundo, valores fixos pela semente): leve, nunca pisca."""
    rnd = random.Random(semente)
    return "".join(f"tl.set('#grao', {{opacity:{rnd.uniform(.05, .11):.3f}}}, {k / 8:.3f});" for k in range(int(dur * 8)))


# ---------------------------------------------------------------- montagem

FIM_S = 20.0
TELA_FIM = f"""<div class="fim-marca" id="fimm"><div class="fim-orn">✦ ✦ ✦</div><div class="titulo">FIM</div>
<div class="fim-nome">{MARCA}</div><div class="cap">história do Brasil, com fonte</div></div>
<div class="fim-slots"><div class="slot" id="fims1"></div><div class="slot redondo" id="fims2"></div></div>"""


def registro(bloco):
    import cenas_hf
    r = getattr(cenas_hf, f"cenas_{bloco}")()
    from blocos import BLOCOS as _B
    cauda = r[2] if len(r) > 2 else 0.4
    if bloco == list(_B)[-1]:
        cauda = max(cauda, FIM_S + 2.0)
    return r[0], r[1], cauda


def montar(bloco):
    meta = json.load(open(f"{HERE}/voz_{bloco}.beats.json"))
    cenas, palito, cauda = registro(bloco)
    fr, dur = meta["frases"], meta["dur"] + cauda
    proj = f"{HERE}/hf-{bloco}"
    os.makedirs(f"{proj}/assets", exist_ok=True)
    shutil.copy(f"{HERE}/voz_{bloco}.wav", f"{proj}/assets/voz.wav")
    fontes_css = copiar_assets(proj)
    from blocos import BLOCOS
    ultimo = bloco == list(BLOCOS)[-1]
    gaps = [g for _, g in BLOCOS[bloco]]
    t_fim = fr[-1]["fim"] + 1.5 if ultimo else None
    secs, js = [], []
    for k, f in enumerate(fr):
        fim = fr[k + 1]["ini"] if k + 1 < len(fr) else (t_fim or dur)
        html, code = cenas.get(k, ("", ""))
        lado = estado(k, palito)[1]
        cls = {"E": "", "D": "lado-d", "C": "lado-c"}[lado]
        secs.append(f'<section id="sc{k}" class="clip scene {cls}" data-start="{f["ini"]:.3f}" '
                    f'data-duration="{fim - f["ini"]:.3f}" data-track-index="2">{html}</section>')
        js.append(f"{{ const T={f['ini']:.3f}, D={f['fim'] - f['ini']:.3f}; {code} }}")
    js += direcao(fr, cenas, palito, dur, gaps)
    if t_fim:
        secs.append(f'<section id="scfim" class="clip scene tela-fim" data-start="{t_fim:.3f}" data-duration="{dur - t_fim:.3f}" data-track-index="2">{TELA_FIM}</section>')
        js.append(f"tl.set('#iris', {{opacity:0}}, {t_fim:.3f});"
                  f"tl.to('#pl-wrap', {{x:{X_E - X_E + 60}, scale:{ESCALA + .15}, duration:.6, ease:'power2.inOut'}}, {t_fim:.3f});"
                  f"tl.to('#pl-vira', {{scaleX:1, svgOrigin:'0 0', duration:.2}}, {t_fim:.3f});"
                  + PL.boca_js("sorriso", t_fim) + PL.chapeu_js(t_fim + .6)
                  + f"tl.from('#fimm', {{opacity:0, y:30, duration:.5}}, {t_fim + .2:.3f}); tl.from('.slot', {{opacity:0, duration:.6, stagger:.2}}, {t_fim + .6:.3f});")
    js.insert(0, tremor_filme(dur))
    page = TEMPLATE.format(dur=f"{dur:.3f}", palito=PL.SVG, scenes="\n".join(secs), js="\n".join(js),
                           fontes=fontes_css, marca=MARCA, dossie=DOSSIE, chao=CHAO, pl_top=CHAO - 360, **PALETA)
    open(f"{proj}/index.html", "w", encoding="utf-8").write(page)
    print(f"ok: hf-{bloco}/index.html  ({dur:.1f}s, {len(fr)} frases)")


TEMPLATE = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<script src="assets/gsap.min.js"></script>
<style>
  {fontes}
  :root {{ --papel:{papel}; --papel2:{papel2}; --tinta:{tinta}; --carimbo:{carimbo}; --sepia:{sepia}; --desbotado:{desbotado}; --sombra:{sombra}; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:1920px; height:1080px; overflow:hidden; background:var(--papel); }}
  #root {{ position:relative; width:100%; height:100%; overflow:hidden; color:var(--tinta);
           background: radial-gradient(ellipse at 50% 45%, var(--papel) 55%, #d9c59c 100%); font-family:'Courier Prime', monospace; }}
  #fibra {{ position:absolute; inset:0; opacity:.35; mix-blend-mode:multiply; pointer-events:none; }}
  #dobra {{ position:absolute; top:0; bottom:0; left:640px; width:3px; background:linear-gradient(90deg, rgba(122,92,58,.18), rgba(255,255,255,.25)); }}
  #grao {{ position:absolute; inset:0; opacity:.08; pointer-events:none; mix-blend-mode:multiply; }}
  #chao {{ position:absolute; left:60px; right:60px; top:{chao}px; height:14px; }}
  #wm {{ position:absolute; right:64px; bottom:38px; font:700 28px 'Courier Prime', monospace; letter-spacing:.18em; color:var(--sepia); }}
  #dossie {{ position:absolute; left:64px; top:40px; font:700 24px 'Courier Prime', monospace; letter-spacing:.12em; color:var(--sepia);
             border:3px solid var(--sepia); padding:6px 14px; }}
  #pl-wrap {{ position:absolute; left:130px; top:{pl_top}px; width:340px; height:380px; transform-origin:50% 94.7%; }}
  #stage, #cam {{ position:absolute; inset:0; }}
  #iris {{ position:absolute; inset:0; pointer-events:none; opacity:0; --x:960px; --y:540px; --r:1500px;
           background:radial-gradient(circle at var(--x) var(--y), transparent var(--r), rgba(42,32,22,.94) calc(var(--r) + 3px)); }}
  .scene {{ position:absolute; left:560px; right:110px; top:130px; bottom:170px;
            display:flex; flex-direction:column; align-items:center; justify-content:center; gap:30px; }}
  .scene.lado-d {{ left:110px; right:560px; }}
  .scene.lado-c {{ left:200px; right:200px; bottom:420px; }}
  .titulo {{ font:400 132px 'Alfa Slab One', serif; line-height:1.02; text-align:center; color:var(--tinta); }}
  .titulo.tijolo {{ color:var(--carimbo); }} .titulo.sepia {{ color:var(--sepia); }}
  .cap {{ font:700 46px 'Courier Prime', monospace; color:var(--sepia); text-align:center; max-width:1150px; line-height:1.2; }}
  .carimbo {{ border:12px double var(--carimbo); padding:18px 46px; color:var(--carimbo); transform:rotate(-7deg);
              font:400 104px 'Alfa Slab One', serif; text-align:center; line-height:1.05; opacity:.92;
              -webkit-mask-image:radial-gradient(circle at 30% 40%, #000 60%, rgba(0,0,0,.75) 61%, #000 75%); }}
  .carimbo.peq {{ font-size:70px; }}
  .ficha {{ background:var(--papel2); border:4px solid var(--tinta); padding:30px 46px 34px; max-width:1150px;
            box-shadow:10px 12px 0 rgba(42,32,22,.25); position:relative; }}
  .ficha::before {{ content:""; position:absolute; top:-18px; right:70px; width:34px; height:60px; border:6px solid var(--sepia); border-bottom:none; border-radius:16px 16px 0 0; }}
  .ficha-r {{ font:700 24px 'Courier Prime', monospace; letter-spacing:.3em; color:var(--carimbo); border-bottom:3px dashed var(--desbotado); padding-bottom:10px; margin-bottom:16px; }}
  .ficha-t {{ font:400 60px 'Alfa Slab One', serif; line-height:1.12; }}
  .ficha-n {{ font:700 36px 'Courier Prime', monospace; margin-top:14px; line-height:1.25; }}
  .ficha-f {{ font:400 32px 'Courier Prime', monospace; color:var(--sepia); margin-top:18px; }}
  .ano {{ display:flex; font:400 250px 'Alfa Slab One', serif; line-height:1; letter-spacing:.02em; }}
  .ano.tijolo {{ color:var(--carimbo); }}
  .numero {{ font:400 190px 'Alfa Slab One', serif; line-height:1; white-space:nowrap; font-variant-numeric:tabular-nums; }}
  .numero.tijolo {{ color:var(--carimbo); }}
  .lista {{ list-style:none; display:flex; flex-direction:column; gap:22px; }}
  .lista li {{ font:700 60px 'Courier Prime', monospace; display:flex; gap:26px; align-items:center; }}
  .lista li b {{ font:400 64px 'Alfa Slab One', serif; width:70px; text-align:center; }}
  .lista li.no b {{ color:var(--carimbo); }} .lista li.no {{ color:var(--sepia); text-decoration:line-through; text-decoration-thickness:4px; }}
  .recorte {{ background:#f4ead2; padding:34px 50px 40px; max-width:1100px; box-shadow:8px 10px 0 rgba(42,32,22,.22);
              clip-path:polygon(0 3%, 6% 0, 14% 2%, 25% 0, 37% 2%, 50% 0, 61% 3%, 74% 0, 86% 2%, 100% 0, 99% 30%, 100% 62%, 98% 100%, 85% 97%, 71% 100%, 58% 97%, 44% 100%, 30% 97%, 17% 100%, 5% 97%, 0 100%, 1% 60%); }}
  .rec-v {{ font:700 28px 'Courier Prime', monospace; letter-spacing:.12em; color:var(--sepia); border-bottom:4px double var(--tinta); padding-bottom:10px; margin-bottom:18px; }}
  .rec-m {{ font:400 74px 'Alfa Slab One', serif; line-height:1.05; }}
  .rec-l {{ height:12px; background:var(--desbotado); margin-top:16px; }} .rec-l.curta {{ width:62%; }}
  .pilha {{ display:flex; flex-direction:column; gap:24px; align-items:center; }}
  .recorte.mini {{ padding:20px 40px 26px; min-width:900px; }} .recorte.mini .rec-m {{ font-size:54px; }}
  .lt {{ position:relative; width:1050px; height:190px; }}
  .lt-eixo {{ position:absolute; left:0; right:0; top:60px; height:10px; background:var(--tinta); }}
  .lt-m {{ position:absolute; top:30px; transform:translateX(-50%); display:flex; flex-direction:column; align-items:center; gap:24px; }}
  .lt-m i {{ display:block; width:42px; height:42px; border-radius:50%; background:var(--carimbo); border:6px solid var(--tinta); margin-top:12px; }}
  .lt-m span {{ font:400 72px 'Alfa Slab One', serif; }}
  .calend {{ background:var(--papel2); border:4px solid var(--tinta); padding:24px 30px; box-shadow:8px 10px 0 rgba(42,32,22,.22); }}
  .cal-h {{ font:400 48px 'Alfa Slab One', serif; text-align:center; margin-bottom:16px; }}
  .cal-g {{ display:grid; grid-template-columns:repeat(7, 118px); gap:8px; }}
  .cal-g i {{ font:700 44px 'Courier Prime', monospace; font-style:normal; text-align:center; padding:14px 0; border:3px solid var(--desbotado); }}
  .cal-g i.on {{ background:var(--carimbo); color:var(--papel2); border-color:var(--carimbo); }}
  .duelo {{ display:flex; gap:40px; align-items:center; }}
  .duelo > b {{ font:400 110px 'Alfa Slab One', serif; color:var(--sepia); }}
  .duelo-c {{ background:var(--papel2); border:4px solid var(--tinta); padding:30px 40px; width:470px; text-align:center; }}
  .duelo-c.no {{ border-color:var(--carimbo); }}
  .duelo-t {{ font:400 56px 'Alfa Slab One', serif; }} .duelo-c.no .duelo-t {{ color:var(--carimbo); }}
  .duelo-x {{ font:700 40px 'Courier Prime', monospace; color:var(--sepia); margin-top:12px; }}
  .placa {{ background:var(--papel2); border:8px solid var(--tinta); padding:34px 60px; text-align:center; position:relative; }}
  .placa::before, .placa::after {{ content:""; position:absolute; top:16px; width:18px; height:18px; border-radius:50%; background:var(--tinta); }}
  .placa::before {{ left:16px; }} .placa::after {{ right:16px; }}
  .placa-t {{ font:400 92px 'Alfa Slab One', serif; color:var(--carimbo); }}
  .placa-s {{ font:700 38px 'Courier Prime', monospace; color:var(--sepia); margin-top:10px; }}
  .cardapio {{ background:var(--papel2); border:4px double var(--tinta); border-width:10px; padding:30px 60px; text-align:center; }}
  .card-h {{ font:400 58px 'Alfa Slab One', serif; color:var(--carimbo); margin-bottom:14px; }}
  .cardapio ul {{ list-style:none; font:700 52px 'Courier Prime', monospace; line-height:1.5; }}
  .cardapio li::before {{ content:"· "; color:var(--sepia); }}
  .multidao {{ display:flex; flex-wrap:wrap; gap:6px 22px; justify-content:center; max-width:1100px; }}
  .multidao.fila {{ flex-wrap:nowrap; gap:8px; }}
  .mini {{ width:80px; height:180px; stroke:var(--tinta); }}
  .prop-w {{ display:flex; justify-content:center; }}
  .seringa {{ width:860px; }} .rato {{ width:420px; }} .mosquito {{ width:520px; }} .medalha {{ width:360px; }} .napoleao {{ width:470px; }}
  .ratos {{ display:grid; grid-template-columns:repeat(4, 230px); gap:10px 26px; }}
  .rato-m svg {{ width:230px; }}
  .row {{ display:flex; align-items:center; justify-content:center; gap:60px; }}
  .row > div {{ display:flex; flex-direction:column; align-items:center; gap:24px; }}
  .tela-fim {{ left:120px !important; right:120px !important; flex-direction:row !important; justify-content:space-between !important; }}
  .fim-marca {{ margin-left:440px; display:flex; flex-direction:column; align-items:center; gap:12px; }}
  .fim-orn {{ font:400 40px 'Alfa Slab One', serif; color:var(--carimbo); letter-spacing:.4em; }}
  .fim-marca .titulo {{ font-size:150px; }}
  .fim-nome {{ font:700 54px 'Courier Prime', monospace; letter-spacing:.2em; }}
  .fim-slots {{ display:flex; flex-direction:column; gap:40px; align-items:center; }}
  .slot {{ width:560px; height:315px; border:5px dashed var(--desbotado); }}
  .slot.redondo {{ width:220px; height:220px; border-radius:50%; }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="1920" data-height="1080" data-duration="{dur}">
  <svg width="0" height="0" style="position:absolute">
    <filter id="f-fibra"><feTurbulence type="fractalNoise" baseFrequency="0.012 0.18" numOctaves="3" seed="11"/>
      <feColorMatrix values="0 0 0 0 .48  0 0 0 0 .36  0 0 0 0 .23  0 0 0 .55 0"/></filter>
    <filter id="f-grao"><feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="5"/><feColorMatrix type="saturate" values="0"/></filter>
  </svg>
  <svg id="fibra" width="1920" height="1080"><rect width="100%" height="100%" filter="url(#f-fibra)"/></svg>
  <div id="dobra"></div>
  <div id="cam">
    <svg id="chao" viewBox="0 0 1800 14" preserveAspectRatio="none"><path d="M0,7 C300,3 600,10 900,6 S1500,3 1800,8" stroke="var(--tinta)" stroke-width="5" fill="none"/>
      <path d="M0,13 H1800" stroke="var(--desbotado)" stroke-width="2"/></svg>
    <div id="stage">
{scenes}
    </div>
    <div id="pl-wrap">{palito}</div>
  </div>
  <div id="iris"></div>
  <svg id="grao" width="1920" height="1080"><rect width="100%" height="100%" filter="url(#f-grao)"/></svg>
  <div id="dossie">{dossie}</div>
  <div id="wm">{marca}</div>
  <audio id="voz" src="assets/voz.wav" data-start="0" data-duration="{dur}" data-track-index="9"></audio>
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
  function fmtBR(v, casas) {{
    const [i, d] = v.toFixed(casas).split('.');
    return i.replace(/\B(?=(\d{{3}})+(?!\d))/g, '.') + (d ? ',' + d : '');
  }}
  function countTo(sel, a, b, t, d, casas, pre = '', suf = '') {{
    const el = document.querySelector(sel), st = {{v:a}};
    tl.to(st, {{v:b, duration:d, ease:'power2.out', onUpdate: () => {{ el.textContent = pre + fmtBR(st.v, casas) + suf; }} }}, t);
  }}
{js}
  window.__timelines = window.__timelines || {{}};
  window.__timelines["main"] = tl;
</script>
</body>
</html>
"""

if __name__ == "__main__":
    montar(sys.argv[1] if len(sys.argv) > 1 else "b0")
