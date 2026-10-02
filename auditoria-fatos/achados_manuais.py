"""Checagem manual a fundo (registro do que foi conferido). Cada achado: post_id, trecho literal curto, problema,
classe (CRÍTICO / DATADO / DÚVIDA), correção sugerida e fonte. DESTINOS: destino sugerido por post com CRÍTICO.
CONFERIDOS: posts lidos a fundo (com ou sem achado) e observação."""

CVM_DFP = "https://dados.cvm.gov.br/dataset/cia_aberta-doc-dfp"
CVM_CAD = "https://dados.cvm.gov.br/dataset/cia_aberta-cad"
B3_COTAHIST = "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/"
BCB_432 = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json"
ITSA_RI = "https://ri.itausa.com.br/"
ITSA_REMUN = "https://ri.itausa.com.br/en/financial-information/shareholders-remuneration/"
L15270 = "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15270.htm"
LC224 = "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp224.htm"
L14754 = "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14754.htm"
IN1585 = "https://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=67494"
BOVA11_PROSP = "https://www.blackrock.com/br/products/251816/ishares-ibovespa-fundo-de-ndice-fund"
CMN5215 = "https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20CMN&numero=5215"

A = []  # achados


def ach(pid, trecho, problema, classe, correcao, fonte):
    A.append(dict(post_id=pid, trecho=trecho, problema=problema, classe=classe, correcao_sugerida=correcao, fonte=fonte))


# ---------------- 1033 Itsa4 ou Itub4 ----------------
ach(1033, "Banco Santander Brasil (ITSA4)", "Ticker trocado: ITSA4 é Itaúsa (holding que tem 37,5% do Itaú), não Santander. O Santander Brasil negocia como SANB11/SANB3/SANB4. O erro se repete no texto, nas tabelas e no FAQ.",
    "CRÍTICO", "Reescrever: comparação é Itaúsa (ITSA4) x Itaú Unibanco (ITUB4); tirar Santander do texto.", f"{CVM_CAD} (ITAUSA S.A., CNPJ 61.532.644/0001-15); {B3_COTAHIST} (ITSA4 = ITAUSA; SANB11 = SANTANDER BR)")
ach(1033, "Itaú S.A. (ITSA4)", "Nome errado: não existe 'Itaú S.A.'; ITSA4 é a PN da Itaúsa S.A.", "CRÍTICO", "Itaúsa (ITSA4).", CVM_CAD)
ach(1033, "As ações preferenciais da Itaú Unibanco, ITSA4 e ITUB4", "ITSA4 não é ação do Itaú Unibanco; é da Itaúsa.", "CRÍTICO", "ITUB4 é a PN do Itaú Unibanco; ITSA4 é a PN da Itaúsa.", CVM_CAD)
ach(1033, "Valor Patrimonial por Ação | R$ 40,21 | R$ 35,17", "VPA inventado. Itaú: PL consolidado de R$ 199,1 bi em 31/12/2023 para 9,80 bi de ações = ~R$ 20 por ação. Itaúsa: PL de R$ 82,95 bi para mais de 10 bi de ações = ~R$ 8. Com ITSA4 a R$ 10,42 em 14/11/2024, VPA de R$ 35 e P/L 10,2 implicariam preço de ~R$ 50.",
    "CRÍTICO", "Apagar a tabela ou refazer com DFP + cotação da data, citando a fonte.", f"{CVM_DFP} (DFP 2023 Itaú e Itaúsa); {B3_COTAHIST}")
ach(1033, "Investimentos em Tecnologia | R$ 8,5 bilhões | R$ 6,2 bilhões", "Número sem fonte, atribuído a Itaú e Santander, com 'lançamentos de produtos digitais 25 em 2021': sem lastro em documento das empresas.",
    "CRÍTICO", "Apagar (não há fonte).", "sem fonte no post; não consta nas DFPs/ITRs da CVM")
ach(1033, "ROE | 19,5% | 18,2%", "Tabela de ROE, margem e DY sem fonte nem data, com dois DY diferentes para a ITSA4 no mesmo post (5,2% e 4,5%).", "DÚVIDA",
    "Apagar ou refazer com dados da CVM e data.", CVM_DFP)

# ---------------- 983 preço justo ITSA4 ----------------
ach(983, "Receita Líquida (R$ milhões) | 57.863 | 69.725 | 75.210", "Números inventados. Itaúsa (DFP consolidada): receita de vendas R$ 8,17 bi (2021) e R$ 8,49 bi (2022); lucro do período R$ 13,29 bi (2021) e R$ 14,15 bi (2022), não 9.015 e 8.954.",
    "CRÍTICO", "Apagar a tabela; se quiser número, usar a DFP com fonte.", f"{CVM_DFP} (ITAÚSA S.A., DFP 2021 e 2022, contas 3.01 e 3.11)")
ach(983, "preço-alvo ITSA4 de R$ 34,50 por ação. Isso mostra um aumento de 15% em relação ao preço atual", "Preço-alvo e 'preço atual' incoerentes e sem fonte: a ITSA4 fechou a R$ 10,42 em 14/11/2024; R$ 34,50 seria +230%. Também é recomendação ('a recomendação ITSA4 é positiva').",
    "CRÍTICO", "Apagar preço-alvo e recomendação.", B3_COTAHIST)
ach(983, "Os principais concorrentes da Itaúsa no Brasil são: Banco Bradesco Banco do Brasil Banco Santander", "Holding comparada com bancos como 'concorrentes'; P/L 12,5x e P/VP 1,2x sem fonte nem data.", "DÚVIDA",
    "Comparar com outras holdings ou tirar.", "sem fonte")
ach(983, "Duratex (Dexco)", "Nomes antigos: Duratex virou Dexco em 2021 e Copagaz virou Copa Energia; faltava a CCR (hoje Motiva) no portfólio.", "DATADO",
    "Usar a lista do RI: Itaú Unibanco, Aegea, Motiva, Alpargatas, Copa Energia, Dexco, NTS.", ITSA_RI)

# ---------------- 998 Itausa o que é ----------------
ach(998, "A Itausa tem a maior parte das ações do banco Itaú", "Errado: a Itaúsa tem 37,5% do capital do Itaú e divide o controle com a família Moreira Salles via IUPAR (o próprio site diz isso no post 993).",
    "CRÍTICO", "Itaúsa tem 37,5% do capital e controle compartilhado via IUPAR.", ITSA_RI)
ach(998, "Receita Líquida (R$ Bilhões) | 25,6 | 27,8 | 30,2", "Números inventados: receita consolidada da Itaúsa foi R$ 8,17 bi (2021) e R$ 8,49 bi (2022); lucro R$ 13,3 bi e R$ 14,2 bi, não 7,5 e 8,1.",
    "CRÍTICO", "Apagar a tabela.", f"{CVM_DFP} (ITAÚSA S.A.)")
ach(998, "Índice de Governança Corporativa | 9,2 | 7,8", "Índice inexistente, sem fonte ('Conformidade com Leis 95%').", "CRÍTICO", "Apagar.", "não há índice com esse nome em CVM/B3")

# ---------------- 1003 Quanto rende ITSA4 ----------------
ach(1003, "Receita Líquida | R$ 85 bilhões | R$ 105 bilhões", "Projeção inventada: a receita consolidada da Itaúsa foi R$ 8,2 bi em 2024 e 2025; 'lucro de R$ 12 bi em 2025' também não bate (R$ 16,5 bi no consolidado de 2025).",
    "CRÍTICO", "Apagar projeções.", f"{CVM_DFP} (ITAÚSA S.A., DFP 2024 e 2025)")
ach(1003, "Alpargatas |  25,9% |  Vestuário e Calçados |  Dexco |  24,1%", "Participações erradas: o RI da Itaúsa informa ~30% na Alpargatas e ~37,7% na Dexco.", "CRÍTICO",
    "Usar a tabela do RI com data (como no post 993).", ITSA_RI)
ach(1003, "Dívida Líquida/EBITDA |  1,2x", "Indicador sem sentido para holding e sem fonte (tabela com 'média do setor' inventada).", "DÚVIDA", "Apagar.", "sem fonte")

# ---------------- 1008 Itausa dividendos ----------------
ach(1008, "Frequência de pagamento de dividendos |  Semestral", "A Itaúsa paga trimestralmente (R$ 0,02 por ação por trimestre) mais adicionais; o post 1003 do mesmo site diz trimestral.",
    "CRÍTICO", "Trimestral + dividendos adicionais, conforme a política de remuneração.", ITSA_REMUN)
ach(1008, "Petrobras |  6,8% |  Pagamentos mais irregulares", "Tabela comparativa sem data nem fonte (yield e valorização redondos).", "DÚVIDA", "Apagar ou refazer com fonte.", "sem fonte")

# ---------------- 1013 Itausa ações ----------------
ach(1013, "Fundação Itaú Unibanco |  39,8% |  Família Vilela Penido |  17,2% |  Família Moreira Salles |  14,2%", "Composição acionária inventada. Quem controla a Itaúsa é a família Egydio de Souza Aranha (33,55% do capital, 63,66% das ON em 29/05/2026, segundo o RI); a Moreira Salles é sócia no Itaú (IUPAR), não na Itaúsa.",
    "CRÍTICO", "Usar a composição do RI com data.", ITSA_RI)
ach(1013, "1974 – Aquisição do Unibanco , que se fundiu com o Itaú em 2008", "Falso: Itaú e Unibanco se associaram em 2008; não houve aquisição do Unibanco em 1974.", "CRÍTICO", "Apagar a linha.", ITSA_RI)
ach(1013, "2019 – Aquisição da participação acionária da família Setubal na Itausa, consolidando o controle da família Villela", "Evento inexistente; o controle segue com o grupo familiar Egydio de Souza Aranha (Setubal e Villela são ramos dele).", "CRÍTICO", "Apagar.", ITSA_RI)
ach(1013, "As corretoras principais para comprar ações Itausa na B3 são Itaú Corretora, XP Investimentos e Clear Corretora", "Cita corretoras pelo nome (regra do canal) e afirma 'principais' sem fonte.", "DÚVIDA", "Tirar os nomes.", "regra editorial")
ach(1013, "Valor de mercado |  R$ 80 bilhões", "Valor de mercado não bate: com ~10,3 bi a 10,9 bi de ações (RI) e ITSA4 a R$ 10,42 em 14/11/2024, passava de R$ 100 bi.", "DÚVIDA", "Apagar ou atualizar com data.", B3_COTAHIST)

# ---------------- 1038 Itausa paga dividendos mensais ----------------
ach(1038, "pelo menos 25% do lucro anual vai para os dividendos mensais dos acionistas", "A Itaúsa não paga dividendos mensais: são trimestrais (R$ 0,02/ação) mais adicionais. O título induz ao erro.",
    "CRÍTICO", "Responder no topo: não, a Itaúsa paga trimestralmente.", ITSA_REMUN)
ach(1038, "os JCP são tributados a 15% na fonte", "JCP: 17,5% na fonte desde 01/01/2026 (LC 224/2025).", "DATADO", "17,5% desde 2026.", LC224)
ach(1038, "Dividendos da Itausa não pagam imposto de renda para quem é pessoa física. Isso quer dizer que você não paga nada", "Desde jan/2026 há IRRF de 10% sobre dividendos acima de R$ 50 mil/mês da mesma empresa (Lei 15.270/2025).", "DATADO",
    "Acrescentar a regra de 2026.", L15270)

# ---------------- 1043 Itausa bonificação ----------------
ach(1043, "2020 |  Sim |  1:5 |  2017 |  Sim |  1:3 |  2014 |  Sim |  1:4", "Histórico de bonificações inventado: as bonificações recentes da Itaúsa foram de 5% (1 nova para 20) em dez/2021, nov/2023 e nov/2024.",
    "CRÍTICO", "Usar o histórico do RI.", ITSA_REMUN)
ach(1043, "Rentabilidade média anual |  12,5% |  15,8% |  Dividendos pagos por ação |  R$ 0,85", "Indicadores sem fonte nem período definido.", "DÚVIDA", "Apagar.", "sem fonte")

# ---------------- 1073 BOVA11 dividendos ----------------
ach(1073, "Em 2022, o BOVA11 pagou R$ 1,90 por cota em dividendos", "Falso: o BOVA11 não distribui proventos; dividendos e JCP das ações são reinvestidos no fundo.", "CRÍTICO",
    "Reescrever: BOVA11 reinveste os proventos; o retorno vem na cota.", BOVA11_PROSP)
ach(1073, "Os dividendos do BOVA11 têm imposto de 15% na fonte", "Não há dividendo distribuído pelo BOVA11, logo não há esse IR; e dividendos de ações não têm 15% na fonte (até R$ 50 mil/mês seguem isentos).", "CRÍTICO",
    "Tirar.", f"{BOVA11_PROSP}; {L15270}")
ach(1073, "BOVA11 |  15% na fonte |  Isento", "Errado: ganho de capital em ETF de ações paga 15% e não tem a isenção de R$ 20 mil; 'ações individuais 15% a 22,5%' também está errado (ações: 15% swing, 20% day trade).", "CRÍTICO",
    "ETF de ações: 15% sobre o ganho, sem isenção de R$ 20 mil.", IN1585)
ach(1073, "O BOVA11 tem uma taxa de apenas 0,30% ao ano", "A taxa do BOVA11 é 0,10% ao ano.", "CRÍTICO", "0,10% a.a.", BOVA11_PROSP)

# ---------------- lote de nov/2024 (ETFs e dividendos) ----------------
ach(1063, "o DIVO11 , o BOVD11 e o XDIV11", "BOVD11 e XDIV11 não existem na B3: nenhum negócio no COTAHIST à vista de 2021 a out/2026 (ETFs de ações aparecem no COTAHIST com CODBDI 14). A tabela dá até volatilidade para eles.",
    "CRÍTICO", "Usar só ETFs que existem (ex.: DIVO11, NDIV11), com dados da gestora.", B3_COTAHIST)
ach(1068, "o SMAL11 e o GLOB11 são boas escolhas. Eles seguem o S&P 500 e o MSCI World", "SMAL11 segue o índice Small Cap da B3 (o próprio post diz isso mais abaixo), não o S&P 500; GLOB11 não aparece no COTAHIST 2021-2026.",
    "CRÍTICO", "SMAL11 = small caps brasileiras; tirar GLOB11.", B3_COTAHIST)
ach(1068, "BOVA11 |  Ibovespa |  ETF mais rentável em ações brasileiras |  0,30% a.a.", "Taxa do BOVA11 é 0,10% a.a.; 'mais rentável' sem fonte.", "CRÍTICO", "0,10% a.a.", BOVA11_PROSP)
ach(1083, "o IVVB11 replica o desempenho de títulos privados de crédito", "IVVB11 é ETF de ações que replica o S&P 500 (em reais), não renda fixa; e não paga rendimento mensal (reinveste).",
    "CRÍTICO", "IVVB11 = S&P 500, reinveste proventos.", "https://www.blackrock.com/br/products/251816/ ; " + B3_COTAHIST + " (IVVB11 = ISHARE SP500)")
ach(1083, "IMAB11 |  Renda Fixa |  Mensal |  5,2% a.a. |  IVVB11 |  Renda Fixa |  Mensal |  6,1% a.a. |  DIVI11 |  Ações |  Mensal", "Tabela inventada: IVVB11 e SMAL11 não distribuem rendimentos; IMAB11 segue o IMA-B (títulos atrelados ao IPCA de todos os prazos), não 'curto prazo'; DIVI11 não existe.",
    "CRÍTICO", "Apagar a tabela.", B3_COTAHIST)
ach(1083, "SDIV11, RYDJ11, XDIV11 e DIVO11", "SDIV11, RYDJ11 e XDIV11 não aparecem no COTAHIST à vista 2021-2026 (não existem na B3).", "CRÍTICO", "Tirar.", B3_COTAHIST)
ach(1083, "Dividendos |  15% |  Ganhos de Capital |  Até 22,5%", "IR de ETF de ações: 15% sobre o ganho de capital; tabela regressiva só vale para ETF de renda fixa.", "CRÍTICO", "Separar ETF de ações (15%) e de renda fixa (tabela própria).", IN1585)
ach(1088, "Renda Fixa |  15% |  Até 6 meses |  Renda Fixa |  17,5% |  Acima de 6 meses e até 1 ano |  Renda Fixa |  20% |  Acima de 1 ano |  Ações |  Isento |  Acima de 180 dias",
    "Tabela de IR invertida e inventada: a regressiva é 22,5% até 180 dias, 20% até 360, 17,5% até 720 e 15% acima; não existe isenção de ETF de ações 'acima de 180 dias' (é 15% sobre o ganho).",
    "CRÍTICO", "Corrigir a tabela regressiva e a regra de ETF de ações.", "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l11033.htm ; " + IN1585)
ach(1088, "iShares S&P 500 – Replicação do índice S&P 500, com retorno médio anual de 18,5%", "Retornos médios sem período nem fonte; 'Bradesco Small Caps', 'Itaú Dividend' e 'Vanguard Real Estate' não são ETFs listados na B3 com esses nomes.", "DÚVIDA", "Apagar a lista.", "sem fonte")
ach(1098, "Tecnologia |  BRTC11 |  18% |  12% |  Energia |  BREN11 |  25% |  16% |  Commodities |  BCOM11", "BRTC11, BREN11 e BCOM11 não existem na B3 (nenhum negócio no COTAHIST 2021-2026); rentabilidades inventadas.", "CRÍTICO", "Apagar a tabela.", B3_COTAHIST)
ach(1113, "Empresa XYZ: Dividend yield de 5,8% ao mês", "Texto-modelo publicado ('Empresa XYZ', 'Empresa ABC', 'Empresa 123', 'Empresa A/B/C') com yields mensais impossíveis (5,8% ao mês).", "CRÍTICO", "Despublicar ou reescrever do zero.", "erro evidente no próprio texto")
ach(1158, "Enel Brasil (ENBR3)", "Ticker trocado: ENBR3 era a EDP Energias do Brasil (nome de pregão ENERGIAS BR), não Enel; e saiu da bolsa em ago/2023 (OPA da EDP), mais de um ano antes do post.", "CRÍTICO", "Tirar ENBR3.", B3_COTAHIST + " (ENBR3 = ENERGIAS BR, último negócio 21/08/2023)")
ach(1158, "Telefônica Brasil (VIVT4)", "VIVT4 não negocia desde antes de 2021 (classes unificadas em VIVT3); nenhum negócio no COTAHIST 2021-2026.", "CRÍTICO", "VIVT3.", B3_COTAHIST)
ach(1158, "Oi |  5,2% |  Distribuição mínima de 25% do lucro líquido", "Oi estava em recuperação judicial e não pagava dividendos; Claro não tem ação na B3. Tabela inventada.", "CRÍTICO", "Apagar.", B3_COTAHIST)
ach(1158, "Itaú Unibanco |  Distribuir no mínimo 50% do lucro líquido ajustado |  12,4 bilhões", "Política e valores de dividendos dos bancos sem fonte (o mínimo estatutário do Itaú é 25%).", "DÚVIDA", "Conferir no RI de cada banco ou apagar.", "https://www.itau.com.br/relacoes-com-investidores/")
ach(1138, "Petrobras (PETR4) – Dividend Yield de 15,2%", "DY sem data nem fonte; o post 1158, publicado no mesmo dia, dá 7,2% para a mesma ação.", "DÚVIDA", "Apagar ou datar com fonte.", "sem fonte")
ach(1153, "Itaú Unibanco |  Bancário |  Compra |  12% |  Magazine Luiza |  Varejo |  Compra", "Recomendação de compra atribuída a 'analistas' sem fonte nem data.", "DÚVIDA", "Tirar a coluna de recomendação.", "sem fonte")
ach(1108, "CDBs , LCIs e LCAs têm alíquotas de IR de 15% a 22,5%", "LCI e LCA são isentas de IR para pessoa física (Lei 11.033/2004, art. 3º; mantido em 2026). Só o CDB segue a tabela regressiva.",
    "CRÍTICO", "CDB: 22,5% a 15%; LCI/LCA: isentas para PF.", "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l11033.htm")
ach(1108, "Itaú |  R$ 35,00 |  Sim |  Bradesco |  R$ 40,00", "Taxas de corretagem atribuídas a bancos sem fonte nem data (e cita instituições pelo nome).", "DÚVIDA", "Apagar a tabela.", "sem fonte")
ach(1128, "Tributação de 15% para o investidor pessoa física |  Isenção de imposto de renda para o investidor pessoa física", "Tabela invertida: quem tinha 15% na fonte era o JCP (17,5% desde 2026) e o dividendo era isento (desde 2026, isento até R$ 50 mil/mês por empresa).",
    "CRÍTICO", "Dividendo: isento até R$ 50 mil/mês/empresa; JCP: 17,5% na fonte.", f"{L15270}; {LC224}")
ach(1133, "Os benefícios incluem baixo risco, isenção de imposto e várias opções de títulos", "Tesouro Direto não é isento: paga IR pela tabela regressiva (22,5% a 15%) e IOF nos primeiros 30 dias.",
    "CRÍTICO", "Tirar 'isenção de imposto'.", "https://www.tesourodireto.com.br/")
ach(1143, "Tesouro Direto |  15% |  0% |  CDB |  22,5% a 27,5%", "Tabela de IR errada: Tesouro e CDB seguem a mesma regressiva de 22,5% a 15%; 27,5% é a alíquota máxima da tabela do IRPF, não de CDB.",
    "CRÍTICO", "Tesouro e CDB: 22,5% (até 180 dias) a 15% (acima de 720 dias).", "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l11033.htm")
ach(1148, "Juros sobre Capital Próprio (JCP) |  Tributados na fonte em 15%", "JCP: 17,5% desde 2026; dividendos acima de R$ 50 mil/mês têm 10% na fonte.", "DATADO", "Atualizar com LC 224/2025 e Lei 15.270/2025.", f"{LC224}; {L15270}")
ach(1103, "A média anual é de 12% a 15% nos últimos 10 anos", "Média de renda fixa sem fonte; o CDI médio de 2015-2024 ficou bem abaixo de 12% a.a. (houve anos com Selic de 2%).", "DÚVIDA", "Citar o CDI acumulado pela série do BCB.", "https://api.bcb.gov.br/dados/serie/bcdata.sgs.4389/dados?formato=json")

# ---------------- lote de nov/2024 (FIIs) ----------------
ach(1163, "O fundo tenha pelo menos 50 cotistas.", "Desde a Lei 14.754/2023 (dez/2023), a isenção exige 100 cotistas ou mais; o post é de nov/2024 e foi revisado em set/2026.", "CRÍTICO",
    "100 cotistas ou mais; cotas só em bolsa; cotista com menos de 10%.", L14754)
ach(1168, "Tributação de Ganho de Capital |  15% |  Aplicável tanto a pessoas físicas quanto jurídicas", "Ganho na venda de cota de FII é 20% (o próprio post diz 20% no FAQ).", "CRÍTICO", "20%.", "https://www.planalto.gov.br/ccivil_03/leis/l8668.htm (art. 18) ; " + IN1585)
ach(1173, "O investidor deve manter as cotas por pelo menos 90 dias. O fundo também deve distribuir 95% de seus lucros", "Requisito inventado: não existe prazo mínimo de 90 dias para a isenção; a regra é fundo com 100+ cotistas, cotas em bolsa e cotista com menos de 10%. Os 95% são obrigação do fundo (Lei 8.668), não condição da isenção.",
    "CRÍTICO", "Usar os requisitos da Lei 14.754/2023.", L14754)
ach(1178, "FIIÁreas (AREA11)", "Fundos inexistentes: AREA11, HGPR11, TRPG11, MAUA11, LOGG11 ('Caixa Logística'), RNDV11, LOGI11 e MASA11 não têm nenhum negócio no COTAHIST 2021-2026. A tabela dá até 'ocupação' para eles.",
    "CRÍTICO", "Despublicar ou reescrever do zero só com fundos que existem.", B3_COTAHIST)
ach(1178, "FII Kinea Índices (KNIP11) |  9,1% |  92%", "KNIP11 é fundo de papel (CRIs), não tem 'ocupação'; números sem fonte.", "CRÍTICO", "Tirar.", B3_COTAHIST + " (KNIP11 = FII KINEA IP)")
ach(1183, "KNRI11 , IRDM11, JHSF11", "JHSF11 não existe (a JHSF negocia JHSF3); IRDM11 parou de negociar em out/2025.", "CRÍTICO", "Tirar JHSF11; atualizar IRDM11.", B3_COTAHIST)
ach(1188, "Imposto de Renda (IR) |  Isenção sobre rendimentos e ganhos de capital |  Imposto de Renda na Fonte (IRF) |  15% sobre os rendimentos recebidos", "Contraditório e errado: rendimento é isento para PF que cumpre os requisitos; ganho de capital paga 20%; não há 15% na fonte para PF.",
    "CRÍTICO", "Rendimentos isentos (requisitos da Lei 14.754); ganho de capital 20%.", L14754)
ach(1188, "nenhum cotista pode ter mais de 25% das cotas do FII", "Regra inventada: os 25% são o limite para o incorporador/construtor sem que o fundo seja tributado como PJ (Lei 9.779/1999, art. 2º), não uma proibição a cotistas.",
    "CRÍTICO", "Explicar a regra certa ou tirar.", "https://www.planalto.gov.br/ccivil_03/leis/l9779.htm")
ach(1188, "RLOG11 |  7,2% |  Trimestral", "RLOG11 não aparece no COTAHIST 2021-2026.", "CRÍTICO", "Tirar.", B3_COTAHIST)
ach(1188, "Instrução CVM nº 472/2008", "A ICVM 472 foi substituída pela Resolução CVM 175 (Anexo III) em 2023.", "DATADO", "Resolução CVM 175.", "https://conteudo.cvm.gov.br/legislacao/resolucoes/resol175.html")
ach(1193, "A alíquota varia de 15% a 22,5%, dependendo do lucro.", "Ganho na venda de cotas de FII é 20% fixo (a tabela logo abaixo diz 20%). Post duplicado do 1213, mesmo título.", "CRÍTICO", "20%; juntar com 1213.", "https://www.planalto.gov.br/ccivil_03/leis/l8668.htm")
ach(1213, "Tributação na venda de cotas |  15% a 22,5%", "Ganho na venda de cotas de FII é 20%.", "CRÍTICO", "20%.", "https://www.planalto.gov.br/ccivil_03/leis/l8668.htm")
ach(1208, "Atualmente, os principais são ALUG11, XFIX11 e URET11.", "URET11 parou de negociar em 10/10/2024, antes do post; volume e patrimônio citados sem data.", "CRÍTICO", "Tirar URET11.", B3_COTAHIST)

# ---------------- 2026: ON x PN ----------------
LSA = "https://www.planalto.gov.br/ccivil_03/leis/l6404consol.htm"
ach(4848, "Para ON, é obrigatório 100% do preço pago. Para PN, foi definido um mínimo de 80%.", "Invertido/errado: a Lei 10.303/2001 (art. 254-A da Lei 6.404) garante tag along de no mínimo 80% às ações COM VOTO (ON); para PN não há tag along obrigatório por lei. O post 1028 do mesmo site diz certo.",
    "CRÍTICO", "ON: mínimo de 80% por lei; PN: só se o estatuto conceder.", LSA)
ach(4848, "Mai/2026 | R$36,80 | R$35,50 | +R$1,30", "Tabela de preços 'Fonte: B3' não bate com o COTAHIST: média de mai/2026 foi R$ 50,17 (PETR3) e R$ 45,25 (PETR4); jan/2023 foi R$ 28,25 e R$ 24,92. O spread real passou de R$ 4.",
    "CRÍTICO", "Refazer a tabela com o COTAHIST, dizendo se é preço ajustado ou não.", B3_COTAHIST)
ach(4848, "ITUB3 (ON) |  |  3.1% |  ITUB4 (PN) |  |  3.3%", "DY de 2025 do Itaú muito abaixo do que o próprio site publica (post 1053: 12,1% na ITUB4 em 2025; página ITUB4 do site-ativos: DY de caixa de 6,3% em 12 meses).", "DÚVIDA",
    "Usar uma só fonte, com data.", "site-ativos/cache/fichas/ITUB4.json (CVM DFC + COTAHIST)")
ach(4848, "Controlador | Governo Federal (~36%)", "A União tem a maioria das ON (50,26%), que é o que dá o controle; ~36% é a fatia no capital total somando BNDES/BNDESPar. O número sem explicação engana.", "DÚVIDA", "Dizer 'União: maioria das ações ON'.", "https://www.investidorpetrobras.com.br/visao-geral/composicao-acionaria/")
ach(4536, "A família Moreira Salles controla o banco com participação dominante", "Errado: o Itaú é controlado pela IUPAR, dividida 50/50 entre Itaúsa e família Moreira Salles (o post 993 do site explica).", "CRÍTICO",
    "Controle compartilhado Itaúsa + Moreira Salles via IUPAR.", ITSA_RI)
ach(4536, "A ITUB4 negocia em torno de R$ 600 milhões por dia. A ITUB3 gira R$ 40-50 milhões", "No COTAHIST, a média de fev a mai/2026 foi R$ 1,36 bi (ITUB4) e R$ 71 mi (ITUB3): ~19 vezes, não 12.", "DÚVIDA", "Atualizar com data.", B3_COTAHIST)
ach(4536, "Em 2025, o banco tem valor de mercado próximo de R$ 300 bilhões", "Com 11,03 bi de ações e ITUB4 a R$ 39,23 (30/12/2025), o valor de mercado passava de R$ 400 bi; hoje ~R$ 509 bi.", "DÚVIDA", "Atualizar com data.", f"{B3_COTAHIST}; {CVM_DFP} (composição do capital)")
ach(4845, "O controle do Itaú Unibanco está na mão da Itaúsa (família Setúbal/Egydio)", "Incompleto: o controle é compartilhado com a família Moreira Salles via IUPAR. Além disso, 4845 e 4536 são o mesmo assunto publicado com 1 dia de diferença.", "DÚVIDA", "Corrigir e juntar os dois.", ITSA_RI)

# ---------------- JEPQ39 (produto que não existe na B3) ----------------
JEPQ_FONTE = B3_COTAHIST + " (nenhum negócio de JEPQ39 de jan/2021 a 01/10/2026; JEPI39 = 'JPM JEPI', negocia desde 23/02/2026); o próprio post 4538 do site, corrigido em 28/09/2026, diz que o JEPQ39 não existe"
for pid, tr in [(4537, "JEPQ39 | JEPQ (JPMorgan) | Covered call Nasdaq 100 | 10–15%"),
                (4544, "BDRs de ETFs como JEPI39 e JEPQ39 são negociados na B3 normalmente"),
                (4568, "olhe para BDRs de ETFs como JEPI39 ou JEPQ39, que distribuem dividendos mensais"),
                (4572, "JEPI39/JEPQ39 (~8% líq. a.a.)"),
                (4573, "3. ETFs de renda em dólar (JEPI39, JEPQ39)"),
                (4816, "ETFs como JEPI39 e JEPQ39 é tributada no Brasil à alíquota de 15%"),
                (3172, "Critério | JEPI (JEPI39) | JEPQ (JEPQ39)")]:
    ach(pid, tr, "Produto inexistente: não há BDR JEPQ39 na B3; o JEPQ só é negociado nos EUA.", "CRÍTICO",
        "Tirar o JEPQ39 ou dizer que ele não existe na B3 (como o post 4538 corrigido).", JEPQ_FONTE)
ach(4544, "BNDW39 | BDR do Vanguard Total World Bond ETF", "BNDW39 e DVDY11 não aparecem no COTAHIST à vista 2021-2026.", "CRÍTICO", "Tirar.", B3_COTAHIST)
ach(4544, "Qualquer corretora com acesso à bolsa brasileira permite a compra", "O JEPI39 foi lançado em 23/02/2026 e, segundo as notícias do lançamento, é destinado a investidores qualificados; não confirmado na fonte primária (prospecto bloqueado pela rede).", "DÚVIDA",
    "Conferir o público-alvo no prospecto/B3 antes de afirmar.", "https://www.b3.com.br/pt_br/produtos-e-servicos/negociacao/renda-variavel/brazilian-depositary-receipts-bdrs-de-etf.htm")
ach(4538, "Aparece no cadastro da B3 a partir de maio de 2026.", "O JEPI39 negocia desde 23/02/2026 (COTAHIST); o post 3172, de 26/02/2026, já falava dele.", "DÚVIDA", "Fevereiro de 2026.", B3_COTAHIST)
ach(4816, "BOVA39", "BOVA39 não existe (o ETF do Ibovespa é BOVA11); não aparece no COTAHIST.", "CRÍTICO", "BOVA11.", B3_COTAHIST)

# ---------------- IR ----------------
RFB_IRPF26 = "https://www.gov.br/receitafederal/pt-br/assuntos/noticias/2026/marco/receita-comeca-a-receber-declaracoes-do-irpf-no-dia-23-de-marco-prazo-de-entrega-se-encerra-em-29-de-maio"
ach(3435, "O prazo para entrega da declaração vai até o final de abril de 2026", "Prazo errado: a declaração do IRPF 2026 foi de 23/03 a 29/05/2026.", "CRÍTICO", "23 de março a 29 de maio de 2026.", RFB_IRPF26)
ach(3435, "desde que o fundo tenha mais de 50 cotistas", "Desde a Lei 14.754/2023 a isenção exige 100 cotistas ou mais (vale para o ano-base 2025 do guia).", "CRÍTICO", "100 cotistas ou mais.", L14754)
ach(3435, "Os dividendos distribuídos por empresas brasileiras são isentos de Imposto de Renda para a pessoa física, por força da lei", "Certo para o ano-base 2025 do guia, mas o post foi revisado em set/2026 sem avisar que, a partir de 2026, há IRRF de 10% acima de R$ 50 mil/mês e JCP a 17,5%.", "DATADO",
    "Acrescentar nota sobre 2026 (Lei 15.270/2025 e LC 224/2025).", f"{L15270}; {LC224}")
ach(2819, "O projeto de lei que expande a isenção do Imposto de Renda para até R$ 5 mil mensais foi aprovado na Câmara", "O projeto virou a Lei 15.270, sancionada em 26/11/2025 e em vigor desde jan/2026; o texto ainda fala em 'segue para o Senado' e 'deve começar'.", "DATADO",
    "Atualizar para lei em vigor.", L15270)

# ---------------- glossário de 07/05/2026 (IR) ----------------
PERGUNTAO = "https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/perguntas-frequentes/declaracoes/dirpf"
for pid, tr in [(5092, "JCP |  15% (retido na fonte)"), (5058, "a corretora retém 15% de IR na fonte"), (5093, "JCP: 15% de IR retido na fonte"), (4874, "juros sobre capital próprio são tributados em 15%")]:
    ach(pid, tr, "Publicado em mai/2026 com JCP a 15%: desde 01/01/2026 o IRRF sobre JCP é 17,5% (LC 224/2025). Os exemplos numéricos (R$ 425 líquidos de R$ 500 etc.) ficam errados.", "CRÍTICO", "17,5%; refazer os exemplos.", LC224)
for pid, tr in [(5092, "FII (rendimentos): desde que o FII tenha mais de 50 cotistas"), (5093, "isentos de IR se o FII tem mais de 50 cotistas"), (5059, "desde que o fundo tenha pelo menos 50 cotistas"), (4874, "O FII precisa ter mais de 50 cotistas"), (4815, "FIIs com mais de 50 cotistas negociados em bolsa"), (5067, "desde que o fundo tenha mais de 50 cotistas"), (4873, "Isento (cotas negociadas em bolsa, > 50 cotistas)")]:
    ach(pid, tr, "Requisito desatualizado desde dez/2023: a isenção exige 100 cotistas ou mais (Lei 14.754/2023), e o cotista precisa ter menos de 10% das cotas.", "CRÍTICO", "100 cotistas ou mais; menos de 10% das cotas.", L14754)
ach(5092, "Dividendos de ações: isentos para pessoa física (debate tributário em andamento no Congresso)", "Em mai/2026 já valia a Lei 15.270/2025: IRRF de 10% sobre dividendos acima de R$ 50 mil/mês da mesma empresa e IRPF mínimo para renda acima de R$ 600 mil/ano. Não é 'debate'.", "CRÍTICO", "Explicar a regra em vigor.", L15270)
ach(5092, "Geralmente exigem carência mínima de 90 a 360 dias", "Prazo mínimo de LCI/LCA sem índice de preços é 6 meses (Res. CMN 5.215/2025); 90 dias não vale desde 2024.", "CRÍTICO", "6 meses (pós/prefixadas); 12 meses LCA e 36 meses LCI com IPCA.", CMN5215)
ach(4875, "A isenção está prevista na Lei 8.668/1993 (LCI) e na Lei 11.076/2004 (LCA)", "Lei errada: a Lei 8.668/1993 é a dos FIIs. A isenção de LCI e LCA para PF está no art. 3º da Lei 11.033/2004.", "CRÍTICO", "Lei 11.033/2004, art. 3º, II e IV.", "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l11033.htm")
ach(4875, "Carência mínima |  90 dias (prefixada) / 12 meses (pós-fixada) |  90 dias", "Prazo mínimo desde mai/2025: 6 meses para LCI e LCA sem correção por índice de preços; com IPCA, 36 meses (LCI) e 12 meses (LCA).", "CRÍTICO", "Atualizar a tabela.", CMN5215)
ach(4875, "Plataformas (XP, BTG) |  |  94% CDI", "Cita instituições pelo nome (regra do canal) e taxas 'médias de mercado' sem fonte.", "DÚVIDA", "Tirar nomes; citar fonte das taxas.", "regra editorial")
ach(5042, "carência mínima de 90 dias (e muitas vezes 1 ano)", "Prazo mínimo da LCI: 6 meses (Res. CMN 5.215/2025).", "CRÍTICO", "6 meses.", CMN5215)
ach(4565, "A LCI tem prazo mínimo de 90 dias (resolução CMN 4.095)", "Desatualizado desde fev/2024 (Res. CMN 5.119) e de novo em mai/2025 (Res. 5.215): hoje 6 meses.", "CRÍTICO", "6 meses (Res. CMN 5.215/2025).", CMN5215)
ach(4566, "A LCA tem prazo mínimo de 90 dias , assim como a LCI.", "Prazo mínimo hoje: 6 meses (Res. CMN 5.215/2025).", "CRÍTICO", "6 meses.", CMN5215)
ach(4816, "O Brasil não cobra IR novamente sobre essa parcela para pessoas físicas", "Errado: dividendo de BDR é tributável no Brasil (carnê-leão/tabela progressiva, com compensação do imposto pago lá fora) e vai em 'Rendimentos tributáveis recebidos do exterior', não em isentos.", "CRÍTICO",
    "Dividendo de BDR: tributável pelo carnê-leão; declarar como rendimento do exterior.", PERGUNTAO)
ach(4816, "Código DARF: 8523 (ganhos em renda variável — bolsa brasileira)", "O código de renda variável em bolsa para PF é 6015; 8523 é ganho de capital em moeda estrangeira.", "CRÍTICO", "6015.", "https://www.gov.br/receitafederal/pt-br/assuntos/orientacao-tributaria/pagamentos-e-parcelamentos/codigos-de-receita")

# ---------------- tickers errados / que já não negociam (conferidos no COTAHIST) ----------------
ach(5113, "Exemplos: ALBT34 (Arbor Realty), LVHD34 (ETF de dividendos)", "ALBT34 e LVHD34 não existem na B3 (nenhum negócio no COTAHIST 2021-2026).", "CRÍTICO", "Tirar ou citar BDRs que existem, conferidos na B3.", B3_COTAHIST)
ach(5113, "XRES11, TVRI11 e similares — ETFs que replicam índices de REITs americanos", "XRES11 não existe; TVRI11 é um FII brasileiro (Tivio Renda Imobiliária), não ETF de REITs.", "CRÍTICO", "Tirar.", B3_COTAHIST + " (TVRI11 = FII TIVIO RI)")
ach(5114, "ETFs como BKCH11 na B3 reúnem esse tipo de ativo", "[leve] Ticker errado: na B3 o que existe é o BDR BKCH39 (GX Blockchain); BKCH11 não aparece no COTAHIST.", "CRÍTICO", "BKCH39 (BDR de ETF).", B3_COTAHIST)
ach(5119, "NAMO11: Nasdaq 100 em reais — 0,30%", "NAMO11 não existe na B3 (o ETF de Nasdaq 100 listado é o NASD11, entre outros).", "CRÍTICO", "Corrigir o ticker conferindo na B3.", B3_COTAHIST)
ach(10097, "Cruzeiro do Sul Educacional |  CSDE3", "[leve] Ticker errado: a Cruzeiro do Sul negocia como CSED3.", "CRÍTICO", "CSED3.", B3_COTAHIST)
ach(12158, "ABNB34 aqui na B3", "[leve] Ticker errado: o BDR da Airbnb é AIRB34; ABNB34 não existe.", "CRÍTICO", "AIRB34.", B3_COTAHIST)
ach(4874, "considere um ETF de FIIs como o IFIX11", "IFIX11 não existe: IFIX é o índice; ETFs de FII listados são, por exemplo, XFIX11.", "CRÍTICO", "XFIX11 (ou 'ETF que replica o IFIX').", B3_COTAHIST)
ach(4874, "Exemplos: BCFF11, RBRF11.", "[leve] BCFF11 já não negociava quando o post saiu (último pregão 18/10/2024); RBRF11 parou em 02/10/2025.", "CRÍTICO", "Trocar os exemplos.", B3_COTAHIST)
ach(4815, "FIIs de fundos de fundos (FOFs) como BCFF11 ou HFOF11", "[leve] BCFF11 parou de negociar em 18/10/2024, antes do post (mai/2026).", "CRÍTICO", "Tirar BCFF11.", B3_COTAHIST)
ach(4573, "utilities (TAEE11, TRPL4, CMIG4)", "[leve] TRPL4 virou ISAE4 em nov/2024 e MALL11 (citado no mesmo post) deixou de negociar em jul/2025; o post é de mai/2026.", "CRÍTICO", "ISAE4; tirar MALL11.", B3_COTAHIST)
ach(4873, "TRPL4 |  |  8.7%", "[leve] TRPL4 não negocia desde 14/11/2024 (virou ISAE4); o post é de mai/2026 e dá DY de 12 meses para ele.", "CRÍTICO", "ISAE4, com DY recalculado.", B3_COTAHIST)
ach(1078, "o MALL11 foca no varejo", "MALL11 era um FII de shoppings (não ETF) e deixou de negociar em jul/2025.", "CRÍTICO", "Tirar.", B3_COTAHIST)
ach(2086, "Grupo Arezzo (ARZZ3)", "[leve] ARZZ3 deixou de negociar em 31/07/2024 (fusão que criou a Azzas 2154, AZZA3), antes do post (mar/2025).", "CRÍTICO", "AZZA3.", B3_COTAHIST)
ach(4812, "Taxa de administração | 0,30% a.a. | 0,24% a.a.", "Taxa do BOVA11 é 0,10% a.a. (o post 5091 do site diz 0,10%); IVVB11 é 0,23% (post 4568).", "CRÍTICO", "BOVA11 0,10%; IVVB11 0,23%.", BOVA11_PROSP)
ach(11638, "só pela atualização trimestral da B3", "[leve] A carteira do Ibovespa é revista a cada 4 meses (jan, mai, set), não por trimestre (o próprio post fala na entrada de setembro).", "CRÍTICO", "quadrimestral.", "https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/ibovespa.htm")
ach(5091, "composta pelas ações mais negociadas da B3 ponderadas por liquidez", "Desde 2014 o Ibovespa pondera pelo valor de mercado do free float (a liquidez é critério de entrada), não por liquidez.", "DÚVIDA", "Conferir na metodologia da B3.", "https://www.b3.com.br/pt_br/market-data-e-indices/indices/indices-amplos/ibovespa.htm")
ach(7378, "a participação da Itaúsa (13,27%)", "[leve] Em mai/2026 a fatia na Aegea já era 14,01% (aumento concluído em mar/2026, segundo os posts 993 e 1028 do site).", "DÚVIDA", "14,0%.", ITSA_RI)
ach(2795, "Valor de Fechamento (01/10/2025): R$ 104,80 por cota.", "[leve] O COTAHIST registra fechamento de R$ 103,62 em 01/10/2025.", "DÚVIDA", "R$ 103,62.", B3_COTAHIST)
ach(1782, "serão emitidas 149 milhões de ações ao preço de R$ 6,70 cada", "Preço de subscrição aparece como R$ 6,70 e R$ 6,79 no mesmo post; total de proventos 'R$ 8,11 bi' não fecha com as parcelas citadas (R$ 4,4 bi + R$ 1,1 bi).", "DÚVIDA", "Conferir no fato relevante da Itaúsa.", ITSA_RI)
ach(1488, "Desde o seu lançamento nos EUA, o ETF equivalente ao COIN11 já pagou uma média de 2% a 2,3% ao mês em dividendos", "Rendimento mensal de 2% a 2,3% e 'investe diretamente em Bitcoin' sem fonte; regulamento do COIN11 não conferido.", "DÚVIDA", "Conferir no regulamento/site da gestora.", B3_COTAHIST + " (COIN11 = ETF BV COIN, negocia desde 13/12/2024)")
ach(2443, "negociados em bolsa como se fossem ações comuns.1", "Texto colado de ferramenta de IA com os números das notas de rodapé soltos no meio das frases ('.1', '.3', '.12') e sem as fontes.", "DÚVIDA", "Revisar o texto e pôr as fontes.", "padrão de texto de IA")

# ---------------- JCP 15% e dividendo 'isento' sem a regra de 2026 (candidatos da varredura, conferidos) ----------------
for pid, tr in [(7376, "Já o JCP (Juros sobre Capital Próprio), que a Telefônica usa bastante, tem retenção de 15% na fonte."),
                (10424, "JCP é uma despesa dedutível para a empresa, tributada em 15% na fonte para o acionista."),
                (4873, "onde a empresa desconta 15% na fonte antes de creditar na sua conta"),
                (5051, "JCP tem retenção de 15% na fonte.")]:
    ach(pid, tr, "Publicado em 2026 com JCP a 15%: desde 01/01/2026 a retenção é de 17,5% (LC 224/2025).", "CRÍTICO", "17,5%.", LC224)
for pid, tr in [(11719, "Dividendos de ações pagos a pessoa física são isentos de IR pela legislação em vigor."),
                (7376, "Dividendos de ações são isentos de IR para pessoa física no Brasil."),
                (5051, "Dividendos recebidos por pessoas físicas no Brasil são isentos de IR"),
                (5077, "os dividendos são isentos de Imposto de Renda para pessoa física"),
                (5093, "Dividendos de ações: isentos de IR para pessoa física (Brasil é um dos poucos países com essa isenção)"),
                (5058, "O dividendo é isento de IR para a pessoa física e não dedutível para a empresa."),
                (4814, "Vantagem: dividendos de ações são isentos de IR."),
                (7530, "Dividendos no Brasil são isentos de IR para pessoa física."),
                (1138, "coloque os dividendos na ficha “Rendimentos Isentos e Não Tributáveis”")]:
    ach(pid, tr, "Isenção total de dividendos deixou de valer em jan/2026 (Lei 15.270/2025): IRRF de 10% sobre o que passar de R$ 50 mil/mês da mesma empresa e IRPF mínimo para renda acima de R$ 600 mil/ano. Para a maioria dos pequenos investidores segue isento, mas a frase sem ressalva ficou errada.",
        "DATADO", "Acrescentar a ressalva da Lei 15.270/2025.", L15270)


# ---------------- destino sugerido (posts com CRÍTICO) ----------------
# 'corrigir' = trocar trechos; 'reescrever' = texto novo no mesmo endereço; '301 -> id' = juntar no post indicado; 'despublicar'.
DESTINOS = {
    1033: ("301 -> 1053", "O 1053 (reescrito em set/2026, com fontes) já responde 'ITSA4 x ITUB4'; o 1033 é o caso Santander/ITSA4."),
    983: ("301 -> 7378", "Preço-alvo e tabelas inventados; o 7378 trata o valuation da Itaúsa (desconto de holding) com dados do RI."),
    998: ("301 -> 993", "O 993 (reescrito, com RI) explica o que a Itaúsa tem e quem controla."),
    1003: ("301 -> 1008", "Mesmo assunto (rendimento/dividendos da ITSA4); juntar no guia de dividendos depois de reescrevê-lo."),
    1008: ("reescrever", "É o 'guia de dividendos da Itaúsa' linkado pelo 1053; refazer com a política de remuneração do RI e proventos por ano."),
    1013: ("301 -> 993", "Composição acionária e histórico inventados; o 993 cobre o tema com fonte."),
    1038: ("301 -> 1008", "Título promete 'dividendos mensais' (falso); responder 'não, trimestrais' dentro do 1008."),
    1043: ("reescrever", "Assunto próprio (bonificação), mas o histórico é inventado; refazer com as bonificações do RI (5% em 2021, 2023 e 2024)."),
    1073: ("301 -> 5091", "BOVA11 não distribui dividendos; o 5091 (O que é BOVA11) tem a taxa certa e pode responder 'BOVA11 paga dividendos? Não, reinveste'."),
    1063: ("301 -> 4537", "Lista ETFs que não existem; juntar no post de ETFs de dividendos de 2026 depois de tirar o JEPQ39 dele."),
    1083: ("301 -> 4537", "Tabela inventada e tickers inexistentes; mesmo tema do 4537."),
    1068: ("301 -> 5064", "Guia genérico de 2024 com erros de índice e taxa; juntar no 'O que é ETF'."),
    1078: ("301 -> 5064", "Mesmo tema genérico ('melhor ETF do momento'), com MALL11 como ETF."),
    1098: ("301 -> 5064", "Tabela de ETFs setoriais que não existem."),
    1088: ("corrigir", "Tabela de IR de ETF invertida; corrigir a tabela regressiva e a regra de ETF de ações (ou 301 -> 5064)."),
    1113: ("despublicar", "Texto-modelo publicado ('Empresa XYZ', 5,8% ao mês)."),
    1158: ("reescrever", "Ranking de 2024 com ticker trocado (ENBR3 = EDP, não Enel), ações que não existem (VIVT4) e Oi/Claro; se não for refeito, 301 -> 4873."),
    1108: ("corrigir", "Tirar 'LCI/LCA 15% a 22,5%' e a tabela de corretagem por banco."),
    1128: ("301 -> 5093", "Tabela dividendos x JCP invertida; o 5093 (proventos) cobre o tema (depois de corrigido para 17,5%)."),
    1133: ("corrigir", "Tirar 'Tesouro Direto isento de imposto'."),
    1143: ("corrigir", "Refazer a tabela de IR (Tesouro/CDB 22,5% a 15%)."),
    1163: ("corrigir", "Trocar 50 por 100 cotistas."),
    1168: ("301 -> 5059", "Ganho de capital 15% x 20% no mesmo post; o 5059 (O que é FII) cobre o tema (depois de corrigido)."),
    1173: ("corrigir", "Tirar o requisito inventado de 90 dias."),
    1178: ("despublicar", "Lista de FIIs majoritariamente inexistentes; não há o que aproveitar."),
    1183: ("301 -> 4874", "FII inexistente (JHSF11); tema coberto pelo guia de FIIs 4874."),
    1188: ("301 -> 5059", "Tributação e limite de 25% errados; mesmo tema de 'O que é FII'."),
    1193: ("301 -> 1213", "Post duplicado (mesmo título); manter o 1213 corrigido."),
    1213: ("corrigir", "Ganho de capital de FII é 20%."),
    1208: ("corrigir", "Tirar URET11 (encerrado) e datar volumes."),
    4848: ("corrigir", "Tag along invertido e tabela de preços que não bate com a B3."),
    4536: ("corrigir", "Controle do Itaú (IUPAR) e volumes; receber o 301 do 4845 (mesmo assunto)."),
    3435: ("corrigir", "Prazo do IRPF 2026 e 100 cotistas."),
    4816: ("reescrever", "Regra de dividendos de BDR, DARF e JEPQ39 errados; é guia de IR, precisa estar certo."),
    5092: ("corrigir", "Tabela de IR: JCP 17,5%, dividendos 2026, 100 cotistas, prazo de LCI/LCA."),
    5058: ("corrigir", "JCP 17,5% e exemplos."),
    5093: ("corrigir", "JCP 17,5%, 100 cotistas, regra de dividendos de 2026."),
    5059: ("corrigir", "100 cotistas."),
    4874: ("corrigir", "100 cotistas, JCP 17,5%, IFIX11 inexistente, FOFs encerrados."),
    4873: ("corrigir", "100 cotistas, JCP 17,5%, TRPL4 -> ISAE4."),
    4875: ("corrigir", "Lei errada e prazos de carência."),
    4815: ("corrigir", "100 cotistas e BCFF11."),
    5067: ("corrigir", "100 cotistas."),
    5042: ("corrigir", "Prazo mínimo de LCI."),
    4565: ("corrigir", "Prazo mínimo de LCI."),
    4566: ("corrigir", "Prazo mínimo de LCA."),
    4537: ("corrigir", "Tirar JEPQ39; receber 301 de 1063 e 1083."),
    4544: ("corrigir", "Tirar JEPQ39, BNDW39 e DVDY11; conferir público-alvo do JEPI39."),
    4568: ("corrigir", "Tirar JEPQ39."),
    4572: ("corrigir", "Tirar JEPQ39 da tabela."),
    4573: ("corrigir", "Tirar JEPQ39, TRPL4 e MALL11."),
    3172: ("corrigir", "Tabela JEPI39 x JEPQ39 trata o JEPQ39 como existente; linkar o 4538."),
    5113: ("corrigir", "Tirar ALBT34, LVHD34, XRES11 e TVRI11 como ETF de REIT."),
    5114: ("corrigir", "BKCH39."),
    5119: ("corrigir", "Ticker do ETF de Nasdaq."),
    10097: ("corrigir", "CSED3."),
    12158: ("corrigir", "AIRB34."),
    1078: ("301 -> 5064", "Mesmo tema genérico ('melhor ETF do momento'), com MALL11 como ETF."),
    2086: ("corrigir", "AZZA3."),
    4812: ("corrigir", "Taxas do BOVA11 e IVVB11."),
    11638: ("corrigir", "Revisão quadrimestral do Ibovespa."),
    7376: ("corrigir", "JCP 17,5% e regra de dividendos de 2026."),
    10424: ("corrigir", "JCP 17,5%."),
    5051: ("corrigir", "JCP 17,5% e regra de dividendos de 2026."),
}

# ---------------- o que foi conferido manualmente ----------------
# 'integral' = texto lido inteiro e afirmações checadas; 'dirigida' = lidas as linhas com números, tickers e regras de IR.
INTEGRAL = [1033, 983, 993, 998, 1003, 1028, 1053, 4848, 4845, 4536, 19466, 1073, 4538]
DIRIGIDA = [1008, 1013, 1038, 1043, 1023, 1048, 1058, 1063, 1068, 1078, 1083, 1088, 1098, 1103, 1108, 1113, 1118, 1123, 1128, 1133,
            1138, 1143, 1148, 1153, 1158, 1163, 1168, 1173, 1178, 1183, 1188, 1193, 1198, 1203, 1208, 1213,
            1773, 1782, 1790, 1815, 1823, 2023, 1455, 1488, 2408, 2443, 2487, 2795, 2917, 2819,
            11719, 4391, 8993, 7380, 18946, 3172, 4537, 4544, 4568, 4572, 4573, 4816, 5054, 5053, 5052, 3435, 5092, 5058,
            4875, 5093, 5059, 4874, 7378, 5091, 11638, 5097, 4812, 5057, 5113, 5114, 5119, 10097, 12158, 4815, 4873, 2086, 1313]
NOTAS_CONFERIDOS = {
    993: "Reescrito em set/2026 com dados do RI; participações e controle conferem com o RI. Sem achado.",
    1028: "Reescrito em set/2026; volumes médios (R$ 286,3 mi x R$ 1,6 mi) e preços de 25/09/2026 conferidos no COTAHIST. Sem achado.",
    1053: "Reescrito em set/2026; coerente com o RI e com a Lei 15.270. Sem achado.",
    19466: "Preços do TRXF11 (R$ 91,10 em 31/07, R$ 71,8 em 21/08, R$ 71,79 em 30/09) e VP de ~R$ 96,6 conferidos no COTAHIST e no informe mensal da CVM. Sem achado.",
    4391: "Lucro do 1T26 (R$ 3,885 bi, +2,1%) conferido no ITR da CVM; alta de 15,3% em 05/05/2026 no COTAHIST (o post diz 'mais de 10%'). Selic 14,5% certa na data. Sem achado.",
    11719: "Selic 14,25% certa na data; eliminação do Brasil pela Noruega nas oitavas (05/07/2026) confirmada. Só a frase de dividendos isentos sem ressalva.",
    7380: "Lucro do 1T26 citado é o ajustado do release (o contábil da CVM é R$ 2,40 bi atribuível); coerente com os releases. Sem achado.",
    18946: "Números do 2T26 do BB batem com o lucro ajustado do release; Selic 14% certa na data. Sem achado.",
    1773: "Prejuízo de US$ 694 mi no 4T24, dividendos e recompra coerentes com o release da Vale. Sem achado.",
    1823: "Números do 4T24 da WEG coerentes com o release. Sem achado.",
    8993: "Recomendações de bancos citadas com fonte (Safra, UBS BB). Sem achado de fato; tem CTA de carteira de ações para comprar.",
    5054: "Só Selic 14,75% fixa no texto (já desatualizada na publicação; meta era 14,5%).",
    5053: "Idem; IPCA de 5,5% também não bate (IPCA 12m de abr/2026 = 4,39%, SGS 13522).",
    5052: "Idem 5053.",
    1313: "Reescrito; SHLD39 (desde 27/05/2026) e EMBJ3 (desde 03/11/2025) conferidos no COTAHIST. Sem achado.",
    5057: "METB3/METB4 são exemplo fictício declarado. Sem achado.",
}

BCB_13522 = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.13522/dados?formato=json"
LISTA_RF_EXTRA = {"IMAB11", "B5P211", "FIXA11", "IRFM11"}
# pares de mesmo assunto conferidos na leitura (além dos detectados pelo título)
DUPLICADOS_MANUAIS = [(4536, 4845), (1003, 1008), (1008, 1038), (1068, 1078), (1078, 1098), (12527, 18934), (5727, 12527)]
