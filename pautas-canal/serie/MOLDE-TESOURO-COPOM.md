# Molde: o vídeo de Tesouro e IPCA+ de cada Copom

Um roteiro que se repete a cada reunião do Copom: só mudam os números entre colchetes. Montado em 03/10/2026. Para o
Denis aprovar.

**Por que vale repetir:** Tesouro e renda fixa é o assunto com mais inscritos esperados por longo nos últimos 12 meses:
195 por vídeo, faixa de 106 a 212, n = 5 (`TEMAS.md`). O relatório mede mediana de 142 inscritos por vídeo e 11,0 por mil
views intencionais, contra 8,8 do resto (`RELATORIO.md`, seção 2 e ação 4). Amostra pequena: trate como hipótese a
validar em 3 reuniões.

**O que os dados do canal dizem sobre o momento:** os 4 longos de Tesouro publicados em semana de Copom saíram **antes**
da decisão, e nenhum depois (`videos.csv` cruzado com as datas das reuniões no BCB):

| vídeo | publicado | reunião | momento | inscritos |
|---|---|---|---|---|
| `dHYQtxnMSrw` ÚLTIMA CHANCE… NTN-B IPCA+7% | qua 28/01/2026 | 27-28/01 | dia da decisão | 421 |
| `KMIsVEOcaLM` CUIDADO com Tesouro Direto IPCA+ 8,32% (veja antes do Copom) | ter 16/06/2026 | 16-17/06 | 1º dia | 246 |
| `tb0nwpl9mFw` NÃO INVISTA no TESOURO DIRETO AGORA… | ter 17/03/2026 | 17-18/03 | 1º dia | 142 |
| `p9wkMT4RV40` O Brasil deu calote no Tesouro Direto? | ter 15/09/2026 | 15-16/09 | 1º dia | 69 |

Não há longo de Tesouro publicado depois de uma decisão para comparar. Por isso o molde tem duas versões (pré e pós) e a
proposta é testar as duas (ver "Quando gravar e publicar").

---

## 1. O que muda a cada reunião e de onde vem

| dado | lacuna no roteiro | fonte primária | endereço (conferido em 03/10/2026) |
|---|---|---|---|
| número e datas da reunião; próxima reunião | [NUM_REUNIAO], [DATAS_REUNIAO], [PROXIMA_REUNIAO] | BCB, calendário do Copom | https://www.bcb.gov.br/controleinflacao/calendarioreunioescopom (página carrega por JavaScript; o conteúdo não veio pelo fetch daqui, conferir no navegador) |
| decisão da Selic | [SELIC_ANTERIOR], [SELIC_NOVA], [DECISAO], [DECISAO_CURTA], [TAMANHO_PP] | BCB, comunicado do Copom | página: https://www.bcb.gov.br/publicacoes/comunicadoscopom · JSON: https://www.bcb.gov.br/api/servico/sitebcb/copom/comunicados?quantidade=1 (lista) e https://www.bcb.gov.br/api/servico/sitebcb/copom/comunicados_detalhes?nro_reuniao=281 (texto). **Os dois JSON responderam daqui.** |
| votação e tom | [VOTACAO], [FRASE_TOM], [TOM] | o texto do comunicado (último parágrafo: o que o Comitê "seguirá" fazendo) | idem |
| meta Selic em vigor | [SELIC_NOVA] (confirmação) | BCB, SGS 432 | https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados/ultimos/1?formato=json (**bloqueado daqui**: o proxy devolveu 502; o `gate_qualidade.py` lê a mesma série no Mac) |
| IPCA do mês | [IPCA_MES], [IPCA_MES_REF] | BCB, SGS 433 (IBGE) | https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados/ultimos/1?formato=json (**bloqueado daqui**, 502) |
| IPCA de 12 meses | [IPCA_12M] | BCB, SGS 13522 | https://api.bcb.gov.br/dados/serie/bcdata.sgs.13522/dados/ultimos/1?formato=json (**bloqueado daqui**; valor de ago/2026 = 4,22%, lido no Mac em 02/10/2026 e salvo em `pipeline/dados/macro_bcb.json`) |
| expectativa do mercado (Focus) | [FOCUS_DATA], [FOCUS_SELIC_REUNIAO], [FOCUS_SELIC_FIM_ANO], [FOCUS_IPCA_ANO] | BCB, Focus (relatório semanal) | página: https://www.bcb.gov.br/publicacoes/focus · PDF: `https://www.bcb.gov.br/content/focus/focus/R{AAAAMMDD}.pdf`, com a data da sexta de referência (o de 25/09/2026 baixou daqui: `R20260925.pdf`) · API Olinda: https://olinda.bcb.gov.br/olinda/servico/Expectativas/versao/v1/odata/ (**bloqueado daqui**, 403) |
| taxas e preços do Tesouro, véspera e dia seguinte | [TAXA_IPCA_2029_ANTES/DEPOIS], [TAXA_IPCA_2035_ANTES], [TAXA_IPCA_2035], [TAXA_IPCA_2050_ANTES/DEPOIS], [TAXA_PRE_2032_ANTES/DEPOIS], [PU_IPCA_2035_ANTES/DEPOIS], [TAXA_SELIC_2029] | Tesouro Nacional | CSV público (Tesouro Transparente): https://www.tesourotransparente.gov.br/ckan/dataset/df56aa42-484a-4a59-8184-7676580c81e3/resource/796d2059-14e9-44e3-80c9-2d9e30b405c1/download/PrecoTaxaTesouroDireto.csv · colunas: `Tipo Titulo;Data Vencimento;Data Base;Taxa Compra Manha;Taxa Venda Manha;PU Compra Manha;PU Venda Manha;PU Base Manha` · **baixou daqui** (176.913 linhas; última data-base 01/10/2026). Site com as taxas do momento: https://www.tesourodireto.com.br/ (**bloqueado daqui**, 403; abrir no Mac) |
| curva de juros | [CURVA_PRE_2027], [CURVA_PRE_2029], [CURVA_PRE_2032] | o mesmo CSV: as taxas dos prefixados de prazos diferentes, lado a lado | idem. Opcional: curva de DI futuro da B3 ou ETTJ da ANBIMA (não conferidos nesta rodada) |
| ata | [DATA_ATA] | BCB, atas | página: https://www.bcb.gov.br/publicacoes/atascopom · JSON: https://www.bcb.gov.br/api/servico/sitebcb/copom/atas?quantidade=1 (**respondeu daqui**; a ata da 281ª saiu em 22/09/2026, terça seguinte à reunião) |

As lacunas [DIF_*] são contas: depois − antes (em p.p. para taxa, em % para preço).

**Cuidado com o CSV do Tesouro Transparente:** em 03/10/2026 (sábado) a última data-base era 01/10. Ele chega com um ou
dois dias úteis de atraso. Na quinta da gravação, a taxa "depois" vem do site do Tesouro Direto (anotar a hora); o CSV
serve para conferir depois e para guardar o histórico.

**"Taxa Compra Manha"** é a taxa para quem compra, na abertura do dia. "Antes" = manhã do dia da decisão (quarta), que
ainda não tem o comunicado. "Depois" = manhã de quinta.

---

## 2. Quando gravar e publicar

Reunião sempre em terça e quarta; o comunicado sai na quarta, a partir das 18h30 (BCB).

| quando | o que fazer | por quê |
|---|---|---|
| segunda da semana da reunião | baixar o Focus da sexta anterior e preencher [FOCUS_*] | o Focus sai às segundas (conferir o horário na página do Focus); é a última leitura do mercado antes da reunião |
| terça (1º dia), até 12h | **roteiro pronto**, só com lacunas de decisão e de taxa "depois"; taxas da manhã de terça como rascunho | tira da quinta todo o trabalho que não depende da decisão. **Versão pré (teste):** publicar às 19h o longo pré, como os 4 que funcionaram |
| quarta (2º dia), manhã | anotar as taxas da manhã: são o [*_ANTES] definitivo. Short pré-decisão (já previsto na v2: 04/11) | é o último preço sem o comunicado |
| quarta, 18h30 | ler o comunicado duas vezes. Preencher [SELIC_NOVA], [DECISAO], [VOTACAO], [FRASE_TOM]. Não gravar à noite | a reação do mercado só aparece na abertura de quinta; gravar na quarta à noite seria opinar sem o dado |
| quinta, depois da abertura do Tesouro Direto | anotar as taxas novas (site do Tesouro Direto, com a hora) → [*_DEPOIS]. Gravar entre 10h e 12h; editar à tarde | o vídeo mostra o que de fato mudou no preço do título, que é a pergunta de quem tem Tesouro |
| quinta, 19h | **publicar a versão pós** | 19h é o horário dos longos do canal (`CALENDARIO-8-SEMANAS.md`) |
| sexta ou segunda | Short derivado: "o IPCA+ subiu ou caiu depois do Copom?" | Shorts de Tesouro vivem de Pesquisa no vitalício (67%, `TEMAS.md`) |
| terça seguinte, 8h | ler a ata; se mudar o tom, comentário fixado ou post na comunidade, sem vídeo novo | a ata explica o comunicado; não justifica outro longo |

**Teste proposto:** em 03-04/11, seguir a v2 (Short na quarta 04/11 e longo pós na quinta 05/11). Em 08-09/12, publicar o
longo pré na terça 08/12 e um Short pós na quinta 10/12. Comparar inscritos e views intencionais de 7 dias. Decidir o padrão
de 2027 com as duas reuniões.

---

## 3. Roteiro-molde (versão pós, quinta)

**Título (até 60 caracteres, escolher um):**
- `Tesouro Direto depois do Copom: o que mudou no IPCA+` (52)
- `Selic a [SELIC_NOVA]%: o que muda no Tesouro IPCA+` (preencher e contar os caracteres)
- `Copom [DECISAO_CURTA] a Selic: e o seu Tesouro Direto?` (preencher e contar)

Sem "vale a pena", "hora de comprar", "trava agora" ou "melhor título" no título: o gate barra.

**Thumbnail:** "IPCA+ [TAXA_IPCA_2035]%" grande, com a seta para cima ou para baixo e "DEPOIS DO COPOM".

**Gancho (0:00 a 0:30)**
> "Ontem à noite o Copom [DECISAO] a Selic para [SELIC_NOVA]%. Hoje de manhã, o Tesouro IPCA+ 2035 abriu a
> [TAXA_IPCA_2035]%, contra [TAXA_IPCA_2035_ANTES]% ontem. Em 10 minutos: o que mudou no preço do seu título, o que o
> Banco Central disse sobre as próximas reuniões e o que isso não quer dizer."

**Bloco 1. A decisão (0:30 a 2:00)**
- [NUM_REUNIAO]ª reunião, [DATAS_REUNIAO]. Selic de [SELIC_ANTERIOR]% para [SELIC_NOVA]% ([TAMANHO_PP] p.p.).
  Votação: [VOTACAO].
- O que o mercado esperava: o Focus de [FOCUS_DATA] apontava [FOCUS_SELIC_REUNIAO]% para esta reunião. A decisão
  [veio igual / veio diferente] do esperado.
- Fonte na tela: comunicado do Copom (bcb.gov.br), com a data.

**Bloco 2. O tom (2:00 a 3:30)**
- Ler a frase que fala do futuro: "[FRASE_TOM]".
- Traduzir em uma linha: [TOM] (exemplo de forma: "o BC não prometeu nada sobre a próxima reunião").
- Lembrar: o comunicado não é promessa; a ata sai em [DATA_ATA].

**Bloco 3. O que mudou no Tesouro (3:30 a 6:30)** (a tabela na tela)

| título | manhã de quarta (antes) | manhã de quinta (depois) | diferença |
|---|---|---|---|
| Tesouro IPCA+ 2029 | [TAXA_IPCA_2029_ANTES]% | [TAXA_IPCA_2029_DEPOIS]% | [DIF_IPCA_2029] p.p. |
| Tesouro IPCA+ 2035 | [TAXA_IPCA_2035_ANTES]% | [TAXA_IPCA_2035]% | [DIF_IPCA_2035] p.p. |
| Tesouro IPCA+ 2050 | [TAXA_IPCA_2050_ANTES]% | [TAXA_IPCA_2050_DEPOIS]% | [DIF_IPCA_2050] p.p. |
| Tesouro Prefixado 2032 | [TAXA_PRE_2032_ANTES]% | [TAXA_PRE_2032_DEPOIS]% | [DIF_PRE_2032] p.p. |
| Tesouro Selic 2029 | — | [TAXA_SELIC_2029]% (acima da Selic) | — |

- Preço (PU) do IPCA+ 2035: de R$ [PU_IPCA_2035_ANTES] para R$ [PU_IPCA_2035_DEPOIS] ([DIF_PU_IPCA_2035]%). Explicar a
  regra: taxa cai, preço sobe; taxa sobe, preço cai. É a marcação a mercado (card para `KMIsVEOcaLM`).
- Curva: prefixado 2027 a [CURVA_PRE_2027]%, 2029 a [CURVA_PRE_2029]%, 2032 a [CURVA_PRE_2032]%. Mostrar se o
  mercado cobra mais ou menos para prazos longos.
- Fonte na tela: Tesouro Direto, taxas da manhã, com dia e hora.

**Bloco 4. Inflação e Focus (6:30 a 8:00)**
- IPCA de [IPCA_MES_REF]: [IPCA_MES]% no mês e [IPCA_12M]% em 12 meses (BCB/IBGE).
- Focus de [FOCUS_DATA]: IPCA de [FOCUS_IPCA_ANO]% para o ano e Selic de [FOCUS_SELIC_FIM_ANO]% no fim do ano.
  Dizer "o mercado projeta", nunca "vai ser".
- A conta do IPCA+: o título paga a inflação + [TAXA_IPCA_2035]% ao ano **se for levado até o vencimento**. Antes disso,
  o preço oscila (Bloco 3).

**Bloco 5. Objeções (8:00 a 9:30)**
- "Então é hora de comprar?" O vídeo não responde isso. Mostra a taxa de hoje, o prazo e o risco de vender antes.
- "E se eu precisar do dinheiro antes?" Venda antecipada pelo preço do dia: pode ser acima ou abaixo do que pagou
  (exemplo da tabela).
- "E o imposto?" Tabela regressiva da renda fixa, pelo tempo de aplicação (Lei 11.033/2004).

**Fechamento (9:30 a 10:00)**
- Próxima reunião: [PROXIMA_REUNIAO]. "Volto com os números no dia seguinte."
- Card: o vídeo de Tesouro mais forte do ano (`dHYQtxnMSrw`) e o episódio da série de renda mensal da semana.

### Versão pré (terça, 1º dia), para o teste
Mesmos blocos, trocando:
- gancho: "Amanhã o Copom decide a Selic. O mercado espera [FOCUS_SELIC_REUNIAO]%. Estes são os 3 números do seu Tesouro
  para olhar hoje e na quinta.";
- Bloco 1 vira "o que o mercado espera" (Focus) e Bloco 2 "o que observar no comunicado";
- Bloco 3 só com a coluna "hoje" (taxas da manhã de terça);
- sem nenhuma previsão da decisão.

---

## 4. Exemplo preenchido: 281ª reunião (15-16/09/2026)

Para testar o molde com dados reais. Tudo conferido em 03/10/2026.

- **Decisão:** Selic de 14,00% para 13,75% ao ano, corte de 0,25 p.p., em 16/09/2026; votação unânime (7 votos).
  Fonte: comunicado da 281ª reunião (API `copom/comunicados_detalhes?nro_reuniao=281`).
- **Tom (frase do comunicado):** "demanda serenidade e cautela na condução da política monetária. O Comitê seguirá
  acompanhando a evolução do cenário de forma a manter a restrição adequada para assegurar a convergência da inflação à
  meta." Leitura: nenhum compromisso com a próxima reunião.
- **Focus antes (relatório de 11/09/2026):** Selic esperada para a reunião de setembro: 13,75%; Selic no fim de 2026:
  13,75%; IPCA de 2026: 4,90%. **Focus depois (25/09/2026):** Selic no fim de 2026: 13,50%; IPCA de 2026: 4,99%. O
  corte veio igual ao esperado; o que mudou foi a projeção para o fim do ano.
- **Taxas do Tesouro, manhã de quarta 16/09 → manhã de quinta 17/09/2026** (CSV do Tesouro Transparente, Taxa Compra Manhã):

  | título | 16/09 | 17/09 | diferença |
  |---|---|---|---|
  | Tesouro IPCA+ 2029 | 7,47% | 7,43% | −0,04 p.p. |
  | Tesouro IPCA+ 2035 | 7,60% | 7,55% | −0,05 p.p. |
  | Tesouro IPCA+ 2050 | 7,23% | 7,19% | −0,04 p.p. |
  | Tesouro Prefixado 2027 | 13,58% | 13,56% | −0,02 p.p. |
  | Tesouro Prefixado 2029 | 13,89% | 13,81% | −0,08 p.p. |
  | Tesouro Prefixado 2032 | 14,30% | 14,15% | −0,15 p.p. |

  PU do IPCA+ 2035: R$ 2.519,79 → R$ 2.531,08 (+0,45%). PU do Prefixado 2032: R$ 495,48 → R$ 499,17 (+0,74%).
- **IPCA de 12 meses:** 4,22% até ago/2026 (SGS 13522, lido no Mac em 02/10/2026). O IPCA mensal de agosto (SGS 433)
  não foi lido nesta rodada: conferir.
- **Ata:** publicada em 22/09/2026.
- **O que o exemplo ensina:** com um corte já esperado, o IPCA+ quase não se mexe (−0,05 p.p.); o prefixado longo mexe
  mais. O vídeo pós precisa estar pronto para dizer "mudou pouco", sem drama.

---

## 5. O que NÃO dizer

| não dizer | por quê | dizer no lugar |
|---|---|---|
| "a Selic vai cair para X" / "o BC vai cortar de novo" | previsão como certeza | "o Focus de [data] projeta X; é projeção" |
| "trava agora" / "corre que acaba" / "última chance" | é ordem de compra | "a taxa de hoje é X; quem leva até o vencimento recebe IPCA + X" |
| "é hora de comprar" / "melhor título para você" / "vale a pena" | recomendação (o gate barra no título e avisa no texto) | "o que pesar: prazo, se pode ficar até o vencimento, o risco de vender antes" |
| "o Tesouro é garantido, não tem risco" | a marcação a mercado existe | "o risco de crédito é do Tesouro Nacional; o preço oscila até o vencimento" |
| "o BC errou" / ataque a pessoa ou governo | política está fora do canal | descrever a decisão e o texto do comunicado |
| nome de corretora ou banco | regra do canal | "no site do Tesouro Direto" ou "na sua corretora" |
| taxa sem data ("a Selic está em 13,75%") | o número muda; o gate avisa | "13,75% desde 17/09/2026" |
| JCP a 15%, FII isento "com 50 cotistas", LCI "com 90 dias" | regra velha; o gate bloqueia | JCP 17,5% (LC 224/2025); FII 100 cotistas (Lei 14.754/2023); LCI e LCA 6 meses (Res. CMN 5.215) |

---

## 6. Datas das próximas reuniões do Copom

| reunião | datas | comunicado | vídeo pós (molde) | fonte |
|---|---|---|---|---|
| 282ª | ter 03 e qua 04/11/2026 | 04/11, a partir das 18h30 | qui 05/11/2026 (já na v2) | ver abaixo |
| 283ª | ter 08 e qua 09/12/2026 | 09/12 | qui 10/12/2026 (ou pré em ter 08/12, teste) | ver abaixo |
| 2027 | 26-27/01 · 16-17/03 · 27-28/04 · 15-16/06 · 03-04/08 · 21-22/09 · 26-27/10 · 07-08/12 | no 2º dia de cada uma | a quinta seguinte: 28/01, 18/03, 29/04, 17/06, 05/08, 23/09, 28/10, 09/12 | ver abaixo |

**Fonte e grau de conferência:**
- **Fonte oficial:** calendário do Copom no BCB, https://www.bcb.gov.br/controleinflacao/calendarioreunioescopom. A página
  abriu (HTTP 200), mas o conteúdo é montado por JavaScript e não veio na leitura automática. **Conferir no bcb.gov.br**
  antes de agendar.
- **2026, confirmado em parte pelo próprio BCB:** a API de comunicados do BCB
  (https://www.bcb.gov.br/api/servico/sitebcb/copom/comunicados?quantidade=10, lida em 03/10/2026) lista as reuniões de
  2026 já feitas: 28/01 (276ª), 18/03 (277ª), 29/04 (278ª), 17/06 (279ª), 05/08 (280ª) e 16/09 (281ª). Elas batem com o
  calendário de 2026 publicado pela imprensa, que traz 03-04/11 e 08-09/12 para as que faltam (busca: CNN Brasil,
  "Calendário do Copom 2026: Banco Central divulga datas de reuniões"; InfoMoney, "Banco Central divulga calendário das
  reuniões do Copom para 2026"). 03-04/11 é também a data que a v2 já usava.
- **2027, só pela imprensa:** o BCB divulgou o calendário em 23/06/2026 (DGABC, "BC divulga calendário de reuniões do
  Copom para 2027 - 23/06/2026"; também CNN Brasil, InfoMoney, Poder360, Investidor10, Canal Rural e a conta do BCB no X).
  Segundo as matérias, as atas saem na terça seguinte às 8h, menos a de outubro, que sai na quarta (feriado de 02/11).
  **Conferir no bcb.gov.br.**
- **Domínios bloqueados nesta rede** (não contornei): www.cnnbrasil.com.br, www.infomoney.com.br e www.poder360.com.br
  (bloqueio do proxy na leitura); www.dgabc.com.br, investidor10.com.br e euqueroinvestir.com (sem conexão);
  api.bcb.gov.br (502), olinda.bcb.gov.br (403) e www.tesourodireto.com.br (403).
