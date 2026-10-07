# Notas do roteiro de 06/10/2026: FII ou imóvel alugado

Roteiro: `2026-10-06-fii-ou-imovel-alugado.md` (v1.7; a v1.4 foi a congelada, ver seções 8, 9 e 10). **Título recomendado mudou na v1.7** (seção 10). Briefing e concorrentes em `pautas-canal/briefings/`.

**Limitações (ler antes das notas).** Todos os papéis foram feitos pela mesma sessão da nuvem, em sequência, e não por
agentes separados. O ouvinte-frio, em especial, **não é uma escuta independente**: quem ouviu já sabia a tese. Os arquivos
`DNA-VOZ-DENIS.md`, `bancoes.txt`, `MECANICAS-DE-PIADA.md`, `frases-de-conexao.md`, os playbooks e o `fala_so.py` não estão
no repositório. A rubrica e o `score_roteiro.py` chegaram no meio do trabalho (commit e070069) e foram usados na v1.4.
**Rodar no Mac:** um ouvinte-frio novo de verdade e o juiz-ritmo com o DNA de voz.

---

## 1. Portão mecânico — `python3 roteiro-regras/score_roteiro.py` (v1.4)

```
ELIMINATORIOS: nenhum
  [PASSA] item  2 — 5 numero(s) no bloco 1
  [FALHA] item  3 — nao achou loop aberto ('guarda esse numero...')
  [PASSA] item  6 — 1 marcador(es) de analogia (alvo: 1, esticada)
  [PASSA] item  8 — nenhum meta-discurso
  [PASSA] item  9 — cada fato 1x
  [PASSA] item 10 — ferramenta nomeada
SIGLAS NA FALA: CVM  (traduzida na hora: "a CVM, a xerife do mercado")
ELIMINATORIOS DE COSTURA: nenhum (pontes ok, zero molde repetido)
parcial mecanico: 5/6   (exit code 1: o script só sai com 0 em 6/6)
```

**CONFLITO PORTÃO × REGRA:** o item 3 do script só reconhece o loop pela fórmula "guarda esse número / guarda o
detalhe / contraste / raciocínio". Essa fórmula e as variantes estão **proibidas desde 01/10/2026** (roteirista-tanaka
e pedido do Denis). O loop existe e está ancorado: "Oito mil e cinquenta reais de diferença por ano" (bloco 0), com
callback nos blocos 4, 5 e 7. O roteiro de 08/10 tem o mesmo FALHA no item 3. **Denis decide:** aceitar 5/6 ou o script
passa a reconhecer o loop pelo número que volta no fecho.

O que o portão pegou e foi consertado da v1.3 para a v1.4:
- molde repetido "aí você deve estar pensando" (também em 08/10 e 14/10) → "Aí você já está pensando";
- item 9: "2026", "2025", "400.000", "10%" e "R$ 15.950" em 2+ blocos (quase tudo nas cartelas) → anos falados como
  "este ano / ano passado", datas das cartelas encurtadas, cartela do bloco 4 sem repetir o R$ 15.950;
- item 10: ferramenta sem nome reconhecível → "a conta do casaco";
- 7 avisos de ouvido (frases abrindo com "ele/ela" e uma de 30 palavras com número) → substantivo repetido, frase quebrada.

## 2. Juiz-roteiro (rubrica 10/10)

### v1.0 — 7/10
```
nota: 7/10
eliminatorio: nenhum
item  6 uma analogia, em camadas .... FALHA — a balança/casaco aparece em B1, B3, B4 ("também chega na balança de casaco"), B5 e B7: metáfora em todo bloco
item  8 atitude, zero meta-discurso . FALHA — "e ele aparece daqui a pouco" (B1) e "Daqui a pouco a gente descobre" (B0)
item  9 arco linear, cada fato 1x ... FALHA — "quinze mil, novecentos e cinquenta" repetido 3x em B3–B4; "o fundo já tirou o mês vazio" dito em B1 e de novo em B4
(demais itens PASSA)
para_corrigir:
- item 6: tirar a imagem do bloco 4
- item 8: tirar as duas referências ao andamento do vídeo
- item 9: um 15.950 a menos; a explicação de "rendimento já líquido" fica num bloco só
```

### v1.1 em diante — 10/10 (conferido de novo na v1.4, depois dos ajustes do portão)
```
nota: 10/10
eliminatorio: nenhum
item  1 clique confirmado ≤15s ...... PASSA — "Só que, em 2026, esse mesmo aluguel chega no seu bolso de dois jeitos. Num deles, chegam os vinte e quatro mil. No outro, chega menos de dezesseis mil."
item  2 número ancorado <20s ........ PASSA — "Oito mil e cinquenta reais de diferença por ano. Mesmo aluguel. Mesmo apartamento."
item  3 loop = número ANCORADO ...... PASSA — "Oito mil e cinquenta reais de diferença por ano" → volta em B4, B5 e B7 ("Oito mil e cinquenta reais por ano.")
item  4 agregado → linha ............ PASSA — "Num fundo com dezenas de imóveis, um prédio vazio é uma linha no relatório. No seu apartamento, a vacância só tem dois valores: zero ou cem por cento."
item  5 prova no espectador ......... PASSA — "Fácil, por quantos meses no ano? O corretor não falou. Você completou sozinho: doze."
item  6 uma analogia, em camadas .... PASSA — B1 "quem se pesou de casaco e bota" · B3 "A segunda peça do casaco é a mais pesada" · B5 "Você não sobe na balança do banheiro desde a pandemia" · B7 "você faz a conta do casaco"
item  7 violação benigna + concessão  PASSA — alvo: anúncio/corretor/leão/gestor; concessão: "E eu não vou fingir que a cota não pesa." e "noventa e sete tinham um imóvel só"
item  8 atitude, zero meta-discurso . PASSA — "A isenção dos cinco mil é uma ótima notícia. Pra quem não tem salário."
item  9 arco linear, cada fato 1x ... PASSA — 15.950 só na conta (B3) e na comparação dos dois lados (B4); 400 mil é premissa
item 10 fecho = ferramenta NOMEADA .. PASSA — "Antes de dizer que o apê rende mais, Tanaka, você faz a conta do casaco: pega o aluguel, multiplica por onze meses, tira o leão, divide pelo preço..."
10b mesmo sujeito .................. PASSA — camada 1: o aluguel do apartamento pesado de casaco; camada final: o Tanaka tira o casaco do mesmo apartamento na mesma balança
elim. costura A — pontes ........... OK — nenhuma frase de abertura descreve o vídeo
elim. costura B — molde repetido ... OK — portão: zero sequência de 5 palavras em 3+ vídeos
para_corrigir: nenhum
```
Checagens extras (29/09): nenhuma afirmação de inexistência; dúvida nº 1 da audiência ("a cota cai, o imóvel não")
respondida no bloco 5; o gancho não entrega o mecanismo (não diz qual lado nem por quê); bloco "o que pesa de cada
lado" com disclaimer ("sem recomendação nenhuma, tá bom?") e os dois lados com número de fonte; nenhuma frase soa como
"compre/venda". Real × nominal: o roteiro compara só renda corrente de imóvel com renda corrente de fundo; CDI fora.

## 3. Juiz-ritmo (piada + conexão)

```
piada: 8/10
  beats por bloco: B0 2 · B1 2 · B2 2 · B3 3 · B4 2 · B5 4 · B6 3 · B7 0 (total 18)
  mecânicas: cena doméstica exagerada (B1, B2, B4, B5) · reversão no rabo da frase (B3, B5, B6)
  cena de vergonha: "Você não sobe na balança do banheiro desde a pandemia e jura que continua com o mesmo peso." (B5)
  piada explicada: nenhuma
  voz: vrau 1 · Tanacão 1 · viu? 1 · tá bom? 1
  melhores 3 beats: "Esse é outro vídeo. E outro advogado." · "A isenção dos cinco mil é uma ótima notícia. Pra quem não tem salário." · "A calça discorda."
  blocos sem beat: B7 (fecho, permitido)
punch-up aplicado na v1.2 (só adição):
  - [B4] "O leão não some. O leão só não entra em fundo cheio."
  - [B5] "A calça discorda."
  - [B6] "Nenhum gestor cobra taxa de você. No máximo a imobiliária."
  - [B6] "Precisou de uma parte? Não dá pra vender a cozinha."
conexao: 8/10 (depois do punch-up; era 7)
  viradas: B0→B1 1 · B1→B2 2 · B2→B3 2 · B3→B4 2 · B4→B5 2 · B5→B6 1 · B6→B7 2
  pontes aplicadas:
  - [B4→B5] fim novo: "Ainda assim, tem gente que vendeu o apartamento, comprou cota de fundo e hoje abre a carteira e vê tudo no vermelho." (puxa a objeção do B5)
  - [B5→B6] começo novo: "Nenhum dos dois é santo." (carrega "ele não te avisa")
  - [B6→B7] fim novo: "Porque é no mês vazio que o aluguel do anúncio começa a escapar." (devolve o 8.050)
veredito: PASSA
```

## 4. Ouvinte-frio (ESCUTA NÃO INDEPENDENTE — ver limitações)

```
### B0  nota 9 — dois mil por mês, vinte e quatro mil no ano, um caminho dá menos de dezesseis mil: oito mil e cinquenta de diferença.
### B1  nota 8 — travou na v1.1: "Os dois falam em seis por cento ao ano" (de onde saiu o seis?) → v1.3 diz "Dois mil por mês, num apartamento de quatrocentos mil. No ano, dá seis por cento do preço."
### B2  nota 8 — travou: "vacância" → v1.3 traduz ("Vacância é o nome chique de imóvel vazio."). 176 de 2.018 vazios; onze aluguéis = vinte e dois mil.
### B3  nota 8 — "sete mil, trezentos e cinquenta" é corte do salário, não do aluguel: entendi. 6.050 de leão, sobram 15.950.
### B4  nota 7 → 8 — travou: "o que sobrou" (qual número?) → v1.3 repete "os quinze mil, novecentos e cinquenta"; "patrimônio do fundo" → traduzido ("o valor dos imóveis e do caixa dele, dividido pelas cotas").
### B5  nota 8 — cota cai 10%, quarenta mil; cinco anos de vantagem.
### B6  nota 8 — 97 de 272 fundos com um imóvel só; MP de 5% derrubada.
### B7  nota 9 — conta do casaco: aluguel × 11, menos leão, dividido pelo preço de venda.
conta central recontada: 2.000 × 11 = 22.000; leão de 27,5% = 6.050; sobra 15.950 ≈ 4% de 400 mil; fundo a 6% isento = 24.000; diferença 8.050 por ano.
média: 8,3/10 · blocos abaixo de 7: nenhum
veredito: PASSA (congelado; os ajustes da v1.4 foram exigência do portão mecânico, não reescrita)
```

## 5. Empacotador-yt

```
titulo_1: "Apê alugado ou fundo imobiliário: o mesmo aluguel chega R$ 8 mil menor em 2026"   frame: revelacao   por que: R$ âncora + ano + tensão; responde ao erro do 26/06 (pergunta genérica)
titulo_2: "Imóvel alugado rende 6%? Depois do mês vazio e do leão, sobra 4%"                frame: revelacao   por que: o número que o anúncio mostra contra o que chega no bolso
titulo_3: "FII ou imóvel alugado em 2026: a conta que o anúncio do apartamento não faz"     frame: revelacao   por que: mantém o termo de busca ("FII", "imóvel alugado") para a Pesquisa
recomendado: 1

cumpre_nos_15s: "Só que, em 2026, esse mesmo aluguel chega no seu bolso de dois jeitos. Num deles, chegam os vinte e quatro mil. No outro, chega menos de dezesseis mil."
gap_fecha_em: bloco 3 (o leão) e bloco 4 (a comparação)

thumbnail_prompt: "Denis standing on a bathroom scale, holding a small apartment building model wearing a tiny winter coat and boots, skeptical raised eyebrow looking at the scale display, clean bright bathroom background, high-contrast YouTube thumbnail style, soft key light from the left, 1280x720"
thumb_texto: "6% → 4%"
thumb_conta: o rendimento encolhendo (o título dá o R$; a thumb dá a porcentagem e a imagem do casaco). R$ só no título.
meme: nenhum entre 0:08 e 0:20.
```
Nota sobre o termo de busca: o calendário associa "fundo imobiliario". O título 1 tem "fundo imobiliário" literal; o 3
tem "FII". Se o Denis quiser priorizar a Pesquisa (que trouxe só 13 views ao vídeo de 26/06), vale o teste A/B 1 × 3.

## 6. Tabela número → fonte

| Número falado | Onde | Fonte | Situação |
|---|---|---|---|
| R$ 2.000/mês, R$ 400 mil, 6% ao ano | B0, B1, B4 | **hipótese** ("se"), em linha com FipeZap ago/26 = 6,14% a.a. | FipeZap só por snippet (PDF bloqueado) — Denis confere |
| 2.018 imóveis prontos; 176 totalmente vazios (quase 1 em 11) | B2 | CVM, informe trimestral de FII, 30/06/2026, fundos com negociação em bolsa | conferido na primária (dados.cvm.gov.br) |
| 1 mês vazio por ano → 11 aluguéis → R$ 22.000 | B2 | hipótese, ordem de grandeza do 176/2.018 | conta |
| R$ 5.000/mês isento; R$ 7.350; 27,5% (faixa só na cartela; na fala: "até cinco mil... acima disso, o desconto vai sumindo") | B3 | Lei 15.270/2025 e tabela do IRPF 2026 (briefing L3) | **conferido na primária em 07/10/2026** (planalto, Lei 15.270 art. 2º → art. 3º-A da Lei 9.250; Receita, tabelas 2026: máx. 27,5%) — seção 12 |
| Caso 1, dono com salário acima de R$ 7.350: R$ 6.050 de IR; sobra R$ 15.950; ≈ 4% | B3, B4 | hipótese ("primeiro caso") + conta: 22.000 × 27,5%; 22.000 − 6.050; 15.950 ÷ 400.000 = 3,99% (briefing L3/L4, seção 4) | conta |
| Caso 2, aluguel como única renda: R$ 2.000/mês < R$ 5.000 → IR zero; ficam R$ 22.000 | B3, B4 | hipótese ("segundo caso") + regra L3 (zero até R$ 5.000/mês de renda tributável) e L4 (carnê-leão, soma no ajuste: 22.000/ano < 12 × 5.000 = 60.000) | conta + lei **conferida na primária em 07/10/2026** (seção 12) |
| R$ 24.000 no fundo, isento; diferença R$ 8.050 (caso 1) e R$ 2.000 (caso 2) | B0, B4, B5, B7 | conta: 400.000 × 6%; 24.000 − 15.950; 24.000 − 22.000; isenção pela Lei 11.033 art. 3º (red. Lei 14.754) | conta + lei (conferida no planalto em 07/10/2026) |
| 100 cotistas; menos de 10% das cotas | B4 | Lei 11.033/2004, art. 3º, III e § 1º, I e II (o 100 é da Lei 14.754/2023; o 10% vem da Lei 11.196/2005, red. Lei 14.130/2021) | **conferido no planalto em 07/10/2026**; cartela corrigida (seção 12) |
| 48 fundos abertos ao público com menos de 100 cotistas | só cartela B4 | CVM, informe mensal ago/2026 | conferido na primária |
| 7,8% (mediana, 12 meses até ago/26, sobre o patrimônio) | B4 | CVM, informe mensal, soma do Dividend_Yield_Mes set/25–ago/26, 290 fundos listados com 100+ cotistas | conferido na primária |
| 10% de queda = R$ 40 mil; 5 anos de vantagem (caso 1); 20 anos (caso 2) | B5 | hipótese ("se") e conta (8.050 × 5 = 40.250; 2.000 × 20 = 40.000) | conta |
| MP de 5% sobre rendimento de FII, derrubada em outubro de 2025 | B6 | MP 1.303/2025, art. 44 e art. 75, I; Ato Declaratório do Presidente da Mesa do CN nº 67/2025 | **conferido no planalto em 07/10/2026**; cartela corrigida (seção 12) |
| 97 de 272 fundos com um imóvel só | B6 | CVM, informe trimestral 30/06/2026 | conferido na primária |

## 7. Validações que só o Denis faz

1. **Resolvida (conferido na primária em 07/10/2026, seção 12; cartela do B4 com a lei corrigida):** Lei 14.754/2023 / Lei 11.033, art. 3º: 100 cotistas e menos de 10% das cotas (B4 e cartela).
2. **Resolvida (conferido na primária em 07/10/2026, seção 12):** Lei 15.270/2025: quem tem salário acima de R$ 7.350 por mês paga 27,5% na margem sobre o aluguel em 2026 (B3);
   e, desde a v1.7, quem tem o aluguel de R$ 2.000/mês como única renda tributável paga zero (seção 10).
   A conta ignora deduções do carnê-leão (IPTU, condomínio, taxa da imobiliária pagos pelo dono): se quiser, uma frase na
   cartela.
3. **Resolvida (conferido na primária em 07/10/2026, seção 12; cartela do B6 corrigida):** MP 1.303/2025: 5% sobre rendimento de FII a partir de 2026 e perda de validade em 08/10/2025 (B6). Fica com o Denis só o verbo da fala, "a Câmara derrubou" (a primária diz que a MP perdeu a validade; o papel da Câmara é imprensa).
4. **FipeZap de ago/2026:** se 6% ao ano bruto continua honesto como hipótese (o snippet diz 6,14%). **CONFERIR NO MAC:** fipe.org.br e downloads.fipe.org.br seguem bloqueados em 07/10/2026.
5. **"Cota de fundo com bastante negócio você vende no mesmo dia"** (B5): a frase é qualitativa; confirmar que não soa
   como promessa de liquidez.
6. **Rodar no Mac:** ouvinte-frio novo (este não foi independente) e juiz-ritmo com o DNA de voz; o portão já rodou aqui.
7. **Item 3 do portão** (seção 1): decidir sobre o conflito com a proibição de "guarda esse número".

---

## 8. Revisão independente (03/10/2026, sessão separada que não escreveu o roteiro)

**A conta é justa? Sim na aritmética e no lado do apartamento; tinha dois pontos de enquadramento que favoreciam o fundo, corrigidos na v1.5.**

Conferido contra o briefing, passo a passo: 2.000 × 11 = 22.000 · 22.000 × 27,5% = 6.050 · 22.000 − 6.050 = 15.950 ·
15.950 ÷ 400.000 = 3,99% · 400.000 × 6% = 24.000 · 24.000 − 15.950 = 8.050 · 8.050 × 5 = 40.250 ≈ 10% de 400 mil. Tudo
bate. A margem de 27,5% para quem tem salário acima de R$ 7.350 é coerente com a Lei 15.270 (L3, secundária); a isenção
do FII com 100 cotistas e menos de 10% (Lei 14.754, L1/L2, secundária) está dita na fala e as três condições na cartela.

O que é honesto e já estava lá:
- O vídeo **diz** que o 6% do apartamento é bruto e o do fundo é líquido (B1: "Os dois números parecem iguais. Só um deles
  já tirou a roupa."; B4: "o rendimento do fundo já sai depois dos imóveis vazios e das despesas dele"). Essa assimetria é
  a tese, não um truque: o 6% do fundo é uma hipótese "se", abaixo da mediana CVM, e não um 6% bruto disfarçado.
- O lado do apartamento é **favorecido**, não prejudicado: a conta não tira o condomínio/IPTU do mês vazio, nem a taxa da
  imobiliária, nem manutenção. (Ignora as deduções do carnê-leão, mas elas só existem sobre custos que a conta também não
  tirou.) Logo, os R$ 8.050 são conservadores contra o fundo pelo lado do imóvel.
- O 1 mês vazio (8,3%) contra os 176/2.018 (8,7%) é ordem de grandeza: o dado da CVM é foto de imóveis 100% vazios em
  30/06, não tempo médio de vacância. A fala diz "mais ou menos a mesma proporção": aceitável.
- Contraponto presente: risco de cota (B5, 10% = 40 mil = 5 anos de vantagem), liquidez dos dois lados (B5), concentração
  (B6, 97 de 272), gestor decide (B6), lei muda (B6, MP 1.303). Nenhum fundo pelo nome, nenhuma corretora, disclaimer
  "sem recomendação nenhuma, tá bom?" no B6, nenhuma frase de compra/venda.

O que **não** era justo e foi mudado:
1. **B0 "Mesmo aluguel. Mesmo apartamento."** era falso ao pé da letra: se o *mesmo apartamento* estivesse dentro de um
   fundo, ele também teria o mês vazio e a taxa do gestor; só o imposto mudaria. O 24 mil é o de um fundo que paga 6% sobre
   os mesmos 400 mil. → "Mesmo dinheiro investido. Mesmo aluguel no papel." (frontmatter `numero_ancorado_trecho` atualizado.)
2. **A mediana de 7,8% como prova de que 6% "não é chute"** mistura fundos de tijolo com fundos de papel (CRI), cuja
   renda é juro, num ano de Selic a 13,75%: seria comparar renda de juro nominal com aluguel (o defeito do P2). Refiz na
   primária (CVM, mesmos arquivos e o mesmo recorte do C5, n = 290, script em scratchpad): fundos com ≥ 50% do ativo
   investido em imóvel: **mediana 6,96% (n = 139; 56 abaixo de 6%)**; com ≥ 50% em CRI/LCI: **11,41% (n = 75)**; por
   segmento declarado, Logística 7,52%, Shoppings 7,40%, Escritórios 4,76%, Residencial 1,93% (n = 19). Conclusão: o 6%
   continua **abaixo da mediana dos fundos de imóvel**, então a hipótese segue honesta, mas a mediana de 7,8% superestima
   a folga. → Três frases novas no B4, **sem número novo na fala**: "Só que essa mediana mistura fundo dono de prédio com
   fundo que empresta dinheiro pro setor imobiliário. / O fundo que empresta vive de juro, e o juro puxa a mediana pra
   cima. / Por causa dessa mistura, a conta dá pro fundo seis por cento, e não a mediana." Cartela do B4 ganhou
   "(mistura fundos de imóvel e fundos de crédito imobiliário)".
3. **O que já está descontado no fundo** ficou explícito: "depois dos imóveis vazios, das despesas e da taxa do gestor".
4. **O lado do apartamento é favorecido** e o vídeo não dizia: B2 ganhou "E olha que eu nem tirei o condomínio do mês
   vazio." (sem número).

Juiz-roteiro / juiz-ritmo (leitura independente, sem refazer as notas):
- **"Esse é outro vídeo. E outro advogado."** depois de "o inquilino que sumiu com a chave" não fechava: quem some com a
  chave não chama advogado; quem para de pagar, sim (despejo). → "E não, não é o inquilino que parou de pagar. / Aí já é
  outro vídeo. E outro advogado." Agora a piada se entende ouvindo.
- O resto soa falado, não traduzido: "A calça discorda.", "onde só mora a poeira", "Pra quem não tem salário.", "Não dá pra
  vender a cozinha." funcionam em português do Brasil. Nenhuma palavra da lista anti-IA. "Escolhe o seu chefe, Tanacão"
  não é recomendação (é piada sobre gestor × síndico). Trechos de pronúncia mais longos, mas legíveis no teleprompter:
  "Os fundos imobiliários contam a vacância pra CVM, a xerife do mercado, de três em três meses, imóvel por imóvel." e a
  frase do patrimônio no B4 — mantidos.
- Ressalva de rubrica (não mexi): o B0 diz "Num deles, chegam os vinte e quatro mil" sem "se"; o "se" só chega no B4.
  É gancho; o juiz anterior aceitou. Denis decide.
- Os acréscimos do B4 adicionam ~35 palavras ao bloco mais denso; não houve ouvinte-frio novo nesta revisão.

Portão (v1.5): `ELIMINATORIOS: nenhum` · 5/6 (o mesmo FALHA do item 3, conflito com a proibição de "guarda esse número",
seção 1) · costura: nenhum · CVM traduzida na hora. Avisos de ouvido: nenhum.

Validações novas para o Denis:
8. **Mediana por tipo de fundo** (item 2 acima): se quiser trocar o 7,8% da fala por um número só de fundos de imóvel
   (≈ 7%, n = 139, critério ≥ 50% do ativo em imóvel), é número novo: conferir o critério e o arquivo antes.
9. **Segmento residencial:** os 19 fundos residenciais listados têm mediana de 1,93% em 12 meses. Se algum comentário
   perguntar "e fundo de apartamento?", a resposta não é o 6%. Fora da fala; só para o Denis saber.
10. Rodar um **ouvinte-frio novo** no B4 (três frases novas).

---

## 9. Ouvinte-frio cego (v1.5) e correções v1.6

Ouvinte-frio **cego** (sessão separada, leu só a fala, `scratchpad/fala-0610.txt`): **REPROVOU a v1.5, média 7,5**.
Bloco "fundo, isenção e mediana" com nota 5 e marcado como ponto de abandono. O mais grave não foi de clareza: ele
sentiu que o vídeo inteiro empurra pro fundo, e o canal não recomenda. Perguntou: "e a valorização do apartamento?
Ninguém falou disso." Correções da v1.6 (só a fala e as cartelas; nenhum número fora do briefing):

1. **Empurrão pro fundo.** B0: "No fim da conta, metade de vocês vai querer apagar o comentário." → "Nenhuma das duas
   respostas está errada. / Errada costuma ser a conta que a gente faz antes de responder." B5 ganhou a valorização,
   qualitativa, sem número: "E vale o contrário. / Se o apartamento subir de preço nesses anos, essa subida não entrou na
   conta dos oito mil e cinquenta. / Os oito mil e cinquenta são só a renda. / Valorização é outra conta, e ela vale pros
   dois lados: o apartamento pode subir ou cair, e a cota também." (o briefing, seção 4, declara que a conta ignora
   valorização e oscilação da cota). Fecho reescrito: sai "É o apartamento que chega na balança de casaco"; a moral agora
   é "a comparação estava torta" e "os dois sem casaco". O "sem recomendação nenhuma" do B6 ficou.
2. **B4 (mediana, patrimônio por cota).** Fala reduzida a: "metade dos fundos que passam nesse corte pagou mais de sete
   vírgula oito por cento. A outra metade pagou menos. / Nessa conta entram fundos que emprestam dinheiro e vivem de juro,
   e o juro puxa pra cima. / Por isso eu usei seis, mais baixo, pra não roubar a favor do fundo." Saíram da fala
   "mediana", "patrimônio... dividido pelas cotas", "Por causa dessa mistura..." e "Ainda assim, tem gente que vendeu o
   apartamento...". O "sobre o valor patrimonial, não sobre o preço de tela" e a mistura tijolo/crédito foram pra [TELA].
3. **B1.** A frase longa da comparação vinha antes do casaco: agora os dois seis por cento vêm primeiro e o casaco
   depois, em duas frases curtas ("Só que o aluguel do anúncio se pesou de casaco e bota. / O rendimento do fundo subiu
   na balança sem roupa."). O "o fundo sobe na balança todo dia" do B1 (balança com outro sentido) virou "o preço da cota
   aparece na tela todo dia"; no B5 a troca é dita: "Só que aqui a balança pesa outra coisa: não é a renda, é o preço."
4. **Vacância** agora chega depois da explicação: "contam pra CVM... quanto de cada imóvel está vazio. / ... / Esse vazio
   tem nome chique: vacância."
5. **De onde vem o 7.350** (L3): "Entre cinco mil e sete mil, trezentos e cinquenta, o desconto vai diminuindo. / Acima
   de sete mil, trezentos e cinquenta, vale a tabela de sempre, com a alíquota cheia."
6. **Piadas que não pegaram:** "E essa peça tem juba." → "A segunda peça do casaco é a mais pesada: o imposto de renda,
   o leão."; "Vrau." saiu; "Tanacão" → "Tanaka" (não aparece mais em lugar nenhum).
7. **MP de 5%** em três frases: governo mandou a MP / "Seriam cinco por cento, a partir deste ano." / "Em outubro, a
   Câmara derrubou, e a proposta caiu."
8. **Fecho** em frases curtas: pega o aluguel × onze meses / tira o leão / divide pelo preço de hoje / valorização fora
   nos dois lados / "Aí sim você põe o apartamento do lado do fundo, os dois sem casaco."

Portão (v1.6): `ELIMINATORIOS: nenhum` · 5/6 (o mesmo FALHA do item 3, conflito da seção 1) · costura: nenhum · CVM
traduzida na hora. Fala limpa em `scratchpad/fala-0610-v16.txt` (174 linhas, 1.698 palavras, ≈ 11:45).
Nota de processo: esta passada **cortou** frases (B4 e "Vrau"), contra a regra "conserto só adiciona"; foi pedido
explícito, porque o resíduo era densidade. **Falta:** novo ouvinte-frio cego na v1.6 antes do Drive.

---

## 10. Ouvinte-frio cego (v1.6) e correções v1.7

Ouvinte-frio **cego** (sessão separada, leu só `scratchpad/fala-0610-v16.txt`; persona: dono de apê herdado, desconfia
de FII): **REPROVOU a v1.6, média 7,75**, bloco do preço da cota com nota 6. O ponto mais grave foi de honestidade: a
conta assume salário acima de R$ 7.350 (27,5% na margem) e o ouvinte, que ganha menos, sentiu que o vídeo trata isso
como regra de todo mundo; "A isenção dos cinco mil é uma ótima notícia. / Pra quem não tem salário." soou deboche.

**O que o briefing sustenta sobre quem vive só do aluguel.** L3 (Lei 15.270/2025, secundária): imposto zero até
R$ 5.000/mês de **renda tributável**, redutor até R$ 7.350. L4: aluguel de pessoa física paga pelo carnê-leão e **soma
no ajuste anual**. Logo, se os R$ 2.000/mês forem a única renda tributável da pessoa, ela fica abaixo de R$ 5.000 por
mês (e 22.000 no ano < 60.000): **IR zero sobre o aluguel**. Conta: o apê entrega 22.000; o fundo a 6%, 24.000;
diferença **24.000 − 22.000 = R$ 2.000 por ano, só o mês vazio**. Contraprova do B5: 40.000 ÷ 2.000 = 20 anos.
O briefing **não** separa o carnê-leão mensal do ajuste nem diz se aposentadoria/pensão contam (contam como renda
tributável, e aí a pessoa volta pro caso do meio). A fala diz "o aluguel é a sua única renda", que é o caso que o
briefing cobre. **Denis valida:** Resolvida (conferido na primária em 07/10/2026, seção 12): (a) que o redutor da Lei 15.270 vale também no carnê-leão mensal, não só no ajuste;
(b) que R$ 2.000/mês de aluguel como única renda tributável dá IR zero em 2026.

Correções da v1.7 (só a fala e as cartelas; nenhum número fora do briefing e das contas declaradas):

1. **Honestidade da conta.** B0: depois do 8.050, "Esse é o caso de quem já tem salário. / Pra quem vive só do aluguel,
   a diferença é bem menor." B3: a faixa do imposto saiu da voz ("Acima disso, o desconto vai sumindo, até voltar a
   tabela de sempre."; faixa completa na [TELA]); "o leão soma o aluguel com o resto da sua renda. / Então quanto o
   leão morde depende de quanto você já ganha."; **primeiro caso** (salário acima de 7.350: 6.050 de leão, sobram
   15.950) e **segundo caso** ("o aluguel é a sua única renda... o leão não leva nada, e os vinte e dois mil ficam
   inteiros. / Pra esse dono, a lei nova é uma notícia boa de verdade."); "quem ganha entre um caso e o outro fica no
   meio do caminho". Saiu "Pra quem não tem salário." B4: os dois resultados e "Pra quem ganha bem, oito mil. Pra quem
   vive só do aluguel, dois mil. / Quem decide o tamanho da diferença é o leão." B5: "Pra quem vive só do aluguel, são
   vinte anos de vantagem." B7: "Oito mil pra quem tem salário. Dois mil pra quem vive do aluguel." e "Tira o leão. O
   seu leão, do tamanho da sua renda." Cartelas de B3, B4, B5 e B7 com os dois cenários; tabela da seção 6 atualizada.
2. **Bloco do preço (B5, agora "O preço na tela").** Saiu a balança inteira (pandemia/calça/farmácia e "aqui a balança
   pesa outra coisa"). Entrou: "A cota do fundo tem preço na tela do app todo dia" / "O apartamento não tem preço na
   tela. / Você só descobre quanto o apartamento vale quando tenta vender." Equilíbrio no lugar de "ele não te avisa":
   "Os dois têm risco de preço. A cota mostra o risco todo dia; o apartamento esconde até a venda. / Mostrar ou
   esconder não deixa nenhum dos dois mais seguro."
3. **B1.** O casaco vem antes da metáfora: "Então o aluguel do anúncio ainda carrega duas coisas que ninguém tirou: o
   mês vazio e o imposto. / Essas duas coisas são o casaco. / O aluguel do anúncio sobe na balança de casaco e bota."
   Saíram "Um chega de casaco. O outro chega pelado. / Não precisa imaginar a cena" e a menção solta ao "defeito" do
   fundo (o preço da cota agora só aparece no B5, puxado pela objeção do Tanaka).
4. **Lei de 2023 (B4):** "O fundo precisa ter pelo menos cem cotistas, e você precisa ter menos de dez por cento
   dele." (L1 diz "menos de 10%"; por isso não "mais de dez"). O corte ficou explícito: "metade dos fundos da bolsa com
   cem cotistas ou mais".
5. **Repetição "a favor do fundo":** saiu o chuveiro do B4 (piada só contra o apê); "pra não roubar a favor do fundo"
   → "pra não inflar a conta"; abertura do B5 → "Oito mil ou dois mil, a renda do fundo chega maior nos dois casos."
6. **Piada do síndico** ("O fundo tem gestor. O apartamento tem síndico. / Escolhe o seu chefe, Tanaka.") saiu.

Mantidos (notas 8–9): gancho, vacância (B2 inteiro), prós e contras do B6, estrutura do fecho.

Título: o "R$ 8 mil menor" da v1.6 só vale para quem tem salário acima de R$ 7.350.
```
titulo_1 (recomendado): "Apê alugado ou fundo imobiliário em 2026: o leão decide se a diferença é R$ 2 mil ou R$ 8 mil"
titulo_2: "Imóvel alugado ou FII em 2026: quanto o leão leva do seu aluguel muda a conta inteira"
titulo_3: "FII ou imóvel alugado em 2026: a conta que o anúncio do apartamento não faz"   (o 3 da v1.6, sem número, ainda honesto)
```
Nenhum diz qual comprar. A thumb "6% → 4%" da seção 5 é o caso de quem tem salário: se mantiver, a thumb precisa de
"com salário" ou troca por "R$ 2 mil ou R$ 8 mil?".

Portão (v1.7): `ELIMINATORIOS: nenhum` · 5/6 (o mesmo FALHA do item 3, conflito da seção 1) · item 9 PASSA (as cartelas
foram escritas sem repetir número entre blocos) · costura: nenhum · avisos de ouvido: nenhum · CVM traduzida na hora.
Marcador de analogia do portão: 1. Fala limpa em `scratchpad/fala-0610-v17.txt` (175 linhas, 1.735 palavras, ≈ 12:00
a 145 por minuto, 12:51 a 135). Nota de processo: de novo houve corte (balança do B5, síndico, chuveiro do B4, "pelado"),
por pedido explícito. **Falta:** novo ouvinte-frio cego na v1.7 antes do Drive.

## 11. Ouvinte-frio cego (v1.7, persona aposentada de 62 anos com R$ 400 mil) e correções v1.8

Média 7,8, REPROVA (o leão com 6: "sou aposentada, em qual caso eu caio?"; o caso do meio ficou sem número). Conta central recontada certa; equilíbrio ok.
Correções (nenhum número novo; "entre dois e oito mil" são os dois casos já calculados):
- "quem tem salário" → "renda alta, de salário ou de aposentadoria"; a regra dos 5 mil dita como "somando salário, aposentadoria e aluguel".
- Os 7.350 ganham o porquê: "é ali que o desconto novo acaba".
- Segundo caso inclui o aposentado com renda total até 5 mil; caso do meio: "entre dois e oito mil por ano; a conta exata é a sua, com a sua declaração na mão".
- "casaco e bota" → "casaco" (a bota nunca era explicada); "Em outubro" → "Em outubro do ano passado".
Validação nova do Denis: aposentado com 65 anos ou mais tem parcela isenta extra no IR; o vídeo não entra nisso (se quiser, uma frase ou o comentário fixado).

---

## 12. Conferência na primária (07/10/2026, planalto.gov.br e Receita abertos neste container)

Fontes abertas em 07/10/2026 (curl, 200):
- Lei 11.033/2004 (compilada): https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l11033.htm
- Lei 14.754/2023: https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14754.htm
- Lei 15.270/2025: https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/l15270.htm
- MP 1.303/2025: https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/mpv/mpv1303.htm
- Ato Declaratório do Presidente da Mesa do CN nº 67/2025: https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/Congresso/adc-67-mpv1.303.htm
- Lei 7.713/1988 (carnê-leão, art. 8º): https://www.planalto.gov.br/ccivil_03/leis/l7713.htm
- Receita, tabelas 2026: https://www.gov.br/receitafederal/pt-br/assuntos/meu-imposto-de-renda/tabelas/2026

| Item | O que o texto diz | Roteiro | Veredito |
|---|---|---|---|
| Isenção do FII | Lei 11.033, art. 3º, III: isento "na fonte e na declaração de ajuste anual das pessoas físicas" o rendimento de FII "cujas cotas sejam admitidas à negociação exclusivamente em bolsas de valores ou no mercado de balcão organizado" (red. Lei 14.130/2021; a versão "efetivamente negociadas" da MP 1.184 está com vigência encerrada). § 1º, I: "no mínimo, 100 (cem) cotistas" (red. **Lei 14.754/2023**, art. 41). § 1º, II: não vale para quem tem "10% (dez por cento) ou mais da totalidade das cotas" ou direito a mais de 10% dos rendimentos (Lei 11.196/2005, red. Lei 14.130/2021) | fala B4 "pelo menos cem cotistas... menos de dez por cento"; cartela "cotas negociadas em bolsa, 100+ cotistas, menos de um décimo" | **bate.** A cartela atribuía tudo à Lei 14.754, que só trouxe o 100 (e a trava de 30% para pessoas ligadas). **Corrigido:** "Lei 11.033/2004, art. 3º (red. Lei 14.754/2023)". Simplificações aceitáveis: "em bolsa" (a lei inclui balcão organizado) e o fundo tem 30 dias para voltar a 100 cotistas (§ 4º) |
| Faixa de 5 mil e redutor até 7.350 | Lei 15.270, art. 2º (novo art. 3º-A da Lei 9.250): "A partir do mês de janeiro do ano-calendário de 2026", redução sobre "rendimentos tributáveis sujeitos à incidência mensal": "até R$ 5.000,00 — até R$ 312,89 (de modo que o imposto devido seja zero)"; "de R$ 5.000,01 até R$ 7.350,00 — R$ 978,62 − (0,133145 × rendimentos)"; § 2º: acima de R$ 7.350,00 "não terão redução". Anual (art. 11-A, a partir do exercício 2027): zero até R$ 60.000,00; redutor até R$ 88.200,00. Receita, tabela mensal 2026: última faixa "Acima de R$ 4.664,68 — 27,5%" | cartela B3 "imposto zero até R$ 5.000/mês de renda tributável; desconto parcial até R$ 7.350; acima disso, tabela antiga (máx. 27,5%)" | **bate** |
| Redutor no carnê-leão | O art. 3º-A fala de "rendimentos tributáveis sujeitos à incidência mensal", sem citar carnê-leão; o carnê-leão é o imposto mensal sobre rendimento recebido de pessoa física (Lei 7.713, art. 8º), calculado pela tabela mensal. Pelo texto, o redutor vale também ali. Nem a lei nem a página de tabelas da Receita (nem a de exemplos da Lei 15.270) dizem "carnê-leão" com todas as letras | não muda nada no roteiro: o caso 2 (R$ 2.000/mês como única renda) já fica abaixo da faixa isenta da tabela mensal (R$ 2.428,80, Receita 2026) e da anual (R$ 29.145,60), **com ou sem redutor**; o caso 1 é decidido no ajuste anual (27,5% na margem para quem passa de R$ 88.200 no ano) | **(a) bate pelo texto** (falta só a confirmação operacional do programa Carnê-Leão, sem efeito na conta); **(b) bate**: IR zero |
| MP 1.303 | MP 1.303/2025, art. 44: rendimentos de FII e Fiagro com cotas em bolsa "ficam sujeitos à retenção do imposto sobre a renda à alíquota de 5% (cinco por cento), quando possuírem, no mínimo, cem cotistas"; art. 75, I, a: efeitos "a partir de 1º de janeiro de 2026" para os arts. 1º a 60. ADC CN nº 67/2025 (DOU 15/10/2025): a MP "teve seu prazo de vigência encerrado no dia 8 de outubro de 2025" | fala B6 "Seriam cinco por cento, a partir deste ano. Em outubro do ano passado, a Câmara derrubou, e a proposta caiu."; cartela "derrubada pela Câmara em 08/10/25" | **5% e 2026 batem; a data bate.** A primária diz que a MP **perdeu a validade** em 08/10/2025; o papel da Câmara (tirou de pauta sem votar o mérito) é imprensa (camara.leg.br bloqueado aqui). **Cartela corrigida:** "perdeu a validade em 08/10/25 sem virar lei (Ato Declaratório do Congresso nº 67/2025)". A fala ficou como estava ("a Câmara derrubou" é a leitura corrente; se o Denis quiser a versão literal: "em outubro do ano passado, ela perdeu a validade sem virar lei") |
| FipeZap ago/2026 | fipe.org.br e downloads.fipe.org.br: CONNECT 403 em 07/10/2026 | hipótese de 6% | **CONFERIR NO MAC** |

