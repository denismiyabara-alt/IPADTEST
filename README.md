# Simulador de marcação a mercado — Tesouro IPCA+ (NTN-B)

Arquivo único, sem dependências externas: `simulador-ntnb/index.html`.

## O que ele faz

- **Choque de taxa:** mostra quanto o preço do título sobe ou cai se a taxa variar (de −3 a +3 p.p.), com a duration, a curva de sensibilidade e a comparação entre todos os vencimentos.
- **Comprei e vou vender:** a partir da data e da taxa de compra e de venda, calcula o valor na venda, os cupons recebidos, a TIR nominal e real e o efeito puro da marcação a mercado.

Metodologia: fluxos descontados por (1 + taxa)^(DU/252), cupom de 2,956301% ao semestre, dias úteis pelo calendário de feriados nacionais. O VNA é projetado pelo IPCA informado pelo usuário. Os valores são brutos, sem IR e sem custódia.

## Como colocar no site

**Opção 1: subir o arquivo e usar iframe (funciona em qualquer site)**

1. Hospede `simulador-ntnb/index.html` no seu servidor ou na biblioteca de mídia, por exemplo em `https://seusite.com.br/simulador-ntnb/`.
2. Cole na página:

```html
<iframe id="simulador-ntnb" src="https://seusite.com.br/simulador-ntnb/"
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

O script ajusta a altura do iframe automaticamente, então não fica barra de rolagem dupla.

**Opção 2: WordPress**

Use um bloco "HTML personalizado" com o iframe acima. Se o tema permitir, também dá pra colar o conteúdo do arquivo direto no bloco.

**Opção 3: GitHub Pages**

Em *Settings → Pages* deste repositório, publique a branch. O simulador fica em `https://<usuario>.github.io/<repo>/simulador-ntnb/`.
