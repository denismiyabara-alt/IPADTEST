# Termos de busca: o que o público procura e acha no canal

Gerado por `termos.py` a partir de `auditoria-canal/dados/termos_busca_canal.csv` (25 termos por mês, de out/25 a
set/26) e de `termos_busca_por_video.csv` (25 termos de cada um dos 50 vídeos com mais views da Pesquisa, no
vitalício).

**Limite dos dados:**
- **Corte mensal:** um termo fora do top 25 de um mês teve menos views que o 25º. Nos últimos 6 meses, o corte foi
  04/26: 725 · 05/26: 613 · 06/26: 436 · 07/26: 383 · 08/26: 284 · 09/26: 299.
- **Teto:** para um termo que nunca entrou no top 25, as views dos 6 meses são no máximo a soma desses cortes.

## Leitura (5 linhas)

1. **A busca do canal hoje é o Short do "1 centavo".** Nos últimos 6 meses, os termos amplos de dinheiro ("como ganhar
   dinheiro na internet", "como ficar rico" etc.) somam 242.173 das 246.325 views dos top 25 mensais
   (98%). Eles quase não convertem: o Short traz cerca de 1 inscrito por mil views.
2. **Investimento quase não aparece nos top 25 recentes.** Os únicos termos de investimento nos últimos 6 meses são
   "trxf11" (1.516), "irbr3" (389): 1.905 views ao todo.
3. **A demanda de investimento que o canal já captou é de cauda longa e está em vídeos antigos:**
   - LCI, LCA e CDB, com o Short de abr/25;
   - ETFs que pagam dividendos mensais (2024);
   - ETF de bitcoin (2024);
   - CDB prefixado (2018);
   - dividendos sintéticos (2022);
   - fundos imobiliários (2023);
   - "como juntar 1 milhão" (Shorts de 2022 e 2024).
4. **Tesouro, IPCA+, Copom e Selic não aparecem em nenhum termo**, nem no top 25 mensal nem nos 50 vídeos de busca. Os
   vídeos de Tesouro, que são os que mais trazem inscritos (TEMAS.md), vivem da página inicial, não da busca.
5. **Bancos e apps** (Next, Nubank, Banco Original, C6, Pix) ainda são o maior bloco do catálogo de busca, mas estão
   fora do foco. Para medir o que os vídeos de 2026 recebem de busca, falta rodar `exportar.py --termos-recentes 180`
   no Mac (comando no fim).

## Termos de investimento (fora o amplo e o catálogo de bancos)

| termo | assunto | vídeo que recebe a busca (ano) | Pesquisa, últimos 6 meses (top 25 do canal) | Pesquisa, vitalício (no vídeo) |
|---|---|---|---|---|
| trxf11 | FII | `—` (—) | 1.516 em 2 meses (+ ≤ 2.157 nos outros) | 0 |
| irbr3 | ações e empresas | `nSQELM25nU8` (2022) | 389 em 1 mês (+ ≤ 2.441 nos outros) | 6.082 |
| criptomoedas | cripto | `1EGx_IxWSbo` (2022) | fora do top 25 (≤ 2.740) | 5.547 |
| opcoes acoes | ações e empresas | `aYQbBXHy0Y0` (2020) | fora do top 25 (≤ 2.740) | 4.988 |
| cdb prefixado | tesouro e renda fixa | `7CdwOTT7U3o` (2018) | fora do top 25 (≤ 2.740) | 3.928 |
| bitcoin | cripto | `1EGx_IxWSbo` (2022) | fora do top 25 (≤ 2.740) | 3.587 |
| lci e lca | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | fora do top 25 (≤ 2.740) | 3.544 |
| mercado de opcoes | ações e empresas | `aYQbBXHy0Y0` (2020) | fora do top 25 (≤ 2.740) | 2.656 |
| barsi | ações e empresas | `XBJqP2JTkkQ` (2022) | fora do top 25 (≤ 2.740) | 2.588 |
| etf bitcoin | cripto | `YxLzaSN2a1M` (2024) | fora do top 25 (≤ 2.740) | 2.443 |
| dividendos sinteticos | ações e empresas | `9B7jEAm-96g` (2022) | fora do top 25 (≤ 2.740) | 2.001 |
| louise barsi | ações e empresas | `nSQELM25nU8` (2022) | fora do top 25 (≤ 2.740) | 1.953 |
| etfs que pagam dividendos mensais | renda mensal | `Y4WHQiKcv1g` (2024) | fora do top 25 (≤ 2.740) | 1.877 |
| barsi investidor | ações e empresas | `XBJqP2JTkkQ` (2022) | fora do top 25 (≤ 2.740) | 1.855 |
| como investir em criptomoedas | cripto | `1EGx_IxWSbo` (2022) | fora do top 25 (≤ 2.740) | 1.811 |
| como juntar 1 milhao de reais | juntar dinheiro e aposentadoria | `tbKsF2qyakU` (2022) | fora do top 25 (≤ 2.740) | 1.803 |
| melhores fundos imobiliarios 2023 | FII | `kipRQb0ksus` (2023) | fora do top 25 (≤ 2.740) | 1.699 |
| opcoes de acoes | ações e empresas | `aYQbBXHy0Y0` (2020) | fora do top 25 (≤ 2.740) | 1.690 |
| fundos imobiliarios 2023 | FII | `kipRQb0ksus` (2023) | fora do top 25 (≤ 2.740) | 1.563 |
| fundos imobiliarios | FII | `kipRQb0ksus` (2023) | fora do top 25 (≤ 2.740) | 1.432 |
| opcoes | ações e empresas | `aYQbBXHy0Y0` (2020) | fora do top 25 (≤ 2.740) | 1.309 |
| etf que pagam dividendos mensais | renda mensal | `Y4WHQiKcv1g` (2024) | fora do top 25 (≤ 2.740) | 1.255 |
| irbr3 hoje | ações e empresas | `nSQELM25nU8` (2022) | fora do top 25 (≤ 2.740) | 1.141 |
| etf | ETF e exterior | `Y4WHQiKcv1g` (2024) | fora do top 25 (≤ 2.740) | 1.096 |
| bitcoin como funciona | cripto | `1EGx_IxWSbo` (2022) | fora do top 25 (≤ 2.740) | 1.061 |
| etfs americanos que pagam dividendos mensais | renda mensal | `Y4WHQiKcv1g` (2024) | fora do top 25 (≤ 2.740) | 1.002 |
| como fazer 1 milhao de reais | juntar dinheiro e aposentadoria | `tbKsF2qyakU` (2022) | fora do top 25 (≤ 2.740) | 935 |
| lci | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | fora do top 25 (≤ 2.740) | 927 |
| dividendo sintetico | ações e empresas | `9B7jEAm-96g` (2022) | fora do top 25 (≤ 2.740) | 892 |
| lca e lci | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | fora do top 25 (≤ 2.740) | 888 |
| investir em criptomoedas | cripto | `1EGx_IxWSbo` (2022) | fora do top 25 (≤ 2.740) | 832 |
| etf de bitcoin | cripto | `YxLzaSN2a1M` (2024) | fora do top 25 (≤ 2.740) | 801 |
| lci ou cdb | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | fora do top 25 (≤ 2.740) | 797 |
| como comprar bitcoin | cripto | `1EGx_IxWSbo` (2022) | fora do top 25 (≤ 2.740) | 792 |
| como investir em bitcoins | cripto | `1EGx_IxWSbo` (2022) | fora do top 25 (≤ 2.740) | 747 |
| lca | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | fora do top 25 (≤ 2.740) | 716 |
| cdb | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | fora do top 25 (≤ 2.740) | 706 |
| como operar opcoes | ações e empresas | `aYQbBXHy0Y0` (2020) | fora do top 25 (≤ 2.740) | 684 |
| fundo imobiliario | FII | `kipRQb0ksus` (2023) | fora do top 25 (≤ 2.740) | 649 |
| simulador bolsa de valores | ações e empresas | `H6uTn-HXTTQ` (2019) | fora do top 25 (≤ 2.740) | 600 |
| spyi11 | ETF e exterior | `Y4WHQiKcv1g` (2024) | fora do top 25 (≤ 2.740) | 599 |
| simulador de bolsa de valores | ações e empresas | `H6uTn-HXTTQ` (2019) | fora do top 25 (≤ 2.740) | 590 |
| luiz barsi | ações e empresas | `XBJqP2JTkkQ` (2022) | fora do top 25 (≤ 2.740) | 580 |
| cdb ou lci | tesouro e renda fixa | `Q1WMbZZn2Ik` (2025) | fora do top 25 (≤ 2.740) | 511 |
| mercado de opcoes na pratica | ações e empresas | `aYQbBXHy0Y0` (2020) | fora do top 25 (≤ 2.740) | 497 |
| carteira do barsi | ações e empresas | `XBJqP2JTkkQ` (2022) | fora do top 25 (≤ 2.740) | 488 |
| irbr3 vale a pena | ações e empresas | `nSQELM25nU8` (2022) | fora do top 25 (≤ 2.740) | 483 |
| melhor fundo imobiliario para 2023 | FII | `kipRQb0ksus` (2023) | fora do top 25 (≤ 2.740) | 477 |
| como operar opcoes na bolsa | ações e empresas | `aYQbBXHy0Y0` (2020) | fora do top 25 (≤ 2.740) | 466 |
| operando opcoes na pratica | ações e empresas | `aYQbBXHy0Y0` (2020) | fora do top 25 (≤ 2.740) | 463 |
| carteira de acoes | ações e empresas | `XBJqP2JTkkQ` (2022) | fora do top 25 (≤ 2.740) | 463 |
| ethereum | cripto | `1EGx_IxWSbo` (2022) | fora do top 25 (≤ 2.740) | 450 |
| crise financeira 2023 | crise e macro | `PoY4WqA1k5Q` (2023) | fora do top 25 (≤ 2.740) | 449 |
| bolsa de valores | ações e empresas | `XBJqP2JTkkQ` (2022) | fora do top 25 (≤ 2.740) | 436 |
| operando opcoes | ações e empresas | `aYQbBXHy0Y0` (2020) | fora do top 25 (≤ 2.740) | 428 |
| etf dividendos | ETF e exterior | `Y4WHQiKcv1g` (2024) | fora do top 25 (≤ 2.740) | 417 |
| recessao 2023 | crise e macro | `PoY4WqA1k5Q` (2023) | fora do top 25 (≤ 2.740) | 406 |
| criptomoeda | cripto | `1EGx_IxWSbo` (2022) | fora do top 25 (≤ 2.740) | 389 |
| hash11 | cripto | `YxLzaSN2a1M` (2024) | fora do top 25 (≤ 2.740) | 383 |
| opcoes na pratica | ações e empresas | `aYQbBXHy0Y0` (2020) | fora do top 25 (≤ 2.740) | 379 |

## Termos que são pergunta curta → o Short (ou longo) do calendário v2 que responde

| termo | views da Pesquisa (vitalício) | categoria | pauta do calendário v2 |
|---|---|---|---|
| como investir em criptomoedas | 1.811 | cripto | 19/11 (longo): Bitcoin depois do 'alerta': o que mudou desde fevereiro |
| como juntar 1 milhao de reais | 1.803 | juntar dinheiro e aposentadoria | 07/10 (short): Como juntar 1 milhão de reais com R$ 1.000 por mês |
| como fazer 1 milhao de reais | 935 | juntar dinheiro e aposentadoria | 07/10 (short): Como juntar 1 milhão de reais com R$ 1.000 por mês |
| lci ou cdb | 797 | tesouro e renda fixa | 05/10 (short): LCI e LCA ou CDB: qual rende mais depois do imposto? |
| como comprar bitcoin | 792 | cripto | 19/11 (longo): Bitcoin depois do 'alerta': o que mudou desde fevereiro |
| como investir em bitcoins | 747 | cripto | 19/11 (longo): Bitcoin depois do 'alerta': o que mudou desde fevereiro |
| como operar opcoes | 684 | ações e empresas | sem pauta: candidato a Short |
| cdb ou lci | 511 | tesouro e renda fixa | 05/10 (short): LCI e LCA ou CDB: qual rende mais depois do imposto? |
| irbr3 vale a pena | 483 | ações e empresas | sem pauta: candidato a Short |
| como operar opcoes na bolsa | 466 | ações e empresas | sem pauta: candidato a Short |
| como funciona o bitcoin | 339 | cripto | 19/11 (longo): Bitcoin depois do 'alerta': o que mudou desde fevereiro |
| como investir em opcoes | 338 | ações e empresas | sem pauta: candidato a Short |
| etfs vale a pena | 236 | ETF e exterior | sem pauta: candidato a Short |
| lci lca ou cdb | 213 | tesouro e renda fixa | 05/10 (short): LCI e LCA ou CDB: qual rende mais depois do imposto? |
| como calcular preco medio de acao | 202 | ações e empresas | sem pauta: candidato a Short |
| lca ou cdb | 190 | tesouro e renda fixa | 05/10 (short): LCI e LCA ou CDB: qual rende mais depois do imposto? |
| como juntar um milhao de reais | 182 | juntar dinheiro e aposentadoria | 07/10 (short): Como juntar 1 milhão de reais com R$ 1.000 por mês |
| como investir na bolsa de valores | 179 | ações e empresas | sem pauta: candidato a Short |
| como investir em lci e lca | 163 | tesouro e renda fixa | 05/10 (short): LCI e LCA ou CDB: qual rende mais depois do imposto? |
| o que sao opcoes no mercado financeiro | 153 | ações e empresas | sem pauta: candidato a Short |
| como operar na bolsa de valores | 153 | ações e empresas | sem pauta: candidato a Short |
| cdb prefixado ou pos fixado | 138 | tesouro e renda fixa | 14/11 (longo): CDB prefixado ou pós-fixado: qual rende mais em 2026 |
| qual melhor fundo imobiliario para 2023 | 137 | FII | 07/11 (longo): Fundos imobiliários para iniciantes: de onde vem a renda |
| como chegar no primeiro milhao | 133 | juntar dinheiro e aposentadoria | 07/10 (short): Como juntar 1 milhão de reais com R$ 1.000 por mês |
| como fazer um milhao de reais | 124 | juntar dinheiro e aposentadoria | 07/10 (short): Como juntar 1 milhão de reais com R$ 1.000 por mês |

## Termos amplos (Short do "1 centavo" e genéricos de dinheiro): os 15 maiores

| termo | vídeo | Pesquisa, últimos 6 meses | vitalício (no vídeo) |
|---|---|---|---|
| como ganhar dinheiro na internet | `aDL4MMF6AnE` | 62.554 | 220.520 |
| como ganhar dinheiro | `aDL4MMF6AnE` | 36.235 | 109.875 |
| como ficar rico | `aDL4MMF6AnE` | 23.928 | 82.935 |
| como investir dinheiro | `aDL4MMF6AnE` | 13.326 | 48.270 |
| como fazer dinheiro na internet | `aDL4MMF6AnE` | 10.218 | 34.395 |
| investimento | `aDL4MMF6AnE` | 8.782 | 28.380 |
| ganhar dinheiro na internet | `aDL4MMF6AnE` | 8.148 | 31.135 |
| como fazer dinheiro | `aDL4MMF6AnE` | 8.126 | 25.455 |
| como ganhar dinheiro em casa | `aDL4MMF6AnE` | 7.876 | 29.467 |
| como juntar dinheiro | `aDL4MMF6AnE` | 7.862 | 22.538 |
| renda extra | `aDL4MMF6AnE` | 6.631 | 26.394 |
| ganhar dinheiro | `aDL4MMF6AnE` | 5.143 | 17.732 |
| como conseguir dinheiro | `aDL4MMF6AnE` | 3.916 | 11.492 |
| como ganhar dinheiro facil | `aDL4MMF6AnE` | 3.891 | 12.660 |
| como investir | `aDL4MMF6AnE` | 3.889 em 5 meses (+ ≤ 299 nos outros) | 14.976 |

## Bancos, apps e outros do catálogo antigo: os 15 maiores (fora do foco)

| termo | vídeo (ano) | Pesquisa, últimos 6 meses | vitalício |
|---|---|---|---|
| caixinha turbo nubank | `_WHHib_xvJ4` (2025) | 1.483 em 2 meses (+ ≤ 1.402 nos outros) | 56.612 |
| banco next | `T956DmDdPDU` (2018) | fora do top 25 (≤ 2.740) | 92.851 |
| next | `T956DmDdPDU` (2018) | fora do top 25 (≤ 2.740) | 82.951 |
| mercado pago | `9tn6b8FaE24` (2025) | 764 em 2 meses (+ ≤ 2.157 nos outros) | 4.824 |
| cartao next | `T956DmDdPDU` (2018) | fora do top 25 (≤ 2.740) | 55.964 |
| banco original | `CaOGCAsOLvE` (2019) | fora do top 25 (≤ 2.740) | 39.928 |
| banco next vale a pena | `T956DmDdPDU` (2018) | fora do top 25 (≤ 2.740) | 20.373 |
| nextjoy | `V68Hd157uac` (2021) | fora do top 25 (≤ 2.740) | 16.508 |
| pedacinho nubank | `_I5dFQ6mvK0` (2021) | fora do top 25 (≤ 2.740) | 11.224 |
| conta next | `T956DmDdPDU` (2018) | fora do top 25 (≤ 2.740) | 9.976 |
| sousmile | `9Jt4U0uhd_U` (2021) | fora do top 25 (≤ 2.740) | 7.409 |
| next banco | `T956DmDdPDU` (2018) | fora do top 25 (≤ 2.740) | 7.159 |
| como funciona a caixinha turbo da nubank | `_WHHib_xvJ4` (2025) | fora do top 25 (≤ 2.740) | 7.154 |
| c6 bank | `yN0kKJf2D1c` (2019) | fora do top 25 (≤ 2.740) | 7.043 |
| caixinha turbo nubank como funciona | `_WHHib_xvJ4` (2025) | fora do top 25 (≤ 2.740) | 6.915 |

## Para fechar a lacuna dos últimos 6 meses (no Mac)

```sh
cd ~/IPADTEST && git pull && cd auditoria-canal \
  && set -a && source ~/.config/investirecocar/credentials.env && set +a \
  && python3 exportar.py --termos-recentes 180 \
  && cd .. && git add auditoria-canal/dados/termos_busca_recentes.csv auditoria-canal/dados/LEIAME_DADOS.md \
  && git commit -m "auditoria-canal: termos de busca recentes" && git push
```

O comando pega os 25 termos de cada vídeo publicado nos últimos 180 dias e dos 50 com mais busca, só no período,
em cerca de 120 consultas ao Analytics. Com ele, a coluna dos 6 meses passa a vir por vídeo, e não do top 25 do canal,
que o "1 centavo" domina.
