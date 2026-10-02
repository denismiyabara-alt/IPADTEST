# Resultados da auditoria (gerado por analisar.py)

Dados até 2026-09-30. 972 vídeos; 471 Shorts. Exportações do Studio: studio_conteudo_longos, studio_conteudo_shorts, studio_origem_trafego_mensal, studio_origem_trafego_mensal_longos.

Studio casado com videos.csv: 972 por ID, 0 por título, 0 sem par.

**Atenção:** sem videos.csv e sem Analytics: a base é só o Studio (formato = de qual exportação veio; dia e hora vazios). Rode o exportar.py no Mac para completar.

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

## 0b. Views ÷ views intencionais (engajadas), por formato

Se o contador de views estiver inflado em relação às views intencionais, a razão sobe. Em Shorts, a contagem mudou em 31/03/2025. Os outliers (um vídeo com ≥ 40% das views do grupo) ficam de fora das linhas por período.

| formato | grupo | vídeos | views | intencionais | views ÷ intenc. (soma) | mediana por vídeo | insc./mil views | insc./mil intenc. | CTR (%) | impressões |
|---|---|---|---|---|---|---|---|---|---|---|
| longo | todos | 500 | 9.376.916 | 9.237.370 | 1,02 | 1,00 | 13,61 | 13,82 | 7,77 | 29.943.325 |
| longo | publicados antes de 27/08/2026 | 492 | 9.200.569 | 9.184.814 | 1,00 | 1,00 | 13,84 | 13,87 | 7,81 | 29.337.158 |
| longo | publicados a partir de 27/08/2026 | 8 | 176.347 | 52.556 | 3,36 | 3,30 | 1,54 | 5,18 | 6,18 | 606.167 |
| short | todos | 466 | 11.223.227 | 5.748.314 | 1,95 | 1,02 | 1,37 | 2,67 | 5,47 | 23.722.143 |
| short | sem outlier — fora: aDL4MMF6AnE (Pra ficar rico você só precisa de 1 cent) | 465 | 3.205.505 | 2.204.558 | 1,45 | 1,02 | 1,76 | 2,56 | 5,29 | 9.391.278 |
| short | publicados antes de 31/03/2025 | 344 | 1.564.499 | 1.463.248 | 1,07 | 1,01 | 2,90 | 3,10 | 4,86 | 7.437.461 |
| short | publicados a partir de 31/03/2025 | 119 | 1.641.004 | 741.308 | 2,21 | 2,06 | 0,67 | 1,48 | 6,96 | 1.953.814 |

## 1. Conversão por formato (inscritos ganhos por mil views)

| formato | vídeos | views | % views | mediana views | insc./mil views | insc./mil engajadas | % média assistida | CTR mediano |
|---|---|---|---|---|---|---|---|---|
| short | 471 | 11.223.227 | 54,5 | 2.270 | 1,37 | 2,67 | 81,6 | 3,32 |
| longo | 501 | 9.376.916 | 45,5 | 12.817 | 13,61 | 13,82 | 50,2 | 2,48 |
| short sem outlier | 470 | 3.205.505 | 100,0 | 2.261 | 1,76 | 2,56 | 81,6 | 3,31 |

## 2a. Por tema (longos)

| tema | vídeos | views | % views | mediana views | insc./mil views | CTR mediano | % média assistida |
|---|---|---|---|---|---|---|---|
| caso com nome | 176 | 3.446.765 | 36,8 | 13.234 | 13,49 | 2,32 | 53,0 |
| produto / comparativo | 182 | 2.549.839 | 27,2 | 11.882 | 14,64 | 1,66 | 53,9 |
| alerta macro | 51 | 966.326 | 10,3 | 11.111 | 10,61 | 6,15 | 39,8 |
| outros | 47 | 923.729 | 9,9 | 14.961 | 15,89 | 3,84 | 41,3 |
| educativo / iniciante | 20 | 857.114 | 9,1 | 14.152 | 11,59 | 2,79 | 43,9 |
| plano de renda | 25 | 633.143 | 6,8 | 25.503 | 14,13 | 5,06 | 38,4 |

## 2b. Por tema (shorts)

| tema | vídeos | views | % views | mediana views | insc./mil views | CTR mediano | % média assistida |
|---|---|---|---|---|---|---|---|
| outros | 194 | 9.294.440 | 82,8 | 1.992 | 1,17 | 3,08 | 81,9 |
| caso com nome | 60 | 763.185 | 6,8 | 3.939 | 1,84 | 3,59 | 78,8 |
| produto / comparativo | 122 | 594.520 | 5,3 | 2.336 | 2,95 | 3,62 | 83,2 |
| alerta macro | 62 | 279.403 | 2,5 | 1.929 | 1,86 | 3,09 | 74,5 |
| plano de renda | 17 | 194.887 | 1,7 | 4.123 | 3,08 | 3,07 | 92,8 |
| educativo / iniciante | 16 | 96.792 | 0,9 | 3.453 | 1,84 | 3,69 | 98,6 |

## 3. Concentração das views

| grupo | vídeos | % top 1 | % top 5 | % top 10 | % top 10% dos vídeos | vídeos p/ 50% | vídeos p/ 80% | Gini |
|---|---|---|---|---|---|---|---|---|
| todos | 972 | 38,9 | 43,8 | 46,9 | 64,8 | 18 | 270 | 0,73 |
| longos | 501 | 4,7 | 11,3 | 16,2 | 34,9 | 108 | 297 | 0,39 |
| shorts | 471 | 71,4 | 76,6 | 79,9 | 88,2 | 1 | 11 | 0,91 |

## 4. Top × fracos (longos de 14 a 540 dias de vida; quartil de cima × de baixo)

|  | top | fracos |
|---|---|---|
| vídeos | 10 | 10 |
| mediana de views | 30.200 | 8.100 |
| inscritos por mil views | 10,86 | 6,98 |
| temas | plano de renda 50%, alerta macro 40%, caso com nome 10% | alerta macro 40%, plano de renda 20%, produto / comparativo 20% |
| % caso com nome | 10 | 10 |
| duração mediana (min) | 14,4 | 19,2 |
| título: caracteres | 59 | 63 |
| % título com número | 70 | 70 |
| % título com ? | 30 | 30 |
| % título em caixa alta | 60 | 30 |
| dia mais comum | — | — |
| hora mediana (Brasília) | — | — |
| CTR mediano (%) | 6,67 | 5,37 |
| impressões medianas | 276.815 | 91.504 |
| % média assistida | 36,6 | 37,6 |
| retenção aos 30 s (%) | — | — |

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

### H1. Desde 27/08/2026 o contador público de views está inflado 2,5 a 2,8x → **CONFIRMA (inflação maior que a hipótese)**

- views por minuto assistido, 28 dias depois ÷ antes (canal_por_dia, 0+0 dias): —x
- views ÷ views engajadas, depois ÷ antes: —x
- longos: mediana de contador público ÷ engajadas, publicados depois (8) ÷ 120 dias antes (6): 3,23x (antes 1,02, depois 3,30)
- Shorts: contador público ÷ engajadas antes de 31/03/2025: 1,01; depois: 2,06 (a contagem de Shorts mudou nessa data; não confundir com o efeito de 27/08)
- Regra: CONFIRMA se o fator (engajadas; senão vídeos; senão minutos) for ≥ 2,2x (acima de 3,2x, a inflação é maior que a hipótese); PARCIAL se ≥ 1,3x; DERRUBA abaixo disso.

### H2. Vídeos de caso com nome convertem 6 a 8 inscritos por mil views; alerta macro e plano de renda ~2 → **DERRUBA**

- caso com nome: 13,49 por mil (176 longos)
- produto / comparativo: 14,64 por mil (182 longos)
- alerta macro: 10,61 por mil (51 longos)
- outros: 15,89 por mil (47 longos)
- educativo / iniciante: 11,59 por mil (20 longos)
- plano de renda: 14,13 por mil (25 longos)
- Regra: CONFIRMA se caso ∈ [5; 9] e a média de alerta macro/plano de renda ∈ [1; 3]; PARCIAL se caso ≥ 2× a média dos outros dois; DERRUBA abaixo disso. Confira a classificação em temas_por_video.csv.

### H3. A origem "Recomendados" caiu de 29% para 2% das views → **PARCIAL**

- Studio, todos · Sugeridos (RELATED_VIDEO), 2025-04 a 2026-09: início 0,8% · pico 5,1% em 2025-11 · fim (2 últimos) 2,5% · último mês 2,5% · pico histórico (meses com ≥ 1.000 views) 28,3% em 2018-11
- Studio, todos · Navegação (BROWSE), 2025-04 a 2026-09: início 2,6% · pico 53,6% em 2026-09 · fim (2 últimos) 34,0% · último mês 53,6% · pico histórico (meses com ≥ 1.000 views) 63,7% em 2023-03
- Studio, longos · Sugeridos (RELATED_VIDEO), 2025-04 a 2026-09: início 17,5% · pico 22,6% em 2026-06 · fim (2 últimos) 7,9% · último mês 4,1% · pico histórico (meses com ≥ 1.000 views) 24,7% em 2019-03
- Studio, longos · Navegação (BROWSE), 2025-04 a 2026-09: início 51,4% · pico 87,5% em 2026-09 · fim (2 últimos) 75,3% · último mês 87,5% · pico histórico (meses com ≥ 1.000 views) 87,5% em 2026-09
- Studio, shorts (todos − longos) · Sugeridos (RELATED_VIDEO), 2025-04 a 2026-09: início 0,0% · pico 0,0% em 2025-10 · fim (2 últimos) 0,0% · último mês 0,0% · pico histórico (meses com ≥ 1.000 views) 37,5% em 2020-12
- Studio, shorts (todos − longos) · Navegação (BROWSE), 2025-04 a 2026-09: início 0,5% · pico 2,8% em 2025-10 · fim (2 últimos) 1,3% · último mês 1,5% · pico histórico (meses com ≥ 1.000 views) 56,9% em 2021-08
- A leitura que mais se aproxima de 29% → 2%: Studio, longos · Sugeridos (22,6% → 7,9%)
- Regra: Testa Sugeridos (RELATED_VIDEO) e Navegação (BROWSE) em cada formato, nos últimos 18 meses fechados. CONFIRMA se alguma série começa (ou tem pico) ≥ 20% e termina ≤ 5%; PARCIAL se caiu pela metade ou mais; DERRUBA se não caiu.

### H4. O tema explica 20 a 50x da diferença de views; a abertura quase não separa top de fracos → **DERRUBA**

- mediana de views do melhor tema ÷ pior tema (longos, temas com ≥ 3 vídeos): 2,5x
- parte da variação de log(views) explicada pelo tema (eta²): 14,4%
- retenção aos 30 s, top × fracos: —% × —% (diferença — p.p.; vem de retencao_30s.csv)
- proxy sem os 30 s: % média assistida, top × fracos: 36,6% × 37,6%
- Regra: CONFIRMA se a razão de temas ∈ [20; 50]x e a abertura difere ≤ 5 p.p. (ou não foi medida); PARCIAL se a razão ≥ 5x; DERRUBA abaixo. Sem retencao_30s.csv a parte da abertura fica em aberto.

### H5. Os Shorts davam 40% dos inscritos e foram encerrados em 28/07/2026 → **DERRUBA**

- % dos inscritos ganhos vindos de Shorts nos 6 meses antes de 07/2026 (canal_por_mes): —%
- % dos inscritos ganhos em Shorts no período todo (por vídeo): 10,7%
- último Short publicado: 2026-09-30; Shorts publicados depois de 28/07: 11 (04/08 BooCl9y-7Oc; 05/08 F4y6q8U6uO4; 05/08 Anljp-ug3eU; 06/08 hry1B6zzUeM; 19/08 hUosb0HS0v8; 20/08 UgRPCygEDG0; 31/08 iQ0hnkj6YXY; 02/09 B7pTiwxsWaI; 29/09 u-ua0-iDnow; 30/09 oMnXltEe4P8; 30/09 dc3o6w2vIvQ)
- Regra: CONFIRMA se a fatia ∈ [30; 50]% e não houve Short depois de 28/07; PARCIAL se a fatia ≥ 20%; DERRUBA abaixo.
