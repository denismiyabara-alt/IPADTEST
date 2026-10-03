# OUTLIER → ENCAIXE

Este sistema acha os vídeos de concorrentes que estouraram no nicho do canal e já traz a solução: o ângulo do Denis, que
**amplia o outlier sem contradizer**, e o encaixe no calendário. Ele não usa LLM. O ângulo, os títulos e o gancho saem de
regras e modelos de texto, e o card avisa que são **rascunho**. Os números (múltiplo, views, vaga e inscritos esperados)
vêm dos arquivos.

```
coletar.py  ──► dados/radar_snapshot.json ──► detectar.py ──► diagnosticar.py ──► propor.py ──► saida/propostas.json
(API, Mac)      (+ dados/historico.json)      (outliers)      (por quê, parecidos)  (ângulo,       │   + propostas.md
                 ou o .md do radar                                                   títulos,      ├─► entregar.py ─► card na lista Ideias
                                                                                     encaixe)      ├─► resumo_manha.py ─► linha 🔥 às 8h50
                                                                                                   └─► encaixar.py aprovar ─► pautas-canal/trocas.json
                                                                                                                            └─► calendario_v3.py (CALENDARIO.md/.csv)
```

| Arquivo | O que faz |
|---|---|
| `coletar.py` | Roda no Mac. Busca uploads, views e inscritos pela API, **sem search**, e grava o snapshot e o histórico de views por idade. |
| `detectar.py` | Encontra os outliers: views na mesma idade comparadas com a mediana do próprio canal, mais os filtros de nicho, de views mínimas e de histórico mínimo. |
| `diagnosticar.py` | Explica por que o vídeo estourou (tema, ângulo, gancho, timing) e procura vídeos parecidos do Denis, com views intencionais e inscritos. |
| `propor.py` | Monta o ângulo, 3 títulos que passam no gate, o gancho, o dado-chave com a fonte e o encaixe. Grava `saida/propostas.json`, `saida/propostas.md` e `estado/propostas.json`, que guarda todas as propostas. |
| `entregar.py` | Cria um card por proposta na lista Ideias do Trello, sem repetir o mesmo vídeo. Tem `--dry-run`. |
| `encaixar.py` | Comandos `aprovar`, `desfazer` e `listar`. Grava a troca em `pautas-canal/trocas.json`, regenera o calendário e guarda o histórico. |
| `descobrir_canais.py` | Roda uma vez, no Mac. Encontra canais candidatos com search, uma busca por termo, e completa o `canais_candidatos.csv`. |
| `canais_aprovados.py` | Gera o `video_radar_channels.json` novo com os canais aprovados. Tem `--dry-run` e guarda o arquivo antigo. |
| `canais_candidatos.csv` | Lista preliminar de canais para o Denis aprovar. |
| `config.json` | Todos os parâmetros, explicados abaixo. |
| `rodar_mac.sh`, `com.denal.outliers.plist` | Fazem a rodada agendada no Mac. |

## 1. Detecção (`detectar.py`)

**Outlier** é o vídeo que cumpre todas estas condições, com os parâmetros do bloco `deteccao` do `config.json`:

- `múltiplo = views do vídeo na idade a ÷ mediana das views dos outros vídeos do MESMO canal e do MESMO formato quando eles tinham a idade a`.
  Como a idade é a mesma, essa é a mesma razão das views por hora. O formato é longo ou Short, com corte em `short_max_s` = 75 s;
- múltiplo ≥ `multiplo_min` (**3×**);
- views ≥ `views_min` (**3.000**), para cortar o ruído de canal minúsculo;
- pelo menos `historico_min` (**10**) vídeos de comparação. Sem isso não há mediana, e o vídeo vai para os descartes com o motivo "histórico curto";
- idade entre `idade_min_h` (6 h) e `idade_max_h` (**72 h**), a janela das primeiras 24 a 72 h;
- nicho do canal, dentro de `nichos`, explicado a seguir.

**Views de um vídeo de comparação na idade a.** Há duas formas de obter esse número, em ordem de preferência:

1. **Histórico (exato).** O `coletar.py` grava a hora e as views de cada vídeo a cada rodada, em `dados/historico.json`.
   Se duas observações cercam a idade a, o valor é interpolado entre elas;
2. **Curva (aproximação).** Enquanto o histórico ainda não cobre aquela idade, o valor é `views atuais × g(a) ÷ g(idade atual)`, com
   `g(t) = t ÷ (t + T)` e `T = curva_meia_vida_h` = 72 h. Isso supõe que metade das views dos primeiros dias chega nas primeiras 72 h.
   A curva só usa vídeos **mais velhos** que a idade a e nunca extrapola para a frente.

Cada outlier informa a base usada: `histórico`, `curva` ou `misto`. Com quatro rodadas por dia, o histórico passa a cobrir
as idades de 6 a 72 h depois de umas duas semanas, e a curva sai de cena aos poucos.

**Pontuação.** É ela que ordena as propostas. Com ela, um canal pequeno com 10× pesa mais que um canal grande com 2×:

```
pontuação     = log2(múltiplo) × peso_do_canal
peso_do_canal = 1 + peso_k × log10(peso_ref_inscritos ÷ inscritos), limitado a [peso_min, peso_max]
                (k = 0,3; ref = 500 mil; limites 0,7 e 1,6; com inscritos desconhecidos, o peso é 1)
```

| Caso | log2(múltiplo) | peso | pontuação |
|---|---|---|---|
| canal de 20 mil inscritos, 10× | 3,32 | 1,42 | **4,7** |
| canal de 200 mil inscritos, 3× | 1,58 | 1,12 | 1,8 |
| canal de 2 milhões de inscritos, 10× | 3,32 | 0,82 | 2,7 |
| canal de 2 milhões de inscritos, 2× | 1,00 | 0,82 | **0,8** |

O log2 faz 10× valer 3,3 vezes mais que 2×, sem deixar que um 50× isolado domine tudo. O peso dá até 60% a mais ao canal
pequeno, que tem a escala do Denis (165 mil): o que estoura lá estoura por causa do tema e do título, não do tamanho da
base. O canal gigante perde até 30%.

**Nicho** (`nichos` no `config.json`, regex sobre o texto sem acento):

- `dentro`: FII, renda mensal, Tesouro e renda fixa (inclui dívida pública), ações (inclui as empresas mais citadas) e
  investimento em geral;
- `fora`: dívida pessoal, cartão, finanças pessoais básicas, política, live e cripto puro.

O título decide primeiro, com `fora` antes de `dentro`. A descrição só decide quando o título é neutro, porque ela vem
cheia de link de patrocínio ("cartão", "conta digital"). Sem nenhum `dentro`, o vídeo fica fora com o motivo "sem nicho do canal".

**Entradas** (`caminhos.entrada_radar`; vale o primeiro arquivo que existir):

1. `outliers/dados/radar_snapshot.json`, gravado pelo `coletar.py`. É o formato completo;
2. adaptador para o `.md` semanal do radar (`/Users/denal/Downloads/Obsidian/Concorrentes/video-radar-*.md`, o mais recente).
   **Ele é uma aproximação.** O "Score Nx" do radar é `views ÷ mediana dos 30 últimos vídeos`, sem levar em conta a idade.
   A idade vem da coluna Dias (dias × 24 + 12 h), a janela passa a ser de 8 dias, o mínimo de 10 vídeos não pode ser verificado
   (o radar usa 30) e o corte de views só funciona quando a tabela tem a coluna Views;
3. adaptador para o JSON do `video_radar.py` antigo, o que usa a API: `ratio` é views ÷ média dos uploads 4 a 20, e a idade é `hours_old`.

## 2. Diagnóstico (`diagnosticar.py`)

- **Tema:** o nicho, os tickers do título e as entidades (CVM, Copom/Selic, Tesouro IPCA+, renda fixa, imposto, inflação,
  ETF, dividendos, FII e bolsa).
- **Ângulo do título:** comparação, veredito/alerta, relato pessoal, lista, conta/número, pergunta ou explicação. Vale a
  primeira regra que casar.
- **Gancho:** caixa alta, número, pergunta, palavra de tensão, ticker nomeado e tamanho do título.
- **Timing:** o título ou a descrição têm cara de evento (`noticia.regex`)? A contagem do prazo começa em `data_evento`,
  se o radar trouxer essa data, ou na publicação do vídeo. **Notícia quente** é evento com até `noticia.prazo_h` = 48 h.
- **O canal já fez parecido?** O script compara os títulos com `auditoria-canal/dados/videos.csv`, pela similaridade de
  cosseno entre os conjuntos de palavras. O ticker pesa 3 e a entidade pesa 2; o limiar é 0,25, no mesmo formato. Para cada
  vídeo parecido, o card traz as views intencionais (`engagedViews`) e os inscritos (`subscribersGained`) de `analytics_por_video.csv`.

## 3. Proposta (`propor.py`)

- **Ângulo do Denis:** parte da mesma premissa do outlier e vai um passo além, com **a conta em reais para quem tem
  R$ 50 a 100 mil** (o Tanaka) e o dado primário na tela. A regra do canal é **ampliar o outlier, não contradizer**. Se
  o título do outlier compara duas opções ("X ou Y"), o card avisa que esse formato é NO-GO no canal. Se o Denis já fez
  um vídeo parecido, a proposta vira continuação (double-down), com link para o vídeo anterior.
- **3 títulos de até 60 caracteres** que passam no gate. O `gate_qualidade.py` do investir-e-cocar entra por import
  (`IEC_PIPELINE` ou `caminhos.gate_dir`), e o título é recusado se tiver problema BLOQUEANTE, de corretora ou de
  recomendação. Sem o gate, vale uma checagem mínima, e o JSON registra isso.
- **Gancho** na voz do canal, sem meta-discurso. É rascunho.
- **Dado-chave**, com a fonte primária: o relatório gerencial no fnet, o texto do parecer na CVM, o comunicado do Copom no BCB, o Tesouro Direto etc.
- **Encaixe:**
  - **notícia quente** vira **Short rápido**, com prazo de 48 h, e o calendário não muda;
  - nos outros casos, a proposta troca a vaga de **menor `inscritos_esperados`** do `CALENDARIO.csv` entre amanhã e as
    próximas `calendario.semanas` = 3 semanas, no mesmo formato do outlier. **Nunca** troca um episódio da série
    (`serie_ep` preenchida), o Copom (`copom` em origem, título ou ângulo) ou uma vaga que já recebeu outlier;
  - só as `deteccao.max_trocas` = 2 propostas de maior pontuação disputam vaga, e duas propostas nunca pegam a mesma.
    As outras ficam como ideia no Trello;
  - quando o modelo do `pautas-canal` carrega, o card mostra também os inscritos esperados para o assunto do título novo
    (é uma ESTIMATIVA). Se o modelo não enxerga ganho, o card avisa que a aposta é a demanda mostrada pelo outlier.

## 4. Entrega

- **Trello** (`entregar.py`): o card vai para a lista **Ideias**. O id da lista é procurado nesta ordem: `TRELLO_LIST_IDEIAS`;
  `trello.lista_ideias_id`; e, por fim, a busca pelo nome "Ideias" no board da lista ENTRADA (`69c031570960846587bca67c`, a
  mesma do ic-health-monitor). **O id da lista Ideias não está em nenhum arquivo do projeto**, por isso a busca pelo nome é
  o padrão. Se ela falhar, defina `TRELLO_LIST_IDEIAS`. O script não cria card repetido: ele confere o vídeo em
  `estado/cards.json` e procura `video_id: <id>` na descrição dos cards da lista. Com `--dry-run`, só imprime e não usa a rede.
- **Resumo das 8h50** (`painel/resumo_manha.py`, bloco `outliers` em `resumo_manha.json`): as linhas aparecem logo depois
  de "Decidir hoje", até `max_linhas` = 2, vindas do `linha_resumo` de cada proposta:
  `🔥 Outlier: <título> (<canal>, Nx) → proposta: trocar o de dd/mm` ou `→ Short rápido`. Se não houver proposta, ou se o
  JSON tiver mais de 26 h, a linha não aparece.

## 5. Troca por comando (`encaixar.py`)

```bash
python3 outliers/encaixar.py listar
python3 outliers/encaixar.py aprovar OUT-<video_id> --quem Denis --dry-run   # mostra as trocas e não grava nada
python3 outliers/encaixar.py aprovar OUT-<video_id> --quem Denis
python3 outliers/encaixar.py desfazer OUT-<video_id>                         # ou o id da troca (T18)
```

O comando `aprovar` confere de novo, no `CALENDARIO.csv` atual, que a vaga existe, é futura e não é série nem Copom.
Depois acrescenta **no fim** de `pautas-canal/trocas.json`, no formato que o `calendario_v3.py` já lê, duas trocas com o
mesmo campo `"proposta"`:

- `op: "titulo"`: a pauta (data + formato + título) recebe o título novo. Também leva os campos `data`, `sai`, `entra`,
  `motivo`, `aprovado_por` e `quando`, para leitura humana;
- `op: "edita"`: grava o ângulo (marcado como RASCUNHO), as fontes, a continuação (o link do outlier) e a origem.

Em seguida, roda o `calendario_v3.py`, que regenera o `CALENDARIO.md` e o `.csv`. Se o gerador falhar, o `trocas.json`
volta como estava. O resto do arquivo nunca é reformatado: cada troca nova ocupa uma linha. O comando `desfazer` tira as
duas trocas e regenera. O histórico das duas ações fica em `estado/historico_trocas.jsonl`, que nenhum comando apaga.

## 6. Canais: a lista candidata e a aprovação

`canais_candidatos.csv` tem as colunas `nome, channel_id, inscritos, faixa, nicho, link, fonte_da_descoberta, aprovado`.
A versão preliminar foi montada daqui, sem acesso ao YouTube: tem **60 canais**, sendo 9 grandes, 25 médios e 26 pequenos
(**faixas estimadas**). Os inscritos estão como "a conferir". As fontes são o `video_radar_channels.json` atual (só os
canais BR do nicho, sem traders, corretoras de trade, finanças pessoais, dívida e política), a busca web (listas e
rankings de canais de FII, dividendos e renda fixa) e os comentários do canal (`comentarios_top30.csv`: Primo Rico 25
menções, Barsi 20, Sardinha 19, "Charles"/Economista Sincero 11). Sete canais da busca web ainda estão sem `channel_id`.

**No Mac, uma vez só:** `python3 outliers/descobrir_canais.py`. O script faz `search.list` para 10 termos (trxf11,
dividendos mensais, tesouro ipca, lci e lca, fundos imobiliários, fii, dividendos, renda passiva, tesouro direto e etf
dividendos mensais), depois `channels.list` em lotes de 50. Ele completa e corrige os inscritos e a faixa, acrescenta
canais novos com 5 mil inscritos ou mais, do Brasil e do nicho, e **não mexe na coluna aprovado**.
**Custo: 10 × 100 + cerca de 6 ≈ 1.006 unidades** (cerca de 10% da cota diária), uma vez só. Para estimar sem gastar nada,
rode `--dry-run`.

**Vídeos sugeridos.** O export atual (`trafego_por_video.csv`) só guarda o tipo de origem (RELATED_VIDEO), **não guarda o
vídeo de origem**. Para coletar no Mac, use `python3 outliers/descobrir_canais.py --sugeridos-analytics`, que consulta o
Analytics com o OAuth do `auditoria-canal/exportar.py` (`dimensions=insightTrafficSourceDetail`,
`filters=insightTrafficSourceType==RELATED_VIDEO`, 25 por mês, 6 meses) e transforma cada vídeo em canal com `videos.list`
(1 unidade a cada 50 vídeos). Outra opção é `--sugeridos-csv arquivo.csv`, com uma coluna `video_id`.

**Como o Denis aprova:**

1. abre `outliers/canais_candidatos.csv` e escreve `sim` ou `não` na coluna `aprovado`;
2. `python3 outliers/canais_aprovados.py --dry-run` mostra os canais que entram, os que saem e os que foram aprovados sem ID;
3. `python3 outliers/canais_aprovados.py` grava o novo `video_radar_channels.json` com os canais "sim". O arquivo antigo é
   guardado como `.bak-AAAAMMDD-HHMMSS`, as chaves de topo continuam iguais, os canais marcados "não" vão para
   `desativados`, e um aprovado sem `channel_id` fica de fora com um aviso. Nunca use o @handle: ele é mutável.

## 7. Cota da API (o radar diário nunca usa search)

Conta para 80 canais e 30 uploads por canal:

| Chamada | Unidades |
|---|---|
| `channels.list` (inscritos), 2 lotes de 50 | 2 |
| `playlistItems.list` da playlist de uploads, 1 por canal | 80 |
| `videos.list` (views e duração), lotes de 50: na 1ª rodada, todos (2.400 vídeos) | 48 |
| `videos.list` nas rodadas seguintes: só os vídeos de até 14 dias (cerca de 150 a 400) | 3 a 8 |
| **1ª rodada** | **130** |
| **rodada normal** | **~85 a 90** |
| **4 rodadas por dia** | **~350 a 360 por dia, cerca de 3,5% da cota padrão de 10.000** |

**Radar atual (yt-dlp) ou o esquema da API?** O radar que roda no Mac (`/Users/denal/video_radar.py`) usa
`yt-dlp --flat-playlist` e não gasta cota, mas **não traz a data de publicação** (a recência vira a posição na lista). Por
isso ele não consegue medir views por idade. Ele já ficou mudo duas vezes sem dar erro (yt-dlp desatualizado em 13 e
17/08; timeout em 23/08). O `video_radar.py` do repositório usa a API, com cerca de 5 unidades por canal, o que dá uns
425 por rodada com 85 canais, e chama `search` para resolver o nome de canais sem ID.
**Recomendação: migrar a detecção diária para o `coletar.py`.** São cerca de 90 unidades por rodada, com data de
publicação exata, histórico por idade, inscritos para a pontuação e falha explícita por canal. O radar com yt-dlp pode
continuar escrevendo a nota semanal no vault até o histórico do `coletar.py` cobrir duas semanas. Depois disso, a nota
pode passar a ser feita a partir do `saida/propostas.md`.

## 8. Instalação no Mac

O radar já roda no Mac, e o YouTube e a chave de API também estão lá.

```bash
cd ~/IPADTEST && git pull                                     # branch claude/friendly-shannon-jjlw8c
python3 -m pytest outliers/tests -q                            # sem rede
python3 outliers/coletar.py --dry-run                          # canais e custo, sem rede
python3 outliers/coletar.py && python3 outliers/propor.py && python3 outliers/entregar.py --dry-run
cp outliers/com.denal.outliers.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.denal.outliers.plist
```

- **Onde o `detectar.py` lê o radar:** primeiro em `~/IPADTEST/outliers/dados/radar_snapshot.json`, gravado pelo
  `coletar.py`. Na falta dele, lê o `video-radar-*.md` mais recente em `/Users/denal/Downloads/Obsidian/Concorrentes/`
  ou em `~/investir-e-cocar/vault/Concorrentes/` (`caminhos.entrada_radar`). Os canais vêm de
  `~/.config/investirecocar/video_radar_channels.json` (`caminhos.canais_radar`).
- **Agendamento:** o `com.denal.outliers.plist` roda o `rodar_mac.sh` às **08:15**, depois do radar das 7h30 e antes do
  resumo das 8h50, e também às 01:30, 13:30 e 19:30, para alimentar o histórico de views por idade. O log fica em
  `/tmp/outliers.log`. O job já está em `painel/resumo_manha.json` (opcional), então aparece no "Jobs" do resumo.
- O gate é importado de `~/investir-e-cocar/pipeline` (o caminho pode ser trocado em `IEC_PIPELINE`). Para o card mostrar
  o esperado do tema novo, o `pautas-canal` precisa estar no mesmo IPADTEST.
- O `encaixar.py aprovar` roda o `pautas-canal/calendario_v3.py`. Depois de aprovar, faça o commit do `trocas.json` e do
  `CALENDARIO.*`, como em qualquer troca.

## 9. Variáveis de ambiente (só os nomes)

`YOUTUBE_API_KEY` (coletar e descobrir); `YT_CLIENT_ID`, `YT_CLIENT_SECRET` e `YT_REFRESH_TOKEN` (só no
`--sugeridos-analytics`); `TRELLO_KEY` e `TRELLO_TOKEN`; `TRELLO_LIST_IDEIAS` (opcional); `IEC_PIPELINE` (opcional,
caminho do gate); `OUTLIERS_CONFIG` (opcional, outra config); `PYTHON` (opcional, no `rodar_mac.sh`). Se uma credencial
não estiver no ambiente, o script procura nos arquivos de `credenciais` da config
(`~/.config/investirecocar/credentials.env`).

## 10. Limites conhecidos

- A curva `t/(t+72h)` é uma suposição até existir histórico real. Quando a base sair "curva", leia o múltiplo como ordem
  de grandeza.
- As regras de nicho e de notícia usam regex: erram em ironia e em temas novos. Para ajustar, edite o `config.json`, não
  o código.
- Ângulo, títulos e gancho saem de modelos de texto. Eles são um ponto de partida para o empacotador, não o título final.
- No adaptador do `.md` não há mediana por idade nem mínimo de histórico. O card avisa isso na linha "base".

## Testes

`python3 -m pytest outliers/tests -q` usa uma saída falsa do radar, com um outlier de FII em canal pequeno, um de dívida
(filtrado), uma notícia quente (que vira Short rápido), um canal com histórico curto e um outlier com poucas views. O canal
do Denis tem um vídeo parecido, e há um calendário de exemplo com série, Copom e vaga fora da janela. Os testes também
cobrem a troca e o desfazer com um gerador falso, a reversão quando o gerador falha, o dry-run (o `urlopen` explode em
todos os testes), a cota da coleta (nunca usa search: 130 unidades na 1ª rodada com 80 canais) e a aprovação dos canais.
