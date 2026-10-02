"""Leitura das demonstrações de uma empresa já normalizadas no SQLite.

Os códigos de conta mudam entre empresas comuns e bancos (ex.: PL é `2.03` na Petrobras e `2.08` no
Itaú; lucro é `3.11` numa e `3.09` noutra). Por isso as contas são achadas pela descrição (DS_CONTA),
com o código fixo só como atalho. Achado do primeiro download real.
"""
import re
from dataclasses import dataclass
from datetime import date, timedelta


@dataclass
class Linha:
    id: int
    doc: str
    dem: str
    dt_refer: str
    dt_ini: str | None
    dt_fim: str
    ordem: str
    versao: int
    cd: str
    ds: str
    valor: float


def _norm(txt: str) -> str:
    import unicodedata
    t = unicodedata.normalize("NFKD", txt or "").encode("ascii", "ignore").decode().lower()
    return re.sub(r"\s+", " ", t).strip()


def nivel(cd: str) -> int:
    return cd.count(".") + 1


def mais_um_dia(d: str) -> str:
    return (date.fromisoformat(d) + timedelta(days=1)).isoformat()


def menos_um_ano(d: str) -> str:
    x = date.fromisoformat(d)
    try:
        return x.replace(year=x.year - 1).isoformat()
    except ValueError:  # 29/02
        return x.replace(year=x.year - 1, day=28).isoformat()


class Demonstracoes:
    """Todas as linhas (maior versão) de uma empresa, num escopo (con ou ind)."""

    def __init__(self, con, cnpj: str):
        self.cnpj = cnpj
        n_con = con.execute("SELECT COUNT(*) FROM conta WHERE cnpj=? AND escopo='con' AND demonstracao='DRE'",
                            (cnpj,)).fetchone()[0]
        self.escopo = "con" if n_con else "ind"
        self.linhas: dict[tuple, list[Linha]] = {}
        for r in con.execute("""SELECT id, doc, demonstracao, dt_refer, dt_ini_exerc, dt_fim_exerc, ordem_exerc, versao,
                                cd_conta, ds_conta, valor_reais FROM conta WHERE cnpj=? AND escopo=?""",
                             (cnpj, self.escopo)):
            ln = Linha(*r)
            self.linhas.setdefault((ln.doc, ln.dt_refer, ln.dem), []).append(ln)
        self.docs = sorted({(k[0], k[1]) for k in self.linhas}, key=lambda d: (d[1], d[0]))
        self.documentos = {(r[0], r[1]): {"versao": r[2], "dt_receb": r[3], "link": r[4], "id_doc": r[5]}
                           for r in con.execute("""SELECT doc, dt_refer, versao, dt_receb, link, id_doc FROM documento
                                                    WHERE cnpj=?""", (cnpj,))}

    # ------------------------------------------------------------------ documentos
    def ultimo_doc(self) -> tuple[str, str] | None:
        """(doc, dt_refer) mais recente que tenha DRE."""
        com_dre = [d for d in self.docs if (d[0], d[1], "DRE") in self.linhas]
        return com_dre[-1] if com_dre else None

    def doc_em(self, dt_refer: str) -> tuple[str, str] | None:
        for d in reversed(self.docs):
            if d[1] == dt_refer and (d[0], d[1], "DRE") in self.linhas:
                return d
        return None

    def inicio_exercicio(self, doc: str, dt_refer: str) -> str | None:
        ls = [x for x in self.linhas.get((doc, dt_refer, "DRE"), []) if x.ordem == "ULTIMO" and x.dt_ini]
        return min(x.dt_ini for x in ls) if ls else None

    def rotulo_doc(self, doc: str, dt_refer: str) -> str:
        d = date.fromisoformat(dt_refer)
        if doc == "DFP":
            nome = f"DFP {d.year}"
        else:
            nome = f"ITR {(d.month - 1) // 3 + 1}T{str(d.year)[2:]}"
        info = self.documentos.get((doc, dt_refer), {})
        esc = "consolidado" if self.escopo == "con" else "individual"
        partes = [f"CVM, {nome} {esc}"]
        if info.get("versao"):
            partes.append(f"versão {info['versao']}")
        if info.get("dt_receb"):
            partes.append(f"entregue em {_br(info['dt_receb'])}")
        return ", ".join(partes)

    # ------------------------------------------------------------------ resolução de contas
    def achar(self, doc: str, dt_refer: str, dem: str, regra: str) -> str | None:
        """Devolve o código da conta que segue a `regra` naquele documento."""
        dems = ["DFC_MI", "DFC_MD"] if dem == "DFC" else [dem]
        ls = [x for d in dems for x in self.linhas.get((doc, dt_refer, d), [])]
        cods = {x.cd: _norm(x.ds) for x in ls}
        return resolver(regra, cods)

    def lista(self, doc, dt_refer, dem, regra) -> list[str]:
        dems = ["DFC_MI", "DFC_MD"] if dem == "DFC" else [dem]
        ls = [x for d in dems for x in self.linhas.get((doc, dt_refer, d), [])]
        cods = {x.cd: _norm(x.ds) for x in ls}
        return resolver_lista(regra, cods)

    def _linhas(self, doc, dt_refer, dem):
        if dem == "DFC":
            return self.linhas.get((doc, dt_refer, "DFC_MI"), []) + self.linhas.get((doc, dt_refer, "DFC_MD"), [])
        return self.linhas.get((doc, dt_refer, dem), [])

    def valor(self, doc, dt_refer, dem, cd, ordem="ULTIMO", dt_ini=None) -> tuple[float | None, list[int]]:
        for x in self._linhas(doc, dt_refer, dem):
            if x.cd == cd and x.ordem == ordem and (dt_ini is None or x.dt_ini == dt_ini):
                return x.valor, [x.id]
        return None, []

    def soma_regra(self, doc, dt_refer, dem, regra, ordem="ULTIMO", dt_ini=None):
        cods = self.lista(doc, dt_refer, dem, regra)
        tot, ids, achou = 0.0, [], False
        for cd in cods:
            v, i = self.valor(doc, dt_refer, dem, cd, ordem, dt_ini)
            if v is not None:
                tot += v
                ids += i
                achou = True
        return (tot if achou else None), ids

    # ------------------------------------------------------------------ fluxos (DRE, DFC, DVA)
    def acumulado(self, doc, dt_refer, dem, regra, ordem="ULTIMO"):
        """Valor acumulado no exercício (do início do exercício até dt_refer)."""
        ini = self.inicio_exercicio(doc, dt_refer)
        if ini is None:
            return None, []
        if ordem == "PENULTIMO":
            ini = menos_um_ano(ini)
        if regra.startswith("soma:"):
            return self.soma_regra(doc, dt_refer, dem, regra[5:], ordem, ini)
        cd = self.achar(doc, dt_refer, dem, regra)
        if cd is None:
            return None, []
        return self.valor(doc, dt_refer, dem, cd, ordem, ini)

    def ttm(self, dt_refer: str, dem: str, regra: str) -> dict:
        """12 meses móveis até dt_refer (DESENHO 4.3). Devolve valor, ids dos insumos e a explicação."""
        d = self.doc_em(dt_refer)
        if d is None:
            return {"valor": None, "motivo": "sem documento nessa data"}
        doc, ref = d
        if doc == "DFP":
            v, ids = self.acumulado(doc, ref, dem, regra)
            return {"valor": v, "insumos": ids, "pecas": [f"DFP {ref[:4]}"], "fim": ref}
        ini = self.inicio_exercicio(doc, ref)
        fim_ant = (date.fromisoformat(ini) - timedelta(days=1)).isoformat()
        if ("DFP", fim_ant, "DRE") not in self.linhas:
            return {"valor": None, "motivo": f"falta a DFP de {fim_ant[:4]}"}
        a, ia = self.acumulado("DFP", fim_ant, dem, regra)
        b, ib = self.acumulado(doc, ref, dem, regra, "ULTIMO")
        c, ic = self.acumulado(doc, ref, dem, regra, "PENULTIMO")
        if None in (a, b, c):
            return {"valor": None, "motivo": "conta ausente em uma das peças"}
        return {"valor": a + b - c, "insumos": ia + ib + ic, "fim": ref,
                "pecas": [f"DFP {fim_ant[:4]}", f"+ acumulado {self.rotulo_curto(doc, ref)}",
                          f"- mesmo período de {int(ref[:4]) - 1} (reapresentado no {self.rotulo_curto(doc, ref)})"]}

    def rotulo_curto(self, doc, dt_refer) -> str:
        d = date.fromisoformat(dt_refer)
        return f"DFP {d.year}" if doc == "DFP" else f"ITR {(d.month - 1) // 3 + 1}T{str(d.year)[2:]}"

    def trimestre(self, dt_refer: str, dem: str, regra: str) -> float | None:
        """Valor só do trimestre que termina em dt_refer. 4º trimestre = DFP - 9 meses (ITR 3T)."""
        d = self.doc_em(dt_refer)
        if d is None:
            return None
        doc, ref = d
        if doc == "ITR":
            dr = date.fromisoformat(ref)
            ini_tri = date(dr.year, dr.month - 2, 1).isoformat() if dr.month >= 3 else None
            ini_exe = self.inicio_exercicio(doc, ref)
            if ini_exe == ini_tri:
                return self.acumulado(doc, ref, dem, regra)[0]
            if dem == "DRE":
                cd = self.achar(doc, ref, dem, regra)
                return self.valor(doc, ref, dem, cd, "ULTIMO", ini_tri)[0] if cd else None
            ant = self._ref_trimestre_anterior(ref)
            a = self.acumulado(doc, ref, dem, regra)[0]
            b = self.acumulado(*self.doc_em(ant), dem, regra)[0] if self.doc_em(ant) else None
            return None if None in (a, b) else a - b
        # DFP: 4º trimestre derivado
        nove = self._ref_trimestre_anterior(ref)
        d9 = self.doc_em(nove)
        if d9 is None:
            return None
        a = self.acumulado(doc, ref, dem, regra)[0]
        b = self.acumulado(*d9, dem, regra)[0]
        return None if None in (a, b) else a - b

    @staticmethod
    def _ref_trimestre_anterior(ref: str) -> str:
        d = date.fromisoformat(ref).replace(day=1) - timedelta(days=62)
        # último dia do mês
        prox = (d.replace(day=28) + timedelta(days=4)).replace(day=1)
        return (prox - timedelta(days=1)).isoformat()

    # ------------------------------------------------------------------ balanço
    def saldo(self, dt_refer: str, dem: str, regra: str):
        d = self.doc_em(dt_refer)
        if d is None:
            return None, []
        if regra.startswith("soma:"):
            return self.soma_regra(d[0], d[1], dem, regra[5:])
        cd = self.achar(d[0], d[1], dem, regra)
        return self.valor(d[0], d[1], dem, cd) if cd else (None, [])


def _br(iso: str) -> str:
    return f"{iso[8:10]}/{iso[5:7]}/{iso[:4]}" if iso and len(iso) >= 10 else iso


# ---------------------------------------------------------------------- regras de busca

def _filhos(cods: dict, pai: str) -> list[str]:
    return [c for c in cods if c.startswith(pai + ".") and nivel(c) == nivel(pai) + 1]


def resolver(regra: str, cods: dict[str, str]) -> str | None:
    """`cods` = {cd_conta: descrição normalizada}. Regras com nome; cada uma documentada."""
    if regra == "receita":
        return "3.01" if "3.01" in cods else None
    if regra == "ebit":  # Resultado Antes do Resultado Financeiro e dos Tributos (não existe em banco)
        for c, d in cods.items():
            if nivel(c) == 2 and d.startswith("resultado antes do resultado financeiro"):
                return c
        return None
    if regra == "lucro_total":
        for c, d in sorted(cods.items()):
            if nivel(c) == 2 and re.match(r"(lucro|prejuizo)[/ ]*(prejuizo|lucro)? ?(consolidado )?do periodo", d):
                return c
        return None
    if regra == "lucro_controladora":
        tot = resolver("lucro_total", cods)
        if tot is None:
            return None
        for c in _filhos(cods, tot):
            if "controladora" in cods[c]:
                return c
        return tot  # demonstração individual: o lucro todo é da controladora
    if regra == "lucro_nao_controladores":
        tot = resolver("lucro_total", cods)
        for c in _filhos(cods, tot) if tot else []:
            if "nao controladores" in cods[c]:
                return c
        return None
    if regra == "pl_total":
        for c, d in sorted(cods.items()):
            if nivel(c) == 2 and c.startswith("2.") and "patrimonio liquido" in d:
                return c
        return None
    if regra == "pl_nao_controladores":
        pl = resolver("pl_total", cods)
        for c in _filhos(cods, pl) if pl else []:
            if "nao controladores" in cods[c]:
                return c
        return None
    if regra == "ativo_total":
        return "1" if "1" in cods else None
    if regra == "passivo_total":
        return "2" if "2" in cods else None
    if regra == "caixa":
        return "1.01.01" if cods.get("1.01.01", "").startswith("caixa") else None
    if regra == "aplicacoes":
        return "1.01.02" if "aplicac" in cods.get("1.01.02", "") else None
    if regra == "da":  # DVA: Depreciação, Amortização e Exaustão (7.04.01 em empresa comum; 7.05.01 em banco)
        for c, d in sorted(cods.items()):
            if c.startswith("7.") and nivel(c) == 3 and "deprecia" in d:
                return c
        return None
    if regra == "lpa_on":
        return "3.99.01.01" if "3.99.01.01" in cods else None
    if regra == "lpa_pn":
        return "3.99.01.02" if "3.99.01.02" in cods else None
    raise KeyError(regra)


PROVENTO = re.compile(r"dividend|juros sobre (o )?capital|jcp|juros s/ ?(o )?capital")


def resolver_lista(regra: str, cods: dict[str, str]) -> list[str]:
    if regra == "divida_bruta":  # Empréstimos e Financiamentos circulante + não circulante
        return [c for c in ("2.01.04", "2.02.01") if "emprestimos e financiamentos" in cods.get(c, "")]
    if regra == "arrendamento":
        # contas com "arrendamento" no passivo (circulante e não circulante), sem contar filho e pai juntos
        achadas = sorted(c for c, d in cods.items()
                         if (c.startswith("2.01.") or c.startswith("2.02.")) and "arrendamento" in d
                         and "direito de uso" not in d)
        return [c for c in achadas if not any(c.startswith(p + ".") for p in achadas if p != c)]
    if regra == "arrendamento_dentro_da_divida":
        dentro = resolver_lista("divida_bruta", cods)
        return [c for c in resolver_lista("arrendamento", cods) if any(c.startswith(p + ".") for p in dentro)]
    if regra == "proventos_pagos":
        # DFC, atividades de financiamento (6.03): dividendos e JCP pagos aos acionistas da empresa.
        # Fica de fora o que foi pago a não controladores (não é provento do acionista da empresa).
        achadas = sorted(c for c, d in cods.items()
                         if c.startswith("6.03.") and PROVENTO.search(d) and "nao controladores" not in d
                         and "recebid" not in d)
        return [c for c in achadas if not any(c.startswith(p + ".") for p in achadas if p != c)]
    if regra == "da_dfc":
        return [c for c, d in cods.items() if c.startswith("6.01.01.") and re.search(r"deprecia|amortiza|exaust", d)
                and "arrendamento" not in d]
    raise KeyError(regra)
