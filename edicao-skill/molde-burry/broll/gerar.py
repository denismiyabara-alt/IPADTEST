#!/usr/bin/env python3
"""B-roll do "Burry x Barsi" numa peca so (HyperFrames): cartelas no traco do Faz a Conta
(papel, linha fervendo a 8 fps, contagem, barras, carimbo, balao) + prints de manchete/documento
com push-in e grifo. Denis (27/09): traco + sons sem palito, foco nas manchetes, fotos do Burry/Barsi.

Entradas: ../../plano.json (entra/dur por id, ancorado na fala) · cenas.py · ../../prints/prints.json
Saidas:   index.html · janelas.json {id: [ini, dur]} · eventos.json {id: [[t_rel, som, ganho], ...]}
ponytail: tempos do som saem do mesmo python que escreve o JS — sem regex no JS (o sfx.py do
Faz a Conta ficava mudo quando entrava helper novo).
"""
import json, os, html as H

W, HH = 1920, 1080
PAL = dict(bg="#f6f2e8", ink="#1c1a17", red="#d6362b", gray="#79756c", faint="#d9d4c7",
           verde="#2e8b57", cobre="#b8652a", paper="#fffdf7")
from cenas import T as CENAS

plano = json.load(open("../../plano.json"))
PR = {p["id"]: p for p in json.load(open("../../prints/prints.json"))} if os.path.exists("../../prints/prints.json") else {}

# cada id base entra uma vez na peca, com a maior duracao pedida
dur_de = {}
for pid, p in plano.items():
    b = pid.split("@")[0]
    dur_de[b] = max(dur_de.get(b, 0), p["dur"])
ordem = sorted(dur_de, key=lambda b: min(p["entra"] for k, p in plano.items() if k.split("@")[0] == b))

def fotos_img(nome):
    for ext in ("png", "jpg"):
        if os.path.exists(f"assets/foto-{nome}.{ext}"): return f"assets/foto-{nome}.{ext}"
    return None

# ---------------- cenas ----------------
def rotulo(t): return f'<div class="rot">{H.escape(t)}</div>' if t else ""

def c_num(i, T0, D, d, ev):
    cor = d.get("cor", "ink")
    foto = fotos_img(d["foto"]) if d.get("foto") else None
    dx = ' class="com-foto"' if foto else ""
    h = rotulo(d["rot"]) + (f'<img class="foto" id="f{i}" src="{foto}">' if foto else "") + f"""
<div class="mid{" com-foto" if foto else ""}">
  {f'<div class="de" id="de{i}">{H.escape(d["de"])} →</div>' if d.get("de") else ""}
  <div class="big {cor}" id="n{i}">{H.escape(d.get("pre",""))}0{H.escape(d.get("suf",""))}</div>
  <div class="cap" id="c{i}">{H.escape(d["sub"])}</div>
  {f'<div class="pe" id="p{i}">{H.escape(d["pe"])}</div>' if d.get("pe") else ""}
</div>"""
    dc = min(1.5, D * .45)
    a0 = 10 if d.get("desce") else 0
    js = [f"pop('#n{i}', {T0:.3f});",
          f"countTo('#n{i}', {a0}, {d['val']}, {T0+.05:.3f}, {dc:.3f}, {d['dec']}, {json.dumps(d.get('pre',''))}, {json.dumps(d.get('suf',''))});",
          f"tl.from('#c{i}', {{opacity:0, y:24, duration:.4}}, {T0+.5:.3f});"]
    if d.get("de"): js.append(f"tl.from('#de{i}', {{opacity:0, x:-30, duration:.35}}, {T0:.3f});")
    if d.get("pe"): js.append(f"stamp('#p{i}', {T0+min(D-1, 1.8):.3f});"); ev.append((min(D-1, 1.8)+.28, "carimbo", .7))
    if foto:
        js.append(f"tl.from('#f{i}', {{x:-500, rotation:-8, duration:.5, ease:'back.out(1.4)'}}, {T0:.3f});")
        ev.append((0, "whoosh", .28))
    ev.append((0, "pop", .35))
    n = int(8 + 10 * dc)
    for k in range(n):
        u = k / n; ev.append((.05 + dc * (1 - (1 - u) ** 2), f"tique:{2600 + 900*u:.0f}", .16))
    return h, js

def c_barras(i, T0, D, d, ev):
    foto = fotos_img(d["foto"]) if d.get("foto") else None
    mx = max(v for _, v, _, _ in d["linhas"]) if not d.get("base") else max(v for _, v, _, _ in d["linhas"])
    rows = "".join(f"""<div class="row" id="r{i}_{k}"><div class="bl">{H.escape(l)}</div>
  <div class="track"><div class="fill {c}" style="width:{max(v/mx*100, .6):.2f}%"></div></div><div class="bv {c}">{H.escape(t)}</div></div>"""
                   for k, (l, v, t, c) in enumerate(d["linhas"]))
    dx = ' class="com-foto"' if foto else ""
    h = rotulo(d["rot"]) + (f'<img class="foto" id="f{i}" src="{foto}">' if foto else "") + f'<div class="mid{" com-foto" if foto else ""}"><div class="bars">{rows}</div>'
    if d.get("nota"): h += f'<div class="cap" id="no{i}">{H.escape(d["nota"])}</div>'
    h += "</div>"
    if d.get("carimbo"): h += f'<div class="stamp" id="st{i}">{H.escape(d["carimbo"])}</div>'
    js = []
    for k in range(len(d["linhas"])):
        t = T0 + .1 + k * .45
        js.append(f"tl.from('#r{i}_{k}', {{opacity:0, x:-40, duration:.3}}, {t:.3f});"
                  f"tl.from('#r{i}_{k} .fill', {{scaleX:0, transformOrigin:'left', duration:.8, ease:'power2.out'}}, {t+.15:.3f});"
                  f"tl.from('#r{i}_{k} .bv', {{opacity:0, scale:.6, duration:.3, ease:'back.out(2)'}}, {t+.8:.3f});")
        ev.append((.25 + k * .45, "riser", .22)); ev.append((.9 + k * .45, "pop", .25))
    t_fim = .1 + len(d["linhas"]) * .45 + .8
    if d.get("nota"): js.append(f"tl.from('#no{i}', {{opacity:0, y:20, duration:.4}}, {T0+t_fim:.3f});")
    if d.get("carimbo"):
        ts = min(max(1.0, D - 1.2), t_fim + .2)
        js.append(f"stamp('#st{i}', {T0+ts:.3f}); shake({T0+ts+.3:.3f});"); ev.append((ts + .28, "carimbo", .8))
    if foto:
        js.append(f"tl.from('#f{i}', {{x:-500, rotation:-8, duration:.5, ease:'back.out(1.4)'}}, {T0:.3f});"); ev.append((0, "whoosh", .28))
    return h, js

def c_formula(i, T0, D, d, ev):
    partes = "".join(f'<span id="fp{i}_{k}">{H.escape(p)}</span>' for k, p in enumerate(d["partes"]))
    h = rotulo(d["rot"]) + f"""<div class="mid"><div class="formula">{partes}</div>
<div class="slam" id="fr{i}">{H.escape(d["res"])}</div><div class="cap" id="c{i}">{H.escape(d["sub"])}</div></div>"""
    js = []
    for k in range(len(d["partes"])):
        js.append(f"pop('#fp{i}_{k}', {T0 + k*.35:.3f});"); ev.append((k * .35, "click", .5))
    tr = len(d["partes"]) * .35 + .25
    js.append(f"tl.fromTo('#fr{i}', {{scale:2.2, opacity:0}}, {{scale:1, opacity:1, duration:.3, ease:'power4.in'}}, {T0+tr:.3f}); shake({T0+tr+.3:.3f});"
              f"tl.from('#c{i}', {{opacity:0, duration:.4}}, {T0+tr+.5:.3f});")
    ev.append((tr + .28, "impacto", .5))
    return h, js

def c_frase(i, T0, D, d, ev):
    foto = fotos_img(d["foto"]) if d.get("foto") else None
    dx = ' class="com-foto"' if foto else ""
    h = rotulo(d["rot"]) + (f'<img class="foto" id="f{i}" src="{foto}">' if foto else "") + \
        f'<div class="mid{" com-foto" if foto else ""}"><div class="head {d.get("cor","ink")}" id="h{i}">{H.escape(d["l1"])}</div><div class="cap" id="c{i}">{H.escape(d["l2"])}</div></div>'
    js = [f"tl.fromTo('#h{i}', {{scale:2.3, opacity:0}}, {{scale:1, opacity:1, duration:.32, ease:'power4.in'}}, {T0+.08:.3f}); shake({T0+.4:.3f});",
          f"tl.from('#c{i}', {{opacity:0, y:24, duration:.4}}, {T0+.6:.3f});"]
    ev += [(0, "whoosh", .25), (.38, "impacto", .45)]
    if foto:
        js.append(f"tl.from('#f{i}', {{x:-500, rotation:-8, duration:.5, ease:'back.out(1.4)'}}, {T0:.3f});")
    return h, js

def c_quote(i, T0, D, d, ev):
    h = f"""<div class="mid"><div class="card" id="q{i}"><div class="card-t">{H.escape(d["txt"])}</div>
<div class="card-f">{H.escape(d["fonte"])}</div></div><div class="cap" id="c{i}">{H.escape(d.get("trad",""))}</div></div>"""
    js = [f"tl.fromTo('#q{i}', {{y:-60, rotation:-4, opacity:0}}, {{y:0, rotation:-1.5, opacity:1, duration:.5, ease:'back.out(1.8)'}}, {T0:.3f});",
          f"tl.from('#c{i}', {{opacity:0, y:20, duration:.4}}, {T0+.9:.3f});"]
    ev.append((0, "whoosh", .3)); ev.append((.45, "papel", .5))
    return h, js

def c_balao(i, T0, D, d, ev):
    h = f'<div class="mid"><div class="balao" id="b{i}">{H.escape(d["txt"])}</div>' + \
        (f'<div class="cap" id="c{i}" style="margin-top:80px">{H.escape(d["sub"])}</div>' if d.get("sub") else "") + "</div>"
    js = [f"pop('#b{i}', {T0:.3f}); tl.to('#b{i}', {{rotation:1.5, duration:.3, yoyo:true, repeat:3, ease:'sine.inOut'}}, {T0+.5:.3f});"]
    if d.get("sub"): js.append(f"tl.from('#c{i}', {{opacity:0, y:20, duration:.4}}, {T0+min(D*.55, 2.2):.3f});")
    ev.append((0, "pop", .45))
    return h, js

def c_cupom(i, T0, D, d, ev):
    h = f"""<div class="mid"><div class="ticket" id="tk{i}"><div class="tk-l">CUPOM</div><div class="tk-c">{H.escape(d["cod"])}</div></div>
<div class="cap" id="c{i}">{H.escape(d["sub"])}</div></div><div class="stamp" id="st{i}">{H.escape(d["off"])}</div>"""
    js = [f"tl.from('#tk{i}', {{y:-120, rotation:-10, opacity:0, duration:.6, ease:'bounce.out'}}, {T0:.3f});",
          f"stamp('#st{i}', {T0+.8:.3f}); shake({T0+1.1:.3f}); tl.from('#c{i}', {{opacity:0, duration:.4}}, {T0+1.2:.3f});"]
    ev += [(0, "whoosh", .3), (1.08, "carimbo", .8), (1.2, "moeda", .45)]
    return h, js

def c_lista(i, T0, D, d, ev):
    its = d["itens"]
    lis = "".join(f'<li id="li{i}_{k}" class="{"q" if k == 0 and d["rot"].startswith("PERGUNTA") else ""}"><b>{"?" if k == 0 and d["rot"].startswith("PERGUNTA") else "✓"}</b>{H.escape(x)}</li>' for k, x in enumerate(its))
    h = rotulo(d["rot"]) + f'<div class="mid"><ul class="lista">{lis}</ul></div>'
    st = min(.7, max(.35, (D - 1.2) / len(its)))
    js = [f"tl.from('#li{i}_{k}', {{opacity:0, x:-50, duration:.3, ease:'back.out(2)'}}, {T0 + .1 + k*st:.3f});" for k in range(len(its))]
    ev += [(.1 + k * st, "click", .5) for k in range(len(its))]
    return h, js

def c_fluxo(i, T0, D, d, ev):
    cx = []
    for k, (t, s, c) in enumerate(d["caixas"]):
        if k: cx.append(f'<b id="fa{i}_{k}">→</b>')
        cx.append(f'<div class="box {c}" id="fb{i}_{k}"><div>{H.escape(t)}</div><small>{H.escape(s)}</small></div>')
    h = rotulo(d["rot"]) + f'<div class="mid"><div class="fluxo">{"".join(cx)}</div></div>'
    js = []
    for k in range(len(d["caixas"])):
        t = .1 + k * .7
        if k: js.append(f"tl.from('#fa{i}_{k}', {{opacity:0, x:-40, duration:.35}}, {T0+t-.3:.3f});"); ev.append((t - .3, "whoosh-curto", .25))
        js.append(f"pop('#fb{i}_{k}', {T0+t:.3f});"); ev.append((t, "pop", .35))
    return h, js

def c_duas(i, T0, D, d, ev):
    fa = fotos_img(d["fa"]) if d.get("fa") else None
    fb = fotos_img(d["fb"]) if d.get("fb") else None
    col = lambda k, t, s, f, cor: f'<div class="col" id="d{i}_{k}">' + (f'<img class="mini" src="{f}">' if f else "") + \
        f'<div class="head2 {cor}">{H.escape(t)}</div><div class="cap">{H.escape(s)}</div></div>'
    h = rotulo(d["rot"]) + f"""<div class="mid"><div class="duas">{col(0, d["a"], d["asub"], fa, "ink")}<div class="vs" id="vs{i}"></div>{col(1, d["b"], d["bsub"], fb, "red")}</div>
{f'<div class="cap" id="c{i}" style="margin-top:50px">{H.escape(d["rodape"])}</div>' if d.get("rodape") else ""}</div>"""
    tb = min(1.0, D * .3)
    js = [f"pop('#d{i}_0', {T0:.3f});", f"tl.from('#vs{i}', {{scaleY:0, duration:.4}}, {T0+.3:.3f});", f"pop('#d{i}_1', {T0+tb:.3f});"]
    if d.get("rodape"): js.append(f"tl.from('#c{i}', {{opacity:0, y:20, duration:.4}}, {T0+tb+.6:.3f});")
    ev += [(0, "pop", .35), (tb, "pop", .35)]
    return h, js

# ---- print (manchete / documento): push-in calculado + grifo desenhado no trecho citado ----
JW, JH, JX, JY = 1560, 760, 180, 150
def c_print(i, T0, D, p, ev):
    iw, ih = p["largura_px"], p["altura_px"]
    x0, y0, x1, y1 = p["bbox_trecho"]
    s0 = min(JW / iw, JH / ih)
    s1 = min(s0 * 2.4, .86 * JW / max(1, (x1 - x0) * iw))   # linha citada ocupa ~86% da janela
    # ponytail: manchete e titulo inteiro, o zoom so aproxima; tabela da Vale sem zoom (senao some o nome da linha)
    s1 = min(s1, s0 * (1.0 if p["id"] == "d5-vale-ebitda" else 1.35 if p["id"].startswith("m") else 2.4))
    s1 = max(s1, s0)
    def pos(s, cx, cy):
        w, h = iw * s, ih * s
        px = (JW - w) / 2 if w <= JW else min(0, max(JW - w, JW / 2 - cx * w))
        py = (JH - h) / 2 if h <= JH else min(0, max(JH - h, JH / 2 - cy * h))
        return px, py
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    px0, py0 = pos(s0, cx, cy); px1, py1 = pos(s1, cx, cy)
    tz = min(2.0, max(1.0, D * .4))
    h = f"""<div class="fonte" id="pf{i}">{H.escape(p["fonte"])}</div>
<div class="janela" id="pj{i}"><div class="pz" id="pz{i}" style="width:{iw}px;height:{ih}px">
  <img src="assets/prints/{H.escape(p["arquivo"])}" width="{iw}" height="{ih}">
  <div class="grifo" id="pg{i}" style="left:{x0*iw-6:.0f}px;top:{y0*ih-4:.0f}px;width:{(x1-x0)*iw+12:.0f}px;height:{(y1-y0)*ih+8:.0f}px"></div>
  <div class="sub" id="ps{i}" style="left:{x0*iw-6:.0f}px;top:{y1*ih+2:.0f}px;width:{(x1-x0)*iw+12:.0f}px;height:{max(4, (y1-y0)*ih*.12):.0f}px"></div>
</div><div class="moldura"></div></div>
{f'<div class="legenda" id="pl{i}">{H.escape(p["legenda"])}</div>' if p.get("legenda") else ""}"""
    js = [f"tl.set('#pz{i}', {{x:{px0:.1f}, y:{py0:.1f}, scale:{s0:.4f}, transformOrigin:'0 0'}}, {T0:.3f});",
          f"tl.fromTo('#pj{i}', {{y:80, rotation:2, opacity:0}}, {{y:0, rotation:0, opacity:1, duration:.4, ease:'power3.out'}}, {T0:.3f});",
          f"tl.from('#pf{i}', {{opacity:0, y:-20, duration:.35}}, {T0+.1:.3f});",
          f"tl.to('#pz{i}', {{x:{px1:.1f}, y:{py1:.1f}, scale:{s1:.4f}, duration:{tz:.2f}, ease:'power2.inOut'}}, {T0+.35:.3f});",
          f"tl.from('#pg{i}', {{scaleX:0, transformOrigin:'left', duration:.55, ease:'power1.inOut'}}, {T0+.35+tz:.3f});",
          f"tl.from('#ps{i}', {{scaleX:0, transformOrigin:'left', duration:.45, ease:'power1.inOut'}}, {T0+.5+tz:.3f});"]
    if p.get("legenda"): js.append(f"tl.from('#pl{i}', {{opacity:0, y:20, duration:.4}}, {T0+.6:.3f});")
    ev += [(0, "whoosh", .32), (.35 + tz, "marca-texto", .55)]
    return h, js

def c_foto(i, T0, D, p, ev):
    """foto real em tela cheia: zoom lento (Ken Burns) + legenda num papel que treme"""
    x0, y0, x1, y1 = p.get("bbox_trecho") or [.3, .3, .7, .7]
    h = f"""<div class="fotocheia"><img id="fc{i}" src="assets/prints/{H.escape(p["arquivo"])}" style="transform-origin:{(x0+x1)*50:.0f}% {(y0+y1)*50:.0f}%"></div>
<div class="fotoleg" id="fl{i}">{H.escape(p.get("legenda",""))}</div>"""
    js = [f"tl.fromTo('#fc{i}', {{scale:1.0}}, {{scale:1.10, duration:{D:.2f}, ease:'none'}}, {T0:.3f});",
          f"tl.from('#fl{i}', {{x:-80, opacity:0, duration:.4, ease:'back.out(1.6)'}}, {T0+.3:.3f});"]
    ev += [(0, "whoosh", .3), (.3, "papel", .4)]
    return h, js

GER = dict(num=c_num, barras=c_barras, formula=c_formula, frase=c_frase, quote=c_quote, balao=c_balao,
           cupom=c_cupom, lista=c_lista, fluxo=c_fluxo, duas=c_duas)

secs, js, jan, eventos, falta, t = [], [], {}, {}, [], 0.0
for i, b in enumerate(ordem):
    D = dur_de[b]
    ev = []
    if b in PR and (b.startswith("foto-") or "foto" in str(PR[b].get("obs", "")).lower()[:12]):
        h, j = c_foto(i, t, D, PR[b], ev)
    elif b in PR:
        h, j = c_print(i, t, D, PR[b], ev)
    elif b in CENAS:
        tipo, d = CENAS[b]
        h, j = GER[tipo](i, t, D, d, ev)
    else:
        falta.append(b); continue
    secs.append(f'<section class="sc" id="sc{i}">{h}</section>')
    js.append(f"tl.set('#sc{i}', {{autoAlpha:1}}, {t:.3f}); tl.set('#sc{i}', {{autoAlpha:0}}, {t+D:.3f});")
    js += j
    jan[b] = [round(t, 3), D]
    eventos[b] = [[round(a, 3), s, g] for a, s, g in ev if a < D]
    t += D
total = round(t, 3)

CSS = """
:root {--bg:%(bg)s; --ink:%(ink)s; --red:%(red)s; --gray:%(gray)s; --faint:%(faint)s; --verde:%(verde)s; --cobre:%(cobre)s; --paper:%(paper)s;}
* {margin:0; padding:0; box-sizing:border-box;}
html, body {width:1920px; height:1080px; overflow:hidden; background:var(--bg);}
#root {position:relative; width:100%%; height:100%%; overflow:hidden; background:var(--bg); font-family:Montserrat, sans-serif; color:var(--ink);}
#grain {position:absolute; inset:0; opacity:.08; pointer-events:none; z-index:5;}
#cam {position:absolute; inset:0;}
.sc {position:absolute; inset:0; visibility:hidden; opacity:0;}
.rot {position:absolute; top:70px; left:0; width:100%%; text-align:center; font:800 30px Montserrat, sans-serif; letter-spacing:.14em; color:var(--gray);}
.mid {position:absolute; left:120px; right:120px; top:150px; bottom:110px; display:flex; flex-direction:column; align-items:center; justify-content:center; gap:34px;}
.big {font:400 230px 'Archivo Black', sans-serif; line-height:1; font-variant-numeric:tabular-nums; white-space:nowrap;}
.ink {color:var(--ink);} .red {color:var(--red);} .verde {color:var(--verde);} .cobre {color:var(--cobre);} .gray {color:var(--gray);}
.de {font:800 56px Montserrat, sans-serif; color:var(--gray);}
.cap {font-weight:700; font-size:50px; color:var(--gray); text-align:center; max-width:1500px; line-height:1.2;}
.pe {font:400 54px 'Archivo Black', sans-serif; color:var(--red); border:7px solid var(--red); padding:6px 26px; transform:rotate(-4deg);}
.foto {position:absolute; left:30px; bottom:0; height:720px; filter:drop-shadow(0 0 0 var(--paper)) drop-shadow(8px 0 0 var(--paper)) drop-shadow(-8px 0 0 var(--paper)) drop-shadow(0 -8px 0 var(--paper)) drop-shadow(10px 12px 0 rgba(28,26,23,.25));}
.mid.com-foto {left:800px; right:50px;} .com-foto .big {font-size:160px;} .com-foto .head {font-size:150px;} .com-foto .row {grid-template-columns:260px 1fr 300px;} .com-foto .bl {font-size:40px;}
.bars {display:flex; flex-direction:column; gap:44px; width:100%%;}
.row {display:grid; grid-template-columns:430px 1fr 330px; align-items:center; gap:26px;}
.bl {font:800 46px Montserrat, sans-serif; text-align:right;}
.track {height:96px; border:6px solid var(--ink); filter:url(#boil); background:var(--paper);}
.fill {height:100%%; background:var(--gray);} .fill.red {background:var(--red);} .fill.verde {background:var(--verde);} .fill.cobre {background:var(--cobre);} .fill.ink {background:var(--ink);} .fill.gray {background:var(--gray);}
.bv {font:400 60px 'Archivo Black', sans-serif; white-space:nowrap;}
.stamp {position:absolute; right:110px; bottom:90px; font:400 76px 'Archivo Black', sans-serif; color:var(--red); border:9px solid var(--red); padding:6px 30px; transform:rotate(-7deg); background:rgba(246,242,232,.85);}
.formula {display:flex; gap:40px; font:400 120px 'Archivo Black', sans-serif;}
.slam {font:400 150px 'Archivo Black', sans-serif; color:var(--red); white-space:nowrap;}
.head {font:400 190px 'Archivo Black', sans-serif; line-height:1; text-align:center;}
.card {background:var(--paper); border:7px solid var(--ink); padding:56px 70px; max-width:1500px; filter:url(#boil); box-shadow:14px 14px 0 rgba(28,26,23,.18);}
.card-t {font:400 74px 'Archivo Black', sans-serif; line-height:1.15;}
.card-f {font:700 38px Montserrat, sans-serif; color:var(--gray); margin-top:24px;}
.balao {position:relative; background:var(--paper); border:8px solid var(--ink); border-radius:48px; padding:50px 70px; font:800 76px Montserrat, sans-serif; max-width:1400px; text-align:center; filter:url(#boil);}
.balao::after {content:""; position:absolute; left:180px; bottom:-54px; border:26px solid transparent; border-top:30px solid var(--ink);}
.ticket {border:9px dashed var(--ink); padding:40px 90px; background:var(--paper); text-align:center; filter:url(#boil);}
.tk-l {font:800 40px Montserrat, sans-serif; letter-spacing:.3em; color:var(--gray);}
.tk-c {font:400 120px 'Archivo Black', sans-serif; margin-top:10px;}
.lista {list-style:none; display:flex; flex-direction:column; gap:34px;}
.lista li {font:800 70px Montserrat, sans-serif; display:flex; gap:34px; align-items:center;}
.lista li b {font-family:'Archivo Black', sans-serif; width:80px; text-align:center; color:var(--verde);}
.lista li.q {font-family:'Archivo Black', sans-serif; font-weight:400; font-size:84px;} .lista li.q b {color:var(--red);}
.fluxo {display:flex; align-items:center; gap:34px;}
.fluxo .box {border:8px solid var(--ink); padding:40px 34px; background:var(--paper); text-align:center; filter:url(#boil); max-width:520px;}
.fluxo .box div {font:400 48px 'Archivo Black', sans-serif;} .fluxo .box small {display:block; font:700 32px Montserrat, sans-serif; color:var(--gray); margin-top:12px;}
.fluxo .box.red {border-color:var(--red);} .fluxo .box.red div {color:var(--red);} .fluxo .box.gray div {color:var(--cobre);}
.fluxo b {font:400 110px 'Archivo Black', sans-serif;}
.duas {display:flex; align-items:center; gap:90px;}
.duas .col {display:flex; flex-direction:column; align-items:center; gap:18px; width:720px;}
.duas .vs {width:8px; height:420px; background:var(--ink); filter:url(#boil);}
.head2 {font:400 128px 'Archivo Black', sans-serif; line-height:1; text-align:center;}
.mini {height:330px; filter:drop-shadow(6px 0 0 var(--paper)) drop-shadow(-6px 0 0 var(--paper)) drop-shadow(0 -6px 0 var(--paper)) drop-shadow(8px 10px 0 rgba(28,26,23,.25));}
.fonte {position:absolute; top:62px; left:180px; right:180px; font:800 34px Montserrat, sans-serif; letter-spacing:.1em; color:var(--ink);}
.janela {position:absolute; left:%(JX)dpx; top:%(JY)dpx; width:%(JW)dpx; height:%(JH)dpx; overflow:hidden; background:#fff; box-shadow:16px 16px 0 rgba(28,26,23,.18);}
.pz {position:absolute; left:0; top:0;} .pz img {display:block;}
.grifo {position:absolute; background:rgba(255,213,0,.42); mix-blend-mode:multiply;}
.sub {position:absolute; background:var(--red); border-radius:3px;}
.moldura {position:absolute; inset:0; border:8px solid var(--ink); filter:url(#boil); pointer-events:none;}
.fotocheia {position:absolute; inset:0; overflow:hidden;} .fotocheia img {width:100%%; height:100%%; object-fit:cover;}
.fotoleg {position:absolute; left:70px; bottom:70px; max-width:1300px; background:var(--paper); border:7px solid var(--ink); padding:22px 34px; font:800 46px Montserrat, sans-serif; filter:url(#boil); box-shadow:10px 10px 0 rgba(28,26,23,.25);}
.legenda {position:absolute; top:942px; left:180px; right:180px; font:700 42px Montserrat, sans-serif; color:var(--gray); text-align:center;}
""" % dict(PAL, JX=JX, JY=JY, JW=JW, JH=JH)

page = f"""<!doctype html>
<html lang="pt-BR"><head><meta charset="UTF-8" /><meta name="viewport" content="width=1920, height=1080" />
<title>TRXF11 cota nova — B-roll</title>
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>{CSS}</style></head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="1920" data-height="1080" data-duration="{total}">
  <svg width="0" height="0" style="position:absolute">
    <filter id="boil"><feTurbulence id="turb" type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="1"/><feDisplacementMap in="SourceGraphic" scale="4"/></filter>
    <filter id="noise"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="7"/><feColorMatrix type="saturate" values="0"/></filter>
  </svg>
  <svg id="grain" width="1920" height="1080"><rect width="100%" height="100%" filter="url(#noise)"/></svg>
  <div id="cam">
{chr(10).join(secs)}
  </div>
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
  const pop = (sel, t) => tl.fromTo(sel, {{scale:.6, opacity:0}}, {{scale:1, opacity:1, duration:.45, ease:'back.out(2.2)'}}, t);
  const stamp = (sel, t) => tl.fromTo(sel, {{scale:2.2, opacity:0}}, {{scale:1, opacity:1, duration:.3, ease:'power4.in'}}, t);
  const shake = (t) => tl.to('#cam', {{x:9, duration:.05, yoyo:true, repeat:5}}, t);
  function fmtBR(v, casas) {{ const [i, d] = v.toFixed(casas).split('.'); return i.replace(/\\B(?=(\\d{{3}})+(?!\\d))/g, '.') + (d ? ',' + d : ''); }}
  function countTo(sel, a, b, t, d, casas, pre = '', suf = '') {{
    const el = document.querySelector(sel), st = {{v:a}};
    tl.to(st, {{v:b, duration:d, ease:'power2.out', onUpdate: () => {{ el.textContent = pre + fmtBR(st.v, casas) + suf; }} }}, t);
  }}
  for (let k = 0; k < {int(total*8)}; k++) tl.set('#turb', {{attr: {{seed: 1 + (k % 6)}}}}, k / 8);
{chr(10).join(js)}
  window.__timelines["main"] = tl;
</script>
</body></html>
"""
open("index.html", "w").write(page)
json.dump(jan, open("janelas.json", "w"), indent=0)
json.dump(eventos, open("eventos.json", "w"), indent=0, ensure_ascii=False)
print(f"{len(jan)} cenas · {total:.1f}s")
if falta: print("sem cena/print ainda:", ", ".join(falta))
