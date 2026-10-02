# Livros de investimento: o que os leitores dizem (e o que dá vídeo)

Pesquisa para o canal **Investir e Coçar**. Coleta feita em 02/10/2026.
Arquivo de dados: [`resenhas.csv`](resenhas.csv) (131 linhas agregadas: livro × tema).

> Aviso rápido: nada aqui é recomendação de ativo, fundo ou corretora. Os números de 2026 vêm com fonte. Onde está escrito **"conferir"**, confira antes de gravar.

---

## (i) Método e fontes

### Como escolhi os livros

- Os 22 títulos misturam três critérios: (1) aparecem em listas de mais vendidos (a Nielsen-PublishNews de 2025 tem *A Psicologia Financeira* e *O Homem Mais Rico da Babilônia* no topo de Negócios); (2) têm muitas avaliações no Goodreads; (3) são os clássicos de investimento que o público brasileiro mais cita (Barsi, Bazin, Bastter, Suno, Cerbasi, Halfeld, Nigro).
- O site da PublishNews está **bloqueado** pelo proxy deste ambiente. Os dados de vendas vieram de resultados de busca, e não da página original. Por isso estão marcados como "conferir".
- Fora do escopo: livros de dívida e de finanças pessoais pura, como *Me Poupe!* e *Casais Inteligentes Enriquecem Juntos*.
- Bastter tem dois títulos (*Eu Quero Ser Rico* e *Filosofia Bastter.com*) porque cada um tem poucas resenhas. Suno também tem dois (Dividendos e FIIs).

### Fontes, na ordem pedida

| Fonte | O que aconteceu | Resenhas lidas |
|---|---|---|
| **Amazon Brasil** | Antes da tarefa, um teste já tinha recebido **503**. Fiz **1 nova tentativa simples** (curl, user-agent fixo, página de busca) e recebi **503** de novo, com corpo de 1,6 KB. Parei aí, sem contornar o bloqueio. | **0** |
| **Skoob** | A home (`/`) responde **302 → `/pt/home`**, que abre normalmente (200). A busca (`/pt/search`) e a página de resenhas de um livro (`/livro/resenhas/11/...`, *Pai Rico Pai Pobre*) redirecionam para **`/pt/login?callbackUrl=...`**. Ou seja, as resenhas **exigem login**. Registrei e parei, sem login e sem contorno. | **0** |
| **Goodreads** | A página de cada livro (`/book/show/ID`) responde 200 e já traz no HTML as **30 resenhas mais populares** da obra, somando todas as edições e idiomas. Em vários pedidos o site devolveu **202 com corpo vazio** (limite de taxa). Nesses casos esperei 20 a 60 s e tentei uma vez. Intervalo entre pedidos: 1,5 a 8 s. | **546** |

- Ferramentas: `curl` com um user-agent comum fixo e cookies de sessão anônima. Só leitura: sem login, sem comentário, sem publicação.
- Coletei 660 resenhas (22 livros × 30). Li as **546 em português ou inglês**, mais umas poucas em espanhol, que contei junto com as em português. As outras estavam em árabe, persa, turco, vietnamita etc., ou vazias, e ficaram de fora. Também excluí 1 spam (*Fora da Curva*).
- Codificação: li cada resenha e marquei os temas citados (elogio, crítica, dúvida ou pergunta). Uma resenha pode cair em mais de um tema. As contagens do CSV são **número de resenhas que tocam no tema**, não porcentagem do público.
- O Goodreads não deixa filtrar por idioma sem JavaScript. Por isso, nos livros estrangeiros, quase todas as resenhas são em **inglês**. Dá para ler isso como "o que o leitor do mundo pensa", não como "o que o brasileiro pensa".

---

## (ii) Livros e resenhas lidas

Nota GR = média geral da obra no Goodreads. Média lidas = média das estrelas nas resenhas que li. Como são as mais populares, puxam para os extremos.

| # | Livro | Autor | Amazon | Skoob | Goodreads lidas (pt/en) | Nota GR | Avaliações GR | Média lidas |
|---|---|---|---|---|---|---|---|---|
| 1 | Pai Rico, Pai Pobre | Robert Kiyosaki | 0 | 0 | 24 (0 / 24) | 4,08 | 764.269 | 2,79 |
| 2 | O Investidor Inteligente | Benjamin Graham | 0 | 0 | 28 (1 / 27) | 4,23 | 158.370 | 3,89 |
| 3 | Os Segredos da Mente Milionária | T. Harv Eker | 0 | 0 | 25 (3 / 22) | 4,22 | 78.000 | 2,60 |
| 4 | Do Mil ao Milhão | Thiago Nigro | 0 | 0 | 29 (28 / 1) | 3,86 | 1.917 | 3,43 |
| 5 | Investimentos Inteligentes | Gustavo Cerbasi | 0 | 0 | 30 (30 / 0) | 3,99 | 853 | 4,21 |
| 6 | O Homem Mais Rico da Babilônia | George S. Clason | 0 | 0 | 25 (2 / 23) | 4,23 | 254.420 | 3,92 |
| 7 | A Psicologia Financeira | Morgan Housel | 0 | 0 | 27 (1 / 26) | 4,27 | 367.384 | 3,63 |
| 8 | O Rei dos Dividendos | Luiz Barsi Filho | 0 | 0 | 30 (28 / 2) | 4,39 | 477 | 4,33 |
| 9 | Eu Quero Ser Rico | Bastter | 0 | 0 | 11 (10 / 1) | 3,81 | 96 | 3,91 |
| 10 | Filosofia Bastter.com | Bastter | 0 | 0 | 7 (7 / 0) | 4,28 | 75 | 4,33 |
| 11 | Guia Suno Dividendos | Tiago Reis | 0 | 0 | 30 (30 / 0) | 4,02 | 452 | 4,03 |
| 12 | Guia Suno Fundos Imobiliários | Marcos Baroni (Suno) | 0 | 0 | 18 (18 / 0) | 4,00 | 337 | 4,11 |
| 13 | Um Passeio Aleatório por Wall Street | Burton Malkiel | 0 | 0 | 30 (0 / 30) | 4,14 | 42.181 | 3,77 |
| 14 | O Jeito Peter Lynch de Investir | Peter Lynch | 0 | 0 | 27 (1 / 26) | 4,29 | 42.260 | 4,31 |
| 15 | O Pequeno Livro do Investidor de Bom Senso | John Bogle | 0 | 0 | 28 (1 / 27) | 4,15 | 27.766 | 3,74 |
| 16 | Ações Comuns, Lucros Extraordinários | Philip Fisher | 0 | 0 | 26 (3 / 23) | 4,14 | 16.932 | 4,08 |
| 17 | O Mais Importante para o Investidor | Howard Marks | 0 | 0 | 30 (2 / 28) | 4,32 | 17.221 | 4,17 |
| 18 | Os Axiomas de Zurique | Max Gunther | 0 | 0 | 28 (12 / 16) | 3,97 | 3.046 | 3,75 |
| 19 | A Bola de Neve | Alice Schroeder | 0 | 0 | 27 (0 / 27) | 4,16 | 55.428 | 3,77 |
| 20 | Fora da Curva | Bartunek, Napolitano, Moreau | 0 | 0 | 22 (21 / 1) | 3,93 | 567 | 4,23 |
| 21 | Investimentos: Como Administrar Melhor Seu Dinheiro | Mauro Halfeld | 0 | 0 | 14 (12 / 2) | 3,83 | 176 | 4,57 |
| 22 | Faça Fortuna com Ações | Décio Bazin | 0 | 0 | 30 (30 / 0) | 4,01 | 670 | 3,55 |
| | **Total** | | **0** | **0** | **546 (240 / 306)** | | | |

### O que se repete em quase todo livro

1. **"Bom para iniciante, raso para quem já leu."** É a crítica nº 1 dos livros brasileiros: Nigro 11, Suno Dividendos 8, Cerbasi 5, Bastter 4.
2. **"Cabe em uma frase / num vídeo de 15 minutos."** Aparece em Bogle (8), Babilônia (6), Housel (6), Suno (2) e Bastter (4). Para um canal de YouTube, é um convite.
3. **"Datado."** Bazin (8), Lynch (5), Fisher (5), Graham (9, salvo pelos comentários de Zweig), Halfeld e Cerbasi (3).
4. **"É biografia, cadê o método?"** Barsi (4 + 3 pedindo o método), Fora da Curva (5), Bola de Neve (3).
5. **"Autoajuda com cara de finanças."** Eker (15 menções somadas), Kiyosaki (14), Nigro (6).

---

## (iii) 15 pautas de vídeo

Em cada pauta: **Gancho** (1 frase), **Número/fato** (com fonte ou "conferir") e **Resenhas** (quantas levantam o tema, na coleta acima).

**1. "Sua casa é um passivo?" (Pai Rico, Pai Pobre)**
- Gancho: Kiyosaki diz que sua casa não é ativo. O banco concorda e manda o boleto todo mês.
- Número/fato: comparar a parcela de um financiamento com o aluguel do mesmo imóvel e com o que o dinheiro da entrada renderia a juro real de ~9% a.a. (Selic 13,75% contra IPCA de 12 meses de 4,22%; conta própria, ver fontes). Taxa atual de financiamento imobiliário: **conferir**.
- Resenhas: 8 reclamam que o livro "diz o quê, não diz o como" (5 críticas + 3 perguntas). 6 dizem que ele despreza o "pai pobre".

**2. "Guardar 10% resolve?" (O Homem Mais Rico da Babilônia)**
- Gancho: um conselho de 1926 que ainda funciona. Mas a gente fez a conta do quanto.
- Número/fato: R$ 300/mês (10% de R$ 3.000) por 30 anos dão ~R$ 206 mil a 4% real a.a. ou ~R$ 292 mil a 6% real a.a. É simulação própria, em valores de hoje, sem imposto nem taxa.
- Resenhas: 11 elogiam a regra dos 10%. 6 dizem que o livro "cabe em duas frases".

**3. "Do mil ao milhão: a conta que o título não mostra" (Thiago Nigro)**
- Gancho: quanto tempo leva, de verdade, para sair do mil e chegar ao milhão?
- Número/fato: aportando R$ 1.000/mês, o milhão chega em ~37 anos a 4% real a.a., ~30 anos a 6% e ~24 anos a 9%. R$ 1.000 aplicados uma única vez levariam ~80 anos a 9% real. Simulação própria.
- Resenhas: 2 duvidam da promessa do título. 11 acham o livro superficial. 4 elogiam justamente a parte de contas (juros e IR).

**4. "A regra dos 6% do Bazin com a Selic a 13,75%" (Faça Fortuna com Ações)**
- Gancho: Bazin mandava comprar ação com dividend yield acima de 6%. Hoje a renda fixa pós-fixada paga mais que o dobro disso, antes do IR.
- Número/fato: Selic de **13,75% a.a.** (Copom, 16/09/2026). Rendimento líquido aproximado de um título atrelado à Selic acima de 2 anos: ~11,7% a.a. (13,75% × 0,85, sem custódia; conta própria).
- Resenhas: 7 elogiam a regra dos 6%. 2 perguntam se ela ainda faz sentido. 1 confunde cash yield com DY.

**5. "Dividendo agora paga imposto? Só se você for o Barsi"** (Barsi, Bazin, Suno Dividendos)
- Gancho: depois de 30 anos, dividendo voltou a ter IR no Brasil. Calma: a régua é alta.
- Número/fato: a **Lei 15.270/2025** cria retenção de **10% na fonte** quando uma mesma empresa paga **mais de R$ 50 mil no mês** a uma mesma pessoa física, a partir de 2026. Há ainda um imposto mínimo para quem tem renda anual acima de R$ 600 mil. Detalhes: **conferir** no Perguntas e Respostas da Receita.
- Resenhas: 31 tratam de dividendos como estratégia (Barsi 11, Suno 13, Bazin 7). 1 pergunta se "renda passiva" existe, já que o dividendo sai do preço da ação.

**6. "Dá pra copiar o Barsi?" (O Rei dos Dividendos)**
- Gancho: o livro conta a vida do maior investidor pessoa física do país. Ficou faltando o manual.
- Número/fato: Barsi começou a investir no fim dos anos 1960 (fonte: sinopse do livro). Tempo de carteira é a variável que ninguém copia. Juros e inflação daquela época contra os de hoje: **conferir** séries do BCB.
- Resenhas: 4 dizem "é biografia, pouco método". 3 pedem o método (BESST, AGF). 3 perguntam se dá para replicar ou se foi sorte.

**7. "O investidor defensivo de Graham, versão Brasil 2026" (O Investidor Inteligente)**
- Gancho: Graham mandava dividir entre títulos e ações. Ele nunca viu um título pagando 9% acima da inflação.
- Número/fato: juro real aproximado de ~9,1% a.a. (Selic 13,75% contra IPCA de 12 meses de 4,22% em ago/2026; conta própria). Taxas atuais de títulos atrelados ao IPCA: **conferir** no Tesouro Direto no dia da gravação.
- Resenhas: 9 dizem que o texto é datado e que os comentários de Zweig salvam. 4 concluem "vou de fundo de índice". 5 acham o livro denso.

**8. "Fundo de índice no Brasil: o capítulo que o Bogle não escreveu" (Bogle e Malkiel)**
- Gancho: os dois livros mais famosos sobre índice foram escritos para americano. Aqui o Leão pega no ganho de outro jeito.
- Número/fato: ETF de ações na B3 paga 15% sobre o ganho e **não tem** a isenção de R$ 20 mil/mês das ações (**conferir** regra vigente). ETFs na B3 somam ~862 mil CPFs (InfoMoney; **conferir data**).
- Resenhas: 17 elogiam o índice barato (Bogle 9, Malkiel 8). 8 acham o Bogle repetitivo. 2 reclamam que o Malkiel é centrado nos EUA.

**9. "Invista no que você conhece, inclusive no celular do seu bolso?" (O Jeito Peter Lynch de Investir)**
- Gancho: Lynch dizia que o amador vê a empresa boa antes de Wall Street. Até 2020, o brasileiro comum mal tinha como comprar essa empresa.
- Número/fato: BDRs liberados para o investidor de varejo em 2020 (CVM, Resolução 3/2020; **conferir data exata**).
- Resenhas: 5 elogiam o "invista no que conhece". 5 acham o livro datado. 3 dizem que o conselho é perigoso nas mãos erradas.

**10. "Diversificar é para covardes? Zurique contra Bogle"**
- Gancho: um livro manda não diversificar. O outro manda comprar o mercado inteiro. Os dois venderam milhões.
- Número/fato: comparação didática da volatilidade de uma ação isolada contra um índice amplo (**conferir** séries da B3 para o exemplo).
- Resenhas: 8 acham Zurique arriscado ou contra a diversificação. 3 discutem se investir e especular são a mesma coisa. 9 elogiam a tese do Bogle.

**11. "O livro de finanças mais vendido do Brasil não ensina a investir" (A Psicologia Financeira)**
- Gancho: e talvez seja justamente por isso que ele vende.
- Número/fato: *A Psicologia Financeira* vendeu ~165 mil exemplares em 2025, 6º lugar geral (Nielsen-PublishNews, via busca; **conferir**).
- Resenhas: 8 elogiam "comportamento vale mais que inteligência". 6 dizem "nada de novo". 5 dizem "muita anedota, pouca psicologia". 2 sentem falta de dica prática.

**12. "Toque na cabeça e repita: isso é marketing" (Os Segredos da Mente Milionária)**
- Gancho: o livro promete mente milionária. Quem ficou milionário com ele foi quem vende o seminário.
- Número/fato: nas 25 resenhas mais populares, a média foi **2,6 estrelas**. A nota geral da obra é **4,22** (Goodreads, coleta de 02/10/2026).
- Resenhas: 15 menções somadas: 5 sobre propaganda de seminário, 6 sobre autoajuda/lei da atração, 4 sobre falta de conselho prático. 5 elogiam a ideia do "modelo de dinheiro".

**13. "Livro de 2001 contra o app do banco em 2026" (Halfeld e Cerbasi)**
- Gancho: os melhores manuais para iniciante foram escritos antes do Pix. O que mudou no mapa?
- Número/fato: o que não existia (ou era nicho) na 1ª edição: Pix (lançado em nov/2020 pelo BCB), BDR no varejo (2020), FIIs com **3,13 milhões de cotistas** (mar/2026, B3 via notícias; **conferir**), escolha do regime de IR da previdência na hora do resgate (Lei 14.803/2024; **conferir**).
- Resenhas: 27 elogiam esses livros como introdução (Cerbasi 16, Halfeld 11). 3 apontam desatualização.

**14. "Poupança x Tesouro: o primeiro capítulo de todo livro brasileiro"**
- Gancho: todo livro nacional começa batendo na poupança. Em 2026, com a Selic onde está, a surra é maior ou menor?
- Número/fato: com Selic acima de 8,5%, a poupança rende 0,5% ao mês + TR, cerca de **6,17% a.a. + TR** (regra da Lei 12.703/2012). Contra isso, Selic de 13,75%. Valor da TR: **conferir**.
- Resenhas: 4 elogiam a comparação feita por Nigro. 2 citam o tema em Halfeld e Suno FII (comparação com Tesouro).

**15. "O livro de FII que não ensina a precificar FII" (Guia Suno Fundos Imobiliários)**
- Gancho: 3 milhões de brasileiros têm FII. Quantos sabem dizer se pagaram caro?
- Número/fato: 3,13 milhões de cotistas em mar/2026 (B3, via notícias; **conferir**). A MP 1.303 caducou em 08/10/2025, e a isenção de LCI/LCA/CRI/CRA para pessoa física continuou valendo.
- Resenhas: 4 dizem que faltou análise de preço ou estratégia. 2 dizem que as partes difíceis são os fundos de papel e o IR.

---

## (iv) Proposta de série: **"O livro que você leu errado"**

**Formato.** De 8 a 12 minutos, um livro por episódio, sempre com o mesmo roteiro:

1. **A frase**: a frase mais famosa do livro, na tela (até 15 palavras, com crédito).
2. **O que o leitor entendeu**: 2 ou 3 resenhas reais, parafraseadas ("23 de 30 leitores acharam X").
3. **O que o livro disse de verdade**: contexto, ano, país, o que o autor *não* prometeu.
4. **A conta de 2026**: uma simulação simples na tela, com a fonte no canto.
5. **Veredito com selo**: ✅ *Vale* · ⚠️ *Vale com asterisco* · 🪦 *Aposentado*.
6. **Pergunta para os comentários**, que alimenta o próximo episódio.

**Regra do canal.** Nunca dizer "compre X". Dizer "a categoria Y funciona assim, e o custo é Z".
**Thumb.** Capa do livro com um carimbo de "CONFERIDO EM 2026".

| Ep. | Livro | O livro diz | A conta de 2026 diz | Por que abrir com ele |
|---|---|---|---|---|
| 1 | **Pai Rico, Pai Pobre** | "Sua casa não é um ativo." | Depende: parcela + juros do financiamento (**conferir**) contra aluguel contra o que a entrada renderia a ~9% real. Às vezes ele tem razão; às vezes, não. | É o livro mais avaliado da lista (764 mil notas) e o mais brigado nas resenhas (média 2,79 nas mais populares). |
| 2 | **O Homem Mais Rico da Babilônia** | "Guarde um décimo de tudo o que ganhar." | 10% de R$ 3.000 por 30 anos dão R$ 206 mil a R$ 292 mil (4% a 6% real). É bom, mas não é "o homem mais rico". | 11 resenhas elogiam a regra; 6 dizem que é óbvia. O vídeo responde aos dois lados. |
| 3 | **Faça Fortuna com Ações (Bazin)** | "Só compre ação com dividend yield acima de 6%." | Com Selic a 13,75%, os 6% perdem para a renda fixa antes do IR. E a Lei 15.270 cria IR sobre dividendos acima de R$ 50 mil/mês por empresa. | Une o clássico nacional a duas notícias de 2025/2026 (juros e imposto). |
| 4 | **Do Mil ao Milhão** | "Do mil ao milhão, sem cortar o cafezinho." | R$ 1.000/mês levam de 24 a 37 anos até o milhão (9% a 4% real). Com R$ 1.000 uma única vez, são ~80 anos. O cafezinho fica; o prazo assusta. | O livro brasileiro mais avaliado da lista. 11 de 29 resenhas pedem profundidade, e o episódio entrega a conta. |
| 5 | **O Investidor Inteligente** | "Divida entre títulos e ações; não especule." | No Brasil, o "título" do Graham é o Tesouro, que hoje paga juro real alto (taxa: **conferir**). O defensivo brasileiro tem vida mais fácil que o americano. Já o fundo de índice tem imposto diferente (**conferir**). | Fecha a temporada com o clássico "chato" e mostra que a parte chata é a que funciona. |

**Próximos candidatos (temporada 2):** Zurique x Bogle (pauta 10), Psicologia Financeira (11), Lynch e BDRs (9), Barsi (6), Mente Milionária (12).

---

## (v) Limitações

- **Só uma fonte de fato.** A Amazon bloqueou (503) e o Skoob exige login para resenhas. Tudo o que está aqui vem do **Goodreads**.
- **Viés de idioma.** Nos 11 livros estrangeiros, quase todas as resenhas lidas estão em inglês. Elas mostram o leitor global, não o brasileiro. As 240 resenhas em português se concentram nos autores nacionais.
- **Viés de seleção.** O Goodreads mostra as 30 resenhas **mais populares**, e não uma amostra aleatória. Resenhas longas e polêmicas sobem. Por isso a média das lidas (ex.: Kiyosaki 2,79) fica bem abaixo da nota geral (4,08).
- **Amostras pequenas.** Bastter (7 e 11) e Halfeld (14) têm poucas resenhas. Trate essas contagens como pistas, não como estatística.
- **Codificação manual.** Os temas e contagens vêm da minha leitura. Outra pessoa poderia agrupar de outro jeito. Os exemplos do CSV são paráfrases curtas ou traduções livres, não citações literais.
- **Lista de mais vendidos.** A PublishNews estava bloqueada no ambiente. A seleção dos livros combina busca, Goodreads e reputação no Brasil, e não um ranking oficial único.
- **Números de 2026.** A Selic e o IPCA vieram de notícias encontradas por busca, não das páginas do BCB e do IBGE. Confira no dia da gravação. As simulações são ilustrativas: sem IR, sem taxas, com juro real constante.

### Fontes citadas

- Selic 13,75% (Copom, 16/09/2026): <https://www.dgabc.com.br/Noticia/4347352/copom-reduz-taxa-selic-em-0-25-ponto-porcentual-para-13-75-ao-ano>
- IPCA de ago/2026 (−0,32%; 12 meses 4,22%): <https://agenciadenoticias.ibge.gov.br/agencia-sala-de-imprensa/2013-agencia-de-noticias/releases/48015-ipca-fica-em-0-32-em-agosto>
- Lei 15.270/2025 (dividendos): <https://www.demarest.com.br/receita-federal-divulga-perguntas-e-respostas-sobre-a-nova-tributacao-de-dividendos-e-altas-rendas/> · <https://dinai.capital/blog/tributacao-dividendos-2026-como-funciona-lc-15270>
- MP 1.303 caducou; tabela regressiva e isenções mantidas: <https://www.seudinheiro.com/2025/financas-pessoais/como-fica-o-imposto-de-renda-dos-investimentos-agora-que-caducou-a-mp-1-303-que-mudava-a-tributacao-julw/>
- FIIs com 3,13 milhões de cotistas: <https://www.fundsexplorer.com.br/noticias/fundos-imobiliarios-313-milhoes-investidores>
- ETFs com 862 mil CPFs: <https://www.infomoney.com.br/onde-investir/etfs-ganham-140-mil-investidores-no-ano-e-ja-somam-862-mil-cpfs/>
- Mais vendidos 2025 (Nielsen-PublishNews, via busca): <https://www.publishnews.com.br/ranking/anual/0/2025/0/0> · <https://www.publishnews.com.br/ranking-nielsen/anual/8/2025/0/0>
- Goodreads (páginas das obras): `https://www.goodreads.com/book/show/<id>`, com os ids 6383503, 42102710, 713273, 42267651, 6377031, 41104302, 57505131, 63239964, 23480566, 36402502, 37050157, 41973969, 59740387, 762462, 171127, 35385890, 10454418, 6470723, 9831191, 31948507, 6470722, 16103312.
- Sem fonte aberta nesta coleta (de memória, marcar **conferir**): lançamento do Pix (nov/2020, BCB); BDR no varejo (CVM Res. 3/2020); regra da poupança (Lei 12.703/2012); previdência com escolha do regime no resgate (Lei 14.803/2024); ETF de ações sem a isenção de R$ 20 mil.
