# Diagnóstico de SEO: investirecocaresocomecar.com.br

Varredura só de leitura feita em 02/10/2026, sem login, com uma requisição por segundo. Foram lidas as **368 URLs dos sitemaps**, mais 5 páginas `cotacao-*` de amostra. Todas responderam 200, sem nenhum 403 nem 429. Os dados por URL estão em [`varredura.csv`](varredura.csv), e o script, em [`varredura.py`](varredura.py).

Escopo: investimentos (FIIs, ações, renda fixa). Dívida, cartão e finanças pessoais ficaram de fora.

## Os 5 problemas de maior impacto

| # | Problema | Páginas | Correção | Quem faz |
|---|---|---|---|---|
| 1 | Schema duplicado: 2 a 5 blocos JSON-LD por página, vindos de 3 fontes | 324 com artigo duplicado, 124 com FAQPage duplicado | Deixar uma fonte só de schema (detalhe abaixo) | Painel (Mac) |
| 2 | Posts órfãos: nenhum link interno no conteúdo apontando para eles | 256 de 368 (70%) | Links contextuais a partir dos posts de glossário e das ferramentas | Conteúdo (Mac). Eu posso gerar a lista de sugestões |
| 3 | Conteúdo duplicado e raso | 3 pares idênticos e 34 páginas com menos de 400 palavras | Redirecionar os duplicados (301) e consolidar ou tirar do índice as páginas rasas | Painel (Mac) |
| 4 | Páginas sem H1 | 34, incluindo calculadoras e guias de FII | Corrigir o modelo dessas páginas para ter um H1 | Painel/tema (Mac) |
| 5 | Títulos longos e em série | 210 títulos com mais de 60 caracteres sem contar o sufixo; cerca de 20 verbetes com o mesmo modelo de título | Reescrever os títulos dos verbetes e encurtar os mais longos | Painel (Mac) |

## 1. Correções de 28/09: conferência

| Item | Situação |
|---|---|
| `robots.txt` | ✅ Não bloqueia mais `themes`, `plugins` nem `wp-includes`. Bloqueia login, xmlrpc, busca, feeds, `?p=` e `?tag=`. Aponta para o `sitemap_index.xml`. Observação: são três grupos `User-agent: *`. O Google junta os três, mas vale unificar num só. |
| `sitemap_index.xml` | ✅ 4 sitemaps, todos com status 200: posts (326), páginas (32), categorias (9) e autor (1). |
| `cotacao-*` no sitemap | ✅ Nenhuma. |
| `cotacao-*` com noindex | ✅ 143 páginas `cotacao-*` recebem links internos; nas 5 da amostra, todas estão com `noindex, follow`. |
| Página com noindex dentro do sitemap | ⚠️ `/carteira-recomendada-fundos-imobiliarios-agosto-2025/` está no sitemap, mas tem `noindex` e não tem canonical. Precisa sair do sitemap, ou perder o noindex. |
| Aviso "uploadDate sem fuso" | ✅ Nas 173 páginas com `VideoObject`, o `uploadDate` já vem com fuso (`+00:00`). O aviso do Search Console deve ser resíduo antigo: vale clicar em "Validar correção". |

## 2. Tabela por URL

Está em [`varredura.csv`](varredura.csv), com status, URL final, canonical, meta robots, title e tamanho, tamanho da meta description, quantidade de H1, palavras no conteúdo, links internos que a página recebe e envia, contagem de og/twitter/JSON-LD e indicadores de peso.

Resumo:

- **Canonical:** 367 de 368 têm exatamente um. A única exceção é a página de carteira de agosto citada acima.
- **Meta description:** 3 páginas sem (`/artigos/`, `/perfil-de-investidor/` e **`/simulador-ntnb/`**) e 2 com duas descriptions (`/vivt3-dividendos-conta-celular-gratis-para-sempre/` e `/imovel-bom-investimento-o-que-ninguem-te-conta/`). Outras 36 passam de 160 caracteres.
- **Duas tags `<title>`:** 20 páginas. A segunda fica dentro de uma `<div>` no corpo do post, provavelmente de um SVG ou de HTML colado. Não altera o título no Google, mas é sinal de HTML sujo no conteúdo.
- **og:image ausente:** 59 páginas, entre elas `/fii-papel-vs-tijolo/`. O compartilhamento fica sem imagem.
- **Slugs com emoji:** 2 (`/vale-a-pena-investir-em-cobre-📈-…` e `/🚀-tesla-tsla34-…`). Funcionam, mas viram `%F0%9F…` quando alguém compartilha o link. Se mudar, precisa de redirecionamento 301.

## 3. Yoast × WPSSO

**O que aparece hoje em todas as 368 páginas:**

- **Yoast:** gera canonical, meta robots, title, description, og:* e twitter:*, uma vez cada. O bloco de schema do Yoast (`yoast-schema-graph`) existe, mas está **vazio** (`"@graph":[]`). Alguém já desligou o schema do Yoast.
- **WPSSO:** gera o bloco `wpsso-schema-graph` (BlogPosting ou Article, BreadcrumbList, FAQPage, ItemList nas categorias, ImageObject em 3 proporções).
- **Blocos sem identificação**, depois do comentário de um snippet ("Snippet final de Proteção contra o Erro de Recuperação…", 398 blocos) e de JSON-LD colado dentro dos posts: `NewsArticle` (324 páginas), `FAQPage` (281), `Article` (55) e `VideoObject` (54).

**O que isso causa:** não há og nem canonical duplicados. A duplicidade está no **schema**. Uma página típica declara o mesmo post como `BlogPosting` (WPSSO) e `NewsArticle` (snippet), e 124 páginas têm **dois FAQPage**. Para o Google, FAQ duplicado é erro de dados estruturados, e dois tipos de artigo conflitantes diluem o sinal.

**Recomendação:** desligar o **WPSSO** e religar o schema do **Yoast**.

- O Yoast já faz todo o resto (sitemaps, canonical, meta, og) e é a licença paga.
- Ao religar o schema do Yoast (removendo o filtro ou a configuração que esvazia o `@graph`), voltam Article, WebPage, BreadcrumbList, Organization e Person num único grafo coerente.
- Depois, revisar o snippet "Proteção contra o Erro de Recuperação" e o JSON-LD colado nos posts, deixando **um único FAQPage** por página.

**O que se perde ao desligar o WPSSO** (conferir no painel antes):

1. O FAQPage que o WPSSO monta sozinho a partir do conteúdo, em 119 páginas. O Yoast só gera FAQ a partir do bloco "FAQ do Yoast". Onde o FAQ vier só do WPSSO, ele some, a menos que o snippet já cubra.
2. As 3 proporções de imagem no schema (1×1, 4×3, 16×9). O Yoast publica uma imagem principal.
3. O `ItemList` nas 9 páginas de categoria.
4. O `QuantitativeValue` dentro do BlogPosting em 112 páginas (provavelmente tempo de leitura ou contagem de palavras). Não gera resultado rico.
5. Qualquer configuração específica do WPSSO para redes sociais. As meta og hoje já vêm do Yoast, então o compartilhamento não deve mudar.

A alternativa, manter o WPSSO e deixar o Yoast sem schema, também funciona. Mas aí são dois plugins grandes para fazer o trabalho de um, e o snippet e o JSON-LD colado continuam duplicando.

## 4. Conteúdo raso, canibalização e órfãos

### Duplicados exatos (mesmo título)

| Manter | Redirecionar (301) |
|---|---|
| `/xp-corta-ibovespa-carteira-defensiva-vale-a-pena/` | `/xp-corta-ibovespa-carteira-defensiva-vale-a-pena-2/` |
| `/ipo-compass-pass3-vale-a-pena-investir/` | `/ipo-compass-pass3-vale-a-pena-investir-2/` |
| `/como-funciona-um-fundo-imobiliario/` | `/como-funciona-um-fundo-imobiliario-entenda-agora/` (as duas estão sem H1) |

Também: `/sobre/` e `/author/investirecocar/` têm o mesmo título. Vale diferenciar o da página de autor.

### Títulos em série

Cerca de 20 verbetes do glossário usam o mesmo modelo: *"O que é X? Definição, como funciona e exemplos práticos"* (LCI, LCA, CRI, CRA, CDB, Selic, IPCA, FII, IFIX, ETF, BDR, ROE, P/L, P/VP, JCP, Tesouro Selic, Tesouro IPCA+…). Não chega a ser canibalização, porque os temas são diferentes, mas o título igual não destaca nenhum na busca. Sugestão: começar pela dúvida real, por exemplo *"LCI: rende mais que CDB? Como funciona a isenção de IR"*.

`/calculadora-lci/` e `/calculadora-lca/` são quase a mesma página. Fundir numa só ("Calculadora LCI e LCA × CDB") e redirecionar a outra.

### Menos de 400 palavras (sem contar categorias e autor)

34 páginas. Os grupos principais:

- **Carteiras e relatórios antigos com 20 a 79 palavras** (provavelmente formulário de captura ou link para PDF): `/carteira-cripto/`, `/carteira-cripto-maio-2025/`, `/carteira-small-caps-maio-2025/`, `/carteira-bdr-agosto-2025/`, `/carteira-recomendada-bdr-julho-2025/`, `/carteira-5-fundos-imobiliarios/`, `/carteira-dividendos-novembro-2025/`, `/carteira-recomendada-fundos-imobiliarios-agosto-2025/`, `/panorama-fundos-imobiliarios-2025/`, `/onde-investir-em-2025/`, `/onde-investir-segundo-semestre-2025/`, `/dividendos-para-tempos-dificeis/`, `/a-nova-velha-criptomoeda-do-momento/`, `/relatorio-caixa-seguridade-cxse3/`, `/resultado-2t25-banco-do-brasil/`, `/nubank-2t25-e-muitas-recomendacoes/`, `/dividendos-extraordinarios-antes-das-mudancas-na-tributacao/`, `/e-book-analise-fundamentalista/` e `/planilha-previdenciaria/`. **Sugestão:** `noindex, follow` e retirar do sitemap. São páginas de captação, não de busca.
- **Perfis de investidor** (4 a 73 palavras, sem H1): `/perfil-de-investidor/`, `-conservador/`, `-moderado/` e `-agressivo/`. **Sugestão:** juntar num único guia com um quiz (ver oportunidades).
- **Posts curtos de verdade:** `/wege3-oportunidade-ou-cilada-da-decada/` (4 palavras: conteúdo provavelmente quebrado, vale abrir), `/mapa-de-calor-do-ibovespa/` (10), `/etfs-dividendos-mensais-b3-2026/` (300), `/o-aviso-mais-importante-para-quem-investe-em-fiis-nao-ignore/` (349), `/irbr3-em-alta-…/` (366) e `/vale3-dividendos-prejuizo-…/` (393).
- **Institucionais** (normal serem curtas): termos, privacidade, `/links/` e `/llms-txt/`.

### Órfãos

**256 de 368 URLs não recebem nenhum link interno dentro do conteúdo** de outra página do sitemap. Os mais linkados são verbetes do glossário (Selic, Ibovespa, ação ON/PN), com 8 ou 9 links. Os posts de análise quase nunca são citados por outros posts. Isso explica boa parte da posição média de 13,3: o Google descobre as páginas pelo sitemap, mas não vê sinal de importância.

`/simulador-ntnb/` também não recebe nenhum link contextual. O ponto de partida óbvio é linkar a partir de `/o-que-e-tesouro-ipca/`, `/o-que-e-tesouro-direto/` e dos posts de renda fixa.

## 5. Velocidade básica (pelo HTML)

| Página | HTML | Scripts | CSS | Imagens | Imagens sem width/height | Arquivos do WP-Optimize |
|---|---|---|---|---|---|---|
| `/` | 113 KB | 4 | 7 | 11 | 0 | 3 |
| `/simulador-ntnb/` | 105 KB | 4 | 7 | 0 | 0 | 3 |
| `/7-acoes-com-vantagem-competitiva-…-moat/` | 177 KB | 7 | 9 | 6 | 1 | 3 |
| `/fii-papel-vs-tijolo/` | 140 KB | 7 | 9 | 5 | 0 | 3 |
| `/o-que-e-tesouro-ipca/` | 147 KB | 7 | 9 | 5 | 0 | 3 |

Média do site: HTML de 144 KB, 6,5 scripts, 8,9 CSS e 1 imagem sem dimensões por página. O WP-Optimize está servindo os arquivos minificados e agrupados (3 por página) em 343 das 368 URLs.

Não é o gargalo. O HTML está um pouco pesado por causa do JSON-LD repetido (item 3), que deve cair quando o schema for unificado. Esta varredura não mede tempo de carregamento real nem Core Web Vitals: para isso, use o PageSpeed Insights ou o relatório do Search Console.

## 6. Oportunidades: 10 páginas

| # | Página | Por quê | Ação |
|---|---|---|---|
| 1 | `/calculadora-lci/` + `/calculadora-lca/` | Quase duplicadas; busca forte ("LCI vale mais que CDB?") | **Ferramenta** no plugin: "LCI/LCA × CDB equivalente"; fundir e redirecionar |
| 2 | `/calculadora-juros-anual-para-mensal/` | Sem H1; busca utilitária constante | **Ferramenta** no plugin, com explicação curta |
| 3 | `/calculadora-renda-fixa/` | 182 palavras | **Ferramenta** (CDB/LCI/Tesouro com IR por prazo) e texto de apoio |
| 4 | `/quanto-rende-1-000-reais-em-um-fundo-imobiliario/` | Sem H1; a pergunta é exatamente o que o `renda-fii` responde | **Refresh** com o shortcode `renda-fii` embutido |
| 5 | `/como-funciona-um-fundo-imobiliario/` | Duplicado e sem H1 | **Refresh** e 301 do duplicado; virar o hub de FIIs |
| 6 | `/qual-e-o-melhor-fundo-imobiliario-para-investir-hoje/` | Sem H1; busca de alto volume | **Refresh** com critérios (P/VP, DY, vacância) e link para o `renda-fii` |
| 7 | `/o-que-e-tesouro-ipca/` | Bem linkado; tema do simulador | **Refresh** levando para o `/simulador-ntnb/` |
| 8 | `/perfil-de-investidor/` (+ 3 variações) | 4 páginas rasas e sem H1 | **Ferramenta**: quiz de perfil, numa página só |
| 9 | `/qual-o-preco-justo-da-itsa4-analise-completa-hoje/` + `/itsa3-ou-itsa4-…/` + `/quem-a-itausa-controla-…/` | Cluster Itaúsa sem H1 | **Ferramenta**: preço justo (Bazin/Graham) e links entre as três |
| 10 | `/mapa-de-calor-do-ibovespa/` | 10 palavras e sem H1 | Explicar como ler o mapa e linkar; ou `noindex` se for só embed |

As ferramentas novas entram no padrão do plugin `iec-ferramentas` (uma pasta por ferramenta e shortcode).

## Limitações

- Só HTML público. Sem acesso ao Search Console nem ao painel, os números de cliques e de indexação são os informados em 28/09.
- "Links recebidos" conta só links dentro do conteúdo das páginas do sitemap. Menu, rodapé e barra lateral ficam de fora de propósito, porque não indicam relevância editorial.
- A recomendação Yoast × WPSSO parte do HTML. As configurações internas dos plugins precisam ser conferidas no painel antes de desligar qualquer coisa.

## 7. Entregas feitas a partir deste diagnóstico

### Sugestões de links internos

O arquivo [`sugestoes-links.csv`](sugestoes-links.csv) foi gerado por [`sugerir_links.py`](sugerir_links.py), a partir do HTML já baixado, sem nenhuma requisição nova.

- **Tipo `orfao`:** 212 páginas órfãs com até 3 páginas de origem cada (670 linhas no total, contando as de ferramenta). A origem é a página com texto mais parecido (TF-IDF) que ainda não linka para o destino. A coluna `ancora_sugerida` traz o início do título do destino; ajuste o texto para caber na frase.
- **Tipo `ferramenta`:** até 8 páginas de origem para cada ferramenta (simulador NTN-B, renda com FIIs, LCI/LCA × CDB, juros, comparador de renda fixa, perfil e preço justo), escolhidas pelo tema da URL.
- Ficam de fora: páginas com noindex, institucionais, categorias, autor, páginas com menos de 400 palavras e os duplicados que vão receber 301.
- Para cada linha: abrir a página de **origem**, achar o trecho que fala do assunto e linkar para o **destino**. Comece pelas linhas com maior `similaridade`.

### Novas ferramentas no plugin (versão 1.2.0)

| Shortcode | Ferramenta | Página sugerida |
|---|---|---|
| `[iec_ferramenta id="lci-lca-cdb"]` | Calculadora LCI e LCA × CDB | `/calculadora-lci/`, com a `/calculadora-lca/` redirecionada para ela |
| `[iec_ferramenta id="juros-anual-mensal"]` | Conversor de juros anual, mensal e diário | `/calculadora-juros-anual-para-mensal/` |
| `[iec_ferramenta id="renda-fixa-comparador"]` | Comparador de renda fixa | `/calculadora-renda-fixa/` |
| `[iec_ferramenta id="perfil-investidor"]` | Quiz de perfil de investidor | `/perfil-de-investidor/`, com as 3 variações redirecionadas para ela |
| `[iec_ferramenta id="preco-justo"]` | Preço justo (Bazin e Graham) | Página nova, linkada a partir do cluster Itaúsa |

Cada ferramenta já vem com H1 de seção, texto explicativo, premissas e links internos para os verbetes do glossário (todos conferidos contra o sitemap).
