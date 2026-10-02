"""Linha de comando. Etapas: baixar → normalizar → selecionar → calcular → validar → gerar → publicar.

  python3 -m iec_ativos tudo            # tudo, menos publicar
  python3 -m iec_ativos baixar
  python3 -m iec_ativos normalizar
  python3 -m iec_ativos selecionar
  python3 -m iec_ativos calcular
  python3 -m iec_ativos validar
  python3 -m iec_ativos gerar
  python3 -m iec_ativos publicar --destino pasta --para /caminho   (sftp e cloudflare: ver publicar.py)
"""
import argparse
import json
import sys

from . import config


def _con():
    from .normalizar import conectar
    return conectar()


def cmd_baixar(a):
    from .baixar import baixar_tudo
    baixar_tudo()


def cmd_normalizar(a):
    from . import normalizar as n
    con = _con()
    n.normalizar_cadastro(con)
    n.normalizar_fca(con)
    n.normalizar_cotahist(con)
    n.completar_ativos(con)
    n.normalizar_fii(con)
    n.normalizar_bcb(con)
    con.commit()
    print("normalizado: cadastro, FCA, COTAHIST, FII, BCB (as demonstrações entram depois da seleção)")


def cmd_selecionar(a):
    from .selecionar import selecionar
    from . import normalizar as n
    con = _con()
    sel = selecionar(con)
    (config.CACHE / "selecao.json").write_text(json.dumps(sel, ensure_ascii=False, indent=1))
    cnpjs = {x["cnpj"] for x in sel["acoes"]}
    if sel.get("unit_teste"):
        cnpjs.add(sel["unit_teste"]["cnpj"])
    n.normalizar_demonstracoes(con, cnpjs)
    con.commit()
    print("ações:", ", ".join(x["ticker"] for x in sel["acoes"]))
    print("FIIs:", ", ".join(x["ticker"] for x in sel["fiis"]))
    for nota in sel["notas"]:
        print("nota:", nota)


def _selecao():
    return json.loads((config.CACHE / "selecao.json").read_text())


def cmd_calcular(a):
    from .calcular import calcular_todos
    calcular_todos(_con(), _selecao())


def cmd_validar(a):
    from .validar import validar_todos
    rel = validar_todos(_con(), _selecao())
    bloq = [t for t, r in rel["ativos"].items() if r["bloqueado"]]
    print(f"validação: {len(rel['ativos'])} ativos, {len(bloq)} bloqueados {bloq}")


def cmd_gerar(a):
    from .gerar import gerar_site
    gerar_site(_con(), _selecao())


def cmd_publicar(a):
    from .publicar import publicar
    publicar(a.destino, a.para, simular=a.simular)


def cmd_tudo(a):
    for f in (cmd_baixar, cmd_normalizar, cmd_selecionar, cmd_calcular, cmd_validar, cmd_gerar):
        print(f"== {f.__name__[4:]}")
        f(a)


def main(argv=None):
    p = argparse.ArgumentParser(prog="iec_ativos")
    sub = p.add_subparsers(dest="cmd", required=True)
    for nome in ("baixar", "normalizar", "selecionar", "calcular", "validar", "gerar", "tudo"):
        sub.add_parser(nome)
    pp = sub.add_parser("publicar")
    pp.add_argument("--destino", default="pasta", choices=["pasta", "sftp", "cloudflare"])
    pp.add_argument("--para", default=None, help="pasta de destino (destino=pasta)")
    pp.add_argument("--simular", action="store_true", help="só lista o que mudaria")
    a = p.parse_args(argv)
    globals()[f"cmd_{a.cmd}"](a)


if __name__ == "__main__":
    sys.exit(main())
