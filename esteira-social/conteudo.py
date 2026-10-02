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

Chave: data do vídeo (AAAA-MM-DD). `titulo` tem de bater com o calendário (o gerador confere).
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

# ------------------------------------------------------------------ semana 05/10
C["2026-10-05"] = dict(
    titulo="LCI e LCA ou CDB: qual rende mais depois do imposto?",
    estrutura="D", mecanica="tradutor-juramentado",
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

C["2026-10-06"] = dict(
    titulo="ETFs que pagam dividendos mensais: o que mudou em 2026",
    estrutura="E", mecanica="mito-x-fato",
    mensagem_capa="O vídeo confere se os fundos que pagam renda mensal entregaram o que prometiam.",
    capa="A renda de cada mês veio igual?",
    slides=[
        "Em 2025, o canal fez uma lista de ETFs (fundos vendidos na bolsa) que pagam renda mensal.",
        "Agora, a prestação de contas: quanto cada um pagou de verdade, mês a mês.",
        "E quanto cada um cobra de taxa por ano, antes de o dinheiro chegar em você.",
        "A data do pagamento é previsível. O valor, não: ele sobe e desce com o mercado.",
    ],
    legenda="Tanaka, a lista de 2025 fez aniversário.\n\n"
            "O vídeo dos ETFs (fundos vendidos na bolsa) que pagam renda mensal entrou no top 10 do ano do canal. "
            "Agora vem a parte que pouca gente grava: conferir quanto cada um pagou de verdade, quanto cobra de taxa "
            "e se cresceu ou encolheu.\n\n"
            "Renda mensal tem data. O valor, quem escolhe é o mercado.",
    posts=[
        "Tanaka, a lista de renda mensal fez aniversário.\n\nEram ETFs (fundos vendidos na bolsa) que pagam a cada "
        "mês.\n\nAgora vem a parte que pouca gente grava: conferir se pagaram o que prometiam.",
        "Mito: um ETF (fundo vendido na bolsa) de renda mensal paga um salário.\n\n"
        "Fato: paga a cada mês, mas o valor muda de um mês pro outro.\n\nA data é previsível. O valor, não.",
        "O que o vídeo confere, ETF por ETF (fundo vendido na bolsa):\n\n→ quanto pagou de verdade, mês a mês\n"
        "→ quanto cobra de taxa\n→ se o fundo cresceu ou encolheu",
        "Esse vídeo entrou no top 10 do ano do canal.\n\nPrometer renda dá audiência. Conferir dá trabalho.\n\n"
        "Por isso a gente conferiu.",
    ],
    numeros=[],
    risco=("baixo", "Continuação de top 10, com bolso (renda mensal). Risco: carrossel mais explica que reage."),
)

C["2026-10-07"] = dict(
    titulo="Como juntar 1 milhão de reais com R$ 1.000 por mês",
    estrutura="A", mecanica="extrato-falso",
    mensagem_capa="Guardar R$ 1.000 por mês leva bem mais tempo do que prometem pra virar um milhão.",
    capa="Quanto tempo leva pra juntar um milhão?",
    slides=[
        "Guardando R$ 1.000 por mês, sem render nada: R$ 264 mil em 22 anos.",
        "Rendendo 6% ao ano acima da inflação: cerca de R$ 535 mil no mesmo prazo, em dinheiro de hoje.",
        "O milhão, com o poder de compra de hoje, chega perto dos 30 anos.",
    ],
    legenda="Tanaka, R$ 1.000 por mês vira um milhão. Mas não no prazo que a internet promete.\n\n"
            "Guardando sem render, são R$ 264 mil em 22 anos. Rendendo 6% ao ano acima da inflação, cerca de "
            "R$ 535 mil, já em dinheiro de hoje. O milhão com poder de compra chega perto dos 30 anos.\n\n"
            "Não é mágica. É tempo.",
    posts=[
        "Tanaka, R$ 1.000 por mês vira um milhão.\n\nMas não no prazo que a internet promete.\n\n"
        "A conta honesta tem um detalhe que o vídeo viral pula.",
        "Extrato de quem guarda R$ 1.000 por mês, sem render nada, por 22 anos:\n\nR$ 264 mil.\n\n"
        "Esforço enorme. Milhão longe.",
        "Rendendo 6% ao ano acima da inflação, a mesma pessoa chega a cerca de R$ 535 mil, em dinheiro de hoje.\n\n"
        "O milhão de verdade: perto dos 30 anos.\n\nQuem promete milhão rápido está contando em real de mentira.",
    ],
    numeros=[
        arq("264", PERG, "Guardando R$ 1.000 por mês sem render nada, são R$ 264 mil em 22 anos."),
        conta("264", "1000 * 12 * 22 / 1000", "R$ 1.000 por mês, 12 meses, 22 anos (CALENDARIO 07/10)"),
    ],
    risco=("alto", "Pauta de finança pessoal básica (juntar dinheiro), que o juiz-post lista como eliminatório."),
)

C["2026-10-08"] = dict(
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

# ------------------------------------------------------------------ semana 12/10
C["2026-10-12"] = dict(
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

C["2026-10-13"] = dict(
    titulo="Dividendos mensais com ações: como montar um calendário",
    estrutura="D", mecanica="eco-do-gatilho (cair)",
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

C["2026-10-14"] = dict(
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

C["2026-10-15"] = dict(
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

# ------------------------------------------------------------------ semana 19/10
C["2026-10-19"] = dict(
    titulo="FII é isento de imposto? Só se cumprir estas 3 regras",
    estrutura="D", mecanica="pergunta-do-leitor",
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

C["2026-10-20"] = dict(
    titulo="ETF de dividendos mensais com opções: de onde vem a renda",
    estrutura="C", mecanica="tradutor-juramentado",
    mensagem_capa="Esses fundos pagam renda alta porque vendem uma parte da alta futura das ações.",
    capa="A renda alta desse fundo tem um preço.",
    slides=[
        "Esses ETFs (fundos vendidos na bolsa) vendem opções de compra (o direito de alguém comprar as ações deles "
        "por um preço combinado).",
        "O que eles recebem por isso vira a renda do mês.",
        "Mercado de lado: a renda brilha. Mercado subindo forte: o fundo fica com uma parte da alta.",
        "É alugar a vaga de garagem no dia da final: entra dinheiro, mas a vaga já está alugada pelo preço combinado.",
    ],
    legenda="Tanaka, tem ETF (fundo vendido na bolsa) que paga renda alta a cada mês. O dinheiro vem, em boa "
            "parte, de vender opções de compra (o direito de alguém comprar as ações do fundo por um preço "
            "combinado).\n\n"
            "É como alugar a vaga de garagem no dia do jogo: entra dinheiro, mas no dia da final a vaga já está "
            "alugada pelo preço combinado.",
    posts=[
        "Tanaka, esse fundo paga renda alta mensal.\n\nÉ um ETF (fundo vendido na bolsa), e o dinheiro não vem de "
        "mágica.\n\nVem de vender uma coisa que você nem sabia que tinha.",
        "Ele vende opções de compra.\n\nTradução: aluga pra alguém o direito de comprar as ações do fundo por um "
        "preço combinado.\n\nO aluguel vira a sua renda do mês.",
        "É como alugar a sua vaga de garagem no dia do jogo.\n\nEntra dinheiro a cada domingo.\n\n"
        "Mas no dia da final, quando a vaga vale ouro, ela já está alugada pelo preço combinado.",
        "ETF de dividendos comum (fundo vendido na bolsa) divide o lucro das empresas.\n\n"
        "O de opções vende o seu ingresso pra final.\n\nRenda alta tem preço. Ele não aparece no extrato do mês.",
    ],
    numeros=[],
    risco=("médio", "Mecanismo de opções é difícil pro leitor leigo; a analogia da garagem carrega a clareza."),
)

C["2026-10-21"] = dict(
    titulo="Casal que investe junto: a conversa que vem antes do dinheiro",
    estrutura="B", mecanica="manual-invertido",
    mensagem_capa="Antes de investir a dois, o casal combina pra que serve o dinheiro e pra quando.",
    capa="Casal: a conversa que vem antes do dinheiro.",
    slides=[
        "Antes da taxa do CDB, o casal combina pra que serve o dinheiro.",
        "A pergunta: esse dinheiro é pra quê, e pra quando?",
        "Viagem daqui a dois anos e aposentadoria daqui a trinta não cabem na mesma aplicação.",
    ],
    legenda="Tanaka, antes da taxa do CDB, o casal precisa combinar uma coisa: pra que serve o dinheiro.\n\n"
            "A pergunta vem antes do produto: esse dinheiro é pra quê, e pra quando? Viagem, casa, reserva e "
            "aposentadoria têm prazos diferentes.\n\n"
            "Igual pizza: primeiro o sabor, depois a fatia.",
    posts=[
        "Tanaka, casal que investe junto combina antes.\n\nAntes da taxa do CDB, vem uma pergunta: pra que serve "
        "esse dinheiro?",
        "Manual pra brigar por dinheiro a dois:\n\n→ abram conta conjunta sem conversar\n"
        "→ cada um investe pensando num sonho diferente\n→ descubram na hora do saque",
        "A conversa: \"esse dinheiro é pra quê, e pra quando?\"\n\n"
        "Viagem daqui a dois anos e aposentadoria daqui a trinta não cabem na mesma aplicação.\n\n"
        "Igual pizza: primeiro o sabor, depois a fatia.",
    ],
    numeros=[],
    risco=("alto", "Pauta de finança pessoal básica (comportamento): eliminatório do juiz-post. Texto não salva."),
)

C["2026-10-22"] = dict(
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

# ------------------------------------------------------------------ semana 26/10
C["2026-10-26"] = dict(
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

C["2026-10-27"] = dict(
    titulo="ETF de dividendos mensais ou fundo imobiliário: o que sobra",
    estrutura="C", mecanica="contraste",
    mensagem_capa="Pra comparar dois tipos de fundo de renda mensal, o que importa é o que sobra depois de taxa e imposto.",
    capa="Renda mensal: compare o que sobra, não o que paga.",
    slides=[
        "Fundo imobiliário: a renda vem de aluguel e de juros de dívida de imóveis.",
        "ETF de dividendos (fundo vendido na bolsa): a renda vem do lucro de várias empresas.",
        "Imposto em 2026: o rendimento do fundo imobiliário pode sair sem imposto, com regras. O ETF (fundo vendido "
        "na bolsa) segue regra própria.",
        "Picanha do cartaz não é a do prato. O que importa é quanto sobra depois da taxa e do imposto.",
    ],
    legenda="Tanaka, ETF (fundo vendido na bolsa) ou fundo imobiliário pra renda mensal? Pouca gente compara o "
            "que sobra.\n\n"
            "O vídeo compara como cada um paga, o imposto de cada um em 2026 e quanto a renda balança de um mês pro "
            "outro. Sem indicar fundo nem ETF.\n\n"
            "Picanha do cartaz não é a do prato.",
    posts=[
        "Tanaka, renda mensal: qual fundo deixa mais?\n\nETF (fundo vendido na bolsa) ou fundo imobiliário?\n\n"
        "A comparação comum olha quanto paga. A que importa olha quanto sobra.",
        "Fundo imobiliário: renda de aluguel e de juros de dívida de imóveis. Pode sair sem imposto de renda, se o "
        "fundo cumprir as regras.\n\nETF de dividendos (fundo vendido na bolsa): renda do lucro de empresas. "
        "Regra de imposto própria.",
        "E tem a balança.\n\nAluguel oscila por um motivo. Lucro de empresa, por outro.\n\n"
        "Mesma renda bruta, sobras diferentes.",
        "Comparar os dois pelo valor pago é escolher churrasco pela picanha do cartaz.\n\n"
        "O que importa é o que sobra no prato.",
    ],
    numeros=[],
    risco=("médio", "Comparação boa pra quem já tem renda; o carrossel explica mais que reage."),
)

C["2026-10-28"] = dict(
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

C["2026-10-29"] = dict(
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

C["2026-10-31"] = dict(
    titulo="TRXF11: o que aconteceu com a renda desde agosto",
    estrutura="B", mecanica="mito-x-fato",
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
    risco=("baixo", "Nome que o público busca + bolso de quem tem cota. Neutro, sem recomendação."),
)

# ------------------------------------------------------------------ semana 02/11
C["2026-11-02"] = dict(
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

C["2026-11-03"] = dict(
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

C["2026-11-04"] = dict(
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

C["2026-11-05"] = dict(
    titulo="Tesouro Direto após o Copom: o que muda no IPCA+ e prefixado",
    estrutura="E", mecanica="atendimento-ao-cliente",
    mensagem_capa="Depois da decisão dos juros, o preço dos títulos do Tesouro mexeu; o contrato de quem leva até o fim, não.",
    capa="Os juros foram decididos ontem. E o seu Tesouro?",
    slides=[
        "Decisão do Copom (a reunião que decide os juros) de 04/11: [CHECAR: Selic decidida].",
        "Antes: as taxas do Tesouro na véspera. Depois: as mesmas taxas 24 h após o anúncio.",
        "O que mexe o preço é a surpresa: a diferença entre o esperado e o decidido.",
        "O contrato do seu título não muda. Muda o preço pra quem quer sair antes.",
    ],
    legenda="Tanaka, o Copom (a reunião que decide os juros) decidiu ontem, e o Tesouro sentiu antes de você abrir "
            "o app.\n\n"
            "O vídeo compara as taxas do Tesouro na véspera com as de 24 h depois do anúncio. O que mexe o preço é a "
            "diferença entre o esperado e o decidido.\n\n"
            "Pra quem leva o título até o fim, o contrato não muda.",
    posts=[
        "Tanaka, os juros foram decididos ontem.\n\nOs juros básicos foram pra [CHECAR: decisão do Copom de 04/11].\n\n"
        "O seu Tesouro sentiu antes de você abrir o app.",
        "Antes: as taxas do Tesouro na véspera.\n\nDepois: as mesmas taxas 24 h após o anúncio.\n\n"
        "O vídeo põe uma do lado da outra.",
        "— Meu título de taxa travada subiu. Ganhei?\n— Se vender hoje, ganhou no preço.\n— E se não vender?\n"
        "— Recebe a taxa que contratou. O resto é paisagem.",
        "A decisão dos juros não muda o contrato do seu título.\n\nMuda o preço pra quem quer sair antes.\n\n"
        "A pergunta que importa é quando você vai precisar desse dinheiro.",
    ],
    numeros=[],
    evento_ao_vivo="Texto escrito para depois da decisão de 04/11: conferir o verbo e preencher o [CHECAR] com o "
                   "comunicado (bcb.gov.br) antes de aprovar.",
    risco=("médio", "Evento ao vivo com [CHECAR] no texto; o print do comunicado precisa ser do dia."),
)

C["2026-11-07"] = dict(
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

# ------------------------------------------------------------------ semana 09/11
C["2026-11-09"] = dict(
    titulo="Imposto sobre dividendos acima de R$ 50 mil por mês: quem paga",
    estrutura="D", mecanica="mito-x-fato",
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

C["2026-11-10"] = dict(
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

C["2026-11-11"] = dict(
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
    risco=("baixo", "Dilema que o Tanaka vive (imóvel x fundo) com R$ na capa."),
)

C["2026-11-12"] = dict(
    titulo="Fundo imobiliário ou imóvel alugado: a conta de 2026",
    estrutura="C", mecanica="eco-do-gatilho (escondido)",
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

C["2026-11-14"] = dict(
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

# ------------------------------------------------------------------ semana 16/11
C["2026-11-16"] = dict(
    titulo="Perfil de investidor: 3 perguntas antes de investir",
    estrutura="B", mecanica="manual-invertido",
    mensagem_capa="Antes de investir, três perguntas: prazo, objetivo e o que você faz se cair.",
    capa="3 perguntas antes de investir.",
    slides=[
        "Prazo: quando vou precisar desse dinheiro?",
        "Objetivo: pra que ele serve?",
        "Queda: se cair bastante, eu vendo ou espero?",
    ],
    legenda="Tanaka, o questionário do banco é longo. As perguntas que importam são 3.\n\n"
            "Prazo: quando você vai precisar do dinheiro. Objetivo: pra que ele serve. Queda: se cair, você vende ou "
            "espera.\n\n"
            "É fácil marcar \"arrojado\" no formulário. Difícil é manter na primeira queda.",
    posts=[
        "Tanaka, o questionário do banco é longo.\n\nAs perguntas que importam são 3.\n\n"
        "E você responde com mais calma sozinho do que clicando \"concordo\".",
        "Manual de como errar o próprio perfil:\n\n→ responda rápido pra liberar o app\n"
        "→ marque \"arrojado\" porque soa bonito\n→ conheça o perfil de verdade na primeira queda",
        "As 3 perguntas:\n\n→ prazo: quando vou precisar desse dinheiro?\n→ objetivo: pra que ele serve?\n"
        "→ queda: se cair bastante, eu vendo ou espero?\n\nA terceira tem resposta honesta depois que acontece.",
    ],
    numeros=[],
    risco=("alto", "Pauta de finança pessoal básica (perfil de investidor): eliminatório do juiz-post."),
)

C["2026-11-17"] = dict(
    titulo="ETF de dividendos mensais: quanto a taxa tira da renda",
    estrutura="C", mecanica="elogio-envenenado",
    mensagem_capa="Uma taxa de 1,5% ao ano tira cerca de 14% do patrimônio em 10 anos.",
    capa="Taxa de 1,5% ao ano é alta?",
    slides=[
        "A taxa de administração (o que o gestor cobra por ano) sai do patrimônio do fundo, a cada dia, sem boleto.",
        "Em 10 anos, uma taxa de 0,5% ao ano come cerca de 5% do patrimônio.",
        "Em 10 anos, uma taxa de 1,5% ao ano come cerca de 14%.",
        "Taxa alta precisa explicar, a cada ano, o que entrega a mais.",
    ],
    legenda="Tanaka, \"essa taxa de 1,50 é alta?\" A pergunta é essa.\n\n"
            "A taxa de administração (o que o gestor cobra por ano) sai do patrimônio do ETF (fundo vendido na "
            "bolsa), um pouco a cada dia. Na conta simples, 0,5% ao ano come cerca de 5% do patrimônio em 10 anos. "
            "A de 1,5% come cerca de 14%.\n\n"
            "Taxa alta precisa se explicar a cada ano.",
    posts=[
        "Tanaka, taxa de 1,5% ao ano é alta?\n\nNum ETF (fundo vendido na bolsa), a resposta cabe numa conta.",
        "A taxa de administração (o que o gestor cobra) sai do patrimônio do fundo, um pouco a cada dia.\n\n"
        "Você não vê o débito.\n\nVê a renda um pouco menor do que poderia ser.",
        "Em 10 anos, uma taxa de 0,5% ao ano come cerca de 5% do patrimônio.\n\nParece pouco. Guarda esse número.",
        "Agora a de 1,5% ao ano, nos mesmos 10 anos: cerca de 14% do patrimônio.\n\n"
        "Um ponto de taxa vira quase o triplo de mordida.",
        "Justiça seja feita ao gestor: ele cobra a cada dia, sem falhar.\n\nNem nos meses em que o fundo pagou menos.\n\n"
        "Disciplina que muito investidor queria ter com o próprio aporte.",
    ],
    numeros=list(N_TAXA_ETF),
    risco=("baixo", "Conta em % com frase que fica ('quase o triplo de mordida')."),
)

C["2026-11-18"] = dict(
    titulo="Juros compostos: por que 1 centavo dobrando todo dia não existe",
    estrutura="B", mecanica="pergunta-do-leitor",
    mensagem_capa="A conta do centavo que dobra é real, mas investimento que dobra a cada dia não existe.",
    capa="1 centavo dobrando vira milionário?",
    slides=[
        "Em 30 dobras, 1 centavo vira R$ 10,7 milhões.",
        "A conta está certa. O investimento que dobra a cada dia é que não existe.",
        "Vida real: R$ 1.000 por mês, rendendo 6% ao ano acima da inflação.",
        "Em 22 anos, isso dá cerca de R$ 535 mil. Menos espetacular. Mais possível.",
    ],
    legenda="Tanaka, 1 centavo dobrando 30 vezes vira R$ 10,7 milhões. A conta é real. O investimento que dobra a "
            "cada dia é que não existe.\n\n"
            "Na vida real, a curva é a mesma, mas em anos: R$ 1.000 por mês a 6% ao ano acima da inflação somam "
            "cerca de R$ 535 mil em 22 anos.\n\n"
            "Menos espetacular. Mais possível.",
    posts=[
        "Tanaka, 1 centavo dobrando vira milionário?\n\nA conta está certa.\n\nO investimento é que não existe.",
        "\"Onde eu acho algo que dobra a cada dia?\"\n\nNão acha.\n\n"
        "Em 30 dobras, o centavo vira R$ 10,7 milhões. A conta mostra a curva. A vida real anda na mesma curva, mas em anos.",
        "Na vida real: R$ 1.000 por mês, a 6% ao ano acima da inflação, dá cerca de R$ 535 mil em 22 anos.\n\n"
        "Não é milhão em um mês.\n\nMas existe. O do centavo, não.",
    ],
    numeros=[
        arq("1", PERG, "1 centavo dobrando 30 vezes"),
        arq("30", PERG, "1 centavo dobrando 30 vezes"),
        arq("10,7", PERG, "R$ 10,7 milhões"),
        conta("10,7", "0.01 * 2 ** 30 / 1e6", "1 centavo e 30 dobras (PERGUNTAS-SEM-RESPOSTA.md)"),
    ] + list(N_JUNTAR),
    risco=("alto", "Pauta de finança pessoal básica (juros compostos); a conta é mandável, mas o tema pode cair no item 1."),
)

C["2026-11-19"] = dict(
    titulo="Bitcoin depois do 'alerta': o que mudou desde fevereiro",
    estrutura="E", mecanica="necrologio",
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

C["2026-11-21"] = dict(
    titulo="Bolha da IA: o que dizem os números",
    estrutura="B", mecanica="boletim-escolar",
    mensagem_capa="O vídeo mostra se o preço das empresas de inteligência artificial anda junto com o lucro delas.",
    capa="Bolha da inteligência artificial? Olha o lucro.",
    slides=[
        "Bolha não é opinião. Deixa rastro nos números.",
        "Lucro: as empresas de inteligência artificial estão ganhando mais?",
        "Gasto: quanto estão investindo pra construir a tecnologia?",
        "Preço: o mercado paga quanto por cada real de lucro? Data do estouro, o vídeo não chuta.",
    ],
    legenda="Tanaka, a turma grita \"bolha da inteligência artificial\". Pouca gente mostra a conta.\n\n"
            "O vídeo olha três números dessas empresas: lucro, quanto estão gastando pra construir a tecnologia e "
            "quanto o mercado paga por cada real de lucro. Quando o preço corre na frente do lucro por muito tempo, o "
            "mercado está pagando por esperança.",
    posts=[
        "Tanaka, a turma grita \"bolha da inteligência artificial\".\n\nPouca gente mostra a conta.\n\n"
        "Bolha não é opinião. Deixa rastro nos números.",
        "A pergunta errada: \"quando estoura?\"\n\nQuem diz que sabe está vendendo curso.\n\n"
        "A pergunta certa: o preço dessas empresas anda junto com o lucro delas, ou na frente?",
        "Três números pra olhar:\n\n→ lucro: as empresas estão ganhando mais?\n"
        "→ gasto: quanto investem pra construir a tecnologia?\n→ preço: quanto o mercado paga por cada real de lucro?",
        "Boletim da inteligência artificial:\n\nLucro: o vídeo mostra.\nGasto: o vídeo mostra.\nPreço: o vídeo mostra.\n"
        "Data do estouro: a turma inteira ficou de recuperação.",
    ],
    numeros=[],
    risco=("alto", "Tema gringo sem ponte com o bolso brasileiro (item 1 e eliminatório de 'nome ou dor no bolso')."),
)

# ------------------------------------------------------------------ semana 23/11
C["2026-11-23"] = dict(
    titulo="Reserva de emergência: onde deixar e onde não deixar",
    estrutura="A", mecanica="manual-invertido",
    mensagem_capa="Reserva de emergência fica onde dá pra sacar rápido, sem perder e rendendo.",
    capa="Reserva de emergência: onde deixar.",
    slides=[
        "Deixar: aplicação com liquidez diária (dá pra sacar no mesmo dia), perto de 100% do CDI (a taxa de "
        "referência dos CDBs).",
        "E com a garantia do FGC (devolve o dinheiro se o banco quebrar), dentro do limite.",
        "Não deixar: aplicação com dinheiro preso, ação, ou conta parada sem render.",
    ],
    legenda="Tanaka, reserva de emergência não é investimento. É extintor.\n\n"
            "Precisa estar perto: aplicação com liquidez diária (dá pra sacar no mesmo dia), rendendo perto de 100% "
            "do CDI (a taxa de referência dos CDBs) e com a garantia do FGC (contra quebra do banco). Longe dela: "
            "dinheiro preso, ação e conta parada.",
    posts=[
        "Tanaka, reserva de emergência não é investimento.\n\nÉ extintor.\n\nE extintor trancado no cofre não apaga incêndio.",
        "Onde deixar: aplicação com liquidez diária (dá pra sacar no mesmo dia).\n\n"
        "Rendendo perto de 100% do CDI (a taxa de referência dos CDBs), com a garantia do FGC (contra quebra de banco).",
        "Manual pra reserva que não serve na hora:\n\n→ coloque em aplicação com dinheiro preso\n→ ou em ação, que oscila\n"
        "→ ou deixe parada na conta, sem render\n\nExtintor tem que estar perto, cheio e funcionando.",
    ],
    numeros=[],
    risco=("alto", "Pauta de finança pessoal básica (reserva de emergência): eliminatório do juiz-post."),
)

C["2026-11-24"] = dict(
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

C["2026-11-25"] = dict(
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
    corte_de="2026-11-17",
    risco=("baixo", "Conta em R$ mandável ('quase o triplo de mordida')."),
)

C["2026-11-26"] = dict(
    titulo="Fundos imobiliários caíram em 2026: e a renda deles?",
    estrutura="D", mecanica="contraste",
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

C["2026-11-28"] = dict(
    titulo="Tesouro Direto na reserva de emergência: Selic, CDB ou conta",
    estrutura="C", mecanica="atendimento-ao-cliente",
    mensagem_capa="Pra reserva de emergência, o vídeo compara Tesouro Selic, CDB de saque diário e conta remunerada.",
    capa="Sua reserva está parada na conta?",
    slides=[
        "Conta corrente parada: dinheiro seguro e perdendo pra inflação.",
        "Tesouro Selic (título que segue os juros básicos): garantia do Tesouro Nacional.",
        "CDB de liquidez diária (saque no mesmo dia): garantia do FGC (contra quebra do banco), dentro do limite.",
        "Conta remunerada: rende o que o banco decidir pagar. Reserva boa é chata.",
    ],
    legenda="Tanaka, sua reserva está na conta corrente? Está segura. E perdendo pra inflação.\n\n"
            "O vídeo faz a conta de três lugares: Tesouro Selic (título que segue os juros básicos), CDB de liquidez "
            "diária (saque no mesmo dia) e conta remunerada. Com imposto, prazo de saque e garantia. Sem indicar "
            "banco nem corretora.\n\n"
            "Reserva boa é chata. Não dá assunto no churrasco.",
    posts=[
        "Tanaka, sua reserva está na conta corrente?\n\nEla está segura.\n\nE perdendo pra inflação a cada dia.",
        "Três candidatos pra guardar a reserva:\n\n→ Tesouro Selic (título que segue os juros básicos)\n"
        "→ CDB com saque no mesmo dia\n→ conta remunerada\n\n"
        "O vídeo faz a conta do que sobra em cada um, com imposto e prazo de saque.",
        "— Qual dos três rende mais?\n— Depende da taxa de cada um, no dia.\n— E qual é o mais seguro?\n"
        "— Os três servem pra reserva. Arriscado é deixar parada na conta sem render.",
        "Reserva boa é chata.\n\nNão sobe, não cai, não dá assunto no churrasco.\n\nSe a sua dá assunto, ela não é reserva.",
    ],
    numeros=[],
    risco=("alto", "Pauta de reserva de emergência (finança pessoal básica): eliminatório do juiz-post."),
)


# ------------------------------------------------------------------ temas do vídeo (hashtags do Instagram)
# Cada vídeo leva só as hashtags dos seus temas (mapa em gerar_cards.HASHTAGS_TEMA) e as gerais da marca.
TEMAS_VIDEO = {
    "2026-10-05": ["renda fixa bancária"],
    "2026-10-06": ["ETF"],
    "2026-10-07": ["juntar dinheiro"],
    "2026-10-08": ["Tesouro"],
    "2026-10-12": ["renda fixa bancária"],
    "2026-10-13": ["ações e dividendos"],
    "2026-10-14": ["Tesouro"],
    "2026-10-15": ["crise"],
    "2026-10-19": ["IR", "FII"],
    "2026-10-20": ["ETF"],
    "2026-10-21": ["comportamento"],
    "2026-10-22": ["renda fixa bancária"],
    "2026-10-26": ["renda fixa bancária"],
    "2026-10-27": ["ETF", "FII"],
    "2026-10-28": ["Tesouro"],
    "2026-10-29": ["Tesouro"],
    "2026-10-31": ["FII"],
    "2026-11-02": ["IR", "ações e dividendos"],
    "2026-11-03": ["ações e dividendos", "FII", "Tesouro"],
    "2026-11-04": ["Tesouro", "juros"],
    "2026-11-05": ["Tesouro", "juros"],
    "2026-11-07": ["FII"],
    "2026-11-09": ["IR", "ações e dividendos"],
    "2026-11-10": ["Tesouro"],
    "2026-11-11": ["FII"],
    "2026-11-12": ["FII"],
    "2026-11-14": ["renda fixa bancária"],
    "2026-11-16": ["comportamento"],
    "2026-11-17": ["ETF"],
    "2026-11-18": ["juntar dinheiro"],
    "2026-11-19": ["cripto"],
    "2026-11-21": ["IA"],
    "2026-11-23": ["renda fixa bancária"],
    "2026-11-24": ["juros", "ações e dividendos", "FII"],
    "2026-11-25": ["ETF"],
    "2026-11-26": ["FII"],
    "2026-11-28": ["Tesouro", "renda fixa bancária"],
}

# ------------------------------------------------------------------ afirmações factuais que não são número
# Ranking, "mais buscado", "top 10", "3º melhor", origem de uma pergunta... Cada uma tem de estar escrita
# literalmente num arquivo do repo (caminho a partir da raiz do IPADTEST). O teste confere o trecho e que o
# `texto` aparece no post.
CAL_MD = "pautas-canal/CALENDARIO-8-SEMANAS.md"
CAL_CSV = "pautas-canal/CALENDARIO-8-SEMANAS.csv"
RELATORIO = "auditoria-canal/RELATORIO.md"
AFIRMACOES = {
    "2026-10-06": [
        {"texto": "entrou no top 10 do ano do canal", "arquivo": CAL_MD,
         "trecho": "renda mensal: Fb0l4KEq27o, TY8oLvUt2Qg e IB1mBcF00jc"},
        {"texto": "entrou no top 10 do ano do canal", "arquivo": RELATORIO,
         "trecho": "Dos 5 maiores do ano, 2 são dessa linha (637 e 324 inscritos)"},
    ],
    "2026-10-08": [
        {"texto": "está no top 10 do ano do canal", "arquivo": RELATORIO, "trecho": "Dois dos top 10 (421 e 246)"},
        {"texto": "está no top 10 do ano do canal", "arquivo": CAL_MD, "trecho": "tesouro: dHYQtxnMSrw"},
    ],
    "2026-10-15": [
        {"texto": "foi o 3º melhor do canal no ano", "arquivo": CAL_MD,
         "trecho": "continuação do 3º melhor vídeo do ano"},
    ],
    "2026-10-31": [
        {"texto": "lidera as buscas", "arquivo": CAL_CSV,
         "trecho": "'trxf11' é o termo de investimento mais buscado do canal nos últimos 6 meses"},
        {"texto": "mais buscado do canal nos últimos 6 meses", "arquivo": CAL_CSV,
         "trecho": "'trxf11' é o termo de investimento mais buscado do canal nos últimos 6 meses"},
        {"texto": "mais buscado no canal nos últimos 6 meses", "arquivo": CAL_CSV,
         "trecho": "'trxf11' é o termo de investimento mais buscado do canal nos últimos 6 meses"},
    ],
    "2026-11-14": [
        {"texto": "rendeu um vídeo aqui em 2018", "arquivo": CAL_CSV, "trecho": "7CdwOTT7U3o (CDB prefixado, 2018"},
    ],
    "2026-11-19": [
        {"texto": "apareceu nos comentários", "arquivo": "pautas-canal/PERGUNTAS-SEM-RESPOSTA.md",
         "trecho": "Eu ficaria devendo se perdesse o valor investido?"},
    ],
}
