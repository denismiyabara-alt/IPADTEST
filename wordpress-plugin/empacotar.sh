#!/bin/sh
# Gera dist/iec-ferramentas.zip pronto para "Plugins → Enviar plugin".
set -e
cd "$(dirname "$0")"
mkdir -p dist
rm -f dist/iec-ferramentas.zip
zip -r -X -q dist/iec-ferramentas.zip iec-ferramentas -x '*.DS_Store'
unzip -l dist/iec-ferramentas.zip
