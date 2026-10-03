"""Testes mínimos do piloto (sem voz e sem render de verdade; rodam em segundos):

    cd canais-dark/historia-brasil && python3 -m pytest -q tests

- o roteiro lê, passa nas regras de voz e o portão de números aceita como o Whisper escreve cada número;
- a trava do fazer.py: não grava voz com fato "CONFERIR NO MAC"; com tudo conferido, gera o blocos.py;
- as cenas montam: toda cena aponta para frase que existe, ids únicos, poses dentro dos limites,
  todo número na tela está no quadro, e o build_hf.py gera um index.html com JS válido;
- nenhuma menção ao dono do canal, à empresa dele nem ao canal irmão na tela ou no texto;
- o palito é outro (não reaproveita o desenho do canal irmão) e o synth não clona ninguém.
"""
import html as html_mod
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

CANAL = Path(__file__).resolve().parents[1]
EP = CANAL / "revolta-da-vacina"
sys.path.insert(0, str(CANAL))
import fazer  # noqa: E402
import palito  # noqa: E402
import roteiro as rot  # noqa: E402

RE_NUM = re.compile(r"\d{1,3}(?:\.\d{3})+(?:,\d+)?|\d+(?:,\d+)?")
RE_COUNT = re.compile(r"countTo\('[^']+', ([-\d.]+), ([-\d.]+), (.+?), (\d+), '([^']*)', '([^']*)'\)")
PROIBIDO_TELA = [r"D[e]nis", r"Miy[a]bara", r"Inv[e]stir e Co", r"\bI[e]C\b", r"Faz a Conta", r"faz-a-conta",
                 r"\bPT\b", r"\bPL\b", r"\bMDB\b", r"\bPSDB\b", r"\bPSOL\b", r"partido", r"Lula", r"Bolsonaro",
                 r"Collor", r"covid", r"Covid", r"invista", r"investimento"]


def ler():
    return rot.ler(EP / "roteiro.md")


def cenas_mod(pasta=EP):
    spec = importlib.util.spec_from_file_location("cenas_ep", pasta / "cenas_hf.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def synth():
    ns = {"__file__": str(EP / "synth_voz.py")}
    exec((EP / "synth_voz.py").read_text(encoding="utf-8").split("def gerar")[0], ns)
    return ns


# ---------------------------------------------------------------- roteiro e portão

def test_roteiro_le_e_so_avisa_dos_fatos_pendentes():
    r = ler()
    assert len(r.blocos) == 8
    avisos = rot.validar(r)
    assert all("conferir no mac" in a for a in avisos), avisos   # nenhum número em algarismo na fala
    assert all(n["fonte"] for n in r.numeros)


def test_duracao_e_tamanho_do_roteiro():
    r = ler()
    frases = [f for b in r.blocos.values() for f in b]
    palavras = sum(len(t.split()) for t, _ in frases)
    seg = sum(len(t) * 0.067 + g for t, g in frases) + 0.35 * len(r.blocos) + 22   # régua do canal irmão
    assert 750 <= palavras <= 1200, palavras
    assert 5 * 60 <= seg <= 8 * 60, seg


def test_pendentes_tem_url_e_estao_marcados():
    pend = [n for n in ler().numeros if n["status"] not in rot.STATUS_OK]
    assert {n["id"] for n in pend} <= {"ratos-compra", "lei-1261", "atestado"}
    for n in pend:
        assert n["status"] == "conferir no mac" and "http" in n["fonte"]


UNI = {"um": 1, "uma": 1, "dois": 2, "duas": 2, "três": 3, "quatro": 4, "cinco": 5, "seis": 6, "sete": 7, "oito": 8,
       "nove": 9, "dez": 10, "onze": 11, "doze": 12, "treze": 13, "catorze": 14, "quatorze": 14, "quinze": 15,
       "dezesseis": 16, "dezessete": 17, "dezoito": 18, "dezenove": 19, "vinte": 20, "trinta": 30, "quarenta": 40,
       "cinquenta": 50, "sessenta": 60, "setenta": 70, "oitenta": 80, "noventa": 90, "cem": 100, "cento": 100,
       "duzentos": 200, "trezentos": 300, "quatrocentos": 400, "quinhentos": 500, "seiscentos": 600,
       "setecentos": 700, "oitocentos": 800, "novecentos": 900, "novecentas": 900, "mil": 1000}


def como_whisper(frase):
    """Imita o Whisper: número por extenso vira algarismo ('mil novecentos e quatro' -> '1904';
    'dez e dezesseis' -> '10 e 16'; o 'um/uma' artigo também vira 1, como às vezes acontece)."""
    ws, out, k = re.findall(r"\w+|[^\w\s]", frase.lower()), [], 0
    while k < len(ws):
        if ws[k] in UNI:
            total, atual, ultimo = 0, 0, None
            while k < len(ws):
                w = ws[k]
                if w == "e" and k + 1 < len(ws) and ws[k + 1] in UNI and ultimo and UNI[ws[k + 1]] < ultimo:
                    k += 1
                    continue
                if w not in UNI or (ultimo and w != "mil" and UNI[w] >= ultimo and ultimo != 1000):
                    break
                if w == "mil":
                    total += (atual or 1) * 1000
                    atual = 0
                else:
                    atual += UNI[w]
                ultimo = UNI[w]
                k += 1
            out.append(str(total + atual))
        else:
            out.append(ws[k])
            k += 1
    return " ".join(out)


def test_conversor_do_teste():
    assert como_whisper("Em mil novecentos e quatro") == "em 1904"
    assert como_whisper("entre dez e dezesseis de novembro") == "entre 10 e 16 de novembro"
    assert como_whisper("De mil oitocentos e noventa e sete a mil novecentos e seis") == "de 1897 a 1906"
    assert como_whisper("mais de novecentas pessoas") == "mais de 900 pessoas"


def test_portao_de_numeros_aceita_cada_frase_como_o_whisper_escreve():
    ns = synth()
    for b, frases in ler().blocos.items():
        for t, _ in frases:
            nota = ns["nota_portao"](t, como_whisper(t))
            assert nota >= ns["MIN_OK"], f"{b}: {t!r} -> {como_whisper(t)!r} ({nota:.2f})"


def test_autoteste_do_portao():
    p = subprocess.run([sys.executable, "synth_voz.py", "--teste"], cwd=EP, capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr


def test_synth_nao_clona_pessoa():
    ns = synth()
    fonte = (EP / "synth_voz.py").read_text(encoding="utf-8")
    assert "ref_denis" not in fonte and "rubberband" not in fonte
    assert "VoiceDesign" in ns["MODELO_DESIGN"]
    assert ns["MESTRA"].endswith("voz/voz-mestra.wav")
    assert ns["LANG"] == "portuguese"


def test_comando_do_mlx_audio(tmp_path, monkeypatch):
    monkeypatch.setenv("HB_MODO", "design")
    ns = synth()
    cmd = ns["comando"]("Olá.", "x")
    assert cmd[cmd.index("--model") + 1] == ns["MODELO_DESIGN"] and "--instruct" in cmd and "--ref_audio" not in cmd
    desc = cmd[cmd.index("--instruct") + 1]
    assert "Brazilian Portuguese" in desc and not re.search(r"like [A-Z]|(?i:parecid|imit|sounds like)", desc)
    monkeypatch.setenv("HB_MODO", "mestra")
    mestra = tmp_path / "voz-mestra.wav"
    mestra.write_bytes(b"RIFF")
    monkeypatch.setenv("HB_VOZ_MESTRA", str(mestra))
    ns = synth()
    cmd = ns["comando"]("Olá.", "x")
    assert cmd[cmd.index("--ref_audio") + 1] == str(mestra) and "--instruct" not in cmd


# ---------------------------------------------------------------- trava do fazer.py

def test_fazer_trava_com_fato_a_conferir(tmp_path):
    pasta = tmp_path / "ep"
    shutil.copytree(EP, pasta, ignore=shutil.ignore_patterns("hf-*", "__pycache__"))
    with pytest.raises(fazer.Falhou, match="conferir no mac"):
        fazer.et_roteiro(pasta, pasta / "fazer.log")
    assert not (pasta / "blocos.py").exists()


def test_fazer_gera_blocos_com_tudo_conferido(tmp_path):
    pasta = tmp_path / "ep"
    shutil.copytree(EP, pasta, ignore=shutil.ignore_patterns("hf-*", "__pycache__"))
    md = pasta / "roteiro.md"
    md.write_text(md.read_text(encoding="utf-8").replace("| CONFERIR NO MAC |", "| conferido |"), encoding="utf-8")
    assert "blocos.py gerado" in fazer.et_roteiro(pasta, pasta / "fazer.log")
    assert "8/8 blocos" in fazer.status(pasta)


# ---------------------------------------------------------------- cenas

def todas():
    m, r = cenas_mod(), ler()
    for b in r.ordem:
        yield b, getattr(m, f"cenas_{b}")(), r


def numeros(texto):
    return {float(t.replace(".", "").replace(",", ".")) for t in RE_NUM.findall(texto)}


def na_tela(cena):
    h, js = cena
    h = re.sub(r"</?span[^>]*>", "", h)        # o ano é batido algarismo por algarismo em <span>
    vistos = set(numeros(html_mod.unescape(re.sub(r"<[^>]+>", " ", h))))
    for a, b, _, casas, pre, suf in RE_COUNT.findall(js):
        final = f"{float(b):,.{int(casas)}f}".replace(",", "_").replace(".", ",").replace("_", ".")
        vistos |= numeros(pre + final + suf)
    return vistos


def texto_tela(cena):
    h, js = cena
    h = re.sub(r"</?span[^>]*>", "", h)
    return html_mod.unescape(re.sub(r"<[^>]+>", " ", h)) + " " + " ".join(p + s for *_, p, s in RE_COUNT.findall(js))


def test_cada_bloco_tem_cena_e_cena_aponta_para_frase():
    m, r = cenas_mod(), ler()
    assert {n[6:] for n in dir(m) if re.fullmatch(r"cenas_b\d+", n)} == set(r.ordem)
    for b, res, r in todas():
        C, P = res[0], res[1]
        n = len(r.blocos[b])
        assert C and all(0 <= k < n for k in C) and all(0 <= k < n for k in P)
        assert len(res) == (3 if b == r.ordem[-1] else 2)
        for pose, lado in P.values():
            assert pose in palito.POSES and lado in ("E", "D", "C")
        ids = re.findall(r'\bid="([^"]+)"', "".join(h for h, _ in C.values()))
        assert len(ids) == len(set(ids)), b
        assert all("repeat:-1" not in js for _, js in C.values())


def test_todo_numero_na_tela_esta_no_quadro():
    for b, res, r in todas():
        ok = {0.0}
        for n in r.numeros:
            ok |= numeros(n["numero"]) | numeros(n["fonte"])
        for k, cena in res[0].items():
            fora = {v for v in na_tela(cena) if v not in ok}
            assert not fora, f"{b} frase {k}: {sorted(fora)} não está no quadro"


def test_tela_sem_partido_politico_vivo_ou_canal_irmao():
    for b, res, _ in todas():
        for k, cena in res[0].items():
            txt = texto_tela(cena)
            achados = [p for p in PROIBIDO_TELA if re.search(p, txt)]
            assert not achados, f"{b}/{k}: {achados}"


def test_b5_sem_piada_nem_carimbo_sobre_os_mortos():
    m = cenas_mod()
    C, _ = m.cenas_b5()
    k = m.indice(m.frases("b5"), "cerca de trinta mortos")
    assert "carimbo" not in C[k][0] and "tl.to('#stage'" not in C[k][1]


def test_poses_dentro_dos_limites():
    for nome, angs in palito.POSES.items():
        for j, a in angs.items():
            lo, hi = palito.LIMITES[j]
            assert lo <= a <= hi, f"{nome}.{j} = {a} fora de {palito.LIMITES[j]}"


def test_palito_e_outro():
    svg = palito.SVG
    assert 'id="pl-chapeu"' in svg and 'id="pl-bigode"' in svg and "<circle cx=\"0\" cy=\"-148\" r=\"24\"" in svg
    assert all(f'id="pl-{o}"' in svg for o in ("anteE", "anteD", "canelaE", "canelaD"))   # cotovelo e joelho
    assert "st-head" not in svg and "boil" not in svg      # nada do desenho do canal irmão


def beats_falsos(frases):
    t, out = .35, []
    for k, (texto, gap) in enumerate(frases):
        fim = t + len(texto) * .067
        out.append({"i": k, "texto": texto, "piii": [], "ini": round(t, 3), "fim": round(fim, 3)})
        t = fim + gap
    return {"dur": round(t, 3), "frases": out}


@pytest.fixture(scope="module")
def montado(tmp_path_factory):
    """Copia o episódio, gera blocos.py e beats falsos e roda build_hf.py + sfx.py em todos os blocos."""
    if not (CANAL / "node_modules" / "gsap").exists():
        pytest.skip("rode `npm install` em canais-dark/historia-brasil (gsap e fontes locais)")
    import numpy as np
    import soundfile as sf
    pasta = tmp_path_factory.mktemp("hb") / "ep"
    shutil.copytree(EP, pasta, ignore=shutil.ignore_patterns("hf-*", "__pycache__"))
    for arq in ("palito.py", "pecas.py", "roteiro.py", "pronuncia.py", "pronuncia.txt"):   # o que fica na raiz do canal
        shutil.copy(CANAL / arq, pasta.parent / arq)
    r = ler()
    (pasta / "blocos.py").write_text(rot.para_blocos_py(r), encoding="utf-8")
    for b in r.ordem:
        bt = beats_falsos(r.blocos[b])
        (pasta / f"voz_{b}.beats.json").write_text(json.dumps(bt, ensure_ascii=False))
        sf.write(pasta / f"voz_{b}.wav", np.zeros(int(bt["dur"] * 24000)), 24000)
    env = {"HB_NODE_MODULES": str(CANAL / "node_modules")}
    import os
    for b in r.ordem:
        p = subprocess.run([sys.executable, "build_hf.py", b], cwd=pasta, capture_output=True, text=True, env={**os.environ, **env})
        assert p.returncode == 0, p.stderr
    p = subprocess.run([sys.executable, "sfx.py", *r.ordem], cwd=pasta, capture_output=True, text=True, env={**os.environ, **env})
    assert p.returncode == 0, p.stderr
    return pasta, r


def test_build_hf_monta_html_valido(montado):
    pasta, r = montado
    for b in r.ordem:
        pagina = (pasta / f"hf-{b}" / "index.html").read_text(encoding="utf-8")
        secoes = re.findall(r'<section id="sc(\w+)" class="clip scene[^"]*" data-start="([\d.]+)" data-duration="([-\d.]+)"', pagina)
        assert len(secoes) == len(r.blocos[b]) + (1 if b == r.ordem[-1] else 0)
        assert all(float(d) > 0 for *_, d in secoes)
        assert (pasta / f"hf-{b}" / "assets" / "gsap.min.js").exists()
        assert "cdn." not in pagina and "fonts.googleapis" not in pagina      # render offline
        assert not [p for p in PROIBIDO_TELA[:6] if re.search(p, pagina)]
        if shutil.which("node"):
            js = re.search(r"<script>\n(.*?)</script>", pagina, re.S).group(1)
            (pasta / f"_{b}.js").write_text(js)
            chk = subprocess.run(["node", "--check", str(pasta / f"_{b}.js")], capture_output=True, text=True)
            assert chk.returncode == 0, chk.stderr


def test_sfx_gera_trilha_do_tamanho_do_bloco(montado):
    import soundfile as sf
    pasta, r = montado
    for b in r.ordem:
        info = sf.info(pasta / f"sfx_{b}.wav")
        assert info.duration > 5


# ---------------------------------------------------------------- nomes proibidos nos arquivos

def test_nenhuma_mencao_ao_dono_em_lugar_nenhum():
    for arq in CANAL.rglob("*"):
        if arq.is_file() and "node_modules" not in arq.parts and arq.suffix in {".py", ".md", ".txt", ".json", ".html"}:
            txt = arq.read_text(encoding="utf-8", errors="ignore")
            # os nomes vão escritos com [ ] para que nem este arquivo os contenha por extenso
            assert not re.search(r"D[e]nis|Miy[a]bara|d[e]nal|Inv[e]stir e Co|\bI[e]C\b", txt), arq


def test_texto_do_video_sem_canal_irmao():
    for arq in (EP / "roteiro.md", EP / "descricao.txt", EP / "TITULO.md", EP / "cenas_hf.py", CANAL / "pecas.py",
                CANAL / "palito.py", CANAL / "voz" / "descricao.txt"):
        assert not re.search(r"(?i)faz a conta|faz-a-conta", arq.read_text(encoding="utf-8")), arq
