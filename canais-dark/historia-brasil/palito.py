"""O Cronista: o palito do canal de história (SVG + GSAP), com cotovelo e joelho.

Diferente do palito do canal irmão de propósito (ver IDENTIDADE.md):
  - cabeça REDONDA e pequena (o outro tem cabeça retangular de cupom com serrilha);
  - chapéu-coco, bigode de guidão e gravata-borboleta (o outro não tem acessório);
  - membros com DOIS segmentos (braço/antebraço, coxa/canela), traço fino de tinta azul-escura;
  - corpo mais alto e esguio (cabeça ≈ 1/7 da altura), sem o filtro de traço tremido.

Esqueleto (coordenadas locais, origem no quadril, y para baixo):
  quadril (0,0) ── tronco até o pescoço (0,-120) ── cabeça centrada em (0,-150), r = 24
  ombros (0,-108): braço 55 px até o cotovelo, antebraço 50 px até a mão
  coxa 65 px até o joelho (0,65), canela 65 px até o pé (0,130); os pés apontam para a frente (perfil), o joelho dobra para trás
Cada osso é um <g> que gira em torno da sua articulação (svgOrigin fixo por osso), relativo ao pai.
Uma pose é só um dicionário de ângulos (graus; positivo = horário, e braço caído = 0).
Tudo sai numa timeline GSAP pausada (o HyperFrames busca quadro a quadro): sem Math.random,
sem repeat infinito; o "aleatório" (piscar, boca) sai daqui com semente fixa.
"""
import random

OSSOS = {  # id do grupo -> origem da rotação (svgOrigin, no sistema do SVG)
    "pl-tronco": "0 0",
    "pl-cabeca": "0 -122",
    "pl-chapeu": "0 -168", "pl-chapeu-r": "0 -168",
    "pl-bracoE": "0 -108", "pl-anteE": "0 -53",
    "pl-bracoD": "0 -108", "pl-anteD": "0 -53",
    "pl-coxaE": "0 0", "pl-canelaE": "0 65",
    "pl-coxaD": "0 0", "pl-canelaD": "0 65",
}

SVG = """
<svg id="palito" viewBox="-170 -230 340 380" width="340" height="380">
 <g id="pl-vira"><g id="pl-pulo"><g id="pl-resp" fill="none" stroke="var(--tinta)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">
  <g id="pl-coxaE"><path d="M0,0 L0,65"/><g id="pl-canelaE"><path d="M0,65 L0,130 L15,131"/></g></g>
  <g id="pl-coxaD"><path d="M0,0 L0,65"/><g id="pl-canelaD"><path d="M0,65 L0,130 L15,131"/></g></g>
  <g id="pl-tronco">
   <path d="M0,0 L0,-122"/>
   <path d="M-11,-114 L11,-104 L11,-114 L-11,-104 Z" fill="var(--carimbo)" stroke="var(--carimbo)" stroke-width="3"/>
   <g id="pl-bracoE"><path d="M0,-108 L0,-53"/><g id="pl-anteE"><path d="M0,-53 L0,-3"/><circle cx="0" cy="1" r="5" fill="var(--tinta)" stroke="none"/></g></g>
   <g id="pl-bracoD"><path d="M0,-108 L0,-53"/><g id="pl-anteD"><path d="M0,-53 L0,-3"/><circle cx="0" cy="1" r="5" fill="var(--tinta)" stroke="none"/></g></g>
   <g id="pl-cabeca">
    <circle cx="0" cy="-148" r="24" fill="var(--papel)"/>
    <g id="pl-olhos" fill="var(--tinta)" stroke="none"><circle cx="-8" cy="-154" r="3.6"/><circle cx="9" cy="-154" r="3.6"/></g>
    <g id="pl-sobr" stroke-width="3"><path d="M-13,-162 L-4,-162"/><path d="M4,-162 L13,-162"/></g>
    <path id="pl-bigode" d="M0,-143 C-5,-146 -12,-145 -15,-141 C-17,-138 -15,-135 -12,-137 M0,-143 C5,-146 12,-145 15,-141 C17,-138 15,-135 12,-137" stroke-width="3"/>
    <g stroke-width="3.5">
     <path class="pl-boca" id="pb-fechada" d="M-5,-133 L5,-133"/>
     <ellipse class="pl-boca" id="pb-aberta" cx="0" cy="-132" rx="4.5" ry="4" fill="var(--tinta)" opacity="0"/>
     <path class="pl-boca" id="pb-sorriso" d="M-7,-135 Q0,-128 7,-135" opacity="0"/>
     <circle class="pl-boca" id="pb-o" cx="0" cy="-131" r="6" opacity="0"/>
    </g>
    <g id="pl-chapeu"><g id="pl-chapeu-r" fill="var(--tinta)" stroke="none">
     <path d="M-21,-168 C-21,-196 21,-196 21,-168 Z"/>
     <path d="M-33,-168 Q0,-176 33,-168 Q0,-161 -33,-168 Z"/>
     <path d="M-21,-172 L21,-172" stroke="var(--carimbo)" stroke-width="4"/>
    </g></g>
   </g>
  </g>
 </g></g></g>
</svg>"""

# braço caído = 0; E = lado esquerdo da tela (positivo afasta do corpo), D = direito (negativo afasta)
POSES = {
    "idle":    dict(bracoE=14, anteE=-10, bracoD=-14, anteD=10, coxaE=7, canelaE=2, coxaD=-7, canelaD=2, tronco=0, cabeca=0),
    "apontar": dict(bracoE=14, anteE=-8, bracoD=-92, anteD=-6, coxaE=9, canelaE=2, coxaD=-9, canelaD=2, tronco=-3, cabeca=-4),
    "shrug":   dict(bracoE=58, anteE=-105, bracoD=-58, anteD=105, coxaE=7, canelaE=2, coxaD=-7, canelaD=2, tronco=0, cabeca=8),
    "pensar":  dict(bracoE=28, anteE=-70, bracoD=-25, anteD=150, coxaE=7, canelaE=2, coxaD=-7, canelaD=2, tronco=2, cabeca=6),
    "maos":    dict(bracoE=42, anteE=-38, bracoD=-42, anteD=38, coxaE=8, canelaE=2, coxaD=-8, canelaD=2, tronco=0, cabeca=0),
    "susto":   dict(bracoE=150, anteE=25, bracoD=-150, anteD=-25, coxaE=14, canelaE=2, coxaD=-14, canelaD=2, tronco=-4, cabeca=-6),
    "vitoria": dict(bracoE=165, anteE=-10, bracoD=-165, anteD=10, coxaE=10, canelaE=2, coxaD=-10, canelaD=2, tronco=0, cabeca=-4),
    "serio":   dict(bracoE=8, anteE=-4, bracoD=-8, anteD=4, coxaE=5, canelaE=2, coxaD=-5, canelaD=2, tronco=4, cabeca=10),
}
# limites por articulação (o teste confere que nenhuma pose passa deles: joelho não dobra pra frente etc.)
LIMITES = dict(bracoE=(-30, 180), bracoD=(-180, 30), anteE=(-160, 60), anteD=(-60, 160),
               coxaE=(-40, 60), coxaD=(-60, 40), canelaE=(-5, 70), canelaD=(-5, 70),
               tronco=(-25, 25), cabeca=(-30, 30))


def _t(t):
    """Instante em JS: número (s) ou expressão ('T+.4')."""
    return t if isinstance(t, str) else f"{t:.3f}"


def _osso(nome):
    return "pl-" + nome


def pose_js(pose, t, dur=.35, ease="back.out(1.6)"):
    """Leva todas as articulações para a pose, a partir do instante t (s)."""
    out = []
    for nome, ang in POSES[pose].items():
        o = _osso(nome)
        out.append(f"tl.to('#{o}', {{rotation:{ang}, svgOrigin:'{OSSOS[o]}', duration:{dur}, ease:'{ease}'}}, {_t(t)});")
    return "".join(out)


def andar_js(t, d):
    """Ciclo de andar com joelho: coxas alternam ±22°, a canela de trás dobra, quadril sobe e desce 6 px.
    Número de passos finito (calculado de d); termina na pose neutra das pernas."""
    passos = max(2, int(round(d / .32)))
    p = d / passos
    out = []
    for k in range(passos):
        s = 1 if k % 2 == 0 else -1
        tk = t + k * p
        out.append(f"tl.to('#pl-coxaE', {{rotation:{22 * s}, svgOrigin:'0 0', duration:{p:.3f}, ease:'sine.inOut'}}, {tk:.3f});"
                   f"tl.to('#pl-coxaD', {{rotation:{-22 * s}, svgOrigin:'0 0', duration:{p:.3f}, ease:'sine.inOut'}}, {tk:.3f});"
                   f"tl.to('#pl-canelaE', {{rotation:{30 if s > 0 else 3}, svgOrigin:'0 65', duration:{p:.3f}}}, {tk:.3f});"
                   f"tl.to('#pl-canelaD', {{rotation:{30 if s < 0 else 3}, svgOrigin:'0 65', duration:{p:.3f}}}, {tk:.3f});"
                   f"tl.to('#pl-pulo', {{y:-6, duration:{p / 2:.3f}, yoyo:true, repeat:1, ease:'sine.inOut'}}, {tk:.3f});")
    return "".join(out)


def boca_js(nome, t):
    return "".join(f"tl.set('#pb-{n}', {{opacity:{1 if n == nome else 0}}}, {_t(t)});"
                   for n in ("fechada", "aberta", "sorriso", "o"))


def falar_js(ini, fim, semente=0, repouso="fechada"):
    """Boca abre e fecha durante a fala (~6 vezes por segundo, ritmo irregular de semente fixa)."""
    rnd = random.Random(semente)
    out, t, aberta = [], ini + .03, False
    while t < fim - .08:
        aberta = not aberta
        out.append(boca_js("aberta" if aberta else "fechada", t))
        t += rnd.uniform(.11, .2)
    out.append(boca_js(repouso, fim))
    return "".join(out)


def piscar_js(dur, semente=1):
    rnd = random.Random(semente)
    out, t = [], 1.1
    while t < dur - .3:
        out.append(f"tl.to('#pl-olhos', {{scaleY:.1, svgOrigin:'0 -154', duration:.06, yoyo:true, repeat:1}}, {t:.2f});")
        t += rnd.uniform(2.6, 4.4)
    return "".join(out)


def respirar_js(dur):
    rep = max(1, int(dur / 1.3) // 2 * 2 - 1)     # repeat finito e ímpar: termina onde começou
    return f"tl.to('#pl-resp', {{scaleY:1.025, svgOrigin:'0 0', duration:1.3, yoyo:true, repeat:{rep}, ease:'sine.inOut'}}, 0);"


def chapeu_js(t):
    """O gesto do canal: tira o chapéu e põe de volta (abre e fecha o episódio)."""
    return (pose_js("idle", t, .3)
            + f"tl.to('#pl-bracoD', {{rotation:-165, svgOrigin:'0 -108', duration:.35, ease:'power2.out'}}, {t:.3f});"
            + f"tl.to('#pl-anteD', {{rotation:-40, svgOrigin:'0 -53', duration:.35}}, {t:.3f});"
            + f"tl.to('#pl-chapeu', {{x:0, y:-34, duration:.35, ease:'power2.out'}}, {t + .25:.3f});"
            + f"tl.to('#pl-chapeu-r', {{rotation:-18, svgOrigin:'0 -168', duration:.35, ease:'power2.out'}}, {t + .25:.3f});"
            + f"tl.to('#pl-chapeu', {{x:0, y:0, duration:.4, ease:'bounce.out'}}, {t + 1.1:.3f});"
            + f"tl.to('#pl-chapeu-r', {{rotation:0, svgOrigin:'0 -168', duration:.3}}, {t + 1.1:.3f});"
            + pose_js("idle", t + 1.2, .4))


def sobrancelha_js(cima, t):
    return f"tl.to('#pl-sobr', {{y:{-5 if cima else 0}, duration:.15}}, {_t(t)});"
