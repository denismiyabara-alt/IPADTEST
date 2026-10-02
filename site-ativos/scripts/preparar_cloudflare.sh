#!/usr/bin/env bash
# Prepara saida/ para o `wrangler deploy`: copia _headers e .assetsignore e confere o build.
# Uso (na raiz de site-ativos/ ou do repo iec-ativos):  bash scripts/preparar_cloudflare.sh
set -euo pipefail
cd "$(dirname "$0")/.."
SAIDA="${IEC_SAIDA:-saida}"
MINIMO="${IEC_MINIMO_PAGINAS:-20}"   # abaixo disso, algo deu errado no build: não publica

test -d "$SAIDA" || { echo "ERRO: $SAIDA/ não existe. Rode antes: python3 -m iec_ativos tudo"; exit 1; }
cp cloudflare/_headers cloudflare/.assetsignore "$SAIDA/"

paginas=$(find "$SAIDA" -name index.html | wc -l)
arquivos=$(find "$SAIDA" -type f | wc -l)
maior=$(find "$SAIDA" -type f -printf '%s\n' | sort -n | tail -1)
echo "páginas: $paginas | arquivos: $arquivos | maior arquivo: $maior bytes"
for f in acoes/index.html fiis/index.html sitemap-ativos.xml; do
  test -s "$SAIDA/$f" || { echo "ERRO: falta $SAIDA/$f"; exit 1; }
done
[ "$paginas" -ge "$MINIMO" ] || { echo "ERRO: só $paginas páginas (mínimo $MINIMO)"; exit 1; }
[ "$arquivos" -le 20000 ] || { echo "ERRO: $arquivos arquivos (limite do Cloudflare: 20.000 por versão)"; exit 1; }
[ "$maior" -le 26214400 ] || { echo "ERRO: arquivo acima de 25 MiB"; exit 1; }
echo "ok: $SAIDA/ pronto para o wrangler"
