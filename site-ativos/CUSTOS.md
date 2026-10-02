# Custos e viabilidade: páginas de ações e FIIs

Estudo de 02/10/2026 para o site de ativos do Investir e Coçar. Ele se apoia em `DESENHO.md`, `RELATORIO-MVP.md` e `README.md`. O MVP gera HTML estático: 20 ativos e 33 páginas.

**Legenda.** **CONFIRMADO** quer dizer que li a fonte oficial em 02/10/2026; a fonte vem ao lado. **conferir** quer dizer que não consegui abrir a página oficial (a rede bloqueou, ou só achei fonte de terceiros), ou que o dado depende de informação que só o Denis tem.

**Dólar usado:** US$ 1 = **R$ 5,2238**. É a PTAX de venda de 02/10/2026, série SGS 1 do Banco Central (`api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados/ultimos/3`, consultada em 02/10/2026). **CONFIRMADO.** Nas datas anteriores: R$ 5,2079 em 01/10 e R$ 5,1809 em 30/09.

---

## Resumo em 6 linhas

1. **Hospedagem: R$ 0 por mês.** A recomendação é publicar no próprio domínio (`/acoes/`, `/fiis/`) com um **Cloudflare Worker de arquivos estáticos**. O DNS do site já passa pelo Cloudflare, então isso funciona sem mexer na HostGator.
2. **Job diário: R$ 0 por mês.** Roda no GitHub Actions, num repositório privado. Com 400 ativos ele gasta de 170 a 370 minutos por mês, e a cota grátis é de 2.000.
3. **Dados da CVM e do BCB: R$ 0.** A licença é ODbL, e exige escrever "Fonte: CVM" e "Fonte: BCB".
4. **Preço da B3 (COTAHIST): R$ 0 *ou* R$ 320 por mês em 2026 (R$ 400 em 2027).** Depende de uma resposta por escrito da B3. A política nova de market data, em vigor desde 01/01/2026, não repete a frase "fim de dia sem custo" e trata o fim de dia como dado "com atraso". **Este é o maior risco de custo do projeto.**
5. **Fundos.NET:** não achei termo de uso que permita coleta automatizada. Os termos gerais da B3 limitam o uso a fins pessoais. **Não automatizar** sem autorização escrita.
6. **Tempo do Denis com 400 ativos:** de **3 a 8 horas por mês**, quase tudo na fila de proventos.

**Custo total recomendado: R$ 0 por mês em dinheiro, mais cerca de 6 horas por mês do Denis.** Se a B3 exigir licença, o total vira **R$ 320 por mês** (R$ 400 a partir de 01/01/2027). Detalhes na seção 6.

---

## 1. Hospedagem

### 1.1 O que descobri sobre a hospedagem atual (sem login, só consultas públicas)

Consultas de 02/10/2026: `curl -sI`, resolvedor DNS público (dnspython com 8.8.8.8) e DNS reverso. O `whois` não está instalado aqui, e o RDAP da ARIN foi bloqueado pela rede.

| O que olhei | Resultado | O que indica |
|---|---|---|
| Cabeçalhos HTTP da home | `server: cloudflare`, `cf-ray`, `cf-cache-status: REVALIDATED`, `wpo-cache-status: cached` | **O Cloudflare está na frente (proxy laranja).** O HTML é guardado em cache no Cloudflare, e o WP-Optimize faz o cache de página na origem. |
| `/wp-json/` e uma URL inexistente | `server-timing: wp-before-template`, 404 do WordPress, `cf-cache-status: MISS` | WordPress na origem. Nenhum cabeçalho mostra o servidor web (o Cloudflare esconde). |
| A e AAAA do domínio | 104.21.68.198, 172.67.198.40 e 2 IPv6 2606:4700:… | IPs de proxy do Cloudflare, não da hospedagem. |
| NS | `wells.ns.cloudflare.com`, `vida.ns.cloudflare.com` | **O DNS é gerenciado no Cloudflare.** Isso abre a opção do Worker (1.2 d). |
| SOA | `dns.cloudflare.com` | Idem. |
| MX | `_dc-mx.bd28a6a1695e.investirecocaresocomecar.com.br` → **108.179.253.89** | O e-mail aponta direto para um servidor fora do Cloudflare. |
| DNS reverso de 108.179.253.89 | `108-179-253-89.unifiedlayer.com` | A Unified Layer é a rede de data center usada pela HostGator. |
| TXT (SPF) | `v=spf1 a mx include:websitewelcome.com ~all` | `websitewelcome.com` é o domínio de e-mail da HostGator. |
| `ftp.`, `cpanel.`, `webmail.`, `mail.` | Resolvem para os IPs do Cloudflare (com proxy). `dados.` não existe. Um nome aleatório não resolve (não há curinga). | Registros típicos de cPanel importados para o Cloudflare. |
| `http://` (sem S) | Respondeu 200, sem redirecionar para `https://` | Achado à parte: o "Always Use HTTPS" parece desligado (conferir no navegador). Não muda o custo, mas vale corrigir por causa do SEO. |

**Conclusão provável:** é hospedagem compartilhada com **cPanel na HostGator** (provavelmente a HostGator Brasil), atrás do **Cloudflare** com DNS e proxy. **conferir:** só o painel ou a fatura confirmam o plano.

**Duas consequências práticas:**

- **Não dá para enviar por SFTP usando `ftp.investirecocaresocomecar.com.br`.** Esse nome passa pelo proxy do Cloudflare, que só repassa HTTP e HTTPS. O envio teria de usar o nome do servidor da HostGator (algo como `brXXX.hostgator.com.br`, que aparece no cPanel) ou o IP de origem.
- **O registro MX expõe o IP da origem (108.179.253.89),** que deveria ficar escondido atrás do Cloudflare. Pode ser o mesmo servidor do site (conferir). Não fiz nenhuma conexão a esse IP.

### 1.2 As opções, com limites e custo

| Opção | Custo por mês | Custo por ano | Limites do plano grátis ou atual | Status |
|---|---|---|---|---|
| **(a) Pasta `/acoes/` e `/fiis/` na HostGator, por SFTP** | R$ 0 a mais (o plano já é pago; valor e plano: **conferir**) | R$ 0 a mais | Inodes: 50.000 no plano Start e 250.000 nos planos P, M e Business, com advertência e risco de suspensão acima disso (**conferir**: só achei pela busca, porque `suporte.hostgator.com.br` está bloqueado aqui). SSH e SFTP na porta 2222 (**conferir**). Banda "ilimitada" com uso justo (**conferir**). Tamanho por arquivo: **conferir**. Builds: não se aplica (o build roda no Actions). | conferir |
| **(b) Subdomínio `dados.` no Cloudflare Pages** | R$ 0 | R$ 0 | 500 builds por mês (builds feitos no Cloudflare), 1 build por vez, 20 minutos por build. **20.000 arquivos por site.** **25 MiB por arquivo.** 100 domínios por projeto. **Requisições a arquivos estáticos grátis e ilimitadas.** Tamanho total: o documento não informa (na prática, 20.000 × 25 MiB). Se o envio pelo Actions (Direct Upload) conta nos 500 builds: **conferir**. | **CONFIRMADO** (docs oficiais do Cloudflare, repositório `cloudflare/cloudflare-docs`: `pages/platform/limits.mdx` e `pages/functions/pricing.mdx`, lidos em 02/10/2026) |
| **(c) GitHub Pages (subdomínio)** | R$ 0 com repositório **público**. Com repositório **privado**, exige GitHub Pro: US$ 4 por mês, ou **R$ 20,90** | R$ 0 ou R$ 250,74 | Site publicado de até **1 GB**. Repositório: 1 GB recomendado. Banda: **100 GB por mês (limite flexível)**. 10 builds por hora (flexível; não vale para quem publica pelo Actions). Deploy com timeout de 10 minutos. **Proibido usar como hospedagem grátis de negócio online voltado a transações comerciais** (um site informativo com anúncio é zona cinzenta). Em repositório privado, só nos planos Pro, Team e Enterprise. | Limites e regra do repositório privado: **CONFIRMADOS** (`github/docs`: `github-pages-limits.md` e `reusables/gated-features/pages.md`, 02/10/2026). Preço do Pro: **conferir** (só fonte de terceiros; `github.com/pricing` não lista o Pro). |
| **(d) Recomendada: Cloudflare Worker com arquivos estáticos numa *rota* do domínio principal** (`investirecocaresocomecar.com.br/acoes/*` e `/fiis/*`) | R$ 0 | R$ 0 | **20.000 arquivos por versão** e 25 MiB por arquivo. **Requisições a arquivos estáticos grátis e ilimitadas, sem custo de armazenamento.** O limite de 100.000 requisições por dia do plano Free vale só quando o *script* roda (não vamos usar script). Exige que o domínio esteja no Cloudflare (está: NS confirmados acima). A pasta de saída tem de repetir o caminho (`saida/acoes/...`), que já é o formato do MVP. | **CONFIRMADO** (`workers/platform/limits.mdx`, `workers/static-assets/billing-and-limitations.mdx` e `workers/static-assets/routing/advanced/serving-a-subdirectory.mdx`, 02/10/2026). Se a visita conta como requisição do Worker quando ele só está na rota: **conferir** no primeiro teste. |
| (d2) Netlify Free (subdomínio) | R$ 0 | R$ 0 | 300 créditos por mês. Banda custa 20 créditos por GB (cerca de 15 GB no mês) e **cada deploy de produção custa 15 créditos**. **Com 22 deploys por mês (dias úteis), são 330 créditos, mais do que o plano grátis dá.** Não serve para atualização diária. | **conferir** (só fontes de terceiros; `netlify.com` está bloqueado aqui) |
| (d3) Bunny Storage + CDN (subdomínio) | Mínimo de US$ 1, ou **R$ 5,22** | R$ 62,69 | CDN a US$ 0,045 por GB na América do Sul (R$ 0,235 por GB) e US$ 0,01 por GB na Europa e América do Norte. Armazenamento a cerca de US$ 0,01 por GB. Nesse volume, sempre cai no mínimo. | **conferir** (só fontes de terceiros; `bunny.net` está bloqueado aqui) |

**Por que a opção (d):**

- Fica na **subpasta do domínio principal**, como pede o desenho, e herda a autoridade do domínio.
- Não precisa de SFTP nem de credencial da HostGator, não gasta inode e não pesa no servidor do WordPress.
- Uma falha no envio não derruba o WordPress.
- O Cloudflare já está no meio, então não há DNS novo.

**Cuidados da opção (d):**

1. As regras de cache de HTML que já existem no Cloudflare (o `REVALIDATED` da home) não podem servir página velha. Depois de cada envio, ou se limpa o cache das URLs `/acoes/*` e `/fiis/*`, ou se usa uma regra de "bypass" nesse caminho.
2. A rota de um Worker tem prioridade sobre a origem. As páginas `cotacao-*` do WordPress continuam onde estão, e os 301 entram depois.

**Por que não as outras:**

- **(a)** funciona, mas depende de quatro coisas que precisam ser confirmadas: SSH liberado, IP do GitHub aceito pelo firewall do cPanel, `.htaccess` dando prioridade à pasta real e limpeza do cache do Cloudflare. Fica como plano B.
- **(b)** e **(c)** usam subdomínio.
- **(c)** cobra R$ 20,90 por mês com repositório privado. Saída sem custo: publicar só o HTML num segundo repositório *público* (as páginas são públicas de qualquer jeito).
- **(d2)** estoura os créditos com deploy diário.

---

## 2. Onde roda o job diário

### 2.1 GitHub Actions (recomendado)

| Item | Valor | Status |
|---|---|---|
| Minutos grátis por mês em repositório privado | GitHub Free: **2.000**. GitHub Pro: 3.000. Qual é o plano do Denis: **conferir**. | **CONFIRMADO** (`github/docs`, `reusables/billing/actions-included-quotas.md`, 02/10/2026) |
| Arredondamento | **Cada job é arredondado para cima, para o minuto inteiro** | **CONFIRMADO** (`billing/reference/actions-runner-pricing.md`) |
| Preço acima da cota (Linux 2 núcleos) | US$ 0,006 por minuto (**R$ 0,031**). Linux de 1 núcleo: US$ 0,002 | **CONFIRMADO** (`reusables/billing/actions-standard-runner-prices.md`) |
| Cache | **10 GB por repositório** (cota separada dos artefatos, que têm 500 MB no Free). Entradas sem acesso há **mais de 7 dias são apagadas**. Acima de 10 GB, apaga as menos usadas. Um cache não pode ser alterado: cada versão nova precisa de uma chave nova. | **CONFIRMADO** (`actions/reference/workflows-and-actions/dependency-caching.md` e `billing/concepts/product-billing/github-actions.md`) |

**Como o cache funciona entre execuções:**

- `actions/cache` restaura `cache/raw/` (os ZIPs da CVM e o COTAHIST já filtrado, cerca de 262 MB hoje) e `cache/dados.sqlite` (207 MB hoje).
- A chave é do tipo `dados-AAAAMMDD`, com `restore-keys: dados-`. Assim, cada dia parte do cache mais recente, e o download só traz o que mudou (o pedido condicional com ETag e If-Modified-Since já existe no código).
- Com cerca de 0,5 a 1,5 GB por entrada, cabem de 6 a 10 dias no limite de 10 GB. As mais antigas saem sozinhas.
- Se o job ficar mais de 7 dias sem rodar, o cache some e a próxima execução é uma carga completa (de 5 a 12 minutos, ainda dentro da cota).

**Minutos por mês:**

| Cenário | Minutos por execução | Execuções | Minutos por mês | % de 2.000 | Custo |
|---|---|---|---|---|---|
| MVP (20 ativos), com cache | 2 (medido no MVP) + 1 de preparo (checkout, pip, cache) = **3** | 22 dias úteis | 66 | 3% | R$ 0 |
| MVP, primeira carga | ~5 + 1 = **6** | 1 vez | 6 | — | R$ 0 |
| **400 ativos, com cache** | **6 a 8** (ver 4.3) | 22 | 132 a 176 | 7% a 9% | R$ 0 |
| 400 ativos + testes a cada push (cerca de 20 por mês × 2 min) + 2 reexecuções | — | — | **170 a 220** | 9% a 11% | R$ 0 |
| 400 ativos, cenário ruim (15 min por execução, falhas, cache perdido) | 15 | 22 + extras | ~370 | 19% | R$ 0 |
| 400 ativos, primeira carga | 10 a 15 | 1 vez | 15 | — | R$ 0 |

Seria preciso passar de 2.000 minutos para pagar alguma coisa. Mesmo nesse caso, 100 minutos a mais custam R$ 3,13.

### 2.2 Mac com `launchd` (plano B)

- **Custo:** R$ 0.
- **Ponto fraco:** só roda se o Mac estiver ligado. Se o Mac estiver dormindo na hora marcada, o `launchd` roda o job quando ele acordar e junta as execuções perdidas numa só. Desligado, não roda. Fonte: `man launchd.plist`, chave `StartCalendarInterval`. **conferir** no Mac do Denis.
- **Vantagens:** o cache fica no disco (sem limite de 10 GB nem regra de 7 dias) e não usa IP de nuvem, caso a CVM ou a B3 bloqueiem o GitHub.
- **Desvantagens:** o Denis vira o "servidor". Se o job falhar, o aviso precisa chegar por e-mail ou notificação.

**Veredito:** Actions para o dia a dia. O Mac só se a CVM ou a B3 bloquearem os IPs do GitHub, ou para a carga inicial.

---

## 3. Custo e licença dos dados

| Fonte | Custo | Licença ou termo | Status |
|---|---|---|---|
| CVM dados abertos (DFP, ITR, FCA, cadastro, informes de FII) | R$ 0 | **ODbL** (Open Data Commons), com atribuição "Fonte: CVM" | **CONFIRMADO** (API CKAN `dados.cvm.gov.br/api/3/action/package_show`, campo `license_id = odc-odbl` em `cia_aberta-doc-dfp` e `fii-doc-inf_mensal`, 02/10/2026) |
| BCB (SGS 11, 12, 432, 433, 13522) | R$ 0 | ODbL no portal de dados abertos | **conferir** (`dadosabertos.bcb.gov.br` está bloqueado aqui; achei pela busca). A API respondeu normalmente. |
| B3 COTAHIST (séries históricas) | Download R$ 0. Exibir num site com anúncio: **R$ 0 ou R$ 320 por mês** | Ver 3.2 | **conferir com a B3** |
| Fundos.NET | R$ 0 | Ver 3.1 | **Não automatizar** sem autorização |

### 3.1 Fundos.NET (`fnet.bmfbovespa.com.br`): permite coleta automatizada?

**Veredito: não achei permissão. Sem autorização escrita da B3, não usar coleta automatizada.**

O que encontrei em 02/10/2026:

- O sistema **não tem página própria de termos de uso.** A página pública (`/fnet/publico/abrirGerenciadorDocumentosCVM`) não traz link de termos no rodapé. `/robots.txt` responde 404. A página de login não respondeu (timeout). A busca por "Fundos.NET termos de uso" só trouxe manuais do sistema.
- **Há CAPTCHA** ("Digite o texto da imagem acima") na exportação em lote ("Anexo B" / extrair informe mensal), segundo o arquivo `gerenciador-documentos-cvm.js`. É um sinal claro de que a B3 não quer extração automática em massa. A consulta da tabela simples não pede CAPTCHA.
- O Fundos.NET é um sistema da B3. Os **Termos de Uso do site da B3** (`b3.com.br/pt_br/termos-de-uso-e-protecao-de-dados/termos-de-uso/`) dizem:

  > "Os visitantes deste website podem utilizar os dados disponíveis nessas páginas para uso exclusivamente pessoal [...]. Não é permitida a reprodução, modificação, transmissão, comercialização, locação, publicação, distribuição ou quaisquer outras formas de utilização para fins comerciais de parte ou totalidade do conteúdo deste website, mediante qualquer forma ou meio, sem autorização prévia e por escrito da B3."

  Formalmente, esse texto cobre o `b3.com.br`. Se ele vale para o Fundos.NET: **conferir com a B3**. Na dúvida, vale o mais restritivo.

**O que fazer:**

1. Pedir autorização por escrito à B3 (fale conosco do Fundos.NET, ou `produtos-marketdata@b3.com.br`). Na pergunta: acesso automatizado e lento (1 requisição por segundo) aos "Avisos aos Cotistas – Estruturado", para exibir rendimento por cota num site com anúncios.
2. Enquanto isso, rendimento de FII pela **fila manual** (o Denis abre o aviso e confirma) ou pelo "DY estimado" com dado da CVM, como no MVP.

### 3.2 Política de market data da B3 para dados de fim de dia (EOD) num site com AdSense

**Veredito: hoje, o texto da B3 não garante mais que exibir EOD seja grátis. Perguntar à B3 por escrito antes de lançar.**

**Antes (até 2025).** A *Política Comercial de Market Data B3*, versão 3.0.4 de 15/10/2024, item 7.9, dizia:

> "Os DADOS DE FIM DE DIA B3 obtidos através das Plataformas de MARKET DATA B3, descritas no Capítulo 2 deste documento, podem ser distribuídos sem custo pelos DISTRIBUIDORES ou REDISTRIBUIDORES sem a necessidade de autorização prévia da B3."

Mesmo esse texto vale para quem é "distribuidor" ou "redistribuidor", isto é, quem assinou contrato com a B3, e para dados vindos das plataformas do capítulo 2 (UMDF e outras), não do download público. A página de **Perguntas frequentes** de distribuidores da B3 ainda repete esse trecho hoje.

**Agora (desde 01/01/2026).** Ao lado da Política Comercial, vale a nova **Política de Consumo de Market Data B3**: v1.0 de 01/01/2026 a 31/10/2026 e **v1.1 a partir de 01/11/2026** (PDF "Politica de Consumo de Market Data B3 V1.1", em `b3.com.br`, lido em 02/10/2026). Ela diz:

- Definições:

  > "Atraso: significa a Distribuição de informações em período igual ou superior a 15 (quinze) minutos após a transmissão dos Dados constantes do Market Data B3 pela B3, **incluindo Dados de Fim de Dia B3**."

- Item 3.3.2:

  > "O Distribuidor ou Redistribuidor que contratar Licença para Distribuição em Atraso possui autorização para distribuir [...]. Para Distribuição em websites abertos, plataformas e outros meios que possuam ou não controle de acesso, o dado em Atraso distribuído deve estar restrito às seguintes informações: preço do último negócio, de referência ou variação diária de preços; preços mínimos, máximos, de abertura e de fim de dia; volume financeiro, contratos em aberto e contratos negociados."

  > "[...] os Dados constantes do Market Data B3 em Atraso, Dados de Fim de Dia B3 e o Market Data Histórico B3 apenas poderão ser utilizados para construção de gráficos e tabelas informacionais, sendo vedados: (i) a comercialização, desenvolvimento de produtos, Distribuição, ou permissão de download ou consumo de qualquer dado [...]"

- A versão nova **não repete** a frase "podem ser distribuídos sem custo... sem a necessidade de autorização prévia".

**Tabela de preços** (*Política Comercial de Market Data B3 2026 V1.1*, item 4.1.1, "Licenças nos Mercados Listados", valores por mês e por dataset, em reais):

| Licença de Distribuição | 2026 | 2027 |
|---|---|---|
| Atraso, Snapshot | **R$ 320** | **R$ 400** |
| Atraso, Contínuo | R$ 1.920 | R$ 2.400 |

Os valores de 2027 vêm da *Política Comercial 2027 V1.1*. **CONFIRMADO** (PDFs oficiais, lidos em 02/10/2026).

**Como eu leio isso (não é parecer jurídico):**

- O que o site mostra (fechamento, mínima, máxima, volume e gráficos e tabelas informativos) está **dentro** da lista permitida.
- O que o site **não pode** fazer: oferecer download dos preços (CSV ou JSON para baixar). O comparador usa JSON embutido só para montar a tabela na tela. Isso deve ficar assim, sem botão de exportar.
- **Ponto aberto:** se um site com AdSense que usa o COTAHIST público precisa da "Licença para Distribuição em Atraso" (R$ 320 por mês em 2026), ou se o download público do COTAHIST está fora dessa política.
- Os Termos de Uso do site da B3 (citados em 3.1) também falam em "uso exclusivamente pessoal".

**O que fazer:** mandar um e-mail para `produtos-marketdata@b3.com.br` (o endereço do item 7.11 da política de 2024) descrevendo o site. Pontos da mensagem: dados de fim de dia do COTAHIST; só tabelas e gráficos; sem download; sem tempo real; site gratuito com AdSense. Pedir a resposta por escrito e guardar.

---

## 4. Escala: de 20 para cerca de 400 ativos

### 4.1 Tamanho medido no MVP (`site-ativos/saida/`, 02/10/2026)

| Tipo | Páginas | Média bruta | Média com gzip |
|---|---|---|---|
| Ação | 10 | 61,4 KB | 14,7 KB |
| FII | 10 | 70,9 KB | 17,2 KB |
| Listas, rankings, metodologia, comparador, calendário | 13 | de 9 a 33 KB | — |
| **Total do MVP** | **33 HTML (39 arquivos)** | **1,6 MB** | — |

- O CSS e os gráficos (SVG) estão dentro do HTML. Não há imagem.
- As fontes vêm do Google Fonts e o AdSense vem do Google, então não gastam a banda da hospedagem.

### 4.2 Com 400 ativos (cerca de 250 ações e 150 FIIs)

| Item | Estimativa |
|---|---|
| Páginas | 400 de ativo + cerca de 30 de lista, ranking e metodologia + cerca de 40 de setor (se entrarem) = **cerca de 470** |
| Arquivos | **cerca de 480** (um `index.html` por pasta, mais sitemap e afins). O limite do Cloudflare é 20.000, então usa 2,4%. |
| Inodes (na opção a) | cerca de 1.000 (pastas + arquivos), 0,4% de 250.000. Quanto o WordPress já usa: **conferir** no cPanel. |
| Tamanho total | 250 × 61 KB + 150 × 71 KB + cerca de 1,5 MB = **cerca de 27 MB** (o GitHub Pages aceita até 1 GB) |
| Maior arquivo | menos de 100 KB (o limite é 25 MiB) |
| Enviado por dia | O preço muda todo dia, então quase todas as páginas mudam: cerca de 430 arquivos e 28 MB por dia. |

### 4.3 Tempo de build (medido)

Rodei `calcular`, `validar` e `gerar` numa cópia do cache, em `IEC_SAIDA` e `IEC_DB` no scratchpad, sem tocar no `saida/` do projeto:

| Etapa | 20 ativos (medido) | 400 ativos (estimado, linear) |
|---|---|---|
| calcular | 3,7 s | cerca de 74 s |
| validar | 2,6 s | cerca de 52 s |
| gerar (33 páginas) | 1,9 s | cerca de 30 s (470 páginas) |
| baixar + normalizar, com cache | cerca de 2 min (relatório) | de 2 a 3 min (os arquivos da CVM e da B3 são os mesmos; a normalização carrega mais empresas) |
| Preparo do Actions (checkout, Python, restaurar 0,5 a 1,5 GB de cache) | — | cerca de 1 min |
| Publicar (Worker: só os arquivos alterados) | — | de 0,5 a 1 min (SFTP: de 1 a 3 min) |
| **Total por execução** | **cerca de 3 min** | **de 6 a 8 min** |

A base SQLite de 400 ativos deve ficar entre 0,5 e 1,5 GB (**conferir** na primeira carga). Cabe no cache de 10 GB.

### 4.4 Banda por mês

Por visita: cerca de **16 KB** com gzip (média de ações e FIIs). No pior caso, sem compressão: 66 KB. Os robôs de busca somam cerca de 0,2 GB por mês (470 páginas × 1 visita por dia).

| Pageviews por mês | Banda com gzip (+ robôs) | Pior caso, sem gzip | Cloudflare (b, d) | GitHub Pages (100 GB) | Netlify (cerca de 15 GB) | Bunny (R$ 0,235/GB, mínimo R$ 5,22) |
|---|---|---|---|---|---|---|
| 10 mil | 0,4 GB | 0,9 GB | R$ 0 | 0,4% | ok (os deploys estouram) | R$ 5,22 |
| 50 mil | 1,0 GB | 3,5 GB | R$ 0 | 1% | ok (os deploys estouram) | R$ 5,22 |
| 200 mil | 3,4 GB | 13,4 GB | R$ 0 | 3,4% a 13% | no limite | R$ 5,22 |

**Banda não é problema em nenhum cenário.**

---

## 5. Manutenção: horas por mês do Denis (com 400 ativos)

### 5.1 Fila de proventos

**Volume esperado:**

- FIIs pagam todo mês: 150 avisos por mês, cerca de **35 por semana**.
- Ações: cerca de 250 empresas com 3 a 4 anúncios por ano (bancos e algumas outras com JCP mensal ou trimestral). Dá cerca de 900 por ano, ou **17 por semana**.
- **Total: cerca de 50 avisos por semana.**

| Cenário | Minutos por aviso | Por semana | Por mês |
|---|---|---|---|
| A. Tudo manual (abrir o PDF do aviso, conferir valor e datas) | 2 a 3 | 100 a 150 min | **7 a 11 h** |
| B. Fila com sugestão automática (parser do Aviso aos Acionistas da CVM/IPE; o Denis só confirma) | cerca de 1 | cerca de 50 min | **cerca de 3,5 h** |
| C. Como B, e FII vindo do Fundos.NET estruturado (se a B3 autorizar); o Denis só vê as divergências | 1 (ações) + 0,1 (FII) | cerca de 20 min | **cerca de 1,5 h** |

O desenho previa 30 minutos por semana, mas isso vale para poucas dezenas de ativos. **Com 400 ativos, a fila de proventos é o maior custo do projeto.**

### 5.2 Outros itens

| Item | Estimativa | Base |
|---|---|---|
| Revisar alertas (testes 5, 6, 9 e 12) | 20 a 30 min por semana, cerca de **1,5 h por mês** | O MVP deu 7 alertas em 20 ativos. Com 400, a primeira leva tem cerca de 140 alertas, quase todos permanentes (desdobramento, troca de ticker, FII sem negócio). Depois disso, cerca de 10 a 20 novos por semana. |
| Temporada de resultados (teste 7, EBITDA × release, por amostra de 20 empresas) | 2 a 3 h por trimestre, cerca de **0,8 h por mês** | Teste manual do desenho |
| Cadastrar desdobramento, grupamento e troca de ticker | cerca de **0,5 h por mês** | Casos reais do MVP: SBSP3 1:5 em 04/2026; Eletrobras → AXIA3 |
| Quebra de layout (CVM, B3 ou plugin) | 1 a 3 incidentes por ano, 2 a 6 h cada (com ajuda do Claude), cerca de **0,5 h por mês** em média | Ver 5.3 |

### 5.3 O que já quebrou de verdade e o que pode quebrar

**Já aconteceu:**

1. **Informes de FII depois da Resolução CVM 175.** Os campos de identificação viraram `CNPJ_Fundo_Classe`, `Nome_Fundo_Classe` e `Tipo_Fundo_Classe`, por causa da separação entre fundo e classe. **A CVM regravou até os arquivos antigos:** o `inf_mensal_fii_2021.zip`, baixado em 02/10/2026, já vem com `CNPJ_Fundo_Classe`. Um leitor que esperava o nome antigo quebraria mesmo no histórico. CONFIRMADO pelo cabeçalho do arquivo e pelo dicionário `meta_inf_mensal_fii.zip`. O nome antigo (`CNPJ_Fundo`) e a data exata da troca: **conferir**.
2. **ISIN repetido em CNPJs diferentes** (20 casos), meses copiados e DY negativo nos informes de FII (`RELATORIO-MVP.md`, achado 8).
3. **Escala de ações em milhares sem coluna de escala** e **LPA marcado como MIL** (achados 1 e 2 do relatório).
4. **A B3 desligou o servidor FTP e os portais antigos da BM&FBOVESPA** (CE 039/2019-VPC, citado no histórico da política de market data). Quem baixava COTAHIST por FTP teve de mudar.
5. **Política de market data reescrita em 2026** (seção 3.2): não é quebra de código, mas muda a regra.
6. **Fundos.NET instável:** respondeu 520 (erro do Cloudflare) no teste do MVP.

**Pode quebrar:**

- Mudança de URL ou de layout do COTAHIST.
- Bloqueio de IP do GitHub pela CVM ou pela B3.
- CAPTCHA ou proteção anti-robô no host da B3 (o `fnet` já está atrás do Cloudflare).
- Novas colunas nos informes de FII.
- Mudança no plano de contas dos bancos.
- Mudança do plugin `iec-ferramentas` (o build já para se o trecho original mudar).
- Regras de cache do Cloudflare servindo página velha.
- Expiração do token do Cloudflare.

**Proteção que já existe no MVP:** testes bloqueantes. Se algo quebra, **a versão de ontem continua no ar** e o Actions avisa a falha por e-mail.

### 5.4 Total de horas do Denis

| Cenário | Horas por mês |
|---|---|
| Otimista (C) | 1,5 + 1,5 + 0,8 + 0,5 + 0,5 = **cerca de 5 h**. Se os alertas permanentes forem silenciados depois da primeira revisão, cai para cerca de 3 h. |
| **Provável (B)** | 3,5 + 1,5 + 0,8 + 0,5 + 0,5 = **cerca de 6 a 7 h** |
| Pessimista (A) | 11 + 1,5 + 0,8 + 0,5 + 0,5 = **cerca de 14 h** |

**Dica para reduzir:** lançar com os 20 a 50 ativos de maior volume, cobrir proventos só desses e crescer quando a fila estiver rodando.

---

## 6. Recomendação

| Item | Escolha | R$ por mês |
|---|---|---|
| Hospedagem | Cloudflare Worker com arquivos estáticos na rota `/acoes/*` e `/fiis/*` do domínio principal | **R$ 0** |
| Job diário | GitHub Actions, repositório privado, plano Free (2.000 min; uso de 170 a 370 min) | **R$ 0** |
| Dados da CVM e do BCB | ODbL, com "Fonte: CVM" e "Fonte: BCB" na página | **R$ 0** |
| Preço da B3 (COTAHIST) | Exibir só tabela e gráfico, sem download. **Perguntar à B3 antes de lançar.** | **R$ 0** (se a B3 confirmar) ou **R$ 320** (2026) / **R$ 400** (2027), se exigir licença de atraso snapshot |
| Fundos.NET | Não usar automatizado. Pedir autorização. | R$ 0 |
| Tempo do Denis | Fila de proventos com sugestão (B) | **cerca de 6 h por mês** |
| **Total** | | **R$ 0 por mês + cerca de 6 h do Denis.** Pior caso: R$ 320 por mês (R$ 400 em 2027) + 6 h. |

**Plano B:**

- **Hospedagem:**
  - (1) Pasta na HostGator por SFTP (R$ 0), se o Denis preferir não usar Worker. Exige SSH na porta 2222, o nome do servidor (não `ftp.`), confirmar que o IP do Actions não é bloqueado e limpar o cache do Cloudflare depois de cada envio.
  - (2) Subdomínio `dados.` no Cloudflare Pages (R$ 0).
- **Job:** Mac com `launchd` (R$ 0), se a CVM ou a B3 bloquearem o GitHub.
- **B3:** se a resposta for "precisa de licença" e o Denis não quiser pagar R$ 320 por mês, as páginas não podem mostrar preço nem indicador que dependa de preço. Só ficariam os dados contábeis da CVM, e o projeto perde boa parte do valor. **Essa resposta decide a viabilidade.**

---

## 7. O que precisa ser confirmado com o Denis

1. **Hospedagem:** é a HostGator? Qual plano (Start, P, M, Business ou Turbo) e quanto paga? Tem **SSH ou SFTP liberado** (porta 2222)? Qual o **nome do servidor** no cPanel? Quantos **inodes** usa hoje?
2. **Cloudflare:** em que conta está o domínio (login do Denis ou da agência)? Qual o plano (Free ou Pro)? Ele pode criar um **Worker com rota** e um **token de API** restrito a esse Worker e à limpeza de cache?
3. **Regra de cache de HTML no Cloudflare:** onde está configurada (o `cf-cache-status: REVALIDATED` mostra que existe), para criar uma exceção em `/acoes/*` e `/fiis/*`.
4. **"Always Use HTTPS"** no Cloudflare: o `http://` hoje responde 200 sem redirecionar.
5. **MX expõe o IP da origem** (108.179.253.89). Se quiser esconder, só a HostGator ou um serviço de e-mail separado resolvem. Opcional.
6. **Plano do GitHub:** Free (2.000 min) ou Pro (3.000 min)? Repositório privado `iec-ativos`?
7. **B3:** topa mandar o e-mail para `produtos-marketdata@b3.com.br` (texto da seção 3.2) e esperar a resposta antes de lançar? Aceita pagar R$ 320 por mês (R$ 400 em 2027) se for exigido?
8. **Fundos.NET:** topa pedir autorização à B3 para os "Avisos aos Cotistas – Estruturado"?
9. **Tempo:** tem cerca de 6 horas por mês para a fila de proventos com 400 ativos? Ou prefere lançar com 20 a 50 e crescer aos poucos?
10. **Mac como plano B:** o Mac fica ligado (ou só dormindo) de manhã nos dias úteis?

---

### Fontes consultadas (02/10/2026)

- BCB, PTAX venda: `api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados/ultimos/3`
- CVM, licença: API CKAN `dados.cvm.gov.br/api/3/action/package_show?id=cia_aberta-doc-dfp` e `?id=fii-doc-inf_mensal`; `inf_mensal_fii_2021.zip` e `meta_inf_mensal_fii.zip`
- B3: *Política Comercial de Market Data* v3.0.4 (15/10/2024); *Política de Consumo de Market Data B3* v1.0 e v1.1; *Política Comercial de Market Data B3 2026 V1.1* e *2027 V1.1* (página "Política comercial e contratos" em `b3.com.br`); Perguntas frequentes de distribuidores; Termos de Uso do site da B3
- Fundos.NET: `fnet.bmfbovespa.com.br/fnet/publico/abrirGerenciadorDocumentosCVM`, `gerenciador-documentos-cvm.js` e `/robots.txt` (404)
- Cloudflare (repositório público `cloudflare/cloudflare-docs`): `pages/platform/limits.mdx`, `pages/functions/pricing.mdx`, `workers/platform/limits.mdx`, `workers/static-assets/billing-and-limitations.mdx` e `workers/static-assets/routing/advanced/serving-a-subdirectory.mdx`
- GitHub (repositório público `github/docs`): `github-pages-limits.md`, `reusables/gated-features/pages.md`, `reusables/billing/actions-included-quotas.md`, `billing/reference/actions-runner-pricing.md`, `reusables/billing/actions-standard-runner-prices.md` e `actions/reference/workflows-and-actions/dependency-caching.md`
- Só por busca (os sites oficiais estão bloqueados aqui, por isso "conferir"): limites da HostGator Brasil (`suporte.hostgator.com.br`), preço do GitHub Pro, créditos da Netlify, preço da Bunny e licença do portal de dados abertos do BCB
