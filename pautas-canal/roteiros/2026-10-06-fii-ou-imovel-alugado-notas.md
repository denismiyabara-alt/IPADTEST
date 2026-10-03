# Notas do roteiro de 06/10/2026: FII ou imóvel alugado

Roteiro: `2026-10-06-fii-ou-imovel-alugado.md` (v1.4, congelado). Briefing e concorrentes em `pautas-canal/briefings/`.

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
| R$ 5.000/mês isento; R$ 7.350; 27,5% | B3 | Lei 15.270/2025 e tabela do IRPF 2026 | só secundária (planalto/Receita bloqueados) — Denis valida |
| R$ 6.050 de IR; sobra R$ 15.950; ≈ 4% | B3, B4 | conta: 22.000 × 27,5%; 22.000 − 6.050; 15.950 ÷ 400.000 = 3,99% | conta |
| R$ 24.000 no fundo, isento; diferença R$ 8.050 | B0, B4, B5, B7 | conta: 400.000 × 6%; 24.000 − 15.950; isenção pela Lei 11.033 art. 3º (red. Lei 14.754) | conta + lei (secundária) |
| 100 cotistas; menos de 10% das cotas | B4 | Lei 14.754/2023 (alterou a Lei 11.033, art. 3º) | só secundária — Denis valida |
| 48 fundos abertos ao público com menos de 100 cotistas | só cartela B4 | CVM, informe mensal ago/2026 | conferido na primária |
| 7,8% (mediana, 12 meses até ago/26, sobre o patrimônio) | B4 | CVM, informe mensal, soma do Dividend_Yield_Mes set/25–ago/26, 290 fundos listados com 100+ cotistas | conferido na primária |
| 10% de queda = R$ 40 mil; 5 anos de vantagem | B5 | hipótese ("se") e conta (8.050 × 5 = 40.250) | conta |
| MP de 5% sobre rendimento de FII, derrubada em outubro de 2025 | B6 | MP 1.303/2025; Câmara, 08/10/2025 | só secundária — Denis valida |
| 97 de 272 fundos com um imóvel só | B6 | CVM, informe trimestral 30/06/2026 | conferido na primária |

## 7. Validações que só o Denis faz

1. **Lei 14.754/2023 / Lei 11.033, art. 3º:** 100 cotistas e menos de 10% das cotas (B4 e cartela).
2. **Lei 15.270/2025:** quem tem salário acima de R$ 7.350 por mês paga 27,5% na margem sobre o aluguel em 2026 (B3).
   A conta ignora deduções do carnê-leão (IPTU, condomínio, taxa da imobiliária pagos pelo dono): se quiser, uma frase na
   cartela.
3. **MP 1.303/2025:** 5% sobre rendimento de FII a partir de 2026 e derrubada pela Câmara em 08/10/2025 (B6).
4. **FipeZap de ago/2026:** se 6% ao ano bruto continua honesto como hipótese (o snippet diz 6,14%).
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
