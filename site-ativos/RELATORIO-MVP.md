# Relatório do MVP: páginas de ações e FIIs

Execução de 02/10/2026, com dados reais (pregão de 01/10/2026, ITR 2T26, informes de FII até 08/2026).
Nada foi publicado. Comandos em `README.md`.

## 1. Os 20 ativos e por quê

Critério do desenho (8.1), calculado pelo script `selecionar`. **A escolha não é recomendação.**

- **Ações:** maior volume financeiro médio diário em 12 meses (01/10/2025 a 01/10/2026; COTAHIST, CODBDI 02, TPMERC 010; volume total ÷ número de pregões), um ticker por empresa, só entre os **133 tickers válidos** das páginas `cotacao-*` (lista de `seo/varredura.json`, chave `cotacoes_linkadas`; cópia versionada em `dados/referencia/cotacoes-linkadas.txt`).
- **FIIs:** maior volume médio diário em 12 meses (CODBDI 12), com pelo menos 24 meses de negociação e informe mensal recente na CVM. Ticker ligado ao CNPJ pelo ISIN.

| Ação | Tipo | Classe | Volume médio/dia | | FII | Volume médio/dia |
|---|---|---|---|---|---|---|
| PETR4 | comum | PN | R$ 1.749 mi | | TRXF11 | R$ 22,5 mi |
| VALE3 | comum | ON | R$ 1.709 mi | | KNCR11 | R$ 19,9 mi |
| ITUB4 | banco | PN | R$ 1.099 mi | | XPML11 | R$ 16,9 mi |
| BBDC4 | banco | PN | R$ 633 mi | | MXRF11 | R$ 15,4 mi |
| BBAS3 | banco | ON | R$ 598 mi | | HGLG11 | R$ 14,6 mi |
| PRIO3 | comum | ON | R$ 567 mi | | BTLG11 | R$ 13,9 mi |
| AXIA3 | comum | ON | R$ 560 mi | | GGRC11 | R$ 11,3 mi |
| BPAC11 | banco | **unit** (1 ON + 2 PN) | R$ 534 mi | | GARE11 | R$ 11,1 mi |
| SBSP3 | comum | ON | R$ 474 mi | | CPOF11 | R$ 10,4 mi |
| ABEV3 | comum | ON | R$ 419 mi | | KNIP11 | R$ 10,2 mi |

O top 10 já trouxe 4 bancos e 1 unit (BPAC11), então nenhuma troca foi necessária. Os seguintes no ranking de ações: RENT3, EMBJ3, WEGE3, ITSA4.

## 2. O que foi implementado

- **Pipeline** (`iec_ativos/`): baixar → normalizar (SQLite) → selecionar → calcular → validar → gerar → publicar, como nas seções 2 a 4 do desenho. Cache em disco, pedido condicional, 1 req/s por host, parada em 403/429. COTAHIST anual lido em streaming e reduzido de ~90 MB para ~15 MB por ano (ZIP apagado). Demonstrações da CVM lidas de dentro do ZIP com filtro por CNPJ em bytes (13 s para 9 arquivos).
- **Fontes usadas:** CVM cadastro, FCA 2026 (tickers e composição de units), DFP 2021–2025, ITR 2023–2026 (consolidado, maior VERSAO, com composição do capital), informe mensal de FII 2024–2026 e trimestral 2025–2026; B3 COTAHIST 2021–2026; BCB SGS 11, 12, 432, 433 e 13522 (CDI 12 meses aparece na página de FII).
- **Número de ações:** composição do capital do DFP/ITR (o caminho do desenho, 4.4). O FRE não foi baixado (só serviria ao teste 6, que ficou adaptado; ver seção 5).
- **Indicadores** (seção 4): P/L, P/VP, ROE, DY de caixa (com esse nome), margem líquida, EBITDA calculado, margem EBITDA, dívida líquida/EBITDA (sem e com arrendamentos), LPA, VPA, valor de mercado por classe, variação de 12 meses. Bancos: só P/L, P/VP, ROE e DY, com a frase que explica. FII: P/VP, DY estimado (ver 5), vacância física ponderada pela área, cotistas, PL. TTM pelo método 4.3. Fonte e data em cada número (`data-fonte` e `data-ref` no HTML e nota visível).
- **Páginas (33):** 10 de ações, 10 de FIIs, `/acoes/` e `/fiis/` (com o aviso da escolha por volume), 4 rankings de ações e 3 de FIIs (com filtros fixos e coluna "por que o número pode enganar"), comparador `/comparar/acoes/` (JS leve com JSON embutido; parâmetros na URL, canonical limpo), calendário `/dividendos/calendario/` **só esqueleto** (não há proventos aprovados), metodologias de ações e de FIIs (fórmulas, testes, registro de correções). Gráficos em SVG gerado no build (sem JS, sem CDN). 3 espaços de anúncio reservados com altura fixa, longe de ferramenta e tabela. Páginas de 53 a 77 KB.
- **Ferramentas:** o plugin publicado (1.2.0) **não foi alterado**. O build lê `markup.html`, `style.css` e `app.js` do plugin e aplica o que a 1.3.0 fará (`iec_ativos/ferramentas.py`): `data-*` com os valores do ativo, campos preenchidos, `modo="compacto"` (as seções explicativas saem e viram link para a metodologia, onde o texto do plugin aparece uma vez só) e **preco-justo só calcula no clique** (botão "Calcular"; nada aparece ao abrir; mudar um campo limpa o resultado). As frases de conclusão "pode haver desconto" e "pode estar cara" foram trocadas por frases neutras. Cada troca confere o trecho original: se o plugin mudar, o build para. O plugin 1.3.0 fica como próximo passo (a mudança no PHP e no JS do plugin não é pequena o bastante para fazer sem testar no WordPress).
- **SEO** (seção 6): URLs `/acoes/{ticker}/` e `/fiis/{ticker}/`, title ≤ 60 + " | Investir e Coçar", meta description com números, um JSON-LD (WebPage + about Corporation/Organization com CNPJ + BreadcrumbList), canonical, `sitemap-ativos.xml` só com as indexáveis, `noindex, follow` nas incompletas, texto gerado curto a partir dos números (frases só existem com dado). `redirects.csv` e `htaccess-exemplo.txt`: 301 das 10 `cotacao-*` do MVP para `/acoes/{t}/` e 410 dos 10 tickers inválidos. **Nada aplicado no site.**
- **Regras:** aviso "não é recomendação" no topo e completo no rodapé de toda página; teste automático de palavras proibidas e de corretoras (o emissor pode aparecer como emissor: Banco BTG Pactual, XP Malls); link "Achou um número errado?".
- **Publicação configurável:** `publicar --destino pasta` (padrão; copia só o que mudou, por hash; `--simular`), stubs documentados para `sftp` e `cloudflare` (credenciais só por variável de ambiente). `IEC_BASE_ATIVOS` troca subpasta por subdomínio.

## 3. Testes

### 3.1 Com os dados reais, a cada execução (`validar` e `gerar`)

154 checagens de dados nos 20 ativos (147 ok, 7 alertas, **0 bloqueantes falhando**) + testes 13, 14 e 15 em cada uma das 33 páginas (todas passaram). Os testes pegaram problemas reais durante o desenvolvimento (ver seção 6): eles bloquearam AXIA3, BPAC11 e SBSP3 até a regra certa ser escrita.

| # | Teste | Tolerância | Tipo |
|---|---|---|---|
| 1 | Ativo total = passivo + PL | R$ 1 mil | bloqueante |
| 2 | Lucro consolidado = controladora + não controladores | 0,1% | bloqueante |
| 3 | Soma dos 4 trimestres do ano = DFP (receita, EBIT, lucro); TTM = soma dos 4 últimos trimestres | R$ 1 mil (+ lucro de não controladores quando a empresa zerou a linha da controladora; diferença aceita só se for igual à reapresentação encontrada) | bloqueante |
| 4 | Escala: nenhum trimestre ±500x o anterior | 500x | bloqueante |
| 5 | LPA calculado × LPA básico divulgado (DFP) | 3% | alerta |
| 6* | Ações em circulação: último documento × anterior (o FRE ficou fora do MVP) | 1% | alerta |
| 9 | Preço: pregão sem negócio; salto diário > 30% sem evento | exato | alerta |
| 10 | FII: patrimônio ÷ cotas = valor patrimonial da cota | 0,5% | bloqueante |
| 12* | FII: DY mensal informado coerente (sem negativo, sem > 3% no mês, sem mês copiado) | — | alerta |
| 13 | Todo número com `data-fonte` e `data-ref` | 100% | bloqueante |
| 14 | Sem palavras de recomendação nem corretoras | zero | bloqueante |
| 15 | HTML bem formado, 1 H1, title ≤ 60, 1 JSON-LD, canonical | 100% | bloqueante |

Alertas desta execução: PRIO3 (−1,15% de ações em circulação no 2T26: recompra), SBSP3 (+400% de ações e queda de 167,00 para 32,99 em 29/04/2026: **desdobramento de 1 para 5 não cadastrado**; a variação de 12 meses é escondida e a página avisa), AXIA3 (27 pregões sem negócio: troca de ticker), CPOF11 (114 pregões sem negócio; DY informado negativo em 4 meses), XPML11 (DY negativo e informes repetidos). Testes 7, 8 e 11 são manuais ou dependem da tabela de proventos aprovada, que ainda não existe.

### 3.2 Sem rede (`python3 -m pytest -q tests`): 26 testes, todos passando

Fixtures de ~250 KB extraídas dos arquivos reais (`scripts/extrair_fixtures.py`): Petrobras, Itaú, BTG, Vale e Axia (DFP 2024–2025, ITR 2025–2026, recorte de contas), HGLG11 e XPML11 (informes), 75 linhas do COTAHIST e o FCA das units.

- **Escala MIL** (receita da Petrobras 497.549.000 × 1000) e **LPA sem escala** (8,54 continua 8,54, embora a linha diga MIL).
- **Maior VERSAO** (ITR 1T26 da Petrobras tem versões 1 e 2; só a 2 fica).
- **TTM = soma das DREs**: lucro da controladora até 30/06/2026 = 110.129 + 85.108 − 61.861 = R$ 133.376 mi = 32.705 + 15.563 + 32.663 + 52.445 (tolerância R$ 1 mil).
- **LPA calculado ≈ divulgado**: 110.129.000.000 ÷ 12.888.732.761 ações = 8,5446 × 8,54 divulgado (0,05%; tolerância 3%). Vale: LPA "ON" está em 3.99.01.02 (3.99.01.01 é "PNA") e as ações vêm em milhares; o teste passa.
- **ON/PN**: valor de mercado da Petrobras com PETR3 para as ON e PETR4 para as PN.
- **Unit**: BTG com preço implícito BPAC11 ÷ 3 e LPA da unit = LPA × 3.
- **Banco sem EBITDA**: Itaú com EBITDA, margens e dívida "não se aplica"; PL achado em 2.08.
- **Receita ≤ 0**: empresa sintética; margens "não se aplica" e P/L "não se aplica (prejuízo)".
- **P/VP de FII ≈ valor patrimonial da cota do informe** (HGLG11, 0,5%); XPML11 com informe inconsistente fica sem DY.
- Controladora preenchida com zero (Axia 3T25), reapresentação explicada (BTG 1T26), layout do COTAHIST, composição de units do FCA, testes de HTML (número sem fonte, palavras proibidas, corretora × emissor, H1, title, JSON-LD, canonical), ferramentas compactas e preco-justo só no clique, publicação só do que mudou.
- **Fluxo bloqueante de ponta a ponta**: gera as páginas, estraga o balanço da Petrobras, roda de novo: o teste 1 bloqueia, a página nova não é gravada e **a versão anterior fica igual**; o 301 da PETR4 sai do mapa de redirecionamento.

### 3.3 Navegador

`scripts/conferir_navegador.mjs` no Chromium headless (1000 px e 390 px): PETR4, ITUB4, HGLG11 e comparador. **Sem erro de JS** e sem rolagem horizontal. preco-justo: antes do clique "—", depois do clique "R$ 49,50" (Bazin). renda-fii de HGLG11 preenchido com 0,75% ao mês. Comparador monta a tabela de 10 linhas. Prints em `prints/` (JPEG, 40 a 140 KB).

## 4. Conferência manual: 3 indicadores × 2 empresas contra a DFP 2025 (CSV da CVM)

Valores lidos direto do CSV com `unzip -p dfp_cia_aberta_2025.zip ... | grep` (ÚLTIMO, consolidado, versão 1, ESCALA_MOEDA = MIL), contas feitas à mão e comparadas com a tabela "Últimos exercícios" da página gerada.

| Empresa | Indicador | Linhas do CSV (R$ mil) | Conta à mão | Página |
|---|---|---|---|---|
| Petrobras (DFP entregue 05/03/2026) | Receita 2025 | 3.01 = 497.549.000 | R$ 497,5 bi | R$ 497,5 bi |
| | Margem líquida 2025 | 3.11 = 110.605.000; 3.01 = 497.549.000 | 22,23% | 22,2% |
| | EBITDA calculado 2025 | 3.05 = 145.628.000; DVA 7.04.01 = −84.388.000 | 145.628 + 84.388 = R$ 230,0 bi | R$ 230,0 bi |
| Ambev (DFP entregue 12/02/2026) | Lucro da controladora 2025 | 3.11.01 = 15.503.400 | R$ 15,5 bi | R$ 15,5 bi |
| | Margem líquida 2025 | 3.11 = 15.988.433; 3.01 = 88.242.467 | 18,12% | 18,1% |
| | EBITDA calculado 2025 | 3.05 = 23.423.386; DVA 7.04.01 = −6.396.868 | R$ 29,8 bi | R$ 29,8 bi |

Conferências extras: LPA da Ambev: 15.503.400 mil ÷ (15.761.639 − 145.113) mil ações = 0,99276 × 0,99269 divulgado (3.99.01.01). P/L da Petrobras: (7.442.231.382 × R$ 54,84 da PETR3 + 5.446.501.379 × R$ 49,77 da PETR4, pregão de 01/10/2026) ÷ R$ 133.376 mi = 5,09, igual à página.

## 5. O que ficou de fora ou "não disponível", e por quê

- **DY 12 meses por ação (data ex) e tabela de proventos:** não há tabela de proventos aprovada (fila de Avisos aos Acionistas ainda não existe). As ações mostram o **"DY de caixa da empresa"** (DFC, dividendos + JCP pagos, sem os pagos a não controladores) com esse nome; o DPA usado no preco-justo também é de caixa e está rotulado.
- **FII: DY e último rendimento:** o Fundos.NET não foi usado (termos por conferir; o host respondeu 520 no teste). No lugar, um **"DY estimado"** = Σ (DY do mês informado à CVM × valor patrimonial da cota) ÷ cotação, com nota. Fica "não disponível" quando o informe é incoerente (XPML11 e CPOF11).
- **Vacância:** existe no informe trimestral (`Percentual_Vacancia`, por imóvel). "Não se aplica" para KNCR11, MXRF11 e KNIP11 (sem imóveis para renda no informe). Vacância financeira não existe no informe estruturado.
- **Calendário:** só o esqueleto, `noindex`.
- **Comparador:** sem gráfico de preço base 100 nem de DY anual; sem pares estáticos (`/comparar/a-vs-b/`).
- **Preço ajustado por desdobramento:** a tabela `evento_societario` existe, mas está vazia; o gráfico é nominal e avisa. O split da SBSP3 foi detectado pelo teste 9 e precisa ser cadastrado à mão.
- **Teste 6 contra o FRE:** FRE não baixado; o teste virou "último documento × anterior". Teste 7 (EBITDA × release), 8 e 11 (proventos) são manuais e dependem de proventos aprovados.
- **uPlot com zoom:** trocado por SVG estático com o valor no `title` de cada ponto (sem JS, sem CDN).
- **Hubs por setor, IPE, Aviso aos Acionistas, planilha de referência, workflow do GitHub Actions:** fora do MVP.
- **Indexação:** pela regra do desenho (6.7), **nenhuma página de ativo é indexável** ainda (proventos não revisados). Rankings e comparador ficam `noindex` até a cobertura ter 30 ativos (lista de 10 é rasa). Indexáveis hoje: `/acoes/`, `/fiis/` e as duas metodologias (4 URLs no sitemap). `IEC_ACEITAR_DY_CAIXA=1` aceita o DY de caixa como substituto; é decisão do Denis.

## 6. Achados novos que mudam o desenho

1. **A composição do capital não tem coluna de escala, e várias empresas informam a quantidade de ações em milhares** (Ambev, Vale, Itaú, Axia). Sem correção, o valor de mercado da Ambev saía R$ 238 milhões. Solução: escala inferida pelo LPA divulgado (lucro ÷ LPA), com fallback pelo VPA. O dicionário da CVM confirma: o campo é só `bigint`. Entra no teste 5.
2. **O LPA (3.99) vem marcado `ESCALA_MOEDA = MIL`, mas está em reais por ação.** Multiplicar por 1000 quebraria tudo. Regra: 3.99 nunca escala.
3. **O código 3.99.01.01 não é sempre ON** (na Vale é "PNA" zerado e a ON está em 3.99.01.02). A classe tem de vir da descrição.
4. **Bancos usam outro plano de contas:** PL em 2.08 (não 2.03), lucro em 3.09/3.11 com outro nome, D&A em 7.05.01, sem 3.05 de EBIT. Contas achadas pela descrição, com regras nomeadas (`iec_ativos/contas.py`).
5. **Empresas preenchem "Atribuído à controladora" com zero** quando não têm minoritários (Sabesp até 2025, Axia no 3T25). Sem regra, o P/L da Sabesp saía 30 em vez de 12. Regra: se controladora e não controladores são zero e o total não, vale o total (com tolerância documentada no teste 3).
6. **Reapresentação também do trimestre do próprio ano** (BTG reapresentou o 1T26 no ITR 2T26): o TTM pelo método 4.3 está certo, mas a soma dos trimestres originais difere. O teste 3 agora calcula a reapresentação e só aceita a diferença se ela for exatamente essa.
7. **O FCA traz a composição das units** (`Composicao_BDR_Unit`, texto livre: "1 ON E 2 PNA", "1 KLBN3 + 4 KLBN4"), o que reduz a digitação manual prevista em 4.4. Mas a linha da BPAC11 vem com ticker "000000"; ficou uma tabela manual de exceções.
8. **Informe mensal de FII:** ISIN repetido em CNPJs diferentes (20 casos; ex.: o ISIN do TRXF11 também aparece num fundo novo de outro nome), meses copiados, DY negativo e de 11,6% num mês. O DY informado não serve como DY da página sem filtro; isso reforça o Fundos.NET (ou a fila manual) como fonte.
9. **Desdobramento detectado só pelo preço:** SBSP3 (1:5 em 04/2026). O cadastro de `evento_societario` precisa de uma fonte (IPE/fato relevante) antes de qualquer gráfico ajustado.
10. **Títulos dos posts do canal** sobre os ativos do MVP usam "vale a pena", "melhor", "comprar" e citam corretora (BTG). Com a regra 7.1 e o teste 14, a página mostra rótulo neutro ("Análise do canal sobre PETR4 (1)"). Decisão do Denis: rótulo neutro, título editado, ou exceção para os próprios posts (`IEC_POSTS_COM_TITULO=1`).
11. **Com a regra 6.7 literal, nenhuma página de ativo entra no índice** até a fila de proventos existir. O MVP sai com 4 URLs no sitemap. Vale decidir se o DY de caixa basta para indexar as 10 ações.
12. **Ticker mudou** (Eletrobras → Axia, AXIA3): o histórico de preço e o volume ficam partidos entre tickers; o critério de volume subestima esses casos.
13. A URL do COTAHIST anual do ano corrente é atualizada todo dia útil (Last-Modified 01/10/2026 23:26, com o pregão de 01/10); os arquivos diários só são necessários depois do último anual.

## 7. Commits (branch de trabalho do projeto)

- `site-ativos: pipeline inicial (baixar, normalizar, selecionar, calcular)`
- `site-ativos: testes bloqueantes com dados reais e correções achadas no download`
- `site-ativos: gerador de páginas, ferramentas compactas, SEO e prints`
- `site-ativos: testes offline com fixtures reais e publicação configurável`
- `site-ativos: README, relatório do MVP, dicionários da CVM e lista das cotacao-*`
