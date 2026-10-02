# Auditoria do canal Investir e Coçar

Três peças:

- `exportar.py` baixa os dados do canal pela YouTube Data API e pela YouTube Analytics API. Ele só lê, usa só a biblioteca padrão e roda **no Mac**, onde estão as credenciais.
- `analisar.py` lê os CSVs de `dados/` e as exportações do Studio em `dados/studio/`, se houver, e calcula as tabelas do relatório. Ele não acessa a rede.
- `RELATORIO.md` é o esqueleto do relatório: as perguntas e as hipóteses que vamos confirmar ou derrubar.

## 1. Exportar (no Mac)

```sh
cd ~/IPADTEST && git pull && cd auditoria-canal \
  && set -a && source ~/.config/investirecocar/credentials.env && set +a \
  && python3 exportar.py --dry-run && python3 exportar.py
```

As credenciais são as mesmas do radar de comentários e do termômetro de 2 h: `YOUTUBE_API_KEY`, `YT_CLIENT_ID`, `YT_CLIENT_SECRET` e `YT_REFRESH_TOKEN`. `YT_CHANNEL_ID` é opcional. Sem ela, o script descobre o canal com `channels?mine=true` e, se isso falhar, usa `UCWA0o8iZl2xbPXRopKu5A5Q`.

Use `set -a; source …; set +a`, como acima. O padrão `source … && python3 <<EOF` não passa as variáveis para o Python no zsh.

Opções:

| opção | efeito |
|---|---|
| `--dry-run` | mostra o plano e a quota estimada; não acessa a rede e não lê credenciais |
| `--so-videos` | só a Data API: `videos.csv` e `comentarios_top30.csv` |
| `--so-analytics` | só a Analytics API: os demais CSVs |
| `--desde 2023-01-01` | início do período por vídeo (padrão: criação do canal; use esta opção se ficar pesado) |
| `--max-videos-detalhe 200` | limita tráfego e inscritos por vídeo aos N vídeos com mais views |
| `--recomecar` | apaga o cache e começa do zero |
| `--termos-busca` | etapa opcional: só baixa os termos buscados no YouTube (top 25 por mês nos últimos 12 meses e no período todo, e top 25 de cada um dos 50 vídeos com mais views da Pesquisa). Precisa de `videos.csv` e `trafego_por_video.csv` já exportados. Grava `termos_busca_canal.csv` e `termos_busca_por_video.csv` |
| `--pausa 0.3` | segundos entre chamadas |

**Analytics por vídeo:** o relatório de "top vídeos" (`dimensions=video`, `sort=-views`) não passa de 200 linhas: com `startIndex=201`, a API devolve 400 "The query is not supported". Por isso o script não pagina. Ele consulta por lotes de IDs do `videos.csv` (`filters=video==ID1,ID2,…`, sem `sort`), começando com 200 por lote. Se a API recusar o lote, ele é dividido ao meio até funcionar, e o tamanho que funcionou fica registrado no `LEIAME_DADOS.md`. Tráfego e inscritos por vídeo usam `dimensions=video,insightTrafficSourceType` e `video,subscribedStatus` no mesmo esquema de lotes. Se a API não aceitar essas duas dimensões com vários vídeos, o script consulta vídeo a vídeo.

**Só do passo 2 em diante:** `python3 exportar.py --so-analytics` pula vídeos e comentários e reaproveita o `dados/videos.csv` e o cache.

**Retomada:** cada resposta fica em `dados/.cache/`, que o git ignora. Se a execução cair (quota, rede ou Ctrl-C), basta rodar o mesmo comando de novo. O fim do período fica fixo na primeira execução, então a retomada no dia seguinte reaproveita tudo. Se a quota da Data API acabar, o script sai com código 3: rode de novo depois da meia-noite do Pacífico.

**Segurança:** nenhuma credencial vai para a tela, para o log (`dados/.cache/exportar.log`) ou para os arquivos. O cache usa a chave da chamada sem a API key, e o access token fica só na memória. Os testes verificam isso.

### Arquivos gerados em `dados/`

| arquivo | conteúdo |
|---|---|
| `videos.csv` | todos os vídeos: título, data (UTC e Brasília), dia e hora, duração, formato, views, likes, comentários, tags, tamanho da descrição e thumb |
| `analytics_por_video.csv` | por vídeo no período: views, minutos, duração e % média, inscritos ganhos e perdidos, likes, shares, comentários, engagedViews, impressões e CTR (estas três, se a API entregar) |
| `trafego_por_video.csv` | por vídeo × origem do tráfego: views e minutos |
| `inscritos_por_video.csv` | por vídeo: views e minutos de inscritos × não inscritos |
| `canal_por_mes.csv` | 18 meses fechados: views, minutos, inscritos, engagedViews e a separação Shorts × longos × lives |
| `canal_por_dia.csv` | últimos 180 dias, para testar datas exatas (27/08, 28/07) |
| `trafego_por_mes.csv` | origem do tráfego por mês, com % das views do mês |
| `comentarios_top30.csv` | comentários e respostas dos 30 vídeos com mais views. Não guarda o nome do autor, só um hash do id do canal |
| `LEIAME_DADOS.md` | data, período, quota usada, colunas, o que veio vazio e por quê |

**Critério de formato:** é short o vídeo com até 60 s; ou com até 180 s publicado a partir de 15/10/2024, quando o limite dos Shorts subiu para 3 min; ou com `#shorts`/`#short` no título ou na descrição. O resto é longo.

### Métricas que podem vir vazias pela API

| métrica | o que fazer |
|---|---|
| impressões e CTR das impressões | normalmente só no Studio. Exporte como abaixo |
| `engagedViews` | é recente na API. Se vier vazia, use a coluna "Visualizações engajadas" do Studio |
| Shorts × longos por mês (`creatorContentType`) | se a API recusar, use o Studio: Modo avançado > Tipo de conteúdo |
| retenção aos 30 s | não sai por API. Anote à mão (passo 3) |

### Quota

A Data API gasta 1 unidade por chamada. São cerca de 2 unidades para o canal e 2 a cada 50 vídeos. Os comentários custam 1 unidade por página de 100, nos 30 vídeos. Para 500 vídeos, a estimativa fica entre **100 e 600 unidades**, do limite de 10.000 por dia. A Analytics API tem limite próprio: são cerca de 2 consultas por vídeo, mais umas 30. O `--dry-run` mostra a estimativa, e o `LEIAME_DADOS.md` registra o que foi gasto.

### Termos de busca (opcional)

```sh
cd ~/IPADTEST && git pull && cd auditoria-canal \
  && set -a && source ~/.config/investirecocar/credentials.env && set +a \
  && python3 exportar.py --termos-busca \
  && cd .. && git add auditoria-canal/dados/termos_busca_*.csv auditoria-canal/dados/LEIAME_DADOS.md \
  && git commit -m "auditoria-canal: termos de busca" && git push
```

A etapa usa `dimensions=insightTrafficSourceDetail` com `insightTrafficSourceType==YT_SEARCH`, com `maxResults=25`, que é
o limite dessa dimensão. São cerca de 63 consultas ao Analytics e nenhuma unidade da Data API. Se a API recusar alguma
consulta (400), a etapa continua e registra uma nota na seção dos termos do `LEIAME_DADOS.md`; o resto do arquivo não
muda.

## 2. Exportações do Studio (opcionais, recomendadas)

Em Studio > Análises > **Modo avançado**, use "Exportar visualização atual" > CSV. Salve o ZIP, ou a pasta com `Tabela.csv`/`Totais.csv`/`Gráfico.csv`, em `dados/studio/` com estes nomes:

- `studio_conteudo_longos` e `studio_conteudo_shorts`: por vídeo, com Impressões, CTR das impressões, Visualizações, Visualizações engajadas, Tempo de exibição, Duração média, % média visualizada, Inscritos e Espectadores únicos;
- `studio_origem_trafego_mensal` (e, se quiser, `_longos` e `_shorts`): origem × mês;
- opcionais: `studio_ctr_por_origem_top30`, `studio_publico_mensal`, `retencao_30s.csv` (`video_id,pct_30s`) e `ask_studio.txt`.

A tabela de conteúdo do Studio para em 500 linhas. Com mais de 500 longos, a soma das linhas não fecha com o Total, e o `analisar.py` avisa. Para ter todos os vídeos, exporte em partes (filtrando por data de publicação) ou rode o `exportar.py`. Os meses incompletos ficam fora das séries mensais.

Os cabeçalhos podem estar em português ou em inglês. O `analisar.py` casa as linhas com `videos.csv` pelo ID ou, se faltar o ID, pelo título.

## 3. Lista para anotar a retenção aos 30 s

Depois do passo 1:

```sh
cd ~/IPADTEST/auditoria-canal && python3 analisar.py --lista-retencao
```

O comando imprime os 10 longos top e os 10 fracos, com IDs e links do Studio, e grava `analise/lista_retencao_30s.csv`. Anote a % de retenção aos 30 s de cada um e salve só `video_id,pct_30s` como `dados/studio/retencao_30s.csv`.

## 4. Subir os dados

```sh
cd ~/IPADTEST
git add auditoria-canal/dados/*.csv auditoria-canal/dados/LEIAME_DADOS.md auditoria-canal/dados/studio
git commit -m "auditoria-canal: dados exportados em $(date +%F)"
git push
```

Os CSVs não têm segredo. O cache e o log ficam fora do git.

## 5. Analisar

```sh
python3 analisar.py      # gera analise/RESULTADOS.md, analise/temas_por_video.csv e a lista de retenção
```

O tema de cada vídeo sai de regras simples sobre o título: `ENTIDADES`, `TEMAS` e `NAO_NOMES`, no topo do `analisar.py`. Para corrigir um vídeo à mão, crie `dados/temas_manual.csv` com as colunas `video_id,tema`.

## Testes

```sh
cd auditoria-canal && python3 -m pytest tests -q
```

Os testes usam mocks e não acessam a rede. Eles cobrem a paginação (playlist e Analytics), short × longo, o erro 400 de métrica indisponível, o retry com backoff, a renovação do token, a quota esgotada e a retomada pelo cache. Também verificam que nenhum segredo aparece em arquivo ou log, e testam a análise com dados e exportações do Studio falsos (ZIP em PT, pasta em EN).
