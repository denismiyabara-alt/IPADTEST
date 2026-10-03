# motion: componentes de motion do Investir e Coçar

- `PROPOSTA.md`: as 5 melhorias de motion de maior impacto na retenção, em ordem de impacto ÷ esforço.
- `PESQUISA-EDICAO-CLAUDE.md`: pesquisa paralela (casos de fora). Não é mantida aqui.
- `grafico_cotacao/`: **protótipo da nº 1**, o gráfico de série que se desenha, em HyperFrames.

## Gráfico de cotação animado

Uma peça de B-roll de 5 a 10 s. A linha de uma série real se desenha, o número grande acompanha a ponta (é o valor
real da série naquele ponto), pousa no último valor com um som grave, e a fonte fica no canto. Aceita 16:9 (longo) e
9:16 (Short). O MP4 de exemplo está em `exemplos/render/`, e os quadros-chave, em `exemplos/frames/`.

```
grafico_cotacao/serie.py    dado real (BCB SGS ou B3 COTAHIST, do cache do site-ativos) → JSON de entrada
grafico_cotacao/gerar.py    JSON → projeto HyperFrames autocontido (index.html + assets/)
grafico_cotacao/quadro.mjs  abre o projeto num Chrome headless e lê o que está na tela num instante (usado no teste)
renderizar.sh               gerar + render, medindo o tempo
tests/test_grafico.py       35 testes
grafico_cotacao/especificacao.py  especificação simples do plano (serie, periodo, rotulo, comparador, aviso) → JSON, com a regra de compliance
exemplos/*.json             entradas de exemplo com dado real (Selic 16:9, PETR4 × CDI 16:9, PETR4 × Ibovespa 9:16)
```

### Instalar (uma vez)

```sh
cd motion
npm install                      # gsap, fontes OFL (@fontsource), hyperframes 0.8.78 (fixo, igual ao faz-a-conta)
npx hyperframes browser ensure   # Chrome headless do HyperFrames, se ainda não houver
python3 -m pip install pytest    # só para os testes
```

Nada vem de CDN na hora do render: o `gerar.py` copia as fontes, o GSAP e o efeito sonoro para `assets/` do projeto.

### Usar

```sh
# 1. dado → JSON (lê o cache do site-ativos: cache/dados.sqlite ou cache/raw/; sem cache, o BCB é baixado e guardado em motion/cache/)
python3 grafico_cotacao/serie.py bcb 432 --desde 2020-01-01 --destacar-extremos \
    --titulo "Selic: de 2% a 15%" --kicker "Meta da taxa Selic · Copom" -o exemplos/selic-16x9.json
python3 grafico_cotacao/serie.py b3 PETR4 --desde 2025-10-01 --formato 9:16 --comparador IBOV \
    --titulo "PETR4 × Ibovespa" -o exemplos/petr4-9x16.json
python3 grafico_cotacao/serie.py b3 PETR4 --desde 2025-10-01 --comparador CDI \
    --titulo "PETR4 contra o CDI" -o exemplos/petr4-cdi-16x9.json

# 2. JSON → MP4
./renderizar.sh exemplos/selic-16x9.json renders/selic.mp4

# ou por partes
python3 grafico_cotacao/gerar.py exemplos/selic-16x9.json -o projetos/selic
cd projetos/selic && npx hyperframes snapshot --at 3,5.2,7.9   # conferir quadros antes (barato)
npx hyperframes render -o ../../renders/selic.mp4
```

**Dado novo.** Qualquer série cabe, desde que o JSON tenha `titulo`, `fonte` (começando com "Fonte:") e
`serie: [{"data": "AAAA-MM-DD", "valor": número}, …]` em ordem. O resto tem padrão:

| campo | padrão | o que faz |
|---|---|---|
| `formato` | `"16:9"` | `"9:16"` para Short (1080×1920) |
| `duracao` | `8` | de 5 a 10 s; a linha pousa em 62% da duração |
| `linha` | `"linha"` | `"degrau"` para Selic (o valor vale até a próxima reunião) |
| `unidade` | `{"prefixo":"", "sufixo":"", "casas":2}` | `"R$ "`, `"%"`… formato brasileiro (1.234,56) |
| `variacao` | `null` | `"pct"` (+58,6% desde out/2025) ou `"pp"` (+9,25 p.p. desde jan/2020) |
| `cor_final` | `"vermelho"` | ou `"ouro"`. Os destaques são sempre ouro: no máximo 2 cores de destaque |
| `destaques` | `[]` | até 3 `{"data", "rotulo", "posicao": "acima"|"abaixo"}`; acendem quando a ponta passa |
| `som` | `false` | `{"pouso": "impact-bass-1"}` (biblioteca), um caminho de arquivo ou `"sintetico"` |
| `rotulo_final` | `"em 02/out/2026"` | texto sob o número final |

Entrada errada para antes de gerar, com a lista de todos os problemas (`gerar.validar`).

**Cuidados com o dado** (as regras do canal valem aqui):
- O COTAHIST traz o fechamento **sem ajuste** por proventos e desdobramento. O `serie.py` recusa a série se achar uma
  variação diária acima de 35% (provável evento societário); `--aceitar-saltos` só depois de conferir.
- A fala ganha da cartela em diferença de arredondamento (memória `feedback-direcao-cena-antes-do-fechamento`). Se o
  Denis falou "13,75%", o JSON tem que terminar em 13,75. E não use dado do dia gerado antes das 17 h como "fechamento".
- O `_origem` do JSON registra de que arquivo saiu o dado e quando o JSON foi gerado.

**Som.** O padrão é **um** som, só no pouso do número: a escolha do Denis no A/B do TRXF11 ("aparentemente o b ficou
melhor": só o número aterrissando, sem tique de contagem). O arquivo é o `impact-bass-1` da biblioteca `media-use`,
que vem dentro do pacote `hyperframes` (`node_modules/hyperframes/dist/skills/media-use/audio/assets/sfx/`), sob a
Pixabay Content License (uso comercial, sem exigência de atribuição; ver `CREDITS.md` lá). O `"sintetico"` (ffmpeg:
seno de 70 Hz com queda rápida e um clique) existe só como reserva sem rede: o Denis já reprovou SFX sintetizado
("ficou muito ruim").

### Testes

```sh
python3 -m pytest -q tests      # 35 testes, ~15 s
```

Eles conferem:
- a validação dos dados (13 casos de entrada errada);
- o formato brasileiro, a variação, a redução de pontos (o pico e o vale nunca somem), a escala e a inversa do easing;
- o dado real: a Selic do `serie.py` termina no último dado do SQLite do site-ativos, e o PETR4 lido do SQLite bate
  com o COTAHIST cru;
- **no navegador**: o projeto gerado abre sem erro de JS e sem requisição falhando, carrega as 5 fontes, e no último
  instante **o número na tela é igual ao último valor da série** (Selic 16:9 e PETR4 9:16). No meio, o número é um
  valor que existe na série.

Os testes de navegador são pulados se não houver `node_modules` ou Chrome headless.

### Tempo de render medido

Neste ambiente: Linux, 4 núcleos Xeon 2,8 GHz, sem GPU, HyperFrames 0.8.78 com workers automáticos (2), 30 fps:

| peça | duração | render | arquivo | pico de memória (Node + Chrome + ffmpeg) |
|---|---|---|---|---|
| Selic 16:9 | 8 s | 17,3 s (20 s com o `npx`) | 813 KB | ~2,1 GB |
| PETR4 9:16 | 8 s | 15,4 s | 907 KB | não medido |
| `snapshot` de 4 quadros | – | ~13 s | – | – |

No Mac de 16 GB, a estimativa é de 10 a 20 s por peça de 8 s (o molde Burry renderiza perto de 1:1 com 4 workers),
com ~2 GB. É um job pesado: não rode junto com transcrição ou voz. Para ir mais leve, use `--workers 1`: um Chrome a menos, render mais lento.

### Por que HyperFrames, e não Remotion

- As peças de B-roll do canal (o molde Burry, as receitas `investir-cocar-broll-dados` e `-materias` e o
  `gerar-cartelas.py`) já são HyperFrames, e foram aprovadas pelo Denis ("o melhor que já fiz até hoje", Prudential).
  O Faz a Conta comparou os dois, e o HyperFrames venceu.
- O padrão que funciona no canal é o de um **gerador Python que escreve o `index.html`** a partir de dados
  (`gen.py`, `build_hf.py`). O componente segue esse padrão: o JSON entra, a pasta do projeto sai, e um número novo
  é só rodar de novo.
- O `PathDraw` e o `IFIXMiniChart` (Remotion) moram só no Mac, em `~/Downloads/fiis-video/remotion`, fora de
  qualquer repositório. A técnica foi refeita aqui: revelação da linha por recorte (`clipPath`), com a ponta e o número
  calculados da própria série, o que vale para linha e para degrau. Ela segue as regras da memória
  `hyperframes-broll-timeline-travada`: sem `DrawSVGPlugin` (pago), sem animar a opacidade do `.clip`, fontes no
  subset `latin`.
- O render é determinístico (o HyperFrames posiciona a timeline do GSAP quadro a quadro), e o teste usa o mesmo
  mecanismo (`seek`) para ler o número na tela.

## Comparador e compliance (03/10)

- **Regra no código** (`especificacao.checar_compliance` e de novo em `gerar.validar`): ativo da B3 (`classe: "ativo"`,
  ação ou FII) só gera com um `comparador` (IBOV, IFIX ou CDI) desenhado junto **ou** com o `aviso` na tela
  ("Não é recomendação de investimento."). Selic, IPCA e CDI (`classe: "indicador"`) podem ir sozinhos.
  `serie.py b3 PETR4 …` sem `--comparador` nem `--aviso` é recusado.
- **2ª linha**: tracejada em cinza (`#6B675F`, não conta como cor de destaque), legenda no alto do gráfico e o valor na
  ponta depois do pouso ("CDI +14,5%"). Ativo com comparador vai em **base 100** na 1ª data; taxa com taxa
  (`comparador: "SGS:<n>"`) fica no mesmo eixo. O número grande continua o valor real da série.
- **Origem**: CDI = BCB SGS 12 acumulado; IBOV = BOVA11 no COTAHIST (o COTAHIST não traz o índice); IFIX = XFIX11 no
  COTAHIST, sem rendimentos. Dado faltando no período → erro claro, nunca extrapolação. A fonte de cada linha vai no
  rodapé ("Fonte: B3 (…) · CDI: BCB (SGS 12)").
- Quadro com comparador: `exemplos/frames/petr4-cdi-16x9-final.png` (render: `exemplos/render/petr4-cdi-16x9.mp4`).

## Integração na edição (feita em 03/10)

A peça `G` do molde Burry (`edicao-skill/molde-burry/broll/grafico.py`) chama este componente. A skill acha esta pasta
pela variável **`IEC_MOTION`** (padrão: `~/IPADTEST/motion`). Ver `edicao-skill/SKILL.md`, seção 2b.

## Notas da 1ª versão: integração planejada (a do molde Burry foi feita; ver acima)

1. **Copiar** `motion/grafico_cotacao/`, `package.json` e `tests/` para `investir-e-cocar/pipeline/motion/` (ou
   referenciar este repo) e rodar `npm install`.
2. **Peça "série" no plano.** No `scripts/plano.py`, um tipo novo `serie`, ancorado numa frase do roteiro como as
   outras peças. A duração sai da fala, com teto de 10 s, e o `duracao` do JSON recebe esse valor (5 a 10 s; abaixo
   de 5 s, não use gráfico). O `mapa.py` passa a enxergar a peça, e o `montar_final.py` corta e concatena o MP4 como
   faz com as cartelas, contando em frames inteiros (`-frames:v`).
3. **Dado conferido.** O JSON da peça entra no mesmo controle de números do roteiro (no Faz a Conta, o quadro
   "Números conferidos"): o último valor da série precisa estar `conferido` antes do render.
4. **Uma cena primeiro.** Renderizar um gráfico, mostrar ao Denis e só então propagar
   (`feedback_iterate_one_scene_first`).
5. **No Faz a Conta**, o mesmo `gerar.py` pode virar uma peça `serie()` no `cenas_hf.py`. O HTML gerado já usa a
   mesma versão (0.8.78) e o mesmo GSAP (3.14.2) do `build_hf.py`.
6. **Short.** O mesmo JSON com `"formato": "9:16"` gera o insert do Short que aponta para o longo (auditoria, ação 6).
