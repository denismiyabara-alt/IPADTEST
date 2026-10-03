---
tema: "ETF que paga dividendos mensais: a renda saiu da cota?" (título PROVISÓRIO; ainda passa pelo empacotador e pelo teste A/B)
serie: Série Renda Mensal, Ep. 1 de 6
formato: long (11-13 min; com os blocos A, de opções, e B, de taxa, absorvidos em 03/10)
data_briefing: 2026-10-03 (revisto no mesmo dia com a conferência do Mac, 2026-10-14-CONFERENCIA.md)
data_publicacao: 2026-10-14 (quarta, 19h)
janela_validade: os preços são de 01/10/2026; se gravar depois de 09/10, refazer o retorno real com o IPCA de setembro (seção 5)
dado_valor_em: 15 s (gancho A)
status: GO, COM AJUSTES (seção 13). A conta central e o bloco A fecharam em fonte primária. O Denis valida as frases de imposto, a do BDR e a descrição do SPYI11
frame: REVELAÇÃO / educativo (método). Nada de COMPARAÇÃO "qual é melhor", nada de "vale a pena"
tickers: DIVD11, DIVO11 (caso de estudo central); SPYI11 (caso de estudo do bloco A); ETHY11, JEPI39 (exemplos de 1 frase). Nenhum é recomendado
concorrentes: 2026-10-14-etf-dividendos-mensais-concorrentes.md
conferencia: 2026-10-14-CONFERENCIA.md (Mac, 03/10/2026; fonte de toda linha "R" em DADOS CONFERIDOS)
puxa: Fb0l4KEq27o (637 inscritos); IB1mBcF00jc (JEPI39, card no bloco A); c9Obo6F5_NU
corte: Short de 25/11 "Taxa de administração do ETF: quanto tira em 10 anos" sai do bloco B (T17)
---

# BRIEFING: ETF que paga todo mês. A renda saiu da cota?

> Para o roteirista (`roteirista-tanaka`). Frame **REVELAÇÃO + MÉTODO**. Eixo: *toda renda de ETF sai da cota; isso não é
> golpe nem defeito. Olhar só a cota engana; a conta certa soma a renda de volta, tira o imposto e compara com o CDI e o
> IPCA do mesmo período.* O caso de estudo é um **par de gêmeos da B3**: mesmo índice (IDIV), um distribui e o outro
> reinveste.
> Dois blocos a mais, absorvidos em 03/10 de longos que saíram do calendário: **A, opções cobertas** (de onde vem a renda
> do SPYI11) e **B, taxa** (quanto a taxa tira em 10 anos).

> ⚠️ **O QUE A CONFERÊNCIA MUDOU (ler antes de escrever):**
> 1. **A tese do gêmeo virou "parece, mas não é".** Só na cota, o distribuidor ficou 9,26 pontos atrás. Somando a renda, ficou
>    **0,74 ponto** atrás. "R$ 9.260 de diferença" **sem** o "somando de volta" engana. O vídeo não pode deixar esse número
>    sozinho em lugar nenhum: gancho, thumbnail e Short incluídos.
> 2. **O imposto mensal existe, mas em 12 meses quase não pesou**: na mesma régua (os dois vendidos no fim), dá 20,12% contra
>    20,75%. Não dizer "o que custa é o imposto mensal".
> 3. **A taxa do par é igual** (0,50% ao ano nas duas lâminas). A taxa **não** explica a diferença do par; o bloco B vira
>    lição geral.
> 4. **No SPYI11, quem vende as opções é o ETF americano** em que ele investe 95% ou mais, e não o fundo brasileiro.
> 5. **Dividendo de BDR: nenhuma alíquota no vídeo.** Só "não é isento; siga o informe da instituição depositária".

> **Regras que continuam:** número firme só de DADOS CONFERIDOS; nenhum ETF recomendado; ETF só pelo código, sem marca da
> gestora e sem corretora (`feedback_nao_citar_corretora_concorrente`, `feedback_assessor_nao_pode_recomendar_alocacao`);
> não reaproveitar texto de imposto do blog (posts 3172, 4537, 4544 e 4816; a conferência, seção 6, mostra o que está errado
> em cada um).

---

## 1. Ficha de validade temporal

```
Evento central: nenhum (tema evergreen de método); o dado novo é o par DIVD11 × DIVO11 em 12 meses
Janela de preço: fechamento de 01/10/2025 → fechamento de 01/10/2026 (B3, COTAHIST)
Janela de renda: eventos com data-base (último dia "com") de 02/10/2025 a 01/10/2026 (fnet)
Régua: CDI acumulado na mesma janela (BCB SGS 12) e IPCA de 12 meses até ago/2026 (BCB SGS 13522)
Publicação: 14/10/2026 (quarta)
Risco de prazo: o IPCA de set/2026 sai por volta de 09/10 (ainda não saiu em 03/10)
Status: DENTRO DA JANELA ✅
```

**Orientação de timing:** dizer "nos 12 meses até 1º de outubro". Se gravar depois de 09/10, trocar só o IPCA (as colunas
"real"); a janela de preço e de renda fica.

**Convenção de arredondamento (para nenhum número mudar de valor entre blocos):** os valores em R$ sobre R$ 100 mil saem
das porcentagens com 2 casas: cota do DIVD11 R$ 115.150, renda bruta R$ 8.520, total R$ 123.670, DIVO11 R$ 124.410,
diferenças de R$ 9.260 e R$ 740. A conferência, calculando a partir das cotas, chega a R$ 115.145 e R$ 8.524; a diferença
é de R$ 4 a R$ 5, só de arredondamento. **O roteiro usa a convenção das porcentagens, sempre.**

---

## 2. Tese (uma frase)

**Todo ETF que paga renda paga com a própria cota. Olhando só a cota, o gêmeo que distribui parece ter perdido R$ 9 mil;
somando a renda, perdeu R$ 740. A conta que separa renda de devolução é o extrato de três linhas: quanto pagou, quanto a
cota andou e quanto ficou acima do CDI e do IPCA, depois do imposto.**

E o mesmo extrato, aplicado a um ETF que paga quase 1% ao mês (SPYI11), mostra o outro lado: a renda alta veio com a cota
parada, e o total ficou **abaixo do CDI**.

---

## 3. A conta central

### 3.1 A fórmula (dizer uma vez, mostrar na tela)

```
retorno total = (cota no fim − cota no começo + rendimentos recebidos) ÷ cota no começo
```

- **Rendimento distribuído** = a soma do que caiu na conta no período (bruto e líquido de IR, as duas colunas), sem
  reinvestir.
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
| IPCA de 12 meses até ago/2026 | 4,22% (C15) |
| retorno real | 1,04 ÷ 1,0422 − 1 = **−0,21%** |
| CDI na mesma janela | 14,47% (C14) |

Leitura: neste exemplo, a "renda de 12%" foi a cota voltando para o bolso. Serve para ensinar a fórmula; o caso real
(3.3) dá outro resultado, e é isso que segura o vídeo.

### 3.3 O caso real: o par de gêmeos (fonte primária: B3, fnet, regulamentos)

Os dois acompanham o **IDIV**, índice de dividendos da B3. O DIVD11 **distribui** todo mês (até o 10º dia útil do mês
seguinte); o DIVO11 **reinveste** (R1). Taxa total máxima de **0,50% ao ano nos dois** (R3).

**Passo 1, só a cota (o que o gráfico mostra):**

| fechamento B3 | 01/10/2025 | 01/10/2026 | variação da cota | R$ 100 mil viraram (só cota) |
|---|---|---|---|---|
| DIVO11 (reinveste) | R$ 106,82 | R$ 132,90 | **+24,41%** | R$ 124.410 |
| DIVD11 (distribui) | R$ 55,86 | R$ 64,32 | **+15,15%** | R$ 115.150 |
| diferença | | | **9,26 pontos** | **R$ 9.260** |

**Passo 2, somando a renda de volta (o que o extrato não mostra):** o DIVD11 pagou **R$ 4,7614 por cota em 12 eventos**,
ou 8,52% da cota de R$ 55,86 (R4).

| 01/10/2025 → 01/10/2026 | cota | renda | retorno total | contra o DIVO11 (+24,41%) | contra o CDI (14,47%) | real (IPCA 4,22%) |
|---|---|---|---|---|---|---|
| DIVD11 bruto | +15,15% | +8,52% | **+23,67%** | **−0,74 ponto** | +9,20 pontos | +18,66% |
| DIVD11 líquido (15% na fonte) | +15,15% | +7,25% | **+22,39%** | −2,02 pontos | +7,92 pontos | +17,43% |
| DIVO11 (sem vender) | +24,41% | 0 | +24,41% | — | +9,94 pontos | +19,37% |

Em R$ 100 mil: cota de R$ 115.150 + renda bruta de R$ 8.520 = **R$ 123.670**, contra **R$ 124.410** do DIVO11.
**Dos 9,26 pontos de diferença na cota, 8,52 voltaram como renda. A diferença de verdade é de 0,74 ponto: R$ 740.**

**Resposta ao título:** sim, a renda saiu da cota, e voltou quase inteira para o bolso. Quem olhou só a cota achou que
perdeu R$ 9 mil.

**Passo 3, o imposto na mesma régua (R5, R6):** o DIVD11 tem 15% retidos na fonte em cada distribuição; o DIVO11 só paga
15% quando a cota é vendida (sem a isenção de R$ 20 mil). Comparar o líquido do DIVD11 com o DIVO11 **sem vender** mistura
régua. Com os dois vendidos em 01/10/2026:
- DIVO11: 24,41% × 0,85 = **20,75%**;
- DIVD11: 15,15% × 0,85 + 7,25% = **20,12%**;
- diferença: **0,63 ponto**, praticamente a mesma do bruto.

**Frase certa sobre o imposto:** "o imposto do distribuidor vem todo mês, em vez de vir no fim; em um ano, isso quase
empatou." O efeito existe (o imposto antecipado deixa de render dentro do fundo, e isso cresce com os anos), mas **não foi
medido** para prazos longos. **Proibido:** "o que custa é o imposto mensal".

**De onde vêm os 0,74 ponto:**
- **Não é a taxa:** é a mesma nos dois (R3).
- Explicações compatíveis com os documentos, **sem medir quanto cada uma pesa**: a renda do DIVD11 foi somada sem
  reinvestir, enquanto o DIVO11 capitaliza no ano; o DIVD11 segura o dinheiro entre receber o dividendo e pagar; e a
  aderência de cada um ao IDIV pode ser diferente.
- No roteiro: "a diferença de verdade foi de menos de 1 ponto em 12 meses". **Não atribuir a nenhuma causa.**

**A renda não é constante (R4):** de R$ 0,03 (nov/2025) a R$ 1,63 (jan/2026) por cota; janeiro sozinho foi 34% do ano.
"Paga todo mês" não quer dizer "paga o mesmo todo mês". Serve para a objeção da seção 11.

### 3.4 Bloco A. Opções cobertas: de onde vem a renda (absorvido do antigo longo de 20/10)

- **Mecânica, com a correção da conferência (R8):** o SPYI11 põe **95% ou mais** do patrimônio em cotas de **um ETF
  americano (o SPYI)**. É esse ETF de lá que tem ações do S&P 500 e **vende opções de compra** fora do dinheiro, renovadas
  todo mês: vende a alguém o direito de comprar acima de um preço e recebe um prêmio. O prêmio é a renda; o preço é abrir
  mão da alta acima daquele ponto. Se a carteira cai, a queda vem inteira. Na tela: **renda alta, alta limitada, queda
  inteira.** O fundo brasileiro **não** vende opção (só pode usar derivativo para hedge). **O Denis valida esta descrição.**
- **A comparação, sem "qual é melhor":** no DIVD11, a renda vem dos dividendos das empresas; no SPYI11, vem principalmente
  do prêmio que o ETF de lá recebe. Onde ler: regulamento (política de investimento).
- **O extrato de três linhas do SPYI11 (R7, R9):**

| linha | bruto | líquido de 15% |
|---|---|---|
| 1. quanto pagou | R$ 13,08 por cota em 12 eventos, crédito **em reais** = **11,76%** da cota de R$ 111,15 (cerca de 0,98% ao mês) | R$ 11,11 = **10,00%** |
| 2. quanto a cota andou | **−1,39%** (R$ 111,15 → R$ 109,60) | idem |
| 3. retorno total | **+10,37%** | **+8,61%** |
| contra o CDI (14,47%) | **−4,10 pontos** (R$ 4.100 em R$ 100 mil) | −5,86 pontos |
| real (IPCA 4,22%) | +5,90% | +4,21% |

- **Câmbio (R10):** a PTAX caiu 2,12% na janela (R$ 5,3208 → R$ 5,2079). Sem o dólar, a cota ficou perto de zero
  (+0,74% em dólar; a PTAX é das 13h e o fechamento da B3 é às 18h, então a separação é aproximada). Frase segura: "pagou
  quase 1% ao mês, a cota ficou parada e, somando tudo, ficou abaixo do CDI do mesmo período."
- **Imposto (R5):** a mesma regra de 15% na distribuição vale para o SPYI11 (a Lei não separa ETF por onde investe; os
  avisos dizem "isento: Não"). Ressalva: o regulamento do SPYI11 não fala de tributação.
- **Régua extrema (10 segundos, opcional; é a primeira coisa que sai se o tempo apertar):** ETHY11, cota de **R$ 101,46 no
  1º pregão (16/12/2025) → R$ 64,99 (−35,95%)** em 01/10/2026 (C9). A "promessa de 30%" **não** foi conferida (item 15):
  sem ela, dizer só "um ETF vendido como de renda alta" e a cota.
- **Proibido no bloco:** dizer qual é melhor, prever a cota, dizer que a renda de quase 1% ao mês "se mantém". O prêmio
  muda com o mercado (frase conceitual, sem número).
- Card para `IB1mBcF00jc` (JEPI39, a mesma família de estratégia, em BDR).

### 3.5 Três coisas que pagam todo mês e não são a mesma coisa (tabela curta; o imposto detalhado é do longo de 27/10, "ETF de dividendos mensais ou FII: imposto e renda de cada um")

| | ETF da B3 que distribui | BDR de ETF americano | FII |
|---|---|---|---|
| exemplo de estudo | DIVD11, SPYI11 | JEPI39 (negocia desde 23/02/2026). **O JEPQ39 não existe na B3**: nenhum negócio no COTAHIST até 01/10/2026 (reconferir na semana da gravação, item 17) | o vídeo não cita ticker |
| de onde vem a renda | dividendos da carteira ou prêmio de opções (no SPYI11, recebido pelo ETF americano), repassados pelo fundo | dividendo pago pelo ETF lá fora, convertido e repassado pela instituição depositária | aluguel ou juros do fundo |
| imposto da renda | **15% retido na fonte**, definitivo para pessoa física (R5) | **não é isento; siga o informe da instituição depositária** (R12). Nenhuma alíquota, nem "carnê-leão", nem "15%" | **isento** para pessoa física se o fundo tiver 100 cotistas ou mais e o cotista tiver menos de 10% das cotas (R13) |
| imposto na venda | 15% sobre o ganho, sem a isenção de R$ 20 mil (R6) | 15% sobre o ganho (R12) | fora do Ep. 1 (é do 27/10) |
| onde ler | regulamento, lâmina e aviso de rendimentos | informe de rendimentos e prospecto do BDR | regulamento e relatório gerencial |

Não dizer **quem** retém o IR do ETF ("a corretora", "a gestora"): a Lei não nomeia e o aviso não diz (R5). Dizer "retido
na fonte".

ETF de renda fixa com distribuição (AREA11 e afins) e ETF de FII ficam **fora** do Ep. 1. Uma frase: "ETF de renda fixa
tem outra regra de imposto, e fica para outro dia." (A regra está conferida em R14, se alguém perguntar.)

### 3.6 Bloco B. Quanto a taxa tira da renda (absorvido do antigo longo de 17/11)

- **O que mudou:** a taxa do par é igual (0,50% ao ano, R3). O bloco B **não** explica a diferença dos gêmeos; vira lição
  geral: *quando dois ETFs têm taxas diferentes, isto é o que pesa em 10 anos.*
- **A conta de 10 anos, só a taxa, sem rendimento (escrever "exemplo" na tela):**

| taxa ao ano | o que sobra em 10 anos | o que a taxa tirou | em R$ 100 mil |
|---|---|---|---|
| 0,5% | 0,995¹⁰ = 95,11% | **4,89%** | **R$ 4.889** |
| 1,5% | 0,985¹⁰ = 85,97% | **14,03%** | **R$ 14.027** |

  (conta própria, C20). Na fala, "cerca de R$ 4,9 mil contra R$ 14 mil".
- **Responde a pergunta dos comentários** "Essa taxa de 1,50 do S&P 500 é bem alta, né?" (`Y4WHQiKcv1g`;
  `PERGUNTAS-SEM-RESPOSTA.md`, item 15). O "1,50" do comentário bate com a **Taxa Máxima de 1,51% ao ano do SPYI11**, que
  soma a taxa do fundo daqui e a do ETF americano em que ele investe (R11). Pode entrar como "taxa máxima de 1,51% no
  regulamento, contando a do fundo lá fora", sem dizer se é cara para ele ou não.
- **Onde ler (R3, R11):** "na lâmina, procure a **taxa total máxima**; no ETF que compra fundo lá fora, veja no regulamento
  se ela soma a taxa do fundo de fora." A licença do índice e outras despesas ficam fora dessa taxa (são encargos à parte).
  **O Denis valida a frase.**
- Analogia: a taxa é o **furo no fundo da caixa**: sai todo dia, haja renda ou não. O imposto fica na torneira.
- O Short de 25/11 é o corte deste bloco (T17).

---

## 4. DADOS CONFERIDOS (só fonte primária)

### 4.1 Preços, régua e dados do canal (conferidos por mim, 03/10/2026)

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
| C19 | Aritmética do exemplo e do Short | (92 − 100 + 12) ÷ 100 = 4%; 1,04 ÷ 1,0422 − 1 = −0,21%; 1% ao mês com a cota caindo 1% ao mês: R$ 100 mil → R$ 88.638 de cota + R$ 11.362 de renda = **R$ 100.000 (zero)** | conta própria | 03/10/2026 |
| C20 | Aritmética do bloco B | 1 − 0,995¹⁰ = 4,89% (R$ 4.889 em R$ 100 mil); 1 − 0,985¹⁰ = 14,03% (R$ 14.027) | conta própria | 03/10/2026 |

### 4.2 Conferidos pelo Mac na fonte primária (`2026-10-14-CONFERENCIA.md`, 03/10/2026)

| # | dado | valor | fonte primária (como está no relatório) | item antigo |
|---|---|---|---|---|
| R1 | Índice e política do par | **DIVD11 e DIVO11 acompanham o IDIV** (B3). DIVD11 distribui mensalmente, até o 10º dia útil do mês seguinte; DIVO11 reinveste ("os resultados da CLASSE serão automaticamente nela reinvestidos") | regulamento do DIVD11 (fnet id 939399, ref. 02/07/2025), Anexo, itens 5 e 5.1; regulamento do DIVO11 (fnet id 932100, ref. 25/06/2025, CNPJ 13.416.245/0001-46), Anexo, item 5. `https://fnet.bmfbovespa.com.br/fnet/publico/downloadDocumento?id=<id>` | 8 |
| R2 | DIVO11 não distribui | nenhum aviso de proventos em dinheiro no fnet de jan/2025 a set/2026 | fnet | 8 |
| R3 | Taxas do par | **iguais**: administração 0,04%, gestão 0,43%, custódia 0,03%; **Taxa Total Máxima 0,50% ao ano** nos dois; sem performance. A taxa total máxima não inclui licença do índice nem outros encargos | lâminas de 31/08/2026 (DIVD11: https://assetfront.arquivosparceiros.cloud.itau.com.br/FND/ITAUIDIV67421_It_Now_IDIV_Renda_Dividendos_RL.pdf; DIVO11: https://assetfront.arquivosparceiros.cloud.itau.com.br/FND/ITAUCARD49295_It_Now_IDIV.pdf); regulamentos, DIVD11 Anexo item 16, DIVO11 Anexo item 17 | 9, 24 |
| R4 | Renda do DIVD11 | **R$ 4,7614 por cota bruto** em 12 eventos (data-base de 06/10/2025 a 04/09/2026; de R$ 0,0336 a R$ 1,6290); líquido de 15%: **R$ 4,0472**. Retorno total **23,67% bruto, 22,39% líquido** | fnet, "Aviso aos Cotistas - Estruturado / Proventos em dinheiro", CNPJ 54.314.981/0001-70, ids 1005111, 1029944, 1052427, 1075160, 1101847, 1126862, 1154608, 1181209, 1211268, 1238292, 1276218, 1309131 (`https://fnet.bmfbovespa.com.br/fnet/publico/exibirDocumento?id=<id>&cvm=true`); campo "Rendimento isento de IR: Não" em todos | 10, 2 |
| R5 | IR na distribuição de ETF (que não seja de renda fixa) | **15%, retido na fonte na data da distribuição**, definitivo para pessoa física; vale também para ETF que investe no exterior. A Lei não nomeia quem retém | Lei 14.754/2023 (planalto, texto compilado): https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14754.htm, **arts. 18, II; 22; 24, caput e § 1º; 32, I; vigência pelo art. 47, II (desde 01/01/2024)**. Se o ETF não se enquadrar como entidade de investimento, cai no art. 26: mesma alíquota de 15% | 1, 2, 3 |
| R6 | Venda de cota de ETF de ações | **15%** sobre o ganho líquido do mês, DARF pago pelo investidor até o último dia útil do mês seguinte, **sem** a isenção de R$ 20 mil | IN RFB 1.585/2015, **arts. 27, I; 56, § 5º; 57; 59, § 2º, II** (https://normasinternet2.receita.fazenda.gov.br/#/consulta/externa/67494) | 6 |
| R7 | Renda do SPYI11 | **R$ 13,0763 por cota bruto** em 12 eventos (data-base de 21/10/2025 a 15/09/2026), **crédito em reais**; líquido de 15%: R$ 11,1149. Retorno total **10,37% bruto, 8,61% líquido** | fnet, avisos do CNPJ 51.949.867/0001-29, versão 2 de cada mês, ids 1018305, 1046500, 1069658, 1088920, 1117292, 1139866, 1167061, 1199732, 1222434, 1261695, 1296519, 1321782; regulamento (fnet id 647768), Anexo 2.4 (moeda de referência: real) | 11 |
| R8 | Estratégia do SPYI11 | índice NEOS U.S. Equity High Income; **95% ou mais** em cotas de um ETF americano (SPYI), que tem ações do S&P 500 e **vende opções de compra** fora do dinheiro, renovadas todo mês; o fundo brasileiro só usa derivativo para hedge; distribuição mensal, no 6º dia útil do mês seguinte | regulamento do SPYI11 (fnet id 647768, ref. 29/04/2024, a versão mais nova achada), Anexo, itens 5.1, 5.1.1, 5.3, 6.1.1 e 14.1 | 21 |
| R9 | Aritmética do extrato do SPYI11 e do par | ver as tabelas 3.3 e 3.4; mesma régua: DIVO11 24,41% × 0,85 = 20,75%; DIVD11 15,15% × 0,85 + 7,25% = 20,12% | conta da conferência, refeita por mim (bate) | 10, 11 |
| R10 | PTAX venda | **R$ 5,3208** (01/10/2025) e **R$ 5,2079** (01/10/2026): dólar **−2,12%**; cota do SPYI11 em dólar ≈ +0,74% | BCB, Olinda/PTAX (CotacaoDolarPeriodo, 13h): https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/ | 22 |
| R11 | Taxa do SPYI11 | administração 0,09% a 0,13% conforme o patrimônio (mínimo de R$ 8 mil por mês), gestão 0,83%, custódia até 0,02%; **Taxa Máxima 1,51% ao ano, somando a do ETF americano** | regulamento do SPYI11 (fnet id 647768), Anexo, itens 7.1, 7.1.2 e 7.3 (a lâmina não foi achada) | 23, 24 |
| R12 | BDR | dividendo de BDR **não é isento** (não há previsão legal de isenção para dividendo de empresa estrangeira); a **venda** paga 15% sobre o ganho líquido. **Nenhuma norma primária diz a forma de pagar o dividendo de BDR** (carnê-leão ou 15% na declaração anual) | P&R IRPF 2026, perguntas 137 e 138 (https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/perguntas-e-respostas/dirpf/p-r-irpf-2026-v1-00-2026-04-23.pdf); IN RFB 1.585/2015, arts. 56, § 1º, I, "a", e 57 (venda); Lei 14.754/2023, arts. 2º a 4º | 4 |
| R13 | FII | isento para pessoa física se o fundo tiver **100 cotistas ou mais**, o cotista tiver menos de 10% das cotas e o grupo de pessoas ligadas, menos de 30% | Lei 11.033/2004, art. 3º, III, e § 1º, I a III, na redação da Lei 14.754, art. 41 (https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l11033.htm). No planalto, o primeiro "100 cotistas" aparece riscado; o vigente vem depois do "500" da MP 1.184, que perdeu a vigência | 7 |
| R14 | ETF de renda fixa | 25% (prazo médio até 180 dias), 20% (181 a 720), 15% (acima de 720) | Lei 13.043/2014, art. 2º, I a III, § 1º e § 4º (http://www.planalto.gov.br/ccivil_03/_ato2011-2014/2014/lei/l13043.htm) | 5 |

O que **continua fora** desta tabela de propósito: a alíquota do dividendo de BDR (não existe regra explícita), quem retém
o IR do ETF (não nomeado) e qualquer número dos itens pendentes da seção 5.

---

## 5. A CONFERIR (o que ainda falta) — 8 itens + 4 validações do Denis

| # | o que | por que importa | fonte primária onde conferir | quem |
|---|---|---|---|---|
| 13 | IPCA de set/2026 (sai por volta de 09/10; não tinha saído em 03/10) | refazer as colunas "real" se gravar depois | BCB SGS 13522 e calendário do IBGE | Mac |
| 17 | JEPQ39 continua sem negociação na semana da gravação | a frase "não existe na B3" | COTAHIST diário (https://bvmf.bmfbovespa.com.br/InstDados/SerHist/) | Mac |
| 15 | ETHY11: a promessa de 2,5% ao mês / 30% ao ano | só se a régua extrema citar a promessa; sem conferir, fica só a cota (C9) | regulamento e lâmina do ETHY11 | Mac |
| 16 | COIN11 com yield de 23,22% em 2025 (só busca) | só se usar | https://borainvestir.b3.com.br/tipos-de-investimentos/renda-variavel/etfs/confira-os-etfs-que-pagaram-mais-dividendos-em-2025/ | Mac |
| 12 | Rendimentos do NDIV11 | só se entrar (a orientação é não entrar) | fnet, avisos de proventos | Mac |
| 18 | Desde quando ETF da B3 pode distribuir (a busca diz 30/01/2023) | só se o roteiro contar a história | comunicado ou ofício da B3 | Mac |
| 19 | Rendimentos do JEPI39 | só se o JEPI39 entrar com número (a orientação é não) | B3, eventos do BDR; informe da instituição depositária | Mac |
| 20 | Views, datas e canais dos concorrentes | radar; não entra no roteiro | YouTube | Mac |

**Validações do Denis (ele assina como assessor; nada bloqueia a gravação, mas o texto final passa por ele):**
- **V1, imposto do ETF (R5):** "15% retido na fonte, definitivo para pessoa física", sem nomear quem retém. Ressalvas da
  conferência, seção 4.1: a base de cálculo na distribuição não está escrita na Lei (leitura usada: 15% sobre o valor
  distribuído; conferir num informe de rendimentos real).
- **V2, BDR (R12):** a frase "não é isento; siga o informe da instituição depositária". Se ele quiser cravar um regime
  (carnê-leão ou 15% na declaração anual), é decisão dele ou de consulta formal; o vídeo não crava.
- **V3, SPYI11 (R8):** "quem vende as opções é o ETF americano em que ele investe". O regulamento é de abril/2024; pode
  haver versão posterior fora do fnet.
- **V4, taxa (R3, R11):** a frase "procure a taxa total máxima; no ETF que compra fundo lá fora, veja se ela soma a taxa
  de lá".

**Pendência de arquivo (não é número do roteiro):** a conferência sugere copiar os documentos baixados (leis, P&R,
regulamentos, lâminas, avisos e PTAX) para `site-ativos/cache/raw/` com sha256, como foi feito com o COTAHIST.

---

## 6. Ângulo de tensão (o "vilão" honesto)

**Não há fraude nem investigação.** Busquei: nada. O vilão é **olhar uma linha só**:

- **O gráfico da cota engana para os dois lados.** No par, a cota sozinha faz o distribuidor parecer R$ 9 mil atrás; somando
  a renda, são R$ 740. No SPYI11, a renda sozinha (quase 1% ao mês) faz parecer ótimo; somando a cota, ficou R$ 4.100 atrás
  do CDI em R$ 100 mil.
- **O ranking por yield premia quem mais devolveu.** ETHY11 −35,95% na cota desde a estreia (C9); COIN11 −45,57% em 12
  meses (C10). (O yield de 23,22% do COIN11 não está conferido; não usar sem o item 16.)
- **O extrato mostra só uma linha.** O app credita "rendimento" todo mês e não mostra o resto.

**Concessão obrigatória (P3), com palavras novas:** distribuir não é defeito, e o par mostra isso: em 12 meses, receber todo
mês custou menos de 1 ponto. Para quem vive da renda, pode valer. O vídeo **não** diz "ETF de renda é ruim" e **não** repete
o frame "GOLPE?" de abril (`c9Obo6F5_NU`: 4.354 views e 17 inscritos, o pior da linha).

---

## 7. Validação de demanda

**GO.** Medida no próprio canal (C17 e C18), sem depender de outlier de concorrente:
- a linha de dividendos mensais converte 14,5 inscritos por mil views intencionais, contra 8,2 do resto (n = 6;
  `RELATORIO.md`, seção 2);
- `Fb0l4KEq27o` (ranking de ETFs, jan/2026) é o longo com mais inscritos do ano: 637, ou 19,7 por mil;
- o termo "etfs que pagam dividendos mensais" é o 11º termo de investimento dos últimos 6 meses (208 views da Pesquisa) e a
  família soma 4.558 no vitalício (`TERMOS.md`);
- **sinal contra:** o frame "GOLPE?" (`c9Obo6F5_NU`) teve 17 inscritos. O público da linha quer a renda; ataque ao produto
  não converte. A virada "parece que perdeu, mas não perdeu" conversa melhor com esse público do que a denúncia.

Concorrência (arquivo `…-concorrentes.md`): ranking, "vale a pena" de um ETF e lançamento com promessa de yield.
**Nenhum** dos resultados de 2025 a out/2026 fez o par distribuidor × acumulador.

---

## 8. Anti-repetição

| já feito ou pautado | data | risco | guardrail do Ep. 1 |
|---|---|---|---|
| "6 ETFs que MAIS PAGARAM DIVIDENDOS MENSAIS em 2025" (`Fb0l4KEq27o`) | 13/01/2026 | baixo | o Ep. 1 é a continuação ("quanto sobrou"), sem lista e sem contradizer. Card no bloco 4 e tela final |
| "ETF DIVIDENDOS MENSAIS são um GOLPE?" (`c9Obo6F5_NU`) | 08/04/2026 | médio | nada de "golpe", nada de dúvida moral; só a conta. O resultado do par até desmente a suspeita |
| "ETF JEPI39 PAGA DIVIDENDOS MENSAIS, mas vale a pena?" (`IB1mBcF00jc`) | 26/02/2026 | baixo | JEPI39 só na tabela 3.5 e no card do bloco A |
| "ETFs que pagam dividendos mensais: o que mudou em 2026" (era 06/10) | foi para a fila de dezembro (T09) | baixo | o par DIVD11 × DIVO11 continua do Ep. 1; o balanço de dezembro cita o Ep. 1 em vez de refazer o par |
| 27/10: "ETF de dividendos mensais ou FII: imposto e renda de cada um" | 13 dias depois | médio | **continua:** tabela 3.5 curta; o imposto detalhado de cada tipo (inclusive as duas leituras do BDR) é do 27/10 |
| 20/10 (opções) e 17/11 (taxa) | **saíram do calendário (T14)** e viraram os blocos A e B deste vídeo | — | os guardrails antigos caíram. No lugar: 20/10 TRXF11 e 17/11 "Fundos imobiliários para iniciantes", sem sobreposição |
| Short de 25/11 "Taxa de administração do ETF: quanto tira em 10 anos" | 25/11 | baixo | é o corte do bloco B (T17): usar C20; se citar ETF real, só a taxa máxima de 1,51% do SPYI11 (R11), sem juízo |

---

## Blocos absorvidos (decisão de 03/10)

**O que mudou** (`../CALENDARIO.md` e `../trocas.json`, troca T14, aprovada pelo Denis): o ETF de dividendos mensais estava
em 4 longos em 5 semanas. Os longos de **20/10 (opções)** e de **17/11 (taxa)** saíram e o conteúdo deles virou dois blocos
deste vídeo. No lugar entram o TRXF11 (20/10) e "Fundos imobiliários para iniciantes" (17/11). O 06/10 foi para a fila de
dezembro (T09). O 27/10 fica, com título novo.

| bloco | conteúdo | posição no vídeo | tempo | conferido |
|---|---|---|---|---|
| **A. Opções cobertas** (era o 20/10) | seção 3.4 | depois do bloco B | ~1:30 | C3, C9, R7, R8, R10, R11 |
| **B. Taxa** (era o 17/11) | seção 3.6 | logo depois do bloco 4 | ~1:00 | C20, R3, R11 |

Duração: **11 a 13 min**. O que encolhe primeiro está na seção 10.

---

## 9. Gancho (3 opções, voz do Denis)

Regras: "Fala, Tanaka." literal, número logo depois, stake em R$ dentro do gancho, a tese não se fecha no gancho, sem
meta-discurso. **Nenhum gancho deixa o R$ 9.260 sozinho.**

**Opção A (o gêmeo: parece, mas não é; recomendada):**
> "Fala, Tanaka. Dois ETFs, mesmo índice, mesmos doze meses na B3. A cota de um subiu 24%; a do outro, 15%. Em R$ 100 mil,
> parece que quem ficou com o segundo perdeu R$ 9.260. Só que o segundo pagou renda todo mês. Somando o que caiu na conta,
> ele perdeu R$ 740. E tem ETF que paga quase 1% ao mês e, na mesma conta, fica atrás do CDI."

Por que: dado da B3 nos primeiros 10 segundos (C1, C2), stake em R$, a virada (R$ 9.260 → R$ 740, R4) e o loop aberto para
o bloco A (o SPYI11, R7: 11,76% de renda no ano, cerca de 0,98% ao mês, e retorno total de 10,37%, abaixo do CDI de
14,47%). Não dizer "o dobro": 11,76% contra 8,52% é 1,4 vez.

**Opção B (a conta do zero; hipotética, escrever "exemplo" na tela):**
> "Fala, Tanaka. Um ETF que te paga 1% ao mês, com a cota caindo 1% ao mês, te pagou em um ano exatamente zero. R$ 100 mil
> viram R$ 88.638 de cota e R$ 11.362 de renda. O extrato te mostra a segunda linha. A primeira, você descobre quando
> vende."

Continua correta como exemplo (C19). Atenção: o caso real do par dá o resultado **oposto** (a renda voltou quase inteira).
Se usar a B, o bloco 3 precisa dizer isso de forma explícita ("no exemplo deu zero; na vida real, olha o que deu"), senão
o vídeo sugere que todo distribuidor devolve tudo. Risco: é hipotética, e o item 2 do portão quer número **ancorado**.

**Opção C (a régua, com o SPYI11):**
> "Fala, Tanaka. Um ETF pagou quase 1% ao mês, em reais, durante um ano inteiro. Somando a renda e a cota, rendeu 10,37%.
> O CDI do mesmo período: 14,47%. Em R$ 100 mil, R$ 4.100 a menos, e isso antes do imposto."

Conta (R7, C14): 14,47% − 10,37% = 4,10 pontos → R$ 4.100 (bruto com bruto). Por que não é a primeira: gasta o bloco A
no gancho, e o par (o achado exclusivo) vira coadjuvante.

---

## 10. Estrutura por blocos (11 a 13 min)

**Analogia (uma só, objeto físico, em camadas; o roteirista pode trocar, mas uma só):** a **caixa d'água com torneira**.
Camada 1: a renda é água saindo pela torneira da própria caixa. Camada 2: o cano que enche a caixa é o que a carteira gera.
Camada 3: o gêmeo é a mesma caixa, com o mesmo cano e sem torneira; **o nível parece mais baixo na caixa com torneira, mas
o balde embaixo dela está quase cheio** (a renda somada de volta). Camada 4: o imposto é um pingo na torneira, todo mês; no
gêmeo, ele sai de uma vez quando a caixa é esvaziada. Camada 5 (bloco B): a taxa é o furo no fundo da caixa, que sai todo
dia, haja renda ou não; no par, o furo é do mesmo tamanho. Bloco A: outra caixa, que recebe água de outro cano (o prêmio da
opção) e tem uma boia que não deixa o nível passar de um ponto (a alta limitada); a torneira jorra, e o nível não sobe. A
última camada mantém o sujeito da primeira (a caixa), como pede o 10b do juiz. **Nada de segunda analogia.**

| bloco | tempo | conteúdo | dado |
|---|---|---|---|
| **1. Gancho** | 0:00–0:30 | opção A | C1, C2, R4 |
| **2. A conta que o extrato não faz** | 0:30–1:45 | a fórmula do 3.1 e o exemplo de 100 → 92 + 12 = 4%; contra o IPCA, −0,21%. Camada 1 | C15, C19 |
| **3. O gêmeo, só a cota** | 1:45–3:30 | as duas cotas na tela (passo 1 da 3.3): mesmo índice (R1), mesma taxa (R3), 9,26 pontos de distância. **Sem a conclusão:** o Tanaka vê que a diferença tem o tamanho da renda antes de o Denis falar (prova no espectador). Camadas 2 e 3 | C1, C2, R1, R3 |
| **4. Somando de volta** | 3:30–6:00 | passo 2 da 3.3: 15,15% + 8,52% = 23,67% contra 24,41%. **R$ 9.260 vira R$ 740.** Depois o passo 3: o imposto na mesma régua (20,12% contra 20,75%): "vem todo mês em vez de vir no fim; em um ano quase empatou". A renda não é constante (R$ 0,03 a R$ 1,63). Camada 4. Card para `Fb0l4KEq27o` | R4, R5, R6, R9 |
| **B. A taxa** (seção 3.6) | 6:00–7:00 | **ponte nova** (abaixo). A conta de 10 anos (0,5% × 1,5%), a taxa máxima de 1,51% do SPYI11 e onde ler na lâmina. Camada 5 | C20, R3, R11 |
| **A. Opções cobertas** (seção 3.4) | 7:00–8:45 | a mecânica corrigida (o ETF americano vende as opções), o extrato de três linhas do SPYI11 (10,37% contra 14,47% do CDI), o câmbio em uma frase, a régua do ETHY11 (opcional). Card para `IB1mBcF00jc` | C3, C9, R7, R8, R10 |
| **6. Três coisas que pagam todo mês** | 8:45–9:30 | tabela 3.5: ETF da B3 (15% na fonte), BDR (não é isento; informe), FII (isento com 100 cotistas). "O detalhe do imposto sai no dia 27" | C11, C12, R5, R6, R12, R13 |
| **7. Objeções** | 9:30–11:00 | seção 11 (escolher 4 a 6) | — |
| **8. Fechamento** | 11:00–11:45 | a ferramenta batizada (seção 12) e a tela final para `Fb0l4KEq27o` | — |

**Ponte do bloco 4 para o B (nova; a antiga dizia que a taxa explicava a diferença, e isso está errado):**
> "Esses R$ 740 não vieram da taxa: nas duas lâminas, ela é a mesma, 0,50% ao ano. Entre gêmeos, a taxa empata. Entre ETFs
> diferentes, não, e lá na caixa d'água ela é o furo que vaza todo dia, com renda ou sem renda."

(Carrega o objeto do bloco 4, os R$ 740, e não anuncia o vídeo; passa no eliminatório de costura A.)

**Ponte do B para o A:** a taxa máxima de 1,51% é do SPYI11, o ETF que paga quase 1% ao mês: "e esse de 1,51% é justamente
o que mais paga renda dos que a gente viu. De onde vem tanta água?"

**Duração-alvo: 11 a 13 min (este desenho dá cerca de 11:45).** Se passar de 13, encolher **nesta ordem**:
1. **bloco 6** (tabela 3.5) vira uma frase e a tabela fica só na tela (o imposto detalhado é do 27/10);
2. a **régua extrema do ETHY11** sai do bloco A;
3. as **objeções** caem para 4 (ficam "a cota volta", "só quero a renda", "e o imposto?" e "1,5% de taxa é alto?");
4. o exemplo hipotético do bloco 2 encurta para a fórmula com uma linha de números.

**Nunca cortar:** os blocos 3 e 4 (a virada de R$ 9.260 para R$ 740), o extrato do SPYI11 no bloco A e o fechamento.

---

## 11. Objeções (e a resposta em uma frase)

| objeção | resposta |
|---|---|
| "Mas a cota volta." | Pode voltar. A conta é de um período; refaça em 2 ou 3 janelas diferentes (12, 24 e 36 meses, quando o ETF tiver idade para isso). |
| "Eu só quero a renda, não ligo para a cota." | A mesma porcentagem sobre uma cota menor é uma renda menor no ano seguinte. A cota é a renda do ano que vem. |
| "Então é melhor o que não distribui?" | Em 12 meses, a diferença foi de menos de 1 ponto (R$ 740 em R$ 100 mil). Quem precisa da renda todo mês paga um preço pequeno para recebê-la; a conta mostra o tamanho. Sem ticker indicado. |
| "E o imposto?" | No ETF da B3, 15% retidos na fonte em cada pagamento (R5); no que reinveste, 15% só quando vende (R6). Em um ano, quase empatou. BDR: não é isento; siga o informe. FII: isento com 100 cotistas ou mais. |
| "Paga todo mês o mesmo valor?" | Não. O DIVD11 pagou de R$ 0,03 a R$ 1,63 por cota no ano; janeiro foi um terço do total (R4). |
| "Essa taxa de 1,5% é alta?" | Em 10 anos, 1,5% ao ano tira cerca de 14% do patrimônio, contra cerca de 4,9% de uma taxa de 0,5% (C20). Procure a taxa total máxima na lâmina. Sem dizer qual ETF escolher. |
| "O de opções paga 1% todo mês, garantido?" | Não há garantia: o prêmio muda com o mercado. Nos 12 meses, pagou quase 1% ao mês, e o total ficou abaixo do CDI (R7). |
| "O yield alto não compensa?" | Yield é rendimento ÷ cota. Se a cota cai, o yield sobe sozinho; ETHY11: −35,95% na cota desde a estreia (C9). |
| "O JEPQ39 não paga mais que o JEPI39?" | Na B3, o JEPQ39 não negociou nenhuma vez até 01/10/2026 (C12; reconferir na semana, item 17). |

---

## 12. Fechamento e Shorts

**Ferramenta batizada (fecho, nunca recap):** **"o extrato de três linhas"**. Antes de olhar o yield de qualquer ETF que
paga todo mês, escreva:
1. **quanto pagou** (soma dos rendimentos, bruto e líquido);
2. **quanto a cota andou** (fim ÷ começo − 1);
3. **quanto ficou acima do CDI e do IPCA** (linha 1 + linha 2, contra a régua do mesmo período).

Callback do gancho, uma frase: "olhando só a linha 2, o gêmeo perdeu R$ 9 mil; com as três, perdeu R$ 740. E o que paga
quase 1% ao mês, com as três, ficou atrás do CDI." Na tela, a planilha de 4 colunas (data, cota, rendimento, acumulado),
com o caminho para baixar cotas (séries históricas da B3) e rendimentos (avisos de proventos no fnet).

**Short derivado (pré-estreia, quarta 07/10, 40 s):**
- Título: "Recebeu 1% ao mês e a cota caiu 1% ao mês: quanto você ganhou?"
- 0–5 s: a pergunta, com R$ 100 mil na tela.
- 5–25 s: 12 meses em 4 quadros: a renda somando (R$ 11.362) e a cota descendo (R$ 88.638).
- 25–35 s: soma = R$ 100.000. "Zero. E o extrato só te mostrou o verde." (escrever "exemplo hipotético" na tela)
- 35–40 s: "Na vida real, nem sempre dá zero. O vídeo da conta com dois ETFs de verdade sai na quarta, dia 14." Link para
  `Fb0l4KEq27o` até 14/10; depois, trocar para o Ep. 1.
- Conta conferida (C19): 100.000 × (1 − 0,99¹²) = 11.362; 100.000 × 0,99¹² = 88.638.

**Short de corte do bloco B (quarta 25/11, T17):** "Taxa de administração do ETF: quanto tira em 10 anos".
- A tabela da 3.6: R$ 100 mil, 10 anos, 0,5% contra 1,5% ao ano: R$ 4.889 contra R$ 14.027 (C20). "Exemplo" na tela.
- Fecho: "procure a taxa total máxima na lâmina". Se citar ETF real, só "1,51% de taxa máxima, contando a do fundo lá fora"
  (R11), sem dizer se é cara.
- Link para o Ep. 1.

---

## 13. Veredito e ajustes de roteiro

**GO, COM AJUSTES.** A conta central (itens 1, 2 e 10) e o bloco A (itens 11, 21, 22 e 23) fecharam em fonte primária.
Nada pendente bloqueia a gravação. As validações V1 a V4 do Denis entram na leitura final do roteiro.

**Ajustes obrigatórios no roteiro (vêm da conferência):**
1. **Gancho, thumbnail e Short:** o "R$ 9.260" nunca aparece sem o "somando a renda, R$ 740". Thumbnail sugerida (o
   empacotador decide): "PERDEU R$ 9 MIL?" com "R$ 740" ao lado, e não "RENDA OU DEVOLUÇÃO?".
2. **Imposto:** "vem todo mês, em vez de vir no fim; em um ano quase empatou" (20,12% contra 20,75%). Proibido "o que custa
   é o imposto mensal".
3. **Os 0,74 ponto:** "menos de 1 ponto". Não atribuir à taxa (é igual) nem a outra causa.
4. **Ponte 4 → B:** a nova, da seção 10. A taxa vira lição geral.
5. **Bloco A:** quem vende as opções é o ETF americano (95% ou mais da carteira); o crédito é em reais; total de 10,37%
   bruto contra CDI de 14,47%.
6. **BDR:** "não é isento; siga o informe da instituição depositária". Nenhuma alíquota, nem "carnê-leão", nem "15%" para o
   dividendo.
7. **IR do ETF:** "15% retido na fonte", sem dizer quem retém.
8. **ETHY11:** só a cota (C9), sem a "promessa de 30%", enquanto o item 15 não for conferido.

**Alertas que continuam:**
- **Título e thumbnail são afirmações factuais** (`feedback_factcheck_titulo_e_qualificadores`). "A renda saiu da cota?"
  é pergunta; a resposta honesta é "saiu, e voltou quase inteira".
- **Cada fato uma vez.** O par aparece no gancho, é desenvolvido nos blocos 3 e 4 e volta só como callback no fechamento.
- **Sem "vale a pena", "melhor", "eu faria".** O gêmeo é grupo de controle; o SPYI11 é caso de estudo.
- **Sem marca de gestora e sem corretora:** DIVD11, DIVO11, NDIV11, SPYI11 e JEPI39 só pelo código; o ETF americano, só
  "o SPYI".
- **Os blocos A e B não pedem segunda analogia** nem ponte que anuncia ("agora vamos falar de taxa").
- **Não puxar texto de imposto do blog** (posts 3172, 4537, 4544 e 4816; correções sugeridas na conferência, seção 6).

---

## 14. Fontes

Primárias:
- B3, séries históricas COTAHIST A2024, A2025 e A2026: https://bvmf.bmfbovespa.com.br/InstDados/SerHist/ (cópias em
  `site-ativos/cache/raw/b3/`, baixadas em 02/10/2026; A2026 com last_modified de 01/10/2026 23:26 GMT).
- BCB, SGS 12, 13522 e 432 (cópias em `site-ativos/cache/raw/bcb/` e `investir-e-cocar/pipeline/dados/macro_bcb.json`,
  baixadas em 02/10/2026); BCB Olinda/PTAX (conferência).
- fnet: avisos de proventos do DIVD11 e do SPYI11; regulamentos do DIVD11 (id 939399), do DIVO11 (id 932100) e do SPYI11
  (id 647768) (conferência, tabelas 2.1 e 2.3).
- Lâminas de 31/08/2026 do DIVD11 e do DIVO11 (conferência, item 9).
- Lei 14.754/2023, Lei 13.043/2014, Lei 11.033/2004 (planalto); IN RFB 1.585/2015 (Receita); P&R IRPF 2026 (Receita)
  (conferência, itens 1 a 7).
- YouTube Analytics do canal (`auditoria-canal/dados/`, exportação de 02/10/2026).

Relatório de conferência: `2026-10-14-CONFERENCIA.md` (Mac, 03/10/2026). Secundárias (só busca, não sustentam número): ver
o arquivo de concorrentes.

*Briefing de 03/10/2026, revisto no mesmo dia com a conferência na fonte primária. Pesquisa de concorrentes feita antes ✅;
preços, régua, renda e imposto do ETF em fonte primária ✅; BDR sem alíquota (não existe regra explícita) ✅; demanda medida
no canal ✅; anti-repetição reconciliada com o calendário v3 ✅. Veredito: **GO, com os 8 ajustes da seção 13.***
