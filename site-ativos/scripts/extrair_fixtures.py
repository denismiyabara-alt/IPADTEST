"""Extrai fixtures pequenas dos arquivos reais do cache para os testes rodarem sem rede.

Uso: python3 scripts/extrair_fixtures.py   (depois de `python3 -m iec_ativos baixar`)
Grava tests/fixtures/ com recortes dos CSVs da CVM (mesmo cabeçalho, mesmas linhas) e linhas do COTAHIST.
"""
import gzip
import re
import sys
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from iec_ativos import config  # noqa: E402
from iec_ativos.normalizar import fmt_cnpj  # noqa: E402

FIX = RAIZ / "tests" / "fixtures"
EMPRESAS = {"33000167000101": "PETR", "60872504000123": "ITUB", "30306294000145": "BPAC",
            "33592510000154": "VALE", "00001180000126": "AXIA"}
FIIS = {"11728688000147": "HGLG11", "28757546000100": "XPML11"}
ANOS = {"dfp": [2024, 2025], "itr": [2025, 2026]}
# Só as contas que o cálculo usa, para a fixture ficar pequena
CONTA_OK = re.compile(r"^(1|2|1\.01\.0[12]|2\.0\d|2\.0\d\.\d\d(\.\d\d)?|3\.\d\d(\.\d\d)?|3\.99(\.\d\d){0,2}|6\.03\.\d\d|7\.0\d\.01)$")
TICKERS = ["PETR4", "PETR3", "ITUB4", "ITUB3", "BPAC11", "BPAC3", "BPAC5", "HGLG11", "XPML11", "VALE3", "AXIA3"]
DATAS = {"20251001", "20251002", "20260630", "20260901", "20260929", "20260930", "20261001"}


def recortar(z, membro, destino, filtro):
    with z.open(membro) as f:
        cab = f.readline()
        linhas = [ln for ln in f if filtro(ln)]
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_bytes(cab + b"".join(linhas))
    return len(linhas)


def main():
    pref = {fmt_cnpj(c).encode() for c in EMPRESAS}
    total = 0
    for doc, anos in ANOS.items():
        for ano in anos:
            z = zipfile.ZipFile(config.RAW / "cvm" / f"{doc}_cia_aberta_{ano}.zip")
            for m in z.namelist():
                if not re.search(r"_(BPA|BPP|DRE|DFC_MI|DVA)_con_|composicao_capital|_cia_aberta_\d{4}\.csv$", m):
                    continue
                def filtro(ln, m=m):
                    if ln[:18] not in pref:
                        return False
                    if "composicao" in m or re.search(r"_cia_aberta_\d{4}\.csv$", m):
                        return True
                    cols = ln.decode("latin-1").split(";")
                    return bool(CONTA_OK.match(cols[11] if "BPA" in m or "BPP" in m else cols[11]))
                # BPA/BPP têm uma coluna a menos (sem DT_INI_EXERC): CD_CONTA é a 11ª (índice 10)
                if "_BPA_" in m or "_BPP_" in m:
                    def filtro(ln, m=m):  # noqa: F811
                        return ln[:18] in pref and bool(CONTA_OK.match(ln.decode("latin-1").split(";")[10]))
                total += recortar(z, m, FIX / "cvm" / f"{doc}_{ano}" / m, filtro)
    # FII: informe mensal 2025 e 2026 e trimestral 2026
    fpref = {fmt_cnpj(c).encode() for c in FIIS}
    for ano in (2025, 2026):
        z = zipfile.ZipFile(config.RAW / "cvm" / f"inf_mensal_fii_{ano}.zip")
        for m in z.namelist():
            col = 1 if "geral" in m else 0
            total += recortar(z, m, FIX / "cvm" / f"inf_mensal_fii_{ano}" / m,
                              lambda ln, col=col: ln.split(b";")[col] in fpref)
    z = zipfile.ZipFile(config.RAW / "cvm" / "inf_trimestral_fii_2026.zip")
    m = "inf_trimestral_fii_imovel_2026.csv"
    total += recortar(z, m, FIX / "cvm" / "inf_trimestral_fii_2026" / m, lambda ln: ln[:18] in fpref)
    # COTAHIST
    linhas = []
    for gz in sorted((config.RAW / "b3").glob("COTAHIST_A202[56].txt.gz")):
        with gzip.open(gz, "rt", encoding="latin-1") as f:
            for ln in f:
                if ln[2:10] in DATAS and ln[12:24].strip() in TICKERS:
                    linhas.append(ln)
    (FIX / "b3").mkdir(parents=True, exist_ok=True)
    (FIX / "b3" / "COTAHIST_recorte.txt").write_text("".join(linhas), encoding="latin-1")
    # FCA (só as linhas de units, mais as das empresas)
    z = zipfile.ZipFile(config.RAW / "cvm" / f"fca_cia_aberta_{config.HOJE.year}.zip")
    m = f"fca_cia_aberta_valor_mobiliario_{config.HOJE.year}.csv"
    total += recortar(z, m, FIX / "cvm" / "fca" / m, lambda ln: ln[:18] in pref or b";Units;" in ln)
    cad = (config.RAW / "cvm" / "cad_cia_aberta.csv").read_bytes().splitlines(keepends=True)
    (FIX / "cvm" / "cad_cia_aberta.csv").write_bytes(cad[0] + b"".join(ln for ln in cad[1:] if ln[:18] in pref))
    for arq in list(FIX.rglob("*.csv")) + list(FIX.rglob("*.txt")):  # gzip: fixture pequena no Git
        with open(arq, "rb") as f_in, gzip.GzipFile(arq.with_name(arq.name + ".gz"), "wb", 9, mtime=0) as f_out:
            f_out.write(f_in.read())
        arq.unlink()
    print(f"{total} linhas da CVM e {len(linhas)} do COTAHIST em {FIX}")


if __name__ == "__main__":
    main()
