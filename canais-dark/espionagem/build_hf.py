"""Monta hf-<bloco>/index.html (HyperFrames + GSAP) de um episodio do canal. Identidade em IDENTIDADE.md.
Rodar NA pasta do episodio:
    python3 ../build_hf.py b0                 # usa voz_b0.beats.json (tempos reais da voz)
    python3 ../build_hf.py b0 --sem-voz       # tempos estimados pelo texto (teste de cena sem Mac)
As cenas vem do cenas_hf.py do episodio: CENAS = {"b0": [("trecho da frase", peca), ...]}.
Cada cena comeca na frase que contem o trecho e dura ate a proxima cena. Trecho que sumir do roteiro = erro.
A cartela de FONTE no canto sai sozinha das linhas "* fonte:" do roteiro.md (ids do quadro de fatos).
O credito de imagem sai sozinho da licencas-ep01.csv (coluna credito_na_tela): ninguem digita credito.
"""
import csv, html as H, json, math, os, re, shutil, sys, unicodedata

RAIZ = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, RAIZ)
import roteiro  # noqa: E402

CANAL = os.environ.get("CANAL_NOME", "CODINOME")
COR = dict(carvao="#111111", carvao2="#1b1b1a", arquivo="#ece6d6", ambar="#f2a93b", cinza="#8b877d", linha="#2c2b29")
SIGLAS = {"BAS": "Bascomb, Hunting Eichmann (2009)", "HAR": "Harel, The House on Garibaldi Street (1975)",
          "MAL": "Malkin e Stein, Eichmann in My Hands (1990)", "ARE": "Arendt, Eichmann em Jerusalém (1963)",
          "CIA": "CIA, name file de Eichmann (NARA RG 263)", "NARA": "CIA, name file de Eichmann (NARA RG 263)", "ONU": "ONU, Resolução 138 (1960)",
          "USHMM": "USHMM, gravação do julgamento (1961)", "Aharoni": "Aharoni, Operation Eichmann",
          "Stangneth": "Stangneth, Eichmann Before Jerusalem (2014)", "commons": "documento de arquivo (ver crédito)"}


def _n(s):
    s = unicodedata.normalize("NFD", s.lower())
    return " ".join("".join(c for c in s if unicodedata.category(c) != "Mn" and (c.isalnum() or c.isspace())).split())


# ---------------------------------------------------------------- dados do episodio
def frases_e_fontes(ep):
    """{bloco: [(texto, pausa, [ids de fonte])]} lendo o roteiro.md (o roteiro.py ignora as linhas '*')."""
    r = roteiro.ler(os.path.join(ep, "roteiro.md"))
    quadro = {n["id"]: n["fonte"] for n in r.numeros}
    out, bloco, pend = {}, None, []
    for linha in open(os.path.join(ep, "roteiro.md"), encoding="utf-8"):
        l = linha.strip()
        m = roteiro.RE_BLOCO.match(l)
        if m:
            bloco, pend = m.group(1).lower(), []
            out[bloco] = []
            continue
        if l.startswith("## "):
            bloco = None
        if not bloco or not l:
            continue
        if l.startswith("* fonte:"):
            pend = l.split(":", 1)[1].split()
        elif not l.startswith(("*", ">")):
            t, g = roteiro._frase(l)
            out[bloco].append((t, g, pend))
            pend = []
    for b, fr in out.items():
        assert [(t, g) for t, g, _ in fr] == r.blocos[b], f"{b}: leitura de fontes fora de sincronia"
    return out, quadro


def rotulo_fonte(ids, quadro):
    nomes = []
    for i in ids:
        for sig, nome in SIGLAS.items():
            if re.search(rf"(^|[^\w]){re.escape(sig)}([^\w]|$)", quadro.get(i, "")) and nome not in nomes:
                nomes.append(nome)
    return " · ".join(nomes[:2])


def creditos(ep):
    arq = os.path.join(RAIZ, "licencas-ep01.csv")
    return {row["arquivo"]: row for row in csv.DictReader(open(arq, encoding="utf-8"))} if os.path.exists(arq) else {}


def tempos(bloco, frases, sem_voz):
    if not sem_voz:
        return json.load(open(f"voz_{bloco}.beats.json"))
    cur, fr = 0.35, []
    for t, g, _ in frases:          # estimativa: ~2,4 palavras por segundo (ritmo documental)
        d = max(0.8, len(t.split()) / 2.4)
        fr.append({"texto": t, "ini": round(cur, 3), "fim": round(cur + d, 3)})
        cur += d + g
    return {"dur": round(cur + 0.4, 3), "frases": fr}


# ---------------------------------------------------------------- pecas (cada uma devolve html, js)
# No js: T = inicio da cena (s), D = duracao da cena (s). Pecas REC levam o selo RECONSTITUICAO.
SELO_REC = '<div class="selo">RECONSTITUIÇÃO</div>'
SELO_ESQ = '<div class="selo sub">ESQUEMA · FORA DE ESCALA</div>'


def cartela_ato(titulo, sub=""):
    s = f'<div class="ato-sub">{H.escape(sub)}</div>' if sub else ""
    return (f'<div class="ato"><div class="ato-regua"></div><div class="ato-t">{H.escape(titulo)}</div>{s}</div>',
            "tl.from(S+' .ato-regua', {scaleX:0, transformOrigin:'left', duration:.6, ease:'power3.out'}, T);"
            "tl.from(S+' .ato-t', {opacity:0, y:30, duration:.7, ease:'power3.out'}, T+.2);"
            "tl.from(S+' .ato-sub', {opacity:0, duration:.6}, T+.7);")


def titulo(t, sub):
    return (f'<div class="titulo"><div class="tit-t">{H.escape(t)}</div><div class="tit-s">{H.escape(sub)}</div></div>',
            "tl.from(S+' .tit-t', {opacity:0, letterSpacing:'0.5em', duration:1.4, ease:'power2.out'}, T);"
            "tl.from(S+' .tit-s', {opacity:0, duration:.8}, T+1.0);")


def datilo(texto, rec=False, classe="data"):
    """Texto batido letra a letra em maquina de escrever (data grande, nome, cartela de morte)."""
    letras = "".join(f'<i>{H.escape(c) if c != " " else "&nbsp;"}</i>' for c in texto)
    return (f'<div class="{classe}">{letras}<b class="cursor">_</b></div>' + (SELO_REC if rec else ""),
            f"tl.from(S+' .{classe} i', {{opacity:0, duration:.01, stagger:Math.min(.07, (D*.5)/{len(texto)})}}, T+.2);"
            "tl.to(S+' .cursor', {opacity:0, duration:.01, repeat:Math.floor(D*2), yoyo:true, ease:'steps(1)'}, T);")


def preto(linhas):
    """Cartela de texto sobre preto, sem imagem (usada para a morte: contada, nunca mostrada)."""
    h = "".join(f'<div class="preto-l">{H.escape(l)}</div>' for l in linhas)
    return (f'<div class="preto">{h}</div>', "tl.from(S+' .preto-l', {opacity:0, duration:1.2, stagger:.8}, T+.3);")


def arquivo(img, zoom="in", foco=(0.5, 0.4)):
    """Foto livre com Ken Burns lento. O credito vem da planilha."""
    a, b = (1.0, 1.12) if zoom == "in" else (1.12, 1.0)
    return (f'<div class="foto" data-img="{H.escape(img)}"><div class="foto-in" style="transform-origin:{foco[0]*100:.0f}% {foco[1]*100:.0f}%">'
            f'@@IMG:{img}@@</div></div>@@CRED:{img}@@',
            f"tl.fromTo(S+' .foto-in', {{scale:{a}}}, {{scale:{b}, duration:D, ease:'none'}}, T);"
            "tl.from(S+' .foto', {opacity:0, duration:.8}, T);")


def documento(img, caixa=None, traducao=None):
    """Pagina de documento: entra inclinada, caixa ambar marca o trecho, traducao datilografada ao lado."""
    cx = ""
    if caixa:
        x, y, w, h = caixa
        cx = f'<div class="doc-caixa" style="left:{x*100}%;top:{y*100}%;width:{w*100}%;height:{h*100}%"></div>'
    tr = f'<div class="doc-trad">{H.escape(traducao)}</div>' if traducao else ""
    return (f'<div class="doc"><div class="doc-pag">@@IMG:{img}@@{cx}</div>{tr}</div>@@CRED:{img}@@',
            "tl.fromTo(S+' .doc-pag', {y:80, rotation:-3, opacity:0}, {y:0, rotation:-1, opacity:1, duration:1.0, ease:'power3.out'}, T);"
            "tl.to(S+' .doc-pag', {scale:1.06, duration:D, ease:'none'}, T);"
            "tl.from(S+' .doc-caixa', {scaleX:0, transformOrigin:'left', duration:.5}, T+1.2);"
            "tl.from(S+' .doc-trad', {opacity:0, x:40, duration:.8}, T+1.6);")


def video(arq):
    """Trecho de cinejornal livre, mudo (a voz do canal por cima). CONFERIR NO MAC: <video> no HyperFrames."""
    return (f'<div class="foto">@@VID:{arq}@@</div>@@CRED:{arq}@@', "tl.from(S+' .foto', {opacity:0, duration:.8}, T);")


def _proj(lat, lon, caixa):
    """equiretangular simples: caixa = (lat_max, lat_min, lon_min, lon_max) -> px no quadro 1600x860"""
    la1, la0, lo0, lo1 = caixa
    return 160 + (lon - lo0) / (lo1 - lo0) * 1600, 110 + (la1 - lat) / (la1 - la0) * 860


def rota(pontos, caixa, contador=None, rec=True):
    """Mapa de grade (meridianos e paralelos, sem litoral de terceiros): a rota se desenha ponto a ponto.
    pontos = [(rotulo, lat, lon)]; contador = (inicio, fim, sufixo) acompanha a ponta da linha."""
    la1, la0, lo0, lo1 = caixa
    g = []
    for lat in range(int(math.floor(la0 / 10) * 10), int(la1) + 1, 10):
        _, y = _proj(lat, lo0, caixa)
        if not 110 <= y <= 960:
            continue
        g.append(f'<path d="M160,{y:.0f} H1760"/><text x="168" y="{y-8:.0f}">{abs(lat)}°{"N" if lat > 0 else "S" if lat < 0 else ""}</text>')
    for lon in range(int(math.ceil(lo0 / 10) * 10), int(lo1) + 1, 10):
        x, _ = _proj(la1, lon, caixa)
        g.append(f'<path d="M{x:.0f},110 V970"/>')
    xy = [_proj(la, lo, caixa) for _, la, lo in pontos]
    d = "M" + " L".join(f"{x:.0f},{y:.0f}" for x, y in xy)
    pins = "".join(f'<g class="pino" style="--d:{k}"><circle cx="{x:.0f}" cy="{y:.0f}" r="9"/>'
                   f'<text x="{x+18:.0f}" y="{y+(52 if k == 0 else -14):.0f}">{H.escape(r)}</text></g>' for k, ((r, _, _), (x, y)) in enumerate(zip(pontos, xy)))
    cont = ""
    js = ("tl.from(S+' .grade path', {opacity:0, duration:.6, stagger:.02}, T);"
          "const L=document.querySelector(S+' .rota'), n=L.getTotalLength(); L.style.strokeDasharray=n;"
          "tl.fromTo(L, {strokeDashoffset:n}, {strokeDashoffset:0, duration:Math.max(1.5, D*.7), ease:'power1.inOut'}, T+.6);"
          "tl.from(S+' .pino', {opacity:0, scale:0, transformOrigin:'center', duration:.4, stagger:Math.max(.4, D*.7/" + str(len(pontos)) + ")}, T+.5);")
    if contador:
        a, b, suf = contador
        cont = f'<div class="contador"><span class="cnt">{a}</span> {H.escape(suf)}</div>'
        js += (f"(function(){{const el=document.querySelector(S+' .cnt'), st={{v:{a}}};"
               f"tl.to(st, {{v:{b}, duration:Math.max(1.5, D*.7), ease:'power1.inOut', onUpdate:()=>{{el.textContent=Math.round(st.v);}}}}, T+.6);}})();")
    svg = (f'<svg class="mapa" viewBox="0 0 1920 1080"><g class="grade">{"".join(g)}</g>'
           f'<path class="rota" d="{d}"/>{pins}</svg>')
    return svg + cont + (SELO_REC if rec else "") + SELO_ESQ, js


def mapa_sf(noite=True, carros=False, relogio=None):
    """San Fernando, rua Garibaldi: ESQUEMA (sem geometria real, sem orientacao), so as relacoes do relato:
    estrada com ponto de onibus, rua de terra, casa. Carros e relogio para a noite da captura."""
    c = ('<rect class="carro" x="905" y="520" width="70" height="38" rx="6"/>'
         '<rect class="carro" x="1010" y="610" width="70" height="38" rx="6"/>') if carros else ""
    svg = f"""<svg class="mapa {'noite' if noite else ''}" viewBox="0 0 1920 1080">
  <path class="estrada" d="M120,330 L1800,250"/><text class="rot" x="1220" y="225">estrada · linha de ônibus</text>
  <path class="terra" d="M940,300 L1040,960"/><text class="rot" x="1065" y="900">rua Garibaldi (de terra)</text>
  <g class="ponto"><circle cx="930" cy="292" r="12"/><text class="rot" x="640" y="270">ponto de ônibus</text></g>
  <g class="casa"><rect x="1100" y="760" width="90" height="70"/><path d="M1090,760 L1145,715 L1200,760"/>
  <text class="rot" x="1210" y="800">casa da família</text></g>{c}
  <circle class="vulto" cx="930" cy="292" r="7"/>
</svg>"""
    rel = f'<div class="relogio"><span class="rel-t">{relogio[0]}</span></div>' if relogio else ""
    js = ("tl.from(S+' .estrada', {opacity:0, duration:.8}, T); tl.from(S+' .terra', {opacity:0, duration:.8}, T+.3);"
          "tl.from(S+' .rot', {opacity:0, duration:.5, stagger:.2}, T+.6); tl.from(S+' .casa', {opacity:0, duration:.6}, T+1);")
    if carros:
        js += "tl.from(S+' .carro', {opacity:0, duration:.6, stagger:.3}, T+1.2);"
        js += "tl.fromTo(S+' .vulto', {opacity:0}, {opacity:1, duration:.3}, T+D*.6); tl.to(S+' .vulto', {attr:{cx:975, cy:520}, duration:D*.35, ease:'none'}, T+D*.62);"
    else:
        js += "tl.set(S+' .vulto', {opacity:0}, T);"
    if relogio:
        a, b = relogio
        m0, m1 = int(a[:2]) * 60 + int(a[3:]), int(b[:2]) * 60 + int(b[3:])
        js += (f"(function(){{const el=document.querySelector(S+' .rel-t'), st={{m:{m0}}};"
               f"tl.to(st, {{m:{m1}, duration:Math.max(1, D*.8), ease:'none', onUpdate:()=>{{const m=Math.round(st.m);"
               f"el.textContent=String(Math.floor(m/60)).padStart(2,'0')+':'+String(m%60).padStart(2,'0');}}}}, T+.4);}})();")
    return svg + rel + SELO_REC + SELO_ESQ, js


def linha_tempo(eventos, ativo):
    """eventos = [(ano, rotulo)]; o 'ativo' acende em ambar e a camera desliza ate ele."""
    n = len(eventos)
    itens = "".join(f'<div class="ev {"on" if k == ativo else ""}" style="left:{140 + k * 1640 / max(1, n - 1):.0f}px">'
                    f'<b></b><span class="ev-a">{a}</span><span class="ev-r">{H.escape(r)}</span></div>' for k, (a, r) in enumerate(eventos))
    return (f'<div class="tempo"><div class="eixo"></div>{itens}</div>' + SELO_REC,
            "tl.from(S+' .eixo', {scaleX:0, transformOrigin:'left', duration:1, ease:'power2.out'}, T);"
            "tl.from(S+' .ev', {opacity:0, y:20, duration:.4, stagger:.12}, T+.4);"
            "tl.fromTo(S+' .ev.on b', {scale:1}, {scale:1.8, duration:.5, ease:'back.out(3)'}, T+1.4);")


def silhueta(tipo):
    """Figuras sem rosto (vetor). Nunca rosto de pessoa real gerado."""
    fig = lambda x, s=1: (f'<g transform="translate({x},0) scale({s})"><circle cx="0" cy="-330" r="48"/>'
                          '<path d="M-70,-270 Q0,-300 70,-270 L85,-20 L-85,-20 Z"/></g>')
    if tipo == "banco":
        corpo = fig(820) + fig(1060) + '<rect x="680" y="-60" width="520" height="22"/>'
    elif tipo == "flores":
        corpo = fig(900) + '<g class="buque"><circle cx="990" cy="-250" r="26"/><circle cx="1012" cy="-226" r="22"/><path d="M985,-220 L960,-120"/></g><rect x="1150" y="-420" width="190" height="400"/>'
    else:
        corpo = fig(960)
    return (f'<svg class="silh" viewBox="0 -560 1920 600">{corpo}</svg>' + SELO_REC,
            "tl.from(S+' .silh', {opacity:0, duration:1.2}, T); tl.to(S+' .silh', {scale:1.04, transformOrigin:'50% 100%', duration:D, ease:'none'}, T);")


def placar(sim, nao, abst, cap):
    return (f'<div class="placar"><div><span>{sim}</span><em>a favor</em></div><div><span>{nao}</span><em>contra</em></div>'
            f'<div><span>{abst}</span><em>abstenções</em></div></div><div class="cap">{H.escape(cap)}</div>' + SELO_REC,
            "tl.from(S+' .placar div', {opacity:0, y:30, duration:.5, stagger:.35}, T); tl.from(S+' .cap', {opacity:0, duration:.6}, T+1.4);")


def planta():
    """Casa alugada (esquema): comodos e um ponto ambar no quarto."""
    return ('<svg class="mapa" viewBox="0 0 1920 1080"><g class="planta"><rect x="560" y="260" width="800" height="560"/>'
            '<path d="M960,260 V820 M560,560 H960 M960,620 H1360"/><text class="rot" x="590" y="300">sala</text>'
            '<text class="rot" x="990" y="300">quarto</text><text class="rot" x="590" y="600">cozinha</text>'
            '<text class="rot" x="990" y="660">entrada</text></g><circle class="alvo" cx="1180" cy="430" r="14"/></svg>' + SELO_REC + SELO_ESQ,
            "tl.from(S+' .planta', {opacity:0, duration:1}, T); tl.from(S+' .alvo', {scale:0, transformOrigin:'center', duration:.4}, T+1);"
            "tl.to(S+' .alvo', {opacity:.3, duration:.6, yoyo:true, repeat:Math.max(1, Math.floor(D/1.2)*2-1)}, T+1.4);")


def lista_fontes(itens):
    li = "".join(f"<li>{H.escape(i)}</li>" for i in itens)
    return (f'<div class="fontes"><div class="fontes-h">FONTES</div><ul>{li}</ul></div>',
            "tl.from(S+' .fontes li', {opacity:0, x:-30, duration:.4, stagger:Math.min(.5, D/10)}, T+.3);")


# ---------------------------------------------------------------- montagem
def _img_html(nome, ep, proj, kind="img"):
    src = os.path.join(ep, "imagens", nome)
    if os.path.exists(src):
        os.makedirs(f"{proj}/assets/img", exist_ok=True)
        shutil.copy(src, f"{proj}/assets/img/{nome}")
        if kind == "vid":
            return f'<video src="assets/img/{H.escape(nome)}" muted playsinline></video>'
        return f'<img src="assets/img/{H.escape(nome)}">'
    print(f"  aviso: falta imagens/{nome} (rode baixar_imagens.py); entra um quadro PENDENTE")
    return f'<div class="pendente">IMAGEM PENDENTE<br>{H.escape(nome)}</div>'


def montar(bloco, ep=".", sem_voz=False):
    ep = os.path.abspath(ep)
    sys.path.insert(0, ep)
    import cenas_hf
    todas, quadro = frases_e_fontes(ep)
    frases = todas[bloco]
    meta = tempos(bloco, frases, sem_voz)
    fr, dur = meta["frases"], meta["dur"] + 0.6
    cred = creditos(ep)
    idx_norm = [_n(t) for t, _, _ in frases]
    cenas = []
    for trecho, peca in cenas_hf.CENAS.get(bloco, []):
        k = next((i for i, t in enumerate(idx_norm) if _n(trecho) in t), None)
        if k is None:
            raise SystemExit(f"{bloco}: trecho de cena nao esta no roteiro: {trecho!r}")
        cenas.append((fr[k]["ini"], peca))
    cenas.sort(key=lambda c: c[0])
    proj = os.path.join(ep, f"hf-{bloco}")
    os.makedirs(f"{proj}/assets/fontes", exist_ok=True)
    for f in os.listdir(os.path.join(RAIZ, "fontes")):
        if f.endswith(".ttf"):
            shutil.copy(os.path.join(RAIZ, "fontes", f), f"{proj}/assets/fontes/{f}")
    gsap_local = os.path.join(RAIZ, "vendor", "gsap.min.js")
    if os.path.exists(gsap_local):
        shutil.copy(gsap_local, f"{proj}/assets/gsap.min.js")
    secs, js = [], []
    for j, (t0, (h, code)) in enumerate(cenas):
        t1 = cenas[j + 1][0] if j + 1 < len(cenas) else dur
        h = re.sub(r"@@IMG:(.+?)@@", lambda m: _img_html(m.group(1), ep, proj), h)
        h = re.sub(r"@@VID:(.+?)@@", lambda m: _img_html(m.group(1), ep, proj, "vid"), h)
        h = re.sub(r"@@CRED:(.+?)@@", lambda m: f'<div class="credito">{H.escape(cred.get(m.group(1), {}).get("credito_na_tela", "CRÉDITO: PREENCHER NA PLANILHA"))}</div>', h)
        secs.append(f'<section id="c{j}" class="clip cena" data-start="{t0:.3f}" data-duration="{t1 - t0:.3f}" data-track-index="2">{h}</section>')
        js.append(f"{{ const T={t0:.3f}, D={t1 - t0:.3f}, S='#c{j}'; {code} }}")
    # cartela de fonte no canto: troca quando a frase traz fonte nova
    ult = None
    for k, f in enumerate(fr):
        rot = rotulo_fonte(frases[k][2], quadro)
        if rot and rot != ult:
            fim = next((fr[m]["ini"] for m in range(k + 1, len(fr)) if rotulo_fonte(frases[m][2], quadro) not in ("", rot)), dur)
            secs.append(f'<div class="clip fonte" data-start="{f["ini"]:.3f}" data-duration="{fim - f["ini"]:.3f}" data-track-index="5">FONTE: {H.escape(rot)}</div>')
            ult = rot
    page = TEMPLATE.format(dur=f"{dur:.3f}", cenas="\n".join(secs), js="\n".join(js), canal=H.escape(CANAL),
                           grao=int(dur * 12), gsap=("assets/gsap.min.js" if os.path.exists(gsap_local)
                                                    else "https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"),
                           audio="" if sem_voz else f'<audio src="assets/voz.wav" data-start="0" data-duration="{dur:.3f}" data-track-index="9"></audio>',
                           **COR)
    if not sem_voz:
        shutil.copy(f"voz_{bloco}.wav", f"{proj}/assets/voz.wav")
    open(f"{proj}/index.html", "w", encoding="utf-8").write(page)
    print(f"ok: hf-{bloco}/index.html ({dur:.1f}s, {len(fr)} frases, {len(cenas)} cenas)")
    return proj, cenas, dur


TEMPLATE = r"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<script src="{gsap}"></script>
<style>
  @font-face {{ font-family:'Courier Prime'; src:url(assets/fontes/CourierPrime-Regular.ttf); font-weight:400; }}
  @font-face {{ font-family:'Courier Prime'; src:url(assets/fontes/CourierPrime-Bold.ttf); font-weight:700; }}
  @font-face {{ font-family:'Barlow Condensed'; src:url(assets/fontes/BarlowCondensed-Medium.ttf); font-weight:500; }}
  @font-face {{ font-family:'Barlow Condensed'; src:url(assets/fontes/BarlowCondensed-SemiBold.ttf); font-weight:600; }}
  :root {{ --carvao:{carvao}; --carvao2:{carvao2}; --arquivo:{arquivo}; --ambar:{ambar}; --cinza:{cinza}; --linha:{linha}; }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:1920px; height:1080px; overflow:hidden; background:var(--carvao); }}
  #root {{ position:relative; width:100%; height:100%; overflow:hidden; background:var(--carvao); color:var(--arquivo);
           font-family:'Barlow Condensed', sans-serif; }}
  .cena {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; }}
  #vinheta {{ position:absolute; inset:0; pointer-events:none; background:radial-gradient(ellipse at center, transparent 55%, rgba(0,0,0,.65) 100%); z-index:8; }}
  #grao {{ position:absolute; inset:0; opacity:.09; pointer-events:none; z-index:9; mix-blend-mode:screen; }}
  #wm {{ position:absolute; right:64px; top:48px; font:600 26px 'Barlow Condensed'; letter-spacing:.35em; color:var(--cinza); z-index:10; }}
  .fonte {{ position:absolute; left:64px; bottom:46px; font:400 22px 'Courier Prime'; color:var(--cinza); z-index:10; letter-spacing:.02em; }}
  .credito {{ position:absolute; right:64px; bottom:46px; font:400 20px 'Courier Prime'; color:var(--cinza); max-width:900px; text-align:right; }}
  .selo {{ position:absolute; left:64px; top:44px; font:700 24px 'Courier Prime'; letter-spacing:.18em; color:var(--ambar);
           border:2px solid var(--ambar); padding:6px 16px; }}
  .selo.sub {{ top:94px; font-size:18px; border:none; padding:6px 0 0 0; color:var(--cinza); letter-spacing:.12em; }}
  /* cartelas */
  .ato {{ display:flex; flex-direction:column; gap:22px; width:1400px; }}
  .ato-regua {{ width:220px; height:4px; background:var(--ambar); }}
  .ato-t {{ font:600 120px 'Barlow Condensed'; letter-spacing:.06em; text-transform:uppercase; line-height:1; }}
  .ato-sub {{ font:400 34px 'Courier Prime'; color:var(--cinza); }}
  .titulo {{ text-align:center; }}
  .tit-t {{ font:600 150px 'Barlow Condensed'; letter-spacing:.12em; text-transform:uppercase; }}
  .tit-s {{ font:400 40px 'Courier Prime'; color:var(--ambar); margin-top:18px; letter-spacing:.2em; }}
  .data, .nome {{ font:700 96px 'Courier Prime'; letter-spacing:.04em; color:var(--arquivo); }}
  .data i, .nome i {{ font-style:normal; }} .cursor {{ color:var(--ambar); font-weight:700; }}
  .nome {{ position:absolute; left:120px; bottom:170px; font-size:72px; }}
  .preto {{ display:flex; flex-direction:column; gap:26px; align-items:center; }}
  .preto-l {{ font:400 50px 'Courier Prime'; color:var(--arquivo); letter-spacing:.08em; }}
  /* arquivo e documento */
  .foto {{ position:absolute; inset:0; overflow:hidden; background:#000; }}
  .foto-in {{ position:absolute; inset:0; display:flex; align-items:center; justify-content:center; }}
  .foto img, .foto video {{ max-width:100%; max-height:100%; object-fit:contain; filter:grayscale(1) contrast(1.08) brightness(.92); }}
  .doc {{ display:flex; gap:70px; align-items:center; }}
  .doc-pag {{ position:relative; height:900px; box-shadow:0 30px 80px rgba(0,0,0,.7); }}
  .doc-pag img {{ height:900px; display:block; filter:grayscale(1) contrast(1.15) sepia(.08); }}
  .doc-caixa {{ position:absolute; border:5px solid var(--ambar); box-shadow:0 0 0 2000px rgba(0,0,0,.35); }}
  .doc-trad {{ width:620px; font:400 34px/1.45 'Courier Prime'; color:var(--arquivo); border-left:4px solid var(--ambar); padding-left:30px; }}
  .pendente {{ width:1100px; height:700px; border:3px dashed var(--cinza); display:flex; align-items:center; justify-content:center;
               text-align:center; font:700 40px 'Courier Prime'; color:var(--cinza); line-height:1.5; }}
  /* mapas */
  .mapa {{ position:absolute; inset:0; width:1920px; height:1080px; }}
  .grade path {{ stroke:var(--linha); stroke-width:1.5; fill:none; }} .grade text {{ fill:var(--cinza); font:400 18px 'Courier Prime'; }}
  .rota {{ stroke:var(--ambar); stroke-width:5; fill:none; stroke-linecap:round; filter:drop-shadow(0 0 8px rgba(242,169,59,.6)); }}
  .pino circle {{ fill:var(--carvao); stroke:var(--ambar); stroke-width:4; }}
  .pino text {{ fill:var(--arquivo); font:600 40px 'Barlow Condensed'; letter-spacing:.05em; text-transform:uppercase; }}
  .contador {{ position:absolute; right:64px; bottom:110px; font:700 64px 'Courier Prime'; color:var(--ambar); }}
  .estrada {{ stroke:var(--arquivo); stroke-width:22; fill:none; opacity:.85; }}
  .terra {{ stroke:var(--cinza); stroke-width:16; stroke-dasharray:4 14; stroke-linecap:round; fill:none; }}
  .noite .estrada {{ opacity:.35; }}
  .rot {{ fill:var(--arquivo); font:400 30px 'Courier Prime'; }}
  .ponto circle {{ fill:var(--ambar); }} .casa rect, .casa path {{ fill:none; stroke:var(--arquivo); stroke-width:4; }}
  .carro {{ fill:none; stroke:var(--ambar); stroke-width:4; }} .vulto {{ fill:var(--arquivo); }}
  .relogio {{ position:absolute; right:64px; bottom:110px; font:700 88px 'Courier Prime'; color:var(--ambar); letter-spacing:.05em; }}
  .planta rect, .planta path {{ fill:none; stroke:var(--arquivo); stroke-width:5; }} .alvo {{ fill:var(--ambar); }}
  .tempo {{ position:absolute; left:0; right:0; top:420px; height:300px; }}
  .eixo {{ position:absolute; left:140px; right:140px; top:100px; height:3px; background:var(--cinza); }}
  .ev {{ position:absolute; top:84px; width:0; }}
  .ev b {{ position:absolute; left:-17px; width:34px; height:34px; border-radius:50%; background:var(--carvao); border:4px solid var(--cinza); }}
  .ev.on b {{ border-color:var(--ambar); background:var(--ambar); }}
  .ev-a {{ position:absolute; left:-80px; width:160px; top:-80px; text-align:center; font:700 44px 'Courier Prime'; color:var(--cinza); }}
  .ev.on .ev-a {{ color:var(--ambar); }}
  .ev-r {{ position:absolute; left:-120px; width:240px; top:60px; text-align:center; font:500 30px 'Barlow Condensed'; color:var(--arquivo); text-transform:uppercase; letter-spacing:.06em; }}
  .silh {{ position:absolute; left:0; bottom:120px; width:1920px; height:600px; fill:#2a2926; stroke:var(--cinza); stroke-width:3; }}
  .buque circle {{ fill:var(--ambar); stroke:none; }}
  .placar {{ display:flex; gap:120px; }} .placar div {{ display:flex; flex-direction:column; align-items:center; }}
  .placar span {{ font:700 200px 'Courier Prime'; color:var(--arquivo); line-height:1; }} .placar div:first-child span {{ color:var(--ambar); }}
  .placar em {{ font:500 44px 'Barlow Condensed'; font-style:normal; letter-spacing:.1em; text-transform:uppercase; color:var(--cinza); }}
  .cap {{ position:absolute; bottom:200px; font:400 36px 'Courier Prime'; color:var(--cinza); }}
  .fontes {{ width:1500px; }} .fontes-h {{ font:600 80px 'Barlow Condensed'; letter-spacing:.2em; color:var(--ambar); margin-bottom:30px; }}
  .fontes li {{ list-style:none; font:400 34px/1.6 'Courier Prime'; color:var(--arquivo); }}
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-width="1920" data-height="1080" data-duration="{dur}">
  <svg width="0" height="0" style="position:absolute"><filter id="ruido"><feTurbulence id="turb" type="fractalNoise" baseFrequency="0.85" numOctaves="2" seed="1"/>
    <feColorMatrix type="saturate" values="0"/></filter></svg>
{cenas}
  <div id="vinheta"></div>
  <svg id="grao" width="1920" height="1080"><rect width="100%" height="100%" filter="url(#ruido)"/></svg>
  <div id="wm">{canal}</div>
  {audio}
</div>
<script>
  const tl = gsap.timeline({{ paused: true }});
{js}
  // grao de filme: a semente muda 12 vezes por segundo (deterministico, seek-safe)
  for (let k = 0; k < {grao}; k++) tl.set('#turb', {{attr: {{seed: 1 + (k % 9)}}}}, k / 12);
  window.__timelines["main"] = tl;
</script>
</body>
</html>
"""

if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a:
        sys.exit(__doc__)
    for b in a:
        montar(b, ".", sem_voz="--sem-voz" in sys.argv)
