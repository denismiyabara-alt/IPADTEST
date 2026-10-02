# Simulador de marcação a mercado — Tesouro IPCA+ (NTN-B)

Arquivo único, sem dependências externas: `simulador-ntnb/index.html`.

## O que ele faz

- **Choque de taxa:** mostra quanto o preço do título sobe ou cai se a taxa variar (de −3 a +3 p.p.), com a duration, a curva de sensibilidade e a comparação entre todos os vencimentos.
- **Comprei e vou vender:** a partir da data e da taxa de compra e de venda, calcula o valor na venda, os cupons recebidos, a TIR nominal e real e o efeito puro da marcação a mercado.

Metodologia: fluxos descontados por (1 + taxa)^(DU/252), cupom de 2,956301% ao semestre, dias úteis pelo calendário de feriados nacionais. O VNA é projetado pelo IPCA informado pelo usuário. Os valores são brutos, sem IR e sem custódia.

## Plugin WordPress (recomendado)

O jeito mais robusto de publicar é o plugin em `wordpress-plugin/`. Ele carrega o CSS e o JS como arquivos, sem colar script na página, e já vem com o visual do site.

- Pacote instalável: `wordpress-plugin/dist/iec-ferramentas.zip`
- Shortcode: `[iec_ferramenta id="simulador-ntnb"]`
- Instruções: `wordpress-plugin/iec-ferramentas/README.md`
- Para regerar o .zip: `wordpress-plugin/empacotar.sh`

## Colar direto no WordPress (alternativa)

O site [investirecocaresocomecar.com.br](https://investirecocaresocomecar.com.br/) usa endereços no padrão do WordPress. Para ele, use o arquivo **`simulador-ntnb/embed-wordpress.html`**. É um trecho pronto para colar, com o CSS isolado dentro do simulador para não brigar com o tema.

### Editor de blocos (Gutenberg)

1. No painel, vá em **Páginas → Adicionar nova**. Título sugerido: *Simulador de Marcação a Mercado do Tesouro IPCA+*.
2. Clique no **+**, procure **HTML personalizado** e adicione o bloco.
3. Abra `embed-wordpress.html` [aqui no GitHub](https://github.com/denismiyabara-alt/IPADTEST/blob/claude/friendly-shannon-jjlw8c/simulador-ntnb/embed-wordpress.html), clique em **Raw**, selecione tudo e copie.
4. Cole no bloco, clique em **Visualizar** para conferir e depois em **Publicar**.
5. Endereço sugerido (campo *slug*): `simulador-ntnb`.

### Elementor

Arraste o widget **HTML** para a página e cole o mesmo conteúdo.

### Se o simulador aparecer como texto ou sem funcionar

- Seu usuário precisa ser **Administrador**: o WordPress remove `<script>` colado por outros perfis.
- Alguns plugins de segurança ou de cache (minificação de JS) podem bloquear scripts embutidos. Exclua essa página da minificação.

## Outras formas de publicar

**Página própria + iframe:** hospede `simulador-ntnb/index.html` em qualquer servidor e incorpore com:

```html
<iframe id="simulador-ntnb" src="https://SEU-ENDERECO/simulador-ntnb/"
        style="width:100%;border:0;min-height:1400px" loading="lazy"
        title="Simulador de marcação a mercado NTN-B"></iframe>
<script>
  window.addEventListener("message", function (e) {
    if (e.data && e.data.tipo === "simulador-ntnb-altura") {
      document.getElementById("simulador-ntnb").style.height = e.data.altura + "px";
    }
  });
</script>
```

O script ajusta a altura do iframe automaticamente.

## Manutenção

Edite só o `index.html` e depois rode `python3 simulador-ntnb/build-embed.py` para regerar a versão do WordPress.
