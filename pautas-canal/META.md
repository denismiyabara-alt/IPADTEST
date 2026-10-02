# Meta de 200 mil inscritos: desdobramento

Gerado por `meta.py`, com os dados de `auditoria-canal/dados/` (exportação de 02/10/2026) e o ranking de `TEMAS.md`.
A mesma conta, em números, está em `meta.csv`.

## Resposta curta

- **200 mil em 31/12/2026 não acontece.** São 11.590 inscritos líquidos por mês, 27
  vezes o ritmo atual. Nenhuma produção possível fecha essa conta.
- **Em 30/06/2027 também não.** São 3.895 líquidos por mês (9,2x o ritmo), o que pede
  25 longos por mês, todos no nível do p90 do último ano.
- **Em 31/12/2027 exige uma mudança de patamar.** São 2.330 líquidos por mês
  (5,5x o ritmo). Com 12 longos por mês, o máximo que o canal já publicou num mês, cada longo
  teria de trazer 186 inscritos. Só 8 dos 80 longos do último ano passaram disso.
  Isso só fecha com vídeos que estouram com frequência, não com a média.
- **No ritmo atual**, de 424 líquidos por mês (média de 6 meses), os 200 mil chegam em
  **ago/33**.
- **Cenário recomendado: o plano de produção abaixo.**
  - **Produção:** 12 longos por mês, com o mix escolhido pelo ranking de temas, e 8 Shorts por mês.
  - **Resultado:** cerca de 1.146 líquidos por mês, 2,7 vezes o ritmo de hoje, e os 200 mil em
    **mai/29** (faixa de mar/28 a set/30).
  - **A alternativa** para 31/12/2027 é a mesma produção com a média por vídeo no nível dos top do ano.

## A árvore da meta

```
inscritos líquidos/mês = ganhos − perdas
  hoje:  424 na média de 6 meses (221 em setembro)
         jul-set: 683 ganhos − 332 perdas = 352 líquidos por mês
         perdas usadas no plano: 350 (média de 6 meses)
  ganhos = catálogo + vídeos novos
    catálogo (vídeos antigos + inscrições fora de vídeo): 449/mês
        = ganhos de jul-set − inscritos dos 45 vídeos publicados em jul-set, por mês
    vídeos novos = Σ formato × assunto (nº de vídeos × inscritos esperados por vídeo)
      inscritos esperados por vídeo = views intencionais medianas × inscritos por mil views intencionais
        longos (12 meses, n = 80): 4.652 × 9,1/mil = 42 por vídeo
                                     (p25–p75: 23–69; real por vídeo: mediana 27, p75 62, p90 150)
        Shorts (12 meses, n = 81, sem o "1 centavo"): 2.274 × 0,72/mil = 1,6 por vídeo
      hoje: ~9 longos e ~6,5 Shorts por mês (medianas de 12 meses)
```

**A árvore fecha com os números de hoje.**
- **Vídeos novos:** 8 longos × 42 + 5,5 Shorts × 1,6 ≈ 348.
- **Catálogo:** + 449.
- **Perdas:** − 350.
- **Total:** ≈ 448 líquidos por mês, contra os
  424 reais da média de 6 meses.

**Por que mediana e não média:** a média de inscritos dos longos do ano é 67 por vídeo, contra
27 na mediana, porque 5 vídeos fizeram 39% dos inscritos. Nos Shorts, o "1 centavo" (9.675 inscritos) fica
fora: sem ele, um Short novo traz cerca de 1 inscrito.

## Os três prazos

| prazo | meses | líquidos/mês | × ritmo atual | ganhos brutos/mês (+ perdas) | vindos de vídeos novos (− catálogo) | views intencionais/mês nos vídeos novos | longos/mês no nível mediano | … no p75 | … no p90 | inscritos por longo com 12 longos/mês |
|---|---|---|---|---|---|---|---|---|---|---|
| 31/12/2026 | 3,0 | 11.590 | 27,3x | 11.940 | 11.491 | 1.261.477 | 426 | 184 | 77 | 958 |
| 30/06/2027 | 9,0 | 3.895 | 9,2x | 4.244 | 3.795 | 416.601 | 141 | 61 | 25 | 316 |
| 31/12/2027 | 15,0 | 2.330 | 5,5x | 2.680 | 2.230 | 244.865 | 83 | 36 | 15 | 186 |

**O que a produção histórica permite:**
- **Longos:** mediana de 9 por mês nos últimos 12 meses; máximo de 12 num mês
  (fev e set/2024).
- **Shorts:** mediana de 6,5 por mês; máximo de 19 (jun/2026).

**Leitura:**
- **31/12/2026:** impossível. Com a produção máxima, cada longo teria de trazer 958 inscritos.
  O melhor vídeo do ano trouxe 637.
- **30/06/2027:** impossível no patamar atual. Pede 316 inscritos por longo, com 12 longos
  por mês. Só 5 dos 80 longos do último ano chegaram lá.
- **31/12/2027:** exige mudança de patamar: 12 longos por mês, cada um com 186 inscritos,
  acima do p90 (150). No último ano, 8 longos chegaram lá, menos de
  1 por mês; o plano pediria 12 por mês. É um alvo para ser revisto a cada trimestre, não um plano.

## Cenário recomendado: plano de produção

O mix de longos sai do ranking de inscritos esperados por vídeo dos últimos 12 meses (`TEMAS.md`). Dá mais espaço ao que
rende e menos a "ações e empresas", que é o assunto mais produzido (28 dos 80 longos) e rende 30 por vídeo.

| assunto | longos/mês | inscritos esperados por vídeo | faixa p25–p75 | n (12 meses) |
|---|---|---|---|---|
| renda mensal | 4,3 | 91 | 69–267 | 7 |
| tesouro e renda fixa | 2,0 | 195 | 106–212 | 5 |
| crise e macro | 1,5 | 52 | 17–75 | 12 |
| cripto | 1,0 | 58 | 35–117 | 4 |
| FII | 1,2 | 45 | 26–56 | 6 |
| ações e empresas | 2,0 | 30 | 22–41 | 28 |
| **Shorts** | 8 | 1,6 | 0,9–3,3 | 81 |
| **Total de vídeos novos** | 12,0 longos + 8 Shorts | **1.046 inscritos/mês** | 652–1.975 | |

**Resultado do plano em regime** (a partir de jan/27):
- **Conta:** 449 do catálogo + 1.046 dos vídeos novos − 350 de perdas =
  **1.146 líquidos por mês** (faixa de 752 a 2.075).
- **Prazo:** os 200 mil chegam em **mai/29**. Na faixa otimista (p75), em mar/28; na
  pessimista (p25), em set/30.

**Premissas, para revisar a cada trimestre:**
- **O ranking se repete:** tesouro e renda mensal têm n = 5 e n = 7, e o número deles é puxado pelos top. A tendência é
  cair em direção à média.
- **Catálogo constante:** ele cai devagar, mas os vídeos novos viram catálogo.
- **Perdas** na média de 6 meses.
- **Defasagem:** os inscritos de cada vídeo chegam 60% no mês da publicação, 25% no seguinte e 15% no outro.
- **Rampa:** em out/26, a produção é de 75% do plano (calendário v2).

## Metas mensais (cenário recomendado)

Hoje = set/26. Na coluna de inscritos líquidos, o "hoje" é 221 (set/26); na média de 6 meses, 424.

| mês | inscritos líquidos | ganhos | perdas | longos | Shorts | inscritos no fim do mês |
|---|---|---|---|---|---|---|
| out/26 | **573** | 922 | 350 | 9 | 8 | 165.573 |
| nov/26 | **925** | 1.274 | 350 | 12 | 8 | 166.497 |
| dez/26 | **1.107** | 1.457 | 350 | 12 | 8 | 167.605 |
| jan/27 | **1.146** | 1.496 | 350 | 12 | 8 | 168.751 |
| fev/27 | **1.146** | 1.496 | 350 | 12 | 8 | 169.897 |
| mar/27 | **1.146** | 1.496 | 350 | 12 | 8 | 171.043 |
| abr/27 | **1.146** | 1.496 | 350 | 12 | 8 | 172.190 |
| mai/27 | **1.146** | 1.496 | 350 | 12 | 8 | 173.336 |
| jun/27 | **1.146** | 1.496 | 350 | 12 | 8 | 174.482 |
| jul/27 | **1.146** | 1.496 | 350 | 12 | 8 | 175.628 |
| ago/27 | **1.146** | 1.496 | 350 | 12 | 8 | 176.774 |
| set/27 | **1.146** | 1.496 | 350 | 12 | 8 | 177.921 |
| out/27 | **1.146** | 1.496 | 350 | 12 | 8 | 179.067 |
| nov/27 | **1.146** | 1.496 | 350 | 12 | 8 | 180.213 |
| dez/27 | **1.146** | 1.496 | 350 | 12 | 8 | 181.359 |

### Indicadores de acompanhamento (meta mensal em regime × hoje)

| indicador | meta mensal (regime) | hoje | fonte do "hoje" |
|---|---|---|---|
| inscritos líquidos | 1.146 (out: 573; nov: 925) | 221 em set; 424 na média de 6 meses | canal_por_mes (Analytics) |
| views intencionais dos longos novos | 95.896 (12,0 longos × medianas do mix) | ~37.220 (8 longos × 4.652); todos os longos em set: ~43.335 (estimativa*) | analytics_por_video, longos de 12 meses |
| views de Shorts sem o "1 centavo" | ≥ 38.312 (8 × mediana de 4.789) | 24.835 em set; 198.548 em jun | Studio E2 (Total − gráfico do outlier) |
| inscritos por mil views intencionais (longos novos) | 10,8 | 9,1 | analytics_por_video, 12 meses |
| publicações | 12 longos + 8 Shorts | 8 longos + 4 Shorts em set | videos.csv |
| % das views de longos pela Pesquisa | ≥ 15% | 5,5% em set (diluída pela Navegação inflada); 14,8% em ago | Studio E3, longos |
| CTR da Pesquisa (longos) | ≥ 13,3% | 12,3% (vitalício; a API não dá CTR por mês) | Studio E3; acompanhar no Studio todo mês |
| CTR geral das impressões (longos) | ≥ 7,1% | 7,1% (vitalício) | Studio E1 |

\* Views intencionais do canal (canal_por_mes) − 0,43 × views de Shorts (Studio). O 0,43 é a
razão intencional/views dos Shorts em agosto, antes do efeito de 27/08.

## Metas semanais (out e nov/26)

As semanas seguem o calendário v2. A meta semanal é a mensal ÷ 4,33. Na produção, a quinta é dia de longo, e a partir de
26/10 entra o 3º longo semanal.

| semana | inscritos líquidos | ganhos | longos | Shorts |
|---|---|---|---|---|
| 05/10–11/10 | 132 | 213 | 2 | 2 |
| 12/10–18/10 | 132 | 213 | 2 | 2 |
| 19/10–25/10 | 132 | 213 | 2 | 2 |
| 26/10–01/11 | 132 | 213 | 3 | 2 |
| 02/11–08/11 | 214 | 294 | 3 | 2 |
| 09/11–15/11 | 214 | 294 | 3 | 2 |
| 16/11–22/11 | 214 | 294 | 3 | 2 |
| 23/11–29/11 | 214 | 294 | 3 | 2 |

**Como acompanhar:** toda segunda, com os números da semana anterior no Studio (inscritos ganhos e perdidos, views
intencionais, % da Pesquisa e CTR). Se duas semanas seguidas ficarem abaixo de 70% da meta, troque a pauta da quinta
seguinte pela do assunto com maior inscrito esperado (`TEMAS.md`).

## Sensibilidade: o que cada alavanca move

São inscritos por mês a mais em regime, sobre o ritmo de hoje, com a faixa de incerteza. A ordem é pelo valor central.

| # | alavanca | inscritos/mês (central) | faixa | base do número |
|---|---|---|---|---|
| 1 | +1 longo por semana da série de renda mensal (+4,3 por mês) | **391** | 297 a 1.146 | renda mensal, longos dos últimos 12 meses (n = 7): 6.527 views intencionais medianas × 13,9 inscritos por mil = 91 por vídeo (faixa p25–p75: 69–267) |
| 2 | +1 longo por mês de Tesouro e renda fixa (Copom e marcação) | **195** | 106 a 212 | tesouro e renda fixa, 12 meses (n = 5): 195 por vídeo (106–212); amostra pequena, puxada por 2 vídeos top |
| 3 | Trocar 2 longos/mês de 'ações e empresas' por renda mensal | **122** | 56 a 490 | ações e empresas é o assunto mais produzido (n = 28 em 12 meses) e rende 30 por vídeo, contra 91 da renda mensal |
| 4 | Republicar (ou regravar) os 30 maiores dos 285 longos fora do ar | **68** | 45 a 91 | os 30 maiores somam 20.272 inscritos vitalícios; o catálogo público rende 0,45% dos inscritos vitalícios por mês (449/mês); faixa de 50% a 100% desse rendimento (o conteúdo é de 2019-2022 e pode estar desatualizado) |
| 5 | Reduzir as perdas em 10% | **35** | 0 a 70 | perdas médias de 350/mês (6 meses); quase nada é atribuível a vídeo (3.959 perdas por vídeo no vitalício), então a alavanca é fraca e incerta |
| 6 | Subir o CTR da Pesquisa nos longos em 1 p.p. (12,3% → 13,3%) | **5** | 2 a 8 | longos recebem 6.742 views/mês da Pesquisa (abr a set/26, Studio); +1 p.p. sobre 12,32% = +8%, a 9,1 inscritos por mil |
| 7 | Voltar a 8 Shorts por mês (hoje 5,5) | **4** | 2 a 126 | por vídeo, um Short novo traz 1,6 inscrito (n = 81, 12 meses, sem o '1 centavo'); o máximo usa a regressão mensal (1,04 por mil) sobre as 120.806 views de Shorts (sem o '1 centavo') que sumiram de jun-jul para ago-set |

**Correção do relatório (ação 6):** o RELATORIO.md estimava que voltar a 8 Shorts por mês recuperaria cerca de 200
inscritos por mês. Por vídeo, porém, um Short novo traz cerca de 1,6 inscrito. A maior parte das views
de Shorts é do "1 centavo", que caiu de 169 mil (jul) para 97 mil (set), e ele não volta com produção. A faixa honesta
para a alavanca dos Shorts vai de 2 a
cerca de 126 inscritos por mês; o valor alto supõe que cada view de Short novo converte como na regressão mensal. Os
Shorts continuam úteis para alcance e para levar público aos longos, mas não sustentam a meta sozinhos.

## Limites

- **"Inscritos esperados por vídeo"** usa os inscritos atribuídos pelo Analytics ao vídeo, no vitalício de vídeos com 1 a
  12 meses de vida. Os mais novos ainda vão ganhar um pouco.
- **Amostras pequenas:** renda mensal (n = 7), tesouro (n = 5), cripto (n = 4) e FII (n = 6). As faixas p25–p75 mostram o
  tamanho da incerteza.
- **Contador arredondado:** o total de 165.000 é arredondado pelo YouTube.
- **Views infladas desde 27/08 (H1):** todas as metas de views usam views intencionais, não o contador.
