---
roteiro: 2026-10-04-ipo-anthropic-spacex-teleprompter.md (v1.4) + 2026-10-04-ipo-anthropic-spacex-EMPACOTAMENTO.md (commit 8c6443c)
conferido_em: 2026-10-03 (sábado), do container na nuvem
regra: só fonte primária (SEC/EDGAR, comunicado oficial, lei/norma). Imprensa só como pista. Preço de pregão = dado de mercado do Yahoo Finance (API de cotação), registrado como tal.
bloqueados_pelo_proxy (403 no CONNECT, testado com curl, não contornado): www.sec.gov, data.sec.gov, efts.sec.gov, www.spacex.com, investors.spacex.com, ir.spacex.com, darioamodei.com, hyrox.com, www.lcatterton.com, site.warrington.ufl.edu, conteudo.cvm.gov.br, www.nasdaq.com, www.morningstar.com, www.reuters.com, www.bloomberg.com, www.axios.com, www.nytimes.com, fortune.com, www.ft.com, www.infomoney.com.br, borainvestir.b3.com.br, arquivos.b3.com.br, www.in.gov.br, investor.fb.com, www.aramco.com, www.saudiexchange.sa, newsroom.arm.com, www.prnewswire.com, www.businesswire.com, web.archive.org
abriram: www.anthropic.com, query1/query2.finance.yahoo.com, www.b3.com.br, www.planalto.gov.br, www.gov.br, normas.receita.fazenda.gov.br (só a casca: a norma carrega por JavaScript e não veio)
---

# Conferência de fatos: IPO SpaceX × Anthropic (gravação 04/10)

## MUDAR ANTES DE GRAVAR

**O motivo da maioria dos itens:** a SPCX fechou **sexta, 02/10, a US$ 158,96** (máxima de US$ 159,84). O roteiro foi escrito com o fechamento de 01/10 (US$ 148,07) e fala "hoje". Com o preço de 02/10, quase todo "hoje" da fala fica errado. Fonte: Yahoo Finance, gráfico diário SPCX (https://query1.finance.yahoo.com/v8/finance/chart/SPCX, consultado em 03/10/2026). A Nasdaq não abriu daqui.

Há dois caminhos. **(a) Datar a fala** ("no dia primeiro de outubro"): os números ficam como estão, a cartela já traz 01/10 e não depende do preço de segunda. É o que recomendo. **(b) Atualizar pra 02/10:** os números estão abaixo, mas mudam de novo no próximo pregão.

| # | Trecho exato | Correção | Fonte |
|---|---|---|---|
| 1 | B0: "Quem colocou dez mil reais na SpaceX pelo preço da oferta **hoje tem quase onze mil**." | (a) "...no dia primeiro de outubro, tinha quase onze mil." (b) com 02/10: R$ 11.775, "quase onze mil e oitocentos" | Yahoo SPCX, fechamento 01/10 US$ 148,07 e 02/10 US$ 158,96 (consultado 03/10) |
| 2 | B0: "**Hoje tem uns nove mil e duzentos.** Saiu no prejuízo." | (a) datar em 01/10. (b) com 02/10: R$ 9.876, "quase dez mil", e continua no prejuízo | idem |
| 3 | B0: "**quase mil e oitocentos reais** de diferença" | (a) datar. (b) com 02/10: R$ 1.898, "quase mil e novecentos" | idem (conta: 10.000 × P/135 − 10.000 × P/160,95) |
| 4 | B9: "Os **nove mil e duzentos** reais do começo..." e H1 (linha 64) "viraram nove mil e duzentos" | segue a mesma escolha do item 2 | idem |
| 5 | B1: "Quem comprou nesse pico está **hoje trinta por cento no vermelho**." | (a) datar em 01/10. (b) com 02/10: **−24,8%**, "um quarto no vermelho" | Yahoo SPCX: 211,39 (16/06) → 158,96 (02/10) |
| 6 | B2: "Depois da trava de setembro, **ficou praticamente parada**." | Com 02/10 a ação **subiu 7,4%** (148,03 em 24/09 → 158,96). Ou se data em 01/10, ou se troca por "subiu um pouco". A cartela da linha 132 tem data (01/10) e está certa | Yahoo SPCX |
| 7 | B8: "**Hoje** a ação está perto de **cento e quarenta e oito** dólares." + [TELA] "SPCX hoje US$ 148,07" | (a) "No dia primeiro de outubro, perto de cento e quarenta e oito". (b) "perto de cento e cinquenta e nove". Na cartela, trocar "hoje" pela data | Yahoo SPCX |
| 8 | B4: "Quem comprou na abertura... está, doze anos depois, **ganhando dezesseis por cento**." | Em 01/10 dá +15,9% (ok com data). Com 02/10, BABA a US$ 105,85: **+14,2%**. Datar em 01/10 ou falar "uns catorze por cento" | Yahoo BABA (abertura 19/09/2014 US$ 92,70) |
| 9 | B4: "a Arm... hoje vale **quase seis vezes** o preço da oferta" | Em 01/10, 5,73×, ok com data. Com 02/10, ARM a US$ 307,49: **6,03×**, "seis vezes". Datar ou trocar | Yahoo ARM |
| 10 | [TELA] B4, Uber: "Pior momento **US$ 25,58 (nov/19, −43%)**" | **US$ 13,71 de mínima no dia 18/03/2020 (−69,5%)**. O menor fechamento foi US$ 14,82 no mesmo dia. Novembro de 2019 não foi o pior momento | Yahoo UBER, histórico diário desde 10/05/2019 |
| 11 | [TELA] B4, Aramco: "**SAR 25,22** (−4,6%)" na coluna "01/10/26" | O fechamento de **01/10 foi SAR 25,28 (−4,4%)**; 25,22 é o de 30/09. Ou se troca o número, ou se troca a data. A fala ("ainda abaixo do preço da oferta") continua certa | Yahoo 2222.SR (desdobramentos 11:10 em 15/05/2022 e 09/05/2023 confirmados no mesmo histórico) |
| 12 | [TELA] B2: "contrato SpaceX–Anthropic de **03/05/26**... **~325 mil GPUs**" | No comunicado oficial da Anthropic (**06/05/2026**), o acordo é usar toda a capacidade do Colossus 1: "more than 300 megawatts of new capacity (**over 220,000 NVIDIA GPUs**)". Se o Mac não achar "325 mil" e "03/05" no 424B4, trocar por "mais de 220 mil GPUs (Anthropic, 06/05/26)". A fala "desde maio" está certa | https://www.anthropic.com/news/higher-limits-spacex (06/05/2026) |
| 13 | B2, fala: "comprou quase um quinto **de tudo que a SpaceX faturou** no trimestre" × [TELA] "Cliente B 19,5%, **só no segmento de IA**" | **A fala contradiz a cartela.** Se os 19,5% são da receita do segmento de IA, a fala erra: o certo seria "quase um quinto do que a SpaceX faturou com IA". O Mac confere no 10-Q qual é a base (ver CONFERIR NO MAC, item M7) e ajusta uma das duas | 10-Q 2T26 (bloqueado daqui) |
| 14 | B6: "O texto foi **coassinado pelo Musk e pelos chefes da OpenAI e do Google DeepMind**" + "Em setembro, **segundo o site americano Axios**" | O texto existe e a fonte primária é o próprio ensaio: https://darioamodei.com/post/we-must-pace-the-frontier. A página oficial da Anthropic linka pra ele e fala em "slowing the pace of frontier AI development... as called for by Anthropic CEO Dario Amodei" (https://www.anthropic.com/institute/measuring-pace-of-ai-development). **Data e coassinaturas eu não consegui ver** (darioamodei.com bloqueado). **Se o Mac não ver os nomes no próprio texto, cortar a frase da coassinatura**: é a afirmação mais forte do roteiro e só tem imprensa como fonte. Com o texto confirmado, dá pra citar o ensaio no lugar de "segundo o Axios" | anthropic.com (página do Institute, consultada 03/10) |

**Recomendação e acesso (sinalizar, não é erro de fato):**
- [TELA] B1, linha 100: "via **Schwab, Fidelity, Robinhood, SoFi e E\*Trade**". Isso **cita corretora/plataforma de acesso pelo nome**. Sugestão: "por corretoras americanas".
- B7: "Se você tem **NASD11**..." e "O da SpaceX é o **SPCX34**". Cita produto e ticker como caminho de acesso. É informativo, mas fica no limite de "por onde comprar"; o Denis decide. Nenhuma frase diz "compre no IPO" nem "vale a pena entrar". A pergunta do B0 ("entra, espera ou passa longe?") é enquete, e o B8 abre com "Não é recomendação".
- B8: "Pra quem pensa em entrar, o argumento a favor..." Está enquadrado, segue o "Não é recomendação" e tem o contra-argumento logo depois. Ok.

---

## CONFERIDO OK

**Anthropic, comunicado oficial (www.anthropic.com):**
- "ainda não publicou o prospecto": o comunicado de **01/06/2026** diz que a Anthropic, PBC "confidentially submitted a draft registration statement on Form S-1" e que "the number of shares to be offered and the price have not yet been set" (https://www.anthropic.com/news/confidential-draft-s1-sec). Na lista de notícias até 02/10/2026 não aparece S-1 público. **O EDGAR não abriu: ver M1.**
- "A Anthropic tem contrato de computação com a SpaceX desde maio": comunicado de 06/05/2026 (https://www.anthropic.com/news/higher-limits-spacex).
- "o Dario Amodei publicou um texto pedindo que o mundo desacelere": a página oficial da Anthropic confirma o pedido e linka o ensaio "We Must Pace the Frontier" (data e coassinaturas: ver item 14).
- "A Anthropic, a dona do Claude": anthropic.com.

**SPCX, pregão (Yahoo Finance, gráfico diário, consultado em 03/10; ticker SPCX na NasdaqGS, nome "Space Exploration Technologies Corp."):**
- 12/06/2026 (sexta): abertura US$ 150,00 · máxima US$ 176,52 · fechamento US$ 160,95 ✓
- "Na terça seguinte": 16/06/2026 cai numa terça ✓. Fechamento de US$ 211,39 = maior fechamento da série ✓. A máxima intradiária foi US$ 225,64; a cartela diz "pico de fechamento" e está certa.
- Piso 05/08 US$ 108,27 = menor fechamento da série ✓. −48,8% desde o pico ✓.
- 20/08 US$ 134,00 · 24/09 US$ 148,03 · 01/10 US$ 148,07 ✓
- Conta da cartela do B0 (pra 01/10): 148,07/135 = R$ 10.968 · 148,07/160,95 = R$ 9.200 · diferença R$ 1.768 ✓
- Nasdaq-100 "15 pregões após o IPO": 07/07/2026 é o 16º pregão contando 12/06, ou seja, 15 depois ✓ (a data da inclusão está em M10)
- EMPACOTAMENTO: "Nos últimos 5 pregões, só 2 fecharam dentro da faixa (25/09 US$ 148,68 e 01/10 US$ 148,07)" ✓ (28/09 145,47 · 29/09 149,24 · 30/09 150,86 ficaram fora)
- SPCX34: primeiro pregão na B3 em **12/06/2026**, mesmo dia de Wall Street ✓ (Yahoo SPCX34.SA, firstTradeDate). A relação 1 ação = 15 BDRs é coerente com o preço (R$ 54,74 × 15 ≈ US$ 160,95 × 5,10), mas a fonte primária é a B3 (M12).

**IPOs do passado (Yahoo Finance):**
- Facebook: estreia 18/05/2012 ✓ · mínima US$ 17,55 em 04/09/2012, "em quatro meses, menos da metade" ✓ · primeiro fechamento ≥ US$ 38 em 02/08/2013 (US$ 38,05) ✓ · 01/10 US$ 725,93 = 19,1× ✓ (02/10: 728,08 = 19,2×, ainda "umas dezenove vezes")
- Alibaba: estreia 19/09/2014, abertura US$ 92,70 ✓ · mínima US$ 57,20 em 29/09/2015 ✓ · 01/10 US$ 107,45 ✓
- Uber: estreia 10/05/2019 ✓ · 01/10 US$ 67,88 ✓ (o pior momento está errado: item 10)
- Aramco: estreia 11/12/2019 ✓ · SAR 32 ÷ 1,21 = 26,45 (bonificações 11:10 de 2022 e 2023) ✓ · "ainda abaixo do preço da oferta" ✓
- Arm: estreia 14/09/2023 ✓ · mínima US$ 46,50 em 20/10/2023 ✓ · 01/10 US$ 292,34 = 5,73× ✓
- "Se o seu filho nasceu no dia da estreia, ele já tá no sexto ano": quem nasceu em set/2014 entra no 1º ano em 2021 (corte de 31/03) e está no 6º ano em 2026 ✓

**Contas (sem fonte nova, conferidas):** 555.555.555 × US$ 135 = US$ 74,99 bi ✓ · 328,4/555,6 = 59%, "mais da metade" ✓ · 1,3 bi > 2 × 555,6 mi ✓ · 11,387/18,7 = 61% ✓ · 1,77 tri/18,7 bi ≈ 95× ✓ · 2 tri/4,6 bi ≈ 435× ✓ · 2 tri/100 bi = 20× ✓ · R$ 50 mil × 2,82% = R$ 1.410 ✓ · 4,6/0,4 ≈ 12× ✓

**Lei:**
- Isenção de R$ 20 mil/mês vale pra "ganhos líquidos auferidos por pessoa física em operações no mercado à vista de **ações**". O texto fala em ações, não em BDR (Lei 11.033/2004, art. 3º, I: https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l11033.htm, consultado 03/10). Que o BDR fica fora é leitura da Receita: ver M13.

**Hyrox / L Catterton:** **nenhum dos dois arquivos deste roteiro menciona Hyrox, LVMH ou L Catterton**, então não há nada pra corrigir aqui. Fora do escopo, mas vale avisar: o Mounjaro v2 só cita Hyrox em `cortados_da_fala`. Já o post `seo/_html/lvmh-hyrox-smartfit-suor-vale-mais-que-bolsa.html` tem como título e og:title "Por que a família dona da LVMH está comprando..." e diz que "o fundo da família Arnault negociou". O FAQ do mesmo post diz que é a L Catterton. Conferir no anúncio (M16) e alinhar o título.

---

## NÃO CONSEGUI CONFERIR

Estes itens dependem de domínio bloqueado ou só têm imprensa como fonte. A fala já atribui à imprensa: "segundo a Bloomberg", "a Reuters viu", "segundo o NYT", "segundo a imprensa americana".

- **Anthropic, imprensa sem fonte primária possível hoje** (não há S-1 público): estreia em novembro, apresentação a partir de 09/11, antes de 26/11 e valor de US$ 1,8–2 tri (Bloomberg 01/10) · captação de até US$ 100 bi · receita/25 ~US$ 4,6 bi, receita/24 ~US$ 0,4 bi, prejuízo ~US$ 42 bi, ~US$ 34 bi sem caixa, prejuízo operacional > US$ 8 bi, caixa US$ 20,3 bi (rascunho visto pela Reuters, 28/09) · classe F = 50,1% dos votos (Reuters 29/09) · receita anualizada > US$ 100 bi (NYT 18/09) · lucro operacional ajustado no 2T26 (Fortune/FT) · "receita depende de lançar modelos em cadência contínua". **Atribuídos na fala, ok assim.** Se o S-1 ficar público antes da gravação (M1), tudo isso passa a ser conferível e o B3 muda.
- "Anthropic sem BDR": não há ticker da Anthropic na B3 no Yahoo (busca em 03/10; só aparecem tokens e derivativos fora de bolsa). A confirmação primária fica com a B3 (M12).
- Reuters 07/06 (varejo dos EUA, até 30%, Brasil só pra qualificado): imprensa. O primário é o 424B4 (M2).

## CONFERIR NO MAC (rede aberta, de manhã)

No EDGAR, use o User-Agent com nome e e-mail. Cada item traz a URL e o que olhar.

| # | URL | O que conferir | Trecho do roteiro |
|---|---|---|---|
| M1 | https://efts.sec.gov/LATEST/search-index?q=%22Anthropic%2C%20PBC%22&forms=S-1,S-1/A · e https://www.sec.gov/cgi-bin/browse-edgar?company=anthropic&type=S-1&action=getcompany | Se já existe S-1 público da Anthropic. **Se existir, o B3 inteiro muda** ("rascunho que a Reuters viu" vira "o prospecto") e os números do B3/B5/B6 precisam ser reconferidos nele | B3, B6, B7 "o prospecto nem saiu" |
| M2 | https://www.sec.gov/cgi-bin/browse-edgar?company=space+exploration+technologies&type=424B4&action=getcompany (abrir o 424B4 de ~11–12/06/2026) | Capa: preço US$ 135 · 555.555.555 ações classe A · US$ 74,99 bi brutos · nenhum selling shareholder (100% primária) · lista de coordenadores (achar o banco brasileiro) · alocação pra varejo (até 30%?) e regra pra estrangeiro/Brasil | B0, B1, B2 |
| M3 | mesmo 424B4, seção "Shares Eligible for Future Sale" / "Lock-up" | 20/08 até 319 mi · 24/09 até 328,4 mi · **09/10** até 328,4 mi · **24/10** até 328,4 mi · 2º pregão após o 3T26 até 1,3 bi · 08/12 até 797,6 mi · Musk 366 dias · "no 1º dia, só as ações da oferta eram livres". **Atenção: 24/10/2026 é sábado.** Conferir se a data é essa mesmo ou se a liberação vale no pregão seguinte (26/10) | B2 "No dia vinte e quatro" |
| M4 | mesmo 424B4, "Principal Stockholders" / "Controlled company" | Musk ~82,4% do poder de voto | B6 |
| M5 | mesmo 424B4, "Subsequent events" / contrato com a Anthropic | Data **03/05/26** · até maio/29 · **~325 mil GPUs** · rescisão com 90 dias de aviso. Se não bater, aplicar o item 12 | B2 |
| M6 | mesmo 424B4, segmentos 2025 | Receita/25 US$ 18,7 bi · Starlink/Connectivity US$ 11,387 bi · "único segmento com lucro operacional" · prejuízo/25 US$ 4,9 bi · ações em circulação pós-IPO (pra conferir ~US$ 1,77 tri a US$ 135) | B0 [TELA], B5, B8 |
| M7 | https://www.sec.gov/cgi-bin/browse-edgar?company=space+exploration+technologies&type=10-Q&action=getcompany (10-Q do 2T26) | Concentração: Cliente A 18,3% · Cliente B 19,5%. **A base é a receita total ou só a de IA?** Define a correção do item 13 | B2 |
| M8 | https://www.sec.gov/cgi-bin/browse-edgar?company=space+exploration+technologies&type=8-K&action=getcompany (8-K de 04/08/2026, ex. 99.1) | Receita do 2T26 US$ 7,814 bi, +92% sobre o 2T25 | B1 |
| M9 | https://darioamodei.com/post/we-must-pace-the-frontier | Data (12/09/26?) e **lista de coassinantes (Altman, Hassabis, Musk?)**. Sem confirmação, cortar a frase (item 14) | B6 |
| M10 | https://www.nasdaq.com/press-release (buscar "SpaceX" "Nasdaq-100", jul/2026) · https://indexes.nasdaqomx.com/Index/Weighting/NDX | Entrada no Nasdaq-100 em **07/07/26** · peso de 2,82% após a revisão de setembro | B7 |
| M11 | https://site.warrington.ufl.edu/ritter/ipo-data/ (PDF "IPO Statistics", atualização de 27/08/26, tabelas 18d e 24) | P/receita > 40×, 1980–2024, 46 casos, −44,8% em 3 anos a partir do 1º fechamento, +3,1% a partir da oferta (14 casos) | B5 |
| M12 | https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/bdrs.htm → lista de BDRs não patrocinados (SPCX34) | SPCX34: não patrocinado, 1 ação = 15 BDRs, início em 12/06/26 · nenhum BDR da Anthropic | B7 |
| M13 | https://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=67494 (IN RFB 1.585/2015) | BDR: 15% sobre o ganho (20% day trade), sem isenção de R$ 20 mil, DARF 6015 até o último dia útil do mês seguinte · e se alguma lei de 2025/26 (ex.: a MP 1.303/2025, citada no art. 3º da Lei 11.033) mudou isso | B7 |
| M14 | https://conteudo.cvm.gov.br/legislacao/resolucoes/resol030.html (art. 12) | Investidor qualificado: o texto diz "**superior a** R$ 1.000.000,00" + atestado por escrito? A fala diz "**pelo menos** um milhão". Se o texto for "superior a", trocar por "mais de um milhão" | B1 |
| M15 | https://www.morningstar.com/stocks/xnas/spcx/valuation · relatório do banco do sindicato de 07/07/26 | Valor justo ~US$ 62–63 · preço-alvo US$ 225 e se esse banco consta como coordenador no 424B4 (M2) | B8 |
| M16 | https://www.lcatterton.com/press-releases · https://hyrox.com/news/ | Comunicado do negócio da Hyrox: **o comprador é a L Catterton** (não a LVMH), data, fatia, valor. Não afeta este roteiro; serve pro post de SEO citado acima | (fora deste roteiro) |
| M17 | https://www.sec.gov/Archives/edgar/data/1326801/000119312512240111/d287954d424b4.htm (424B4 do Facebook) · https://www.sec.gov/cgi-bin/browse-edgar?company=alibaba&type=424B4 · https://www.sec.gov/cgi-bin/browse-edgar?company=uber+technologies&type=424B4 · https://www.sec.gov/cgi-bin/browse-edgar?company=arm+holdings&type=424B4 | Preço da oferta: FB US$ 38 · BABA US$ 68 · UBER US$ 45 · ARM US$ 51 (estes conferi só pelo histórico; o prospecto confirma). Aramco SAR 32: prospecto na Tadawul (saudiexchange.sa) | B4 [TELA] |

## Contagem

14 itens em MUDAR ANTES DE GRAVAR (9 por causa do fechamento de 02/10) + 3 sinalizações de acesso e recomendação · 41 fatos conferidos ok · 17 verificações pro Mac (M1–M17) · 10 grupos de afirmação só com imprensa, já atribuídos na fala.

## Conferido no Mac (03/10)

| item | veredito | valor da fonte | fonte |
|---|---|---|---|
| M1 S-1 da Anthropic | OK (não existe) | Busca full-text S-1/S-1A "Anthropic, PBC": só SpaceX, Figma e SPAC. EDGAR "anthropic" = só fundos (Form D) → B3 fica como está | efts.sec.gov · browse-edgar |
| M2 capa do 424B4 | OK | "$135.00 per share"; "555,555,555 shares"; total "$74,999,999,925"; tudo "from us" (sem selling stockholder; greenshoe de 83.333.333 também primário). Banco brasileiro no sindicato: **BTG Pactual**. Varejo: o 424B4 só diz "a number of shares … allocated to retail investors", **sem %** (os 30% ficam atribuídos à Reuters) | sec.gov 424B4 de 12/06/26 (CIK 1181412) |
| M3 lock-up | OK nas datas · **DIVERGE em "duas travas já abriram"** | 20/08 "319.0 million"; 24/09, 09/10 e 24/10 "328.4 million" cada; após o 3T26 "1.3 billion"; 08/12 "797.6 million"; Musk "366 days". O prospecto diz "October 24, 2026 (135th day)", sem regra de pregão seguinte (cai num sábado; na prática, negocia a partir de 26/10). **Mas antes de 24/09 abriram mais travas:** 2º pregão após o balanço do 2T ("up to 911.5 million", 20%), 09/09 ("319.0 million") e 10/09 (59,1 mi de afiliados) | 424B4, "Shares Eligible for Future Sale" |
| M4 Musk | OK | "approximately 82.4% of the voting power" | 424B4 |
| M5 contrato Anthropic | OK | "On May 3, 2026 … through May 2029"; "approximately 325,000 NVIDIA GPUs"; "terminated by either party upon 90 days' notice" (após os 3 meses iniciais); US$ 1,25 bi/mês | 424B4 |
| M6 segmentos 2025 | OK | receita "$18,674 million"; Connectivity "$11,387 million" (61%); Space e AI com prejuízo operacional; prejuízo líquido "(4,937)"; 13.075.865.175 ações pós-IPO × US$ 135 = US$ 1,765 tri | 424B4 |
| M7 concentração | **DIVERGE a [TELA]** (a fala está certa) | "Consolidated revenue from significant customers … Customer B 19.5 %"; "revenue from Customer B relates to the AI segment". Base = receita **total**; o cliente é que é do segmento de IA | 10-Q 2T26 (spcx-20260630.htm) |
| M8 receita 2T26 | OK | "Revenues of $7.8 billion, up 92%"; total "$7,814" × "$4,071" | 8-K 04/08/26, ex. 99.1 |
| M9 texto do Dario | **DIVERGE** | Página datada só "September 2026", assinada só por Dario Amodei; **nenhum coassinante** (Hassabis só aparece citado: "the mechanism suggested by Demis Hassabis"). Musk/Altman não aparecem | darioamodei.com/post/we-must-pace-the-frontier |
| M10 Nasdaq-100 | OK na data · NÃO ABRIU o peso | SPCX ausente em 06/07 (102 nomes) e presente a partir de 07/07/26 (103). Peso 2,82%: a tabela de pesos exige login | indexes.nasdaqomx.com WeightingData |
| M11 Ritter | OK | Tabela 18d: "40<PSR 46 … -44.8%" (desde o 1º fechamento); oferta: "14 … 3.1%". PDF atual é de 25/09/26 (tabela de 07/04/26) | site.warrington.ufl.edu/ritter/files/IPO-Statistics.pdf |
| M12 BDRs | OK SPCX34 · **nuance na Anthropic** | SPCX34: DRN (não patrocinado), cotação desde 12/06/26; 8.333.333.325 BDRs ÷ 555.555.555 ações = 15. **ANTHROPIC PBC já tem cadastro de BDR DRN na B3 desde 29/07/26**, sem código e sem cotação ("hasQuotation N") | sistemaswebb3-listados.b3.com.br (GetCompaniesBDR / GetDetail) |
| M13 IN RFB 1.585 | NÃO ABRIU | normas.receita redireciona para app em JS (normasinternet2), sem texto via curl/WebFetch | normas.receita.fazenda.gov.br |
| M14 investidor qualificado | **DIVERGE** | Art. 12, II: "investimentos financeiros em valor superior a R$ 1.000.000,00 … e que, adicionalmente, atestem por escrito" | conteudo.cvm.gov.br resol030consolid.pdf |
| M15 Morningstar / banco | OK (via imprensa) · NÃO ABRIU a primária | Morningstar 403. Imprensa: valor justo US$ 63 no IPO, depois US$ 62. Preço-alvo US$ 225 não conferido. BTG Pactual consta no sindicato do 424B4 | Yahoo Finance / morningstar.com (busca) |
| M16 Hyrox | OK (via imprensa) | Comprador: consórcio liderado pela L Catterton (set/26), ~€ 600 mi, fundadores retomam controle | Kirkland, Bloomberg Law, swissinfo (busca) |
| M17 preços de IPO | OK | FB "public offering price of $38.00"; BABA "US$68.00"; UBER "$45.00"; ARM "$51.00". Aramco não conferida | 424B4s na SEC |
