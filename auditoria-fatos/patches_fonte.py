"""Fonte dos patches de texto (lotes A, B e C). gerar_patches.py valida e grava patches/<post_id>.json.

Cada post: motivo, fonte, trocas [(de, para)] e, se preciso, 'manual' (o que só dá para fazer no editor, como
célula de tabela repetida ou trecho com aspas/travessão que não é seguro casar).
Regra de texto: só corrigir o que está errado, sem mudar a voz; taxa variável sem número ou com data e fonte.
"""
from referencia import REGRAS_IR

L15270 = REGRAS_IR["dividendos_2026"]["fonte"]
LC224 = REGRAS_IR["jcp"]["fonte"]
L14754 = "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14754.htm"
CMN5215 = "https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20CMN&numero=5215"
L11033 = "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l11033.htm"
SGS432 = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json"
SGS13522 = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.13522/dados?formato=json"
B3 = "https://www.b3.com.br/pt_br/market-data-e-indices/servicos-de-dados/market-data/historico/mercado-a-vista/series-historicas/"
RFB_IRPF26 = ("https://www.gov.br/receitafederal/pt-br/assuntos/noticias/2026/marco/"
              "receita-comeca-a-receber-declaracoes-do-irpf-no-dia-23-de-marco-prazo-de-entrega-se-encerra-em-29-de-maio")
RFB_DIRPF = "https://www.gov.br/receitafederal/pt-br/centrais-de-conteudo/publicacoes/perguntas-frequentes/declaracoes/dirpf"

# frases-padrão (sem número de taxa variável)
SELIC_SITE = "a meta Selic vigente está no site do Banco Central"
DIV_2026 = ("desde janeiro de 2026, dividendos acima de R$ 50 mil por mês pagos pela mesma empresa "
            "à mesma pessoa têm 10% de IR retido na fonte (Lei 15.270/2025)")

PATCHES = {}
LOTES = {"A": [], "B": [], "C": []}
DESCRICAO = {
    "A": "Regras de IR de 2026: JCP 17,5% (LC 224/2025), FII com 100 cotistas (Lei 14.754/2023), dividendos acima de "
         "R$ 50 mil/mês (Lei 15.270/2025), prazo mínimo de LCI/LCA (Res. CMN 5.215/2025). Os posts deste lote levam "
         "também as correções de taxa fixa (Selic/CDI/IPCA) e de ticker que tinham, para não haver dois patches no mesmo post.",
    "B": "Post 4537 (destino de 301 do 1083): sem o JEPQ39 e com os demais erros corrigidos.",
    "C": "Posts publicados em 07/05/2026 que não estão no lote A: Selic/CDI/IPCA fixos no texto trocados por frase sem "
         "número ou por valor com data e fonte; demais erros pontuais encontrados na leitura.",
}


def post(pid, lote, motivo, fonte, trocas, manual=None):
    assert pid not in PATCHES, pid
    PATCHES[pid] = {"motivo": motivo, "fonte": fonte, "trocas": trocas, "manual": manual or []}
    LOTES[lote].append(pid)


# =====================================================================================================  LOTE A
post(4873, "A", "JCP a 15% (é 17,5% desde 2026), FII com 50 cotistas (são 100), dividendos 'isentos até maio de 2026' "
     "sem a Lei 15.270/2025, Selic fixa.",
     f"{LC224} ; {L14754} ; {L15270} ; {SGS432}",
     [
         ("15% de IR na fonte", "17,5% de IR na fonte (desde 2026)"),
         ("O valor líquido que cai na sua conta já vem com o desconto de 15%.",
          "O valor líquido que cai na sua conta já vem com o desconto de 17,5% (alíquota do JCP desde 2026)."),
         ("50 cotistas)", "99 cotistas, isto é, 100 ou mais)"),
         ("Isento (dividendos), 15% (JCP)", "Isento (dividendos até R$ 50 mil/mês por empresa), 17,5% (JCP)"),
         ("onde a empresa desconta 15% na fonte antes de creditar na sua conta",
          "onde a empresa desconta 17,5% na fonte antes de creditar na sua conta"),
         ("Fique atento: há debates legislativos recorrentes sobre tributação de dividendos, mas até maio de 2026 a isenção se mantém.",
          "Fique atento: " + DIV_2026 + "; abaixo disso, seguem isentos."),
         ("Com a Selic em 14,75%, a renda fixa de curto prazo concorre diretamente com os dividendos.",
          "Com a Selic alta (" + SELIC_SITE + "), a renda fixa de curto prazo concorre diretamente com os dividendos."),
     ],
     manual=["Linha TRPL4 do gráfico e da tabela de DY: a TRPL4 não negocia desde 14/11/2024 (virou ISAE4). "
             "Trocar por ISAE4 com DY recalculado ou tirar a linha (célula curta e repetida, não dá para casar com segurança).",
             "Célula 'Isento de IR' da linha Dividendo na tabela Dividendo x JCP: acrescentar 'até R$ 50 mil/mês por empresa'."])

post(4874, "A", "FII com 50 cotistas (são 100), JCP a 15% (17,5%), ETF 'IFIX11' que não existe, FOFs encerrados, Selic fixa.",
     f"{L14754} ; {LC224} ; {B3} (IFIX11 sem negócios; XFIX11 = TREND IFIX-L; BCFF11 último pregão 18/10/2024; RBRF11 02/10/2025) ; {SGS432}",
     [
         ("mais de 50 cotistas", "100 cotistas ou mais"),
         ("mas juros sobre capital próprio são tributados em 15%", "mas juros sobre capital próprio são tributados em 17,5% (desde 2026)"),
         ("Exemplos: BCFF11, RBRF11.", "Confira na B3 se o FoF ainda está listado antes de investir: BCFF11 e RBRF11, que eram exemplos comuns, deixaram de ser negociados."),
         ("Com a Selic em 13,75% ao ano, isso significa que",
          "Num exemplo com CDI de 13,75% ao ano (" + SELIC_SITE + "), isso significa que"),
         ("considere um ETF de FIIs como o IFIX11", "considere um ETF que replica o IFIX, como o XFIX11"),
         ("ETF de FIIs (IFIX11) ou selecionar FIIs individualmente?", "ETF de FIIs (como o XFIX11) ou selecionar FIIs individualmente?"),
         ("o IFIX11 é uma resposta honesta", "um ETF que replica o IFIX (como o XFIX11) é uma resposta honesta"),
     ])

post(5092, "A", "Tabela de IR com JCP a 15%, FII com 50 cotistas, LCI/LCA com carência de 90 dias e dividendos como 'debate'.",
     f"{LC224} ; {L14754} ; {CMN5215} ; {L15270}",
     [
         ("15% (retido na fonte)", "17,5% (retido na fonte, desde 2026)"),
         ("Geralmente exigem carência mínima de 90 a 360 dias.",
          "Prazo mínimo de 6 meses (Res. CMN 5.215/2025; 12 meses na LCA e 36 meses na LCI corrigidas pelo IPCA)."),
         ("desde que o FII tenha mais de 50 cotistas e as cotas sejam negociadas em bolsa",
          "desde que o FII tenha 100 cotistas ou mais, as cotas sejam negociadas em bolsa e você tenha menos de 10% das cotas"),
         ("isentos para pessoa física (debate tributário em andamento no Congresso).",
          "isentos para pessoa física até R$ 50 mil por mês por empresa; acima disso, 10% de IR na fonte desde 2026 (Lei 15.270/2025)."),
     ],
     manual=["Célula 'Isentos' da linha Dividendos de ações na tabela do topo: acrescentar 'até R$ 50 mil/mês por empresa'."])

post(5058, "A", "Post sobre JCP com a alíquota antiga (15%); desde 01/01/2026 é 17,5%. Exemplos recalculados; Selic fixa.",
     f"{LC224} ; {L15270} ; {SGS432}",
     [
         ("o JCP sofre retenção de 15% de imposto de renda na fonte", "o JCP sofre retenção de 17,5% de imposto de renda na fonte (desde 2026)"),
         ("a corretora retém 15% de IR na fonte e o valor líquido cai na sua conta automaticamente",
          "a corretora retém 17,5% de IR na fonte e o valor líquido cai na sua conta automaticamente"),
         ("Um ponto de atenção: como a Selic está em 14,75% ao ano e o CDI em 14,65%, a TJLP",
          "Um ponto de atenção: como a Selic e o CDI estão muito acima da TJLP (" + SELIC_SITE + "), a TJLP"),
         ("Porém, como o IR de 15% é retido na fonte, você recebe R$ 425,00 líquidos.",
          "Porém, como o IR de 17,5% é retido na fonte, você recebe R$ 412,50 líquidos."),
         ("A diferença de R$ 75,00 parece clara a favor dos dividendos.", "A diferença de R$ 87,50 parece clara a favor dos dividendos."),
         ("Com a Selic a 14,75%, um JCP com yield bruto de 6% ao ano equivale a 5,1% líquido após IR. Um CDB que paga 100% do CDI (14,65%) rende 12,45% líquido.",
          "Num exemplo com CDI de 14,65% ao ano, um JCP com yield bruto de 6% ao ano equivale a 4,95% líquido após o IR de 17,5%. Um CDB que paga 100% desse CDI rende 12,45% líquido."),
         ("há retenção de 15% de IR na fonte", "há retenção de 17,5% de IR na fonte (desde 2026)"),
         ("15% retido na fonte", "17,5% retido na fonte"),
         ("O dividendo é isento de IR para a pessoa física e não dedutível para a empresa.",
          "O dividendo é isento de IR para a pessoa física até R$ 50 mil por mês por empresa (acima disso, 10% na fonte desde 2026) e não é dedutível para a empresa."),
     ],
     manual=["Frase 'Em 2025, a TJLP está em torno de 7% ao ano': conferir a TJLP vigente no BNDES/BCB e datar."])

post(5059, "A", "FII com 50 cotistas (são 100 desde a Lei 14.754/2023); Selic, CDI e IPCA fixos no texto.",
     f"{L14754} ; {SGS432} ; {SGS13522}",
     [
         ("desde que o fundo tenha pelo menos 50 cotistas e suas cotas sejam negociadas exclusivamente na bolsa",
          "desde que o fundo tenha pelo menos 100 cotistas, suas cotas sejam negociadas exclusivamente na bolsa e você tenha menos de 10% das cotas"),
         ("Um CDB que paga 100% do CDI (hoje em torno de 14,65% ao ano)",
          "Um CDB que paga 100% do CDI (que anda colado na Selic; " + SELIC_SITE + ")"),
         ("Num cenário com Selic a 14,75% e IPCA a 5,5%, os FIIs de papel", "Num cenário de Selic e IPCA altos, os FIIs de papel"),
         ("se o Tesouro Selic paga 14,75% com zero risco", "se o Tesouro Selic paga a Selic com risco mínimo"),
         ("Um FII com dividend yield de 11% numa época de CDI a 14,65% está pagando menos do que a renda fixa",
          "Um FII com dividend yield de 11% numa época de CDI acima disso está pagando menos do que a renda fixa"),
         ("num CDB a 100% do CDI (14,65% ao ano) por 12 meses", "num CDB a 100% do CDI (num exemplo com CDI de 14,65% ao ano) por 12 meses"),
         ("Em cenário de juros altos (Selic a 14,75%), FIIs de papel", "Em cenário de juros altos, FIIs de papel"),
     ])

S1475 = "14,75% (meta de março e abril de 2026, segundo o Copom; " + SELIC_SITE + ")"
C1465 = "14,65% (CDI de abril de 2026)"
IPCA_ABR26 = "4,39% (IPCA em 12 meses até abril de 2026, segundo o IBGE)"
LCI_PRAZO = ("6 meses para LCI e LCA sem correção pela inflação (Res. CMN 5.215/2025); com IPCA, 12 meses na LCA "
             "e 36 meses na LCI")

post(5093, "A", "JCP a 15% (17,5% desde 2026), FII com 50 cotistas (100), dividendos sem a regra da Lei 15.270/2025, Selic fixa.",
     f"{LC224} ; {L14754} ; {L15270} ; {SGS432}",
     [
         ("Dividendos são isentos de Imposto de Renda para a pessoa física no Brasil (mas atenção: isso pode mudar com reformas tributárias em discussão).",
          "Dividendos são isentos de Imposto de Renda para a pessoa física no Brasil até R$ 50 mil por mês da mesma empresa; acima disso, há 10% retido na fonte desde janeiro de 2026 (Lei 15.270/2025)."),
         ("Para o investidor, o JCP tem 15% de IR retido na fonte. Na prática: se uma empresa distribui R$1,00 de JCP, você recebe R$0,85 líquido.",
          "Para o investidor, o JCP tem 17,5% de IR retido na fonte (desde 2026). Na prática: se uma empresa distribui R$1,00 de JCP, você recebe R$0,825 líquido."),
         ("é considerado razoável no ambiente atual de Selic em 14,75%.", "é considerado razoável num ambiente de Selic acima de 14%, como o de abril de 2026."),
         ("isentos de IR para pessoa física (Brasil é um dos poucos países com essa isenção)",
          "isentos de IR para pessoa física até R$ 50 mil por mês por empresa (acima disso, 10% na fonte desde 2026)"),
         ("isentos de IR se o FII tem mais de 50 cotistas e a cota é negociada em bolsa",
          "isentos de IR se o FII tem 100 cotistas ou mais, a cota é negociada em bolsa e você tem menos de 10% das cotas"),
         ("Dividendos são isentos de IR para pessoa física; JCP tem 15% retido na fonte.",
          "Dividendos são isentos de IR para pessoa física até R$ 50 mil por mês por empresa; JCP tem 17,5% retido na fonte."),
         ("JCP tem 15% retido na fonte antes de chegar à sua conta.", "JCP tem 17,5% retido na fonte antes de chegar à sua conta."),
         ("mesmo que o acionista pague 15%.", "mesmo que o acionista pague 17,5%."),
     ],
     manual=["Lista de tributação: item 'JCP:' seguido de '15% de IR retido na fonte' (nó curto); trocar por 17,5%."])

post(5051, "A", "JCP a 15% (17,5% desde 2026), dividendos sem a regra de 2026, Selic/CDI/IPCA fixos como se fossem de maio de 2026.",
     f"{LC224} ; {L15270} ; {SGS432} ; {SGS13522}",
     [
         ("Em maio de 2026, a Selic está em 14,75% ao ano, o CDI em torno de 14,65% e o IPCA acumulado em 5,5%.",
          "Em abril de 2026, a Selic estava em 14,75% ao ano, o CDI em torno de 14,65% e o IPCA em 12 meses em 4,39% (Copom e IBGE; confira os valores atuais no site do Banco Central)."),
         ("ainda mais quando se considera que os dividendos são isentos de Imposto de Renda para pessoas físicas no Brasil",
          "ainda mais quando se considera que os dividendos são isentos de Imposto de Renda para pessoas físicas no Brasil até R$ 50 mil por mês por empresa"),
         ("A desvantagem para o investidor pessoa física é que o JCP sofre retenção de 15% de IR na fonte, ao contrário dos dividendos, que são isentos.",
          "A desvantagem para o investidor pessoa física é que o JCP sofre retenção de 17,5% de IR na fonte (desde 2026), ao contrário dos dividendos, que são isentos até R$ 50 mil por mês por empresa."),
         ("Dividendos recebidos por pessoas físicas no Brasil são isentos de IR; JCP tem retenção de 15% na fonte.",
          "Dividendos recebidos por pessoas físicas no Brasil são isentos de IR até R$ 50 mil por mês por empresa (acima disso, 10% na fonte desde 2026); JCP tem retenção de 17,5% na fonte."),
         ("Com Selic em 14,75%, um DY precisa ser consistente", "Com a Selic acima de 14%, um DY precisa ser consistente"),
     ])

post(4815, "A", "FII com 50 cotistas (são 100 desde a Lei 14.754/2023) e BCFF11, que deixou de negociar em 2024.",
     f"{L14754} ; {B3} (BCFF11: último pregão 18/10/2024; HFOF11 negocia)",
     [
         ("em FIIs com mais de 50 cotistas negociados em bolsa.", "em FIIs com 100 cotistas ou mais, negociados em bolsa, para quem tem menos de 10% das cotas."),
         ("FIIs de fundos de fundos (FOFs) como BCFF11 ou HFOF11", "FIIs de fundos de fundos (FOFs) como o HFOF11"),
     ])

post(5067, "A", "FII com 50 cotistas (100 desde a Lei 14.754/2023); Selic, CDI e IPCA fixos no texto.",
     f"{L14754} ; {SGS432} ; {SGS13522}",
     [
         ("que está em torno de 5,5% ao ano atualmente", "que estava em " + IPCA_ABR26),
         ("Um CRI indexado ao CDI, hoje em 14,65% ao ano, rende bem mais do que em períodos de juros baixos.",
          "Um CRI indexado ao CDI rende bem mais com juros altos do que em períodos de juros baixos."),
         ("como o atual patamar de 14,75%", "como o de 2025 e 2026 (" + SELIC_SITE + ")"),
         ("desde que o fundo tenha mais de 50 cotistas e seja negociado em bolsa",
          "desde que o fundo tenha 100 cotistas ou mais, seja negociado em bolsa e o cotista tenha menos de 10% das cotas"),
         ("Em um cenário de Selic a 14,75%, os FIIs de papel", "Em um cenário de Selic acima de 14%, os FIIs de papel"),
     ])

post(4875, "A", "Lei errada para a isenção (8.668 é a lei dos FIIs) e prazos mínimos de LCI/LCA desatualizados (6 meses desde a "
     "Res. CMN 5.215/2025); CDI fixo.",
     f"{L11033} (art. 3º, II e IV) ; {CMN5215} ; https://api.bcb.gov.br/dados/serie/bcdata.sgs.12/dados?formato=json",
     [
         ("A isenção está prevista na Lei 8.668/1993 (LCI) e na Lei 11.076/2004 (LCA).",
          "A isenção para pessoa física está no art. 3º da Lei 11.033/2004; a LCI foi criada pela Lei 10.931/2004 e a LCA pela Lei 11.076/2004."),
         ("90 dias (prefixada) / 12 meses (pós-fixada)", "6 meses (sem correção pela inflação) / 36 meses (IPCA+)"),
         ("CDI 14,65% a.a.", "CDI de exemplo 14,65% a.a."),
         ("LCA com carência de 90 dias é mais flexível que a LCI com carência de 12 meses. Se você precisar de liquidez antes de 12 meses, olhe primeiro a LCA ou a LCI com vencimento curto.",
          "Desde a Res. CMN 5.215/2025, LCI e LCA sem correção pela inflação têm o mesmo prazo mínimo, de 6 meses (com IPCA, 12 meses na LCA e 36 meses na LCI). Se você precisar de liquidez antes disso, LCI e LCA não servem."),
         ("Com CDI a 14,65% ao ano, uma LCI de 90% do CDI", "Num exemplo com CDI de 14,65% ao ano, uma LCI de 90% do CDI"),
         ("(indexada ao CDI): carência mínima de 12 meses", "(indexada ao CDI): prazo mínimo de 6 meses"),
         ("Com CDI em 14,65%: LCI 80% = 11,72% ao ano.", "Num exemplo com CDI de 14,65%: LCI 80% = 11,72% ao ano."),
         ("LCA com carência de 90 dias acima de 93% do CDI é ótima para dinheiro que você sabe que não vai precisar por pelo menos 3 meses.",
          "LCA de 6 meses (o prazo mínimo desde a Res. CMN 5.215/2025) acima de 93% do CDI é ótima para dinheiro que você sabe que não vai precisar por pelo menos 6 meses."),
     ],
     manual=["Tabela LCI x LCA, célula de carência da LCA ('90 dias'): trocar por '6 meses (12 meses se IPCA+)'.",
             "Lista de carências: 'LCI prefixada ou IPCA+: carência mínima de 90 dias' e 'LCA (qualquer indexador): carência mínima de 90 dias' "
             "viram 'LCI prefixada: 6 meses; LCI IPCA+: 36 meses' e 'LCA sem índice de preços: 6 meses; LCA IPCA+: 12 meses' "
             "(as duas frases são iguais no HTML, não dá para trocar uma só com segurança)."])

post(5042, "A", "Prazo mínimo de LCI desatualizado (6 meses desde a Res. CMN 5.215/2025); Selic, CDI e IPCA fixos no texto.",
     f"{CMN5215} ; {SGS432} ; {SGS13522}",
     [
         ("e hoje está em torno de 14,65% ao ano", "e anda colado na Selic (" + SELIC_SITE + ")"),
         ("você vai receber aproximadamente 14,65% ao ano sobre o valor aplicado",
          "você vai receber aproximadamente o CDI do período sobre o valor aplicado, antes do IR"),
         ("rende a inflação medida pelo IPCA, hoje em torno de 5,5% ao ano, mais uma taxa fixa.",
          "rende a inflação medida pelo IPCA (que estava em " + IPCA_ABR26 + "), mais uma taxa fixa."),
         ("Com o CDI em 14,65% ao ano, 110% do CDI", "Num exemplo com CDI de 14,65% ao ano, 110% do CDI"),
         ("carência mínima de 90 dias (e muitas vezes 1 ano)", "prazo mínimo de 6 meses (Res. CMN 5.215/2025; 36 meses se for corrigida pelo IPCA)"),
         ("A maioria dos CDBs rende um percentual do CDI (hoje ~14,65% a.a.)", "A maioria dos CDBs rende um percentual do CDI (que acompanha a Selic)"),
         ("Com a Selic em 14,75%, a poupança rende 0,5% ao mês", "Com a Selic acima de 8,5% ao ano, a poupança rende 0,5% ao mês mais TR"),
         ("Um CDB a 100% do CDI rende aproximadamente 14,65% ao ano bruto", "Num exemplo com CDI de 14,65% ao ano, um CDB a 100% do CDI rende aproximadamente 14,65% ao ano bruto"),
     ],
     manual=["Frase 'bem próximo da Selic, que está em 14,75% ao ano' (logo depois do CDI, mesmo parágrafo com travessão): trocar por 'bem próximo da Selic'."])

post(4565, "A", "Prazo mínimo da LCI desatualizado: 90 dias valia antes de 2024; desde a Res. CMN 5.215/2025 são 6 meses (36 se IPCA+).",
     CMN5215,
     [
         ("A LCI tem prazo mínimo de", "A LCI tinha prazo mínimo de"),
         ("(resolução CMN 4.095). Antes disso, não é possível resgatar.",
          "(regra antiga). Desde a Res. CMN 5.215/2025, o prazo mínimo é de 6 meses para LCI sem correção pela inflação e 36 meses para LCI corrigida pelo IPCA. Antes disso, não é possível resgatar."),
     ])

post(4566, "A", "Prazo mínimo da LCA desatualizado: desde a Res. CMN 5.215/2025 são 6 meses (12 se IPCA+).",
     CMN5215,
     [
         ("A LCA tem prazo mínimo de", "A LCA tinha prazo mínimo de"),
         (", assim como a LCI. Antes disso, o resgate não é permitido.",
          ", assim como a LCI (regra antiga). Desde a Res. CMN 5.215/2025, o prazo mínimo é de 6 meses para LCA sem correção pela inflação e 12 meses para LCA corrigida pelo IPCA. Antes disso, o resgate não é permitido."),
     ])

post(4816, "A", "Guia de IR de BDR: dividendo de BDR tratado como isento (é tributável, carnê-leão), JEPQ39 e BOVA39 que não existem.",
     f"{RFB_DIRPF} ; {B3} (JEPQ39 e BOVA39 sem negócios 2021-2026; JEPI39 desde 23/02/2026)",
     [
         ("O Brasil não cobra IR novamente sobre essa parcela para pessoas físicas.",
          "No Brasil, o dividendo de BDR é rendimento tributável: entra no carnê-leão (tabela progressiva) e o imposto pago lá fora pode ser compensado, nos limites da lei."),
         ("dentro de ETFs como JEPI39 e JEPQ39 é tributada", "dentro de ETFs como o JEPI39 (o JEPQ não tem BDR na B3) é tributada"),
         ("você comprou 200 BDRs de BOVA39 por R$50 cada", "você comprou 200 BDRs de um ETF americano por R$50 cada"),
         ("Você não precisa lançar o imposto pago no exterior separadamente, pois o Brasil não cobra novamente sobre essa parcela. Declare apenas o valor líquido recebido como rendimento isento.",
          "Declare o dividendo como rendimento tributável recebido do exterior (carnê-leão) e informe o imposto pago lá fora, que pode ser compensado até o limite do imposto devido no Brasil."),
     ],
     manual=["Bloco 'Onde declarar' dos dividendos: trocar 'Rendimentos Isentos e Não Tributáveis → Código 26 (Outros). Informe o valor líquido' "
             "por 'Rendimentos Tributáveis Recebidos de Pessoa Física/do Exterior (carnê-leão), com o imposto pago no exterior'.",
             "Código DARF '8523' (é de ganho de capital em moeda estrangeira): trocar por 6015 (renda variável em bolsa, pessoa física)."])

post(3435, "A", "Guia IRPF 2026: prazo de entrega errado (foi até 29/05), FII com 50 cotistas (100) e falta de aviso sobre JCP e "
     "dividendos a partir de 2026.",
     f"{RFB_IRPF26} ; {L14754} ; {LC224} ; {L15270}",
     [
         ("O prazo para entrega da declaração vai até o final de abril de 2026.", "O prazo para entrega da declaração foi de 23 de março a 29 de maio de 2026."),
         ("para a pessoa física, por força da lei. No entanto, devem ser declarados obrigatoriamente na ficha",
          "para a pessoa física, por força da lei (regra do ano-base 2025; desde 2026, há 10% retido na fonte acima de R$ 50 mil por mês da mesma empresa). No entanto, devem ser declarados obrigatoriamente na ficha"),
         ("é diferente do dividendo. Ele sofre retenção de 15% na fonte, e deve ser declarado na ficha",
          "é diferente do dividendo. Ele sofreu retenção de 15% na fonte em 2025 (desde 2026 são 17,5%, pela LC 224/2025), e deve ser declarado na ficha"),
         (", desde que o fundo tenha mais de 50 cotistas, as cotas sejam negociadas em bolsa",
          ", desde que o fundo tenha 100 cotistas ou mais, as cotas sejam negociadas em bolsa"),
         ("JCP tem tributação exclusiva de 15% e vai em ficha diferente.", "JCP tem tributação exclusiva (15% em 2025; 17,5% desde 2026) e vai em ficha diferente."),
     ])

post(1163, "A", "FII com 50 cotistas: desde a Lei 14.754/2023 a isenção exige 100 cotistas ou mais.", L14754,
     [("O fundo tenha pelo menos 50 cotistas.", "O fundo tenha pelo menos 100 cotistas (Lei 14.754/2023).")])

post(7376, "A", "JCP a 15% (17,5% desde 2026), dividendos sem a regra de 2026 e Selic fixa na tabela.",
     f"{LC224} ; {L15270} ; {SGS432}",
     [
         ("Importante: dividendos de ações têm isenção de IR para pessoa física no Brasil. O JCP tem retenção de 15%",
          "Importante: dividendos de ações têm isenção de IR para pessoa física no Brasil até R$ 50 mil por mês por empresa. O JCP tem retenção de 17,5% (desde 2026)"),
         ("Dividendos de ações são isentos de IR para pessoa física no Brasil. Já o JCP (Juros sobre Capital Próprio), que a Telefônica usa bastante, tem retenção de 15% na fonte.",
          "Dividendos de ações são isentos de IR para pessoa física no Brasil até R$ 50 mil por mês por empresa (acima disso, 10% na fonte desde 2026). Já o JCP (Juros sobre Capital Próprio), que a Telefônica usa bastante, tem retenção de 17,5% na fonte."),
         ("~13,75% ao ano", "Selic do período"),
         ("~15,1% ao ano", "110% do CDI do período"),
     ])

post(10424, "A", "JCP a 15% (17,5% desde 2026) e lei citada pelo número do projeto (é a Lei 15.270/2025).",
     f"{LC224} ; {L15270}",
     [
         ("que o PL 1087/2025 (sancionado e em vigor desde 01/01/2026) manteve",
          "que a Lei 15.270/2025 (o antigo PL 1087/2025, em vigor desde 01/01/2026) manteve"),
         ("com alíquota de 15% de IR retida direto no pagamento", "com alíquota de 17,5% de IR retida direto no pagamento (desde 2026)"),
         ("15% retido na fonte", "17,5% retido na fonte"),
         ("Valor líquido = bruto menos 15%", "Valor líquido = bruto menos 17,5%"),
         ("JCP é uma despesa dedutível para a empresa, tributada em 15% na fonte para o acionista.",
          "JCP é uma despesa dedutível para a empresa, tributada em 17,5% na fonte para o acionista."),
         ("desde a vigência do PL 1087/2025.", "desde a vigência da Lei 15.270/2025."),
     ])

post(1038, "A", "JCP a 15% e dividendos 'sem imposto nenhum': desde 2026, JCP 17,5% e 10% na fonte acima de R$ 50 mil/mês.",
     f"{LC224} ; {L15270}",
     [
         ("para quem é pessoa física. Isso quer dizer que você não paga nada sobre esses valores. Por outro lado, os",
          "para quem é pessoa física até R$ 50 mil por mês (acima disso, 10% retido na fonte desde 2026, pela Lei 15.270/2025). Por outro lado, os"),
         ("são tributados a 15% na fonte.", "são tributados a 17,5% na fonte (desde 2026; eram 15% até 2025)."),
     ])

post(1148, "A", "Tabela com JCP a 15% e dividendos isentos sem ressalva: regras de 2026.", f"{LC224} ; {L15270}",
     [
         ("Tributados na fonte em 15%", "Tributados na fonte em 17,5% (desde 2026)"),
         ("Isentos de Imposto de Renda", "Isentos de IR até R$ 50 mil/mês por empresa (desde 2026)"),
     ])

post(2819, "A", "Texto ainda trata a taxação de dividendos como projeto: virou a Lei 15.270/2025, sancionada em 26/11/2025 e em vigor desde jan/2026.",
     L15270,
     [
         ("A medida, que agora segue para o Senado, exige", "A medida foi aprovada no Senado e sancionada como Lei 15.270/2025 em 26/11/2025. Ela exige"),
         (", caso a lei seja sancionada em 2025.", ", já que a lei foi sancionada em novembro de 2025 (Lei 15.270/2025)."),
     ])

post(11719, "A", "Dividendos 'isentos pela legislação em vigor' sem a regra de 2026; Selic citada sem data.", f"{L15270} ; {SGS432}",
     [
         ("com a Selic hoje em 14,25% ao ano", "com a Selic em 14,25% ao ano (meta de julho de 2026, segundo o Copom)"),
         ("Dividendos de ações pagos a pessoa física são isentos de IR pela legislação em vigor.",
          "Dividendos de ações pagos a pessoa física são isentos de IR até R$ 50 mil por mês por empresa; acima disso, há 10% retido na fonte desde 2026 (Lei 15.270/2025)."),
     ])

post(5077, "A", "Dividendos isentos sem a regra de 2026; Selic, CDI e IPCA fixos no texto.", f"{L15270} ; {SGS432} ; {SGS13522}",
     [
         ("porque os dividendos são isentos de Imposto de Renda para pessoa física.",
          "porque os dividendos são isentos de Imposto de Renda para pessoa física até R$ 50 mil por mês por empresa (acima disso, 10% na fonte desde 2026)."),
         ("Com a Selic em 14,75% ao ano e o CDI em 14,65%, o investidor brasileiro",
          "Com a Selic em " + S1475 + " e o CDI perto disso, o investidor brasileiro"),
         ("acima do IPCA de 5,5% e próximo do CDI de 14,65%", "acima do IPCA e próximo do CDI de 14,65% (valores de exemplo)"),
     ])

post(4814, "A", "Dividendos isentos sem a regra de 2026; Selic fixa no texto.", f"{L15270} ; {SGS432}",
     [
         ("Com Selic a 14,75%, a renda anual bruta", "Com Selic a " + S1475 + ", a renda anual bruta"),
         ("Vantagem: dividendos de ações são isentos de IR.", "Vantagem: dividendos de ações são isentos de IR até R$ 50 mil por mês por empresa."),
         ("gera ~R$5.000/mês bruto hoje (Selic 14,75%)", "gera ~R$5.000/mês bruto com a Selic de abril de 2026 (14,75%)"),
     ])

post(7530, "A", "Dividendos isentos sem a regra de 2026, limite de isenção do IRPF antigo (desde 2026 é R$ 5 mil) e TRPL (virou ISAE4).",
     f"{L15270} ; {B3} (TRPL4 último pregão 14/11/2024; ISAE4 desde 18/11/2024)",
     [
         ("Dividendos no Brasil são isentos de IR para pessoa física.", "Dividendos no Brasil são isentos de IR para pessoa física até R$ 50 mil por mês por empresa."),
         ("utilities (SAPR, TRPL)", "utilities (SAPR, ISAE)"),
         ("Descontado o imposto de renda (para quem recebe acima de R$",
          "Descontado o imposto de renda (em 2026, isento até R$ 5 mil por mês e com redução parcial até R$ 7.350, pela Lei 15.270/2025; antes, o limite era R$"),
     ],
     manual=["Conferir o valor líquido do teto do INSS ('entre R$ 7.600 e R$ 7.900') com a tabela do IRPF de 2026."])
