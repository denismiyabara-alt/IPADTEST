#!/usr/bin/env bash
# Gera o projeto HyperFrames a partir de um JSON e renderiza o MP4, medindo o tempo.
# Uso: ./renderizar.sh exemplos/selic-16x9.json [saida.mp4]
# Um job pesado por vez (Mac de 16 GB): não rode junto com transcrição, voz ou outro render.
set -euo pipefail
cd "$(dirname "$0")"
ENTRADA="$1"
NOME=$(basename "$ENTRADA" .json)
SAIDA="${2:-renders/$NOME.mp4}"
[ -d node_modules/hyperframes ] || npm install
mkdir -p "$(dirname "$SAIDA")"
python3 grafico_cotacao/gerar.py "$ENTRADA" -o "projetos/$NOME"
INI=$(date +%s)
(cd "projetos/$NOME" && npx hyperframes render -o "$(cd - >/dev/null; cd "$(dirname "$SAIDA")"; pwd)/$(basename "$SAIDA")" 2>&1 | grep -E "rendered in|rror" || true)
echo "render: $(( $(date +%s) - INI )) s → $SAIDA"
