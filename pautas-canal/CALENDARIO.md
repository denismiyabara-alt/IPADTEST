# Calendário oficial: v3 (05/10 a 29/11/2026)

**Aprovado pelo Denis em 03/10/2026.** Gerado por `calendario_v3.py` a partir do v2 e da proposta aprovada
(`serie/PROPOSTA-CALENDARIO-V3.md`). Todas as colunas estão em `CALENDARIO.csv`.

**Histórico:** o v2 continua em `CALENDARIO-8-SEMANAS.md` e `.csv` (gerados por `calendario_v2.py`, sem mudança; a
`esteira-social/` ainda lê esse arquivo) e o v1 em `CALENDARIO-8-SEMANAS_v1.*`.

**Inscritos esperados são ESTIMATIVA, não previsão:** views intencionais medianas do assunto × inscritos por mil, nos
últimos 12 meses (`modelo.py`, `TEMAS.md`). São inscritos vitalícios de cada vídeo, que chegam ao longo de 1 a 3 meses.

## O que mudou do v2 para o v3

1. **Série de renda mensal aprovada:** 6 episódios às quartas, 19h (14/10, 21/10, 28/10, 11/11, 18/11 e 25/11).
   **Os títulos são provisórios:** ainda passam pelo empacotador e pelo teste A/B (coluna `status_titulo`).
2. **Saem as 7 pautas fora do nicho** (tabela abaixo), trocadas pelos Shorts derivados dos episódios ou pelos episódios.
3. **Copom de 03-04/11: Tesouro ANTES da decisão**, na **terça 03/11, 19h**, com a versão pré do molde. A pauta de renda
   mensal que estava na terça 03/11 vai para a quinta 05/11, que era do longo pós.
4. **Nenhuma semana com mais de 3 longos:** 2 longos saíram da semana pela regra (tabela abaixo).
5. **O Ep. 1 não tem concorrente na mesma semana:** o longo de ETF de dividendos mensais de 06/10 vai para depois da
   série, e o título do 27/10 muda (tabela abaixo).
6. **Total:** 23 longos e 16 Shorts (v2: 21 e 16).

### As 7 pautas fora do nicho

| data | saiu (v2) | entrou (v3) |
|---|---|---|
| 07/10 qua | short: "Como juntar 1 milhão de reais com R$ 1.000 por mês" | Ep. 1 (Short): "Recebeu 1% ao mês e a cota caiu 1%: quanto ganhou?" |
| 21/10 qua | short: "Casal que investe junto: a conversa que vem antes do dinheiro" | Ep. 2 (Short): "O dividend yield dobrou e a empresa não pagou nada a mais" |
| 16/11 seg | short: "Perfil de investidor: 3 perguntas antes de investir" | Ep. 4 (Short): "LCI e LCA não pagam todo mês. Mas dá para fazer vencer uma por mês" |
| 18/11 qua | short: "Juros compostos: por que 1 centavo dobrando todo dia não existe" | Ep. 3 (Short): "R$ 100 mil, 10 anos: gastar a renda ou reinvestir?" |
| 21/11 sáb | longo: "Bolha da IA: o que dizem os números" | nada no dia; o longo da semana passa a ser o Ep. 5 (18/11) |
| 23/11 seg | short: "Reserva de emergência: onde deixar e onde não deixar" | Ep. 5 (Short): "R$ 1.000 de renda hoje compram quanto em 10 anos?" |
| 28/11 sáb | longo: "Tesouro Direto na reserva de emergência: Selic, CDB ou conta" | nada no dia; o longo da semana passa a ser o Ep. 6 (25/11) |

O Short do Ep. 6 ("Recebe todo mês? Veja quais meses ficam vazios") fica para seg 30/11, fora da janela.

### Semanas com 4 longos: a decisão

Regra aprovada: numa semana com mais de 3 longos, sai o de **menor número de inscritos esperados** pelo modelo, ou ele é
empurrado para a próxima semana com vaga. Os episódios da série e o Copom são fixos (aprovados com data).

**Semana de 26/10** (4 longos):

| data | longo | inscritos esperados | fixo? | decisão |
|---|---|---|---|---|
| 27/10 | ETF de dividendos mensais ou FII: imposto e renda de cada um | 91 | não | fica |
| 28/10 | Gastar ou reinvestir os dividendos: a conta de 10 anos | 91 | sim | fica |
| 29/10 | Tesouro IPCA+ acima de 7%: o que é travar a taxa | 195 | não | fica |
| 31/10 | TRXF11: o que aconteceu com a renda desde agosto | 45 | não | **sai da janela (fila de dezembro): nenhuma semana seguinte até 29/11 tem vaga** |

**Semana de 09/11** (4 longos):

| data | longo | inscritos esperados | fixo? | decisão |
|---|---|---|---|---|
| 10/11 | Renda mensal com Tesouro Direto: juros semestrais e RendA+ | 91 | não | fica |
| 11/11 | LCI e LCA para renda mensal: a escada de vencimentos | 91 | sim | fica |
| 12/11 | Fundo imobiliário ou imóvel alugado: a conta de 2026 | 45 | não | **puxado para ter 06/10, na vaga do ETF que canibalizava o Ep. 1 (nenhuma semana seguinte tinha vaga)** |
| 14/11 | CDB prefixado ou pós-fixado: qual rende mais em 2026 | 195 | não | fica |

Nas duas semanas, o mais fraco é um longo de FII (45 esperados contra 91 de renda mensal e 195 de Tesouro), e
nenhuma semana seguinte até 29/11 tem vaga (todas já têm 3 longos). O de 12/11 foi para a vaga de 06/10 (seção
seguinte); o TRXF11 de 31/10 vai para a fila de dezembro. A proposta sugeria tirar o CDB prefixado de 14/11, mas pelo
modelo ele é o mais forte da semana (Tesouro e renda fixa, 195).
**Atenção:** o TRXF11 de 31/10 é o termo de investimento mais buscado do canal nos últimos 6 meses (1.516 views da
Pesquisa). O modelo de inscritos não enxerga busca; se o Denis preferir a busca ao modelo, a troca natural é com o
longo de FII de 07/11 (o mesmo assunto e o mesmo esperado).

### Ep. 1 sem canibalização (briefing do Ep. 1)

O briefing `briefings/2026-10-14-etf-dividendos-mensais-briefing.md` apontou que o longo do v2 de 06/10 sai 8 dias
antes do Ep. 1 com o mesmo tema e o mesmo termo de busca ("etfs que pagam dividendos mensais").

| data | antes | decisão | por quê |
|---|---|---|---|
| ter 06/10 | longo "ETFs que pagam dividendos mensais: o que mudou em 2026" (renda mensal, 91) | **vai para depois da série (fila de dezembro)** | é a atualização da lista de 2025; em dezembro vira o balanço do ano e não disputa o termo com o Ep. 1. O Ep. 1 não muda |
| ter 06/10 | (vaga) | **entra "Fundo imobiliário ou imóvel alugado: a conta de 2026"** (FII, 45), que saía de 12/11 pela regra dos 3 longos | é o mais forte da fila sem ETF de dividendos. O outro da fila, TRXF11, repetiria o vídeo de 29/09/2026 sobre o fundo. O canal fez "Fundos Imobiliários ou Imóveis" em 26/06/2026 (14 inscritos): o ângulo de 2026 (Lei 14.754/2023, vacância, liquidez) tem de ficar claro no título final. O Short "FII ou aluguel" de 11/11 passa a ser corte deste longo |
| ter 20/10 | "ETF de dividendos mensais com opções: de onde vem a renda" | fica, com guardrail | a mecânica das opções cobertas é deste vídeo; o Ep. 1 só a cita em uma frase |
| ter 27/10 | "ETF de dividendos mensais ou fundo imobiliário: o que sobra" | **título novo: "{TITULO_27_10[1]}"** | o título do v2 usava "o que sobra", como a promessa do Ep. 1; o imposto detalhado é deste vídeo e o Ep. 1 só tem uma tabela curta |

Custo na estimativa: −46 inscritos (sai um longo de renda mensal, 91; entra um de FII, 45). Trocar os dois de lugar
(o FII em dezembro) não resolveria: o ETF de 06/10 é o que canibaliza.

## Copom de 03-04/11: Tesouro antes da decisão

**Data escolhida: terça 03/11/2026, 19h** (1º dia da reunião), com a versão pré do `serie/MOLDE-TESOURO-COPOM.md`.
Título provisório: "Tesouro Direto antes do Copom: o que olhar no IPCA+ hoje".

Por que terça e não segunda 02/11:
- **02/11 é feriado (Finados).** Longos publicados em feriado nacional (ou Carnaval e Corpus Christi) renderam
  menos: mediana de 27 inscritos por vídeo em 17 longos, contra 40 nos 656 dos outros dias
  (vitalício, com 30 dias ou mais de vida). Nos últimos 12 meses há só 1 longo em feriado, com
  13 inscritos de mediana, contra 27. Amostra pequena, mas nada a favor do feriado. (Nos Shorts o
  feriado não muda nada: mediana de 4 em 9 Shorts, contra 4; por isso o Short de seg 12/10,
  feriado de Nossa Senhora Aparecida, fica.)
- **Segunda é o dia que menos converte:** 6,0 inscritos por mil views intencionais, contra 10,4 da terça
  (`PROPOSTA-CALENDARIO-V3.md`, 80 longos de 12 meses).
- **O Focus de segunda não sai no feriado.** O relatório de referência 30/10 sai no 1º dia útil, terça 03/11 (conferir
  em bcb.gov.br/publicacoes/focus). Um vídeo de segunda teria de usar o Focus de 23/10, de 10 dias antes; o de terça
  19h já usa o de 30/10, que é o [FOCUS_*] do molde.
- **É o padrão que funcionou:** 3 dos 4 longos de Tesouro em semana de Copom saíram na terça, 1º dia da reunião
  (`KMIsVEOcaLM` 246, `tb0nwpl9mFw` 142 e `p9wkMT4RV40` 69 inscritos); o 4º, na quarta da decisão (`dHYQtxnMSrw`, 421).
- **Custo:** a pauta de renda mensal de 03/11 ("Dividendos mensais de R$ 1.000…") vai para a quinta 05/11, 19h, que
  ficou livre com a saída do longo pós. A semana continua com 3 longos.

O Short de quarta 04/11 ("Copom hoje…") vira um corte do longo pré, com as taxas da manhã de quarta. No dia seguinte à
decisão não há vídeo novo: comunicado e reação das taxas vão num comentário fixado no longo de 03/11 e num post na
comunidade (quinta, depois da abertura do Tesouro Direto).

### Regra para 08-09/12 (fora da janela)

Medida: inscritos do longo pré de 03/11 nos 7 primeiros dias (Studio, de 03/11 a 09/11).

- **Se fizer 69 inscritos ou mais em 7 dias, repetir o pré:** longo na terça 08/12, 19h, e Short pós na quinta 10/12.
- **Se fizer menos de 69, testar o pós:** Short pré na quarta 09/12 e longo pós na quinta 10/12, 19h (versão pós do
  molde).
- **Por que 69:** é o total do pré-Copom mais fraco do ano (`p9wkMT4RV40`, setembro), medido com 16 dias de vida na
  exportação de 02/10. Passar disso em 7 dias é ficar acima do pior caso conhecido em menos da metade do tempo. O
  esperado do modelo é 195 no vitalício.
- O padrão de 2027 sai da comparação das duas reuniões (inscritos e views intencionais de 7 dias), como no molde.

### Conferência das datas no BCB (03/10/2026)

- **Não consegui ler o calendário oficial.** A página
  https://www.bcb.gov.br/controleinflacao/calendarioreunioescopom responde (HTTP 200), mas é um app Angular. A rota
  `api/paginasite/sitebcb/controleinflacao/calendarioreunioescopom` devolve só o componente `bcb-pagina-tipo0`.
  O componente consulta `api/servico/sitebcb/hub?tipo='calendarioreunioescopom'&listsite=controleinflacao`, que voltou
  vazio (`{"conteudo":[]}`), assim como `paginatipo` e `conteudosite`.
- **Endpoints tentados na API do site:** `copom/calendario`, `copom/agenda`, `copom/reunioes`, `copom/calendarioreunioes`,
  `copom/proximasreunioes` e `copom/datasreunioes` deram HTTP 500; `calendariocopom` e `agendacopom` deram HTTP 400.
- **O que respondeu:** `copom/comunicados?quantidade=1` (281ª reunião, 16/09/2026) e `copom/atas?quantidade=1` (281ª,
  "15-16 setembro, 2026", ata em 22/09). Nenhum dos dois traz reuniões futuras.
- **Continua valendo "conferir no bcb.gov.br"** para 03-04/11 e 08-09/12. A fonte de hoje é a imprensa
  (`MOLDE-TESOURO-COPOM.md`, seção 6). Nenhum bloqueio foi contornado.

## Inscritos esperados (estimativa)

### v2 × v3

| | v2 | v3 | diferença |
|---|---|---|---|
| longos / Shorts nas 8 semanas | 21 / 16 | 23 / 16 | +2 / +0 |
| inscritos esperados (central) | 2.293 | **2.453** | **+160** |
| faixa p25–p75 | 1.401 a 3.964 | 1.593 a 4.952 | |

A conta: 2.293 − 258 (as 7 pautas fora do nicho) + os 6 episódios e 5 Shorts da série − o TRXF11 (fila de
dezembro) − o ETF de 06/10 (depois da série) ± zero do FII de 12/11, que só mudou para 06/10. O Copom muda de quinta
para terça e não muda o esperado.

### Contra a meta mensal (META.md)

Mesma conta do `META.md`: inscritos líquidos do mês = catálogo (449) + vídeos novos − perdas
(350). Os vídeos novos entram com a defasagem do `meta.py` (60% no mês da publicação, 25% no seguinte e
15% no outro). Outubro conta só os vídeos da janela (de 05/10 em diante).

| mês | longos | Shorts | inscritos esperados dos vídeos do mês (vitalício) | entram no mês (com defasagem) | líquidos estimados | meta (META.md) | diferença |
|---|---|---|---|---|---|---|---|
| 10/26 | 11 | 8 | 1.248 (792–2.392) | 749 | **849** (575–1.535) | 573 | +276 |
| 11/26 | 12 | 8 | 1.205 (802–2.560) | 1.035 | **1.135** (779–2.234) | 925 | +210 |

**Leitura:**
- Na estimativa central, outubro e novembro ficam acima da
  meta mensal. Na faixa p25 (pessimista), novembro
  fica abaixo.
- Outubro tem 11 longos na janela, mais o de 01/10 já publicado; o plano do `META.md` contava 9 (rampa de 75%).
- Uma parte dos inscritos de novembro chega em dezembro e janeiro (defasagem). Não conta aqui, mas entra na meta de
  dezembro (1.107).
- **Cenário pessimista:** se renda mensal e Tesouro renderem como a mediana geral dos longos (42 por vídeo, e
  não 91 e 195), as 8 semanas ficam em ~1.055.
- **Risco do título provisório:** pela regra de assunto do título, os títulos provisórios do Ep. 2 e do Ep. 3 caem em
  "ações e empresas" (30 por longo), não em renda mensal. Se o título final ficar assim e o vídeo render como o
  assunto do título, a série perde ~122. A coluna `assunto_pelo_titulo` mostra isso.
- **Validação:** depois do Ep. 3 (28/10), comparar os inscritos de 7 dias dos 3 episódios com os 91 esperados.
  Se a mediana ficar abaixo de 42 (a mediana geral), rever a série antes do Ep. 4.

### Por semana

A meta semanal é o plano de vídeos novos de `META.md` ÷ 4,33, com a rampa de outubro (o mesmo do v2).

| semana | longos | Shorts | v2 | v3 (faixa p25–p75) | meta semanal de vídeos novos | v3 − meta |
|---|---|---|---|---|---|---|
| 05/10–11/10 | 2 | 2 | 289 | **245** (135–274) | 182 | +63 |
| 12/10–18/10 | 3 | 2 | 147 | **238** (160–615) | 182 | +56 |
| 19/10–25/10 | 3 | 2 | 294 | **383** (248–753) | 182 | +201 |
| 26/10–01/11 | 3 | 2 | 336 | **382** (249–751) | 182 | +200 |
| 02/11–08/11 | 3 | 2 | 338 | **338** (206–542) | 242 | +97 |
| 09/11–15/11 | 3 | 2 | 344 | **389** (253–761) | 242 | +148 |
| 16/11–22/11 | 3 | 2 | 205 | **244** (175–657) | 242 | +2 |
| 23/11–29/11 | 3 | 2 | 338 | **233** (168–600) | 242 | −8 |
| **8 semanas** | 23 | 16 | 2.293 | **2.453** | 1.695 | +758 |

## As 8 semanas

| data | formato | título | série | assunto | termo de busca real | Pesquisa 6 meses | continuação de | inscritos esperados (p25–p75) |
|---|---|---|---|---|---|---|---|---|
| **semana 1 · 05/10–11/10** | | | | | | | | |
| 05/10 seg | short | **LCI e LCA ou CDB: qual rende mais depois do imposto?** | — | tesouro e renda fixa | o que é lci e lca | 1.091 | — | 2,2 (2,1–3,1) |
| 06/10 ter | longo | **Fundo imobiliário ou imóvel alugado: a conta de 2026** | — | FII | fundo imobiliario | 167 | Gjw4crGh6Xg (92) | 45 (26,1–55,9) |
| 07/10 qua | short | **Recebeu 1% ao mês e a cota caiu 1%: quanto ganhou?** *(provisório)* | Ep. 1 (Short) | renda mensal | — (sem termo) | — | Fb0l4KEq27o (637); trocar o link pelo Ep. 1 em 14/10 | 1,6 (0,9–3,3) |
| 08/10 qui | longo | **Tesouro IPCA+ a 7% em janeiro: quanto ganhou quem comprou** | — | tesouro e renda fixa | tesouro ipca | 1.009 | dHYQtxnMSrw (421) | 195 (106,2–211,5) |
| **semana 2 · 12/10–18/10** | | | | | | | | |
| 12/10 seg | short | **Resgatou o CDB antes de 30 dias? O IOF come o rendimento** | — | tesouro e renda fixa | — (sem termo) | — | — | 2,2 (2,1–3,1) |
| 13/10 ter | longo | **Dividendos mensais com ações: como montar um calendário** | — | renda mensal | dividendos mensais | 339 | TY8oLvUt2Qg (324) | 91 (69,1–266,6) |
| 14/10 qua | longo | **ETF que paga dividendos mensais: a renda saiu da cota?** *(provisório)* | Ep. 1 | renda mensal | etfs que pagam dividendos mensais | 331 | Fb0l4KEq27o (637) e c9Obo6F5_NU | 91 (69,1–266,6) |
| 14/10 qua | short | **Tesouro IPCA+ negativo? Calma, isso tem nome** | — | tesouro e renda fixa | — (sem termo) | — | — | 2,2 (2,1–3,1) |
| 15/10 qui | longo | **Crise financeira: o gráfico de 1929, 2008 e 2020, hoje** | — | crise e macro | crise financeira | 3 | IcN3m7whpl8 (357) | 52 (17,4–75,5) |
| **semana 3 · 19/10–25/10** | | | | | | | | |
| 19/10 seg | short | **FII é isento de imposto? Só se cumprir estas 3 regras** | — | imposto e regras | — (sem termo) | — | — | 4,1 (2,7–4,9) |
| 20/10 ter | longo | **ETF de dividendos mensais com opções: de onde vem a renda** | — | renda mensal | etf dividendos mensais | 425 | IB1mBcF00jc (131) | 91 (69,1–266,6) |
| 21/10 qua | longo | **Dividendos altos demais: 4 contas antes de confiar na renda** *(provisório)* | Ep. 2 | renda mensal | dividendos | 117 | TY8oLvUt2Qg (324) | 91 (69,1–266,6) |
| 21/10 qua | short | **O dividend yield dobrou e a empresa não pagou nada a mais** *(provisório)* | Ep. 2 (Short) | renda mensal | — (sem termo) | — | Ep. 2 (mesmo dia) | 1,6 (0,9–3,3) |
| 22/10 qui | longo | **LCI e LCA ou CDB: a conta de 2026 com imposto e prazo** | — | tesouro e renda fixa | lci e lca | 1.175 | — | 195 (106,2–211,5) |
| **semana 4 · 26/10–01/11** | | | | | | | | |
| 26/10 seg | short | **FGC: o que cobre e o que não cobre** | — | tesouro e renda fixa | fgc | 0 | — | 2,2 (2,1–3,1) |
| 27/10 ter | longo | **ETF de dividendos mensais ou FII: imposto e renda de cada um** | — | renda mensal | etf dividendos | 417 | lwV6tbkk4Cw (93) | 91 (69,1–266,6) |
| 28/10 qua | longo | **Gastar ou reinvestir os dividendos: a conta de 10 anos** *(provisório)* | Ep. 3 | renda mensal | dividendos mensais | 597 | IB1mBcF00jc (131) | 91 (69,1–266,6) |
| 28/10 qua | short | **Quanto rende R$ 1.000 no Tesouro Selic hoje** | — | tesouro e renda fixa | qual investimento rende mais | 43 | — | 2,2 (2,1–3,1) |
| 29/10 qui | longo | **Tesouro IPCA+ acima de 7%: o que é travar a taxa** | — | tesouro e renda fixa | tesouro ipca | 1.009 | KMIsVEOcaLM (246; recebe 'tesouro direto' e 'ipca + 8' na busca) | 195 (106,2–211,5) |
| **semana 5 · 02/11–08/11** | | | | | | | | |
| 02/11 seg | short | **JCP em 2026: já vem com 17,5% de imposto** | — | imposto e regras | — (sem termo) | — | — | 4,1 (2,7–4,9) |
| 03/11 ter | longo | **Tesouro Direto antes do Copom: o que olhar no IPCA+ hoje** | — | tesouro e renda fixa | tesouro direto | 1.024 | KMIsVEOcaLM (246), tb0nwpl9mFw (142) e dHYQtxnMSrw (421) | 195 (106,2–211,5) |
| 04/11 qua | short | **Copom hoje: 3 números para olhar no seu Tesouro** | — | tesouro e renda fixa | — (sem termo) | — | longo pré de 03/11 | 2,2 (2,1–3,1) |
| 05/11 qui | longo | **Dividendos mensais de R$ 1.000: quanto precisa investir** | — | renda mensal | dividendos mensais | 331 | — | 91 (69,1–266,6) |
| 07/11 sáb | longo | **Fundos imobiliários para iniciantes: de onde vem a renda** | — | FII | fundos imobiliarios | 167 | kipRQb0ksus (busca de FII, 2023) | 45 (26,1–55,9) |
| **semana 6 · 09/11–15/11** | | | | | | | | |
| 09/11 seg | short | **Imposto sobre dividendos acima de R$ 50 mil por mês: quem paga** | — | imposto e regras | — (sem termo) | — | — | 4,1 (2,7–4,9) |
| 10/11 ter | longo | **Renda mensal com Tesouro Direto: juros semestrais e RendA+** | — | renda mensal | tesouro direto | 1.009 | — | 91 (69,1–266,6) |
| 11/11 qua | longo | **LCI e LCA para renda mensal: a escada de vencimentos** *(provisório)* | Ep. 4 | renda mensal | lci e lca | 1.175 | Q1WMbZZn2Ik (Short) e dHYQtxnMSrw (421) | 91 (69,1–266,6) |
| 11/11 qua | short | **FII ou aluguel: quanto rende R$ 100 mil em cada um** | — | FII | — (sem termo) | — | — | 7,6 (5,7–11,3) |
| 14/11 sáb | longo | **CDB prefixado ou pós-fixado: qual rende mais em 2026** | — | tesouro e renda fixa | cdb prefixado | 5 | 7CdwOTT7U3o (CDB prefixado, 2018: 3.928 views da Pesquisa) | 195 (106,2–211,5) |
| **semana 7 · 16/11–22/11** | | | | | | | | |
| 16/11 seg | short | **LCI e LCA não pagam todo mês. Mas dá para fazer vencer uma por mês** *(provisório)* | Ep. 4 (Short) | renda mensal | — (sem termo) | — | Ep. 4 (11/11) | 1,6 (0,9–3,3) |
| 17/11 ter | longo | **ETF de dividendos mensais: quanto a taxa tira da renda** | — | renda mensal | etf dividendos mensais | 417 | — | 91 (69,1–266,6) |
| 18/11 qua | longo | **Renda mensal e inflação: quanto reinvestir para não encolher** *(provisório)* | Ep. 5 | renda mensal | tesouro ipca | 1.009 | dHYQtxnMSrw (421) e KMIsVEOcaLM (246) | 91 (69,1–266,6) |
| 18/11 qua | short | **R$ 100 mil, 10 anos: gastar a renda ou reinvestir?** *(provisório)* | Ep. 3 (Short) | renda mensal | — (sem termo) | — | Ep. 3 (28/10) | 1,6 (0,9–3,3) |
| 19/11 qui | longo | **Bitcoin depois do 'alerta': o que mudou desde fevereiro** | — | cripto | bitcoin | 56 | JDtxzQthFlk (224) | 58 (35,4–117,2) |
| **semana 8 · 23/11–29/11** | | | | | | | | |
| 23/11 seg | short | **R$ 1.000 de renda hoje compram quanto em 10 anos?** *(provisório)* | Ep. 5 (Short) | renda mensal | — (sem termo) | — | Ep. 5 (18/11) | 1,6 (0,9–3,3) |
| 24/11 ter | longo | **Dividendos mensais com a Selic caindo: o que acontece** | — | renda mensal | dividendos mensais | 333 | — | 91 (69,1–266,6) |
| 25/11 qua | longo | **Renda todo mês com Tesouro e FII: a grade de 12 meses** *(provisório)* | Ep. 6 | renda mensal | tesouro direto | 779 | TY8oLvUt2Qg (324) e KMIsVEOcaLM (246) | 91 (69,1–266,6) |
| 25/11 qua | short | **Taxa de administração do ETF: quanto tira em 10 anos** | — | ETF e exterior | — (sem termo) | — | — | 4,3 (2,8–7,5) |
| 26/11 qui | longo | **Fundos imobiliários caíram em 2026: e a renda deles?** | — | FII | fundos imobiliarios | 167 | 8xsUtGCE-vI ('ACABOU O SONHO?') | 45 (26,1–55,9) |

**Regras:** longos às 19h; Shorts às segundas e quartas (e no dia do episódio, quando é o Short dele). Não recomendar
ativo nem citar corretora. Fora: dívida, cartão de crédito e política. Conferir as fontes antes de gravar.

## Ângulo e fontes de cada pauta

- **05/10 · LCI e LCA ou CDB: qual rende mais depois do imposto?** (v2) — Taxa equivalente com a alíquota de IR do prazo. *Conferir:* Lei 11.033/2004; prazo mínimo de LCI vigente. *Esperado:* tesouro e renda fixa, shorts, 12 meses (n = 5) · ESTIMATIVA. *Busca:* 14 termos da família. 8.488 views da Pesquisa no vitalício (sobretudo em Q1WMbZZn2Ik); 6 meses: 1.091.
- **06/10 · Fundo imobiliário ou imóvel alugado: a conta de 2026** (v2 (puxada de 12/11 para a vaga de 06/10)) — Rendimento, custo, vacância, imposto e liquidez lado a lado. *Conferir:* IFIX (B3); FipeZap; Lei 14.754/2023. *Esperado:* FII, longos, 12 meses (n = 6) · ESTIMATIVA. *Busca:* 30 termos da família. 7.643 views da Pesquisa no vitalício (sobretudo em kipRQb0ksus); 6 meses: 167.
- **07/10 · Recebeu 1% ao mês e a cota caiu 1%: quanto ganhou?** (série de renda mensal) — Short pré-estreia do Ep. 1: a conta do retorno total em 40 s. *Conferir:* IPCA 12 meses (SGS 13522). *Esperado:* renda mensal, shorts, todos os shorts (12 meses) (n = 81) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **08/10 · Tesouro IPCA+ a 7% em janeiro: quanto ganhou quem comprou** (v2) — Prestação de contas do vídeo de janeiro: preço na compra e hoje, cupons, marcação. *Conferir:* Tesouro Direto (histórico). *Esperado:* tesouro e renda fixa, longos, 12 meses (n = 5) · ESTIMATIVA. *Busca:* 32 termos da família. 26 views da Pesquisa no vitalício (sobretudo em KMIsVEOcaLM); 6 meses: 1.009.
- **12/10 · Resgatou o CDB antes de 30 dias? O IOF come o rendimento** (v2) — Tabela regressiva do IOF em 40 s. *Conferir:* Decreto 6.306/2007. *Esperado:* tesouro e renda fixa, shorts, 12 meses (n = 5) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **13/10 · Dividendos mensais com ações: como montar um calendário** (v2) — 'Todo mês' é calendário, não promessa: data com, pagamento e por que o valor varia. Sem lista de compra. *Conferir:* B3 (eventos corporativos); JCP 17,5% (LC 224/2025). *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 7 termos da família. 4.558 views da Pesquisa no vitalício (sobretudo em Y4WHQiKcv1g); 6 meses: 339.
- **14/10 · ETF que paga dividendos mensais: a renda saiu da cota?** (série de renda mensal) — Ep. 1: retorno total = cota + rendimentos; o passo a passo para refazer com o histórico da B3, sem lista de ETFs. *Conferir:* SGS 13522 (IPCA 12 meses); B3 (séries históricas e eventos corporativos); regras de 2026 da série (LC 224/2025; Lei 14.754/2023; Lei 15.270/2025; Res. CMN 5.215; fgc.org.br; Lei 11.033/2004). *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 6 termos da família. 4.558 views da Pesquisa no vitalício (sobretudo em Y4WHQiKcv1g); 6 meses: 331.
- **14/10 · Tesouro IPCA+ negativo? Calma, isso tem nome** (v2) — Marcação a mercado em 40 s; corte do longo de 08/10. *Conferir:* Tesouro Direto. *Esperado:* tesouro e renda fixa, shorts, 12 meses (n = 5) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **15/10 · Crise financeira: o gráfico de 1929, 2008 e 2020, hoje** (v2) — Revisão honesta do indicador: o que marcava, o que marca, alarmes falsos. Inclui os sinais do vídeo de novembro de 2025 (tpobf1e1OtM), que perdeu a pauta própria por falta de busca. *Conferir:* Série do indicador original. *Esperado:* crise e macro, longos, 12 meses (n = 12) · ESTIMATIVA. *Busca:* 15 termos da família. 2.538 views da Pesquisa no vitalício (sobretudo em PoY4WqA1k5Q); 6 meses: 3.
- **19/10 · FII é isento de imposto? Só se cumprir estas 3 regras** (v2) — Lei 14.754/2023: 100 cotistas ou mais, cotas em bolsa e menos de 10% das cotas; ganho na venda paga 20%. *Conferir:* Lei 14.754/2023; Lei 8.668/1993. *Esperado:* imposto e regras, shorts, vitalício (n = 11) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **20/10 · ETF de dividendos mensais com opções: de onde vem a renda** (v2 (título ou ângulo ajustado ao Ep. 1)) — Mecânica das opções cobertas, renda alta e alta limitada, comparada com ETF de dividendos comum. Guardrail do Ep. 1: a mecânica das opções cobertas é deste vídeo; o Ep. 1 só a cita em uma frase. *Conferir:* Regulamento do ETF/BDR. *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 18 termos da família. 9.538 views da Pesquisa no vitalício (sobretudo em Y4WHQiKcv1g); 6 meses: 425.
- **21/10 · Dividendos altos demais: 4 contas antes de confiar na renda** (série de renda mensal) — Ep. 2: efeito preço, payout, lucro que não se repete e histórico de 5 anos; exemplos hipotéticos. *Conferir:* RAD da CVM e RI, se usar empresa real; regras de 2026 da série (LC 224/2025; Lei 14.754/2023; Lei 15.270/2025; Res. CMN 5.215; fgc.org.br; Lei 11.033/2004). *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 2 termos da família. 41 views da Pesquisa no vitalício (sobretudo em GpdXuQipVaQ); 6 meses: 117.
- **21/10 · O dividend yield dobrou e a empresa não pagou nada a mais** (série de renda mensal) — Short do Ep. 2: a conta do efeito preço em 35 s, publicado depois do longo. *Conferir:* —. *Esperado:* renda mensal, shorts, todos os shorts (12 meses) (n = 81) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **22/10 · LCI e LCA ou CDB: a conta de 2026 com imposto e prazo** (v2) — Taxa equivalente, carência mínima, liquidez e FGC; responde '80 mil em LCI por 12 meses?' sem recomendar. *Conferir:* Lei 11.033/2004; resolução do CMN sobre prazos; fgc.org.br. *Esperado:* tesouro e renda fixa, longos, 12 meses (n = 5) · ESTIMATIVA. *Busca:* 20 termos da família. 9.184 views da Pesquisa no vitalício (sobretudo em Q1WMbZZn2Ik); 6 meses: 1.175.
- **26/10 · FGC: o que cobre e o que não cobre** (v2) — R$ 250 mil por CPF por instituição, teto de R$ 1 milhão a cada 4 anos; não cobre Tesouro, fundos e ações. *Conferir:* fgc.org.br. *Esperado:* tesouro e renda fixa, shorts, 12 meses (n = 5) · ESTIMATIVA. *Busca:* 4 termos da família. 170 views da Pesquisa no vitalício (sobretudo em uT2tgrjUvOA); 6 meses: 0.
- **27/10 · ETF de dividendos mensais ou FII: imposto e renda de cada um** (v2 (título ou ângulo ajustado ao Ep. 1)) — Comparar como cada um paga, a tributação de cada um em 2026 e a volatilidade da renda. Guardrail do Ep. 1: o imposto detalhado é deste vídeo; o Ep. 1 só tem uma tabela curta. Título trocado (o do v2 terminava em "o que sobra", como o Ep. 1); o empacotador vê os dois juntos. *Conferir:* Lei 14.754/2023; regulamentos. *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 10 termos da família. 5.748 views da Pesquisa no vitalício (sobretudo em Y4WHQiKcv1g); 6 meses: 417.
- **28/10 · Gastar ou reinvestir os dividendos: a conta de 10 anos** (série de renda mensal) — Ep. 3: R$ 100 mil a 0,6% ao mês, gastar × reinvestir × meio-termo, ano a ano. *Conferir:* só aritmética (1,006¹²⁰ = 2,05); regras de 2026 da série (LC 224/2025; Lei 14.754/2023; Lei 15.270/2025; Res. CMN 5.215; fgc.org.br; Lei 11.033/2004). *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 28 termos da família. 9.150 views da Pesquisa no vitalício (sobretudo em tbKsF2qyakU); 6 meses: 597.
- **28/10 · Quanto rende R$ 1.000 no Tesouro Selic hoje** (v2) — A conta líquida de IR em 30 s. *Conferir:* Taxa do Tesouro Selic do dia. *Esperado:* tesouro e renda fixa, shorts, 12 meses (n = 5) · ESTIMATIVA. *Busca:* 2 termos da família. 273 views da Pesquisa no vitalício (sobretudo em Q1WMbZZn2Ik); 6 meses: 43.
- **29/10 · Tesouro IPCA+ acima de 7%: o que é travar a taxa** (v2) — TROCA pelos termos recentes (era 'Recessão em 2026?', com 3 views de busca no período): o que significa comprar IPCA+ a 7% ou mais, o que acontece até o vencimento e na marcação, sem dizer se é hora de comprar. Os sinais de crise do vídeo de novembro (tpobf1e1OtM) entram no longo de 15/10. *Conferir:* Tesouro Direto (taxas e preços); IPCA (IBGE). *Esperado:* tesouro e renda fixa, longos, 12 meses (n = 5) · ESTIMATIVA. *Busca:* 32 termos da família. 26 views da Pesquisa no vitalício (sobretudo em KMIsVEOcaLM); 6 meses: 1.009.
- **02/11 · JCP em 2026: já vem com 17,5% de imposto** (v2) — Saiu do longo da v1: imposto rende 16 por longo. O JCP é retido na fonte com 17,5% (LC 224/2025). *Conferir:* LC 224/2025. *Esperado:* imposto e regras, shorts, vitalício (n = 11) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **03/11 · Tesouro Direto antes do Copom: o que olhar no IPCA+ hoje** (Copom (versão pré)) — VERSÃO PRÉ do molde (MOLDE-TESOURO-COPOM.md): o que o mercado espera (Focus de 30/10, divulgado na terça 03/11 por causa de Finados: conferir), o que observar no comunicado e as taxas da manhã de terça. Sem prever a decisão. *Conferir:* Focus (bcb.gov.br/publicacoes/focus); CSV do Tesouro Transparente e site do Tesouro Direto; datas: conferir em bcb.gov.br/controleinflacao/calendarioreunioescopom. *Esperado:* tesouro e renda fixa, longos, 12 meses (n = 5) · ESTIMATIVA. *Busca:* 34 termos da família. 26 views da Pesquisa no vitalício (sobretudo em KMIsVEOcaLM); 6 meses: 1.024.
- **04/11 · Copom hoje: 3 números para olhar no seu Tesouro** (v2 (ângulo ajustado ao pré)) — Corte do longo pré de 03/11 com as taxas da manhã de quarta (o [*_ANTES] definitivo do molde); link para o longo. Sem prever a decisão. *Conferir:* Taxas do Tesouro do dia. *Esperado:* tesouro e renda fixa, shorts, 12 meses (n = 5) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **05/11 · Dividendos mensais de R$ 1.000: quanto precisa investir** (v2 (movida de ter 03/11)) — Capital necessário em três classes, líquido de imposto. Sem indicar ativos. *Conferir:* Taxas do Tesouro; IFIX; regras de IR. *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 8 termos da família. 4.810 views da Pesquisa no vitalício (sobretudo em Y4WHQiKcv1g); 6 meses: 331.
- **07/11 · Fundos imobiliários para iniciantes: de onde vem a renda** (v2) — TROCA da v2 (era 'recompra de ações', sem nenhum termo de busca e com o assunto que menos rende): como o FII gera e distribui renda, sem indicar fundos. *Conferir:* Lei 8.668/1993; Lei 14.754/2023; IFIX (B3). *Esperado:* FII, longos, 12 meses (n = 6) · ESTIMATIVA. *Busca:* 30 termos da família. 7.643 views da Pesquisa no vitalício (sobretudo em kipRQb0ksus); 6 meses: 167.
- **09/11 · Imposto sobre dividendos acima de R$ 50 mil por mês: quem paga** (v2) — Retenção de 10% só acima de R$ 50 mil por mês da mesma empresa (Lei 15.270/2025). *Conferir:* Lei 15.270/2025. *Esperado:* imposto e regras, shorts, vitalício (n = 11) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **10/11 · Renda mensal com Tesouro Direto: juros semestrais e RendA+** (v2) — Como transformar o Tesouro em renda (cupons, RendA+), com a conta do imposto. *Conferir:* Tesouro Direto (regras dos títulos). *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 32 termos da família. 26 views da Pesquisa no vitalício (sobretudo em KMIsVEOcaLM); 6 meses: 1.009.
- **11/11 · LCI e LCA para renda mensal: a escada de vencimentos** (série de renda mensal) — Ep. 4: 12 degraus de R$ 10 mil, prazo mínimo de 6 meses, LCI × CDB líquido e FGC. Refazer o exemplo se o Copom de 04/11 mudar a Selic. *Conferir:* SGS 4389 (CDI) e 432 (Selic); regras de 2026 da série (LC 224/2025; Lei 14.754/2023; Lei 15.270/2025; Res. CMN 5.215; fgc.org.br; Lei 11.033/2004). *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 20 termos da família. 9.184 views da Pesquisa no vitalício (sobretudo em Q1WMbZZn2Ik); 6 meses: 1.175.
- **11/11 · FII ou aluguel: quanto rende R$ 100 mil em cada um** (v2) — A conta simples do rendimento líquido. *Conferir:* IFIX; índice de aluguel (FipeZap). *Esperado:* FII, shorts, vitalício (n = 30) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **14/11 · CDB prefixado ou pós-fixado: qual rende mais em 2026** (v2) — TROCA da v2 (era o cobre: commodities tem n = 1 e nenhum termo de busca): a conta prefixado × pós com a curva de juros de hoje; responde 'cdb prefixado ou pós fixado'. *Conferir:* Taxas DI futuro (B3); Lei 11.033/2004; FGC. *Esperado:* tesouro e renda fixa, longos, 12 meses (n = 5) · ESTIMATIVA. *Busca:* 15 termos da família. 4.557 views da Pesquisa no vitalício (sobretudo em 7CdwOTT7U3o); 6 meses: 5.
- **16/11 · LCI e LCA não pagam todo mês. Mas dá para fazer vencer uma por mês** (série de renda mensal) — Short do Ep. 4: o desenho dos 12 degraus. *Conferir:* Res. CMN 5.215. *Esperado:* renda mensal, shorts, todos os shorts (12 meses) (n = 81) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **17/11 · ETF de dividendos mensais: quanto a taxa tira da renda** (v2) — A conta de 10 anos com taxas diferentes; responde 'essa taxa de 1,50 é alta?'. *Conferir:* Lâminas dos ETFs. *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 10 termos da família. 5.748 views da Pesquisa no vitalício (sobretudo em Y4WHQiKcv1g); 6 meses: 417.
- **18/11 · Renda mensal e inflação: quanto reinvestir para não encolher** (série de renda mensal) — Ep. 5: R$ 1.000 hoje compram R$ 661 em 10 anos com IPCA de 4,22%; reinvestir = inflação ÷ rendimento. *Conferir:* SGS 13522; CSV do Tesouro Transparente; Focus mais recente; regras de 2026 da série (LC 224/2025; Lei 14.754/2023; Lei 15.270/2025; Res. CMN 5.215; fgc.org.br; Lei 11.033/2004). *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 32 termos da família. 26 views da Pesquisa no vitalício (sobretudo em KMIsVEOcaLM); 6 meses: 1.009.
- **18/11 · R$ 100 mil, 10 anos: gastar a renda ou reinvestir?** (série de renda mensal) — Short do Ep. 3: as duas colunas em 30 s (mesmo tema de juros compostos do Short que saiu). *Conferir:* —. *Esperado:* renda mensal, shorts, todos os shorts (12 meses) (n = 81) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **19/11 · Bitcoin depois do 'alerta': o que mudou desde fevereiro** (v2) — Os argumentos de fevereiro com os dados de hoje; 'posso perder mais do que investi?'. *Conferir:* Preço do BTC; regra de declaração (Receita). *Esperado:* cripto, longos, 12 meses (n = 4) · ESTIMATIVA. *Busca:* 57 termos da família. 43.302 views da Pesquisa no vitalício (sobretudo em YxLzaSN2a1M); 6 meses: 56.
- **23/11 · R$ 1.000 de renda hoje compram quanto em 10 anos?** (série de renda mensal) — Short do Ep. 5: a conta e a regra de bolso. *Conferir:* SGS 13522. *Esperado:* renda mensal, shorts, todos os shorts (12 meses) (n = 81) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **24/11 · Dividendos mensais com a Selic caindo: o que acontece** (v2) — O que muda nos dividendos, nos FIIs e na renda fixa quando o juro cai, com histórico. *Conferir:* BCB (Selic histórica); IFIX. *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 7 termos da família. 4.558 views da Pesquisa no vitalício (sobretudo em Y4WHQiKcv1g); 6 meses: 333.
- **25/11 · Renda todo mês com Tesouro e FII: a grade de 12 meses** (série de renda mensal) — Ep. 6: grade de 12 meses com cupons do Tesouro, FII e ações; mostra os meses vazios. Fecha a série. *Conferir:* Tesouro Direto (meses de cupom); Lei 8.668/1993; regras de 2026 da série (LC 224/2025; Lei 14.754/2023; Lei 15.270/2025; Res. CMN 5.215; fgc.org.br; Lei 11.033/2004). *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 39 termos da família. 6.814 views da Pesquisa no vitalício (sobretudo em kipRQb0ksus); 6 meses: 779.
- **25/11 · Taxa de administração do ETF: quanto tira em 10 anos** (v2) — 0,5% contra 1,5% ao ano em 10 anos; corte do longo de 17/11. *Conferir:* Lâminas. *Esperado:* ETF e exterior, shorts, vitalício (n = 12) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **26/11 · Fundos imobiliários caíram em 2026: e a renda deles?** (v2) — Cotas × rendimentos distribuídos: o que caiu e o que não caiu. *Conferir:* IFIX; relatórios gerenciais. *Esperado:* FII, longos, 12 meses (n = 6) · ESTIMATIVA. *Busca:* 30 termos da família. 7.643 views da Pesquisa no vitalício (sobretudo em kipRQb0ksus); 6 meses: 167.
