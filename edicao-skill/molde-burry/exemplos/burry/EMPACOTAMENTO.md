# Empacotamento: Burry × Barsi, o mesmo cobre (teste A/B, 3 pares)

Vídeo final: 18:50. Todo número abaixo foi conferido em `final.json`. As falas usadas estão entre aspas, com o segundo em que aparecem.

- 0:15 "está valendo quase 20 mil reais"
- 0:26 "vale mais ou menos hoje R$ 2.900"
- 0:46 "a diferença chegou a R$ 17.000 para cada R$ 10.000 investidos"
- 1:14 "mais de 40% mais caro" (em dólar)
- 3:27 "o forno da Paranapanema refinou zero tonelada na Bahia"
- 15:40 "É o zero lá do começo" e 16:53 "se o zero virou algum número" (o loop fecha)

## 1. Títulos

```
titulo_A: "Mesmo cobre: dobrou na mina do Burry, derreteu na do Barsi"   (58 car.)  frame: revelacao
  hipótese: os dois nomes conhecidos mais o contraste de verbos puxam o clique sem precisar de número. O R$ fica na thumb.
titulo_B: "R$ 10 mil: quase 20 na do Burry, 2.900 na do Barsi"           (50 car.)  frame: revelacao
  hipótese: molde vencedor do canal (R$ âncora + ativo nomeado). É literalmente a fala de 0:09 a 0:26. O R$ fica só no título.
titulo_C: "O cobre subiu 40% e só a mina do Burry subiu junto"           (50 car.)  frame: revelacao
  hipótese: paradoxo (a commodity sobe e alguém perde). O Barsi fica fora do título e entra pela thumb.
recomendado: B
```

**Por que aposto no B.** É o único dos três que o vídeo prova sem interpretação: a fala de 0:09 a 0:26 é o próprio título. Isso importa porque neste canal CTR alto costuma vir com conversão baixa. O B não promete nada que o bloco 1 não pague, então a retenção não desaba. Ele também segue o molde que venceu antes (R$ âncora + nomes que o Tanaka reconhece nas 5 primeiras palavras). O A é o de maior risco de CTR bom com retenção ruim, porque "derreteu" é mais forte que a fala.

Não entra em nenhum título: "plot twist", compre ou vale a pena, opinião sobre ERO/PMAM3/VALE3, "Barsi errou" ou "Barsi vendeu".

## 2. Thumbs feitas à mão (A e B, mesmo fundo)

**Fundo (A e B):** foto de fundição com cobre derretido sendo vazado, laranja incandescente sobre o preto. O lado esquerdo fica escurecido em uns 60% pra segurar o texto. Tem que ser foto genérica de banco de imagens, não a planta da Paranapanema: o forno dela está desligado, e mostrá-lo aceso seria afirmação falsa. O cobre derretido serve de pista visual pro "derreteu" e pro forno, sem repetir o dado.

**Quem aparece (A e B, idênticos):** recortes reais do Burry e do Barsi à direita, lado a lado, ocupando uns 45% da largura. Burry à esquerda do par, Barsi na ponta. O Denis fica de fora das duas. O clique aqui vem dos dois rostos lendários, e com o Denis seriam 3 pessoas mais o texto, acima do limite de 3 elementos. Como A e B têm o mesmo fundo e as mesmas pessoas, a comparação entre elas mede só o texto. A presença do Denis é testada na C.

### Thumb A: narrativa

| Linha | Texto exato | Cor |
|---|---|---|
| 1 | MESMO COBRE, | branco |
| 2 | MESMA ESTRADA | branco |
| 3 | R$ 17 MIL DE DIFERENÇA | verde |

- **O que a thumb diz e o título A não diz:** o tamanho do buraco em R$, e que as duas estão na mesma estrada (o caminhão da Bahia).

### Thumb B: número gigante

| Elemento | Texto exato | Cor e tamanho |
|---|---|---|
| Kicker | O FORNO REFINOU | branco, curto, no alto |
| Número | ZERO | verde neon, meia tela |

- **O que a thumb diz e o título B não diz:** o porquê. O título dá o placar em R$, a thumb dá o mistério da causa.
- **Onde a lacuna fecha:** a fala de 3:27, e de novo nos callbacks de 15:40 e 16:53.
- **R$:** a thumb B não tem R$, porque ele está no título B.

## 3. Prompt pro "Receber sugestões" do Studio (thumb C)

```
Crie uma miniatura para este vídeo, toda em português do Brasil. Não use nenhuma palavra em inglês. NÃO inclua documentos, boletos, gráficos com legenda, relatórios nem papéis com texto. Use no máximo 3 palavras grandes em caixa alta, "E O BARSI?", mais o número "R$ 17 MIL" (dezessete mil reais, nenhum outro valor) em verde neon, bem grande. Mostre à direita o apresentador do vídeo com as duas mãos na cabeça, em choque. Ele é a única pessoa na imagem: não desenhe outras pessoas reais. Ao fundo, cobre derretido laranja numa fundição escura. Fundo escuro, alto contraste, no máximo 3 elementos.
```

- **Antes de subir:** confira se o número saiu "R$ 17 MIL". Em 25/09 o gerador já inventou valor. Se ele só descrever em texto, mande "gere as imagens agora".
- **Rosto:** o rosto do Denis na C vai ser sintético (semelhança gerada), o que pede a marcação de conteúdo alterado. Se preferir evitar, use o recorte real do Denis sobre o fundo gerado.
- **O que a thumb diz e o título C não diz:** o Barsi e o custo em R$. O título C só cita o Burry.

## 4. Pares do teste

| Par | Título | Thumb | O que testa |
|---|---|---|---|
| A | Mesmo cobre: dobrou na mina do Burry, derreteu na do Barsi | A: narrativa, R$ 17 MIL | nomes + contraste de verbos |
| B | R$ 10 mil: quase 20 na do Burry, 2.900 na do Barsi | B: O FORNO REFINOU ZERO | R$ âncora no título + mistério na thumb |
| C | O cobre subiu 40% e só a mina do Burry subiu junto | C: Studio, E O BARSI? + R$ 17 MIL, Denis | paradoxo + callback, Denis na foto, gerador × mão |

Em cada par, o R$ aparece num lugar só.

## Checklist do playbook

| # | Pergunta | Resposta |
|---|---|---|
| 1 | Saiu de dado exclusivo do roteiro? | Sim. O par Ero × Paranapanema e o caminhão da Bahia só existem neste vídeo. |
| 2 | Nome reconhecível nas 5–8 primeiras palavras? | Sim nos três (Burry/Barsi). Sem ticker. |
| 3 | Custo no bolso? | B no título. A e C na thumb (R$ 17 mil). |
| 4 | Leigo entende e o iniciado vê surpresa? | Sim. "Mina" e "forno" não são jargão. |
| 5 | Sem pergunta binária, culpado negado ou "a verdade sobre"? | Sim. O "E O BARSI?" da C é pergunta aberta, não binária. |
| 6 | Texto da thumb com 1–4 palavras e dizendo o que o título não diz? | B e C sim. A tem 8 palavras: ver CONFLITO PLAYBOOK 1. |
| 7 | R$ em um só lugar? | Sim, nos três pares. |
| 8 | No máximo 3 elementos, Denis em reação ativa? | Elementos: sim. Denis: só na C. Ver CONFLITO PLAYBOOK 2. |
| 9 | Fala do bloco 1 prova o título em 15s? Desconhecido entende em 2s? | Ver seção seguinte. O pacote diz "cobre, Burry, Barsi, um ganhou, outro perdeu". |
| 10 | Checagem factual? | Ver as notas de risco. |
| 11 | 3 thumbs com 1 "segura"? | Sim. A é a segura, no padrão do canal. |
| 12 | Título no ar = título aprovado? | Conferir no Studio na hora de subir. |

**CONFLITO PLAYBOOK 1:** "texto da thumb 1–4 palavras" × o padrão A narrativa (2 linhas + 1 linha de número). A thumb A fica com 8 palavras. Se o Denis quiser cumprir o limite, a versão mínima é "MESMO COBRE" / "R$ 17 MIL". O Denis decide.

**CONFLITO PLAYBOOK 2:** "Denis em reação ativa" × a escolha de Burry e Barsi nas thumbs A e B. Tirei o Denis de propósito para não passar de 3 elementos. A thumb C mede a diferença. O Denis decide.

## Prova nos primeiros segundos (título recomendado B)

- **cumpre_nos_15s:** "Pensa em 10 mil reais, 12 meses atrás, na mineradora que o Michael Burr [...] acabou de comprar hoje, está valendo quase 20 mil reais." (0:09–0:19), seguido de "Os mesmos 10 mil reais na [...] Paranapanema, empresa que o velho Barsi é acionista, vale mais ou menos hoje R$ 2.900." (0:20–0:28)
- **Ressalva:** o vídeo abre com 9 s de meta ("Depois de uma temporada fora em Jamaica…"). Por isso a metade Burry cai dentro dos 15 s e a metade Barsi só termina em 0:28. O título continua certo; quem atrasa é a abertura.
- **gap_fecha_em:** bloco 0 (o placar, 0:09–0:46). O "zero" da thumb B fecha no bloco 1 (3:27).

## Notas de risco factual

- **"na do Barsi":** o Barsi tem pouco mais de 1% da Paranapanema (fala de 4:34). "A do Barsi" é a mesma abreviação que a cartela do roteiro usa, "(a do Barsi)". Se o Denis achar que isso passa a ideia de dono, a troca é "na Paranapanema do Barsi", que também é curta.
- **"na mina do Burry":** ele comprou uma posição em 21/09, e o dinheiro dobrou nos 12 meses anteriores. Por isso os títulos dizem que o dinheiro dobrou "na mina", nunca "com o Burry".
- **"subiu 40%" (título C):** a fala diz "mais de 40%… em dólar". O título solta o "em dólar". Isso é aceitável porque o preço do cobre é cotado em dólar, mas é um qualificador que caiu.
- **Aviso sobre memes:** se entrar insert de meme, nada na janela 0:08–0:20. O vídeo já está fechado, então vale só pra cortes e reedições.
