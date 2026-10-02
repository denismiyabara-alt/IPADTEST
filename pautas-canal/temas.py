#!/usr/bin/env python3
"""Ranking de assuntos por inscritos esperados por vídeo (longos e Shorts; 12 meses e vitalício) → TEMAS.md.

inscritos esperados por vídeo = views intencionais medianas do assunto × inscritos por mil views intencionais do
assunto (somados). Faixa = p25 e p75 das views intencionais × a mesma taxa. Também mostra os inscritos reais por
vídeo (p25–p75) e de onde vem o tráfego (trafego_por_video.csv, 300 vídeos com mais views).
Assunto = analisar.assunto(título) (regras em auditoria-canal/analisar.py, ASSUNTOS).

uso: python3 temas.py
"""
from pathlib import Path

import modelo as mo
from modelo import an

AQUI = Path(__file__).resolve().parent


def br(x, casas=0):
    if x is None:
        return "—"
    s = f"{x:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def esperado_por_assunto(d, formato, assunto):
    """Inscritos esperados (central, p25, p75, n, fonte) para um assunto: 12 meses se n ≥ 3, senão vitalício,
    senão a média do formato nos 12 meses."""
    for janela in ("12 meses", "vitalício"):
        rk, tot, _ = mo.ranking(d, formato, janela)
        for r in rk:
            if r["assunto"] == assunto and r["ranqueado"]:
                return r["esperado"], r["esperado_p25"], r["esperado_p75"], r["n"], janela
    _, tot, _ = mo.ranking(d, formato, "12 meses")
    return tot["esperado"], tot["esperado_p25"], tot["esperado_p75"], tot["n"], f"todos os {formato}s (12 meses)"


def tabela(d, formato, janela):
    rk, tot, fora = mo.ranking(d, formato, janela)
    casas = 1 if formato == "short" else 0
    L = ["| # | assunto | n | views intencionais (p25 / mediana / p75) | inscritos por mil | **inscritos esperados por vídeo** "
         "(p25–p75) | inscritos reais por vídeo (p25–p75) | % Pesquisa / Navegação (vídeos com dado) | perfil |",
         "|---|---|---|---|---|---|---|---|---|"]
    k = 0
    for r in rk:
        k += 1 if r["ranqueado"] else 0
        L.append(f"| {k if r['ranqueado'] else '—'} | {r['assunto']}{'' if r['ranqueado'] else ' (n < 3, fora do ranking)'} | "
                 f"{r['n']} | {br(r['eng_p25'])} / {br(r['eng_med'])} / {br(r['eng_p75'])} | {br(r['insc_mil'], 1)} | "
                 f"**{br(r['esperado'], casas)}** ({br(r['esperado_p25'], casas)}–{br(r['esperado_p75'], casas)}) | "
                 f"{br(r['insc_p25'])}–{br(r['insc_p75'])} | {br(r.get('pct_busca'))}% / {br(r.get('pct_navegacao'))}% "
                 f"({r.get('n_trafego', 0)}) | {r.get('perfil', '')} |")
    L.append(f"| | **todos** | {tot['n']} | {br(tot['eng_p25'])} / {br(tot['eng_med'])} / {br(tot['eng_p75'])} | "
             f"{br(tot['insc_mil'], 1)} | **{br(tot['esperado'], casas)}** ({br(tot['esperado_p25'], casas)}–"
             f"{br(tot['esperado_p75'], casas)}) | {br(tot['insc_p25'])}–{br(tot['insc_p75'])} | | |")
    if fora:
        L.append(f"\nFora (outlier, ≥ 40% das views do grupo): {', '.join(v['id'] + ' ' + v['titulo'][:50] for v in fora)}.")
    return "\n".join(L)


def conferencia(d, n=20):
    vl, _ = mo.videos(d, "longo", "12 meses")
    L = ["| vídeo | inscritos | assunto (novo) | tema antigo (analisar.tema) | título |", "|---|---|---|---|---|"]
    for v in sorted(vl, key=lambda v: -an.ganhos(v))[:n]:
        L.append(f"| `{v['id']}` | {br(an.ganhos(v))} | {an.assunto(v['titulo'])} | {an.tema(v['titulo'])} | "
                 f"{v['titulo'][:70].replace('|', '/')} |")
    return "\n".join(L)


def markdown(d):
    b = mo.base(d)
    return f"""# Temas: o que traz inscritos (ranking por inscritos esperados por vídeo)

Gerado por `temas.py` com os dados de `auditoria-canal/dados/`. A métrica é **inscritos esperados por vídeo**:
views intencionais medianas do assunto × inscritos por mil views intencionais do assunto. Usamos a mediana, e não a
média, para um vídeo que estoura não fazer o assunto parecer melhor do que é. A faixa vai do p25 ao p75 das views
intencionais.

## Por que um assunto novo ("assunto" no lugar de "tema")

O `tema` do relatório misturava forma e conteúdo: qualquer título com "cuidado" virava "alerta macro". Na conferência
dos 20 longos que mais pesam no resultado (abaixo), o vídeo de Tesouro IPCA+ "CUIDADO… (veja antes do Copom)" caía em
alerta macro, o de NTN-B em plano de renda e o de dividendos todo mês em produto/comparativo. O `assunto` classifica
pelo conteúdo. As regras estão em `auditoria-canal/analisar.py`, na lista `ASSUNTOS`; a ordem importa, e o primeiro que
casar leva. Os 20 foram conferidos à mão e estão no assunto certo. O `tema` antigo continua no analisar.py, porque as
hipóteses do relatório (H2) usam ele.

{conferencia(d)}

## Longos: últimos 12 meses (o ranking que decide a pauta)

{tabela(d, "longo", "12 meses")}

## Longos: vitalício (para ver o que já funcionou, inclusive em busca)

{tabela(d, "longo", "vitalício")}

## Shorts: últimos 12 meses

{tabela(d, "short", "12 meses")}

## Shorts: vitalício

{tabela(d, "short", "vitalício")}

## Leitura

1. **Longos que mais trazem inscritos por vídeo, nos últimos 12 meses:** tesouro e renda fixa, renda mensal, cripto,
   crise e macro e FII. Todos vivem de Navegação (página inicial), ou seja, de picos. O vídeo precisa ser escolhido
   pelo algoritmo na semana em que sai. Dependem de título e thumb mais que de busca.
2. **Ações e empresas** é o assunto mais produzido (28 dos 80 longos do ano) e rende cerca de 30 inscritos por vídeo,
   um terço da renda mensal. É o primeiro lugar de onde tirar espaço.
3. **Imposto e regras, ETF e exterior e juntar dinheiro** rendem pouco como longo novo (de 10 a 16 por vídeo).
   - Juntar dinheiro e ETF/exterior vivem de Pesquisa no vitalício (33% e 37%): pautas de busca perene, melhores como
     Shorts e como vídeo de catálogo.
   - Imposto converte pouco por view (6,5 por mil).
4. **No vitalício,** bancos e contas foi o melhor assunto (193 por vídeo, 67% da Pesquisa). É o conteúdo de 2019 a 2022
   que hoje está, em boa parte, fora do ar (`META.md`, alavanca 4).
5. **Shorts novos trazem de 1 a 4 inscritos cada.** Os melhores em 12 meses são comportamento e família, bancos e
   contas e tesouro. No vitalício, juntar dinheiro, FII e tesouro vivem de Pesquisa (de 33% a 67%). Shorts servem para
   alcance e busca; a conta de inscritos vem dos longos.

## Demanda de busca: o que temos e o que falta

- **Hoje:** só a origem YT_SEARCH do próprio canal, por vídeo, sem os termos. A regra de volume (alto, médio ou baixo)
  está no `CALENDARIO-8-SEMANAS_v1.md`.
- **Termos de busca:** o exportador ganhou a etapa opcional `--termos-busca`. Ela baixa os 25 termos mais buscados por
  mês (12 meses) e no período todo, e os 25 de cada um dos 50 vídeos com mais views da Pesquisa
  (`insightTrafficSourceDetail` com `insightTrafficSourceType==YT_SEARCH`). Comando para o Mac:
  `cd ~/IPADTEST/auditoria-canal && set -a && source ~/.config/investirecocar/credentials.env && set +a && python3 exportar.py --termos-busca`
  Depois, suba `dados/termos_busca_canal.csv` e `dados/termos_busca_por_video.csv`.
- **Autocomplete do YouTube** (`suggestqueries.google.com`): **bloqueado nesta rede** (o proxy recusa o CONNECT com 403).
  Não contornei. Pode ser rodado no Mac, como sinal qualitativo, se o Denis quiser.

Base de hoje para comparação: {br(b['longos_mes_med'])} longos por mês, {br(b['longo']['esperado'])} inscritos esperados
por longo e {br(b['short']['esperado'], 1)} por Short (12 meses).
"""


if __name__ == "__main__":
    d = mo.carregar()
    (AQUI / "TEMAS.md").write_text(markdown(d), encoding="utf-8")
    print("ok: TEMAS.md")
