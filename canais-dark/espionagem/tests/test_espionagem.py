"""Testes minimos do canal (rodam sem Mac, sem voz e sem rede):  python3 -m pytest canais-dark/espionagem/tests -q"""
import csv, os, re, shutil, subprocess, sys, unicodedata
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
EP = RAIZ / "ep01-eichmann"
sys.path.insert(0, str(RAIZ))
import roteiro  # noqa: E402
import portao  # noqa: E402


def _sem_acento(s):
    return "".join(c for c in unicodedata.normalize("NFD", s.lower()) if unicodedata.category(c) != "Mn")


@pytest.fixture(scope="module")
def rot():
    return roteiro.ler(EP / "roteiro.md")


def test_roteiro_passa_no_normalizador_de_numeros(rot):
    avisos = [a for a in roteiro.validar(rot) if "algarismo" in a or "começa com número" in a or "vazio" in a]
    assert not avisos, avisos


def test_tamanho_do_roteiro(rot):
    palavras = sum(len(t.split()) for f in rot.blocos.values() for t, _ in f)
    assert 2000 <= palavras <= 2600, palavras


def test_fontes_citadas_existem_no_quadro(rot):
    ids = {n["id"] for n in rot.numeros}
    texto = (EP / "roteiro.md").read_text(encoding="utf-8")
    citados = set(re.findall(r"\bF\d\d\b", "\n".join(l for l in texto.splitlines() if l.startswith("* fonte:"))))
    assert citados <= ids, citados - ids
    assert ids <= citados, f"fato no quadro sem uso no roteiro: {ids - citados}"
    assert all(n["fonte"] for n in rot.numeros)


def test_trava_de_fatos_bloqueia_voz_enquanto_houver_conferir(rot):
    pend = [n for n in rot.numeros if n["status"] not in roteiro.STATUS_OK]
    for n in pend:
        assert n["status"] == "conferir no mac", n


def test_portao_de_voz():
    portao._autoteste()


def test_cenas_montam_e_imagens_estao_na_planilha(tmp_path):
    copia = tmp_path / "ep"
    shutil.copytree(EP, copia, ignore=shutil.ignore_patterns("hf-*", "imagens", "voz_*", "render_*", "__pycache__"))
    for b in roteiro.ler(copia / "roteiro.md").ordem:
        p = subprocess.run([sys.executable, str(RAIZ / "build_hf.py"), b, "--sem-voz"], cwd=copia, capture_output=True, text=True)
        assert p.returncode == 0, p.stdout + p.stderr
        html = (copia / f"hf-{b}" / "index.html").read_text(encoding="utf-8")
        assert 'data-composition-id="main"' in html and "window.__timelines" in html
    nomes = set(re.findall(r'(?:arquivo|documento|video)\("([^"]+)"', (EP / "cenas_hf.py").read_text(encoding="utf-8")))
    planilha = {r["arquivo"] for r in csv.DictReader(open(RAIZ / "licencas-ep01.csv", encoding="utf-8"))}
    assert nomes and nomes <= planilha, nomes - planilha


def test_morte_contada_nunca_mostrada():
    sys.path.insert(0, str(EP))
    import cenas_hf
    cena = dict(cenas_hf.CENAS["b8"])["Adolf Eichmann foi enforcado"]
    assert "@@IMG" not in cena[0] and "@@VID" not in cena[0] and 'class="preto"' in cena[0]


def test_planilha_no_formato_do_modelo_e_sem_nc_nd():
    modelo = next(csv.reader(open(RAIZ.parent / "licencas-modelo.csv", encoding="utf-8")))
    linhas = list(csv.DictReader(open(RAIZ / "licencas-ep01.csv", encoding="utf-8")))
    assert list(linhas[0].keys()) == modelo
    proib = re.compile(r"\b(NC|ND)\b|non-?commercial|no-?deriv|não comercial|sem derivação|BY-NC|BY-ND", re.I)
    for r in linhas:
        assert not proib.search(r["licenca"]), r["arquivo"]
        assert not re.search(r"CC[ -]?BY[- ](NC|ND)", r["base_legal"]), r["arquivo"]
        assert all(r[c].strip() for c in modelo), f"coluna vazia em {r['arquivo']}"


def test_nenhuma_mencao_ao_dono_nem_aos_outros_canais():
    # escritos de tras para frente para que nem este teste contenha os nomes
    proibidos = [w[::-1] for w in ['sined', 'arabayim', 'laned', 'racoc e ritsevni', 'atnoc a zaf', 'atnocazaf', 'racoceritsevni']]
    achados = []
    for p in RAIZ.rglob("*"):
        if p.is_file() and p.suffix in {".md", ".py", ".txt", ".csv", ".html", ".json"} and "hf-" not in str(p.parent):
            t = _sem_acento(p.read_text(encoding="utf-8", errors="ignore"))
            achados += [f"{p.name}: {w}" for w in proibidos if w in t]
    assert not achados, achados
