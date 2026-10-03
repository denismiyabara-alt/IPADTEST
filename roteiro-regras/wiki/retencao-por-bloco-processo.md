---
tags: [roteiro, retenção, analytics, processo]
updated: 2026-07-09
owner: TANAKA METRICS, SCRIPT-WRITER
---

# Processo: ligar curva de retenção real ao bloco do roteiro

> Hoje ninguém cruza "a retenção caiu nesse segundo" com "esse era o Bloco X do roteiro". Sem isso, decisão de o que funciona é achismo. Este processo fecha esse loop — roda depois de CADA vídeo publicado, com pelo menos 48h de dado acumulado.

## Passo a passo

1. **Puxar a curva de retenção por segundo** via YouTube Analytics API (`averageViewPercentage` por vídeo, e se possível a curva completa via Studio — ver `reference_yt_analytics_channel_access` na memória).
2. **Marcar os timestamps de início de cada bloco** do roteiro publicado (já temos isso no frontmatter/estrutura — cada `## BLOCO N` tem intervalo estimado tipo "0:15-2:30").
3. **Cruzar:** pra cada bloco, ver se a retenção caiu, subiu ou ficou estável no intervalo dele.
4. **Registrar aqui embaixo** (tabela por vídeo) qual bloco causou a maior queda — isso vira dado real pra saber que TIPO de conteúdo/bloco perde audiência (é sempre a lista de números? é a virada pro contra-argumento? é a pausa longa?).
5. Depois de 5-10 vídeos com esse dado, dá pra generalizar um padrão real (ex: "todo bloco de comparação de produto financeiro perde X% de retenção — ou é reescrever, ou é encurtar").

## Log (preencher após cada vídeo, 48h+ depois de publicar)

| Data | Vídeo | Bloco com maior queda de retenção | % perdido | Hipótese |
|---|---|---|---|---|
| 12/08/2026 | Bolha da IA / Samsung | **Patrocínio Grana, 1:05→2:36** | **−11,2 pts** (50,2%→39,0%) | Patrocínio de 91s colocado no minuto 1 — 3x o teto de 30s |
| 12/08/2026 | Método Barsi 19 min | Abertura 0:00→0:30 | −34,1 pts (94,3%→60,2%) | Setup narrativo sem fato nem número — ver [[abertura-10-20s]] |

### Achado 1: o patrocínio é o bloco mais caro do canal

No Samsung, o patrocínio do Grana começa em **1:05** e termina em **2:36** — 91 segundos, mais de 3x o teto de 30s que já estava definido nas 4 regras do Ask Studio (memória `feedback_askstudio_4_regras`). A retenção cai de 50,2% para 39,0% dentro dele.

Agravante: logo antes do corte pro patrocínio ele abre um loop ("fica até o final porque no meio do caminho tem Michael Burry entrando nessa história") e **quebra o próprio loop com anúncio**. Promete pagamento e cobra pedágio na frente.

**Regra:** patrocínio nunca no minuto 1. Teto de 30s. Se o roteiro abriu um loop, o patrocínio não pode ser a próxima coisa a acontecer.

### Achado 2: os picos de retenção são analogia, não dado

Os dois vídeos têm picos onde a audiência **sobe** — comportamento de rewatch. O que está neles:

- **Barsi 6:30 (33,6% → 41,8%, +8 pts):** "você pode cancelar a Netflix a qualquer momento, pode trocar de celular, pode adiar a compra de um carro, **mas tenta ficar sem energia elétrica** para você ver, tenta viver sem conta bancária, tenta passar meses sem água."
- **Barsi 15:30 (25,7% → 31,1%, +5 pts):** "quanto dinheiro precisa acumular para viver de renda? Só que quase ninguém sabe responder isso" — pergunta que o Tanaka tem na cabeça, seguida da planilha.
- **Samsung 4:00 (38,2% → 40,8%):** "o mercado não te pune por errar, ele te pune por não superar o que ninguém te disse em voz alta que esperava de você. É igual a nossa mãe, nosso pai."

Nenhum pico é número, tabela ou gráfico. **Todos são analogia doméstica ou reenquadramento.** Confirma o teste de 1 segundo com dado do próprio canal, e sugere que analogia forte não é tempero — é o que segura o corpo do vídeo.

**Ressalva:** o Studio entrega 100 pontos interpolados, então os picos são consistentes com rewatch mas não são prova de rewatch. Vale confirmar com mais vídeos antes de virar regra dura.

### Achado 3: não é ter patrocínio, é ONDE ele entra

Varri as legendas dos 6 vídeos atrás de marcador de patrocínio (cupom, QR code, link da descrição). Resultado:

| Vídeo | Retenção 30s | Patrocínio em | % do vídeo |
|---|---|---|---|
| SAUD3 | 73,2% (melhor) | ~13:50 de 18:04 | **77%** |
| FUGA GERAL | 71,5% | não tem | — |
| Perigo BTC | 71,1% | ~3:20 de 9:31 | **35%** |
| Samsung | 61,9% | **1:05 de 12:13** | **9%** |
| Alerta bancões | 61,1% | não tem | — |

**Ter patrocínio não prevê nada** — FUGA GERAL (bom) e Alerta bancões (ruim) não têm nenhum. **Onde ele entra prevê tudo.** O único vídeo com patrocínio no minuto 1 é justamente o que perde 11 pontos ali.

**A ponte do SAUD3 é o modelo a copiar.** O vídeo inteiro fala de um prazo (o Bradesco tem até 2027 pra resolver o free float). O patrocínio entra assim:

> "E falando em **prazos que você não pode perder**, tem um vencendo essa semana… tá acabando o prazo da declaração do imposto de renda."

Ele usa o próprio assunto do vídeo como porta de entrada. Não é corte pra comercial, é continuação de raciocínio. É o vídeo de melhor retenção do canal.

**No Samsung acontece o oposto:** abre um loop ("fica até o final porque tem Michael Burry entrando nessa história") e corta pro anúncio imediatamente, antes de ter entregado qualquer payoff. O Perigo BTC também abre loop antes do patrocínio — mas só depois de já ter fechado uma pergunta inteira (a Micro Strategy não explica a queda), e no minuto 3, não no minuto 1.

**Regra:** patrocínio depois de 35% do vídeo, nunca antes do primeiro payoff entregue, teto de 30s, e com ponte feita pelo assunto do próprio vídeo.

### Achado 3b: confirmado — patrocínio bem colocado custa ZERO

Curva do Perigo BTC dentro do bloco de patrocínio (~3:20, 35% do vídeo):

| Tempo | Retenção |
|---|---|
| 2:45 (antes) | 48,1% |
| 3:19 (dentro) | 48,3% |
| 3:53 (depois) | 47,9% |

**Perda: 0,2 ponto.** Contra os **11,2 pontos** do Samsung no minuto 1. Mesmo canal, mesmo formato de leitura, mesma marca. A única variável é a posição. Tese fechada.

*(A curva do SAUD3 veio truncada em 11:34 de um vídeo de 18:03, então o patrocínio dele, em ~13:50, segue sem medição. Não muda a conclusão — o BTC já isola a variável.)*

### Achado 4: repetir o mesmo ponto é a maior queda do corpo

Maior queda do SAUD3 depois da intro: **8:44, de 32,2% para 24,7% (−7,5 pts)**. O que está ali:

> "…o free float vai subir de 8,6 para 15, 20%. E aí vai tá perene, né? **Isso é uma boa notícia para ação. Mais liquidez, mais compradores.** Isso obviamente **é uma boa notícia para ação**, né? Vai ter **mais liquidez**, consequentemente **mais compradores** institucionais."

A mesma frase, duas vezes, em doze segundos. O Tanaka entendeu na primeira e saiu na segunda. Não é assunto chato — é redundância.

**Regra:** um ponto, uma vez. Se a segunda formulação não acrescenta informação nova, corta na edição. Vale checar no roteiro E no corte.

### Achado 5 (reforço): quarta confirmação de que analogia segura

O maior pico do BTC — **5:35 → 7:16, de 39,7% para 51,5%, +11,8 pontos** — contém:

> "Em poucas horas, mais de 1 bilhão de dólares em posições evaporaram. **Estala dedo do Thanos** nos bitcoins do povo. Pensa como a **fileira de dominó**: o primeiro cai, empurra o segundo, que empurra o terceiro… O mercado não apenas caiu, **ele começou a expulsar investidores da mesa**."

Três imagens em sequência: cultura pop, analogia física, reenquadramento. É o maior pico medido em qualquer vídeo até agora. Já são **4 picos analisados, 4 vezes analogia ou reenquadramento, 0 vezes número/tabela.** Pode virar regra dura.

## Por que isso importa mais que teoria de copywriting

A pesquisa de 08/07/2026 mostrou retorno decrescente em estudar mais framework (Derral Eves etc.) — o que falta não é teoria, é dado real do PRÓPRIO canal. Esse log, depois de umas 10 linhas preenchidas, vale mais que qualquer curso.
