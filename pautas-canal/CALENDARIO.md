# Calendário oficial: v3 (05/10 a 29/11/2026)

**Aprovado pelo Denis em 03/10/2026, com o ajuste do mesmo dia.** Gerado por `calendario_v3.py`: parte do v2 e aplica,
na ordem, as 17 trocas aprovadas de `trocas.json` (com data, motivo e quem aprovou). Para trocar uma pauta,
acrescente uma troca no fim de `trocas.json` e rode o script. Todas as colunas estão em `CALENDARIO.csv` (a coluna
`trocas_aplicadas` diz quais trocas mexeram em cada pauta).

**Histórico:** o v2 continua em `CALENDARIO-8-SEMANAS.md` e `.csv` (gerados por `calendario_v2.py`, sem mudança) e o
v1 em `CALENDARIO-8-SEMANAS_v1.*`. A proposta está em `serie/PROPOSTA-CALENDARIO-V3.md`.

**Inscritos esperados são ESTIMATIVA, não previsão:** views intencionais medianas do assunto × inscritos por mil, nos
últimos 12 meses (`modelo.py`, `TEMAS.md`). São inscritos vitalícios de cada vídeo, que chegam ao longo de 1 a 3 meses.

## O que mudou do v2 para o v3

1. **Série de renda mensal aprovada:** 6 episódios às quartas, 19h (14/10, 21/10, 28/10, 11/11, 18/11 e 25/11).
   **Os títulos são provisórios:** ainda passam pelo empacotador e pelo teste A/B (coluna `status_titulo`).
2. **Saem as 7 pautas fora do nicho** (tabela abaixo), trocadas pelos Shorts derivados dos episódios ou pelos episódios.
3. **Copom de 03-04/11: Tesouro ANTES da decisão**, na **terça 03/11, 19h**, com a versão pré do molde. A pauta de renda
   mensal que estava na terça 03/11 vai para a quinta 05/11, que era do longo pós.
4. **Nenhuma semana com mais de 3 longos** (tabela abaixo).
5. **ETF de dividendos mensais só no Ep. 1** (ajuste de 03/10): o tema estava em 4 longos em 5 semanas. O de 06/10 vai
   para depois da série; os de 20/10 (opções) e 17/11 (taxa) viram blocos do Ep. 1. O TRXF11 volta em 20/10 e o FII
   para iniciantes passa de sáb 07/11 para ter 17/11.
6. **Total:** 22 longos e 16 Shorts (v2: 21 e 16).

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

**Semana de 26/10** (4 longos, troca T07):

| data | longo | inscritos esperados | fixo? | decisão |
|---|---|---|---|---|
| 27/10 | ETF de dividendos mensais ou fundo imobiliário: o que sobra | 91 | não | fica |
| 28/10 | Gastar ou reinvestir os dividendos: a conta de 10 anos | 91 | sim | fica |
| 29/10 | Tesouro IPCA+ acima de 7%: o que é travar a taxa | 195 | não | fica |
| 31/10 | TRXF11: o que aconteceu com a renda desde agosto | 45 | não | **sai para a fila de dezembro** |

**Semana de 09/11** (4 longos, troca T08):

| data | longo | inscritos esperados | fixo? | decisão |
|---|---|---|---|---|
| 10/11 | Renda mensal com Tesouro Direto: juros semestrais e RendA+ | 91 | não | fica |
| 11/11 | LCI e LCA para renda mensal: a escada de vencimentos | 91 | sim | fica |
| 12/11 | Fundo imobiliário ou imóvel alugado: a conta de 2026 | 45 | não | **sai para a fila de dezembro** |
| 14/11 | CDB prefixado ou pós-fixado: qual rende mais em 2026 | 195 | não | fica |

Nas duas semanas, o mais fraco é um longo de FII (45 esperados contra 91 de renda mensal e 195 de Tesouro), e
nenhuma semana seguinte até 29/11 tinha vaga. Os dois foram para a fila de dezembro e depois voltaram por outras trocas:
o FII ou imóvel de 12/11 para 06/10 (T10) e o TRXF11 de 31/10 para 20/10 (T15). A proposta sugeria tirar o CDB
prefixado de 14/11, mas pelo modelo ele é o mais forte da semana (Tesouro e renda fixa, 195).

### ETF de dividendos mensais só no Ep. 1 (briefing do Ep. 1 e ajuste de 03/10)

No v2, o ETF de dividendos mensais era tema de 4 longos em 5 semanas (06/10, 20/10, 27/10 e 17/11), mais o Ep. 1 em
14/10: saturação e canibalização do termo "etfs que pagam dividendos mensais". Agora, dentro da janela, ele só é tema
de longo no Ep. 1. O 27/10 fica porque é comparação com FII (o imposto de cada um), com título novo e guardrail.

| data | antes | depois | troca e motivo |
|---|---|---|---|
| ter 06/10 | "ETFs que pagam dividendos mensais: o que mudou em 2026" (renda mensal, 91) | **fila de dezembro** (depois da série; vira o balanço do ano) | T09: sai 8 dias antes do Ep. 1, com o mesmo termo de busca |
| ter 06/10 | (vaga) | **"Fundo imobiliário ou imóvel alugado: a conta de 2026"** (FII, 45), que tinha saído de 12/11 pela regra | T10: o melhor da fila sem ETF de dividendos. O canal fez "Fundos Imobiliários ou Imóveis" em 26/06/2026 (14 inscritos): o ângulo de 2026 (Lei 14.754/2023, vacância, liquidez) tem de ficar claro no título final |
| qua 14/10 | Ep. 1 | **Ep. 1 com 2 blocos a mais** | T14: opções cobertas: como o prêmio vira renda e por que a alta fica limitada (era o 20/10); taxa: a conta de 10 anos com 0,5% e 1,5% ao ano e onde ler a taxa na lâmina (era o 17/11). O que cada bloco traz está no briefing do Ep. 1, seção "Blocos absorvidos (decisão de 03/10)" |
| ter 20/10 | "ETF de dividendos mensais com opções: de onde vem a renda" (91) | **"TRXF11: o que aconteceu com a renda desde agosto"** (FII, 45) | T14 + T15: as opções viram bloco do Ep. 1; o TRXF11 volta da fila ("trxf11" é o termo de investimento mais buscado do canal nos últimos 6 meses, 1.516 views da Pesquisa) |
| ter 27/10 | "ETF de dividendos mensais ou fundo imobiliário: o que sobra" | **"ETF de dividendos mensais ou FII: imposto e renda de cada um"** | T11 + T12: o título do v2 usava "o que sobra", como a promessa do Ep. 1; o imposto detalhado é deste vídeo |
| sáb 07/11 | "Fundos imobiliários para iniciantes: de onde vem a renda" (45) | **vaga** (a semana de 02/11 fica com 2 longos: o Copom e a renda mensal) | T16 |
| ter 17/11 | "ETF de dividendos mensais: quanto a taxa tira da renda" (91) | **"Fundos imobiliários para iniciantes: de onde vem a renda"** (movido de 07/11) | T14 + T16: a taxa vira bloco do Ep. 1. A fila de dezembro só tinha o ETF de dividendos, que não pode voltar; mover não muda o total, mas põe o vídeo na terça (o melhor dia, 10,4 inscritos por mil, contra sábado sem histórico) e tira a semana de 16/11 de 89 abaixo da meta semanal |
| qua 25/11 | Short "Taxa de administração do ETF" (corte do 17/11) | o mesmo Short, agora corte do bloco de taxa do Ep. 1 | T17 |

**Atenção:** com o TRXF11 em 20/10 e o FII para iniciantes em 17/11, há 4 longos de FII na janela (06/10, 20/10, 17/11 e
26/11), nenhum na mesma semana de outro.

### Fila de dezembro

- ETFs que pagam dividendos mensais: o que mudou em 2026 (longo, renda mensal, 91 esperados; era 06/10; trocas T09)

### Trocas aprovadas (`trocas.json`)

| troca | aprovada por | operação | o quê | efeito no esperado das 8 semanas | motivo |
|---|---|---|---|---|---|
| T01 | Denis Miyabara | entra | 07/10 Recebeu 1% ao mês e a cota caiu 1%: quanto ganhou?; 14/10 ETF que paga dividendos mensais: a renda saiu da cota?; 21/10 Dividendos altos demais: 4 contas antes de confiar na renda; 21/10 O dividend yield dobrou e a empresa não pagou nada a mais; 28/10 Gastar ou reinvestir os dividendos: a conta de 10 anos; 11/11 LCI e LCA para renda mensal: a escada de vencimentos; 16/11 LCI e LCA não pagam todo mês. Mas dá para fazer vencer uma por mês; 18/11 Renda mensal e inflação: quanto reinvestir para não encolher; 18/11 R$ 100 mil, 10 anos: gastar a renda ou reinvestir?; 23/11 R$ 1.000 de renda hoje compram quanto em 10 anos?; 25/11 Renda todo mês com Tesouro e FII: a grade de 12 meses (de: serie) | +554 | Série de renda mensal aprovada (serie/SERIE-RENDA-MENSAL.md): 6 episódios às quartas e os Shorts derivados. Títulos provisórios até o empacotador e o teste A/B. |
| T02 | Denis Miyabara | sai | 07/10 Como juntar 1 milhão de reais com R$ 1.000 por mês; 21/10 Casal que investe junto: a conversa que vem antes do dinheiro; 16/11 Perfil de investidor: 3 perguntas antes de investir; 18/11 Juros compostos: por que 1 centavo dobrando todo dia não existe; 21/11 Bolha da IA: o que dizem os números; 23/11 Reserva de emergência: onde deixar e onde não deixar; 28/11 Tesouro Direto na reserva de emergência: Selic, CDB ou conta → removida | −258 | Fora do nicho (serie/PROPOSTA-CALENDARIO-V3.md): as vagas vão para os Shorts dos episódios ou para os próprios episódios. |
| T03 | Denis Miyabara | sai | 05/11 Tesouro Direto após o Copom: o que muda no IPCA+ e prefixado → removida | −195 | Tesouro ANTES do Copom: o longo pós de quinta 05/11 dá lugar à versão pré na terça 03/11. |
| T04 | Denis Miyabara | move | Dividendos mensais de R$ 1.000: quanto precisa investir: 03/11 → 05/11 | +0 | A terça 03/11 passa a ser do Tesouro pré-Copom; a pauta de renda mensal vai para a quinta, que ficou livre. |
| T05 | Denis Miyabara | entra | 03/11 Tesouro Direto antes do Copom: o que olhar no IPCA+ hoje (de: copom) | +195 | Tesouro pré-Copom na terça 03/11, 19h (02/11 é Finados; o Focus de 30/10 só sai na terça). Versão pré do serie/MOLDE-TESOURO-COPOM.md. |
| T06 | Denis Miyabara | edita | 04/11 Copom hoje: 3 números para olhar no seu Tesouro | +0 | Com o longo pré na terça, o Short de quarta vira corte dele. |
| T07 | Denis Miyabara (regra: no máximo 3 longos por semana) | sai | 31/10 TRXF11: o que aconteceu com a renda desde agosto → fila de dezembro | −45 | Semana de 26/10 com 4 longos: sai o de menor esperado pelo modelo (FII, 45); nenhuma semana seguinte até 29/11 tem vaga. |
| T08 | Denis Miyabara (regra: no máximo 3 longos por semana) | sai | 12/11 Fundo imobiliário ou imóvel alugado: a conta de 2026 → fila de dezembro | −45 | Semana de 09/11 com 4 longos: sai o de menor esperado pelo modelo (FII, 45); nenhuma semana seguinte até 29/11 tem vaga. |
| T09 | coordenação (briefing do Ep. 1), dentro da aprovação do v3 | sai | 06/10 ETFs que pagam dividendos mensais: o que mudou em 2026 → fila de dezembro | −91 | Canibalização: sai 8 dias antes do Ep. 1, com o mesmo tema e o mesmo termo de busca (briefings/2026-10-14-etf-dividendos-mensais-briefing.md). Vai para depois da série. |
| T10 | coordenação (briefing do Ep. 1), dentro da aprovação do v3 | entra | 06/10 Fundo imobiliário ou imóvel alugado: a conta de 2026 (de: fila) | +45 | A vaga de 06/10 recebe o melhor da fila sem ETF de dividendos (o TRXF11 repetiria o vídeo de 29/09 sobre o fundo). |
| T11 | coordenação (briefing do Ep. 1), dentro da aprovação do v3 | titulo | 27/10: "ETF de dividendos mensais ou fundo imobiliário: o que sobra" → "ETF de dividendos mensais ou FII: imposto e renda de cada um" | +0 | O título do v2 terminava em "o que sobra", como a promessa do Ep. 1. |
| T12 | coordenação (briefing do Ep. 1), dentro da aprovação do v3 | edita | 27/10 ETF de dividendos mensais ou FII: imposto e renda de cada um | +0 | Guardrail do briefing do Ep. 1 para o 27/10. |
| T13 | coordenação (briefing do Ep. 1), dentro da aprovação do v3 | edita | 11/11 FII ou aluguel: quanto rende R$ 100 mil em cada um | +0 | O longo de FII ou imóvel foi para 06/10; o Short de 11/11 vira corte dele. |
| T14 | Denis Miyabara (ajuste do v3) | absorve | 20/10 ETF de dividendos mensais com opções: de onde vem a renda; 17/11 ETF de dividendos mensais: quanto a taxa tira da renda → blocos do 14/10 | −182 | Saturação: o ETF de dividendos mensais estava em 4 longos em 5 semanas. Os longos de 20/10 (opções) e 17/11 (taxa) viram blocos do Ep. 1. |
| T15 | Denis Miyabara (ajuste do v3) | entra | 20/10 TRXF11: o que aconteceu com a renda desde agosto (de: fila) | +45 | O TRXF11 volta da fila de dezembro para a vaga de 20/10: "trxf11" é o termo de investimento mais buscado do canal nos últimos 6 meses. |
| T16 | Denis Miyabara (ajuste do v3: FII de 07/11 ou o melhor da fila); escolha pelo modelo | move | Fundos imobiliários para iniciantes: de onde vem a renda: 07/11 → 17/11 | +0 | A vaga de 17/11 vai para o FII de 07/11: a fila de dezembro só tem o ETF de dividendos mensais, que não pode voltar para a janela. Mover não muda o total, mas tira o vídeo do sábado (dia sem histórico de longos) e o põe na terça (10,4 inscritos por mil, o melhor dia), e equilibra as semanas: a de 16/11 ficaria 89 abaixo da meta semanal sem ele; a de 02/11 fica acima mesmo com 2 longos. |
| T17 | Denis Miyabara (ajuste do v3) | edita | 25/11 Taxa de administração do ETF: quanto tira em 10 anos | +0 | O longo de 17/11 (taxa) foi absorvido pelo Ep. 1; o Short de 25/11 vira corte do bloco de taxa do Ep. 1. |

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
| longos / Shorts nas 8 semanas | 21 / 16 | 22 / 16 | +1 / +0 |
| inscritos esperados (central) | 2.293 | **2.316** | **+23** |
| faixa p25–p75 | 1.401 a 3.964 | 1.481 a 4.474 | |

A conta, troca por troca, está na coluna "efeito" da tabela de trocas acima (2.293 do v2 + a soma dos efeitos
= 2.316).

### Contra a meta mensal (META.md)

Mesma conta do `META.md`: inscritos líquidos do mês = catálogo (449) + vídeos novos − perdas
(350). Os vídeos novos entram com a defasagem do `meta.py` (60% no mês da publicação, 25% no seguinte e
15% no outro). Outubro conta só os vídeos da janela (de 05/10 em diante).

| mês | longos | Shorts | inscritos esperados dos vídeos do mês (vitalício) | entram no mês (com defasagem) | líquidos estimados | meta (META.md) | diferença |
|---|---|---|---|---|---|---|---|
| 10/26 | 11 | 8 | 1.202 (749–2.181) | 721 | **821** (549–1.409) | 573 | +249 |
| 11/26 | 11 | 8 | 1.114 (733–2.293) | 969 | **1.069** (727–2.021) | 925 | +144 |

**Leitura:**
- Na estimativa central, outubro e novembro ficam acima da
  meta mensal. Na faixa p25 (pessimista), outubro e novembro
  ficam abaixo.
- Outubro tem 11 longos na janela, mais o de 01/10 já publicado; o plano do `META.md` contava 9 (rampa de 75%).
- Uma parte dos inscritos de novembro chega em dezembro e janeiro (defasagem). Não conta aqui, mas entra na meta de
  dezembro (1.107).
- **Cenário pessimista:** se renda mensal e Tesouro renderem como a mediana geral dos longos (42 por vídeo, e
  não 91 e 195), as 8 semanas ficam em ~1.015.
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
| 19/10–25/10 | 3 | 2 | 294 | **338** (205–542) | 182 | +156 |
| 26/10–01/11 | 3 | 2 | 336 | **382** (249–751) | 182 | +200 |
| 02/11–08/11 | 2 | 2 | 338 | **293** (180–486) | 242 | +51 |
| 09/11–15/11 | 3 | 2 | 344 | **389** (253–761) | 242 | +148 |
| 16/11–22/11 | 3 | 2 | 205 | **198** (132–446) | 242 | −44 |
| 23/11–29/11 | 3 | 2 | 338 | **233** (168–600) | 242 | −8 |
| **8 semanas** | 22 | 16 | 2.293 | **2.316** | 1.695 | +621 |

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
| 14/10 qua | longo | **ETF que paga dividendos mensais: a renda saiu da cota?** *(provisório)* | Ep. 1 | renda mensal | etfs que pagam dividendos mensais | 331 | Fb0l4KEq27o (637) e c9Obo6F5_NU; absorve 20/10 "ETF de dividendos mensais com opções: de onde vem a renda" e 17/11 "ETF de dividendos mensais: quanto a taxa tira da renda" | 91 (69,1–266,6) |
| 14/10 qua | short | **Tesouro IPCA+ negativo? Calma, isso tem nome** | — | tesouro e renda fixa | — (sem termo) | — | — | 2,2 (2,1–3,1) |
| 15/10 qui | longo | **Crise financeira: o gráfico de 1929, 2008 e 2020, hoje** | — | crise e macro | crise financeira | 3 | IcN3m7whpl8 (357) | 52 (17,4–75,5) |
| **semana 3 · 19/10–25/10** | | | | | | | | |
| 19/10 seg | short | **FII é isento de imposto? Só se cumprir estas 3 regras** | — | imposto e regras | — (sem termo) | — | — | 4,1 (2,7–4,9) |
| 20/10 ter | longo | **TRXF11: o que aconteceu com a renda desde agosto** | — | FII | trxf11 | 1.553 | XOqLAz3dkV4 e o vídeo anterior de TRXF11 (21 e 33 inscritos) | 45 (26,1–55,9) |
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
| **semana 6 · 09/11–15/11** | | | | | | | | |
| 09/11 seg | short | **Imposto sobre dividendos acima de R$ 50 mil por mês: quem paga** | — | imposto e regras | — (sem termo) | — | — | 4,1 (2,7–4,9) |
| 10/11 ter | longo | **Renda mensal com Tesouro Direto: juros semestrais e RendA+** | — | renda mensal | tesouro direto | 1.009 | — | 91 (69,1–266,6) |
| 11/11 qua | longo | **LCI e LCA para renda mensal: a escada de vencimentos** *(provisório)* | Ep. 4 | renda mensal | lci e lca | 1.175 | Q1WMbZZn2Ik (Short) e dHYQtxnMSrw (421) | 91 (69,1–266,6) |
| 11/11 qua | short | **FII ou aluguel: quanto rende R$ 100 mil em cada um** | — | FII | — (sem termo) | — | longo de 06/10 (FII ou imóvel alugado) | 7,6 (5,7–11,3) |
| 14/11 sáb | longo | **CDB prefixado ou pós-fixado: qual rende mais em 2026** | — | tesouro e renda fixa | cdb prefixado | 5 | 7CdwOTT7U3o (CDB prefixado, 2018: 3.928 views da Pesquisa) | 195 (106,2–211,5) |
| **semana 7 · 16/11–22/11** | | | | | | | | |
| 16/11 seg | short | **LCI e LCA não pagam todo mês. Mas dá para fazer vencer uma por mês** *(provisório)* | Ep. 4 (Short) | renda mensal | — (sem termo) | — | Ep. 4 (11/11) | 1,6 (0,9–3,3) |
| 17/11 ter | longo | **Fundos imobiliários para iniciantes: de onde vem a renda** | — | FII | fundos imobiliarios | 167 | kipRQb0ksus (busca de FII, 2023) | 45 (26,1–55,9) |
| 18/11 qua | longo | **Renda mensal e inflação: quanto reinvestir para não encolher** *(provisório)* | Ep. 5 | renda mensal | tesouro ipca | 1.009 | dHYQtxnMSrw (421) e KMIsVEOcaLM (246) | 91 (69,1–266,6) |
| 18/11 qua | short | **R$ 100 mil, 10 anos: gastar a renda ou reinvestir?** *(provisório)* | Ep. 3 (Short) | renda mensal | — (sem termo) | — | Ep. 3 (28/10) | 1,6 (0,9–3,3) |
| 19/11 qui | longo | **Bitcoin depois do 'alerta': o que mudou desde fevereiro** | — | cripto | bitcoin | 56 | JDtxzQthFlk (224) | 58 (35,4–117,2) |
| **semana 8 · 23/11–29/11** | | | | | | | | |
| 23/11 seg | short | **R$ 1.000 de renda hoje compram quanto em 10 anos?** *(provisório)* | Ep. 5 (Short) | renda mensal | — (sem termo) | — | Ep. 5 (18/11) | 1,6 (0,9–3,3) |
| 24/11 ter | longo | **Dividendos mensais com a Selic caindo: o que acontece** | — | renda mensal | dividendos mensais | 333 | — | 91 (69,1–266,6) |
| 25/11 qua | longo | **Renda todo mês com Tesouro e FII: a grade de 12 meses** *(provisório)* | Ep. 6 | renda mensal | tesouro direto | 779 | TY8oLvUt2Qg (324) e KMIsVEOcaLM (246) | 91 (69,1–266,6) |
| 25/11 qua | short | **Taxa de administração do ETF: quanto tira em 10 anos** | — | ETF e exterior | — (sem termo) | — | Ep. 1 (14/10), bloco de taxa | 4,3 (2,8–7,5) |
| 26/11 qui | longo | **Fundos imobiliários caíram em 2026: e a renda deles?** | — | FII | fundos imobiliarios | 167 | 8xsUtGCE-vI ('ACABOU O SONHO?') | 45 (26,1–55,9) |

**Regras:** longos às 19h; Shorts às segundas e quartas (e no dia do episódio, quando é o Short dele). Não recomendar
ativo nem citar corretora. Fora: dívida, cartão de crédito e política. Conferir as fontes antes de gravar.

## Ângulo e fontes de cada pauta

- **05/10 · LCI e LCA ou CDB: qual rende mais depois do imposto?** (v2) — Taxa equivalente com a alíquota de IR do prazo. *Conferir:* Lei 11.033/2004; prazo mínimo de LCI vigente. *Esperado:* tesouro e renda fixa, shorts, 12 meses (n = 5) · ESTIMATIVA. *Busca:* 14 termos da família. 8.488 views da Pesquisa no vitalício (sobretudo em Q1WMbZZn2Ik); 6 meses: 1.091.
- **06/10 · Fundo imobiliário ou imóvel alugado: a conta de 2026** (v2 (voltou da fila em 06/10; era 12/11)) — Rendimento, custo, vacância, imposto e liquidez lado a lado. *Conferir:* IFIX (B3); FipeZap; Lei 14.754/2023. *Esperado:* FII, longos, 12 meses (n = 6) · ESTIMATIVA. *Busca:* 30 termos da família. 7.643 views da Pesquisa no vitalício (sobretudo em kipRQb0ksus); 6 meses: 167.
- **07/10 · Recebeu 1% ao mês e a cota caiu 1%: quanto ganhou?** (série de renda mensal) — Short pré-estreia do Ep. 1: a conta do retorno total em 40 s. *Conferir:* IPCA 12 meses (SGS 13522). *Esperado:* renda mensal, shorts, todos os shorts (12 meses) (n = 81) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **08/10 · Tesouro IPCA+ a 7% em janeiro: quanto ganhou quem comprou** (v2) — Prestação de contas do vídeo de janeiro: preço na compra e hoje, cupons, marcação. *Conferir:* Tesouro Direto (histórico). *Esperado:* tesouro e renda fixa, longos, 12 meses (n = 5) · ESTIMATIVA. *Busca:* 32 termos da família. 26 views da Pesquisa no vitalício (sobretudo em KMIsVEOcaLM); 6 meses: 1.009.
- **12/10 · Resgatou o CDB antes de 30 dias? O IOF come o rendimento** (v2) — Tabela regressiva do IOF em 40 s. *Conferir:* Decreto 6.306/2007. *Esperado:* tesouro e renda fixa, shorts, 12 meses (n = 5) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **13/10 · Dividendos mensais com ações: como montar um calendário** (v2) — 'Todo mês' é calendário, não promessa: data com, pagamento e por que o valor varia. Sem lista de compra. *Conferir:* B3 (eventos corporativos); JCP 17,5% (LC 224/2025). *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 7 termos da família. 4.558 views da Pesquisa no vitalício (sobretudo em Y4WHQiKcv1g); 6 meses: 339.
- **14/10 · ETF que paga dividendos mensais: a renda saiu da cota?** (série de renda mensal) — Ep. 1: retorno total = cota + rendimentos; o passo a passo para refazer com o histórico da B3, sem lista de ETFs. BLOCOS ABSORVIDOS (T14): opções cobertas: como o prêmio vira renda e por que a alta fica limitada (era o 20/10); taxa: a conta de 10 anos com 0,5% e 1,5% ao ano e onde ler a taxa na lâmina (era o 17/11). *Conferir:* SGS 13522 (IPCA 12 meses); B3 (séries históricas e eventos corporativos); regras de 2026 da série (LC 224/2025; Lei 14.754/2023; Lei 15.270/2025; Res. CMN 5.215; fgc.org.br; Lei 11.033/2004). *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 6 termos da família. 4.558 views da Pesquisa no vitalício (sobretudo em Y4WHQiKcv1g); 6 meses: 331.
- **14/10 · Tesouro IPCA+ negativo? Calma, isso tem nome** (v2) — Marcação a mercado em 40 s; corte do longo de 08/10. *Conferir:* Tesouro Direto. *Esperado:* tesouro e renda fixa, shorts, 12 meses (n = 5) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **15/10 · Crise financeira: o gráfico de 1929, 2008 e 2020, hoje** (v2) — Revisão honesta do indicador: o que marcava, o que marca, alarmes falsos. Inclui os sinais do vídeo de novembro de 2025 (tpobf1e1OtM), que perdeu a pauta própria por falta de busca. *Conferir:* Série do indicador original. *Esperado:* crise e macro, longos, 12 meses (n = 12) · ESTIMATIVA. *Busca:* 15 termos da família. 2.538 views da Pesquisa no vitalício (sobretudo em PoY4WqA1k5Q); 6 meses: 3.
- **19/10 · FII é isento de imposto? Só se cumprir estas 3 regras** (v2) — Lei 14.754/2023: 100 cotistas ou mais, cotas em bolsa e menos de 10% das cotas; ganho na venda paga 20%. *Conferir:* Lei 14.754/2023; Lei 8.668/1993. *Esperado:* imposto e regras, shorts, vitalício (n = 11) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **20/10 · TRXF11: o que aconteceu com a renda desde agosto** (v2 (voltou da fila em 20/10; era 31/10)) — TROCA pelos termos recentes (era 'ETF de bitcoin', com 21 views de busca no período): 'trxf11' é o termo de investimento mais buscado do canal nos últimos 6 meses (1.516). Acompanhamento neutro dos números do fundo (rendimento, vacância, cota), sem dizer se compra ou vende. *Conferir:* Relatórios gerenciais e informes do fundo (B3/CVM). *Esperado:* FII, longos, 12 meses (n = 6) · ESTIMATIVA. *Busca:* 7 termos da família. 0 views da Pesquisa no vitalício (sobretudo em XOqLAz3dkV4); 6 meses: 1.553.
- **21/10 · Dividendos altos demais: 4 contas antes de confiar na renda** (série de renda mensal) — Ep. 2: efeito preço, payout, lucro que não se repete e histórico de 5 anos; exemplos hipotéticos. *Conferir:* RAD da CVM e RI, se usar empresa real; regras de 2026 da série (LC 224/2025; Lei 14.754/2023; Lei 15.270/2025; Res. CMN 5.215; fgc.org.br; Lei 11.033/2004). *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 2 termos da família. 41 views da Pesquisa no vitalício (sobretudo em GpdXuQipVaQ); 6 meses: 117.
- **21/10 · O dividend yield dobrou e a empresa não pagou nada a mais** (série de renda mensal) — Short do Ep. 2: a conta do efeito preço em 35 s, publicado depois do longo. *Conferir:* —. *Esperado:* renda mensal, shorts, todos os shorts (12 meses) (n = 81) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **22/10 · LCI e LCA ou CDB: a conta de 2026 com imposto e prazo** (v2) — Taxa equivalente, carência mínima, liquidez e FGC; responde '80 mil em LCI por 12 meses?' sem recomendar. *Conferir:* Lei 11.033/2004; resolução do CMN sobre prazos; fgc.org.br. *Esperado:* tesouro e renda fixa, longos, 12 meses (n = 5) · ESTIMATIVA. *Busca:* 20 termos da família. 9.184 views da Pesquisa no vitalício (sobretudo em Q1WMbZZn2Ik); 6 meses: 1.175.
- **26/10 · FGC: o que cobre e o que não cobre** (v2) — R$ 250 mil por CPF por instituição, teto de R$ 1 milhão a cada 4 anos; não cobre Tesouro, fundos e ações. *Conferir:* fgc.org.br. *Esperado:* tesouro e renda fixa, shorts, 12 meses (n = 5) · ESTIMATIVA. *Busca:* 4 termos da família. 170 views da Pesquisa no vitalício (sobretudo em uT2tgrjUvOA); 6 meses: 0.
- **27/10 · ETF de dividendos mensais ou FII: imposto e renda de cada um** (v2 (título trocado)) — Comparar como cada um paga, a tributação de cada um em 2026 e a volatilidade da renda. Guardrail do Ep. 1: o imposto detalhado é deste vídeo; o Ep. 1 só tem uma tabela curta. O empacotador vê os dois títulos juntos. *Conferir:* Lei 14.754/2023; regulamentos. *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 10 termos da família. 5.748 views da Pesquisa no vitalício (sobretudo em Y4WHQiKcv1g); 6 meses: 417.
- **28/10 · Gastar ou reinvestir os dividendos: a conta de 10 anos** (série de renda mensal) — Ep. 3: R$ 100 mil a 0,6% ao mês, gastar × reinvestir × meio-termo, ano a ano. *Conferir:* só aritmética (1,006¹²⁰ = 2,05); regras de 2026 da série (LC 224/2025; Lei 14.754/2023; Lei 15.270/2025; Res. CMN 5.215; fgc.org.br; Lei 11.033/2004). *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 28 termos da família. 9.150 views da Pesquisa no vitalício (sobretudo em tbKsF2qyakU); 6 meses: 597.
- **28/10 · Quanto rende R$ 1.000 no Tesouro Selic hoje** (v2) — A conta líquida de IR em 30 s. *Conferir:* Taxa do Tesouro Selic do dia. *Esperado:* tesouro e renda fixa, shorts, 12 meses (n = 5) · ESTIMATIVA. *Busca:* 2 termos da família. 273 views da Pesquisa no vitalício (sobretudo em Q1WMbZZn2Ik); 6 meses: 43.
- **29/10 · Tesouro IPCA+ acima de 7%: o que é travar a taxa** (v2) — TROCA pelos termos recentes (era 'Recessão em 2026?', com 3 views de busca no período): o que significa comprar IPCA+ a 7% ou mais, o que acontece até o vencimento e na marcação, sem dizer se é hora de comprar. Os sinais de crise do vídeo de novembro (tpobf1e1OtM) entram no longo de 15/10. *Conferir:* Tesouro Direto (taxas e preços); IPCA (IBGE). *Esperado:* tesouro e renda fixa, longos, 12 meses (n = 5) · ESTIMATIVA. *Busca:* 32 termos da família. 26 views da Pesquisa no vitalício (sobretudo em KMIsVEOcaLM); 6 meses: 1.009.
- **02/11 · JCP em 2026: já vem com 17,5% de imposto** (v2) — Saiu do longo da v1: imposto rende 16 por longo. O JCP é retido na fonte com 17,5% (LC 224/2025). *Conferir:* LC 224/2025. *Esperado:* imposto e regras, shorts, vitalício (n = 11) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **03/11 · Tesouro Direto antes do Copom: o que olhar no IPCA+ hoje** (Copom (versão pré)) — VERSÃO PRÉ do molde (MOLDE-TESOURO-COPOM.md): o que o mercado espera (Focus de 30/10, divulgado na terça 03/11 por causa de Finados: conferir), o que observar no comunicado e as taxas da manhã de terça. Sem prever a decisão. *Conferir:* Focus (bcb.gov.br/publicacoes/focus); CSV do Tesouro Transparente e site do Tesouro Direto; datas: conferir em bcb.gov.br/controleinflacao/calendarioreunioescopom. *Esperado:* tesouro e renda fixa, longos, 12 meses (n = 5) · ESTIMATIVA. *Busca:* 34 termos da família. 26 views da Pesquisa no vitalício (sobretudo em KMIsVEOcaLM); 6 meses: 1.024.
- **04/11 · Copom hoje: 3 números para olhar no seu Tesouro** (v2) — Corte do longo pré de 03/11 com as taxas da manhã de quarta (o [*_ANTES] definitivo do molde); link para o longo. Sem prever a decisão. *Conferir:* Taxas do Tesouro do dia. *Esperado:* tesouro e renda fixa, shorts, 12 meses (n = 5) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **05/11 · Dividendos mensais de R$ 1.000: quanto precisa investir** (v2 (movida de 03/11)) — Capital necessário em três classes, líquido de imposto. Sem indicar ativos. *Conferir:* Taxas do Tesouro; IFIX; regras de IR. *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 8 termos da família. 4.810 views da Pesquisa no vitalício (sobretudo em Y4WHQiKcv1g); 6 meses: 331.
- **09/11 · Imposto sobre dividendos acima de R$ 50 mil por mês: quem paga** (v2) — Retenção de 10% só acima de R$ 50 mil por mês da mesma empresa (Lei 15.270/2025). *Conferir:* Lei 15.270/2025. *Esperado:* imposto e regras, shorts, vitalício (n = 11) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **10/11 · Renda mensal com Tesouro Direto: juros semestrais e RendA+** (v2) — Como transformar o Tesouro em renda (cupons, RendA+), com a conta do imposto. *Conferir:* Tesouro Direto (regras dos títulos). *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 32 termos da família. 26 views da Pesquisa no vitalício (sobretudo em KMIsVEOcaLM); 6 meses: 1.009.
- **11/11 · LCI e LCA para renda mensal: a escada de vencimentos** (série de renda mensal) — Ep. 4: 12 degraus de R$ 10 mil, prazo mínimo de 6 meses, LCI × CDB líquido e FGC. Refazer o exemplo se o Copom de 04/11 mudar a Selic. *Conferir:* SGS 4389 (CDI) e 432 (Selic); regras de 2026 da série (LC 224/2025; Lei 14.754/2023; Lei 15.270/2025; Res. CMN 5.215; fgc.org.br; Lei 11.033/2004). *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 20 termos da família. 9.184 views da Pesquisa no vitalício (sobretudo em Q1WMbZZn2Ik); 6 meses: 1.175.
- **11/11 · FII ou aluguel: quanto rende R$ 100 mil em cada um** (v2) — A conta simples do rendimento líquido. *Conferir:* IFIX; índice de aluguel (FipeZap). *Esperado:* FII, shorts, vitalício (n = 30) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **14/11 · CDB prefixado ou pós-fixado: qual rende mais em 2026** (v2) — TROCA da v2 (era o cobre: commodities tem n = 1 e nenhum termo de busca): a conta prefixado × pós com a curva de juros de hoje; responde 'cdb prefixado ou pós fixado'. *Conferir:* Taxas DI futuro (B3); Lei 11.033/2004; FGC. *Esperado:* tesouro e renda fixa, longos, 12 meses (n = 5) · ESTIMATIVA. *Busca:* 15 termos da família. 4.557 views da Pesquisa no vitalício (sobretudo em 7CdwOTT7U3o); 6 meses: 5.
- **16/11 · LCI e LCA não pagam todo mês. Mas dá para fazer vencer uma por mês** (série de renda mensal) — Short do Ep. 4: o desenho dos 12 degraus. *Conferir:* Res. CMN 5.215. *Esperado:* renda mensal, shorts, todos os shorts (12 meses) (n = 81) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **17/11 · Fundos imobiliários para iniciantes: de onde vem a renda** (v2 (movida de 07/11)) — TROCA da v2 (era 'recompra de ações', sem nenhum termo de busca e com o assunto que menos rende): como o FII gera e distribui renda, sem indicar fundos. *Conferir:* Lei 8.668/1993; Lei 14.754/2023; IFIX (B3). *Esperado:* FII, longos, 12 meses (n = 6) · ESTIMATIVA. *Busca:* 30 termos da família. 7.643 views da Pesquisa no vitalício (sobretudo em kipRQb0ksus); 6 meses: 167.
- **18/11 · Renda mensal e inflação: quanto reinvestir para não encolher** (série de renda mensal) — Ep. 5: R$ 1.000 hoje compram R$ 661 em 10 anos com IPCA de 4,22%; reinvestir = inflação ÷ rendimento. *Conferir:* SGS 13522; CSV do Tesouro Transparente; Focus mais recente; regras de 2026 da série (LC 224/2025; Lei 14.754/2023; Lei 15.270/2025; Res. CMN 5.215; fgc.org.br; Lei 11.033/2004). *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 32 termos da família. 26 views da Pesquisa no vitalício (sobretudo em KMIsVEOcaLM); 6 meses: 1.009.
- **18/11 · R$ 100 mil, 10 anos: gastar a renda ou reinvestir?** (série de renda mensal) — Short do Ep. 3: as duas colunas em 30 s (mesmo tema de juros compostos do Short que saiu). *Conferir:* —. *Esperado:* renda mensal, shorts, todos os shorts (12 meses) (n = 81) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **19/11 · Bitcoin depois do 'alerta': o que mudou desde fevereiro** (v2) — Os argumentos de fevereiro com os dados de hoje; 'posso perder mais do que investi?'. *Conferir:* Preço do BTC; regra de declaração (Receita). *Esperado:* cripto, longos, 12 meses (n = 4) · ESTIMATIVA. *Busca:* 57 termos da família. 43.302 views da Pesquisa no vitalício (sobretudo em YxLzaSN2a1M); 6 meses: 56.
- **23/11 · R$ 1.000 de renda hoje compram quanto em 10 anos?** (série de renda mensal) — Short do Ep. 5: a conta e a regra de bolso. *Conferir:* SGS 13522. *Esperado:* renda mensal, shorts, todos os shorts (12 meses) (n = 81) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **24/11 · Dividendos mensais com a Selic caindo: o que acontece** (v2) — O que muda nos dividendos, nos FIIs e na renda fixa quando o juro cai, com histórico. *Conferir:* BCB (Selic histórica); IFIX. *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 7 termos da família. 4.558 views da Pesquisa no vitalício (sobretudo em Y4WHQiKcv1g); 6 meses: 333.
- **25/11 · Renda todo mês com Tesouro e FII: a grade de 12 meses** (série de renda mensal) — Ep. 6: grade de 12 meses com cupons do Tesouro, FII e ações; mostra os meses vazios. Fecha a série. *Conferir:* Tesouro Direto (meses de cupom); Lei 8.668/1993; regras de 2026 da série (LC 224/2025; Lei 14.754/2023; Lei 15.270/2025; Res. CMN 5.215; fgc.org.br; Lei 11.033/2004). *Esperado:* renda mensal, longos, 12 meses (n = 7) · ESTIMATIVA. *Busca:* 39 termos da família. 6.814 views da Pesquisa no vitalício (sobretudo em kipRQb0ksus); 6 meses: 779.
- **25/11 · Taxa de administração do ETF: quanto tira em 10 anos** (v2) — 0,5% contra 1,5% ao ano em 10 anos; corte do bloco de taxa do Ep. 1 (14/10). *Conferir:* Lâminas. *Esperado:* ETF e exterior, shorts, vitalício (n = 12) · ESTIMATIVA. *Busca:* sem termo associado (Short de alcance).
- **26/11 · Fundos imobiliários caíram em 2026: e a renda deles?** (v2) — Cotas × rendimentos distribuídos: o que caiu e o que não caiu. *Conferir:* IFIX; relatórios gerenciais. *Esperado:* FII, longos, 12 meses (n = 6) · ESTIMATIVA. *Busca:* 30 termos da família. 7.643 views da Pesquisa no vitalício (sobretudo em kipRQb0ksus); 6 meses: 167.
