# Publicar o site de ativos no Cloudflare: passo a passo

Para o Denis. Escrito em 02/10/2026. Segue a recomendação do `CUSTOS.md` (seção 6): **Cloudflare Worker só com arquivos estáticos** nas rotas `/acoes/*`, `/fiis/*` etc. do domínio principal, e **GitHub Actions** rodando o job diário. Custo: R$ 0 por mês nos dois.

**Antes de pôr no domínio principal (passo 7), espere a resposta da B3** sobre a licença dos preços (`EMAIL-B3.md`). Os passos 1 a 6 podem ser feitos antes: eles publicam só num endereço de teste `*.workers.dev`, com `noindex`.

## O que já está pronto (e testado aqui em 02/10/2026)

| Arquivo | Para quê |
|---|---|
| `wrangler.toml` | Configuração do Worker `iec-ativos`. Ambiente padrão = **teste** (só `*.workers.dev`). Ambiente `producao` = rotas no domínio. Sem nenhum token. |
| `cloudflare/_headers` | Cabeçalhos: segurança básica, cache do sitemap (1 h) e `X-Robots-Tag: noindex` no endereço `*.workers.dev`. O HTML fica com o padrão do Cloudflare (`max-age=0, must-revalidate` + `ETag`): o navegador sempre confere se há versão nova, então **não é preciso limpar cache** depois do deploy. |
| `cloudflare/.assetsignore` | Tira do site os relatórios internos do gerador (`_relatorio.json`, `paginas.csv`, `redirects.csv`, `htaccess-exemplo.txt`, `robots-trecho.txt`). |
| `scripts/preparar_cloudflare.sh` | Copia os dois arquivos acima para `saida/` e confere o build (páginas mínimas, limite de 20.000 arquivos e de 25 MiB por arquivo). |
| `.github/workflows/diario.yml` | Job diário. **Modelo:** dentro do IPADTEST ele não roda (o GitHub só lê a pasta `.github/` da raiz do repositório). Passa a valer quando `site-ativos/` virar a raiz do `iec-ativos`. |

**Por que não há código de Worker (`main`):** os cabeçalhos de cache cabem no `_headers`, então o Worker não precisa de script. Assim, toda visita é "pedido de arquivo estático", que é grátis e ilimitado; o limite de 100.000 pedidos por dia do plano Free só conta quando um script roda (`workers/static-assets/billing-and-limitations.mdx`).

**Testes feitos aqui:**

- Build completo com rede (`python3 -m iec_ativos tudo`, numa cópia do cache): 2 min 10 s, 20 ativos, 0 bloqueados, 33 páginas (22 indexáveis), pregão de 01/10/2026.
- `pytest`: 28 testes passando.
- `wrangler 4.147.0`, `deploy --dry-run` nos dois ambientes: ok. No `producao`, o wrangler confirmou as 5 rotas e a pasta que cada uma serve.
- `wrangler dev` local: `/acoes/petr4/` responde 200 com `ETag`; `/acoes/petr4` redireciona para `/acoes/petr4/` (307); `/paginas.csv`, `/_relatorio.json` e `/_headers` dão 404; `/sitemap-ativos.xml` sai com `max-age=3600`; o host `*.workers.dev` recebe `X-Robots-Tag: noindex` e o domínio principal não.
- `actionlint` no workflow: sem erros.
- Simulei o repositório `iec-ativos` (cópia de `site-ativos/` + `vendor/iec-ferramentas` + `dados/referencia/varredura.csv`) com as variáveis do workflow: testes, build e dry-run ok.
- **Não testado:** o deploy de verdade (não há conta nem token aqui) e o workflow rodando no GitHub.

---

## 1. Criar o repositório `iec-ativos` (privado)

1. No GitHub: **New repository** → nome `iec-ativos` → **Private** → sem README.
2. No computador, copie o conteúdo versionado de `site-ativos/` para a raiz do repositório novo. O `git archive` leva também os arquivos ocultos (`.github/`, `.gitignore`, `cloudflare/.assetsignore`) e deixa de fora `cache/` e `saida/`:

   ```sh
   git clone git@github.com:<seu-usuario>/iec-ativos.git
   git -C IPADTEST archive HEAD:site-ativos | tar -x -C iec-ativos
   ```

3. Duas coisas que vêm de fora de `site-ativos/`:
   - **Plugin das calculadoras:** copie `IPADTEST/wordpress-plugin/iec-ferramentas` para `iec-ativos/vendor/iec-ferramentas` (ou adicione como submódulo nesse caminho). O workflow lê dali (`IEC_PLUGIN`).
   - **Posts do canal:** copie `IPADTEST/seo/varredura.csv` para `iec-ativos/dados/referencia/varredura.csv`. Sem ele, o bloco "Análises do canal" sai vazio (o resto funciona).
4. Commit e push na `main`.
5. Na aba **Actions** do repositório, o workflow `diario` aparece. Rode uma vez à mão (**Run workflow**). Sem os secrets, ele faz tudo e termina com o aviso "Dry-run: nada foi publicado". A primeira execução leva de 5 a 12 minutos (carga completa); as seguintes, cerca de 3.

## 2. Conta no Cloudflare

O DNS do site **já está** no Cloudflare (`CUSTOS.md`, seção 1.1). Use **a mesma conta** onde está o domínio `investirecocaresocomecar.com.br`: as rotas só funcionam na conta dona da zona. Se o domínio estiver na conta de uma agência, peça para ser adicionado como membro ou para transferir a zona.

1. Entre em `dash.cloudflare.com` com essa conta.
2. Menu **Workers & Pages**. Se for a primeira vez, o Cloudflare pede para escolher o subdomínio `*.workers.dev` da conta (exemplo: `investirecocar.workers.dev`). O endereço de teste vai ser `https://iec-ativos.<subdominio>.workers.dev/acoes/`.
3. Plano: **Free** basta.
4. Anote o **Account ID** (em **Workers & Pages**, coluna da direita, ou na página inicial da conta → menu do domínio → **API** → *Account ID*).

## 3. Token de API com permissão mínima

1. **Meu perfil → API Tokens → Create Token → Create Custom Token.**
2. Nome: `iec-ativos GitHub Actions`.
3. Permissões:

   | Tipo | Recurso | Nível |
   |---|---|---|
   | Account | Workers Scripts | Edit |
   | Zone | Workers Routes | Edit |
   | Zone | Zone | Read |

4. **Account Resources:** *Include* → só a sua conta.
5. **Zone Resources:** *Include → Specific zone* → `investirecocaresocomecar.com.br`.
6. **TTL:** ponha uma data de validade (por exemplo, 12 meses) e anote na agenda para renovar. Filtro de IP: deixe vazio (os IPs do GitHub mudam).
7. Crie e copie o token. Ele só aparece uma vez. **Não cole em arquivo, e-mail ou chat.**

**conferir no primeiro deploy:** é o mínimo que o wrangler deveria precisar para publicar um Worker com rotas (`Zone: Read` serve para ele achar a zona pelo nome). Se o deploy falhar com "Authentication error [code: 10000]", troque pelo modelo pronto **"Edit Cloudflare Workers"** (é o que a documentação do Cloudflare indica para CI), mantendo a mesma restrição de conta e de zona.

Não dê permissão de DNS nem de cache: o deploy não precisa delas.

## 4. Secrets no GitHub

No repositório `iec-ativos`: **Settings → Secrets and variables → Actions**.

- Aba **Secrets → New repository secret**:
  - `CLOUDFLARE_API_TOKEN` = o token do passo 3.
  - `CLOUDFLARE_ACCOUNT_ID` = o Account ID do passo 2.
- Aba **Variables**: **não** crie `IEC_AMBIENTE` ainda. Sem ela, o deploy vai só para o endereço de teste.

O workflow só publica se **os dois** secrets existirem. Faltando um, faz dry-run e termina com sucesso.

## 5. Primeiro deploy no endereço de teste

1. **Actions → diario → Run workflow** (deixe "Só dry-run" desmarcado).
2. No log do passo "Deploy no Cloudflare" aparecem "Publicando no endereço de TESTE" e a URL `https://iec-ativos.<subdominio>.workers.dev`.
3. Abra `https://iec-ativos.<subdominio>.workers.dev/acoes/petr4/` e `.../fiis/hglg11/`. Confira a data do pregão no cartão.
4. Os links do cabeçalho e o canonical apontam para o domínio principal (é proposital: é lá que as páginas vão morar). Por isso alguns links levam a 404 enquanto não for para produção.

## 6. Horário do job diário

O cron do GitHub é em UTC. Brasília é UTC−3 o ano todo (sem horário de verão desde 2019).

| Execução | UTC | Brasília | Dias |
|---|---|---|---|
| Principal | 05h17 | 02h17 | terça a sábado (pregões de segunda a sexta) |
| Nova tentativa | 11h47 | 08h47 | terça a sábado; só roda se a principal do dia não terminou com sucesso |

- O COTAHIST do dia sai entre 20h16 e 00h24 (Brasília). A execução principal deixa quase 2 horas de folga depois do horário mais tardio.
- Minutos "quebrados" (17 e 47) de propósito: o GitHub atrasa mais os agendamentos na hora cheia.
- Se as duas falharem, a madrugada seguinte recupera sozinha (o download traz tudo o que mudou) e o site continua com a versão anterior.
- Feriado da B3: o job roda, não acha pregão novo e o deploy não muda nada.
- O GitHub manda e-mail quando um job agendado falha (para quem editou o agendamento por último).

## 7. Ir para o domínio principal (só depois da resposta da B3)

1. **Confira que o WordPress não usa** `/acoes/`, `/fiis/`, `/comparar/` nem `/dividendos/calendario/` (abra cada um no navegador: hoje devem dar 404 do WordPress). A partir do passo 3, esses caminhos passam a ser servidos pelo Worker, e o WordPress não os vê mais.
2. Se existir `www.investirecocaresocomecar.com.br` sem redirecionar para o domínio sem `www`, crie o redirecionamento no Cloudflare antes (as rotas cobrem só o domínio sem `www`, que é o do canonical).
3. No GitHub: **Settings → Secrets and variables → Actions → Variables → New repository variable** `IEC_AMBIENTE` = `producao`.
4. **Actions → diario → Run workflow.** O log mostra "Publicando em PRODUÇÃO". O wrangler cria o Worker `iec-ativos-producao` com as rotas:
   - `investirecocaresocomecar.com.br/acoes/*`
   - `investirecocaresocomecar.com.br/fiis/*`
   - `investirecocaresocomecar.com.br/comparar/*`
   - `investirecocaresocomecar.com.br/dividendos/calendario/*`
   - `investirecocaresocomecar.com.br/sitemap-ativos.xml`
5. Teste: `https://investirecocaresocomecar.com.br/acoes/petr4/`. No terminal, `curl -sI https://investirecocaresocomecar.com.br/acoes/petr4/` deve mostrar `etag` e **não** deve mostrar `x-robots-tag`.
6. Depois de 1 ou 2 dias rodando bem:
   - acrescente ao `robots.txt` do site a linha do `robots-trecho.txt` (`Sitemap: https://investirecocaresocomecar.com.br/sitemap-ativos.xml`) e envie o sitemap no Search Console;
   - os 301 das `cotacao-*` (`redirects.csv` e `htaccess-exemplo.txt`, no artefato "relatorio" de cada execução) são um passo separado, no WordPress, quando você decidir.
7. Quando o calendário ganhar páginas mensais (`/dividendos/2026/10/`), acrescente a rota correspondente no `wrangler.toml`.

**Cache do Cloudflare:** o `CUSTOS.md` alertava que a regra de cache de HTML do site poderia servir página velha. Com o Worker na rota, a resposta vem do Worker e leva `max-age=0` + `ETag`, então isso não deve acontecer. **Conferir** no primeiro dia: a página tem de mostrar o pregão do dia anterior.

### Alternativa: subdomínio em vez de subpasta

Se preferir não mexer em caminhos do domínio principal, troque as rotas do `[env.producao]` por:

```toml
routes = [ { pattern = "dados.investirecocaresocomecar.com.br", custom_domain = true } ]
```

e gere o site com `IEC_BASE_ATIVOS=https://dados.investirecocaresocomecar.com.br` (variável de ambiente no passo "Gerar o site" do workflow). O Cloudflare cria o registro DNS sozinho. O subdomínio herda menos autoridade do domínio (`DESENHO.md`, seção 1).

---

## 8. Como voltar atrás

Do mais leve ao mais forte:

| Situação | O que fazer |
|---|---|
| Uma publicação saiu com erro | No painel: **Workers & Pages → iec-ativos-producao → Deployments** → versão anterior → **Rollback**. Ou no terminal: `npx wrangler rollback --env producao` (pede o token; use `wrangler login`). **conferir** no primeiro uso. |
| Parar as publicações automáticas | **Actions → diario → ⋯ → Disable workflow.** O site fica como está. |
| Voltar a só dry-run | Apague o secret `CLOUDFLARE_API_TOKEN`. O job continua gerando e testando, mas não publica. |
| Tirar as páginas do domínio principal (o WordPress volta a responder nesses caminhos) | Apague a variável `IEC_AMBIENTE` e, no painel, **Workers & Pages → iec-ativos-producao → Settings → Domains & Routes** → apague as 5 rotas. Ou apague o Worker inteiro: `npx wrangler delete --env producao`. |
| Apagar o endereço de teste | `npx wrangler delete` (ambiente padrão) ou pelo painel (Worker `iec-ativos`). |
| Token vazou ou não é mais usado | **Meu perfil → API Tokens → Roll** (gera outro) ou **Delete**. Depois atualize o secret no GitHub. |

Se as páginas saírem do domínio depois de indexadas, o Google vai ver 404 nelas. Para uma saída definitiva, prefira 301 para uma página do WordPress.

## 9. Conferências pendentes (marcadas "conferir" acima)

1. Permissões mínimas do token (passo 3).
2. Rollback com arquivos estáticos (passo 8).
3. Que a regra de cache de HTML do domínio não interfere nas rotas do Worker (passo 7).
4. Se a visita a uma rota do Worker sem script conta como pedido de Worker no plano Free (`CUSTOS.md`, opção d). Acompanhe em **Workers & Pages → iec-ativos-producao → Metrics** na primeira semana.
5. `/acoes/petr4` (sem barra) redireciona com **307** para `/acoes/petr4/`. Os links internos e o sitemap já usam a barra, então isso quase não acontece; se o Search Console reclamar, dá para trocar por 301 com um arquivo `_redirects`.
