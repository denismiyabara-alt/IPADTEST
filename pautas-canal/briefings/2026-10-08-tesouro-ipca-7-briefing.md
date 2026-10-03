---
tema: "Tesouro IPCA+ a 7% em janeiro: quanto ganhou quem comprou" (definido no v2)
data_video: 2026-10-08 (quinta, longo, 19h)
linha_calendario: pautas-canal/CALENDARIO.csv, linha 5
angulo: "Prestação de contas do vídeo de janeiro: preço na compra e hoje, cupons, marcação."
termo_busca: "tesouro ipca"
video_referencia: dHYQtxnMSrw ("ÚLTIMA CHANCE de GANHAR MUITO DINHEIRO na RENDA FIXA (NTN-B IPCA+7%)", 28/01/2026, 31.506 views, 421 inscritos; auditoria-canal/dados/videos.csv e analytics_por_video.csv)
corte: Short de 14/10 "Tesouro IPCA+ negativo? Calma, isso tem nome" (marcação a mercado em 40 s)
montado_em: 2026-10-03
fonte_principal: Tesouro Transparente, PrecoTaxaTesouroDireto.csv (baixado em 03/10/2026; última data-base 01/10/2026)
---

# Briefing: Tesouro IPCA+ a 7% em janeiro, a prestação de contas

Todos os números deste briefing saem de **uma fonte só**, o CSV oficial de preços e taxas do Tesouro Direto, salvo onde
está escrito outra coisa. Conta derivada vem marcada com **[conta]** e a fórmula ao lado.

## 0. Pesquisa de concorrência (papel do `pesquisador-concorrencia`)

**YouTube: BLOQUEADO nesta rede, não contornado.** `youtube.com` responde 302 ao curl; o `yt-dlp` (instalado do PyPI)
recebeu `Tunnel connection failed: 403 Forbidden` do proxy e, em seguida, "Sign in to confirm you're not a bot". Não usei
cookies nem espelho. Ficou faltando: top vídeos dos últimos 60 dias, legendas, e os comentários (inclusive os do próprio
vídeo de janeiro). **Rodar o passo 1 a 3 do pesquisador no Mac antes de gravar.**

**Web (WebSearch, 03/10/2026):**

| fonte | data | o que diz | status |
|---|---|---|---|
| melhorinvestimento.net, "Tesouro Direto oferece IPCA+ de 8,33% em julho de 2026" | jul/2026 | IPCA+ 2035 a 8,33% em julho; chama o 2035 de "o mais negociado" | **não verificado**. O CSV oficial (taxa de compra, manhã) tem máximo de **8,22%** em 30/07. O 8,33% pode ser taxa da tarde ou de outro título. O vídeo usa o CSV. |
| seudinheiro.com, "A 'janela de ouro' do Tesouro IPCA+, que pode render até 91% com a queda dos juros" | 2026 | tese de ganho com a queda dos juros | só o título (domínio **bloqueado**); é a mesma tese do "ganhar muito dinheiro" de janeiro: depende de a taxa cair |
| arevista.com.br, "Tesouro IPCA+ 2032 cai para 7,53%: o que mudou depois da onda dos 8%" | 30/09/2026 | IPCA+ 2032 a 7,53% na manhã de 30/09 | só o resumo da busca (domínio **bloqueado**); bate com a ordem de grandeza do CSV (7,62% de compra em 01/10) |
| investidor10.com.br, "Mais um título do Tesouro Direto passa a pagar IPCA+ 8%" e "Taxas do Tesouro Direto batem recorde em 2026" | 2026 | onda dos 8% no meio do ano | só título (domínio bloqueado em rodada anterior; ver MOLDE-TESOURO-COPOM.md) |
| infomoney.com.br, "Tesouro IPCA+ decepciona investidor e dá prejuízo de quase 4% em abril" | (ano não confirmado) | quem comprou no começo do mês e vendeu no fim perdeu ~4% | não verificado; serve só de pista do sentimento |

**Dúvida nº 1 (inferida, não medida):** sem os comentários do YouTube, a dúvida que aparece em todas as matérias é
"o app mostra negativo: eu perdi dinheiro?" (marcação a mercado e venda antes do vencimento). O roteiro responde no bloco 2,
que é também o corte do Short de 14/10. **Confirmar com os comentários no Mac.**

**Ângulo que ninguém cobriu (nas matérias achadas):** o extrato de quem comprou num dia específico, contra uma
alternativa concreta (o Tesouro Selic do mesmo dia), com a diferença quebrada em pedaços: o pedágio entre taxa de compra e
de venda, a taxa que subiu um pouco e o juro maior do Selic. As matérias falam de "marcação" em geral; nenhuma mostra
quanto custa a diferença entre o preço de compra e o de recompra no mesmo dia.

## 1. Quais IPCA+ pagavam mais de 7% em janeiro de 2026, e a quanto estão hoje

Taxa de compra da manhã (o que recebe quem compra). 28/01/2026 = o dia do vídeo de referência (publicado às 19h; quem
comprou depois do vídeo pegou a taxa de 29/01, ver nota). Hoje = data-base 01/10/2026, a mais recente do CSV em 03/10.

| título | 28/01 compra | máx. em jan/26 | 01/10 compra | 01/10 venda |
|---|---|---|---|---|
| Tesouro IPCA+ 2029 (15/05/2029) | 7,73% | 8,00% | 7,43% | 7,55% |
| Tesouro IPCA+ 2035 (15/05/2035) | 7,47% | 7,70% (20/01) | 7,56% | 7,68% |
| Tesouro IPCA+ 2040 (15/08/2040) | 7,28% | 7,42% | 7,26% | 7,38% |
| Tesouro IPCA+ 2045 (15/05/2045) | 6,99% (abaixo de 7) | 7,22% | 7,05% | 7,17% |
| Tesouro IPCA+ 2050 (15/08/2050) | 6,87% (abaixo de 7) | 7,13% | 7,06% | 7,18% |
| IPCA+ c/ Juros Semestrais 2030 (15/08/2030) | 7,72% | 7,94% | 7,59% | 7,71% |
| IPCA+ c/ Juros Semestrais 2032 (15/08/2032) | 7,64% | 7,90% | 7,60% | 7,72% |
| IPCA+ c/ Juros Semestrais 2035 (15/05/2035) | 7,53% | 7,76% | 7,55% | 7,67% |
| IPCA+ c/ Juros Semestrais 2040 (15/08/2040) | 7,38% | 7,54% | 7,34% | 7,46% |
| IPCA+ c/ Juros Semestrais 2045 (15/05/2045) | 7,19% | 7,40% | 7,20% | 7,32% |
| IPCA+ c/ Juros Semestrais 2050 (15/08/2050) | 7,11% | 7,34% | 7,19% | 7,31% |
| IPCA+ c/ Juros Semestrais 2055 (15/05/2055) | 7,07% | 7,29% | 7,11% | 7,23% |
| IPCA+ c/ Juros Semestrais 2060 (15/08/2060) | 7,10% | 7,32% | 7,10% | 7,22% |
| IPCA+ e IPCA+ c/ Juros Semestrais 2026 (15/08/2026) | 10,28% | 10,30% | vencido em 15/08/2026 | — |

- **Em 28/01, 11 títulos que ainda não venceram pagavam mais de 7%** (3 sem cupom + 8 com juros semestrais) [conta:
  contagem na tabela, excluindo o 2026, que venceu, e o 2045 e 2050 sem cupom, abaixo de 7% nesse dia].
- Em algum dia de janeiro **todos** os IPCA+ listados passaram de 7% (coluna "máx.").
- Títulos novos desde janeiro (não existiam no CSV em jan/26): Tesouro IPCA+ 2032 (15/08/2032; 7,62% em 01/10) e IPCA+ c/
  Juros Semestrais 2037 (15/05/2037; 7,53% em 01/10). Fora da conta.
- Nota: 29/01, IPCA+ 2035 a 7,41% (PU R$ 2.376,11). Mudaria o resultado em ~0,5 p.p.; o roteiro usa 28/01.

## 2. Quanto ganhou quem comprou em 28/01 (marcação a mercado até 01/10/2026)

Regra: entra pelo **PU Compra** de 28/01 (preço que o investidor paga) e sai pelo **PU Venda** de 01/10 (preço que o
Tesouro paga na recompra). Antes de IR e de taxa de custódia. R$ 10 mil = conta proporcional, sem arredondar a fração do título.

| título | PU compra 28/01 | PU venda 01/10 | preço | cupons [conta] | total | R$ 10 mil viraram | pior momento do preço* |
|---|---|---|---|---|---|---|---|
| IPCA+ 2029 | 3.604,42 | 3.931,09 | +9,06% | — | +9,06% | R$ 10.906 | −0,40% (28/01) |
| **IPCA+ 2035** | **2.363,30** | **2.519,80** | **+6,62%** | — | **+6,62%** | **R$ 10.662** | −1,74% (09/03) |
| IPCA+ 2040 | 1.662,90 | 1.777,77 | +6,91% | — | +6,91% | R$ 10.691 | −2,23% (04/02) |
| Semestrais 2030 | 4.439,46 | 4.533,52 | +2,12% | 2 × (fev e ago) | +8,34% | R$ 10.834 | −3,33% (16/03) |
| Semestrais 2032 | 4.356,75 | 4.423,76 | +1,54% | 2 × | +7,88% | R$ 10.788 | −3,57% (09/03) |
| **Semestrais 2035** | **4.213,62** | **4.388,12** | +4,14% | 1 × (mai) | **+7,44%** | **R$ 10.744** | −2,64% (10/06) |
| Semestrais 2040 | 4.188,15 | 4.220,88 | +0,78% | 2 × | +7,38% | R$ 10.738 | −4,11% (09/03) |
| Semestrais 2045 | 4.116,87 | 4.256,07 | +3,38% | 1 × | +6,76% | R$ 10.676 | −4,42% (10/06) |
| Semestrais 2050 | 4.163,27 | 4.121,42 | −1,01% | 2 × | +5,63% | R$ 10.563 | −5,74% (17/08) |
| Semestrais 2055 | 4.080,31 | 4.188,42 | +2,65% | 1 × | +6,06% | R$ 10.606 | −5,48% (10/06) |
| Semestrais 2060 | 4.104,90 | 4.089,94 | −0,36% | 2 × | +6,36% | R$ 10.636 | −5,51% (09/03) |
| **Tesouro Selic 2029** (comparação) | **18.252,04** | **19.970,63** | **+9,42%** | — | **+9,42%** | **R$ 10.942** | — |

\* pior momento = menor PU venda ÷ PU compra de 28/01 entre 28/01 e 01/10, **só preço**, sem somar cupom.

- **Os 11 IPCA+ acima de 7% em 28/01 estão atrás do Tesouro Selic 2029 no mesmo período** [conta: coluna "total" < 9,42%
  em todas as linhas]. O mais perto é o IPCA+ 2029 (9,06%); o mais longe, o Semestrais 2050 (5,63%).
- **IPCA+ 2035 no pico de julho:** 30/07/2026, taxa de compra 8,22% (máxima do período), PU venda R$ 2.355,68 →
  R$ 10 mil = **R$ 9.968** [conta: 10.000 × 2.355,68 ÷ 2.363,30]. Dias de pregão com o preço abaixo da compra entre 28/01
  e 01/10: 30 (de 28/01 a 30/07).
- **Comprou e vendeu no mesmo minuto em 28/01:** R$ 10 mil = **R$ 9.894** [conta: 10.000 × 2.338,16 (PU venda 28/01) ÷
  2.363,30]. A taxa de venda fica 0,12 p.p. acima da de compra em todos os IPCA+ (7,47% × 7,59% no 2035, 28/01).

### 2a. Onde estão os R$ 280 do IPCA+ 2035 contra o Tesouro Selic [conta]

R$ 10.942 − R$ 10.662 = R$ 280 (arredondados; sem arredondar, R$ 279,4).

| pedaço | R$ (em R$ 10 mil) | como saiu |
|---|---|---|
| pedágio entre compra e venda (0,12 p.p.) | ~R$ 108 | PU compra 01/10 (2.545,29) − PU venda 01/10 (2.519,80), proporcional aos R$ 10 mil |
| a taxa subiu de 7,47% para 7,56% | ~R$ 77 | PU estimado de 01/10 a 7,47% (2.563,58) contra o PU real a 7,56% (2.545,29); estimativa: PU × (1,0756/1,0747)^(du/252), du = 2.156 dias úteis até 15/05/2035, feriados nacionais calculados |
| o Selic pagou mais juro que IPCA + 7,47% no período | ~R$ 94 | 9,42% (Selic) − 8,47% (IPCA+ 2035 se a taxa não tivesse mexido) |

Soma: R$ 279. O "pedaço do Selic" é residual da conta, não leitura direta de IPCA e Selic (as duas séries estão bloqueadas
daqui, ver seção 4).

## 3. Cupons do Tesouro IPCA+ com Juros Semestrais [conta]

- Cupom = 6% ao ano sobre o VNA, pago a cada seis meses: (1,06)^0,5 − 1 = **2,9563% do VNA** por cupom.
  Títulos com vencimento em maio pagam em 15/05 e 15/11; em agosto, em 15/02 e 15/08.
- **VNA não está no CSV, e a ANBIMA está bloqueada.** Estimei o VNA a partir do Tesouro IPCA+ 2026 (sem cupom), que vale
  VNA ÷ (1 + taxa)^(du/252) e venceu em 15/08/2026: VNA ≈ R$ 4.600 em 15/02, R$ 4.704,56 em 15/05 e R$ 4.742,62 em
  15/08 (o de agosto é o mais firme: 1 dia útil para o vencimento em 14/08).
- Cupom por título ≈ R$ 136 (fev), **R$ 139,08 (mai)**, R$ 140,21 (ago).
- **Semestrais 2035 comprado em 28/01:** R$ 10 mil = 2,3733 títulos → cupom de maio ≈ **R$ 330** bruto; preço de hoje
  + cupom = **R$ 10.744** [conta: 10.000 × (4.388,12 + 139,08) ÷ 4.213,62].
- O preço do título cai mais ou menos do tamanho do cupom no dia do pagamento (por isso a coluna "preço" dos semestrais
  é menor). O IR do cupom é retido no pagamento, pela tabela regressiva contada desde a compra.
- **Validação do Denis:** conferir o cupom num extrato real ou no VNA da ANBIMA (bloqueado daqui). Diferença esperada: centavos.

## 4. Inflação, CDI, Selic e imposto

| dado | valor | fonte | status |
|---|---|---|---|
| IPCA mensal (SGS 433) | **não lido** | api.bcb.gov.br | **bloqueado** (502 no CONNECT, 03/10/2026). IBGE (apisidra/sidra/www.ibge.gov.br) também **bloqueado** (403/sem conexão). Não contornei. |
| IPCA 12 meses até ago/2026 | 4,22% | SGS 13522, lido no Mac em 02/10/2026 (MOLDE-TESOURO-COPOM.md) | não reconferido daqui; **não vai pra fala** |
| IPCA acumulado jan–jul/2026, implícito no VNA | ≈ 3,4% | [conta] VNA 15/08 (4.742,62) ÷ VNA 15/01 (≈4.585,15) | estimativa; **não vai pra fala**; conferir com SGS 433 |
| CDI (SGS 12) | **não lido** | api.bcb.gov.br | **bloqueado**. O vídeo compara com o **Tesouro Selic** (mesmo CSV), que acompanha a Selic. Não dizer "CDI". |
| Selic meta | 13,75% desde 17/09/2026 | comunicado da 281ª reunião (MOLDE-TESOURO-COPOM.md) | não vai pra fala |
| IR | 22,5% até 180 dias; 20% de 181 a 360; 17,5% de 361 a 720; 15% acima | Lei 11.033/2004, art. 1º | 28/01 → 08/10 = 253 dias → **20%**, igual para IPCA+ e Selic |
| ganho líquido de IR (20%) em R$ 10 mil | IPCA+ 2035: R$ 530 · Selic: R$ 754 | [conta] 662 × 0,8 e 942 × 0,8 | tela |
| taxa de custódia B3 | não incluída | — | fora da conta nos dois lados; dizer "antes da taxa de custódia" na tela |

## 5. Domínios bloqueados nesta rodada (não contornados)

api.bcb.gov.br (502) · apisidra.ibge.gov.br (403) · sidra.ibge.gov.br e www.ibge.gov.br (sem conexão) ·
www.youtube.com / yt-dlp (403 + bot check) · www.seudinheiro.com, arevista.com.br (bloqueio do proxy) ·
borainvestir.b3.com.br, investnews.com.br, maisretorno.com, www.anbima.com.br, www.tesourodireto.com.br (sem conexão).
Funcionou: www.tesourotransparente.gov.br (CSV, 200) e www.b3.com.br (200, não usado).

## 6. Atualizar na véspera da gravação

O CSV chega com 1–2 dias úteis de atraso. Na quarta 07/10, baixar de novo e trocar a data-base "01/10" pela mais recente:
```
curl -sSo td.csv "https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv"
grep -E "^Tesouro (IPCA\+;15/05/2035|Selic;01/03/2029|IPCA\+ com Juros Semestrais;15/05/2035)" td.csv | grep -E ";(28/01/2026|0[5-7]/10/2026);"
```
R$ 10 mil hoje = 10.000 × PU Venda (hoje) ÷ PU Compra (28/01). Se a ordem (Selic na frente) mudar, o roteiro muda de tese: avisar.

## 7. O que NÃO dizer

"última chance" como verdade, "trava agora", "vale a pena", "compre"/"venda", nome de corretora, "CDI" (não lido),
"8,33%" (não está no CSV), "o mais negociado" (não verificado), "garantido sem risco" (o preço oscila até o vencimento).
