# Série Renda Mensal: os 6 próximos episódios

Pauta aprovada pelo Denis em 03/10/2026. Montada em 03/10/2026 com os dados de `auditoria-canal/dados/` (exportação de 02/10/2026),
`pautas-canal/TERMOS.md` e `pautas-canal/TEMAS.md`. A checagem automática dos títulos está em `checar_serie.py`, nesta
pasta.

## Por que uma série, e por que estes 6

- **O que converte:** a linha de dividendos mensais teve 14,5 inscritos por mil views intencionais nos últimos 12 meses,
  contra 8,2 do resto (n = 6; `RELATORIO.md`, seção 2). O tema "plano de renda" teve 11,7 por mil (n = 10; H2). Dos 10
  longos que mais trouxeram inscritos no ano, 3 são de renda mensal.
- **O que se espera de cada episódio:** 91 inscritos por longo de renda mensal, faixa de 69 a 267 (n = 7; `TEMAS.md`).
  É mediana de amostra pequena: valide depois de 6 semanas.
- **Regra da série:** cada episódio ensina um critério ou faz uma conta com exemplo. Nenhum indica ativo para comprar,
  nenhum cita corretora. Quando aparece um produto, ele aparece como categoria (ETF, LCI, FII, Tesouro IPCA+).
- **Fora:** dívida, cartão e finança pessoal básica (regra de nicho do Denis). Reserva de emergência fica fora da série.

### O que já foi feito e o que não pode se repetir

Longos de renda dos últimos 6 meses (`videos.csv`, de 04/04 a 01/10/2026) e pautas de renda do calendário v2:

| já feito ou já pautado | quando | o episódio que chega perto | o ângulo novo |
|---|---|---|---|
| "ETF DIVIDENDOS MENSAIS são um GOLPE?" (`c9Obo6F5_NU`) | 08/04/2026 | Ep. 1 | lá foi a dúvida; aqui é a conta do retorno total (renda + variação da cota), com o passo a passo para refazer com o histórico da B3 |
| v2: "ETFs que pagam dividendos mensais: o que mudou em 2026" | 06/10 (v2) | Ep. 1 | a v2 atualiza cada ETF da lista; o Ep. 1 ensina o método, sem lista |
| "RANI3 PAGA 11% ao ano — mas o LUCRO caiu 70%" (`Z27KBNJcPDA`) | 04/08/2026 | Ep. 2 | lá foi uma empresa; aqui são 4 contas que servem para qualquer ação ou FII |
| "Método Barsi de Dividendos" (`IunRW7GKjck`) | 30/06/2026 | Ep. 2 | o Barsi é método de escolha de setor; o Ep. 2 é a checagem do número do dividendo |
| "DIVIDENDOS: PLANO para RECEBER 10 MIL" (`Rgfh5HuNdJo`) e v2 03/11 "R$ 1.000: quanto precisa investir" | 11/09/2026 e 03/11 (v2) | Ep. 3 e Ep. 5 | aqueles calculam o capital necessário; o Ep. 3 decide o que fazer com a renda (gastar ou reinvestir) e o Ep. 5 mede quanto ela encolhe com a inflação |
| v2 22/10 "LCI e LCA ou CDB: a conta de 2026" | 22/10 (v2) | Ep. 4 | a v2 compara um título com outro; o Ep. 4 monta renda mensal com vencimentos escalonados |
| "Fim do IPCA+ 8%?" (`qtbczPm6RHY`), "PREFIXADO vs IPCA+" (`GQbZFJwkIHc`), "IPCA+ 8,32%" (`KMIsVEOcaLM`) | 16/06 a 08/09/2026 | Ep. 5 | aqueles falam de taxa e marcação; o Ep. 5 fala do poder de compra da renda |
| v2 13/10 "calendário de dividendos com ações" e v2 10/11 "renda com Tesouro: juros semestrais" | 13/10 e 10/11 (v2) | Ep. 6 | cada um trata uma classe; o Ep. 6 junta as duas com FII numa grade de 12 meses e mostra os meses vazios |

### A ordem

1. ETF: a renda saiu da cota? (critério)
2. Dividendos altos demais (critério)
3. Gastar ou reinvestir (decisão)
4. Escada de LCI e LCA (construção, renda fixa)
5. Renda e inflação (proteção)
6. A grade de 12 meses (fechamento: junta tudo)

Datas APROVADAS pelo Denis em 03/10/2026: quartas às 19 h, de 14/10 a 25/11, pulando a semana do Copom (calendário
oficial: `../CALENDARIO.md`). Os títulos abaixo são provisórios: ainda passam pelo empacotador e pelo teste A/B.

**Fontes que valem para todos os episódios** (regras de 2026 já conferidas no projeto; use só estas):

| regra | fonte primária |
|---|---|
| JCP com IRRF de 17,5% | LC 224/2025: https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp224.htm |
| FII isento só com 100 cotistas ou mais; ganho de capital na venda de cota a 20% | Lei 14.754/2023: https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14754.htm |
| dividendos acima de R$ 50 mil por mês da mesma empresa com retenção de 10% | Lei 15.270/2025: https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15270.htm |
| LCI e LCA com prazo mínimo de 6 meses | Res. CMN 5.215: https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20CMN&numero=5215 |
| FGC: R$ 250 mil por CPF e instituição, teto de R$ 1 milhão a cada 4 anos | https://www.fgc.org.br/garantia-fgc/sobre-a-garantia-fgc |
| tabela regressiva do IR em renda fixa (22,5% até 180 dias; 20% até 360; 17,5% até 720; 15% acima) | Lei 11.033/2004: https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l11033.htm |

---

## Ep. 1 · quarta 14/10/2026

- **Título de busca:** `ETF que paga dividendos mensais: a renda saiu da cota?` (54 caracteres)
- **Alternativas:** `Dividendos mensais de ETF: renda ou devolução da cota?` · `ETF de dividendos mensais: a conta do retorno total`
- **Termo de busca:** "etfs que pagam dividendos mensais": 208 views da Pesquisa nos últimos 6 meses (04/04 a
  01/10/2026, `termos_busca_recentes.csv`) e 1.877 no vitalício (`termos_busca_por_video.csv`, vídeo `Y4WHQiKcv1g`).
  É o 11º termo de investimento do período (`TERMOS.md`). A família "etf que pagam / etf dividendos mensais" soma 331
  views no período e 4.558 no vitalício.
- **Promessa:** você sai sabendo fazer a conta que separa renda de verdade de dinheiro que só saiu da própria cota.
- **Roteiro:**
  - **Gancho (até 30 s):** "Um ETF que paga 1% ao mês e cuja cota cai 1% ao mês te pagou quanto? Quase nada. Hoje eu
    te mostro a conta que o extrato não mostra."
  - **Conta central:** retorno total = (cota no fim − cota no começo + rendimentos recebidos) ÷ cota no começo.
    - Exemplo com números redondos (hipotético, dizer na tela): cota de R$ 100, R$ 1,00 por mês por 12 meses = R$ 12;
      cota termina em R$ 92. Retorno total: (92 − 100 + 12) ÷ 100 = 4% em 12 meses.
    - Contra a inflação: IPCA de 12 meses até ago/2026 de 4,22% (BCB, SGS 13522). Retorno real do exemplo: cerca de
      −0,2%. A "renda" de 12% foi, na prática, a cota voltando para o bolso.
    - Como refazer com um ETF de verdade: histórico de rendimentos na B3 (eventos corporativos do fundo) e cotação de
      fechamento nas séries históricas da B3. Mostrar a planilha com 4 colunas: data, cota, rendimento, acumulado.
    - Por que acontece: ETF com venda de opções cobertas troca parte da alta por renda (ligar no longo de 20/10 da v2);
      distribuição acima do que a carteira gera sai do patrimônio.
  - **Objeções:**
    - "Mas a cota volta." Talvez. A conta mostra o resultado de um período; refaça em 2 ou 3 janelas diferentes.
    - "Eu só quero a renda." A mesma porcentagem sobre uma cota menor é uma renda menor no ano seguinte.
    - "E o imposto?" Depende do tipo de ETF e do regulamento. Mostrar onde ler (lâmina e regulamento), sem dar alíquota
      que não esteja no regulamento.
  - **Fechamento:** checklist de 3 perguntas (quanto pagou, quanto a cota andou, quanto ficou acima do IPCA) e card
    para o vídeo dos 6 ETFs de jan/26.
- **Números para conferir antes de gravar:**
  - IPCA de 12 meses, último divulgado: SGS 13522, https://api.bcb.gov.br/dados/serie/bcdata.sgs.13522/dados/ultimos/1?formato=json
    (4,22% em ago/2026, lido em 02/10/2026 pelo `gate_qualidade.py`; o de setembro sai no começo de outubro; conferir a data no calendário do IBGE).
  - Rendimentos e cotas do ETF usado na demonstração: B3, séries históricas
    (https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/)
    e o informe de distribuição do administrador. Se mostrar um ETF real, é demonstração do método, sem dizer se compra.
- **Thumbnail:** "RENDA OU DEVOLUÇÃO?" com uma seta da cota descendo e moedas saindo dela.
- **Short derivado:** "Recebeu 1% ao mês e a cota caiu 1% ao mês: quanto você ganhou?" (40 s, a conta do exemplo e o
  link para o Ep. 1).
- **Continuação:** puxa `Fb0l4KEq27o` ("6 ETFs que MAIS PAGARAM DIVIDENDOS MENSAIS em 2025…", 637 inscritos, 19,7 por
  mil, o maior do ano) e `c9Obo6F5_NU` (o "GOLPE?" de abril). Card no minuto da conta e tela final para `Fb0l4KEq27o`.

## Ep. 2 · quarta 21/10/2026

- **Título de busca:** `Dividendos altos demais: 4 contas antes de confiar na renda` (59 caracteres)
- **Alternativas:** `Dividend yield alto: 4 contas antes de confiar na renda` · `Dividendo alto ou armadilha? 4 contas que separam os dois`
- **Termo de busca:** "dividendos": 109 views da Pesquisa nos últimos 6 meses (`termos_busca_recentes.csv`; 19º do top 20 de
  `TERMOS.md`). Apoio: "acoes que pagam dividendos todo mes", 8 views no período (baixo; o tema vive mais de Navegação,
  como toda a linha de renda mensal: 58% das views vêm da página inicial nos 3 vídeos com dado, `TEMAS.md`).
- **Promessa:** com 4 contas simples, você descobre se um dividendo alto vai se repetir ou se foi uma vez só.
- **Roteiro:**
  - **Gancho:** "O dividend yield de uma ação pode dobrar sem a empresa pagar um real a mais. Basta o preço cair pela
    metade."
  - **Conta central (exemplos hipotéticos, números redondos):**
    1. **Efeito preço:** dividendo de R$ 1 por ação; preço de R$ 20 → yield de 5%. Preço cai para R$ 10 → yield de 10%.
       A renda não mudou; o risco, talvez.
    2. **Payout:** dividendos ÷ lucro. Lucro de R$ 100 milhões e dividendos de R$ 150 milhões = 150%. Acima de 100%, a
       empresa paga mais do que ganhou: sai do caixa ou de dívida.
    3. **Lucro que não se repete:** venda de um ativo ou crédito tributário engorda o lucro de um ano. Onde achar: notas
       explicativas do resultado (CVM).
    4. **Histórico de 5 anos:** o dividendo por ação de cada ano. Uma linha que pula de 1 para 4 e volta para 1 não é
       renda mensal.
    - No FII, o mesmo raciocínio: rendimento que veio de venda de imóvel ou de reserva acaba.
    - Imposto que entra na conta da renda líquida: JCP chega com 17,5% retido (LC 224/2025); dividendos acima de
      R$ 50 mil por mês da mesma empresa têm retenção de 10% (Lei 15.270/2025).
  - **Objeções:**
    - "Então dividendo alto é ruim?" Não. É um número que pede as outras 3 contas.
    - "Onde eu acho o payout?" No relatório de resultados da empresa (RI) e no formulário de referência da CVM.
    - "E a ação que caiu muito, não está barata?" Pode estar. O episódio não decide isso; ele mostra se a renda se
      sustenta.
  - **Fechamento:** a ficha de 4 linhas para preencher antes de confiar no yield; card para o vídeo de dividendos todos os
    meses (out/25).
- **Números para conferir:** nenhum dado de mercado no roteiro principal (os exemplos são hipotéticos e precisam aparecer
  assim na tela). Se usar uma empresa real como demonstração: lucro e proventos no RAD da CVM (https://www.rad.cvm.gov.br/)
  e no RI da empresa, com a data do documento; regras de JCP e de dividendos nas leis acima.
- **Thumbnail:** "YIELD 10%… DE QUÊ?" com o preço caindo e a seta do yield subindo.
- **Short derivado:** "O dividend yield dobrou e a empresa não pagou nada a mais" (a conta do efeito preço em 35 s).
- **Continuação:** puxa `TY8oLvUt2Qg` ("RECEBA DIVIDENDOS TODOS os MESES de AÇÕES SEGURAS…", 324 inscritos, 18,0 por mil,
  o 5º do ano). Card no item 4 (histórico) e tela final.

## Ep. 3 · quarta 28/10/2026

- **Título de busca:** `Gastar ou reinvestir os dividendos: a conta de 10 anos` (54 caracteres)
- **Alternativas:** `Reinvestir dividendos: quanto muda a renda em 10 anos` · `Renda mensal: gastar agora ou reinvestir? A conta`
- **Termo de busca:** a família "dividendos mensais" (331 views no período; 4.558 no vitalício, `TERMOS.md`) e a de
  "como juntar 1 milhão de reais" (316 no período; 1.803 só no termo exato no vitalício, vídeo `tbKsF2qyakU`). Nos
  comentários, o grupo "começar a investir e juros compostos" tem 101 perguntas, a 3ª maior fila
  (`PERGUNTAS-SEM-RESPOSTA.md`).
- **Promessa:** você vê, em reais, quanto custa gastar a renda hoje em vez de reinvestir, e como achar o meio-termo.
- **Roteiro:**
  - **Gancho:** "Com o mesmo dinheiro, uma pessoa recebe R$ 600 por mês e a outra R$ 1.230. A diferença é uma decisão
    que ela tomou 10 anos antes."
  - **Conta central (taxa de exemplo, dizer que é exemplo):** R$ 100 mil rendendo 0,6% ao mês (cerca de 7,4% ao ano),
    sem imposto e sem inflação para simplificar.
    - Gastando tudo: R$ 600 por mês, R$ 72 mil em 10 anos, e o capital continua em R$ 100 mil.
    - Reinvestindo tudo: 100.000 × 1,006¹²⁰ ≈ R$ 205 mil em 10 anos. A renda do mês seguinte passa a ser ≈ R$ 1.230.
    - Meio-termo: reinvestir só a parte da inflação e gastar o resto (ligar no Ep. 5).
    - Mostrar a planilha: uma linha por ano, as duas colunas lado a lado.
  - **Objeções:**
    - "Eu preciso da renda agora." Então o meio-termo; a planilha mostra o custo de cada escolha.
    - "A taxa não é fixa." Certo: é exemplo. O que importa é a diferença entre as colunas, que aparece com qualquer
      taxa positiva.
    - "E o imposto?" Cada produto tem a sua regra; o FII é isento só com 100 cotistas ou mais (Lei 14.754/2023), o JCP
      chega com 17,5% retido. O imposto reduz as duas colunas.
  - **Fechamento:** a pergunta para o comentário: "em que fase você está, juntar ou viver da renda?"; card para o vídeo
    do JEPI39.
- **Números para conferir:** só a aritmética (refazer na planilha antes de gravar: 1,006¹²⁰ = 2,05). Se trocar a taxa de
  exemplo por uma taxa real de mercado, citar a fonte e a data (Tesouro Transparente, CSV de preços e taxas).
- **Thumbnail:** "R$ 600 × R$ 1.230" com o mesmo cofrinho dos dois lados.
- **Short derivado:** "R$ 100 mil, 10 anos: gastar a renda ou reinvestir?" (as duas colunas em 30 s).
- **Continuação:** puxa `IB1mBcF00jc` ("ETF JEPI39 PAGA DIVIDENDOS MENSAIS…", 131 inscritos, 10º do ano). Card no
  meio-termo e tela final.

## Ep. 4 · quarta 11/11/2026

- **Título de busca:** `LCI e LCA para renda mensal: a escada de vencimentos` (52 caracteres)
- **Alternativas:** `Escada de LCI e LCA: renda todo mês com prazo mínimo` · `Renda mensal com LCI e LCA: como escalonar os vencimentos`
- **Termo de busca:** "lci e lca": 473 views da Pesquisa nos últimos 6 meses (4º termo de investimento do período) e 3.544 no
  vitalício, no Short `Q1WMbZZn2Ik`. A família "LCI, LCA e CDB" soma 1.360 no período e 15.565 no vitalício
  (`TERMOS.md`).
- **Promessa:** você aprende a montar uma escada de LCI e LCA que vence um degrau por mês e entende por que ela demora
  a começar.
- **Roteiro:**
  - **Gancho:** "LCI e LCA não pagam juros todo mês. Mas dá para fazer vencer uma todo mês."
  - **Conta central:**
    - A regra que manda no desenho: prazo mínimo de 6 meses (Res. CMN 5.215). A escada não começa a pagar no mês 1.
    - Desenho simples: R$ 120 mil divididos em 12 aplicações de R$ 10 mil, de 12 meses cada, uma por mês. Do 13º mês em
      diante, vence uma por mês; gasta-se o rendimento e o principal volta para um novo degrau de 12 meses.
    - Exemplo de taxa (dizer que é exemplo): LCI a 90% do CDI. Em out/2026, com CDI de 13,65% ao ano (Selic de 13,75% desde
      17/09/2026 menos 0,10 p.p.; conferir no dia), dá 12,29% ao ano: cerca de R$ 1.229 de rendimento em cada degrau
      de R$ 10 mil que vence.
    - Comparação com CDB (Lei 11.033/2004): em 12 meses, o CDB paga 17,5% de IR. LCI de 90% do CDI = CDB de cerca de
      109% do CDI (90 ÷ 0,825).
    - FGC: R$ 250 mil por CPF e instituição, com teto de R$ 1 milhão a cada 4 anos. Escada grande pede emissores
      diferentes.
  - **Objeções:**
    - "Não posso resgatar antes?" Em geral, não: a carência é parte do produto. Por isso a escada não serve como reserva.
    - "Por que não um CDB que paga juros todo mês?" Também é uma escada, de outro jeito. Comparar pela taxa líquida.
    - "E o Tesouro?" Fica para o Ep. 6, a grade de 12 meses.
  - **Fechamento:** a tabela de 12 linhas (mês, valor, vencimento) para copiar; card para o Short de LCI ou CDB.
- **Números para conferir:**
  - CDI do dia: SGS 4389 (CDI anualizado, base 252), https://api.bcb.gov.br/dados/serie/bcdata.sgs.4389/dados/ultimos/1?formato=json.
  - Meta Selic: SGS 432 (13,75% desde 17/09/2026; comunicado da 281ª reunião, https://www.bcb.gov.br/api/servico/sitebcb/copom/comunicados?quantidade=1,
    lido em 03/10/2026). Se o Copom de 03-04/11 mudar a Selic, refazer o exemplo.
  - Prazo mínimo de LCI e LCA (Res. CMN 5.215), tabela do IR (Lei 11.033/2004) e FGC (fgc.org.br), nos links acima.
- **Thumbnail:** "UMA VENCE POR MÊS" com a escada de 12 degraus.
- **Short derivado:** "LCI e LCA não pagam todo mês. Mas dá para fazer vencer uma por mês" (o desenho dos 12 degraus).
- **Continuação:** o vídeo que recebe a busca "lci e lca" é o Short `Q1WMbZZn2Ik` (99 inscritos). Entre os longos top,
  puxa `dHYQtxnMSrw` ("ÚLTIMA CHANCE… NTN-B IPCA+7%", 421 inscritos, 2º do ano). Card para os dois.

## Ep. 5 · quarta 18/11/2026

- **Título de busca:** `Renda mensal e inflação: quanto reinvestir para não encolher` (60 caracteres)
- **Alternativas:** `Sua renda mensal encolhe: a conta da inflação em 10 anos` · `Renda que não encolhe: quanto guardar para a inflação`
- **Termo de busca:** a família "Tesouro Direto e IPCA+": 1.009 views no período, com "ipca + 8" (213), "tesouro ipca" (69) e
  "tesouro ipca+ 2032" (63), quase tudo em `KMIsVEOcaLM` (`TERMOS.md`).
- **Promessa:** você calcula quanto da sua renda precisa voltar para o investimento para ela valer o mesmo daqui a 10 anos.
- **Roteiro:**
  - **Gancho:** "R$ 1.000 por mês hoje, com a inflação de agora, compram R$ 661 daqui a 10 anos."
  - **Conta central:**
    - Inflação de referência: IPCA de 12 meses até ago/2026 de 4,22% (SGS 13522). 1.000 ÷ 1,0422¹⁰ ≈ R$ 661;
      em 20 anos, ≈ R$ 438. Mantida a inflação constante (hipótese).
    - Regra de bolso: para a renda não encolher, reinvista a parte da renda igual à inflação. Se o investimento rende 10%
      ao ano e a inflação é 4,22%, reinvista 42% da renda (4,22 ÷ 10) e gaste 58%.
    - O caso do título atrelado à inflação: o Tesouro IPCA+ já corrige o principal pelo IPCA; a taxa contratada é a parte
      acima da inflação. Taxa de compra do IPCA+ 2035 na manhã de 01/10/2026: 7,56% (Tesouro Transparente).
    - Tabela: renda nominal, renda em reais de hoje, ano a ano.
  - **Objeções:**
    - "A inflação não vai ficar em 4,22%." Certo. A conta se refaz com qualquer número; o Focus de 25/09/2026 projeta 4,99%
      para 2026 (projeção, não certeza).
    - "FII e ação não sobem com a inflação?" Podem subir, sem garantia. A conta mostra quanto precisam subir.
    - "Então só IPCA+?" Não. O episódio mede; não escolhe produto.
  - **Fechamento:** a fórmula na tela (reinvestir = inflação ÷ rendimento) e o card para o vídeo da NTN-B de janeiro.
- **Números para conferir:**
  - IPCA de 12 meses: SGS 13522 (link no Ep. 1). Se sair o de setembro antes da gravação, refazer as contas.
  - Taxa do IPCA+ 2035: CSV do Tesouro Transparente,
    https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv
    (coluna "Taxa Compra Manha", vencimento 15/05/2035; 7,56% na data-base 01/10/2026, baixado em 03/10/2026).
  - Focus: https://www.bcb.gov.br/content/focus/focus/R20260925.pdf (IPCA 2026: 4,99%; lido em 03/10/2026). Usar o
    relatório mais recente na semana da gravação.
- **Thumbnail:** "R$ 1.000 → R$ 661" com uma nota encolhendo.
- **Short derivado:** "R$ 1.000 de renda hoje compram quanto em 10 anos?" (a conta e a regra de bolso).
- **Continuação:** puxa `dHYQtxnMSrw` ("ÚLTIMA CHANCE… NTN-B IPCA+7%", 421 inscritos) e `KMIsVEOcaLM` ("CUIDADO com Tesouro
  Direto IPCA+ 8,32%", 246). Card para o primeiro no trecho do IPCA+.

## Ep. 6 · quarta 25/11/2026

- **Título de busca:** `Renda todo mês com Tesouro e FII: a grade de 12 meses` (53 caracteres)
- **Alternativas:** `Tesouro, FII e ações: em que mês cai cada renda` · `Renda mensal de verdade: juntando Tesouro, FII e ações`
- **Termo de busca:** "tesouro direto": 456 views da Pesquisa no período (5º termo de investimento, `TERMOS.md`). Apoio:
  "fundos imobiliarios" (47 no período; 1.261 no vitalício) e "acoes que pagam dividendos todo mes" (8).
- **Promessa:** você monta uma grade de 12 meses e vê, antes de investir, quais meses ficam sem renda.
- **Roteiro:**
  - **Gancho:** "Quem diz que recebe todo mês quase sempre tem 2 ou 3 meses vazios no ano. Vamos achar os seus."
  - **Conta central (a grade):**
    - Tesouro IPCA+ com juros semestrais: os vencimentos de maio pagam em maio e novembro; os de agosto, em fevereiro
      e agosto. Tesouro Prefixado com juros semestrais: janeiro e julho. Só com Tesouro, 6 meses do ano têm pagamento.
    - FII: a lei manda distribuir lucro em base semestral (Lei 8.668/1993); na prática, a maioria distribui todo mês.
      Conferir no regulamento de cada fundo.
    - Ações: as datas mudam de empresa para empresa e de ano para ano (ligar no calendário do 13/10 da v2).
    - Exemplo: meta de R$ 1.000 por mês. A grade mostra que o Tesouro concentra a renda em 6 meses e o FII preenche os
      outros; ao final, a soma anual é o que importa, e a grade mostra quanto guardar nos meses cheios.
    - Imposto: cupom do Tesouro paga IR pela tabela regressiva a cada pagamento (Lei 11.033/2004; conferir a regra de
      prazo no site do Tesouro Direto); FII isento só com 100 cotistas ou mais (Lei 14.754/2023); JCP com 17,5%.
  - **Objeções:**
    - "Ficou complicado." Fica. A alternativa é receber em menos meses e separar a renda do mês cheio.
    - "E o Tesouro RendA+?" Paga mensal só depois da data de conversão. Conferir no Tesouro Direto e ligar no longo de
      10/11 da v2.
    - "E se o FII cortar o rendimento?" As 4 contas do Ep. 2.
  - **Fechamento:** recapitular a série em 6 linhas, a grade para baixar (descrição) e o card para o vídeo de dividendos
    todos os meses.
- **Números para conferir:**
  - Meses de pagamento de cupom de cada título: página de cada título no Tesouro Direto (https://www.tesourodireto.com.br/;
    bloqueado nesta rede, conferir no Mac). Os vencimentos à venda estão no CSV do Tesouro Transparente (data-base
    01/10/2026): IPCA+ com juros semestrais 2030, 2032, 2035, 2037, 2040, 2045, 2050, 2055 e 2060; Prefixado com juros
    semestrais 2027, 2029, 2031, 2033, 2035 e 2037.
  - Regra de distribuição do FII: Lei 8.668/1993, https://www.planalto.gov.br/ccivil_03/leis/l8668.htm.
- **Thumbnail:** um calendário de 12 quadrados, 3 vazios em vermelho: "E ESTES MESES?"
- **Short derivado:** "Recebe todo mês? Veja quais meses ficam vazios" (a grade em 45 s).
- **Continuação:** puxa `TY8oLvUt2Qg` (dividendos todos os meses, 324) e `KMIsVEOcaLM` (IPCA+ 8,32%, 246). Tela final
  com a playlist da série.

---

## Resumo para a planilha

| ep. | data | título | termo de busca | Pesquisa 6 meses | puxa | Short derivado |
|---|---|---|---|---|---|---|
| 1 | qua 14/10 | ETF que paga dividendos mensais: a renda saiu da cota? | etfs que pagam dividendos mensais | 208 | Fb0l4KEq27o (637) | 07/10 (pré-estreia) |
| 2 | qua 21/10 | Dividendos altos demais: 4 contas antes de confiar na renda | dividendos | 109 | TY8oLvUt2Qg (324) | 21/10 |
| 3 | qua 28/10 | Gastar ou reinvestir os dividendos: a conta de 10 anos | dividendos mensais / como juntar 1 milhão | 331 / 316 | IB1mBcF00jc (131) | 18/11 |
| 4 | qua 11/11 | LCI e LCA para renda mensal: a escada de vencimentos | lci e lca | 473 | dHYQtxnMSrw (421) | 16/11 |
| 5 | qua 18/11 | Renda mensal e inflação: quanto reinvestir para não encolher | tesouro ipca / ipca + 8 | 69 / 213 | dHYQtxnMSrw (421) | 23/11 |
| 6 | qua 25/11 | Renda todo mês com Tesouro e FII: a grade de 12 meses | tesouro direto | 456 | TY8oLvUt2Qg (324) | 30/11 |

As datas dos Shorts seguem a troca das pautas fora do nicho (`PROPOSTA-CALENDARIO-V3.md`).
