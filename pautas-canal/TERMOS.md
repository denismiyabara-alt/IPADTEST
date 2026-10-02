# Termos de busca: o que o público procura e acha no canal

Gerado por `termos.py` a partir de três exportações de `auditoria-canal/dados/`:
- **`termos_busca_recentes.csv`:** 25 termos por vídeo, de 2026-04-04 a 01/10/2026, em 118 vídeos (os publicados no
  período e os 50 com mais busca). **É a fonte dos "últimos 6 meses".**
- **`termos_busca_por_video.csv`:** 25 termos de cada um dos 50 vídeos com mais busca, no vitalício.
- **`termos_busca_canal.csv`:** 25 termos do canal por mês, de out/25 a set/26.

**Filtros**, iguais aos de antes:
- fora os termos que chegam pelo Short do "1 centavo";
- fora os genéricos de dinheiro ("como ganhar dinheiro"...);
- fora os de bancos e apps do catálogo (Next, Nubank, Pix...).
- Um ticker sozinho ("trxf11", "suzb3") herda o assunto do vídeo que recebe a busca.

## Leitura (5 linhas)

1. **O "1 centavo" ainda domina:** desde 2026-04-04, 236.226 das 262.158 views da Pesquisa
   (90%) vêm dele e dos termos amplos. Investimento soma 10.066
   (4%); bancos e apps, 12.934.
2. **Tesouro agora aparece.** "tesouro direto", "ipca + 8", "tesouro ipca" e "tesouro ipca+ 2032" somam ~1 mil views
   no período, quase todas no vídeo de jun/26 (KMIsVEOcaLM). Ficam atrás de tickers de ações, FII, LCI/LCA/CDB e
   Barsi (tabela de famílias). **Copom e Selic quase não são buscados** (15 views).
3. **Tickers são a busca recente mais forte de investimento:**
   - o FII trxf11 (1.516, o termo nº 1, do vídeo de ago/26);
   - ações (pass3, suzb3, saud3, rani3, bbas3), todas em vídeos de 2026.
   - Quem busca o ticker acha o vídeo do canal sobre aquele ativo, e isso é demanda de cauda longa. Mas ações rendem
     poucos inscritos por vídeo (TEMAS.md).
4. **ETFs que pagam dividendos mensais seguem com demanda** (~420 views no período, pelo vídeo de 2024). Barsi e
   "juntar 1 milhão" também, em vídeos antigos.
5. **Crise, recessão, bitcoin, ETF de bitcoin, dividendos sintéticos e CDB prefixado quase não têm busca recente**
   (de 3 a 56 views). Esses assuntos vivem de Navegação (crise) ou de vídeos antigos (CDB prefixado, 2018).

## Top 20 termos de investimento nos últimos 6 meses (2026-04-04 a 01/10/2026)

| # | termo | assunto | views da Pesquisa no período | vídeo que recebe a busca |
|---|---|---|---|---|
| 1 | trxf11 | FII | 1.516 | `XOqLAz3dkV4` (2026-08-26) TRXF11: DIVIDENDOS atraentes ou PROBLEMAS à vista? |
| 2 | barsi | ações e empresas | 731 | `XBJqP2JTkkQ` (2022-12-15) BARSI ABRIU SUA CARTEIRA DE AÇÕES NA BOLSA DE VALORES # |
| 3 | pass3 | ações e empresas | 483 | `PEHR3h-r4DE` (2026-07-27) PASS3: O que os 6 bancos NÃO te contam | Conflito de in |
| 4 | lci e lca | tesouro e renda fixa | 473 | `Q1WMbZZn2Ik` (2025-04-28) O QUE RENDE MAIS CDB ou LCI/LCA? #investimentos |
| 5 | tesouro direto | tesouro e renda fixa | 456 | `KMIsVEOcaLM` (2026-06-16) CUIDADO com Tesouro Direto IPCA+ 8,32% (veja antes do C |
| 6 | suzb3 | ações e empresas | 433 | `OH0J9RX1VXc` (2026-04-30) SUZB3 ficou BARATA demais ou é uma ARMADILHA disfarçada |
| 7 | saud3 | ações e empresas | 396 | `ZPbbhbmSzRE` (2026-05-28) SAUD3: O Bradesco vai fechar o capital? Entenda a tese |
| 8 | bolsa de valores | ações e empresas | 265 | `XBJqP2JTkkQ` (2022-12-15) BARSI ABRIU SUA CARTEIRA DE AÇÕES NA BOLSA DE VALORES # |
| 9 | ipo spacex | ações e empresas | 216 | `6FxiU14JAVE` (2026-06-09) IPO da SPACEX: A Maior Oportunidade da Década ou Cilada |
| 10 | ipca + 8 | tesouro e renda fixa | 213 | `KMIsVEOcaLM` (2026-06-16) CUIDADO com Tesouro Direto IPCA+ 8,32% (veja antes do C |
| 11 | etfs que pagam dividendos mensais | renda mensal | 208 | `Y4WHQiKcv1g` (2024-07-03) DIVIDENDOS MENSAIS: 4 ÚNICOS ETFs que PAGAM MENSALMENTE |
| 12 | rani3 | ações e empresas | 182 | `Z27KBNJcPDA` (2026-08-04) RANI3 PAGA 11% ao ano — mas o LUCRO caiu 70% (Armadilha |
| 13 | lci | tesouro e renda fixa | 172 | `Q1WMbZZn2Ik` (2025-04-28) O QUE RENDE MAIS CDB ou LCI/LCA? #investimentos |
| 14 | barsi investidor | ações e empresas | 148 | `XBJqP2JTkkQ` (2022-12-15) BARSI ABRIU SUA CARTEIRA DE AÇÕES NA BOLSA DE VALORES # |
| 15 | etf | ETF e exterior | 133 | `c9Obo6F5_NU` (2026-04-08) ETF DIVIDENDOS MENSAIS são um GOLPE? (Entenda antes que |
| 16 | spcx34 | ações e empresas | 129 | `6FxiU14JAVE` (2026-06-09) IPO da SPACEX: A Maior Oportunidade da Década ou Cilada |
| 17 | bbas3 | ações e empresas | 123 | `UpbPXeG2eGc` (2026-05-20) BBAS3: NÃO COMPRE BANCO do BRASIL SEM ENTENDER ISSO |
| 18 | acoes | ações e empresas | 109 | `-0qJhPGLN0E` (2026-04-20) A Maior Distorção da Bolsa em 20 Anos — e Por Que o Gri |
| 19 | dividendos | ações e empresas | 109 | `c9Obo6F5_NU` (2026-04-08) ETF DIVIDENDOS MENSAIS são um GOLPE? (Entenda antes que |
| 20 | rara11 | ETF e exterior | 102 | `WnDsCpB4PzY` (2026-07-03) RARA11: o ETF que a mídia ignorou (mas não deveria) |

## Famílias de investimento: período × vitalício

| família | views no período | views no vitalício (50 vídeos de busca) | termos |
|---|---|---|---|
| ações por ticker | 1.842 | 6.367 | 60 |
| FII (incl. tickers de FII) | 1.779 | 7.643 | 64 |
| LCI, LCA e CDB | 1.360 | 15.565 | 53 |
| Barsi | 1.139 | 8.868 | 28 |
| Tesouro Direto e IPCA+ | 1.009 | 26 | 32 |
| ETFs e dividendos mensais | 421 | 5.961 | 12 |
| juntar 1 milhão | 316 | 5.206 | 27 |
| bolha da IA | 91 | 0 | 4 |
| bitcoin e cripto | 70 | 44.327 | 67 |
| Copom e Selic | 15 | 0 | 2 |
| crise e recessão | 3 | 2.262 | 13 |

## Termos de investimento: tabela completa (os 60 maiores no período)

| termo | assunto | vídeo que recebe a busca (ano) | Pesquisa, últimos 6 meses (por vídeo) | Pesquisa, vitalício (no vídeo) |
|---|---|---|---|---|
| trxf11 | FII | `XOqLAz3dkV4` (2026) | 1.516 | 0 |
| barsi | ações e empresas | `XBJqP2JTkkQ` (2022) | 731 | 2.588 |
| pass3 | ações e empresas | `PEHR3h-r4DE` (2026) | 483 | 0 |
| lci e lca | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | 473 | 3.544 |
| tesouro direto | tesouro e renda fixa | `KMIsVEOcaLM` (2026) | 456 | 0 |
| suzb3 | ações e empresas | `OH0J9RX1VXc` (2026) | 433 | 0 |
| saud3 | ações e empresas | `ZPbbhbmSzRE` (2026) | 396 | 0 |
| bolsa de valores | ações e empresas | `XBJqP2JTkkQ` (2022) | 265 | 436 |
| ipo spacex | ações e empresas | `6FxiU14JAVE` (2026) | 216 | 0 |
| ipca + 8 | tesouro e renda fixa | `KMIsVEOcaLM` (2026) | 213 | 0 |
| etfs que pagam dividendos mensais | renda mensal | `Y4WHQiKcv1g` (2024) | 208 | 1.877 |
| rani3 | ações e empresas | `Z27KBNJcPDA` (2026) | 182 | 0 |
| lci | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | 172 | 927 |
| barsi investidor | ações e empresas | `XBJqP2JTkkQ` (2022) | 148 | 1.855 |
| etf | ETF e exterior | `Y4WHQiKcv1g` (2024) | 133 | 1.096 |
| spcx34 | ações e empresas | `6FxiU14JAVE` (2026) | 129 | 0 |
| bbas3 | ações e empresas | `UpbPXeG2eGc` (2026) | 123 | 0 |
| acoes | ações e empresas | `XBJqP2JTkkQ` (2022) | 109 | 81 |
| dividendos | ações e empresas | `Y4WHQiKcv1g` (2024) | 109 | 41 |
| rara11 | ETF e exterior | `WnDsCpB4PzY` (2026) | 102 | 0 |
| lca | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | 98 | 716 |
| etfs | ETF e exterior | `Y4WHQiKcv1g` (2024) | 93 | 309 |
| lca e lci | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | 92 | 888 |
| carteira de acoes | ações e empresas | `XBJqP2JTkkQ` (2022) | 86 | 463 |
| lci ou cdb | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | 83 | 797 |
| como juntar 1 milhao de reais | juntar dinheiro e aposentadoria | `tbKsF2qyakU` (2022) | 77 | 1.803 |
| etf que pagam dividendos mensais | renda mensal | `Y4WHQiKcv1g` (2024) | 77 | 1.255 |
| carteira do barsi | ações e empresas | `XBJqP2JTkkQ` (2022) | 74 | 488 |
| itub4 | ações e empresas | `4HMqxGqjHpA` (2026) | 69 | 0 |
| tesouro ipca | tesouro e renda fixa | `KMIsVEOcaLM` (2026) | 69 | 0 |
| opa santander | ações e empresas | `nzxLnlP9nfs` (2026) | 64 | 0 |
| luiz barsi | ações e empresas | `XBJqP2JTkkQ` (2022) | 63 | 580 |
| 1 milhao | juntar dinheiro e aposentadoria | `tbKsF2qyakU` (2022) | 63 | 341 |
| tesouro ipca+ 2032 | tesouro e renda fixa | `KMIsVEOcaLM` (2026) | 63 | 0 |
| ivwo11 | ações e empresas | `fztzCXiHxq0` (2026) | 53 | 0 |
| fundos imobiliarios | FII | `kipRQb0ksus` (2023) | 50 | 1.432 |
| bolha da ia | crise e macro | `DEgfZlK6FZM` (2026) | 49 | 0 |
| lci lca | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | 46 | 339 |
| investimento cdb | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | 46 | 191 |
| ipo spacex vale a pena | ações e empresas | `6FxiU14JAVE` (2026) | 42 | 0 |
| como fazer 1 milhao de reais | juntar dinheiro e aposentadoria | `tbKsF2qyakU` (2022) | 41 | 935 |
| fiis | FII | `kipRQb0ksus` (2023) | 39 | 104 |
| ipo compass | ações e empresas | `LHV92db3NHs` (2026) | 39 | 0 |
| cdb ou lci | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | 35 | 511 |
| etf dividendos | ETF e exterior | `Y4WHQiKcv1g` (2024) | 35 | 417 |
| melhores lci e lca hoje | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | 33 | 179 |
| ipo da spacex | ações e empresas | `6FxiU14JAVE` (2026) | 32 | 0 |
| primeiro milhao | juntar dinheiro e aposentadoria | `tbKsF2qyakU` (2022) | 31 | 313 |
| bolha ia | crise e macro | `DEgfZlK6FZM` (2026) | 31 | 0 |
| xbci11 etf | ETF e exterior | `c9Obo6F5_NU` (2026) | 30 | 0 |
| etf de dividendos | ETF e exterior | `Y4WHQiKcv1g` (2024) | 29 | 202 |
| luiz barsi dividendos | ações e empresas | `XBJqP2JTkkQ` (2022) | 29 | 85 |
| ipca | tesouro e renda fixa | `KMIsVEOcaLM` (2026) | 29 | 0 |
| etfs americanos que pagam dividendos mensais | renda mensal | `Y4WHQiKcv1g` (2024) | 28 | 1.002 |
| ipca+ | tesouro e renda fixa | `KMIsVEOcaLM` (2026) | 27 | 0 |
| ipca 2032 | tesouro e renda fixa | `KMIsVEOcaLM` (2026) | 27 | 0 |
| etf brasileiros que pagam dividendos | ETF e exterior | `Y4WHQiKcv1g` (2024) | 26 | 342 |
| um milhao de reais | juntar dinheiro e aposentadoria | `tbKsF2qyakU` (2022) | 26 | 160 |
| investimento lci e lca | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | 25 | 188 |
| lci lca ou cdb | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | 24 | 213 |

## Termos que são pergunta curta → o Short (ou longo) do calendário v2 que responde

| termo | views da Pesquisa (vitalício) | categoria | pauta do calendário v2 |
|---|---|---|---|
| como investir em criptomoedas | 1.811 | cripto | 19/11 (longo): Bitcoin depois do 'alerta': o que mudou desde fevereiro |
| como juntar 1 milhao de reais | 1.803 | juntar dinheiro e aposentadoria | 07/10 (short): Como juntar 1 milhão de reais com R$ 1.000 por mês |
| como fazer 1 milhao de reais | 935 | juntar dinheiro e aposentadoria | 07/10 (short): Como juntar 1 milhão de reais com R$ 1.000 por mês |
| lci ou cdb | 797 | tesouro e renda fixa | 05/10 (short): LCI e LCA ou CDB: qual rende mais depois do imposto? |
| como comprar bitcoin | 792 | cripto | 19/11 (longo): Bitcoin depois do 'alerta': o que mudou desde fevereiro |
| como investir em bitcoins | 747 | cripto | 19/11 (longo): Bitcoin depois do 'alerta': o que mudou desde fevereiro |
| como operar opcoes | 684 | ações e empresas | sem pauta: candidato a Short |
| cdb ou lci | 511 | tesouro e renda fixa | 05/10 (short): LCI e LCA ou CDB: qual rende mais depois do imposto? |
| irbr3 vale a pena | 483 | ações e empresas | sem pauta: candidato a Short |
| como operar opcoes na bolsa | 466 | ações e empresas | sem pauta: candidato a Short |
| como funciona o bitcoin | 339 | cripto | 19/11 (longo): Bitcoin depois do 'alerta': o que mudou desde fevereiro |
| como investir em opcoes | 338 | ações e empresas | sem pauta: candidato a Short |
| etfs vale a pena | 236 | ETF e exterior | sem pauta: candidato a Short |
| lci lca ou cdb | 213 | tesouro e renda fixa | 05/10 (short): LCI e LCA ou CDB: qual rende mais depois do imposto? |
| como calcular preco medio de acao | 202 | ações e empresas | sem pauta: candidato a Short |
| lca ou cdb | 190 | tesouro e renda fixa | 05/10 (short): LCI e LCA ou CDB: qual rende mais depois do imposto? |
| como juntar um milhao de reais | 182 | juntar dinheiro e aposentadoria | 07/10 (short): Como juntar 1 milhão de reais com R$ 1.000 por mês |
| como investir na bolsa de valores | 179 | ações e empresas | sem pauta: candidato a Short |
| como investir em lci e lca | 163 | tesouro e renda fixa | 05/10 (short): LCI e LCA ou CDB: qual rende mais depois do imposto? |
| como operar na bolsa de valores | 153 | ações e empresas | sem pauta: candidato a Short |
| o que sao opcoes no mercado financeiro | 153 | ações e empresas | sem pauta: candidato a Short |
| cdb prefixado ou pos fixado | 138 | tesouro e renda fixa | 14/11 (longo): CDB prefixado ou pós-fixado: qual rende mais em 2026 |
| qual melhor fundo imobiliario para 2023 | 137 | FII | 07/11 (longo): Fundos imobiliários para iniciantes: de onde vem a renda |
| como chegar no primeiro milhao | 133 | juntar dinheiro e aposentadoria | 07/10 (short): Como juntar 1 milhão de reais com R$ 1.000 por mês |
| como fazer um milhao de reais | 124 | juntar dinheiro e aposentadoria | 07/10 (short): Como juntar 1 milhão de reais com R$ 1.000 por mês |

## Termos amplos (Short do "1 centavo" e genéricos de dinheiro): os 15 maiores

| termo | vídeo | Pesquisa, últimos 6 meses | vitalício (no vídeo) |
|---|---|---|---|
| como ganhar dinheiro na internet | `aDL4MMF6AnE` | 60.550 | 220.520 |
| como ganhar dinheiro | `aDL4MMF6AnE` | 35.437 | 109.875 |
| como ficar rico | `aDL4MMF6AnE` | 23.392 | 82.935 |
| como investir dinheiro | `aDL4MMF6AnE` | 12.970 | 48.270 |
| como fazer dinheiro na internet | `aDL4MMF6AnE` | 9.827 | 34.395 |
| investimento | `aDL4MMF6AnE` | 8.521 | 28.380 |
| ganhar dinheiro na internet | `aDL4MMF6AnE` | 7.908 | 31.135 |
| como fazer dinheiro | `aDL4MMF6AnE` | 8.013 | 25.455 |
| como ganhar dinheiro em casa | `aDL4MMF6AnE` | 7.651 | 29.467 |
| como juntar dinheiro | `aDL4MMF6AnE` | 7.720 | 22.538 |
| renda extra | `aDL4MMF6AnE` | 6.468 | 26.394 |
| ganhar dinheiro | `aDL4MMF6AnE` | 5.031 | 17.732 |
| como conseguir dinheiro | `aDL4MMF6AnE` | 3.833 | 11.492 |
| como ganhar dinheiro facil | `aDL4MMF6AnE` | 3.805 | 12.660 |
| como investir | `aDL4MMF6AnE` | 3.946 | 14.976 |

## Bancos, apps e outros do catálogo antigo: os 15 maiores (fora do foco)

| termo | vídeo (ano) | Pesquisa, últimos 6 meses | vitalício |
|---|---|---|---|
| caixinha turbo nubank | `_WHHib_xvJ4` (2025) | 2.415 | 56.612 |
| banco next | `T956DmDdPDU` (2018) | 7 | 92.851 |
| next | `T956DmDdPDU` (2018) | 0 | 82.951 |
| mercado pago | `9tn6b8FaE24` (2025) | 2.455 | 4.824 |
| cartao next | `T956DmDdPDU` (2018) | 0 | 55.964 |
| banco original | `CaOGCAsOLvE` (2019) | 0 | 39.928 |
| banco next vale a pena | `T956DmDdPDU` (2018) | 2 | 20.373 |
| nextjoy | `V68Hd157uac` (2021) | 0 | 16.508 |
| pedacinho nubank | `_I5dFQ6mvK0` (2021) | 0 | 11.224 |
| conta next | `T956DmDdPDU` (2018) | 0 | 9.976 |
| sousmile | `9Jt4U0uhd_U` (2021) | 17 | 7.409 |
| next banco | `T956DmDdPDU` (2018) | 0 | 7.159 |
| como funciona a caixinha turbo da nubank | `_WHHib_xvJ4` (2025) | 346 | 7.154 |
| c6 bank | `yN0kKJf2D1c` (2019) | 42 | 7.043 |
| caixinha turbo nubank como funciona | `_WHHib_xvJ4` (2025) | 420 | 6.915 |

**Para atualizar**, rode `exportar.py --termos-recentes 180` no Mac, como na última vez, suba o
`termos_busca_recentes.csv` e regere com `python3 termos.py && python3 calendario_v2.py`.
