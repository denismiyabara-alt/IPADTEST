# Esteira social: do calendário de vídeos aos posts de Instagram e X

Para cada vídeo do calendário oficial, `pautas-canal/CALENDARIO.csv` (v3, aprovado em 03/10/2026: 23 longos e 16
Shorts), a esteira gera **um card 🎬**. O `CALENDARIO-8-SEMANAS.csv` (v2) virou histórico. Cada card tem:
- o carrossel do Instagram, com a capa e os slides;
- a legenda;
- de 3 a 5 posts do X (A, B, C…).

Esse é o formato que o **juiz-post** espera (`agentes/juiz-post.md`, a cópia do Mac). São **39 cards**, todos com
status `rascunho`. Nada aqui publica nada.

**v3:** entram os 6 episódios da Série Renda Mensal e 4 Shorts derivados (o 6º Short fica para 30/11, fora da janela),
mais o Tesouro antes do Copom (03/11). Os textos saem de `pautas-canal/serie/SERIE-RENDA-MENSAL.md`,
`serie/MOLDE-TESOURO-COPOM.md` e, no Ep. 1, do briefing `pautas-canal/briefings/2026-10-14-etf-dividendos-mensais-briefing.md`.
No Ep. 1 e no Short dele, o número do briefing vem **só** da seção "4. DADOS CONFERIDOS" (há um teste para isso), e o
que está em "A CONFERIR" vira `[CHECAR: …]`. DIVD11 e DIVO11 aparecem como prova da conta, nunca como escolha.
- **Títulos provisórios:** os 11 títulos `provisório` da série levam a marca **"título provisório: atualizar depois do
  empacotador/A-B"** no frontmatter, no cabeçalho e no INDICE. O texto do card não depende das palavras do título.
- **Cards que saíram:** ficam em `cards/_arquivo/` (README com o motivo). São as 7 pautas fora do nicho, as 2 que foram
  para dezembro (ETFs de 06/10 e TRXF11), o pós-Copom (trocado pelo pré) e as versões antigas das 3 pautas que mudaram
  de data ou de título (27/10, 03/11 → 05/11, 12/11 → 06/10).

```
calendário oficial (CALENDARIO.csv, v3) ──► gerar_cards.py + conteudo.py ──► cards/*.md + INDICE.csv
   ──► autoexame + gate de qualidade ──► renderizar PNGs ──► juiz-post (APROVADO só com 9-10 e nenhum eliminatório)
   ──► leitor-frio (PNGs + legenda; PASSA com zero trava na capa) ──► Denis aprova ──► publicação
```

## Como rodar

```bash
cd esteira-social
python3 gerar_cards.py            # 39 cards, INDICE.csv, GATE-RELATORIO.md e AUTOEXAME.md
python3 gerar_cards.py --checar   # só o autoexame; sai com 1 se algum card falhar
python3 -m pytest -q tests/       # 336 testes; os de gate pulam se o gate não for encontrado
```

- **Gerador:** usa só a biblioteca padrão. Os testes precisam de `pytest`.
- **Gate:** é o `investir-e-cocar/pipeline/gate_qualidade.py`, importado sem alteração. Para apontar outro, use
  `--gate CAMINHO` ou a variável `IC_GATE`.
- **Texto:** fica em `conteudo.py`, escrito à mão, um bloco por vídeo, com a chave `data|formato`, porque o v3 tem longo e Short no mesmo dia. Se faltar o texto de um vídeo, ou se o título
  mudar no calendário, o gerador para com erro.
- **`agentes/`:** é a cópia do Mac. A esteira não mexe lá.

## O card que o juiz-post recebe

Arquivo: `cards/<data do vídeo>-<slug>.md`.

| seção | conteúdo |
|---|---|
| frontmatter | id, `tipo: 🎬 vídeo do canal`, status, juiz, depois (`leitor-frio`), vídeo, temas, mensagem da capa, estrutura, mecânica, datas de publicação, pendências, PNGs |
| **PARA O JUIZ-POST** | o carrossel, a legenda, as hashtags e os posts do X (detalhe abaixo) |
| **PARA O LEITOR-FRIO** | os PNGs em ordem, a legenda e a **mensagem pretendida da capa**, que quem chama compara com "a capa quer me dizer" |
| FONTES E NÚMEROS | origem de cada número e de cada afirmação de ranking (não vai no post) |
| PENDÊNCIAS | `[CHECAR]` e os PNGs a renderizar |
| PUBLICAÇÃO | datas e o destino do link do vídeo. Fica fora do julgamento e não é texto do post |
| `---JSON---` | o mesmo conteúdo em JSON, com a chave `tweets` que o pipeline usa |

Detalhe da seção PARA O JUIZ-POST:
- **Carrossel:** 5 slides no longo; 4 ou 5 no Short. Cada slide traz o texto, a imagem e o caminho do PNG.
- **Legenda:** de 200 a 500 caracteres, mais as hashtags do tema.
- **Posts do X:** 4 ou 5 no longo, 3 no Short.

**Imagens (item 4, Prova):**
- A capa do carrossel e o post A usam a **thumbnail do vídeo no YouTube**, a regra do card 🎬 (Denis, 30/09).
- O slide 2 leva o **print legível e do dia** da fonte oficial que o calendário manda conferir, ou nenhuma imagem.
- Nenhum card sugere foto de banco de imagens ou imagem de IA, porque isso elimina o card.

**PNGs:** ficam em `esteira-social/render/<id>/slide-N.png` e `post-A.png`. **Ainda não existem.** O juiz-post abre
cada PNG (passo 4), então é preciso renderizar antes de chamar o juiz.

## O que o autoexame mede (e os testes exigem zero problemas)

`cards/AUTOEXAME.md` aplica a cada card os critérios do juiz-post e do leitor-frio que dá para medir no texto.

**Eliminatórios do juiz-post:**
- **Afirmação absoluta:** "só", "somente", "apenas", "nunca", "todo", "tudo", "ninguém", "sempre", "nenhum"…
- **CTA ou link:** "link", "bio", "siga", "comenta", "salva", "compartilha", URL, @.
- **Palavras e listas:** palavra proibida, "Você sabia", "plot twist", ✅🚀💡.
- **Números:** número sem fonte e conta que não fecha. Cada número vem da linha do calendário ou de `numeros`
  (trecho literal ou conta refeita).
- **Afirmações de ranking:** "top 10", "3º melhor" e "mais buscado" precisam de trecho literal do calendário, dos
  TEMAS/TERMOS ou do `auditoria-canal/RELATORIO.md`.

**Capa (item 3 e passo 1 do leitor-frio):** uma ideia, até 10 palavras, no máximo 1 número e nenhuma palavra técnica.

**Leitor-frio nos slides:**
- até 3 números por slide;
- frase de até 25 palavras;
- slide de até 140 caracteres, para não estourar o PNG;
- **todo jargão explicado no próprio slide, entre parênteses.** Exemplos: "ETF (fundo vendido na bolsa)", "FGC
  (garantia que devolve o dinheiro se o banco quebrar)", "marcação a mercado (o preço se você vendesse hoje)".

**X:**
- cada post funciona sozinho: jargão explicado nele mesmo, até 280 caracteres, sem hashtag nem emoji;
- o post A abre com "Tanaka," e tem até 8 palavras na 1ª linha;
- o post A tem no máximo 1 número; os outros, até 4.

**Voz:** a legenda abre com "Tanaka,". Nenhuma mecânica de piada aparece mais de 5 vezes. As estruturas A-E ficam
entre 7 e 8 cada. Nem a estrutura nem a mecânica se repetem em dois cards seguidos.

**Regras do canal:**
- nenhuma recomendação de ativo nem corretora;
- sem fonte nem disclaimer no corpo do post;
- hashtags só do tema do vídeo, de 5 a 10.

**O que o autoexame não mede** fica como risco por card, na Parte 2 do AUTOEXAME.md:
- **item 1, Pauta:** o juiz elimina finança pessoal básica e tema gringo sem ponte com o bolso;
- **item 2, Voz + piada:** um carrossel que explica em vez de reagir vale no máximo 1;
- **item 4:** a qualidade real da thumbnail.

## Decisões e conflitos

- **[CHECAR]:** o Denis preenche na publicação, e a marca **não elimina** o card (decisão do Mac). O contrato do
  juiz-post não fala em `[CHECAR]`, mas o juiz julga "o que o Tanaka vê". Um `[CHECAR: …]` visível no PNG pode ser lido
  como texto quebrado ou número sem fonte. No v3 são cinco cards: o Ep. 1 (14/10), 27/10, 28/10 (Short), 03/11 e o
  Ep. 6 (25/11).
- **CTA para o vídeo:** o pedido original queria CTA. O juiz-post elimina CTA e link. Por isso o texto julgado não tem
  CTA nem link. O destino do link (bio do Instagram e, no X, uma resposta à parte depois da aprovação) está na seção
  PUBLICAÇÃO, fora do julgamento.
- **Um card por vídeo, não por rede:** o contrato define o card como carrossel + legenda + posts. As duas redes
  continuam cobertas, agora dentro do mesmo card.
- **Shorts:** o contrato não tem Reels. Os Shorts também viram carrossel, de 4 ou 5 slides, com a thumbnail do Short.
- **Arquivos que o juiz lê no Mac e que não estão aqui:** `pipeline/campeoes_ig.md` e `pipeline/voz_ig_denis.md`.
  A voz foi escrita pelos briefs e pelas memórias, sem essas duas réguas.
