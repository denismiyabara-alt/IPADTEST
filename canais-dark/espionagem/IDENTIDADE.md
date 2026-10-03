# Identidade visual do canal de espionagem

A ideia: **sala de arquivo às escuras, uma lâmpada acesa sobre a mesa**. Fundo preto-carvão, texto em branco de arquivo, um único acento âmbar de lâmpada, máquina de escrever para tudo o que é documento e uma sans condensada para os títulos. Grão de filme leve por cima de tudo.

É diferente, de propósito, dos outros canais da casa: nada de fundo claro, nada de cor saturada, nada de personagem desenhado, e nada de sépia ou papel envelhecido (o tom do canal de história do Brasil). Aqui o papel só aparece quando é um documento de verdade, escaneado.

Os quadros de teste renderizados neste ambiente estão em `quadros/` (HyperFrames 0.8.78, Chrome headless, 1920×1080).

| Quadro | O que mostra |
|---|---|
| `quadros/rec-mapa-sanfernando-b0.jpg` | reconstituição: esquema da rua Garibaldi na noite da captura, relógio âmbar, selo RECONSTITUIÇÃO, fonte no rodapé |
| `quadros/documento-cia-1953-b3.jpg` | documento real (memorando da CIA de 9/10/1953, NARA RG 263): caixa âmbar no trecho, tradução datilografada ao lado, crédito vindo da planilha |
| `quadros/rec-rota-voo-b6.jpg` | mapa de grade (sem litoral de terceiros): rota Buenos Aires → Dakar → Lod se desenhando |

## Paleta

| Token | Cor | Uso |
|---|---|---|
| `--carvao` | `#111111` | fundo de tudo |
| `--carvao2` | `#1b1b1a` | reserva (painéis) |
| `--arquivo` | `#ece6d6` | texto principal, traços dos esquemas |
| `--ambar` | `#f2a93b` | **o único acento**: selo, rota, relógio, caixa de destaque, data ativa. Nunca em mais de um ou dois elementos por quadro |
| `--cinza` | `#8b877d` | fonte, crédito, rótulos secundários, marca d'água |
| `--linha` | `#2c2b29` | grade dos mapas |

Fotos de arquivo entram em **preto e branco** (filtro `grayscale` + contraste leve), mesmo quando o original tem cor: o âmbar fica só para o que o canal desenha.

## Tipografia (as duas com licença SIL Open Font License 1.1, arquivos em `fontes/`)

| Fonte | Uso |
|---|---|
| **Courier Prime** (Regular e Bold), Quote-Unquote Apps | máquina de escrever: datas grandes batidas letra a letra, documentos recriados, traduções, selo, fonte e crédito |
| **Barlow Condensed** (Medium e SemiBold), Jeremy Tribby | títulos, cartelas de ato (caixa alta, espaçamento largo), rótulos de mapa, marca d'água |

As fontes vão junto no repositório (a OFL permite redistribuir) e o `build_hf.py` copia para cada `hf-bN/assets/fontes/`: o render não depende de rede nem de fonte instalada no Mac.

## Textura e movimento

- **Grão de filme:** ruído fractal (SVG `feTurbulence`) em tela cheia, opacidade 0,09, semente trocada 12 vezes por segundo (determinístico, aguenta busca de quadro).
- **Vinheta:** escurece as bordas (gradiente radial).
- **Ritmo:** lento. Entradas de 0,6 a 1,4 s, `power2/power3.out`. Nada de tremor de tela, carimbo batendo, "zoom punch" nem som de impacto: o assunto não comporta.
- **Ken Burns** lento nas fotos (escala 1,00 → 1,12 ao longo da cena).
- **Máquina de escrever:** datas e nomes aparecem letra a letra, com cursor âmbar piscando.

## Peças (todas em `build_hf.py`, usadas pelo `cenas_hf.py` de cada episódio)

| Peça | O que é | Selo |
|---|---|---|
| `cartela_ato(titulo, sub)` | régua âmbar + título condensado do ato | — |
| `titulo(t, sub)` | título do episódio | — |
| `datilo(texto)` | texto batido à máquina (data, nome) | RECONSTITUIÇÃO se `rec=True` |
| `preto(linhas)` | texto sobre preto, sem imagem. **É a única forma de narrar morte** | — |
| `arquivo(img)` | foto livre com Ken Burns; crédito automático da planilha | crédito |
| `documento(img, caixa, traducao)` | página escaneada, caixa âmbar no trecho, tradução ao lado | crédito |
| `video(arq)` | trecho de cinejornal livre, mudo | crédito |
| `rota(pontos, caixa)` | mapa de grade (paralelos/meridianos calculados no Python), rota que se desenha | RECONSTITUIÇÃO + ESQUEMA |
| `mapa_sf(noite, carros, relogio)` | esquema da rua Garibaldi (sem geometria real) | RECONSTITUIÇÃO + ESQUEMA |
| `linha_tempo(eventos, ativo)` | eixo 1906–1962, o ano ativo acende | RECONSTITUIÇÃO |
| `silhueta(tipo)` | figuras **sem rosto**, vetoriais | RECONSTITUIÇÃO |
| `planta()` | planta esquemática da casa | RECONSTITUIÇÃO + ESQUEMA |
| `placar(sim, não, abst)` | votação | RECONSTITUIÇÃO |
| `lista_fontes(itens)` | bibliografia no fecho | — |

Fixos em todo quadro: marca d'água do canal no canto superior direito (variável `CANAL_NOME`, padrão `CODINOME`, trocar quando o nome for escolhido), cartela `FONTE:` no canto inferior esquerdo (gerada das linhas `* fonte:` do roteiro) e crédito da imagem no canto inferior direito (gerado da coluna `credito_na_tela` da planilha).

## Regras visuais que não mudam

1. Nenhuma imagem realista gerada por IA de pessoa ou de fato real. Reconstituição é sempre motion gráfico, com o selo.
2. Morte contada, nunca mostrada: cartela `preto()`, sem foto de forca, cela, corpo ou cinzas (há um teste para isso).
3. Suástica só dentro de documento ou foto de arquivo e com narração explicando; nunca na miniatura.
4. Mapas do canal são de grade ou esquema; litoral só de fonte em domínio público (Natural Earth), se um dia entrar.
5. Miniatura: fundo carvão, uma palavra em Barlow Condensed, uma data em Courier âmbar, foto de arquivo em P&B. Sem arma, sem sangue, sem rosto em close de criminoso como "herói".
