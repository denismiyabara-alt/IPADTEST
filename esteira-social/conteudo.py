"""Texto dos cards da esteira social (X e Instagram), um bloco por vídeo do calendário v2.

Escrito à mão, na voz do Denis ("Tanaka,"; frases curtas; humor de contraste), seguindo:
- .claude/scheduled-tasks/ic-copywriter/SKILL.md (formato do card e checklist);
- vault/Pipeline/X-COPYWRITER-BRIEF.md (5 estruturas A-E em rotação, sem CTA/hashtag/emoji/link no corpo,
  link numa reply depois do último tweet, [CHECAR: ...] para número que não veio do briefing);
- vault/Pipeline/IG-COPYWRITER-BRIEF.md (SETUP -> TENSÃO -> PUNCH, 200-500 caracteres, hashtags no fim);
- vault/Pipeline/MECANICAS-DE-PIADA.md (mecânica registrada no card, sem repetir a da thread anterior);
- memory/feedback_copywriter_sem_fonte_sem_disclaimer.md (sem fonte e sem "não é recomendação" no corpo:
  a fonte de cada número fica no campo `numeros`, que é para o juiz-post e o Denis, e não vai no post).

Regra dos números: todo número do texto tem de estar na própria linha do calendário (qualquer coluna) ou
declarado em `numeros`, com o trecho literal do arquivo de origem (pautas-canal/) ou com a conta que o gera.
Os testes conferem as duas coisas. Número que depende do dia da gravação fica como [CHECAR: ...].

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


# Números de outras linhas do calendário que mais de um card usa
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
    x=dict(
        estrutura="D", mecanica="tradutor-juramentado",
        tweets=[
            "Tanaka, LCI paga menos que CDB.\n\nE mesmo assim pode render mais.\n\nNão é mágica. É imposto.",
            "A pergunta errada: \"qual paga a maior taxa?\"\n\nA certa: \"quanto sobra depois do leão?\"\n\n"
            "LCI e LCA são isentas de IR pra pessoa física. O CDB paga, e a mordida depende do prazo.",
            "O anúncio: \"CDB que paga mais\".\n\nTradução: paga mais antes do leão.\n\n"
            "Pra comparar de verdade, calcula quanto o CDB precisaria pagar, já com o IR do prazo, pra empatar com a LCI. "
            "Abaixo disso, a taxa maior perde.",
        ],
        imagem="Print genérico de vitrine de banco com duas taxas lado a lado, a maior riscada pelo leão do IR.",
    ),
    ig=dict(
        slides=[
            "LCI ou CDB? A taxa maior pode perder.",
            "LCI e LCA: isentas de IR pra pessoa física.",
            "CDB: paga IR, e a alíquota cai com o prazo.",
            "Compare o que sobra, não a taxa do anúncio.",
        ],
        legenda="LCI e LCA ou CDB: qual rende mais depois do imposto?\n\n"
                "A taxa do anúncio engana. A LCI paga menos e chega na frente quando o imposto do CDB come a diferença.\n\n"
                "O jeito de comparar é a taxa equivalente: quanto o CDB teria de pagar, já descontado o IR do prazo, "
                "pra empatar com a LCI.\n\n"
                "Você compara a taxa bruta ou o que cai na conta?",
        imagem="Reels com o Short; capa com as duas taxas e o leão no meio.",
    ),
    numeros=[],
)

C["2026-10-06"] = dict(
    titulo="ETFs que pagam dividendos mensais: o que mudou em 2026",
    x=dict(
        estrutura="E", mecanica="mito-x-fato",
        tweets=[
            "Tanaka, a lista de 2025 fez aniversário.\n\nO vídeo dos ETFs que pagam todo mês entrou no top 10 do ano do "
            "canal: 637 inscritos.\n\nAgora vem a parte que ninguém grava: conferir.",
            "Mito: \"ETF de dividendo mensal paga um salário.\"\n\nFato: paga todo mês, mas o valor muda todo mês.\n\n"
            "A data de pagamento é previsível. O valor, nunca foi.",
            "O que eu fui olhar, ETF por ETF:\n\n→ quanto pagou de verdade, mês a mês\n→ quanto cobra de taxa\n"
            "→ se o patrimônio cresceu ou encolheu\n\nPrometido contra pago. Lado a lado.",
            "E as dúvidas que vocês deixaram nos comentários entram no vídeo.\n\n"
            "Inclusive a que todo dono de ETF de renda faz um dia:\n\n\"por que esse mês veio menos?\"",
            "Dividendo mensal não é salário.\n\nÉ boleto ao contrário: chega todo mês, mas quem escolhe o valor "
            "é o mercado.",
        ],
        imagem="Capa: print do vídeo de 2025 com um carimbo de 'conferido' por cima.",
    ),
    ig=dict(
        slides=[
            "ETFs que pagam dividendos mensais: o que mudou em 2026",
            "Em 2025 a gente montou uma lista. Agora é a prestação de contas.",
            "Pagamento real, mês a mês. Não o prometido.",
            "Taxa: quanto fica com o gestor antes de chegar em você.",
            "Patrimônio: o ETF cresceu ou encolheu?",
            "Dividendo mensal não é salário. É boleto ao contrário.",
        ],
        legenda="ETFs que pagam dividendos mensais: em 2025 eu fiz uma lista. Em 2026 fui conferir.\n\n"
                "Pagamento real, taxa e patrimônio de cada um, lado a lado com o que se esperava. "
                "Mais as dúvidas que vocês deixaram nos comentários.\n\n"
                "Dividendo mensal chega todo mês. O valor, quem escolhe é o mercado.\n\n"
                "Qual mês veio menor no seu extrato?",
        imagem="Carrossel em fundo claro; slide 3 com barras 'prometido x pago' sem números até o vídeo sair.",
    ),
    numeros=[arq("637", TEMAS, "`Fb0l4KEq27o` | 637 |")],
)

C["2026-10-07"] = dict(
    titulo="Como juntar 1 milhão de reais com R$ 1.000 por mês",
    x=dict(
        estrutura="A", mecanica="extrato-falso",
        tweets=[
            "Tanaka, R$ 1.000 por mês vira 1 milhão.\n\nSó que não em 22 anos.\n\n"
            "A conta que a internet te vendeu esqueceu um detalhe.",
            "Extrato de 22 anos guardando R$ 1.000 por mês:\n\nSem render nada: R$ 264 mil.\n"
            "A 6% ao ano acima da inflação: cerca de R$ 535 mil.\nO milhão: chega perto dos 30 anos.",
            "O detalhe esquecido é a inflação.\n\nUm milhão daqui a 22 anos não compra o que um milhão compra hoje.\n\n"
            "Quem promete milhão rápido está contando em real de mentira.",
        ],
        imagem="Extrato bancário estilizado com as três linhas; a última em destaque.",
    ),
    ig=dict(
        slides=[
            "R$ 1.000 por mês vira 1 milhão? A conta honesta.",
            "Guardando sem render: R$ 264 mil em 22 anos.",
            "A 6% ao ano acima da inflação: cerca de R$ 535 mil.",
            "O milhão de verdade: perto de 30 anos.",
        ],
        legenda="Como juntar 1 milhão de reais com R$ 1.000 por mês: a conta sem maquiagem.\n\n"
                "Em 22 anos, só guardando, são R$ 264 mil. Rendendo 6% ao ano acima da inflação, cerca de R$ 535 mil, "
                "já em dinheiro de hoje. O milhão com poder de compra chega perto dos 30 anos.\n\n"
                "Não é mágica. É tempo e constância.\n\n"
                "Quantos anos a sua planilha promete?",
        imagem="Reels com o Short; capa com '22 anos' riscado e '30' escrito à mão.",
    ),
    numeros=[
        arq("264", PERG, "Guardando R$ 1.000 por mês sem render nada, são R$ 264 mil em 22 anos."),
        conta("264", "1000 * 12 * 22 / 1000", "R$ 1.000 por mês, 12 meses, 22 anos (CALENDARIO 07/10)"),
    ],
)

C["2026-10-08"] = dict(
    titulo="Tesouro IPCA+ a 7% em janeiro: quanto ganhou quem comprou",
    x=dict(
        estrutura="E", mecanica="atendimento-ao-cliente",
        tweets=[
            "Tanaka, em janeiro o Tesouro pagava IPCA+ 7%.\n\nQuem comprou ouviu \"travou a taxa\".\n\n"
            "Agora a pergunta que ninguém refaz: quanto ganhou até hoje?",
            "O vídeo de janeiro está no top 10 do ano do canal.\n\n"
            "Prometer é fácil. Prestar conta é que dá trabalho.\n\nEntão eu fui atrás do extrato.",
            "Três números decidem a conversa:\n\n→ o preço do título na compra\n→ o preço hoje\n"
            "→ os cupons que caíram no caminho\n\nUm deles pode estar no vermelho. E isso não quer dizer prejuízo.",
            "— Meu título caiu. Perdi dinheiro?\n— Só se vender hoje.\n— E se eu segurar?\n"
            "— Aí vale a taxa que você travou. A tela só mostra o humor do mercado.",
            "A taxa você travou em janeiro.\n\nO preço, ninguém trava.\n\nQuem confunde os dois vende no pior dia.",
        ],
        imagem="Capa: thumb do vídeo de janeiro ao lado de um extrato com 'janeiro' e 'hoje'.",
    ),
    ig=dict(
        slides=[
            "Tesouro IPCA+ a 7% em janeiro: quanto ganhou quem comprou?",
            "Janeiro: o Tesouro pagava IPCA+ 7%. Quem comprou, travou.",
            "Hoje: o preço na compra contra o preço de agora.",
            "No caminho: os cupons que já caíram na conta.",
            "Marcação a mercado: o preço mexe todo dia. A taxa travada, não.",
            "A taxa você travou. O preço, ninguém trava.",
        ],
        legenda="Tesouro IPCA+ a 7% em janeiro: quanto ganhou quem comprou? Prestação de contas.\n\n"
                "Preço na compra, preço hoje e os cupons do caminho. Se a tela mostra vermelho, o vídeo explica por que "
                "isso não é o mesmo que prejuízo pra quem leva até o vencimento.\n\n"
                "A taxa fica travada. O preço passeia.\n\n"
                "Você abriu o extrato este mês ou preferiu não ver?",
        imagem="Carrossel com linha do tempo janeiro -> hoje; slide 5 com uma gangorra juros x preço.",
    ),
    numeros=[],
)

# ------------------------------------------------------------------ semana 12/10
C["2026-10-12"] = dict(
    titulo="Resgatou o CDB antes de 30 dias? O IOF come o rendimento",
    x=dict(
        estrutura="A", mecanica="manual-invertido",
        tweets=[
            "Tanaka, o CDB rendeu.\n\nVocê sacou na segunda semana.\n\nE o rendimento chegou mordido.",
            "Manual pra perder rendimento:\n\n→ aplique no CDB\n→ precise do dinheiro antes de 30 dias\n→ resgate\n\n"
            "O IOF faz o resto. Quanto mais cedo o saque, maior a mordida.",
            "No dia 30, o IOF zera e sobra só o IR.\n\nAntes disso, ele é regressivo: começa alto e cai dia a dia.\n\n"
            "Dinheiro que você mexe todo mês pede outra aplicação.",
        ],
        imagem="Calendário de 30 dias com uma boca mordendo os primeiros dias.",
    ),
    ig=dict(
        slides=[
            "Resgatou o CDB antes de 30 dias? O IOF chegou primeiro.",
            "Antes de 30 dias, o resgate paga IOF.",
            "A mordida é regressiva: maior no começo, menor a cada dia.",
            "No dia 30, o IOF zera. Sobra só o IR.",
        ],
        legenda="Resgatou o CDB antes de 30 dias? O IOF come o rendimento.\n\n"
                "O imposto é regressivo: quem saca nos primeiros dias deixa uma fatia grande do que rendeu. "
                "A cada dia a mordida diminui, e no dia 30 ela some. Aí sobra só o IR.\n\n"
                "Dinheiro que pode sair a qualquer hora pede aplicação pensada pra isso.\n\n"
                "Você já levou essa mordida?",
        imagem="Reels com o Short; capa com o calendário mordido.",
    ),
    numeros=[],
)

C["2026-10-13"] = dict(
    titulo="Dividendos mensais com ações: como montar um calendário",
    x=dict(
        estrutura="D", mecanica="eco-do-gatilho (cair)",
        tweets=[
            "Tanaka, dividendo não cai todo mês por mágica.\n\nCai por calendário.\n\n"
            "E quase ninguém sabe ler o calendário.",
            "A pergunta de sempre: \"qual ação paga todo mês?\"\n\nPergunta errada.\n\n"
            "A certa: em que mês cada empresa costuma pagar, e até quando você precisa ter a ação pra entrar na lista?",
            "Duas datas mandam no jogo:\n\n→ data com: o último dia pra ter a ação e ter direito\n"
            "→ data de pagamento: quando o dinheiro cai\n\nEntre uma e outra podem passar semanas. Às vezes meses.",
            "E o valor muda. Sempre.\n\nDividendo vem do lucro. Lucro caiu, dividendo cai junto.\n\n"
            "E se vier como JCP, já chega com 17,5% de imposto retido na fonte.",
            "Renda mensal com ação é escala de churrasco da família.\n\nCada mês um primo paga a carne.\n\n"
            "O problema é quando o primo de março cai fora.",
        ],
        imagem="Calendário de parede com nomes genéricos ('primo 1', 'primo 2') em cada mês, um deles riscado.",
    ),
    ig=dict(
        slides=[
            "Dividendos mensais com ações: como montar um calendário",
            "\"Todo mês\" não é promessa. É calendário.",
            "Data com: o último dia pra ter a ação e entrar na lista.",
            "Data de pagamento: quando o dinheiro cai. Pode levar semanas.",
            "O valor varia: vem do lucro. E o JCP chega com 17,5% retido.",
            "Renda mensal com ação é escala de churrasco: cada mês um primo paga a carne.",
        ],
        legenda="Dividendos mensais com ações: o segredo é o calendário, não a ação.\n\n"
                "Cada empresa paga em meses diferentes. O que decide se você recebe é a data com. O que decide quando "
                "recebe é a data de pagamento. E o valor muda, porque dividendo sai do lucro.\n\n"
                "Sem lista de compra aqui. Só o mapa.\n\n"
                "Em que mês o seu calendário tem buraco?",
        imagem="Carrossel com um calendário anual que vai sendo preenchido slide a slide, sem tickers.",
    ),
    numeros=[],
)

C["2026-10-14"] = dict(
    titulo="Tesouro IPCA+ negativo? Calma, isso tem nome",
    x=dict(
        estrutura="A", mecanica="tradutor-juramentado",
        tweets=[
            "Tanaka, seu Tesouro IPCA+ ficou negativo?\n\nRespira.\n\nIsso tem nome: marcação a mercado.",
            "O app diz: \"rentabilidade negativa\".\n\nTradução: se você vendesse hoje, venderia mais barato do que comprou.\n\n"
            "Se não vender, essa linha é só o humor do mercado no dia.",
            "Juros sobem, o preço do título cai.\nJuros caem, o preço sobe.\n\n"
            "Quem leva até o vencimento recebe a taxa que travou. Quem vende no susto transforma humor em prejuízo.",
        ],
        imagem="Print genérico de app com '-' em vermelho e uma legenda 'humor do dia'.",
    ),
    ig=dict(
        slides=[
            "Tesouro IPCA+ negativo? Calma, isso tem nome.",
            "Marcação a mercado: o título tem preço todo dia.",
            "Juros sobem, o preço cai. Juros caem, o preço sobe.",
            "Até o vencimento, vale a taxa que você travou.",
        ],
        legenda="Tesouro IPCA+ negativo no app? Isso se chama marcação a mercado.\n\n"
                "O título tem preço todo dia. Quando os juros sobem, o preço cai. Quem leva até o vencimento recebe a "
                "taxa contratada. Quem vende no susto realiza a queda.\n\n"
                "O vermelho na tela é humor do mercado, não sentença.\n\n"
                "Você já vendeu no susto?",
        imagem="Reels com o Short (corte do longo de 08/10); capa com a gangorra juros x preço.",
    ),
    numeros=[],
    corte_de="2026-10-08",
)

C["2026-10-15"] = dict(
    titulo="Crise financeira: o gráfico de 1929, 2008 e 2020, hoje",
    x=dict(
        estrutura="B", mecanica="boletim-escolar",
        tweets=[
            "Tanaka, um gráfico acertou 1929, 2008 e 2020.\n\nO vídeo sobre ele foi o 3º melhor do canal no ano.\n\n"
            "Agora ele vai ter que se explicar.",
            "Todo indicador de crise tem fã-clube.\n\nAcerta uma vez, vira profeta.\n\n"
            "Erra três, ninguém lembra. Igual vidente de fim de ano na TV.",
            "Então o vídeo faz o que quase ninguém faz:\n\n→ o que o gráfico marcava antes de cada crise\n"
            "→ o que ele marca hoje\n→ quantas vezes ele gritou \"crise\" e não veio nada",
            "E entram os sinais do vídeo de novembro de 2025, \"A crise já está acontecendo\".\n\n"
            "Um ano depois, cada sinal com o dado de hoje do lado.\n\nO que se confirmou. O que não.",
            "Boletim do indicador:\n\nAs três crises: acertou.\nAlarmes falsos: o vídeo conta.\n"
            "Observação da professora: bom aluno, mas grita demais na sala.",
        ],
        imagem="Boletim escolar com o nome 'Indicador' e as três crises como matérias.",
    ),
    ig=dict(
        slides=[
            "Crise financeira: o gráfico de 1929, 2008 e 2020, hoje",
            "Ele acertou as três. Virou profeta.",
            "O que ele marcava antes de cada crise.",
            "O que ele marca hoje.",
            "E as vezes em que gritou \"crise\" e nada aconteceu.",
            "Indicador bom não é o que acerta. É o que você sabe quando erra.",
        ],
        legenda="Crise financeira: o gráfico que acertou 1929, 2008 e 2020 passou por revisão.\n\n"
                "O que ele marcava antes de cada crise, o que marca hoje e os alarmes falsos no caminho. Mais os sinais "
                "do vídeo de novembro de 2025, conferidos um a um com o dado de agora.\n\n"
                "Sem prever data de crash. Ninguém sabe.\n\n"
                "Você confia em gráfico que acertou três vezes?",
        imagem="Carrossel com o gráfico original e três marcações; slide 5 com balões de 'alarme' vazios.",
    ),
    numeros=[],
)

# ------------------------------------------------------------------ semana 19/10
C["2026-10-19"] = dict(
    titulo="FII é isento de imposto? Só se cumprir estas 3 regras",
    x=dict(
        estrutura="D", mecanica="pergunta-do-leitor",
        tweets=[
            "Tanaka, rendimento de FII é isento de IR.\n\nMas só se passar em 3 regras.\n\nE uma delas depende de você.",
            "As 3 regras:\n\n→ o fundo tem 100 cotistas ou mais\n→ as cotas são negociadas em bolsa\n"
            "→ você tem menos de 10% das cotas\n\nFalhou uma? O rendimento paga imposto.",
            "\"Mas FII não era isento?\"\n\nO rendimento, sim, com as regras.\n\n"
            "A venda da cota com lucro, não: paga 20% sobre o ganho. Isenção tem endereço.",
        ],
        imagem="Checklist com três caixas, a terceira com o rosto do Tanaka.",
    ),
    ig=dict(
        slides=[
            "FII é isento de imposto? Só com estas 3 regras.",
            "100 cotistas ou mais. Cotas negociadas em bolsa.",
            "Você com menos de 10% das cotas.",
            "Vendeu com lucro? Paga 20% sobre o ganho.",
        ],
        legenda="FII é isento de imposto? O rendimento é, se o fundo cumprir 3 regras: 100 cotistas ou mais, cotas "
                "negociadas em bolsa e você com menos de 10% das cotas.\n\n"
                "A venda é outra história. Lucro na venda da cota paga 20%.\n\n"
                "Isenção tem condição. Quem lê só a manchete descobre na declaração.\n\n"
                "Você já conferiu o número de cotistas do seu fundo?",
        imagem="Reels com o Short; capa com o checklist das 3 regras.",
    ),
    numeros=[],
)

C["2026-10-20"] = dict(
    titulo="ETF de dividendos mensais com opções: de onde vem a renda",
    x=dict(
        estrutura="C", mecanica="tradutor-juramentado",
        tweets=[
            "Tanaka, esse ETF paga renda alta todo mês.\n\nO dinheiro não vem só de dividendo.\n\n"
            "Vem de vender uma coisa que você nem sabia que tinha.",
            "Ele vende opções de compra sobre as ações da carteira.\n\n"
            "Tradução: aluga pra alguém o direito de comprar as ações dele por um preço combinado.\n\n"
            "O aluguel vira a sua renda do mês.",
            "É como alugar a sua vaga de garagem no dia do jogo.\n\nEntra dinheiro todo domingo.\n\n"
            "Mas no dia da final, quando a vaga vale ouro, ela já está alugada pelo preço de sempre.",
            "Na prática:\n\n→ mercado de lado: a renda das opções brilha\n"
            "→ mercado subindo forte: o ETF fica com só uma parte da alta\n"
            "→ mercado caindo: a renda amortece, não impede a queda",
            "ETF de dividendos comum divide o lucro das empresas.\n\nO de opções vende o seu ingresso pra final.\n\n"
            "Renda alta tem preço. Ele só não aparece no extrato do mês.",
        ],
        imagem="Vaga de garagem com placa 'alugada' em frente a um estádio lotado.",
    ),
    ig=dict(
        slides=[
            "ETF de dividendos mensais com opções: de onde vem a renda",
            "Não é só dividendo. É aluguel.",
            "Ele vende opções de compra sobre as ações que tem.",
            "Mercado de lado: a renda brilha.",
            "Mercado subindo forte: você fica com só uma parte da alta.",
            "Renda alta tem preço. Ele não aparece no extrato do mês.",
        ],
        legenda="ETF de dividendos mensais com opções: a renda alta vem de vender opções de compra sobre as ações da "
                "carteira, não só de dividendo.\n\n"
                "Funciona como alugar a vaga de garagem: entra dinheiro todo mês, mas no dia da final a vaga já está "
                "alugada pelo preço de sempre. A alta forte fica limitada.\n\n"
                "O vídeo compara com o ETF de dividendos comum.\n\n"
                "De onde vem a renda do seu ETF?",
        imagem="Carrossel com a vaga de garagem como fio condutor do slide 2 ao 6.",
    ),
    numeros=[],
)

C["2026-10-21"] = dict(
    titulo="Casal que investe junto: a conversa que vem antes do dinheiro",
    x=dict(
        estrutura="B", mecanica="manual-invertido",
        tweets=[
            "Tanaka, casal briga por dinheiro.\n\nQuase nunca pela taxa do CDB.\n\n"
            "Briga porque nunca combinou pra que serve o dinheiro.",
            "Manual pra brigar por dinheiro a dois:\n\n→ abram conta conjunta sem conversar\n"
            "→ cada um investe pensando num sonho diferente\n→ descubram na hora do saque",
            "A conversa que vem antes: \"esse dinheiro é pra quê, e pra quando?\"\n\n"
            "Viagem daqui a dois anos e aposentadoria daqui a trinta não cabem na mesma aplicação.\n\n"
            "Igual pizza: primeiro o sabor, depois a fatia.",
        ],
        imagem="Pizza meio a meio com sabores que não combinam.",
    ),
    ig=dict(
        slides=[
            "Casal que investe junto: a conversa vem antes do dinheiro.",
            "A pergunta: esse dinheiro é pra quê?",
            "E pra quando? O prazo muda tudo.",
            "Primeiro o sabor da pizza. Depois a fatia.",
        ],
        legenda="Casal que investe junto começa por uma conversa, não por um produto.\n\n"
                "A pergunta é simples: esse dinheiro é pra quê, e pra quando? Viagem, casa, reserva e aposentadoria "
                "têm prazos diferentes. Misturar tudo na mesma aplicação é pedir briga no meio do caminho.\n\n"
                "Igual pizza: primeiro o sabor, depois a fatia.\n\n"
                "Vocês já tiveram essa conversa?",
        imagem="Reels com o Short; capa com a pizza meio a meio.",
    ),
    numeros=[],
)

C["2026-10-22"] = dict(
    titulo="LCI e LCA ou CDB: a conta de 2026 com imposto e prazo",
    x=dict(
        estrutura="C", mecanica="eco-do-gatilho (preso)",
        tweets=[
            "Tanaka, 80 mil na LCI por 12 meses?\n\nA pergunta é essa, seca.\n\n"
            "A resposta não é sim nem não. É uma conta.",
            "LCI e LCA não pagam IR pra pessoa física.\n\nCDB paga, e a alíquota cai conforme o prazo.\n\n"
            "Por isso a taxa menor da LCI pode deixar mais dinheiro no seu bolso que a taxa maior do CDB.",
            "Mas imposto é só um dos quatro itens da conta:\n\n→ taxa equivalente\n"
            "→ carência: quanto tempo o dinheiro fica preso\n→ liquidez: se dá pra sair antes\n"
            "→ FGC: até onde a garantia cobre",
            "Na prática: antes de comparar taxa, compare o prazo.\n\n"
            "Se você pode precisar do dinheiro no meio do caminho, a LCI com carência vira cofre trancado "
            "com a chave do lado de dentro.",
            "O banco anuncia a taxa em letra grande.\n\nA carência vem em letra miúda.\n\n"
            "E é ela que decide quanto tempo o seu dinheiro fica preso.",
        ],
        imagem="Cofre com a chave pendurada do lado de dentro, visto pela fechadura.",
    ),
    ig=dict(
        slides=[
            "LCI e LCA ou CDB: a conta de 2026 com imposto e prazo",
            "80 mil na LCI por 12 meses? A resposta é uma conta.",
            "LCI e LCA: sem IR pra pessoa física. CDB: IR que cai com o prazo.",
            "Taxa equivalente: quanto o CDB precisa pagar pra empatar.",
            "Carência e liquidez: quando o dinheiro pode sair.",
            "FGC: até onde a garantia cobre. Taxa em letra grande, carência em letra miúda.",
        ],
        legenda="LCI e LCA ou CDB em 2026: a conta tem quatro itens, não um.\n\n"
                "Imposto (LCI e LCA isentas pra pessoa física, CDB com IR que cai com o prazo), carência, liquidez e "
                "FGC. A pergunta \"80 mil em LCI por 12 meses?\" vira conta, sem recomendação.\n\n"
                "Taxa em letra grande. Carência em letra miúda.\n\n"
                "Qual das duas você leu primeiro?",
        imagem="Carrossel com contrato em letra miúda e lupa no slide 5.",
    ),
    numeros=[],
)

# ------------------------------------------------------------------ semana 26/10
C["2026-10-26"] = dict(
    titulo="FGC: o que cobre e o que não cobre",
    x=dict(
        estrutura="A", mecanica="atendimento-ao-cliente",
        tweets=[
            "Tanaka, o FGC não cobre tudo.\n\nE o que ele não cobre costuma ser o que você acha que cobre.",
            "Cobre: até R$ 250 mil por CPF por instituição.\n\nTeto: R$ 1 milhão a cada 4 anos, somando tudo.\n\n"
            "Vale pra CDB, LCI e LCA, entre outros.",
            "— E o meu Tesouro, o FGC cobre?\n— Não. Quem garante é o Tesouro Nacional.\n— E o fundo? E a ação?\n"
            "— Aí não tem garantia. O risco é seu, com nome e CPF.",
        ],
        imagem="Guarda-chuva com o rótulo 'FGC' cobrindo só metade de uma mesa de investimentos.",
    ),
    ig=dict(
        slides=[
            "FGC: o que cobre e o que não cobre",
            "Cobre: até R$ 250 mil por CPF por instituição.",
            "Teto: R$ 1 milhão a cada 4 anos.",
            "Não cobre: Tesouro Direto, fundos e ações.",
        ],
        legenda="FGC: o que cobre e o que não cobre.\n\n"
                "Cobre até R$ 250 mil por CPF por instituição, com teto de R$ 1 milhão a cada 4 anos. Vale pra CDB, "
                "LCI e LCA, entre outros.\n\n"
                "Não cobre Tesouro Direto, fundos e ações. No Tesouro, quem responde é o Tesouro Nacional. Em fundo e "
                "ação, o risco é de quem investe.\n\n"
                "Você sabe quanto tem em cada banco?",
        imagem="Reels com o Short; capa com o guarda-chuva pela metade.",
    ),
    numeros=[],
)

C["2026-10-27"] = dict(
    titulo="ETF de dividendos mensais ou fundo imobiliário: o que sobra",
    x=dict(
        estrutura="C", mecanica="contraste",
        tweets=[
            "Tanaka, ETF ou FII pra renda mensal?\n\nTodo mundo compara quanto paga.\n\n"
            "Quase ninguém compara quanto sobra.",
            "O que sobra depende de três coisas:\n\n→ como cada um paga\n→ quanto imposto morde em 2026\n"
            "→ quanto a renda balança de um mês pro outro",
            "FII: o rendimento pode ser isento pra pessoa física, se o fundo cumprir as regras.\n\n"
            "ETF: a regra de imposto é outra.\n\nMesma renda bruta, sobras diferentes.",
            "E tem a balança.\n\nRenda de FII vem de aluguel e de juros de papel.\n\n"
            "Renda de ETF de dividendos vem do lucro de várias empresas.\n\nCada uma oscila por um motivo diferente.",
            "Comparar ETF com FII pelo valor pago é escolher churrasco pela picanha do cartaz.\n\n"
            "O que importa é quanto sobra no prato. Depois da taxa e do imposto.",
        ],
        imagem="Cartaz de churrascaria com picanha enorme ao lado de um prato com uma fatia fina.",
    ),
    ig=dict(
        slides=[
            "ETF de dividendos mensais ou fundo imobiliário: o que sobra",
            "Todo mundo compara quanto paga. Pouca gente compara quanto sobra.",
            "Como cada um paga: aluguel e papel de um lado, lucro de empresas do outro.",
            "Imposto em 2026: FII com isenção condicionada. ETF com regra própria.",
            "Volatilidade: cada renda balança por um motivo diferente.",
            "A picanha do cartaz não é a do prato.",
        ],
        legenda="ETF de dividendos mensais ou fundo imobiliário? A pergunta certa é quanto sobra.\n\n"
                "O vídeo compara como cada um paga, a tributação de cada um em 2026 e o quanto a renda varia de um mês "
                "pro outro. Sem indicar fundo nem ETF.\n\n"
                "A picanha do cartaz não é a do prato.\n\n"
                "Você olha o valor pago ou o que sobra?",
        imagem="Carrossel com duas colunas (ETF | FII) que vão sendo preenchidas.",
    ),
    numeros=[],
)

C["2026-10-28"] = dict(
    titulo="Quanto rende R$ 1.000 no Tesouro Selic hoje",
    x=dict(
        estrutura="D", mecanica="conta-rapida",
        tweets=[
            "Tanaka, R$ 1.000 no Tesouro Selic.\n\nQuanto rende de verdade?\n\n"
            "Não a taxa do anúncio. O que cai na conta.",
            "A conta líquida em uma linha:\n\nrendimento bruto do título, menos o IR do prazo.\n\n"
            "E se sacar antes de 30 dias, ainda tem IOF na fila.",
            "Conta rápida pra R$ 1.000 em um ano:\n\n→ bruto: a taxa do dia\n→ menos o IR do prazo\n"
            "→ líquido: [CHECAR: valor líquido com a taxa do Tesouro Selic do dia da gravação]\n\n"
            "Tesouro Selic não é pra ficar rico. É pra dormir.",
        ],
        imagem="Nota de R$ 1.000 fictícia (sem marca) dentro de um travesseiro.",
    ),
    ig=dict(
        slides=[
            "Quanto rende R$ 1.000 no Tesouro Selic hoje",
            "Bruto: a taxa do dia. Líquido: depois do IR do prazo.",
            "Saiu antes de 30 dias? Tem IOF.",
            "Em um ano: [CHECAR: valor líquido de R$ 1.000 com a taxa do dia].",
        ],
        legenda="Quanto rende R$ 1.000 no Tesouro Selic hoje, já descontado o imposto.\n\n"
                "A conta é simples: rendimento bruto menos o IR do prazo, e IOF se o resgate vier antes de 30 dias. "
                "Com a taxa do dia da gravação, o líquido em um ano fica em [CHECAR: valor líquido em um ano].\n\n"
                "Não é pra enriquecer. É pra dormir.\n\n"
                "Você sabe quanto rende o seu?",
        imagem="Reels com o Short; capa com o travesseiro.",
    ),
    numeros=[],
)

C["2026-10-29"] = dict(
    titulo="Tesouro IPCA+ acima de 7%: o que é travar a taxa",
    x=dict(
        estrutura="E", mecanica="eco-do-gatilho (travar)",
        tweets=[
            "Tanaka, travar IPCA+ 7% parece simples.\n\nVocê compra, a taxa fica.\n\n"
            "Só que \"travar\" tem letra miúda, e ela aparece no meio do caminho.",
            "Começa pelo fim: no vencimento, você recebe a inflação do período mais a taxa que travou.\n\n"
            "Isso não muda. Nem se o mercado surtar.\n\nO problema é o meio.",
            "No meio, o título tem preço todo dia.\n\nSe os juros sobem depois da sua compra, o preço cai.\n\n"
            "Travou a taxa, não travou o preço. São duas travas, e só uma está na sua mão.",
            "Na prática:\n\n→ levou até o vencimento: recebe o combinado\n"
            "→ vendeu antes: recebe o preço do dia, que pode ser maior ou menor\n\n"
            "A decisão real não é a taxa. É o prazo que você consegue esperar.",
            "O vídeo não dá palpite de compra.\n\nMostra o que você assina quando compra.\n\n"
            "Quem trava a taxa e não trava a paciência destrava no pior dia.",
        ],
        imagem="Cadeado fechado na taxa e uma corrente solta no preço.",
    ),
    ig=dict(
        slides=[
            "Tesouro IPCA+ acima de 7%: o que é travar a taxa",
            "No vencimento: inflação do período + a taxa travada.",
            "No meio do caminho: o preço muda todo dia.",
            "Juros sobem depois da compra? O preço cai.",
            "Vendeu antes: preço do dia. Levou até o fim: o combinado.",
            "Travou a taxa. Agora trava a paciência.",
        ],
        legenda="Tesouro IPCA+ acima de 7%: o que significa travar a taxa.\n\n"
                "No vencimento, você recebe a inflação do período mais a taxa contratada. No caminho, o título tem "
                "preço diário e pode cair se os juros subirem. Vender antes é aceitar o preço do dia.\n\n"
                "Travar a taxa é fácil. Difícil é travar a paciência.\n\n"
                "Quanto tempo você aguenta sem mexer?",
        imagem="Carrossel com o cadeado da taxa e a corrente do preço.",
    ),
    numeros=[],
)

C["2026-10-31"] = dict(
    titulo="TRXF11: o que aconteceu com a renda desde agosto",
    x=dict(
        estrutura="B", mecanica="mito-x-fato",
        tweets=[
            "Tanaka, TRXF11 lidera as buscas de investimento.\n\n"
            "É o termo de investimento mais buscado do canal nos últimos 6 meses.\n\nEntão vamos aos números do fundo, sem torcida.",
            "Desde agosto, três linhas contam a história de um FII:\n\n→ quanto distribuiu de rendimento\n"
            "→ quanto dos imóveis está vago\n→ quanto vale a cota\n\nO vídeo põe as três lado a lado, mês a mês.",
            "Mito: \"o vídeo vai dizer se compra ou vende.\"\n\n"
            "Fato: o vídeo mostra rendimento, vacância e cota, mês a mês, e para aí.\n\n"
            "O número é do fundo. A decisão é sua.",
            "Por que tanta busca? Quem tem cota quer saber se a renda vai se manter.\n\n"
            "Pergunta justa. A resposta honesta vem dos informes do fundo, não do grupo de WhatsApp.",
            "Cota é humor.\n\nRendimento é aluguel.\n\nVacância é o quarto vazio que ninguém gosta de mostrar na visita.",
        ],
        imagem="Três termômetros lado a lado: rendimento, vacância, cota.",
    ),
    ig=dict(
        slides=[
            "TRXF11: o que aconteceu com a renda desde agosto",
            "O termo de investimento mais buscado do canal nos últimos 6 meses.",
            "Rendimento distribuído: mês a mês.",
            "Vacância: quanto dos imóveis está sem inquilino.",
            "Cota: quanto o mercado paga hoje.",
            "Sem torcida, sem compra, sem venda. Só os números do fundo.",
        ],
        legenda="TRXF11: o que aconteceu com a renda desde agosto.\n\n"
                "Foi o termo de investimento mais buscado no canal nos últimos 6 meses. Então o vídeo abre os números "
                "do fundo: rendimento distribuído, vacância e cota, mês a mês, a partir dos relatórios e informes.\n\n"
                "Acompanhamento neutro. Ninguém aqui diz compra ou vende.\n\n"
                "Qual desses três números você olha primeiro?",
        imagem="Carrossel com os três termômetros; nenhuma seta de compra ou venda.",
    ),
    numeros=[],
)

# ------------------------------------------------------------------ semana 02/11
C["2026-11-02"] = dict(
    titulo="JCP em 2026: já vem com 17,5% de imposto",
    x=dict(
        estrutura="C", mecanica="contraste",
        tweets=[
            "Tanaka, o JCP de 2026 chega mordido.\n\nNão na empresa. Em você.\n\n"
            "Vem com 17,5% de imposto retido na fonte.",
            "O que a empresa anuncia: o JCP bruto.\n\nO que cai na sua conta: o JCP menos 17,5%.\n\n"
            "A mordida acontece no caminho, antes de você ver o extrato.",
            "Na prática: o JCP cai na conta já descontado.\n\nO valor que a empresa anuncia não é o que você recebe.\n\n"
            "Dividendo, até R$ 50 mil por mês da mesma empresa, segue sem retenção. O JCP paga pedágio sempre.",
        ],
        imagem="Dois envelopes: 'anunciado' cheio e 'recebido' com uma mordida no canto.",
    ),
    ig=dict(
        slides=[
            "JCP em 2026: já vem com 17,5% de imposto",
            "JCP é retido na fonte: 17,5%.",
            "O valor anunciado não é o que cai na conta.",
            "Dividendo até R$ 50 mil por mês da mesma empresa: sem retenção.",
        ],
        legenda="JCP em 2026 já vem com 17,5% de imposto retido na fonte.\n\n"
                "O valor que a empresa anuncia é bruto. O que cai na conta vem descontado. Dividendo segue sem retenção "
                "até R$ 50 mil por mês da mesma empresa.\n\n"
                "Parecem irmãos. Só um paga pedágio sempre.\n\n"
                "Você confere o líquido ou o anunciado?",
        imagem="Reels com o Short; capa com os dois envelopes.",
    ),
    numeros=[arq("50", CAL, "Retenção de 10% só acima de R$ 50 mil por mês da mesma empresa (Lei 15.270/2025).")],
)

C["2026-11-03"] = dict(
    titulo="Dividendos mensais de R$ 1.000: quanto precisa investir",
    x=dict(
        estrutura="D", mecanica="conta-rapida",
        tweets=[
            "Tanaka, R$ 1.000 por mês de dividendo.\n\nTodo mundo quer.\n\n"
            "Pouca gente fez a conta de quanto precisa ter investido pra isso.",
            "A conta começa simples:\n\nR$ 1.000 por mês = R$ 12 mil por ano.\n\n"
            "Agora divide pelo rendimento líquido anual de onde o dinheiro está. Esse divisor muda tudo.",
            "O vídeo faz a conta em três classes:\n\n→ Tesouro\n→ fundos imobiliários\n→ ações que pagam dividendos\n\n"
            "Cada uma com o imposto que cabe a ela, porque renda bruta não paga boleto.",
            "E aqui mora a pegadinha da conta:\n\nquanto maior o rendimento prometido, menor o capital necessário.\n\n"
            "E maior a chance de a renda oscilar. Quem escolhe só pelo divisor esquece da balança.",
            "R$ 1.000 por mês não é um número mágico.\n\nÉ uma divisão.\n\nO resto da conta é paciência, que não tem ticker.",
        ],
        imagem="Guardanapo de bar com a divisão 'R$ 12 mil ÷ ?' escrita à caneta.",
    ),
    ig=dict(
        slides=[
            "Dividendos mensais de R$ 1.000: quanto precisa investir",
            "R$ 1.000 por mês = R$ 12 mil por ano.",
            "Capital necessário = R$ 12 mil ÷ rendimento líquido anual.",
            "Três classes: Tesouro, fundos imobiliários e ações.",
            "Rendimento maior, capital menor. E renda mais instável.",
            "Paciência não tem ticker.",
        ],
        legenda="Dividendos mensais de R$ 1.000: quanto precisa investir?\n\n"
                "A conta começa com R$ 12 mil por ano divididos pelo rendimento líquido anual. O vídeo faz isso em três "
                "classes (Tesouro, fundos imobiliários e ações), já descontado o imposto de cada uma. Sem indicar ativo.\n\n"
                "Rendimento alto encolhe a conta e aumenta o balanço da renda.\n\n"
                "Qual divisor você usa na sua planilha?",
        imagem="Carrossel com o guardanapo; slide 4 com três copos de tamanhos diferentes.",
    ),
    numeros=[conta("12", "1000 * 12 / 1000", "R$ 1.000 por mês x 12 meses, em mil (título do vídeo)")],
)

C["2026-11-04"] = dict(
    titulo="Copom hoje: 3 números para olhar no seu Tesouro",
    x=dict(
        estrutura="C", mecanica="previsao-do-tempo",
        tweets=[
            "Tanaka, hoje tem Copom.\n\nA decisão sai no fim do dia.\n\n"
            "Antes dela, 3 números no seu Tesouro merecem uma olhada.",
            "Previsão do tempo pro seu Tesouro:\n\n→ taxa do IPCA+ hoje\n→ taxa do prefixado hoje\n"
            "→ a Selic que o mercado espera\n\nAnota antes. Amanhã você compara.",
            "Se a decisão vier diferente do esperado, as taxas mexem e o preço dos títulos mexe junto.\n\n"
            "Quem anotou entende o que aconteceu.\n\nQuem não anotou descobre pelo app, no susto.",
        ],
        imagem="Mapa do tempo de telejornal com 'IPCA+', 'prefixado' e 'Selic' no lugar das cidades.",
    ),
    ig=dict(
        slides=[
            "Copom hoje: 3 números para olhar no seu Tesouro",
            "Taxa do IPCA+ antes da decisão.",
            "Taxa do prefixado antes da decisão.",
            "A Selic que o mercado espera.",
        ],
        legenda="Copom hoje: 3 números para anotar no seu Tesouro antes da decisão.\n\n"
                "A taxa do IPCA+, a do prefixado e a Selic que o mercado espera. Se a decisão surpreender, as taxas e os "
                "preços dos títulos se mexem, e quem anotou entende o porquê.\n\n"
                "Amanhã sai o vídeo com o que mudou.\n\n"
                "Você vai olhar antes ou só depois?",
        imagem="Reels com o Short; capa com o mapa do tempo.",
    ),
    numeros=[],
    evento_ao_vivo="Postar ANTES do anúncio do Copom (04/11, fim do dia). Depois do anúncio, o texto envelhece.",
)

C["2026-11-05"] = dict(
    titulo="Tesouro Direto após o Copom: o que muda no IPCA+ e prefixado",
    x=dict(
        estrutura="E", mecanica="atendimento-ao-cliente",
        tweets=[
            "Tanaka, o Copom decidiu ontem.\n\nA Selic foi pra [CHECAR: decisão do Copom de 04/11].\n\n"
            "O seu Tesouro sentiu antes de você abrir o app.",
            "Antes: as taxas do IPCA+ e do prefixado na véspera.\n\n"
            "Depois: as mesmas taxas 24 h depois do comunicado.\n\nO vídeo põe uma do lado da outra.",
            "O que mexe o preço não é só a decisão.\n\nÉ a diferença entre o que o mercado esperava e o que veio.\n\n"
            "Veio igual ao esperado? Às vezes nada muda. Veio diferente? Aí o título reprecifica.",
            "— Meu prefixado subiu. Ganhei?\n— Se vender hoje, ganhou no preço.\n— E se não vender?\n"
            "— Recebe a taxa que contratou. O resto é paisagem.",
            "Copom não muda o contrato do seu título.\n\nMuda o preço de quem quer sair antes.\n\n"
            "A pergunta nunca é \"o que o Copom fez\". É \"quando eu vou precisar desse dinheiro\".",
        ],
        imagem="Duas fotos do mesmo painel de taxas: 'véspera' e '24 h depois'.",
    ),
    ig=dict(
        slides=[
            "Tesouro Direto após o Copom: o que muda no IPCA+ e prefixado",
            "Decisão de 04/11: [CHECAR: Selic decidida].",
            "Antes: as taxas na véspera.",
            "Depois: as taxas 24 h após o comunicado.",
            "Mexe o preço a surpresa, não só a decisão.",
            "O contrato não muda. Muda o preço de quem sai antes.",
        ],
        legenda="Tesouro Direto após o Copom: o que muda no IPCA+ e no prefixado.\n\n"
                "O vídeo compara as taxas da véspera com as de 24 h depois do comunicado de 04/11. O que mexe o preço "
                "é a diferença entre o esperado e o decidido.\n\n"
                "Pra quem leva o título até o vencimento, o contrato não muda.\n\n"
                "Você olhou o app hoje ou deixou pra semana que vem?",
        imagem="Carrossel 'véspera x 24 h depois' com as taxas preenchidas na hora (CHECAR).",
    ),
    numeros=[],
    evento_ao_vivo="Texto escrito para depois da decisão de 04/11: conferir o verbo e preencher o [CHECAR] com o "
                   "comunicado (bcb.gov.br) antes de aprovar.",
)

C["2026-11-07"] = dict(
    titulo="Fundos imobiliários para iniciantes: de onde vem a renda",
    x=dict(
        estrutura="A", mecanica="tradutor-juramentado",
        tweets=[
            "Tanaka, fundo imobiliário não é mágica.\n\nÉ aluguel.\n\n"
            "Dividido com muita gente que você nunca vai conhecer.",
            "O folheto diz: \"renda passiva todo mês\".\n\n"
            "Tradução: o fundo tem imóveis ou títulos de dívida imobiliária, recebe aluguel ou juros e repassa a "
            "maior parte pros cotistas.\n\nPassiva pra você. O gestor trabalha.",
            "Dois tipos de renda, dois riscos:\n\n→ tijolo: aluguel de galpão, shopping, escritório. Risco: imóvel vazio.\n"
            "→ papel: juros de dívida imobiliária. Risco: quem deve não pagar.",
            "E o imposto? O rendimento pode ser isento pra pessoa física, se o fundo cumprir as regras.\n\n"
            "A venda da cota com lucro paga imposto.\n\nIniciante que só lê \"isento\" descobre o resto na declaração.",
            "Fundo imobiliário é ser dono de um pedaço de shopping sem ter a chave.\n\nVocê não escolhe o inquilino.\n\n"
            "Mas sente quando ele vai embora.",
        ],
        imagem="Chaveiro com uma chave faltando, em frente a um shopping.",
    ),
    ig=dict(
        slides=[
            "Fundos imobiliários para iniciantes: de onde vem a renda",
            "FII não é mágica. É aluguel dividido.",
            "Tijolo: aluguel de imóveis. Risco: imóvel vazio.",
            "Papel: juros de dívida imobiliária. Risco: calote.",
            "Rendimento pode ser isento, com regras. A venda com lucro paga imposto.",
            "Dono de um pedaço do shopping, sem a chave.",
        ],
        legenda="Fundos imobiliários para iniciantes: de onde vem a renda.\n\n"
                "O fundo tem imóveis ou títulos de dívida imobiliária, recebe aluguel ou juros e repassa a maior parte "
                "aos cotistas. Tijolo depende de inquilino. Papel depende de quem deve pagar. Sem indicar fundo.\n\n"
                "Você vira dono de um pedaço do shopping, sem a chave.\n\n"
                "Qual foi a sua primeira dúvida sobre FII?",
        imagem="Carrossel com tijolo x papel em cores diferentes.",
    ),
    numeros=[],
)

# ------------------------------------------------------------------ semana 09/11
C["2026-11-09"] = dict(
    titulo="Imposto sobre dividendos acima de R$ 50 mil por mês: quem paga",
    x=dict(
        estrutura="D", mecanica="mito-x-fato",
        tweets=[
            "Tanaka, dividendo agora paga imposto?\n\nSó se passar de R$ 50 mil por mês.\n\n"
            "Da mesma empresa. Pra mesma pessoa.",
            "Acima disso, 10% retidos na fonte.\n\nAbaixo, segue como era.\n\n"
            "A regra nova tem endereço. E não é o seu, a não ser que uma empresa te pague mais de R$ 50 mil num mês só.",
            "Mito: \"agora todo dividendo paga imposto.\"\n\n"
            "Fato: a conta é por empresa. Várias empresas pagando menos de R$ 50 mil cada não entram, mesmo que a soma passe.\n\n"
            "Entra quem recebe mais que isso de uma só.",
        ],
        imagem="Envelope de carta com endereço de mansão e o Tanaka olhando pela janela do vizinho.",
    ),
    ig=dict(
        slides=[
            "Imposto sobre dividendos acima de R$ 50 mil por mês: quem paga",
            "Acima de R$ 50 mil por mês da mesma empresa: 10% retidos.",
            "Abaixo disso: sem retenção.",
            "A conta é por empresa, não pela soma.",
        ],
        legenda="Imposto sobre dividendos em 2026: só acima de R$ 50 mil por mês pagos pela mesma empresa à mesma "
                "pessoa. Acima disso, 10% retidos na fonte.\n\n"
                "A conta é por empresa, não pela soma da carteira.\n\n"
                "A regra nova existe. Só não mora na casa da maioria.\n\n"
                "Qual empresa te pagaria R$ 50 mil num mês?",
        imagem="Reels com o Short; capa com o envelope endereçado à mansão.",
    ),
    numeros=[],
)

C["2026-11-10"] = dict(
    titulo="Renda mensal com Tesouro Direto: juros semestrais e RendA+",
    x=dict(
        estrutura="B", mecanica="extrato-falso",
        tweets=[
            "Tanaka, o Tesouro paga renda.\n\nSó que de seis em seis meses.\n\nE o boleto do condomínio chega todo mês.",
            "Extrato de um título com juros semestrais:\n\nUm mês: cupom.\nCinco meses: silêncio.\nDe novo: cupom.\n\n"
            "O condomínio não leu esse extrato. Pra virar renda mensal, você mesmo divide o cupom em seis.",
            "O RendA+ faz outra coisa:\n\nvocê junta durante anos e, numa data combinada, ele passa a pagar todo mês, "
            "por um prazo fixo, corrigido pela inflação.\n\nÉ carnê ao contrário: quem recebe é você.",
            "E tem imposto nos dois.\n\nO cupom semestral paga IR a cada pagamento, pela tabela do prazo.\n\n"
            "O vídeo faz a conta do que sobra líquido, porque renda bruta não paga mercado.",
            "Renda mensal com Tesouro existe.\n\nMas chega de dois jeitos: em blocos, ou com data marcada pra começar.\n\n"
            "A pergunta é qual dos dois combina com o seu calendário de boletos.",
        ],
        imagem="Extrato com cinco linhas em branco entre dois cupons.",
    ),
    ig=dict(
        slides=[
            "Renda mensal com Tesouro Direto: juros semestrais e RendA+",
            "Juros semestrais: cupom duas vezes por ano.",
            "Pra virar mensal: você divide o cupom em seis.",
            "RendA+: você acumula, e depois ele paga todo mês, corrigido pela inflação.",
            "Os dois pagam IR. O vídeo faz a conta do líquido.",
            "Mesada semestral ou salário com data marcada?",
        ],
        legenda="Renda mensal com Tesouro Direto: dois caminhos.\n\n"
                "Os títulos com juros semestrais pagam cupom duas vezes por ano, e você divide em seis. O RendA+ "
                "acumula por anos e depois paga todo mês, corrigido pela inflação. Nos dois casos tem IR, e o vídeo faz a "
                "conta do que sobra.\n\n"
                "Mesada semestral ou salário com data marcada?",
        imagem="Carrossel com o extrato de cinco linhas vazias e, no slide 4, um carnê virado ao contrário.",
    ),
    numeros=[],
)

C["2026-11-11"] = dict(
    titulo="FII ou aluguel: quanto rende R$ 100 mil em cada um",
    x=dict(
        estrutura="A", mecanica="contraste",
        tweets=[
            "Tanaka, R$ 100 mil: imóvel ou FII?\n\nOs dois pagam aluguel.\n\n"
            "Só um deles te liga de madrugada porque o chuveiro queimou.",
            "A conta justa compara o que sobra:\n\n"
            "→ imóvel: aluguel menos IPTU e condomínio do mês vago, reforma, corretagem e IR\n"
            "→ FII: rendimento, que pode ser isento pra pessoa física\n\nBruto contra bruto é conversa de churrasco.",
            "Cota de FII: vende num clique.\n\nApartamento: vende quando aparecer comprador. E vende inteiro.\n\n"
            "Liquidez não aparece na planilha de rendimento. Aparece no dia em que você precisa.",
        ],
        imagem="Chuveiro queimado ao lado de um celular com o app da corretora genérico (sem marca).",
    ),
    ig=dict(
        slides=[
            "FII ou aluguel: quanto rende R$ 100 mil em cada um",
            "Imóvel: aluguel menos custos, vacância e IR.",
            "FII: rendimento que pode ser isento pra pessoa física.",
            "Liquidez: a cota sai num clique. O imóvel, quando aparecer comprador.",
        ],
        legenda="FII ou aluguel: quanto rende R$ 100 mil em cada um.\n\n"
                "A comparação honesta é líquida. No imóvel, saem IPTU e condomínio do mês vago, manutenção e IR do "
                "aluguel. No FII, o rendimento pode ser isento pra pessoa física, se o fundo cumprir as regras.\n\n"
                "E só um dos dois te liga quando o chuveiro queima.\n\n"
                "Você já fez essa conta com o seu imóvel?",
        imagem="Reels com o Short; capa com o chuveiro.",
    ),
    numeros=[],
)

C["2026-11-12"] = dict(
    titulo="Fundo imobiliário ou imóvel alugado: a conta de 2026",
    x=dict(
        estrutura="C", mecanica="eco-do-gatilho (escondido)",
        tweets=[
            "Tanaka, imóvel ou fundo imobiliário?\n\nA pergunta de sempre é \"qual rende mais\".\n\n"
            "Falta metade da pergunta.",
            "A pergunta inteira tem cinco partes:\n\n→ rendimento\n→ custo\n→ vacância\n→ imposto\n→ liquidez\n\n"
            "Quem compara só a primeira escolhe pela foto do anúncio.",
            "Custo e vacância são o lado escondido do imóvel.\n\n"
            "Mês sem inquilino, você paga condomínio e IPTU do próprio bolso.\n\n"
            "No FII, a vacância também existe. Só vem diluída entre vários imóveis.",
            "Imposto e liquidez são o lado escondido do FII.\n\nRendimento pode ser isento, com regras. Venda com lucro paga.\n\n"
            "E a cota oscila todo dia na tela, coisa que o preço do seu apartamento faz escondido.",
            "O apartamento não cai na tela.\n\nIsso não quer dizer que ele não caiu.\n\nQuer dizer que ninguém te mostrou.",
        ],
        imagem="Anúncio de apartamento com foto linda e, por trás, a planilha de custos.",
    ),
    ig=dict(
        slides=[
            "Fundo imobiliário ou imóvel alugado: a conta de 2026",
            "Rendimento é só a primeira linha.",
            "Custo: condomínio, IPTU, manutenção.",
            "Vacância: no imóvel, o mês vazio sai do seu bolso.",
            "Imposto e liquidez: o lado escondido do FII.",
            "O apartamento não cai na tela. Isso não quer dizer que não caiu.",
        ],
        legenda="Fundo imobiliário ou imóvel alugado em 2026: rendimento, custo, vacância, imposto e liquidez, lado a "
                "lado.\n\n"
                "O imóvel esconde o custo do mês vazio. O FII mostra a oscilação todo dia. Cada um tem a sua letra "
                "miúda, e o vídeo lê as duas sem indicar fundo.\n\n"
                "O apartamento não cai na tela. Não quer dizer que não caiu.\n\n"
                "Quando foi a última avaliação do seu?",
        imagem="Carrossel em duas colunas, com o lado escondido de cada um revelado no slide 5.",
    ),
    numeros=[],
)

C["2026-11-14"] = dict(
    titulo="CDB prefixado ou pós-fixado: qual rende mais em 2026",
    x=dict(
        estrutura="E", mecanica="atendimento-ao-cliente",
        tweets=[
            "Tanaka, prefixado ou pós?\n\nEssa dúvida rendeu um vídeo aqui em 2018.\n\n"
            "Oito anos depois, a pergunta é a mesma. A curva de juros, não.",
            "Prefixado: você trava a taxa hoje. Se os juros caírem, você ganhou a aposta.\n\n"
            "Pós-fixado: acompanha o CDI. Se os juros subirem, você vai junto.\n\n"
            "Nos dois casos, é uma aposta sobre o futuro dos juros.",
            "A régua pra comparar é a curva de juros do mercado.\n\nEla mostra quanto se espera de juros pra cada prazo.\n\n"
            "Prefixado acima da curva? Paga pelo risco. Abaixo? O banco agradece.",
            "— Qual rende mais?\n— Depende de pra onde os juros vão.\n— E pra onde vão?\n"
            "— Se eu soubesse, não estaria gravando vídeo.",
            "Prefixado é guarda-chuva comprado com sol.\n\nSe chover, você é gênio.\n\nSe fizer sol, carregou peso à toa.",
        ],
        imagem="Guarda-chuva fechado num dia de sol, com uma nuvem pequena no canto.",
    ),
    ig=dict(
        slides=[
            "CDB prefixado ou pós-fixado: qual rende mais em 2026",
            "Prefixado: taxa travada hoje.",
            "Pós-fixado: acompanha o CDI.",
            "A régua: a curva de juros do mercado.",
            "Os dois seguem a mesma tabela de IR. E têm FGC, nos limites.",
            "Prefixado é guarda-chuva comprado com sol.",
        ],
        legenda="CDB prefixado ou pós-fixado em 2026: a resposta depende da curva de juros, não do anúncio.\n\n"
                "No prefixado, você trava a taxa e ganha se os juros caírem. No pós, você acompanha o CDI. O vídeo faz "
                "a conta com a curva de hoje e lembra que os dois seguem a mesma tabela de IR.\n\n"
                "Guarda-chuva comprado com sol.\n\n"
                "Você aposta em chuva ou em sol?",
        imagem="Carrossel com o guarda-chuva e, no slide 4, a curva de juros desenhada à mão.",
    ),
    numeros=[],
)

# ------------------------------------------------------------------ semana 16/11
C["2026-11-16"] = dict(
    titulo="Perfil de investidor: 3 perguntas antes de investir",
    x=dict(
        estrutura="B", mecanica="manual-invertido",
        tweets=[
            "Tanaka, o questionário do banco é longo.\n\nAs perguntas que importam são 3.\n\n"
            "E você responde melhor sozinho, com calma, do que clicando \"concordo\".",
            "Manual de como errar o próprio perfil:\n\n→ responda rápido pra liberar o app\n"
            "→ marque \"arrojado\" porque soa melhor\n→ conheça o perfil de verdade na primeira queda",
            "As 3 perguntas:\n\n→ prazo: quando vou precisar desse dinheiro?\n→ objetivo: pra que ele serve?\n"
            "→ queda: se cair bastante, eu vendo ou espero?\n\nA terceira só tem resposta honesta depois que acontece.",
        ],
        imagem="Formulário com a caixinha 'arrojado' marcada e uma gota de suor.",
    ),
    ig=dict(
        slides=[
            "3 perguntas antes de investir",
            "Prazo: quando vou precisar desse dinheiro?",
            "Objetivo: pra que ele serve?",
            "Queda: se cair, eu vendo ou espero?",
        ],
        legenda="Antes de qualquer aplicação, 3 perguntas.\n\n"
                "Prazo: quando você vai precisar do dinheiro. Objetivo: pra que ele serve. Tolerância a queda: se cair, "
                "você vende ou espera.\n\n"
                "A terceira é a mais difícil. Todo mundo é arrojado até a primeira queda.\n\n"
                "Qual das três você nunca respondeu?",
        imagem="Reels com o Short; capa com o formulário.",
    ),
    numeros=[],
)

C["2026-11-17"] = dict(
    titulo="ETF de dividendos mensais: quanto a taxa tira da renda",
    x=dict(
        estrutura="C", mecanica="elogio-envenenado",
        tweets=[
            "Tanaka, \"essa taxa de 1,50 é alta?\"\n\nA pergunta é essa.\n\nA resposta cabe numa conta de 10 anos.",
            "Taxa de administração não aparece como boleto.\n\nEla sai do patrimônio do ETF, um pouquinho todo dia.\n\n"
            "Você nunca vê o débito. Só vê a renda um pouco menor do que poderia ser.",
            "A conta de 10 anos, sem mexer em mais nada:\n\n→ taxa de 0,5% ao ano: come cerca de 5% do patrimônio\n"
            "→ taxa de 1,5% ao ano: come cerca de 14%\n\nUm ponto de taxa por ano vira quase o triplo de mordida.",
            "Justiça seja feita ao gestor: ele cobra todo dia, sem falhar um.\n\nNem nos meses em que o ETF pagou menos.\n\n"
            "Disciplina que muito investidor queria ter com o próprio aporte.",
            "Taxa baixa não garante ETF bom.\n\nMas taxa alta precisa explicar, todo ano, o que entrega a mais.\n\n"
            "E a explicação sai do seu bolso.",
        ],
        imagem="Medalha de 'funcionário do mês' pendurada numa calculadora de taxa.",
    ),
    ig=dict(
        slides=[
            "ETF de dividendos mensais: quanto a taxa tira da renda",
            "\"Essa taxa de 1,50 é alta?\"",
            "A taxa sai do patrimônio do ETF, todo dia, sem boleto.",
            "Em 10 anos: 0,5% ao ano come cerca de 5% do patrimônio.",
            "Em 10 anos: 1,5% ao ano come cerca de 14%.",
            "Taxa alta precisa explicar, todo ano, o que entrega a mais.",
        ],
        legenda="ETF de dividendos mensais: quanto a taxa de administração tira da renda em 10 anos.\n\n"
                "A taxa não chega como boleto. Sai do patrimônio do fundo, todo dia. Na conta simples, 0,5% ao ano "
                "come cerca de 5% do patrimônio em 10 anos. A de 1,5% come cerca de 14%.\n\n"
                "Taxa alta precisa se explicar todo ano.\n\n"
                "Quanto cobra o seu?",
        imagem="Carrossel com duas barras de patrimônio encolhendo em ritmos diferentes (slides 4 e 5).",
    ),
    numeros=list(N_TAXA_ETF),
)

C["2026-11-18"] = dict(
    titulo="Juros compostos: por que 1 centavo dobrando todo dia não existe",
    x=dict(
        estrutura="B", mecanica="pergunta-do-leitor",
        tweets=[
            "Tanaka, 1 centavo dobrando vira milionário?\n\nEm 30 dobras, dá R$ 10,7 milhões.\n\n"
            "A conta está certa. O investimento é que não existe.",
            "\"Onde eu acho algo que dobra todo dia?\"\n\nEm lugar nenhum.\n\n"
            "A conta não mentiu: ela mostrou a curva. A vida real anda na mesma curva, só que em anos.",
            "Na vida real: R$ 1.000 por mês a 6% ao ano acima da inflação dá cerca de R$ 535 mil em 22 anos.\n\n"
            "Não é milhão em um mês.\n\nMas existe. E o do centavo, não.",
        ],
        imagem="Moeda de 1 centavo com uma escada infinita atrás e uma placa 'em obras'.",
    ),
    ig=dict(
        slides=[
            "1 centavo dobrando todo dia: a conta certa de um investimento que não existe",
            "30 dobras: R$ 10,7 milhões. Matemática pura.",
            "Nada sério dobra todo dia.",
            "Vida real: R$ 1.000 por mês a 6% acima da inflação, cerca de R$ 535 mil em 22 anos.",
        ],
        legenda="Juros compostos: por que 1 centavo dobrando todo dia não existe.\n\n"
                "A conta é real: 30 dobras levam 1 centavo a R$ 10,7 milhões. O investimento é que não existe. Na vida "
                "real, a curva é a mesma, só que em anos: R$ 1.000 por mês a 6% ao ano acima da inflação somam cerca de "
                "R$ 535 mil em 22 anos.\n\n"
                "Você acreditou no centavo?",
        imagem="Reels com o Short; capa com a moeda e a escada.",
    ),
    numeros=[
        arq("1", PERG, "1 centavo dobrando 30 vezes"),
        arq("30", PERG, "1 centavo dobrando 30 vezes"),
        arq("10,7", PERG, "R$ 10,7 milhões"),
        conta("10,7", "0.01 * 2 ** 30 / 1e6", "1 centavo e 30 dobras (PERGUNTAS-SEM-RESPOSTA.md)"),
    ] + list(N_JUNTAR),
)

C["2026-11-19"] = dict(
    titulo="Bitcoin depois do 'alerta': o que mudou desde fevereiro",
    x=dict(
        estrutura="E", mecanica="necrologio",
        tweets=[
            "Tanaka, lembra do alerta do bitcoin?\n\nFevereiro. Título em caixa alta: \"Morte do bitcoin?\"\n\n"
            "Agora é abrir o arquivo e ver o que envelheceu bem.",
            "Todo alerta tem prazo de validade.\n\n"
            "O de fevereiro tinha argumentos. O vídeo pega cada um e põe o dado de hoje do lado.\n\n"
            "O que se confirmou fica. O que não se confirmou, a gente admite.",
            "Laudo do alerta de fevereiro, item por item:\n\n→ o argumento\n→ o que aconteceu desde então\n"
            "→ se ele ainda vale\n\nSem torcida contra nem a favor. Bitcoin não lê comentário.",
            "E uma pergunta que apareceu nos comentários:\n\n\"Posso perder mais do que investi?\"\n\n"
            "Comprando à vista, o máximo que se perde é o que se colocou. Com alavancagem, é outra história.",
            "Bitcoin já morreu tantas vezes que merecia plano funerário.\n\nO alerta não era sobre a morte dele.\n\n"
            "Era sobre quanto do seu dinheiro você aguenta ver no velório.",
        ],
        imagem="Coroa de flores com a faixa 'Bitcoin' e um bitcoin vivo espiando por trás.",
    ),
    ig=dict(
        slides=[
            "Bitcoin depois do 'alerta': o que mudou desde fevereiro",
            "Fevereiro: \"Morte do bitcoin?\"",
            "Cada argumento do alerta, com o dado de hoje do lado.",
            "O que se confirmou. O que não.",
            "\"Posso perder mais do que investi?\" À vista, não. Alavancado, pode.",
            "Bitcoin já morreu tantas vezes que merecia plano funerário.",
        ],
        legenda="Bitcoin depois do alerta de fevereiro: o que mudou.\n\n"
                "O vídeo pega os argumentos daquele alerta e confere cada um com os dados de hoje. Também responde a "
                "pergunta que apareceu nos comentários: dá pra perder mais do que investiu? Comprando à vista, não. Com "
                "alavancagem, a história muda.\n\n"
                "Sem previsão de preço.\n\n"
                "O que você lembra daquele vídeo?",
        imagem="Carrossel com a thumb de fevereiro e um carimbo 'revisado'.",
    ),
    numeros=[],
)

C["2026-11-21"] = dict(
    titulo="Bolha da IA: o que dizem os números",
    x=dict(
        estrutura="B", mecanica="boletim-escolar",
        tweets=[
            "Tanaka, todo mundo grita \"bolha da IA\".\n\nQuase ninguém mostra a conta.\n\n"
            "Bolha não é opinião. Deixa rastro nos números.",
            "A pergunta errada: \"quando estoura?\"\n\nNinguém sabe. Quem diz que sabe está vendendo curso.\n\n"
            "A pergunta certa: o preço dessas empresas anda junto com o lucro delas, ou na frente?",
            "Três números pra olhar:\n\n→ lucro: as empresas de IA estão ganhando mais?\n"
            "→ investimento: quanto estão gastando pra construir a IA?\n"
            "→ preço: quanto o mercado paga por cada real de lucro?",
            "Quando o preço corre muito mais que o lucro, por muito tempo, o mercado está pagando por esperança.\n\n"
            "Esperança não é crime.\n\nMas é a primeira coisa que some quando o trimestre decepciona.",
            "Boletim da IA:\n\nLucro: o vídeo mostra.\nInvestimento: o vídeo mostra.\nPreço: o vídeo mostra.\n"
            "Data do estouro: matéria em que nenhum aluno passou.",
        ],
        imagem="Boletim escolar com a matéria 'Data do estouro' em branco.",
    ),
    ig=dict(
        slides=[
            "Bolha da IA: o que dizem os números",
            "Bolha não é opinião. Deixa rastro.",
            "Lucro: as empresas de IA estão ganhando mais?",
            "Investimento: quanto estão gastando?",
            "Preço: quanto o mercado paga por cada real de lucro?",
            "Data do estouro: a matéria em que nenhum aluno passou.",
        ],
        legenda="Bolha da IA: o que dizem os números de lucro, investimento e preço das empresas de inteligência "
                "artificial.\n\n"
                "Quando o preço corre na frente do lucro por muito tempo, o mercado está pagando por esperança. O vídeo "
                "mostra onde estamos, sem prever topo nem data.\n\n"
                "Bolha não é opinião. Deixa rastro.\n\n"
                "Você acha que é bolha? Com base em quê?",
        imagem="Carrossel com três gráficos simples (lucro, investimento, preço) e o boletim no fim.",
    ),
    numeros=[],
)

# ------------------------------------------------------------------ semana 23/11
C["2026-11-23"] = dict(
    titulo="Reserva de emergência: onde deixar e onde não deixar",
    x=dict(
        estrutura="A", mecanica="manual-invertido",
        tweets=[
            "Tanaka, reserva de emergência não é investimento.\n\nÉ extintor.\n\n"
            "E extintor trancado no cofre não apaga incêndio.",
            "Onde deixar: lugar com liquidez diária, rendendo perto de 100% do CDI e com garantia do FGC dentro dos "
            "limites.\n\nTrês critérios. Na ordem: sair rápido, não perder, render.",
            "Manual pra reserva que não serve na hora:\n\n→ coloque em aplicação com carência\n"
            "→ ou em ação, que oscila\n→ ou deixe parada na conta, sem render\n\n"
            "Extintor tem que estar perto, cheio e funcionando.",
        ],
        imagem="Extintor dentro de um cofre trancado.",
    ),
    ig=dict(
        slides=[
            "Reserva de emergência: onde deixar e onde não deixar",
            "Deixar: liquidez diária, perto de 100% do CDI, FGC.",
            "Não deixar: carência, ação, conta parada.",
            "Reserva é extintor, não investimento.",
        ],
        legenda="Reserva de emergência: onde deixar e onde não deixar.\n\n"
                "Deixar: aplicação com liquidez diária, rendendo perto de 100% do CDI e com cobertura do FGC dentro dos "
                "limites. Não deixar: aplicação com carência, ativo que oscila e conta corrente parada.\n\n"
                "Reserva é extintor. Precisa estar perto e funcionando.\n\n"
                "Se precisasse amanhã, você sacava em quanto tempo?",
        imagem="Reels com o Short; capa com o extintor no cofre.",
    ),
    numeros=[],
)

C["2026-11-24"] = dict(
    titulo="Dividendos mensais com a Selic caindo: o que acontece",
    x=dict(
        estrutura="D", mecanica="eco-do-gatilho (vizinho)",
        tweets=[
            "Tanaka, quando a Selic cai, quem perde?\n\nA renda fixa nova paga menos. Até aí, todo mundo sabe.\n\n"
            "O que pouca gente olha é o que acontece com quem vive de dividendo.",
            "Antes: com juro alto, a renda fixa paga bem sem esforço.\n\n"
            "Dividendo precisa competir com isso.\n\nJuro alto é o vizinho que faz churrasco toda semana. "
            "Ninguém aparece na sua festa.",
            "Depois: com juro em queda, o vizinho diminui o churrasco.\n\nO dinheiro procura renda em outro lugar.\n\n"
            "Parte dele pode ir pra FII e ação pagadora de dividendos. Pode.\n\n"
            "Se foi assim nas outras vezes, o histórico do vídeo mostra.",
            "E tem o efeito dentro das empresas e dos fundos:\n\n→ dívida mais barata ajuda o lucro\n"
            "→ FII de papel atrelado ao CDI recebe juros menores\n→ FII de tijolo depende do aluguel, não da Selic",
            "Selic caindo não é boa nem má notícia pra renda.\n\nÉ mudança de vizinho.\n\n"
            "O vídeo mostra, com o histórico, quem fez festa e quem perdeu convidado das outras vezes.",
        ],
        imagem="Dois quintais vizinhos: um churrasco minguando, o outro começando a encher.",
    ),
    ig=dict(
        slides=[
            "Dividendos mensais com a Selic caindo: o que acontece",
            "Juro alto: a renda fixa faz churrasco toda semana.",
            "Juro em queda: o dinheiro procura renda em outro lugar.",
            "FII de papel atrelado ao CDI recebe menos. FII de tijolo depende do aluguel.",
            "Empresas com dívida pagam menos juros. O lucro agradece.",
            "Cada renda reage de um jeito. O histórico mostra como.",
        ],
        legenda="Dividendos mensais com a Selic caindo: o que acontece com dividendos, FIIs e renda fixa quando o juro "
                "cai.\n\n"
                "A renda fixa nova paga menos. FII de papel atrelado ao CDI recebe menos juros. Empresas endividadas "
                "respiram. O vídeo mostra, com o histórico, como cada renda reagiu nos ciclos anteriores.\n\n"
                "Não é previsão. É memória.\n\n"
                "Sua renda depende de qual vizinho?",
        imagem="Carrossel com os dois quintais; slide 6 com uma linha do tempo dos ciclos de juros.",
    ),
    numeros=[],
)

C["2026-11-25"] = dict(
    titulo="Taxa de administração do ETF: quanto tira em 10 anos",
    x=dict(
        estrutura="A", mecanica="conta-rapida",
        tweets=[
            "Tanaka, taxa de 1,5% ao ano parece pouco.\n\nEm 10 anos, não é.",
            "Conta no guardanapo, em cada R$ 100 mil, sem contar rendimento:\n\n"
            "→ taxa de 0,5% ao ano: cerca de R$ 4,9 mil ficam pelo caminho\n→ taxa de 1,5% ao ano: cerca de R$ 14 mil",
            "Um ponto percentual de diferença.\n\nQuase o triplo de dinheiro com o gestor.\n\n"
            "A taxa não chega como boleto. Por isso ninguém reclama.",
        ],
        imagem="Guardanapo de bar com as duas contas escritas à caneta.",
    ),
    ig=dict(
        slides=[
            "Taxa de administração do ETF: quanto tira em 10 anos",
            "0,5% ao ano: cerca de R$ 4,9 mil em cada R$ 100 mil.",
            "1,5% ao ano: cerca de R$ 14 mil.",
            "A taxa não chega como boleto. Sai do patrimônio.",
        ],
        legenda="Taxa de administração do ETF: quanto tira em 10 anos.\n\n"
                "Na conta simples, em cada R$ 100 mil e sem contar rendimento, 0,5% ao ano levam cerca de R$ 4,9 mil. "
                "A de 1,5% leva cerca de R$ 14 mil. Um ponto de diferença, quase o triplo de mordida.\n\n"
                "A taxa não manda boleto. Sai do patrimônio, todo dia.\n\n"
                "Você sabe a taxa do seu ETF?",
        imagem="Reels com o Short (corte do longo de 17/11); capa com o guardanapo.",
    ),
    numeros=[
        arq("100", CAL, "FII ou aluguel: quanto rende R$ 100 mil em cada um"),
        conta("4,9", "100000 * (1 - 0.995 ** 10) / 1000", "R$ 100 mil, 0,5% ao ano, 10 anos (CALENDARIO 25/11 e 11/11)"),
        conta("14", "100000 * (1 - 0.985 ** 10) / 1000", "R$ 100 mil, 1,5% ao ano, 10 anos (CALENDARIO 25/11 e 11/11)"),
    ],
    corte_de="2026-11-17",
)

C["2026-11-26"] = dict(
    titulo="Fundos imobiliários caíram em 2026: e a renda deles?",
    x=dict(
        estrutura="D", mecanica="contraste",
        tweets=[
            "Tanaka, as cotas de FII caíram em 2026.\n\nA pergunta que importa não é quanto caiu a cota.\n\n"
            "É se o aluguel caiu junto.",
            "Cota e rendimento são coisas diferentes.\n\nCota é o preço que o mercado paga hoje.\n\n"
            "Rendimento é o aluguel ou o juro que o fundo recebeu e repassou.\n\nUm pode cair sem o outro.",
            "O vídeo separa os dois:\n\n→ o que aconteceu com as cotas\n→ o que aconteceu com os rendimentos distribuídos\n\n"
            "O que caiu, e o que não caiu.",
            "É como o preço do apartamento no prédio.\n\nO vizinho vendeu barato e o seu \"valor\" caiu.\n\n"
            "Mas o inquilino continua pagando o aluguel no mesmo dia de sempre.",
            "Cota caindo assusta quem olha a tela.\n\nRendimento caindo é o que machuca quem vive da renda.\n\n"
            "Saber qual dos dois caiu muda a conversa inteira.",
        ],
        imagem="Placa de 'vende-se' barata no prédio e um inquilino pagando o aluguel na porta ao lado.",
    ),
    ig=dict(
        slides=[
            "Fundos imobiliários caíram em 2026: e a renda deles?",
            "Cota: o preço que o mercado paga hoje.",
            "Rendimento: o aluguel ou juro repassado.",
            "Um pode cair sem o outro.",
            "O vídeo separa: o que caiu e o que não caiu.",
            "O vizinho vendeu barato. O inquilino continua pagando.",
        ],
        legenda="Fundos imobiliários caíram em 2026. E a renda deles?\n\n"
                "Cota e rendimento são coisas diferentes: a cota é o preço de hoje, o rendimento é o aluguel ou juro "
                "repassado. O vídeo separa o que caiu do que não caiu, sem indicar fundo.\n\n"
                "O vizinho vendeu barato. O inquilino continua pagando.\n\n"
                "No seu extrato, caiu a cota ou o rendimento?",
        imagem="Carrossel com duas linhas (cota e rendimento) que se separam no slide 4.",
    ),
    numeros=[],
)

C["2026-11-28"] = dict(
    titulo="Tesouro Direto na reserva de emergência: Selic, CDB ou conta",
    x=dict(
        estrutura="C", mecanica="atendimento-ao-cliente",
        tweets=[
            "Tanaka, sua reserva está na conta corrente?\n\nEla está segura.\n\nE perdendo pra inflação todo santo dia.",
            "Três candidatos pra guardar a reserva:\n\n→ Tesouro Selic\n→ CDB com liquidez diária\n→ conta remunerada\n\n"
            "O vídeo faz a conta líquida de cada um, com o imposto e o prazo de saque.",
            "Tesouro Selic: garantido pelo Tesouro Nacional, saque em dia útil.\n\n"
            "CDB de liquidez diária: rende o CDI contratado, com FGC nos limites.\n\n"
            "Conta remunerada: depende de quanto o banco decide pagar.",
            "— Qual dos três rende mais?\n— Depende da taxa de cada um, no dia.\n— E qual é o mais seguro?\n"
            "— Os três servem pra reserva. Inseguro é deixar parada na conta sem render.",
            "Reserva boa é chata.\n\nNão sobe, não cai, não dá assunto no churrasco.\n\n"
            "Se a sua dá assunto, ela não é reserva.",
        ],
        imagem="Cofrinho bocejando numa mesa de churrasco animada.",
    ),
    ig=dict(
        slides=[
            "Tesouro Direto na reserva de emergência: Selic, CDB ou conta",
            "Conta parada: segura e perdendo pra inflação.",
            "Tesouro Selic: garantia do Tesouro Nacional.",
            "CDB de liquidez diária: FGC nos limites.",
            "Conta remunerada: depende do que o banco paga.",
            "Reserva boa é chata. Se dá assunto no churrasco, não é reserva.",
        ],
        legenda="Tesouro Direto na reserva de emergência: Tesouro Selic, CDB de liquidez diária ou conta "
                "remunerada?\n\n"
                "O vídeo faz a conta líquida de cada opção, com imposto, prazo de saque e garantia (Tesouro Nacional ou "
                "FGC). Sem indicar banco nem corretora.\n\n"
                "Reserva boa é chata. Não dá assunto no churrasco.\n\n"
                "A sua reserva dá assunto?",
        imagem="Carrossel com o cofrinho bocejando; slides 3 a 5 em três cores.",
    ),
    numeros=[],
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
        {"texto": "lidera as buscas de investimento", "arquivo": CAL_CSV,
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
