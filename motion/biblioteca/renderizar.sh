#!/usr/bin/env bash
# Gera o projeto HyperFrames de uma peça da biblioteca (barras ou rosca, lida do campo "peca" do JSON),
# renderiza o MP4 medindo o tempo e, com --gif, faz um GIF curto para revisão.
# Mesmo jeito do motion/renderizar.sh do grafico_cotacao (que não muda).
# Uso (de motion/): ./biblioteca/renderizar.sh exemplos/rosca-megasena-9x16.json [saida.mp4] [--gif]
# Um job pesado por vez (Mac de 16 GB): não rode junto com transcrição, voz ou outro render.
set -euo pipefail
cd "$(dirname "$0")/.."
ENTRADA="$1"
NOME=$(basename "$ENTRADA" .json)
SAIDA="${2:-renders/$NOME.mp4}"
GIF="${3:-}"
[ "$SAIDA" = "--gif" ] && { SAIDA="renders/$NOME.mp4"; GIF="--gif"; }
[ -d node_modules/hyperframes ] || npm install
[ -d biblioteca/node_modules/@fontsource ] || (cd biblioteca && npm install)
PECA=$(python3 -c "import json,sys; print(json.load(open(sys.argv[1])).get('peca', ''))" "$ENTRADA")
case "$PECA" in barras|rosca) ;; *) echo "campo 'peca' deve ser barras ou rosca (veio '$PECA')" >&2; exit 2;; esac
mkdir -p "$(dirname "$SAIDA")"
python3 "biblioteca/$PECA/gerar.py" "$ENTRADA" -o "projetos/$NOME"
ABS="$(cd "$(dirname "$SAIDA")"; pwd)/$(basename "$SAIDA")"
INI=$(date +%s.%N)
(cd "projetos/$NOME" && npx hyperframes render --crf "${CRF:-20}" -o "$ABS" 2>&1 | grep -E "rendered in|rror" || true)
FIM=$(date +%s.%N)
printf 'render: %.1f s → %s (%s KB)\n' "$(echo "$FIM - $INI" | bc)" "$SAIDA" "$(( $(stat -c %s "$SAIDA") / 1024 ))"
if [ "$GIF" = "--gif" ]; then
  G="${SAIDA%.mp4}.gif"
  ffmpeg -v error -y -i "$SAIDA" -vf "fps=12,scale='if(gt(iw,ih),640,360)':-1:flags=lanczos,split[a][b];[a]palettegen=max_colors=48[p];[b][p]paletteuse=dither=bayer:bayer_scale=4" "$G"
  echo "gif: $G ($(( $(stat -c %s "$G") / 1024 )) KB)"
fi
