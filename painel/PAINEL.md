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
