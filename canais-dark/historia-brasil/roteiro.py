"""Formato de episódio do canal de história: roteiro.md <-> blocos.py (o mesmo formato do canal irmão, sem mudança de regra).

    python3 roteiro.py <pasta>/roteiro.md          # valida e mostra o resumo
    python3 roteiro.py --de-blocos <pasta>         # converte um blocos.py antigo em roteiro.md
"""
import ast
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

GAP_PADRAO = 0.40
GAP_PAUSA = 0.75
STATUS_OK = {"conferido", "calculado"}
# Aceita "## B1 — CONTA", "## B1 - CONTA", "## B1: CONTA", "## B1 CONTA" e "## B1".
RE_BLOCO = re.compile(r"^##\s+(B\d+)\b\s*(?:[—–:\-]+\s*)?(.*?)\s*$", re.I)
# Qualquer cabeçalho "## B<n>..." que não case com RE_BLOCO é erro (não pode sumir em silêncio).
RE_QUASE_BLOCO = re.compile(r"^##\s+B\d", re.I)
RE_COMENTARIO = re.compile(r"<!--.*?(?:-->|\Z)", re.S)
RE_GAP = re.compile(r"\s*\{(\d+(?:[.,]\d+)?)\}\s*$")


@dataclass
class Roteiro:
    titulo: str = ""
    numeros: list = field(default_factory=list)
    notas: str = ""
    blocos: dict = field(default_factory=dict)
    titulos: dict = field(default_factory=dict)

    @property
    def ordem(self):
        return list(self.blocos)


def _frase(linha):
    """'Texto. ⏸ {0.95}' -> ('Texto.', 0.95). Sem {x}: ⏸ vale 0.75, senão 0.40."""
    gap = None
    m = RE_GAP.search(linha)
    if m:
        gap = float(m.group(1).replace(",", "."))
        linha = linha[:m.start()]
    pausa = "⏸" in linha
    texto = linha.replace("⏸", "").strip()
    return texto, gap if gap is not None else (GAP_PAUSA if pausa else GAP_PADRAO)


def ler(caminho):
    r, secao, bloco = Roteiro(), None, None
    notas = []
    texto = Path(caminho).read_text(encoding="utf-8")
    # comentários HTML (inclusive multilinha, ou sem fechar) saem por inteiro antes de ler as linhas
    texto = RE_COMENTARIO.sub("", texto)
    for bruta in texto.splitlines():
        linha = bruta.strip()
        if linha.startswith("# ") and not r.titulo:
            r.titulo = linha[2:].strip()
            continue
        m = RE_BLOCO.match(linha)
        if m:
            bloco = m.group(1).lower()
            if bloco in r.blocos:
                raise ValueError(f"bloco {bloco} repetido")
            r.blocos[bloco], r.titulos[bloco], secao = [], (m.group(2) or "").strip(), "bloco"
            continue
        if RE_QUASE_BLOCO.match(linha):
            raise ValueError(f"cabeçalho de bloco não reconhecido: {linha!r} (use '## B0 — TÍTULO')")
        if linha.startswith("## "):
            nome = linha[3:].strip().lower()
            secao = "numeros" if nome.startswith("números") or nome.startswith("numeros") else "notas" if nome.startswith("notas") else "outra"
            bloco = None
            continue
        if not linha:
            continue
        if secao == "numeros" and linha.startswith("|"):
            cel = [c.strip() for c in linha.strip("|").split("|")]
            if cel[0].lower() == "id" or all(set(c) <= set("-: ") for c in cel):
                continue  # cabeçalho ou separador do quadro
            if len(cel) >= 4:
                r.numeros.append({"id": cel[0], "numero": cel[1], "fonte": cel[2], "status": cel[3].lower()})
            else:
                # linha incompleta conta como pendente: a trava falha FECHADA
                r.numeros.append({"id": cel[0] or linha, "numero": cel[1] if len(cel) > 1 else "",
                                  "fonte": cel[2] if len(cel) > 2 else "",
                                  "status": f"linha incompleta ({len(cel)} de 4 colunas)"})
        elif secao == "notas":
            notas.append(bruta.rstrip())
        elif secao == "bloco" and not linha.startswith(("*", ">")):
            r.blocos[bloco].append(_frase(linha))
    r.notas = "\n".join(notas).strip()
    if not r.blocos:
        raise ValueError("nenhum bloco '## B0 — ...' encontrado")
    return r


def validar(r):
    """Avisos (não travam): regras de voz e de conferência."""
    avisos = []
    for b, frases in r.blocos.items():
        if not frases:
            avisos.append(f"{b}: bloco vazio")
        for texto, _ in frases:
            if re.match(r"^\W*\d", texto):
                avisos.append(f"{b}: frase começa com número (regra de voz): {texto[:40]!r}")
            elif re.search(r"\d", texto):
                avisos.append(f"{b}: número em algarismo; escreva por extenso para a voz: {texto[:40]!r}")
    for n in r.numeros:
        if n["status"] not in STATUS_OK:
            avisos.append(f"número '{n['id']}' está '{n['status']}'")
        if not n["fonte"]:
            avisos.append(f"número '{n['id']}' sem fonte")
    return avisos


def para_blocos_py(r):
    cab = [f"{r.titulo} — gerado de roteiro.md por fazer.py. NÃO edite à mão: edite o roteiro.md."]
    if r.numeros:
        cab.append("")
        cab += [f"{n['id']}: {n['numero']} ({n['fonte']}) [{n['status']}]" for n in r.numeros]
    if r.notas:
        cab += ["", r.notas]
    doc = "\n".join(cab).replace('"""', "'''")
    linhas = [f'"""{doc}\n"""', "", "BLOCOS = {"]
    for b, frases in r.blocos.items():
        linhas.append(f'"{b}": [')
        linhas += [f"    ({texto!r}, {gap:.2f})," for texto, gap in frases]
        linhas.append("],")
    linhas.append("}")
    return "\n".join(linhas) + "\n"


def de_blocos_py(pasta, titulo=None, numeros=None):
    """Converte o blocos.py de um episódio antigo para roteiro.md (sem perder frase nem pausa)."""
    pasta = Path(pasta)
    fonte = (pasta / "blocos.py").read_text(encoding="utf-8")
    arvore = ast.parse(fonte)
    doc = ast.get_docstring(arvore) or ""
    blocos = next(ast.literal_eval(n.value) for n in arvore.body
                  if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "BLOCOS" for t in n.targets))
    antigo = next(pasta.glob("ROTEIRO-*.md"), None)
    titulos = {}
    if antigo:
        for linha in antigo.read_text(encoding="utf-8").splitlines():
            m = RE_BLOCO.match(linha.strip())
            if m:
                titulos[m.group(1).lower()] = (m.group(2) or "").strip()
    out = [f"# {titulo or pasta.name.upper()}", "", "## Números conferidos", "",
           "| id | número | conta ou fonte | status |", "|---|---|---|---|"]
    out += [f"| {n['id']} | {n['numero']} | {n['fonte']} | {n['status']} |" for n in (numeros or [])]
    out += ["", "## Notas", "", doc, ""]
    for b, frases in blocos.items():
        out += [f"## {b.upper()} — {titulos.get(b, '')}".rstrip(" —"), ""]
        for texto, gap in frases:
            if abs(gap - GAP_PADRAO) < 1e-9:
                sufixo = ""
            elif abs(gap - GAP_PAUSA) < 1e-9:
                sufixo = "  ⏸"
            else:
                sufixo = f"  ⏸ {{{gap:.2f}}}" if gap >= 0.6 else f"  {{{gap:.2f}}}"
            out.append(texto + sufixo)
        out.append("")
    return "\n".join(out)


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--de-blocos":
        print(de_blocos_py(sys.argv[2]))
    elif len(sys.argv) == 2:
        r = ler(sys.argv[1])
        print(f"{r.titulo}: {len(r.blocos)} blocos, {sum(map(len, r.blocos.values()))} frases, "
              f"{len(r.numeros)} números ({sum(n['status'] in STATUS_OK for n in r.numeros)} ok)")
        for a in validar(r):
            print("  aviso:", a)
    else:
        sys.exit(__doc__)
