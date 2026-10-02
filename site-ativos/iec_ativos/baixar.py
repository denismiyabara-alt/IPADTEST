"""Etapa 1: baixar. CVM (cadastro, FCA, DFP, ITR, FII), B3 (COTAHIST) e BCB (SGS).

Os ZIPs da CVM (de 1 a 30 MB) ficam no cache: o normalizar lê de dentro deles em streaming.
O COTAHIST anual (~90 MB) é filtrado na hora (só mercado à vista, TPMERC 010) para um .txt.gz
pequeno, e o ZIP é apagado. O meta.json fica, para o pedido condicional da próxima vez.
"""
import gzip
import zipfile
from datetime import date, timedelta

from . import config
from .rede import baixar, baixar_texto, meta_de

CVM = "https://dados.cvm.gov.br/dados/"
B3_SERHIST = "https://bvmf.bmfbovespa.com.br/InstDados/SerHist/"
BCB = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie}/dados?formato=json&dataInicial={ini}&dataFinal={fim}"
SERIES_BCB = {12: "CDI diário", 11: "Selic diária", 432: "Meta Selic", 433: "IPCA mensal", 13522: "IPCA 12 meses"}


def arquivos_cvm() -> list[tuple[str, str]]:
    """(caminho relativo na CVM, nome local)."""
    lst = [("CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv", "cvm/cad_cia_aberta.csv")]
    for a in [config.HOJE.year]:
        lst.append((f"CIA_ABERTA/DOC/FCA/DADOS/fca_cia_aberta_{a}.zip", f"cvm/fca_cia_aberta_{a}.zip"))
    for a in config.ANOS_DFP:
        lst.append((f"CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_{a}.zip", f"cvm/dfp_cia_aberta_{a}.zip"))
    for a in config.ANOS_ITR:
        lst.append((f"CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_{a}.zip", f"cvm/itr_cia_aberta_{a}.zip"))
    for a in config.ANOS_FII:
        lst.append((f"FII/DOC/INF_MENSAL/DADOS/inf_mensal_fii_{a}.zip", f"cvm/inf_mensal_fii_{a}.zip"))
    for a in config.ANOS_FII[-2:]:
        lst.append((f"FII/DOC/INF_TRIMESTRAL/DADOS/inf_trimestral_fii_{a}.zip", f"cvm/inf_trimestral_fii_{a}.zip"))
    return lst


def baixar_cvm(log=print) -> None:
    for rel, local in arquivos_cvm():
        destino = config.RAW / local
        try:
            _, mudou = baixar(CVM + rel, destino)
            log(f"CVM {local}: {'baixado' if mudou else 'sem mudança'}")
        except FileNotFoundError:
            log(f"CVM {local}: não existe (404), seguindo")


def _filtrar_cotahist(zip_path, saida_gz) -> int:
    """Guarda só as linhas de mercado à vista (TPMERC 010). Lê o ZIP em streaming."""
    n = 0
    with zipfile.ZipFile(zip_path) as z, gzip.open(saida_gz, "wt", encoding="latin-1") as out:
        for nome in z.namelist():
            with z.open(nome) as f:
                for linha in f:
                    if linha[:2] == b"01" and linha[24:27] == b"010":
                        out.write(linha.decode("latin-1").rstrip("\r\n") + "\n")
                        n += 1
    return n


def baixar_cotahist(log=print) -> None:
    pasta = config.RAW / "b3"
    for a in config.ANOS_COTAHIST:
        zp = pasta / f"COTAHIST_A{a}.ZIP"
        gz = pasta / f"COTAHIST_A{a}.txt.gz"
        _, mudou = baixar(B3_SERHIST + zp.name, zp)
        if mudou or not gz.exists():
            n = _filtrar_cotahist(zp, gz)
            log(f"B3 {zp.name}: {n} linhas à vista guardadas em {gz.name}")
        else:
            log(f"B3 {zp.name}: sem mudança")
        if zp.exists():
            zp.unlink()  # ~90 MB: apagar depois de extrair (o meta.json fica)
    # Pregões depois do último dia do anual (o anual do ano corrente costuma vir até o dia anterior).
    ultimo = ultimo_pregao_no_cache()
    d = (ultimo or config.HOJE - timedelta(days=1)) + timedelta(days=1)
    while d < config.HOJE:
        if d.weekday() < 5:
            zp = pasta / f"COTAHIST_D{d:%d%m%Y}.ZIP"
            gz = pasta / f"COTAHIST_D{d:%d%m%Y}.txt.gz"
            try:
                baixar(B3_SERHIST + zp.name, zp)
                _filtrar_cotahist(zp, gz)
                zp.unlink()
                log(f"B3 {zp.name}: ok")
            except FileNotFoundError:
                log(f"B3 {zp.name}: ainda não publicado")
        d += timedelta(days=1)


def ultimo_pregao_no_cache() -> date | None:
    gz = config.RAW / "b3" / f"COTAHIST_A{config.HOJE.year}.txt.gz"
    if not gz.exists():
        return None
    ultimo = ""
    with gzip.open(gz, "rt", encoding="latin-1") as f:
        for linha in f:
            if linha[2:10] > ultimo:
                ultimo = linha[2:10]
    return date(int(ultimo[:4]), int(ultimo[4:6]), int(ultimo[6:8])) if ultimo else None


def baixar_bcb(log=print) -> None:
    fim = config.HOJE
    ini = date(fim.year - 6, 1, 1)  # limite da API: 10 anos por consulta em séries diárias
    for serie, nome in SERIES_BCB.items():
        url = BCB.format(serie=serie, ini=f"{ini:%d/%m/%Y}", fim=f"{fim:%d/%m/%Y}")
        baixar_texto(url, config.RAW / "bcb" / f"sgs_{serie}.json")
        log(f"BCB série {serie} ({nome}): ok")


def baixar_tudo(log=print) -> None:
    baixar_bcb(log)
    baixar_cvm(log)
    baixar_cotahist(log)


if __name__ == "__main__":
    baixar_tudo()
