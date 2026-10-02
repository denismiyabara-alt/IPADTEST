"""Monta, a partir de tests/fixtures (recortes dos arquivos reais), um cache de mentira e um SQLite.

Os testes rodam sem rede. As fixtures saem de scripts/extrair_fixtures.py.
"""
import gzip
import shutil
import sys
import zipfile
from datetime import date
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
FIX = RAIZ / "tests" / "fixtures"


def _zip_de_pasta(pasta: Path, destino: Path):
    with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
        for gz in sorted(pasta.glob("*.gz")):
            z.writestr(gz.name[:-3], gzip.decompress(gz.read_bytes()))


@pytest.fixture(scope="session")
def ambiente(tmp_path_factory):
    from iec_ativos import config
    base = tmp_path_factory.mktemp("iec")
    raw = base / "raw"
    (raw / "cvm").mkdir(parents=True)
    (raw / "b3").mkdir()
    for pasta in (FIX / "cvm").iterdir():
        if pasta.is_dir() and pasta.name.startswith(("dfp_", "itr_")):
            doc, ano = pasta.name.split("_")
            _zip_de_pasta(pasta, raw / "cvm" / f"{doc}_cia_aberta_{ano}.zip")
        elif pasta.is_dir() and pasta.name.startswith("inf_"):
            _zip_de_pasta(pasta, raw / "cvm" / f"{pasta.name}.zip")
        elif pasta.is_dir() and pasta.name == "fca":
            _zip_de_pasta(pasta, raw / "cvm" / "fca_cia_aberta_2026.zip")
    (raw / "cvm" / "cad_cia_aberta.csv").write_bytes(gzip.decompress((FIX / "cvm" / "cad_cia_aberta.csv.gz").read_bytes()))
    with gzip.open(raw / "b3" / "COTAHIST_A2026.txt.gz", "wb") as f:
        f.write(gzip.decompress((FIX / "b3" / "COTAHIST_recorte.txt.gz").read_bytes()))
    antigos = {k: getattr(config, k) for k in ("RAW", "CACHE", "DB", "SAIDA", "HOJE", "ANOS_DFP", "ANOS_ITR",
                                                  "ANOS_FII", "SEO_VARREDURA")}
    config.RAW, config.CACHE, config.DB, config.SAIDA = raw, base, base / "dados.sqlite", base / "saida"
    config.HOJE = date(2026, 10, 2)
    config.ANOS_DFP, config.ANOS_ITR, config.ANOS_FII = [2024, 2025], [2025, 2026], [2025, 2026]
    config.SEO_VARREDURA = base / "nao-existe.json"
    from iec_ativos import normalizar as n
    con = n.conectar()
    n.normalizar_cadastro(con)
    n.normalizar_fca(con)
    n.normalizar_cotahist(con)
    n.completar_ativos(con)
    n.normalizar_fii(con)
    n.normalizar_demonstracoes(con, {"33000167000101", "60872504000123", "30306294000145", "33592510000154",
                                     "00001180000126"})
    con.commit()
    yield {"con": con, "base": base}
    con.close()
    for k, v in antigos.items():
        setattr(config, k, v)
    shutil.rmtree(base, ignore_errors=True)
