"""Ajuda para os testes de navegador da biblioteca: abre o projeto num Chrome headless (comum/quadro.mjs)
e devolve o que está na tela em cada instante. Mesma lógica de pulo do tests/test_grafico.py: sem
node_modules ou sem Chrome headless, os testes de navegador são pulados."""
import json, os, shutil, subprocess

import pytest

COMUM = os.path.dirname(os.path.abspath(__file__))
MOTION = os.path.dirname(COMUM)


def _chrome():
    if os.environ.get("PRODUCER_HEADLESS_SHELL_PATH"):
        return True
    bin_ = os.path.join(MOTION, "node_modules", ".bin", "hyperframes")
    if not os.path.exists(bin_):
        return False
    r = subprocess.run([bin_, "browser", "path"], capture_output=True, text=True)
    return r.returncode == 0 and os.path.exists(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else "")


def _pronto():
    return bool(shutil.which("node") and os.path.isdir(os.path.join(MOTION, "node_modules", "puppeteer-core"))
                and _chrome())


precisa_navegador = pytest.mark.skipif(not _pronto(), reason="sem node_modules (npm install) ou sem Chrome headless")


def quadros(projeto, instantes, png=None):
    """-> {"quadros": [{"t", "duracao", "tela"}...], "fontes": [...], "erros": [...]}"""
    cmd = ["node", os.path.join(COMUM, "quadro.mjs"), projeto, ",".join(str(t) for t in instantes)] + ([png] if png else [])
    out = subprocess.run(cmd, capture_output=True, text=True, check=True, timeout=180).stdout
    return json.loads(out.strip().splitlines()[-1])
