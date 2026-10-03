---
name: edicao-investir-cocar
description: Edita um vídeo longo do canal Investir e Coçar do bruto até o master — corte pela regra do pato, auditoria até zerar, peças de B-roll (dados, prints de fonte primária, frases) com duração derivada da fala, e montagem final. Use quando Denis mandar "vamos cortar o vídeo do X", "faz a edição", "monta o B-roll", "junta tudo" ou entregar um .MOV de gravação de teleprompter.
---

# Edição — Investir e Coçar

> **PADRÃO ATUAL (29/09/2026): molde Burry/TRXF11 em `molde-burry/`** — leia `molde-burry/README.md` primeiro.
> Denis aprovou: pessoa do vídeo entrando na cena (recorte), MUITOS prints de fonte real (35+; "quanto mais melhor"),
> cartelas animadas com som, ~50% de cobertura. Scripts prontos (corte pela onda, prints, gerar, plano, mapa, montar, sfx)
> e exemplos completos (cenas/pecas/prints.json) do Burry e do TRXF11 cota nova. As seções abaixo são o porquê de cada etapa.
> **4ª peça (03/10/2026): gráfico de série** (`G`), ancorado em frase, com regra de compliance no código: seção 2b.

Pipeline validado no vídeo do TRXF11 (ago/2026): 25min48 de bruto → 22min24 com 55 cartelas
e 41% de cobertura de imagem. Cada etapa aqui existe porque a versão ingênua dela falhou.

## 0. Antes de tudo

- `ffmpeg` moderno: a flag é **`-/filter_complex arquivo.txt`**. `-filter_complex_script` foi removida.
- **`timeout` não existe no macOS.** Comando com `timeout` falha em silêncio e parece bloqueio do site.
- Chrome headless precisa de **`--user-data-dir` próprio** se o Chrome normal estiver aberto, e de
  **`--user-agent` de navegador real** (Investidor10 e portais bloqueiam o UA headless).
- Rodar **uma coisa pesada por vez**. O número antigo aqui ("Whisper carrega 1,5GB") estava
  errado por 8x e fazia planejar mal: medido em 30/ago/2026, `mlx_whisper` com
  `large-v3` + `--word-timestamps True` num áudio de **44 min** chegou a **12 GB**.
  **Por isso o modelo aqui é o `large-v3-turbo`**: no mesmo áudio de 49 min ele mede
  **1,9 GB de pico e 5,5 min** (contra 12 GB e 9 min), com 99,31% de similaridade de texto
  e 0,12 s de deriva de timestamp. Medido, não estimado. Não voltar pro `large-v3` sem
  refazer essa medição.
  Somado a um `synth_qwen_clone.py` de 4 GB, deu 16 GB numa máquina de 16 GB — travamento
  total e 6 eventos de jetsam. Antes de disparar lote de transcrição, conferir:
  ```bash
  top -l 1 -o mem -n 5 -stats pid,command,mem,cmprs   # nada pesado rodando junto?
  ```
  ⚠️ Job lançado pela ferramenta Bash de uma sessão Claude Code aparece no Activity Monitor
  **somado dentro do `Claude.app`** (é descendente dele). "Claude com 23 GB" pode ser 16 GB
  da sua própria transcrição — forçar o encerramento do Claude mata o lote junto. Conferir a
  árvore com `ps -o ppid=` antes de matar qualquer coisa.
  Pra aliviar sem perder trabalho: `kill -STOP <pid>` congela, `kill -CONT <pid>` retoma.

## 1. Corte (regra do pato)

Marcadores: "pato/pata amarelo/vermelho" — ver `[[marcadores-gravacao-pato]]` no vault.

```bash
ffmpeg -v error -y -i BRUTO.MOV -ac 1 -ar 16000 master.wav
mlx_whisper master.wav --model mlx-community/whisper-large-v3-turbo --language pt \
  --condition-on-previous-text False --word-timestamps True --output-format json --output-name master
python3 scripts/timeline.py master.json > timeline.txt
python3 scripts/repetidos.py master.json      # take repetido sem marcador
```

`timeline.py` marca três coisas: `PATO` (regex pela **cor**, não pela palavra — o Whisper escreve
"fato vermelho", "do lado vermelho"), `GAP-PAL` (vazio escondido **dentro** de uma palavra esticada)
e `ENGOLIDO?` (segmento longo com poucas palavras).

**Delimitar cada corte por `silencedetect` numa janela de 3s, nunca pelos timestamps da transcrição** —
o Whisper transcreve o mesmo trecho diferente a cada passada. Gate: **-30dB** (o -35dB não pega nada
em gravação com piso de ruído alto) e `-v info`, porque `-v error` suprime a saída do filtro.

Escrever `cuts.py` (lista `(ini, fim, motivo)`) → gera `filter.txt` → renderizar **sempre do master**.

**Corte pela onda (19/09, substitui o gate -30dB):** limiar Otsu no envelope, borda no meio da maior pausa,
`ilhas.py` (pato por ilha de fala), `auditar.py` (pausa > 0,5 s + transcrição de cada emenda), `vazios.py`.
Molde: `~/Downloads/MORGAN STANLEY/cuts.py`. Ver `[[feedback-corte-pela-onda-otsu-e-emendas]]`.

**Auditoria obrigatória, em loop**: transcrever o *render*, procurar `\bp[ai]t[oa]s?\b|\b(vermelh|amarel)[oa]s?\b`,
corrigir, renderizar de novo. Três rodadas foi o normal no BBAS3 e no TRXF11. Fecho: `silencedetect -30dB:d=1.2`
no render não pode achar nada.

## 1b. Corte com remendo (dois brutos)

Molde validado no "Dividendos 10 anos" (set/2026): `~/Downloads/dividendos-10-anos/cuts.py`
(trecho = `(fonte, ini, fim)`, pickup entra por rótulo depois do corte do parágrafo velho) e
`corte_frames.py`. **Não renderize o corte por `trim`+`concat`**: o iPhone grava VFR (29,99 fps
com frame dropado) e 37 trechos deram +6 frames e +200 ms de deriva. Vídeo trecho a trecho com
`-ss a -frames:v N` + assert, áudio numa passada só (`atrim` de `a` a `a+N/30`), mux por cópia.
Aparar vazio pelo **intervalo entre palavras** do Whisper, não pela grade de silêncio (ruído
quebra o silêncio e sobra respiração). Borda sem silêncio: `envelope.py` acha o vale e a
transcrição do trecho *até o vale* diz de que lado a palavra caiu. `checa_sync.py` com um
ponto no meio de cada pickup. Ver `[[feedback_corte_com_pickups_duas_fontes]]`.

## 2. Peças de B-roll (três, sempre; a 4ª, o gráfico, quando um número mudou no tempo)

| Peça | O que é | Gerador |
|---|---|---|
| **dados** | 1 número por cena, tipografia extrema, count-up | `scripts/gerar-cartelas.py` |
| **prints** | fonte primária real com push-in e sublinhado desenhado no trecho citado | `scripts/gerar-prints.py` |
| **frases** | as frases-âncora do roteiro em tipografia | `scripts/gerar-cartelas.py` |
| **grafico** | série real (Selic, IPCA, cotação) que se desenha; o número acompanha a ponta e pousa no último valor | `molde-burry/broll/grafico.py` → `$IEC_MOTION/grafico_cotacao` |

### 2b. Gráfico de série (4ª peça, peça `G`, aprovado pelo Denis em 03/10/2026)

Ancorado em FRASE como as outras: uma linha em `pecas.py` com a peça `"G"`, e a especificação em
`videos/broll/cenas.py` com o tipo `"grafico"`:

```python
# pecas.py
("54-selic", "G", r"corrigidas pelo cdi", 0.0),
# videos/broll/cenas.py
"54-selic": ("grafico", dict(serie="SGS:432", periodo="2020-01-01:", rotulo="Selic: de 2% a 15%",
                             kicker="O CDI anda colado na Selic", destaques="extremos")),
```

| campo | valores |
|---|---|
| `serie` | `"SGS:<n>"` (BCB: 432 Selic, 433 IPCA, 13522 IPCA 12 meses, 12 CDI) ou `"COTAHIST:<TICKER>"` (B3) |
| `periodo` | `"2020-01-01:"`, `"2025-10-01:2026-10-01"`, `"12m"` ou `"5a"` |
| `rotulo` | o título na tela |
| `unidade` | opcional: `"%"`, `"R$"` ou `"pontos"` (o padrão sai da fonte) |
| `comparador` | opcional: `"IBOV"`, `"IFIX"`, `"CDI"` ou `"SGS:<n>"` (2ª linha, tracejada em cinza, com legenda) |
| `aviso` | opcional: `True` escreve "Não é recomendação de investimento." na tela |
| `formato` | opcional: `"16:9"` (padrão) ou `"9:16"` (Short) |
| `kicker`, `destaques`, `cor_final` | opcionais (`destaques="extremos"` marca a mínima e a máxima) |

**Duração:** sai da fala, como nas outras peças, mas com mínimo de 5 s e teto de 10 s (`LIMITES["G"]` no
`plano.py`). O número pousa em 62% da duração. Se a próxima peça entra antes de 5 s, o `plano.py` para com
erro; se o `mapa.py` precisar aparar o gráfico para antes do pouso, também para.

**Compliance (no código, não é só regra escrita):** ação ou FII (`COTAHIST:`) **exige** um `comparador`
(IBOV, IFIX ou CDI) desenhado junto **ou** `aviso=True`. Sem nenhum dos dois, o `grafico.py` recusa o plano
inteiro com erro e não gera nada. Séries do BCB (Selic, IPCA, CDI) podem ir sozinhas. A mesma regra é
conferida de novo no `gerar.validar()` do componente, para um JSON escrito à mão não passar por fora.

**De onde vem cada comparador** (faltou dado no período → erro; nada é extrapolado):
- `CDI`: BCB SGS 12, acumulado dia a dia desde a 1ª data do gráfico.
- `IBOV`: BOVA11 no COTAHIST (o COTAHIST não traz o índice; o ETF segue o Ibovespa menos 0,10% a.a.).
- `IFIX`: XFIX11 no COTAHIST, preço sem os rendimentos distribuídos (subestima o retorno total).
- `SGS:<n>`: outra taxa do BCB no mesmo eixo (por exemplo, Selic × IPCA 12 meses).
Ativo com comparador é desenhado em **base 100** na 1ª data, porque as unidades são diferentes; taxa com taxa
fica no mesmo eixo. O número grande continua sendo o valor real (R$ 49,77), não o da base 100.

**Dado:** o cache do site-ativos (`IPADTEST/site-ativos/cache/`: SQLite e COTAHIST cru). Sem ele, o BCB é
baixado e guardado em `$IEC_MOTION/cache/`. O COTAHIST é o fechamento **sem ajuste** por proventos; um salto
diário acima de 35% (desdobramento) recusa a série. A fala ganha da cartela em diferença de arredondamento.

**Comandos** (depois do `plano.py`; a variável aponta para a pasta `motion/` do repo IPADTEST):
```bash
export IEC_MOTION=~/IPADTEST/motion          # onde você clonou o IPADTEST; 1ª vez: (cd $IEC_MOTION && npm install)
cd videos/broll && python3 gerar.py && python3 grafico.py --render && cd ../..
python3 mapa.py && python3 montar.py && python3 sfx.py
```
O som do pouso não vai no mp4 do gráfico: entra como evento `impacto` (impact-bass-1) no `sfx.py`, junto com
os outros sons, e o Denis escolheu o esparso (só o número aterrissando).

**Custo de render:** cada gráfico é um render HyperFrames próprio, de 5 a 10 s. Medido no Linux (4 núcleos,
sem GPU): 15 a 17 s por gráfico de 8 s, com ~2 GB de pico. No Mac, a estimativa é de 10 a 20 s por gráfico.
É um job pesado: rode sem transcrição ou voz ao mesmo tempo. Teste: `IEC_MOTION=... python3 -m pytest -q
molde-burry/tests` (plano → gráfico → mapa → montar num corte sintético, mais as regras de compliance).

Estilo congelado: papel `#F4F1EA`, Anton + Inter + JetBrains Mono, ícone stroke-only que se desenha
atrás do número. Receitas em `~/.media/recipes/investir-cocar-broll-*`.

**Prints**: sempre documento primário (fato relevante, nota técnica, comunicado, post do gestor),
nunca a matéria que cita o documento. PDF → PNG com `pdftoppm -r 130`; a posição do trecho citado sai
de `pdftotext -bbox-layout` (coordenadas em pontos, dividir pelo tamanho da página). Se o nome está
dentro de logotipo, o texto não sai no `pdftotext` — **renderizar a página como imagem e conferir com o olho**
(foi assim que se pegou a ocupação dos shoppings trocada de nome).

O zoom de cada print é **calculado** pra linha citada ocupar ~92% da janela, não chutado.

## 3. Duração de cada cartela = duração da fala

O erro mais caro do TRXF11: durações fixas de 5-7s. A cartela sai enquanto o Denis ainda está falando
do assunto — aconteceu em **52 das 53**. A duração sai da transcrição: da entrada até o fim do último
segmento sobre aquele assunto, teto de 11s. Isso leva a cobertura de ~10% para ~40%.

Regra de ouro: **conferir a saída da imagem, não só a entrada.**

## 4. Mapa de inserção

`scripts/plano.py` ancora cada peça numa **frase do roteiro**, não num timecode: acha a frase na
transcrição do corte, deriva a duração da fala e, quando a fala é mais longa que o teto, empurra a
*entrada* pra peça sair junto com ela (itera até convergir). Saída: `plano.json`.
Recortou o master de novo? Roda de novo e as 55 peças se reposicionam sozinhas — escrever
timecode à mão quebrou duas vezes.

`scripts/mapa.py` calcula a janela de cada cartela dentro da peça a partir dos geradores e apara quem
encostar na seguinte. Nunca escrever o mapa à mão — mudou uma duração, o mapa se ajusta sozinho.
Saída: `cartelas.json`.

## 5. Montagem

`scripts/montar_final.py`: corta o FINAL e as peças em pedaços e junta com `concat -c copy`.

**Não use overlay encadeado.** 24 overlays deram **0,087× (4 horas de render)** porque cada `trim`
redecodifica o input inteiro. Cortar e concatenar faz uma passada só.

Áudio: **`-c:a copy`**. Reencodar gera segunda geração de AAC — o hash denuncia.

⚠️ **Contabilidade em frames inteiros, nunca em segundos.** Cortar com `-ss X -to Y` e avançar
o cursor pelo valor *pedido* acumula meio frame por peça: 53 peças deram **+0,84s de deriva
monotônica** — o áudio soa adiantado do meio pro fim. Aconteceu em dois vídeos seguidos e
passou batido porque a conferência só olhava a duração total. `-frames:v N` trava a duração
de cada peça, e um `assert` por peça mais um no total fecham a conta.
Ver `[[feedback_montagem_deriva_frame_meio_a_meio]]`.

## 6. Conferência final (as três)

```bash
# áudio: tem que bater com o do corte auditado
for f in FINAL-corte.mp4 VIDEO-FINAL.mp4; do
  ffmpeg -v error -i "$f" -map 0:a -f s16le -ar 16000 -ac 1 - 2>/dev/null | shasum; done
# sincronia: duração das duas streams < 1 frame de diferença
ffprobe -v error -select_streams v -show_entries stream=nb_frames,duration -of default=nw=1 VIDEO-FINAL.mp4
# imagem: amostrar frames nos pontos de inserção e olhar o contact sheet
```

## 7. O que fica de fora

Título e thumbnail **não** são desta skill — usar o agente `empacotador-yt`, e nunca deixar quem
escreveu o roteiro escolher o próprio título. Memes e corte fino de respiração o Denis faz no CapCut
por cima do master achatado.

## 7b. Ritmo das cartelas (Denis, 11/09/2026)

- **Duração = a frase que carrega o número**, teto 6 s (`plano.py`: fim do segmento da âncora).
  Antes era "até o fim do assunto", teto 11 s: média de 10,5 s e o Denis reclamou "fica tempo
  demais". A mesma cartela **pode voltar** quando ele retoma o número: id `xx@2` em `pecas.py`.
- **Corte seco, sem fade.** O fade pra papel vazio dava "pisque" na saída. `OVER=0`, `APARA=0`,
  e toda animação de entrada começa em 0–0,1 s (grid: `0.12 + i*PASSO`), senão o primeiro frame
  é papel em branco.
- **"Fala, Tanaka" atrás do Denis na abertura**: `abertura/` — `hyperframes remove-background`
  (CoreML, 72 frames em 11 s) + texto Anton em PNG + `overlay` do fg por cima. Entra como peça
  `C` em `cartelas.json`, 0:00–0:02,4, e a 1ª cartela cola em 0:02,4. Nada entre 0:08 e 0:20.

## 8. Faxina (rodar assim que o passo 6 passar)

**Apagar DURANTE, não só no fim** (Denis, 11/09): `corte_frames.py` apaga `pecas/` depois do
mux, `montar.py` apaga `montagem/` depois do concat. `FINAL-corte.mp4` fica até o Denis aprovar
o final — sem ele, qualquer remontagem custa 5 min de re-corte.

O TRXF11 deixou **11 GB de intermediário** pra entregar 1,8 GB. O `patrimonio-presidenciaveis`
guardou `MESCLA-FINAL-v5/v6/v7` e `MASTER-corte-v3/v4` — 3,7 GB de versões superadas, e o v7
ainda duplicado em `.mkv` e `.mp4`. Ninguém volta nesses arquivos. Apague no fim da edição,
não "depois".

**Fica** (nessa ordem de importância):
- o `.MOV` bruto do teleprompter — é o único insubstituível
- `VIDEO-FINAL.mp4` — o master que vai pro CapCut
- `montagem/base-*.mp4` — as peças de B-roll, se quiser remontar sem re-renderizar
- `cartelas.json`, `master.wav` — baratos e reconstroem o mapa

**Sai**, assim que os dois hashes do passo 6 baterem:
- `FINAL-corte.mp4` — existe só pra ser o lado esquerdo daquela comparação
- `montagem/video-mudo.mp4` — montagem intermediária
- qualquer `RENDER-*.mp4` / `*-v[0-9]*.mp4` que não seja a última versão
- `.mkv` quando já existe o `.mp4` do mesmo corte
- `.wav` de render intermediário (`render03.wav` e afins) — o `master.wav` basta

⚠️ Antes de apagar duplicata de container, **compare stream a stream**, não o tamanho:
```bash
for f in X.mp4 X.mkv; do
  ffmpeg -v error -i "$f" -map 0:a:0 -f s16le -ar 16000 -ac 1 - 2>/dev/null | shasum
  ffmpeg -v error -i "$f" -map 0:v:0 -f rawvideo -t 20 - 2>/dev/null | shasum
done
```
`-map 0:a` (sem o `:0`) falha em silêncio quando há duas trilhas e devolve o SHA de entrada
vazia (`da39a3ee...`) pros dois arquivos — parece que bateu e não comparou nada.
