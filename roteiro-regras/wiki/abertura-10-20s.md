---
name: A janela de 0:10–0:20 — onde o vídeo é ganho ou perdido
description: Regra de abertura de vídeo longo, medida no Ask Studio (27 vídeos, 90d até 12/08/2026) e cruzada com a transcrição real dos 3 melhores e 3 piores
type: semantic
updated: 2026-08-12
tags: [roteiro, retencao, abertura, hook, medido]
owner: SCRIPT-WRITER, QUALITY-JUDGE, DIRETOR-YT
---

# A janela de 0:10–0:20

**Aos 10 segundos, os melhores e os piores vídeos do canal são indistinguíveis.** A separação inteira acontece nos dez segundos seguintes.

| Vídeo | 10s | 20s | Queda 10→20 | 30s |
|---|---|---|---|---|
| Perigo Oculto BTC | 85,4% | 78,0% | **−7,4** | 71,1% |
| FUGA GERAL | 90,1% | 80,3% | **−9,8** | 71,5% |
| SAUD3 Bradesco | 87,4% | 76,3% | **−11,1** | 73,2% |
| Bolha IA Samsung | 91,1% | 77,9% | **−13,2** | 61,9% |
| Alerta nos bancões | 86,6% | 70,7% | **−15,9** | 61,1% |
| Método Barsi | 82,0% | 64,5% | **−17,5** | 62,0% |

A ordem da coluna "queda 10→20" é praticamente a mesma da retenção aos 30s. Quem segura essa janela, segura o vídeo.

**O CTR não explica nada disso.** Melhores 6,63% de média, piores 5,93%, todos vindos de Navegação. A porta funciona nos dois grupos — o que muda é o que acontece nos primeiros 20 segundos lá dentro.

---

## O que os 3 bons fazem entre 0:10 e 0:20

Todos entregam **fato novo com número, e uma virada**:

- **FUGA GERAL:** "Só quem seguiu esse conselho ganhou 25% em reais. **Só que** em dólar, Tanacão, esse valor foi de 38% em um ano."
- **SAUD3:** "A regra mínima do novo mercado para free float. **E a B3 deixou isso passar** e disse: tudo bem pra você, só que você tem prazo até 2027."
- **Perigo BTC:** "Bilhões de dólares acabaram evaporando do mercado de cripto. O Bitcoin caiu forte e os investidores foram liquidados."

Cada frase adiciona informação que a anterior não tinha. Nenhum deles fala sobre o vídeo — todos estão dentro do fato.

## O que os 3 ruins fazem no mesmo intervalo

**Alerta nos bancões — meta-discurso.** Abre com "Nesse vídeo vamos fazer uma batalha de bancões" e aos 10–20s ainda está anunciando pauta: "o jogo para quem investe pensando principalmente em dividendos. E eu não tô falando de uma quedinha qualquer, não, viu?". **Nenhum número nos primeiros 40 segundos.** Perdeu 15,9 pontos.

**Método Barsi — setup narrativo sem fato.** Aos 10–20s: "apartamento comum, sem carro de luxo, sem motorista, sem mansão, sem nenhum sinal externo de riqueza". Uma lista de negações. Aos 40 segundos ainda não aconteceu nada e ainda não apareceu um número. Pior queda dos seis: 17,5 pontos.

**Bolha IA Samsung — caso especial, e o mais instrutivo.** A abertura dele é BOA: número aos 3s ("lucrou 19 vezes mais"), virada aos 17s ("no mesmo dia a ação derreteu mais de 7%"). Por isso tem a **melhor** retenção aos 10s de todos (91,1%). E mesmo assim é a segunda pior retenção total do canal (33,5%) — o corpo desmonta o que a abertura montou. É o vídeo que o `voz-denis-corpus/DNA-VOZ-DENIS.md` usa como exemplo canônico de "CNBC traduzido". **Abertura boa não salva corpo sem voz.**

---

## As regras

1. **Número concreto antes dos 20 segundos, sem exceção.** Os três bons têm; os dois piores não têm nem aos 40s. Número ancorado, com consequência — ver [[numero-ancorado-exemplos]].
2. **Zero meta-discurso.** "Nesse vídeo vamos", "eu vou te mostrar", "esse vídeo é sobre" — proibido antes dos 30s. Anunciar a pauta não é entregar a pauta. O mapa do vídeo, se existir, vai depois dos 35s.
3. **Uma virada até os 20s.** "Só que", "e mesmo assim", "e a B3 deixou passar". O fato entra e imediatamente se contradiz.
4. **Nada de setup narrativo longo.** História de terceiro que leva 40 segundos pra chegar no ponto perde 17 pontos de audiência antes de chegar lá. Se for contar história, o fato chocante vem primeiro e a história explica depois.
5. **Nada custoso entre 0:20 e 0:35.** Esse trecho sangra 4–7% sozinho até nos melhores vídeos. CTA de inscrição, disclaimer e mapa não podem morar aí.

## O que NÃO é o problema

- **Não é o CTR** — bons e ruins têm CTR parecido.
- **Não são os primeiros 10 segundos** — bons e ruins empatam ali.
- **Não é a duração** — os seis estão na mesma faixa de tempo assistido.

## Contraprova pendente

O Samsung mostra que essa regra governa só a abertura. Um vídeo pode passar em todas as 5 regras acima e ainda assim afundar no corpo por falhar nos marcadores de voz. As duas checagens são independentes: esta aqui vale até os 40s, o `DNA-VOZ-DENIS.md` vale do início ao fim.

**Fonte:** Ask Studio (27 vídeos longos, 90 dias até 12/08/2026) + legendas automáticas dos 6 vídeos, extraídas via yt-dlp. Retenção segundo a segundo é interpolada de 100 pontos pelo Studio — a granularidade real é de ~5–8s por ponto, então "segundo 17" é aproximação, mas a comparação 10s vs 20s é sólida.
