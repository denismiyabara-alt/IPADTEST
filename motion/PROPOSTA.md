# Motion no Investir e Coçar: as 5 melhorias que mais seguram o espectador

Data: 03/10/2026. Base: a auditoria do canal (`auditoria-canal/RELATORIO.md`), a pesquisa paralela
(`motion/PESQUISA-EDICAO-CLAUDE.md`, commits d5d4201 e 2421fae), o sistema de edição atual
(`investir-e-cocar/.claude/skills/edicao-investir-cocar` e `memory/`) e o pipeline do Faz a Conta
(`faz-a-conta/`, HyperFrames 0.8.78).

**O protótipo da nº 1 está pronto e testado:** `motion/grafico_cotacao/` (ver `motion/README.md`).
Render real: `exemplos/render/selic-16x9.mp4` (8 s, 813 KB) e `exemplos/render/petr4-9x16.mp4` (8 s, 907 KB).

## O diagnóstico que orienta a escolha

1. **A abertura não é o problema.** Aos 30 s, os 10 melhores vídeos do ano retêm 71,3% e os 10 mais fracos, 73,7%
   (auditoria, H4). Gastar motion no gancho não muda nada que os dados mostrem.
2. **O vídeo perde gente no miolo.** A % média assistida é de 36,9% no top e 41,0% nos fracos. Em vídeos de 15 a 20 min
   (a duração que mais converte, mediana de 31,5 inscritos), mais da metade do vídeo passa sem ninguém assistindo.
   O motion que importa é o que entra no meio.
3. **O miolo é, na maior parte, câmera pura.** No TRXF11, a cobertura de imagem foi de 41%; cerca de 59% do vídeo é o
   Denis falando, sem nada na tela (pesquisa, recomendação 1). A regra dos 28 s (zoom, palavra, gráfico ou corte a cada
   ~28 s de câmera) existe, mas é aplicada à mão no CapCut.
4. **Os temas que convertem são temas de série no tempo.** Renda mensal (14,5 inscritos por mil views intencionais),
   Tesouro/IPCA+ (11,0 por mil, mediana de 142 inscritos por vídeo) e alerta macro (37% do top). Um dos 3 maiores do ano
   tem o gráfico no título: "Esse Gráfico Acertou as CRISES 1929, 2008 e 2020…" (357 inscritos).
5. **O que separa top de fraco é distribuição** (auditoria, ação 10). Uma peça de motion que também vira Short,
   imagem de thumbnail ou post da comunidade trabalha nas duas frentes.
6. **Os Shorts continuam no plano.** Trouxeram cerca de 40,8% dos inscritos de abr/25 a ago/26, e a auditoria recomenda
   voltar a 8 por mês, cada um apontando para um longo (H5 e ação 6). O longo é a prioridade, mas pelo menos uma melhoria
   precisa servir ao 9:16.

### O que já existe e por isso não entra na lista

- **Número que conta até o valor:** já existe (count-up das cartelas de dados, `NumberRoller` no Remotion, `roller()` no molde Burry).
- **Manchete com push-in e marca-texto:** já existe (peça "prints": fonte primária com push-in calculado e sublinhado desenhado).
- A regra do pato, as 3 peças de B-roll ancoradas em frase, o molde Burry e a motion library em Remotion também ficam
  como estão. A lista abaixo só fecha buracos.

## As 5, em ordem de impacto ÷ esforço

| # | melhoria | impacto na retenção | esforço | render no Mac (por 10 s) | onde encaixa |
|---|---|---|---|---|---|
| 1 | **Gráfico de série que se desenha** (4ª peça de B-roll), com dado da B3 ou do BCB | alto | médio, já feito; integrar leva ~½ dia | ~10–20 s, ~2 GB | HyperFrames, ao lado de `gerar-cartelas.py` |
| 2 | **Zoom por ênfase automático** nos trechos de câmera pura (16:9 e 9:16) | alto | baixo a médio (~1 dia) | ~3–6 s, <0,5 GB (só ffmpeg) | `zoom.py` antes do `montar_final.py` |
| 3 | **Legenda palavra por palavra nos Shorts** (9:16) | alto nos Shorts; não vale no longo | baixo (~½ dia) | ~1–2 s com ASS no ffmpeg | etapa de Shorts, a partir do JSON do mlx_whisper |
| 4 | **Comparador em base 100** (Tesouro IPCA+ × CDI × IPCA × Ibovespa) | médio a alto nos temas de renda | baixo depois da nº 1 (~1 dia) | igual à nº 1 | modo novo do mesmo componente |
| 5 | **Eventos sobre o gráfico** (Copom, crises, datas-com) | médio | baixo depois da nº 1 (~½ dia) | igual à nº 1 | campo novo no JSON da nº 1 |

Os tempos do Mac são estimativas. Neste ambiente (Linux, 4 núcleos Xeon, sem GPU), o render da nº 1 foi **medido**:
8 s de vídeo em **17,3 s** (16:9) e **15,4 s** (9:16), com 2 workers, e o pico de memória do processo inteiro
(Node, Chrome e ffmpeg) ficou em **~2,1 GB**. No Mac, o molde Burry renderiza perto de 1:1 com 4 workers
(memória `hyperframes-broll-timeline-travada`: 60 s em 54 s), por isso a estimativa de 10 a 20 s por 10 s.
Todos respeitam a regra de um job pesado por vez.

---

## 1. Gráfico de série que se desenha (a nº 1, com protótipo)

**O que é.** Uma peça de B-roll de 5 a 10 s, em tela cheia: a linha de uma série real (Selic, cotação, IPCA) se
desenha da esquerda para a direita. O número grande, em cima, acompanha a ponta da linha e mostra **o valor real da
série naquele ponto**, não uma contagem inventada. No último ponto, o número "pousa": ganha a cor de destaque, dá um
pulso curto e toca um único som grave (o `impact-bass-1`). Depois entra a variação ("+9,25 p.p. desde jan/2020").
A mínima, a máxima ou outra data marcada acendem quando a ponta passa por elas. No canto, "Fonte: BCB (SGS 432)" ou
"Fonte: B3 (COTAHIST…)", como manda a regra do canal.

**Por que retém.**
- Ataca o miolo (diagnóstico 2 e 3): é uma peça para os trechos em que o Denis explica um número que **mudou no tempo**,
  que hoje viram câmera pura ou uma cartela com um número só.
- Combina com os temas que mais convertem (diagnóstico 4): Selic e IPCA+ para o Tesouro, cotação e dividendo para a
  renda mensal, série histórica para o alerta macro.
- Cria uma pergunta e a responde na tela: a linha sobe, o espectador quer ver onde ela para, e o número para em
  4 a 6 s. É o mesmo mecanismo do count-up que o Denis já aprovou, só que com 6 anos de história dentro.
- Segue o gosto registrado: "manchetes REAIS preferíveis a tela preta com número gigante" (stack de vídeo, mai/2026) e
  "muito melhor que texto subindo" (motion library). O dado é real e a fonte está na tela.
- Serve à distribuição (diagnóstico 5): o mesmo JSON gera a versão 9:16 para o Short que aponta para o longo, e o
  último quadro serve de imagem para a thumbnail ou o post da comunidade.

**Exemplo visual (render real).** `exemplos/frames/selic-16x9-quadros.jpg` traz 4 quadros do MP4:
- 1,0 s: título "Selic: de 2% a 15%", kicker "META DA TAXA SELIC · COPOM" em mono, grade com 0%, 5%, 10% e 15% e os anos,
  a ponta parada em 4,50%;
- 3,0 s: a linha em degrau já passou pela "Mínima: 2,00%" (em ouro) e o número no alto marca 13,25%;
- 5,1 s: pousou. "13,75%" em vermelho, o anel se abrindo no último ponto, a "Máxima: 15,00%" acesa;
- 7,9 s: "em 02/out/2026" e o selo "+9,25 p.p. desde jan/2020".

Versão 9:16: `exemplos/frames/petr4-9x16-final.jpg` (PETR4 em 12 meses, "R$ 49,77", "+58,6% desde out/2025").

**Esforço.** O protótipo está feito: gerador, fonte de dados, teste e render. Para entrar no pipeline, falta ~½ dia:
um tipo `serie` no `plano.py` e no `mapa.py` (a duração sai da fala, com teto de 10 s) e uma rodada com o Denis
numa cena só antes de propagar (regra `feedback_iterate_one_scene_first`).

**Custo de render.** Medido aqui: 17,3 s para 8 s em 16:9 (cerca de 22 s por 10 s), pico de ~2,1 GB.
Estimado no Mac: 10 a 20 s por 10 s, ~2 GB. Um vídeo com 6 gráficos de 8 s custa cerca de 2 min de render.

**Como encaixa.** Em **HyperFrames**, como as outras peças de B-roll. Justificativa da escolha no `README.md`.
Resumindo: as peças de B-roll do canal e o Faz a Conta já renderizam em HyperFrames; o Remotion ficou nos projetos de
motion mais antigos (fiis-video, Barsi, RARA11). O `PathDraw` e o `IFIXMiniChart` do Remotion moram só no Mac
(`~/Downloads/fiis-video/remotion/src/components/`), e por isso a técnica foi refeita em HyperFrames com os tokens do
molde Burry (papel `#F4F1EA`, Anton, Inter e JetBrains Mono, vermelho `#C8261D`, ouro `#966B00`). Olhei o bloco
`data-chart` do catálogo do HyperFrames: é um gráfico genérico de barras e linha. Não posiciona por data, não tem
degrau e não traz o número que acompanha a ponta nem a fonte obrigatória, então não serve como base.

**Por que esta é a nº 1, e não o zoom por ênfase** (que a pesquisa pôs em primeiro):
- O zoom **automatiza uma regra que já existe**: o Denis já faz zoom à mão no CapCut, a cada ~28 s de câmera. O ganho é
  de tempo de edição e de constância, e a parte de retenção já existe onde o zoom manual foi feito.
- O gráfico **coloca na tela uma informação que hoje não existe**: o caminho do número no tempo. Hoje as cartelas
  mostram um número por cena.
- O gráfico é o único dos cinco que trabalha também na distribuição: Short 9:16, imagem de thumbnail e post, com o
  mesmo JSON (diagnóstico 5).
- O risco de rejeição é baixo: estilo, fontes, cores e som saem do molde que o Denis já aprovou, e o som é a única
  escolha dele ("só número aterrissando", feedback `sfx-sintetizado-soa-barato`).
- A nº 2 vem logo atrás e é barata. As duas juntas atacam os 59% de câmera pura por dois lados: a nº 1 onde há dado,
  a nº 2 onde só há fala.

---

## 2. Zoom por ênfase automático nos trechos de câmera pura (longo e Short)

**O que é.** Um `zoom.py` lê o `cartelas.json` (onde já há imagem) e o JSON por palavra do `mlx_whisper`. Em cada
trecho de câmera pura com mais de ~8 s, o Claude escolhe 1 ou 2 palavras de ênfase (o número, o "mas", o punch).
Nelas entra um push-in de 1,1 a 1,25×, que começa suave na palavra e sai no fim da frase. É a recomendação 1 da
pesquisa (casos 7 e 8). No **Short 9:16**, o mesmo script trabalha sobre o recorte vertical do rosto: o crop por rosto
do claude-shorts (pesquisa, caso 7) e o push-in na palavra.

**Por que retém.** Quebra a monotonia de enquadramento no miolo (diagnóstico 2 e 3) sem tirar o rosto do Denis, que é o
que segura o fraco "que segura quem chega" (auditoria, seção 2). Torna a regra dos 28 s automática e constante, em vez
de depender do tempo que sobra no CapCut.

**Exemplo visual.** Câmera pura, 1920×1080, o Denis no terço esquerdo. Na palavra "quinze" de "a Selic chegou a quinze
por cento", o quadro vai de 1,00× para 1,18× em 0,4 s, centrado no rosto, e volta a 1,00× no silêncio do fim da frase.
Nada de texto e nada de som.

**Esforço.** Baixo a médio, ~1 dia. A transcrição por palavra, o `cartelas.json` e a contabilidade em frames inteiros
já existem. Falta o script e a escolha das palavras (prompt mais lista de exceções).

**Custo de render.** Só ffmpeg (`crop` + `scale` com expressão no tempo), sem Chrome. Re-encoda só as janelas com zoom
(2 a 4 s cada) com `-frames:v` exato e junta com `concat -c copy`, como o `montar_final.py` já faz. Estimativa no Mac:
3 a 6 s por 10 s de trecho com zoom, com menos de 0,5 GB. O vídeo inteiro não é re-encodado.

**Como encaixa.** Nem Remotion nem HyperFrames: é uma etapa de ffmpeg entre o corte auditado e o `montar_final.py`, com
os mesmos `assert` de frames por peça. Ponto de atenção: zoom sobre 1080p perde nitidez acima de ~1,25× (por isso o
teto). Se a gravação for 4K, dá para ir mais longe sem perda.

---

## 3. Legenda palavra por palavra nos Shorts (9:16)

**O que é.** Uma legenda de 2 a 4 palavras por vez, grande, no terço de cima do Short, com a palavra falada em destaque
(o número em vermelho). Sai do mesmo JSON por palavra do `mlx_whisper`. É a recomendação "template-tiktok" da pesquisa
(caso 3): alto nos Shorts e incerto no longo.

**Por que retém.** O Short é visto com som desligado com frequência e é achado por busca (em 2026, 74% a 92% das views
de Shorts vieram da Pesquisa; auditoria, seção 5). Os Shorts já têm 82% de média assistida: a legenda protege essa
média nos Shorts novos, que devem voltar a 8 por mês (ação 6). **No longo, não:** o estilo aprovado é "sem
legendas/karaokê" (memória `remotion-audio-video-process`), e o longo fica só com a palavra-chave isolada dentro do
zoom da nº 2.

**Exemplo visual.** 1080×1920, o Denis recortado no centro. Em y ≈ 560, "A SELIC CAIU PRA" em Inter 900, 96 px, branco
com contorno escuro. Na palavra seguinte, "13,75%" entra sozinho em Anton vermelho, 150 px, com pop de 0,15 s.

**Esforço.** Baixo, ~½ dia: paginação do JSON por palavra em blocos de até 4 palavras ou ~1,2 s, mais o estilo.

**Custo de render.** O caminho barato é gerar um `.ass` e queimar com o `ffmpeg-full` (que tem libass; memória
`ffmpeg-brew-sem-libass-usar-ffmpeg-full`): ~1 a 2 s por 10 s no Mac, menos de 0,5 GB. Se o Denis quiser animação mais
rica, os componentes `caption-*` do catálogo HyperFrames fazem isso como overlay WebM transparente, a ~1,5 a 2 s por
segundo de vídeo, com ~2 GB.

**Como encaixa.** Etapa nova no fluxo de Shorts: corte do Short, depois a legenda (ffmpeg/ASS), depois o card para o longo.
O gráfico da nº 1 em 9:16 entra no mesmo Short como insert.

---

## 4. Comparador em base 100 ("quem rendeu mais")

**O que é.** Um modo do componente da nº 1 com 2 a 4 linhas normalizadas em 100 na data inicial: Tesouro IPCA+, CDI,
IPCA e Ibovespa, por exemplo. As linhas se desenham juntas, e na ponta de cada uma aparece o valor final
("R$ 100 viraram R$ 187"). A vencedora fica na cor de destaque e as outras em cinza, para manter o limite de 2 cores.

**Por que retém.** É o formato natural das duas linhas que mais convertem: renda mensal e Tesouro/IPCA+ (diagnóstico 4).
A pergunta "qual rendeu mais?" fica aberta até o fim do desenho.

**Exemplo visual.** 16:9, título "R$ 100 em jan/2020", quatro linhas finas em cinza. Ao fim, uma linha engrossa em
vermelho, com "R$ 187" na ponta. "Fonte: BCB (SGS 12 e 433), B3".

**Esforço.** Baixo depois da nº 1, ~1 dia: o `serie.py` já lê o CDI (SGS 12) e o IPCA (433) do cache do site-ativos.
Falta o eixo comum, os rótulos de ponta sem colisão e a série do Tesouro (preço e taxa do Tesouro Transparente).

**Custo de render.** Igual à nº 1 (o SVG é leve; 4 linhas não mudam o custo de forma perceptível).

**Como encaixa.** HyperFrames, no mesmo `gerar.py`, com `"series": [...]` no lugar de `"serie"`.

---

## 5. Eventos sobre o gráfico (linha do tempo dentro da série)

**O que é.** Datas marcadas na série que acendem quando a ponta passa por elas: "Copom sobe para 15%", "pandemia",
"data-com". Opcionalmente, uma faixa sombreada de período ("governo X", "crise de 2008"), sempre factual e com fonte.

**Por que retém.** Liga o número à história que o Denis está contando. É o formato do "Esse Gráfico Acertou as CRISES"
(top 3 do ano) e do alerta macro, que é 37% do top. O espectador ganha um marco a cada 1 a 2 s enquanto a linha corre.

**Exemplo visual.** O gráfico da Selic da nº 1, com 3 marcos em ouro: "mar/2021: começa a alta", "jun/2025: 15%" e
"set/2026: 1º corte". Cada um acende com um pop de 0,4 s na passagem da ponta.

**Esforço.** Baixo, ~½ dia: os `destaques` da nº 1 já fazem isso (até 3, posicionados pela inversa da curva de easing
para acender no instante certo). Falta a faixa de período e a checagem de colisão de rótulos.

**Custo de render.** Igual à nº 1.

**Como encaixa.** HyperFrames, campo `eventos` (ou os `destaques` atuais) no JSON da nº 1.

---

## Transversal: revisor visual com contexto limpo

Não é motion na tela, mas protege as cinco: antes do render cheio, `npx hyperframes snapshot --at …` gera a folha de
quadros, e um agente que **não** escreveu a cena a revisa (pesquisa, recomendação 3). A regra é a mesma do título:
quem escreveu não aprova. Ela evita repetir as três rodadas de "ficou amador" de mai/2026, de ~30 min de render cada.
O protótipo já foi conferido assim: quadros do snapshot, e depois quadros extraídos do MP4 final.

## Como medir se funcionou

A auditoria já baixa a curva de retenção por vídeo (`audienceWatchRatio` por `elapsedVideoTimeRatio`). Para os 4 a 6
próximos longos com a nº 1 e a nº 2, compare a inclinação da curva nos 30 s depois de cada inserção com os trechos de
câmera pura do mesmo vídeo, e a % média assistida com a mediana dos últimos 12 meses (36,9% no top e 41,0% nos fracos).
São amostras pequenas: leia como pista, como a própria auditoria faz.
