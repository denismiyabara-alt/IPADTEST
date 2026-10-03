"""Montagem do projeto HyperFrames autocontido, comum às peças da biblioteca.

O que faz (igual ao grafico_cotacao/gerar.py, sem alterá-lo):
  - copia para assets/ as fontes OFL do estilo (@fontsource), o GSAP e o efeito de pouso;
  - escreve meta.json, entrada.json e assets/CREDITOS.txt;
  - monta o <head> (fontes, cores, filtro boil do Faz a Conta) e o JS comum (fmtBR, timeline, leitura da tela).

As dependências vêm de motion/node_modules (hyperframes, gsap, fontes do IeC) e de
motion/biblioteca/node_modules (fontes do Faz a Conta: Archivo Black e Montserrat).
"""
import json, os, shutil, subprocess

from estilo import ESTILOS, FORMATOS

COMUM = os.path.dirname(os.path.abspath(__file__))
MOTION = os.path.dirname(COMUM)
NODE_MODULES = [os.path.join(MOTION, "node_modules"), os.path.join(MOTION, "biblioteca", "node_modules")]
SFX_DIR = os.path.join(MOTION, "node_modules", "hyperframes", "dist", "skills", "media-use", "audio", "assets", "sfx")
SOM_PADRAO = "impact-bass-1"


def achar(rel):
    for base in NODE_MODULES:
        p = os.path.join(base, rel)
        if os.path.exists(p):
            return p
    return None


def preparar_som(som, assets):
    """-> (nome do arquivo em assets/, duração, crédito) ou (None, 0, ''). Um único som: o do pouso."""
    if not som:
        return None, 0.0, ""
    pedido = som["pouso"]
    if os.path.exists(pedido):
        origem, credito = pedido, f"Efeito de pouso: {os.path.basename(pedido)} (arquivo informado na entrada; confira a licença)."
    elif os.path.exists(os.path.join(SFX_DIR, pedido + ".mp3")):
        origem = os.path.join(SFX_DIR, pedido + ".mp3")
        credito = (f"Efeito de pouso: {pedido}.mp3, biblioteca media-use do HyperFrames "
                   "(node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx/CREDITS.md), "
                   "Pixabay Content License: uso comercial, sem exigência de atribuição.")
    else:
        raise SystemExit(f"efeito de pouso '{pedido}' não encontrado em {SFX_DIR}. Rode: cd motion && npm install")
    nome = "pouso" + os.path.splitext(origem)[1]
    shutil.copy(origem, os.path.join(assets, nome))
    return nome, duracao_audio(origem), credito


def duracao_audio(caminho):
    try:
        out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", caminho],
                             capture_output=True, text=True, check=True).stdout
        return min(float(out), 3.0)
    except Exception:
        return 1.5


def css_fontes(estilo):
    return "".join(
        f"@font-face{{font-family:'{fam}';font-weight:{peso};font-style:normal;font-display:block;"
        f"src:url('assets/fonts/{os.path.basename(arq)}') format('woff2');}}"
        for arq, fam, peso in ESTILOS[estilo]["fontes"].values())


def preparar_assets(d, destino, peca):
    """Copia fontes, GSAP e som; escreve créditos. -> (sfx_nome, sfx_duracao)."""
    assets = os.path.join(destino, "assets")
    os.makedirs(os.path.join(assets, "fonts"), exist_ok=True)
    faltando = []
    for arq, _, _ in ESTILOS[d["estilo"]]["fontes"].values():
        o = achar(arq)
        if o:
            shutil.copy(o, os.path.join(assets, "fonts", os.path.basename(arq)))
        else:
            faltando.append(arq)
    gsap = achar(os.path.join("gsap", "dist", "gsap.min.js"))
    if gsap:
        shutil.copy(gsap, os.path.join(assets, "gsap.min.js"))
    else:
        faltando.append("gsap/dist/gsap.min.js")
    if faltando:
        raise SystemExit(f"faltam dependências: {faltando}. Rode: cd motion && npm install && "
                         "(cd biblioteca && npm install)")
    sfx, sfx_dur, credito = preparar_som(d.get("som"), assets)
    fams = sorted({fam for _, fam, _ in ESTILOS[d["estilo"]]["fontes"].values()})
    open(os.path.join(assets, "CREDITOS.txt"), "w").write(
        f"Fontes: {', '.join(fams)} (SIL Open Font License 1.1), via @fontsource no npm.\n"
        "GSAP 3.14.2 (licença padrão sem custo da GreenSock/Webflow), via npm.\n"
        + (credito + "\n" if credito else "Sem som.\n")
        + f"Dado: {d['fonte']}\n")
    W, H = FORMATOS[d["formato"]]
    json.dump({"id": peca, "name": d["titulo"], "width": W, "height": H},
              open(os.path.join(destino, "meta.json"), "w"), ensure_ascii=False)
    json.dump(d, open(os.path.join(destino, "entrada.json"), "w"), ensure_ascii=False, indent=1)
    return sfx, sfx_dur


def audio_pouso(sfx, sfx_dur, t_pouso):
    if not sfx:
        return ""
    return (f'<audio id="sfx-pouso" src="assets/{sfx}" data-start="{max(0, t_pouso - 0.03):.3f}" '
            f'data-duration="{sfx_dur:.3f}" data-track-index="91" data-volume="0.6"></audio>')


def tipo(estilo, papel, px):
    return ESTILOS[estilo]["tipo"][papel].format(px=px)


def cabeca(d, css_peca):
    """<head> completo: fontes locais, GSAP local, variáveis de cor e o CSS da peça."""
    e = ESTILOS[d["estilo"]]
    W, H = FORMATOS[d["formato"]]
    cores = "".join(f"--{k}:{v};" for k, v in e["cores"].items())
    return f"""<!doctype html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width={W}, height={H}" />
<script src="assets/gsap.min.js"></script>
<style>
  {css_fontes(d['estilo'])}
  :root {{ {cores} }}
  * {{ margin:0; padding:0; box-sizing:border-box; }}
  html, body {{ width:{W}px; height:{H}px; overflow:hidden; background:var(--papel); }}
  #root {{ position:relative; width:{W}px; height:{H}px; overflow:hidden; color:var(--tinta);
           background:var(--papel); font-family:Montserrat, sans-serif; }}
  .cena {{ position:absolute; inset:0; }}
  #marca {{ position:absolute; right:70px; bottom:42px; font:800 30px Montserrat, sans-serif; letter-spacing:.12em; color:var(--cinza); }}
{css_peca}
</style>
</head>
<body>
"""


def filtro_boil(d):
    """Filtro de traço 'fervendo' do Faz a Conta (troca a semente a 8 fps). Vazio no estilo iec."""
    if not ESTILOS[d["estilo"]]["boil"]:
        return ""
    return ('<svg width="0" height="0" style="position:absolute"><filter id="boil">'
            '<feTurbulence id="turb" type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="1"/>'
            '<feDisplacementMap in="SourceGraphic" scale="4"/></filter></svg>')


def js_boil(d):
    if not ESTILOS[d["estilo"]]["boil"]:
        return ""
    n = int(float(d["duracao"]) * 8)
    return f"for (let k = 0; k < {n}; k++) tl.set('#turb', {{attr: {{seed: 1 + (k % 6)}}}}, k / 8);"


def marca(d):
    m = ESTILOS[d["estilo"]]["marca"]
    return f'<div id="marca">{m}</div>' if m else ""


# 1234567.8 -> "1.234.567,8" sem depender do locale do Chrome (igual ao fmt_br)
JS_FMT = r"""
  function fmtBR(v, casas) {
    const neg = v < 0 && Math.abs(v).toFixed(casas) !== (0).toFixed(casas);
    const [i, d] = Math.abs(v).toFixed(casas).split('.');
    return (neg ? '-' : '') + i.replace(/\B(?=(\d{3})+(?!\d))/g, '.') + (d ? ',' + d : '');
  }
"""


def grafico_cotacao():
    """O módulo motion/grafico_cotacao/gerar.py (escala, easing, layout e o próprio gráfico), carregado uma vez
    com nome próprio (as peças da biblioteca também se chamam gerar.py)."""
    import importlib.util, sys
    nome = "grafico_cotacao_gerar"
    if nome not in sys.modules:
        spec = importlib.util.spec_from_file_location(nome, os.path.join(MOTION, "grafico_cotacao", "gerar.py"))
        m = importlib.util.module_from_spec(spec)
        sys.modules[nome] = m
        spec.loader.exec_module(m)
    return sys.modules[nome]


def escrever_tela(destino, tela_js):
    """assets/tela.js: o leitor da tela que o teste usa (comum/quadro.mjs). Fora da timeline: não roda no render."""
    open(os.path.join(destino, "assets", "tela.js"), "w").write(
        "// lido pelo teste (comum/quadro.mjs)\n(() => {\n" + tela_js + "})();\n")
