# Auditoria do canal Investir e Coçar: relatório (ESQUELETO)

> Este relatório ainda não tem conclusões. Os números entram quando `dados/` chegar do Mac: rode `python3 analisar.py` e copie as tabelas de `analise/RESULTADOS.md`. Cada afirmação deve citar o número e o arquivo de onde ele veio.

**Meta:** 200 mil inscritos até 31/12/2026.
**Situação atual:** _[inscritos hoje (LEIAME_DADOS.md) · faltam X · ritmo necessário de Y por dia × ritmo dos últimos 90 dias (canal_por_dia.csv)]_

## 1. O que separa os vídeos top dos fracos

_Tabela 4 de RESULTADOS.md: longos de 14 a 540 dias de vida, quartil de cima × de baixo._

- Tema: _[% de cada tema em top × fracos; inscritos por mil views por tema]_
- Formato: _[short × longo]_
- Título: _[tamanho, número, pergunta, caixa alta, nome próprio]_
- Thumb e CTR: _[CTR e impressões medianas (Studio)]_
- Duração: _[mediana em min]_
- Dia e hora: _[dia mais comum, hora mediana]_
- Abertura: _[retenção aos 30 s (retencao_30s.csv); proxy: % média assistida]_

## 2. Evolução mês a mês

_Tabela 5: views, minutos, inscritos líquidos, inscritos por mil views, % engajadas, % de Shorts._

- _[quando começou a queda (ou a alta), e o que mudou na mesma época]_

## 3. Dependência de poucos vídeos

_Tabela 3: % das views no top 1, 5 e 10; quantos vídeos fazem 50% e 80% das views; Gini._

## 4. Shorts × longos

_Tabelas 1 e 5: inscritos por mil views em cada formato; fatia dos inscritos que vinha de Shorts; o que aconteceu depois do fim dos Shorts._

## 5. O que o público pergunta

_Seção 8: % de perguntas, temas, termos frequentes, perguntas mais curtidas, % respondidas pelo canal._

## 6. Origem do tráfego

_Tabela 6 (API) e 6b (Studio, com impressões e CTR por origem): Recomendados (RELATED_VIDEO), Navegação (BROWSE), Pesquisa e Shorts, mês a mês._

## 7. Hipóteses a CONFIRMAR OU DERRUBAR

Nenhuma destas é verdade até os dados dizerem. O `analisar.py` calcula os números e aplica a regra de cada uma (seção 7 de RESULTADOS.md). Aqui entra o veredito, com o número.

| # | hipótese | como testar | veredito |
|---|---|---|---|
| H1 | Desde 27/08 o contador público de views está inflado 2,5 a 2,8x | views ÷ views engajadas e views ÷ minutos assistidos, 28 dias antes × depois (canal_por_dia); contador público ÷ engajadas por vídeo (Studio). Em Shorts, separar o efeito da nova contagem de 31/03/2025 | _[ ]_ |
| H2 | Vídeos de "caso com nome" convertem 6 a 8 inscritos por mil views, contra ~2 por mil de alerta macro e plano de renda | inscritos ganhos ÷ views × 1000 por tema (longos); conferir a classificação em temas_por_video.csv | _[ ]_ |
| H3 | A origem "Recomendados" caiu de 29% para 2% | % RELATED_VIDEO por mês (trafego_por_mes); comparar com BROWSE | _[ ]_ |
| H4 | O tema explica 20 a 50x da diferença, e a abertura quase não separa top de fracos | mediana de views do melhor tema ÷ pior tema; eta² do log das views por tema; retenção aos 30 s top × fracos | _[ ]_ |
| H5 | Os Shorts davam 40% dos inscritos e foram encerrados em 28/07 | % dos inscritos ganhos em SHORTS nos 6 meses antes de 07/2026 (canal_por_mes); data do último Short (videos.csv) | _[ ]_ |

## 8. As 10 ações priorizadas para 200 mil inscritos até 31/12/2026

Cada ação traz o número que a sustenta e o efeito esperado em inscritos. Ordem: maior efeito × menor esforço.

| # | ação | número que sustenta (fonte) | efeito estimado |
|---|---|---|---|
| 1 | _[ ]_ | _[ ]_ | _[ ]_ |
| 2 | _[ ]_ | _[ ]_ | _[ ]_ |
| 3 | _[ ]_ | _[ ]_ | _[ ]_ |
| 4 | _[ ]_ | _[ ]_ | _[ ]_ |
| 5 | _[ ]_ | _[ ]_ | _[ ]_ |
| 6 | _[ ]_ | _[ ]_ | _[ ]_ |
| 7 | _[ ]_ | _[ ]_ | _[ ]_ |
| 8 | _[ ]_ | _[ ]_ | _[ ]_ |
| 9 | _[ ]_ | _[ ]_ | _[ ]_ |
| 10 | _[ ]_ | _[ ]_ | _[ ]_ |

**Conta da meta:** _[inscritos que faltam ÷ dias até 31/12 = por dia; com as ações 1 a 10, de X para Y por dia]_

## Limites dos dados

- A API não entrega impressões nem CTR (em geral). Esses números vêm do Studio, se exportados.
- A retenção aos 30 s vem de anotação manual de 20 vídeos (10 top e 10 fracos).
- O tema sai de regras sobre o título (`analisar.py`), não de leitura humana. Confira `temas_por_video.csv`.
- Os vídeos antigos acumulam views. Por isso, top × fracos usa só longos de 14 a 540 dias de vida.
