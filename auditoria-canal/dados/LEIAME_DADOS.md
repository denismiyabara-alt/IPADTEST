# Dados exportados do canal (auditoria)

Gerado por `exportar.py`. Não edite à mão: rode o exportador de novo.

- Exportação: 2026-10-02 17:38 UTC (modo: completo)
- Canal: Investir e Coçar | Denis Miyabara (`UCWA0o8iZl2xbPXRopKu5A5Q`), criado em 2018-05-28; inscritos no contador público: 165000
- Período por vídeo (Analytics): 2018-05-28 a 2026-10-01
- Período mensal: 2025-04 a 2026-09 (18 meses fechados); diário: últimos 180 dias
- Quota da Data API nesta execução: 252 unidades (acumulado: 300; limite do projeto: 10.000/dia)
- Consultas ao Analytics nesta execução: 0 (acumulado: 48); respostas vindas do cache: 97
- Fuso: horários em UTC e em Brasília (UTC-3). Formato: short = duração ≤ 60 s; ou ≤ 180 s publicado a partir de 15/10/2024 (quando o limite dos Shorts subiu para 3 min); ou com #shorts/#short no título ou na descrição. O resto é longo.
- Privacidade: os comentários não trazem nome do autor; `autor_canal_id` é um hash do id do canal.
- Atenção: `views` de videos.csv é o contador público de hoje; `views` do Analytics é do período e pode diferir (o contador público conta views que o Analytics filtra, e vice-versa).

## videos.csv (1145 linhas)

- `id`: id do vídeo
- `titulo`: título atual
- `publicado_em_utc`: data e hora da publicação em UTC
- `publicado_em_brt`: data e hora da publicação em Brasília (UTC-3)
- `dia_semana`: dia da semana em Brasília
- `hora`: hora cheia em Brasília (0-23)
- `duracao_s`: duração em segundos
- `formato`: short ou longo (critério abaixo)
- `views`: contador público de views (Data API, no momento da exportação)
- `likes`: likes públicos
- `comentarios`: total de comentários públicos
- `tags`: tags separadas por |
- `descricao_tamanho`: nº de caracteres da descrição
- `thumbnail_url`: maior thumbnail disponível

## analytics_por_video.csv (1142 linhas)

- `video_id`: id do vídeo
- `titulo`: título (de videos.csv)
- `formato`: short ou longo
- `publicado_em_brt`: publicação em Brasília
- `views`: views no período (Analytics)
- `estimatedMinutesWatched`: minutos assistidos
- `averageViewDuration`: duração média da visualização (s)
- `averageViewPercentage`: % média assistida
- `subscribersGained`: inscritos ganhos
- `subscribersLost`: inscritos perdidos
- `likes`: likes
- `shares`: compartilhamentos
- `comments`: comentários
- `engagedViews`: views engajadas (se a API tiver a métrica)
- `impressions`: impressões da thumbnail (se a API devolver)
- `impressionsClickThroughRate`: CTR das impressões, % (se a API devolver)
- **Colunas vazias:** impressions, impressionsClickThroughRate
- Nota: consulta por lotes de até 200 IDs (filters=video==...; dimensions=video)
- Nota: coluna impressions vazia: a API recusou (videoThumbnailImpressions: HTTP 400 The query is not supported. Check the documentation at https://developers.google.com/youtube/analytics/v2/available_repo; impressions: HTTP 400 Unknown identifier (impressions) given in field parameters.metrics.). Exporte pelo YouTube Studio (Análises > Modo avançado > Conteúdo) para dados/studio/.
- Nota: coluna impressionsClickThroughRate vazia: a API recusou (videoThumbnailImpressionsClickRate: HTTP 400 The query is not supported. Check the documentation at https://developers.google.com/youtube/analytics/v2/available_repo; impressionsClickThroughRate: HTTP 400 Unknown identifier (impressionsClickThroughRate) given in field parameters.metrics.). Exporte pelo YouTube Studio (Análises > Modo avançado > Conteúdo) para dados/studio/.
- Nota: 3 vídeo(s) de videos.csv sem linha no Analytics (sem views no período ou recentes demais)

## trafego_por_video.csv (3287 linhas)

- `video_id`: id do vídeo
- `origem`: insightTrafficSourceType
- `origem_pt`: nome no Studio
- `views`: views
- `minutos`: estimatedMinutesWatched
- Nota: só os 300 vídeos com mais views (--max-videos-detalhe)
- Nota: consulta por lotes de até 200 IDs (filters=video==...; dimensions=video,insightTrafficSourceType)

## inscritos_por_video.csv (300 linhas)

- `video_id`: id do vídeo
- `views_inscritos`: views de quem é inscrito
- `views_nao_inscritos`: views de quem não é inscrito
- `minutos_inscritos`: minutos de inscritos
- `minutos_nao_inscritos`: minutos de não inscritos
- Nota: só os 300 vídeos com mais views (--max-videos-detalhe)
- Nota: consulta por lotes de até 200 IDs (filters=video==...; dimensions=video,subscribedStatus)

## canal_por_mes.csv (18 linhas)

- `mes`: AAAA-MM
- `views`: views
- `minutos`: minutos assistidos
- `inscritos_ganhos`: inscritos ganhos
- `inscritos_perdidos`: inscritos perdidos
- `engagedViews`: views engajadas (se a API tiver)
- `views_shorts`: views de Shorts (creatorContentType=SHORTS)
- `views_longos`: views de vídeos longos (VIDEO_ON_DEMAND)
- `views_lives`: views de lives
- `minutos_shorts`: minutos de Shorts
- `minutos_longos`: minutos de longos
- `minutos_lives`: minutos de lives
- `inscritos_ganhos_shorts`: inscritos ganhos em Shorts
- `inscritos_ganhos_longos`: inscritos ganhos em longos
- `inscritos_ganhos_lives`: inscritos ganhos em lives
- `inscritos_perdidos_shorts`: inscritos perdidos em Shorts
- `inscritos_perdidos_longos`: inscritos perdidos em longos
- `inscritos_perdidos_lives`: inscritos perdidos em lives
- **Colunas vazias:** views_shorts, views_longos, views_lives, minutos_shorts, minutos_longos, minutos_lives, inscritos_ganhos_shorts, inscritos_ganhos_longos, inscritos_ganhos_lives, inscritos_perdidos_shorts, inscritos_perdidos_longos, inscritos_perdidos_lives

## canal_por_dia.csv (178 linhas)

- `dia`: AAAA-MM-DD
- `views`: views
- `minutos`: minutos assistidos
- `inscritos_ganhos`: inscritos ganhos
- `inscritos_perdidos`: inscritos perdidos
- `engagedViews`: views engajadas (se a API tiver)

## trafego_por_mes.csv (278 linhas)

- `mes`: AAAA-MM
- `origem`: insightTrafficSourceType
- `origem_pt`: nome no Studio
- `views`: views
- `minutos`: minutos
- `pct_views_mes`: % das views do mês
- Nota: a API não aceitou month+origem juntos; consultei mês a mês

## comentarios_top30.csv (12318 linhas)

- `video_id`: id do vídeo
- `comentario_id`: id do comentário
- `resposta_a`: id do comentário-pai (vazio se não for resposta)
- `autor_canal_id`: hash SHA-256 (16 hex) do id do canal do autor; o nome NÃO é gravado
- `eh_do_canal`: 1 se quem escreveu foi o próprio canal
- `texto`: texto do comentário
- `likes`: likes
- `publicado_em`: data e hora UTC
- `eh_resposta`: 1 se é resposta
- Nota: aDL4MMF6AnE: parei em 20 páginas de comentários (--max-paginas-comentarios)

## Métricas que a API pode não entregar

- Impressões e CTR das impressões: em geral só no YouTube Studio. Se as colunas vierem vazias, exporte em Studio > Análises > Modo avançado > Conteúdo (todo o período), com Impressões e Taxa de cliques, e salve o ZIP como `dados/studio/studio_conteudo_longos.zip` (e `..._shorts.zip`): o analisar.py lê esses arquivos.
- Retenção nos primeiros 30 s (abertura): não existe por API para lista de vídeos; o proxy é averageViewPercentage.

<!-- termos-busca -->
## Termos de busca (exportados em 2026-10-02 20:47 UTC; quota da Data API: 0; consultas ao Analytics: 63)

### termos_busca_canal.csv (325 linhas)

- `periodo`: AAAA-MM, ou 'total' para o período inteiro
- `posicao`: posição do termo no período (1 = mais views)
- `termo`: termo buscado no YouTube (insightTrafficSourceDetail com origem YT_SEARCH)
- `views`: views que vieram desse termo
- `minutos`: minutos assistidos vindos desse termo
- Nota: a API devolve no máximo 25 termos por consulta (maxResults ≤ 25 para insightTrafficSourceDetail)

### termos_busca_por_video.csv (1250 linhas)

- `video_id`: id do vídeo
- `titulo`: título
- `posicao`: posição do termo no vídeo
- `termo`: termo buscado
- `views`: views desse termo no vídeo (período inteiro)
- `minutos`: minutos

<!-- /termos-busca -->
