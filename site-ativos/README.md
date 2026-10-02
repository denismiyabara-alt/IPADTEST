# iec-ativos (MVP)

Páginas estáticas de ações e FIIs do Investir e Coçar, com dados oficiais da CVM, da B3 e do Banco Central.
Desenho aprovado: `DESENHO.md`. O que foi feito, conferências e achados: `RELATORIO-MVP.md`.

Esta pasta já está no formato do futuro repositório `iec-ativos`: dá para copiar `site-ativos/` inteira para lá.
A única referência de fora é o plugin `iec-ferramentas` (fonte única das calculadoras), lido de
`../wordpress-plugin/iec-ferramentas` ou de `IEC_PLUGIN=/caminho` (no repo novo: submódulo ou `vendor/`).

## Instalar

```sh
python3 --version          # 3.11 ou mais
pip install -r requirements.txt   # jinja2 e pytest
```

## Rodar

```sh
python3 -m iec_ativos tudo          # baixar → normalizar → selecionar → calcular → validar → gerar (não publica)
python3 -m pytest -q tests          # 26 testes, sem rede (fixtures em tests/fixtures)
```

Etapas soltas: `baixar`, `normalizar`, `selecionar`, `calcular`, `validar`, `gerar`.

- **baixar**: CVM (cadastro, FCA, DFP 5 anos, ITR 4 anos, informes de FII), B3 (COTAHIST anual de 6 anos e diários
  depois do último anual) e BCB (SGS 11, 12, 432, 433 e 13522). Cache em `cache/raw/`, pedido condicional
  (If-Modified-Since/ETag), 1 requisição por segundo por host, para em 403/429. O ZIP anual do COTAHIST (~90 MB)
  é lido em streaming, filtrado para o mercado à vista (`.txt.gz` de ~15 MB) e apagado. Primeira carga: ~5 min.
- **normalizar**: SQLite em `cache/dados.sqlite` (tabelas da seção 3 do desenho).
- **selecionar**: os 20 ativos (10 ações, 10 FIIs) por volume; grava `cache/selecao.json` e carrega as demonstrações só dessas empresas.
- **calcular**: fichas em `cache/fichas/<TICKER>.json` e tabela `indicador`.
- **validar**: testes da seção 8.2 com os dados reais → `cache/validacao.json`. Bloqueante impede a página.
- **gerar**: HTML em `saida/` + `sitemap-ativos.xml`, `robots-trecho.txt`, `redirects.csv`, `htaccess-exemplo.txt`,
  `paginas.csv` (index/noindex e motivo) e `_relatorio.json`.

Conferir no navegador (Chromium headless, Playwright):

```sh
python3 -m http.server 8765 -d saida &
CHROMIUM=/opt/pw-browsers/chromium-1194/chrome-linux/chrome PLAYWRIGHT=$(npm root -g)/playwright \
  node scripts/conferir_navegador.mjs        # erros de JS, rolagem horizontal, prints em prints/
```

Regerar as fixtures dos testes a partir do cache real: `python3 scripts/extrair_fixtures.py`.

## Publicar (nada é publicado sozinho)

```sh
python3 -m iec_ativos publicar --destino pasta --para /caminho --simular   # lista o que mudou (por hash)
python3 -m iec_ativos publicar --destino pasta --para /caminho             # copia só o que mudou
python3 -m iec_ativos publicar --destino sftp          # stub: IEC_SFTP_HOST, IEC_SFTP_USUARIO, IEC_SFTP_CHAVE, IEC_SFTP_PASTA
python3 -m iec_ativos publicar --destino cloudflare    # stub: CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID, IEC_CF_PROJETO
```

Credenciais só por variável de ambiente. Os stubs explicam (em `iec_ativos/publicar.py`) o que falta para virarem envio real.

## Variáveis de ambiente

| Variável | Para quê | Padrão |
|---|---|---|
| `IEC_BASE_ATIVOS` | raiz das páginas (subpasta ou subdomínio) | `https://investirecocaresocomecar.com.br` |
| `IEC_HOJE` | data de corte (reproduzir uma execução) | hoje |
| `IEC_ACEITAR_DY_CAIXA=1` | aceita o DY de caixa / DY estimado no lugar dos proventos revisados para indexar | desligado (regra do desenho) |
| `IEC_POSTS_COM_TITULO=1` | mostra o título dos posts do canal (vários têm "vale a pena") | rótulo neutro |
| `IEC_ADSENSE_CLIENT` | `ca-pub-...` para preencher os 3 blocos reservados | vazio (só o espaço reservado) |
| `IEC_PLUGIN`, `IEC_CACHE`, `IEC_SAIDA`, `IEC_DB`, `IEC_COTACOES` | caminhos | ver `iec_ativos/config.py` |

## Estrutura

```
iec_ativos/        pacote: rede, baixar, normalizar, selecionar, contas, calcular, validar, graficos, texto,
                   ferramentas, seo, gerar, publicar, formato, __main__
templates/         Jinja2 (ação, FII, lista, ranking, comparador, calendário, metodologia)
tests/             pytest + fixtures (recortes reais, gzip, ~250 KB)
dados/referencia/  lista das cotacao-* linkadas (cópia versionada do seo/varredura.json)
dados/dicionarios/ dicionários de dados da CVM (cadastro, DFP, ITR, FII mensal e trimestral)
scripts/           extrair_fixtures.py, conferir_navegador.mjs
prints/            capturas do Chromium headless
cache/, saida/     gerados (fora do Git)
```
