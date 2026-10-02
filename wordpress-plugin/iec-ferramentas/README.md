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

- `simulador-ntnb`: simulador de marcação a mercado do Tesouro IPCA+ (NTN-B).
