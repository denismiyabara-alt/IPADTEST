---
tema: "Todo ETF que paga renda paga com a própria cota. Pelo gráfico da cota, o gêmeo que distribui ficou R$ 9.260 atrás em R$ 100 mil; com a conta inteira (cota + renda), R$ 740. E o que paga quase 1% ao mês, com a mesma conta, ficou R$ 4.100 atrás do CDI."
serie: Série Renda Mensal, Ep. 1 de 6
formato: long (teleprompter)
data_publicacao: 2026-10-14 (quarta, 19h)
data_roteiro: 2026-10-03
versao: v2 (v1 reescrita no esqueleto de roteiro-regras/, commit 795bc06)
duracao_estimada: "~13:15 (cerca de 1.990 palavras faladas a 150 por minuto, números por extenso contados como palavra, mais a pausa de 2 s; teto 14:00)"
status: "RASCUNHO v2. Notas dos juízes no fim (aplicadas pelo próprio roteirista, NÃO independentes). Falta: juiz-roteiro, juiz-ritmo e ouvinte-frio independentes; score_roteiro.py e fala_so.py (Mac); leitura do Denis"
briefing: pautas-canal/briefings/2026-10-14-etf-dividendos-mensais-briefing.md (GO, com ajustes)
conferencia: pautas-canal/briefings/2026-10-14-CONFERENCIA.md
concorrentes: pautas-canal/briefings/2026-10-14-etf-dividendos-mensais-concorrentes.md
card_social: esteira-social/cards/2026-10-14-etf-que-paga-dividendos-mensais-a-renda-saiu-da.md (mecânica extrato-falso, a mesma do bloco 3)
frame: REVELAÇÃO + MÉTODO. Os tickers são prova da conta, nunca escolha. Nada de "qual é melhor", nada de "vale a pena", nenhuma corretora, nenhuma marca de gestora
esqueleto: "PROMESSA (bloco 0) → PERGUNTA (bloco 0) → bloco 1 abre com a moral → um ponto por bloco → CONCLUSÃO (o número da promessa volta e a ferramenta fecha, com o Tanaka de sujeito, na imagem da caixa e do balde)"
analogia_unica: "a caixa d'água e o balde (bloco 1: você abre a torneira da sua caixa e enche o balde · bloco 2: a caixa sem torneira · bloco 3: o balde quase cheio · bloco 4→5: o furo da taxa, na ponte · bloco 6: a caixa com boia · fecho: você põe o balde de volta na caixa)"
mecanicas_de_piada: "1 do catálogo: Extrato Falso (bloco 3). O resto são beats de um toque"
loop_abre: "BLOCO 0: R$ 4.100 atrás do CDI em R$ 100 mil, de um ETF que paga quase 1% ao mês"
loop_fecha: "BLOCO 6 (o extrato do SPYI11) e FECHO (callback curto)"
pronuncia: "DIVD11 = 'DIVD onze', DIVO11 = 'DIVO onze', SPYI11 = 'SPYI onze', JEPI39 = 'JEPI trinta e nove' (o Denis confirma)"
orcamento_numeros: "datas-base: 1 (a mesma janela de 12 meses, 01/10/2025 → 01/10/2026, para todo número real) + exemplos hipotéticos marcados com 'se' (bloco 1 e bloco 5). Números novos falados por bloco: B0 5 · B1 4 · B2 5 · B3 5 · B4 4 · B5 6 · B6 5 · B7 3 · B8 2 · FECHO 0. Frases com 3+ números: 0. O resto vai pra [TELA]"
conflitos_registrados:
  - "CONFLITO briefing × roteirista-tanaka (gancho promete, não revela): o briefing (ajuste 1) manda o R$ 9.260 nunca aparecer sem o R$ 740. Os dois números ficam no bloco 0, mas o mecanismo (a renda somada de volta) só aparece no bloco 3: o gancho diz 'pelo gráfico' e 'pela conta inteira', sem dizer o que a conta inteira soma."
  - "CONFLITO briefing × roteirista-tanaka (fecho): o briefing batiza a ferramenta como 'o extrato de três linhas' (checklist). As regras de 01-02/10 proíbem checklist, quiz e 'eu chamo isso de'. A ferramenta virou uma conta só, com o nome dentro da frase: 'a conta do balde na caixa'."
  - "CONFLITO roteirista-tanaka (bloco 'comprar, vender ou ficar' em vídeo de ativo com nome) × pedido e briefing (os ETFs são prova da conta, nunca recomendação): o bloco não entra; no lugar, a concessão do bloco 3 e a objeção 'então o certo é o que não distribui?'. O Denis decide."
  - "CONFLITO roteirista-tanaka (máximo de 2 fontes no vídeo) × briefing (B3, fnet, BCB, lâminas, regulamentos e leis): lido como 'datas-base'; todo número real é da mesma janela de 12 meses."
  - "Pesquisa de comentários: o arquivo de concorrentes não agrupa dúvidas de comentário. A única dúvida de público registrada sobre o tema ('essa taxa de 1,50 do S&P 500 é bem alta?', PERGUNTAS-SEM-RESPOSTA.md item 15) é respondida no bloco 5, como objeção na voz do Denis."

titulo_escolhido: "ETFs que pagam dividendos mensais: a renda saiu da cota?"
titulo_alternativas:
  - "Pelo gráfico, perdeu R$ 9 mil. Na conta inteira, R$ 740"
  - "O ETF que pagou quase 1% ao mês e perdeu do CDI"
titulos_descartados:
  - "Vale a pena ETF que paga dividendo todo mês?"   # gate RECOMENDACAO_TITULO
  - "DIVO11 ou DIVD11: qual é melhor?"                # vira comparação de compra; o par é grupo de controle
  - "Perdeu R$ 9.260 com ETF de dividendos"           # o R$ 9.260 nunca sai sem o R$ 740 (ajuste 1 do briefing)
thumbnail_texto: "PERDEU R$ 9 MIL? (riscado em vermelho) e, ao lado, R$ 740"
thumbnail_conceito: "Denis agachado ao lado de um balde quase cheio embaixo de uma torneira de caixa d'água, olhando pra câmera com a sobrancelha levantada, no meio do gesto de apontar pro balde. Fundo creme do molde Burry (#f6f2e8); vermelho #d6362b só no texto. Nenhum código de ETF na thumbnail. O R$ fica na thumb; o título escolhido não tem R$."
thumbnail_prompt: "Denis crouching next to a nearly full metal bucket under the tap of a rooftop water tank, pointing at the bucket and looking at the camera with one eyebrow raised, mid-gesture, warm afternoon light, clean cream background (#f6f2e8), editorial photography, shallow depth of field, no text, 1280x720"

gancho_escolhido: "A do briefing (o gêmeo), reescrito no esqueleto promessa → pergunta"
cumpre_nos_15s: "Fala, Tanaka. Cem mil reais em cada um de dois ETFs da B3 que seguem o mesmo índice, nos mesmos doze meses. Pelo gráfico da cota, o que paga renda todo mês ficou nove mil, duzentos e sessenta reais atrás do outro. Pela conta inteira, ficou setecentos e quarenta."

hook_trecho: "Pelo gráfico da cota, o que paga renda todo mês ficou nove mil, duzentos e sessenta reais atrás do outro."
stake_trecho: "Pela conta inteira, ficou setecentos e quarenta."
pergunta_trecho: "o ETF que paga todo mês está te pagando, ou está te devolvendo o seu próprio dinheiro?"
loop_trecho: "Nos mesmos cem mil reais, ele ficou quatro mil e cem reais atrás do CDI."
moral_trecho: "Todo ETF que paga renda paga com a própria cota, e isso não é golpe nem defeito."
agregado_para_linha_trecho: "Dos nove vírgula dois seis pontos que pareciam perdidos, quase tudo estava no balde."
prova_no_espectador_trecho: "Pensa dois segundos antes de eu falar, Tanaka: pra onde foi essa água?"
cena_de_vergonha_trecho: "Você já deu print nesse verdinho e mandou no grupo da família."
analogia_camada1_trecho: "Pensa que você tem uma caixa d'água com uma torneira embaixo."
analogia_camada3_trecho: "O nível da caixa com torneira parecia bem mais baixo. Só que o balde embaixo dela estava quase cheio."
analogia_ultima_trecho: "você põe o balde de volta na caixa"
concessao_trecho: "Pra quem vive dessa renda, esse preço pode fazer todo o sentido."
alvo_poderoso_trecho: "O aplicativo te mostra o balde enchendo, mês a mês, em verde."
objecao_trecho: "Aí você deve estar pensando: \"mas a cota volta\"."
ferramenta_trecho: "faz a conta do balde na caixa"
---

# ETFs que pagam dividendos mensais: a renda saiu da cota?

> Janela de todo número real: fechamento de 01/10/2025 → 01/10/2026 (B3, COTAHIST); renda com data-base no mesmo período
> (fnet); CDI acumulado no período (BCB, SGS 12); IPCA de 12 meses até ago/2026 (BCB, SGS 13522). **Se gravar depois de
> 09/10, trocar só o IPCA** (o 4,22% do bloco 1); o resto fica.
> Convenção de arredondamento do briefing (seção 1): todo R$ sobre R$ 100 mil sai das porcentagens com 2 casas.
> Teto: 14 min. O que encolhe primeiro: bloco 7 vira uma frase e a tabela fica só na tela; depois a objeção do yield
> (bloco 8); depois o exemplo do bloco 1.

**Ganchos alternativos (o briefing, seção 9, traz três; o A é o escolhido):**

- **B, a conta do zero (hipotético; "EXEMPLO" na tela).** "Fala, Tanaka. Se um ETF te pagasse um por cento ao mês e a
  cota caísse um por cento ao mês, em um ano você teria ganhado exatamente zero. O aplicativo te mostraria onze mil,
  trezentos e sessenta e dois reais de renda em cem mil. A cota, você só ia ver quando vendesse." *Se usar o B, o bloco 2
  tem de dizer que na vida real o resultado foi outro, senão o vídeo sugere que todo distribuidor devolve tudo. É a
  abertura do Short de 07/10.*
- **C, o SPYI11 primeiro.** "Fala, Tanaka. Um ETF pagou quase um por cento ao mês, em reais, durante um ano inteiro. Em
  cem mil reais, ele ficou quatro mil e cem atrás do CDI do mesmo ano, e isso antes do imposto." *Gasta o bloco 6 no
  gancho e o par vira coadjuvante; fica de reserva para o teste A/B do Short.*

---

## BLOCO 0 - PROMESSA E PERGUNTA (0:00–0:40)

Fala, Tanaka. Cem mil reais em cada um de dois ETFs da B3 que seguem o mesmo índice, nos mesmos doze meses.

Pelo gráfico da cota, o que paga renda todo mês ficou nove mil, duzentos e sessenta reais atrás do outro.

Pela conta inteira, ficou setecentos e quarenta.

[TELA: duas barras sem nome, "o que reinveste" e "o que paga todo mês"; embaixo, "R$ 9.260" aparece, risca em vermelho, e
"R$ 740" pousa ao lado (um som, só no pouso). Peça `barras` da biblioteca, rótulos sem ticker. Fonte: B3 (COTAHIST) e fnet]

Os mesmos dois fundos, o mesmo ano, e dois números que não moram nem no mesmo bairro.

E tem um terceiro ETF, que paga quase um por cento ao mês. Nos mesmos cem mil reais, ele ficou quatro mil e cem reais atrás do CDI, a taxa de referência dos CDBs.

E a conta inteira cabe numa folha, com o ETF que estiver aí na sua carteira.

Antes dela, o seu palpite: o ETF que paga todo mês está te pagando, ou está te devolvendo o seu próprio dinheiro? Escreve aí embaixo.

> ⛔ Nada de insert, meme ou cartela nova entre 0:08 e 0:20: é onde o R$ 9.260 vira R$ 740.

---

## BLOCO 1 - A CAIXA E O BALDE (0:40–1:50)

Todo ETF que paga renda paga com a própria cota, e isso não é golpe nem defeito.

Pensa que você tem uma caixa d'água com uma torneira embaixo. Todo mês você abre a torneira e enche um balde. Só que a água do balde saiu da caixa, e o nível da caixa baixou.

O ETF que paga renda é essa caixa. A cota é o nível da caixa. A renda é o balde.

O aplicativo te mostra o balde enchendo, mês a mês, em verde. Você já deu print nesse verdinho e mandou no grupo da família. Eu também, Tanaka.

Se um ETF pagasse doze por cento de renda num ano, o balde estaria lindo. Se, no mesmo ano, a cota desse ETF caísse oito por cento, o ganho de verdade seria de quatro por cento.

[TELA: EXEMPLO HIPOTÉTICO · cota R$ 100 → R$ 92 (−8%) · renda R$ 12 (+12%) · (92 − 100 + 12) ÷ 100 = 4% em 12 meses]

E a inflação oficial, o IPCA, nos doze meses até agosto, foi de quatro vírgula dois dois por cento. Com o ganho de quatro e a inflação de quatro e pouco, o exemplo andou pra trás.

[TELA: EXEMPLO HIPOTÉTICO · IPCA de 12 meses até ago/2026: 4,22% (BCB, SGS 13522) · retorno real: 1,04 ÷ 1,0422 − 1 = −0,21%]

[TELA: retorno total = (cota no fim − cota no começo + rendimentos) ÷ cota no começo]

No exemplo, a renda era a própria cota voltando pro bolso. Pra saber se na vida real também é assim, precisava de duas caixas iguais: uma com torneira e outra sem.

---

## BLOCO 2 - AS DUAS CAIXAS (1:50–3:10)

E a B3 tem essas duas caixas: o DIVD onze e o DIVO onze.

Os dois seguem o IDIV, uma cesta de empresas da B3 que pagam bastante dividendo.

O DIVD onze tem torneira: repassa o dividendo pra você todo mês. O DIVO onze não tem torneira: o dividendo fica lá dentro e é reinvestido.

Gêmeos de novela, Tanaka. Mesma cara, e o público jura que um deles é o vilão.

[TELA: os dois regulamentos lado a lado, a definição de "Índice" grifada em cada um (fnet, ids 939399 e 932100). Embaixo:
"Não é recomendação de investimento."]

Nos doze meses até primeiro de outubro, a cota do DIVO onze, o que reinveste, subiu vinte e quatro vírgula quatro um por cento.

No mesmo período, a cota do DIVD onze, o que paga todo mês, subiu quinze vírgula um cinco.

[TELA: `grafico_cotacao`, dois gráficos em sequência, 6 s cada: `serie.py b3 DIVO11 --desde 2025-10-01 --aviso` (R$ 106,82 →
R$ 132,90, +24,41%) e `serie.py b3 DIVD11 --desde 2025-10-01 --aviso` (R$ 55,86 → R$ 64,32, +15,15%). Fonte: B3 (COTAHIST,
fechamento sem ajuste). Na tela: "Não é recomendação de investimento."]

Do DIVO onze pro DIVD onze, a distância na cota é de nove vírgula dois seis pontos. Nos cem mil reais do começo, são os nove mil, duzentos e sessenta.

Duas caixas com o mesmo cano enchendo, e a que tem torneira está nove pontos mais baixa.

Pensa dois segundos antes de eu falar, Tanaka: pra onde foi essa água?

[PAUSA: 2 s, olhando pra câmera. Sem B-roll]

Isso. Você chegou antes de mim. Está no balde. E quanta água caiu no balde é justamente a conta que o aplicativo não faz.

> [CORTE SHORT 1 — de "Do DIVO onze pro DIVD onze, a distância na cota" até "são os setecentos e quarenta do começo" (bloco 3), ~60 s.
> Título provisório: "Pelo gráfico, perdeu R$ 9 mil. Na conta inteira, R$ 740". O R$ 9.260 nunca sai sem o R$ 740 no mesmo
> corte. "Não é recomendação de investimento." na tela.]

---

## BLOCO 3 - O BALDE (3:10–5:00)

O balde do DIVD onze está escrito, aviso por aviso, no fnet, o site da B3 onde os fundos publicam cada pagamento.

Lido no tom do aplicativo, o extrato do ano fica assim.

Rendimento: três centavos por cota. Três centavos, Tanaka. Nem a bala do troco da padaria.

Rendimento: um real e sessenta e três. Esse veio de terno e gravata.

E por aí vai, um aviso por mês. Linha da cota: não consta.

[TELA: extrato falso, fonte de aplicativo, as 12 linhas rolando: R$ 0,3020 · R$ 0,0336 · R$ 0,4254 · R$ 1,6290 · R$ 0,1276 ·
R$ 0,2981 · R$ 0,2062 · R$ 0,3013 · R$ 0,1166 · R$ 0,3738 · R$ 0,1495 · R$ 0,7983 · soma: R$ 4,7614 por cota = 8,52% da cota de
R$ 55,86. Fonte: fnet, avisos de proventos do DIVD11 (data-base de 06/10/2025 a 04/09/2026). No fim: "Linha da cota: não consta."]

Somando os doze avisos, o balde do DIVD onze dá pra medir em porcentagem da cota do começo.

Agora você põe o balde de volta na caixa. A cota do DIVD onze subiu quinze vírgula um cinco por cento, e o balde soma mais oito vírgula cinco dois.

Somando a cota e o balde, o DIVD onze rendeu vinte e três vírgula seis sete por cento. O DIVO onze, sem balde nenhum, rendeu os mesmos vinte e quatro vírgula quatro um de antes.

[TELA: peça `barras`, 2º momento "cota + balde": DIVD11 vai de 15,15% para 23,67% (15,15 + 8,52); DIVO11 fica em 24,41%.
Fonte: B3 (COTAHIST) e fnet. `"ativos": true`, critério "Critério: os dois ETFs da B3 que seguem o IDIV, um distribui e o
outro reinveste" → "Não é recomendação de investimento." na tela]

Dos nove vírgula dois seis pontos que pareciam perdidos, quase tudo estava no balde.

A diferença de verdade, do DIVO onze pro DIVD onze, é de zero vírgula sete quatro ponto. Nos cem mil reais, são os setecentos e quarenta do começo.

[TELA: R$ 100 mil · DIVD11: R$ 115.150 de cota + R$ 8.520 de renda = R$ 123.670 · DIVO11: R$ 124.410 · diferença: R$ 740]

O nível da caixa com torneira parecia bem mais baixo. Só que o balde embaixo dela estava quase cheio.

E as duas caixas passaram com folga do CDI do mesmo período. A conta não acusou ninguém, viu?

Em doze meses, receber todo mês custou menos de um ponto. Pra quem vive dessa renda, esse preço pode fazer todo o sentido. A conta mostra o tamanho do preço; quem decide se paga é você.

[CARD: Fb0l4KEq27o, "6 ETFs que mais pagaram dividendos mensais em 2025"]

Só que esse balde ainda não passou pelo imposto.

---

## BLOCO 4 - O IMPOSTO (5:00–6:00)

E o imposto do DIVD onze sai do balde todo mês: quinze por cento retidos na fonte, em cada pagamento.

O imposto do DIVO onze sai da caixa uma vez só, quando você vende a cota: os mesmos quinze por cento, cobrados no lucro da venda.

E na venda de ETF não tem aquela isenção das ações, de quem vende até vinte mil reais no mês.

Comparar o DIVD onze, que já pagou o imposto, com o DIVO onze, que ainda nem foi cobrado, é covardia.

Com os dois vendidos no mesmo dia, primeiro de outubro, o DIVD onze fica com vinte vírgula um dois por cento. O DIVO onze fica com vinte vírgula sete cinco.

[TELA: depois do IR, os dois vendidos em 01/10/2026 · DIVO11: 24,41% × 0,85 = 20,75% · DIVD11: 15,15% × 0,85 + 7,25% = 20,12%
(a renda de 8,52%, menos 15% retidos na fonte, vira 7,25%). Fonte: Lei 14.754/2023, art. 24 (15% retidos na distribuição);
IN RFB 1.585/2015, arts. 57 e 59 (15% na venda, sem a isenção de R$ 20 mil)]

Um imposto vem todo mês e o outro vem no fim. Em um ano, os dois quase empataram.

E os setecentos e quarenta também não vieram da taxa. Nas duas lâminas, que é o resumo que todo fundo publica, a taxa total é a mesma: zero vírgula cinco por cento ao ano.

[TELA: as duas lâminas de 31/08/2026, "Taxa Total Máxima: 0,50% a.a." grifada nas duas]

Entre gêmeos, a taxa empata. Entre ETFs diferentes, ela é um furo no fundo da caixa, e furo pequeno, em dez anos, faz poça grande.

---

## BLOCO 5 - O FURO (6:00–7:10)

O tamanho da poça sai de uma conta só da taxa, sem rendimento nenhum: cem mil reais parados por dez anos.

Se a taxa for de zero vírgula cinco por cento ao ano, ela leva uns quatro mil e novecentos reais.

Se a taxa for de um e meio por cento ao ano, ela leva uns catorze mil.

[TELA: EXEMPLO · só a taxa, sem rendimento · R$ 100 mil por 10 anos · 0,5% a.a.: 0,995¹⁰ = 95,11% → a taxa tirou 4,89% =
R$ 4.889 · 1,5% a.a.: 0,985¹⁰ = 85,97% → tirou 14,03% = R$ 14.027 · conta própria]

E a taxa não tira férias, Tanaka. O imposto só cobra quando tem renda. A taxa cobra em mês bom e em mês ruim.

Aí você deve estar pensando: "um e meio de taxa num ETF de S&P 500 é alto, né?".

Esse um e meio existe na B3: é a taxa máxima do SPYI onze, um vírgula cinco um por cento ao ano, já somando a taxa do fundo americano em que ele investe. Se é alto pra você, a conta dos dez anos mostra o tamanho do furo.

[TELA: regulamento do SPYI11 (fnet id 647768), Anexo, item 7.1.2, "Taxa Máxima: 1,51% ao ano" grifada]

Onde achar: na lâmina, procura a taxa total máxima. Se o ETF compra fundo lá fora, confere no regulamento se ela já soma a do fundo de fora, tá bom?

E o SPYI onze, o da taxa de um e meio, é justamente o que mais pagou renda de todos que apareceram aqui. De onde vem tanta água?

> [CORTE SHORT 3 — o bloco 5 de "O tamanho da poça" até "a conta dos dez anos mostra o tamanho do furo" (~50 s) é o Short de 25/11,
> "Taxa de administração do ETF: quanto tira em 10 anos" (T17). Abre com uma frase nova: "Cem mil reais parados dez anos num
> ETF." "EXEMPLO" na tela; o SPYI11 só com a taxa máxima de 1,51%, sem juízo.]

---

## BLOCO 6 - A CAIXA COM BOIA (7:10–9:00)

Vem de outro cano.

O SPYI onze põe noventa e cinco por cento ou mais do dinheiro num ETF americano, o SPYI. É o fundo de lá que tem as ações do S&P 500, as maiores da bolsa americana, e todo mês vende opções de compra.

Traduzindo: o fundo de lá vende pra alguém o direito de comprar aquelas ações por um preço acima do de hoje. Quem compra o direito paga na hora, vrau, e esse valor se chama prêmio. O prêmio é a renda.

O preço dessa renda: se as ações subirem além daquele ponto, a alta fica com quem comprou o direito. Se a carteira cair, a queda vem inteirinha. É a única parte do pacote que vem sem limite.

[TELA: três palavras, uma por vez: RENDA ALTA · ALTA LIMITADA · QUEDA INTEIRA. Fonte: regulamento do SPYI11 (fnet id 647768),
Anexo, itens 5.1 e 6.1.1]

Na caixa d'água, é uma caixa enchida pelo cano do prêmio, com uma boia que não deixa o nível passar de certo ponto. A torneira jorra, e o nível não sobe.

O fundo brasileiro, aliás, não vende opção nenhuma. O regulamento só deixa ele usar esse tipo de contrato pra se proteger. Quem vende é o fundo de lá.

A conta inteira do SPYI onze, nos mesmos doze meses.

O balde: em doze pagamentos, em reais, ele recebeu onze vírgula sete seis por cento da cota do começo. Quase um por cento ao mês.

A caixa: a cota caiu um vírgula três nove por cento.

Somando a cota e o balde, o SPYI onze rendeu dez vírgula três sete por cento no ano.

E o CDI, nos mesmos doze meses, rendeu catorze vírgula quatro sete.

Do CDI pro SPYI onze, nos cem mil reais do começo, são os quatro mil e cem de distância. E essa distância ainda é antes do imposto.

[TELA: o SPYI11, 01/10/2025 → 01/10/2026 · balde: R$ 13,0763 por cota em 12 eventos ÷ R$ 111,15 = 11,76% · cota: R$ 111,15 →
R$ 109,60 = −1,39% · total: 11,76 − 1,39 = 10,37% (líquido de 15%: 8,61%) · CDI acumulado de 02/10/2025 a 01/10/2026: 14,47%
· distância: 14,47 − 10,37 = 4,10 pontos = R$ 4.100 em R$ 100 mil. Fonte: fnet (avisos do SPYI11), B3 (COTAHIST), BCB (SGS 12).
"Não é recomendação de investimento."]

E teve o dólar, que caiu no período. Sem o efeito do dólar, a cota ficou praticamente parada.

[TELA: `grafico_cotacao`, `serie.py b3 SPYI11 --desde 2025-10-01 --comparador CDI` (cota parada × CDI subindo). Fonte: B3
(COTAHIST) · CDI: BCB (SGS 12). Legenda: "PTAX: R$ 5,3208 → R$ 5,2079 (−2,12%), BCB"]

Não é ranking de ETF. No DIVD onze, a água vem do dividendo das empresas; no SPYI onze, principalmente do prêmio. O regulamento diz qual cano enche qual caixa.

E quase um por cento ao mês não é promessa: o prêmio muda com o mercado, e a renda muda junto.

[CARD: IB1mBcF00jc, JEPI39, a mesma família de estratégia, em BDR]

E o JEPI trinta e nove, que é dessa mesma família, chega à B3 por outro caminho. Ele é BDR, e BDR paga imposto de outro jeito.

> [CORTE SHORT 2 — de "A conta inteira do SPYI onze" até "E essa distância ainda é antes do imposto" (~45 s), abrindo
> com uma frase nova: "Um ETF pagou quase um por cento ao mês, em reais, durante um ano." Título provisório: "O ETF que pagou
> quase 1% ao mês e perdeu do CDI". "Não é recomendação de investimento." na tela.]

---

## BLOCO 7 - TRÊS COISAS QUE PAGAM TODO MÊS (9:00–9:40)

BDR, Tanaka, é um recibo negociado aqui de um ativo que está lá fora.

E o imposto da renda muda com o tipo. No ETF da B3 que distribui, são os quinze por cento retidos na fonte. No BDR, o rendimento não é isento, e a forma de pagar vem no informe da instituição depositária, que é o nome chique de quem emite o BDR aqui. No fundo imobiliário, a pessoa física não paga imposto sobre a renda, com as condições que estão na tela.

[TELA: tabela de 3 colunas · ETF da B3 que distribui: 15% retidos na fonte (Lei 14.754/2023, art. 24); na venda, 15% sobre o
ganho, sem a isenção de R$ 20 mil · BDR de ETF americano (JEPI39, na B3 desde 23/02/2026): não é isento; siga o informe da
instituição depositária; na venda, 15% sobre o ganho · FII: isento para pessoa física com 100 cotistas ou mais e cotista com
menos de 10% das cotas (Lei 11.033/2004, art. 3º). Nenhuma alíquota no BDR]

O detalhe de cada um sai no vídeo do dia vinte e sete.

---

## BLOCO 8 - AS OBJEÇÕES (9:40–10:50)

Aí você deve estar pensando: "mas a cota volta".

Pode voltar. A conta de doze meses é uma janela só. Refaz em mais de uma janela, de dois e de três anos, quando o ETF tiver idade pra isso.

"Tá, mas eu só quero a renda, não ligo pra cota." A mesma porcentagem em cima de uma cota menor dá uma renda menor no ano seguinte. A cota de hoje é a renda do ano que vem.

Aí vem a outra: "então o certo é ficar com o que não distribui?". Em doze meses, a diferença foi de menos de um ponto. Quem precisa da renda todo mês pagou pouco pra receber todo mês. E nenhum desses códigos está aqui como indicação: não é recomendação de investimento, é material de conta.

[TELA: "Não é recomendação de investimento."]

E o yield alto? Yield é a renda dividida pelo preço da cota. Se a cota cai, o yield sobe sozinho, sem o fundo pagar um centavo a mais. Um ETF vendido como de renda alta, que estreou em dezembro, tem a cota trinta e cinco vírgula nove cinco por cento abaixo da estreia. Com a cota no chão, qualquer yield fica lindo no ranking.

[TELA: `grafico_cotacao`, `serie.py b3 ETHY11 --desde 2025-12-16 --aviso` · R$ 101,46 (1º pregão, 16/12/2025) → R$ 64,99
(01/10/2026): −35,95%. Fonte: B3 (COTAHIST). "Não é recomendação de investimento." Sem "promessa de 30%" (item 15 não conferido)]

---

## FECHO - O BALDE DE VOLTA NA CAIXA (10:50–11:45)

Nove mil, duzentos e sessenta pelo gráfico. Setecentos e quarenta pela conta inteira. E quatro mil e cem atrás do CDI, num ETF que pagava quase um por cento ao mês.

O seu palpite lá do começo tinha resposta dupla: o ETF que paga todo mês te paga e te devolve ao mesmo tempo. Qual dos dois pesou mais, só a conta diz. A cota está nas séries históricas da B3; a renda, nos avisos do fnet.

[TELA: folha de 4 colunas: data · cota · rendimento · acumulado. Embaixo: "cotas: B3, séries históricas · rendimentos: fnet,
avisos de proventos" · "Não é recomendação de investimento."]

Então, Tanaka, da próxima vez que o aplicativo te mostrar o balde enchendo, antes de mandar o print pro grupo, faz a conta do balde na caixa: você põe o balde de volta na caixa, soma com o que a cota andou e compara com o CDI do mesmo ano.

[TELA FINAL: Fb0l4KEq27o]

---

## CUIDADOS DE GRAVAÇÃO

- **Uma imagem só: a caixa d'água e o balde.** Improviso de "cofre", "bolo", "torta" ou "copo" é segunda analogia. "Gêmeos de
  novela" é piada de uma linha sobre o nome do par, não explica mecanismo; se o juiz contar como segunda analogia, cortar a frase.
- **O R$ 9.260 nunca fica sozinho.** No gancho, nos Shorts e na thumbnail ele vem com o R$ 740 (ajuste 1 do briefing).
- **Os 0,74 ponto não têm causa no vídeo.** "Não veio da taxa" e só. Se escapar "foi o imposto" ou "foi a taxa", refazer o take.
- **Imposto:** "retido na fonte", sem dizer quem retém (nem "a corretora", nem "a gestora"). Proibido "o que custa é o imposto
  mensal". No BDR, nenhuma alíquota, nem "carnê-leão", nem "quinze por cento".
- **SPYI11:** quem vende as opções é o fundo americano (o SPYI). O fundo brasileiro não vende opção.
- **Sem marca de gestora e sem corretora.** Os ETFs só pelo código; o ETF americano só como "o SPYI". "Aplicativo" é genérico.
- **A pausa do bloco 2** ("pra onde foi essa água?") é real, 2 s, olhando pra câmera. É a prova no espectador.
- **Extrato falso do bloco 3:** ler as linhas no tom seco de notificação de banco; a graça está em não sorrir.
- **"né?":** uma vez no roteiro inteiro (na objeção do bloco 5). Nada de "ó".

---

## VALIDAÇÕES DO DENIS (só ele confirma; nada bloqueia a gravação, mas o texto final passa por ele)

1. **V1, imposto do ETF (blocos 4 e 7):** "quinze por cento retidos na fonte, em cada pagamento", sem nomear quem retém. A base
   usada é 15% sobre o valor distribuído (leitura da conferência; a Lei não escreve a base). Conferir num informe de rendimentos real.
2. **V2, BDR (bloco 7):** "o rendimento não é isento; a forma de pagar vem no informe da instituição depositária". Se o Denis
   quiser cravar um regime (carnê-leão ou 15% na declaração anual), é decisão dele ou de consulta formal; o roteiro não crava.
3. **V3, SPYI11 (bloco 6):** "quem vende é o fundo de lá" e "o regulamento só deixa ele usar esse tipo de contrato pra se
   proteger". O regulamento achado é de abril/2024; pode haver versão mais nova fora do fnet.
4. **V4, taxa (bloco 5):** "na lâmina, procura a taxa total máxima; se o ETF compra fundo lá fora, confere no regulamento se
   ela já soma a do fundo de fora" e "licença do índice e outras despesas são cobradas à parte".
5. **A objeção do "um e meio de taxa"** (bloco 5) vem do comentário do vídeo Y4WHQiKcv1g (PERGUNTAS-SEM-RESPOSTA, item 15).
   Ligar o "1,50" ao SPYI11 é leitura do briefing ("bate com"). A resposta do vídeo não diz se a taxa é alta: só mostra a conta.
6. **Aviso de recomendação falado** (bloco 8, "não é recomendação de investimento, é material de conta"): ele está na tela em toda
   peça com ticker. O Denis decide se também fala ou se fica só na tela.
7. **Bloco "comprar, vender ou ficar"** (regra do roteirista-tanaka para vídeo de ativo com nome): ficou fora, porque o pedido
   e o briefing tratam os ETFs como prova da conta. O Denis decide se quer o bloco.
8. **Pronúncia dos códigos** (DIVD onze, DIVO onze, SPYI onze, JEPI trinta e nove) e do índice (IDIV).
9. **"Eu também já mandei" (bloco 1):** é o Denis entrando junto na cena do print (P4). Ele confirma se é verdade e se quer dizer.
10. **Piadas** (ele corta o que não soar dele): "dois números que não moram nem no mesmo bairro", "gêmeos de novela", "nem a
    bala do troco da padaria", "esse veio de terno e gravata", "linha da cota: não consta", "é covardia", "a taxa não tira
    férias", "furo pequeno, em dez anos, faz poça grande", "com a cota no chão, qualquer yield fica lindo no ranking".

**Antes de gravar (Mac, não é do Denis):** IPCA de set/2026 se gravar depois de 09/10 (item 13; troca o 4,22% e o −0,21%);
receita do `motion/biblioteca/dados.py` para as barras do par (a biblioteca pede que o número saia da origem, não digitado);
`score_roteiro.py`, `fala_so.py` e os agentes independentes no Mac.

---

## NÚMEROS → FONTE

Toda linha cita o item do briefing (C = conferido no briefing, seção 4.1; R = conferência do Mac, seção 4.2) ou declara a conta.

| número no roteiro (fala ou tela) | valor | fonte |
|---|---|---|
| cota do DIVO11 | R$ 106,82 → R$ 132,90 = +24,41% | C1 (B3, COTAHIST) |
| cota do DIVD11 | R$ 55,86 → R$ 64,32 = +15,15% | C2 (B3, COTAHIST) |
| distância só na cota | 9,26 pontos ("nove pontos" na prova do bloco 2); R$ 9.260 em R$ 100 mil | conta: 24,41 − 15,15 (C1, C2); convenção do briefing, seção 1 |
| mesmo índice (IDIV); um distribui, o outro reinveste | — | R1, R2 |
| renda do DIVD11, evento a evento (tela) | R$ 0,3020 · 0,0336 · 0,4254 · 1,6290 · 0,1276 · 0,2981 · 0,2062 · 0,3013 · 0,1166 · 0,3738 · 0,1495 · 0,7983 | conferência, tabela 2.1 (fnet) |
| "três centavos", "um real e sessenta e três" | R$ 0,0336; R$ 1,6290 | conferência, tabela 2.1 (arredondados na fala) |
| renda somada do DIVD11 | R$ 4,7614 por cota em 12 eventos = 8,52% da cota | R4; conta: 4,7614 ÷ 55,86 |
| retorno total do DIVD11 | 23,67% (bruto) | R4; conta: 15,15 + 8,52 |
| R$ 115.150 · R$ 8.520 · R$ 123.670 · R$ 124.410 (tela) | — | briefing 1 (convenção) e 3.3 |
| diferença de verdade | 0,74 ponto; R$ 740 | conta: 24,41 − 23,67 (C1, R4) |
| "as duas caixas passaram com folga do CDI" | DIVD11 +9,20 e DIVO11 +9,94 pontos sobre 14,47% | briefing 3.3, tabela do passo 2 (C14, R4) |
| IR na distribuição do ETF | 15% retido na fonte | R5 (Lei 14.754/2023, art. 24) |
| IR na venda da cota de ETF, sem a isenção de R$ 20 mil | 15% | R6 (IN RFB 1.585/2015, arts. 57 e 59) |
| renda líquida do DIVD11 (tela) | 7,25% | briefing 3.3; conta: 8,52 × 0,85 |
| os dois vendidos em 01/10/2026 | 20,75% × 20,12% | R9; contas: 24,41 × 0,85 e 15,15 × 0,85 + 7,25 |
| taxa total máxima do par | 0,50% ao ano nos dois | R3 (lâminas de 31/08/2026) |
| exemplo hipotético do bloco 1 | renda de 12%, cota −8%, ganho de 4%; (92 − 100 + 12) ÷ 100 = 4% | C19 |
| IPCA de 12 meses até ago/2026 | 4,22% | C15 (BCB, SGS 13522) |
| retorno real do exemplo (tela) | −0,21% | C19; conta: 1,04 ÷ 1,0422 − 1 |
| taxa em 10 anos, sem rendimento | 0,5%: 4,89% = R$ 4.889 ("uns quatro mil e novecentos"); 1,5%: 14,03% = R$ 14.027 ("uns catorze mil") | C20 |
| taxa máxima do SPYI11 | 1,51% ao ano, somando a do ETF americano | R11 (regulamento, Anexo, 7.1.2) |
| SPYI11 investe 95% ou mais no SPYI, que vende opções de compra todo mês | — | R8 (regulamento, Anexo, 5.1 e 6.1.1) |
| renda do SPYI11 | R$ 13,0763 por cota em 12 eventos, em reais = 11,76%; cerca de 0,98% ao mês ("quase um por cento") | R7; conta: 13,0763 ÷ 111,15 (briefing 3.4) |
| cota do SPYI11 | R$ 111,15 → R$ 109,60 = −1,39% | C3 |
| retorno total do SPYI11 | 10,37% bruto; 8,61% líquido (tela) | R7 |
| CDI no período | 14,47% (02/10/2025 a 01/10/2026) | C14 (BCB, SGS 12) |
| SPYI11 contra o CDI | 4,10 pontos = R$ 4.100 em R$ 100 mil | briefing 3.4 e 9 (gancho C); conta: 14,47 − 10,37 (R7, C14) |
| dólar no período (tela) | PTAX R$ 5,3208 → R$ 5,2079 = −2,12%; "cota praticamente parada" sem o dólar | R10 (BCB, PTAX); a cota em dólar (+0,74%) fica fora para não confundir com os 0,74 ponto do par |
| JEPI39 na B3 (tela) | desde 23/02/2026 | C11 |
| FII isento | 100 cotistas ou mais; cotista com menos de 10% das cotas | R13 (Lei 11.033/2004, art. 3º) |
| BDR | não é isento; sem alíquota | R12 |
| ETHY11 ("um ETF vendido como de renda alta") | R$ 101,46 (1º pregão, 16/12/2025) → R$ 64,99 (01/10/2026) = −35,95% | C9 |
| janelas de dois e de três anos | — | briefing, seção 11 (objeção "a cota volta") |

---

## CHECADORES E NOTAS DOS JUÍZES

### Checadores mecânicos (rodados em 03/10/2026, na nuvem)

- `investir-e-cocar/pipeline/gate_qualidade.py` neste arquivo, `--data 2026-10-14`, título escolhido: **OK, 0 bloqueantes, 0
  avisos, padrão de IA 0 pts.** Na 1ª rodada deu 1 BLOQUEANTE falso (`IR_BDR_DIVIDENDO_ISENTO` na frase do FII, que vinha logo
  depois da do BDR): a frase do FII foi reescrita sem mudar o fato ("a pessoa física não paga imposto sobre a renda").
- O mesmo gate nas checagens de título (`checar_recomendacao`, `checar_corretora`, `checar_tickers`), como faz o
  `checar_serie.py`, nos 3 títulos: **0 problemas**; os 3 com até 60 caracteres (56, 55 e 47), sem "vale a pena"/"qual a melhor".
- `pautas-canal/serie/checar_serie.py`: **OK** (só avisos antigos dos arquivos da série, nenhum deste roteiro).
- Molde repetido (substituto local do `score_roteiro.py`): 5-gramas da fala contra os 369 roteiros de
  `investir-e-cocar/vault/roteiros/`. Em 3+ vídeos só aparecem sequências de número ("cinco por cento ao ano", "um por cento ao
  mês") e o aviso "não é recomendação de investimento", que a rubrica isenta. "por cento sobre o ganho" (3 vídeos) foi reescrito.
- **Não rodaram:** `score_roteiro.py` e `fala_so.py` (estão no Mac).

### Juízes

(em andamento)
