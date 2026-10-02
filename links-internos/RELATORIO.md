# Links internos em lotes

Feito em 02/10/2026, só leitura no site. Aqui ficam os **patches**. Quem aplica é o Mac, com o `auditoria-fatos/aplicar_patches.py`, que ganhou a opção `--pasta`.

## Números

| Lote | O que liga | Posts (patches) | Links novos |
|---|---|---|---|
| **L1** | as 11 ferramentas do plugin `iec-ferramentas` 1.3.0 | 61 | 80 |
| **L2** | os 6 guias corrigidos ou reescritos (4873, 4874, 5091, 1053, 993, 4537) | 33 | 40 |
| **L3** | órfãos restantes do `seo/sugestoes-links.csv`, pelo ticker do título | 22 | 26 |
| **Total** | | **116** | **146** |

Cada post entra em um lote só, e cada lote tem um patch por post. Dos 116 posts, 89 ganham 1 link, 24 ganham 2 e 3 ganham 3. Nenhum post passa de 3.

O detalhe de cada link está em [`resumo.csv`](resumo.csv): lote, origem, destino, âncora, `de`, `para` e se o destino era órfão.

## Onde as ferramentas estão publicadas

Nenhum post em cache tem o shortcode `[iec_ferramenta]`. As ferramentas estão em páginas. Baixei as 52 páginas publicadas pela API pública (`/wp-json/wp/v2/pages`, uma requisição), e o shortcode aparece no rendered como `<div id="..." class="iec-ferramenta">`. **As 11 já estão publicadas**, inclusive as 4 da 1.3.0 (páginas 19541 a 19547), então nenhuma ficou de fora.

| Ferramenta | Página |
|---|---|
| simulador-ntnb | `/simulador-ntnb/` (19488) |
| renda-fii | `/simulador-renda-fii/` (19496) |
| lci-lca-cdb | `/calculadora-lci-lca-cdb/` (19502) |
| juros-anual-mensal | `/calculadora-juros-anual-para-mensal/` (19504) |
| renda-fixa-comparador | `/calculadora-cdb-lci-prefixado-ipca/` (19506) |
| perfil-investidor | `/quiz-perfil-de-investidor/` (19508) |
| preco-justo | `/calculadora-preco-justo/` (19510) |
| um-milhao | `/calculadora-1-milhao/` (19541) |
| jcp-liquido | `/calculadora-jcp-liquido/` (19543) |
| aposentadoria-renda | `/calculadora-aposentadoria-renda-passiva/` (19545) |
| ir-fii-venda | `/calculadora-ir-venda-fii/` (19547) |

⚠️ O **post 1198** e a **página 19504** usam o mesmo endereço, `/calculadora-juros-anual-para-mensal/`. O mesmo acontece com o post 2649 e a página 2658 (`/carteira-recomendada-fundos-imobiliarios-agosto-2025/`). Só um dos dois aparece para o visitante. Vale tirar o post antigo do ar ou mudar o slug dele. O 1198 ficou fora como origem.

## Destinos: quantos links cada um recebe

"Era órfão" quer dizer que nenhum post nem página (fora as `cotacao-*`) linkava o destino dentro do conteúdo, no cache de hoje.

| Lote | Destino | Links | Era órfão? |
|---|---|---|---|
| L1 | [Simulador de marcação a mercado do Tesouro IPCA+](https://investirecocaresocomecar.com.br/simulador-ntnb/) | 8 | não |
| L1 | [Simulador de renda mensal com FIIs](https://investirecocaresocomecar.com.br/simulador-renda-fii/) | 8 | sim |
| L1 | [Calculadora LCI/LCA × CDB](https://investirecocaresocomecar.com.br/calculadora-lci-lca-cdb/) | 8 | sim |
| L1 | [Calculadora de juros anual para mensal](https://investirecocaresocomecar.com.br/calculadora-juros-anual-para-mensal/) | 3 | não |
| L1 | [Comparador de renda fixa (CDB, LCI, prefixado e IPCA+)](https://investirecocaresocomecar.com.br/calculadora-cdb-lci-prefixado-ipca/) | 8 | sim |
| L1 | [Quiz de perfil de investidor](https://investirecocaresocomecar.com.br/quiz-perfil-de-investidor/) | 8 | sim |
| L1 | [Calculadora de preço justo (Bazin e Graham)](https://investirecocaresocomecar.com.br/calculadora-preco-justo/) | 6 | sim |
| L1 | [Calculadora: quanto falta para juntar 1 milhão](https://investirecocaresocomecar.com.br/calculadora-1-milhao/) | 8 | sim |
| L1 | [Calculadora de JCP líquido](https://investirecocaresocomecar.com.br/calculadora-jcp-liquido/) | 8 | sim |
| L1 | [Calculadora de aposentadoria com renda passiva e INSS](https://investirecocaresocomecar.com.br/calculadora-aposentadoria-renda-passiva/) | 8 | sim |
| L1 | [Calculadora de IR na venda de FII](https://investirecocaresocomecar.com.br/calculadora-ir-venda-fii/) | 7 | sim |
| L2 | [4873 Dividendos e dividend yield](https://investirecocaresocomecar.com.br/dividendos-o-que-sao-dividend-yield/) | 10 | não |
| L2 | [4874 Fundos imobiliários, guia completo](https://investirecocaresocomecar.com.br/fundos-imobiliarios-o-que-sao-fiis/) | 10 | sim |
| L2 | [5091 O que é BOVA11](https://investirecocaresocomecar.com.br/o-que-e-bova11/) | 7 | sim (só as `cotacao-*` linkavam) |
| L2 | [1053 Itaúsa × Itaú (ITSA4 × ITUB4)](https://investirecocaresocomecar.com.br/qual-a-diferenca-entre-itausa-e-itau-guia-completo/) | 4 | não |
| L2 | [993 Quem a Itaúsa controla](https://investirecocaresocomecar.com.br/quem-a-itausa-controla-conheca-suas-empresas/) | 6 | sim |
| L2 | [4537 ETFs de dividendos mensais (JEPI39)](https://investirecocaresocomecar.com.br/etfs-dividendos-mensais-b3-2026/) | 3 | não |

O teto foi de 8 links por ferramenta e 10 por guia. Os que ficaram abaixo do teto não tinham mais frases boas: o "juros anual para mensal" pede "taxa mensal" ou "juros ao mês" num post de tema próximo, e o 4537 pede "JEPI39" ou "ETF de dividendos", mas sem citar o JEPQ39 na mesma frase.

## Órfãos que deixam de ser órfãos (31)

- **Ferramentas (9):** `/simulador-renda-fii/`, `/calculadora-lci-lca-cdb/`, `/calculadora-cdb-lci-prefixado-ipca/`, `/quiz-perfil-de-investidor/`, `/calculadora-preco-justo/`, `/calculadora-1-milhao/`, `/calculadora-jcp-liquido/`, `/calculadora-aposentadoria-renda-passiva/` e `/calculadora-ir-venda-fii/`.
- **Guias (3):** `/fundos-imobiliarios-o-que-sao-fiis/` (4874), `/quem-a-itausa-controla-conheca-suas-empresas/` (993) e `/o-que-e-bova11/` (5091).
- **L3 (19):** `/abev3-copa-2026-vale-investir-pausa-hidratacao/`, `/ambev-abev3-resultado-1t26-vale-a-pena-investir/`, `/acoes-do-nubank-roxo34-despencam-10-o-que-aconteceu-e-o-que-esperar/`, `/banco-do-brasil-bbas3-corte-dividendo-payout-2026/`, `/banco-do-brasil-ou-itau-melhor-acao-dividendos-2026/`, `/bbas3-roe-abaixo-selic-banco-do-brasil-dividendos-2026/`, `/bbse3-cxse3-pssa3-melhor-seguradora-dividendos/`, `/cxse3-bbse3-rebaixamento-jpmorgan-vale-a-pena/`, `/bradsaude-saud3-lucro-sobe-acao-cai-sinistralidade/`, `/saud3-bradesco-vai-fechar-capital-bradsaude/`, `/compass-pass3-bancos-ipo-recomendam-compra-conflito-interesse/`, `/ipo-compass-pass3-vale-a-pena-investir/`, `/copel-cple3-dividendo-cortado-vale-a-pena-investir/`, `/o-melhor-etf-de-bitcoin-da-b3-hodl11-comparacao-completa-com-bith11-qbtc11-e-biti11/`, `/opa-santander-brasil-sanb11-minoritario-refem/`, `/trxf11-faria-lima-dos-galpoes-vale-o-hype/`, `/vale3-cobre-ia-vale-a-pena-investir/`, `/vivt3-dividendos-conta-celular-gratis-para-sempre/` e `/weg-wege3-lucro-cai-acao-sobe-vale-a-pena-investir/`.

Os outros órfãos do `sugestoes-links.csv` continuam sem link. Ou o título não tem um ticker que apareça numa frase boa das origens sugeridas, ou o post tem achado CRÍTICO sem correção, ou ele vai ser redirecionado. Para eles, a âncora precisa ser escolhida à mão.

## Cinco exemplos (antes → depois)

1. **4850** (L1, comparador de renda fixa): `paga IR pela tabela regressiva.` → `paga IR pela <a href="…/calculadora-cdb-lci-prefixado-ipca/">tabela regressiva</a>.`
2. **9591** (L1, renda com FIIs): `cada faixa de renda mensal com fundos imobiliários:` → `cada faixa de <a href="…/simulador-renda-fii/">renda mensal com fundos imobiliários</a>:`
3. **11563** (L1, simulador NTN-B): `a 8% ganha na marcação a mercado se a recompra` → `a 8% ganha na <a href="…/simulador-ntnb/">marcação a mercado</a> se a recompra`
4. **4845** (L2, guia 1053): `mas sim ITUB4 vs ITSA4.` → `mas sim <a href="…/qual-a-diferenca-entre-itausa-e-itau-guia-completo/">ITUB4 vs ITSA4</a>.`
5. **3172** (L2, guia 4537): `Sim, o JEPI39 paga` → `Sim, o <a href="…/etfs-dividendos-mensais-b3-2026/">JEPI39</a> paga`

(`…` = `https://investirecocaresocomecar.com.br`; nos patches, a URL vai completa.)

## Como os links foram escolhidos

Quem faz tudo é o [`gerar_links.py`](gerar_links.py), sem rede. Ele lê o cache dos posts, o cache das páginas, `seo/varredura.json`, `seo/sugestoes-links.csv` e `auditoria-fatos/achados.csv`. Para validar, importa o `patchlib.py` e o `carregar_posts()` da auditoria-fatos, sem mudar nada neles.

- **Relevância:** similaridade TF-IDF entre a origem e o destino (para uma ferramenta, o texto da página dela), multiplicada pelo tráfego provável da origem (`1 + 0,25·ln(1 + links internos recebidos)`, da varredura). A origem também precisa falar do tema: um mínimo de menções, por exemplo 6 de FII/fundo imobiliário para o simulador de renda com FIIs.
- **Distribuição:** cada destino escolhe, uma rodada de cada vez, a melhor origem livre. Os guias (L2) escolhem primeiro, porque as âncoras deles são mais raras. Um post fica num lote só, para que um lote aplicado não quebre o patch de outro.
- **Âncora:** um termo que já está na frase (como "marcação a mercado", "tabela regressiva", "dividend yield", "BOVA11" ou "juros sobre capital próprio") vira link. Nenhuma palavra é acrescentada ou trocada, e o teste confere que o texto visível fica idêntico. Algumas âncoras só valem com contexto na mesma frase: "ganho de capital" e "DARF" só com FII ou cota, e "ITUB4" só com Itaúsa ou ITSA4.
- **Onde o link não entra:** em `<a>`, títulos, `<th>`/`<td>`, botões, legendas, FAQ, índice, `<script>`, frase com JEPQ39, aviso legal ("não é recomendação…") e frase que tenha achado na `achados.csv`, porque essas ainda vão mudar.
- **Destinos proibidos:** posts que serão redirecionados ou despublicados (1033, 998, 1073, 1083, 1113, 1178, 1183, e também 983, 1003, 1013, 1038, 1063, 1068, 1078, 1098, 1128, 1168, 1188 e 1193, do RELATORIO da auditoria), `cotacao-*`, duplicados que vão para 301, páginas do Elementor e posts com CRÍTICO que não está corrigido nos lotes A/B.
- **Origens excluídas:** as mesmas, mais os posts marcados para reescrever (1008, 1043, 1158 e 4816), onde o link se perderia, e o post que divide o endereço com a página da ferramenta (1198).
- **Regras do `de`** (as do `gerar_patches.py`): trecho seguro, sem aspas, travessão, reticências, `&`, `<`, `>`, quebra ou NxN; dentro de um único nó de texto; e **1 vez no post todo**, contando o `<script>`, porque o `para` leva aspas no `href` e não pode cair num JSON-LD.
- **Convivência com os lotes A/B:** 21 posts têm patch nos dois lugares (4873, 4874, 5042, 7376 e outros). Para eles, o `de` do link não encosta em nenhuma troca de A/B, e as duas aplicações funcionam em qualquer ordem. O teste confere isso.

## Testes

```
python3 -m pytest -q links-internos/tests auditoria-fatos/tests
```

O resultado foi 134 testes passando.

- `links-internos/tests/test_links.py` confere estes pontos:
  - Cada um dos 116 patches segue as regras: `de` seguro, único e com `de_rendered`; um único `<a href>` por troca; texto visível igual; nenhum destino proibido, repetido ou que o post já linka; no máximo 3 links.
  - Cada post está num lote só.
  - Com um WordPress falso, o `aplicar_patches.py` faz `--checar` e `--aplicar` em **2 patches reais** (o primeiro do L1 e o primeiro do L2). Ele grava o backup, insere os links e não muda mais nada, e uma segunda aplicação é pulada.
  - Pela opção `--pasta`, o `main()` confere os lotes L1, L2 e L3 inteiros: todos os posts saem "PRONTO".
  - Os posts em comum com os lotes A/B aceitam as duas ordens.
  - Sem o cache dos posts, o teste é pulado.
- `auditoria-fatos/tests/test_aplicar_patches.py` ganhou 2 testes. O primeiro cobre `--pasta` com um lote `L1` (`--checar` não grava, `--aplicar` aplica, e lote ou pasta inexistente dá erro claro). O segundo confere que, sem `--pasta`, `--lote A` continua lendo `auditoria-fatos/patches/LOTE_A.json`. Os 10 testes antigos seguem passando.

No teste, o `content.raw` é simulado com o `content.rendered` do cache. No WordPress, quem confere o raw de verdade é o `--checar`.

## Comandos do Mac

Rode na raiz do repositório, com `WP_USER` e `WP_APP_PASSWORD` no ambiente. Sempre `--checar` antes de `--aplicar`. Os lotes A/B podem ir antes ou depois.

```
# L1: ferramentas
python3 auditoria-fatos/aplicar_patches.py --pasta links-internos/patches --checar --lote L1
python3 auditoria-fatos/aplicar_patches.py --pasta links-internos/patches --aplicar --lote L1

# L2: guias corrigidos
python3 auditoria-fatos/aplicar_patches.py --pasta links-internos/patches --checar --lote L2
python3 auditoria-fatos/aplicar_patches.py --pasta links-internos/patches --aplicar --lote L2

# L3: órfãos por ticker
python3 auditoria-fatos/aplicar_patches.py --pasta links-internos/patches --checar --lote L3
python3 auditoria-fatos/aplicar_patches.py --pasta links-internos/patches --aplicar --lote L3

# um post só, ou desfazer (restaura o backup mais recente do post)
python3 auditoria-fatos/aplicar_patches.py --pasta links-internos/patches --checar --lote L1 --so 4850
python3 auditoria-fatos/aplicar_patches.py --desfazer 4850
```

O `--aplicar` só grava os posts em que **todas** as trocas casam exatamente 1 vez no raw. O resto aparece como PULADO, com o motivo. O backup e o log vão para `auditoria-fatos/backup/`, como nos lotes A/B. Depois de cada lote, limpe o cache do WP-Optimize.

Para refazer os patches depois de novas mudanças no site:

```
python3 auditoria-fatos/auditar.py baixar        # posts, 1 req/s, em auditoria-fatos/cache/
python3 links-internos/baixar_paginas.py         # páginas, 1 req/s
python3 links-internos/gerar_links.py            # regrava patches/, LOTE_L*.json e resumo.csv
```
