# Rascunho: e-mail para a B3 (market data e Fundos.NET)

**Status: rascunho. Não foi enviado. Quem envia é o Denis.**

Por que mandar: `CUSTOS.md`, seção 3. A licença dos preços da B3 é o maior risco de custo do projeto (R$ 0 ou R$ 320 por mês em 2026) e decide se as páginas podem mostrar preço. O Fundos.NET não tem termo de uso que permita coleta automatizada.

## Antes de enviar

1. Preencha os campos entre colchetes: `[...]`. Apague as linhas que não se aplicam (por exemplo, a do CNPJ, se o site for de pessoa física).
2. Se puder, mande o e-mail **do domínio do site** (por exemplo, `contato@investirecocaresocomecar.com.br`). Isso ajuda a B3 a ligar o pedido ao site.
3. Mantenha o pedido de **resposta por escrito**. Guarde a resposta junto com o `CUSTOS.md`.
4. **Não lance as páginas no domínio principal antes da resposta** (`DEPLOY.md`, passo 7).
5. Se não houver resposta em 10 dias úteis, reenvie citando a data do primeiro envio. O Fundos.NET também pode ser perguntado pelo "Fale conosco" do próprio sistema.

---

**Para:** produtos-marketdata@b3.com.br
**Assunto:** Consulta sobre licença para exibir dados de fim de dia (COTAHIST) em site educacional gratuito e uso do Fundos.NET

Prezados,

Meu nome é Denis Miyabara. Sou responsável pelo Investir e Coçar (https://investirecocaresocomecar.com.br), um site e canal de educação financeira com acesso gratuito e aberto, sem cadastro e sem assinatura. O site é mantido com anúncios do Google AdSense.

Estamos preparando páginas informativas sobre ações e fundos imobiliários. Antes de publicá-las, gostaríamos de confirmar com a B3 quais são as condições de uso dos dados.

**O que pretendemos exibir**

- **Fonte dos preços:** arquivos de Séries Históricas (COTAHIST), baixados de `bvmf.bmfbovespa.com.br/InstDados/SerHist/`, uma vez por dia, depois do fechamento.
- **Campos usados:** preço de fechamento, abertura, mínima, máxima e volume financeiro, só do mercado à vista.
- **Dados exibidos:**
  - preço de fechamento do último pregão, com a data;
  - variação em 12 meses;
  - gráfico do preço de fechamento dos últimos 5 anos;
  - indicadores calculados com o preço de fechamento e com dados públicos da CVM: valor de mercado, P/L, P/VP e dividend yield (DY).
- **Cobertura:** hoje são 20 ativos (10 ações e 10 FIIs, escolhidos pelo volume negociado) em 33 páginas. O plano é chegar a cerca de 400 ativos.
- **O que não fazemos:**
  - não exibimos dado em tempo real nem intradiário: a atualização é uma vez por dia, depois que o arquivo é publicado;
  - não oferecemos download dos preços (nem CSV, nem planilha, nem API);
  - não revendemos dados;
  - não fazemos recomendação de investimento.
- **Atribuição atual:** cada número traz a fonte e a data. Exemplo: "Fonte: B3, COTAHIST, pregão de 01/10/2026".
- **Audiência estimada do site:** [visitas por mês, do Google Analytics ou do Site Kit].

**Perguntas**

1. **Licença.** Um site gratuito e aberto, com anúncios, pode exibir os dados de fim de dia derivados do COTAHIST descritos acima (preço de fechamento, DY calculado com esse preço e histórico em gráfico) sem licença? Ou esse uso exige contrato com a B3? Lemos a Política de Consumo de Market Data B3 (v1.0 e v1.1, que vale a partir de 01/11/2026). Ela define "Atraso" incluindo os Dados de Fim de Dia B3. Não ficou claro para nós se o download público do COTAHIST está dentro dessa política.

2. **Plano e custo.** Se for preciso licença, qual se aplica? Na Política Comercial de Market Data B3 2026 V1.1 (item 4.1.1, Licenças nos Mercados Listados), encontramos a Licença de Distribuição em Atraso, modalidade Snapshot, por R$ 320,00 por mês por dataset em 2026 (R$ 400,00 na política de 2027). Gostaríamos de confirmar:
   - se é essa a licença correta;
   - quantos datasets o nosso caso conta (ações e FIIs do mercado à vista);
   - se há outros custos, como taxa de adesão ou relatórios;
   - se a contratação pode ser feita por [pessoa física / CNPJ: XX.XXX.XXX/XXXX-XX, razão social: ...].

3. **Atribuição.** Quais são as exigências de atribuição? Por exemplo: texto exato da fonte, logotipo, link para a B3, aviso de atraso ou outro aviso legal.

4. **Indicadores e gráficos.** O DY, o P/L, o P/VP, o valor de mercado e a variação em 12 meses são calculados por nós a partir do preço de fechamento. Eles contam como "gráficos e tabelas informacionais" (item 3.3.2 da Política de Consumo)? Ou têm regra própria?

5. **Fundos.NET (FIIs).** Para mostrar o rendimento por cota dos FIIs, queremos usar os documentos de "Aviso aos Cotistas – Estruturado" publicados no Fundos.NET (`fnet.bmfbovespa.com.br`). A consulta seria automatizada e lenta: no máximo 1 requisição por segundo, uma vez por dia, só dos fundos cobertos. Cada número teria o link do documento original. Não encontramos termo de uso específico do sistema.
   - Esse acesso automatizado é permitido? Se for, há condições, limites ou uma forma oficial de acesso (API ou arquivo)?
   - Se não for permitido, podemos exibir os valores conferidos manualmente nos avisos, citando o Fundos.NET como fonte?
   - Se essa pergunta for de outra área, agradeço se puderem encaminhar ou indicar o contato correto.

Peço, se possível, a resposta por escrito, para guardarmos junto com a documentação do projeto.

Obrigado pela atenção.

Atenciosamente,

Denis Miyabara
Investir e Coçar: https://investirecocaresocomecar.com.br
[e-mail de contato]
[telefone, se quiser]
[CNPJ, se houver]
