#!/usr/bin/env python3
"""Canal de história: um comando do roteiro ao vídeo final (mesmo motor do canal irmão, adaptado:
voz desenhada em vez de clonada, cenas com a identidade deste canal, render com o HyperFrames local).

    python3 fazer.py <pasta-do-episodio>            # roda o que falta e retoma de onde parou
    python3 fazer.py <pasta> --status               # só mostra o que está feito e o que falta
    python3 fazer.py <pasta> --refazer voz          # força uma etapa (e as seguintes) de novo
    python3 fazer.py <pasta> --novo --modelo revolta-da-vacina   # cria a pasta copiando os scripts do modelo

Etapas, nesta ordem (cada uma só roda se a saída não existe ou está mais velha que a entrada):
    roteiro      roteiro.md -> blocos.py   (trava se algum número do quadro não estiver conferido;
                 só regrava o blocos.py se o conteúdo mudar)
    voz          voz_<b>.wav + voz_<b>.beats.json, bloco a bloco (synth_voz.py: Qwen3-TTS com a
                 voz-mestra SINTÉTICA do canal); refaz só o bloco cujas frases ou pausas mudaram
                 (hash em voz_<b>.hash)                                   [pesada]
    conferencia  conferir.log; trava se alguma linha começar com "!!"  [pesada]
    render       hf-<b>/ -> render_<b>.mp4, bloco a bloco; emenda em <NOME>-video.mp4   [pesada]
    efeitos      sfx_<b>.wav, bloco a bloco
    mix          <NOME>-final.mp4

--refazer fica anotado em .refazer-<etapa> (com os blocos que faltam) até a etapa terminar:
se a rodada parar no meio, a próxima (mesmo sem a flag) termina o que foi pedido.

Mac de 16 GB: só um job pesado por vez (trava compartilhada com o canal irmão, vale entre terminais e
entre canais) e,
antes de cada um, espera ter memória livre (FAZ_MIN_GB, padrão 6 GB).
Log de tudo em <pasta>/fazer.log.
"""
import argparse
import ast
import fcntl
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pronuncia
import roteiro as rot

RAIZ = Path(__file__).resolve().parent
# mesma trava do outro canal de propósito: na mesma máquina, nunca dois jobs pesados ao mesmo tempo
LOCK = Path(os.environ.get("FAZ_LOCK", Path.home() / ".faz-a-conta.lock"))
MIN_GB = float(os.environ.get("FAZ_MIN_GB", "6"))
ESPERA_MAX_S = int(os.environ.get("FAZ_ESPERA_MAX_S", str(2 * 3600)))
HYPERFRAMES = "hyperframes@0.8.78"   # versão fixada no package.json do canal
SCRIPTS_MODELO = ["synth_voz.py", "conferir.py", "build_hf.py", "sfx.py", "mixar.py",
                  "suavizar_bordas.py", "trocar_frase.py"]


class Falhou(Exception):
    pass


# ---------------------------------------------------------------- execução (os testes trocam isto)

def executar(cmd, cwd, log):
    """Roda um comando e manda a saída para o log. Devolve (código, saída)."""
    with open(log, "a", encoding="utf-8") as f:
        f.write(f"\n$ {' '.join(map(str, cmd))}\n")
        p = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        f.write(p.stdout)
    return p.returncode, p.stdout


def memoria_livre_gb():
    """macOS: páginas livres + inativas + especulativas do vm_stat. Linux: MemAvailable."""
    try:
        out = subprocess.run(["vm_stat"], capture_output=True, text=True, check=True).stdout
        pagina = int(re.search(r"page size of (\d+)", out).group(1))
        paginas = sum(int(re.search(rf"{k}:\s+(\d+)", out).group(1)) for k in ("Pages free", "Pages inactive", "Pages speculative"))
        return paginas * pagina / 1024 ** 3
    except (OSError, subprocess.CalledProcessError, AttributeError):
        pass
    try:
        for linha in Path("/proc/meminfo").read_text().splitlines():
            if linha.startswith("MemAvailable:"):
                return int(linha.split()[1]) / 1024 ** 2
    except OSError:
        pass
    return float("inf")


class JobPesado:
    """Context manager: trava global (um pesado por vez) + espera memória livre."""

    def __init__(self, nome, log, memoria=None, dormir=None, agora=None):
        self.nome, self.log = nome, log
        self.memoria = memoria or (lambda: memoria_livre_gb())
        self.dormir = dormir or (lambda s: time.sleep(s))
        self.agora = agora or (lambda: time.time())

    def __enter__(self):
        LOCK.parent.mkdir(parents=True, exist_ok=True)
        self.fh = open(LOCK, "w")
        inicio = self.agora()
        while True:
            try:
                fcntl.flock(self.fh, fcntl.LOCK_EX | fcntl.LOCK_NB)
                break
            except BlockingIOError:
                if self.agora() - inicio > ESPERA_MAX_S:
                    self.fh.close()
                    raise Falhou(f"{self.nome}: outro job pesado ocupou a máquina por mais de {ESPERA_MAX_S // 60} min")
                anotar(self.log, f"{self.nome}: esperando outro job pesado terminar")
                self.dormir(30)
        while (livre := self.memoria()) < MIN_GB:
            if self.agora() - inicio > ESPERA_MAX_S:
                fcntl.flock(self.fh, fcntl.LOCK_UN)
                self.fh.close()
                raise Falhou(f"{self.nome}: só {livre:.1f} GB livres (mínimo {MIN_GB} GB). Feche apps pesados e rode de novo.")
            anotar(self.log, f"{self.nome}: {livre:.1f} GB livres, esperando {MIN_GB} GB")
            self.dormir(30)
        return self

    def __exit__(self, *a):
        fcntl.flock(self.fh, fcntl.LOCK_UN)
        self.fh.close()


def anotar(log, msg):
    linha = f"[{time.strftime('%H:%M:%S')}] {msg}"
    print(linha, flush=True)
    with open(log, "a", encoding="utf-8") as f:
        f.write(linha + "\n")


# ---------------------------------------------------------------- etapas

def mais_novo(saida, *entradas):
    """True se a saída existe e não é mais velha que nenhuma entrada existente."""
    if not saida.exists():
        return False
    t = saida.stat().st_mtime
    return all(t >= e.stat().st_mtime for e in entradas if e.exists())


def blocos_de(pasta):
    return rot.ler(pasta / "roteiro.md").ordem


def forcado(forcar, b):
    """forcar é True (todos os blocos), False/vazio (nenhum) ou o conjunto de blocos a refazer."""
    return forcar is True or (bool(forcar) and b in forcar)


def aceitas(pasta):
    """Pares (frase, ouvido) que um humano ouviu e aceitou, em <pasta>/conferir_aceitas.txt:
    uma linha por frase, `frase exata <TAB> ouvido exato <TAB> quem e quando`. O aceite vale só
    para AQUELE ouvido: se a voz for refeita e o ASR ouvir outra coisa, a frase volta a travar."""
    arq = pasta / "conferir_aceitas.txt" if pasta else None
    if not arq or not arq.exists():
        return set()
    out = set()
    for l in arq.read_text(encoding="utf-8").splitlines():
        partes = l.split("\t")
        if len(partes) >= 2 and not l.lstrip().startswith("#"):
            out.add((partes[0].strip(), partes[1].strip()))
    return out


def reprovadas(texto, pasta=None):
    """Linhas do conferir.py reprovadas: só as que COMEÇAM com '!!' ('Olha só!!' no meio não conta).
    Com a pasta, tira as que um humano aceitou (conferir_aceitas.txt), conferindo o ouvido inteiro
    no ouvido_<b>.json que o conferir.py grava."""
    ruins = [l for l in texto.splitlines() if l.lstrip().startswith("!!")]
    ok = aceitas(pasta)
    if not ok:
        return ruins
    ouvidos = []
    for arq in sorted(pasta.glob("ouvido_*.json")):
        try:
            ouvidos += json.loads(arq.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            pass
    aceito_prefixo = [f["texto"][:50] for f in ouvidos if (f["texto"], f["ouvido"]) in ok]
    # a linha do log traz '!! [0.89] <texto[:50]>  -> ...'
    return [l for l in ruins if not any(p and p in l for p in aceito_prefixo)]


def hash_bloco(frases, mapa_pronuncia=None):
    """Hash das frases e pausas de um bloco: é isso que decide se a voz do bloco precisa ser refeita.
    Frase que o dicionário de pronúncia muda entra com o texto da voz também: mudou o pronuncia.txt,
    só os blocos que têm a palavra são refeitos (os outros mantêm o hash de antes)."""
    mapa = pronuncia.carregar() if mapa_pronuncia is None else mapa_pronuncia
    linhas = []
    for t, g in frases:
        voz = pronuncia.aplicar(t, mapa)
        linhas.append([t, round(g, 2)] if voz == t else [t, round(g, 2), voz])
    dados = json.dumps(linhas, ensure_ascii=False)
    return hashlib.sha256(dados.encode("utf-8")).hexdigest()


# ---- pedido de --refazer persistido: .refazer-<etapa> guarda os blocos que ainda faltam

def marca_refazer(pasta, etapa):
    return pasta / f".refazer-{etapa}"


def ler_refazer(pasta, etapa):
    """Blocos pendentes de um --refazer anterior (conjunto), ou False se não há pedido."""
    m = marca_refazer(pasta, etapa)
    if not m.exists():
        return False
    try:
        return set(json.loads(m.read_text(encoding="utf-8")))
    except (ValueError, TypeError):
        return True  # marcador ilegível: refaz a etapa inteira (falha fechada)


def gravar_refazer(pasta, etapa, blocos):
    m = marca_refazer(pasta, etapa)
    tmp = m.with_name(m.name + ".tmp")
    tmp.write_text(json.dumps(sorted(blocos)), encoding="utf-8")
    os.replace(tmp, m)


def bloco_refeito(pasta, etapa, b):
    """Tira um bloco já refeito do pedido de --refazer (se houver)."""
    pend = ler_refazer(pasta, etapa)
    if isinstance(pend, set) and b in pend:
        gravar_refazer(pasta, etapa, pend - {b})


def nome_video(pasta):
    return pasta.resolve().name.upper()


def mesmos_blocos(texto_py, r):
    """True se o BLOCOS do blocos.py (texto) tem exatamente as frases e pausas do roteiro."""
    try:
        arvore = ast.parse(texto_py)
        blocos = next(ast.literal_eval(n.value) for n in arvore.body
                      if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "BLOCOS" for t in n.targets))
        norm = lambda d: {b: [(t, round(float(g), 2)) for t, g in fr] for b, fr in d.items()}
        return norm(blocos) == norm(r.blocos)
    except (SyntaxError, ValueError, StopIteration, TypeError, AttributeError):
        return False


def et_roteiro(pasta, log, forcar=False):
    md, py = pasta / "roteiro.md", pasta / "blocos.py"
    r = rot.ler(md)
    pendentes = [n for n in r.numeros if n["status"] not in rot.STATUS_OK]
    if pendentes:
        raise Falhou("roteiro: números sem conferência no quadro: " + ", ".join(f"{n['id']} ({n['status']})" for n in pendentes))
    avisos = rot.validar(r)
    for a in avisos:
        anotar(log, f"roteiro: aviso: {a}")
    novo = rot.para_blocos_py(r)
    # só regrava se o conteúdo mudou: regravar à toa muda o mtime e dispara o resto
    if py.exists():
        atual = py.read_text(encoding="utf-8")
        if atual == novo:
            return "já feito"
        if "gerado de roteiro.md por fazer.py" not in atual.split("\n", 1)[0] and mesmos_blocos(atual, r):
            # blocos.py escrito à mão (episódio antigo) com as mesmas frases e pausas:
            # regravar mudaria o mtime e a voz inteira seria refeita (e sobrescrita) à toa
            return "já feito (blocos.py antigo, mesmas frases e pausas do roteiro.md)"
        shutil.copy(py, py.with_suffix(".py.antes"))
    py.write_text(novo, encoding="utf-8")
    return f"blocos.py gerado ({len(r.ordem)} blocos)"


def voz_bate(beats, frases):
    """O beats.json gravado é destas frases e pausas? True/False; None se ele não guarda o texto."""
    try:
        fr = json.loads(beats.read_text(encoding="utf-8"))["frases"]
        if not fr or any("texto" not in f for f in fr):
            return None
    except (OSError, ValueError, KeyError, TypeError):
        return None
    if [f["texto"] for f in fr] != [t for t, _ in frases]:
        return False
    # pausa gravada = pausa do roteiro; o reespacar.py pode ter esticado as de punch (>= 0,6 s) em até 0,8 s
    def pausa_ok(k):
        gravada, pedida = fr[k + 1]["ini"] - fr[k]["fim"], frases[k][1]
        return pedida - .02 <= gravada <= pedida + (.82 if pedida >= .6 else .02)
    return all(pausa_ok(k) for k in range(len(fr) - 1))


VOZ_MESTRA = RAIZ / "voz" / "voz-mestra.wav"   # SINTÉTICA (VoiceDesign), ver VOZ.md


def ref_voz(pasta):
    """A voz-mestra do canal (modo padrão). No modo design (HB_MODO=design) não há referência:
    devolve o caminho da descrição. None se faltar o que o modo precisa."""
    if os.environ.get("HB_MODO", "mestra") == "design":
        d = RAIZ / "voz" / "descricao.txt"
        return d if d.exists() else None
    p = Path(os.environ.get("HB_VOZ_MESTRA", VOZ_MESTRA))
    return p if p.exists() else None


def et_voz(pasta, log, forcar=False):
    """Voz bloco a bloco. Um bloco só é refeito se o hash das suas frases+pausas mudou (voz_<b>.hash),
    se falta alguma saída ou se foi pedido com --refazer. Mudar Notas ou outro bloco não mexe nele."""
    r, feitos = rot.ler(pasta / "roteiro.md"), []
    for b, frases in r.blocos.items():
        wav, beats, arq_hash = pasta / f"voz_{b}.wav", pasta / f"voz_{b}.beats.json", pasta / f"voz_{b}.hash"
        h = hash_bloco(frases)
        if not forcado(forcar, b) and wav.exists() and beats.exists():
            if arq_hash.exists() and arq_hash.read_text(encoding="utf-8").strip() == h:
                continue
            if not arq_hash.exists():
                # episódio de antes do hash: se a voz gravada é a destas frases e pausas, só anota o hash.
                # Confere pelo texto do beats.json (o trocar_frase.py mexe no blocos.py depois da voz,
                # então o mtime sozinho mandaria refazer blocos que estão certos); sem texto, vale o mtime.
                bate = voz_bate(beats, frases)
                # voz de antes do dicionário de pronúncia: se o bloco tem palavra do pronuncia.txt,
                # a voz gravada falou a grafia antiga e precisa ser refeita
                muda_voz = any(pronuncia.aplicar(t) != t for t, _ in frases)
                if not muda_voz and (bate or (bate is None and mais_novo(wav, pasta / "blocos.py"))):
                    arq_hash.write_text(h, encoding="utf-8")
                    continue
        if ref_voz(pasta) is None:
            raise Falhou(f"voz {b}: falta a voz-mestra ({VOZ_MESTRA}). Gere com voz/desenhar_voz.py "
                         f"(passo 2 do COMO-RODAR.md)")
        arq_hash.unlink(missing_ok=True)  # se a voz falhar no meio, o bloco continua pendente
        with JobPesado(f"voz {b}", log):
            cod, _ = executar([sys.executable, "synth_voz.py", b], pasta, log)
        if cod != 0 or not wav.exists():
            raise Falhou(f"voz {b}: falhou (veja fazer.log)")
        arq_hash.write_text(h, encoding="utf-8")
        bloco_refeito(pasta, "voz", b)
        feitos.append(b)
    return f"voz de {', '.join(feitos)}" if feitos else "já feito"


def conferir_quebrou(cod, out):
    """O conferir.py sai com 1 quando REPROVA frase (linhas '!!'), e isso não é quebra: as
    reprovadas seguem para o reprovadas(), que aplica o aceite humano. Quebra é traceback,
    outro código de saída, ou saída sem nenhum bloco conferido ('=== b...')."""
    if cod == 0:
        return False
    if cod != 1 or "Traceback (most recent call last)" in out:
        return True
    return not (re.search(r"^=== ", out, re.M) and reprovadas(out))


def et_conferencia(pasta, log, forcar=False):
    saida = pasta / "conferir.log"
    vozes = [pasta / f"voz_{b}.wav" for b in blocos_de(pasta)]
    if not forcar and mais_novo(saida, *vozes) and not reprovadas(saida.read_text(encoding="utf-8"), pasta):
        return "já feito"
    with JobPesado("conferência", log):
        cod, out = executar([sys.executable, "conferir.py", *blocos_de(pasta)], pasta, log)
    if conferir_quebrou(cod, out):
        # conferir.py quebrou (traceback etc.): nada de conferir.log, senão a próxima rodada acha que passou
        saida.unlink(missing_ok=True)
        raise Falhou("conferência: o conferir.py falhou (veja fazer.log)")
    tmp = saida.with_name(saida.name + ".tmp")
    tmp.write_text(out, encoding="utf-8")
    os.replace(tmp, saida)
    ruins = reprovadas(out, pasta)
    if ruins:
        raise Falhou(f"conferência: {len(ruins)} frase(s) reprovada(s). Refaça com trocar_frase.py ou "
                     f"'fazer.py {pasta.name} --refazer voz' e rode de novo:\n  " + "\n  ".join(ruins[:5]))
    return "todas as frases aprovadas"


def blocos_sem_cenas(pasta, blocos):
    """Blocos que não têm cenas_<b> no cenas_hf.py. Lê por AST (não executa nada): função
    `def cenas_b0()` ou atribuição `cenas_b1 = ...`, como no piloto."""
    try:
        arvore = ast.parse((pasta / "cenas_hf.py").read_text(encoding="utf-8"))
    except SyntaxError as e:
        raise Falhou(f"render: cenas_hf.py com erro de sintaxe na linha {e.lineno}")
    nomes = {n.name for n in arvore.body if isinstance(n, ast.FunctionDef)}
    nomes |= {t.id for n in arvore.body if isinstance(n, ast.Assign) for t in n.targets if isinstance(t, ast.Name)}
    return [b for b in blocos if f"cenas_{b}" not in nomes]


def et_render(pasta, log, forcar=False):
    blocos, feitos = blocos_de(pasta), []
    if not (pasta / "cenas_hf.py").exists():
        raise Falhou("render: falta cenas_hf.py (a direção de cena de cada bloco é feita à mão)")
    sem = blocos_sem_cenas(pasta, blocos)
    if sem:
        raise Falhou(f"render: o cenas_hf.py não tem cena para {', '.join(sem)} (falta def cenas_<bloco>())")
    hf_bin = RAIZ / "node_modules" / ".bin" / "hyperframes"
    if not hf_bin.exists():
        raise Falhou("render: falta o HyperFrames local. Rode `npm install` em " + str(RAIZ))
    for b in blocos:
        mp4 = pasta / f"render_{b}.mp4"
        if not forcado(forcar, b) and mais_novo(mp4, pasta / f"voz_{b}.beats.json", pasta / "cenas_hf.py"):
            continue
        with JobPesado(f"render {b}", log):
            cod, _ = executar([sys.executable, "build_hf.py", b], pasta, log)
            hf = pasta / f"hf-{b}"
            if cod == 0:
                cod, _ = executar([str(hf_bin), "render", "-o", f"../render_{b}.mp4"], hf, log)
        if cod != 0 or not mp4.exists():
            raise Falhou(f"render {b}: falhou (veja fazer.log)")
        bloco_refeito(pasta, "render", b)
        feitos.append(b)
    video = pasta / f"{nome_video(pasta)}-video.mp4"
    if feitos or forcar or not mais_novo(video, *[pasta / f"render_{b}.mp4" for b in blocos]):
        (pasta / "concat.txt").write_text("".join(f"file 'render_{b}.mp4'\n" for b in blocos))
        cod, _ = executar(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "concat.txt", "-c", "copy", video.name], pasta, log)
        if cod != 0 or not video.exists():
            raise Falhou("render: não consegui emendar os blocos (ffmpeg)")
        return f"render de {', '.join(feitos) or 'nenhum bloco novo'}; {video.name} emendado"
    return "já feito"


def et_efeitos(pasta, log, forcar=False):
    faltam = [b for b in blocos_de(pasta)
              if forcado(forcar, b) or not mais_novo(pasta / f"sfx_{b}.wav", pasta / f"render_{b}.mp4", pasta / f"voz_{b}.beats.json")]
    if not faltam:
        return "já feito"
    cod, _ = executar([sys.executable, "sfx.py", *faltam], pasta, log)
    if cod != 0 or not all((pasta / f"sfx_{b}.wav").exists() for b in faltam):
        raise Falhou("efeitos: sfx.py falhou (veja fazer.log)")
    return f"efeitos de {', '.join(faltam)}"


def et_mix(pasta, log, forcar=False):
    final = pasta / f"{nome_video(pasta)}-final.mp4"
    entradas = [pasta / f"{nome_video(pasta)}-video.mp4"] + [pasta / f"sfx_{b}.wav" for b in blocos_de(pasta)]
    if not forcar and mais_novo(final, *entradas):
        return "já feito"
    trilha = [str(p.name) for p in sorted(pasta.glob("trilha*.mp3"))[:1]]
    cod, _ = executar([sys.executable, "mixar.py", *trilha], pasta, log)
    if cod != 0 or not final.exists():
        raise Falhou("mix: mixar.py falhou (veja fazer.log)")
    return f"{final.name} pronto"


ETAPAS = [("roteiro", et_roteiro), ("voz", et_voz), ("conferencia", et_conferencia),
          ("render", et_render), ("efeitos", et_efeitos), ("mix", et_mix)]


def rodar(pasta, refazer=None):
    pasta = Path(pasta)
    log = pasta / "fazer.log"
    if not (pasta / "roteiro.md").exists():
        raise Falhou(f"{pasta}/roteiro.md não existe (formato em FORMATO-EPISODIO.md)")
    faltando = [s for s in SCRIPTS_MODELO[:5] if not (pasta / s).exists()]
    if faltando:
        raise Falhou(f"faltam scripts na pasta: {', '.join(faltando)} (use --novo --modelo <pasta>)")
    nomes = [n for n, _ in ETAPAS]
    if refazer and refazer not in nomes:
        raise Falhou(f"etapa desconhecida: {refazer} (use uma de: {', '.join(nomes)})")
    if refazer:
        # o pedido fica gravado (etapa pedida e as seguintes, com todos os blocos) e só some quando
        # cada etapa termina: se esta rodada parar no meio, a próxima termina o que foi pedido
        blocos = blocos_de(pasta)
        for nome in nomes[nomes.index(refazer):]:
            gravar_refazer(pasta, nome, blocos)
    anotar(log, f"=== {pasta.name}: começando")
    for nome, fn in ETAPAS:
        pend = ler_refazer(pasta, nome)
        anotar(log, f"{nome}: {fn(pasta, log, forcar=pend)}")
        marca_refazer(pasta, nome).unlink(missing_ok=True)
    anotar(log, f"=== {pasta.name}: pronto")


def cenas_status(pasta, blocos):
    if not (pasta / "cenas_hf.py").exists():
        return "não (o render vai parar)"
    try:
        sem = blocos_sem_cenas(pasta, blocos)
    except Falhou as e:
        return str(e)
    return f"{len(blocos) - len(sem)}/{len(blocos)} blocos" + (f" (faltam {', '.join(sem)})" if sem else "")


def status(pasta):
    pasta = Path(pasta)
    r = rot.ler(pasta / "roteiro.md")
    bl = r.ordem
    def tem(padrao):
        return sum((pasta / padrao.format(b)).exists() for b in bl)
    nome = nome_video(pasta)
    linhas = [f"{pasta.name}: {len(bl)} blocos",
              f"  números conferidos: {sum(n['status'] in rot.STATUS_OK for n in r.numeros)}/{len(r.numeros)}",
              f"  blocos.py: {'sim' if (pasta / 'blocos.py').exists() else 'não'}",
              f"  voz: {tem('voz_{}.wav')}/{len(bl)}",
              f"  cenas_hf.py: {cenas_status(pasta, bl)}",
              f"  conferência: {'ok' if (pasta / 'conferir.log').exists() and not reprovadas((pasta / 'conferir.log').read_text(encoding='utf-8'), pasta) else 'pendente'}",
              f"  render: {tem('render_{}.mp4')}/{len(bl)} · emendado: {'sim' if (pasta / f'{nome}-video.mp4').exists() else 'não'}",
              f"  efeitos: {tem('sfx_{}.wav')}/{len(bl)}",
              f"  final: {'sim' if (pasta / f'{nome}-final.mp4').exists() else 'não'}"]
    pedidos = [n for n, _ in ETAPAS if marca_refazer(pasta, n).exists()]
    if pedidos:
        linhas.append(f"  --refazer pendente: {', '.join(pedidos)}")
    return "\n".join(linhas)


def novo(pasta, modelo):
    pasta, modelo = Path(pasta), RAIZ / modelo
    pasta.mkdir(parents=True, exist_ok=True)
    for s in SCRIPTS_MODELO:
        if (modelo / s).exists() and not (pasta / s).exists():
            shutil.copy(modelo / s, pasta / s)
    if not (pasta / "roteiro.md").exists():
        shutil.copy(RAIZ / "modelo-roteiro.md", pasta / "roteiro.md")
    falta = "" if (pasta / "cenas_hf.py").exists() else " Falta: cenas_hf.py (direção de cena)."
    return f"{pasta}: scripts copiados de {modelo.name}.{falta}"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Canal de história: roteiro → vídeo final, retomando de onde parou.")
    ap.add_argument("pasta")
    ap.add_argument("--status", action="store_true")
    ap.add_argument("--refazer", metavar="ETAPA")
    ap.add_argument("--novo", action="store_true")
    ap.add_argument("--modelo", default="revolta-da-vacina")
    a = ap.parse_args(argv)
    try:
        if a.novo:
            print(novo(a.pasta, a.modelo))
        elif a.status:
            print(status(a.pasta))
        else:
            rodar(a.pasta, a.refazer)
        return 0
    except Falhou as e:
        print(f"PAROU: {e}", file=sys.stderr)
        if Path(a.pasta).exists():
            with open(Path(a.pasta) / "fazer.log", "a", encoding="utf-8") as f:
                f.write(f"PAROU: {e}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
