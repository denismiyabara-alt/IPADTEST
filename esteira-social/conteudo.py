"""Texto dos cards da esteira social, um card 🎬 por vídeo do calendário v2, no contrato do juiz-post.

Contrato (esteira-social/agentes/juiz-post.md e leitor-frio.md, vindos do Mac):
- Um card = carrossel do Instagram (capa + slides) + legenda + 3 a 5 posts do X (A, B, C...). Card de vídeo do
  canal (🎬): a capa do carrossel e a imagem do post A são a THUMBNAIL do YouTube; o texto da capa conta a mesma
  coisa que a thumbnail.
- Eliminatórios que o texto pode evitar: afirmação absoluta ("só", "nunca", "todo", "ninguém", "sempre"...),
  CTA, link, "Você sabia", palavra proibida, número sem fonte ou que muda entre slide/legenda/posts, capa com
  dois fatos colados ou piada que precisa de contexto.
- Leitor-frio (depois do juiz): leitor leigo, sem jargão. Capa com 1 ideia, no máximo 1 número e nenhuma
  palavra técnica; nos outros slides, até 3 números, frase de até 25 palavras e jargão sempre explicado ali
  mesmo, entre parênteses. Por isso os posts e slides dizem "ETF (fundo vendido na bolsa)", "FGC (garantia
  contra quebra do banco)" etc. a cada vez que a sigla aparece.

Regras que continuam: números só da linha do calendário ou declarados em `numeros` (trecho literal ou conta),
ranking/superlativo só com trecho literal (AFIRMACOES), nada de ativo recomendado nem corretora, sem fonte e sem
disclaimer no corpo do post, [CHECAR: ...] para o número do dia (o Denis preenche na publicação).

Chave: "AAAA-MM-DD|formato" (o calendário v3 tem longo e Short no mesmo dia). `titulo` tem de bater com o calendário (o gerador confere).
"""

CAL = "CALENDARIO-8-SEMANAS.csv"
PERG = "PERGUNTAS-SEM-RESPOSTA.md"
TEMAS = "TEMAS.md"
TERMOS = "TERMOS.md"


def arq(valor, arquivo, trecho):
    """Número tirado de um arquivo de pautas-canal/: o trecho tem de existir lá, literal."""
    return {"valor": valor, "fonte": arquivo, "trecho": trecho}


def conta(valor, expressao, entradas):
    """Número calculado: `expressao` (Python, só aritmética) tem de dar `valor` dentro do arredondamento."""
    return {"valor": valor, "fonte": "cálculo", "conta": expressao, "entradas": entradas}


N_JUNTAR = [
    arq("1.000", CAL, "Como juntar 1 milhão de reais com R$ 1.000 por mês"),
    arq("6", CAL, "Com 6% ao ano acima da inflação, ~R$ 535 mil em 22 anos e 1 milhão em ~30"),
    arq("535", CAL, "Com 6% ao ano acima da inflação, ~R$ 535 mil em 22 anos e 1 milhão em ~30"),
    arq("22", CAL, "Com 6% ao ano acima da inflação, ~R$ 535 mil em 22 anos e 1 milhão em ~30"),
]
N_TAXA_ETF = [
    arq("0,5", CAL, "0,5% contra 1,5% ao ano em 10 anos"),
    arq("1,5", CAL, "0,5% contra 1,5% ao ano em 10 anos"),
    conta("5", "(1 - 0.995 ** 10) * 100", "0,5% ao ano por 10 anos, sem rendimento (CALENDARIO 25/11)"),
    conta("14", "(1 - 0.985 ** 10) * 100", "1,5% ao ano por 10 anos, sem rendimento (CALENDARIO 25/11)"),
]

C = {}

# ------------------------------------------------------------------ vídeos que vêm do v2 (mesmo título)
C["2026-10-05|short"] = dict(
    titulo="LCI e LCA ou CDB: qual rende mais depois do imposto?",
    estrutura="B", mecanica="tradutor-juramentado",
    mensagem_capa="Uma aplicação que paga taxa menor pode deixar mais dinheiro no bolso, por causa do imposto.",
    capa="A taxa menor pode render mais.",
    slides=[
        "LCI e LCA (aplicações de banco) não pagam imposto de renda pra pessoa física.",
        "O CDB paga imposto de renda. E a mordida diminui quanto mais tempo o dinheiro fica.",
        "Compare o que sobra depois do imposto, não a taxa do anúncio.",
    ],
    legenda="Tanaka, o banco anuncia o CDB com a taxa maior em letra grande.\n\n"
            "O que ele não escreve: o CDB paga imposto de renda, e a LCI e a LCA (aplicações de banco) não pagam, "
            "pra pessoa física.\n\n"
            "Por isso a taxa menor pode deixar mais dinheiro no seu bolso. A conta certa compara o que sobra, "
            "não o que brilha no anúncio.",
    posts=[
        "Tanaka, o anúncio diz: \"CDB que paga mais\".\n\nTradução: paga mais antes do imposto de renda.\n\n"
        "Depois dele, a história pode virar.",
        "LCI e LCA (aplicações de banco) não pagam imposto de renda pra pessoa física.\n\nO CDB paga.\n\n"
        "Por isso a taxa menor da LCI pode deixar mais dinheiro no bolso que a taxa maior do CDB.",
        "A conta que resolve: quanto o CDB precisa pagar, depois do imposto, pra empatar com a LCI (aplicação de "
        "banco sem imposto de renda).\n\nAbaixo disso, a taxa maior perde. E o banco não grifa essa parte.",
    ],
    numeros=[],
    risco=("médio", "Pauta de produto bancário: pode ler como finança pessoal básica. Carrossel mais explica que reage."),
)

C["2026-10-06|longo"] = dict(
    titulo="Fundo imobiliário ou imóvel alugado: a conta de 2026",
    estrutura="E", mecanica="eco-do-gatilho (escondido)",
    mensagem_capa="Imóvel e fundo imobiliário escondem custos diferentes; a comparação justa olha cinco coisas.",
    capa="Imóvel ou fundo imobiliário: a conta tem cinco partes.",
    slides=[
        "Rendimento, custo, imóvel vazio, imposto e facilidade de vender.",
        "No apartamento, o mês sem inquilino sai do seu bolso: condomínio e IPTU.",
        "No fundo, o imóvel vazio também existe, diluído entre vários imóveis.",
        "A cota oscila na tela a cada dia. O preço do apartamento oscila escondido.",
    ],
    legenda="Tanaka, imóvel ou fundo imobiliário? A pergunta comum é qual rende mais. Falta metade.\n\n"
            "A conta inteira tem cinco partes: rendimento, custo, imóvel vazio, imposto e facilidade de vender. O "
            "imóvel esconde o custo do mês vazio. O fundo mostra a oscilação a cada dia. O vídeo lê as duas letras "
            "miúdas, sem indicar fundo.",
    posts=[
        "Tanaka, imóvel ou fundo imobiliário?\n\nA pergunta comum é \"qual rende mais\".\n\nFalta metade da pergunta.",
        "A pergunta inteira tem cinco partes:\n\n→ rendimento\n→ custo\n→ imóvel vazio\n→ imposto\n"
        "→ facilidade de vender\n\nQuem compara a primeira escolhe pela foto do anúncio.",
        "Custo e imóvel vazio são o lado escondido do apartamento.\n\n"
        "Mês sem inquilino, você paga condomínio e IPTU do próprio bolso.\n\n"
        "No fundo, o imóvel vazio também existe, diluído entre vários imóveis.",
        "O apartamento não cai na tela.\n\nIsso não quer dizer que ele não caiu.\n\nQuer dizer que a tela não te mostrou.",
    ],
    numeros=[],
    risco=("médio", "Repete o dilema do Short de 11/11; o carrossel explica mais que reage."),
)

C["2026-10-08|longo"] = dict(
    titulo="Tesouro IPCA+ a 7% em janeiro: quanto ganhou quem comprou",
    estrutura="E", mecanica="atendimento-ao-cliente",
    mensagem_capa="O vídeo mostra quanto ganhou até agora quem comprou o título do Tesouro em janeiro.",
    capa="Quem comprou em janeiro ganhou ou perdeu?",
    slides=[
        "Em janeiro, o Tesouro IPCA+ (título que paga a inflação mais uma taxa) pagava 7% acima da inflação.",
        "O vídeo compara o preço do título na compra com o preço de agora.",
        "E soma os juros que o título já pagou no caminho.",
        "Vermelho no app não é prejuízo pra quem leva até o vencimento. O preço muda a cada dia; a taxa contratada, não.",
    ],
    legenda="Tanaka, em janeiro o Tesouro IPCA+ (título que paga a inflação mais uma taxa) pagava 7% acima da "
            "inflação. O vídeo sobre isso está no top 10 do ano do canal.\n\n"
            "Agora é a prestação de contas: preço na compra, preço hoje e os juros que caíram no caminho.\n\n"
            "A taxa fica travada. O preço passeia.",
    posts=[
        "Tanaka, quem comprou em janeiro ganhou quanto?\n\nO Tesouro pagava 7% acima da inflação, e quem comprou "
        "ouviu \"travou a taxa\".\n\nAgora vem a prestação de contas.",
        "O vídeo de janeiro está no top 10 do ano do canal.\n\nPrometer é fácil. Prestar conta dá trabalho.\n\n"
        "Então o vídeo foi atrás do extrato: preço na compra, preço hoje e os juros pagos no caminho.",
        "— Meu título caiu. Perdi dinheiro?\n— Se vender hoje, perde.\n— E se eu esperar o vencimento?\n"
        "— Aí vale a taxa que você travou. A tela mostra o humor do mercado.",
        "A taxa, você travou em janeiro.\n\nO preço não tem trava.\n\nQuem confunde os dois vende no pior dia.",
    ],
    numeros=[],
    risco=("baixo", "Continuação de top 10, bolso claro. Risco: o print oficial do Tesouro precisa ser do dia."),
)

C["2026-10-12|short"] = dict(
    titulo="Resgatou o CDB antes de 30 dias? O IOF come o rendimento",
    estrutura="A", mecanica="manual-invertido",
    mensagem_capa="Sacar o CDB antes de 30 dias faz um imposto comer parte do rendimento.",
    capa="Sacou o CDB antes de 30 dias?",
    slides=[
        "Antes de 30 dias, o saque paga IOF (um imposto sobre quem resgata cedo).",
        "Quanto mais cedo o saque, maior a mordida. Ela diminui a cada dia.",
        "No dia 30, o IOF (imposto do saque cedo) zera. Fica o imposto de renda.",
    ],
    legenda="Tanaka, o CDB rendeu. Você sacou na segunda semana. E o rendimento chegou mordido.\n\n"
            "Antes de 30 dias, o resgate paga IOF (imposto sobre o saque cedo). A mordida é maior nos primeiros dias "
            "e diminui até sumir no dia 30. Depois disso, fica o imposto de renda.\n\n"
            "Dinheiro que pode sair a qualquer hora pede aplicação pensada pra isso.",
    posts=[
        "Tanaka, o CDB rendeu.\n\nVocê sacou na segunda semana.\n\nE o rendimento chegou mordido.",
        "Manual pra perder rendimento:\n\n→ aplique no CDB\n→ precise do dinheiro antes de 30 dias\n→ resgate\n\n"
        "O IOF (imposto sobre saque cedo) faz o resto.",
        "A mordida do IOF (imposto sobre saque cedo) é maior no começo e diminui a cada dia.\n\n"
        "No dia 30, ela some.\n\nDinheiro que você mexe a cada mês pede outra aplicação.",
    ],
    numeros=[],
    risco=("médio", "Pauta de produto bancário básico; capa clara e com bolso."),
)

C["2026-10-13|longo"] = dict(
    titulo="Dividendos mensais com ações: como montar um calendário",
    estrutura="B", mecanica="eco-do-gatilho (cair)",
    mensagem_capa="Receber dividendo mensal depende de montar um calendário de pagamentos, não de achar uma ação mágica.",
    capa="Dividendo mensal é calendário, não mágica.",
    slides=[
        "Cada empresa costuma pagar dividendos em meses diferentes do ano.",
        "A data com (o último dia pra ter a ação e entrar na lista) decide se você recebe.",
        "A data de pagamento decide quando o dinheiro cai. Entre uma e outra, podem passar semanas.",
        "O valor muda: dividendo sai do lucro. E o JCP (provento parecido com dividendo) chega com 17,5% de imposto descontado.",
    ],
    legenda="Tanaka, dividendo mensal não cai por mágica. Cai por calendário.\n\n"
            "Cada empresa paga em meses diferentes. A data com (o último dia pra ter a ação) decide se você recebe; "
            "a data de pagamento decide quando. E o valor muda, porque dividendo sai do lucro.\n\n"
            "Aqui não tem lista de compra. Tem o mapa.",
    posts=[
        "Tanaka, dividendo mensal não cai por mágica.\n\nCai por calendário.\n\nE pouca gente sabe ler esse calendário.",
        "Duas datas mandam no jogo:\n\n→ data com (o último dia pra ter a ação e ter direito)\n"
        "→ data de pagamento (quando o dinheiro cai)\n\nEntre uma e outra podem passar semanas.",
        "O valor muda de um pagamento pro outro.\n\nDividendo sai do lucro. Lucro caiu, dividendo cai junto.\n\n"
        "E o JCP (provento parecido com dividendo) já cai na conta com 17,5% de imposto descontado.",
        "Renda mensal com ação é escala de churrasco da família.\n\nCada mês, um primo paga a carne.\n\n"
        "O problema é quando o primo de março cai fora.",
    ],
    numeros=[],
    risco=("médio", "Pauta boa (renda mensal); o carrossel explica mais que reage, o que limita a voz a 1."),
)

C["2026-10-14|short"] = dict(
    titulo="Tesouro IPCA+ negativo? Calma, isso tem nome",
    estrutura="A", mecanica="tradutor-juramentado",
    mensagem_capa="Ver o título do Tesouro no vermelho no app não quer dizer prejuízo.",
    capa="Seu Tesouro ficou no vermelho? Calma.",
    slides=[
        "O título do Tesouro tem preço a cada dia. Isso é a marcação a mercado (o preço se você vendesse hoje).",
        "Juros do país sobem, o preço do título cai. Juros caem, o preço sobe.",
        "Quem leva até o vencimento recebe a taxa contratada. O vermelho é o preço de hoje.",
    ],
    legenda="Tanaka, o Tesouro ficou negativo no app? Respira.\n\n"
            "Isso é a marcação a mercado (o preço que o título teria se você vendesse hoje). Quando os juros sobem, "
            "o preço cai. Quem leva até o vencimento recebe a taxa contratada. Quem vende no susto transforma o "
            "vermelho em prejuízo.",
    posts=[
        "Tanaka, seu Tesouro ficou negativo no app?\n\nRespira.\n\nIsso tem nome, e não é prejuízo.",
        "O app diz: \"rentabilidade negativa\".\n\nTradução: se você vendesse hoje, venderia mais barato do que "
        "comprou.\n\nSe não vender, essa linha é o humor do mercado no dia.",
        "Juros do país sobem, o preço do título cai. Juros caem, o preço sobe.\n\n"
        "Quem leva até o vencimento recebe a taxa que travou.\n\nQuem vende no susto transforma humor em prejuízo.",
    ],
    numeros=[],
    corte_de="2026-10-08",
    risco=("baixo", "Dor no bolso clara (vermelho no app). Risco: jargão do título na thumbnail não conta como trava."),
)

C["2026-10-15|longo"] = dict(
    titulo="Crise financeira: o gráfico de 1929, 2008 e 2020, hoje",
    estrutura="B", mecanica="boletim-escolar",
    mensagem_capa="Um gráfico que acertou três crises passa por revisão: o que mostra hoje e quantas vezes errou.",
    capa="O gráfico que acertou três crises está certo hoje?",
    slides=[
        "Ele marcou as crises de 1929, 2008 e 2020.",
        "O vídeo sobre ele foi o 3º melhor do canal no ano. Agora ele presta contas.",
        "O vídeo mostra o que o gráfico marca hoje e quantas vezes ele gritou crise e nada veio.",
        "Boletim do gráfico: acertou três. Errou outras. O vídeo mostra quais.",
    ],
    legenda="Tanaka, um gráfico acertou as crises de 1929, 2008 e 2020 e virou profeta.\n\n"
            "O vídeo faz a revisão: o que ele marcava antes de cada crise, o que marca hoje e os alarmes falsos no "
            "caminho. Mais os sinais do vídeo de novembro, conferidos um a um com o dado de agora.\n\n"
            "Data de crash, o vídeo não chuta.",
    posts=[
        "Tanaka, um gráfico acertou três crises grandes.\n\nVirou profeta.\n\nAgora ele vai ter que se explicar.",
        "As três: 1929, 2008 e 2020.\n\nAcerta uma vez, vira profeta. Erra três, vira esquecido.\n\n"
        "Igual vidente de fim de ano na TV.",
        "O vídeo sobre esse gráfico foi o 3º melhor do canal no ano.\n\nPor isso ele merece revisão:\n\n"
        "→ o que marcava antes de cada crise\n→ o que marca hoje\n→ quantas vezes gritou crise e nada veio",
        "Boletim do gráfico:\n\nAs três crises: acertou.\nAlarmes falsos: o vídeo conta.\n"
        "Observação da professora: bom aluno, mas grita demais na sala.",
    ],
    numeros=[],
    risco=("médio", "Pauta de crise sem ponte clara com o bolso; 'e daí?' é o risco do item 1."),
)

C["2026-10-19|short"] = dict(
    titulo="FII é isento de imposto? Só se cumprir estas 3 regras",
    estrutura="E", mecanica="pergunta-do-leitor",
    mensagem_capa="O rendimento do fundo imobiliário fica sem imposto de renda se três regras forem cumpridas.",
    capa="Fundo imobiliário sem imposto? Depende de 3 regras.",
    slides=[
        "Primeira regra: o fundo tem 100 cotistas (donos de cotas) ou mais.",
        "Segunda: as cotas são negociadas na bolsa. Terceira: você tem menos de 10% das cotas do fundo.",
        "Vendeu a cota com lucro? Aí paga 20% sobre o ganho. O rendimento pode ficar sem imposto; a venda com lucro, não.",
    ],
    legenda="Tanaka, rendimento de fundo imobiliário pode não pagar imposto de renda. Mas tem 3 regras principais, "
            "e uma delas depende de você.\n\n"
            "O fundo precisa ter 100 cotistas (donos de cotas) ou mais e cotas negociadas na bolsa. E você precisa "
            "ter menos de 10% das cotas.\n\n"
            "Vender a cota com lucro é outra conversa: paga 20% sobre o ganho.",
    posts=[
        "Tanaka, fundo imobiliário pode render sem imposto.\n\nDepende de 3 regras.\n\nE uma delas depende de você.",
        "As 3 regras principais:\n\n→ o fundo tem 100 cotistas (donos de cotas) ou mais\n"
        "→ as cotas são negociadas na bolsa\n→ você tem menos de 10% das cotas\n\nFalhou uma? O rendimento paga imposto.",
        "\"Mas fundo imobiliário não era livre de imposto?\"\n\nO rendimento pode ser, com as regras.\n\n"
        "A venda da cota com lucro, não: paga 20% sobre o ganho.",
    ],
    numeros=[],
    risco=("médio", "Regra de imposto: o juiz pede a regra INTEIRA; o texto fala em 'regras principais' "
                    "(Lei 14.754/2023 tem outros detalhes que o calendário não traz)."),
)

C["2026-10-22|longo"] = dict(
    titulo="LCI e LCA ou CDB: a conta de 2026 com imposto e prazo",
    estrutura="C", mecanica="eco-do-gatilho (preso)",
    mensagem_capa="Antes de deixar R$ 80 mil presos por um ano, a conta tem imposto, prazo e garantia.",
    capa="R$ 80 mil presos por um ano? Faça a conta.",
    slides=[
        "LCI e LCA (aplicações de banco) não pagam imposto de renda pra pessoa física. O CDB paga.",
        "Por isso a taxa menor da LCI (aplicação de banco sem imposto de renda) pode deixar mais no bolso que a "
        "taxa maior do CDB.",
        "Carência (tempo em que o dinheiro fica preso) e liquidez (poder sacar antes) contam tanto quanto a taxa.",
        "Confira o limite do FGC (garantia que devolve o dinheiro se o banco quebrar). Taxa em letra grande, prazo "
        "preso em letra miúda.",
    ],
    legenda="Tanaka, R$ 80 mil numa LCI por 12 meses? A pergunta é essa, seca. A resposta é uma conta.\n\n"
            "LCI e LCA (aplicações de banco) não pagam imposto de renda pra pessoa física; o CDB paga. Mas imposto é "
            "um item de quatro: tem também a carência (tempo em que o dinheiro fica preso), a liquidez (poder sacar "
            "antes) e a garantia do FGC (contra quebra do banco).\n\n"
            "Taxa em letra grande. Prazo preso em letra miúda.",
    posts=[
        "Tanaka, R$ 80 mil presos por um ano?\n\nA pergunta é essa, seca.\n\nA resposta não é sim nem não. É uma conta.",
        "LCI e LCA (aplicações de banco) não pagam imposto de renda pra pessoa física.\n\n"
        "O CDB paga, e a mordida diminui com o prazo.\n\nPor isso a taxa menor da LCI pode deixar mais dinheiro no bolso.",
        "Mas imposto é um item de quatro:\n\n→ quanto rende depois do imposto\n"
        "→ carência (quanto tempo o dinheiro fica preso)\n→ liquidez (se dá pra sair antes)\n"
        "→ FGC (garantia se o banco quebrar)",
        "O banco anuncia a taxa em letra grande.\n\nO prazo em que o dinheiro fica preso vem em letra miúda.\n\n"
        "E é ele que decide quando você consegue sacar.",
    ],
    numeros=[],
    risco=("médio", "Pauta de produto bancário; pergunta real com R$ dá bolso. Carrossel explicativo."),
)

C["2026-10-26|short"] = dict(
    titulo="FGC: o que cobre e o que não cobre",
    estrutura="A", mecanica="atendimento-ao-cliente",
    mensagem_capa="A garantia contra quebra de banco tem limite e deixa Tesouro, fundos e ações de fora.",
    capa="A garantia do seu banco tem limite.",
    slides=[
        "O FGC (garantia que devolve o dinheiro se o banco quebrar) cobre até R$ 250 mil por CPF por instituição.",
        "Teto: R$ 1 milhão a cada 4 anos, somando as instituições.",
        "Fica de fora: Tesouro Direto, fundos e ações.",
    ],
    legenda="Tanaka, o FGC (a garantia que devolve seu dinheiro se o banco quebrar) tem limite.\n\n"
            "Cobre até R$ 250 mil por CPF por instituição, com teto de R$ 1 milhão a cada 4 anos. Vale pra CDB, LCI "
            "e LCA (aplicações de banco), entre outros.\n\n"
            "Tesouro Direto, fundos e ações ficam de fora. No Tesouro, quem responde é o Tesouro Nacional.",
    posts=[
        "Tanaka, a garantia do seu banco tem limite.\n\nO FGC (fundo que devolve o dinheiro se o banco quebrar) "
        "cobre aplicações de banco, até um teto.\n\nO que fica de fora costuma ser o que você acha que está dentro.",
        "Cobre: até R$ 250 mil por CPF por instituição.\n\nTeto: R$ 1 milhão a cada 4 anos, somando as "
        "instituições.\n\nVale pra CDB, LCI e LCA (aplicações de banco), entre outros.",
        "— E o meu Tesouro, a garantia do banco cobre?\n— Não. Quem garante é o Tesouro Nacional.\n"
        "— E o fundo? E a ação?\n— Aí não tem garantia. O risco é seu, com nome e CPF.",
    ],
    numeros=[],
    risco=("médio", "Pauta de produto bancário básico; regra completa no calendário (limite e teto)."),
)

C["2026-10-28|short"] = dict(
    titulo="Quanto rende R$ 1.000 no Tesouro Selic hoje",
    estrutura="D", mecanica="conta-rapida",
    mensagem_capa="O vídeo mostra quanto sobra de R$ 1.000 no Tesouro em um ano, depois do imposto.",
    capa="Quanto sobra de R$ 1.000 no Tesouro?",
    slides=[
        "Tesouro Selic (título que acompanha os juros básicos do país): rende a taxa do dia, antes do imposto.",
        "Depois, sai o imposto de renda, que diminui quanto mais tempo o dinheiro fica.",
        "Em um ano, R$ 1.000 viram [CHECAR: valor líquido com a taxa do Tesouro Selic do dia da gravação].",
    ],
    legenda="Tanaka, R$ 1.000 no Tesouro Selic (o título que acompanha os juros básicos). Quanto rende de verdade?\n\n"
            "A conta é rendimento bruto menos o imposto de renda do prazo, e mais um imposto se sair antes de 30 "
            "dias. Com a taxa do dia da gravação, o líquido em um ano fica em [CHECAR: valor líquido em um ano].\n\n"
            "Não é pra enriquecer. É pra dormir.",
    posts=[
        "Tanaka, R$ 1.000 no Tesouro rende quanto?\n\nNo Tesouro Selic (o título que segue os juros do país), a "
        "resposta não é a taxa do anúncio.\n\nÉ o que cai na conta.",
        "Conta rápida pra R$ 1.000 em um ano:\n\n→ bruto: a taxa do dia\n→ menos o imposto de renda do prazo\n"
        "→ líquido: [CHECAR: valor com a taxa do Tesouro Selic do dia da gravação]",
        "Sacou antes de 30 dias? Ainda tem mais um imposto na fila.\n\n"
        "Tesouro Selic (título que segue os juros do país) não é pra ficar rico.\n\nÉ pra dormir.",
    ],
    numeros=[],
    risco=("baixo", "Conta em R$ e bolso claro. Pendência: o [CHECAR] da taxa do dia (decisão do Mac: não elimina)."),
)

C["2026-10-29|longo"] = dict(
    titulo="Tesouro IPCA+ acima de 7%: o que é travar a taxa",
    estrutura="E", mecanica="eco-do-gatilho (travar)",
    mensagem_capa="Travar a taxa do Tesouro garante o combinado no fim, mas o preço no caminho continua mudando.",
    capa="Travou a taxa. E o preço?",
    slides=[
        "No Tesouro IPCA+ (título que paga a inflação mais uma taxa), a taxa de 7% ou mais fica travada até o vencimento.",
        "No vencimento, você recebe a inflação do período mais a taxa travada.",
        "No meio do caminho, o preço muda a cada dia. Se os juros sobem, o preço cai.",
        "Vendeu antes: recebe o preço do dia. Levou até o fim: recebe o combinado.",
    ],
    legenda="Tanaka, travar o Tesouro IPCA+ (título que paga a inflação mais uma taxa) acima de 7% parece simples: "
            "compra e a taxa fica.\n\n"
            "No vencimento, você recebe a inflação mais a taxa travada. No caminho, o preço muda a cada dia e pode "
            "cair se os juros subirem. Vender antes é aceitar o preço do dia.\n\n"
            "Travar a taxa é fácil. Difícil é travar a paciência.",
    posts=[
        "Tanaka, travar 7% no Tesouro parece simples.\n\nVocê compra, a taxa fica.\n\n"
        "Mas \"travar\" tem letra miúda, e ela aparece no meio do caminho.",
        "Começa pelo fim: no vencimento, você recebe a inflação do período mais a taxa que travou.\n\n"
        "Isso não muda, nem se o mercado surtar.\n\nO problema é o meio.",
        "No meio, o título tem preço a cada dia.\n\nSe os juros sobem depois da sua compra, o preço cai.\n\n"
        "Travou a taxa, não travou o preço.",
        "Quem trava a taxa e não trava a paciência destrava no pior dia.\n\n"
        "A decisão real não é a taxa. É o prazo que você consegue esperar.",
    ],
    numeros=[],
    risco=("médio", "Pauta forte (busca de 'tesouro ipca'), mas o conceito é técnico pro leitor leigo."),
)

C["2026-11-02|short"] = dict(
    titulo="JCP em 2026: já vem com 17,5% de imposto",
    estrutura="C", mecanica="contraste",
    mensagem_capa="Esse provento pago pela empresa chega na conta com 17,5% de imposto descontado.",
    capa="Esse provento chega mordido: 17,5%.",
    slides=[
        "O JCP (provento parecido com dividendo) vem com 17,5% de imposto retido na fonte.",
        "O valor que a empresa anuncia é bruto. O que cai na sua conta vem descontado.",
        "Dividendo, até R$ 50 mil por mês da mesma empresa, segue sem desconto na fonte.",
    ],
    legenda="Tanaka, o JCP (provento parecido com dividendo) de 2026 chega mordido: 17,5% de imposto retido na fonte.\n\n"
            "O valor que a empresa anuncia é bruto. O que cai na conta vem descontado. Dividendo segue sem desconto "
            "na fonte até R$ 50 mil por mês da mesma empresa.\n\n"
            "Parecem irmãos. Um deles paga pedágio na saída.",
    posts=[
        "Tanaka, esse provento chega mordido em 2026.\n\nÉ o JCP (pago pela empresa, parecido com dividendo).\n\n"
        "E a mordida é em você, não na empresa.",
        "O que a empresa anuncia: o JCP (provento parecido com dividendo) bruto.\n\n"
        "O que cai na sua conta: o JCP menos 17,5% de imposto.\n\nA mordida acontece antes de você ver o extrato.",
        "Dividendo, até R$ 50 mil por mês da mesma empresa, segue sem desconto na fonte.\n\n"
        "O JCP (provento parecido com dividendo) tem desconto de 17,5%.\n\nParecem irmãos. Um deles paga pedágio na saída.",
    ],
    numeros=[arq("50", CAL, "Retenção de 10% só acima de R$ 50 mil por mês da mesma empresa (Lei 15.270/2025).")],
    risco=("baixo", "Dor no bolso direta e regra do calendário. Risco: JCP é jargão, explicado em cada peça."),
)

C["2026-11-04|short"] = dict(
    titulo="Copom hoje: 3 números para olhar no seu Tesouro",
    estrutura="C", mecanica="previsao-do-tempo",
    mensagem_capa="Antes da decisão dos juros de hoje, anote três números do seu Tesouro pra comparar amanhã.",
    capa="Hoje decidem os juros. Anote 3 números.",
    slides=[
        "Taxa do Tesouro IPCA+ (título que paga a inflação mais uma taxa) antes da decisão.",
        "Taxa do Tesouro prefixado (taxa travada na compra) antes da decisão.",
        "A Selic (os juros básicos do país) que o mercado espera.",
    ],
    legenda="Tanaka, hoje tem Copom (a reunião do Banco Central que decide os juros). A decisão sai no fim do dia.\n\n"
            "Antes dela, anote a taxa do Tesouro IPCA+, a do prefixado e a Selic (juros básicos) que o mercado "
            "espera. Se a decisão surpreender, as taxas e os preços dos títulos se mexem.\n\n"
            "Amanhã sai o vídeo com o que mudou.",
    posts=[
        "Tanaka, hoje decidem os juros do país.\n\nÉ o Copom (a reunião do Banco Central). A decisão sai no fim do "
        "dia.\n\nAntes dela, 3 números do seu Tesouro merecem uma olhada.",
        "Previsão do tempo pro seu Tesouro:\n\n→ taxa do IPCA+ (inflação mais uma taxa) hoje\n"
        "→ taxa do prefixado (taxa travada) hoje\n→ a Selic (juros básicos) que o mercado espera\n\n"
        "Anota antes. Amanhã você compara.",
        "Se a decisão vier diferente do esperado, as taxas mexem e o preço dos títulos mexe junto.\n\n"
        "Quem anotou entende o que aconteceu.\n\nQuem não anotou descobre pelo app, no susto.",
    ],
    numeros=[],
    evento_ao_vivo="Postar ANTES do anúncio do Copom (04/11, fim do dia). Depois do anúncio, o texto envelhece.",
    risco=("baixo", "Evento com data e bolso. Risco: três ideias técnicas pro leitor leigo nos slides."),
)

C["2026-11-05|longo"] = dict(
    titulo="Dividendos mensais de R$ 1.000: quanto precisa investir",
    estrutura="D", mecanica="conta-rapida",
    mensagem_capa="Pra receber R$ 1.000 por mês, o dinheiro investido depende de quanto cada investimento rende depois do imposto.",
    capa="Quanto investir pra receber R$ 1.000 por mês?",
    slides=[
        "R$ 1.000 por mês são R$ 12 mil por ano.",
        "Capital necessário: R$ 12 mil dividido pelo rendimento anual, já sem imposto.",
        "O vídeo faz a conta em três caminhos: Tesouro, fundos imobiliários e ações.",
        "Rendimento maior encolhe a conta. E deixa a renda mais instável.",
    ],
    legenda="Tanaka, R$ 1.000 por mês de dividendo. Pouca gente fez a conta de quanto precisa investir pra isso.\n\n"
            "A conta começa com R$ 12 mil por ano divididos pelo rendimento anual, já sem imposto. O vídeo faz isso "
            "em três caminhos (Tesouro, fundos imobiliários e ações), com o imposto de cada um. Sem indicar ativo.\n\n"
            "Rendimento alto encolhe a conta e aumenta o balanço da renda.",
    posts=[
        "Tanaka, R$ 1.000 por mês de dividendo.\n\nMuita gente quer.\n\n"
        "Pouca gente fez a conta de quanto precisa investir pra isso.",
        "A conta começa simples:\n\nR$ 1.000 por mês = R$ 12 mil por ano.\n\n"
        "Agora divide pelo rendimento anual, já sem imposto. Esse divisor muda a conta inteira.",
        "O vídeo faz a conta em três caminhos:\n\n→ Tesouro\n→ fundos imobiliários\n→ ações que pagam dividendos\n\n"
        "Cada um com o imposto dele, porque renda bruta não paga boleto.",
        "Pegadinha da conta: rendimento maior, capital menor.\n\nE renda mais instável.\n\n"
        "Quem escolhe pelo divisor esquece da balança.",
    ],
    numeros=[conta("12", "1000 * 12 / 1000", "R$ 1.000 por mês x 12 meses, em mil (título do vídeo)")],
    risco=("baixo", "Promessa em R$ que cabe no bolso do Tanaka; conta simples."),
)

C["2026-11-17|longo"] = dict(
    titulo="Fundos imobiliários para iniciantes: de onde vem a renda",
    estrutura="A", mecanica="tradutor-juramentado",
    mensagem_capa="Fundo imobiliário é aluguel e juros de imóveis divididos entre muita gente.",
    capa="Fundo imobiliário não é mágica. É aluguel.",
    slides=[
        "O fundo tem imóveis ou títulos de dívida de imóveis. Recebe aluguel ou juros e repassa a maior parte a quem tem cota.",
        "Fundo de tijolo: renda de aluguel. Risco: imóvel vazio.",
        "Fundo de papel: renda de juros de dívida de imóveis. Risco: quem deve não pagar.",
        "O rendimento pode sair sem imposto de renda, se o fundo cumprir as regras. A venda da cota com lucro paga imposto.",
    ],
    legenda="Tanaka, o folheto diz \"renda passiva\". Tradução: o fundo imobiliário tem imóveis ou dívidas de "
            "imóveis, recebe aluguel ou juros e repassa a maior parte a quem tem cota.\n\n"
            "Tijolo depende de inquilino. Papel depende de quem deve pagar. Sem indicar fundo.\n\n"
            "Você vira dono de um pedaço do shopping, sem a chave.",
    posts=[
        "Tanaka, fundo imobiliário não é mágica.\n\nÉ aluguel.\n\nDividido com muita gente que você não vai conhecer.",
        "O folheto diz: \"renda passiva\".\n\nTradução: o fundo tem imóveis ou dívidas de imóveis, recebe aluguel "
        "ou juros e repassa a maior parte a quem tem cota.\n\nPassiva pra você. O gestor trabalha.",
        "Dois tipos de renda, dois riscos:\n\n→ tijolo: aluguel de galpão, shopping, escritório. Risco: imóvel vazio.\n"
        "→ papel: juros de dívida de imóveis. Risco: quem deve não pagar.",
        "Fundo imobiliário é ser dono de um pedaço de shopping sem ter a chave.\n\nVocê não escolhe o inquilino.\n\n"
        "Mas sente quando ele vai embora.",
    ],
    numeros=[],
    risco=("médio", "Pauta de iniciante: 'abstrato' é o risco do item 1; a analogia do shopping segura a voz."),
)

C["2026-11-09|short"] = dict(
    titulo="Imposto sobre dividendos acima de R$ 50 mil por mês: quem paga",
    estrutura="A", mecanica="mito-x-fato",
    mensagem_capa="O imposto novo sobre dividendos vale pra quem recebe mais de R$ 50 mil por mês de uma mesma empresa.",
    capa="Dividendo paga imposto? Acima de R$ 50 mil por mês.",
    slides=[
        "Acima de R$ 50 mil por mês, pagos pela mesma empresa à mesma pessoa: 10% de imposto na fonte.",
        "Abaixo disso, segue sem desconto na fonte.",
        "A conta é por empresa, não pela soma da carteira.",
    ],
    legenda="Tanaka, dividendo agora paga imposto? Acima de R$ 50 mil por mês pagos pela mesma empresa à mesma "
            "pessoa, sim: 10% retidos na fonte.\n\n"
            "A conta é por empresa, não pela soma da carteira.\n\n"
            "A regra nova tem endereço. Confira se é o seu antes de entrar em pânico no grupo da família.",
    posts=[
        "Tanaka, dividendo agora paga imposto?\n\nAcima de R$ 50 mil por mês da mesma empresa, sim.\n\n"
        "Abaixo disso, sem desconto na fonte.",
        "Acima disso, 10% retidos na fonte.\n\nA regra nova tem endereço.\n\n"
        "E ela bate na porta de quem recebe mais de R$ 50 mil num mês de uma empresa.",
        "Mito: agora dividendo paga imposto pra quem recebe de várias empresas.\n\n"
        "Fato: a conta é por empresa. Várias pagando menos de R$ 50 mil cada não entram na retenção, mesmo que a soma passe.",
    ],
    numeros=[],
    risco=("médio", "Regra de imposto: o juiz pede a regra inteira; a Lei 15.270/2025 também tem o imposto mínimo "
                    "de alta renda, que o calendário não traz."),
)

C["2026-11-10|longo"] = dict(
    titulo="Renda mensal com Tesouro Direto: juros semestrais e RendA+",
    estrutura="B", mecanica="extrato-falso",
    mensagem_capa="O Tesouro paga renda de dois jeitos: juros a cada seis meses, ou pagamento mensal a partir de uma data.",
    capa="O Tesouro paga renda. Mas não a cada mês.",
    slides=[
        "Títulos com juros semestrais (pagos duas vezes por ano): pra virar renda mensal, você divide cada pagamento em seis.",
        "O RendA+ (título do Tesouro pensado pra aposentadoria) junta por anos e depois paga a cada mês, corrigido pela inflação.",
        "Os dois pagam imposto de renda. O vídeo faz a conta do que sobra.",
        "Mesada semestral ou salário com data marcada pra começar?",
    ],
    legenda="Tanaka, o Tesouro paga renda, mas de seis em seis meses. E o boleto do condomínio chega a cada mês.\n\n"
            "Títulos com juros semestrais pagam duas vezes por ano, e você divide em seis. O RendA+ (título pensado "
            "pra aposentadoria) acumula por anos e depois paga mensalmente, corrigido pela inflação. Os dois têm "
            "imposto, e o vídeo faz a conta do que sobra.",
    posts=[
        "Tanaka, o Tesouro paga renda.\n\nMas de seis em seis meses.\n\nE o boleto do condomínio chega a cada mês.",
        "Extrato de um título com juros semestrais (pagos duas vezes por ano):\n\nUm mês: pagamento.\n"
        "Cinco meses: silêncio.\nDe novo: pagamento.\n\nPra virar renda mensal, você mesmo divide em seis.",
        "O RendA+ (título do Tesouro pensado pra aposentadoria) faz outra coisa:\n\nvocê junta por anos e, numa "
        "data combinada, ele passa a pagar a cada mês, corrigido pela inflação.\n\nÉ carnê ao contrário: quem recebe é você.",
        "Renda mensal com Tesouro existe.\n\nChega em blocos, ou com data marcada pra começar.\n\n"
        "A pergunta é qual dos dois combina com o seu calendário de boletos.",
    ],
    numeros=[],
    risco=("médio", "Pauta boa (renda), mas o carrossel explica mais que reage."),
)

C["2026-11-11|short"] = dict(
    titulo="FII ou aluguel: quanto rende R$ 100 mil em cada um",
    estrutura="A", mecanica="contraste",
    mensagem_capa="Comparar apartamento alugado e fundo imobiliário com R$ 100 mil exige descontar custos, imposto e tempo pra vender.",
    capa="R$ 100 mil: apartamento ou fundo imobiliário?",
    slides=[
        "Apartamento: aluguel menos IPTU e condomínio do mês vazio, reforma e imposto de renda.",
        "Fundo imobiliário: rendimento que pode sair sem imposto, se o fundo cumprir as regras.",
        "Pra vender: a cota sai pelo app, no mesmo dia. O apartamento, quando aparecer comprador.",
    ],
    legenda="Tanaka, R$ 100 mil num apartamento alugado ou num fundo imobiliário?\n\n"
            "Os dois pagam aluguel. Mas no apartamento saem IPTU e condomínio do mês vazio, manutenção e imposto de "
            "renda do aluguel. No fundo, o rendimento pode sair sem imposto, se o fundo cumprir as regras.\n\n"
            "E um dos dois te liga quando o chuveiro queima.",
    posts=[
        "Tanaka, R$ 100 mil: apartamento ou fundo imobiliário?\n\nOs dois pagam aluguel.\n\n"
        "Um deles te liga de madrugada porque o chuveiro queimou.",
        "A conta justa compara o que sobra:\n\n→ apartamento: aluguel menos IPTU e condomínio do mês vazio, "
        "reforma, corretagem e imposto\n→ fundo imobiliário: rendimento, que pode sair sem imposto\n\n"
        "Bruto contra bruto é conversa de churrasco.",
        "Cota de fundo imobiliário: vende pelo app, no mesmo dia.\n\nApartamento: vende quando aparecer comprador. E vende inteiro.\n\n"
        "Poder vender rápido não aparece na planilha. Aparece no dia em que você precisa.",
    ],
    numeros=[],
    corte_de="2026-10-06",
    risco=("baixo", "Dilema que o Tanaka vive (imóvel x fundo) com R$ na capa."),
)

C["2026-11-14|longo"] = dict(
    titulo="CDB prefixado ou pós-fixado: qual rende mais em 2026",
    estrutura="E", mecanica="atendimento-ao-cliente",
    mensagem_capa="Escolher entre CDB de taxa travada e CDB que acompanha os juros é uma aposta sobre os juros do futuro.",
    capa="CDB de taxa travada ou que segue os juros?",
    slides=[
        "Prefixado (taxa travada na compra): ganha se os juros do país caírem.",
        "Pós-fixado (acompanha os juros do país): ganha se os juros subirem.",
        "O vídeo compara com a expectativa de juros do mercado pra cada prazo.",
        "Os dois pagam o mesmo imposto de renda pelo prazo e têm a garantia do FGC (contra quebra do banco), "
        "dentro do limite.",
    ],
    legenda="Tanaka, CDB prefixado (taxa travada) ou pós-fixado (acompanha os juros do país)? Essa dúvida rendeu um "
            "vídeo aqui em 2018. A pergunta é a mesma; os juros, não.\n\n"
            "No prefixado, você ganha se os juros caírem. No pós, você acompanha os juros. O vídeo faz a conta com a "
            "expectativa de juros de hoje.\n\n"
            "Taxa travada é guarda-chuva comprado com sol.",
    posts=[
        "Tanaka, CDB de taxa travada ou flutuante?\n\nEssa dúvida rendeu um vídeo aqui em 2018.\n\n"
        "A pergunta é a mesma. Os juros, não.",
        "Prefixado (taxa travada hoje): se os juros caírem, você ganhou a aposta.\n\n"
        "Pós-fixado (segue os juros do país): se os juros subirem, você vai junto.\n\n"
        "Nos dois casos, é uma aposta sobre o futuro dos juros.",
        "— Qual rende mais?\n— Depende de pra onde os juros vão.\n— E pra onde vão?\n"
        "— Se eu soubesse, não estaria gravando vídeo.",
        "CDB de taxa travada é guarda-chuva comprado com sol.\n\nSe chover, você é gênio.\n\nSe fizer sol, carregou peso à toa.",
    ],
    numeros=[],
    risco=("médio", "Pauta de produto bancário; título com 'qual rende mais' pode soar comparativo de compra."),
)

C["2026-11-19|longo"] = dict(
    titulo="Bitcoin depois do 'alerta': o que mudou desde fevereiro",
    estrutura="B", mecanica="necrologio",
    mensagem_capa="O vídeo confere, com os dados de hoje, os argumentos do alerta de fevereiro sobre o bitcoin.",
    capa="O alerta do bitcoin de fevereiro acertou?",
    slides=[
        "Em fevereiro, o vídeo perguntava: morte do bitcoin?",
        "Agora, cada argumento daquele alerta, com o dado de hoje do lado.",
        "\"Posso perder mais do que investi?\" Comprando à vista, não. Com alavancagem (dinheiro emprestado), pode.",
        "O vídeo não chuta preço. Mostra o que mudou desde fevereiro.",
    ],
    legenda="Tanaka, lembra do alerta do bitcoin? Fevereiro, título em caixa alta: \"Morte do bitcoin?\"\n\n"
            "O vídeo pega os argumentos daquele alerta e confere cada um com os dados de hoje. Também responde uma "
            "pergunta que apareceu nos comentários: dá pra perder mais do que investiu? Comprando à vista, não. Com "
            "alavancagem (dinheiro emprestado), pode.\n\n"
            "Sem previsão de preço.",
    posts=[
        "Tanaka, lembra do alerta do bitcoin?\n\nFevereiro. Título em caixa alta: \"Morte do bitcoin?\"\n\n"
        "Agora é abrir o arquivo e ver o que envelheceu bem.",
        "Alerta tem prazo de validade.\n\nO de fevereiro tinha argumentos. O vídeo pega cada um e põe o dado de hoje "
        "do lado.\n\nO que se confirmou fica. O que não se confirmou, a gente admite.",
        "E uma pergunta que apareceu nos comentários:\n\n\"Posso perder mais do que investi?\"\n\n"
        "Comprando à vista, o máximo que se perde é o que se colocou. Com alavancagem (dinheiro emprestado), é outra história.",
        "Alerta de \"morte do bitcoin\" não era sobre a morte dele.\n\n"
        "Era sobre quanto do seu dinheiro você aguenta ver no velório.",
    ],
    numeros=[],
    risco=("baixo", "Nome que o brasileiro reconhece (bitcoin) e continuação de top 10."),
)

C["2026-11-24|longo"] = dict(
    titulo="Dividendos mensais com a Selic caindo: o que acontece",
    estrutura="D", mecanica="eco-do-gatilho (vizinho)",
    mensagem_capa="Quando os juros do país caem, a renda fixa nova paga menos e cada tipo de renda reage de um jeito.",
    capa="Quando os juros caem, quem vive de renda perde?",
    slides=[
        "Juro alto: a renda fixa paga bem sem esforço, e o dividendo precisa competir com isso.",
        "Juro em queda: a renda fixa nova paga menos. Parte do dinheiro pode procurar renda em outro lugar.",
        "Fundo imobiliário de papel ligado aos juros recebe menos. O de tijolo depende do aluguel.",
        "Empresa com dívida paga menos juros, e o lucro respira. O vídeo mostra o histórico de outros ciclos.",
    ],
    legenda="Tanaka, quando a Selic (os juros básicos do país) cai, quem vive de renda perde?\n\n"
            "A renda fixa nova paga menos. Fundo imobiliário de papel ligado aos juros recebe menos. Empresa "
            "endividada respira. O vídeo mostra, com o histórico, como cada renda reagiu nos ciclos anteriores.\n\n"
            "Não é previsão. É memória.",
    posts=[
        "Tanaka, quando os juros caem, quem perde?\n\nA Selic (os juros básicos do país) caindo faz a renda fixa nova "
        "pagar menos.\n\nO que pouca gente olha é quem vive de dividendo.",
        "Juro alto é o vizinho que faz churrasco a cada semana.\n\n"
        "A renda fixa paga bem sem esforço, e o dividendo precisa competir.\n\nPouca gente aparece na festa do dividendo.",
        "Juro em queda: o vizinho diminui o churrasco.\n\n"
        "Parte do dinheiro pode ir pra fundo imobiliário e ação que paga dividendo. Pode.\n\n"
        "Se foi assim nas outras vezes, o histórico do vídeo mostra.",
        "Dentro das empresas e dos fundos:\n\n→ dívida mais barata ajuda o lucro\n"
        "→ fundo imobiliário de papel ligado aos juros recebe menos\n→ fundo de tijolo depende do aluguel",
    ],
    numeros=[],
    risco=("médio", "Pauta macro com ponte pra renda; clareza depende de o leitor ligar juros e dividendos."),
)

C["2026-11-25|short"] = dict(
    titulo="Taxa de administração do ETF: quanto tira em 10 anos",
    estrutura="A", mecanica="conta-rapida",
    mensagem_capa="Em 10 anos, a diferença entre uma taxa de 0,5% e uma de 1,5% ao ano vira milhares de reais.",
    capa="Taxa de 1,5% ao ano parece pouco.",
    slides=[
        "A taxa de administração (o que o gestor cobra por ano) sai do patrimônio do fundo.",
        "Conta em cada R$ 100 mil, por 10 anos, sem contar rendimento.",
        "Taxa de 0,5% ao ano: cerca de R$ 4,9 mil pelo caminho.",
        "Taxa de 1,5% ao ano: cerca de R$ 14 mil. Quase o triplo.",
    ],
    legenda="Tanaka, taxa de 1,5% ao ano num ETF (fundo vendido na bolsa) parece pouco. Em 10 anos, não é.\n\n"
            "Na conta simples, em cada R$ 100 mil e sem contar rendimento, 0,5% ao ano levam cerca de R$ 4,9 mil. A "
            "de 1,5% leva cerca de R$ 14 mil. Um ponto de diferença, quase o triplo de mordida.\n\n"
            "A taxa não manda boleto.",
    posts=[
        "Tanaka, taxa de 1,5% ao ano parece pouco.\n\nCom o tempo, não é.",
        "Conta no guardanapo, em cada R$ 100 mil, por 10 anos: taxa de 0,5% ao ano leva cerca de R$ 4,9 mil.",
        "Nos mesmos 10 anos, a taxa de 1,5% ao ano leva cerca de R$ 14 mil.\n\n"
        "Um ponto de diferença, quase o triplo de mordida.\n\nE a taxa não manda boleto.",
    ],
    numeros=[
        arq("100", CAL, "FII ou aluguel: quanto rende R$ 100 mil em cada um"),
        conta("4,9", "100000 * (1 - 0.995 ** 10) / 1000", "R$ 100 mil, 0,5% ao ano, 10 anos (CALENDARIO 25/11 e 11/11)"),
        conta("14", "100000 * (1 - 0.985 ** 10) / 1000", "R$ 100 mil, 1,5% ao ano, 10 anos (CALENDARIO 25/11 e 11/11)"),
    ],
    corte_de="2026-10-14",
    risco=("baixo", "Conta em R$ mandável ('quase o triplo de mordida')."),
)

C["2026-11-26|longo"] = dict(
    titulo="Fundos imobiliários caíram em 2026: e a renda deles?",
    estrutura="E", mecanica="contraste",
    mensagem_capa="Em 2026, o preço das cotas dos fundos imobiliários caiu; o vídeo mostra se o aluguel distribuído caiu junto.",
    capa="As cotas caíram. O aluguel caiu junto?",
    slides=[
        "Cota: o preço que o mercado paga hoje por um pedaço do fundo.",
        "Rendimento: o aluguel ou o juro que o fundo recebeu e repassou.",
        "Um pode cair sem o outro. O vídeo separa o que caiu do que não caiu.",
        "O preço do prédio caiu? O inquilino pode continuar pagando o mesmo aluguel.",
    ],
    legenda="Tanaka, os fundos imobiliários caíram em 2026. E a renda deles?\n\n"
            "Cota e rendimento são coisas diferentes: a cota é o preço de hoje, o rendimento é o aluguel ou juro "
            "repassado. O vídeo separa o que caiu do que não caiu, sem indicar fundo.\n\n"
            "Preço do prédio caiu não quer dizer inquilino sumiu.",
    posts=[
        "Tanaka, os fundos imobiliários caíram em 2026.\n\nA pergunta que importa não é quanto caiu a cota.\n\n"
        "É se o aluguel caiu junto.",
        "Cota é o preço que o mercado paga hoje.\n\nRendimento é o aluguel ou o juro que o fundo recebeu e repassou.\n\n"
        "Um pode cair sem o outro.",
        "É como o preço do apartamento no prédio.\n\nO vizinho vendeu barato e o preço do seu caiu.\n\n"
        "Mas o inquilino continua pagando o aluguel no mesmo dia.",
        "Cota caindo assusta quem olha a tela.\n\nRendimento caindo machuca quem vive da renda.\n\n"
        "Saber qual dos dois caiu muda a conversa.",
    ],
    numeros=[],
    risco=("baixo", "Dor no bolso de quem tem fundo imobiliário, com uma ideia por peça."),
)


# ------------------------------------------------------------------ voltou da fila de dezembro (v3 ajustado, T15)
C["2026-10-20|longo"] = dict(
    titulo="TRXF11: o que aconteceu com a renda desde agosto",
    estrutura="C", mecanica="mito-x-fato",
    mensagem_capa="O vídeo mostra os números do fundo mais buscado no canal desde agosto, sem dizer se compra ou vende.",
    capa="Esse fundo lidera as buscas do canal. E a renda?",
    slides=[
        "TRXF11 (um fundo imobiliário) é o termo de investimento mais buscado do canal nos últimos 6 meses.",
        "Rendimento: quanto o fundo distribuiu, mês a mês, desde agosto.",
        "Imóvel vazio: quanto dos imóveis está sem inquilino. Cota: quanto o mercado paga hoje.",
        "O número é do fundo. A decisão é sua. O vídeo não diz compra nem venda.",
    ],
    legenda="Tanaka, o TRXF11 (um fundo imobiliário) foi o termo de investimento mais buscado no canal nos últimos "
            "6 meses.\n\n"
            "Então o vídeo abre os números do fundo desde agosto: rendimento distribuído, imóveis sem inquilino e "
            "preço da cota, mês a mês, a partir dos relatórios do fundo.\n\n"
            "Acompanhamento neutro. Aqui não tem dica de compra nem de venda.",
    posts=[
        "Tanaka, esse fundo lidera as buscas do canal.\n\nÉ o TRXF11 (um fundo imobiliário).\n\n"
        "Então vamos aos números dele, sem torcida.",
        "É o termo de investimento mais buscado do canal nos últimos 6 meses.\n\n"
        "Quem tem cota quer saber se a renda vai se manter.\n\n"
        "Pergunta justa. A resposta vem dos relatórios do fundo, não do grupo de WhatsApp.",
        "Desde agosto, três linhas contam a história:\n\n→ quanto o fundo distribuiu de rendimento\n"
        "→ quanto dos imóveis está vazio\n→ quanto vale a cota",
        "Mito: o vídeo vai dizer se compra ou vende.\n\n"
        "Fato: o vídeo mostra rendimento, imóvel vazio e cota, mês a mês, e para aí.\n\n"
        "O número é do fundo. A decisão é sua.",
    ],
    numeros=[],
    risco=("baixo", "Nome que o público busca + bolso de quem tem cota. Neutro, sem recomendação. Voltou da fila de dezembro (troca T15); texto do card de 31/10 do v2, números reconferidos: o único é '6 meses', da linha do calendário."),
)


# ------------------------------------------------------------------ v3: série de renda mensal e Tesouro antes do Copom
# Fontes: serie/SERIE-RENDA-MENSAL.md, serie/MOLDE-TESOURO-COPOM.md e, no Ep. 1, só a seção "4. DADOS CONFERIDOS" de
# briefings/2026-10-14-etf-dividendos-mensais-briefing.md (o que está "A CONFERIR" vira [CHECAR: ...]).
SERIE = "serie/SERIE-RENDA-MENSAL.md"
MOLDE = "serie/MOLDE-TESOURO-COPOM.md"
BRIEF_EP1 = "briefings/2026-10-14-etf-dividendos-mensais-briefing.md"

N_EP1_SHORT = [
    arq("100", BRIEF_EP1, "R$ 100 mil → R$ 88.638 de cota + R$ 11.362 de renda"),
    arq("88.638", BRIEF_EP1, "R$ 100 mil → R$ 88.638 de cota + R$ 11.362 de renda"),
    arq("11.362", BRIEF_EP1, "R$ 100 mil → R$ 88.638 de cota + R$ 11.362 de renda"),
    arq("100.000", BRIEF_EP1, "R$ 100.000 (zero)"),
]
N_EP2 = [
    arq("1", SERIE, "dividendo de R$ 1 por ação; preço de R$ 20 → yield de 5%. Preço cai para R$ 10 → yield de 10%."),
    arq("20", SERIE, "dividendo de R$ 1 por ação; preço de R$ 20 → yield de 5%. Preço cai para R$ 10 → yield de 10%."),
    arq("5", SERIE, "dividendo de R$ 1 por ação; preço de R$ 20 → yield de 5%. Preço cai para R$ 10 → yield de 10%."),
    arq("10", SERIE, "dividendo de R$ 1 por ação; preço de R$ 20 → yield de 5%. Preço cai para R$ 10 → yield de 10%."),
]
N_EP3 = [
    arq("600", SERIE, "uma pessoa recebe R$ 600 por mês e a outra R$ 1.230"),
    arq("1.230", SERIE, "uma pessoa recebe R$ 600 por mês e a outra R$ 1.230"),
    arq("100", SERIE, "R$ 100 mil rendendo 0,6% ao mês"),
    arq("0,6", SERIE, "R$ 100 mil rendendo 0,6% ao mês"),
    arq("205", SERIE, "100.000 × 1,006¹²⁰ ≈ R$ 205 mil em 10 anos"),
    arq("10", SERIE, "100.000 × 1,006¹²⁰ ≈ R$ 205 mil em 10 anos"),
    conta("205", "100000 * 1.006 ** 120 / 1000", "R$ 100 mil a 0,6% ao mês por 120 meses (SERIE-RENDA-MENSAL.md, Ep. 3)"),
    conta("1.230", "100000 * 1.006 ** 120 * 0.006", "renda de 0,6% sobre ~R$ 205 mil (SERIE-RENDA-MENSAL.md, Ep. 3)"),
]
N_EP4 = [
    arq("120", SERIE, "R$ 120 mil divididos em 12 aplicações de R$ 10 mil, de 12 meses cada, uma por mês"),
    arq("12", SERIE, "R$ 120 mil divididos em 12 aplicações de R$ 10 mil, de 12 meses cada, uma por mês"),
    arq("10", SERIE, "R$ 120 mil divididos em 12 aplicações de R$ 10 mil, de 12 meses cada, uma por mês"),
    arq("13", SERIE, "Do 13º mês em"),
    arq("6", SERIE, "prazo mínimo de 6 meses (Res. CMN 5.215)"),
]
N_EP5 = [
    arq("1.000", SERIE, "R$ 1.000 por mês hoje, com a inflação de agora, compram R$ 661 daqui a 10 anos."),
    arq("661", SERIE, "R$ 1.000 por mês hoje, com a inflação de agora, compram R$ 661 daqui a 10 anos."),
    arq("10", SERIE, "R$ 1.000 por mês hoje, com a inflação de agora, compram R$ 661 daqui a 10 anos."),
    arq("4,22", SERIE, "IPCA de 12 meses até ago/2026 de 4,22% (SGS 13522)"),
    arq("42", SERIE, "ao ano e a inflação é 4,22%, reinvista 42% da renda (4,22 ÷ 10) e gaste 58%."),
    arq("10", SERIE, "Se o investimento rende 10%"),
    conta("661", "1000 / 1.0422 ** 10", "R$ 1.000 descontados de 4,22% ao ano por 10 anos (SERIE-RENDA-MENSAL.md, Ep. 5)"),
]

C["2026-10-07|short"] = dict(
    titulo="Recebeu 1% ao mês e a cota caiu 1%: quanto ganhou?",
    estrutura="B", mecanica="conta-rapida",
    mensagem_capa="Receber 1% ao mês enquanto a cota cai 1% ao mês dá, em um ano, ganho zero.",
    capa="Recebeu 1% ao mês. Ganhou quanto?",
    slides=[
        "Exemplo: R$ 100 mil num ETF (fundo vendido na bolsa) que paga 1% ao mês.",
        "Em um ano, a renda que caiu na conta soma R$ 11.362.",
        "No mesmo ano, a cota cai 1% ao mês e termina em R$ 88.638.",
        "Somando os dois: R$ 100.000. Ganho de zero. Na vida real, nem sempre dá zero.",
    ],
    legenda="Tanaka, um ETF (fundo vendido na bolsa) te paga 1% ao mês, e a cota cai 1% ao mês. Quanto você ganhou "
            "em um ano?\n\n"
            "No exemplo, R$ 100 mil viram R$ 11.362 de renda e R$ 88.638 de cota. Somando: R$ 100.000. Zero.\n\n"
            "O extrato mostra a renda caindo na conta. A cota descendo, você descobre quando vende. Na vida real, nem "
            "sempre dá zero: o vídeo com dois ETFs de verdade sai na quarta que vem.",
    posts=[
        "Tanaka, recebeu 1% ao mês e ficou feliz?\n\nA cota caiu 1% ao mês no mesmo período.\n\nAgora soma.",
        "Exemplo com R$ 100 mil num ETF (fundo vendido na bolsa):\n\n→ renda do ano: R$ 11.362\n"
        "→ cota no fim: R$ 88.638\n\nSoma: R$ 100.000.",
        "Ganho do ano, no exemplo: zero.\n\nO extrato mostra a renda caindo na conta. A cota descendo, ele não mostra.\n\n"
        "Na vida real, nem sempre dá zero. O vídeo com dois fundos de verdade sai na quarta que vem.",
    ],
    numeros=list(N_EP1_SHORT),
    risco=("baixo", "Conta em R$ simples e mandável; exemplo hipotético dito como exemplo."),
)

C["2026-10-14|longo"] = dict(
    titulo="ETF que paga dividendos mensais: a renda saiu da cota?",
    estrutura="E", mecanica="extrato-falso",
    mensagem_capa="Olhando só a cota, um ETF parece ter perdido R$ 9 mil para o gêmeo; somando a renda, perdeu R$ 740.",
    capa="Parece que perdeu R$ 9 mil. Perdeu?",
    slides=[
        "Dois ETFs (fundos vendidos na bolsa) do mesmo índice: o DIVD11 (paga renda mensal) e o DIVO11 (reinveste).",
        "A cota sozinha, em 12 meses: a do que reinveste subiu 24,41%; a do que paga renda, 15,15%.",
        "Somando a renda que caiu na conta, o que paga renda chega a 23,67%. A diferença cai pra 0,74 ponto.",
        "Em R$ 100 mil, a perda aparente de R$ 9.260 vira R$ 740.",
    ],
    legenda="Tanaka, dois ETFs (fundos vendidos na bolsa) do mesmo índice. Olhando a cota sozinha, o DIVD11, que paga "
            "renda mensal, parece ter perdido R$ 9.260 em cada R$ 100 mil para o DIVO11, que reinveste.\n\n"
            "Mas ele pagou R$ 4,7614 por cota em 12 eventos: 8,52 pontos voltaram como renda. A diferença de verdade "
            "foi de R$ 740. Com o imposto na mesma régua, quase empatou.\n\n"
            "Os dois entram como prova da conta, não como escolha.",
    posts=[
        "Tanaka, parece que perdeu R$ 9 mil.\n\nUm ETF (fundo vendido na bolsa) que paga renda mensal ficou atrás do "
        "gêmeo que reinveste.\n\nMas a renda caiu na conta. Somando, a história muda.",
        "A cota sozinha, num ano:\n\n→ DIVO11 (fundo da bolsa que reinveste): +24,41%\n→ DIVD11 (fundo da bolsa que paga renda mensal): +15,15%\n\n"
        "Parece perda. Falta somar a renda que caiu na conta.",
        "Somando a renda que o DIVD11 (fundo da bolsa que paga renda mensal) pagou no ano, o retorno total vai a 23,67%.\n\n"
        "A diferença pro gêmeo cai pra 0,74 ponto: R$ 740 em cada R$ 100 mil.\n\n"
        "Os dois entram como prova da conta, não como escolha.",
        "E o imposto? O DIVD11 (fundo da bolsa que paga renda mensal) tem 15% retidos a cada pagamento; o gêmeo paga 15% ao vender.\n\n"
        "Com os dois vendidos: 20,12% contra 20,75%. Quase empatou.\n\n"
        "E não é a taxa: a dos dois é 0,50% ao ano.",
        "O SPYI11 (fundo da bolsa que investe num fundo americano) pagou quase 1% ao mês, em reais.\n\n"
        "Somando renda e cota: 10,37% em um ano, contra 14,47% do CDI (taxa de referência dos CDBs).\n\n"
        "Quem vende as opções de compra (a alta acima de um preço) é o fundo americano, o SPYI.",
    ],
    numeros=[
        arq("24,41", BRIEF_EP1, "R$ 132,90 (01/10/2026): **+24,41%**"),
        arq("15,15", BRIEF_EP1, "R$ 55,86 → R$ 64,32: **+15,15%**"),
        arq("4,7614", BRIEF_EP1, "**R$ 4,7614 por cota bruto** em 12 eventos"),
        arq("12", BRIEF_EP1, "**R$ 4,7614 por cota bruto** em 12 eventos"),
        arq("23,67", BRIEF_EP1, "Retorno total **23,67% bruto, 22,39% líquido**"),
        arq("15", BRIEF_EP1, "**15%, retido na fonte na data da distribuição**"),
        arq("20,75", BRIEF_EP1, "DIVO11 24,41% × 0,85 = 20,75%; DIVD11 15,15% × 0,85 + 7,25% = 20,12%"),
        arq("20,12", BRIEF_EP1, "DIVO11 24,41% × 0,85 = 20,75%; DIVD11 15,15% × 0,85 + 7,25% = 20,12%"),
        arq("0,50", BRIEF_EP1, "**Taxa Total Máxima 0,50% ao ano** nos dois"),
        arq("10,37", BRIEF_EP1, "Retorno total **10,37% bruto, 8,61% líquido**"),
        arq("14,47", BRIEF_EP1, "**14,47%** (251 dias úteis, 02/10/2025 a 01/10/2026)"),
        conta("9", "24.41 - 15.15", "cotas do DIVO11 e do DIVD11 (C1 e C2): 9,26 pontos, 'R$ 9 mil' em R$ 100 mil"),
        conta("9.260", "100000 * (0.2441 - 0.1515)", "R$ 100 mil x 9,26 pontos (C1 e C2)"),
        conta("100", "100000 / 1000", "base de R$ 100 mil"),
        conta("8,52", "4.7614 / 55.86 * 100", "R$ 4,7614 por cota (R4) sobre a cota de R$ 55,86 (C2)"),
        conta("0,74", "24.41 - 23.67", "DIVO11 (C1) menos o retorno total do DIVD11 (R4)"),
        conta("740", "100000 * (0.2441 - 0.2367)", "0,74 ponto em R$ 100 mil (C1 e R4)"),
        conta("1", "13.0763 / 111.15 / 12 * 100", "'quase 1% ao mês': R$ 13,0763 em 12 eventos (R7) sobre a cota de R$ 111,15 (C3)"),
    ],
    risco=("baixo", "Virada forte e conferida (R$ 9.260 que vira R$ 740), com tickers como prova da conta, não escolha. "
                    "Imposto e taxa na régua do briefing (sem 'o imposto mensal é o que custa' e sem pôr os 0,74 ponto "
                    "na taxa)."),
)

C["2026-10-21|longo"] = dict(
    titulo="Dividendos altos demais: 4 contas antes de confiar na renda",
    estrutura="D", mecanica="mito-x-fato",
    mensagem_capa="Um dividendo alto pode ser só o preço da ação caindo; quatro contas mostram se a renda se sustenta.",
    capa="Dividendo alto: renda ou susto?",
    slides=[
        "Primeira conta, o preço. Exemplo: dividendo de R$ 1 por ação, com a ação a R$ 20, rende 5%.",
        "A ação cai pra R$ 10. O mesmo R$ 1 agora rende 10%. A empresa não pagou nada a mais.",
        "Segunda conta: payout (dividendo dividido pelo lucro). Acima de 100%, a empresa paga mais do que ganhou.",
        "Terceira e quarta: lucro que não se repete e o histórico de 5 anos do dividendo por ação.",
    ],
    legenda="Tanaka, o dividend yield (quanto o dividendo rende sobre o preço) pode dobrar sem a empresa pagar um real a "
            "mais. Basta o preço cair pela metade.\n\n"
            "O vídeo traz 4 contas antes de confiar na renda: o efeito do preço, o payout (dividendo dividido pelo "
            "lucro), o lucro que não se repete e o histórico de 5 anos. Sem lista de ações.",
    posts=[
        "Tanaka, o rendimento dobrou.\n\nA empresa pagou o mesmo. O preço da ação é que caiu pela metade.\n\n"
        "Renda alta pode ser susto disfarçado.",
        "Mito: dividendo alto é renda garantida.\n\nFato: no exemplo, R$ 1 por ação com a ação a R$ 20 rende 5%. A ação "
        "cai pra R$ 10 e o mesmo R$ 1 rende 10%.\n\nA renda não mudou. O risco, talvez.",
        "Segunda conta: payout (dividendo dividido pelo lucro).\n\nExemplo: lucro de R$ 100 milhões e dividendos de "
        "R$ 150 milhões. Payout de 150%.\n\nA diferença saiu do caixa ou de dívida.",
        "Terceira: lucro que não se repete, como a venda de um ativo da empresa.\n\nQuarta: o dividendo por ação dos "
        "últimos 5 anos.\n\nUma linha que pula de 1 pra 4 e volta pra 1 não é renda mensal.",
    ],
    numeros=list(N_EP2) + [
        arq("100", SERIE, "Lucro de R$ 100 milhões e dividendos de R$ 150 milhões = 150%."),
        arq("150", SERIE, "Lucro de R$ 100 milhões e dividendos de R$ 150 milhões = 150%."),
        arq("5", SERIE, "**Histórico de 5 anos:**"),
        arq("4", SERIE, "Uma linha que pula de 1 para 4 e volta para 1"),
    ],
    risco=("baixo", "Bolso claro (dividendo) e critério aplicável; exemplos hipotéticos ditos como exemplo."),
)

C["2026-10-21|short"] = dict(
    titulo="O dividend yield dobrou e a empresa não pagou nada a mais",
    estrutura="A", mecanica="conta-rapida",
    mensagem_capa="O rendimento do dividendo pode dobrar só porque o preço da ação caiu pela metade.",
    capa="O rendimento dobrou. A empresa pagou igual.",
    slides=[
        "Exemplo: dividendo de R$ 1 por ação. Com a ação a R$ 20, rende 5% ao ano.",
        "A ação cai pra R$ 10. O mesmo R$ 1 agora rende 10%.",
        "O dividendo não subiu. O preço é que caiu. Antes de comemorar, olhe por que caiu.",
    ],
    legenda="Tanaka, o dividend yield (quanto o dividendo rende sobre o preço da ação) dobrou e a empresa não pagou nada "
            "a mais.\n\n"
            "No exemplo, R$ 1 de dividendo com a ação a R$ 20 rende 5%. A ação cai pra R$ 10, e o mesmo R$ 1 rende 10%. "
            "A renda não mudou. O que mudou foi o preço.\n\n"
            "Rendimento alto pede a pergunta: por que o preço caiu?",
    posts=[
        "Tanaka, o rendimento dobrou. A empresa pagou igual.\n\nO truque não é da empresa. É da conta.",
        "Conta rápida, com exemplo:\n\n→ R$ 1 de dividendo, ação a R$ 20: rende 5%\n"
        "→ ação cai pra R$ 10: o mesmo R$ 1 rende 10%",
        "O dividendo não subiu. O preço caiu.\n\nAntes de comemorar o rendimento alto, pergunte por que a ação caiu "
        "pela metade.",
    ],
    numeros=list(N_EP2),
    risco=("baixo", "Conta curta e mandável."),
)

C["2026-10-28|longo"] = dict(
    titulo="Gastar ou reinvestir os dividendos: a conta de 10 anos",
    estrutura="C", mecanica="contraste",
    mensagem_capa="Com o mesmo dinheiro, gastar ou reinvestir a renda muda quanto você recebe daqui a 10 anos.",
    capa="Gastar a renda hoje custa quanto?",
    slides=[
        "Exemplo: R$ 100 mil rendendo 0,6% ao mês, sem imposto e sem inflação, pra simplificar.",
        "Gastando a renda: R$ 600 por mês. O capital segue em R$ 100 mil.",
        "Reinvestindo: em 10 anos, cerca de R$ 205 mil. A renda do mês seguinte vira cerca de R$ 1.230.",
        "Meio-termo: reinvestir a parte da inflação e gastar o resto. A planilha mostra o custo de cada escolha.",
    ],
    legenda="Tanaka, com o mesmo dinheiro, uma pessoa recebe R$ 600 por mês e outra R$ 1.230. A diferença é uma decisão "
            "tomada 10 anos antes.\n\n"
            "No exemplo, R$ 100 mil rendendo 0,6% ao mês: quem gasta a renda fica com R$ 600 por mês; quem reinveste "
            "chega a cerca de R$ 205 mil e passa a receber cerca de R$ 1.230. O vídeo mostra o meio-termo.",
    posts=[
        "Tanaka, mesmo dinheiro, rendas diferentes.\n\nUma pessoa recebe R$ 600 por mês. A outra, quase o dobro.\n\n"
        "A diferença foi uma decisão tomada uma década antes.",
        "Exemplo: R$ 100 mil rendendo 0,6% ao mês, sem imposto e sem inflação.\n\n"
        "Gastando a renda: R$ 600 por mês, e o capital fica em R$ 100 mil.",
        "Reinvestindo a renda por 10 anos: cerca de R$ 205 mil.\n\nA renda do mês seguinte vira cerca de R$ 1.230.\n\n"
        "Mesmo dinheiro inicial. Escolha diferente.",
        "Precisa da renda agora? Existe o meio-termo: reinvestir a parte da inflação e gastar o resto.\n\n"
        "A taxa do exemplo é exemplo. A diferença entre as colunas aparece com qualquer taxa positiva.",
    ],
    numeros=list(N_EP3),
    risco=("baixo", "Conta em R$ com contraste forte (R$ 600 x R$ 1.230)."),
)

C["2026-11-03|longo"] = dict(
    titulo="Tesouro Direto antes do Copom: o que olhar no IPCA+ hoje",
    estrutura="B", mecanica="atendimento-ao-cliente",
    mensagem_capa="Antes da decisão dos juros de quarta, o vídeo mostra quais números do Tesouro anotar hoje.",
    capa="Amanhã decidem os juros. O que olhar hoje?",
    slides=[
        "Amanhã à noite, o Copom (reunião do Banco Central que decide os juros) anuncia a Selic (juros básicos do país).",
        "O que o mercado espera pra reunião: [CHECAR: Selic esperada no Focus da semana].",
        "Anote as taxas de hoje do Tesouro IPCA+ (inflação mais uma taxa) e do prefixado (taxa travada).",
        "Em setembro, com o corte esperado, o Tesouro IPCA+ 2035 (título atrelado à inflação) mexeu 0,05 ponto.",
    ],
    legenda="Tanaka, amanhã o Copom (a reunião do Banco Central que decide os juros) anuncia a Selic. Hoje é o dia de "
            "anotar os números do seu Tesouro.\n\n"
            "O vídeo mostra o que o mercado espera pra reunião, as taxas do Tesouro IPCA+ e do prefixado na manhã de "
            "hoje e o que observar no comunicado. Sem previsão da decisão.\n\n"
            "Em setembro, o corte veio igual ao esperado, e o IPCA+ quase não se mexeu.",
    posts=[
        "Tanaka, amanhã decidem os juros do país.\n\nÉ o Copom (a reunião do Banco Central). O anúncio sai à noite.\n\n"
        "Hoje é o dia de anotar os números do seu Tesouro.",
        "Três números pra anotar hoje:\n\n→ a Selic (juros básicos) que o mercado espera\n"
        "→ a taxa do Tesouro IPCA+ (inflação mais uma taxa)\n→ a taxa do prefixado (taxa travada)",
        "— O que vai acontecer com o meu título?\n— Depende da surpresa, não da decisão.\n— Como assim?\n"
        "— Se vier o esperado, o preço mexe pouco. Se vier diferente, mexe mais.",
        "Em setembro, o corte veio igual ao esperado.\n\nO Tesouro IPCA+ 2035 (título atrelado à inflação) mexeu "
        "0,05 ponto.\n\nO vídeo não chuta a decisão. Mostra o que olhar.",
    ],
    numeros=[
        arq("2035", MOLDE, "| Tesouro IPCA+ 2035 | 7,60% | 7,55% | −0,05 p.p. |"),
        arq("0,05", MOLDE, "| Tesouro IPCA+ 2035 | 7,60% | 7,55% | −0,05 p.p. |"),
    ],
    evento_ao_vivo="Postar ANTES do anúncio do Copom (04/11, a partir das 18h30). Preencher o [CHECAR] com o Focus "
                   "da semana; as taxas da manhã vêm do site do Tesouro Direto, com a hora.",
    risco=("baixo", "Tesouro é o assunto com mais inscritos por longo; evento com data. Pendência: o Focus [CHECAR]."),
)

C["2026-11-11|longo"] = dict(
    titulo="LCI e LCA para renda mensal: a escada de vencimentos",
    estrutura="D", mecanica="tradutor-juramentado",
    mensagem_capa="LCI e LCA não pagam juros a cada mês, mas dá pra fazer uma vencer a cada mês.",
    capa="Faça uma aplicação vencer a cada mês.",
    slides=[
        "LCI e LCA (aplicações de banco sem imposto de renda pra pessoa física) pagam no vencimento, não a cada mês.",
        "A escada: R$ 120 mil em 12 aplicações de R$ 10 mil, de 12 meses cada, uma por mês.",
        "Do 13º mês em diante, vence uma por mês. Gasta o rendimento e o principal volta pra um novo degrau.",
        "Ela demora a começar: prazo mínimo de 6 meses pra LCI e LCA (aplicações de banco). Não serve como reserva.",
    ],
    legenda="Tanaka, LCI e LCA (aplicações de banco sem imposto de renda pra pessoa física) não pagam juros a cada mês. "
            "Mas dá pra fazer vencer uma por mês.\n\n"
            "No exemplo, R$ 120 mil viram 12 aplicações de R$ 10 mil, de 12 meses cada. Do 13º mês em diante, vence uma "
            "por mês. O prazo mínimo de 6 meses faz a escada demorar a começar, e ela não serve como reserva.",
    posts=[
        "Tanaka, essa aplicação não paga a cada mês.\n\nÉ a LCI ou a LCA (aplicação de banco sem imposto de renda).\n\n"
        "Mas dá pra fazer uma vencer a cada mês.",
        "Tradução de \"escada de vencimentos\": R$ 120 mil divididos em 12 aplicações de R$ 10 mil, de 12 meses cada, "
        "uma por mês.\n\nDo 13º mês em diante, vence uma por mês.",
        "Venceu o degrau: gasta o rendimento, e o principal volta pra um novo degrau de 12 meses.\n\n"
        "A escada se repete. A renda chega no ritmo dos vencimentos.",
        "Ela demora a começar: LCI e LCA (aplicações de banco) têm prazo mínimo de 6 meses.\n\n"
        "E o dinheiro fica preso até vencer. Por isso a escada não serve como reserva.",
    ],
    numeros=list(N_EP4),
    risco=("médio", "Produto bancário; construção útil, mas o carrossel explica mais que reage."),
)

C["2026-11-16|short"] = dict(
    titulo="LCI e LCA não pagam todo mês. Mas dá para fazer vencer uma por mês",
    estrutura="C", mecanica="pergunta-do-leitor",
    mensagem_capa="Com 12 aplicações escalonadas, uma LCI ou LCA vence a cada mês a partir do 13º mês.",
    capa="Uma aplicação vencendo por mês. Dá?",
    slides=[
        "\"Mas LCI e LCA (aplicações de banco) não pagam mensal?\" Não. Pagam no vencimento.",
        "A escada: 12 aplicações de R$ 10 mil, de 12 meses cada, uma por mês.",
        "Do 13º mês em diante, vence uma por mês. No começo, a escada ainda está subindo.",
    ],
    legenda="Tanaka, LCI e LCA (aplicações de banco sem imposto de renda pra pessoa física) não pagam mensal. Mas dá pra "
            "fazer vencer uma por mês.\n\n"
            "A escada: 12 aplicações de R$ 10 mil, de 12 meses cada, uma por mês. Do 13º mês em diante, vence uma por "
            "mês, e o dinheiro de cada degrau volta pra um novo.\n\n"
            "A escada demora a começar. Depois, anda sozinha.",
    posts=[
        "Tanaka, quer uma aplicação vencendo por mês?\n\nCom LCI e LCA (aplicações de banco), dá. É uma escada.",
        "\"Mas LCI e LCA (aplicações de banco) não pagam mensal?\"\n\nNão. Pagam no vencimento.\n\n"
        "Por isso a escada: 12 aplicações de R$ 10 mil, de 12 meses cada, uma por mês.",
        "Do 13º mês em diante, vence uma por mês.\n\nO dinheiro de cada degrau volta pra um novo.\n\n"
        "A escada demora a começar. Depois, anda sozinha.",
    ],
    numeros=list(N_EP4),
    risco=("médio", "Produto bancário; capa clara."),
)

C["2026-11-18|longo"] = dict(
    titulo="Renda mensal e inflação: quanto reinvestir para não encolher",
    estrutura="E", mecanica="manual-invertido",
    mensagem_capa="Com a inflação de agora, R$ 1.000 de renda hoje compram cerca de R$ 661 daqui a 10 anos.",
    capa="Sua renda de hoje encolhe em 10 anos.",
    slides=[
        "Com 4,22% de inflação ao ano, mantida igual, R$ 1.000 de hoje compram cerca de R$ 661 depois de uma década.",
        "Regra de bolso: reinvista a parte da renda igual à inflação. O resto você pode gastar.",
        "Exemplo: rendendo 10% ao ano, com 4,22% de inflação, reinvista 42% da renda.",
        "O Tesouro IPCA+ (título que paga a inflação mais uma taxa) já corrige o valor. A taxa é a parte acima dela.",
    ],
    legenda="Tanaka, R$ 1.000 de renda hoje compram cerca de R$ 661 daqui a 10 anos, com 4,22% de inflação ao ano "
            "mantida igual.\n\n"
            "O vídeo mostra quanto da renda precisa voltar pro investimento pra ela valer o mesmo: a parte igual à "
            "inflação. No exemplo, rendendo 10% ao ano, isso é 42% da renda.\n\n"
            "A conta não escolhe produto. Mede o encolhimento.",
    posts=[
        "Tanaka, sua renda mensal está encolhendo.\n\nDevagar, sem aparecer no extrato.\n\nA culpa é da inflação, e a "
        "conta assusta.",
        "Com 4,22% de inflação ao ano, mantida igual:\n\nR$ 1.000 de renda hoje compram cerca de R$ 661 depois de "
        "uma década.",
        "Manual pra renda encolher:\n\n→ gaste a renda inteira\n→ ignore a inflação\n→ repita por dez anos\n\n"
        "Funciona sem esforço.",
        "A regra de bolso: reinvista a parte da renda igual à inflação.\n\nRendendo 10% ao ano, com 4,22% de inflação: "
        "reinvista 42% e gaste o resto.\n\nA conta não escolhe produto. Mede o encolhimento.",
    ],
    numeros=list(N_EP5),
    risco=("baixo", "Dor no bolso (renda encolhendo) com conta em R$."),
)

C["2026-11-18|short"] = dict(
    titulo="R$ 100 mil, 10 anos: gastar a renda ou reinvestir?",
    estrutura="B", mecanica="extrato-falso",
    mensagem_capa="Em 10 anos, reinvestir a renda de R$ 100 mil quase dobra a renda mensal, no exemplo.",
    capa="R$ 100 mil: gastar a renda ou reinvestir?",
    slides=[
        "Exemplo: R$ 100 mil rendendo 0,6% ao mês, sem imposto e sem inflação.",
        "Extrato de quem gasta: R$ 600 por mês, por 10 anos. O capital segue em R$ 100 mil.",
        "Extrato de quem reinveste: cerca de R$ 205 mil em 10 anos. Renda de cerca de R$ 1.230 por mês.",
    ],
    legenda="Tanaka, R$ 100 mil, 10 anos: gastar a renda ou reinvestir?\n\n"
            "No exemplo, rendendo 0,6% ao mês, quem gasta recebe R$ 600 por mês e continua com R$ 100 mil. Quem "
            "reinveste chega a cerca de R$ 205 mil e passa a receber cerca de R$ 1.230.\n\n"
            "O episódio da série faz a conta ano a ano, com o meio-termo.",
    posts=[
        "Tanaka, R$ 100 mil: gastar ou reinvestir?\n\nA resposta muda a sua renda daqui a uma década.",
        "Extrato de quem gasta, no exemplo de 0,6% ao mês:\n\nR$ 600 por mês, por 10 anos.\n"
        "Capital no fim: os mesmos R$ 100 mil.",
        "Extrato de quem reinveste:\n\nCerca de R$ 205 mil em 10 anos.\nRenda nova: cerca de R$ 1.230 por mês.\n\n"
        "Quase o dobro, com o mesmo dinheiro inicial.",
    ],
    numeros=list(N_EP3),
    corte_de="2026-10-28",
    risco=("baixo", "Conta em R$ e contraste claro."),
)

C["2026-11-23|short"] = dict(
    titulo="R$ 1.000 de renda hoje compram quanto em 10 anos?",
    estrutura="C", mecanica="extrato-falso",
    mensagem_capa="Com a inflação de agora, R$ 1.000 de renda viram poder de compra de cerca de R$ 661 em 10 anos.",
    capa="Seus R$ 1.000 de renda vão encolher.",
    slides=[
        "Conta com 4,22% de inflação ao ano, mantida igual.",
        "Depois de uma década, R$ 1.000 compram o que hoje custa cerca de R$ 661.",
        "A saída: reinvestir a parte da renda igual à inflação. O episódio da série faz a conta.",
    ],
    legenda="Tanaka, R$ 1.000 de renda hoje compram quanto em 10 anos?\n\n"
            "Com 4,22% de inflação ao ano, mantida igual, cerca de R$ 661. A renda no extrato fica igual, e o poder de "
            "compra encolhe por fora dele.\n\n"
            "A saída é reinvestir a parte da renda igual à inflação. O episódio da série de renda mensal faz a conta inteira.",
    posts=[
        "Tanaka, seus R$ 1.000 de renda vão encolher.\n\nNo extrato, o número fica igual. No mercado, não.",
        "Extrato do poder de compra, com 4,22% de inflação ao ano:\n\nHoje: R$ 1.000.\n"
        "Daqui a uma década: o mesmo que R$ 661 hoje.",
        "A saída: reinvestir a parte da renda igual à inflação.\n\nO resto, você gasta sem culpa.",
    ],
    numeros=list(N_EP5),
    corte_de="2026-11-18",
    risco=("baixo", "Dor no bolso e uma conta só."),
)

C["2026-11-25|longo"] = dict(
    titulo="Renda todo mês com Tesouro e FII: a grade de 12 meses",
    estrutura="D", mecanica="boletim-escolar",
    mensagem_capa="Juntando Tesouro e fundos imobiliários numa grade de 12 meses, você vê quais meses ficam sem renda.",
    capa="Quais meses do ano ficam sem renda?",
    slides=[
        "A grade: 12 meses lado a lado e, em cada um, de onde vem a renda.",
        "Títulos do Tesouro com juros semestrais (pagos duas vezes por ano) enchem alguns meses. [CHECAR: meses de cada título]",
        "Fundos imobiliários (fundos que dividem aluguel): a frequência está no regulamento de cada um.",
        "Boletim da grade: mês cheio, mês vazio. A soma do ano é o que importa; a grade mostra quanto guardar.",
    ],
    legenda="Tanaka, renda mensal de verdade pede uma grade de 12 meses.\n\n"
            "Os títulos do Tesouro com juros semestrais (pagos duas vezes por ano) enchem alguns meses. Os fundos "
            "imobiliários preenchem outros, conforme o regulamento de cada um. A grade mostra, antes de investir, quais "
            "meses ficam vazios e quanto guardar dos meses cheios.\n\n"
            "É o fechamento da série de renda mensal.",
    posts=[
        "Tanaka, sua renda cai a cada mês mesmo?\n\nMonte a grade de 12 meses e confira.\n\n"
        "Os meses vazios aparecem na hora.",
        "Títulos do Tesouro com juros semestrais (pagos duas vezes por ano) pagam em meses fixos.\n\n"
        "[CHECAR: meses de pagamento de cada título no site do Tesouro Direto]\n\nSozinhos, eles deixam buracos no ano.",
        "Fundos imobiliários (fundos que dividem aluguel) entram nos buracos.\n\n"
        "A lei manda distribuir o lucro em base semestral. A frequência real está no regulamento de cada fundo.",
        "Exemplo de boletim da grade:\n\nJaneiro: presente.\nMarço: faltou.\nMaio: presente.\n\n"
        "O boletim é seu, e sai antes de investir.",
    ],
    numeros=[],
    risco=("médio", "Fechamento da série; as datas de pagamento do Tesouro ficam em [CHECAR] até o Mac conferir."),
)

C["2026-10-27|longo"] = dict(
    titulo="ETF de dividendos mensais ou FII: imposto e renda de cada um",
    estrutura="C", mecanica="contraste",
    mensagem_capa="ETF e fundo imobiliário pagam renda mensal com regras de imposto diferentes; o vídeo compara as duas.",
    capa="Renda mensal: qual imposto morde cada uma?",
    slides=[
        "Fundo imobiliário: o rendimento pode sair sem imposto de renda pra pessoa física, com as regras da lei.",
        "Uma das regras: o fundo ter 100 cotistas (donos de cotas) ou mais.",
        "ETF (fundo vendido na bolsa) de dividendos: regra de imposto própria. [CHECAR: alíquota e retenção na distribuição]",
        "Renda de fundo imobiliário vem de aluguel e juros de imóveis. A do ETF (fundo vendido na bolsa), do lucro de empresas.",
    ],
    legenda="Tanaka, ETF (fundo vendido na bolsa) de dividendos mensais ou fundo imobiliário? Os dois pagam renda mensal, "
            "com regras de imposto diferentes.\n\n"
            "No fundo imobiliário, o rendimento pode sair sem imposto de renda pra pessoa física, com as regras da lei. "
            "No ETF, a regra é outra, e o vídeo mostra onde ler. Sem indicar fundo nem ETF.\n\n"
            "Compare líquido com líquido.",
    posts=[
        "Tanaka, renda mensal: qual imposto morde cada uma?\n\nETF (fundo vendido na bolsa) e fundo imobiliário pagam "
        "com regras diferentes.",
        "Fundo imobiliário: o rendimento pode sair sem imposto de renda pra pessoa física.\n\n"
        "Uma das regras: o fundo ter 100 cotistas (donos de cotas) ou mais.",
        "ETF de dividendos (fundo vendido na bolsa): regra de imposto própria.\n\n"
        "[CHECAR: alíquota e retenção na distribuição do ETF de ações]\n\n"
        "Onde ler: regulamento, lâmina e aviso de rendimentos.",
        "Mesma renda bruta, impostos diferentes.\n\nComparar os dois pelo valor pago é escolher churrasco pela picanha "
        "do cartaz.",
    ],
    numeros=[arq("100", SERIE, "FII isento só com 100 cotistas ou mais")],
    risco=("médio", "Imposto do ETF ainda não conferido em fonte primária ([CHECAR]); o juiz pede a regra inteira."),
)


# ------------------------------------------------------------------ temas do vídeo (hashtags do Instagram)
# Chave: "AAAA-MM-DD|formato" (o v3 tem longo e Short no mesmo dia). Mapa de hashtags em gerar_cards.HASHTAGS_TEMA.
TEMAS_VIDEO = {
    "2026-10-05|short": ["renda fixa bancária"],
    "2026-10-06|longo": ["FII"],
    "2026-10-07|short": ["ETF"],
    "2026-10-08|longo": ["Tesouro"],
    "2026-10-12|short": ["renda fixa bancária"],
    "2026-10-13|longo": ["ações e dividendos"],
    "2026-10-14|longo": ["ETF"],
    "2026-10-14|short": ["Tesouro"],
    "2026-10-15|longo": ["crise"],
    "2026-10-19|short": ["IR", "FII"],
    "2026-10-20|longo": ["FII"],
    "2026-10-21|longo": ["ações e dividendos"],
    "2026-10-21|short": ["ações e dividendos"],
    "2026-10-22|longo": ["renda fixa bancária"],
    "2026-10-26|short": ["renda fixa bancária"],
    "2026-10-27|longo": ["ETF", "FII", "IR"],
    "2026-10-28|longo": ["ações e dividendos"],
    "2026-10-28|short": ["Tesouro"],
    "2026-10-29|longo": ["Tesouro"],
    "2026-11-02|short": ["IR", "ações e dividendos"],
    "2026-11-03|longo": ["Tesouro", "juros"],
    "2026-11-04|short": ["Tesouro", "juros"],
    "2026-11-05|longo": ["ações e dividendos", "FII", "Tesouro"],
    "2026-11-09|short": ["IR", "ações e dividendos"],
    "2026-11-10|longo": ["Tesouro"],
    "2026-11-11|longo": ["renda fixa bancária"],
    "2026-11-11|short": ["FII"],
    "2026-11-14|longo": ["renda fixa bancária"],
    "2026-11-16|short": ["renda fixa bancária"],
    "2026-11-17|longo": ["FII"],
    "2026-11-18|longo": ["inflação"],
    "2026-11-18|short": ["ações e dividendos"],
    "2026-11-19|longo": ["cripto"],
    "2026-11-23|short": ["inflação"],
    "2026-11-24|longo": ["juros", "ações e dividendos", "FII"],
    "2026-11-25|longo": ["Tesouro", "FII"],
    "2026-11-25|short": ["ETF"],
    "2026-11-26|longo": ["FII"],
}

# ------------------------------------------------------------------ afirmações factuais que não são número
# Ranking, "top 10", "3º melhor", origem de uma pergunta... Cada uma tem de estar escrita literalmente num arquivo do
# repo (caminho a partir da raiz do IPADTEST). O teste confere o trecho e que o `texto` aparece no post.
CAL_MD = "pautas-canal/CALENDARIO-8-SEMANAS.md"
RELATORIO = "auditoria-canal/RELATORIO.md"
AFIRMACOES = {
    "2026-10-20|longo": [
        {"texto": "lidera as buscas", "arquivo": "pautas-canal/CALENDARIO.csv",
         "trecho": "'trxf11' é o termo de investimento mais buscado do canal nos últimos 6 meses"},
        {"texto": "mais buscado do canal nos últimos 6 meses", "arquivo": "pautas-canal/CALENDARIO.csv",
         "trecho": "'trxf11' é o termo de investimento mais buscado do canal nos últimos 6 meses"},
        {"texto": "mais buscado no canal nos últimos 6 meses", "arquivo": "pautas-canal/CALENDARIO.csv",
         "trecho": "'trxf11' é o termo de investimento mais buscado do canal nos últimos 6 meses"},
    ],
    "2026-10-08|longo": [
        {"texto": "está no top 10 do ano do canal", "arquivo": RELATORIO, "trecho": "Dois dos top 10 (421 e 246)"},
        {"texto": "está no top 10 do ano do canal", "arquivo": CAL_MD, "trecho": "tesouro: dHYQtxnMSrw"},
    ],
    "2026-10-15|longo": [
        {"texto": "foi o 3º melhor do canal no ano", "arquivo": CAL_MD, "trecho": "continuação do 3º melhor vídeo do ano"},
    ],
    "2026-11-14|longo": [
        {"texto": "rendeu um vídeo aqui em 2018", "arquivo": "pautas-canal/CALENDARIO.csv",
         "trecho": "7CdwOTT7U3o (CDB prefixado, 2018"},
    ],
    "2026-11-19|longo": [
        {"texto": "apareceu nos comentários", "arquivo": "pautas-canal/PERGUNTAS-SEM-RESPOSTA.md",
         "trecho": "Eu ficaria devendo se perdesse o valor investido?"},
    ],
}
