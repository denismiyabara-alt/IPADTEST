# Esteira social: do calendário de vídeos aos posts de X e Instagram

Para cada vídeo do `pautas-canal/CALENDARIO-8-SEMANAS.csv` (v2: 21 longos e 16 Shorts), a esteira gera **dois cards**:
um de X e um de Instagram. Isso dá **74 cards**, todos com status `rascunho`, prontos para o **juiz-post**.
Nada aqui publica nada.

```
calendário (CSV v2) ──► gerar_cards.py + conteudo.py ──► cards/*.md + INDICE.csv ──► gate de qualidade
        ──► juiz-post (nota por card) ──► Denis aprova ou devolve ──► publicação manual (X e IG)
```

## Como rodar

```bash
cd esteira-social
python3 gerar_cards.py                 # gera os 74 cards, o INDICE.csv e roda o gate (GATE-RELATORIO.md)
python3 gerar_cards.py --checar        # só confere números e limites, sem gravar
python3 gerar_cards.py --sem-gate      # gera sem o gate
python3 -m pytest -q tests/            # 306 testes; os de gate pulam se o gate não for encontrado
```

- **Só biblioteca padrão** no gerador. Os testes precisam de `pytest`.
- **O gate** é o `investir-e-cocar/pipeline/gate_qualidade.py` (branch `gate-qualidade`), importado sem alteração.
  - O caminho padrão é `/home/user/investir-e-cocar/pipeline/`. No Mac, use `--gate ~/investir-e-cocar/pipeline/gate_qualidade.py`
    ou a variável `IC_GATE`.
  - Ele aceita texto solto pelo stdin (`gate_qualidade.py - --titulo ... --data ...`). A esteira usa o import, e um teste confere
    que a linha de comando dá o mesmo veredito.
- **O texto dos posts** está em `conteudo.py`, escrito à mão, um bloco por vídeo. O gerador só monta o card.
  - Se o calendário ganhar um vídeo sem texto, o gerador **para com erro**, em vez de gravar um template vazio.
  - Se um título mudar no calendário, o gerador também para, para o texto não sair desalinhado com o vídeo.

## O que cada card tem

Arquivo: `cards/<data do vídeo>-<slug do título>-<x|ig>.md`. A data no nome é a **do vídeo**, para o par X/IG ficar junto.
A data de publicação está no frontmatter.

O formato segue o do `ic-copywriter` (`.claude/scheduled-tasks/ic-copywriter/SKILL.md`): cabeçalho com status, um bloco por
tweet, sugestão de imagem e o bloco `---JSON---` … `---FIM---` com a chave `tweets`. É esse bloco que o pipeline usa para
reconhecer um card de thread válido (`project_gate_fila_copywriter_ago2026`).

| campo | X | Instagram |
|---|---|---|
| **frontmatter** | id, rede, formato, status, juiz, data_publicacao, horario, relativa_ao_video, video_*, assunto, termo_busca, gancho, estrutura (A-E), mecanica, pendencias_checar | o mesmo, sem estrutura e mecânica |
| **corpo** | longo: thread de 5 posts. Short: thread de 3 posts | longo: carrossel de 6 slides. Short: Reels com 4 telas |
| **gancho** | 1ª linha do tweet 1, sempre "Tanaka, …" e com até 8 palavras | 1ª linha da legenda |
| **CTA para o vídeo** | numa **reply** depois do último tweet, com o link | última linha da legenda ("link na bio") |
| **hashtags** | nenhuma (o brief do X proíbe) | 10, no fim |
| **fontes e números** | seção própria, que **não vai no post** | idem |
| **pendências** | `[CHECAR: …]` que o Denis preenche antes de aprovar | idem |

**Agenda (relativa ao vídeo):**
- **Longo:** X no D+0 às 19h30, 30 minutos depois do vídeo das 19h. IG no D+1 ao meio-dia.
- **Short:** X no D+0 ao meio-dia e IG (Reels com o mesmo vídeo) no D+0 às 18h.
- **Copom (04/11):** X às 9h e IG às 10h, **antes** da decisão.

## Regras que a esteira cumpre (e os testes conferem)

- **Nenhum número inventado.** Todo número de um post precisa ter uma destas origens:
  - estar na própria linha do calendário, que é o briefing do vídeo;
  - estar declarado em `numeros`, com o **trecho literal** de `pautas-canal/` (CALENDARIO, TEMAS, TERMOS ou
    PERGUNTAS-SEM-RESPOSTA);
  - estar declarado com a **conta** que o gera. Exemplo: em 10 anos, 1,5% ao ano come `(1 − 0,985¹⁰)` ≈ 14% do patrimônio.

  O teste reabre cada arquivo, procura o trecho e refaz cada conta. Quando o número depende do dia, fica `[CHECAR: …]`,
  como manda o X-COPYWRITER-BRIEF. São só dois casos: a taxa do Tesouro Selic do dia (28/10) e a decisão do Copom (05/11).
- **Sem fonte e sem disclaimer no post** (`feedback_copywriter_sem_fonte_sem_disclaimer`). A fonte de cada número fica na
  seção "FONTES E NÚMEROS" do card, para o juiz e o Denis. O teste reprova "segundo…", "de acordo com", "Fonte:" e
  "não é recomendação".
- **Sem recomendação de ativo nem corretora.** O teste reprova "vale a pena", "melhor ação", "hora de comprar" e nomes de
  corretoras. O TRXF11 aparece só como acompanhamento neutro dos números do fundo, como o calendário pede.
- **Voz.** As threads abrem com "Tanaka," e nunca com "Fala, Tanaka" (`feedback_persona_tanaka_voice`). A promessa cabe no
  bolso de quem tem de R$ 50 mil a R$ 100 mil (`feedback_promessa_perto_do_tanaka`). Não há palavra da lista anti-IA. A
  estrutura (A-E) e a mecânica de piada **não se repetem** em duas threads seguidas.
- **Limites.** X: até 280 caracteres por post (o maior tem 217). IG: legenda de 200 a 500 caracteres; total com CTA e
  hashtags até 2.200; slide até 120.
- **Gate.** Nenhum card é bloqueado. Os avisos estão em `cards/GATE-RELATORIO.md`.

## Como o juiz-post consome os cards

> **Atenção:** não existe definição de `juiz-post` no repo `investir-e-cocar`. O `grep -ril "juiz-post"` em `.claude/`,
> `memory/` e `vault/Pipeline/`, em todas as branches, não acha nada. O contrato abaixo copia o do `juiz-roteiro`
> (`.claude/agents/juiz-roteiro.md`), que é o juiz que existe. Precisa da confirmação do Denis.

**Entrada:** só o caminho do card, como no juiz-roteiro. O juiz não sabe quem escreveu, e a justificativa do autor não conta.
- `cards/INDICE.csv` é a fila. O juiz pega os cards com `status = rascunho` e `gate_resultado != BLOQUEADO`, em ordem de
  `data_publicacao`.
- O juiz lê o **frontmatter** (contexto) e o **bloco JSON** (o texto exato que vai ao ar). As seções em Markdown são as
  mesmas informações, para leitura humana.
- A seção "FONTES E NÚMEROS" serve para o juiz checar cada número. Ela nunca vai no post.

**Saída sugerida** (mesmo molde do juiz-roteiro: item com trecho literal, ou não passa):

```
card: <id>
nota: N/10
eliminatorio: nenhum | <número sem origem · recomendação de ativo/corretora · fonte ou disclaimer no corpo ·
              palavra anti-IA · link/hashtag/emoji no corpo do X · "Fala, Tanaka" ou "Taná" · [CHECAR] pendente>
item 1 gancho para o scroll (≤ 8 palavras) ....... PASSA/FALHA — "<trecho>"
item 2 cada post planta a pergunta do próximo ..... PASSA/FALHA — "<trecho>"
item 3 número com contraste (não solto) ........... PASSA/FALHA — "<trecho>"
item 4 analogia brasileira, sem explicar a piada .. PASSA/FALHA — "<trecho>"
item 5 conta em R$ que o Tanaka aplica ............ PASSA/FALHA — "<trecho>"
item 6 fecho que alguém printaria (sem moral) ..... PASSA/FALHA — "<trecho>"
item 7 provoca resposta sem pedir (sem CTA no corpo) PASSA/FALHA — "<trecho>"
item 8 mecânica registrada aparece no texto ....... PASSA/FALHA — "<trecho>"
para_corrigir:
- item N: <o que falta, em uma frase>
```

**Depois do juiz:**
- **Nota abaixo do corte:** o card volta para reescrita em `conteudo.py`. Roda `gerar_cards.py` e os testes de novo.
- **Nota no corte ou acima:** o card vai para o Denis.
  - No pipeline atual, isso é a lista "Aprovar X" do Trello. O card do Trello começa com 🧵 e leva o bloco JSON.
  - O Denis preenche os `[CHECAR]`, troca `[LINK DO VÍDEO…]` pelo link real e aprova (lista "Aprovado X").
  - A publicação continua manual (ou pelo `ic-publish-x`). O status `publicado` é marcado à mão no INDICE, nunca por esta esteira.

## Fluxo completo

1. **Calendário:** `pautas-canal/calendario_v2.py` gera o CSV. Se a pauta mudar, ajuste o bloco do vídeo em `conteudo.py`.
2. **Cards:** `python3 gerar_cards.py`, depois `python3 -m pytest -q tests/`. Os dois têm de passar.
3. **Juiz-post:** dá a nota de cada card, citando trecho.
4. **Denis aprova:** preenche `[CHECAR]` e o link, e escolhe o horário final.
5. **Publica:** X com a thread e o link na reply. IG com o carrossel ou o Reels e a legenda com o CTA.

## O que ficou de fora, de propósito

- **Imagens prontas:** cada card traz só uma sugestão de imagem. A arte é outra etapa.
- **Link dos vídeos:** ainda não existem. Fica o marcador `[LINK DO VÍDEO: preencher na publicação]`.
- **Selic, IPCA e taxas do dia:** não estão no calendário. Os textos foram escritos sem esses números, e onde eles são o
  assunto fica `[CHECAR]`.
- **Hashtags no X:** o brief proíbe.
- **Disclaimer no IG:** a memória permite, "se necessário". Nenhum card recomenda ativo, então não foi preciso.
