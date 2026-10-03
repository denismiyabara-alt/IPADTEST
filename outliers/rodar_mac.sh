#!/bin/bash
# Rodada do OUTLIER → ENCAIXE no Mac (chamada pelo com.denal.outliers.plist).
# coleta (API, sem search) -> propostas -> cards no Trello (sem duplicar). Cada passo segue mesmo se o anterior falhar:
# sem coleta nova, o propor.py usa o último snapshot (ou o .md do radar); sem Trello, o resumo das 8h50 ainda lê o JSON.
set -u
cd "$(dirname "$0")/.." || exit 1
PY="${PYTHON:-/usr/bin/python3}"
echo "== $(date '+%Y-%m-%d %H:%M') outliers"
"$PY" outliers/coletar.py || echo "AVISO: coleta falhou (o propor.py usa a última saída)"
"$PY" outliers/propor.py || { echo "ERRO: propor.py falhou"; exit 1; }
"$PY" outliers/entregar.py || echo "AVISO: Trello falhou (os cards saem na próxima rodada)"
