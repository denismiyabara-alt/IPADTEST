# Molde Burry/TRXF11 — o padrão de edição que o Denis aprovou (set/2026)

Aprovado: "Burry x Barsi" (27/09, 114 inserções, 47%) e "TRXF11 cota nova" (29/09, 156 inserções, 49,5%, 85 prints).
Denis: "ficou muito legal com ele entrando, com o Barsi, muitos prints". "Quanto mais prints melhor, não precisa economizar."

## O que faz o molde funcionar
1. **Muitos prints de fonte real** (fato relevante no fnet, cotação no Investidor10, manchetes de portal, Receita):
   push-in calculado + grifo amarelo + sublinhado vermelho no trecho citado. Meta: 35+ por vídeo; o TRXF11 teve 85.
2. **A pessoa do vídeo ENTRA na cena**: recorte (PNG sem fundo) do Burry/Barsi que desliza da esquerda
   (`foto="burry"` nas cenas num/frase/barras/duas → `assets/foto-<nome>.png`). Recorte: `hyperframes remove-background`.
3. **Gráfico de série** (peça `G`, desde 03/10): Selic, IPCA ou cotação real que se desenha, com fonte no canto.
   Ação/FII só com comparador (IBOV, IFIX, CDI) ou aviso na tela; o código recusa o resto. Ver SKILL.md, seção 2b.
3a. **Cartelas animadas no traço do Faz a Conta**: papel, linha "fervendo" a 8 fps, contagem, barras, carimbo, balão, fórmula, lista, fluxo.
4. **Sons em cada evento** (whoosh, pop, tique da contagem, carimbo, marca-texto) → `sfx.wav` mixado a 0,55.
5. **Cobertura ~50%**, cartela dura a frase (teto 6 s), corte seco, entrada ancorada em FRASE (regex), nunca em timecode.
6. **Número errado na fala**: a cartela escreve o do roteiro; a fala fica (Denis 29/09: "segue o roteiro e deixa minha fala").

## Estrutura de pasta do projeto (os scripts assumem isso)
```
<projeto>/  BRUTO.MOV · master.wav/json · cuts.py · corte_frames.py · FINAL-corte.mp4 · final.json
            pecas.py · plano.py · mapa.py · montar.py · sfx.py · prints/ (png + prints.json) · tools/
            videos/broll/ gerar.py · grafico.py · cenas.py · hyperframes.json · package.json · assets/{prints/,foto-*.png}
                          graficos/<id>/ (projeto) · graficos/renders/<id>.mp4 · graficos.json
```

## Cadeia (comandos)
1. Corte: `mlx_whisper` (caminho: `~/Library/Python/3.9/bin/mlx_whisper`, modelo large-v3-turbo) → `timeline.py`/`repetidos.py`
   (skill/scripts) → `palavras.py a-b` pra bordas → editar `CORTES` em `corte/cuts.py` → `python3 cuts.py` (onda/Otsu)
   → trocar `SRC` em `corte_frames.py` → `python3 corte_frames.py` → transcrever o FINAL-corte (`final.json`)
   → procurar pato → `auditar.py FINAL-corte.mp4 cuts.json` (python do CommandLineTools, que tem mlx_whisper).
   GAP-PAL perto de pato = re-transcrever aquela janela de 30 s antes de confiar na borda.
2. Prints: agente general-purpose em BACKGROUND com `prints-tools/` (shot.mjs web / pdfshot.py PDF / build_prints.py),
   saída `prints/*.png` + `prints/prints.json` com `bbox_trecho` 0–1. Exemplo de pedido: ver `exemplos/`.
3. Cartelas: `videos/broll/cenas.py` (id → tipo, dados) — modelos em `exemplos/*/cenas.py`.
4. Âncoras: `pecas.py` (id, "A"|"B", regex no texto SEM acento do final.json, atraso) → `python3 plano.py final.json`.
   Peças a < 2 s uma da outra estouram o mapa: dar atraso 1,5–2 s ou tirar uma.
5. `cp prints/*.png videos/broll/assets/prints/` → `cd videos/broll && python3 gerar.py` →
   `npx -y hyperframes@0.6.40 snapshot --at t1,t2` (fonte no snapshot sai diferente; no render sai certa) →
   `npx -y hyperframes@0.6.40 render -o renders/broll.mp4` (~5 min p/ 650 s).
5b. Gráficos (peça G): `export IEC_MOTION=~/IPADTEST/motion` → `cd videos/broll && python3 grafico.py --render`
   (um render por gráfico, 10–20 s cada; saída `graficos.json`, lida pelo mapa, montar e sfx).
6. `python3 mapa.py && python3 montar.py && python3 sfx.py` → mix:
   `ffmpeg -i VIDEO-FINAL.mp4 -i sfx.wav -filter_complex "[1:a]aresample=48000,volume=0.55[s];[0:a][s]amix=inputs=2:duration=first:normalize=0[a]" -map 0:v -map "[a]" -c:v copy -c:a aac -b:a 320k VIDEO-FINAL-com-efeitos.mp4`
7. Conferir: hash do áudio FINAL-corte = VIDEO-FINAL; nb_frames vídeo = áudio; contact sheet de 12 frames.

## Dependência externa
`sfx.py` importa `~/Downloads/faz-a-conta/bets/sfx.py` (sons sintetizados + biblioteca media-use). NÃO apagar essa pasta.
