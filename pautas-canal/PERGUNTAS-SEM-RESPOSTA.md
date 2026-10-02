# Perguntas sem resposta do canal

Fonte: `auditoria-canal/dados/comentarios_top30.csv`, com os comentários e as respostas dos 30 vídeos com mais views. A maioria desses vídeos é antiga (bancos digitais e cripto, de 2019 a 2023), e um deles é o Short do 1 centavo. A lista completa, uma pergunta por linha, está em **`perguntas.csv`**, gerada por `python3 perguntas.py`.

## Como as perguntas foram detectadas

- **Pergunta:** comentário de topo (não é resposta), escrito pelo público (não pelo canal), cujo texto casa a regra `PERGUNTA` do `analisar.py`. A regra pede que o texto tenha "?" ou comece com como, qual, quais, quando, onde, quanto, por que, o que, vale a pena, devo, compensa, alguém sabe, será que, tem como, dá pra, você acha ou faz um vídeo.
- **Sem resposta:** nenhum comentário do próprio canal responde àquela pergunta. Resposta de outro usuário não conta.
- **Resultado:** 1.777 perguntas, das quais **765 sem resposta do canal** (43%). O relatório falava em 766, porque arredondou 43,1% de 1.777; a contagem exata é 765.
- **Tema:** regras de palavras-chave no `perguntas.py`. O primeiro tema que casar leva a pergunta, então a ordem importa: imposto e cripto vêm antes de conta digital. As perguntas do Short do 1 centavo sem outro tema formam um grupo próprio.
- **Fora do escopo:** cartão de crédito, dívida pessoal e política ficam separados e não recebem rascunho.
- **Privacidade:** os textos aparecem sem autor e sem @menções (trocadas por "@…").

## Grupos

| tema | perguntas | likes | 2 exemplos (sem autor) |
|---|---|---|---|
| Short do 1 centavo: como dobra? é possível? | 194 | 5 | "Gente, se aquecer a moeda para facilitar a dobra dá certo?" · "E se eu disser que se você juntar 200 mil por mês, em um ano terá mais de 2 milhões?" |
| Outros (sem palavra-chave de tema) | 147 | 315 | "Muito vago… qual a taxa de retorno? Qual investimento?" · "Você acha que realmente vai ter queda no valor dos imóveis no Brasil?" |
| Começar a investir e juros compostos | 101 | 125 | "Poderia falar mais sobre os juros compostos?" · "Mil reais por mês em 22 anos vai dar um milhão? Não. Demora 80 anos." |
| Conta digital: tarifas, transferências e funcionamento | 83 | 110 | "Comprando bitcoin pelo app, eles poderiam mexer no meu saldo? Eu ficaria devendo se perdesse o valor investido?" · "Quando eu fizer 18 anos, o que acontece com a conta?" |
| Ações, dividendos e FIIs | 58 | 65 | "FIIs pagando 0,8% a 0,9% ao mês com base em aluguéis, depois de todos os custos…" · "E cadê as outras ações que ele já falou ter?" |
| Rendimento: quanto rende, CDB, LCI, poupança, Tesouro | 45 | 52 | "O porquinho do [banco digital] tem a segurança do FGC?" · "Se eu guardar 3 mil todo mês no CDB de uma conta digital, serve?" |
| Imposto de renda e declaração | 37 | 236 | "Queremos o vídeo da declaração, com alguém que só tem a BDR para declarar" · "Para investir em bitcoin pelo app, preciso declarar imposto de renda?" |
| Cartão de crédito (fora do escopo) | 33 | 32 | sem rascunho |
| ETFs, BDRs e exterior | 22 | 31 | "Com lock-up de 12 meses, posso aportar na BDR quando cair na estreia?" · "Esse alerta serve também para as BDRs de outros bancos?" |
| Cripto | 20 | 150 | "Novo em criptomoeda… alguém pode me orientar sobre a abordagem certa para obter um bom lucro?" (padrão de robô de golpe) · "Como posso fazer um investimento mais lucrativo em criptomoedas sem grandes perdas?" |
| Menor de idade e filhos | 12 | 87 | "Os pais conseguem monitorar tudo o que as crianças fazem?" · "Vou abrir para meu filho de 3 anos. E quanto ao IR?" |
| Política (fora do escopo) | 7 | 2 | sem rascunho |
| Dívida pessoal (fora do escopo) | 6 | 5 | sem rascunho |

**O que isso diz:**
- **O maior grupo é a desconfiança sobre a conta do Short do 1 centavo** (194 perguntas): o vídeo que mais trouxe inscritos também gerou mais dúvida. Vale um Short e um longo com a conta honesta (já estão no calendário em 25 e 26/11).
- **Imposto tem poucas perguntas, mas muitos likes** (37 perguntas, 236 likes): demanda reprimida para vídeo de declaração.
- **No grupo cripto, as perguntas mais curtidas seguem o padrão de comentário de golpe:** pedem "orientação para lucro" e atraem respostas de falsos gestores. A resposta 20 trata disso.

---

## 20 rascunhos de resposta (para o Denis aprovar)

**Regras:**
- texto neutro e educativo;
- nada de recomendar ativo ou citar corretora;
- fonte quando há regra;
- convite para um vídeo do canal quando cabe.

As regras de imposto seguem o que vale em 2026:
- JCP com 17,5% (LC 224/2025);
- FII isento com 100 cotistas ou mais (Lei 14.754/2023);
- retenção de 10% sobre dividendos acima de R$ 50 mil por mês da mesma empresa (Lei 15.270/2025).

Onde está **[conferir]**, a regra não foi rechecada nesta rodada e deve ser conferida antes de publicar.

Cada item traz o vídeo e o id do comentário, para responder no lugar certo.

### 1. "Que cálculo é este?" (Short do 1 centavo; `aDL4MMF6AnE`, comentário `UgzLtieXco1f1T5cVkR4AaABAg`) · para o Denis aprovar
> É a conta do dobro: 1 centavo dobrando 30 vezes dá 0,01 × 2³⁰ ≈ R$ 10,7 milhões. É um exercício para mostrar a força do crescimento exponencial, não um investimento: nada sério dobra todo dia. Na vida real, os juros compostos fazem a mesma curva, só que em anos. Com R$ 1.000 por mês a 6% ao ano acima da inflação, são cerca de R$ 535 mil em 22 anos. A conta completa está aqui: https://youtu.be/tbKsF2qyakU

### 2. "Mil reais por mês em 22 anos vai dar um milhão?" (`tbKsF2qyakU`, `UgxU6A1RQXY2Mva6Sth4AaABAg`) · para o Denis aprovar
> Depende da taxa. Guardando R$ 1.000 por mês sem render nada, são R$ 264 mil em 22 anos. Com 10% ao ano (nominal), são cerca de R$ 895 mil. Com 6% ao ano acima da inflação, cerca de R$ 535 mil em poder de compra de hoje, e o milhão real chega em cerca de 30 anos. Não são 80, mas também não é mágica: o que mais pesa é o tempo e a constância do aporte. Mais contas aqui: https://youtu.be/wYb9_xSNFV8

### 3. "Poderia falar mais sobre juros compostos?" (`SsZAITSAR6s`, `UgzZQDym6ZlloKAzf-N4AaABAg`) · para o Denis aprovar
> Juros compostos são juros sobre juros: o rendimento de cada mês passa a render também. No começo quase não se nota; depois de alguns anos, o rendimento do mês passa a ser maior que o próprio aporte. Tem um vídeo novo com a conta passo a passo no calendário. Por enquanto, este ajuda: https://youtu.be/wYb9_xSNFV8

### 4. "O porquinho do [banco digital] tem a segurança do FGC?" (`9tn6b8FaE24`, `UgwjQyi2ZxCNwzEg6qd4AaABAg`) · para o Denis aprovar
> Depende do que existe por trás do "porquinho". Se o dinheiro vai para um CDB, RDB, LCI ou LCA emitido por uma instituição associada ao FGC, há garantia de até R$ 250 mil por CPF por instituição, com teto de R$ 1 milhão a cada 4 anos. Se for um fundo, não tem FGC. Veja no app o nome do produto e quem é o emissor. Fonte: regulamento do FGC (fgc.org.br). Explicamos aqui: https://youtu.be/FC-eKTK3ozE

### 5. "Tenho que tirar depois de 30 dias para não cobrar IOF?" (`_WHHib_xvJ4`, `UgwThmI9huFSioW7VCl4AaABAg`) · para o Denis aprovar
> O IOF só incide se você resgatar antes de 30 dias da aplicação. Ele é regressivo: começa em 96% do rendimento no 1º dia e chega a zero no 30º. Depois disso, sobra só o IR, que também cai com o prazo: 22,5% até 180 dias e 15% acima de 720. Você não precisa tirar o dinheiro; precisa só evitar resgatar antes de 30 dias. Fontes: Decreto 6.306/2007 (tabela do IOF) e Lei 11.033/2004 (IR). [conferir: nenhuma mudança na tabela do IR em 2026]

### 6. "Se eu guardar 3 mil todo mês no CDB de uma conta digital, serve?" (`tbKsF2qyakU`, `UgxCBKUGT9-P1W258yF4AaABAg`) · para o Denis aprovar
> Serve para quê? Esta é a primeira pergunta. Para reserva de emergência, olhe três coisas: liquidez diária, rendimento perto de 100% do CDI e garantia do FGC (até R$ 250 mil por instituição). Para objetivos longos, vale comparar com outras opções de prazo maior. Sobre onde deixar a reserva: https://youtu.be/mZ6ohk9JCVY

### 7. "Tenho 80 mil; é bom colocar em LCI por 12 meses?" (`Q1WMbZZn2Ik`, `Ugz-1ZARf-sRb6ofL_J4AaABAg`) · para o Denis aprovar
> Não dá para dizer "é bom" sem saber seu objetivo, mas dá para comparar. A LCI é isenta de IR; em 12 meses, o CDB paga 17,5%. Divida a taxa da LCI por 0,825: uma LCI de 90% do CDI equivale a um CDB de cerca de 109% do CDI. Confira também a carência (você não pode resgatar antes) e o limite do FGC por instituição. A comparação está aqui: https://youtu.be/Q1WMbZZn2Ik [conferir o prazo mínimo vigente de LCI e LCA]

### 8. "Comprei 100 reais, deu 97,23 e foi subindo… rende diário?" (`4zHZprjxLu4`, `UgyGgunlpslbbwvGi6l4AaABAg`) · para o Denis aprovar
> Cripto não rende como renda fixa: o preço sobe e desce o tempo todo. Os R$ 2,77 que "sumiram" na compra são a diferença entre o preço de compra e o de venda (o spread), somada às taxas. A partir daí, o saldo acompanha a cotação. Você só realiza o ganho ou a perda quando vende.

### 9. "Para investir em bitcoin pelo app, preciso declarar?" (`4zHZprjxLu4`, `Ugzp2NFHnMSGUxGWZSp4AaABAg`) · para o Denis aprovar
> Se você é obrigado a declarar o IR, informe as criptos em Bens e Direitos pelo valor de compra quando o total de cada tipo passar do limite que a Receita fixa nas instruções do ano; na regra mais recente, R$ 5 mil. Ter cripto não gera imposto; a venda com lucro pode gerar, conforme a regra do ano. Fonte: Receita Federal, Perguntas e Respostas do IRPF. [conferir: limite e isenção na venda em 2026]

### 10. "Declarar não significa que vou pagar, né?" (`_I5dFQ6mvK0`, `UgwziBqDSLYBWZWXUyN4AaABAg`) · para o Denis aprovar
> Isso. Declarar é informar o que você tem e o que recebeu; o imposto depende de rendimentos tributáveis. Exemplo: vendas de ações de até R$ 20 mil no mês (fora day trade) são isentas, mas as ações aparecem na declaração. Passo a passo da declaração de 2026: https://youtu.be/HOJ-kcS63i8 [conferir os critérios de obrigatoriedade do ano]

### 11. "Na compra desses ETFs preciso declarar?" (`Y4WHQiKcv1g`, `UgwXj-GonSzgqdCQHR94AaABAg`) · para o Denis aprovar
> A compra em si não gera imposto. Se você é obrigado a declarar, o ETF entra em Bens e Direitos pelo custo de compra. Na venda com lucro, ETF de ações paga 15% sobre o ganho e **não** tem a isenção de R$ 20 mil por mês das ações; o DARF vence no último dia útil do mês seguinte. A tributação do rendimento distribuído depende do tipo de ETF: confira no regulamento e no informe de rendimentos. [conferir]

### 12. "É possível ficar devendo? Posso perder mais do que comprei?" (`1EGx_IxWSbo`, `UgwKIqNFiOAMSVR3WwV4AaABAg`) · para o Denis aprovar
> Comprando à vista, como cripto num app, ações ou ETF, o máximo que você perde é o que colocou. Dívida aparece só em operações alavancadas: margem, venda a descoberto, alguns derivativos e empréstimo para investir. Se você não contratou nada disso, não fica devendo.

### 13. "Comprar dentro do banco é o certo? Muitos falam para ir na corretora" (`HJRqnCA4ra0`, `UgzjZOfMHiQfiyL9G0R4AaABAg`) · para o Denis aprovar
> Os dois caminhos funcionam; o que muda é custo e variedade. Compare a taxa de corretagem e de custódia, os produtos disponíveis e o spread (em cripto). Em ações, FIIs e ETFs, os ativos ficam registrados no seu CPF na B3, seja qual for a instituição. Em cripto, veja se dá para transferir para uma carteira própria.

### 14. "Posso vender um ETF sem pagar taxas?" (`QjiF99_cINk`, `Ugy_jrkMe79u3cLZPj54AaABAg`) · para o Denis aprovar
> Taxa zero, não. Pode haver corretagem (muitas instituições zeraram), há emolumentos da bolsa (pequenos) e há imposto sobre o lucro. No Brasil, ETF de ações paga 15% sobre o ganho. No exterior, o ganho entra na declaração anual com 15% (Lei 14.754/2023). A taxa de administração não aparece na venda: ela já está descontada no preço ao longo do tempo.

### 15. "Essa taxa de 1,50 do S&P 500 é bem alta, né?" (`Y4WHQiKcv1g`, `UgxTL7qSCvZza5WzFUt4AaABAg`) · para o Denis aprovar
> Para um índice amplo, sim, é alta: muitos fundos que replicam índices cobram bem menos. A taxa é descontada todo ano. Em 10 anos, 1,5% ao ano tira cerca de 14% do patrimônio; 0,3% ao ano, cerca de 3%. Compare sempre a taxa total na lâmina do fundo.

### 16. "E se o cara está em FII para ter ganho de capital?" (`fDUsjBJQmC4`, `Ugy9o0qz9nVIalRkdHF4AaABAg`) · para o Denis aprovar
> São regras diferentes. O rendimento mensal é isento para pessoa física se o fundo tiver 100 cotistas ou mais, cotas negociadas em bolsa e você tiver menos de 10% das cotas (Lei 14.754/2023, que alterou a Lei 8.668/1993). Já o ganho na venda das cotas paga 20%, via DARF, sem isenção mensal. Quem compra FII pensando em ganho de capital paga mais imposto que quem busca renda.

### 17. "Como ficam as novas taxas criadas pelo governo?" (`QjiF99_cINk`, `UgzWu-kaLYmI8mynP454AaABAg`) · para o Denis aprovar
> O que vale em 2026 para quem investe:
> - ganhos e rendimentos no exterior: 15% na declaração anual (Lei 14.754/2023);
> - JCP: 17,5% retido na fonte (LC 224/2025);
> - dividendos acima de R$ 50 mil por mês da mesma empresa para a mesma pessoa: 10% retido na fonte (Lei 15.270/2025); abaixo disso, nada muda.
>
> Explicamos o impacto aqui: https://youtu.be/qnWje5V23Ps

### 18. "Convém tirar os investimentos do banco? Podem confiscar…" (`PoY4WqA1k5Q`, `UgzNiUNjDGEm5HMhod54AaABAg`) · para o Denis aprovar
> O medo vem do bloqueio de 1990. Desde 2001, a Constituição proíbe medida provisória que vise a "detenção ou sequestro de bens, de poupança popular ou qualquer outro ativo financeiro" (art. 62, § 1º, II). O risco mais concreto é a quebra da instituição: para isso existe o FGC (até R$ 250 mil por CPF por instituição), e o Tesouro Direto é dívida do governo federal, não do banco.

### 19. "Vou abrir para meu filho de 3 anos. E quanto ao IR?" (`V68Hd157uac`, `Ugx7qgPMuxCc5rT1ZOV4AaABAg`) · para o Denis aprovar
> Se o filho for seu dependente na declaração, o saldo e os investimentos dele entram na sua declaração, em Bens e Direitos, indicando que pertencem ao dependente; os rendimentos dele somam aos seus. Outra opção é ele não ser dependente e ter declaração própria, quando obrigado. Fonte: Receita Federal, Perguntas e Respostas do IRPF. Sobre conta para menor: https://youtu.be/SsZAITSAR6s

### 20. "Novo em cripto… alguém pode me orientar sobre a abordagem certa para obter um bom lucro?" (`1EGx_IxWSbo`, `UgxZt4SyzxxOo3PIhWN4AaABAg`, 93 likes) · para o Denis aprovar
> Atenção, pessoal: comentários assim costumam atrair respostas de "gestores" e "mentores" que pedem para chamar no WhatsApp ou no Telegram. É golpe. Ninguém sério promete lucro em cripto nem pede para você transferir dinheiro para outra pessoa operar. Se for investir, comece pequeno, numa plataforma em seu nome, e só com o que pode perder.

---

**Antes de publicar:**
- Confira os itens marcados com [conferir].
- Responda primeiro as perguntas com mais likes: 20 (93), 1, 2 e 10 (22).
- Em respostas de imposto, cite a lei como está no texto, não a interpretação.
