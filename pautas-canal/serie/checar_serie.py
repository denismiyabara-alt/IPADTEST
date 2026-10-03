"""Checagem da série de renda mensal e do molde do Copom.

Uso:  python3 checar_serie.py            (sai com 1 se algo falhar)
      GATE_DIR=/caminho/pipeline python3 checar_serie.py

O que confere:
1. todo título (os 6 de busca, as 12 alternativas e os títulos fechados do molde) tem até 60 caracteres, não usa
   "vale a pena" nem "qual a melhor" e passa nas checagens de título do gate (recomendação, corretora e ticker);
2. os 3 arquivos .md passam no gate inteiro sem BLOQUEANTE (avisos são listados, não falham);
3. toda lacuna [ASSIM] do roteiro-molde está documentada na tabela de fontes (seção 1);
4. as datas do Copom são pares terça-quarta e os episódios caem em quartas, um por semana, fora da semana do Copom.

O gate (`gate_qualidade.py`) é só importado: nada nele é alterado.
"""
import datetime as dt
import os
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
GATE_DIR = Path(os.environ.get("GATE_DIR", "/home/user/investir-e-cocar/pipeline"))
SERIE = AQUI / "SERIE-RENDA-MENSAL.md"
MOLDE = AQUI / "MOLDE-TESOURO-COPOM.md"
PROPOSTA = AQUI / "PROPOSTA-CALENDARIO-V3.md"
LIMITE = 60
PROIBIDO = re.compile(r"vale(m)? a pena|qual (é |e )?a melhor", re.I)

falhas = []


def falha(msg):
    falhas.append(msg)
    print("FALHA:", msg)


def carregar_gate():
    sys.path.insert(0, str(GATE_DIR))
    try:
        import gate_qualidade as g  # noqa: E402
    except ImportError as e:
        falha(f"não consegui importar o gate em {GATE_DIR}: {e}")
        return None
    return g


def titulos_da_serie(texto):
    out = []
    for linha in texto.splitlines():
        if linha.startswith("- **Título de busca:**") or linha.startswith("- **Alternativas:**"):
            out += re.findall(r"`([^`]+)`", linha)
    return out


def titulos_do_molde(texto):
    bloco = texto.split("**Título (até 60 caracteres, escolher um):**", 1)[1].split("\n\n", 1)[0]
    # só os títulos fechados; os com [LACUNA] são contados depois de preenchidos
    return [t for t in re.findall(r"`([^`]+)`", bloco) if "[" not in t]


def checar_titulos(g, titulos):
    for t in titulos:
        if len(t) > LIMITE:
            falha(f"título com {len(t)} caracteres (> {LIMITE}): {t}")
        if PROIBIDO.search(t):
            falha(f'título com expressão barrada ("vale a pena"/"qual a melhor"): {t}')
        if g:
            post = g.Post(t, "", "md")
            probs = g.checar_recomendacao(post) + g.checar_corretora(post) + g.checar_tickers(post)
            for p in probs:
                falha(f"gate no título [{p['nivel']} {p['codigo']}]: {t} — {p['mensagem']}")
    print(f"títulos conferidos: {len(titulos)}")


def checar_arquivos_no_gate(g, hoje):
    for arq in (SERIE, MOLDE, PROPOSTA):
        post = g.Post("", arq.read_text(encoding="utf-8"), "md", hoje)
        r = g.avaliar(post)
        print(f"gate em {arq.name}: {r['resultado']} ({r['bloqueantes']} bloqueante(s), {r['avisos']} aviso(s), "
              f"padrão de IA {r['pontos_ia']} pts)")
        for p in r["problemas"]:
            linha = f"   [{p['nivel']}] {p['codigo']}: {p['mensagem']} | {p.get('trecho', '')[:140]}"
            if p["nivel"] == g.BLOQ:
                falha(f"{arq.name}:{linha}")
            else:
                print(linha)


def checar_lacunas(texto):
    sec1 = texto.split("## 1.", 1)[1].split("## 2.", 1)[0]
    sec3 = texto.split("## 3.", 1)[1].split("## 4.", 1)[0]
    usadas = sorted(set(re.findall(r"\[([A-Z][A-Z0-9_]+)\]", sec3)))
    for nome in usadas:
        if nome.startswith("DIF_"):
            continue  # conta: depois − antes (documentada na seção 1)
        base = re.sub(r"_(ANTES|DEPOIS)$", "", nome)
        ok = (f"[{nome}]" in sec1 or f"[{base}_ANTES/DEPOIS]" in sec1
              or any(f"[{p}_*]" in sec1 for p in [nome.split("_")[0]]))
        if not ok:
            falha(f"lacuna [{nome}] do roteiro não está na tabela de fontes")
    print(f"lacunas do roteiro conferidas: {len(usadas)}")


def checar_datas(molde, serie):
    sec6 = molde.split("## 6.", 1)[1]
    pares = []
    for d1, d2, m, a in re.findall(r"ter (\d{2}) e qua (\d{2})/(\d{2})/(\d{4})", sec6):
        pares.append((dt.date(int(a), int(m), int(d1)), dt.date(int(a), int(m), int(d2))))
    linha27 = next(l for l in sec6.splitlines() if l.startswith("| 2027 |"))
    for d1, d2, m in re.findall(r"(\d{2})-(\d{2})/(\d{2})", linha27.split("|")[2]):
        pares.append((dt.date(2027, int(m), int(d1)), dt.date(2027, int(m), int(d2))))
    for a, b in pares:
        if a.weekday() != 1 or b != a + dt.timedelta(days=1):
            falha(f"reunião do Copom fora do padrão terça-quarta: {a} e {b}")
    print(f"reuniões do Copom conferidas: {len(pares)} (2026: {sum(p[0].year == 2026 for p in pares)}, "
          f"2027: {sum(p[0].year == 2027 for p in pares)})")

    eps = [dt.date(2026, int(m), int(d)) for d, m in re.findall(r"^## Ep\. \d · quarta (\d{2})/(\d{2})/2026", serie, re.M)]
    if len(eps) != 6:
        falha(f"esperava 6 episódios com data, achei {len(eps)}")
    semanas = [e.isocalendar()[1] for e in eps]
    if len(set(semanas)) != len(semanas):
        falha("dois episódios na mesma semana")
    for e in eps:
        if e.weekday() != 2:
            falha(f"episódio fora da quarta: {e}")
        for a, _ in pares:
            if a.isocalendar()[:2] == e.isocalendar()[:2]:
                falha(f"episódio {e} cai na semana do Copom ({a})")
    print(f"episódios conferidos: {len(eps)}")


def main():
    hoje = dt.date.today().isoformat()
    g = carregar_gate()
    serie = SERIE.read_text(encoding="utf-8")
    molde = MOLDE.read_text(encoding="utf-8")
    titulos = titulos_da_serie(serie)
    if len(titulos) != 18:
        falha(f"esperava 18 títulos na série (6 + 12 alternativas), achei {len(titulos)}")
    checar_titulos(g, titulos + titulos_do_molde(molde))
    if g:
        checar_arquivos_no_gate(g, hoje)
    checar_lacunas(molde)
    checar_datas(molde, serie)
    print("\nOK" if not falhas else f"\n{len(falhas)} falha(s)")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
