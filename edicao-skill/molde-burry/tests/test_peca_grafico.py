"""Peca "grafico" (4a peca de B-roll) no molde Burry: ponta a ponta e regra de compliance.

Rodar da raiz do repo:  IEC_MOTION=$PWD/motion python3 -m pytest -q edicao-skill/molde-burry/tests
(sem IEC_MOTION, o teste usa a pasta motion/ vizinha de edicao-skill/).

Ponta a ponta, num projeto falso com a estrutura do molde (FINAL-corte.mp4 sintetico de 24 s + final.json):
  pecas.py (peca G ancorada em frase) → plano.py → broll/grafico.py --render → mapa.py → montar.py
e confere: duracao derivada da fala, o grafico no lugar certo do VIDEO-FINAL (frame a frame contra o mp4
do grafico), contagem de frames igual a do corte, e o numero final na tela = ultimo valor da serie.
Precisa de ffmpeg, node, `npm install` no motion/, Chrome headless e o cache do site-ativos;
o que faltar faz o teste ser pulado (as regras de compliance rodam sem render).
"""
import json, os, shutil, subprocess, sys, textwrap

import pytest

MOLDE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPO = os.path.dirname(os.path.dirname(MOLDE))
MOTION = os.environ.get("IEC_MOTION") or os.path.join(REPO, "motion")
sys.path.insert(0, os.path.join(MOTION, "grafico_cotacao"))
import serie as S  # noqa: E402

FPS = 30
ENV = {**os.environ, "IEC_MOTION": MOTION, "MONTAR_VCODEC": os.environ.get("MONTAR_VCODEC", "libx264")}

tem_cache = pytest.mark.skipif(not S._sqlite(), reason="sem cache do site-ativos (cache/dados.sqlite)")
tem_render = pytest.mark.skipif(
    not (shutil.which("ffmpeg") and shutil.which("node")
         and os.path.isdir(os.path.join(MOTION, "node_modules", "hyperframes"))),
    reason="sem ffmpeg/node ou sem npm install no motion/")

SEGMENTOS = [  # transcricao falsa do corte, no formato do mlx_whisper (texto com acento, como sai dele)
    {"start": 0.0, "end": 5.0, "text": "Parte do preço ficou para depois."},
    {"start": 5.0, "end": 13.4, "text": "E as parcelas da Iguatemi vêm corrigidas pelo CDI, que anda colado na Selic."},
    {"start": 13.4, "end": 18.0, "text": "Isso não sai de graça."},
    {"start": 18.0, "end": 24.0, "text": "Cada cota nova puxa o dividendo."},
]


def projeto(tmp, cenas, pecas):
    """Pasta com a estrutura do molde (README: <projeto>/ pecas.py plano.py ... videos/broll/)."""
    raiz = tmp / "proj"
    broll = raiz / "videos" / "broll"
    broll.mkdir(parents=True)
    for f in ("plano.py", "mapa.py", "montar.py"):
        shutil.copy(os.path.join(MOLDE, f), raiz / f)
    shutil.copy(os.path.join(MOLDE, "broll", "grafico.py"), broll / "grafico.py")
    (raiz / "pecas.py").write_text("PECAS = " + repr(pecas) + "\n")
    (broll / "cenas.py").write_text("T = " + repr(cenas) + "\n")
    json.dump({"segments": SEGMENTOS}, open(raiz / "final.json", "w"), ensure_ascii=False)
    return raiz, broll


def rodar(cmd, cwd):
    return subprocess.run(cmd, cwd=cwd, env=ENV, capture_output=True, text=True)


def grafico_py(broll, *extra):
    return rodar([sys.executable, "grafico.py", *extra], broll)


# ------------------------------------------------------------ compliance (sem render)
@tem_cache
def test_acao_sem_comparador_nem_aviso_e_recusada(tmp_path):
    raiz, broll = projeto(tmp_path, {"g1": ("grafico", dict(serie="COTAHIST:PETR4", periodo="2025-10-01:",
                                                           rotulo="PETR4 em 12 meses"))},
                          [("g1", "G", r"corrigidas pelo cdi", 0.0)])
    assert rodar([sys.executable, "plano.py", "final.json"], raiz).returncode == 0
    r = grafico_py(broll)
    assert r.returncode != 0
    assert "COMPLIANCE" in r.stderr and "ativo isolado" in r.stderr and "IBOV, IFIX ou CDI" in r.stderr
    assert not (broll / "graficos").exists() and not (broll / "graficos.json").exists()


@tem_cache
def test_acao_com_cdi_passa_e_desenha_duas_linhas(tmp_path):
    raiz, broll = projeto(tmp_path, {"g1": ("grafico", dict(serie="COTAHIST:PETR4", periodo="2025-10-01:",
                                                           rotulo="PETR4 contra o CDI", comparador="CDI"))},
                          [("g1", "G", r"corrigidas pelo cdi", 0.0)])
    rodar([sys.executable, "plano.py", "final.json"], raiz)
    r = grafico_py(broll)
    assert r.returncode == 0, r.stderr
    html = (broll / "graficos" / "g1" / "index.html").read_text()
    assert 'id="linha-comp"' in html and "base 100" in html and "CDI: BCB (SGS 12)" in html


@tem_cache
def test_acao_com_aviso_passa_e_escreve_o_aviso(tmp_path):
    raiz, broll = projeto(tmp_path, {"g1": ("grafico", dict(serie="COTAHIST:PETR4", periodo="2025-10-01:",
                                                           rotulo="PETR4 em 12 meses", aviso=True))},
                          [("g1", "G", r"corrigidas pelo cdi", 0.0)])
    rodar([sys.executable, "plano.py", "final.json"], raiz)
    assert grafico_py(broll).returncode == 0
    assert "Não é recomendação de investimento." in (broll / "graficos" / "g1" / "index.html").read_text()


@tem_cache
def test_selic_sozinha_passa(tmp_path):
    raiz, broll = projeto(tmp_path, {"g1": ("grafico", dict(serie="SGS:432", periodo="2020-01-01:", rotulo="Selic"))},
                          [("g1", "G", r"corrigidas pelo cdi", 0.0)])
    rodar([sys.executable, "plano.py", "final.json"], raiz)
    r = grafico_py(broll)
    assert r.returncode == 0, r.stderr
    ultimo = S.serie_bcb(432, "2020-01-01")[0][-1][1]
    assert json.load(open(broll / "graficos.json"))["g1"]["final"] == S.fmt_br(ultimo, 2) + "%"


def test_regra_vale_sem_cache_e_antes_de_buscar_dado():
    import especificacao as E
    with pytest.raises(E.ErroCompliance):
        E.montar_entrada({"serie": "COTAHIST:QUALQUER3", "periodo": "12m", "rotulo": "x"})
    E.checar_compliance("indicador", None, None)          # SGS sozinha: ok
    E.checar_compliance("ativo", "CDI", None)             # com comparador: ok
    E.checar_compliance("ativo", None, True)              # com aviso: ok


def test_taxa_com_indice_acumulado_e_recusada():
    import especificacao as E
    if not S._sqlite():
        pytest.skip("sem cache")
    with pytest.raises(E.ErroEspecificacao, match="taxa"):
        E.montar_entrada({"serie": "SGS:432", "periodo": "2020-01-01:", "rotulo": "x", "comparador": "IBOV"})


def test_grafico_com_pouco_espaco_e_recusado_no_plano(tmp_path):
    raiz, _ = projeto(tmp_path, {}, [("g1", "G", r"corrigidas pelo cdi", 0.0), ("x2", "A", r"anda colado", 0.0)])
    segs = [dict(s) for s in SEGMENTOS]
    segs[1] = {"start": 5.0, "end": 8.0, "text": "corrigidas pelo CDI"}
    segs.insert(2, {"start": 8.0, "end": 13.4, "text": "anda colado na Selic"})
    json.dump({"segments": segs}, open(raiz / "final.json", "w"))
    r = rodar([sys.executable, "plano.py", "final.json"], raiz)
    assert r.returncode != 0 and "precisa de 5 s" in r.stderr


# ------------------------------------------------------------ ponta a ponta
def ffprobe_frames(mp4):
    return int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-count_frames", "-show_entries",
                               "stream=nb_read_frames", "-of", "default=nw=1:nk=1", str(mp4)],
                              capture_output=True, text=True).stdout.strip())


def psnr(a, ta, b, tb):
    """PSNR entre o frame do instante ta de a e o de tb de b (dB; inf = identicos)."""
    r = subprocess.run(["ffmpeg", "-v", "info", "-ss", f"{ta:.3f}", "-i", str(a), "-ss", f"{tb:.3f}", "-i", str(b),
                        "-frames:v", "1", "-lavfi", "[0:v][1:v]psnr", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    linha = [l for l in r.splitlines() if "PSNR" in l and "average:" in l][-1]
    v = linha.split("average:")[1].split()[0]
    return float("inf") if v == "inf" else float(v)


@tem_cache
@tem_render
def test_ponta_a_ponta_plano_mapa_montar(tmp_path):
    cenas = {"54-selic": ("grafico", dict(serie="SGS:432", periodo="2020-01-01:", rotulo="Selic: de 2% a 15%",
                                          kicker="O CDI anda colado na Selic", destaques="extremos"))}
    raiz, broll = projeto(tmp_path, cenas, [("54-selic", "G", r"corrigidas pelo cdi", 0.0)])
    # corte falso: 24 s de imagem de teste + tom, 30 fps, como o FINAL-corte.mp4
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i", "testsrc2=s=1920x1080:r=30:d=24",
                    "-f", "lavfi", "-i", "sine=f=220:d=24:sample_rate=48000", "-c:v", "libx264", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-shortest", str(raiz / "FINAL-corte.mp4")], check=True)

    r = rodar([sys.executable, "plano.py", "final.json"], raiz)
    assert r.returncode == 0, r.stderr
    plano = json.load(open(raiz / "plano.json"))
    assert plano["54-selic"] == {"peca": "G", "entra": 5.0, "dur": 8.4}    # da frase: 5,0 s → 13,4 s

    r = grafico_py(broll, "--render")
    assert r.returncode == 0, r.stdout + r.stderr
    reg = json.load(open(broll / "graficos.json"))["54-selic"]
    ultimo = S.serie_bcb(432, "2020-01-01")[0][-1][1]
    assert reg["final"] == S.fmt_br(ultimo, 2) + "%"
    assert reg["eventos"] == [[round(8.4 * 0.62, 3), "impacto", 0.55]]
    mp4 = raiz / reg["mp4"]
    assert ffprobe_frames(mp4) == round(8.4 * FPS)

    # o numero na tela, no ultimo instante do grafico, e o ultimo valor da serie
    q = subprocess.run(["node", os.path.join(MOTION, "grafico_cotacao", "quadro.mjs"),
                        str(broll / "graficos" / "54-selic"), "8.4"], capture_output=True, text=True, env=ENV)
    tela = json.loads(q.stdout.strip().splitlines()[-1])
    assert tela["erros"] == [] and tela["numero"] == reg["final"]

    r = rodar([sys.executable, "mapa.py"], raiz)
    assert r.returncode == 0, r.stdout + r.stderr
    cart = json.load(open(raiz / "cartelas.json"))
    assert cart == [{"peca": "G", "ini": 0.0, "fim": 8.4, "entra": 5.0, "id": "54-selic"}]

    r = rodar([sys.executable, "montar.py"], raiz)
    assert r.returncode == 0, r.stdout + r.stderr
    final = raiz / "VIDEO-FINAL.mp4"
    assert ffprobe_frames(final) == 24 * FPS
    # dentro da janela, o VIDEO-FINAL mostra o grafico (inclusive o quadro final, com o numero pousado)...
    # (o montar re-encoda: o mesmo quadro fica acima de 25 dB; quadros diferentes ficam abaixo de 15 dB)
    corte = raiz / "FINAL-corte.mp4"
    for t in (2.0, 8.2):
        assert psnr(final, 5.0 + t, mp4, t) > 25
        assert psnr(final, 5.0 + t, corte, 5.0 + t) < 15
    # ...e fora dela, o corte original
    for t in (2.0, 15.0, 23.0):
        assert psnr(final, t, corte, t) > 25
    shutil.copy(final, tmp_path / "VIDEO-FINAL.mp4")
