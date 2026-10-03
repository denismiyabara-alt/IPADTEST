"""Peças de cena do canal de história (HTML + JS GSAP). Cada peça devolve (html, js); no js,
T = início da frase (s) e D = duração falada, como no formato de cenas do canal irmão.

Linguagem visual própria (IDENTIDADE.md): papel de arquivo, tinta azul-escura, carimbo
vermelho-tijolo. As peças entram como PAPEL: caem com um leve giro e assentam (sem o "pop" elástico),
o carimbo bate com tranco de mesa, e a fonte de cada fato aparece numa ficha datilografada.
"""


def _cap(sid, cap, atraso=".45"):
    if not cap:
        return "", ""
    return (f'<div class="cap" id="{sid}c">{cap}</div>',
            f"tl.from('#{sid}c', {{opacity:0, y:16, duration:.4}}, T+{atraso});")


def papel(sel, t="T", rot=-4):
    """Entrada padrão: a folha cai e assenta."""
    return (f"tl.fromTo('{sel}', {{y:-70, rotation:{rot}, opacity:0}}, "
            f"{{y:0, rotation:0, opacity:1, duration:.5, ease:'power3.out'}}, {t});")


def titulo(txt, cap=None, cor="", sid="x"):
    c, cj = _cap(sid, cap)
    return f'<div class="titulo {cor}" id="{sid}b">{txt}</div>{c}', papel(f"#{sid}b") + cj


def carimbo(txt, cap=None, sid="x", pequeno=False):
    """Carimbo vermelho-tijolo: bate de cima, a mesa treme (tl.to('#stage', {x...}))."""
    c, cj = _cap(sid, cap, ".75")
    js = (f"tl.fromTo('#{sid}b', {{scale:2.2, opacity:0, rotation:-14}}, {{scale:1, opacity:1, rotation:-7, duration:.28, ease:'power4.in'}}, T+.15);"
          f"tl.to('#stage', {{x:7, y:3, duration:.05, yoyo:true, repeat:5}}, T+.43);" + cj)
    return f'<div class="carimbo{" peq" if pequeno else ""}" id="{sid}b"><span>{txt}</span></div>{c}', js


def ficha(titulo_, fonte, sid="x", rotulo="DOCUMENTO", nota=None):
    """Ficha de arquivo: o fato em cima, a nota datilografada e a fonte embaixo (a fonte na tela)."""
    n = f'<div class="ficha-n">{nota}</div>' if nota else ""
    html = (f'<div class="ficha" id="{sid}k"><div class="ficha-r">{rotulo}</div>'
            f'<div class="ficha-t">{titulo_}</div>{n}<div class="ficha-f">fonte: {fonte}</div></div>')
    js = papel(f"#{sid}k", rot=3) + f"tl.from('#{sid}k .ficha-f', {{opacity:0, duration:.3}}, T+.6);"
    return html, js


def ano(sid, valor, cap=None, cor=""):
    """Ano grande, batido na máquina de escrever: um algarismo por vez."""
    dig = "".join(f"<span>{d}</span>" for d in str(valor))
    c, cj = _cap(sid, cap, ".6")
    return (f'<div class="ano {cor}" id="{sid}">{dig}</div>{c}',
            f"tl.from('#{sid} span', {{opacity:0, y:-24, duration:.08, stagger:.11, ease:'steps(2)'}}, T);" + cj)


def contador(sid, a, b, casas=0, pre="", suf="", cap=None, cor="", dur=1.3):
    c, cj = _cap(sid, cap, ".5")
    js = (papel(f"#{sid}w") + f"countTo('#{sid}n', {a}, {b}, T+.1, Math.min({dur}, D), {casas}, '{pre}', '{suf}');" + cj)
    return f'<div class="numero {cor}" id="{sid}w"><span id="{sid}n">{pre}{a}{suf}</span></div>{c}', js


def lista(itens, sid="x"):
    """itens = [(texto, True/False)] -> ✓ em tinta / ✗ em vermelho-tijolo, datilografados um a um."""
    li = "".join(f'<li class="{"ok" if ok else "no"}"><b>{"✓" if ok else "✗"}</b>{t}</li>' for t, ok in itens)
    return (f'<ul class="lista" id="{sid}l">{li}</ul>',
            f"tl.from('#{sid}l li', {{opacity:0, x:-30, duration:.3, stagger:Math.min(.7, D/{len(itens) + 1}), ease:'power2.out'}}, T);")


def recorte(manchete, veiculo, data, sid="x"):
    """Recorte de jornal/revista com borda rasgada."""
    html = (f'<div class="recorte" id="{sid}r"><div class="rec-v">{veiculo} · {data}</div>'
            f'<div class="rec-m">{manchete}</div><div class="rec-l"></div><div class="rec-l"></div><div class="rec-l curta"></div></div>')
    return html, papel(f"#{sid}r", rot=-6)


def recortes(sid, itens):
    """Vários recortes empilhados, um por vez (itens = [manchete, ...])."""
    h = "".join(f'<div class="recorte mini" style="transform:rotate({(-1) ** k * (2 + k)}deg)"><div class="rec-m">{m}</div>'
                f'<div class="rec-l"></div><div class="rec-l curta"></div></div>' for k, m in enumerate(itens))
    return (f'<div class="pilha" id="{sid}">{h}</div>',
            f"tl.from('#{sid} > .recorte', {{y:-80, opacity:0, duration:.4, stagger:Math.min(.8, D/{len(itens) + 1}), ease:'power3.out'}}, T);")


def linha_tempo(sid, anos, cap=None):
    """Eixo com os anos; as marcas acendem da esquerda para a direita."""
    n = len(anos)
    marcas = "".join(f'<div class="lt-m" style="left:{(k / max(1, n - 1)) * 100:.1f}%"><i></i><span>{a}</span></div>'
                     for k, a in enumerate(anos))
    c, cj = _cap(sid, cap, ".9")
    return (f'<div class="lt" id="{sid}"><div class="lt-eixo"></div>{marcas}</div>{c}',
            f"tl.from('#{sid} .lt-eixo', {{scaleX:0, transformOrigin:'left', duration:.7, ease:'power2.inOut'}}, T);"
            f"tl.from('#{sid} .lt-m', {{opacity:0, y:20, duration:.3, stagger:.35}}, T+.3);" + cj)


def calendario(sid, mes, dias, destaque):
    """Folha de calendário com os dias; os de 'destaque' ficam marcados um a um."""
    cel = "".join(f'<i class="{"on" if d in destaque else ""}">{d}</i>' for d in dias)
    return (f'<div class="calend" id="{sid}"><div class="cal-h">{mes}</div><div class="cal-g">{cel}</div></div>',
            papel(f"#{sid}") + f"tl.from('#{sid} i.on', {{backgroundColor:'rgba(0,0,0,0)', color:'var(--tinta)', duration:.15, stagger:Math.min(.25, D/{len(destaque) + 2})}}, T+.4);")


def duelo(sid, esq, dir_, cap=None):
    """Duas colunas: (titulo, texto, ok) de cada lado."""
    def col(t, txt, ok):
        return f'<div class="duelo-c {"ok" if ok else "no"}"><div class="duelo-t">{t}</div><div class="duelo-x">{txt}</div></div>'
    c, cj = _cap(sid, cap, "1.0")
    return (f'<div class="duelo" id="{sid}">{col(*esq)}<b>×</b>{col(*dir_)}</div>{c}',
            f"tl.from('#{sid} .duelo-c', {{y:-60, opacity:0, duration:.45, stagger:Math.min(.9, D/3), ease:'power3.out'}}, T);"
            f"tl.from('#{sid} > b', {{scale:0, duration:.3, ease:'back.out(3)'}}, T+.3);" + cj)


def placa(txt, sub, sid="x"):
    """Placa pregada (anúncio de rua)."""
    return (f'<div class="placa" id="{sid}p"><div class="placa-t">{txt}</div><div class="placa-s">{sub}</div></div>',
            f"tl.fromTo('#{sid}p', {{rotation:-25, y:-200, opacity:0}}, {{rotation:-3, y:0, opacity:1, duration:.6, ease:'bounce.out'}}, T);")


def cardapio(titulo_, itens, sid="x"):
    li = "".join(f"<li>{i}</li>" for i in itens)
    return (f'<div class="cardapio" id="{sid}m"><div class="card-h">{titulo_}</div><ul>{li}</ul></div>',
            papel(f"#{sid}m", rot=2) + f"tl.from('#{sid}m li', {{opacity:0, duration:.2, stagger:Math.min(.5, D/{len(itens) + 1})}}, T+.4);")


# ---------- desenhos (SVG de traço único, tinta) ----------
MINI_CHAPEU = {
    "coco": '<path d="M-11,-104 C-11,-118 11,-118 11,-104 Z M-17,-104 H17" />',
    "cartola": '<path d="M-9,-104 V-124 H9 V-104 Z M-17,-104 H17" />',
    "bone": '<path d="M-12,-104 C-12,-115 12,-115 12,-104 Z M12,-104 H22" />',
    "palheta": '<path d="M-10,-104 V-111 H10 V-104 Z M-19,-104 H19" />',
}


def mini_palito(chapeu="coco", on=False):
    return (f'<svg class="mini {"on" if on else ""}" viewBox="-30 -130 60 135"><g fill="none" stroke-width="6" stroke-linecap="round">'
            f'<circle cx="0" cy="-92" r="12"/>{MINI_CHAPEU[chapeu]}<path d="M0,-80 V-38 M0,-38 L-14,-12 L-12,0 M0,-38 L14,-12 L12,0 M0,-70 L-18,-48 M0,-70 L18,-48"/></g></svg>')


def multidao(sid, n, destaque=0, cap=None, fila=False):
    tipos = list(MINI_CHAPEU)
    p = "".join(mini_palito(tipos[k % len(tipos)], k < destaque) for k in range(n))
    c, cj = _cap(sid, cap, "1.0")
    return (f'<div class="multidao{" fila" if fila else ""}" id="{sid}m">{p}</div>{c}',
            f"tl.from('#{sid}m svg', {{y:30, opacity:0, duration:.25, stagger:.06, ease:'power2.out'}}, T);"
            + (f"tl.to('#{sid}m svg.on', {{stroke:'var(--carimbo)', duration:.2, stagger:.08}}, T+1.0);" if destaque else "") + cj)


SERINGA = ('<svg class="prop seringa" id="{sid}" viewBox="0 0 420 120"><g fill="none" stroke="var(--tinta)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">'
           '<path d="M70,35 H300 V85 H70 Z" fill="var(--papel2)"/><path d="M300,60 H405"/><path d="M70,60 H20 M20,30 V90"/>'
           '<path d="M110,35 V52 M150,35 V52 M190,35 V52 M230,35 V52 M270,35 V52" stroke-width="4"/>'
           '<path d="M80,48 H190 V72 H80 Z" fill="var(--carimbo)" stroke="none" opacity=".75"/></g></svg>')

RATO = ('<svg class="prop rato" viewBox="0 0 220 120"><g fill="none" stroke="var(--tinta)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">'
        '<path d="M30,90 C30,45 120,35 160,70 L190,82 L160,92 C120,100 60,100 30,90 Z" fill="var(--papel2)"/>'
        '<circle cx="150" cy="62" r="11"/><circle cx="172" cy="78" r="3" fill="var(--tinta)"/>'
        '<path d="M30,88 C10,85 5,70 15,58 C25,48 20,35 8,32"/><path d="M80,98 V112 M130,98 V112"/>'
        '<path d="M192,82 L212,76 M192,84 L212,88" stroke-width="3"/></g></svg>')

MOSQUITO = ('<svg class="prop mosquito" viewBox="0 0 260 200"><g fill="none" stroke="var(--tinta)" stroke-width="6" stroke-linecap="round" stroke-linejoin="round">'
            '<ellipse cx="130" cy="110" rx="60" ry="16" fill="var(--papel2)"/><circle cx="198" cy="104" r="13"/><path d="M210,108 L250,124"/>'
            '<path d="M120,96 C90,40 60,40 70,90 M140,96 C170,40 200,40 190,90" stroke-width="4"/>'
            '<path d="M100,124 L80,170 M130,126 L130,175 M160,124 L180,170" stroke-width="4"/>'
            '<path d="M80,110 H170 M95,100 V120 M115,98 V122 M135,98 V122 M155,100 V120" stroke-width="3"/></g></svg>')

MEDALHA = ('<svg class="prop medalha" viewBox="0 0 240 320"><g stroke="var(--tinta)" stroke-width="6" stroke-linejoin="round">'
           '<path d="M70,0 L120,120 L170,0 Z" fill="var(--carimbo)"/><circle cx="120" cy="200" r="90" fill="#c9a24a"/>'
           '<circle cx="120" cy="200" r="66" fill="none" stroke-width="4"/>'
           '<text x="120" y="192" text-anchor="middle" stroke="none" fill="var(--tinta)" font-family="Alfa Slab One" font-size="34">OURO</text>'
           '<text x="120" y="222" text-anchor="middle" stroke="none" fill="var(--tinta)" font-family="Courier Prime" font-weight="700" font-size="21">{l1}</text><text x="120" y="246" text-anchor="middle" stroke="none" fill="var(--tinta)" font-family="Courier Prime" font-weight="700" font-size="21">{l2}</text></g></svg>')


def napoleao(sid, cap=None, medalha=False):
    """Palito-caricatura com bicorne e seringa de espada (a charge de 1904, redesenhada)."""
    med = '<circle cx="14" cy="-70" r="9" fill="#c9a24a" stroke-width="3"/>' if medalha else ""
    svg = (f'<svg class="prop napoleao" id="{sid}s" viewBox="-150 -230 300 300"><g fill="none" stroke="var(--tinta)" stroke-width="7" stroke-linecap="round" stroke-linejoin="round">'
           '<path d="M-70,-168 Q0,-230 70,-168 Q0,-185 -70,-168 Z" fill="var(--tinta)"/><circle cx="0" cy="-140" r="24" fill="var(--papel)"/>'
           '<path d="M-10,-132 C-14,-137 -20,-134 -22,-129 M10,-132 C14,-137 20,-134 22,-129" stroke-width="4"/>'
           '<circle cx="-8" cy="-146" r="3.5" fill="var(--tinta)" stroke="none"/><circle cx="9" cy="-146" r="3.5" fill="var(--tinta)" stroke="none"/>'
           '<path d="M0,-116 V-10 M0,-10 L-30,60 M0,-10 L30,60 M0,-95 L-40,-60 L-12,-40 M0,-95 L50,-120"/>'
           '<path d="M50,-120 L130,-200" stroke-width="5"/><path d="M40,-112 L62,-134 M62,-122 L130,-200" stroke="var(--carimbo)" stroke-width="10"/>'
           f'{med}</g></svg>')
    c, cj = _cap(sid, cap, ".6")
    return svg + c, (f"tl.fromTo('#{sid}s', {{x:-260, opacity:0}}, {{x:0, opacity:1, duration:.6, ease:'power3.out'}}, T);"
                     f"tl.to('#{sid}s', {{rotation:4, transformOrigin:'50% 100%', duration:.3, yoyo:true, repeat:3, ease:'sine.inOut'}}, T+.6);" + cj)


def prop(svg, sid, cap=None, entrada="papel"):
    """Põe um desenho na cena. svg com {sid} ou {legenda} já resolvidos."""
    html = f'<div class="prop-w" id="{sid}w">{svg}</div>'
    c, cj = _cap(sid, cap, ".5")
    js = papel(f"#{sid}w") if entrada == "papel" else f"tl.fromTo('#{sid}w', {{x:300, opacity:0}}, {{x:0, opacity:1, duration:.7, ease:'power2.out'}}, T);"
    return html + c, js + cj


def ratos(sid, n, cap=None):
    """n ratos que vão aparecendo (a 'criação')."""
    r = "".join(f'<div class="rato-m">{RATO}</div>' for _ in range(n))
    c, cj = _cap(sid, cap, "1.0")
    return (f'<div class="ratos" id="{sid}">{r}</div>{c}',
            f"tl.from('#{sid} .rato-m', {{scale:0, opacity:0, duration:.2, stagger:Math.min(.18, (D-.4)/{n}), ease:'back.out(2.5)'}}, T);" + cj)


def junta(*pecas):
    return "".join(h for h, _ in pecas), "".join(j for _, j in pecas)


def lado_a_lado(*pecas):
    h = "".join(f"<div>{p[0]}</div>" for p in pecas)
    return f'<div class="row">{h}</div>', "".join(p[1] for p in pecas)


def no_momento(cena, frac):
    """Atrasa a cena para a hora em que a palavra é dita: T vira T + frac*D."""
    html, js = cena
    return html, f"((T) => {{ {js} }})(T + {frac:.2f}*D);"
