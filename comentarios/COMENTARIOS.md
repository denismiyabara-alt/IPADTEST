# Fila de comentários sem resposta

> **Nada é postado por estes scripts.** `coletar.py` só chama endpoints de leitura (`channels.list`,
> `playlistItems.list`, `commentThreads.list`, `comments.list` e o relatório do YouTube Analytics). `fila.py` e `voz.py`
> não acessam a rede. Responder, ocultar ou apagar comentário é uma etapa separada, feita depois e só com o que o Denis
> aprovar.

## O que tem aqui

| arquivo | o que é | vai para o git? |
|---|---|---|
| `coletar.py` | baixa os comentários de topo de todos os vídeos, marca os que estão sem resposta do canal e guarda as respostas do canal | sim |
| `fila.py` | monta a fila por prioridade, com rascunho, tema e nota de risco | sim |
| `voz.py` | mede as respostas do canal e atualiza o bloco automático do `voz_denis.md` | sim |
| `regras.py` | detecção de pergunta, spam/golpe, risco e tema (reaproveita `analisar.py` e `perguntas.py`) | sim |
| `voz_denis.md` | a voz do Denis nas respostas: números, padrões e 12 exemplos sem nome | sim |
| `rascunhos.json` | `comment_id → rascunho` (sem autor), escrito na voz do `voz_denis.md` | sim |
| `fila_exemplo.csv` | a fila gerada da fixture (dados inventados), para ver o formato | sim |
| `dados/threads.csv` | saída do coletar: tem nome de autor | **não** (`comentarios/.gitignore`) |
| `dados/respostas_canal.csv` | respostas do canal (texto, data, thread) | **não** (`comentarios/.gitignore`) |
| `fila.csv` | a fila real: tem nome e texto de terceiros | **não** (`comentarios/.gitignore`) |

## Como rodar no Mac

```sh
cd ~/IPADTEST && git pull \
  && set -a && source ~/.config/investirecocar/credentials.env && set +a \
  && python3 comentarios/coletar.py --dry-run \
  && python3 comentarios/coletar.py \
  && python3 comentarios/voz.py \
  && python3 comentarios/fila.py \
  && open comentarios/fila.csv
```

- `--dry-run` mostra a estimativa de cota, sem rede e sem ler credencial.
- `--max-unidades 4000` (padrão) é o teto de unidades da Data API em cada execução. Ao bater o teto, o script grava o
  que já coletou e sai com código 4. Rodando de novo no mesmo dia, o cache do dia (`dados/.cache/AAAA-MM-DD/`) evita
  repetir as chamadas.
- `--dias 90` coleta só os comentários dos últimos 90 dias (para de paginar ao passar da data, porque a ordem é
  `order=time`). É o modo barato para rodar toda semana.
- `--sem-respostas-extras` economiza cota: não busca as respostas além das que vêm na thread. O custo é que uma thread
  com mais de 5 respostas, em que o canal respondeu depois da 5ª, pode aparecer como sem resposta.
- `--api-key` lê os comentários com `YOUTUBE_API_KEY` (só comentários públicos), sem OAuth.
- `python3 comentarios/fila.py --de-auditoria` monta a fila sem coletar nada, a partir de
  `auditoria-canal/dados/comentarios_top30.csv` (só 30 vídeos; sem autor e sem views de 28 dias).

## Token e escopo

O `coletar.py` usa a mesma autorização do `auditoria-canal/exportar.py`, por import da classe `Cliente` de lá. Não há
segredo no código. As variáveis são `YT_CLIENT_ID`, `YT_CLIENT_SECRET` e `YT_REFRESH_TOKEN`; `YT_CHANNEL_ID` é
opcional.

- **`commentThreads.list` e `comments.list` com OAuth: escopo `https://www.googleapis.com/auth/youtube.force-ssl`.** É o
  escopo que a documentação do Google lista para os recursos de comentário, e o token do Mac já tem. Não conte com
  `youtube.readonly` para esses recursos: ele não aparece na lista de escopos deles. Sem OAuth, com `--api-key`, a
  leitura dos comentários públicos funciona só com a chave.
- **Views dos últimos 28 dias:** YouTube Analytics, escopo `https://www.googleapis.com/auth/yt-analytics.readonly` (o
  mesmo que o `exportar.py` já usa). Se o token não tiver esse escopo, a coluna `views_28d` fica vazia e a fila usa a
  data do vídeo no lugar.
- O `youtube.force-ssl` também permite responder e moderar comentários, mas estes scripts não chamam nenhum endpoint de
  escrita. A publicação é de outra etapa.

## Cota

A Data API dá 10.000 unidades por dia por projeto. Toda chamada `.list` custa 1 unidade por página.

| chamada | quantas | unidades (canal de hoje: 1.145 vídeos, 63.747 comentários) |
|---|---|---|
| `channels.list` | 1 ou 2 | 2 |
| `playlistItems.list` (50 vídeos por página) | vídeos ÷ 50 | 23 |
| `commentThreads.list` (100 threads por página; no mínimo 1 por vídeo) | ~metade dos comentários são de topo ÷ 100 | ~1.240 |
| `comments.list` (threads com mais respostas do que as 5 que vêm junto) | ~3% das threads | ~960 |
| **total, coleta completa** | | **~2.200** |
| YouTube Analytics (views de 28 dias, lotes de 200 vídeos) | ~6 consultas | cota separada |

Com `--dias 90`, quase todo vídeo antigo custa só 1 página: cerca de 1.200 unidades. O `--dry-run` refaz a conta com o
`videos.csv` do dia.

## Prioridade

`prioridade = 100 × (0,50 × likes + 0,30 × vídeo vivo + 0,20 × recência)`, cada fator entre 0 e 1:

- **likes:** `log(1 + likes) / log(51)`, com teto 1 (50 likes ou mais é nota cheia);
- **vídeo vivo:** `log10(1 + views_28d) / log10(50.001)`, com teto 1; sem Analytics, `1 / (1 + idade_do_vídeo / 365)`;
- **recência:** `1 / (1 + idade_do_comentário / 90)` (comentário de 3 meses vale 0,5).

A coluna `peso` mostra a conta de cada linha. Spam e golpe vão para o fim.

## Colunas da fila

`prioridade, video_id, video_titulo, link, comment_id, autor, data, likes, texto, tema, rascunho, status, nota_risco, peso`

- `link` abre o vídeo já no comentário: `https://www.youtube.com/watch?v=ID&lc=COMMENT_ID`.
- `nota_risco`: `pede_recomendacao` (ativo específico, "qual comprar", "vale a pena"), `tributario` (regra de IR),
  `reclamacao` (crítica) e `spam/golpe` (pede contato, WhatsApp/Telegram, oferece mentoria, "Sra. Fulana me deu
  lucro", ou é a isca dos robôs de cripto). Pode haver mais de um, separados por `;`.
- `status` que o script escreve:
  - `rascunho`: tem rascunho em `rascunhos.json`;
  - `precisa_rascunho`: pergunta sem rascunho (as novas, que chegam depois, entram assim);
  - `fora_escopo`: cartão de crédito, dívida pessoal ou política, sem rascunho;
  - `ocultar`: spam/golpe. **Não recebe resposta**; é para o Denis ocultar no Studio.

## Aprovação em lote (o Denis)

1. Abra `comentarios/fila.csv` no Numbers ou no Excel.
2. Em cada linha com rascunho, troque a coluna `status` para:
   - `aprovado`: publica o rascunho como está;
   - `editado`: corrija o texto na coluna `rascunho` e ele publica o texto corrigido;
   - `pular`: não responde.
3. Linhas `ocultar`: oculte o comentário no Studio (ou deixe marcado para a etapa de moderação).
4. Salve como CSV, com o mesmo nome.

Ao rodar `fila.py` de novo, as linhas marcadas como `aprovado`, `editado` ou `pular` mantêm o status e o texto. As
threads que o canal já respondeu saem da fila sozinhas na coleta seguinte. A sessão que publica lê só `aprovado` e
`editado`.

## Rascunhos

- Estão em `rascunhos.json` e seguem o `voz_denis.md`, que foi medido nas próprias respostas do canal: curtos (a
  mediana dele é de uns 40 caracteres), diretos, com risada, `^^` ou `s2` no fim, "Tanaka" no lugar do nome. Na
  aprovação, dá para trocar "Tanaka" por "Fulano San" usando a coluna `autor`.
- Escopo desta rodada: as **30 perguntas de maior prioridade** com os dados de hoje (auditoria de 01/10/2026, fila de
  03/10/2026). As outras ficam `precisa_rascunho`.
- Nunca: nome de ativo, de banco, de corretora ou de exchange; "compre"/"venda"; previsão de preço; promessa de retorno.
  Pergunta de "qual comprar" recebe o critério, não o nome.
- Regra de imposto só com a lei que está no repositório (Lei 14.754/2023, LC 224/2025, Lei 15.270/2025, tabela do IOF e
  do IR) ou mandando para a Receita (Perguntas e Respostas do IRPF) ou para o vídeo do canal.
- Os testes (`python3 -m pytest comentarios/tests`) barram rascunho com instituição pelo nome, ticker, promessa de
  retorno ou expressão de recomendação. Quando o repositório `investir-e-cocar` está na máquina, eles usam também as
  regras do `pipeline/gate_qualidade.py`, por import.

## Testes

```sh
python3 -m pytest comentarios/tests
```

Sem rede: a API é a fixture `tests/fixture_api.json`, com canal, vídeos, autores e textos inventados. Para regenerar o
`fila_exemplo.csv`: `python3 comentarios/fila.py --exemplo`.
