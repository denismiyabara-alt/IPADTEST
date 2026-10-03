# Identidade visual do canal "História do Brasil com humor"

Nome de trabalho na tela: **TEM DOCUMENTO**, que é também o bordão do narrador ("Parece piada. Mas tem documento."). Ele só está em `MARCA` no `revolta-da-vacina/build_hf.py`. **Antes de publicar, procure o nome no YouTube e no INPI.** Se estiver ocupado, troque nesse único lugar.

O motor é o mesmo do canal irmão: roteiro.md → blocos.py → voz → conferência → HyperFrames → efeitos → mix. **Nada do que aparece na tela é igual**, nem a paleta, nem a fonte, nem o palito, nem os sons. Um espectador que conhece um dos canais não reconhece o outro.

## O conceito: o arquivo histórico

Cada episódio é um **dossiê** aberto sobre a mesa. Tem papel envelhecido, ficha datilografada, recorte de jornal, carimbo e a íris de cinema mudo nas pausas. O conceito sai do próprio produto: o canal conta história **com documento**, e a fonte aparece na tela como uma ficha de arquivo.

## Paleta (tokens em `PALETA`, `build_hf.py`)

| Token | Cor | Uso | Por quê |
|---|---|---|---|
| `papel` | `#ecdfc0` | fundo (com vinheta `#d9c59c` nas bordas e fibra de papel) | papel de arquivo envelhecido, quente; o canal irmão usa um off-white frio (`#f6f2e8`) |
| `papel2` | `#f7efdc` | fichas, recortes, placas | a folha nova sobre a velha |
| `tinta` | `#1e2b4a` | traço do palito, títulos, texto | tinta de caneta-tinteiro azul-escura; o canal irmão usa quase-preto (`#1c1a17`) |
| `carimbo` | `#a8402b` | carimbo, destaque, a gravata do palito | vermelho-tijolo de carimbo de cartório; o canal irmão usa vermelho vivo (`#d6362b`) |
| `sepia` | `#7a5c3a` | legendas, fonte, marca-d'água | tinta desbotada; substitui o cinza neutro do canal irmão |
| `desbotado` | `#cdb991` | linhas de apoio, slots da tela final | |
| `sombra` | `#2a2016` | íris de cinema mudo | |

O contraste em tela cheia está bom: a tinta sobre o papel passa de 10:1, e o carimbo sobre o papel fica perto de 4,6:1 (calculado pela fórmula WCAG, valor aproximado). Por isso o carimbo só aparece em texto grande.

## Tipografia (OFL, local via @fontsource, sem Google Fonts nem CDN no render)

- **Alfa Slab One** (`@fontsource/alfa-slab-one`, OFL-1.1): títulos, anos, números grandes, carimbos. É uma serifa grossa de cartaz e de manchete de jornal do começo do século XX.
- **Courier Prime** (`@fontsource/courier-prime`, OFL-1.1): legendas, fichas, fontes. É a máquina de escrever do arquivo.
- O canal irmão usa Archivo Black e Montserrat (sem serifa), que nunca aparecem aqui.
- O `build_hf.py` copia os `.woff2` e o `gsap.min.js` do `node_modules` para `hf-<b>/assets/`. O render fica 100% local, sem depender de rede.

## O palito: O Cronista (`palito.py`)

| | Canal irmão | **O Cronista** |
|---|---|---|
| Cabeça | retângulo de cupom fiscal com serrilha | **círculo pequeno** (r = 24) |
| Acessórios | nenhum | **chapéu-coco** com fita vermelho-tijolo, **bigode de guidão**, **gravata-borboleta** |
| Membros | 1 segmento | **2 segmentos**: braço e antebraço (cotovelo), coxa e canela (joelho), com os pés de perfil |
| Proporção | cabeça grande | **alto e esguio** (cabeça ≈ 1/7 da altura) |
| Traço | 10 px, quase-preto, filtro de traço tremido | **7 px, tinta azul-escura, limpo** (sem o tremido) |
| Expressão | 4 bocas | 4 bocas (fechada, aberta, sorriso, "o"), **sobrancelhas** e a boca que **fala** no ritmo da frase |
| Gesto-assinatura | aceno | **tira o chapéu** ao abrir cada bloco e na tela final |
| Pausa de punchline | zoom de 2,6× na cara | **íris de cinema mudo** que fecha no rosto e reabre na frase seguinte |

**Poses** (dicionário de ângulos, com limites conferidos em teste): `idle`, `apontar`, `shrug`, `pensar` (mão no queixo), `maos`, `susto`, `vitoria` e `serio` (cabeça baixa, usada no bloco das mortes).
**Ações:** `andar_js` (ciclo com joelho, quando troca de lado), `falar_js` (a boca abre e fecha cerca de 6 vezes por segundo durante a frase, com semente fixa), `piscar_js`, `respirar_js`, `chapeu_js` e reação de susto ao carimbo.
Tudo fica numa timeline GSAP pausada, sem `Math.random` e sem `repeat:-1`, porque o HyperFrames busca quadro a quadro.

## Peças de cena (`pecas.py`)

`ficha` (a fonte na tela), `carimbo`, `ano` (datilografado, um algarismo por vez), `contador`, `lista` (✓/✗ datilografados), `recorte` e `recortes` (jornal de borda rasgada), `linha_tempo`, `calendario`, `duelo`, `placa` (anúncio pregado), `cardapio`, `multidao` (minipalitos com chapéu-coco, cartola, boné e palheta) e os desenhos `SERINGA`, `RATO`, `MOSQUITO`, `MEDALHA` e `napoleao` (a charge de 1904 redesenhada com bicorne e seringa no lugar da espada).
**Movimento:** a peça cai como papel (−70 px, com giro de 3 a 6°) e assenta. O carimbo bate e a mesa treme. O ano é batido na máquina. O canal irmão usa "pop" elástico, que aqui não entra.
**Textura:** fibra de papel (`feTurbulence` em sépia), uma dobra vertical no papel, grão de filme e cintilação de projetor (8 por segundo, semente fixa, opacidade entre 0,05 e 0,11).

## Som (`revolta-da-vacina/sfx.py`)

Todos os sons são sintetizados no próprio script (papel, carimbo de madeira, tecla e campainha de máquina de escrever, guincho de rato, clique de projetor). Nenhum vem de biblioteca, e nenhum é igual aos do canal irmão.

## Quadros de conferência

Os quadros abaixo foram renderizados no container com o HyperFrames 0.8.78 (Chromium local). A voz era falsa e o tempo das frases foi estimado.

- `quadros-chave/1-b0-uma-vacina.png`: carimbo "UMA VACINA" e o palito em susto
- `quadros-chave/2-b1-ficha-oswaldo-cruz.png`: ficha com a fonte na tela e o palito apontando
- `quadros-chave/3-b4-napoleao-da-seringa.png`: a charge redesenhada

O bloco b3 inteiro (34,3 s) também foi renderizado em MP4 no container (2 min 41 s, com GPU por software) para provar que o pipeline monta.
