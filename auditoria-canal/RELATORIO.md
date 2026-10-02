# Auditoria do canal Investir e Coçar

Dados até 01/10/2026. Os números vêm de `dados/` (Data API + Analytics API, exportados em 02/10/2026) e das exportações do Studio em `dados/studio/` (E1 longos, E2 Shorts, E3 origem do tráfego). Todas as tabelas saem de `python3 analisar.py`, que grava `analise/RESULTADOS.md`; a seção de cada número está indicada como (R§n).

## Resumo em 6 linhas

1. **A meta não fecha.** Faltam 35.000 inscritos em 91 dias: são 11.692 líquidos por mês. A média dos últimos 6 meses é de 424 por mês (221 em setembro). O necessário é 28 vezes o ritmo atual e 5,6 vezes o melhor mês dos últimos 18 (R§10).
2. **Desde 27/08, o contador público não mede audiência.** Nos longos publicados depois de 27/08, há 3,4 views para cada view intencional; antes, era 1,1. Em setembro, as views de longos foram 4,6 vezes as de agosto, e os inscritos caíram para 503 (H1).
3. **O inflado vem da página inicial (Navegação),** não da perda de "Recomendados". Nos longos, as views de Navegação foram de 25,8 mil em agosto para 163,7 mil em setembro (R§6c).
4. **Os inscritos caíram pela metade depois de julho:** a média de fevereiro a julho de 2026 foi de 1.170 ganhos por mês; a de agosto e setembro, 540. Cerca de um terço da queda se explica pela redução dos Shorts (H5).
5. **O tema não explica 20 a 50x da diferença** (é 2,1x), e "caso com nome" não converte mais que os outros temas (H2, H4). **A abertura também não separa:** aos 30 s, o top retém 71,3% e os fracos 73,7% (n = 10 de cada lado). Pelo que os dados mostram, as linhas que mais convertem nos últimos 12 meses são renda mensal (ETFs e dividendos mensais) e Tesouro/IPCA+.
6. **285 longos que estão fora do ar (privados ou excluídos) fizeram 32,7% dos inscritos históricos vindos de longos** (R§0b).

---

## 1. Hipóteses: o que os dados dizem

| # | hipótese | veredito | número que decide | amostra |
|---|---|---|---|---|
| H1 | Desde 27/08, contador público inflado 2,5 a 2,8x | **CONFIRMA, nos longos novos** (3,1x) / **PARCIAL no canal** (1,6x) | views ÷ views intencionais: 3,39 nos longos publicados a partir de 27/08 × 1,09 nos dos 120 dias anteriores | **8 longos** depois × 33 antes (pequena) |
| H2 | "Caso com nome" converte 6 a 8 por mil; alerta macro e plano de renda ~2 | **DERRUBA** | últimos 12 meses: caso com nome 4,0/mil × alerta macro 7,1 × plano de renda 11,7 | 12 / 23 / 10 longos; tema por regra |
| H3 | "Recomendados" caiu de 29% para 2% | **PARCIAL** | Sugeridos nos longos: 22,6% (jun/26) → 4,1% (set/26). No canal, sempre de 1% a 5% desde abr/25 | 18 meses, Studio |
| H4 | O tema explica 20 a 50x; a abertura quase não separa | **DERRUBA** (tema) / **CONFIRMA** (abertura não separa) | melhor ÷ pior tema: 2,1x; o tema explica 10% da variação. Retenção aos 30 s: mediana de 71,3% no top × 73,7% nos fracos | tema: 681 longos; abertura: **10 + 10 vídeos** |
| H5 | Shorts davam 40% dos inscritos e foram encerrados em 28/07 | **PARCIAL** | Shorts: 40,8% dos inscritos em abr/25 a ago/26 (estimativa) e 27,5% em fev a jul/26. Depois de 28/07 saíram 11 Shorts | modelo com 17 meses, R² = 0,91 |

### H1. Views infladas desde 27/08: confirmada nos longos novos, com amostra pequena

- **Longos, por vídeo (Analytics):** nos 8 longos publicados a partir de 27/08, views ÷ views intencionais = 3,39; nos 33 longos dos 120 dias anteriores, 1,09. Fator: **3,1x**, um pouco acima da faixa de 2,5 a 2,8x. São só 8 vídeos.
- **Canal, por dia (28 dias antes × 28 depois):** views ÷ intencionais foi de 1,76 para 2,89 (1,64x). Views por minuto assistido subiram 1,36x. No canal, o salto é menor porque os Shorts já tinham razão perto de 2 antes de 27/08.
- **A data bate:** nos 28 dias antes, a razão diária ficou entre 1,4 e 2,1; foi a 3,75 em 27/08 e, nos 33 dias seguintes, ficou entre 2,3 e 3,6 (canal_por_dia.csv).
- **As views a mais não trouxeram inscritos.** Em setembro, os longos tiveram 187.475 views (4,6x agosto), quase todas da Navegação. O modelo de conversão do canal (14,7 inscritos por mil views de longos) previa 2.881 inscritos; vieram 503.
- **Nos Shorts, é outro efeito:** nos Shorts publicados a partir de 31/03/2025, a razão já era 2,21 (contra 1,07 antes), sem o outlier "1 centavo". Foi a mudança de contagem dos Shorts. Não confunda com 27/08.
- **Consequência:** a partir de 27/08, "views" no Studio e no contador público não servem para comparar vídeos. Use views intencionais, minutos e inscritos.

### H2. "Caso com nome" converte 6 a 8 por mil: derrubada

| tema (longos) | últimos 12 meses: insc./mil views | n | vitalício: insc./mil views | n |
|---|---|---|---|---|
| plano de renda | **11,7** | 10 | 14,8 | 62 |
| produto / comparativo | 7,1 | 25 | 14,4 | 190 |
| alerta macro | 7,1 | 23 | 9,8 | 123 |
| outros | 6,4 | 17 | 14,0 | 107 |
| caso com nome | **4,0** | 12 | 13,1 | 151 |

Nas duas janelas, "caso com nome" fica abaixo de plano de renda e, nos últimos 12 meses, também de alerta macro. A hipótese previa o contrário: caso com nome 3 a 4 vezes acima.

**Ressalvas:**
- O tema sai de regras sobre o título (`analisar.py`, `ENTIDADES` e `TEMAS`); confira em `analise/temas_por_video.csv`.
- Os grupos dos últimos 12 meses têm de 10 a 25 vídeos.
- O inscrito do Analytics é atribuído ao vídeo onde a pessoa se inscreveu.

### H3. "Recomendados" de 29% para 2%: parcial

"Recomendados", no Studio em português, provavelmente quer dizer **Vídeos sugeridos** (RELATED_VIDEO). Testei também **Recursos de navegação** (BROWSE, a página inicial).

| série (Studio, % das views do mês) | início da janela (abr a jun/25) | pico | fim (ago a set/26) |
|---|---|---|---|
| Longos · Sugeridos | 17,5% | 22,6% (jun/26) | 7,9% (set: 4,1%) |
| Longos · Navegação | 51,4% | 87,5% (set/26) | 75,3% |
| Canal · Sugeridos | 0,8% | 5,1% (nov/25) | 2,5% |
| Shorts · Sugeridos | 0,0% | 0,0% | 0,0% |

- **Nos longos, a queda em % existe,** mas grande parte é efeito do denominador. Em views absolutas, Sugeridos variou com os vídeos que estouraram: 22,0 mil em fev/26, 4,2 mil em mai/26, 12,1 mil em jun/26 e 7,7 mil em set/26. Em setembro, a Navegação inflada (163,7 mil) espremeu a fatia de Sugeridos para 4,1%.
- **No canal todo, "2%" é verdade há 18 meses,** porque os Shorts nunca recebem Sugeridos e dominavam o volume.
- **O pico histórico de Sugeridos nos longos** foi 24,7% (mar/2019). Os 29% não aparecem em nenhum mês com mais de mil views.
- **Veredito:** a origem caiu nos longos (de 22,6% para 4,1%), mas não de 29% para 2%. O movimento grande de 2026 foi a explosão da Navegação em setembro.

### H4. O tema explica 20 a 50x: derrubada; a abertura não separa top de fracos: confirmada

- **Mediana de views:** do melhor tema ÷ a do pior, nos longos = **2,1x**. O tema explica **10%** da variação do log das views (eta²).
- **Top × fracos dos últimos 12 meses:** o top tem 37% de alerta macro, e os fracos, 32% de produto/comparativo. Os mesmos temas aparecem nos dois lados (R§4).
- **Abertura (retenção aos 30 s):**

  | grupo | n | mediana | faixa |
  |---|---|---|---|
  | top | 10 | **71,3%** | 63,4% a 76,0% |
  | fracos | 10 | **73,7%** | 65,7% a 78,2% |

  - A diferença é de −2,4 p.p.: os fracos retêm um pouco mais, e as faixas se sobrepõem quase inteiras.
  - **Método:** Analytics API, `dimensions=elapsedVideoTimeRatio` e `metrics=audienceWatchRatio` por vídeo (vitalício), interpolando no ponto 30 ÷ duração. Não veio do Studio; está em `dados/studio/retencao_30s.csv`.
  - Os 20 vídeos são os da lista da seção 6.
  - **Ressalva:** são 10 vídeos de cada lado. Uma diferença de 2 a 3 p.p. não é detectável com essa amostra, mas uma vantagem grande da abertura no top também não aparece.
- **O proxy aponta para o mesmo lado:** a % média assistida é 36,9% no top e 41,0% nos fracos (quartis de 19 vídeos).
- **Conclusão:**
  - **O que separa top de fracos é a distribuição** (impressões, Navegação e busca), não a abertura nem a retenção. O fraco segura quem chega; chega pouca gente.
  - O próximo esforço vai para pauta, título e thumb, e não para refazer ganchos.

### H5. Shorts davam 40% dos inscritos e foram encerrados: parcial

A API não aceitou `creatorContentType` por mês, e as colunas por formato do `canal_por_mes.csv` vieram vazias. Por isso a fatia é **estimada**: uma regressão dos inscritos ganhos do mês sobre as views de longos e de Shorts (Studio, Total.csv) em 17 meses (abr/25 a ago/26, R² = 0,91) dá **14,7 inscritos por mil views de longos e 1,04 por mil de Shorts**.

- **Fatia estimada dos Shorts nos inscritos:**
  - **40,8%** em abr/25 a ago/26 (a hipótese bate na janela longa);
  - **27,5%** em fev a jul/26, os 6 meses antes de 28/07;
  - 62% a 74% em abr e mai/25, quando os Shorts tinham 1,4 a 1,7 milhão de views por mês.
- **Os Shorts não foram encerrados:**
  - fev a jul/26: 45 publicados (7,5 por mês, com 19 em junho);
  - depois de 28/07: 11 (7 em agosto, 4 em setembro), o último em 30/09.
- **O que aconteceu depois:**
  - views de Shorts: de 320 mil por mês (fev a jul) para 130 mil (ago a set), queda de 60%;
  - inscritos ganhos: de 1.170 por mês para 540;
  - pelo modelo, cerca de 200 inscritos por mês a menos vêm dos Shorts, um terço da queda; o resto é a queda dos longos.

---

## 2. O que separa os top dos fracos

População: longos publicados nos últimos 12 meses, com 30 dias ou mais de vida e pelo menos 500 views intencionais (79 vídeos). A ordem é por inscritos ganhos. Comparo o quartil de cima com o de baixo, 19 vídeos de cada lado (R§4).

| | top | fracos |
|---|---|---|
| inscritos ganhos (mediana) | 131 | 9 |
| views intencionais (mediana) | 15.781 | 2.238 |
| inscritos por mil views intencionais | 11,5 | 3,6 |
| temas principais | alerta macro 37%, produto 26%, plano de renda 21% | produto 32%, alerta macro 26%, outros 26% |
| duração mediana | 16,0 min | 13,4 min |
| título com "?" | 37% | 53% |
| título mais em caixa alta | 32% | 47% |
| dia mais comum / hora mediana | terça / 19 h | quinta / 19 h |
| CTR (Studio) | 6,67% | sem dado (fora dos 500 da exportação) |
| % média assistida | 36,9% | 41,0% |

**O que separa, com os dados que há:**

1. **Alcance, não conversão nem abertura.** O top converte 3x mais por view intencional (11,5 contra 3,6 por mil) e tem 7x mais views intencionais. O fraco não "segura menos": tem % média assistida maior (41,0% contra 36,9%) e retenção aos 30 s parecida (73,7% contra 71,3%; n = 10 de cada lado). Ele simplesmente não é distribuído.
2. **Linhas de renda mensal e de Tesouro/IPCA+.** Nos últimos 12 meses:

   | linha | inscritos por mil views intencionais | resto | n |
   |---|---|---|---|
   | dividendos mensais (ETFs, "todos os meses") | 14,5 | 8,2 | 6 |
   | Tesouro/IPCA+/renda fixa (mediana de 142 inscritos por vídeo) | 11,0 | 8,8 | 5 |
   | ETFs | 11,8 | 8,6 | 11 |

   Dos 10 vídeos top do ano, 3 são de renda mensal e 3 de Tesouro/IPCA+. As amostras são pequenas.
3. **Duração de 15 a 20 min:** mediana de 31,5 inscritos por vídeo (n = 32), contra 20 nos de 10 a 15 min (n = 34).
4. **Títulos com pergunta e em caixa alta aparecem mais entre os fracos** (53% contra 37%; 47% contra 32%). Com 19 vídeos de cada lado, isso é pista para teste A/B, não regra.
5. **Dia e hora não separam:** quase tudo sai às 19 h, e a diferença entre terça e quinta está dentro do ruído (medianas de 31 e 34 inscritos).
6. **Thumb e CTR:** só o top tem CTR na exportação do Studio (6,67%). Para comparar, exporte do Studio os longos dos últimos 12 meses (filtro por data), que cabem nas 500 linhas.

## 3. Evolução mês a mês (R§5)

| mês | views (Analytics) | views intencionais | views longos | views Shorts | inscritos ganhos | perdidos | líquidos |
|---|---|---|---|---|---|---|---|
| abr/25 | 1.438.990 | 637.574 | 60.144 | 1.378.833 | 1.907 | 473 | 1.434 |
| mai/25 | 1.715.968 | 748.461 | 42.480 | 1.673.481 | 2.630 | 533 | **2.097** |
| ago/25 | 1.259.005 | 560.576 | 39.288 | 1.219.709 | 1.779 | 483 | 1.296 |
| out/25 | 461.031 | 237.265 | 49.273 | 411.744 | 1.150 | 440 | 710 |
| jan/26 | 423.778 | 253.759 | 96.788 | 326.970 | 1.906 | 463 | 1.443 |
| fev/26 | 536.962 | 318.642 | 111.683 | 425.259 | 2.323 | 499 | 1.824 |
| abr/26 | 326.526 | 173.769 | 32.859 | 293.655 | 795 | 370 | 425 |
| jun/26 | 437.391 | 219.079 | 53.444 | 373.846 | 1.026 | 374 | 652 |
| jul/26 | 350.911 | 194.841 | 64.917 | 268.568 | 971 | 385 | 586 |
| ago/26 | 191.130 | 100.590 | 40.792 | 137.813 | 576 | 328 | 248 |
| set/26 | 278.349 | 95.645 | 187.475* | 121.651 | 503 | 282 | **221** |

\* Inflado (H1). A tabela completa, com os 18 meses, está em R§5.

**Leitura:**
- **2025 foi puxado por Shorts virais:** mais de 1,2 milhão de views por mês em abr, mai e ago.
- **2026 teve dois bons meses de longos,** jan e fev, com 97 e 112 mil views e cerca de 1.400 a 1.800 líquidos.
- **De abr/26 em diante,** os longos ficaram entre 33 e 65 mil views por mês.
- **Depois de julho,** os Shorts caíram, e os inscritos líquidos chegaram ao menor nível da série (221 em setembro).
- **Perdas:** ficaram estáveis ou caindo (de 533 para 282 por mês). A razão perdidos ÷ ganhos subiu de 25% para 56% só porque os ganhos caíram. O problema é ganhar, não perder.

## 4. Concentração (R§3 e R§0b)

- **Longos públicos (681):** 71 vídeos fazem 50% das views; os 10 maiores fazem 21%; Gini 0,59.
- **Longos dos últimos 12 meses:** os 10 melhores fizeram **58% dos inscritos** (5.327 no total, em 80 vídeos); os 5 melhores, 39%.
- **Shorts:** um único vídeo ("1 centavo", `aDL4MMF6AnE`) tem 71% das views de Shorts (8,0 mi de 11,2 mi) e 9.675 inscritos. Fica à parte em todas as comparações.
- **Fora do ar:** 285 longos que estão no Studio, mas não na playlist pública (privados, não listados ou excluídos), somam 4,15 mi de views e 52.351 inscritos: 31,7% das views e 32,7% dos inscritos vitalícios vindos de longos. Os maiores são de 2020 a 2022, sobre bancos digitais (Next, Nubank, Santander) e ações (IRBR3, OIBR3).

## 5. Shorts × longos

| | longos | Shorts | fonte |
|---|---|---|---|
| inscritos por mil views (vitalício, por vídeo) | 12,9 | 1,37 (1,78 sem o "1 centavo") | R§1 |
| inscritos por mil views, modelo mensal abr/25 a ago/26 | **14,7** | **1,04** | H5 |
| Shorts publicados a partir de 31/03/2025: por mil views / por mil intencionais | — | 0,67 / 1,48 | R§0c |
| % média assistida | 41% | 82% | R§1 |
| origem principal em 2026 | Navegação (50% a 65%, 87% em set) | Pesquisa (50% a 92%) | R§6c |

- **Conversão:** uma view de longo converte cerca de 14 vezes mais que uma de Short.
- **Volume e custo:** os Shorts dão volume barato. Eles também são achados por busca (em 2026, de 74% a 92% das views de Shorts vieram da Pesquisa).
- **Temas de Shorts que convertem melhor:** produto/comparativo e plano de renda, com cerca de 3 inscritos por mil views, contra 1,2 dos "outros" (R§2b).

## 6. Retenção aos 30 s: os 10 top e os 10 fracos (medida)

**Critério:** longos publicados nos últimos 365 dias, com 30 dias ou mais de vida e pelo menos 500 views intencionais; ordem por inscritos ganhos (empate: views intencionais). A mesma lista está em `analise/lista_retencao_30s.csv`. A retenção aos 30 s (última coluna) foi medida pela Analytics API (`audienceWatchRatio` interpolado em 30 s) e está em `dados/studio/retencao_30s.csv`. Medianas: 71,3% no top e 73,7% nos fracos (H4).

| grupo | vídeo | título | inscritos | views intenc. | insc./mil | 30 s |
|---|---|---|---|---|---|---|
| top | [`Fb0l4KEq27o`](https://studio.youtube.com/video/Fb0l4KEq27o/analytics/tab-overview/period-default) | 6 ETFs que MAIS PAGARAM DIVIDENDOS MENSAIS em 2025… | 637 | 32.294 | 19,7 | 64,1% |
| top | [`dHYQtxnMSrw`](https://studio.youtube.com/video/dHYQtxnMSrw/analytics/tab-overview/period-default) | ÚLTIMA CHANCE de GANHAR MUITO DINHEIRO na RENDA FIXA (NTN-B IPCA+7%) | 421 | 31.427 | 13,4 | 72,3% |
| top | [`IcN3m7whpl8`](https://studio.youtube.com/video/IcN3m7whpl8/analytics/tab-overview/period-default) | Esse Gráfico Acertou as CRISES 1929, 2008 e 2020… | 357 | 28.821 | 12,4 | 69,8% |
| top | [`tpobf1e1OtM`](https://studio.youtube.com/video/tpobf1e1OtM/analytics/tab-overview/period-default) | A Crise Já Está Acontecendo (e Só os Espertos Estão Vendo) | 345 | 33.147 | 10,4 | 71,5% |
| top | [`TY8oLvUt2Qg`](https://studio.youtube.com/video/TY8oLvUt2Qg/analytics/tab-overview/period-default) | RECEBA DIVIDENDOS TODOS os MESES de AÇÕES SEGURAS… | 324 | 17.994 | 18,0 | 63,4% |
| top | [`lt2LWbwu3mc`](https://studio.youtube.com/video/lt2LWbwu3mc/analytics/tab-overview/period-default) | O COBRE É O NOVO PETRÓLEO? Descubra Antes que Dispare… | 255 | 15.288 | 16,7 | 67,5% |
| top | [`KMIsVEOcaLM`](https://studio.youtube.com/video/KMIsVEOcaLM/analytics/tab-overview/period-default) | CUIDADO com Tesouro Direto IPCA+ 8,32% (veja antes do Copom) | 246 | 19.302 | 12,7 | 71,1% |
| top | [`JDtxzQthFlk`](https://studio.youtube.com/video/JDtxzQthFlk/analytics/tab-overview/period-default) | MORTE DO BITCOIN? O ALERTA QUE O MERCADO NÃO QUER OUVIR | 224 | 32.339 | 6,9 | 74,1% |
| top | [`tb0nwpl9mFw`](https://studio.youtube.com/video/tb0nwpl9mFw/analytics/tab-overview/period-default) | NÃO INVISTA no TESOURO DIRETO AGORA SEM SABER DISSO (CUIDADO) | 142 | 17.840 | 8,0 | 76,0% |
| top | [`IB1mBcF00jc`](https://studio.youtube.com/video/IB1mBcF00jc/analytics/tab-overview/period-default) | ETF JEPI39 PAGA DIVIDENDOS MENSAIS, mas vale a pena? | 131 | 20.232 | 6,5 | 75,5% |
| fraco | [`J_UAjVSbg-c`](https://studio.youtube.com/video/J_UAjVSbg-c/analytics/tab-overview/period-default) | PRUDENTIAL VENDIDA: se você tem SEGURO de VIDA ou VGBL… | 9 | 2.218 | 4,1 | 75,4% |
| fraco | [`R9DfUgYxLl8`](https://studio.youtube.com/video/R9DfUgYxLl8/analytics/tab-overview/period-default) | Concentrar ou Diversificar? A estratégia para bater o S&P500 | 8 | 2.036 | 3,9 | 78,2% |
| fraco | [`yBoRbHQlzCE`](https://studio.youtube.com/video/yBoRbHQlzCE/analytics/tab-overview/period-default) | Quem INVESTIR pode PERDER DINHEIRO (e nem sabe) [AXIA7, CYRE4…] | 7 | 2.205 | 3,2 | 73,9% |
| fraco | [`Z27KBNJcPDA`](https://studio.youtube.com/video/Z27KBNJcPDA/analytics/tab-overview/period-default) | RANI3 PAGA 11% ao ano — mas o LUCRO caiu 70% (Armadilha?) | 7 | 869 | 8,1 | 73,1% |
| fraco | [`lFPZmp8kLuo`](https://studio.youtube.com/video/lFPZmp8kLuo/analytics/tab-overview/period-default) | SINAL FORTE da BOLHA da INTELIGÊNCIA ARTIFICIAL | 5 | 2.297 | 2,2 | 74,4% |
| fraco | [`5i9cNa6uEc0`](https://studio.youtube.com/video/5i9cNa6uEc0/analytics/tab-overview/period-default) | NOVA LEI DA HERANÇA: SUA FAMÍLIA VAI PAGAR MAIS? | 5 | 892 | 5,6 | 72,0% |
| fraco | [`2TCAvZrl5nA`](https://studio.youtube.com/video/2TCAvZrl5nA/analytics/tab-overview/period-default) | ETF de GUERRA. É Horrível, Mas Isso Pode Multiplicar Seu Patrimônio… | 4 | 3.249 | 1,2 | 72,8% |
| fraco | [`GFHFMCaPn60`](https://studio.youtube.com/video/GFHFMCaPn60/analytics/tab-overview/period-default) | Michael Burry fez de novo — e dessa vez é a Nvidia | 4 | 990 | 4,0 | 73,5% |
| fraco | [`nRHvGe4-bTU`](https://studio.youtube.com/video/nRHvGe4-bTU/analytics/tab-overview/period-default) | GREVE DOS CAMINHONEIROS PREPARE sua CARTEIRA | 2 | 2.385 | 0,8 | 76,0% |
| fraco | [`uLVNra6EWc4`](https://studio.youtube.com/video/uLVNra6EWc4/analytics/tab-overview/period-default) | Alerta nos bancões: Quem sobrevive e quem perde dinheiro em 2026? | 2 | 994 | 2,0 | 65,7% |

## 7. O que o público pergunta (R§8)

A amostra tem 12.318 comentários (9.482 do público) dos 30 vídeos com mais views no contador. A maioria desses vídeos é antiga (bancos digitais, 2018 a 2022), e 23% dos comentários são do Short "1 centavo". A amostra retrata o público do catálogo antigo, não o dos vídeos de 2026.

- **Perguntas:** 1.777 (29,5% dos comentários de topo do público). O canal respondeu **56,9%**, então 766 ficaram sem resposta.

| tema dos comentários | % | exemplos curtos (sem autor) |
|---|---|---|
| Bancos digitais, contas e cartões | 25,7% | "Se eu tenho uma conta no next e faço uma transferência para bancos como Itaú, Santander… o next cobra?" |
| Crítica, dúvida sobre o conteúdo ou ironia | 7,2% | "É o mesmo discurso daqueles que falam: é só vender R$ 2800 por dia…" |
| Começar com pouco / centavos | 3,6% | "Se 1 centavo vira 10 milhões, R$ 1 vira 1 bilhão?" |
| Ações e tickers | 2,0% | "O que aconteceu com VVAR3?" · "Qual corretora o Luiz Barsi usa?" |
| Imposto de renda | 1,5% | "Faz um vídeo explicando como declarar o imposto de renda do zero!" |
| ETFs e BDRs | 1,4% | "Quais são os impostos cobrados para quem investe em ETFs?" |
| FIIs | 1,4% | "Vou ganhar R$ 300 mil de herança e quero pôr tudo em FII. Quais os mais seguros?" |
| Dividendos e renda passiva | 1,3% | (renda mensal, quanto rende) |
| Menor de idade e filhos | 1,3% | "Como faço para comprar ações no nome do meu filho de 11 anos?" |
| Tesouro e renda fixa | 1,1% | "Tenho 80 mil; é bom colocar em LCI por 12 meses?" |
| Cripto | 1,0% | Inclui robôs de golpe ("Sou novo no comércio. Como posso investir em criptomoedas…"). |
| outros | 47,8% | (sem palavra-chave de tema) |

**Pedidos explícitos de vídeo:**
- declarar IR do zero;
- conta e investimento para menor de idade;
- "a BDR do mês";
- como dobrar com pouco dinheiro.

---

## 8. As 10 ações priorizadas

### A meta, com honestidade

200 mil inscritos até 31/12/2026 exigem **11.692 líquidos por mês (385 por dia)**.

| ritmo | líquidos por mês |
|---|---|
| último mês (set/26) | 221 |
| média dos últimos 6 meses | 424 |
| melhor mês dos últimos 18 (mai/25, com Shorts virais) | 2.097 |

No ritmo atual, o canal fecha 2026 com cerca de **166 mil** e chegaria a 200 mil por volta de 2033. Nenhuma combinação de ações realista fecha 35 mil em 3 meses.

**Proposta:** manter os 200 mil como meta de 2027 e fixar como meta de 2026 **voltar a 1.500 líquidos por mês até dezembro**. Esse foi o nível de jan e fev/26 (1.443 e 1.824). Nesse ritmo, 200 mil chegam em cerca de 23 meses; a 2.500 por mês, em 14.

### Ações, da maior alavanca para a menor

| # | ação | número que a sustenta | efeito esperado |
|---|---|---|---|
| 1 | **Medir por inscritos e views intencionais, não pelo contador.** Painel semanal com intencionais, minutos e inscritos por vídeo; parar de usar "views" para decidir pauta ou thumb. | Longos novos: 3,4 views por intencional desde 27/08 (antes, 1,1). Set/26 teve 4,6x as views de longos de agosto e 503 inscritos (o modelo previa 2.881). | Evita decisões erradas a partir de um número inflado. Pré-requisito das demais. |
| 2 | **Revisar a meta:** 1.500 líquidos por mês em dez/26 e 200 mil em 2027. | Necessário 11.692 por mês, contra 424 de média (28x) e 2.097 de recorde (5,6x). | Meta que orienta, em vez de uma que já está perdida. |
| 3 | **Uma série fixa de renda mensal** (ETFs e ações que pagam todo mês, carteira de dividendos mensais), com um vídeo por semana. | Insc./mil intencionais 14,5 contra 8,2 do resto (n = 6). Dos 5 maiores do ano, 2 são dessa linha (637 e 324 inscritos). Plano de renda: 11,7/mil nos últimos 12 meses. | +150 a 250 inscritos por mês, se mantiver a mediana de 112 por vídeo. Amostra pequena: validar em 6 semanas. |
| 4 | **Tesouro/IPCA+ no momento certo:** um vídeo a cada Copom ou mudança forte de taxa. | Tesouro/IPCA+: mediana de 142 inscritos por vídeo (n = 5); 11,0/mil contra 8,8. Dois dos top 10 (421 e 246) e "NÃO INVISTA no TESOURO…" (142). | +100 a 150 por mês. |
| 5 | **Continuações dos 10 vídeos top** ("6 ETFs… 2026, atualizado", "o gráfico das crises, 6 meses depois", "cobre"), com link no fim e card para o original. | Os 10 melhores do ano fizeram 58% dos 5.327 inscritos dos 80 longos novos. Converteram de 6,5 a 19,7 por mil. | Aproveita a demanda já provada; melhora Sugeridos (de 22,6% para 4,1% nos longos). |
| 6 | **Voltar a 8 Shorts por mês,** com temas de produto/comparativo e renda, e cada Short apontando para um longo. | Inscritos ganhos: 1.170 por mês (fev a jul) contra 540 (ago e set). Shorts: de 320 mil views por mês para 130 mil. A 1,04 inscrito por mil, isso dá cerca de 200 inscritos por mês perdidos. Shorts de produto/renda: ~3/mil contra 1,2 dos demais. | Recupera cerca de 200 por mês (um terço da queda). |
| 7 | **Auditar os 285 longos fora do ar:** listar os 30 maiores, ver por que saíram e republicar (ou regravar atualizados) os temas perenes de busca. | 4,15 mi de views e 52.351 inscritos (32,7% dos inscritos vitalícios de longos). Os maiores tratam de Next/Nubank/Santander, que ainda são 25,7% dos comentários do catálogo. | Tráfego de busca perene. Precisa da decisão do Denis (podem ter saído por motivo legal ou por estarem desatualizados). |
| 8 | **Título pensado para a busca em todo longo** (produto, ticker, "vale a pena", ano). Testar título e thumb no "Testar e comparar" do Studio, com menos "?" e menos caixa alta. | Pesquisa: CTR de 12,3% nos longos, contra 7,2% da Navegação (vitalício). Fracos têm mais "?" (53% contra 37%) e caixa alta (47% contra 32%), com n = 19 de cada lado. | Mais CTR e um tráfego que não depende do feed. |
| 9 | **Responder as perguntas e tirar pauta delas:** responder os 43% sem resposta nos vídeos novos e gravar as pautas pedidas. | 1.777 perguntas, das quais 766 sem resposta. Pedidos diretos: IR do zero, investimento para menor de idade, BDR do mês. | Engajamento dos inscritos (que já são 30% das views dos longos novos, contra 17% dos antigos; só 23 longos novos têm esse dado) e pauta com demanda comprovada. |
| 10 | **Investir em distribuição (thumb, título e CTR), não em refazer ganchos.** Exportar do Studio os longos dos últimos 12 meses com Impressões e CTR, para comparar a thumb de top e fracos, e usar o "Testar e comparar" em todo longo novo. | Abertura medida: retenção aos 30 s de 71,3% no top e 73,7% nos fracos (n = 10 de cada lado, Analytics API). % média assistida: 36,9% contra 41,0%. Os fracos têm 7x menos views intencionais com retenção igual ou maior. Eles não têm CTR na exportação atual. | Ataca a diferença real (alcance). Sem os dados de CTR dos fracos, a parte da thumb ainda é hipótese. |

**Duração:** manter os longos entre 15 e 20 min. A mediana é de 31,5 inscritos por vídeo (n = 32), contra 20 nos de 10 a 15 min (n = 34). É um ajuste de baixo custo, mas a diferença é pequena e pode ter outras causas.

## Limites dos dados

- **Impressões e CTR:** a API recusou (400) e as colunas vieram vazias. O CTR e as impressões vêm do Studio, que exporta só os 500 longos com mais views. Por isso os vídeos fracos e recentes não têm CTR.
- **Shorts × longos por mês (`creatorContentType`):** a API recusou. A fatia de inscritos por formato (H5) é estimativa de modelo.
- **Tráfego e inscritos/não inscritos por vídeo:** cobrem só os 300 vídeos com mais views (`--max-videos-detalhe 300`).
- **Contador de inscritos:** é arredondado pelo YouTube (165.000).
- **Inscritos ganhos por vídeo:** o Analytics atribui ao vídeo onde a inscrição aconteceu. Perdas por vídeo quase não são atribuídas: 3.959 de todos os vídeos, contra 280 a 530 por mês no canal.
- **Retenção aos 30 s:** medida em 20 vídeos (10 + 10) pela Analytics API, interpolando a curva vitalícia. É suficiente para descartar uma vantagem grande da abertura, não diferenças pequenas.
- **Tema:** classificado por regras sobre o título. Os grupos dos últimos 12 meses têm de 10 a 25 vídeos. Confira e corrija em `dados/temas_manual.csv`.
- **Comentários:** vêm dos 30 vídeos com mais views do catálogo, majoritariamente antigos.
