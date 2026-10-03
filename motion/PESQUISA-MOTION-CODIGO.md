# Motion graphics escrito em código por modelos de IA: o que copiar para o Investir e Coçar

Data da pesquisa: 03/10/2026. Para o `motion/` deste repo (HyperFrames 0.8.78, GSAP 3.14.2) e para a skill de edição
(`edicao-skill/`: `plano.py`, `mapa.py`, `gerar-cartelas.py`).

**Como ler as marcas:**
- **[aberto]**: abri a página e o que está escrito saiu dela.
- **[só busca]**: o domínio estava bloqueado pelo proxy, e a informação veio do resumo do buscador. Trate como indício.
- **[conferido aqui]**: verifiquei neste ambiente (arquivo, pacote ou banco).

Quase todas as fontes indicadas estavam bloqueadas (lista na seção (d)). O que abriu foi o GitHub. Por isso, a parte de
**estrutura** (pipeline, regras, checagem) está bem apoiada; a parte de **exemplos visuais** vem, em grande parte, de
resumo de busca.

**Estilo congelado do canal (não muda nada aqui):** papel `#F4F1EA`, Anton + Inter + JetBrains Mono, vermelho
`#C8261D` e ouro `#966B00` (no máximo 2 cores de destaque), dado real com "Fonte:" na tela, **um** som só no pouso
(`impact-bass-1`), corte seco sem fade, HyperFrames.

---

## O que as pessoas estão fazendo (resumo em 6 linhas)

1. O modelo **não gera vídeo**: escreve um programa (HTML com SVG/Canvas, GSAP, às vezes three.js) em que cada quadro é
   função do tempo `t`. Um navegador headless posiciona o tempo quadro a quadro e o ffmpeg junta. É exatamente o que o
   HyperFrames já faz no canal.
2. Os virais (história da civilização ocidental em 2min16, "showreel de motion designer" em 15 s, clipe de música)
   são **abstratos**: tipografia cinética, formas geométricas, interface. Nenhum traz dado real com fonte.
3. Quem mostra o processo admite que **não foi um prompt só**: lista de estados, referência e várias rodadas de correção
   (Charlie Hills); storyboard e segunda passada (o vídeo da civilização ocidental).
4. O padrão de prompt que funciona é **"lista de estados, não clima"**: nomear cada estado da animação e o instante
   em que ele acontece.
5. O pipeline sério é **determinístico**: proíbe `Math.random()` sem semente, `Date.now()`, transição de CSS e
   `<video>`/`<audio>` dentro da cena, e checa a cena antes do render (erro de JS, texto visível em vários instantes).
6. A conferência visual é por **folha de quadros** (contact sheet) com nota, repetida até passar.

---

## (a) Técnicas visuais copiáveis para o estilo congelado

Ordem: as cinco pedidas primeiro, depois duas de apoio. Todas são SVG/DOM com a timeline do GSAP pausada que o
HyperFrames posiciona (`window.__timelines[...]`), igual ao `grafico_cotacao/gerar.py`. Nenhuma usa filtro de blur,
WebGL nem vídeo, então o custo fica na faixa medida do gráfico de série: **~17 s de render para 8 s de peça,
~2 GB de pico** (Linux, 4 núcleos; README do `motion/`).

> **Licença do GSAP, corrigindo o README:** o `motion/README.md` diz "sem `DrawSVGPlugin` (pago)". Desde a 3.13, todos
> os plugins são grátis, inclusive para uso comercial. O pacote `gsap@3.14.2` que o canal já fixa traz
> `dist/MorphSVGPlugin.min.js`, `dist/DrawSVGPlugin.min.js` e `dist/SplitText.min.js`, e o README do pacote diz
> "GSAP is now 100% FREE including ALL of the bonus plugins" **[conferido aqui: `npm pack gsap@3.14.2`]**. A regra de
> não usar DrawSVG pode continuar por outro motivo (o recorte por `clipPath` já está testado), mas licença não é mais
> impedimento. O `gerar.py` copia o plugin para `assets/` como já faz com o `gsap.min.js`, sem CDN.

### 1. Barra que vira linha (morph de gráfico)

- **O que é.** Um gráfico de barras se transforma num gráfico de linha **sem corte**: cada barra encolhe até virar o
  ponto do topo dela, e os pontos se ligam numa linha. A mudança de forma conta uma mudança de leitura ("cada mês é
  pouco; somado, vira isto").
- **Onde aparece.** É um dos 16 motions do Charlie Hills ("a bar chart that morphs into a line"), com o método em 3
  passos: escolher um movimento, mostrar uma referência e **nomear cada estado**, pedir HTML+SVG e corrigir por rodadas
  [só busca: https://charliehills.substack.com/p/opus-55-motion-graphics e
  https://x.com/charliejhills/status/2103893708550914076]. A Remotion tem um prompt de barra + linha combinadas
  [só busca: https://www.remotion.dev/prompts/bar-line-chart-combined].
- **Como fazer em HyperFrames/GSAP (sem MorphSVG, com a integridade do dado em todo quadro):**
  1. No Python, calcular para cada ponto `i` o `x_i`, o topo `y_i` e a base `y0`. As barras e a linha usam **a mesma
     escala**, então o topo da barra é exatamente o ponto da linha.
  2. Estado A (barras): `rect` de largura `w`, de `y0` até `y_i`.
  3. Estado B (pontos): a altura vai a zero **subindo a base até o topo**, e a largura vai de `w` ao diâmetro do ponto.
     Um único `prog.p` de 0 a 1 controla tudo num `onUpdate`, como o `desenhar()` do `gerar.py`.
  4. Estado C (linha): a linha que liga os topos se revela da esquerda para a direita pelo mesmo `clipPath` do gráfico
     de série (`#cortina`).
  5. Pouso: o número do último ponto ganha a cor de destaque e toca o som.

  ```js
  // D.pts = [{x, y}], D.y0, D.w vêm do Python (mesma escala para barra e linha)
  const m = { p: 0 };
  function barras() {
    D.pts.forEach((pt, i) => {
      const r = document.getElementById('b' + i);
      const base = D.y0 + (pt.y - D.y0) * m.p;          // a base sobe até o topo
      const w = D.w + (D.dot - D.w) * m.p;              // a barra afina até virar ponto
      r.setAttribute('x', pt.x - w / 2); r.setAttribute('width', w);
      r.setAttribute('y', Math.min(pt.y, base)); r.setAttribute('height', Math.abs(base - pt.y));
      r.setAttribute('rx', (w / 2) * m.p);              // canto arredonda no fim
    });
  }
  tl.to(m, { p: 1, duration: 1.0, ease: 'power2.inOut', onUpdate: barras }, D.tMorph);
  tl.to('#cortina', { attr: { width: D.larguraUtil }, duration: 1.2, ease: 'power1.inOut' }, D.tMorph + 0.8);
  ```

  Com MorphSVG (agora grátis) dá para fazer o morph de um `path` só (`morphSVG: '#linha'`), mas ele interpola formas
  e não garante que o meio do caminho corresponda a algum dado. O jeito por ponto acima é mais honesto e testável.
- **Custo de render.** Igual ao gráfico de série (24 a 36 elementos SVG).
- **Combina com dado real?** Sim, e é onde ela faz sentido: **a mesma série em duas leituras** (mensal → acumulado).
  Não use para trocar de grandeza (barra de uma coisa vira linha de outra): isso engana.

### 2. Manchete que "se enche" (de dado, de marca-texto ou de imagem)

- **O que é.** O texto da manchete entra vazado (só contorno) e é preenchido. Três variantes: (a) o **gráfico da série
  desenhado dentro das letras**; (b) um **nível** que sobe até uma fração que é o próprio dado; (c) o marca-texto que o
  canal já tem nos prints.
- **Onde aparece.** "A headline that fills with artwork" no Charlie Hills [só busca, link acima]. Máscara de texto com
  SVG e GSAP é técnica conhecida de tipografia cinética
  [só busca: https://tympanus.net/codrops/2023/01/31/bringing-letters-to-life-coding-a-kinetic-svg-typography-animation/].
  O pacote `motion-graphics-skills` traz `animated-chart` "com precisão exata do valor" e kinetic type sobre HyperFrames
  [aberto: https://github.com/anupamme/motion-graphics-skills].
- **Como fazer:**
  1. `<clipPath id="letras"><text ...>SELIC</text></clipPath>`, com Anton em tamanho extremo (a fonte já é copiada para
     `assets/`, subset `latin`).
  2. Dentro de `<g clip-path="url(#letras)">`, desenhar o conteúdo: a linha/área da série (variante a) ou um `rect`
     cuja altura é `valor / teto` da escala (variante b).
  3. Por cima, o mesmo `<text>` só com `stroke` em tinta escura, para o contorno ficar legível o tempo todo.
  4. Animar o preenchimento com a mesma `#cortina` (a) ou com `attr: { y, height }` (b). O número em JetBrains Mono ao
     lado pousa junto, com o som.
- **Custo de render.** Baixo. Texto em `clipPath` é barato; não use `filter` (blur, turbulência), que é o que encarece.
- **Combina com dado real?** A variante (a) sim, sem fato novo: é a mesma série do gráfico. A (b) só quando a escala
  tem um teto **com fonte** (por exemplo, o teto da meta de inflação, que precisaria de documento do CMN conferido); sem
  isso, o nível é decoração e não deve parecer dado.

### 3. Transição por objeto (o elemento de uma cena vira o da próxima)

- **O que é.** Em vez de cortar, um elemento da cena A viaja e vira um elemento da cena B: o número grande encolhe e
  vira o ponto final do gráfico; o ponto do gráfico cresce e vira o círculo de um ícone; a barra vira a régua da
  manchete. No cinema, é o *match cut*.
- **Onde aparece.** O "botão que abre um player" do Charlie Hills é desse tipo [só busca]. O `motion-launch-video`
  documenta transições "zoom-through" e "diagonal wipe" num template de linha do tempo
  [aberto: https://github.com/SuhaasNv/motion-launch-video]. O plugin Flip do GSAP faz transição de elemento
  compartilhado na web [só busca: https://motion.page/learn/using-gsaps-flip-plugin-in-motion-page-%F0%9F%94%A5/].
- **Como fazer em HyperFrames:**
  1. As duas cenas ficam **na mesma composição** (uma peça de B-roll com 2 cenas), cada uma no seu `section.clip`.
  2. O objeto que atravessa fica num **terceiro elemento** num `data-track-index` mais alto, com `data-start` no fim da
     cena A e duração que passa da fronteira.
  3. O Python calcula as duas geometrias (posição e tamanho em A e em B), e a timeline faz
     `tl.fromTo('#ponte', {x:xA, y:yA, scale:sA}, {x:xB, y:yB, scale:sB, duration:.5, ease:'power3.inOut'}, tFronteira)`.
     Não use o Flip no render: ele mede o DOM em tempo de execução, e o determinismo fica melhor com as duas posições
     calculadas antes.
  4. Na fronteira, o elemento original de A some e o de B aparece no mesmo quadro (`tl.set`), escondidos atrás da ponte.
- **Limite no fluxo atual.** As peças de B-roll são MP4 separados, cortados e concatenados com a câmera do Denis entre
  eles (`montar_final.py`). A transição por objeto só funciona **dentro de uma peça com mais de uma cena**. Entre peças
  separadas por câmera, o corte seco continua.
- **Custo de render.** Baixo; é um elemento a mais.
- **Combina com dado real?** Sim, quando o objeto é o mesmo dado nas duas cenas (o "13,75%" do placar é o último ponto
  da Selic). Não invente ligação entre dados diferentes.

### 4. Número que vira gráfico

- **O que é.** Abre com o número gigante do jeito que o canal já faz (count-up, Anton, pouso com som). Em vez de a
  cena acabar, o número **encolhe e voa até o canto direito**, onde vira o último ponto da série, e a linha se desenha
  **para trás**, mostrando o caminho até ali. É o caso particular mais útil da técnica 3.
- **Onde aparece.** Os blocos de "stat animations" e "charts" da categoria de motion graphics do HyperFrames
  [só busca: https://github.com/heygen-com/hyperframes e páginas de skill do catálogo]; o `milestone-reveal` (contagem
  numérica) e o `animated-chart` do `motion-graphics-skills` [aberto, link acima]. A combinação dos dois numa cena só não
  apareceu pronta em nenhuma fonte: é adaptação.
- **Como fazer:**
  1. Cena 1 (0 a ~2 s): o placar do `gerar.py` com o último valor, já pousado (o som toca aqui, uma vez).
  2. Ponte (~0,5 s): o `#numero` faz `fromTo` de `{x, y, scale:1}` para a posição e escala do rótulo do último ponto,
     calculadas no Python; um círculo nasce no lugar onde o ponto vai ficar.
  3. Cena 2: a `#cortina` do `clipPath` anda **da direita para a esquerda** (anima `x` e `width` juntos) e revela o
     histórico. O kicker e a "Fonte:" entram junto. Nada de segundo som.
- **Custo de render.** Igual ao gráfico de série.
- **Combina com dado real?** Sim, é o caso ideal: o número que o Denis fala é o último ponto de uma série de fonte
  primária.

### 5. Eventos que entram na linha do tempo

- **O que é.** Enquanto a ponta da linha corre, marcos acendem quando ela passa pela data: "1ª alta", "pico",
  "1º corte". O espectador ganha um marco a cada 1 a 2 s.
- **Onde aparece.** É a gramática dos explainers de história em código (o vídeo da civilização ocidental: storyboard
  por cena, marco a marco) [só busca: https://x.com/minchoi/status/2103461343663730868]. No canal, já existe em parte:
  os `destaques` do `grafico_cotacao` (até 3, acendem pela inversa do easing) e a melhoria nº 5 da `PROPOSTA.md`.
- **Como fazer (o que falta):**
  1. **Eventos tirados do próprio dado, não escritos à mão.** Para a Selic, cada mudança da meta na SGS 432 é uma
     decisão do Copom. Uma função `eventos_da_serie()` acha "primeira alta depois do vale", "máximo" e "primeiro corte
     depois do máximo" e gera os rótulos com data e valor. Assim, o rótulo nunca discorda do gráfico.
  2. O instante de cada um continua saindo da inversa do easing (`tempo_da_ease`), que já existe e é testada.
  3. Rótulo alternando acima/abaixo, com checagem de colisão em pixels no Python antes de gerar.
  4. Faixa de período opcional (`rect` com opacidade baixa entre duas datas), só com fonte.
- **Custo de render.** Igual ao gráfico de série.
- **Combina com dado real?** Sim. Evento com texto livre ("pandemia", "crise de 2008") precisa de fonte própria e entra
  no mesmo controle de números conferidos.

### 6 e 7. De apoio (já existem ou são baratas)

- **Texto que entra por palavra (SplitText).** O plugin agora é grátis e está no pacote. Serve para a peça "frases",
  com o mesmo grid de entrada `0.12 + i*PASSO` da skill. Custo baixo.
- **Linhas em base 100 que se separam** (comparador). Já é a melhoria nº 4 da `PROPOSTA.md`; a técnica 1 (morph) e a 5
  (eventos) servem a ela sem mudança.

---

## (b) Prompts e estruturas que eles usam para o modelo compor a cena em código

### O que se repete em todas as fontes

1. **Saída = programa, não vídeo.** "Escreva uma cena que renderize qualquer instante `t`": um HTML com Canvas ou SVG,
   que define `window.DURATION` e expõe `async window.seek(t)`; cada pixel é função pura do tempo
   [só busca: https://huggingface.co/blog/karmen-beatapi/how-to-make-videos-with-claude-opus-5-5 e
   https://youmind.com/opus-5-5-prompts].
2. **Determinismo como regra escrita no prompt.** Proibido: `Date.now`, laço de `requestAnimationFrame`, timers,
   transição de CSS, `Math.random()` sem semente. O LaunchVideo também proíbe `<video>`, `<audio>`, `<iframe>` e imagem
   externa [aberto: https://github.com/diggerhq/shipvideo].
3. **Pipeline em 4 passos:** o modelo escreve a cena → um navegador headless move a cena para `t` e tira o quadro →
   ffmpeg codifica em H.264 → o áudio entra depois, num mux separado [só busca: blog do Hugging Face]. O LaunchVideo usa
   Playwright com **relógio virtual injetado** (controla rAF, timers, `Date` e animações CSS/WAAPI por `__seek(t)`),
   JPEG por quadro, `libx264 crf 18 yuv420p +faststart`, 1920×1080 a 30 fps; 30 s de filme renderizam em 30 a 40 s
   [aberto]. O `motion-launch-video` captura a 120 fps e mistura pares de quadros para 60 fps, simulando motion blur
   [aberto].
4. **Lista de estados, não clima.** "Escreva a lista de estados, não a vibe", com um modelo em XML aberto
   [só busca: https://x.com/0xMovez/status/2104216919033192746]. "Mostre uma referência e nomeie cada estado"
   [só busca: Charlie Hills].
5. **Storyboard antes do acabamento.** Animatic em 960×540 com áudio provisório para acertar o ritmo antes de polir
   [só busca: 0xMovez]. "Estude o produto, faça o storyboard numa grade de batidas, construa, revise com contact sheets,
   ponha o som, renderize" [aberto: motion-launch-video].
6. **Checagem visual com nota.** Renderizar 3 a 5 quadros, dar nota de 1 a 10 por critério, registrar num
   `docs/review_log.md` e repetir até tudo dar 8 ou mais [só busca: 0xMovez]. O LaunchVideo tem a ferramenta
   `check_scene`: carrega o HTML sob o relógio virtual, relata erro de JS e **captura o texto visível em vários
   instantes** antes do render [aberto].
7. **"Fatos primeiro".** O `motion-graphics-skills` exige que nomes e números saiam de uma lista aprovada e checa
   texto cortado, sobreposição e exatidão quadro a quadro antes de exportar; todo skill lê antes um `brand.md` e um
   `MOTION.md` [aberto: https://github.com/anupamme/motion-graphics-skills].
8. **Conhecimento injetado por tema.** O gerador de motion da Remotion classifica o pedido, detecta quais "skills"
   (gráfico, tipografia, transição) se aplicam e injeta só esses guias e exemplos no prompt; pede constantes no topo
   do código para edição fácil [aberto: https://github.com/remotion-dev/template-prompt-to-motion-graphics-saas].
9. **Custo.** O LaunchVideo gasta ~100 mil tokens por filme de 20 a 40 s e leva ~4 min do URL ao MP4
   [só busca: https://launchvideo.io/ e https://ai-tldr.dev/releases/diggerhq-launchvideo/].

### O canal já tem a maior parte disso

| prática de fora | no canal hoje |
|---|---|
| render quadro a quadro, sem tempo real | HyperFrames posiciona a timeline do GSAP quadro a quadro |
| `seek(t)` + texto visível em vários instantes | `quadro.mjs` lê o número na tela num instante; o teste compara com o último valor da série |
| folha de quadros antes do render cheio | `npx hyperframes snapshot --at ...` |
| `brand.md` / `MOTION.md` | estilo congelado em `molde-burry/` e nas receitas `investir-cocar-broll-*` |
| "fatos primeiro" | "Números conferidos" do Faz a Conta, `fonte` obrigatória e `validar()` no `gerar.py` |
| cena ancorada no tempo | `plano.py` ancora na **frase**, que é melhor que timecode |

**O que falta:** (1) uma **especificação de cena** curta que o modelo escreva **no lugar do HTML**; (2) a lista de
estados com o instante de cada um, que vira teste; (3) o revisor com nota, de contexto limpo.

### Como adotar (decisão)

- **Não adotar** "o modelo escreve o HTML livre de cada cena". No canal, o HTML sai de **gerador Python** a partir de
  JSON (`gerar.py`, `gen.py`, `gerar-cartelas.py`) e foi assim que o estilo ficou aprovado. HTML livre por cena
  reabre o risco de "ficou amador" e de número sem fonte na tela.
- **Adotar** a especificação de cena: o modelo escolhe a técnica de um **catálogo fechado** (as da seção (a), cada uma
  com seu gerador), aponta o dado (série e recorte, nunca o número digitado) e escreve a **lista de estados**. O Python
  valida, busca o dado, gera o HTML, e os estados viram as checagens.
- **Usar HTML livre só para prototipar técnica nova.** Quando uma técnica nova for aprovada pelo Denis numa cena, ela
  vira função de gerador e entra no catálogo.
- **Encaixe no fluxo da skill:**
  1. `plano.py`: tupla nova com peça `"M"` (motion), por exemplo `("m1-selic", "M", r"a selic chegou a", 0.0)`.
     A duração continua saindo da fala, e o `plano.json` passa a duração para a cena.
  2. `cenas/m1-selic.json`: a especificação abaixo. O `duracao` vem do `plano.json`, não do modelo.
  3. `motion/biblioteca/<tecnica>.py` gera o projeto HyperFrames. O `snapshot` sai **nos instantes dos estados**.
  4. Checagem automática (o `check_scene` do canal): sem erro de JS, sem requisição falhando, 5 fontes carregadas e,
     em cada estado, o texto na tela igual ao `espera` da spec (é o que o `quadro.mjs` já faz para o número final).
  5. Revisor de contexto limpo olha a folha de quadros com uma rubrica de 5 itens (legível em celular, fonte visível,
     no máximo 2 cores de destaque, nada cortado, o número da tela igual à fala) e dá nota; abaixo de 8, volta.
  6. `mapa.py` e `montar_final.py` tratam o MP4 como qualquer outra peça, em frames inteiros.

### Proposta: especificação de cena no padrão do canal

**Prompt-modelo** (o que se manda ao modelo, com o trecho do roteiro e o catálogo):

```text
Você vai escrever UMA especificação de cena em JSON para o B-roll do Investir e Coçar. Não escreva HTML.

Trecho do roteiro (a cena entra nesta frase): "{frase_ancora}"
Duração (vem da fala, não mude): {duracao} s. Formato: {16:9 | 9:16}.

Regras:
- Escolha UMA técnica do catálogo: serie | barra_vira_linha | numero_vira_grafico | manchete_enche | eventos.
- O dado vem de fonte primária livre: BCB SGS (código), B3 COTAHIST (ticker) ou IBGE (tabela). Informe a série
  e o recorte de datas. Nunca digite o valor: o gerador busca.
- "valor_falado" é o número exatamente como o Denis fala. Se o dado não bater com a fala, diga isso; não arredonde.
- Escreva a lista de estados: cada estado tem um nome, o instante (s) e o que deve estar legível na tela.
  Máximo de 5 estados. O pouso é o único com som.
- Textos: título em até 5 palavras, kicker em até 6. Sem adjetivo; o dado fala.
- Estilo é fixo (papel, Anton/Inter/JetBrains Mono, vermelho e ouro). Não proponha cor, fonte ou efeito.

Responda só com o JSON.
```

**JSON de exemplo** (técnica 4, número que vira gráfico, com eventos da técnica 5):

```json
{
  "id": "m1-selic",
  "ancora": "a selic chegou a",
  "tecnica": "numero_vira_grafico",
  "formato": "16:9",
  "duracao": 8.0,
  "dado": {
    "fonte": "bcb",
    "serie": 432,
    "desde": "2020-01-01",
    "ate": "ultimo",
    "rotulo_fonte": "Fonte: BCB (SGS 432)",
    "linha": "degrau",
    "unidade": { "sufixo": "%", "casas": 2 }
  },
  "valor_falado": "13,75%",
  "textos": { "titulo": "Selic: de 2% a 15%", "kicker": "Meta da taxa Selic · Copom" },
  "eventos": { "modo": "automatico", "quais": ["minimo", "maximo", "primeiro_corte"] },
  "estados": [
    { "nome": "placar",  "t": 0.4, "espera": ["13,75%", "Fonte: BCB (SGS 432)"] },
    { "nome": "pouso",   "t": 1.6, "espera": ["13,75%"], "som": "impact-bass-1" },
    { "nome": "ponte",   "t": 2.3, "espera": ["13,75%"] },
    { "nome": "historia","t": 5.5, "espera": ["Mínima: 2,00%", "Máxima: 15,00%"] },
    { "nome": "fim",     "t": 7.9, "espera": ["+9,25 p.p. desde jan/2020"] }
  ]
}
```

Os estados viram três coisas ao mesmo tempo: os instantes do `snapshot --at`, as asserções do teste no navegador e a
folha que o revisor avalia. O `valor_falado` é comparado com o último valor da série antes de gerar (regra "a fala ganha
da cartela" do README). Os valores do exemplo são os do `exemplos/selic-16x9.json` e do SQLite do site-ativos
(última meta 13,75% em 02/10/2026) **[conferido aqui]**.

---

## (c) As técnicas a implementar primeiro em `motion/biblioteca`

Só com dado que já está no cache do site-ativos (`site-ativos/cache/dados.sqlite` e `cache/raw/`) **[conferido aqui]**:
SGS 11 e 12 (Selic diária e CDI, 2020-01-02 a 2026-10-01), 432 (meta Selic, até 2026-10-02), 433 (IPCA mensal) e 13522
(IPCA 12 meses, ambos até ago/2026), COTAHIST 2021 a 2026 (2.252 tickers). A tabela `provento` está **vazia**, então
datas-com ficam de fora por enquanto.

1. **Número que vira gráfico + eventos automáticos** (técnicas 4 e 5 juntas).
   - **Por que primeiro:** reaproveita quase todo o `grafico_cotacao` (escala, degrau, `clipPath`, inversa do easing,
     placar, som no pouso, teste de "número na tela = último valor"). Junta o que o Denis já aprovou (o número que
     pousa) com a história do número. Os eventos saem do dado, então não há texto novo para conferir.
   - **Dado:** meta Selic, BCB SGS 432, jan/2020 a out/2026 (2,00% → 15,00% → 13,75%). Eventos: mínima, máxima e
     primeiro corte, detectados nas mudanças da série. Variante 9:16 para Short com o mesmo JSON.
   - **Esforço estimado:** ~1 dia (a ponte, a cortina ao contrário e `eventos_da_serie()` com teste).

2. **Barra que vira linha: IPCA mês a mês → IPCA acumulado**.
   - **Por que:** é a técnica mais citada nas fontes, é a que o canal não tem, e serve aos temas que convertem
     (inflação, Tesouro IPCA+, renda). A transformação diz algo verdadeiro: o mesmo dado em duas leituras.
   - **Dado:** IPCA, BCB SGS 433, últimos 24 meses (set/2024 a ago/2026) em barras; a linha é o acumulado
     `∏(1 + v/100) − 1` desses mesmos meses, calculado no gerador. Conferência: o acumulado dos 12 últimos meses tem que
     bater com a SGS 13522 do mesmo mês (4,22% em ago/2026), e isso vira teste.
   - **Esforço estimado:** ~1 dia.

3. **Manchete que se enche com a série** (técnica 2, variante a).
   - **Por que:** é barata, dá abertura forte para a peça "frases" e usa a mesma série da nº 1, sem fato novo.
   - **Dado:** a mesma SGS 432 desenhada dentro de "SELIC", ou o fechamento do PETR4 (COTAHIST 2025-2026, já testado
     contra o arquivo cru no `grafico_cotacao`) dentro de "PETR4". Atenção: o COTAHIST não é ajustado por proventos; o
     `serie.py` já recusa saltos acima de 35%.
   - **Esforço estimado:** ~½ dia.

A transição por objeto (técnica 3) fica para depois: no fluxo atual, as peças são separadas por câmera, e ela só rende
dentro de uma peça de várias cenas. A nº 1 já é um caso particular dela.

Regra para as três: uma cena primeiro, mostrar ao Denis, só então propagar.

---

## (d) Hype × realidade

| o que se diz | o que as fontes mostram |
|---|---|
| "Um prompt só, um tiro só." | Quem abre o processo mostra lista de estados, referência e rodadas de correção (Charlie Hills: "não foi um prompt"); o vídeo da civilização ocidental teve storyboard e segunda passada [só busca]. O curso do 0xMovez repete crítica até nota 8 [só busca]. |
| "Substitui o motion designer." | Funciona bem em forma geométrica, tipografia cinética e interface; é fraco em realismo [só busca]. Os virais são abstratos e **nenhum traz dado real com fonte**. A parte difícil do canal (dado certo, fonte, número igual à fala) não aparece em nenhum exemplo. |
| "Vídeo gerado por IA." | Não há modelo de vídeo: é HTML/JS renderizado por navegador headless e ffmpeg. É o mesmo mecanismo que o canal já usa com HyperFrames desde antes da onda. |
| "Rápido e barato." | LaunchVideo: ~100 mil tokens e ~4 min por filme de 20 a 40 s, render em torno de 1:1 [aberto/só busca]. No canal, o render medido é ~17 s por 8 s com ~2 GB, e o Denis já reprovou três rodadas de "ficou amador" de ~30 min cada. O gargalo é o gosto e a conferência, não o código. |
| "Ganha nota por ser bonito." | Para um canal de finanças, um gráfico bonito com número errado é pior que nenhum. Por isso a proposta é catálogo fechado + dado buscado pelo gerador + estados testados, e não HTML livre. |
| "DrawSVG/MorphSVG são pagos." | Não são mais: grátis desde a 3.13, e já estão no `gsap@3.14.2` do canal [conferido aqui]. |

### Fontes: o que abriu e o que não abriu

**Abriram [aberto]:**
- https://github.com/diggerhq/shipvideo (o repositório do LaunchVideo)
- https://github.com/heygen-com/hyperframes
- https://github.com/anupamme/motion-graphics-skills
- https://github.com/remotion-dev/template-prompt-to-motion-graphics-saas
- https://github.com/SuhaasNv/motion-launch-video
- pacote npm `gsap@3.14.2` (via `npm pack`) [conferido aqui]

**Bloqueadas pelo proxy (usado só o resumo da busca, marcado [só busca]):**
- officechai.com (os 10 melhores exemplos)
- huggingface.co (pipeline de render determinístico)
- daily.dev
- charliehills.substack.com (os 16 motions)
- youmind.com e jasonzhu.ai (bibliotecas de prompt)
- hyperframes.heygen.com (guia de prompt e catálogo do HyperFrames)
- www.remotion.dev (prompts de exemplo)
- ciyo.ai, apimaster.ai, pasqualepillitteri.it, explainx.ai (guias e análises de terceiros)
- gsap.com (documentação do MorphSVG)

**Não tentei abrir** x.com, threads.com, launchvideo.io e ai-tldr.dev; as menções a eles vêm do resumo da busca.

**Domínios a liberar, em ordem de utilidade:** `hyperframes.heygen.com`, `charliehills.substack.com`,
`huggingface.co`, `youmind.com`, `officechai.com`, `www.remotion.dev`, `gsap.com`, `jasonzhu.ai`, `daily.dev`
(e, se possível, `x.com`, onde está a maior parte dos exemplos originais).

### Outros links da busca (não abertos)

- Exemplos e cursos no X: https://x.com/EricBuess/status/2103226548413182366,
  https://x.com/notdwd/article/2104684539142648062, https://x.com/socialwithaayan/article/2104519430814482644,
  https://x.com/liu8in/status/2104360119849083093
- Coletâneas de prompt: https://www.revid.ai/claude-motion-graphics, https://www.iart.ai/blog/claude-motion-graphics,
  https://www.ayautomate.com/resources/claude-opus-5-5-motion-graphics, https://deepseekartifacts.com/prompts/opus-5-5-video
- Skills de vídeo de lançamento: https://github.com/timscheuerai/launch-video-kit,
  https://github.com/dheerajsarwaiya/launch-video
- Linha com MorphSVG: https://codepen.io/clementGir/pen/WNwGqLm
