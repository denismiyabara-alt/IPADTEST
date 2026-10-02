# Páginas de ações e FIIs: desenho

Projeto para o Investir e Coçar (investirecocaresocomecar.com.br). Rascunho de 02/10/2026. Ainda não tem código de produção.

**Objetivo:** criar uma página para cada ação e cada FII, com dados oficiais, gráficos e as ferramentas do plugin `iec-ferramentas`. As páginas servem para busca orgânica e para AdSense. A categoria é a mesma de sites como Status Invest e Investidor 10, mas nada vem deles: nem dados, nem textos, nem layout.

**Legenda:** **conferir** marca o que não deu para confirmar daqui. Os hosts da CVM, da B3 e do Banco Central estão bloqueados nesta nuvem, então nomes de arquivo, campos e horários marcados assim precisam ser confirmados no primeiro download real.

---

## 0. O que existe hoje (lido da varredura de 02/10/2026)

**Páginas `cotacao-*`: encontrei 143.**

- Elas estão fora do sitemap. Apareceram como links internos no JSON da varredura (`seo/varredura.json`, chave `cotacoes_linkadas`). O `varredura.csv` não tem nenhuma linha `cotacao`, porque cobre só as 368 URLs dos sitemaps.
- **Quem linka para elas:** o hub `/cotacoes/` linka as 143 (é a página com 869 palavras e 145 links de saída). Fora ele, há 1 link de `/category/cotacoes/` e 2 de `/quem-a-itausa-controla-conheca-suas-empresas/`. Na prática, 140 delas recebem um único link interno.
- **Amostra de 5** (ABEV3, ALOS3, ALPA4, AMBP3 e AMER3): todas com `noindex, follow`, **sem canonical**, título no modelo "XXXX: Cotação, Gráfico e Análise", de 326 a 413 palavras e 4 blocos JSON-LD cada.
- **Tickers quebrados:** 10 dos 143 não são tickers válidos (`b8in8l`, `bmte5l`, `cics5l`, `f8df5l`, `fmsa6l`, `i8rd6l`, `m9gv6l`, `ngrd3l`, `poly8l`, `spgs6l`). Parecem lixo de alguma importação. Sobram **133 tickers válidos**, incluindo 9 terminados em 11: units como BPAC11, SANB11, KLBN11, ENGI11 e IGTI11, mais AQPA11, EBTA11, WTXA11 e ONCO11, que precisam ser conferidos.
- **FIIs:** praticamente nenhum. As páginas `cotacao-*` são quase todas de ações.
- **Tráfego:** a pasta `seo/` não tem dados do Search Console. Como as páginas estão com `noindex`, o tráfego orgânico delas deve ser perto de zero. **Para confirmar:** o Denis exporta, no Search Console, *Desempenho → Páginas* filtrando "cotacao-" (últimos 16 meses).
- **Posts com ticker no endereço:** 26 dos 133 tickers têm posts com o ticker no slug. Os que mais têm são ITSA4 (6), PASS3 (5), BBAS3 (4), ITUB4 (4), ABEV3, CXSE3, ITUB3 e WEGE3 (3 cada). Esses posts são a fonte natural de links internos para as páginas novas.

**Site atual:**

- WordPress com o tema Blocksy, Yoast e WPSSO (com schema duplicado, ver `seo/RELATORIO.md`), WP-Optimize, Jetpack e Site Kit.
- Há sinal de Cloudflare (o beacon do Cloudflare Insights). Se o DNS passa pelo Cloudflare: **conferir**.
- O AdSense não aparece no HTML estático, só um `preconnect` para `pagead2`. Deve ser injetado pelo Site Kit (anúncios automáticos): **conferir**.

**Plugin `iec-ferramentas` 1.2.0:**

- O shortcode `[iec_ferramenta id="..."]` devolve o `markup.html` da ferramenta, e o CSS e o JS vão por `wp_enqueue_*`.
- **Cada ferramenta só pode aparecer uma vez por página**, porque os ids do HTML são fixos.
- **Os valores iniciais estão fixos no HTML** (por exemplo, `g-preco = 10.00` no `preco-justo` e `f-dy = 0.80` no `renda-fii`). Ainda não há como preencher com os números do ativo.
- **Cada ferramenta traz de 2 a 3 seções de texto explicativo** (`<h2>`). Se esse texto se repetir em 300 páginas, vira conteúdo duplicado.
- **Mudança necessária (versão 1.3):** ver a seção 5.6.

---

## 1. Arquitetura recomendada

### Opções comparadas

| Critério | A. Gerador estático em Python (HTML pronto) | B. Páginas no WordPress (via API REST ou import) | C. App separado (Next.js ou Django com banco) |
|---|---|---|---|
| **Custo mensal** | R$ 0 (GitHub Actions e a hospedagem atual, ou Cloudflare Pages) | R$ 0 de ferramenta, mas pesa no servidor do WP | Servidor e banco: de R$ 50 a R$ 300 por mês |
| **Velocidade da página** | A melhor: HTML pronto, de 30 a 60 KB, sem PHP | A do tema: cerca de 144 KB de HTML e 6 a 7 scripts | Boa, se bem feita |
| **SEO** | Controle total de title, canonical, schema e sitemap. Na subpasta, herda a autoridade do domínio | Herda o Yoast, mas também o schema duplicado de hoje (WPSSO + snippet) | Igual ao A, porém com mais coisas que podem quebrar |
| **AdSense** | Tag manual e blocos em posições fixas. A conta já cobre o domínio | Anúncios automáticos do Site Kit, sem controle de posição | Igual ao A |
| **Ferramentas do plugin** | Usa os mesmos arquivos do plugin, copiados no build (uma fonte só) | Shortcode nativo | Precisa portar |
| **Atualização diária de preço** | Gerar de novo e enviar só os arquivos alterados | Mais de 300 posts atualizados todo dia: revisões no banco, cache para limpar e risco para o site principal | Natural |
| **Manutenção** | Um script e um template. Se falhar, a versão de ontem continua no ar | Depende de plugins, tema e API. Uma falha pode sujar posts | Servidor, segurança, banco e deploy |
| **Quem atualiza** | Automático (Actions). O Denis só revisa proventos | Automático, mas mexendo no WP de produção | Automático |

### Recomendação: opção A (gerador estático em Python), publicado numa subpasta do domínio principal

1. Um pipeline em Python baixa CVM, B3 e BCB, calcula os indicadores e gera HTML estático: uma página por ativo, mais o comparador, o ranking e o calendário.
2. O resultado é publicado em `investirecocaresocomecar.com.br/acoes/…` e `/fiis/…`, como arquivos estáticos no mesmo servidor do WordPress. O `.htaccess` padrão do WP só envia para o `index.php` o que não existe como arquivo ou pasta (`!-f` e `!-d`), então uma pasta real `/acoes/` é servida direto, sem passar pelo WP. Isso precisa ser confirmado na hospedagem: **conferir**.
3. **Plano B:** se a hospedagem não permitir envio automático (SFTP ou SSH), usar o subdomínio `dados.investirecocaresocomecar.com.br` no Cloudflare Pages ou no GitHub Pages. O subdomínio herda menos autoridade do domínio, mas funciona do mesmo jeito.

**Por que a opção A:**

- **Separa os riscos.** Os dados mudam todo dia, e o WordPress não precisa ser tocado por isso. Se o pipeline errar, ele não publica, e a versão anterior continua no ar.
- **Escapa da bagunça de schema do WP.** As páginas novas nascem com um único JSON-LD limpo.
- **É a opção mais rápida.** Isso ajuda nos Core Web Vitals, e os Core Web Vitals ajudam o AdSense: página rápida tende a ter mais anúncio visto.
- **Custo zero, com tudo versionado no Git.** Dá para ver exatamente qual número mudou e quando.
- **As ferramentas continuam numa fonte só.** O build lê `markup.html`, `style.css` e `app.js` direto da pasta do plugin.

**O que se perde com a opção A:**

- Cabeçalho, menu e rodapé do Blocksy precisam ser replicados no template estático, numa versão simples com as mesmas fontes (Archivo e IBM Plex Sans, que o plugin já usa) e as mesmas cores.
- O Yoast não enxerga essas páginas. O sitemap delas é gerado pelo pipeline e declarado no `robots.txt`.

---

## 2. Pipeline de dados

```
baixar ──► normalizar ──► calcular ──► validar ──► gerar HTML ──► publicar
(raw/)     (dados.sqlite)  (indicadores)  (testes)    (dist/)        (rsync/SFTP só do que mudou)
```

| Etapa | O que faz |
|---|---|
| **Baixar** | Pede cada arquivo com `If-Modified-Since` ou ETag e só baixa o que mudou. Guarda o zip original em `raw/<fonte>/<arquivo>`, com o sha256, a URL e a data em `fonte_arquivo`. Faz uma requisição por vez, com pausa de 1 s, e para em 403 ou 429, igual à varredura SEO. |
| **Normalizar** | Lê os CSVs da CVM (`latin-1`, separador `;`), converte `ESCALA_MOEDA` (MIL vira ×1000), fica com a maior `VERSAO` por empresa e data de referência, lê o COTAHIST (posições fixas de 245 bytes) e grava tudo num SQLite. |
| **Calcular** | Monta os 12 meses móveis (TTM), o valor de mercado e os indicadores da seção 4. Cada resultado grava os ids dos insumos. |
| **Validar** | Roda os testes da seção 8. Se um teste "bloqueante" falhar, o ativo não é regerado e fica com a versão anterior. |
| **Gerar** | Usa templates Jinja2: HTML, JSON pequeno para os gráficos, sitemap e páginas de hub. |
| **Publicar** | Envia só os arquivos que mudaram e limpa o cache do Cloudflare nas URLs alteradas, se o Cloudflare for usado. |

### Frequência de cada fonte

| Fonte | Frequência | Observação |
|---|---|---|
| B3 COTAHIST diário (`COTAHIST_D{DDMMAAAA}.ZIP`) | Dias úteis, 7h30 (horário de Brasília) | Pega o pregão anterior. Horário de publicação do arquivo: **conferir**. No começo, carrega o histórico com os arquivos anuais `COTAHIST_A{AAAA}.ZIP`. |
| BCB SGS (CDI 12, Selic 11 e 432, IPCA 433 e 13522) | Dias úteis, 7h30 | O IPCA sai por volta do dia 10. Desde 26/03/2025, séries diárias exigem `dataInicial` e `dataFinal`, com no máximo 10 anos por consulta. |
| CVM DFP e ITR | Verificação diária, com download só se o arquivo mudou | Na temporada de resultados (ITR até 45 dias depois do trimestre, DFP até março) muda quase todo dia. |
| CVM cadastro de companhias, FCA | Semanal | Mapeia CNPJ, código CVM, setor e tickers. |
| CVM FRE | Mensal | Só para conferir o histórico de dividendos (item 3.5) e o capital social. |
| CVM IPE (índice de documentos) | Diária | Detecta "Aviso aos Acionistas" novos e coloca na fila de revisão de proventos. |
| CVM FII informe mensal e trimestral | Semanal | A CVM diz que esses arquivos são atualizados semanalmente com reenvios. |
| Fundos.NET, documentos estruturados de rendimentos de FII | Diária (se aprovado, ver 2.2) | **conferir** os termos. |

### Onde roda

**Recomendado: GitHub Actions**, com um cron nos dias úteis às 10h30 UTC (7h30 em Brasília).

- O runner tem internet aberta e não depende do Mac estar ligado.
- Num repositório privado, o plano gratuito dá 2.000 minutos por mês. A estimativa é de 5 a 10 minutos por execução, ou seja, de 150 a 300 minutos por mês.
- A carga inicial do histórico (COTAHIST desde 2010 e DFP/ITR desde 2011) roda uma vez à mão, pelo `workflow_dispatch`, ou no Mac.
- **Plano B: o Mac do Denis via `launchd`.** O mesmo script, com um `.plist` diário às 7h30. Vale se a CVM ou a B3 bloquearem os IPs do GitHub (**conferir** no primeiro teste).

**Segredos** (nos Secrets do GitHub, nunca no código): host, usuário e chave SFTP da hospedagem, e o token do Cloudflare (se for usado).

### Cache

- **`raw/`:** zips originais. No Actions, ficam no `actions/cache` (chave = nome do arquivo + ETag). No Mac, ficam numa pasta local. **Não vão para o Git** (o COTAHIST anual tem cerca de 90 MB).
- **`dados.sqlite`:** a base normalizada, de algumas centenas de MB. No Actions, é salva como artefato ou release da execução anterior. Só dá para versionar com Git LFS, e não vale o custo.
- **`dist/`:** o HTML gerado. É comparado com o publicado por hash, e só sobe o que mudou.

### 2.1 Fontes e arquivos exatos

Base: `https://dados.cvm.gov.br/dados/`. A licença do portal da CVM é ODbL, com atribuição "Fonte: CVM" (**conferir** na página do portal).

| Conjunto | Caminho | Arquivos dentro do zip (CSV `;`, latin-1) | Uso |
|---|---|---|---|
| Cadastro | `CIA_ABERTA/CAD/DADOS/cad_cia_aberta.csv` | um só | CNPJ, `CD_CVM`, `DENOM_SOCIAL`, `SIT`, `SETOR_ATIV` (identifica bancos e seguradoras) |
| DFP (anual) | `CIA_ABERTA/DOC/DFP/DADOS/dfp_cia_aberta_{AAAA}.zip` | `dfp_cia_aberta_{BPA,BPP,DRE,DFC_MI,DFC_MD,DVA,DMPL,DRA}_{con,ind}_{AAAA}.csv`, `dfp_cia_aberta_composicao_capital_{AAAA}.csv`, `dfp_cia_aberta_{AAAA}.csv` (índice, com link para o documento) | Balanço, DRE, fluxo de caixa, DVA e número de ações |
| ITR (trimestral) | `CIA_ABERTA/DOC/ITR/DADOS/itr_cia_aberta_{AAAA}.zip` | o mesmo padrão, com prefixo `itr_` | Trimestres e acumulado do ano |
| FCA | `CIA_ABERTA/DOC/FCA/DADOS/fca_cia_aberta_{AAAA}.zip` | `fca_cia_aberta_valor_mobiliario_{AAAA}.csv` (`Codigo_Negociacao`, `Valor_Mobiliario`, classe, mercado, segmento) e `..._geral_...` | Ticker ↔ CNPJ e classes |
| FRE | `CIA_ABERTA/DOC/FRE/DADOS/fre_cia_aberta_{AAAA}.zip` | `fre_cia_aberta_distribuicao_dividendos_{AAAA}.csv` (item 3.5), `..._capital_social_...` (**conferir** os nomes) | Conferir dividendos anuais e capital |
| IPE | `CIA_ABERTA/DOC/IPE/DADOS/ipe_cia_aberta_{AAAA}.zip` | `ipe_cia_aberta_{AAAA}.csv`: categoria, tipo, espécie, assunto, data de entrega, link de download (**conferir** as colunas) | Lista de "Aviso aos Acionistas", "Fato Relevante" e "Comunicado ao Mercado" |
| FII mensal | `FII/DOC/INF_MENSAL/DADOS/inf_mensal_fii_{AAAA}.zip` | `inf_mensal_fii_geral_...` (CNPJ, nome, ISIN, segmento, mandato), `inf_mensal_fii_complemento_...` (`Total_Numero_Cotistas`, `Patrimonio_Liquido`, `Cotas_Emitidas`, `Valor_Patrimonial_Cotas`, `Percentual_Dividend_Yield_Mes`, `Percentual_Rentabilidade_Efetiva_Mes`) e `inf_mensal_fii_ativo_passivo_...` (`Rendimentos_Distribuir`) | VP por cota, cotistas e PL |
| FII trimestral | `FII/DOC/INF_TRIMESTRAL/DADOS/inf_trimestral_fii_{AAAA}.zip` | `inf_trimestral_fii_imovel_...` (por imóvel: área, `Percentual_Vacancia`, `Percentual_Inadimplencia`, `Percentual_Receitas_FII`), `..._resultado_contabil_financeiro_...` e outros (**conferir** os nomes) | Vacância e inadimplência |
| Dicionários | página de cada conjunto em `dados.cvm.gov.br/dataset/...` | `meta_*.txt` / zip "Dicionário de Dados" | Baixar e versionar no repositório |

**Atenção (conferir):** os informes de FII mudaram de layout com a adaptação à Resolução CVM 175 (há leiautes 2016–2020, 2021+ e um posterior a agosto de 2025). O leitor precisa reconhecer o leiaute pelo cabeçalho.

**B3:**

- Arquivos anuais e diários: `https://bvmf.bmfbovespa.com.br/InstDados/SerHist/COTAHIST_A{AAAA}.ZIP` e `COTAHIST_D{DDMMAAAA}.ZIP`.
- Layout: `SeriesHistoricas_Layout.pdf`, em `www.b3.com.br`.
- Campos usados: `DATA`, `CODBDI` (02 = lote padrão, 12 = FII), `CODNEG`, `TPMERC` (010 = à vista), `PREABE`, `PREMAX`, `PREMIN`, `PREULT`, `PREMED`, `TOTNEG`, `QUATOT`, `VOLTOT`, `FATCOT` e `CODISI`.
- Os preços vêm **sem ajuste** por proventos e desdobramentos.

**BCB:**

- API: `https://api.bcb.gov.br/dados/serie/bcdata.sgs.{codigo}/dados?formato=json&dataInicial=dd/mm/aaaa&dataFinal=dd/mm/aaaa`.
- Séries: 12 (CDI diário), 11 (Selic diária), 432 (meta Selic), 433 (IPCA mensal) e 13522 (IPCA em 12 meses).

### 2.2 Proventos: onde há fonte oficial e permitida

Proventos são o ponto fraco. Não existe um CSV oficial e aberto com "dividendo por ação, data com e data de pagamento" para todas as ações.

| Fonte | O que tem | Pode automatizar? |
|---|---|---|
| **B3, Empresas Listadas → Eventos corporativos → Proventos em dinheiro** (`sistemaswebb3-listados.b3.com.br`) | Tabela por ticker (tipo, valor, data de aprovação, data com, pagamento), vinda do formulário de proventos que a empresa preenche na B3 | **Não recomendo.** A página usa uma API interna, sem documentação nem termo de uso para acesso automatizado. A B3 vende esses dados pelo UP2DATA e pelos canais de market data. Usar só como **conferência manual**. |
| **CVM IPE → "Aviso aos Acionistas"** (PDF no `www.rad.cvm.gov.br`) | Documento oficial com o valor por ação, a data com e o pagamento | Sim, para **baixar e listar**: o índice é dado aberto. O valor está em PDF de texto livre. Proposta: o pipeline baixa o PDF, extrai uma **sugestão** (com regex e pdfplumber) e põe numa fila. O Denis aprova cada linha antes de publicar. Com 10 ações, são poucos avisos por mês. |
| **CVM DFP/ITR, demonstração de fluxo de caixa** | Total de dividendos e JCP **pagos** pela empresa no período (linhas de 6.03 com "dividendo" ou "juros sobre capital" na descrição) | Sim. Serve para um **"DY de caixa"** em nível da empresa, enquanto a tabela por ação não estiver completa. |
| **CVM FRE, item 3.5** | Dividendos distribuídos por exercício e payout | Sim. Usado como conferência anual. |
| **Fundos.NET** (`fnet.bmfbovespa.com.br`), documentos **estruturados** de rendimentos e amortizações de FII | XML com o valor por cota, a data base e o pagamento, enviado pelo administrador à CVM e à B3 | Provavelmente sim: é o canal oficial de envio à CVM, e as páginas de documento são públicas. Os termos de uso e o limite de requisições estão **por conferir**. É a melhor fonte para o DY de FII. |
| **CVM informe mensal de FII** | `Percentual_Dividend_Yield_Mes` e `Rendimentos_Distribuir` | Sim. O DY informado é sobre o PL, não sobre a cotação (**conferir** a definição no dicionário). Serve como conferência, não como o DY da página. |

**Decisão proposta:**

- **Ações:** fila semiautomática pelos Avisos aos Acionistas da CVM, com aprovação do Denis. Até a tabela ter 12 meses completos, a página mostra o "DY de caixa" da DFC, com esse nome.
- **FIIs:** Fundos.NET estruturado, se os termos permitirem. Se não permitirem, a mesma fila manual pelos avisos aos cotistas.

---

## 3. Modelo de dados

Um arquivo SQLite (`dados.sqlite`). **Regra geral:** todo número publicado aponta para um `fonte_arquivo_id` e tem uma `data_ref`. A página mostra os dois.

| Tabela | Campos principais |
|---|---|
| `fonte_arquivo` | `id`, `fonte` (CVM-DFP, CVM-ITR, B3-COTAHIST, BCB-SGS…), `url`, `arquivo`, `etag`, `last_modified`, `baixado_em`, `sha256`, `linhas` |
| `empresa` | `cnpj` (14 dígitos, sem máscara), `cd_cvm`, `nome`, `setor_cvm`, `tipo` (`comum`, `banco`, `seguradora` ou `holding`; automático pelo setor, com correção manual), `situacao`, `fonte_arquivo_id`, `data_ref` |
| `ativo` | `ticker`, `cnpj_emissor`, `isin`, `classe` (ON, PN, PNA, PNB, UNIT ou FII), `composicao_unit` (JSON, ex.: `{"ON":1,"PN":4}`, com a fonte: estatuto ou FRE), `listado_desde`, `ativo` (sim/não), `fonte_arquivo_id` |
| `conta` | `cnpj`, `doc` (DFP ou ITR), `demonstracao` (BPA, BPP, DRE, DFC_MI, DFC_MD ou DVA), `escopo` (con ou ind), `dt_refer`, `dt_ini_exerc`, `dt_fim_exerc`, `ordem_exerc`, `versao`, `cd_conta`, `ds_conta`, `conta_fixa`, `valor_reais` (já multiplicado pela escala), `escala_original`, `fonte_arquivo_id` |
| `capital` | `cnpj`, `doc`, `dt_refer`, `versao`, `qt_on`, `qt_pn`, `qt_total`, `qt_on_tesouraria`, `qt_pn_tesouraria`, `fonte_arquivo_id` |
| `preco_diario` | `ticker`, `data`, `abertura`, `maxima`, `minima`, `fechamento`, `medio`, `negocios`, `quantidade`, `volume_rs`, `fatcot`, `isin`, `codbdi`, `fonte_arquivo_id` |
| `evento_societario` | `ticker`, `tipo` (desdobramento, grupamento ou bonificação), `fator`, `data_ex`, `doc_url` (CVM), `conferido_por`, `conferido_em` |
| `provento` | `ticker`, `tipo` (DIV, JCP, RENDIMENTO ou AMORTIZACAO), `valor_bruto_por_acao`, `data_aprovacao`, `data_com`, `data_ex`, `data_pagamento`, `doc_url` (protocolo CVM ou Fundos.NET), `origem` (aviso_cvm, fnet ou manual), `status` (sugerido ou aprovado), `aprovado_por`, `aprovado_em` |
| `fii_mensal` | `cnpj`, `data_ref`, `cotistas`, `pl`, `cotas_emitidas`, `vp_cota`, `dy_mes_informado`, `rendimentos_distribuir`, `segmento`, `mandato`, `versao`, `fonte_arquivo_id` |
| `fii_imovel_trim` | `cnpj`, `data_ref`, `imovel`, `classe`, `area_m2`, `vacancia_pct`, `inadimplencia_pct`, `pct_receita`, `fonte_arquivo_id` |
| `macro` | `serie` (12, 11, 432, 433 ou 13522), `data`, `valor`, `fonte_arquivo_id` |
| `indicador` | `ticker`, `nome`, `valor`, `status` (ok, nao_se_aplica, sem_dado ou negativo), `data_preco`, `periodo_contabil` (ex.: "TTM até 30/06/2026"), `formula_versao`, `insumos` (JSON com os ids de `conta`, `preco_diario` e `provento`), `calculado_em` |
| `pagina` | `url`, `tipo`, `indexavel` (sim/não, ver 6.7), `hash_conteudo`, `lastmod_dados` (muda só quando muda dado contábil ou provento, não com o preço), `publicado_em` |

---

## 4. Indicadores e fórmulas

### 4.1 Convenções

- **Empresa comum:** usar o **consolidado** (`_con`). Se a empresa não publica consolidado, usar o individual (`_ind`) e marcar na página "demonstração individual".
- **Versão:** para cada (CNPJ, `DT_REFER`), usar a maior `VERSAO`.
- **Reapresentações:** o período do ano anterior vem do documento **mais recente**, ou seja, da linha `ORDEM_EXERC = PENÚLTIMO` do ITR ou da DFP atual, porque essa já traz a reapresentação. A página avisa: "Valores do ano anterior conforme reapresentados no ITR de …".
- **Escala:** `ESCALA_MOEDA = MIL` vale ×1000. Teste de sanidade: se a receita variar mais de 500 vezes em relação ao período anterior, a página não é publicada e o caso vai para revisão. Já houve empresa declarando "UNIDADE" com valores em milhares.
- **Ano fiscal que não fecha em dezembro:** é raro, mas existe. A soma TTM usa `DT_INI_EXERC` e `DT_FIM_EXERC`, nunca o "trimestre do calendário".
- **Códigos de conta:** só são estáveis os de `ST_CONTA_FIXA = S`. Os demais são buscados pela descrição (`DS_CONTA`), com uma lista de sinônimos versionada.

### 4.2 Contas usadas (empresas não financeiras; códigos **conferir** no primeiro download)

| Termo | Conta |
|---|---|
| Receita líquida | DRE `3.01` Receita de Venda de Bens e/ou Serviços |
| EBIT | DRE `3.05` Resultado Antes do Resultado Financeiro e dos Tributos |
| Lucro líquido total | DRE `3.11` Lucro/Prejuízo Consolidado do Período |
| Lucro da controladora | DRE `3.11.01` Atribuído a Sócios da Empresa Controladora (no individual, `3.11`) |
| LPA divulgado | DRE `3.99.01.01` (ON) e `3.99.01.02` (PN), básico. Usado só para conferência |
| D&A | DVA `7.04.01` Depreciação, Amortização e Exaustão. Se faltar, somar as linhas de `6.01.01` da DFC indireta que contêm "deprecia", "amortiza" ou "exaust" |
| Caixa | BPA `1.01.01` Caixa e Equivalentes de Caixa |
| Aplicações de curto prazo | BPA `1.01.02` Aplicações Financeiras |
| Dívida bruta | BPP `2.01.04` + `2.02.01` Empréstimos e Financiamentos (circulante e não circulante; debêntures entram aqui) |
| Arrendamentos | Sem código fixo: buscar "arrendamento" em `2.01.05`/`2.02.02` e nas subcontas. É mostrado à parte |
| PL total | BPP `2.03` Patrimônio Líquido Consolidado |
| Participação de não controladores | BPP `2.03.09` (**conferir**; o código varia em algumas empresas, então buscar também por "Não Controladores") |
| Proventos pagos (DY de caixa) | DFC: linhas de `6.03` com "dividendo" ou "juros sobre (o) capital", sinal invertido |

### 4.3 Doze meses móveis (TTM) a partir do ITR acumulado

A DRE do ITR traz linhas do trimestre (3 meses) e do acumulado no ano. A DFC e a DVA trazem só o acumulado. O 4º trimestre não tem ITR: ele aparece só na DFP.

```
TTM(ano A, trimestre q) = DFP(A-1, 12 meses)
                        + Acumulado(A, até q)         [ITR atual, ORDEM_EXERC = ÚLTIMO, DT_INI = 01/01/A]
                        - Acumulado(A-1, até q)       [ITR atual, ORDEM_EXERC = PENÚLTIMO]
Quando q = 4º trimestre: TTM = DFP(A).
4º trimestre isolado (para os gráficos) = DFP(A) - Acumulado 9 meses(A) [ITR do 3º trimestre].
```

Se a DFP do ano anterior foi reapresentada depois do ITR, vale a versão mais recente, desde que as duas peças sejam coerentes: o teste 8.2 confere isso.

Itens de balanço (caixa, dívida, PL) **não** têm TTM: vale a posição do último ITR ou DFP.

### 4.4 Número de ações e valor de mercado

- Ações em circulação por classe = `capital.qt_on − qt_on_tesouraria` e `qt_pn − qt_pn_tesouraria`, do último ITR ou DFP. A página mostra a data. Recompras e bonificações posteriores só entram no documento seguinte; enquanto isso, a página avisa.
- **Valor de mercado** = Σ por classe de (fechamento da classe × ações em circulação da classe).
  - **ON e PN negociadas:** cada uma com o seu preço.
  - **Classe sem negociação** (ex.: uma ON que não é negociada): usar o preço da classe negociada e marcar "estimado".
  - **Units** (SANB11, KLBN11, ENGI11, BPAC11, IGTI11, TAEE11…): o preço implícito de cada classe sai do preço da unit dividido pela composição (`ativo.composicao_unit`), quando a ON ou a PN avulsa não tem liquidez. Indicadores por ação da unit = indicador por ação × ações por unit. Os valores de `composicao_unit` vêm do estatuto ou do FRE, digitados à mão com a fonte. A composição dos exemplos está por **conferir** para cada caso.
- **Preço:** fechamento (`PREULT`) do COTAHIST, `CODBDI` 02 e `TPMERC` 010, dividido por `FATCOT` quando for maior que 1.
- **Gráfico de preço:** mostra o preço nominal e, à parte, o preço "ajustado por desdobramentos" com base em `evento_societario`. Para não haver ajuste errado, eventos não confirmados não ajustam nada.

### 4.5 Ações: fórmulas

| Indicador | Fórmula | Regras |
|---|---|---|
| **P/L** | Valor de mercado ÷ Lucro da controladora TTM | Com lucro ≤ 0, mostrar "não se aplica (prejuízo em 12 meses)" |
| **P/VP** | Valor de mercado ÷ (PL `2.03` − não controladores `2.03.09`) | Com PL ≤ 0, mostrar "não se aplica" |
| **DY 12 meses** | Σ proventos brutos por ação (dividendos + JCP) com **data ex** nos últimos 365 dias ÷ fechamento atual | Só com proventos `aprovado`. O JCP entra **bruto**, com a nota "JCP tem 15% de IR na fonte". Enquanto a tabela não fecha 12 meses, mostrar o **"DY de caixa da empresa"** = proventos pagos TTM (DFC) ÷ valor de mercado, com esse nome |
| **ROE** | Lucro da controladora TTM ÷ média do PL da controladora (data atual e 12 meses antes) | Com PL médio ≤ 0, "não se aplica" |
| **Margem líquida** | Lucro líquido total `3.11` TTM ÷ Receita `3.01` TTM | Receita ≤ 0 vira "não se aplica" |
| **EBITDA (calculado)** | EBIT `3.05` TTM + D&A TTM (DVA `7.04.01`) | Ver ressalvas abaixo |
| **Margem EBITDA** | EBITDA TTM ÷ Receita TTM | |
| **Dívida líquida / EBITDA** | (Dívida bruta − caixa `1.01.01` − aplicações `1.01.02`) ÷ EBITDA TTM | Com EBITDA ≤ 0, "não se aplica". Uma segunda linha mostra "com arrendamentos" quando a conta for encontrada |

**Ressalvas do EBITDA:**

- É o mesmo conceito da Resolução CVM 156/2022 (lucro + tributos + resultado financeiro + D&A, sem ajustes). **Não** é o "EBITDA ajustado" do release da empresa, e a página diz isso.
- O EBIT (`3.05`) inclui a equivalência patrimonial e os itens não recorrentes, como impairment e venda de ativos.
- Com IFRS 16, a D&A inclui a amortização do direito de uso. Por isso, a dívida com arrendamentos aparece à parte.

### 4.6 Bancos, seguradoras e holdings

- **Bancos** (`SETOR_ATIV` de intermediação financeira, mais uma lista manual: ITUB4, BBAS3, BBDC4, SANB11, BPAC11, BMGB4, BRSR6…): a DRE começa em "Receitas da Intermediação Financeira", e a dívida é matéria-prima do negócio. Mostrar **só** P/L, P/VP, ROE e DY. Sem EBITDA, sem margem EBITDA, sem dívida líquida, e sem margem líquida, porque a "receita" não é comparável. A página diz por quê.
- **Seguradoras e holdings de seguros** (BBSE3, CXSE3): o mesmo tratamento dos bancos. **conferir** o plano de contas.
- **Holdings** (ITSA4): EBITDA e dívida/EBITDA dizem pouco, porque o lucro vem da equivalência patrimonial. Mostrar com o aviso "holding: lucro vem principalmente das participações".

### 4.7 FIIs

| Indicador | Fórmula e fonte |
|---|---|
| **DY 12 meses** | Σ rendimentos por cota com **data base (data com)** nos últimos 365 dias ÷ fechamento atual (COTAHIST, `CODBDI` 12). Rendimentos do Fundos.NET estruturado ou da fila manual. Amortização **não** entra no DY e aparece à parte. |
| **P/VP** | Fechamento ÷ `Valor_Patrimonial_Cotas` do último informe mensal (com a data de referência na página, normalmente 1 a 2 meses atrás). Conferência: `Patrimonio_Liquido ÷ Cotas_Emitidas`. |
| **Vacância física** | Do **informe trimestral**, arquivo de imóveis (**conferir** o nome e o campo `Percentual_Vacancia`). Média ponderada pela área: Σ(área × vacância) ÷ Σ área, só para imóveis de renda (tijolo). Para fundos de papel, "não se aplica". A defasagem é de até cerca de 2 meses depois do trimestre, e a página diz isso. A vacância **financeira** não está no informe estruturado (**conferir**), então não é mostrada. |
| **Número de cotistas** | `Total_Numero_Cotistas` do informe mensal (complemento). Gráfico com a evolução mensal. |
| **Inadimplência** | Mesmo arquivo da vacância, ponderada pela participação na receita. Indicador opcional. |

---

## 5. Páginas

**Visual:** simples, com as fontes do plugin (Archivo e IBM Plex Sans) e as cores do site. Cabeçalho com o logo e o menu principal apontando para o WordPress. Largura de leitura de 760 px, com tabelas que rolam de lado no celular.

**Gráficos:**

- Pequenos (lucro trimestral, proventos, cotistas): **SVG gerado no build**, sem JavaScript. São leves e aparecem já no HTML.
- Preço com zoom: **uPlot** (cerca de 45 KB), servido do próprio site ou do cdnjs, carregado só quando o gráfico entra na tela.

**Regras gerais para anúncios:**

- No máximo 3 blocos manuais por página.
- Altura reservada no CSS, para a página não "pular" (CLS).
- **Nunca** dentro ou colado em ferramenta, formulário, tabela ou botão, para evitar clique acidental, que é proibido pela política do AdSense.
- Sem anúncio fixo cobrindo gráfico no celular.
- Anúncios automáticos desligados nessas páginas, para manter o controle de posição.

### 5.1 Página de ação: `/acoes/petr4/`

1. **Breadcrumb:** Início › Ações › Petrobras (PETR4).
2. **H1:** "PETR4: indicadores, dividendos e resultados da Petrobras".
3. **Cartão-resumo:** fechamento e data do pregão, variação em 12 meses, P/L, P/VP, DY 12m, ROE e valor de mercado. Cada número tem uma nota curta com a fonte e a data (ex.: "B3, pregão de 01/10/2026" ou "CVM, ITR 2T26, entregue em 07/08/2026").
4. **Resumo em texto gerado** (ver 6.4): de 3 a 6 frases que só existem se houver dado.
5. **[Anúncio 1]**
6. **Gráfico de preço** (5 anos, nominal e com ajuste de desdobramentos).
7. **Resultados:** gráfico de barras com receita e lucro por trimestre (últimos 12 trimestres) e uma tabela anual de 5 anos (receita, EBITDA calculado, lucro, margens).
8. **Endividamento:** dívida bruta, caixa, dívida líquida e dívida líquida/EBITDA ao longo de 8 trimestres. Para bancos, o bloco é trocado por uma frase que explica a ausência.
9. **Proventos:** tabela dos últimos 24 meses (tipo, valor bruto, data com, data ex, pagamento, link para o documento da CVM) e um gráfico de barras anual.
10. **[Anúncio 2]**
11. **Ferramenta `preco-justo`**, com o preço, o DPA dos últimos 12 meses, o LPA e o VPA já preenchidos (ver 5.6). Texto: "conta matemática com os dados acima; não é preço-alvo nem recomendação".
12. **Ações parecidas:** de 4 a 6 empresas do mesmo setor CVM, com links. Não é ranking, é só navegação.
13. **Análises do canal:** links para os posts do Denis sobre o ticker (encontrados pelo slug ou pela tag; hoje são 26 tickers com posts).
14. **Metodologia e fontes:** fórmulas resumidas, com link para a página `/acoes/metodologia/`.
15. **Aviso:** "Não é recomendação…" (ver seção 7).
16. **[Anúncio 3]**, antes do rodapé.

### 5.2 Página de FII: `/fiis/hglg11/`

1. Breadcrumb e **H1:** "HGLG11: dividendos, P/VP e vacância do fundo".
2. **Cartão:** fechamento, DY 12m, P/VP, último rendimento (valor e data com), cotistas, PL, segmento e mandato (informe mensal).
3. **Resumo em texto gerado.**
4. **[Anúncio 1]**
5. **Rendimentos:** barras mensais de 24 meses e uma tabela com o documento de origem.
6. **Gráfico:** cotação × VP por cota (mensal).
7. **Imóveis e vacância** (só tijolo): vacância ponderada por trimestre e a tabela de imóveis do último informe (nome, área, vacância).
8. **Cotistas:** linha mensal.
9. **[Anúncio 2]**
10. **Ferramenta `renda-fii`**, já preenchida com o rendimento mensal médio dos últimos 12 meses em % da cotação (`f-dy`). Abaixo, um link para o comparador de renda fixa (`/calculadora-renda-fixa/`), com o CDI do BCB citado no texto.
11. FIIs do mesmo segmento, posts do canal, metodologia, aviso, **[Anúncio 3]**.

### 5.3 Comparador: `/comparar/`

- **Página única e indexável:** `/comparar/acoes/`. O leitor escolhe de 2 a 4 tickers, e o JavaScript monta a tabela a partir de um JSON pequeno com os indicadores de todos. As URLs com parâmetro (`?a=petr4&b=prio3`) levam `canonical` para `/comparar/acoes/` e não entram no sitemap.
- **Pares estáticos indexáveis:** só os que têm busca real e post do canal (ex.: `/comparar/itsa4-vs-itub4/`, `/comparar/petr3-vs-petr4/`, ligados aos posts que já existem). No começo, no máximo 20. **Nada de gerar todas as combinações**: seriam milhares de páginas rasas.
- **Blocos:** tabela lado a lado, um gráfico de preço normalizado (base 100), um gráfico de DY anual e um texto gerado com as diferenças objetivas ("A tem margem maior; B tem dívida/EBITDA menor"), sem dizer qual é "melhor".
- **Anúncios:** 2, um depois da tabela e outro no fim.
- **Ferramentas:** só links (`preco-justo`).

### 5.4 Ranking: `/acoes/ranking/maiores-dividend-yield/` e outros

- **Rankings:** maiores DY, menores P/VP, maiores ROE, maiores valores de mercado; para FIIs, maiores DY, mais cotistas e menor vacância.
- **Títulos descritivos:** "Ações com maior dividend yield em 12 meses". Nunca "melhores ações".
- **Filtros fixos e declarados no topo:** liquidez mínima (volume médio diário em 3 meses ≥ R$ 1 milhão), lucro positivo e dado com menos de 6 meses. Os filtros evitam DY distorcido por preço ou por provento extraordinário. Uma coluna "por que o número pode enganar" marca os casos de **provento extraordinário** ou **lucro não recorrente**.
- **Blocos:** texto de 2 a 3 parágrafos explicando o indicador (com link para o verbete do glossário, ex.: `/dividendos-o-que-sao-dividend-yield/`), a tabela com os 30 primeiros e a data de corte.
- **Anúncios:** um antes da tabela e um depois. Nunca no meio da tabela.
- **Ferramentas:** `renda-fii` no ranking de FIIs, sem preenchimento; `preco-justo` como link no de ações.

### 5.5 Calendário de dividendos: `/dividendos/calendario/` e `/dividendos/2026/10/`

- **Fonte:** só proventos `aprovado`, com link para o documento.
- **Página mensal:** tabela com data com, data ex, pagamento, ticker, tipo e valor, filtrável por ação ou FII. Inclui um resumo em texto ("Em outubro de 2026, 14 empresas da cobertura têm pagamento previsto…").
- **Cuidado com canibalização:** o Denis já tem posts como `/calendario-dividendos-julho-2026-logg3-vale-a-pena/`. Proposta: o calendário vira a página de dados, e os posts mensais passam a linkar para ele (ou o contrário). Combinar com o Denis qual URL fica com a busca "calendário de dividendos outubro 2026".
- **Anúncios:** 2, antes e depois da tabela.
- **Ferramentas:** `renda-fii` (FIIs) como link.

### 5.6 Mudança no plugin (versão 1.3.0, pequena)

1. **Preenchimento por atributo:** `[iec_ferramenta id="preco-justo" preco="38.12" dpa="4.10" lpa="5.30" vpa="31.20" fonte="CVM ITR 2T26; B3 01/10/2026"]`.
   - O shortcode grava os valores como `data-*` no contêiner.
   - O `app.js` lê `RAIZ.dataset` na inicialização e sobrescreve os `value` padrão.
   - O gerador estático escreve os mesmos `data-*` no HTML.
2. **`modo="compacto"`:** esconde as seções "Como funcionam…" e "Premissas", trocando-as por um link para a página da ferramenta. Isso evita repetir o mesmo texto em centenas de páginas, o que conta como conteúdo duplicado.
3. **Continua valendo:** uma ferramenta de cada tipo por página.

O gerador lê `wordpress-plugin/iec-ferramentas/ferramentas/<id>/` como fonte única (submódulo Git ou cópia no build), então uma correção no plugin vale para os dois lados.

---

## 6. SEO

### 6.1 URLs

| Tipo | URL |
|---|---|
| Ação | `/acoes/{ticker}/` (minúsculas) — um por ticker negociado. PETR3 e PETR4 são páginas separadas, com bloco "outras classes" e canonical **própria** (o conteúdo de preço e DY é diferente). Units têm página própria. |
| FII | `/fiis/{ticker}/` |
| Hubs | `/acoes/` (lista por setor), `/fiis/` (lista por segmento), `/acoes/setor/{setor}/` |
| Ranking | `/acoes/ranking/{criterio}/`, `/fiis/ranking/{criterio}/` |
| Comparador | `/comparar/acoes/`, `/comparar/{a}-vs-{b}/` |
| Calendário | `/dividendos/calendario/`, `/dividendos/{aaaa}/{mm}/` |
| Metodologia | `/acoes/metodologia/`, `/fiis/metodologia/` |

**Conferir antes:** se o WordPress já usa `/acoes/` ou `/fiis/`. A categoria hoje é `/category/acoes/`, então não há conflito aparente.

### 6.2 Títulos e descrição

- **Ação:** `PETR4: dividendos, P/L e resultados da Petrobras` (até 60 caracteres), mais o sufixo " | Investir e Coçar".
- **FII:** `HGLG11: dividendos, P/VP e vacância`.
- **Meta description gerada com números**, sem adjetivos: "DY de 9,8% em 12 meses, P/L 4,1 e lucro de R$ 98 bi até jun/26. Dados da CVM e da B3, atualizados em 02/10/2026."

### 6.3 Dados estruturados

- **Ações e FIIs:** um único bloco JSON-LD por página, com `WebPage` (`name`, `dateModified`, `isPartOf` = `WebSite`, `publisher` = `Organization` do site, `about` = `Corporation` com `name`, `tickerSymbol`, `legalName` e `identifier` = CNPJ) e `BreadcrumbList`.
- **Rich result:** só o **breadcrumb** tem. Não existe rich result de ação no Google, então não vamos prometer.
- **`Dataset`** (com `license`, `creator` = CVM e B3, `temporalCoverage`) é opcional e só serve ao Google Dataset Search. Proposta: usar só em `/acoes/metodologia/`.
- **Não usar:**
  - `FAQPage`: desde 2023, o Google só mostra FAQ para sites de governo e saúde, e o site já tem FAQ duplicado.
  - `Review` ou `Rating`.
  - `Product` ou `FinancialProduct` com preço, que daria a impressão de oferta.
  - `NewsArticle`.

### 6.4 Conteúdo único por página (texto gerado sem enrolação)

A regra é cada frase existir só se o dado existir e disser algo. Exemplos de regras:

- **Lucro:** "Nos 12 meses até 30/06/2026, a {empresa} lucrou R$ {x} ({±y}% contra os 12 meses anteriores)." Sai se faltar um dos dois períodos.
- **Margem:** "A margem líquida foi de {m}%, {acima/abaixo} da média de 5 anos ({m5}%)." Só com 5 anos de dados.
- **Dívida:** "A dívida líquida é {d}× o EBITDA calculado." Some para bancos.
- **Proventos:** "Nos últimos 12 meses, foram {n} pagamentos, somando R$ {s} por ação; {k}% em JCP."
- **FII:** "A vacância ponderada pela área era de {v}% no trimestre encerrado em {data}, contra {v0}% um ano antes."
- **Proibido:** frases genéricas ("é uma empresa sólida"), adjetivos de valor ("barata", "oportunidade") e qualquer verbo de ação ("compre", "venda", "aproveite").
- **Contexto humano:** o bloco "Análises do canal" traz o que o Denis já escreveu sobre o ativo, e é o que diferencia essas páginas de um agregador.

### 6.5 Links internos

- **Página do ativo** linka para: o hub do setor, de 4 a 6 ativos do mesmo setor, os posts do canal, os verbetes do glossário (`/o-que-e-pl-acoes/`, `/o-que-e-pvp-acoes/`, `/o-que-e-roe/`, `/dividendos-o-que-sao-dividend-yield/`) e a ferramenta usada.
- **Posts do WordPress** passam a linkar para a página do ativo, por exemplo `/ambev-abev3-resultado-1t26-vale-a-pena-investir/` → `/acoes/abev3/`. O pipeline gera um CSV de sugestões no mesmo formato de `seo/sugestoes-links.csv`.
- **Hub `/cotacoes/` atual:** recebe 301 para `/acoes/`, ou vira uma página que linka só para as páginas novas que já estiverem prontas.

### 6.6 Como substituir as 143 páginas `cotacao-*`

As 143 estão com `noindex`, sem canonical, fora do sitemap e com um link interno cada. Há pouca autoridade a preservar, então a solução mais limpa é uma **URL nova com 301**.

| Caso | Ação |
|---|---|
| Ticker já coberto pelo site novo | **301** de `/cotacao-{t}/` para `/acoes/{t}/` (Yoast Premium Redirects, plugin Redirection ou `.htaccess`). Despublicar o post antigo. |
| Ticker válido ainda não coberto | Manter como está (`noindex`) até a página nova existir. Depois, 301. |
| 10 tickers quebrados (`b8in8l` e outros) | Despublicar e responder **410**, ou 301 para `/acoes/`. Não há o que preservar. |
| Hub `/cotacoes/` e `/category/cotacoes/` | 301 para `/acoes/` quando houver pelo menos 20 páginas novas. |

**Por que não reaproveitar a URL `/cotacao-petr4/`:**

- Ela é um post do WordPress. Reaproveitar exige servir arquivo estático no lugar de um post, o que é frágil.
- O nome "cotação" não descreve uma página de indicadores e dividendos.
- Uma única regra no `.htaccess` resolve todas: `RedirectMatch 301 ^/cotacao-([a-z0-9]+)/?$ /acoes/$1/`. Ela só pode ser ligada quando todos os tickers estiverem cobertos; antes disso, é preciso uma lista explícita.

### 6.7 Sitemap, atualização e cuidados com conteúdo raso

- **Sitemap:** `sitemap-ativos.xml` gerado pelo pipeline e declarado no `robots.txt` (e enviado no Search Console). O `lastmod` muda **só** quando muda um dado contábil, um provento ou um informe, **não** com o preço diário. Mudar a data todo dia sem conteúdo novo é sinal falso de atualização.
- **Indexação condicionada:** a página só entra com `index` se tiver pelo menos 8 trimestres de DRE (ou 12 informes, no caso de FII), proventos dos últimos 12 meses revisados e todos os testes bloqueantes aprovados. Se não tiver, fica `noindex, follow` e fora do sitemap.
- **Ritmo:** começar com as 20 do MVP. Depois, cerca de 30 por mês, acompanhando no Search Console a cobertura ("Rastreada, mas não indexada") e o CTR. Se a taxa de páginas não indexadas passar de 30%, parar e melhorar o conteúdo antes de criar mais. O Google trata a criação de páginas em massa com pouco valor como "abuso de conteúdo em escala" (política de março de 2024).
- **Canonical:** cada página aponta para si mesma. Parâmetros de filtro levam canonical para a página limpa.

---

## 7. Regras de conteúdo

1. **Sem recomendação.** Nada de "compre", "venda", "vale a pena", "barata", "cara", "oportunidade", "preço-alvo" ou "melhor ação". Um teste automático procura essas palavras em todo HTML gerado e bloqueia a publicação.
2. **Sem citar corretora:** nem nome, nem link, nem "abra conta". Atenção: alguns emissores também são tickers (ex.: o Inter); nesse caso, aparecem só como emissor.
3. **Fonte e data em cada número:** na nota do cartão e no rodapé de cada tabela e gráfico. Exemplos: "Fonte: CVM, DFP 2025 consolidada, versão 2, entregue em 27/02/2026" e "Fonte: B3, COTAHIST, pregão de 01/10/2026".
4. **Aviso fixo** (no topo, curto, e no rodapé, completo): *"Esta página reúne dados públicos da CVM, da B3 e do Banco Central, calculados automaticamente. Não é recomendação de compra ou venda, nem análise de valores mobiliários. Os números podem ter atraso ou erro: confira nos documentos oficiais, linkados em cada tabela, antes de decidir."*
5. **Ferramenta `preco-justo` preenchida:** a página diz que é uma conta matemática e que a taxa mínima (`g-taxa`) é escolha de quem usa. A Resolução CVM 20/2021 regula a atividade de **analista de valores mobiliários**. Vale o Denis confirmar com advogado se preencher automaticamente Bazin e Graham por ticker pode ser lido como análise. Alternativa mais segura: preencher só os dados (preço, DPA, LPA, VPA) e deixar o resultado aparecer só depois de um clique em "Calcular".
6. **Erros:** um link "Achou um número errado?" (e-mail) e um registro público de correções na página de metodologia.

---

## 8. MVP e plano de testes

### 8.1 Escolha dos 20 ativos (critério objetivo, **não é recomendação**)

**Ações (10):**

- Maior **volume financeiro médio diário nos últimos 12 meses** (COTAHIST `VOLTOT`, `CODBDI` 02, `TPMERC` 010).
- Um ticker por empresa (o mais negociado).
- Só entre os 133 tickers válidos que já têm `cotacao-*`, para que cada página nova substitua uma antiga com 301.
- A lista sai do script. Pelo histórico, deve incluir nomes como PETR4, VALE3, ITUB4 e BBAS3, mas isso está por **conferir** quando o download funcionar.
- Se o top 10 não tiver nenhuma **unit**, a unit mais negociada entra **só nos testes**, não no MVP publicado, para exercitar o caso.

**FIIs (10):**

- Maior volume financeiro médio diário em 12 meses (`CODBDI` 12).
- Pelo menos 24 meses de negociação e informe mensal entregue nos últimos 2 meses.
- Também sai do script.

**Na página da lista**, dizer: "Os primeiros ativos foram escolhidos pelo volume negociado na B3 nos últimos 12 meses. A escolha não é recomendação."

### 8.2 Testes (rodam a cada execução; "bloqueante" impede publicar o ativo)

| # | Teste | Tolerância | Tipo |
|---|---|---|---|
| 1 | Ativo total (BPA `1`) = Passivo + PL (BPP `2`) | Diferença ≤ R$ 1 mil | Bloqueante |
| 2 | `3.11` = `3.11.01` + `3.11.02` | ≤ 0,1% | Bloqueante |
| 3 | TTM calculado no 4º trimestre = valor anual da DFP (receita, EBIT, lucro) | ≤ R$ 1 mil | Bloqueante |
| 4 | 4º trimestre derivado (DFP − 9 meses) com o mesmo sinal da tendência, e nunca ±1000× o trimestre anterior | Regra de escala | Bloqueante |
| 5 | LPA calculado (lucro da controladora ÷ ações ex-tesouraria) × LPA básico divulgado (`3.99.01.0x`) | ≤ 3% (a média ponderada difere da posição final) | Alerta |
| 6 | Ações em circulação × FRE (capital social) | ≤ 1% | Alerta |
| 7 | EBITDA calculado × EBITDA (CVM 156) divulgado na nota ou no release da empresa, conferido à mão para as 10 do MVP | ≤ 5%. Diferença maior precisa de explicação escrita | Manual, uma vez por trimestre |
| 8 | Proventos aprovados × soma anual do FRE 3.5 e da DFC (dividendos + JCP pagos) | ≤ 5% (diferença de competência é normal) | Alerta |
| 9 | Preço: nenhum dia útil sem negociação para o ticker (calendário B3) e variação diária acima de 30% só com evento conhecido | Exato | Alerta |
| 10 | FII: `Patrimonio_Liquido ÷ Cotas_Emitidas` × `Valor_Patrimonial_Cotas` | ≤ 0,5% | Bloqueante |
| 11 | FII: rendimento por cota (Fundos.NET ou fila) × aviso aos cotistas ou relatório gerencial, conferido à mão para os 10 | Exato até R$ 0,0001 | Manual |
| 12 | FII: DY 12m calculado × soma dos `Percentual_Dividend_Yield_Mes` (convertido para a mesma base) | Só sinaliza divergência acima de 1 p.p. | Alerta |
| 13 | Toda célula de número no HTML tem `data-fonte` e `data-ref` preenchidos | 100% | Bloqueante |
| 14 | Palavras proibidas e nomes de corretoras no HTML | Zero | Bloqueante |
| 15 | HTML válido, um H1, title ≤ 60, um JSON-LD, canonical | 100% | Bloqueante |

Para os 20 do MVP, antes de publicar, o Denis (ou eu) preenche uma **planilha de referência** com os números das próprias demonstrações. Para 3 empresas (uma comum, um banco e uma unit), os números ficam fixados como teste automático, com o PDF da DFP como fonte.

---

## 9. Nome do repositório

| Nome | Comentário |
|---|---|
| **`iec-ativos`** | Curto, segue o padrão `iec-ferramentas` e cobre ações e FIIs. **Recomendado.** |
| `iec-dados` | Genérico demais: pode ser confundido com dados do blog. |
| `iec-fundamentos` | Bom para ações, mas não descreve bem os FIIs. |

O Denis cria o repositório (privado). Estrutura sugerida: `pipeline/` (baixar, normalizar, calcular), `templates/`, `testes/`, `dados/referencia/` (planilha e PDFs de conferência), `.github/workflows/diario.yml` e o plugin como submódulo ou cópia em `vendor/iec-ferramentas/`.

---

## 10. Riscos, custos e liberação de rede

### Riscos

| Risco | Tamanho | Como reduzir |
|---|---|---|
| **Termos da B3 para dados de fim de dia** | Médio | A Política Comercial de Market Data da B3 diz, em resumo, que dados de fim de dia podem ser redistribuídos sem custo e sem autorização prévia. A versão mais recente (2024) e se "site com anúncios" é uso permitido estão por **conferir**: o Denis lê o PDF e, na dúvida, pergunta à B3. Não usar dado intradiário nem com atraso de 15 minutos. |
| **Proventos sem fonte aberta estruturada** | Alto | Fila semiautomática a partir da CVM, com aprovação humana. DY de caixa enquanto isso. Nunca automatizar a página de proventos da B3. |
| **Google ver as páginas como conteúdo em escala** | Alto | Indexação condicionada, ritmo gradual, texto vindo dos números, bloco "Análises do canal" e, no começo, só ativos com dados completos. |
| **AdSense** com "conteúdo de pouco valor" | Médio | Mesmos cuidados, no máximo 3 blocos, nada perto de ferramenta. |
| **Erro de dado da CVM** (escala, reapresentação, conta fora do padrão) | Médio | Testes bloqueantes. A página mantém a versão anterior. Registro de correções. |
| **Mudança de leiaute da CVM** (FII depois da Resolução 175) | Médio | Leitor por cabeçalho, testes de colunas e alerta por e-mail (falha do Actions). |
| **Regulatório** (Resolução CVM 20, analista) | Baixo a médio | Sem recomendação, aviso fixo e decisão consciente sobre preencher o `preco-justo` (seção 7.5). |
| **Bloqueio de IP do GitHub pela CVM ou pela B3** | Baixo (conferir) | Plano B: Mac com `launchd`. |
| **Hospedagem não aceitar envio automático** | Baixo a médio | Plano B: subdomínio no Cloudflare Pages. |

### Custos

| Item | Custo |
|---|---|
| Dados (CVM, B3 fim de dia, BCB) | R$ 0 |
| GitHub Actions (privado, cerca de 300 min por mês) | R$ 0 (dentro da cota gratuita) |
| Hospedagem | A atual (subpasta) ou Cloudflare Pages grátis (subdomínio) |
| Tempo do Denis | Cerca de 30 min por semana para aprovar proventos e conferir alertas. Depois, cerca de 2 h por trimestre na temporada de resultados (teste 7) |

### Hosts para liberar nesta nuvem (desenvolvimento)

Hoje estão bloqueados aqui, exceto `api.bcb.gov.br`, que responde por curl/Python (só o WebFetch falhou). Os outros, testei e a conexão foi recusada pelo proxy.

| Host | Para quê | Necessário? |
|---|---|---|
| `dados.cvm.gov.br` | DFP, ITR, FCA, FRE, IPE, cadastro e informes de FII | **Sim** |
| `bvmf.bmfbovespa.com.br` | COTAHIST anual e diário | **Sim** |
| `api.bcb.gov.br` | SGS (CDI, Selic, IPCA) | **Sim** (já liberado: testado em 02/10 com curl) |
| `www.rad.cvm.gov.br` | PDFs de "Aviso aos Acionistas" (links do IPE) | Sim, para proventos de ações |
| `fnet.bmfbovespa.com.br` | Documentos estruturados de rendimentos de FII | Sim, se a fonte for aprovada (2.2) |
| `www.b3.com.br` | Layout do COTAHIST, política de market data e classificação setorial (documentação) | Recomendado |
| `sistemaswebb3-listados.b3.com.br` | Proventos da B3 | **Não**: só conferência manual no navegador do Denis |

No **GitHub Actions** e no **Mac**, a rede é aberta, então não é preciso liberar nada lá. Para publicar, o Actions precisa alcançar o host SFTP da hospedagem (ou a API do Cloudflare).

---

## Decisões que o Denis precisa tomar

1. **Onde publicar:** subpasta `/acoes/` e `/fiis/` no domínio principal (precisa de acesso SFTP ou SSH da hospedagem e confirmação de que pasta real tem prioridade sobre o WordPress) ou subdomínio `dados.` (Cloudflare Pages). Qual é a hospedagem, e o DNS passa pelo Cloudflare?
2. **Onde roda:** GitHub Actions (recomendado) ou Mac com `launchd`.
3. **Proventos:** topa aprovar a fila semanal de avisos (cerca de 30 min por semana)? E usar o Fundos.NET para os FIIs depois de ler os termos?
4. **Termos da B3:** ler a Política Comercial de Market Data (versão atual) e, se houver dúvida sobre o uso em site com AdSense, consultar a B3.
5. **`preco-justo` preenchido por ticker:** preencher automaticamente ou só sob clique? Consultar advogado sobre a Resolução CVM 20?
6. **Calendário de dividendos:** a página de dados substitui os posts mensais (`/calendario-dividendos-julho-2026-…`) ou convive com eles, com links?
7. **`cotacao-*`:** confirmar o 301 para `/acoes/{ticker}/` à medida que as páginas ficam prontas e 410 para os 10 tickers quebrados. Exportar o Search Console das `cotacao-*` antes, para confirmar que o tráfego é perto de zero.
8. **Plugin 1.3.0:** aprovar os atributos de preenchimento e o `modo="compacto"`.
9. **Nome do repositório:** `iec-ativos` (recomendado).
