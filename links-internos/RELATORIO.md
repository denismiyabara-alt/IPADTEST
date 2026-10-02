# Links internos em lotes

Feito em 02/10/2026, só leitura no site. Aqui ficam os **patches**. Quem aplica é o Mac, com o `auditoria-fatos/aplicar_patches.py`, que ganhou a opção `--pasta`.

## Números

| Lote | O que liga | Posts (patches) | Links novos |
|---|---|---|---|
| **L1** | as 11 ferramentas do plugin `iec-ferramentas` 1.3.0 | 60 | 80 |
| **L2** | os 6 guias corrigidos ou reescritos (4873, 4874, 5091, 1053, 993, 4537) | 33 | 40 |
| **L3** | órfãos restantes do `seo/sugestoes-links.csv` e substitutos neutros, pelo ticker do título | 7 | 7 |
| **Total** | | **102** | **129** |

Cada post entra em um lote só, e cada lote tem um patch por post. Dos 100 posts, 79 ganham 1 link, 19 ganham 2 e 4 ganham 3. Nenhum post passa de 3.

A primeira versão tinha 116 posts e 146 links (L1 61/80, L2 33/40, L3 22/26). Depois da revisão, saíram os destinos com título ou endereço de recomendação e os posts do `posts-para-refresh.csv`; veja [Destinos excluídos por título](#destinos-excluídos-por-título). Também saíram os posts 1198 e 2649, que viraram rascunho. Na última rodada, o gate passou a bloquear "qual é a melhor" (commit cf0ac38 no investir-e-cocar), e o `/bbse3-cxse3-pssa3-melhor-seguradora-dividendos/` saiu dos destinos (1 link a menos no L3). Depois, na aplicação, o Mac tirou os 2 links do L3 para `/abev3-copa-2026-vale-investir-pausa-hidratacao/` (posts 4391 e 11719), porque o endereço tem "vale investir". A regra agora pega também "vale investir" e "vale comprar", no gate e aqui, e o L3 ficou com 7 posts e 7 links, como foi aplicado. Quem mais perdeu foi o L3. L1 e L2 continuam com os mesmos destinos e as mesmas contagens.

O detalhe de cada link está em [`resumo.csv`](resumo.csv): lote, origem, destino, âncora, `de`, `para` e se o destino era órfão. Os destinos barrados estão em [`destinos-bloqueados.csv`](destinos-bloqueados.csv).

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

**Posts 1198 e 2649 (rascunho):** os dois viraram rascunho no WordPress. O endereço `/calculadora-juros-anual-para-mensal/` ficou com a página da ferramenta (19504), e `/carteira-recomendada-fundos-imobiliarios-agosto-2025/` ficou com a página 2658. Os dois posts estão fora como origem e como destino (`RASCUNHO` no `gerar_links.py`): nenhum patch para eles e nenhum link para eles. Os 3 links para `/calculadora-juros-anual-para-mensal/` continuam valendo, porque o endereço agora é da ferramenta.

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

## Destinos excluídos por título

Nenhum post recebe link se:

- o título for barrado pela regra **RECOMENDACAO_TITULO** do gate de qualidade (`pipeline/gate_qualidade.py`, branch `gate-qualidade` do repositório investir-e-cocar). A regex `RE_RECOM_TITULO` foi copiada sem mudança, e um teste compara a cópia com o gate quando ele está na máquina;
- **o endereço** cair na mesma regra. Isso vale também quando o título já foi neutralizado, como em `/ambev-abev3-resultado-1t26-vale-a-pena-investir/`, cujo título passa no gate mas cujo slug diz "vale a pena";
- o post estiver no **`site-ativos/posts-para-refresh.csv`**.

Os links que caíram foram trocados, quando deu, por outro post do mesmo ativo com título e endereço neutros, que recebe as mesmas origens sugeridas (coluna "substituto"). Não há página de ativo do site-ativos publicada para usar no lugar. Quando não há substituto, a frase fica sem link.

A coluna "links" mostra quantos links o post receberia se o bloqueio caísse: a mesma seleção, refeita com ele na lista. Quando o título (e o slug, com 301) for corrigido e o post sair do `posts-para-refresh.csv`, basta rodar o `gerar_links.py` de novo para ele voltar a receber links.

| Destino | Links | Motivo | Substituto |
|---|---|---|---|
| /abev3-copa-2026-vale-investir-pausa-hidratacao/ | 2 | endereço com "vale investir" | — |
| /ambev-abev3-resultado-1t26-vale-a-pena-investir/ | 2 | endereço com "vale a pena" | — |
| /banco-do-brasil-bbas3-corte-dividendo-payout-2026/ | 2 | título com "vale a pena" (RECOMENDACAO_TITULO); está no site-ativos/posts-para-refresh.csv | /bbas3-resultado-2t-cartao-de-credito-inadimplencia/ |
| /banco-do-brasil-ou-itau-melhor-acao-dividendos-2026/ | 2 | título com "qual a melhor" (RECOMENDACAO_TITULO); endereço com "melhor acao" | — |
| /bbas3-roe-abaixo-selic-banco-do-brasil-dividendos-2026/ | 2 | título com "Vale a Pena" (RECOMENDACAO_TITULO); está no site-ativos/posts-para-refresh.csv | — |
| /o-melhor-etf-de-bitcoin-da-b3-hodl11-comparacao-completa-com-bith11-qbtc11-e-biti11/ | 2 | título com "Melhor ETF" (RECOMENDACAO_TITULO); endereço com "melhor etf" | — |
| /bradsaude-saud3-lucro-sobe-acao-cai-sinistralidade/ | 1 | título com "vale a pena" (RECOMENDACAO_TITULO) | — |
| /copel-cple3-dividendo-cortado-vale-a-pena-investir/ | 1 | título com "Vale a pena" (RECOMENDACAO_TITULO); endereço com "vale a pena" | — |
| /cxse3-bbse3-rebaixamento-jpmorgan-vale-a-pena/ | 1 | título com "Vale a pena" (RECOMENDACAO_TITULO); endereço com "vale a pena" | — |
| /ipo-compass-pass3-vale-a-pena-investir/ | 1 | título com "Vale a Pena" (RECOMENDACAO_TITULO); endereço com "vale a pena" | /pass3-compass-ipo-conflito-de-interesse-bancos-coordenadores/ |
| /opa-santander-brasil-sanb11-minoritario-refem/ | 1 | título com "vale a pena" (RECOMENDACAO_TITULO) | — |
| /trxf11-faria-lima-dos-galpoes-vale-o-hype/ | 1 | título com "vale a pena" (RECOMENDACAO_TITULO); está no site-ativos/posts-para-refresh.csv | /trxf11-buraco-22-reais-cota-compensacao-de-creditos/ |
| /vale3-cobre-ia-vale-a-pena-investir/ | 1 | título com "vale a pena" (RECOMENDACAO_TITULO); endereço com "vale a pena"; está no site-ativos/posts-para-refresh.csv | — |
| /vivt3-dividendos-conta-celular-gratis-para-sempre/ | 1 | título com "Vale a Pena" (RECOMENDACAO_TITULO) | — |
| /weg-wege3-lucro-cai-acao-sobe-vale-a-pena-investir/ | 1 | título com "vale a pena" (RECOMENDACAO_TITULO); endereço com "vale a pena" | — |
| /%f0%9f%9a%80-tesla-tsla34-vale-a-pena-descubra-se-ainda-faz-sentido-investir-em-2025/ | 0 | título com "Vale a Pena" (RECOMENDACAO_TITULO); endereço com "vale a pena" | — |
| /auau3-petz-cobasi-sinergia-vale-a-pena-investir/ | 0 | título com "vale a pena" (RECOMENDACAO_TITULO); endereço com "vale a pena" | — |
| /aura-minerals-aura33-vale-a-pena-investir-turnaround/ | 0 | título com "Vale a Pena" (RECOMENDACAO_TITULO); endereço com "vale a pena" | — |
| /brco11-gpa-quebrou-contrato-vale-a-pena-investir/ | 0 | endereço com "vale a pena" | — |
| /calendario-dividendos-julho-2026-logg3-vale-a-pena/ | 0 | título com "Vale a Pena" (RECOMENDACAO_TITULO); endereço com "vale a pena" | — |
| /goat11-o-etf-hibrido-da-b3-com-80-em-renda-fixa-e-20-em-variavel-vale-a-pena-investir/ | 0 | título com "Vale a Pena" (RECOMENDACAO_TITULO); endereço com "vale a pena" | — |
| /hype3-santander-conviccao-corte-preco-alvo-vale-a-pena/ | 0 | título com "vale a pena" (RECOMENDACAO_TITULO); endereço com "vale a pena" | — |
| /kncr11-subscricao-vale-a-pena/ | 0 | título com "Vale a Pena" (RECOMENDACAO_TITULO); endereço com "vale a pena"; está no site-ativos/posts-para-refresh.csv | — |
| /nike-adidas-copa-2026-bolsa-nike34-vale-a-pena/ | 0 | título com "Vale a pena" (RECOMENDACAO_TITULO); endereço com "vale a pena" | — |
| /petr4-65-por-cento-lucro-estatais-vale-a-pena-investir/ | 0 | título com "vale a pena" (RECOMENDACAO_TITULO); endereço com "vale a pena"; está no site-ativos/posts-para-refresh.csv | — |
| /radl3-mercado-livre-ozempic-vale-a-pena-comprar-a-queda/ | 0 | título com "vale a pena" (RECOMENDACAO_TITULO); endereço com "vale a pena" | — |
| /rara11-etf-terras-raras-vale-a-pena-investir/ | 0 | título com "vale a pena" (RECOMENDACAO_TITULO); endereço com "vale a pena" | — |
| /ugpa3-ultrapar-dividendos-2026-vale-a-pena/ | 0 | endereço com "vale a pena" | — |
| /weg-wege3-cai-mais-de-7-apos-resultados-do-4t24-e-hora-de-comprar/ | 0 | título com "Hora de Comprar" (RECOMENDACAO_TITULO); endereço com "hora de comprar" | — |

São 30 destinos, que receberiam 22 links no total. Os que aparecem com 0 não ganhariam link de qualquer jeito, porque não houve frase boa nas origens sugeridas.

## Órfãos que deixam de ser órfãos (15)

- **Ferramentas (9):** `/simulador-renda-fii/`, `/calculadora-lci-lca-cdb/`, `/calculadora-cdb-lci-prefixado-ipca/`, `/quiz-perfil-de-investidor/`, `/calculadora-preco-justo/`, `/calculadora-1-milhao/`, `/calculadora-jcp-liquido/`, `/calculadora-aposentadoria-renda-passiva/` e `/calculadora-ir-venda-fii/`.
- **Guias (3):** `/fundos-imobiliarios-o-que-sao-fiis/` (4874), `/quem-a-itausa-controla-conheca-suas-empresas/` (993) e `/o-que-e-bova11/` (5091).
- **L3 (3):** `/acoes-do-nubank-roxo34-despencam-10-o-que-aconteceu-e-o-que-esperar/`, `/compass-pass3-bancos-ipo-recomendam-compra-conflito-interesse/` e `/saud3-bradesco-vai-fechar-capital-bradsaude/`.
- O L3 também manda links para 2 substitutos que já recebiam link, então não contam como órfãos resolvidos: `/bbas3-resultado-2t-cartao-de-credito-inadimplencia/` (2 links) e `/trxf11-buraco-22-reais-cota-compensacao-de-creditos/` (1 link).

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
- **Destinos proibidos:** título ou endereço com recomendação (regra do gate), posts do `posts-para-refresh.csv`, os rascunhos 1198 e 2649, posts que serão redirecionados ou despublicados (1033, 998, 1073, 1083, 1113, 1178, 1183, e também 983, 1003, 1013, 1038, 1063, 1068, 1078, 1098, 1128, 1168, 1188 e 1193, do RELATORIO da auditoria), `cotacao-*`, duplicados que vão para 301, páginas do Elementor e posts com CRÍTICO que não está corrigido nos lotes A/B.
- **Origens excluídas:** as mesmas, mais os posts marcados para reescrever (1008, 1043, 1158 e 4816), onde o link se perderia, e os rascunhos 1198 e 2649.
- **Regras do `de`** (as do `gerar_patches.py`): trecho seguro, sem aspas, travessão, reticências, `&`, `<`, `>`, quebra ou NxN; dentro de um único nó de texto; e **1 vez no post todo**, contando o `<script>`, porque o `para` leva aspas no `href` e não pode cair num JSON-LD.
- **Convivência com os lotes A/B:** 21 posts têm patch nos dois lugares (4873, 4874, 5042, 7376 e outros). Para eles, o `de` do link não encosta em nenhuma troca de A/B, e as duas aplicações funcionam em qualquer ordem. O teste confere isso.

## Testes

```
python3 -m pytest -q links-internos/tests auditoria-fatos/tests
```

O resultado foi 124 testes passando.

- `links-internos/tests/test_links.py` confere estes pontos:
  - Cada um dos 102 patches segue as regras: `de` seguro, único e com `de_rendered`; um único `<a href>` por troca; texto visível igual; nenhum destino proibido, repetido ou que o post já linka; no máximo 3 links.
  - Cada post está num lote só.
  - Com um WordPress falso, o `aplicar_patches.py` faz `--checar` e `--aplicar` em **2 patches reais** (o primeiro do L1 e o primeiro do L2). Ele grava o backup, insere os links e não muda mais nada, e uma segunda aplicação é pulada.
  - Pela opção `--pasta`, o `main()` confere os lotes L1, L2 e L3 inteiros: todos os posts saem "PRONTO".
  - Os posts em comum com os lotes A/B aceitam as duas ordens.
  - Nenhum `para` aponta para post cujo título ou endereço o gate barra, nem para post do `posts-para-refresh.csv`. A regex copiada é igual à do gate.
  - Não há patch para 1198 nem para 2649, e nenhum link aponta para eles. Os links para `/calculadora-juros-anual-para-mensal/`, que agora é a página da ferramenta, continuam.
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
python3 links-internos/gerar_links.py            # regrava patches/, LOTE_L*.json, resumo.csv e destinos-bloqueados.csv
```
