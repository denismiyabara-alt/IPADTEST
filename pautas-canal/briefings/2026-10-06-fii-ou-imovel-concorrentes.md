# Pesquisa de concorrentes: FII ou imóvel alugado (para o longo de 06/10/2026)

> Papel: `pesquisador-concorrencia`. Feito em 03/10/2026 na nuvem. Termo do calendário: "fundo imobiliario".

## O que deu e o que não deu para coletar

| Etapa do agente | Resultado |
|---|---|
| 1. Busca no YouTube (`yt-dlp ytsearch` e página de resultados) | **Funcionou** para título, canal e views. **Data de publicação veio vazia** (NA) em todas as linhas. |
| 2. Legenda dos top vídeos | **Bloqueado.** Ao abrir o vídeo, o YouTube pede login ("Sign in to confirm you're not a bot"). Não contornei (sem cookies). |
| 3. Comentários dos 3 maiores | **Bloqueado** pelo mesmo pedido de login. Usei, no lugar, os **comentários do próprio canal** em `auditoria-canal/dados/comentarios_top30.csv`. |
| 4. Web (notícias) | Só busca (snippets). Os sites de notícia e os de lei deram `EGRESS_BLOCKED` no proxy (ver briefing, seção 9). |

Consequência: **não dá para afirmar que os vídeos são dos últimos 60 dias**, nem o que cada um disse por dentro. A tese
abaixo é **inferida do título** e está marcada assim. Nada daqui entra no roteiro como fato sobre concorrente.

## Vídeos sobre o tema (busca de 03/10/2026; views da busca; data não disponível)

| # | Título | Canal | Views | Tese (inferida do título) |
|---|---|---|---|---|
| 1 | Aula de Fundos Imobiliários (do zero aos iniciantes) | Primo Pobre | 2.080.271 | didático, FII como porta de entrada |
| 2 | Tudo o que eu aprendi investindo em imóveis | O Primo Rico | 942.101 | experiência pessoal com imóvel |
| 3 | Por que não compro casa pra alugar? (ouça com humildade) | Investidor Sardinha | 353.743 | contra imóvel físico |
| 4 | Deve manter o imóvel alugado ou vender e investir? #CerbasiResponde | Gustavo Cerbasi | 134.267 | depende; consultório |
| 5 | O que é melhor: Imóvel físico ou Fundos imobiliários? | Professor Baroni e Sidney Angulo | 99.588 | comparação clássica |
| 6 | Aluguel ou dividendos: qual vale mais na economia atual | Economista Sincero | 70.373 | comparação de renda |
| 7 | Comprar imóvel ou investir? Cálculo na prática (planta x renda fixa) | Nord Research | 67.104 | imóvel na planta x renda fixa |
| 8 | Vale a pena vender seu imóvel para investir? FIIs x imóvel alugado | Investidor Sardinha | 53.071 | vender o imóvel e ir pro FII |
| 9 | Imóvel alugado x FIIs: qual paga mais? | Gêmeos Investem | 52.803 | comparação de renda |
| 10 | Imóveis ou fundos imobiliários: em qual investir? | Os Sócios Podcast | 33.617 | debate |
| 11 | Aluguel vs. dividendos: qual renda vale mais a pena | Finclass | 12.429 | comparação de renda |
| 12 | Dividendos de FIIs ou aluguel de imóveis? Veja quem rende mais | InfoMoney | 607 | comparação de renda |

Todos os 12 títulos fazem a **mesma pergunta genérica** ("qual rende mais / qual é melhor"). Nenhum título cita 2026,
imposto, a lei, vacância medida ou o corte dos 100 cotistas. **Hipótese** (não confirmada, legendas bloqueadas): o
debate público está no "rende mais", com o número bruto do anúncio de um lado e o dividendo do outro.

## O vídeo do próprio canal que já fez o tema

`GbmXrqvUOkM` — "Fundos Imobiliários ou Imóveis: Qual rende mais no bolso?", sexta 26/06/2026, 19h, 13:52.
Fonte: `auditoria-canal/dados/analytics_por_video.csv` e `videos.csv`.

| Métrica | GbmXrqvUOkM | Longos do canal abr–set/2026 (n = 48), mediana |
|---|---|---|
| Views | 1.923 (7ª **menor** de 48) | 4.722 |
| % média assistida | **45,9%** (4ª **maior** de 48) | 37,5% |
| Inscritos ganhos | 14 | 21,5 |
| Inscritos por mil views | **7,3** | 5,4 |
| Views vindas da Pesquisa, termo "fiis" | 13 (`termos_busca_recentes.csv`) | — |

**Diagnóstico:** quem entrou, ficou e se inscreveu acima da média. **O que falhou foi a porta**: o título é a mesma
pergunta dos 12 concorrentes acima, sem número, sem ano, sem tensão, e saiu numa sexta. Não há transcrição dele no
repositório, então não sei o que o roteiro disse; o problema medido é de alcance, não de retenção.
**Consequência para 06/10:** o título novo precisa de número em R$ e de "2026", e o vídeo precisa de um fato que os
outros não têm (a conta líquida com o imposto de 2026 e a vacância medida na CVM).

## Comentários (do próprio canal, porque os dos concorrentes estão atrás de login)

Fonte: `auditoria-canal/dados/comentarios_top30.csv` (24 comentários com "aluguel/alugado"; os ligados a FII estão em
`fDUsjBJQmC4`, fev/2025). Citações literais:

1. "O que me chama a atençao sao FIIs pagando 0.8% 0.9% baseados em alugueis apos todos os custos do Fundo. Alguem aqui ja
   tentou alugar um imovel pedindo 1% de locação ao mês? Vai esperar deitado!" — **19 likes, o mais curtido do grupo**
2. "Vendi um imóvel e aportei tudo em fiis. A carteira ta como a de todo mundo: em déficit. Mas os proventos caem normais."
3. "mas o gestor nao precisa vender o imovel pra manter o rendimento do fii se estiver com os inquilinos e tudo rodando
   normalmente"
4. "Só estou olhando se os imóveis estão lá e estão pagando o aluguel e não tem muita dívidas"
5. De `auditoria-canal/RELATORIO.md`: "Vou ganhar R$ 300 mil de herança e quero pôr tudo em FII. Quais os mais seguros?"

**Dúvida nº 1:** *"O FII paga mais que o aluguel, mas a cota cai. O imóvel não cai. Qual é o truque?"* (1 + 2).
O roteiro responde no bloco 5: o imóvel tem preço e também oscila; ele só não aparece numa tela todo dia.
Pedido de "quais os mais seguros" (5) **não** é respondido com nome de fundo (regra: nunca recomendar ativo).

## Documentos primários que o briefing precisa

- Informe mensal e trimestral de FII na CVM (dados.cvm.gov.br) — **baixado e lido** (ver briefing).
- Lei 14.754/2023 e Lei 11.033/2004, art. 3º — **bloqueado** (planalto.gov.br, normas.leg.br).
- Lei 15.270/2025 (isenção até R$ 5 mil, IRPFM, exclusão do FII) — **bloqueado**; só snippet.
- MP 1.303/2025 (proposta de 5% sobre rendimento de FII; caiu em 08/10/2025) — **bloqueado**; só snippet.
- FipeZap locação residencial (rentabilidade do aluguel) — **bloqueado** (downloads.fipe.org.br); só snippet.
- IFIX: página da metodologia na B3 **lida** (índice de retorno total); valores históricos **bloqueados** (sistemaswebb3).

## Ângulo não coberto

Nenhum título trata da **conta líquida de 2026**: o mesmo aluguel bruto passando pelo mês vazio e pelo leão (que a
isenção dos R$ 5 mil de 2026 não alivia para quem já tem salário), contra um rendimento de fundo que já chega líquido,
mas com uma cota que aparece na tela todo dia. Junto: a vacância **medida** nos informes da CVM (imóvel 100% vazio é
fato comum) e o corte dos 100 cotistas da Lei 14.754.
