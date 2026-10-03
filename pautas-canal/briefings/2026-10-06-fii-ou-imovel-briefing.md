---
tema: "Fundo imobiliário ou imóvel alugado: a conta de 2026" (título de trabalho do calendário; o empacotador decide)
formato: longo (alvo 12-13 min; teto 14)
data_briefing: 2026-10-03 (nuvem)
data_publicacao: 2026-10-06 (terça)
termo_busca: "fundo imobiliario" (30 termos da família; 7.643 views da Pesquisa no vitalício, sobretudo em kipRQb0ksus)
continuacao_de: Gjw4crGh6Xg ("Por que os ricos não investem em FII", 92 inscritos)
ja_feito: GbmXrqvUOkM, 26/06/2026, "Fundos Imobiliários ou Imóveis: Qual rende mais no bolso?" (14 inscritos)
concorrentes: 2026-10-06-fii-ou-imovel-concorrentes.md
frame: REVELAÇÃO + MÉTODO. Nada de "qual é melhor". Nenhum fundo citado pelo nome, nenhuma corretora
status: GO COM RESSALVAS. Os números da CVM e do BCB foram conferidos na fonte primária. As regras de imposto e o
  FipeZap só foram conferidos em fonte secundária (primária bloqueada no proxy): o Denis valida (seção 10)
---

# BRIEFING: FII ou imóvel alugado, a conta de 2026

## 0. Por que este vídeo é diferente do de 26/06

O de 26/06 teve **retenção boa** (45,9% assistido, 4º melhor de 48 longos de abr–set/2026) e **conversão boa** (7,3
inscritos por mil views, contra mediana de 5,4), mas **alcance ruim** (1.923 views, 7º pior de 48). A porta falhou: o
título "Qual rende mais no bolso?" é a mesma pergunta de 12 vídeos concorrentes (ver arquivo de concorrentes), sem
número, sem ano. Dados: `auditoria-canal/dados/analytics_por_video.csv`.

**O ângulo de 2026 (uma frase):** *o mesmo aluguel de R$ 2 mil por mês chega no bolso como R$ 24 mil por ano dentro de
um fundo que passa no corte dos 100 cotistas, e como menos de R$ 16 mil num apartamento no seu nome, depois do mês vazio
e do leão. A isenção de R$ 5 mil de 2026 não muda essa conta para quem tem salário, e a isenção do FII quase caiu em
outubro de 2025.* Em troca, o FII mostra o preço todo dia e o apartamento não: é a dúvida nº 1 da audiência.

## 1. Ficha de validade temporal

```
Evento central: nenhum (método). Os fatos de 2026: Lei 15.270/2025 em vigor desde jan/2026; MP 1.303/2025 caiu em 08/10/2025
Dados CVM: informe mensal ago/2026 e trimestral jun/2026 (arquivos de 26/09/2026, baixados em 03/10/2026)
Juros/inflação (só contexto, fora da fala): BCB, consultado em 03/10/2026
Publicação: 06/10/2026
Status: DENTRO DA JANELA
```

## 2. DADOS CONFERIDOS EM FONTE PRIMÁRIA

### 2.1 CVM, informes de FII (dados.cvm.gov.br/dados/FII/DOC/)

Método: arquivos `inf_mensal_fii_{2025,2026}.zip` e `inf_trimestral_fii_2026.zip`; última versão de cada fundo e mês;
"listado" = `Mercado_Negociacao_Bolsa = S` no informe geral do mês.

| ID | Dado | Valor | Recorte |
|---|---|---|---|
| C1 | Fundos que declaram negociação em bolsa | **695** | informe mensal, ago/2026 |
| C2 | Desses, com menos de 100 cotistas | **251** (1 sem dado) | ago/2026 |
| C3 | Dos 251, abertos a "investidores em geral" | **48** (os outros 203 são para investidor profissional/qualificado) | ago/2026 |
| C4 | Listados abertos a "investidores em geral" com 100 ou mais cotistas | 319 | ago/2026 |
| C5 | Rendimento distribuído em 12 meses (set/25–ago/26), **mediana**, fundos listados com 100+ cotistas e os 12 meses informados | **7,83%** sobre o valor patrimonial (n = 290) | soma do `Percentual_Dividend_Yield_Mes` |
| C6 | O mesmo, ponderado pelo patrimônio | 8,86% | idem |
| C7 | Imóveis prontos para renda declarados por fundos listados | **2.018** imóveis, 272 fundos | trimestral, 30/06/2026 |
| C8 | Desses, com vacância de 100% (totalmente vazios) | **176** (8,7%, quase 1 em cada 11) | 30/06/2026 |
| C9 | Com vacância zero | 1.520 (75%) | 30/06/2026 |
| C10 | Fundos com **um imóvel só** | **97 de 272** (mediana: 3 imóveis por fundo) | 30/06/2026 |
| C11 | Fundos com pelo menos um imóvel 100% vazio | 39 | 30/06/2026 |

Ressalvas: (a) o `Dividend_Yield` da CVM é sobre o **valor patrimonial** da cota, não sobre o preço de tela; conferido
num fundo grande (1,01% no mês × cota patrimonial de R$ 9,26 ≈ R$ 0,094 por cota). Na fala, dizer "sobre o patrimônio".
(b) Um "imóvel" no informe pode ser um prédio com muitas unidades; 100% de vacância é o imóvel inteiro vazio.
(c) O número de cotistas é o declarado pelo fundo; a isenção depende disso **e** de outras condições (seção 3).

### 2.2 B3

| ID | Dado | Fonte |
|---|---|---|
| B1 | "O IFIX é um índice de retorno total" (reinveste os rendimentos) | b3.com.br, página "Índice de Fundos de Investimentos Imobiliários (IFIX B3)", lida em 03/10/2026 |

Pontos e rentabilidade do IFIX: **não conferidos** (sistemaswebb3-listados.b3.com.br bloqueado). Fora do roteiro.

### 2.3 Banco Central (contexto, fora da fala)

| ID | Dado | Fonte |
|---|---|---|
| J1 | Meta Selic 13,75% desde 17/09/2026 (Copom nº 281, 16/09) | bcb.gov.br/api/servico/sitebcb/historicotaxasjuros |
| J2 | IPCA 12 meses 4,22% (mês de referência não vem no JSON; provável ago/26) | bcb.gov.br/api/servico/sitebcb/indicadorInflacao |

O SGS (api.bcb.gov.br) não resolveu no proxy. **CDI fica fora do roteiro de propósito:** aluguel e rendimento de FII
são renda corrente de ativo real; comparar com CDI nominal é o defeito do P2 ("retorno real contra nominal").

## 3. DADOS CONFERIDOS SÓ EM FONTE SECUNDÁRIA (primária bloqueada) — Denis valida

| ID | Afirmação | Onde vi | Primária que falta |
|---|---|---|---|
| L1 | Rendimento de FII é isento de IR para pessoa física se: cotas negociadas só em bolsa/balcão, **100+ cotistas**, cotista com **menos de 10%** das cotas; cotistas vinculados com 30%+ perdem | busca: renovainvest, Demarest, PwC (resumos da Lei 14.754/2023) | Lei 11.033/2004 art. 3º, na redação da Lei 14.754/2023 (planalto.gov.br: bloqueado) |
| L2 | A Lei 14.754/2023 subiu o mínimo de 50 para 100 cotistas | idem | idem |
| L3 | Desde jan/2026 (Lei 15.270/2025): imposto zero até R$ 5.000/mês de renda tributável, redutor até R$ 7.350; acima disso, tabela de 2025 sem mudança, alíquota máxima 27,5% | busca: omie, contabilizei, jettax, gov.br/receitafederal (só snippet) | Lei 15.270/2025; tabela da Receita 2026 |
| L4 | Aluguel recebido de pessoa física paga pelo carnê-leão e soma no ajuste anual | idem | RIR/2018; página da Receita |
| L5 | Lei 15.270/2025 tira da base do imposto mínimo de alta renda o rendimento de FII/Fiagro listado com 100+ cotistas | busca: Mayer Brown, Forvis Mazars | Lei 15.270/2025 |
| L6 | MP 1.303/2025 propunha 5% de IR sobre rendimento de FII a partir de 2026; a Câmara derrubou em 08/10/2025 e a MP caducou | busca: InfoMoney, Seu Dinheiro, XP (snippets) | planalto.gov.br (mpv1303), Câmara |
| F1 | FipeZap: rentabilidade do aluguel residencial **6,14% ao ano** em ago/2026; comercial 7,63% | busca (snippet de portal; o PDF da Fipe está bloqueado) | downloads.fipe.org.br, informe de ago/2026 |
| G1 | Venda de cota de FII: ganho de capital 20% | busca | Lei 8.668/1993 / 11.033 — **fora do roteiro** |

**Não conferido e fora do roteiro:** alíquota de IR do rendimento de FII que **não** passa no corte (as fontes
divergem: 20% na fonte pela Lei 8.668 art. 17 x tabela regressiva). No vídeo: só "perde a isenção".

## 4. A conta central (hipotética, com "se"; refazível de cabeça)

Premissa: **se** um apartamento de R$ 400 mil aluga por R$ 2 mil por mês (0,5% ao mês = 6% ao ano bruto; em linha com
o F1, que o Denis confere). **Se** o dono já tem salário acima de R$ 7.350 por mês (L3), cada real de aluguel paga 27,5%.

| Passo | Conta | Resultado |
|---|---|---|
| 1. anúncio | 2.000 × 12 | 24.000 |
| 2. um mês vazio por ano (hipótese; ordem de grandeza do C8: 1 em cada 11 imóveis de fundo vazio em jun/26) | 2.000 × 11 | 22.000 |
| 3. leão | 22.000 × 27,5% | 6.050 |
| 4. líquido | 22.000 − 6.050 | **15.950** |
| 5. sobre o preço | 15.950 ÷ 400.000 | 3,99% (≈ 4%) |
| 6. FII, **se** pagar os mesmos 6% (abaixo da mediana C5 de 7,83%), isento (L1) | 400.000 × 6% | 24.000 |
| 7. diferença | 24.000 − 15.950 | **8.050 por ano** (número do loop) |
| 8. contraprova | 8.050 × 5 | 40.250 ≈ uma queda de 10% da cota de R$ 400 mil (40.000): ~5 anos de vantagem |

Simplificações declaradas (o roteiro não esconde): ignora deduções do carnê-leão (IPTU/condomínio/administração pagos
pelo dono reduzem a base, mas também são custo), ignora reajuste do aluguel e valorização do imóvel, ignora a oscilação
da cota no passo 6. O rendimento do FII (C5) já vem depois da vacância e das despesas do fundo.

## 5. Os dois lados (sem veredito)

A favor do apartamento: você decide (inquilino, reforma, preço); pode usar financiamento; pode morar ou deixar pra
família; não paga taxa de gestor; a isenção do FII é regra de lei e quase mudou (L6).
A favor do FII: o rendimento chega líquido de vacância, despesa e (hoje) imposto; a vacância de vários imóveis se dilui;
vende em dias, não meses. Contra o FII: a cota aparece na tela todo dia e cai; 97 de 272 fundos têm um imóvel só (C10),
o mesmo risco do apê; quem decide é o gestor; fundo com menos de 100 cotistas perde a isenção (C3: 48 abertos ao público).

## 6. Dúvida nº 1 da audiência (ver concorrentes)

"O FII paga mais, mas a cota cai; o imóvel não cai." Resposta: o imóvel também tem preço e ele também muda; só não é
publicado todo dia. O dia em que se descobre é o dia da venda. (Sem número de queda de preço de imóvel: FipeZap venda não
foi conferido.)

## 7. Analogia (uma só)

Balança. Rendimento de FII = pesado sem roupa (já líquido); aluguel do anúncio = pesado de casaco e bota (bruto).
Camada 2: a cota sobe na balança todo dia; o apartamento não se pesa desde a pandemia. Camada 3 (fecho): pesar os dois
do mesmo jeito.

## 8. O que NÃO entra

CDI/Selic na fala; IFIX em pontos; qualquer fundo pelo nome; corretora; alocação em %; dívida, financiamento como
"dica", finanças pessoais básicas; alíquota de FII não isento; FipeZap como número firme antes da validação.

## 9. Domínios bloqueados (03/10/2026, proxy da nuvem)

planalto.gov.br, normas.leg.br, gov.br/receitafederal, normas.receita.fazenda.gov.br, camara.leg.br, senado.leg.br,
in.gov.br, api.bcb.gov.br (SGS; DNS não resolve), olinda.bcb.gov.br, www3.bcb.gov.br, fipe.org.br,
downloads.fipe.org.br, datazap.com.br, sistemaswebb3-listados.b3.com.br, arquivos.b3.com.br, borainvestir.b3.com.br,
ibge.gov.br, sidra.ibge.gov.br, anbima.com.br, prefeitura.sp.gov.br, infomoney, valor, legisweb, jusbrasil, portais
de FII. YouTube: busca OK, **página do vídeo pede login** (legendas e comentários de concorrentes não coletados).
statusinvest (403) e Yahoo Finance (429) não foram tentados de novo: não são fonte primária. Nada foi contornado.
Funcionaram: dados.cvm.gov.br, www.b3.com.br (páginas institucionais), www.bcb.gov.br (API do site).

## 10. Validações que só o Denis faz

1. L1/L2: ler o art. 3º da Lei 11.033 na redação da Lei 14.754 (100 cotistas, menos de 10%).
2. L3/L4: confirmar que, para quem tem salário acima de R$ 7.350, o aluguel paga 27,5% na margem em 2026.
3. L6: data e conteúdo da MP 1.303 (5%; derrubada em 08/10/2025).
4. F1: abrir o FipeZap de ago/2026 e ver se 6% ao ano de aluguel bruto continua uma hipótese honesta para a fala.
5. Se for citar no vídeo a frase de exclusão do FII do imposto mínimo (L5): conferir na Lei 15.270.
