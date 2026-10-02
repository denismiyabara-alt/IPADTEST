# Temas: o que traz inscritos (ranking por inscritos esperados por vídeo)

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

| vídeo | inscritos | assunto (novo) | tema antigo (analisar.tema) | título |
|---|---|---|---|---|
| `Fb0l4KEq27o` | 637 | renda mensal | plano de renda | 6 ETFs que MAIS PAGARAM DIVIDENDOS MENSAIS em 2025 e devem continuar e |
| `dHYQtxnMSrw` | 421 | tesouro e renda fixa | plano de renda | ÚLTIMA CHANCE de GANHAR MUITO DINHEIRO na RENDA FIXA (NTN-B IPCA+7%) |
| `IcN3m7whpl8` | 357 | crise e macro | alerta macro | Esse Gráfico Acertou as CRISES 1929, 2008 e 2020… Agora Ele Aponta CRI |
| `tpobf1e1OtM` | 345 | crise e macro | alerta macro | A Crise Já Está Acontecendo (e Só os Espertos Estão Vendo) |
| `TY8oLvUt2Qg` | 324 | renda mensal | produto / comparativo | RECEBA DIVIDENDOS TODOS os MESES de AÇÕES SEGURAS (mesmo começando do  |
| `lt2LWbwu3mc` | 255 | commodities | outros | O COBRE É O NOVO PETRÓLEO? Descubra Antes que Dispare (MAIS)! Vale a P |
| `KMIsVEOcaLM` | 246 | tesouro e renda fixa | alerta macro | CUIDADO com Tesouro Direto IPCA+ 8,32% (veja antes do Copom) |
| `JDtxzQthFlk` | 224 | cripto | alerta macro | MORTE DO BITCOIN? O ALERTA QUE O MERCADO NÃO QUER OUVIR |
| `tb0nwpl9mFw` | 142 | tesouro e renda fixa | alerta macro | NÃO INVISTA no TESOURO DIRETO AGORA SEM SABER DISSO (CUIDADO) |
| `IB1mBcF00jc` | 131 | renda mensal | plano de renda | ETF JEPI39 PAGA DIVIDENDOS MENSAIS, mas vale a pena? |
| `GpdXuQipVaQ` | 115 | ações e empresas | outros | A Klabin ia pagar dívida — e torrou meio bilhão na própria ação |
| `eZE1d_CHlPU` | 101 | cripto | produto / comparativo | Qual é o Melhor ETF de Bitcoin para Investir em 2025? |
| `lwV6tbkk4Cw` | 93 | renda mensal | plano de renda | DIVIDENDOS MENSAIS: ETF de Dividendos Sintéticos ou Fundo Imobiliário? |
| `Gjw4crGh6Xg` | 92 | FII | produto / comparativo | Por que os RICOS NÃO INVESTEM em Fundos Imobiliários (e o que isso sig |
| `fwWG6AIP52Q` | 88 | ações e empresas | caso com nome | Se você é JOVEM DEVERIA INVESTIR em AÇÕES / Como investe Nicolas Agnez |
| `PWotyrtMXBs` | 84 | crise e macro | alerta macro | Os Sinais de Alerta da Crise que Ninguém Está Levando a Sério |
| `qnWje5V23Ps` | 77 | imposto e regras | alerta macro | Dividendos Tributados! Veja o impacto da nova lei no seu bolso |
| `HqLOOtyyGR0` | 75 | FII | produto / comparativo | Se você INVESTE em FUNDOS IMOBILIÁRIOS deveria ENTENDER isso (+4 fundo |
| `6FxiU14JAVE` | 73 | ações e empresas | produto / comparativo | IPO da SPACEX: A Maior Oportunidade da Década ou Cilada? (SPCX, SPCX34 |
| `UA3rJPz7IVk` | 64 | ações e empresas | alerta macro | 20 ações prontas para explodir em dividendos – antes do governo morder |

## Longos: últimos 12 meses (o ranking que decide a pauta)

| # | assunto | n | views intencionais (p25 / mediana / p75) | inscritos por mil | **inscritos esperados por vídeo** (p25–p75) | inscritos reais por vídeo (p25–p75) | % Pesquisa / Navegação (vídeos com dado) | perfil |
|---|---|---|---|---|---|---|---|---|
| 1 | tesouro e renda fixa | 5 | 9.695 / 17.840 / 19.302 | 11,0 | **195** (106–212) | 46–246 | 6% / 60% (4) | Navegação (pico) |
| 2 | renda mensal | 7 | 4.952 / 6.527 / 19.113 | 13,9 | **91** (69–267) | 26–228 | 19% / 58% (3) | Navegação (pico) |
| 3 | cripto | 4 | 4.662 / 7.688 / 15.444 | 7,6 | **58** (35–117) | 32–132 | 11% / 55% (2) | Navegação (pico) |
| 4 | crise e macro | 12 | 1.971 / 5.870 / 8.565 | 8,8 | **52** (17–75) | 5–62 | 3% / 68% (4) | Navegação (pico) |
| 5 | FII | 6 | 3.468 / 6.028 / 7.430 | 7,5 | **45** (26–56) | 24–66 | 4% / 81% (3) | Navegação (pico) |
| 6 | ações e empresas | 28 | 3.012 / 4.212 / 5.698 | 7,2 | **30** (22–41) | 13–48 | 2% / 68% (4) | Navegação (pico) |
| 7 | imposto e regras | 5 | 2.475 / 2.497 / 6.774 | 6,5 | **16** (16–44) | 12–44 | 5% / 69% (1) | Navegação (pico) |
| 8 | outros | 4 | 2.406 / 2.900 / 3.567 | 5,0 | **15** (12–18) | 8–24 | —% / —% (0) | sem dado |
| 9 | juntar dinheiro e aposentadoria | 3 | 2.976 / 3.735 / 9.558 | 3,8 | **14** (11–37) | 10–36 | 3% / 78% (1) | Navegação (pico) |
| 10 | ETF e exterior | 5 | 2.238 / 2.270 / 2.902 | 4,4 | **10** (10–13) | 8–15 | —% / —% (0) | sem dado |
| — | commodities (n < 3, fora do ranking) | 1 | 15.288 / 15.288 / 15.288 | 16,7 | **255** (255–255) | 255–255 | 15% / 53% (1) | Navegação (pico) |
| | **todos** | 80 | 2.526 / 4.652 / 7.600 | 9,1 | **42** (23–69) | 13–62 | | |

## Longos: vitalício (para ver o que já funcionou, inclusive em busca)

| # | assunto | n | views intencionais (p25 / mediana / p75) | inscritos por mil | **inscritos esperados por vídeo** (p25–p75) | inscritos reais por vídeo (p25–p75) | % Pesquisa / Navegação (vídeos com dado) | perfil |
|---|---|---|---|---|---|---|---|---|
| 1 | bancos e contas | 53 | 6.456 / 12.408 / 32.430 | 15,5 | **193** (100–504) | 69–648 | 67% / 8% (36) | Pesquisa (perene) |
| 2 | renda mensal | 36 | 3.068 / 6.056 / 17.572 | 18,6 | **112** (57–326) | 22–211 | 24% / 50% (14) | misto |
| 3 | FII | 60 | 3.198 / 5.664 / 9.206 | 14,6 | **83** (47–135) | 26–123 | 11% / 59% (23) | Navegação (pico) |
| 4 | cripto | 22 | 2.206 / 5.187 / 17.296 | 13,8 | **72** (30–239) | 11–202 | 72% / 11% (9) | Pesquisa (perene) |
| 5 | ações e empresas | 219 | 2.954 / 5.326 / 8.124 | 12,2 | **65** (36–99) | 17–73 | 23% / 45% (58) | misto |
| 6 | imposto e regras | 13 | 2.497 / 6.766 / 11.843 | 8,1 | **55** (20–96) | 14–85 | 13% / 62% (5) | Navegação (pico) |
| 7 | crise e macro | 44 | 2.282 / 5.207 / 9.533 | 10,1 | **53** (23–97) | 9–85 | 6% / 76% (15) | Navegação (pico) |
| 8 | ETF e exterior | 52 | 2.262 / 3.696 / 6.020 | 13,5 | **50** (30–81) | 11–66 | 37% / 17% (9) | Pesquisa (perene) |
| 9 | tesouro e renda fixa | 70 | 2.096 / 4.302 / 6.404 | 10,0 | **43** (21–64) | 18–62 | 20% / 39% (15) | misto |
| 10 | juntar dinheiro e aposentadoria | 28 | 2.222 / 4.096 / 8.266 | 8,9 | **36** (20–73) | 11–65 | 9% / 60% (8) | Navegação (pico) |
| 11 | outros | 71 | 1.672 / 3.386 / 6.930 | 10,3 | **35** (17–71) | 7–58 | 25% / 38% (16) | Pesquisa (perene) |
| 12 | comportamento e família | 3 | 1.032 / 1.287 / 3.680 | 5,7 | **7** (6–21) | 6–23 | —% / —% (0) | sem dado |
| — | commodities (n < 3, fora do ranking) | 2 | 8.333 / 10.652 / 12.970 | 18,8 | **200** (157–244) | 173–228 | 15% / 53% (1) | Navegação (pico) |
| | **todos** | 673 | 2.629 / 4.886 / 9.356 | 13,2 | **65** (35–124) | 15–97 | | |

## Shorts: últimos 12 meses

| # | assunto | n | views intencionais (p25 / mediana / p75) | inscritos por mil | **inscritos esperados por vídeo** (p25–p75) | inscritos reais por vídeo (p25–p75) | % Pesquisa / Navegação (vídeos com dado) | perfil |
|---|---|---|---|---|---|---|---|---|
| 1 | comportamento e família | 15 | 2.206 / 4.284 / 8.304 | 0,8 | **3,6** (1,8–7,0) | 2–6 | 2% / 3% (10) | misto |
| 2 | bancos e contas | 3 | 2.036 / 2.160 / 2.789 | 1,5 | **3,2** (3,0–4,1) | 2–5 | —% / —% (0) | sem dado |
| 3 | tesouro e renda fixa | 5 | 2.236 / 2.323 / 3.229 | 0,9 | **2,2** (2,1–3,1) | 1–7 | 3% / 1% (2) | misto |
| 4 | cripto | 9 | 2.274 / 3.099 / 5.660 | 0,6 | **2,0** (1,4–3,6) | 0–3 | 3% / 1% (4) | misto |
| 5 | ações e empresas | 19 | 1.472 / 3.061 / 6.796 | 0,5 | **1,6** (0,8–3,6) | 0–4 | 2% / 1% (7) | misto |
| 6 | crise e macro | 3 | 1.668 / 1.834 / 5.528 | 0,7 | **1,3** (1,2–4,0) | 1–4 | 3% / 1% (1) | misto |
| 7 | outros | 20 | 872 / 1.124 / 1.903 | 0,9 | **1,0** (0,8–1,7) | 0–2 | 1% / 1% (2) | misto |
| 8 | juntar dinheiro e aposentadoria | 4 | 1.268 / 1.402 / 1.718 | 0,5 | **0,7** (0,6–0,8) | 0–1 | —% / —% (0) | sem dado |
| — | commodities (n < 3, fora do ranking) | 1 | 12.152 / 12.152 / 12.152 | 0,2 | **3,0** (3,0–3,0) | 3–3 | 4% / 3% (1) | misto |
| — | ETF e exterior (n < 3, fora do ranking) | 1 | 3.674 / 3.674 / 3.674 | 0,0 | **0,0** (0,0–0,0) | 0–0 | 1% / 1% (1) | misto |
| — | imposto e regras (n < 3, fora do ranking) | 1 | 3.240 / 3.240 / 3.240 | 0,0 | **0,0** (0,0–0,0) | 0–0 | —% / —% (0) | sem dado |
| | **todos** | 81 | 1.212 / 2.274 / 4.591 | 0,7 | **1,6** (0,9–3,3) | 0–4 | | |

## Shorts: vitalício

| # | assunto | n | views intencionais (p25 / mediana / p75) | inscritos por mil | **inscritos esperados por vídeo** (p25–p75) | inscritos reais por vídeo (p25–p75) | % Pesquisa / Navegação (vídeos com dado) | perfil |
|---|---|---|---|---|---|---|---|---|
| 1 | bancos e contas | 18 | 2.612 / 6.724 / 13.314 | 2,3 | **15,4** (6,0–30,5) | 6–42 | 56% / 3% (6) | Pesquisa (perene) |
| 2 | juntar dinheiro e aposentadoria | 16 | 1.406 / 2.260 / 10.253 | 4,0 | **9,1** (5,6–41,1) | 2–46 | 33% / 2% (6) | Pesquisa (perene) |
| 3 | ações e empresas | 146 | 1.345 / 2.576 / 4.794 | 3,1 | **8,0** (4,2–14,9) | 1–14 | 24% / 8% (28) | misto |
| 4 | FII | 30 | 974 / 1.298 / 1.932 | 5,8 | **7,6** (5,7–11,3) | 2–8 | 49% / 2% (2) | Pesquisa (perene) |
| 5 | tesouro e renda fixa | 24 | 1.996 / 2.624 / 4.959 | 2,3 | **6,0** (4,6–11,3) | 3–11 | 67% / 4% (6) | Pesquisa (perene) |
| 6 | ETF e exterior | 12 | 1.213 / 1.892 / 3.256 | 2,3 | **4,3** (2,8–7,5) | 1–7 | 24% / 2% (2) | misto |
| 7 | imposto e regras | 11 | 2.063 / 3.226 / 3.816 | 1,3 | **4,1** (2,7–4,9) | 2–6 | 2% / 1% (1) | misto |
| 8 | crise e macro | 53 | 1.074 / 1.420 / 1.708 | 2,6 | **3,7** (2,8–4,4) | 2–5 | 18% / 1% (3) | misto |
| 9 | outros | 116 | 1.102 / 1.710 / 2.826 | 2,0 | **3,4** (2,2–5,7) | 1–7 | 15% / 1% (15) | misto |
| 10 | comportamento e família | 19 | 1.122 / 2.978 / 5.772 | 0,8 | **2,5** (1,0–4,9) | 2–6 | 2% / 3% (10) | misto |
| 11 | cripto | 12 | 2.130 / 2.538 / 3.852 | 0,7 | **1,7** (1,5–2,6) | 0–3 | 3% / 1% (4) | misto |
| — | commodities (n < 3, fora do ranking) | 2 | 4.160 / 6.824 / 9.488 | 0,2 | **1,5** (0,9–2,1) | 1–2 | 4% / 3% (1) | misto |
| | **todos** | 459 | 1.192 / 1.924 / 4.090 | 2,6 | **5,0** (3,1–10,6) | 1–10 | | |

Fora (outlier, ≥ 40% das views do grupo): aDL4MMF6AnE Pra ficar rico você só precisa de 1 centavo #inves.

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

Base de hoje para comparação: 9 longos por mês, 42 inscritos esperados
por longo e 1,6 por Short (12 meses).
