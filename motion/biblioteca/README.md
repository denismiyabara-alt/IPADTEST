# Biblioteca de animações de dado (Investir e Coçar e Faz a Conta)

Peças de B-roll de 5 a 10 s, no mesmo padrão do `grafico_cotacao`: HyperFrames 0.8.78, projeto autocontido
(fontes, GSAP e som copiados para `assets/`, nada de CDN), dado REAL e conferido com `Fonte: …` na tela, **um único
som, só no pouso**, formatos 16:9 e 9:16, e teste que prova que os números da tela são iguais aos do dado.

| peça | o que é | pasta |
|---|---|---|
| **barras** | barras horizontais que crescem do zero com o valor contando junto; com dois momentos (antes → depois), trocam de lugar | `barras/` |
| **rosca** | uma rosca que se divide em fatias, uma por vez, com rótulo e percentual; a soma tem de dar 100% | `rosca/` |
| **eventos** (lote 2) | o gráfico de cotação com marcadores anotados (ex.: decisões do Copom) que acendem quando a linha passa | `eventos/` |
| **barra_linha** (lote 2) | a taxa do mês em barras que se transformam na linha do acumulado em 12 meses (IPCA 433 → 12 meses) | `barra_linha/` |
| **numero_linha** (lote 2) | o número grande (Selic de hoje) que encolhe e vira o último ponto da linha histórica | `numero_linha/` |
| **manchete** (lote 2) | a frase de manchete em que a palavra-chave se enche de vermelho (ou ganha marca-texto) no tempo da fala | `manchete/` |

```
comum/estilo.py        estilos, formato brasileiro (fmt_br), validação comum, checar_ativos; o estilo iec é LIDO do molde Burry
comum/projeto.py       monta o projeto: fontes, GSAP, som de pouso, créditos, <head>, filtro boil, marca-d'água;
                       grafico_cotacao() carrega o grafico_cotacao/gerar.py (escala, easing, layout) para o lote 2
comum/quadro.mjs       abre o projeto num Chrome headless, faz seek e lê window.__tela() (genérico para qualquer peça)
comum/teste.py         ajuda dos testes de navegador (pulados sem node_modules ou Chrome)
biblioteca/dados.py    monta os JSON de exemplo a partir da origem (SQLite do site-ativos, fact-check do Faz a Conta)
biblioteca/barras/gerar.py, biblioteca/rosca/gerar.py   JSON → projeto HyperFrames
biblioteca/{eventos,barra_linha,numero_linha,manchete}/gerar.py   lote 2, mesmo padrão
biblioteca/renderizar.sh   gerar + render + tempo (+ GIF com --gif); escolhe a peça pelo campo "peca"
biblioteca/tests/      114 testes (54 do lote 1 em test_biblioteca.py, 60 do lote 2 em test_lote2.py)
```

O `grafico_cotacao/`, o `renderizar.sh` da raiz e os `tests/` dele não mudaram.

## Instalar (uma vez)

```sh
cd motion
npm install                       # hyperframes 0.8.78, gsap, puppeteer (via hyperframes)
(cd biblioteca && npm install)    # @fontsource/archivo-black e @fontsource/montserrat (OFL)
npx hyperframes browser ensure    # Chrome headless, se ainda não houver
```

## Usar

```sh
# 1. dado → JSON (sem digitar número: lê a origem)
python3 biblioteca/dados.py dy-caixa --destaque PETR4 -o exemplos/barras-dy-caixa-16x9.json
python3 biblioteca/dados.py cotistas --formato 9:16 -o exemplos/barras-cotistas-9x16.json
python3 biblioteca/dados.py megasena --peca rosca --formato 9:16 -o exemplos/rosca-megasena-9x16.json
python3 biblioteca/dados.py megasena --peca rosca --estilo fazaconta -o exemplos/rosca-megasena-fazaconta-16x9.json
python3 biblioteca/dados.py copom -o exemplos/eventos-selic-copom-16x9.json                 # lote 2
python3 biblioteca/dados.py ipca --formato 9:16 -o exemplos/barra-linha-ipca-9x16.json
python3 biblioteca/dados.py selic -o exemplos/numero-linha-selic-16x9.json
python3 biblioteca/dados.py manchete-ipca --marca marca-texto --formato 9:16 -o exemplos/manchete-ipca-marcatexto-9x16.json

# 2. JSON → MP4 (+ GIF de revisão)
./biblioteca/renderizar.sh exemplos/rosca-megasena-9x16.json renders/rosca.mp4 --gif

# conferir antes do render cheio (barato): quadros num instante
python3 biblioteca/rosca/gerar.py exemplos/rosca-megasena-9x16.json -o projetos/rosca
node comum/quadro.mjs projetos/rosca 2.5,8 snapshots/rosca     # PNG de cada instante + o que está na tela
```

Entrada errada para antes de gerar, com a lista de todos os problemas (`validar()` de cada peça).

## Estilo: `"estilo": "iec" | "fazaconta"`

- **`iec`** (padrão): o estilo oficial do Investir e Coçar é o do **molde Burry**. A fonte de verdade é a `PAL` e as
  fontes de `edicao-skill/molde-burry/broll/gerar.py`: o `comum/estilo.py` lê esse arquivo (sem executá-lo) e tira dele
  as cores (`bg #f6f2e8`, `ink #1c1a17`, `red #d6362b`, `gray #79756c`, `faint #d9d4c7`) e as famílias e pesos do CSS
  (Montserrat 700/800 nos rótulos, Archivo Black nos números e títulos). Nenhuma cor fica fixa no código das peças.
  Se o molde estiver em outro lugar (no Mac, dentro da skill), aponte `IEC_MOLDE_BURRY_GERAR` para o `gerar.py`.
  Um teste falha se as cores da variante `iec` divergirem da `PAL`.
- **`fazaconta`**: a `PALETA` do `faz-a-conta/*/build_hf.py` (o teste confere contra o arquivo do repo faz-a-conta),
  com a marca-d'água **FAZ A CONTA** no canto.

Os dois usam o traço que "ferve" (filtro `boil`, semente trocada a 8 fps) nas bordas das barras e da rosca. Hoje as
duas paletas têm os mesmos valores (o molde Burry nasceu do Faz a Conta); o que muda é a marca e a fonte de verdade.

## Peça: barras

**O que acontece:** título e kicker entram; as barras crescem do zero, de cima para baixo, com o valor contando junto;
o número grande (o "placar") acompanha a barra-chave. Com dois momentos, as barras param no "antes" com o selo do
1º momento (`ago/2025`), e então os valores vão para o "depois" enquanto as barras trocam de lugar (quem sobe passa por
cima). No **pouso**, a barra-chave ganha o vermelho, o número dá um pulso e toca o único som. Depois entra a variação.

```json
{
  "peca": "barras", "estilo": "iec", "formato": "9:16", "duracao": 8,
  "titulo": "FIIs com mais cotistas", "kicker": "Fundos imobiliários · número de cotistas",
  "fonte": "Fonte: CVM (informe mensal de FII, ago/2025 e ago/2026)",
  "unidade": {"prefixo": "", "sufixo": "", "casas": 0},
  "itens": [{"rotulo": "MXRF11", "antes": 1325308, "valor": 1529305}, "…"],
  "destaque": "GGRC11", "rotulo_placar": "GGRC11 · cotistas",
  "momentos": ["ago/2025", "ago/2026"], "variacao": "pct",
  "ativos": true, "criterio": "Critério: …",
  "som": {"pouso": "impact-bass-1"}
}
```

| campo | padrão | o que faz |
|---|---|---|
| `itens` | obrigatório | 2 a 10 barras: `rotulo`, `valor` (≥ 0), `antes` (opcional, em todos ou em nenhum), `detalhe` (linha pequena, se couber) |
| `destaque` | obrigatório | rótulo da barra-chave (ganha a cor no pouso; o placar mostra o valor dela) |
| `ordem` | `"desc"` | `"asc"` para ranking de menor para maior (ex.: menor P/VP) |
| `momentos` | `null` | obrigatório com `antes`: os nomes dos dois momentos |
| `variacao` | `"posicao"` com dois momentos | `"posicao"` ("subiu do 8º para o 7º lugar"), `"pct"` ("+116,2% desde ago/2025") ou `null` |
| `ativos` / `criterio` | `false` / `""` | ver compliance |
| `unidade`, `rotulo_placar`, `som`, `formato`, `duracao`, `estilo` | | como no grafico_cotacao |

## Peça: rosca

**O que acontece:** o anel vazio aparece com o total no centro ("R$ 6,00 · a sua aposta"). As fatias se desenham
**uma por vez**, no sentido horário a partir do topo, e a linha da legenda de cada uma entra junto, com o percentual
contando. No **pouso**, a fatia-chave engrossa e fica vermelha, e o centro pousa na parte dela ("R$ 2,63 · viram
prêmio") com o único som. Por fim, "soma: 100,00%".

```json
{
  "peca": "rosca", "estilo": "fazaconta", "formato": "16:9", "duracao": 8,
  "titulo": "Pra onde vão os seus R$ 6", "kicker": "Mega-Sena · cada aposta simples",
  "fonte": "Fonte: Lei 13.756/2018, art. 16", "casas": 2,
  "fatias": [{"rotulo": "Prêmio (com IR)", "pct": 43.79}, {"rotulo": "Caixa e lotéricas", "pct": 19.13}, "…"],
  "destaque": "Prêmio (com IR)",
  "centro": {"valor": 6, "unidade": {"prefixo": "R$ ", "casas": 2}, "rotulo": "a sua aposta", "rotulo_final": "viram prêmio"}
}
```

| campo | padrão | o que faz |
|---|---|---|
| `fatias` | obrigatório | 2 a 10, na ordem do desenho: `rotulo`, `pct` (> 0) |
| `casas` | `1` | casas do percentual (0 a 2) |
| `destaque` | obrigatório | rótulo da fatia-chave |
| `centro` | `null` | o total; no pouso, vira `valor × pct da chave` (6 × 43,79% = R$ 2,63). Sem ele, o centro pousa no % da chave |

**Soma 100%, validada.** Dá erro (e nada é gerado) se: a soma do dado não for 100 (tolerância de 1e-6); a soma dos
percentuais **como aparecem na tela** (arredondados em `casas`) não der 100 (ex.: 33,33 × 3 = 99,99%); ou uma fatia
aparecer como 0%.

## Lote 2: eventos, barra_linha, numero_linha e manchete

As quatro seguem o padrão do lote 1: `gerar.py` (JSON → projeto autocontido), `validar()` que recusa a entrada
errada com a lista dos problemas, `assets/tela.js` lido pelo `comum/quadro.mjs` no teste, um único som no pouso,
16:9 e 9:16, só cores da PAL do molde Burry (estilo `iec`), e o `Fonte: BCB/SGS <n>` no rodapé a peça inteira.
O dado sai do `dados.py`, que lê as séries do BCB pelo mesmo caminho do `grafico_cotacao/serie.py`: SQLite do
site-ativos → JSON cru do site-ativos (`cache/raw/bcb/sgs_<n>.json`) → cache próprio → API do BCB.

**Rede, 03/10/2026:** daqui, a `api.bcb.gov.br` está bloqueada pelo proxy (CONNECT recusado). Os exemplos saíram do
cache do site-ativos, baixado da API em 02/10/2026 16:09 UTC (433 e 13522 até ago/2026; 432 até 02/10/2026). Nenhum
número foi digitado.

### Peça: eventos

**O que acontece:** é o gráfico de cotação inteiro (o mesmo `grafico_cotacao/gerar.py`, com a mesma validação e a
mesma regra de compliance), com uma camada a mais: cada evento é um traço tracejado vertical, um ponto sobre a linha
e um rótulo curto, que **acendem quando a ponta da linha passa pela data**. O rótulo vai do lado oposto ao da linha
(em cima se a linha está embaixo) e desce um nível se fosse bater no vizinho.

```json
{"peca": "eventos", "titulo": "Selic: da alta ao 1º corte", "classe": "indicador", "linha": "degrau",
 "fonte": "Fonte: BCB/SGS 432 (meta Selic; data de vigência de cada decisão)", "serie": ["…"],
 "eventos": [{"data": "2024-09-19", "rotulo": "1ª alta: 10,75%"}, {"data": "2025-06-19", "rotulo": "Pico: 15,00%"},
             {"data": "2026-03-19", "rotulo": "1º corte: 14,75%"}]}
```

| campo | padrão | o que faz |
|---|---|---|
| (todos os do grafico_cotacao) | | `serie`, `classe`, `linha`, `unidade`, `variacao`, `comparador`/`aviso`, `som`… |
| `eventos` | obrigatório | 1 a 8 `{data, rotulo}`, em ordem, dentro do período; rótulo de até 22 caracteres |

No `dados.py copom`, os eventos são achados nas mudanças da própria SGS 432 (cada mudança da meta é uma decisão do
Copom): a 1ª alta e o 1º corte de cada ciclo e o início do pico. A data é a de **vigência** que a SGS registra (o dia
seguinte à reunião), e a fonte na tela diz isso.

### Peça: barra_linha

**O que acontece:** as barras do mês crescem do zero (para baixo se negativo), com o valor em cima de cada uma, e o
placar mostra o valor do mês da última barra que entrou (sempre um número real). Depois, cada barra **encolhe num
ponto, na altura do acumulado em 12 meses daquele mês**, enquanto a escala troca; a linha liga os pontos e o placar
pousa no último acumulado, em vermelho, com o único som.

O acumulado é **calculado** a partir do mensal (composto: prod(1 + m/100) dos 12 meses − 1, não a soma). Com
`referencia_12m` (a série oficial), cada mês mostrado tem de bater em até 0,01 p.p. (o BCB arredonda); se não bater,
`validar()` recusa e nada é gerado. O `dados.py ipca` sempre põe a SGS 13522 como referência e para se divergir.

| campo | padrão | o que faz |
|---|---|---|
| `mensal` | obrigatório | `[{data, valor}]` mês a mês, sem buraco, com 11 meses antes do 1º mostrado |
| `mostrar` | `12` | quantos meses (6 a 24), os últimos |
| `referencia_12m` | `null` | a série oficial do acumulado (SGS 13522) para conferir mês a mês |
| `rotulos` | `{"mes": "no mês", "doze": "em 12 meses"}` | texto sob o placar em cada fase |
| `duracao` | `9` | 5 a 10 s |

**Conferência (cache de 02/10/2026):** o acumulado calculado do 433 bate com a 13522 em todos os 69 meses do cache
(dez/2020 a ago/2026) dentro de 0,01 p.p.; nos 12 meses mostrados, a diferença é zero. Ago/2026: calculado
4,2235% → **4,22%**, SGS 13522 = **4,22%**. O único mês em que o arredondamento difere é dez/2022 (5,7848% → 5,78
contra 5,79 publicado), dentro da tolerância.

### Peça: numero_linha

**O que acontece:** o número grande (o último valor da série) pousa no centro com o único som e o rótulo
("meta Selic em 02/out/2026"). Ele encolhe e desliza até a faixa logo acima do último ponto do gráfico, os eixos
entram, o ponto final acende (um traço tracejado liga o número ao ponto) e **a linha se desenha da direita para a
esquerda**, do hoje até o começo. No fim, a variação ("+9,25 p.p. desde jan/2020") entra sob o número.

| campo | padrão | o que faz |
|---|---|---|
| `serie` | obrigatório | `[{data, valor}]` em ordem; o número é o último valor |
| `linha` | `"linha"` | `"degrau"` para a Selic |
| `rotulo_numero` | `"em 02/out/2026"` | texto sob o número grande |
| `variacao` | `null` | `"pp"` ou `"pct"`, como no grafico_cotacao |
| `classe` | `"indicador"` | `"ativo"` exige `"ativos": true` (e o aviso vai na tela) |

### Peça: manchete

**O que acontece:** a frase entra palavra por palavra e, no instante em que a palavra-chave é falada (`t_chave`),
ela se enche da esquerda para a direita: `"preencher"` = o texto vira vermelho; `"marca-texto"` = uma faixa vermelha
passa por trás e o texto fica da cor do papel. No fim do preenchimento, um pulso e o único som.

| campo | padrão | o que faz |
|---|---|---|
| `frase` | obrigatório | até 90 caracteres |
| `chave` | obrigatório | palavra(s) inteira(s) da frase, que aparecem uma vez só |
| `marca` | `"preencher"` | ou `"marca-texto"` |
| `palavras` | `null` | o instante (s) de cada palavra da frase, tirado da transcrição (ex.: Whisper com word timestamps); sem ele, as palavras entram em cascata |
| `t_chave` | o instante da chave em `palavras`, senão logo depois da cascata | quando a chave começa a encher; tem de terminar até 0,8 s antes do fim |
| `dur_chave` | `0.5` | 0,15 a 1,5 s |

No exemplo, a frase sai da SGS 13522: o verbo ("cai", "sobe" ou "fica") compara o último mês com o anterior
(ago/2026 4,22% contra jul/2026 4,44%), e a fonte na tela mostra os dois números.

## Compliance (vale para todas as peças)

- `fonte` é obrigatória e começa com `Fonte:`; ela fica no canto a peça inteira.
- **Ranking ou composição de ativos** (FII ou ação) exige `"ativos": true` e um `criterio` começando com `Critério:`
  (como a lista foi montada: universo, filtros, data). A tela mostra o critério e **"Não é recomendação de
  investimento."** Se algum rótulo tiver cara de ticker (`ABCD3`, `ABCD11`) e `ativos` não estiver ligado, a entrada é
  recusada.
- A barra-chave é escolha editorial (o ativo de que o vídeo fala), não indicação: a ordem é só a do número.
- O dado vem de origem conferida e o JSON guarda de onde saiu (`_origem`). Não digite número à mão: use o `dados.py`.
- **Lote 2** (texto livre: manchete, rótulos de evento, títulos): `estilo.checar_ativos` recusa a entrada se algum
  texto citar um ticker (`ABCD3`, `ABCD11`) sem `"ativos": true`; com ele, a tela mostra "Não é recomendação de
  investimento." O `eventos` também herda a regra do grafico_cotacao (ativo isolado só com comparador ou aviso).
  Os exemplos do lote 2 são só indicadores (Selic, IPCA): nenhum ativo aparece nem é recomendado.

## Testes

```sh
python3 -m pytest -q biblioteca/tests      # 114 testes (54 + 60), ~50 s
```

- validação: 17 casos de barras errada, 5 de rosca que não soma 100% (e não gera projeto), 6 outros de rosca;
- estilo: as cores e as fontes da variante `iec` são as da `PAL` do molde Burry (falha se divergirem); as do
  `fazaconta`, as do `build_hf.py`; nenhuma cor fixa em `barras/gerar.py` ou `rosca/gerar.py`; `fmt_br` igual ao do
  `grafico_cotacao`;
- dado real: o JSON do DY de caixa é igual ao SQLite do site-ativos **e** à tabela da página publicada
  (`saida/acoes/ranking/maiores-dy-de-caixa/`); o de cotistas é igual ao informe da CVM no SQLite e ao indicador que o
  site publica; o da Mega-Sena é igual ao fact-check e ao quadro "Números conferidos" (R$ 6,00 e 43,79% = R$ 2,63);
- **no navegador** (Chrome headless, mesmo `seek` do render): para os 5 exemplos, sem erro de JS e sem requisição
  falhando, fontes carregadas e, no último instante, cada valor/percentual na tela é igual ao do JSON, na ordem certa,
  com a largura proporcional (barras) ou o arco medindo o percentual (rosca), a chave no vermelho, o centro em
  R$ 2,63 e a soma em 100%. No meio: nas barras de dois momentos, a tela mostra os valores e a ordem do "antes"; na
  rosca, 2 fatias completas, a 3ª parcial e o resto zerado (uma por vez).

**Lote 2** (`tests/test_lote2.py`, 60 testes): 31 casos de entrada errada nas quatro peças (inclusive acumulado
que não bate com a 13522, mês faltando, chave fora da frase, chave antes de ser falada, ticker sem aviso); o
acumulado é composto (12 × 1% = 12,68%); estrutura: o `comum/quadro.mjs` passa no `node --check`, cada HTML
registra a timeline com o id da composição, carrega `assets/tela.js`, não usa CDN, tem a fonte no rodapé e só cores
da PAL; dado real: o acumulado do 433 bate com a 13522 em todos os meses do cache e dá 4,22% em ago/2026, os
exemplos são iguais ao SQLite (433, 13522, 432), os eventos são mudanças reais da 432; **no navegador**: eventos no
lugar, sem sobreposição e acesos só depois de a linha passar; barras com altura proporcional ao mês e, no fim,
pontos na altura do acumulado, placar em 4,22% vermelho; o número grande no centro e, no fim, pequeno logo acima do
último ponto, com a linha revelada de trás para a frente; a chave vazia antes da fala, pela metade no meio e cheia no
fim, na cor certa.

## Exemplos com dado real

| exemplo | estilo | dado | fonte na tela |
|---|---|---|---|
| `barras-dy-caixa-16x9` | iec | DY de caixa 12 m das 10 ações cobertas pelo site (VALE3 8,1% … PETR4 5,6% … PRIO3 0,0%), chave PETR4 | Fonte: CVM (DFC, 12 meses até 30/06/2026) e B3 (COTAHIST, 01/10/2026) |
| `barras-cotistas-9x16` | iec | cotistas dos 8 maiores FIIs da cobertura, ago/2025 → ago/2026; GARE11 passa BTLG11 e GGRC11 passa TRXF11; chave GGRC11 (190.185 → 411.230, +116,2%) | Fonte: CVM (informe mensal de FII, ago/2025 e ago/2026) |
| `rosca-megasena-9x16` | iec | pra onde vão os R$ 6 da Mega-Sena: 9 fatias somando 100,00%; centro R$ 2,63 | Fonte: Lei 13.756/2018, art. 16 |
| `rosca-megasena-fazaconta-16x9` | fazaconta | o mesmo | idem |
| `barras-megasena-fazaconta-9x16` | fazaconta | o mesmo, em barras (%) | idem |
| `eventos-selic-copom-16x9` | iec | Selic desde jan/2024 (11,75%; mínima 10,50%; hoje 13,75%) com 1ª alta 10,75% (19/09/2024), pico 15,00% (19/06/2025) e 1º corte 14,75% (19/03/2026) | Fonte: BCB/SGS 432 (meta Selic; data de vigência de cada decisão) |
| `barra-linha-ipca-16x9`, `-9x16` | iec | IPCA de set/2025 a ago/2026 (0,48 … 0,88 … −0,32) → 12 meses de 5,17% a 4,22% | Fonte: BCB/SGS 433 (IPCA mensal) · 12 meses calculado e conferido com a SGS 13522 |
| `numero-linha-selic-16x9`, `-9x16` | iec | 13,75% (02/10/2026) que vira o último ponto da Selic desde jan/2020 (+9,25 p.p.) | Fonte: BCB/SGS 432 (meta Selic) |
| `manchete-ipca-16x9` (preencher), `manchete-ipca-marcatexto-9x16` | iec | "Inflação em 12 meses cai para 4,22% em agosto", chave 4,22% | Fonte: BCB/SGS 13522 (IPCA em 12 meses, ago/2026; jul/2026: 4,44%) |

Divisão da Mega-Sena usada (fact-check do Faz a Conta, 26/09/2026, Lei 13.756 art. 16): prêmio 43,79% (com o IR),
custeio Caixa e lotéricas 19,13%, seguridade 17,32%, segurança pública (FNSP) 6,8%, esporte 4,36%, Funpen 3%,
cultura (FNC) 2,91%, COB 1,73%, CPB 0,96%. Somam 100,00%.

Render em `../exemplos/render/`, GIF em `../exemplos/gif/` e quadros em `../exemplos/frames/` (`*-quadros.jpg`: 4
instantes; `*-final.jpg`: o último quadro).

## Tempo de render medido

Linux, 4 núcleos Xeon 2,8 GHz, sem GPU, HyperFrames 0.8.78, workers automáticos, 30 fps, `--crf 20` (o padrão do
`renderizar.sh` da biblioteca; mude com `CRF=16`). Tempo de parede do `renderizar.sh` (gerar + render):

| peça | duração | render | MP4 | GIF |
|---|---|---|---|---|
| barras DY de caixa 16:9 (iec) | 8 s | 20,7 s | 1,2 MB | 864 KB |
| barras cotistas 9:16 (iec, dois momentos) | 8 s | 18,8 s | 1,4 MB | 704 KB |
| barras Mega-Sena 9:16 (fazaconta) | 8 s | 20,7 s | 872 KB | 438 KB |
| rosca Mega-Sena 9:16 (iec) | 8 s | 24,6 s | 1,0 MB | 420 KB |
| rosca Mega-Sena 16:9 (fazaconta) | 8 s | 33,3 s | 1,1 MB | 493 KB |
| eventos Selic/Copom 16:9 (lote 2) | 8 s | 20,3 s | 697 KB | 396 KB |
| barra_linha IPCA 16:9 | 9 s | 19,8 s | 734 KB | 355 KB |
| barra_linha IPCA 9:16 | 9 s | 19,4 s | 762 KB | 346 KB |
| numero_linha Selic 16:9 | 8 s | 19,9 s | 565 KB | 367 KB |
| numero_linha Selic 9:16 | 8 s | 17,4 s | 536 KB | 345 KB |
| manchete IPCA 16:9 (preencher) | 6 s | 14,3 s | 322 KB | 99 KB |
| manchete IPCA 9:16 (marca-texto) | 6 s | 14,2 s | 317 KB | 105 KB |

Na mesma faixa do gráfico de cotação (17 s por 8 s). No Mac, a estimativa é a mesma: 10 a 20 s por peça de 8 s,
~2 GB. Um job pesado por vez.

## Som

Um só, no pouso (`data-start` = instante do pouso − 30 ms): `impact-bass-1.mp3` da biblioteca `media-use` do
HyperFrames (`node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx/`), **Pixabay Content License** (uso
comercial, sem exigência de atribuição; ver `CREDITS.md` lá). É a escolha do Denis no A/B do TRXF11 ("só o número
aterrissando"). Sem tique de contagem e sem SFX sintetizado. Cada projeto gerado traz o crédito em `assets/CREDITOS.txt`.
Fontes: Montserrat e Archivo Black (SIL OFL 1.1, via @fontsource); GSAP 3.14.2 (licença sem custo).

## Onde usar

**Investir e Coçar**
- Barras: rankings de dividendos (DY de caixa, DY estimado de FII), "quem mais cresceu" em cotistas, patrimônio,
  vacância; antes → depois para "como mudou em 12 meses". Sempre com critério e aviso na tela.
- Rosca: composição de carteira de um FII (por segmento, por imóvel), destino do lucro (dividendos × reinvestimento),
  peso de setores num índice. Encaixa como peça do molde Burry, ao lado do gráfico de série.
- 9:16: o mesmo JSON vira insert de Short.

**Faz a Conta** (as peças servem direto aos episódios novos)
- Rosca: "pra onde vai o seu dinheiro" (Mega-Sena, bets, emendas, fundo eleitoral), sempre com soma 100% validada.
- Barras: comparações de chance, de preço e de repasse; antes → depois para "quanto mudou" (orçamento 2025 → 2026).
- O JSON entra no mesmo controle do quadro "Números conferidos": só número com status `conferido` (ou `calculado` a
  partir de conferido) vai para a tela.
