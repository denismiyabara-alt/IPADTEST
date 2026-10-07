# IEC Ferramentas

Plugin WordPress das calculadoras e simuladores do Investir e Coçar. Cada ferramenta entra na página por shortcode, e o CSS e o JS são carregados como arquivos (`wp_enqueue_*`), nunca colados no conteúdo. Por isso o editor do WordPress não tem como estragar o script (como no caso do `&&` que virava `&#038;&#038;`).

PHP 7.4+, sem dependências, sem build.

## Instalar

1. **Plugins → Adicionar novo → Enviar plugin** e envie o `iec-ferramentas.zip`.
2. Ative o plugin.
3. Na página, troque o bloco HTML personalizado por um bloco **Shortcode** com:

   ```
   [iec_ferramenta id="simulador-ntnb"]
   ```

4. Limpe o cache do WP-Optimize.

O CSS só é carregado nas páginas que usam o shortcode, no `<head>`. O JS vai no rodapé. A versão dos arquivos é a data de modificação, então toda atualização fura o cache sozinha.

Se o id não existir, quem pode editar vê um aviso no lugar da ferramenta. O visitante não vê nada.

## Atributos opcionais (1.3.0)

Os shortcodes antigos continuam funcionando do mesmo jeito. A partir da 1.3.0, dá para acrescentar:

| Atributo | O que faz |
|---|---|
| `modo="compacto"` | Tira a seção explicativa ("Por que...", "Premissas") e põe uma linha: "Ferramenta educativa, não é recomendação de investimento." Útil em páginas que repetem a ferramenta muitas vezes. |
| `metodologia="/link/"` | Só no modo compacto: acrescenta "Veja as premissas e a metodologia" com esse link. Recomendado, para as premissas continuarem a um clique. |
| `<id do campo>="valor"` | Preenche o campo com esse id. Aceita só número (`1500`, `6,5`) ou data (`2026-10-02`); qualquer outra coisa é ignorada e o campo fica com o valor padrão. |

Exemplos:

```
[iec_ferramenta id="um-milhao" um-aporte="1500" um-taxa="5"]
[iec_ferramenta id="renda-fii" f-dy="0,95" modo="compacto" metodologia="/fiis/metodologia/"]
[iec_ferramenta id="jcp-liquido" jcp-por-acao="0,42" jcp-qtd="200"]
```

Os ids dos campos estão no `markup.html` de cada ferramenta (ex.: `<input id="um-aporte" ...>`). O modo compacto acrescenta `data-modo="compacto"` no contêiner.

## Adicionar uma ferramenta nova

Crie uma pasta em `ferramentas/<id>/` com três arquivos:

| Arquivo | Conteúdo |
|---|---|
| `markup.html` | Só o HTML, dentro de um contêiner com id próprio (ex.: `<div id="calc-juros" class="iec-ferramenta">`). Sem `<script>` e sem `<style>`. |
| `style.css` | Todo seletor começa pelo id do contêiner, para não vazar para o tema. |
| `app.js` | Código dentro de uma função `(function(){ ... })();` que começa procurando o contêiner e sai se não achar. Use comentários `/* */`. |

O id da pasta só pode ter letras minúsculas, números, `-` e `_`. Depois, é só usar `[iec_ferramenta id="<id>"]`.

Cada ferramenta pode aparecer uma vez por página (os ids do HTML são fixos).

## WP-Optimize

Os arquivos já funcionam com a minificação ligada. Se algum dia uma ferramenta quebrar só com a minificação ativa:

1. **WP-Optimize → Minify → JavaScript**, no campo de exclusões, adicione uma linha por arquivo:

   ```
   /wp-content/plugins/iec-ferramentas/ferramentas/simulador-ntnb/app.js
   ```

2. Se for o CSS, faça o mesmo na aba **CSS** com `.../simulador-ntnb/style.css`.
3. Clique em **Purge the minified files** e limpe o cache de página.

Handles registrados, caso o WP-Optimize ou outro plugin peça por nome:

- `iec-ferramentas-fontes` (Google Fonts: Archivo e IBM Plex Sans)
- `iec-ferramenta-<id>`, ex.: `iec-ferramenta-simulador-ntnb` (CSS e JS)

## Ferramentas incluídas

- `simulador-ntnb`: simulador de marcação a mercado do Tesouro IPCA+ (NTN-B). Contêiner `#sim-ntnb`.
- `renda-fii`: simulador de renda mensal com fundos imobiliários, reinvestindo ou não, em valores nominais e em dinheiro de hoje. Contêiner `#renda-fii`.
- `lci-lca-cdb`: calculadora LCI/LCA × CDB, com o CDB equivalente prazo a prazo. Contêiner `#calc-lci-lca`.
- `juros-anual-mensal`: conversor de taxa anual, semestral, mensal e diária. Contêiner `#juros-conv`.
- `renda-fixa-comparador`: CDB pós, prefixado, IPCA+ e LCI/LCA lado a lado, depois do IR. Contêiner `#calc-rf`.
- `perfil-investidor`: quiz de 7 perguntas (conservador, moderado ou arrojado). Contêiner `#perfil-inv`.
- `preco-justo`: preço teto de Bazin e preço justo de Graham. Contêiner `#preco-justo`.
- `um-milhao`: quanto tempo para juntar R$ 1 milhão (ou outra meta) guardando um valor por mês, com gráfico, tabela ano a ano e o inverso (quanto guardar para chegar em N anos). Contêiner `#um-milhao`. Campos: `um-aporte`, `um-inicial`, `um-taxa`, `um-meta`, `um-anos`.
- `jcp-liquido`: JCP líquido depois do IR na fonte (17,5% desde 01/01/2026, 15% antes) comparado a um dividendo do mesmo valor (isento até R$ 50 mil por mês da mesma empresa; acima, 10% retidos). Contêiner `#jcp-liquido`. Campos: `jcp-por-acao`, `jcp-qtd`, `jcp-total`, `jcp-data`.
- `aposentadoria-renda`: simulador de aposentadoria com renda passiva e INSS: patrimônio necessário (retirada ajustável, padrão 4%), quanto falta, aporte necessário e gráfico. Contêiner `#aposentadoria-renda`. Campos: `ap-idade`, `ap-alvo`, `ap-renda`, `ap-inss`, `ap-patrimonio`, `ap-aporte`, `ap-taxa`, `ap-retirada`.
- `ir-fii-venda`: IR de 20% na venda de cotas de FII, com compensação de prejuízo, dedo-duro, DARF 6015 e vencimento. Contêiner `#ir-fii-venda`. Campos: `fv-pm`, `fv-venda`, `fv-qtd`, `fv-custos`, `fv-prejuizo`, `fv-data`.

As regras de imposto e o teto do INSS citados nas ferramentas foram conferidos em 02/10/2026, cada um com a fonte na própria ferramenta. Quando a lei mudar, troque o texto no `markup.html` e a constante no `app.js`.

## Testes

Na pasta `wordpress-plugin/`:

```
node --test tests/calculos.test.js
PLAYWRIGHT=$(npm root -g)/playwright node tests/navegador.mjs
```

- `tests/calculos.test.js`: confere as contas das ferramentas novas (funções puras exportadas pelo `app.js` quando roda no Node). Sem dependências.
- `tests/navegador.mjs`: monta as páginas com o próprio plugin (`tests/pagina.php` imita o WordPress), abre as 11 ferramentas no Chromium, em tela de computador e de celular, normais e no modo compacto. Procura erro de JS e rolagem horizontal, digita valores, confere os resultados e salva prints em `prints/1.3.0/`. Precisa de PHP e Playwright.

## Versões

- 1.3.2: quiz em uma pergunta por vez, barra de progresso, resultado sobe sozinho pra tela, medidor de cagaço e botão de compartilhar no WhatsApp.
- 1.3.1: quiz de perfil vira "Qual é o seu nível de cagaço?" (Bunda na parede, Bundão, Furico aberto) e ganha captura de e-mail no Brevo (lista "Quiz Nível de Cagaço", campo PERFIL).
- 1.3.0: adiciona `um-milhao`, `jcp-liquido`, `aposentadoria-renda` e `ir-fii-venda`; atributos opcionais no shortcode (`modo="compacto"`, `metodologia` e preenchimento de campos).
- 1.2.0: adiciona `lci-lca-cdb`, `juros-anual-mensal`, `renda-fixa-comparador`, `perfil-investidor` e `preco-justo`.
- 1.1.0: adiciona `renda-fii`.
- 1.0.0: primeira versão, com `simulador-ntnb`.
