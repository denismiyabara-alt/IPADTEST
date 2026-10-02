# 10 ideias: 7 para fazer e 3 para parar

Tarefa 26 do pacote. Todos os números vêm de arquivos deste repo ou dos repos do projeto, com o lugar indicado. Onde a amostra é pequena, isso aparece escrito.

**Impacto** = efeito esperado em inscritos, tráfego ou tempo do Denis. **Esforço** = horas do Denis (o trabalho de máquina não conta).

## Resumo

| # | ideia | impacto | esforço do Denis | número que sustenta |
|---|---|---|---|---|
| 1 | Regravar os 6 temas perenes dos longos fora do ar (não republicar) | médio-alto | baixo (confirmar 7 linhas) | 285 longos fora do ar fizeram 32,7% dos inscritos de longos; dos 30 maiores, 23 são recomendação datada e 7 são tema perene (8.137 inscritos) |
| 2 | Série fixa de renda mensal, 1 por semana | alto | baixo (já está no calendário) | 14,5 inscritos por mil views intencionais, contra 8,2 do resto (n = 6) |
| 3 | Continuações dos 10 longos top do ano | alto | baixo | os 10 melhores fizeram 58% dos inscritos dos 80 longos novos |
| 4 | Título de busca e "Testar e comparar" em todo longo | médio | baixo (5 min por vídeo) | CTR de busca 12,3% contra 7,2% da página inicial |
| 5 | Responder as perguntas paradas e tirar pauta delas | médio | médio (rascunhos prontos) | 765 perguntas sem resposta; 20 rascunhos em `pautas-canal/PERGUNTAS-SEM-RESPOSTA.md` |
| 6 | Reescrever os títulos de recomendação do blog | médio (SEO e risco) | baixo, com ajuda | 30 destinos que o gate barra e que deixaram de receber 22 links internos |
| 7 | Decidir pauta só por inscritos e views intencionais | pré-requisito | zero (já está no painel) | o contador infla 3,4x nos longos novos desde 27/08 |
| 8 | **PARAR** de fazer "caso com nome" como carro-chefe | libera vaga para o que converte | zero | 4,0 inscritos por mil, contra 11,7 do plano de renda (12 meses) |
| 9 | **PARAR** o swing trade e o radar de puts como fonte de retorno | libera atenção | zero | nenhum setup passou fora da amostra; a put pura perdeu para o CDI em 18 de 20 ativos |
| 10 | **PARAR** o bot de temperatura da Polymarket | libera atenção | zero | o modelo só empata com o mercado (Brier 0,664 × 0,664); a configuração atual erraria as 15 apostas |

---

## Para fazer

### 1. Regravar os temas perenes dos longos fora do ar (não republicar)

- **O dado:** 285 longos estão no Studio, mas fora da playlist pública (privados, não listados ou excluídos). Eles somam 4,15 milhões de views e 52.351 inscritos, que são **32,7% de todos os inscritos que vieram de longos**. Fonte: `auditoria-canal/RELATORIO.md`, seção 4.
- **O que a lista dos 30 maiores mostrou** (`fora-do-ar-top30.csv`, gerado por `fora_do_ar.py`): 23 dos 30 são chamadas de compra ou venda, ou notícias de 2019 a 2022 ("COMPRE SÓ HOJE", "preço-alvo", "melhores ações para 2020", IRBR3, OIBR3, VVAR3). **Esses não devem voltar:** é provável que tenham saído justamente por isso, e o gate barraria todos. Republicar seria risco sem retorno.
- **O que vale:** 7 dos 30 tratam de temas que continuam sendo buscados e que dá para fazer sem recomendar ativo. Juntos, fizeram 8.137 inscritos e 383.912 views:
  - comparar bancos digitais (o Next × Nubank, com 3.474 inscritos, é o maior dos 285);
  - cheque especial e os dias sem juros;
  - quanto rendem R$ 100, R$ 1.000 e R$ 10.000;
  - como investir em empresa americana pela B3 (BDR);
  - desdobramento de ações;
  - follow-on (2 vídeos).
- **O que fazer:** regravar esses 6 temas, atualizados para 2026, com título de busca e sem nome de banco no título. O Denis confirma na coluna `decisao_denis` do CSV.
- **Impacto:** a demanda está provada pelo próprio canal, mas um vídeo novo não herda os inscritos do antigo. O efeito esperado é o de um longo de busca bom, não o de "recuperar 8 mil inscritos".

### 2. Série fixa de renda mensal

- **O dado:** 14,5 inscritos por mil views intencionais, contra 8,2 do resto (n = 6). Dos 5 maiores longos do ano, 2 são dessa linha (637 e 324 inscritos). Plano de renda: 11,7 por mil nos últimos 12 meses. Fonte: `auditoria-canal/RELATORIO.md`, seção 8, ação 3.
- **O que fazer:** manter um vídeo por semana com o mesmo nome de série. O calendário v2 já puxa nessa direção.
- **Atenção:** n = 6 é pouco. O teste vale por 6 semanas: se a mediana ficar abaixo de ~60 inscritos por vídeo em 7 dias, a série perde a vaga fixa.

### 3. Continuações dos 10 top

- **O dado:** os 10 melhores longos do ano fizeram 58% dos 5.327 inscritos dos 80 longos novos, com 6,5 a 19,7 inscritos por mil views. Fonte: `auditoria-canal/RELATORIO.md`, seção 8, ação 5.
- **O que fazer:** fazer a versão "6 meses depois" ou "atualizada" de cada um, com card e tela final apontando para o original. A tela final também ajuda a recuperar "Sugeridos", que caiu de 22,6% para 4,1% nos longos.

### 4. Título de busca e "Testar e comparar"

- **O dado:** o CTR da Pesquisa é de 12,3% nos longos, contra 7,2% da página inicial (vitalício). Os títulos fracos têm mais "?" (53% contra 37%) e mais caixa alta (47% contra 32%), com n = 19 de cada lado. Fonte: `auditoria-canal/RELATORIO.md`, seção 8, ação 8. Os termos que as pessoas buscam estão em `pautas-canal/TERMOS.md`.
- **O que fazer:** cada longo sobe com 3 títulos no "Testar e comparar" do Studio, um deles com o termo exato de busca.
- **Limite:** o título não pode cair na regra de recomendação do gate ("vale a pena", "qual a melhor"). O gate já confere isso.

### 5. Responder as perguntas paradas

- **O dado:** das 1.777 perguntas nos comentários, 766 estão sem resposta (43%). Os pedidos diretos são IR do zero, investimento para menor de idade e BDR do mês. Fonte: `auditoria-canal/RELATORIO.md`, seção 8, ação 9, e `pautas-canal/PERGUNTAS-SEM-RESPOSTA.md`, que tem 765 perguntas e 20 rascunhos de resposta.
- **O que fazer:** 15 minutos por dia, começando pelos rascunhos prontos. Quando um tema aparece 3 vezes, ele vira pauta (o filtro do radar já usa essa regra).

### 6. Títulos de recomendação no blog

- **O dado:** 30 posts têm título ou endereço que o gate barra por recomendação ("vale a pena investir", "qual a melhor", "hora de comprar"). Esses posts deixaram de receber 22 links internos. Mais 11 estão na fila de refresh do site de ativos. Fontes: `links-internos/destinos-bloqueados.csv` e `site-ativos/posts-para-refresh.csv`.
- **O que fazer:** reescrever o título e o H1 de forma neutra ("os números da ABEV3 em 2026"), mantendo o endereço com um redirect 301 no Yoast. Depois, rodar o `gerar_links.py` de novo: esses posts voltam a receber os links.
- **Por que importa:** o título é o que o Google mostra. Um título de recomendação é ao mesmo tempo risco regulatório e um post que o próprio blog não pode citar.

### 7. Decidir pauta só por inscritos e views intencionais

- **O dado:** desde 27/08 há 3,4 views para cada view intencional nos longos novos; antes, eram 1,1. Setembro teve 4,6 vezes as views de longos de agosto e só 503 inscritos, quando o modelo previa 2.881. Fonte: `auditoria-canal/RELATORIO.md`, H1.
- **O que já foi feito:** o painel diário passou a mostrar views intencionais no bloco do canal (commit d5dc79c). O Studio continua mostrando o contador inflado, e é por isso que a regra precisa ser explícita: thumb, título e pauta se comparam pelas intencionais e pelos inscritos, nunca pelo contador.

---

## Para parar

### 8. Parar "caso com nome" como carro-chefe

- **O dado:** nos últimos 12 meses, "caso com nome" converteu 4,0 inscritos por mil views, contra 11,7 do plano de renda e 7,1 dos comparativos e alertas macro (n de 10 a 25 por grupo). A hipótese de que esse tema convertia de 6 a 8 por mil foi derrubada. Fonte: `auditoria-canal/RELATORIO.md`, H2.
- **O que muda:** o tema continua quando a notícia é grande, mas deixa de ocupar vaga fixa no calendário. A vaga vai para renda mensal e Tesouro.
- **Ressalva:** o tema foi classificado por regras sobre o título. Vale conferir `auditoria-canal/dados/temas_manual.csv` antes de cortar de vez.

### 9. Parar de tratar o swing trade e o radar de puts como fonte de retorno

- **O dado:**
  - Swing v2: nenhum dos 3 setups passou fora da amostra. A expectativa ficou entre −0,03R e +0,01R, com intervalos que cruzam o zero, e 2026 foi negativo nos três.
  - Radar de puts: com prêmio igual à volatilidade histórica, a venda de put pura perdeu para o CDI em 18 de 20 ativos.
  - Fonte: `stock-signal-bot/RESUMO-TRADER.md`, módulos 2 e 3.
- **O que muda:** o robô das 8h40 continua rodando, porque é barato e o painel lê o resultado. Mas ninguém olha sinal de swing nem de put como "oportunidade". O radar de puts serve para ensinar (colchão, strike, risco de exercício) e pode virar conteúdo, não carteira.
- **O que continua valendo:** a carteira de estudo "momento + baixa vol" teve CAGR de 16,7% e Sharpe de 0,45 no backtest de 10 anos, contra 12,2% do Ibovespa. É backtest com viés de sobrevivência possível, então segue como estudo em papel.

### 10. Parar o bot de temperatura da Polymarket

- **O dado:** no backtest de 552 eventos (julho a setembro de 2026, 47 cidades), o melhor peso para o modelo foi zero. Modelo e mercado ficaram com o mesmo Brier, 0,664, e a configuração de hoje faria 15 apostas e erraria as 15. O critério de liberação não foi atendido. Fonte: backtest rodado no Mac (`~/pmw-backtest/reports/backtest/RELATORIO.md`) e `polymarket-weather-bot/RESUMO.md`.
- **O que muda:** desligar o agendamento do scanner, arquivar a branch e não gastar mais hora nisso. Se um dia aparecer uma fonte de previsão que o mercado não usa, o backtest está pronto para testar de novo em 1 comando.

---

## O que eu faria primeiro

1. **Esta semana:** a 7 (já feita no painel), a 2 e a 3 (só escolher a pauta) e a 10 (desligar).
2. **Próximas 2 semanas:** a 1. A lista dos 30 já está pronta; o Denis confirma os 7 perenes e eles entram no calendário.
3. **Contínuo:** a 4 e a 5 viram rotina; a 6 entra num lote só, como os patches de fatos.
