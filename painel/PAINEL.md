# Painel único diário

Uma página para abrir de manhã, com cinco blocos: **CANAL**, **POSTS**, **TRADER**, **SITE** e **RADAR**. No topo fica **"O que fazer hoje"**, com no máximo 5 itens.

- O script é `gerar_painel.py`. Usa só a biblioteca padrão do Python (3.9 ou mais) e só **lê** arquivos locais.
- Grava `saida/painel-AAAA-MM-DD.html`: um arquivo só, com CSS dentro e sem JavaScript. Funciona no celular e tem modo escuro.
- Rede só se você pedir: com `--wp-rest` (ou `PAINEL_WP_REST=1`), lê os 5 posts mais recentes na API pública do WordPress. É só GET, sem login e sem credencial. Se a rede falhar, a lista some e o resto do painel sai normal.
- Não há segredo no código e o painel não lê nenhum arquivo de credencial.

Exemplo gerado com os dados deste repositório em 02/10/2026: `saida/exemplo.html`.

## Rodar

```bash
cd ~/IPADTEST/painel                       # CONFIRMAR o caminho do IPADTEST no Mac
python3 gerar_painel.py                    # gera saida/painel-AAAA-MM-DD.html
open saida/painel-$(date +%F).html
python3 gerar_painel.py --wp-rest          # inclui os posts recentes do blog (rede)
python3 gerar_painel.py --agora 2026-10-05T08:50   # simula outro dia (horário de Brasília)
python3 -m pytest -q tests                 # testes, sem rede
```

## Caminhos

A ordem de prioridade é: argumento, depois variável de ambiente, depois o padrão.

| O quê | Argumento | Variável | Padrão | No Mac |
|---|---|---|---|---|
| repo IPADTEST (canal, pautas, patches, site) | `--ipadtest` | `PAINEL_IPADTEST` | a pasta acima de `painel/` | **CONFIRMAR**. Se o painel rodar de dentro do clone, o padrão já serve. |
| repo investir-e-cocar (vault e video-radar) | `--iec` | `PAINEL_IEC` | `~/investir-e-cocar` | `/Users/denal/investir-e-cocar` (é o caminho do `pipeline/RESUMO.md`; confirmar) |
| stock-signal-bot | `--trader` | `PAINEL_TRADER` | `~/stock-signal-bot` | `/Users/denal/stock-signal-bot` (está no `com.denal.trader-novo.plist`) |
| saídas do gate | `--gate-dir` | `PAINEL_GATE_DIR` | `/tmp` | `/tmp`, onde o `ic-publish-blog` grava (`GATE.md`). Somem quando o Mac reinicia. |
| card do radar de comentários | `--radar-json` | `PAINEL_RADAR_JSON` | `/tmp/radar.json` | **CONFIRMAR** o `--saida` que o launchd de segunda usa. O RESUMO mostra `/tmp/radar.json`. |
| log dos patches aplicados | `--backup` | `PAINEL_BACKUP` | `<ipadtest>/auditoria-fatos/backup` | É onde o `aplicar_patches.py` grava. Confirmar que ele roda do mesmo clone. |
| pasta do HTML | `--saida` | `PAINEL_SAIDA` | `painel/saida` | |
| idade máxima do dado | `--max-horas` | `PAINEL_MAX_HORAS` | `36` | |

## O que cada bloco lê

| Bloco | Fonte | Data do dado |
|---|---|---|
| **CANAL** | `auditoria-canal/dados/`: `canal_por_dia.csv` (views e inscritos por dia), `videos.csv` (últimos 5 vídeos e views públicas), `analytics_por_video.csv` (% média assistida), `studio/retencao_30s.csv` (fica aos 30 s) e o contador de inscritos do `LEIAME_DADOS.md`. De `pautas-canal/`: `meta.csv` (meta do mês: 573 em out, 925 em nov), `META.md` (200 mil em mai/29) e `CALENDARIO-8-SEMANAS.csv` (vídeo de hoje e o próximo). | linha "Exportação" do `LEIAME_DADOS.md` |
| **POSTS** | `auditoria-fatos/patches/LOTE_*.json` e `links-internos/patches/LOTE_*.json` (lotes A, B, L1, L2 e L3). O que já foi aplicado vem de `auditoria-fatos/backup/log_*.jsonl`: "desfazer" tira o post da conta, e um post que está em dois lotes só conta no lote cujas trocas batem com o log. As saídas do gate vêm de `gate_<id>.saida.json` (`--json`) e `gate_estado*.jsonl` (`--wp-todos`). | hora dos arquivos |
| **TRADER** | `swing_v2_resultado.json` (sinais do dia e setups liberados), `radar_puts_resultado.json` (puts aprovadas), `carteira_longo_resultado.json` (carteira de estudo e rebalanceamento) e `ai_portfolio.json` (carteira de papel: valor, posições e última operação simulada). Tudo tem o rótulo **SIMULAÇÃO**. O `portfolio.json`, que é a carteira real, **não é lido**. | `gerado_em` (a mais antiga das três rodadas) |
| **SITE** | `site-ativos/saida/_relatorio.json` (data da geração), `saida/paginas.csv` (páginas e indexáveis) e `cache/dados.sqlite` (último pregão do COTAHIST, lido só para leitura). | `gerado_em` |
| **RADAR** | Card do `pipeline/radar_comentarios.py` (`--saida`, com as 5 dúvidas mais pedidas) e o último `vault/Concorrentes/video-radar-*.md` (vídeos de concorrentes acima da média, sem os títulos de política e eleição). O vault é lido do disco; se o arquivo não estiver lá, sai com `git show HEAD:...`, **sem checkout**. | hora do card / data do video-radar |

## Dado velho e dado faltando

- **Faltou a fonte:** o bloco mostra "sem dado" e diz o que rodar.
- **Dado com mais de 36 horas úteis:** o bloco mostra "dado velho · <data>" e continua exibindo os números. Sábado e domingo não contam. Assim, o trader de sexta às 19h10 ainda está "em dia" na segunda às 8h50.
- O radar de comentários roda uma vez por semana, então de quarta em diante ele aparece como velho. Isso é esperado.
- O "último pregão esperado" do COTAHIST não conhece os feriados da B3. No dia seguinte a um feriado, o painel pode acusar um atraso que não existe.

## Regras do "O que fazer hoje"

No máximo 5 itens, nesta ordem:

1. Vídeo do calendário com a data de hoje.
2. Post bloqueado no gate (só se a saída tiver até 36 h úteis).
3. Lote de patches com post pendente: o primeiro da fila, com o comando `--checar`.
4. Inscritos abaixo do ritmo da meta do mês. Com dias do mês nos dados, a conta é líquidos do mês contra meta × dias / dias do mês. Sem dias do mês, compara os últimos 30 dias com a meta.
5. Trader com novidade: sinal de swing, put aprovada ou rebalanceamento hoje. Se o trader estiver velho, o item avisa que ele não rodou.
6. CANAL ou SITE com dado velho: o item diz o comando para atualizar.
7. COTAHIST atrasado no site.
8. Dúvida nº 1 do radar, se o card for recente e tiver ranking.

Os itens 4, 5 e 7 só valem com dado em dia. Sinal velho não vira tarefa.

## Agendar (exemplo, nada foi instalado)

`com.denal.painel.plist` roda o painel de segunda a sexta às 8h50:

```bash
cp com.denal.painel.plist ~/Library/LaunchAgents/
launchctl load ~/Library/LaunchAgents/com.denal.painel.plist
```

Antes de instalar, confira:

- **Horário do trader.** O pedido fala em trader às 8h40, mas o `com.denal.trader-novo.plist` deste repositório roda às **19h10**, nos dias úteis. Com 19h10, o painel das 8h50 pega a rodada da noite anterior, e tudo funciona do mesmo jeito. Se no Mac existir outro agendamento às 8h40, ele também fica antes do painel.
- **O Python do plist.** É `/Library/Developer/CommandLineTools/usr/bin/python3`, o mesmo do `rodar_trader_novo.sh`.
- **Os caminhos do plist** marcados com CONFIRMAR, principalmente o do IPADTEST.

Os arquivos `saida/painel-*.html` do dia a dia ficam fora do git (`.gitignore`). Só o `exemplo.html` é versionado.

## Resumo da manhã no Telegram (`resumo_manha.py`)

Uma mensagem só, às 8h50 dos dias úteis, para ler em 30 segundos no celular. Ela **não refaz nenhum radar**: só lê as saídas que já existem e reaproveita as funções de bloco e o "O que fazer hoje" do `gerar_painel.py` (importa, não copia). Seções, nesta ordem:

1. **🎯 Decidir hoje**, com até 5 itens: o 1º item do "O que fazer hoje" do painel, os cards do Trello esperando aprovação, uma promoção de milhas ⭐ nova, um job com problema, o resto do painel e a ação do termômetro (quando não é "não mexer").
2. **📋 Trello**: quantos cards há em cada lista de aprovação ("Aprovar X", "Aprovar Instagram" e "Aprovar Blog") e os 3 mais antigos, pela última atividade.
3. **📡 Radares**:
   - ✈️ milhas: só os ⭐ e os "novo" do `milhas_relatorio.md`;
   - 💬 comentários: os 3 temas do card do radar quando ele tem até 24 h. Até 8 dias, mostra "nenhuma pergunta nova";
   - 🌡️ termômetro: o último veredito do `termometro_2h.py --auto` (log) ou, sem log, os números do `termometro_historico.jsonl`;
   - 📈 trader: só o resumo, com o rótulo **[SIMULAÇÃO]**.
4. **⚙️ Jobs**, numa linha: ❌ para quem saiu com código diferente de 0 no `launchctl list`, não está carregado ou não atualizou a saída depois do último horário agendado (mais a tolerância). Os outros ganham ✅. Os jobs `com.denal.*` e `com.denis.*` que não estão na config entram só pelo código de saída.

Fonte faltando ou velha aparece como "sem dado (motivo)" e não quebra a mensagem. Acima de 4096 caracteres (o limite do Telegram, contado em UTF-16, então um emoji vale 2), a mensagem é cortada no fim de uma linha e termina com "✂️ Cortado: ver painel (caminho do HTML do dia)". A mensagem vai em texto puro, sem Markdown: título de card com `_` ou `*` não derruba o envio.

### Instalar no Mac, passo a passo

1. **Atualizar o clone** do IPADTEST na branch deste trabalho e conferir os caminhos marcados com CONFIRMAR em `painel/resumo_manha.json` e em `painel/com.denal.resumo-manha.plist`:
   - o IPADTEST está em `/Users/denal/IPADTEST`?
   - o log do termômetro `--auto` (`termometro.log`) e o label dos jobs do radar de comentários e do termômetro. Hoje esses dois estão marcados como `opcional` e não acusam ❌ se o label não existir.
2. **Credenciais**: só os nomes vão aqui, nunca os valores. Nada de novo para criar: o script procura primeiro no ambiente e depois nos arquivos, na mesma ordem do `notifier.py` do stock-signal-bot.

   | Variável | Para quê | Onde o script procura |
   |---|---|---|
   | `TELEGRAM_BOT_TOKEN` | bot que envia | ambiente → `~/.hermes/.env` → `~/.config/investirecocar/credentials.env` → `~/.claude/credentials.env` |
   | `TELEGRAM_CHAT_ID` (ou `TELEGRAM_HOME_CHANNEL`) | conversa do Denis | idem |
   | `TRELLO_KEY` (não é `TRELLO_API_KEY`) | leitura das listas | ambiente → `~/.config/investirecocar/credentials.env` |
   | `TRELLO_TOKEN` | idem | idem |
   | `RESUMO_CONFIG` (opcional) | caminho da config | só ambiente (o plist já define) |

   Os caminhos do painel vêm do `resumo_manha.json` (seção `painel`). As variáveis `PAINEL_*` continuam valendo para o que ficar `null` lá.
3. **Testar sem enviar**:
   ```bash
   cd ~/IPADTEST/painel
   python3 resumo_manha.py --dry-run               # imprime a mensagem; lê o Trello (GET) e o launchctl
   python3 resumo_manha.py --dry-run --sem-trello  # sem nenhuma rede
   launchctl list | grep -E 'com\.den(al|is)\.'    # o que a linha de Jobs está vendo
   python3 -m pytest -q tests                      # testes do painel e do resumo, sem rede
   ```
   Se o Trello responder `invalid key`, a variável está com o nome errado. Não é credencial revogada.
4. **Mandar uma vez de verdade**: `python3 resumo_manha.py`. Ele sai com 0 se enviou e com 1 se o envio falhou (a mensagem vai para o log). O ❌ aparece no resumo do dia seguinte.
5. **Agendar** (exemplo, não instalado):
   ```bash
   cp com.denal.resumo-manha.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.denal.resumo-manha.plist
   ```
   O log fica em `/tmp/resumo-manha.log`, e a própria config usa esse arquivo para saber se o resumo rodou.

### Horários que o resumo espera (`jobs.esperados`)

| Job | Quando | Saída conferida |
|---|---|---|
| `com.denis.milhasradar` (Smiles no Chrome) | todo dia 3h | `run.log` |
| `com.denis.milhasrss` | todo dia 7h40 | `milhas_relatorio.md` |
| `com.denal.radar-comentarios` (CONFIRMAR o label) | segunda 8h | `/tmp/radar.json` |
| `com.denal.portfolioreview` | segunda 8h30 | `logs/portfolio.log` |
| `com.denal.painel` e `com.denal.resumo-manha` | dias úteis 8h50 | HTML do dia / `/tmp/resumo-manha.log` |
| `com.denal.stocksignal`, `.robusto`, `.wheel-robusto`, `com.denal.wheel`, `com.denal.tanaka-pm` | 9h15, 9h45, 10h, seg 9h30, 11h | `logs/*.log` |
| `com.denal.trader-novo` | dias úteis **19h10** (tolerância de 90 min) | `swing_v2_resultado.json` |

O pedido fala em trader às 8h40, mas o `com.denal.trader-novo.plist` roda às 19h10. Às 8h50, o resumo usa a rodada da noite anterior. Um job agendado depois das 8h50 é cobrado pela rodada do dia útil anterior. A tolerância padrão é de 30 min (`tolerancia_min`). Um log só muda quando o job imprime algo: se um job ficar ❌ "não rodou" sem motivo, troque a `saida` dele por um arquivo que ele sempre grava.

### Substitui ou convive?

**Convive.** O resumo não desliga nenhum envio, e o `com.denal.painel` (HTML) continua igual. Estes são os alertas que hoje saem separados no Telegram e o que se repete no resumo:

| Alerta de hoje | Repete no resumo? | Sugestão (quem decide é o Denis) |
|---|---|---|
| `milhas_radar.py` (7h40): 1 mensagem por post novo relevante | **Sim**: os ⭐ e os "novo" voltam no resumo às 8h50 | Manter o alerta imediato só para ⭐ (promoção acaba rápido) e deixar os 📰 "post novo relevante" só no resumo. Hoje não há opção para isso: precisaria de um ajuste pequeno no `milhas_radar.py`. O `--dry-run` dele **não** serve, porque não grava o `milhas_vistos.json` e o "novo" nunca sairia. |
| `termometro_2h.py --auto` (de hora em hora), se o Denis ligou a saída dele no bot | **Sim**: o último veredito aparece de novo de manhã | Manter o alerta das 2 h, porque é ele que dá tempo de trocar a thumb. A linha do resumo é só uma lembrança. |
| `radar_puts_telegram.txt` do trader novo, se algo no Mac envia esse texto | **Em parte**: o resumo traz a contagem de puts aprovadas | Se esse envio existir, dá para desligar e ficar com o resumo e o `placar.html`. |
| `scanner.py` (`com.denal.stocksignal` 9h15 e `portfolioreview` seg 8h30): "SINAIS IA" pelo `notifier.py` | Não: o resumo lê o trader **novo**, não o scanner antigo | Nada a fazer por causa do resumo. |
| `pm_run.py` (`com.denal.tanaka-pm`, 11h): "Carteira TANAKA" | Não | Nada a fazer. |
| `radar.py` (Smiles, 3h) | Não: só o status do job | Nada a fazer. |
| `ic-health-monitor` (a cada 3 h, só quando algo falha) | Pouco: ele olha Paperclip, sessões, cards **Aprovado** parados, Instagram e WP; o resumo olha os cards **Aprovar** e os jobs do launchd | Convive. |
