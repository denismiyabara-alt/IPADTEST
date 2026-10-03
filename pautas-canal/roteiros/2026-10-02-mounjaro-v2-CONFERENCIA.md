---
roteiro: pautas-canal/roteiros/2026-10-02-mounjaro-v2-teleprompter.md (v2.1, commit 8c6443c)
conferido_em: 2026-10-03 (madrugada), pra gravação de amanhã
data_base_mercado: fechamento de sex 02/10/2026 (último pregão antes da gravação)
regra: fonte primária = documento da empresa/órgão/estudo ou dado de bolsa. Imprensa só como pista.
---

# Conferência factual — Mounjaro v2.1

## MUDAR ANTES DE GRAVAR

1. **B3 (fala) — previsão da Novo desatualizada.**
   Trecho: "No começo do ano, a Novo avisou que as vendas de dois mil e vinte e seis vão cair."
   Problema: a Novo melhorou a previsão duas vezes. Fev/26: −5% a −13%. Mai/26 (1º tri): −4% a −12%. **04/08/26 (2º tri): 0% a −6%**, e as vendas ajustadas do 2º tri subiram 7% a câmbio constante. Hoje a previsão oficial inclui "não cair". Do jeito que está, a frase vira "a Novo vai vender menos em 2026", e isso a própria Novo já não afirma.
   Correção sugerida (sem mexer no resto): "No começo do ano, a Novo avisou que as vendas de dois mil e vinte e seis podiam cair. Depois aliviou a previsão, mas o estrago na ação já estava feito." Na [TELA], acrescentar: "revisada em 04/08/26 para 0% a −6% (a câmbio constante)".
   Fonte primária (bloqueada daqui, **conferir no Mac**): 6-K da Novo de 04/08/2026 — https://www.sec.gov/Archives/edgar/data/0000353278/000117184326005184/f6k_080426.htm · 6-K de 03/02/2026 — https://www.sec.gov/Archives/edgar/data/353278/000117184326000596/f6k_020326.htm · relatório do 1º tri — https://www.sec.gov/Archives/edgar/data/0000353278/000035327826000018/caq12026.htm (pistas: Yahoo/Nasdaq "Novo Nordisk raises adjusted sales… outlook for 2026", ago/26).

2. **B3 (fala e [TELA]) — "primeira previsão de queda em vinte e cinco anos".**
   Problema: a imprensa diverge. Uma parte diz "a primeira em 25 anos" (CNBC/NordiskPost). Outra diz "a primeira queda anual desde 2017" (em coroas, no valor reportado). Não está no comunicado que deu pra ver.
   Correção: trocar por "a primeira previsão de queda em muitos anos". Se o Mac achar "25 years" no 6-K de 03/02/26 (link acima), pode manter.

3. **B5 (fala) — Smart Fit "uns vinte e seis por cento".**
   Trecho: "a ação da Smart Fit caiu uns vinte e seis por cento no ano."
   Na data-base do vídeo (02/10/26, a mesma da Pague Menos) a SMFT3 fechou a R$ 17,63 contra R$ 23,30 em 30/12/25. Dá **−24,3%**. Os −26% eram do fechamento de 01/10 (R$ 17,15).
   Correção: "caiu uns vinte e quatro por cento no ano". Na [TELA]: "SMFT3 23,30 → 17,63 = −24,3%, 30/12/25 → 02/10/26, só preço".
   Fonte: série diária da SMFT3.SA (Yahoo Finance chart API, puxada em 03/10/26).

4. **B4 [TELA] — Hypera "+4,8% no ano" está errado.**
   HYPE3: R$ 23,56 (30/12/25) → R$ 24,65 (01/10) = +4,6%. → R$ 25,16 (02/10) = **+6,8%**.
   Correção: "HYPE3 +6,8% no ano (30/12/25 → 02/10/26, só preço)".
   Fonte: série diária HYPE3.SA (Yahoo chart API, 03/10/26).

5. **B4 (fala) — Mercado Livre: fato novo que o roteiro omite.**
   Trecho: "No fim de setembro, o Mercado Livre anunciou que vai vender remédio com receita, caneta inclusa."
   Problema: em **29/09/26 a Anvisa notificou o Mercado Livre e mandou suspender a venda/intermediação** até ele provar que está regular (prazo 01/10). Um espectador vai apontar isso nos comentários.
   Correção sugerida: depois da frase, acrescentar "Três dias depois, a Anvisa mandou suspender até ele provar que está tudo regular. Mas a ação das farmácias já tinha caído." Na [TELA]: "29/09/26: Anvisa notifica e manda suspender (prazo 01/10)".
   Fonte: só imprensa por enquanto (Bloomberg Línea, O Povo, 29/09/26). **Conferir no Mac** a nota da Anvisa em https://www.gov.br/anvisa/pt-br/assuntos/noticias-anvisa/2026 (procurar "Mercado Livre", 29/09). Se não houver nota oficial, falar "segundo a imprensa".

6. **B2 (fala) — WeightWatchers não começou a receitar caneta depois de sair da Justiça.**
   Trecho: "E saiu da Justiça fazendo o quê, Tanaka? Receitando a caneta, numa clínica online."
   Problema: a clínica online da WW (compra da Sequence) receita GLP-1 desde 2023, antes do Chapter 11 (06/05/25). O que mudou depois foi a aposta virar o centro do negócio: 24,6% da receita no 2º tri de 2026.
   Correção mínima: "E saiu da Justiça apostando em quê, Tanaka? Na caneta, numa clínica online." O resto do trecho fica igual.
   Fonte: release do 2T26 da WW (8-K) — **conferir no Mac**: https://www.sec.gov/Archives/edgar/data/0000105319/000119312526335047/d15116dex991.htm (confirmar que é o do 2T26; senão, procurar o 8-K de 05/08/26 em https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000105319&type=8-K).

7. **B4 [TELA] — banco citado pelo nome (compliance).**
   Trecho: "relatório de banco (Itaú BBA) via Seu Dinheiro". A fala diz só "relatório de banco", o que está certo. A cartela dá o nome de uma instituição que tem corretora no grupo, num vídeo com publi de app de investimento.
   Correção: tirar "(Itaú BBA)" da [TELA] e deixar "relatório de banco, via Seu Dinheiro, 03/07/26". Se o Denis quiser manter o nome, é decisão editorial, não erro factual.

8. **B5 [TELA] — cargo do Diogo Corona.**
   "Diogo Corona, COO da Smart Fit": ele era COO quando deu a frase (ago/25), mas **virou CEO em 02/03/26**. O fato relevante "Mudança na Administração" saiu na CVM em 10/02/26.
   Correção: "Diogo Corona, então COO (hoje CEO) da Smart Fit". A fala ("o diretor de operações… disse, no ano passado") está correta e fica como está.

## CONFERIDO OK

Dados de bolsa: série diária do Yahoo Finance chart API, puxada em 03/10/26. Os sites da B3 e da Nasdaq Copenhagen estão bloqueados daqui. A conta foi refeita.

- **Novo "perdeu três quartos desde o pico, junho de 2024"**: NOVO-B.CO fechou a DKK 1.028,00 em 25/06/24 (máximo de fechamento) e a 248,75 em 02/10/26 = −75,8%. ADR NVO: US$ 146,91 → 37,32 = −74,6%. Bate com a [TELA].
- **Novo "valia mais de meio trilhão, hoje uns 165 bi"**: NVO US$ 129,21 em 01/05/24 × ~4,45 bi de ações dá ~US$ 575 bi (bate com os "> 570 bi" da Fortune). No pico, ~US$ 654 bi. Hoje: US$ 37,32 × 4,4248 bi de ações (30/06/26, série de ações do Yahoo) = **US$ 165,1 bi**. OK.
- **Lilly passou de US$ 1 tri em 21/11/25**: a máxima do dia foi US$ 1.066,65 e a empresa tinha ~945 mi de ações emitidas, então cruzou US$ 1 tri. CNBC 21/11/25 é só pista. Em 02/10/26: US$ 1.142,85 × 891,5 mi = ~US$ 1,02 tri. OK. "Primeira empresa de saúde": só pela CNBC/Nasdaq.com. Pista coerente, sem fonte primária possível.
- **Pague Menos R$ 10 mil → "uns seis mil"**: PGMN3 R$ 6,09 (30/12/25) → R$ 3,70 (02/10/26) = 0,6076 → R$ 6.076 (−39%). OK em B0, B4 e B7.
- **PGMN3 −8,0% em 24/09/26** (3,75 → 3,45) e **RADL3 −5,38%** (19,50 → 18,45): OK.
- **"A RD também caiu"**: RADL3 R$ 23,45 → 19,50 (02/10) = −16,8% no ano. OK.
- **Patente da semaglutida (Ozempic) venceu em 20/03/26**: nota da Anvisa de 26/05/2026, que diz "teve sua patente expirada em 20 de março". https://www.gov.br/anvisa/pt-br/assuntos/noticias-anvisa/2026/anvisa-aprova-primeira-caneta-de-semaglutida-sintetica-analoga-ao-ozempic-para-diabetes
- **EMS — primeira cópia nacional (Ozivy)**: registro publicado pela Anvisa em 26/05/26 (mesma nota). Lançamento nas farmácias em 15/06 só pela imprensa (CFF, Exame, Meio & Mensagem). "Lançou em junho" é coerente.
- **Hypera — Semavy**: registro da Anvisa em 29/07/26, em nome da Cosmed, empresa do grupo Hypera. https://www.gov.br/anvisa/pt-br/assuntos/noticias-anvisa/2026/anvisa-registra-cinco-novas-canetas-de-semaglutida . Lançamento em 04/09 a R$ 333 só pela imprensa (Exame, Forbes). Coerente.
- **"Aqui no Brasil, a farmácia é o caixa por onde a caneta legal passa" / caneta da Lilly é a mais vendida**: a apresentação do 2T26 da RD (CVM, 05/08/26) mostra a **tirzepatida (Mounjaro) com 70% da receita de GLP-1 da RD** e a semaglutida com 30%. https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1552326&numSequencia=1077032&numVersao=1
- **Pague Menos vende caneta**: o release do 2T26 (CVM, 03/08/26) diz que GLP-1 foi 8,2% das vendas totais no trimestre e que a semaglutida caiu ~40% de preço depois da patente. https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1551400&numSequencia=1076106&numVersao=1
- **Conta 150 ÷ 60 = 2,5**: a aritmética está certa. Os números de origem estão em "não consegui conferir".
- **Grana "parceiro da B3"**: nota da B3 de 26/05/2022, "B3 celebra parceria com Grana Capital". https://www.b3.com.br/pt_br/noticias/b3-e-grana-capital-trazem-nova-solucao-para-o-investidor-no-calculo-e-declaracao-do-imposto-de-renda.htm
- **Smart Fit trocou de CEO**: a CVM lista o fato relevante "Mudança na Administração" de 10/02/2026. O PDF veio corrompido; o conteúdo (Diogo CEO a partir de 02/03/26) está só na imprensa (Exame/Poder360).

## NÃO CONSEGUI CONFERIR (daqui)

| Item do roteiro | Por quê | Pista (imprensa) |
|---|---|---|
| Novo, "a mais valiosa da Europa" | Não há fonte primária (é ranking de mercado) | CNBC/CNN/Fortune 01–05/09/23: passou a LVMH. Coerente |
| Ibovespa contém RD (RADL3) | A carteira teórica está em sistemaswebb3-listados.b3.com.br (bloqueado) | Praticamente certo; Mac confirma |
| Mounjaro nº 1 do ranking IQVIA | O dado da IQVIA não é público | Guairá News 24/09/26 (76% do mercado de GLP-1). O dado da RD acima corrobora |
| Pague Menos: cliente de GLP-1 gasta ~9x mais | Não está no release nem na apresentação do 2T26 (CVM, conferidos). Deve ter saído de call ou entrevista | InfoMoney 24/09/26. Release cita outra métrica (cuidado contínuo 6,4x) |
| Itaú BBA: GLP-1 ≈ 12% da receita da RD em 2026; R$ 150–160 × R$ 60 de lucro bruto; ~metade fora do canal formal | Relatório de banco não é público | Seu Dinheiro / NeoFeed 03/07/26 (os números batem entre as duas) |
| "A B3 também investiu" no Grana (publi) | Sem documento da B3 sobre o aporte | startups.com.br ("Grana Capital atrai B3 e RTM em nova rodada"). Texto do patrocinador |
| Mercado Livre anuncia remédio com receita (24/09) | Mercado Livre bloqueado; sem 6-K | Exame/InfoMoney 24–25/09/26 |
| McDonald's: adulto no Happy Meal; "não espera impacto material" | HBR e site de RI bloqueados | Yahoo/Moneywise set/26 (entrevista à HBR). O "não material" foi dito numa teleconferência de resultados, data não confirmada |
| Fala da Smart Fit (InvestNews, 20/08/25) | A entrevista só existe na imprensa | InvestNews, "Magro e musculoso…" |
| Itens de SEC, NEJM, Cornell, PwC, Bain, Walmart, Mondelez | Domínios bloqueados → ver "CONFERIR NO MAC" | Todas as pistas batem com o roteiro, exceto a Mondelez (ver abaixo) |

## CONFERIR NO MAC (rede aberta, de manhã) — URL exata e o que olhar

1. Novo 6-K 03/02/26 — https://www.sec.gov/Archives/edgar/data/353278/000117184326000596/f6k_020326.htm → previsão "−5 to −13%" (vendas ajustadas, CER); há "25 years"? (itens 1 e 2 do MUDAR)
2. Novo 6-K 04/08/26 — https://www.sec.gov/Archives/edgar/data/0000353278/000117184326005184/f6k_080426.htm → previsão "0 to −6%"; 2º tri +7% CER (item 1)
3. Novo 6-K 23/02/26 (REDEFINE 4) — https://www.sec.gov/Archives/edgar/data/353278/000117184326000996/f6k_022326.htm → 809 pacientes, 84 semanas, 23,0% × 25,5% (estimando "se todos aderissem"; no estimando de regime, 20,2% × 23,6%), não inferioridade não atingida. Pista: GlobeNewswire 23/02/26 bate
4. Novo 6-K 10/09/25 — https://www.sec.gov/Archives/edgar/data/353278/000117184325005809/f6k_091025.htm → ~9.000 vagas de 78.400
5. WW 8-K 06/05/25 (Chapter 11) — https://www.sec.gov/Archives/edgar/data/105319/000119312525114307/d934787d8k.htm ; saída em 24/06/25 e release do 2T26 (197 mil, +55,7%) — https://www.sec.gov/Archives/edgar/data/0000105319/000119312526335047/d15116dex991.htm ou o índice https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000105319&type=8-K
6. SURMOUNT-5 ("remédio da Lilly emagrece mais") — https://www.nejm.org/doi/full/10.1056/NEJMoa2416394 e https://clinicaltrials.gov/study/NCT05822830 → tirzepatida −20,2% × semaglutida −13,7% em 72 semanas
7. Cornell — https://www.news.cornell.edu/stories/2025/12/ozempic-changing-foods-americans-buy → −5,3% em 6 meses; renda alta >8%; salgadinho ~−10%; fast food/café caem (~8%); iogurte é o que mais sobe; ~150 mil lares Numerator
8. Walmart, teleconferência do 4º tri do ano fiscal 2026 (19/02/26) — https://stock.walmart.com/_assets/_5813cf69129ed45d080396680f549a44/walmart/db/938/9972/transcript_management_call/Earnings+Transcript+(FY26+Q4).pdf → Rainey: "it's kind of a wash"; cesta com frescos maior "double-digit"
9. Mondelez → **conferir o número da [TELA]**: as pistas divergem entre "0,5–1%" (Food Dive) e "1–1,5% de volume em 10 anos" (Van de Put, em outra fala). Procurar a transcrição da CAGNY/teleconferência de fev/26 em https://ir.mondelezinternational.com/events-and-presentations . Se não bater, tirar o número da [TELA] e deixar só "mínimo"
10. PwC — https://www.pwc.com/us/en/industries/consumer-markets/library/glp-1-consumer-trends.html → 4–9/05/26, 3.089 consumidores, 1.063 usuários; 26% gastam mais com roupa
11. Bain, 08/09/26 — https://www.bain.com/pt-br/about/media-center/press-releases/south-america/2026/mercado-de-whey-protein-dobra-de-tamanho-com-avanco-do-glp-1-e-busca-por-longevidade → usuários de GLP-1 ≈ 10% da demanda de whey
12. Ibovespa — https://sistemaswebb3-listados.b3.com.br/indexPage/day/IBOV?language=pt-br → RADL3 está na carteira de set–dez/26
13. Anvisa × Mercado Livre — https://www.gov.br/anvisa/pt-br/assuntos/noticias-anvisa/2026 → nota de 29/09/26 (item 5 do MUDAR)
14. McDonald's — https://corporate.mcdonalds.com/corpmcd/investors.html (transcrições) → Kempczinski: GLP-1 "not material"; data da fala
15. Smart Fit fato relevante 10/02/26 (PDF não abriu daqui) — https://www.rad.cvm.gov.br/ENET/frmDownloadDocumento.aspx?Tela=ext&descTipo=IPE&CodigoInstituicao=1&numProtocolo=1475852&numSequencia=1000558&numVersao=1

## RECOMENDAÇÃO DE ATIVO / CORRETORA — sinalizações

- **Título do B6, "E AGORA: COMPRAR, VENDER OU FICAR"**: se esse título aparecer como capítulo do YouTube ou na tela, soa como recomendação. Sugestão: "E AGORA: O QUE CADA PONTA ARRISCA". Se ficar só no roteiro, sem problema.
- **B6, "Quem pensa na ponta da torneira, a fabricante, tem o argumento de que é ali que o dinheiro para."** Está ok, porque vem com o "cuidado" logo depois e com o "Nada disso é recomendação" na abertura. Manter os dois juntos na edição, sem cortar o cuidado.
- **B6, "Quem pensa em vender ação de comida e bebida…" / "quem já tem e vai ficar…"**: descreve o que o investidor faz, sem mandar fazer. Ok.
- **B4 [TELA], "(Itaú BBA)"**: nome de instituição com corretora no grupo (item 7 do MUDAR).
- Nenhuma frase do tipo "compre X". Nenhuma corretora citada na fala. Na publi, o Grana é um app de IR e proventos, não corretora; a afirmação "parceiro da B3" foi conferida.
- **Cuidado extra (Anvisa)**: em 25/09/26 a Anvisa **proibiu a propaganda do Semavy**, que é tarja vermelha (https://www.gov.br/anvisa/pt-br/assuntos/noticias-anvisa/2026/anvisa-proibe-propaganda-da-caneta-semavy). Na [TELA] do B4, mostrar "Semavy, R$ 333" como dado jornalístico, sem imagem de anúncio nem da embalagem com preço promocional.

## Domínios bloqueados pelo proxy (testados com curl em 03/10/26, CONNECT 403; nada foi contornado)

sec.gov, data.sec.gov, efts.sec.gov · novonordisk.com · lilly.com / investor.lilly.com · nejm.org · thelancet.com · clinicaltrials.gov · pubmed/eutils (ncbi) · doi.org · crossref · news.cornell.edu · journals.sagepub.com · pwc.com · bain.com · corporate.walmart.com / stock.walmart.com · mondelezinternational.com · corporate.mcdonalds.com · hbr.org · weightwatchers / q4cdn (RI da WW) · stockanalysis.com · companiesmarketcap · nasdaqomxnordic.com · sistemaswebb3-listados.b3.com.br · api.bcb.gov.br · in.gov.br (DOU) · consultas.anvisa.gov.br · busca.inpi.gov.br · api.mziq.com (RI Pague Menos) · ri.rdsaude / ri.hypera / ri.smartfit · mercadolivre · globenewswire · investegate · imprensa (cnbc, reuters, infomoney, seudinheiro, investnews, exame, biospace, fooddive etc.) · wikipedia · web.archive.org

**Acessíveis e usados:** finance.yahoo.com (chart API), www.b3.com.br, www.gov.br (Anvisa/INPI), dados.cvm.gov.br e www.rad.cvm.gov.br.
