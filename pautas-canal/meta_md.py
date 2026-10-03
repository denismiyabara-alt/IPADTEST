"""Texto do META.md (separado de meta.py para os testes não dependerem do texto)."""
import statistics

import modelo as mo
from modelo import an


def br(x, casas=0):
    if x is None:
        return "—"
    s = f"{x:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def mes_br(m):
    nomes = "jan fev mar abr mai jun jul ago set out nov dez".split()
    return f"{nomes[int(m[5:]) - 1]}/{m[2:4]}" if m else "—"


def markdown(r):
    import meta as me
    b, p, d = r["b"], r["p"], r["d"]
    L, S = b["longo"], b["short"]
    rk, tot, _ = mo.ranking(d, "longo", "12 meses")
    por = {x["assunto"]: x for x in rk}
    eng_plano = sum(n * por.get(a, tot)["eng_med"] for a, n in me.PLANO_LONGOS.items())
    n_plano = sum(me.PLANO_LONGOS.values())
    insc_mil_plano = (p["novos"] - me.PLANO_SHORTS * S["esperado"]) / eng_plano * 1000
    st = an.origens_studio(d)
    busca = {m: an.pct(st["longos"][m].get("YT_SEARCH", 0), sum(st["longos"][m].values())) for m in ("2026-08", "2026-09")}
    so = mo.origens_studio_shorts_sem_outlier(d)
    mes_set = next(x for x in d.mes if x["mes"] == "2026-09")
    pub_set = b["pub_ultimos"]["2026-09"]
    cal = {nome: c for nome, _, c in r["cen"]}
    c26, c27a, c27b = cal["31/12/2026"], cal["30/06/2027"], cal["31/12/2027"]
    vl, _ = mo.videos(d, "longo", "12 meses")
    perdas3 = statistics.mean(an.num(x["inscritos_perdidos"]) or 0 for x in d.mes[-3:])

    def acima(x):
        return sum(1 for v in vl if an.ganhos(v) >= x)
    hoje_quando = r["hoje"][0]
    out = []
    add = out.append
    add(f"""# Meta de 200 mil inscritos: desdobramento

Gerado por `meta.py`, com os dados de `auditoria-canal/dados/` (exportação de 02/10/2026) e o ranking de `TEMAS.md`.
A mesma conta, em números, está em `meta.csv`.

## Resposta curta

- **200 mil em 31/12/2026 não acontece.** São {br(c26['liquidos'])} inscritos líquidos por mês, {br(c26['x_ritmo'], 0)}
  vezes o ritmo atual. Nenhuma produção possível fecha essa conta.
- **Em 30/06/2027 também não.** São {br(c27a['liquidos'])} líquidos por mês ({br(c27a['x_ritmo'], 1)}x o ritmo), o que pede
  {br(c27a['longos_insc_p90'])} longos por mês, todos no nível do p90 do último ano.
- **Em 31/12/2027 exige uma mudança de patamar.** São {br(c27b['liquidos'])} líquidos por mês
  ({br(c27b['x_ritmo'], 1)}x o ritmo). Com 12 longos por mês, o máximo que o canal já publicou num mês, cada longo
  teria de trazer {br(c27b['insc_por_longo_no_max'])} inscritos. Só {acima(c27b['insc_por_longo_no_max'])} dos {len(vl)} longos do último ano passaram disso.
  Isso só fecha com vídeos que estouram com frequência, não com a média.
- **No ritmo atual**, de {br(b['liq_6m'])} líquidos por mês (média de 6 meses), os 200 mil chegam em
  **{mes_br(f"{hoje_quando:%Y-%m}")}**.
- **Cenário recomendado: o plano de produção abaixo.**
  - **Produção:** 12 longos por mês, com o mix escolhido pelo ranking de temas, e 8 Shorts por mês.
  - **Resultado:** cerca de {br(p['liquidos'])} líquidos por mês, 2,7 vezes o ritmo de hoje, e os 200 mil em
    **{mes_br(r['quando'])}** (faixa de {mes_br(r['quando75'])} a {mes_br(r['quando25'])}).
  - **A alternativa** para 31/12/2027 é a mesma produção com a média por vídeo no nível dos top do ano.

## A árvore da meta

```
inscritos líquidos/mês = ganhos − perdas
  hoje:  {br(b['liq_6m'])} na média de 6 meses ({br(b['liq_ult'])} em setembro)
         jul-set: {br(b['ganhos_3m'])} ganhos − {br(perdas3)} perdas = {br(b['ganhos_3m'] - perdas3)} líquidos por mês
         perdas usadas no plano: {br(b['perdas_6m'])} (média de 6 meses)
  ganhos = catálogo + vídeos novos
    catálogo (vídeos antigos + inscrições fora de vídeo): {br(b['catalogo'])}/mês
        = ganhos de jul-set − inscritos dos {len([1 for v in d.v.values() if v['publicado'] and f"{v['publicado']:%Y-%m}" in b['meses_trimestre']])} vídeos publicados em jul-set, por mês
    vídeos novos = Σ formato × assunto (nº de vídeos × inscritos esperados por vídeo)
      inscritos esperados por vídeo = views intencionais medianas × inscritos por mil views intencionais
        longos (12 meses, n = {L['n']}): {br(L['eng_med'])} × {br(L['insc_mil'], 1)}/mil = {br(L['esperado'])} por vídeo
                                     (p25–p75: {br(L['esperado_p25'])}–{br(L['esperado_p75'])}; real por vídeo: mediana {br(L['insc_med'])}, p75 {br(L['insc_p75'])}, p90 {br(L['insc_p90'])})
        Shorts (12 meses, n = {S['n']}, sem o "1 centavo"): {br(S['eng_med'])} × {br(S['insc_mil'], 2)}/mil = {br(S['esperado'], 1)} por vídeo
      hoje: ~{br(b['longos_mes_med'])} longos e ~{br(b['shorts_mes_med'], 1)} Shorts por mês (medianas de 12 meses)
```

**A árvore fecha com os números de hoje.**
- **Vídeos novos:** 8 longos × {br(L['esperado'])} + 5,5 Shorts × {br(S['esperado'], 1)} ≈ {br(8 * L['esperado'] + 5.5 * S['esperado'])}.
- **Catálogo:** + {br(b['catalogo'])}.
- **Perdas:** − {br(b['perdas_6m'])}.
- **Total:** ≈ {br(8 * L['esperado'] + 5.5 * S['esperado'] + b['catalogo'] - b['perdas_6m'])} líquidos por mês, contra os
  {br(b['liq_6m'])} reais da média de 6 meses.

**Por que mediana e não média:** a média de inscritos dos longos do ano é {br(L['insc_total'] / L['n'])} por vídeo, contra
{br(L['insc_med'])} na mediana, porque 5 vídeos fizeram 39% dos inscritos. Nos Shorts, o "1 centavo" (9.675 inscritos) fica
fora: sem ele, um Short novo traz cerca de 1 inscrito.

## Os três prazos

| prazo | meses | líquidos/mês | × ritmo atual | ganhos brutos/mês (+ perdas) | vindos de vídeos novos (− catálogo) | views intencionais/mês nos vídeos novos | longos/mês no nível mediano | … no p75 | … no p90 | inscritos por longo com 12 longos/mês |
|---|---|---|---|---|---|---|---|---|---|---|""")
    for nome, _, c in r["cen"]:
        add(f"| {nome} | {br(c['meses'], 1)} | {br(c['liquidos'])} | {br(c['x_ritmo'], 1)}x | {br(c['ganhos'])} | {br(c['novos'])} | "
            f"{br(c['views_intenc_novos'])} | {br(c['longos_insc_med'])} | {br(c['longos_insc_p75'])} | {br(c['longos_insc_p90'])} | "
            f"{br(c['insc_por_longo_no_max'])} |")
    add(f"""
**O que a produção histórica permite:**
- **Longos:** mediana de {br(b['longos_mes_med'])} por mês nos últimos 12 meses; máximo de {b['longos_mes_max']} num mês
  (fev e set/2024).
- **Shorts:** mediana de {br(b['shorts_mes_med'], 1)} por mês; máximo de {b['shorts_mes_max']} (jun/2026).

**Leitura:**
- **31/12/2026:** impossível. Com a produção máxima, cada longo teria de trazer {br(c26['insc_por_longo_no_max'])} inscritos.
  O melhor vídeo do ano trouxe 637.
- **30/06/2027:** impossível no patamar atual. Pede {br(c27a['insc_por_longo_no_max'])} inscritos por longo, com 12 longos
  por mês. Só {acima(c27a['insc_por_longo_no_max'])} dos {len(vl)} longos do último ano chegaram lá.
- **31/12/2027:** exige mudança de patamar: 12 longos por mês, cada um com {br(c27b['insc_por_longo_no_max'])} inscritos,
  acima do p90 ({br(L['insc_p90'])}). No último ano, {acima(c27b['insc_por_longo_no_max'])} longos chegaram lá, menos de
  1 por mês; o plano pediria 12 por mês. É um alvo para ser revisto a cada trimestre, não um plano.

## Cenário recomendado: plano de produção

O mix de longos sai do ranking de inscritos esperados por vídeo dos últimos 12 meses (`TEMAS.md`). Dá mais espaço ao que
rende e menos a "ações e empresas", que é o assunto mais produzido (28 dos 80 longos) e rende {br(por['ações e empresas']['esperado'])} por vídeo.

| assunto | longos/mês | inscritos esperados por vídeo | faixa p25–p75 | n (12 meses) |
|---|---|---|---|---|""")
    for a, n, e, e25, e75, nn in p["linhas"]:
        add(f"| {a} | {br(n, 1)} | {br(e)} | {br(e25)}–{br(e75)} | {nn} |")
    add(f"""| **Shorts** | {me.PLANO_SHORTS} | {br(S['esperado'], 1)} | {br(S['esperado_p25'], 1)}–{br(S['esperado_p75'], 1)} | {S['n']} |
| **Total de vídeos novos** | {br(n_plano, 1)} longos + {me.PLANO_SHORTS} Shorts | **{br(p['novos'])} inscritos/mês** | {br(p['novos_p25'])}–{br(p['novos_p75'])} | |

**Resultado do plano em regime** (a partir de jan/27):
- **Conta:** {br(b['catalogo'])} do catálogo + {br(p['novos'])} dos vídeos novos − {br(b['perdas_6m'])} de perdas =
  **{br(p['liquidos'])} líquidos por mês** (faixa de {br(p['liquidos_p25'])} a {br(p['liquidos_p75'])}).
- **Prazo:** os 200 mil chegam em **{mes_br(r['quando'])}**. Na faixa otimista (p75), em {mes_br(r['quando75'])}; na
  pessimista (p25), em {mes_br(r['quando25'])}.

**Premissas, para revisar a cada trimestre:**
- **O ranking se repete:** tesouro e renda mensal têm n = 5 e n = 7, e o número deles é puxado pelos top. A tendência é
  cair em direção à média.
- **Catálogo constante:** ele cai devagar, mas os vídeos novos viram catálogo.
- **Perdas** na média de 6 meses.
- **Defasagem:** os inscritos de cada vídeo chegam 60% no mês da publicação, 25% no seguinte e 15% no outro.
- **Rampa:** em out/26, a produção é de 75% do plano (calendário v2). O calendário oficial, v3 (`CALENDARIO.md`),
  tem 11 longos de 05/10 a 31/10 e compara a estimativa dele com estas metas.

## Metas mensais (cenário recomendado)

Hoje = set/26. Na coluna de inscritos líquidos, o "hoje" é {br(b['liq_ult'])} (set/26); na média de 6 meses, {br(b['liq_6m'])}.

| mês | inscritos líquidos | ganhos | perdas | longos | Shorts | inscritos no fim do mês |
|---|---|---|---|---|---|---|""")
    for m in r["mensal"]:
        add(f"| {mes_br(m['mes'])} | **{br(m['liquidos'])}** | {br(m['ganhos'])} | {br(m['perdas'])} | {m['longos']} | {m['shorts']} | "
            f"{br(m['inscritos_fim_mes'])} |")
    eng_l_hoje = (an.num(mes_set["engagedViews"]) or 0) - mo.RAZAO_INTENC_SHORTS * (an.views_mensais_studio(d)["short"]["2026-09"])
    add(f"""
### Indicadores de acompanhamento (meta mensal em regime × hoje)

| indicador | meta mensal (regime) | hoje | fonte do "hoje" |
|---|---|---|---|
| inscritos líquidos | {br(p['liquidos'])} (out: {br(r['mensal'][0]['liquidos'])}; nov: {br(r['mensal'][1]['liquidos'])}) | {br(b['liq_ult'])} em set; {br(b['liq_6m'])} na média de 6 meses | canal_por_mes (Analytics) |
| views intencionais dos longos novos | {br(eng_plano)} ({br(n_plano, 1)} longos × medianas do mix) | ~{br(8 * L['eng_med'])} (8 longos × {br(L['eng_med'])}); todos os longos em set: ~{br(eng_l_hoje)} (estimativa*) | analytics_por_video, longos de 12 meses |
| views de Shorts sem o "1 centavo" | ≥ {br(me.PLANO_SHORTS * 4789)} (8 × mediana de 4.789) | {br(so.get('2026-09'))} em set; {br(so.get('2026-06'))} em jun | Studio E2 (Total − gráfico do outlier) |
| inscritos por mil views intencionais (longos novos) | {br(insc_mil_plano, 1)} | {br(L['insc_mil'], 1)} | analytics_por_video, 12 meses |
| publicações | 12 longos + 8 Shorts | {pub_set['longo']} longos + {pub_set['short']} Shorts em set | videos.csv |
| % das views de longos pela Pesquisa | ≥ 15% | {br(busca['2026-09'], 1)}% em set (diluída pela Navegação inflada); {br(busca['2026-08'], 1)}% em ago | Studio E3, longos |
| CTR da Pesquisa (longos) | ≥ 13,3% | 12,3% (vitalício; a API não dá CTR por mês) | Studio E3; acompanhar no Studio todo mês |
| CTR geral das impressões (longos) | ≥ 7,1% | 7,1% (vitalício) | Studio E1 |

\\* Views intencionais do canal (canal_por_mes) − {br(mo.RAZAO_INTENC_SHORTS, 2)} × views de Shorts (Studio). O 0,43 é a
razão intencional/views dos Shorts em agosto, antes do efeito de 27/08.

## Metas semanais (out e nov/26)

A meta semanal é a mensal ÷ 4,33. A coluna de longos é a do plano (rampa do calendário v2: 2 por semana até 25/10 e 3
depois). O calendário oficial, v3 (`CALENDARIO.md`), já tem 3 longos por semana a partir de 12/10 e nunca mais de 3.

| semana | inscritos líquidos | ganhos | longos | Shorts |
|---|---|---|---|---|""")
    for s in r["semanas"]:
        add(f"| {s['semana']} | {br(s['liquidos'])} | {br(s['ganhos'])} | {s['longos']} | {s['shorts']} |")
    add("""
**Como acompanhar:** toda segunda, com os números da semana anterior no Studio (inscritos ganhos e perdidos, views
intencionais, % da Pesquisa e CTR). Se duas semanas seguidas ficarem abaixo de 70% da meta, troque a pauta da quinta
seguinte pela do assunto com maior inscrito esperado (`TEMAS.md`).

## Sensibilidade: o que cada alavanca move

São inscritos por mês a mais em regime, sobre o ritmo de hoje, com a faixa de incerteza. A ordem é pelo valor central.

| # | alavanca | inscritos/mês (central) | faixa | base do número |
|---|---|---|---|---|""")
    for i, a in enumerate(r["alavancas"], 1):
        add(f"| {i} | {a['alavanca']} | **{br(a['central'])}** | {br(a['min'])} a {br(a['max'])} | {a['base']} |")
    add(f"""
**Correção do relatório (ação 6):** o RELATORIO.md estimava que voltar a 8 Shorts por mês recuperaria cerca de 200
inscritos por mês. Por vídeo, porém, um Short novo traz cerca de {br(S['esperado'], 1)} inscrito. A maior parte das views
de Shorts é do "1 centavo", que caiu de 169 mil (jul) para 97 mil (set), e ele não volta com produção. A faixa honesta
para a alavanca dos Shorts vai de {br(r['alavancas'][-1]['min'] if r['alavancas'][-1]['alavanca'].startswith('Voltar') else 2)} a
cerca de 126 inscritos por mês; o valor alto supõe que cada view de Short novo converte como na regressão mensal. Os
Shorts continuam úteis para alcance e para levar público aos longos, mas não sustentam a meta sozinhos.

## Limites

- **"Inscritos esperados por vídeo"** usa os inscritos atribuídos pelo Analytics ao vídeo, no vitalício de vídeos com 1 a
  12 meses de vida. Os mais novos ainda vão ganhar um pouco.
- **Amostras pequenas:** renda mensal (n = 7), tesouro (n = 5), cripto (n = 4) e FII (n = 6). As faixas p25–p75 mostram o
  tamanho da incerteza.
- **Contador arredondado:** o total de 165.000 é arredondado pelo YouTube.
- **Views infladas desde 27/08 (H1):** todas as metas de views usam views intencionais, não o contador.
""")
    return "\n".join(out)
