"""Consulta rápida às DFPs da CVM já baixadas em site-ativos/cache/raw/cvm (sem rede).
Uso: python3 auditoria-fatos/dfp.py <cnpj só dígitos ou trecho do nome> [conta ...]
Mostra, por ano (exercício social, ÚLTIMO), as contas pedidas da DRE/BPP consolidada (ou individual se não houver)."""
import csv, io, re, sys, zipfile
from pathlib import Path
RAW = Path(__file__).resolve().parent.parent / "site-ativos" / "cache" / "raw" / "cvm"

def fmt_cnpj(d):
    return f"{d[:2]}.{d[2:5]}.{d[5:8]}/{d[8:12]}-{d[12:]}"

def contas(alvo, codigos=("3.01", "3.11", "2.03"), escopos=("con", "ind")):
    out = {}
    for z in sorted(RAW.glob("dfp_cia_aberta_20*.zip")):
        ano = z.stem[-4:]
        with zipfile.ZipFile(z) as zf:
            for esc in escopos:
                for dem in ("DRE", "BPP"):
                    nome = f"dfp_cia_aberta_{dem}_{esc}_{ano}.csv"
                    if nome not in zf.namelist():
                        continue
                    for r in csv.DictReader(io.TextIOWrapper(zf.open(nome), encoding="latin-1"), delimiter=";"):
                        if not (r["CNPJ_CIA"] == alvo or alvo.lower() in r["DENOM_CIA"].lower()):
                            continue
                        if r["ORDEM_EXERC"] != "ÚLTIMO" or r["CD_CONTA"] not in codigos:
                            continue
                        esc_mult = 1000 if r["ESCALA_MOEDA"] == "MIL" else 1
                        chave = (r["DENOM_CIA"], esc, r["DT_FIM_EXERC"], r["CD_CONTA"], r["DS_CONTA"])
                        out[chave] = float(r["VL_CONTA"]) * esc_mult
    return out

if __name__ == "__main__":
    alvo = sys.argv[1]
    if alvo.isdigit():
        alvo = fmt_cnpj(alvo)
    cods = tuple(sys.argv[2:]) or ("3.01", "3.11", "2.03")
    for (den, esc, dt, cd, ds), v in sorted(contas(alvo, cods).items(), key=lambda x: (x[0][1], x[0][3], x[0][2])):
        print(f"{den[:30]:30} {esc} {dt} {cd:6} {ds[:45]:45} R$ {v/1e9:10.3f} bi")
