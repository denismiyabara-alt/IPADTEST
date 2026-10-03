---
tema: "ETF que paga dividendos mensais: a renda saiu da cota?" (título PROVISÓRIO; ainda passa pelo empacotador e pelo teste A/B)
serie: Série Renda Mensal, Ep. 1 de 6
formato: long (11-13 min; com os blocos A, de opções, e B, de taxa, absorvidos em 03/10)
data_briefing: 2026-10-03
data_publicacao: 2026-10-14 (quarta, 19h)
janela_validade: os preços são de 01/10/2026; se gravar depois de 09/10, refazer IPCA, CDI e cotas (seção 4)
dado_valor_em: 15 s (gancho A)
status: GO condicional. A conta central fecha só depois de conferir os rendimentos do DIVD11 e o IR da distribuição (A CONFERIR 1, 2 e 10); o bloco A fecha só com os rendimentos do SPYI11 (A CONFERIR 11)
frame: REVELAÇÃO / educativo (método). Nada de COMPARAÇÃO "qual é melhor", nada de "vale a pena"
tickers: DIVD11, DIVO11 (caso de estudo central); SPYI11 (caso de estudo do bloco A, opções); ETHY11, JEPI39 (exemplos de 1 frase). Nenhum é recomendado
concorrentes: 2026-10-14-etf-dividendos-mensais-concorrentes.md
puxa: Fb0l4KEq27o (637 inscritos); IB1mBcF00jc (JEPI39, card no bloco A); c9Obo6F5_NU
corte: Short de 25/11 "Taxa de administração do ETF: quanto tira em 10 anos" sai do bloco B (T17)
---

# BRIEFING: ETF que paga todo mês. A renda saiu da cota?

> Para o roteirista (`roteirista-tanaka`). Frame **REVELAÇÃO + MÉTODO**. Eixo: *toda renda de ETF sai da cota; isso não é
> golpe nem defeito. A pergunta é quanto sobra quando você soma a renda de volta, tira o imposto e compara com o CDI e o
> IPCA do mesmo período.* O caso de estudo é um **par de gêmeos da B3**: mesmo índice, um distribui e o outro reinveste.
> Desde 03/10 o vídeo tem **dois blocos a mais**, absorvidos de longos que saíram do calendário: **A, opções cobertas**
> (de onde vem a renda do SPYI11) e **B, taxa** (quanto a taxa tira em 10 anos). Os dois servem à mesma conta: a
> renda vem de algum lugar (A) e a caixa tem mais de uma saída (B).

> ⚠️ **LER ANTES DE ESCREVER:**
> 1. **Nenhum ETF é recomendado.** Ticker aparece como caso de estudo, com o critério do que olhar. Nada de "eu montaria",
>    "vale a pena", "o melhor" (`feedback_assessor_nao_pode_recomendar_alocacao`).
> 2. **Nada de corretora**, e nada da marca da gestora: DIVD11, DIVO11 e NDIV11 são de gestoras de grupos que têm
>    corretora. Usar só o ticker (`feedback_nao_citar_corretora_concorrente`).
> 3. **Imposto é o ponto mais arriscado do vídeo.** Nenhuma alíquota entra no roteiro sem estar na tabela DADOS CONFERIDOS.
>    Hoje **nenhuma regra de imposto de ETF ou BDR está conferida em fonte primária** (planalto, Receita e B3 estão
>    bloqueados nesta rede). Ver A CONFERIR 1 a 7. Se não for conferida até a gravação, o roteiro diz **onde ler**
>    (regulamento, lâmina, aviso de rendimentos) e não diz o número.
> 4. **Não reaproveitar texto de imposto do blog do canal.** Os posts 4816, 4537 e 4544 se contradizem sobre o dividendo de
>    BDR (isento × carnê-leão × "15% via DARF"). O post 4816 cai no bloqueio `IR_BDR_DIVIDENDO_ISENTO` do `gate_qualidade.py`.

---

## 1. Ficha de validade temporal

```
Evento central: nenhum (tema evergreen de método); o dado novo é o par DIVD11 × DIVO11 em 12 meses
Janela de preço: fechamento de 01/10/2025 → fechamento de 01/10/2026 (B3, COTAHIST)
Régua: CDI acumulado na mesma janela (BCB SGS 12) e IPCA de 12 meses até ago/2026 (BCB SGS 13522)
Publicação: 14/10/2026 (quarta)
Risco de prazo: o IPCA de set/2026 sai por volta de 09/10 (conferir no calendário do IBGE)
Status: DENTRO DA JANELA ✅ (com a ressalva do IPCA)
```

**Orientação de timing:** dizer sempre "nos 12 meses até 1º de outubro". Se gravar depois de 09/10, trocar o IPCA pelo de
setembro e manter a janela de preço (não precisa mover: a janela é fechada e datada).

---

## 2. Tese (uma frase)

**Todo ETF que paga renda paga com a própria cota, e o par de gêmeos da B3 prova isso. O que separa renda de devolução
não é o yield; é a conta de três linhas: quanto pagou, quanto a cota andou e quanto ficou acima do CDI e do IPCA, depois
do imposto.**

O que o Tanaka leva: a conta, a planilha de 4 colunas para refazer com qualquer ETF e o nome da ferramenta (seção 10).

---

## 3. A conta central

### 3.1 A fórmula (dizer uma vez, mostrar na tela)

```
retorno total = (cota no fim − cota no começo + rendimentos recebidos) ÷ cota no começo
```

- **Rendimento distribuído** = a soma do que caiu na conta no período (bruto e líquido de IR, as duas colunas).
- **Variação da cota** = (cota no fim ÷ cota no começo) − 1.
- **Retorno total** = as duas coisas somadas. É **esse** número que se compara com o CDI e com o IPCA. Bruto com bruto,
  líquido com líquido (`feedback_mesma_regua_nos_dois_lados`).

### 3.2 O exemplo hipotético (números redondos; escrever "exemplo" na tela)

| | valor |
|---|---|
| cota no começo | R$ 100 |
| rendimento: R$ 1,00 por mês × 12 | R$ 12 |
| cota no fim | R$ 92 |
| retorno total | (92 − 100 + 12) ÷ 100 = **4%** em 12 meses |
| IPCA de 12 meses até ago/2026 | 4,22% (conferido, seção 4) |
| retorno real | 1,04 ÷ 1,0422 − 1 = **−0,21%** |
| CDI na mesma janela | 14,47% (conferido) |

Leitura: a "renda de 12%" foi, na prática, a cota voltando para o bolso. Contra a inflação, empatou para baixo; contra o
CDI, perdeu 10 pontos.

### 3.3 O caso real: o par de gêmeos (fonte primária: B3)

Segundo a busca, os dois ETFs acompanham o mesmo índice de dividendos da B3 (IDIV); **conferir no regulamento** (A
CONFERIR 8). Um distribui todo mês, o outro reinveste.

| fechamento B3 | 01/10/2025 | 01/10/2026 | variação da cota | R$ 100 mil viraram (só cota) |
|---|---|---|---|---|
| DIVO11 (reinveste) | R$ 106,82 | R$ 132,90 | **+24,41%** | R$ 124.410 |
| DIVD11 (distribui) | R$ 55,86 | R$ 64,32 | **+15,15%** | R$ 115.150 |
| diferença | | | **9,26 pontos** | **R$ 9.260** |

**A pergunta "a renda saiu da cota?" tem resposta com dado da B3: sim.** A diferença de 9,26 pontos é, em grande parte,
o dinheiro que o DIVD11 mandou para a conta do cotista. Até aqui não há vilão.

**A linha que fecha o vídeo (falta um número, A CONFERIR 10):**

```
retorno total do DIVD11 = 15,15% + (soma dos rendimentos de 02/10/2025 a 01/10/2026 ÷ R$ 55,86)
líquido               = 15,15% + (rendimentos × (1 − alíquota da distribuição) ÷ R$ 55,86)      ← alíquota: A CONFERIR 1 e 2
```

Comparar com: DIVO11 (+24,41%, que ainda paga 15% de IR só quando vender, se a regra do ganho de capital for confirmada,
A CONFERIR 6), CDI (14,47%) e IPCA (4,22%).

**Os três finais possíveis (o roteiro escreve o que a conta der, nenhum outro):**
- (a) bruto ≈ gêmeo e líquido abaixo: "a renda não sumiu; o que custa é o imposto cobrado todo mês, em vez de no fim";
- (b) bruto abaixo do gêmeo além do que a taxa explica: investigar (diferença de taxa, de caixa parado ou de data-ex);
- (c) bruto acima do gêmeo: dizer isso e cortar a tese de "custo". O vídeo continua de pé, porque o método é o produto.

> ⚠️ Não fechar o roteiro antes de ter o número. É o furo que o juiz pega como "número inventado" (eliminatório).

### 3.4 Bloco A. Opções cobertas: de onde vem a renda (absorvido do antigo longo de 20/10)

- **Mecânica em linguagem simples:** o fundo vende a alguém o direito de comprar a carteira acima de um preço e recebe um
  prêmio por isso. O prêmio é a renda; o preço é abrir mão da alta acima daquele ponto. Se a carteira cai, a queda vem
  inteira. Resumo para a tela: **renda alta, alta limitada, queda inteira.**
- **A comparação (sem "qual é melhor"):** no DIVD11, a renda vem dos dividendos das empresas da carteira; no SPYI11
  (segundo a busca, ações do S&P 500 com venda de opções de compra; conferir no regulamento, A CONFERIR 21), vem
  principalmente do prêmio. Onde ler: regulamento (política de investimento) e lâmina.
- **O número:** cota do SPYI11 na B3 de **R$ 111,15 para R$ 109,60 (−1,39%)** de 01/10/2025 a 01/10/2026 (C3,
  conferido). Com os rendimentos da mesma janela (A CONFERIR 11), fazer na tela o **extrato de três linhas do SPYI11**.
  Atenção: a cota em reais carrega o dólar. Separar o câmbio (A CONFERIR 22) ou dizer, na fala, que a cota em reais
  mistura índice e dólar.
- **Régua extrema (10 segundos, opcional; é a primeira coisa que sai se o tempo apertar):** ETHY11, vendido com "30% de
  yield" nos títulos dos concorrentes: cota de **R$ 101,46 na estreia (16/12/2025) → R$ 64,99 (−35,95%)** em
  01/10/2026 (C9). Não explicar o produto (é cripto): só o par "yield de 30%, cota de −36%".
- **Proibido no bloco:** dizer qual é melhor, prever a cota, dizer que o prêmio de 1% ao mês "se mantém". O prêmio muda
  com a volatilidade do mercado (frase conceitual, sem número).
- Card para `IB1mBcF00jc` (JEPI39, a mesma estratégia em BDR).

### 3.5 Três coisas que pagam todo mês e não são a mesma coisa (tabela curta; o imposto detalhado é do longo de 27/10, "ETF de dividendos mensais ou FII: imposto e renda de cada um")

| | ETF da B3 que distribui | BDR de ETF americano | FII |
|---|---|---|---|
| exemplo de estudo | DIVD11, SPYI11 | JEPI39 (negocia desde 23/02/2026). **O JEPQ39 não existe na B3**: nenhum negócio no COTAHIST até 01/10/2026 (o post 4537 do blog já corrige isso) | o vídeo não cita ticker |
| de onde vem a renda | dividendos da carteira ou prêmio de opções, repassados pelo fundo | dividendo pago pelo ETF lá fora, convertido e repassado pela instituição depositária | aluguel ou juros do fundo |
| imposto da renda | **A CONFERIR 1 a 3** | **A CONFERIR 4** (pela busca, tabela progressiva e carnê-leão; não dizer até conferir) | isento só com 100 cotistas ou mais (Lei 14.754/2023, regra que a série já conferiu; reconferir o link, A CONFERIR 7) |
| onde ler | regulamento, lâmina e aviso de rendimentos | informe de rendimentos e prospecto do BDR | regulamento e relatório gerencial |

ETF de renda fixa com distribuição (AREA11 e afins) e ETF de FII ficam **fora** do Ep. 1. Uma frase: "ETF de renda fixa
tem outra regra de imposto, e fica para outro dia."

### 3.6 Bloco B. Quanto a taxa tira da renda (absorvido do antigo longo de 17/11)

- **A conta de 10 anos, só a taxa, sem rendimento (escrever "exemplo" na tela):**

| taxa ao ano | o que sobra em 10 anos | o que a taxa tirou | em R$ 100 mil |
|---|---|---|---|
| 0,5% | 0,995¹⁰ = 95,11% | **4,89%** | **R$ 4.889** |
| 1,5% | 0,985¹⁰ = 85,97% | **14,03%** | **R$ 14.027** |

  (conta própria, C20). Na fala, arredondar para "cerca de R$ 4,9 mil contra R$ 14 mil".
- **Responde a pergunta dos comentários** "Essa taxa de 1,50 do S&P 500 é bem alta, né?" (`Y4WHQiKcv1g`;
  `PERGUNTAS-SEM-RESPOSTA.md`, item 15) com a conta, sem dizer qual ETF escolher.
- **Liga com a conta central:** a taxa é uma das explicações para a diferença entre o DIVD11 e o DIVO11 no final (b) da
  3.3. Só dizer quanto ela explica depois de ter a taxa de cada um nas lâminas (A CONFERIR 9).
- **Onde ler:** lâmina do ETF, "taxa de administração" e "taxa total" (as duas podem ser diferentes). **Taxa de ETF real
  só com lâmina conferida** (A CONFERIR 9 e 23); até lá, as taxas do bloco são as do exemplo (0,5% e 1,5%).
- Analogia: a taxa é o **furo no fundo da caixa**: sai todo dia, haja renda ou não. O imposto fica na torneira (camada 4).
- O Short de 25/11 ("Taxa de administração do ETF: quanto tira em 10 anos") é o corte deste bloco (T17).

---

## 4. DADOS CONFERIDOS (só fonte primária)

| # | dado | valor | fonte primária | data |
|---|---|---|---|---|
| C1 | DIVO11, fechamento | R$ 106,82 (01/10/2025) → R$ 132,90 (01/10/2026): **+24,41%** | B3, COTAHIST A2025 e A2026: https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A2026.ZIP (cópia em `site-ativos/cache/raw/b3/`, sha256 no `.meta.json`) | baixado em 02/10/2026; lido em 03/10/2026 |
| C2 | DIVD11, fechamento | R$ 55,86 → R$ 64,32: **+15,15%** (mín. R$ 53,89; máx. R$ 70,52) | idem | idem |
| C3 | SPYI11, fechamento | R$ 111,15 → R$ 109,60: **−1,39%** (mín. R$ 99,24; máx. R$ 118,25) | idem | idem |
| C4 | NDIV11, fechamento | R$ 113,20 → R$ 123,93: **+9,48%** | idem | idem |
| C5 | QQQI11, fechamento | R$ 99,94 → R$ 99,36: **−0,58%** | idem | idem |
| C6 | IWMI11, fechamento | R$ 80,73 → R$ 78,50: **−2,76%** | idem | idem |
| C7 | BEST11, fechamento | R$ 104,00 → R$ 118,15: **+13,61%** (1º pregão em 09/09/2025) | idem | idem |
| C8 | BOVA11, fechamento (referência do Ibovespa) | R$ 142,52 → R$ 184,41: **+29,39%** | idem | idem |
| C9 | ETHY11, fechamento | R$ 101,46 (1º pregão, 16/12/2025) → R$ 64,99: **−35,95%** (mín. R$ 44,40) | idem | idem |
| C10 | COIN11, fechamento | R$ 85,75 → R$ 46,67: **−45,57%** | idem | idem |
| C11 | JEPI39 | 1º pregão em 23/02/2026 a R$ 51,12; R$ 50,05 em 01/10/2026 (−2,09%) | idem | idem |
| C12 | JEPQ39 | **nenhum negócio** de 02/01/2024 a 01/10/2026 | idem (busca do código nos 3 arquivos) | idem |
| C13 | Sem desdobramento nas séries acima | nenhuma variação diária maior que 20% em C1 a C11 | idem | idem |
| C14 | CDI acumulado | **14,47%** (251 dias úteis, 02/10/2025 a 01/10/2026) | BCB, SGS 12 (cópia em `site-ativos/cache/raw/bcb/sgs_12.json`, url e sha256 no `.meta.json`) | baixado em 02/10/2026 |
| C15 | IPCA de 12 meses | **4,22%** até ago/2026 | BCB, SGS 13522: https://api.bcb.gov.br/dados/serie/bcdata.sgs.13522/dados?formato=json (cópia em `sgs_13522.json`) | baixado em 02/10/2026 |
| C16 | Meta Selic | 13,75% desde 17/09/2026 | BCB, SGS 432 (`investir-e-cocar/pipeline/dados/macro_bcb.json`) | 02/10/2026 |
| C17 | `Fb0l4KEq27o` | 637 inscritos; 32.294 views intencionais; 19,7 inscritos por mil; 64,1% aos 30 s | YouTube Analytics do canal (`auditoria-canal/dados/`, `RELATORIO.md` seção 6) | exportação de 02/10/2026 |
| C18 | Busca "etfs que pagam dividendos mensais" | 208 views da Pesquisa em 6 meses (176 em `Y4WHQiKcv1g` + 32 em `c9Obo6F5_NU`); 1.877 no vitalício em `Y4WHQiKcv1g` | `termos_busca_recentes.csv` e `termos_busca_por_video.csv` | exportação de 02/10/2026 |
| C19 | Aritmética do exemplo | (92 − 100 + 12) ÷ 100 = 4%; 1,04 ÷ 1,0422 − 1 = −0,21%; 1% ao mês com a cota caindo 1% ao mês: R$ 100 mil → R$ 88.638 de cota + R$ 11.362 de renda = **R$ 100.000 (zero)** | conta própria | 03/10/2026 |
| C20 | Aritmética do bloco B | 1 − 0,995¹⁰ = 4,89% (R$ 4.889 em R$ 100 mil); 1 − 0,985¹⁰ = 14,03% (R$ 14.027) | conta própria | 03/10/2026 |

O que **não** está nesta tabela de propósito: nenhuma alíquota, nenhum rendimento pago por ETF, nenhuma taxa de ETF real e
nenhum dado de lâmina ou regulamento.

---

## 5. A CONFERIR (todo número que entra no roteiro e ainda não foi conferido) — 24 itens

**Quem confere:** o **Mac** baixa e lê a fonte (as páginas abaixo estão bloqueadas nesta rede); o **Denis** valida
imposto e qualquer frase que descreva produto (é ele quem assina como assessor).

| # | o que | por que importa | fonte primária onde conferir | quem |
|---|---|---|---|---|
| **1** | 🔴 **IR do rendimento distribuído por ETF de ações da B3**: alíquota, se é retido na fonte e se é definitivo (a busca diz 15% retido na fonte, sem fonte primária) | a linha "líquido" da conta central | Lei 14.754/2023 (artigo dos fundos de índice): https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14754.htm e a IN da Receita que a regulamentou (dez/2023) | Mac baixa; **Denis** valida |
| **2** | 🔴 **O DIVD11 retém o IR na distribuição?** Valor bruto e líquido por cota | sem isso, a coluna "líquido" é chute | aviso de rendimentos do administrador no fnet (CNPJ 54.314.981/0001-70, segundo a busca): https://fnet.bmfbovespa.com.br/fnet/publico/abrirGerenciadorDocumentosCVM?cnpjFundo=54314981000170 e regulamento do DIVD11 | Mac |
| **3** | 🔴 **IR do rendimento do ETF da B3 que investe no exterior** (SPYI11): a mesma regra do item 1? | só se o roteiro falar do imposto do SPYI11 | regulamento e lâmina do SPYI11 (administrador) + Lei 14.754/2023 | Mac; **Denis** valida |
| **4** | 🔴 **IR do dividendo de BDR** (JEPI39): tabela progressiva e carnê-leão? crédito do imposto retido nos EUA? A Lei 14.754/2023 mudou algo para BDR? | o blog do canal tem 3 versões diferentes (posts 4816, 4537 e 4544) | IN RFB 1.585/2015 (artigo de BDR) e Lei 14.754/2023; informe da instituição depositária | **Denis** |
| 5 | ETF de renda fixa: 25%, 20% ou 15% conforme o prazo médio da carteira (Lei 13.043/2014, art. 2º, visto só em busca) | só se o roteiro citar ETF de renda fixa (a orientação é não citar) | http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l13043.htm | Mac |
| 6 | Ganho de capital na venda de cota de ETF de ações: 15%, sem a isenção de R$ 20 mil por mês | a comparação com o DIVO11 (que só paga na venda) | IN RFB 1.585/2015 + Lei 13.043/2014 | Mac; **Denis** valida |
| 7 | FII isento só com 100 cotistas ou mais | a tabela 3.5 | Lei 14.754/2023 (já está em "Fontes que valem para todos os episódios" do `SERIE-RENDA-MENSAL.md`; não reconferido hoje porque o planalto está bloqueado) | Mac |
| 8 | DIVD11 e DIVO11 acompanham **o mesmo índice** (IDIV) | é a premissa do experimento | regulamento de cada um (administrador) e metodologia do IDIV na B3 | Mac |
| 9 | Taxa de administração e taxa total do DIVD11 e do DIVO11 (a busca diz 0,50% no DIVD11) | bloco B: quanto da diferença do par a taxa explica (final b da 3.3) | lâminas de 31/08/2026 dos dois (administrador) | Mac |
| **10** | 🔴 **Soma dos rendimentos do DIVD11 por cota, com data-ex de 02/10/2025 a 01/10/2026**, bruto e líquido | **fecha a conta central**; sem ele o bloco 4 não existe | B3, eventos corporativos do fundo + avisos de rendimento no fnet (item 2) | Mac |
| **11** | 🔴 **Soma dos rendimentos do SPYI11 por cota, data-ex de 02/10/2025 a 01/10/2026**, bruto e líquido, e a moeda do crédito (a busca fala em "dólar"; na conta cai em R$?) | **fecha o bloco A** (extrato de três linhas do SPYI11); sem ele, o bloco A fica só na mecânica | B3, eventos corporativos + avisos do administrador | Mac |
| 12 | Rendimentos do NDIV11 na mesma janela | só se entrar como segundo exemplo (a orientação é não entrar) | idem | Mac |
| 13 | IPCA de set/2026 (sai por volta de 09/10) | refazer o retorno real | BCB SGS 13522 e calendário do IBGE | Mac |
| 14 | CDI acumulado e cotas, se a janela for movida | evitar janela velha | BCB SGS 12; COTAHIST diário | Mac |
| 15 | ETHY11: data de estreia (16/12/2025 é o 1º pregão no COTAHIST) e a promessa de 2,5% ao mês (só busca) | só se usar a régua extrema | regulamento e lâmina do ETHY11 (administrador) | Mac |
| 16 | COIN11 com yield de 23,22% em 2025 (B3 Bora Investir, só busca) | só se usar no bloco A | https://borainvestir.b3.com.br/tipos-de-investimentos/renda-variavel/etfs/confira-os-etfs-que-pagaram-mais-dividendos-em-2025/ | Mac |
| 17 | JEPQ39 continua sem negociação na semana da gravação | a frase "não existe na B3" | COTAHIST diário (https://bvmf.bmfbovespa.com.br/InstDados/SerHist/) | Mac |
| 18 | Desde quando ETF da B3 pode distribuir (a busca diz 30/01/2023) | só se o roteiro contar a história | comunicado ou ofício da B3 | Mac |
| 19 | Rendimentos do JEPI39 desde 23/02/2026 | só se o JEPI39 entrar com número | B3, eventos corporativos do BDR; informe da instituição depositária | Mac |
| 20 | Views, datas e canais dos vídeos concorrentes (todos "só busca") | radar e anti-repetição; não entra no roteiro | YouTube (bloqueado aqui) | Mac |
| 21 | Estratégia do SPYI11 no regulamento: índice de referência (a busca diz NEOSSPYI), venda de opções de compra sobre o S&P 500, política de distribuição | a frase "a renda vem do prêmio" do bloco A | regulamento e lâmina do SPYI11 (administrador); fnet | Mac; **Denis** valida a descrição |
| 22 | Dólar (PTAX) de 01/10/2025 e de 01/10/2026 | separar câmbio de índice na cota do SPYI11 (bloco A) | BCB, SGS 1 (PTAX venda): https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=json | Mac |
| 23 | Taxa de administração e taxa total do SPYI11 | só se o bloco B usar uma taxa real (a orientação é ficar no exemplo de 0,5% e 1,5%) | lâmina do SPYI11 | Mac |
| 24 | O que a lâmina chama de "taxa total" (inclui custódia, índice, outras despesas?) | a frase "onde ler" do bloco B | lâmina e regulamento de qualquer um dos ETFs acima | Mac; **Denis** valida |

**Os 3 mais críticos:** **10** (sem ele a conta central não fecha), **1 + 2** (a alíquota e a retenção da distribuição do
ETF; é a linha "líquido") e **4** (imposto de BDR, em que o próprio blog do canal se contradiz). Logo depois vem o **11**,
que fecha o bloco A.

---

## 6. Ângulo de tensão (o "vilão" honesto)

**Não há fraude nem investigação.** Busquei: nada. O vilão é a **embalagem**:

- **O ranking por yield premia quem mais devolveu.** O topo de yield de 2025 segundo a B3 (COIN11, 23,22%, só busca) teve
  a cota em −45,57% em 12 meses (C10). O ETHY11, vendido em vídeo como "30% de yield", tem −35,95% desde a estreia (C9).
- **O extrato mostra só uma linha.** O app credita "rendimento" todo mês e não credita "cota que saiu". O Tanaka vê o
  verde e não vê o vermelho.
- **"Paga 1% ao mês" sem régua.** Com CDI de 14,47% na janela (C14), 12% ao ano com a cota parada perdeu do CDI na
  comparação bruto com bruto.

**Concessão obrigatória (P3), com palavras novas:** distribuir não é defeito. Para quem vive da renda, receber todo mês
pode valer o custo, desde que ele saiba o custo. O vídeo **não** diz "ETF de renda é ruim" e **não** repete o frame
"GOLPE?" de abril (`c9Obo6F5_NU`: 4.354 views e 17 inscritos, o pior da linha).

---

## 7. Validação de demanda

**GO.** Medida no próprio canal (C17 e C18), sem depender de outlier de concorrente:
- a linha de dividendos mensais converte 14,5 inscritos por mil views intencionais, contra 8,2 do resto (n = 6;
  `RELATORIO.md`, seção 2);
- `Fb0l4KEq27o` (ranking de ETFs, jan/2026) é o longo com mais inscritos do ano: 637, ou 19,7 por mil;
- o termo "etfs que pagam dividendos mensais" é o 11º termo de investimento dos últimos 6 meses (208 views da Pesquisa) e a
  família soma 4.558 no vitalício (`TERMOS.md`);
- **sinal contra:** o frame "GOLPE?" (`c9Obo6F5_NU`) teve 17 inscritos. O público da linha quer a renda; ataque ao produto
  não converte. O ângulo do Ep. 1 é "conta", não "denúncia".

Concorrência (arquivo `…-concorrentes.md`): ranking, "vale a pena" de um ETF e lançamento com promessa de yield.
**Nenhum** dos resultados de 2025 a out/2026 fez o par distribuidor × acumulador.

---

## 8. Anti-repetição

| já feito ou pautado | data | risco | guardrail do Ep. 1 |
|---|---|---|---|
| "6 ETFs que MAIS PAGARAM DIVIDENDOS MENSAIS em 2025" (`Fb0l4KEq27o`) | 13/01/2026 | baixo | o Ep. 1 é a continuação ("quanto sobrou"), sem lista e sem contradizer. Card no bloco 4 e tela final |
| "ETF DIVIDENDOS MENSAIS são um GOLPE?" (`c9Obo6F5_NU`) | 08/04/2026 | médio | nada de "golpe", nada de dúvida moral; só a conta |
| "ETF JEPI39 PAGA DIVIDENDOS MENSAIS, mas vale a pena?" (`IB1mBcF00jc`) | 26/02/2026 | baixo | JEPI39 só na tabela 3.5 |
| "ETFs que pagam dividendos mensais: o que mudou em 2026" (era 06/10) | foi para a fila de dezembro (T09) | baixo | o par DIVD11 × DIVO11 continua do Ep. 1; quando o balanço de dezembro for roteirizado, ele cita o Ep. 1 em vez de refazer o par |
| 27/10: "ETF de dividendos mensais ou FII: imposto e renda de cada um" (título novo) | 13 dias depois | médio | **continua:** tabela 3.5 curta; o imposto detalhado de cada tipo é do 27/10. O Ep. 1 não compara o imposto de ETF com o de FII além da tabela |
| 20/10 (opções) e 17/11 (taxa) | **saíram do calendário (T14)** e viraram os blocos A e B deste vídeo | — | os guardrails antigos ("opções em uma frase", "taxa só no final b") **caíram**. No lugar: 20/10 TRXF11 e 17/11 "Fundos imobiliários para iniciantes", sem sobreposição |
| Short de 25/11 "Taxa de administração do ETF: quanto tira em 10 anos" | 25/11 | baixo | é o corte do bloco B (T17): usar os mesmos números (C20), sem taxa de ETF real |

---

## Blocos absorvidos (decisão de 03/10)

**O que mudou** (`../CALENDARIO.md` e `../trocas.json`, troca T14, aprovada pelo Denis): o ETF de dividendos mensais estava
em 4 longos em 5 semanas. Os longos de **20/10 (opções)** e de **17/11 (taxa)** saíram e o conteúdo deles virou dois blocos
deste vídeo. No lugar entram o TRXF11 (20/10) e "Fundos imobiliários para iniciantes" (17/11). O 06/10 foi para a fila de
dezembro (T09). O 27/10 fica, com título novo.

Onde está cada coisa neste briefing (a versão reconciliada substitui o rascunho que estava aqui):

| bloco | conteúdo | posição no vídeo | tempo | conferido | a conferir |
|---|---|---|---|---|---|
| **A. Opções cobertas** (era o 20/10) | seção 3.4 | depois do bloco B, no lugar do antigo "onde o padrão aperta" | ~1:30 | C3, C9 | 11, 21, 22 (e 16, se usar o COIN11) |
| **B. Taxa** (era o 17/11) | seção 3.6 | logo depois do bloco 4 (a taxa explica parte da diferença do par) | ~1:00 | C20 | 9, 23, 24 |

Duração: **11 a 13 min**. O que encolhe primeiro está na seção 10.

## 9. Gancho (3 opções, voz do Denis)

Regras: "Fala, Tanaka." literal, número logo depois, stake em R$ dentro do gancho, a tese não se fecha no gancho, sem
meta-discurso.

**Opção A (o gêmeo; recomendada):**
> "Fala, Tanaka. Mesmo índice, mesmos doze meses na B3. A cota de um ETF subiu 24%. A do outro, 15%. O de 15% é o que
> te pagou renda todo mês. Em R$ 100 mil, são R$ 9.260 de diferença só na cota. Esse dinheiro sumiu, ou foi parar na sua
> conta? E, se foi, chegou inteiro?"

Por que: dado da B3 nos primeiros 10 segundos (C1, C2), stake em R$ e duas perguntas abertas (para onde foi e quanto
chegou). A resposta da primeira vem no bloco 3; a da segunda, no bloco 4.

**Opção B (a conta do zero; hipotética, escrever "exemplo" na tela):**
> "Fala, Tanaka. Um ETF que te paga 1% ao mês, com a cota caindo 1% ao mês, te pagou em um ano exatamente zero. R$ 100 mil
> viram R$ 88.638 de cota e R$ 11.362 de renda. O extrato te mostra a segunda linha. A primeira, você descobre quando
> vende."

Por que: é a conta do Short de 07/10 (seção 12); quem veio do Short reconhece. Risco: é hipotético, e o item 2 do portão
quer número **ancorado**.

**Opção C (a régua):**
> "Fala, Tanaka. 'Paga 1% ao mês.' Nos últimos doze meses, o CDI pagou 14,47%. Um ETF que te deu 12% de renda e deixou a
> cota parada perdeu do CDI por R$ 2.470 a cada R$ 100 mil, e isso antes de qualquer imposto."

Conta: 14,47% − 12% = 2,47 pontos → R$ 2.470 em R$ 100 mil (bruto com bruto). Por que não é a primeira: entrega a régua
cedo demais e esvazia o bloco 4.

---

## 10. Estrutura por blocos (11 a 13 min)

**Analogia sugerida (uma só, objeto físico, em camadas; o roteirista pode trocar, mas uma só):** a **caixa d'água com
torneira**. Camada 1: a renda é água saindo pela torneira da própria caixa. Camada 2: o cano que enche a caixa é o que
a carteira gera (dividendos, prêmio de opção). Camada 3: o gêmeo é a mesma caixa, com o mesmo cano e sem torneira; dá
para medir o nível das duas. Camada 4: o imposto é o vazamento na torneira, todo mês. Camada 5 (bloco B): a taxa é o furo no fundo da caixa, que
sai todo dia, haja renda ou não. No bloco A, a mesma caixa recebe água de outro cano (o prêmio da opção) e tem uma boia
que não deixa o nível passar de um ponto (a alta limitada). A última camada mantém o sujeito da primeira (a caixa), como
pede o 10b do juiz. **Nada de segunda analogia** para opções ou taxa.

| bloco | tempo | conteúdo | dado |
|---|---|---|---|
| **1. Gancho** | 0:00–0:30 | opção A | C1, C2 |
| **2. A conta que o extrato não faz** | 0:30–2:00 | a fórmula do 3.1 e o exemplo de 100 → 92 + 12 = 4%; contra o IPCA, −0,21%. Camada 1 da analogia | C15, C19 |
| **3. O gêmeo** | 2:00–4:00 | as duas cotas na tela, lado a lado, **sem** a conclusão: o Tanaka vê os 9,26 pontos e conclui que é a renda (prova no espectador). Depois o Denis confirma: "sim, saiu da cota, e é assim que funciona". Camadas 2 e 3 | C1, C2 |
| **4. Somando de volta** | 4:00–6:30 | retorno total do DIVD11 (bruto e líquido) contra DIVO11, CDI e IPCA. Agregado → linha: dos 9,26 pontos, quanto voltou como renda, quanto ficou no imposto e quanto é diferença de verdade. Camada 4 (vazamento na torneira). Card para `Fb0l4KEq27o` | C1, C2, C14, C15 + **A CONFERIR 1, 2 e 10** |
| **B. A taxa** (seção 3.6) | 6:30–7:30 | sai da "diferença de verdade" do bloco 4: o que mais tira da caixa, todo dia? A conta de 10 anos (0,5% × 1,5%) e onde ler na lâmina. Camada 5 (furo no fundo) | C20 + A CONFERIR 9 |
| **A. Opções cobertas** (seção 3.4) | 7:30–9:00 | de onde vem a renda quando ela é alta: prêmio de opção. Renda alta, alta limitada, queda inteira. Extrato de três linhas do SPYI11. Régua extrema do ETHY11 (opcional). Camada 2 de novo: o cano de outra água. Card para `IB1mBcF00jc` | C3, C9 + **A CONFERIR 11**, 21, 22 |
| **6. Três coisas que pagam todo mês** | 9:00–9:45 | tabela 3.5: ETF da B3, BDR de ETF americano (o JEPQ39 não existe na B3), FII. Imposto: só o que estiver conferido; o resto é "onde ler" e "o detalhe sai no dia 27" | C11, C12 + A CONFERIR 4 e 7 |
| **7. Objeções** | 9:45–11:15 | seção 11 (escolher 4 a 6) | — |
| **8. Fechamento** | 11:15–12:00 | a ferramenta batizada (seção 12) e a tela final para `Fb0l4KEq27o` | — |

**Duração-alvo: 11 a 13 min (este desenho dá cerca de 12).** Se passar de 13, encolher **nesta ordem**:
1. **bloco 6** (tabela 3.5) vira uma frase e a tabela fica só na tela (o imposto detalhado é do 27/10);
2. a **régua extrema do ETHY11** sai do bloco A;
3. as **objeções** caem para 4 (ficam "a cota volta", "só quero a renda", "e o imposto?" e "1,5% de taxa é alto?");
4. o exemplo hipotético do bloco 2 encurta para a fórmula com uma linha de números.

**Nunca cortar:** os blocos 3 e 4 (a conta central), o número do SPYI11 no bloco A e o fechamento.

**Por que B antes de A:** o bloco 4 termina na "diferença de verdade" entre os gêmeos, e a taxa é a primeira explicação
dela. Depois disso, o bloco A troca de gêmeo para um ETF cuja renda vem de outro lugar. Se a conta do item 10 der o
final (c) da 3.3 (o distribuidor ganhou do gêmeo), a ponte do bloco 4 para o B muda: a taxa entra como "mesmo assim,
tem um furo que não aparece no extrato".

Transições: carregar o objeto do bloco anterior (a caixa, o gêmeo, a linha do extrato). Proibido "agora vamos para",
"e aí vem a parte que" (eliminatório de costura A).

---

## 11. Objeções (e a resposta em uma frase)

| objeção | resposta |
|---|---|
| "Mas a cota volta." | Pode voltar. A conta é de um período; refaça em 2 ou 3 janelas diferentes (12, 24 e 36 meses, quando o ETF tiver idade para isso). |
| "Eu só quero a renda, não ligo para a cota." | A mesma porcentagem sobre uma cota menor é uma renda menor no ano seguinte. A cota é a renda do ano que vem. |
| "Então é melhor o que não distribui?" | O vídeo não decide isso. Quem precisa da renda todo mês paga um preço para recebê-la; a conta mostra o tamanho do preço. Sem ticker indicado. |
| "E o imposto?" | Depende do tipo (ETF da B3, BDR, FII) e está no regulamento e no aviso de rendimentos. **Alíquota só se estiver em DADOS CONFERIDOS.** |
| "O yield de 30% não compensa?" | Yield é rendimento ÷ cota. Se a cota cai, o yield sobe sozinho; ETHY11: −35,95% na cota desde a estreia. |
| "O JEPQ39 não paga mais que o JEPI39?" | Na B3, o JEPQ39 não negociou nenhuma vez até 01/10/2026 (C12). |
| "Essa taxa de 1,5% é alta?" | Em 10 anos, 1,5% ao ano tira cerca de 14% do patrimônio, contra cerca de 4,9% de uma taxa de 0,5% (C20). Compare a taxa total na lâmina. Sem dizer qual ETF escolher. |
| "O de opções paga 1% todo mês, garantido?" | Não há garantia: o prêmio muda com o mercado, e a renda muda junto. A conta de 12 meses mostra quanto veio de fato (bloco A). |

---

## 12. Fechamento e Short derivado

**Ferramenta batizada (fecho, nunca recap):** **"o extrato de três linhas"**. Antes de olhar o yield de qualquer ETF que
paga todo mês, escreva:
1. **quanto pagou** (soma dos rendimentos, bruto e líquido);
2. **quanto a cota andou** (fim ÷ começo − 1);
3. **quanto ficou acima do CDI e do IPCA** (linha 1 + linha 2, contra a régua do mesmo período).

Se a linha 3 for negativa, a renda foi devolução. Na tela, a planilha de 4 colunas (data, cota, rendimento, acumulado),
com o caminho para baixar cotas (séries históricas da B3) e rendimentos (eventos corporativos do fundo).

**Short derivado (pré-estreia, quarta 07/10, 40 s):**
- Título: "Recebeu 1% ao mês e a cota caiu 1% ao mês: quanto você ganhou?"
- 0–5 s: a pergunta, com R$ 100 mil na tela.
- 5–25 s: 12 meses em 4 quadros: a renda somando (R$ 11.362) e a cota descendo (R$ 88.638).
- 25–35 s: soma = R$ 100.000. "Zero. E o extrato só te mostrou o verde." (escrever "exemplo hipotético" na tela)
- 35–40 s: link para `Fb0l4KEq27o` até 14/10; depois de 14/10, trocar para o Ep. 1 (`PROPOSTA-CALENDARIO-V3.md`).
- Conta conferida (C19): 100.000 × (1 − 0,99¹²) = 11.362; 100.000 × 0,99¹² = 88.638.

**Short de corte do bloco B (quarta 25/11, T17):** "Taxa de administração do ETF: quanto tira em 10 anos".
- A tabela da 3.6: R$ 100 mil, 10 anos, 0,5% contra 1,5% ao ano: R$ 4.889 contra R$ 14.027 (C20). "Exemplo" na tela.
- Fecho: "a taxa está na lâmina; procure a taxa total". Sem ticker e sem taxa de ETF real.
- Link para o Ep. 1.

---

## 13. Alertas para o roteirista

1. **Não gravar com a conta central aberta.** Se o item 10 não chegar, o bloco 4 vira "o método", com o exemplo
   hipotético, e o gêmeo fica só como prova de que a renda sai da cota (bloco 3).
2. **Título e thumbnail são afirmações factuais** (`feedback_factcheck_titulo_e_qualificadores`). "A renda saiu da cota?"
   é pergunta; a resposta honesta é "sim, e é assim que funciona". O título não pode prometer escândalo.
3. **Cada fato uma vez.** O 24% contra 15% aparece no gancho e volta só como callback curto no bloco 4.
4. **Sem "vale a pena", "melhor", "eu faria".** O gêmeo é grupo de controle, não indicação.
5. **Não puxar texto de imposto do blog** (posts 3172, 4537, 4544 e 4816).
6. **Sem marca de gestora e sem corretora:** DIVD11, DIVO11, NDIV11, SPYI11 e JEPI39 só pelo código.
7. **Bloco A (opções):** o SPYI11 é caso de estudo. Proibido "qual é melhor", prever a cota ou chamar a renda de
   "garantida". A cota em reais mistura índice e dólar: dizer isso ou separar com a PTAX (A CONFERIR 22).
8. **Bloco B (taxa):** só os números do exemplo (0,5% e 1,5%). Taxa de ETF real só depois da lâmina (A CONFERIR 9 e 23).
9. **Os blocos A e B não pedem uma segunda analogia** nem ponte que anuncia ("agora vamos falar de taxa"): a ponte para o B
   carrega a "diferença de verdade" do bloco 4, e a ponte para o A carrega a pergunta "e quando a renda é alta demais?".

---

## 14. Fontes

Primárias (conferidas):
- B3, séries históricas COTAHIST A2024, A2025 e A2026: https://bvmf.bmfbovespa.com.br/InstDados/SerHist/ (cópias em
  `site-ativos/cache/raw/b3/`, baixadas em 02/10/2026; A2026 com last_modified de 01/10/2026 23:26 GMT).
- BCB, SGS 12, 13522 e 432 (cópias em `site-ativos/cache/raw/bcb/` e `investir-e-cocar/pipeline/dados/macro_bcb.json`,
  baixadas em 02/10/2026).
- YouTube Analytics do canal (`auditoria-canal/dados/`, exportação de 02/10/2026).

Secundárias (só busca, **não** sustentam número no roteiro): ver o arquivo de concorrentes. Regras de imposto vistas só em
busca: Lei 14.754/2023 (ETF com retenção de 15% na distribuição), Lei 13.043/2014, art. 2º (ETF de renda fixa por prazo)
e IN RFB 1.585/2015 (BDR na tabela progressiva). Todas na lista A CONFERIR.

*Briefing de 03/10/2026. Pesquisa de concorrentes feita antes ✅; dados da B3 e do BCB de fonte primária ✅; demanda medida no
canal ✅; anti-repetição ✅ (reconciliada com o calendário v3 de 03/10, troca T14: blocos A e B absorvidos); imposto ❌
ainda não conferido (A CONFERIR 1 a 7). Veredito: GO condicional aos itens 1, 2 e 10 (conta central) e 11 (bloco A).*
