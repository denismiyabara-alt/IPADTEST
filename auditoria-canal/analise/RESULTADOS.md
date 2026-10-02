# Resultados da auditoria (gerado por analisar.py)

Dados até 2026-10-01. 1145 vídeos; 464 Shorts. Exportações do Studio: studio_conteudo_longos, studio_conteudo_shorts, studio_origem_trafego_mensal, studio_origem_trafego_mensal_longos.

Studio casado com videos.csv: 676 por ID, 1 por título, 294 sem par.

## 0. Conferência do Studio (soma das linhas × linha Total)

| exportação | vídeos | métrica | Total do Studio | soma das linhas | diferença % |
|---|---|---|---|---|---|
| longos | 501 | impressões | 46.727.801 | 29.943.325 | -35,92 |
| longos | 501 | CTR (%) | 7,09 | 7,77 | 9,65 |
| longos | 501 | views | 13.067.113 | 9.376.916 | -28,24 |
| longos | 501 | views intencionais | 12.918.719 | 9.237.370 | -28,50 |
| longos | 501 | horas | 918.688,0 | 655.080,4 | -28,69 |
| longos | 501 | inscritos | 159.874 | 127.620 | -20,17 |
| shorts | 471 | impressões | 23.733.775 | 23.722.156 | -0,05 |
| shorts | 471 | CTR (%) | 5,48 | 5,47 | -0,14 |
| shorts | 471 | views | 11.224.568 | 11.223.227 | -0,01 |
| shorts | 471 | views intencionais | 5.749.210 | 5.748.314 | -0,02 |
| shorts | 471 | horas | 46.630,5 | 46.624,2 | -0,01 |
| shorts | 471 | inscritos | 15.322 | 15.320 | -0,01 |

**A tabela do Studio de longos parou em ~500 linhas** (limite da exportação): a soma das linhas não fecha com o Total, e as tabelas abaixo cobrem só esses vídeos. Para ter todos, exporte em partes (filtrando por data de publicação) ou use o exportar.py (Analytics, sem esse limite).

## 0b. Vídeos do Studio fora da playlist pública (privados, não listados ou excluídos)

294 vídeos do Studio não estão em videos.csv (285 longos). Só entre os 500 longos da exportação, eles somam 4.148.429 views (31,7% das views vitalícias de longos) e 52.351 inscritos ganhos (32,7% dos inscritos vindos de longos). Os 5 maiores:

- `U53EJSYX-ew` Jan 2, 2020: BANCO NEXT ou NUBANK? Conta NUBANK ou NEXT qual o melhor? NEXT vale a pena? NUBA — 113.575 views, 3.474 inscritos
- `k08bpBRzm3U` May 14, 2020: SANTANDER USE O TRUQUE DOS BANCOS A SEU FAVOR! SANTANDER DÁ 10 DIAS DE DINHEIRO  — 95.898 views, 1.292 inscritos
- `es9ap7LDRXo` Dec 1, 2021: QUANTO RENDE 100, 1000 e 10.000 REAIS NA NUBANK? VALE A PENA INVESTIR COM POUCO  — 87.777 views, 1.053 inscritos
- `fa7ziMZUink` Jul 21, 2021: 💣IRBR3 - BARSI COMPRA AÇÕES DA IRB BRASIL E REVELA PREÇO ALVO PARA AS AÇÕES  IRB — 43.728 views, 489 inscritos
- `21Z-frnEeTk` Feb 9, 2022: OIBR3 VENDEU E AGORA O QUE VAI ACONTECER COM AS AÇÕES DA OI? — 41.974 views, 251 inscritos

## 0c. Views ÷ views intencionais (engajadas), por formato

Se o contador de views estiver inflado em relação às views intencionais, a razão sobe. Em Shorts, a contagem mudou em 31/03/2025. Os outliers (um vídeo com ≥ 40% das views do grupo) ficam de fora das linhas por período.

| formato | grupo | vídeos | views | intencionais | views ÷ intenc. (soma) | mediana por vídeo | insc./mil views | insc./mil intenc. | CTR (%) | impressões |
|---|---|---|---|---|---|---|---|---|---|---|
| longo | todos | 680 | 7.009.995 | 6.886.575 | 1,02 | 1,00 | 12,93 | 13,06 | 7,76 | 26.928.356 |
| longo | publicados antes de 27/08/2026 | 672 | 6.864.021 | 6.843.477 | 1,00 | 1,00 | 13,17 | 13,11 | 7,79 | 26.322.189 |
| longo | publicados a partir de 27/08/2026 | 8 | 145.974 | 43.098 | 3,39 | 3,29 | 1,39 | 6,31 | 6,18 | 606.167 |
| short | todos | 464 | 11.227.645 | 5.756.123 | 1,95 | 1,02 | 1,37 | 2,67 | 5,47 | 23.703.492 |
| short | sem outlier — fora: aDL4MMF6AnE (Pra ficar rico você só precisa de 1 cent) | 463 | 3.214.737 | 2.214.159 | 1,45 | 1,02 | 1,78 | 2,58 | 5,30 | 9.372.627 |
| short | publicados antes de 31/03/2025 | 345 | 1.574.472 | 1.473.604 | 1,07 | 1,01 | 2,93 | 3,13 | 4,86 | 7.419.219 |
| short | publicados a partir de 31/03/2025 | 118 | 1.640.265 | 740.555 | 2,21 | 2,07 | 0,67 | 1,48 | 6,96 | 1.953.408 |

## 1. Conversão por formato (inscritos ganhos por mil views)

| formato | vídeos | views | % views | mediana views | insc./mil views | insc./mil engajadas | % média assistida | CTR mediano |
|---|---|---|---|---|---|---|---|---|
| short | 464 | 11.227.645 | 61,5 | 2.311 | 1,37 | 2,67 | 81,6 | 3,35 |
| longo | 681 | 7.018.800 | 38,5 | 4.954 | 12,91 | 13,16 | 41,0 | 6,49 |
| short sem outlier | 463 | 3.214.737 | 100,0 | 2.310 | 1,78 | 2,58 | 81,6 | 3,35 |

## 2a. Por tema (longos)

| tema | vídeos | views | % views | mediana views | insc./mil views | CTR mediano | % média assistida |
|---|---|---|---|---|---|---|---|
| caso com nome | 151 | 1.895.253 | 27,0 | 6.318 | 13,10 | 6,58 | 41,9 |
| produto / comparativo | 190 | 1.361.467 | 19,4 | 4.350 | 14,38 | 6,65 | 41,5 |
| alerta macro | 123 | 1.181.713 | 16,8 | 5.387 | 9,79 | 6,67 | 39,8 |
| outros | 107 | 1.028.028 | 14,6 | 4.965 | 14,04 | 5,49 | 41,2 |
| educativo / iniciante | 48 | 935.366 | 13,3 | 3.198 | 11,87 | 5,59 | 42,5 |
| plano de renda | 62 | 616.973 | 8,8 | 3.945 | 14,78 | 6,40 | 39,9 |

## 2b. Por tema (shorts)

| tema | vídeos | views | % views | mediana views | insc./mil views | CTR mediano | % média assistida |
|---|---|---|---|---|---|---|---|
| outros | 191 | 9.319.573 | 83,0 | 2.069 | 1,17 | 3,13 | 82,2 |
| caso com nome | 57 | 733.678 | 6,5 | 3.939 | 1,91 | 3,63 | 78,4 |
| produto / comparativo | 121 | 595.673 | 5,3 | 2.260 | 2,95 | 3,61 | 83,6 |
| alerta macro | 62 | 287.167 | 2,6 | 1.944 | 1,96 | 3,09 | 74,0 |
| plano de renda | 17 | 194.855 | 1,7 | 4.123 | 3,08 | 3,07 | 92,8 |
| educativo / iniciante | 16 | 96.699 | 0,9 | 3.452 | 1,84 | 3,69 | 98,6 |

## 3. Concentração das views

| grupo | vídeos | % top 1 | % top 5 | % top 10 | % top 10% dos vídeos | vídeos p/ 50% | vídeos p/ 80% | Gini |
|---|---|---|---|---|---|---|---|---|
| todos | 1145 | 43,9 | 49,7 | 53,2 | 73,3 | 6 | 197 | 0,79 |
| longos | 681 | 7,0 | 15,8 | 21,3 | 49,3 | 71 | 263 | 0,59 |
| shorts | 464 | 71,4 | 76,5 | 79,8 | 88,0 | 1 | 11 | 0,90 |

## 4. Top × fracos (quartil de cima × de baixo)

População: longos publicados nos últimos 365 dias, com ≥ 30 dias de vida e ≥ 500 views intencionais; ordem por inscritos ganhos (empate: views intencionais).

|  | top | fracos |
|---|---|---|
| vídeos | 19 | 19 |
| inscritos ganhos (mediana) | 131 | 9 |
| views intencionais (mediana) | 15.781 | 2.238 |
| views (mediana) | 16.096 | 2.299 |
| inscritos por mil views intencionais | 11,54 | 3,62 |
| inscritos por mil views | 11,42 | 3,56 |
| temas | alerta macro 37%, produto / comparativo 26%, plano de renda 21% | produto / comparativo 32%, alerta macro 26%, outros 26% |
| % caso com nome | 5 | 11 |
| duração mediana (min) | 16,0 | 13,4 |
| título: caracteres | 68 | 63 |
| % título com número | 42 | 47 |
| % título com ? | 37 | 53 |
| % título em caixa alta | 32 | 47 |
| dia mais comum | terça | quinta |
| hora mediana (Brasília) | 19 | 19 |
| CTR mediano (%) | 6,67 | — |
| impressões medianas | 181.226 | — |
| % média assistida | 36,9 | 41,0 |
| retenção aos 30 s (%) | — | — |

### 4b. Lista para anotar a retenção aos 30 s (10 top e 10 fracos)

Critério: longos publicados nos últimos 365 dias, com ≥ 30 dias de vida e ≥ 500 views intencionais; ordem por inscritos ganhos (empate: views intencionais).

| grupo | vídeo | título | publicado | inscritos | views intenc. | insc./mil intenc. | Studio |
|---|---|---|---|---|---|---|---|
| top | `Fb0l4KEq27o` | 6 ETFs que MAIS PAGARAM DIVIDENDOS MENSAIS em 2025 e devem c | 2026-01-13 | 637 | 32.294 | 19,7 | [abrir](https://studio.youtube.com/video/Fb0l4KEq27o/analytics/tab-overview/period-default) |
| top | `dHYQtxnMSrw` | ÚLTIMA CHANCE de GANHAR MUITO DINHEIRO na RENDA FIXA (NTN-B  | 2026-01-28 | 421 | 31.427 | 13,4 | [abrir](https://studio.youtube.com/video/dHYQtxnMSrw/analytics/tab-overview/period-default) |
| top | `IcN3m7whpl8` | Esse Gráfico Acertou as CRISES 1929, 2008 e 2020… Agora Ele  | 2026-01-29 | 357 | 28.821 | 12,4 | [abrir](https://studio.youtube.com/video/IcN3m7whpl8/analytics/tab-overview/period-default) |
| top | `tpobf1e1OtM` | A Crise Já Está Acontecendo (e Só os Espertos Estão Vendo) | 2025-11-07 | 345 | 33.147 | 10,4 | [abrir](https://studio.youtube.com/video/tpobf1e1OtM/analytics/tab-overview/period-default) |
| top | `TY8oLvUt2Qg` | RECEBA DIVIDENDOS TODOS os MESES de AÇÕES SEGURAS (mesmo com | 2025-10-29 | 324 | 17.994 | 18,0 | [abrir](https://studio.youtube.com/video/TY8oLvUt2Qg/analytics/tab-overview/period-default) |
| top | `lt2LWbwu3mc` | O COBRE É O NOVO PETRÓLEO? Descubra Antes que Dispare (MAIS) | 2025-10-10 | 255 | 15.288 | 16,7 | [abrir](https://studio.youtube.com/video/lt2LWbwu3mc/analytics/tab-overview/period-default) |
| top | `KMIsVEOcaLM` | CUIDADO com Tesouro Direto IPCA+ 8,32% (veja antes do Copom) | 2026-06-16 | 246 | 19.302 | 12,7 | [abrir](https://studio.youtube.com/video/KMIsVEOcaLM/analytics/tab-overview/period-default) |
| top | `JDtxzQthFlk` | MORTE DO BITCOIN? O ALERTA QUE O MERCADO NÃO QUER OUVIR | 2026-02-05 | 224 | 32.339 | 6,9 | [abrir](https://studio.youtube.com/video/JDtxzQthFlk/analytics/tab-overview/period-default) |
| top | `tb0nwpl9mFw` | NÃO INVISTA no TESOURO DIRETO AGORA SEM SABER DISSO (CUIDADO | 2026-03-17 | 142 | 17.840 | 8,0 | [abrir](https://studio.youtube.com/video/tb0nwpl9mFw/analytics/tab-overview/period-default) |
| top | `IB1mBcF00jc` | ETF JEPI39 PAGA DIVIDENDOS MENSAIS, mas vale a pena? | 2026-02-26 | 131 | 20.232 | 6,5 | [abrir](https://studio.youtube.com/video/IB1mBcF00jc/analytics/tab-overview/period-default) |
| fraco | `J_UAjVSbg-c` | PRUDENTIAL VENDIDA : se você tem SEGURO de VIDA ou VGBL, vej | 2026-08-07 | 9 | 2.218 | 4,1 | [abrir](https://studio.youtube.com/video/J_UAjVSbg-c/analytics/tab-overview/period-default) |
| fraco | `R9DfUgYxLl8` | Concentrar ou Diversificar? A estratégia para bater o S&P500 | 2026-04-23 | 8 | 2.036 | 3,9 | [abrir](https://studio.youtube.com/video/R9DfUgYxLl8/analytics/tab-overview/period-default) |
| fraco | `yBoRbHQlzCE` | Quem INVESTIR pode PERDER DINHEIRO (e nem sabe) [AXIA7,CYRE4 | 2026-03-23 | 7 | 2.205 | 3,2 | [abrir](https://studio.youtube.com/video/yBoRbHQlzCE/analytics/tab-overview/period-default) |
| fraco | `Z27KBNJcPDA` | RANI3 PAGA 11% ao ano — mas o LUCRO caiu 70% (Armadilha?) | 2026-08-04 | 7 | 869 | 8,1 | [abrir](https://studio.youtube.com/video/Z27KBNJcPDA/analytics/tab-overview/period-default) |
| fraco | `lFPZmp8kLuo` | SINAL FORTE da BOLHA da INTELIGÊNCIA ARTIFICIAL (você precis | 2026-04-01 | 5 | 2.297 | 2,2 | [abrir](https://studio.youtube.com/video/lFPZmp8kLuo/analytics/tab-overview/period-default) |
| fraco | `5i9cNa6uEc0` | NOVA LEI DA HERANÇA: SUA FAMÍLIA VAI PAGAR MAIS? | 2026-08-12 | 5 | 892 | 5,6 | [abrir](https://studio.youtube.com/video/5i9cNa6uEc0/analytics/tab-overview/period-default) |
| fraco | `2TCAvZrl5nA` | ETF de GUERRA. É Horrível, Mas Isso Pode Multiplicar Seu Pat | 2026-04-09 | 4 | 3.249 | 1,2 | [abrir](https://studio.youtube.com/video/2TCAvZrl5nA/analytics/tab-overview/period-default) |
| fraco | `GFHFMCaPn60` | Michael Burry fez de novo — e dessa vez é a Nvidia (Risco de | 2026-07-31 | 4 | 990 | 4,0 | [abrir](https://studio.youtube.com/video/GFHFMCaPn60/analytics/tab-overview/period-default) |
| fraco | `nRHvGe4-bTU` | GREVE DOS CAMINHONEIROS PREPARE sua CARTEIRA (a de Investime | 2026-03-19 | 2 | 2.385 | 0,8 | [abrir](https://studio.youtube.com/video/nRHvGe4-bTU/analytics/tab-overview/period-default) |
| fraco | `uLVNra6EWc4` | Alerta nos bancões: Quem sobrevive e quem perde dinheiro em  | 2026-05-26 | 2 | 994 | 2,0 | [abrir](https://studio.youtube.com/video/uLVNra6EWc4/analytics/tab-overview/period-default) |

## 5. Mês a mês

Views e minutos: Analytics (canal). Views de longos e de Shorts: Studio (Total.csv). % de inscritos de Shorts marcada com * é estimativa do modelo (ver H5).

| mês | views | views intenc. | % intenc. | minutos | views longos | views Shorts | ganhos | perdidos | líquidos | insc./mil views | % inscritos de Shorts |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 2025-04 | 1.438.990 | 637.574 | 44,3 | 669.876 | 60.144 | 1.378.833 | 1.907 | 473 | 1.434 | 1,33 | 61,9* |
| 2025-05 | 1.715.968 | 748.461 | 43,6 | 596.405 | 42.480 | 1.673.481 | 2.630 | 533 | 2.097 | 1,53 | 73,6* |
| 2025-06 | 831.061 | 394.703 | 47,5 | 490.238 | 63.060 | 767.986 | 1.914 | 460 | 1.454 | 2,30 | 46,3* |
| 2025-07 | 814.856 | 369.207 | 45,3 | 408.307 | 41.951 | 772.897 | 1.528 | 473 | 1.055 | 1,88 | 56,6* |
| 2025-08 | 1.259.005 | 560.576 | 44,5 | 471.710 | 39.288 | 1.219.709 | 1.779 | 483 | 1.296 | 1,41 | 68,8* |
| 2025-09 | 579.453 | 292.096 | 50,4 | 514.073 | 67.530 | 511.913 | 1.598 | 423 | 1.175 | 2,76 | 35,0* |
| 2025-10 | 461.031 | 237.265 | 51,5 | 378.574 | 49.273 | 411.744 | 1.150 | 440 | 710 | 2,49 | 37,2* |
| 2025-11 | 338.452 | 204.239 | 60,3 | 477.988 | 84.960 | 253.454 | 1.409 | 399 | 1.010 | 4,16 | 17,5* |
| 2025-12 | 316.204 | 173.634 | 54,9 | 345.042 | 48.204 | 267.993 | 994 | 396 | 598 | 3,14 | 28,3* |
| 2026-01 | 423.778 | 253.759 | 59,9 | 650.676 | 96.788 | 326.970 | 1.906 | 463 | 1.443 | 4,50 | 19,3* |
| 2026-02 | 536.962 | 318.642 | 59,3 | 653.257 | 111.683 | 425.259 | 2.323 | 499 | 1.824 | 4,33 | 21,3* |
| 2026-03 | 350.248 | 199.361 | 56,9 | 426.697 | 62.120 | 288.112 | 1.133 | 377 | 756 | 3,23 | 24,8* |
| 2026-04 | 326.526 | 173.769 | 53,2 | 235.316 | 32.859 | 293.655 | 795 | 370 | 425 | 2,43 | 38,8* |
| 2026-05 | 307.657 | 162.625 | 52,9 | 264.958 | 33.990 | 271.738 | 770 | 358 | 412 | 2,50 | 36,2* |
| 2026-06 | 437.391 | 219.079 | 50,1 | 378.111 | 53.444 | 373.846 | 1.026 | 374 | 652 | 2,35 | 33,2* |
| 2026-07 | 350.911 | 194.841 | 55,5 | 425.021 | 64.917 | 268.568 | 971 | 385 | 586 | 2,77 | 22,7* |
| 2026-08 | 191.130 | 100.590 | 52,6 | 224.313 | 40.792 | 137.813 | 576 | 328 | 248 | 3,01 | 19,3* |
| 2026-09 | 278.349 | 95.645 | 34,4 | 288.244 | 187.475 | 121.651 | 503 | 282 | 221 | 1,81 | — |

## 6. Origem do tráfego (% das views do mês, API)

RELATED_VIDEO = vídeos sugeridos ("Recomendados"); BROWSE = Início/Inscrições.

| mês | RELATED_VIDEO | BROWSE | YT_SEARCH | SHORTS | EXT_URL | NO_LINK_OTHER |
|---|---|---|---|---|---|---|
| 2025-04 | 0,8 | 2,6 | 11,0 | 83,9 | 0,3 | 0,1 |
| 2025-05 | 0,4 | 1,6 | 18,1 | 77,9 | 0,3 | 0,1 |
| 2025-06 | 1,4 | 5,2 | 33,8 | 56,7 | 0,5 | 0,1 |
| 2025-07 | 1,1 | 3,2 | 37,6 | 55,6 | 0,4 | 0,1 |
| 2025-08 | 0,6 | 1,9 | 24,2 | 71,5 | 0,2 | 0,1 |
| 2025-09 | 1,8 | 7,6 | 43,7 | 43,9 | 0,4 | 0,2 |
| 2025-10 | 1,9 | 8,0 | 46,3 | 40,2 | 0,8 | 0,2 |
| 2025-11 | 5,1 | 15,7 | 60,4 | 14,7 | 0,5 | 0,4 |
| 2025-12 | 2,9 | 8,6 | 68,0 | 16,8 | 0,5 | 0,3 |
| 2026-01 | 4,6 | 13,6 | 64,8 | 12,8 | 0,7 | 0,4 |
| 2026-02 | 4,1 | 13,2 | 44,6 | 33,5 | 0,7 | 0,4 |
| 2026-03 | 3,0 | 10,8 | 78,2 | 5,1 | 0,4 | 0,4 |
| 2026-04 | 1,4 | 5,5 | 76,8 | 13,5 | 0,4 | 0,2 |
| 2026-05 | 1,4 | 6,3 | 68,6 | 20,8 | 0,4 | 0,3 |
| 2026-06 | 2,8 | 7,4 | 45,0 | 40,4 | 0,3 | 0,3 |
| 2026-07 | 3,0 | 12,6 | 51,5 | 29,0 | 0,3 | 0,4 |
| 2026-08 | 2,5 | 14,3 | 61,3 | 18,2 | 0,4 | 0,4 |
| 2026-09 | 2,3 | 51,7 | 40,3 | 3,4 | 0,2 | 0,4 |

### 6b. Origem do tráfego, vitalício (todos, Studio)

| origem | views | % views | impressões | CTR (%) | horas |
|---|---|---|---|---|---|
| Pesquisa do YouTube | 7.638.798 | 31,0 | 47.033.295 | 8,53 | 228.778 |
| Feed dos Shorts | 6.422.996 | 26,1 | — | — | 24.016 |
| Recursos de navegação | 5.452.562 | 22,1 | 55.179.072 | 6,92 | 390.253 |
| Vídeos sugeridos | 1.325.564 | 5,4 | 27.075.813 | 3,51 | 127.297 |
| Notificações | 1.302.068 | 5,3 | — | — | 82.389 |
| Externa | 1.124.189 | 4,6 | — | — | 52.886 |
| Páginas do canal | 481.288 | 2,0 | 9.794.878 | 3,36 | 29.034 |
| Outros recursos do YouTube | 302.896 | 1,2 | — | — | 23.826 |
| Publicidade no YouTube | 219.801 | 0,9 | — | — | 17.756 |
| Origem direta ou desconhecida | 181.574 | 0,7 | — | — | 10.572 |
| Telas finais | 69.596 | 0,3 | — | — | 7.150 |
| Playlists | 65.247 | 0,3 | 1.092.103 | 2,68 | 5.815 |
| Anotações e cards de vídeo | 23.948 | 0,1 | — | — | 1.595 |
| Shorts relacionados | 14.044 | 0,1 | — | — | 451 |
| Páginas de hashtag | 6.043 | 0,0 | — | — | 146 |
| Páginas de música | 1.319 | 0,0 | — | — | 8 |
| Vídeo remixado | 93 | 0,0 | — | — | 0 |
| Feed vertical ao vivo | 9 | 0,0 | — | — | 0 |
| Páginas dos produtos | — | 0,0 | 5 | 0,00 | — |

### 6b. Origem do tráfego, vitalício (longos, Studio)

| origem | views | % views | impressões | CTR (%) | horas |
|---|---|---|---|---|---|
| Recursos de navegação | 5.142.238 | 39,4 | 25.149.823 | 7,18 | 375.781 |
| Pesquisa do YouTube | 3.261.671 | 25,0 | 8.445.322 | 12,32 | 205.195 |
| Vídeos sugeridos | 1.253.299 | 9,6 | 10.056.708 | 3,63 | 119.985 |
| Notificações | 1.158.130 | 8,9 | — | — | 75.223 |
| Externa | 1.075.343 | 8,2 | — | — | 51.054 |
| Páginas do canal | 381.851 | 2,9 | 2.640.952 | 3,47 | 26.785 |
| Outros recursos do YouTube | 232.177 | 1,8 | — | — | 22.388 |
| Publicidade no YouTube | 217.590 | 1,7 | — | — | 17.519 |
| Origem direta ou desconhecida | 174.965 | 1,3 | — | — | 9.985 |
| Telas finais | 68.590 | 0,5 | — | — | 7.036 |
| Playlists | 61.127 | 0,5 | 434.992 | 2,36 | 5.599 |
| Anotações e cards de vídeo | 23.598 | 0,2 | — | — | 1.558 |
| Shorts relacionados | 13.934 | 0,1 | — | — | 451 |
| Páginas de hashtag | 2.224 | 0,0 | — | — | 126 |
| Feed dos Shorts | 11 | 0,0 | — | — | 0 |
| Páginas de música | 9 | 0,0 | — | — | 1 |
| Vídeo remixado | 6 | 0,0 | — | — | 0 |
| Páginas dos produtos | — | 0,0 | 4 | 0,00 | — |

### 6c. % das views por origem, mês a mês (todos, Studio, últimos 24 meses fechados)

| mês | views | Sugeridos | Navegação | Pesquisa | Feed Shorts | Notificações | Externa |
|---|---|---|---|---|---|---|---|
| 2024-10 | 133.261 | 11,7 | 56,3 | 16,3 | 4,1 | 2,6 | 1,7 |
| 2024-11 | 85.552 | 6,9 | 50,5 | 28,3 | 0,6 | 3,1 | 3,1 |
| 2024-12 | 99.102 | 6,3 | 53,7 | 25,9 | 1,2 | 2,0 | 3,5 |
| 2025-01 | 92.691 | 6,4 | 47,6 | 28,5 | 8,0 | 1,3 | 2,2 |
| 2025-02 | 140.651 | 11,6 | 58,0 | 13,4 | 5,4 | 1,3 | 1,9 |
| 2025-03 | 165.726 | 3,5 | 18,7 | 21,4 | 49,9 | 1,3 | 1,4 |
| 2025-04 | 1.438.990 | 0,8 | 2,6 | 11,0 | 83,9 | 0,2 | 0,3 |
| 2025-05 | 1.715.968 | 0,4 | 1,6 | 18,1 | 77,9 | 0,2 | 0,3 |
| 2025-06 | 831.061 | 1,4 | 5,2 | 33,8 | 56,7 | 0,4 | 0,5 |
| 2025-07 | 814.856 | 1,1 | 3,2 | 37,6 | 55,6 | 0,2 | 0,4 |
| 2025-08 | 1.259.005 | 0,6 | 1,9 | 24,2 | 71,5 | 0,2 | 0,2 |
| 2025-09 | 579.453 | 1,8 | 7,6 | 43,7 | 43,9 | 0,4 | 0,4 |
| 2025-10 | 461.031 | 1,9 | 8,0 | 46,3 | 40,2 | 0,7 | 0,8 |
| 2025-11 | 338.452 | 5,1 | 15,7 | 60,4 | 14,7 | 0,7 | 0,5 |
| 2025-12 | 316.204 | 2,9 | 8,5 | 67,9 | 16,8 | 0,9 | 0,5 |
| 2026-01 | 423.778 | 4,6 | 13,6 | 64,8 | 12,8 | 0,7 | 0,7 |
| 2026-02 | 536.962 | 4,1 | 13,3 | 44,6 | 33,5 | 0,9 | 0,7 |
| 2026-03 | 350.248 | 3,0 | 10,8 | 78,2 | 5,1 | 0,5 | 0,4 |
| 2026-04 | 326.526 | 1,4 | 5,5 | 76,8 | 13,5 | 0,5 | 0,4 |
| 2026-05 | 307.657 | 1,4 | 6,3 | 68,6 | 20,7 | 0,8 | 0,4 |
| 2026-06 | 437.391 | 2,8 | 7,4 | 45,0 | 40,4 | 1,7 | 0,3 |
| 2026-07 | 350.911 | 3,0 | 12,6 | 51,5 | 29,0 | 1,2 | 0,3 |
| 2026-08 | 191.130 | 2,5 | 14,3 | 61,3 | 18,2 | 0,8 | 0,4 |
| 2026-09 | 309.080 | 2,5 | 53,6 | 37,4 | 4,1 | 0,4 | 0,2 |

### 6c. % das views por origem, mês a mês (longos, Studio, últimos 24 meses fechados)

| mês | views | Sugeridos | Navegação | Pesquisa | Feed Shorts | Notificações | Externa |
|---|---|---|---|---|---|---|---|
| 2024-10 | 117.676 | 13,3 | 61,7 | 13,6 | 0,0 | 2,1 | 1,6 |
| 2024-11 | 76.434 | 7,7 | 55,1 | 23,6 | 0,0 | 3,0 | 2,9 |
| 2024-12 | 86.188 | 7,3 | 60,7 | 19,2 | 0,0 | 2,1 | 3,0 |
| 2025-01 | 71.536 | 8,2 | 59,9 | 20,6 | 0,0 | 1,6 | 2,7 |
| 2025-02 | 123.779 | 13,1 | 65,1 | 9,3 | 0,0 | 1,4 | 2,0 |
| 2025-03 | 51.871 | 11,0 | 54,0 | 21,1 | 0,0 | 2,3 | 2,9 |
| 2025-04 | 60.144 | 18,9 | 52,3 | 14,5 | 0,0 | 2,3 | 2,7 |
| 2025-05 | 42.480 | 15,9 | 45,4 | 18,8 | 0,0 | 2,8 | 3,8 |
| 2025-06 | 63.060 | 17,5 | 51,4 | 13,9 | 0,0 | 2,8 | 4,5 |
| 2025-07 | 41.951 | 19,8 | 45,7 | 16,9 | 0,0 | 2,2 | 3,8 |
| 2025-08 | 39.288 | 18,3 | 46,0 | 17,6 | 0,0 | 2,0 | 3,5 |
| 2025-09 | 67.530 | 15,2 | 59,6 | 13,0 | 0,0 | 1,7 | 1,9 |
| 2025-10 | 49.273 | 17,1 | 51,6 | 17,2 | 0,0 | 1,9 | 3,3 |
| 2025-11 | 84.960 | 20,2 | 58,8 | 10,7 | 0,0 | 1,3 | 1,3 |
| 2025-12 | 48.204 | 18,8 | 50,8 | 17,3 | 0,0 | 1,6 | 2,2 |
| 2026-01 | 96.788 | 20,2 | 57,0 | 10,5 | 0,0 | 1,4 | 2,2 |
| 2026-02 | 111.683 | 19,7 | 60,9 | 8,5 | 0,0 | 1,4 | 1,3 |
| 2026-03 | 62.120 | 16,8 | 57,7 | 13,4 | 0,0 | 2,2 | 1,8 |
| 2026-04 | 32.859 | 13,7 | 50,3 | 19,5 | 0,0 | 3,3 | 2,3 |
| 2026-05 | 33.990 | 12,4 | 54,2 | 18,7 | 0,0 | 3,0 | 2,2 |
| 2026-06 | 53.444 | 22,6 | 53,5 | 11,4 | 0,0 | 2,0 | 1,2 |
| 2026-07 | 64.917 | 16,5 | 65,0 | 8,0 | 0,0 | 1,9 | 1,0 |
| 2026-08 | 40.792 | 11,8 | 63,1 | 14,8 | 0,0 | 1,7 | 1,2 |
| 2026-09 | 187.125 | 4,1 | 87,5 | 5,5 | 0,0 | 0,5 | 0,2 |

### 6c. % das views por origem, mês a mês (shorts (todos − longos), Studio, últimos 24 meses fechados)

| mês | views | Sugeridos | Navegação | Pesquisa | Feed Shorts | Notificações | Externa |
|---|---|---|---|---|---|---|---|
| 2024-10 | 15.585 | 0,2 | 16,1 | 36,8 | 34,7 | 6,3 | 2,0 |
| 2024-11 | 9.118 | 0,1 | 12,0 | 67,4 | 5,2 | 4,2 | 4,5 |
| 2024-12 | 12.914 | 0,1 | 7,6 | 70,3 | 9,0 | 1,6 | 7,3 |
| 2025-01 | 21.155 | 0,1 | 6,0 | 55,0 | 34,8 | 0,5 | 0,6 |
| 2025-02 | 16.872 | 0,1 | 6,1 | 43,6 | 45,1 | 0,6 | 1,1 |
| 2025-03 | 113.855 | 0,0 | 2,7 | 21,5 | 72,6 | 0,8 | 0,7 |
| 2025-04 | 1.378.846 | 0,0 | 0,5 | 10,9 | 87,5 | 0,1 | 0,2 |
| 2025-05 | 1.673.488 | 0,0 | 0,4 | 18,1 | 79,9 | 0,1 | 0,2 |
| 2025-06 | 768.001 | 0,0 | 1,4 | 35,4 | 61,4 | 0,2 | 0,2 |
| 2025-07 | 772.905 | 0,0 | 0,9 | 38,8 | 58,6 | 0,1 | 0,2 |
| 2025-08 | 1.219.717 | 0,0 | 0,4 | 24,4 | 73,8 | 0,1 | 0,1 |
| 2025-09 | 511.923 | 0,0 | 0,7 | 47,7 | 49,7 | 0,2 | 0,2 |
| 2025-10 | 411.758 | 0,0 | 2,8 | 49,8 | 45,0 | 0,6 | 0,5 |
| 2025-11 | 253.492 | 0,0 | 1,2 | 77,1 | 19,6 | 0,5 | 0,2 |
| 2025-12 | 268.000 | 0,0 | 0,9 | 77,1 | 19,8 | 0,8 | 0,2 |
| 2026-01 | 326.990 | 0,0 | 0,8 | 80,9 | 16,6 | 0,5 | 0,2 |
| 2026-02 | 425.279 | 0,0 | 0,7 | 54,1 | 42,3 | 0,8 | 0,5 |
| 2026-03 | 288.128 | 0,0 | 0,7 | 92,2 | 6,2 | 0,1 | 0,1 |
| 2026-04 | 293.667 | 0,0 | 0,5 | 83,2 | 15,0 | 0,2 | 0,1 |
| 2026-05 | 273.667 | 0,0 | 0,4 | 74,8 | 23,3 | 0,5 | 0,1 |
| 2026-06 | 383.947 | 0,0 | 1,0 | 49,6 | 46,0 | 1,7 | 0,2 |
| 2026-07 | 285.994 | 0,0 | 0,7 | 61,3 | 35,6 | 1,0 | 0,1 |
| 2026-08 | 150.338 | 0,0 | 1,1 | 73,9 | 23,1 | 0,6 | 0,2 |
| 2026-09 | 121.955 | 0,0 | 1,5 | 86,4 | 10,5 | 0,3 | 0,2 |

## 7. Hipóteses (a confirmar ou derrubar)

### H1. Desde 27/08/2026 o contador público de views está inflado 2,5 a 2,8x → **CONFIRMA — amostra pequena: 8 longos**

- longos publicados a partir de 27/08 (n = 8): views ÷ views intencionais = 3,39; longos dos 120 dias anteriores (n = 33): 1,09 → fator 3,12x (Analytics por vídeo)
- canal inteiro, 28 dias antes × depois (canal_por_dia, 28+28 dias): views ÷ intencionais 1,76 → 2,89 (1,64x); views por minuto assistido 1,36x. O canal mistura Shorts, cuja razão já era ~2.
- Shorts: views ÷ intencionais 1,07 nos publicados antes de 31/03/2025 e 2,21 depois, sem o outlier (mudança de contagem dos Shorts, outro efeito)
- 2026-09: views de longos 187.475 (4,6x o mês anterior), mas inscritos ganhos 503; pelo modelo de conversão seriam 2.881. As views a mais não trouxeram inscritos.
- Regra: Fator = (views ÷ intencionais dos longos publicados depois) ÷ (o mesmo nos 120 dias antes); sem longos novos, a série diária do canal. CONFIRMA se ≥ 2,2x; PARCIAL se ≥ 1,3x; DERRUBA abaixo.

### H2. Vídeos de caso com nome convertem 6 a 8 inscritos por mil views; alerta macro e plano de renda ~2 → **DERRUBA**

- últimos 12 meses: plano de renda 11,7/mil (n = 10); produto / comparativo 7,1/mil (n = 25); alerta macro 7,1/mil (n = 23); outros 6,4/mil (n = 17); educativo / iniciante 5,4/mil (n = 1); caso com nome 4,0/mil (n = 12)
- vitalício: plano de renda 14,8/mil (n = 62); produto / comparativo 14,4/mil (n = 190); outros 14,0/mil (n = 107); caso com nome 13,1/mil (n = 151); educativo / iniciante 11,9/mil (n = 48); alerta macro 9,8/mil (n = 123)
- razão caso ÷ (alerta macro, plano de renda), últimos 12 meses: 0,42x
- Regra: Inscritos ganhos ÷ views (Analytics) × 1000, longos publicados nos últimos 12 meses. CONFIRMA se caso ∈ [5; 9] e a média de alerta macro/plano de renda ∈ [1; 3]; PARCIAL se caso ≥ 1,5× essa média; DERRUBA abaixo. Tema por regra sobre o título: confira temas_por_video.csv.

### H3. A origem "Recomendados" caiu de 29% para 2% das views → **PARCIAL**

- API, todos · Sugeridos (RELATED_VIDEO), 2025-04 a 2026-09: início 0,8% · pico 5,1% em 2025-11 · fim (2 últimos) 2,4% · último mês 2,3% · pico histórico (meses com ≥ 1.000 views) —% em —
- API, todos · Navegação (BROWSE), 2025-04 a 2026-09: início 2,6% · pico 51,7% em 2026-09 · fim (2 últimos) 33,0% · último mês 51,7% · pico histórico (meses com ≥ 1.000 views) —% em —
- Studio, todos · Sugeridos (RELATED_VIDEO), 2025-04 a 2026-09: início 0,8% · pico 5,1% em 2025-11 · fim (2 últimos) 2,5% · último mês 2,5% · pico histórico (meses com ≥ 1.000 views) 28,3% em 2018-11
- Studio, todos · Navegação (BROWSE), 2025-04 a 2026-09: início 2,6% · pico 53,6% em 2026-09 · fim (2 últimos) 34,0% · último mês 53,6% · pico histórico (meses com ≥ 1.000 views) 63,7% em 2023-03
- Studio, longos · Sugeridos (RELATED_VIDEO), 2025-04 a 2026-09: início 17,5% · pico 22,6% em 2026-06 · fim (2 últimos) 7,9% · último mês 4,1% · pico histórico (meses com ≥ 1.000 views) 24,7% em 2019-03
- Studio, longos · Navegação (BROWSE), 2025-04 a 2026-09: início 51,4% · pico 87,5% em 2026-09 · fim (2 últimos) 75,3% · último mês 87,5% · pico histórico (meses com ≥ 1.000 views) 87,5% em 2026-09
- Studio, shorts (todos − longos) · Sugeridos (RELATED_VIDEO), 2025-04 a 2026-09: início 0,0% · pico 0,0% em 2025-10 · fim (2 últimos) 0,0% · último mês 0,0% · pico histórico (meses com ≥ 1.000 views) 37,5% em 2020-12
- Studio, shorts (todos − longos) · Navegação (BROWSE), 2025-04 a 2026-09: início 0,5% · pico 2,8% em 2025-10 · fim (2 últimos) 1,3% · último mês 1,5% · pico histórico (meses com ≥ 1.000 views) 56,9% em 2021-08
- A leitura que mais se aproxima de 29% → 2%: Studio, longos · Sugeridos (22,6% → 7,9%)
- Regra: Testa Sugeridos (RELATED_VIDEO) e Navegação (BROWSE) em cada formato, nos últimos 18 meses fechados. CONFIRMA se alguma série começa (ou tem pico) ≥ 20% e termina ≤ 5%; PARCIAL se caiu pela metade ou mais; DERRUBA se não caiu.

### H4. O tema explica 20 a 50x da diferença de views; a abertura quase não separa top de fracos → **DERRUBA**

- mediana de views do melhor tema ÷ pior tema (longos, temas com ≥ 3 vídeos): 2,1x
- parte da variação de log(views) explicada pelo tema (eta²): 10,1%
- retenção aos 30 s, top × fracos: —% × —% (diferença — p.p.; vem de retencao_30s.csv)
- proxy sem os 30 s: % média assistida, top × fracos: 36,9% × 41,0%
- Regra: CONFIRMA se a razão de temas ∈ [20; 50]x e a abertura difere ≤ 5 p.p. (ou não foi medida); PARCIAL se a razão ≥ 5x; DERRUBA abaixo. Sem retencao_30s.csv a parte da abertura fica em aberto.

### H5. Os Shorts davam 40% dos inscritos e foram encerrados em 28/07/2026 → **PARCIAL**

- fatia dos inscritos ganhos vinda de Shorts, 2026-02 a 2026-07: 27,5%; em toda a janela de 18 meses: 40,8% (estimativa: regressão dos inscritos ganhos do mês sobre as views de longos e de Shorts (Studio, 17 meses, R² = 0,91): 14,7 inscritos por mil views de longos e 1,04 por mil de Shorts)
- Shorts publicados: 45 de 2026-02 a 2026-07 (7,5/mês); depois de 28/07: 11 (2026-08: 7, 2026-09: 4). Os Shorts foram reduzidos, não encerrados.
- inscritos ganhos por mês: média 1.170 de 2026-02 a 2026-07 → 540 depois (576, 503); views de Shorts por mês: 320.196 → 129.732
- Regra: CONFIRMA se a fatia ∈ [30; 50]% e não houve Short depois de 28/07; PARCIAL se a fatia ≥ 20% (ou os Shorts só diminuíram); DERRUBA abaixo. Sem creatorContentType na API, a fatia é estimada.

## 8. O que o público pergunta

12318 comentários; 1777 perguntas (29,5% dos comentários de topo do público); 56,9% das perguntas têm resposta do canal.

Termos mais frequentes nas perguntas: conta (358), cartao (271), next (222), tenho (188), credito (169), dinheiro (161), banco (129), debito (85), investir (73), usar (73), reais (72), bradesco (72), sem (71), pagar (71), mes (70), faco (70), cartao credito (70), abrir (70), valor (69), nubank (69), sera (68), vou (67), conta next (66), mesmo (64), dias (63)

Perguntas mais curtidas:

- (156 likes, fDUsjBJQmC4) Po tanaka, a essas horas? A gente compra renda, eu vendi 2 casas em 2019, recebia, 0,4 e 0,35% de yeld em cada uma. Hoje tenho uma carteira de 800 k e recebi em jan 0,99, que paga mais e 0,85 esse mês
- (94 likes, 0kD4_42HV24) ITSA4 caiu? Compro. Lateralizou? Compro. Subiu? Compro. Quem é a ITSA4? Para o cego, é a luz. Para o faminto, é o pão. Para o sedento, é a fonte de água. Para o morto, é a vida. Para o enfermo, é a cu
- (93 likes, 1EGx_IxWSbo) novo em criptomoeda e não entende como isso realmente funciona. Alguém pode me orientar sobre a abordagem certa para investir e obter um bom lucro com o investimento em criptomoeda?
- (92 likes, flmY3ta0ClE) Como vou entender o golpe com esse áudio no 10x kkkkkk
- (88 likes, aDL4MMF6AnE) É possível comprovar fazendo uma progressão geométrica. Acontece da seguinte forma: a1 é o termo inicial que no nosso caso é 1 centavo. Sendo assim a1=1 A fórmula canónica é a seguinte an=a1×r^(n-1) O
- (64 likes, fDUsjBJQmC4) FII são para Renda , Ciclo Imobiliario é no Mínimo 10 anos e os últimos 5 anos tivemos uma Pandemia E atualmente uma Praga...Impossível FII ter bom desempenho com TD esse Macro. ( da mesma forma que a
- (40 likes, SsZAITSAR6s) Mas se o menor de 18 anos fizer uma divida a responsabilidade é do menor né?
- (33 likes, tbKsF2qyakU) Muito vago japaooooo....qual a taxa de retorno ?...qual investimento ?...
- (30 likes, _I5dFQ6mvK0) Quando o produto é de graça é porque o produto é você.
- (28 likes, -b6Jdl4zFKg) A conta do seu Carlos deixa todas as menininhas apaixonadas !Loucas de amor!A rizada do seu Carlos?Ele rindo e pensando?Ela é tão inocente, achando que vai dar o golpe ,quando na realidade ela é só a 
- (28 likes, fDUsjBJQmC4) Gerdau não subiu por recompra de posição vendida. Eles tem fábricas em solo americano, e se beneficiam potencialmente das taxas. Não sabia?
- (24 likes, _I5dFQ6mvK0) Faz um vídeo explicando como declara o imposto de renda do zero! Vlw vídeo ótimo
- (24 likes, bStv54OaC_8) Se eu tenho uma conta no next, e faço uma transferência para bancos como (Itaú, santander e etc) o next cobra?
- (22 likes, _I5dFQ6mvK0) Fala Japa, tudo na paz? Eu sou novo aqui e esse foi p primeiro vídeo seu q assisti e já me amarrei! Só duas perguntas: O fato de declarar não significa q terei q pagar né, mesmo aceitando a doação mes
- (20 likes, 4zHZprjxLu4) Sou novo no comércio. Como posso fazer um investimento mais lucrativo em criptomoedas sem incorrer em grandes perdas?

### 8b. Todos os comentários do público por tema (9482 em 30 vídeos; 2194 deles, 23,1%, são do vídeo `aDL4MMF6AnE`)

| tema | comentários | % | perguntas | exemplos (sem autor) |
|---|---|---|---|---|
| outros | 4528 | 47,8 | 923 | “Muito vago japaooooo....qual a taxa de retorno ?...qual investimento ?...” · “Quando o produto é de graça é porque o produto é você.” |
| Bancos digitais, contas e cartões | 2439 | 25,7 | 1093 | “Se eu tenho uma conta no next, e faço uma transferência para bancos como (Itaú, santander e etc) o next cobra?” · “Tem como (a)(o)s menino(a)s comprar acoes por essa conta do next , Japa ?” |
| Crítica, dúvida sobre o conteúdo ou ironia | 679 | 7,2 | 40 | “É o mesmo discurso daqueles que falam : " é só vender R$2800 por dia que em 1 ano vc junta 1 milhão" como se fosse a coi” · “Aí todo mundo corre para investir sobe o valor e ele vende kkkkkkkkkkk” |
| Começar com pouco / centavos | 344 | 3,6 | 81 | “Se 1 Centavo vira 10 milhões, r$ 1 vira 1Bilhão?” · “Tá, dobrar um centavo em que? No rolo compressivo ou pode ser na marretada mesmo? 📚✅✅🤣” |
| Elogio ou agradecimento | 281 | 3,0 | 18 | “*Um ótimo vídeo, como sempre.* Todos devem aprender a trabalhar duro, ser disciplinados e pacientes para alcançar grande” · “Boa noite meu querido!! Sempre renovando vc e foda meu querido 😎😎😎 muito bom as dicas...” |
| Ações (empresas e tickers) | 193 | 2,0 | 58 | “Japa, o que aconteceu com vvar3? Levei uma queda. Diz aí” · “Qual corretora Luis Barsi investe?” |
| Crise, governo e macro | 159 | 1,7 | 22 | “Quando a crise realmente bater, os investidores grandes comem os pequenos. Provável que voce também não vá gostar da cri” · “Poderia falar mais sobre os juros composto? Ótimo canal japonês 👍” |
| Imposto de renda e tributação | 140 | 1,5 | 42 | “Faz um vídeo explicando como declara o imposto de renda do zero! Vlw vídeo ótimo” · “Olá, é a primeira vez que vejo o seu canal e gostei, tem como fazer um passo a passo de como fazer está declaração?” |
| ETFs, BDRs e exterior | 136 | 1,4 | 40 | “Japão! Que tal você fazer um vídeo "a BDR do mês" comentando sobre esses ativos. Por exemplo, vale a pena comprar BDR da” · “Quais são os impostos cobrados para quem pensa em investir em etfs?” |
| Fundos imobiliários (FIIs) | 129 | 1,4 | 28 | “Tanaka, vou ganhar 300,000 de herança, quero colocar tudo em fundo imobiliário. Quais os mais seguros para investir ?? P” · “referente ao spyi11 o percentual que eh cobrado eh sobre o lucro?” |
| Dividendos e renda passiva | 122 | 1,3 | 47 | “Ok... Concordo em partes..mas em capital total que vc tem hj nos fundos de 2019 você consegue comprar novamente suas cas” · “Olá, ótimo vídeo! Poderia me esclarecer se o banco cobra taxa mensal ?” |
| Menor de idade e filhos | 121 | 1,3 | 41 | “Mas se o menor de 18 anos fizer uma divida a responsabilidade é do menor né?” · “Grande Japa, fala ai como faço para comprar açoes no nome do meu filho de 11 anos?” |
| Tesouro Direto e renda fixa | 104 | 1,1 | 34 | “Tenho 80 k e seria bom colocar no LCI por 12 meses?” · “Eu havia entendido q era possível usar o fgts para investir em renda fixa e não se tem garantia pelo fgc. É possível usa” |
| Cripto | 92 | 1,0 | 25 | “Sou novo no comércio. Como posso fazer um investimento mais lucrativo em criptomoedas sem incorrer em grandes perdas?” · “Pra investir em Bitcoin pelo mercado pago,precisa declarar imposto de renda?” |
| Aposentadoria e previdência | 15 | 0,2 | 3 | “Eu sou isenta do imposto . Tamb terei que pagar? Sou aposentada por invalidez” · “Oii eu sou aposentado posso investir nisso? Tenq declara ?” |

## 10. Conta da meta (200 mil inscritos até 31/12/2026)

- Inscritos hoje: 165.000 (contador público arredondado do YouTube, LEIAME_DADOS.md).
- Faltam 35.000 em 91 dias: 11.692 líquidos por mês (385 por dia).
- Ritmo real: 221 líquidos no último mês fechado; média de 424 por mês nos últimos 6 meses; melhor mês dos últimos 18: 2.097 (2025-05).
- O necessário é 28x a média dos últimos 6 meses e 5,6x o melhor mês.
- No ritmo dos últimos 6 meses, o canal chega a 31/12/2026 com cerca de 166.269 inscritos; 200 mil chegariam em 08/2033 (daqui a ~7 anos).
