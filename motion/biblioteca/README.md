# Biblioteca de animações de dado (Investir e Coçar e Faz a Conta)

Peças de B-roll de 5 a 10 s, no mesmo padrão do `grafico_cotacao`: HyperFrames 0.8.78, projeto autocontido
(fontes, GSAP e som copiados para `assets/`, nada de CDN), dado REAL e conferido com `Fonte: …` na tela, **um único
som, só no pouso**, formatos 16:9 e 9:16, e teste que prova que os números da tela são iguais aos do dado.

| peça | o que é | pasta |
|---|---|---|
| **barras** | barras horizontais que crescem do zero com o valor contando junto; com dois momentos (antes → depois), trocam de lugar | `barras/` |
| **rosca** | uma rosca que se divide em fatias, uma por vez, com rótulo e percentual; a soma tem de dar 100% | `rosca/` |

```
comum/estilo.py        estilos, formato brasileiro (fmt_br), validação comum; o estilo iec é LIDO do molde Burry
comum/projeto.py       monta o projeto: fontes, GSAP, som de pouso, créditos, <head>, filtro boil, marca-d'água
comum/quadro.mjs       abre o projeto num Chrome headless, faz seek e lê window.__tela() (genérico para qualquer peça)
comum/teste.py         ajuda dos testes de navegador (pulados sem node_modules ou Chrome)
biblioteca/dados.py    monta os JSON de exemplo a partir da origem (SQLite do site-ativos, fact-check do Faz a Conta)
biblioteca/barras/gerar.py, biblioteca/rosca/gerar.py   JSON → projeto HyperFrames
biblioteca/renderizar.sh   gerar + render + tempo (+ GIF com --gif)
biblioteca/tests/      54 testes
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

## Compliance (vale para as duas peças)

- `fonte` é obrigatória e começa com `Fonte:`; ela fica no canto a peça inteira.
- **Ranking ou composição de ativos** (FII ou ação) exige `"ativos": true` e um `criterio` começando com `Critério:`
  (como a lista foi montada: universo, filtros, data). A tela mostra o critério e **"Não é recomendação de
  investimento."** Se algum rótulo tiver cara de ticker (`ABCD3`, `ABCD11`) e `ativos` não estiver ligado, a entrada é
  recusada.
- A barra-chave é escolha editorial (o ativo de que o vídeo fala), não indicação: a ordem é só a do número.
- O dado vem de origem conferida e o JSON guarda de onde saiu (`_origem`). Não digite número à mão: use o `dados.py`.

## Testes

```sh
python3 -m pytest -q biblioteca/tests      # 54 testes, ~20 s
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

## Exemplos com dado real

| exemplo | estilo | dado | fonte na tela |
|---|---|---|---|
| `barras-dy-caixa-16x9` | iec | DY de caixa 12 m das 10 ações cobertas pelo site (VALE3 8,1% … PETR4 5,6% … PRIO3 0,0%), chave PETR4 | Fonte: CVM (DFC, 12 meses até 30/06/2026) e B3 (COTAHIST, 01/10/2026) |
| `barras-cotistas-9x16` | iec | cotistas dos 8 maiores FIIs da cobertura, ago/2025 → ago/2026; GARE11 passa BTLG11 e GGRC11 passa TRXF11; chave GGRC11 (190.185 → 411.230, +116,2%) | Fonte: CVM (informe mensal de FII, ago/2025 e ago/2026) |
| `rosca-megasena-9x16` | iec | pra onde vão os R$ 6 da Mega-Sena: 9 fatias somando 100,00%; centro R$ 2,63 | Fonte: Lei 13.756/2018, art. 16 |
| `rosca-megasena-fazaconta-16x9` | fazaconta | o mesmo | idem |
| `barras-megasena-fazaconta-9x16` | fazaconta | o mesmo, em barras (%) | idem |

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
