#!/usr/bin/env python3
"""Calendário v2 (05/10 a 29/11/2026): pautas escolhidas pelo ranking de inscritos esperados por vídeo (TEMAS.md) e
pela demanda de busca do próprio canal, com os inscritos esperados de cada pauta e a soma semanal comparada com a
meta semanal de META.md. Gera CALENDARIO-8-SEMANAS.md e .csv. A v1 está em CALENDARIO-8-SEMANAS_v1.*.

O assunto de cada pauta sai do PRÓPRIO TÍTULO (analisar.assunto); o teste confere que bate com o planejado.

uso: python3 calendario_v2.py
"""
import csv
from collections import defaultdict
from datetime import date, timedelta
from pathlib import Path

import meta as me
import termos
from collections import Counter
import modelo as mo
import temas

AQUI = Path(__file__).resolve().parent
DIAS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]

# (data, formato, assunto planejado, título, palavra-chave, volume e base, continuação de, ângulo, conferir)
L = "longo"
S = "short"
PAUTAS = [
    # ------------------------------------------------------------------ semana 1
    ("2026-10-05", S, "tesouro e renda fixa", "LCI e LCA ou CDB: qual rende mais depois do imposto?", "CDB ou LCI",
     "ALTO: Q1WMbZZn2Ik, 57.527 views da Pesquisa (77%)", "", "Taxa equivalente com a alíquota de IR do prazo.",
     "Lei 11.033/2004; prazo mínimo de LCI vigente"),
    ("2026-10-06", L, "renda mensal", "ETFs que pagam dividendos mensais: o que mudou em 2026",
     "ETF dividendos mensais", "ALTO: Y4WHQiKcv1g, 26.783 views da Pesquisa (44%)", "Fb0l4KEq27o (637 inscritos)",
     "O que aconteceu com cada ETF da lista de 2025 (pagamento real, taxa, patrimônio) e as dúvidas dos comentários.",
     "B3 (proventos); lâminas dos ETFs"),
    ("2026-10-07", S, "juntar dinheiro e aposentadoria", "Como juntar 1 milhão de reais com R$ 1.000 por mês",
     "juntar 1 milhão", "ALTO: tbKsF2qyakU, 46.026 views da Pesquisa (70%)", "",
     "Com 6% ao ano acima da inflação, ~R$ 535 mil em 22 anos e 1 milhão em ~30. Saiu do longo da v1: como longo, "
     "o assunto rende 14 por vídeo; como Short, é o 2º melhor no vitalício e vive de busca.", "Selic e IPCA do dia"),
    ("2026-10-08", L, "tesouro e renda fixa", "Tesouro IPCA+ a 7% em janeiro: quanto ganhou quem comprou",
     "Tesouro IPCA+ marcação a mercado", "BAIXO: dHYQtxnMSrw, 2.072 views da Pesquisa (7%)", "dHYQtxnMSrw (421)",
     "Prestação de contas do vídeo de janeiro: preço na compra e hoje, cupons, marcação.", "Tesouro Direto (histórico)"),
    # ------------------------------------------------------------------ semana 2
    ("2026-10-12", S, "tesouro e renda fixa", "Resgatou o CDB antes de 30 dias? O IOF come o rendimento",
     "IOF CDB 30 dias", "MÉDIO: pergunta repetida nos comentários do Short _WHHib_xvJ4 (59% das views pela Pesquisa)", "",
     "Tabela regressiva do IOF em 40 s.", "Decreto 6.306/2007"),
    ("2026-10-13", L, "renda mensal", "Dividendos mensais com ações: como montar um calendário",
     "ações que pagam dividendos todo mês", "ALTO: TY8oLvUt2Qg, 49% das views pela Pesquisa", "TY8oLvUt2Qg (324)",
     "'Todo mês' é calendário, não promessa: data com, pagamento e por que o valor varia. Sem lista de compra.",
     "B3 (eventos corporativos); JCP 17,5% (LC 224/2025)"),
    ("2026-10-14", S, "tesouro e renda fixa", "Tesouro IPCA+ negativo? Calma, isso tem nome",
     "Tesouro IPCA+ caiu", "BAIXO: vídeos de IPCA+ do canal têm de 1% a 9% das views pela Pesquisa", "",
     "Marcação a mercado em 40 s; corte do longo de 08/10.", "Tesouro Direto"),
    ("2026-10-15", L, "crise e macro", "Crise financeira: o gráfico de 1929, 2008 e 2020, hoje",
     "sinal de crise 2026", "BAIXO: IcN3m7whpl8, 1.161 views da Pesquisa (4%)", "IcN3m7whpl8 (357)",
     "Revisão honesta do indicador: o que marcava, o que marca, alarmes falsos.", "Série do indicador original"),
    # ------------------------------------------------------------------ semana 3
    ("2026-10-19", S, "imposto e regras", "FII é isento de imposto? Só se cumprir estas 3 regras",
     "FII isento de imposto", "MÉDIO: vídeos de FII do canal, 35.246 views da Pesquisa (14%)", "",
     "Lei 14.754/2023: 100 cotistas ou mais, cotas em bolsa e menos de 10% das cotas; ganho na venda paga 20%.",
     "Lei 14.754/2023; Lei 8.668/1993"),
    ("2026-10-20", L, "renda mensal", "Dividendos sintéticos: o ETF que paga todo mês com opções",
     "ETF opções cobertas dividendos mensais", "BAIXO: IB1mBcF00jc, 1.126 views da Pesquisa (5,5%)", "IB1mBcF00jc (131)",
     "Mecânica das opções cobertas, renda alta e alta limitada, comparada com ETF de dividendos comum.",
     "Regulamento do ETF/BDR"),
    ("2026-10-21", S, "comportamento e família", "Casal que investe junto: a conversa que vem antes do dinheiro",
     "casal finanças", "BAIXO: sem vídeo de busca; é o assunto de Short com mais inscritos por vídeo em 12 meses", "",
     "Uma pergunta para fazer antes de investir a dois.", "—"),
    ("2026-10-22", L, "tesouro e renda fixa", "LCI e LCA ou CDB: a conta de 2026 com imposto e prazo", "CDB ou LCI",
     "ALTO: Q1WMbZZn2Ik, 57.527 views da Pesquisa (77%)", "",
     "Taxa equivalente, carência mínima, liquidez e FGC; responde '80 mil em LCI por 12 meses?' sem recomendar.",
     "Lei 11.033/2004; resolução do CMN sobre prazos; fgc.org.br"),
    # ------------------------------------------------------------------ semana 4
    ("2026-10-26", S, "tesouro e renda fixa", "FGC: o que cobre e o que não cobre", "FGC",
     "MÉDIO: FC-eKTK3ozE, 3.247 views da Pesquisa (36%)", "",
     "R$ 250 mil por CPF por instituição, teto de R$ 1 milhão a cada 4 anos; não cobre Tesouro, fundos e ações.",
     "fgc.org.br"),
    ("2026-10-27", L, "renda mensal", "ETF de dividendos mensais ou fundo imobiliário: o que sobra",
     "ETF ou FII renda mensal", "MÉDIO: vídeos de dividendos mensais com 14% a 44% das views pela Pesquisa",
     "lwV6tbkk4Cw (93)", "Comparar como cada um paga, a tributação de cada um em 2026 e a volatilidade da renda.",
     "Lei 14.754/2023; regulamentos"),
    ("2026-10-28", S, "tesouro e renda fixa", "Quanto rende R$ 1.000 no Tesouro Selic hoje", "quanto rende 1000 tesouro selic",
     "MÉDIO: Kwf4IvhOb9s ('quanto rende R$ 1.000'), 2.748 views da Pesquisa (16%)", "",
     "A conta líquida de IR em 30 s.", "Taxa do Tesouro Selic do dia"),
    ("2026-10-29", L, "crise e macro", "Recessão em 2026? Os sinais de crise de 2025, um a um",
     "crise 2026", "BAIXO: tpobf1e1OtM, 624 views da Pesquisa (2%)", "tpobf1e1OtM (345)",
     "Cada sinal do vídeo original com o dado de hoje, sem repetir o alarme.", "BCB/SGS, IBGE, FRED"),
    ("2026-10-31", L, "cripto", "ETF de bitcoin na B3: como funciona e quanto custa", "ETF de bitcoin",
     "MÉDIO: vídeos de bitcoin do canal, 268.961 views da Pesquisa (55%), quase todas antigas", "eZE1d_CHlPU (101)",
     "Como o ETF replica o bitcoin, taxa, imposto e diferença para a cripto direta. Sem indicar compra.",
     "Regulamentos; regra de IR de ETF"),
    # ------------------------------------------------------------------ semana 5 (Copom 03-04/11)
    ("2026-11-02", S, "imposto e regras", "JCP em 2026: já vem com 17,5% de imposto", "JCP imposto",
     "BAIXO: 3sfCQWv2kIQ, 962 views da Pesquisa (4%)", "",
     "Saiu do longo da v1: imposto rende 16 por longo. O JCP é retido na fonte com 17,5% (LC 224/2025).",
     "LC 224/2025"),
    ("2026-11-03", L, "renda mensal", "Quanto investir para receber R$ 1.000 por mês",
     "quanto investir para ter renda de 1000 por mês", "MÉDIO: sem vídeo igual; 'juntar 1 milhão' tem 70% a 81% das "
     "views pela busca", "", "Capital necessário em três classes, líquido de imposto. Sem indicar ativos.",
     "Taxas do Tesouro; IFIX; regras de IR"),
    ("2026-11-04", S, "tesouro e renda fixa", "Copom hoje: 3 números para olhar no seu Tesouro", "Copom hoje",
     "MÉDIO: vídeos de Copom/Selic do canal, 11.321 views da Pesquisa (9%)", "KMIsVEOcaLM (246)",
     "Pré-decisão: taxa do IPCA+, do prefixado e a Selic esperada.", "Taxas do Tesouro do dia"),
    ("2026-11-05", L, "tesouro e renda fixa", "Copom de novembro: o que muda no Tesouro IPCA+ e prefixado",
     "Copom novembro 2026", "MÉDIO: vídeos de Copom/Selic, 11.321 views da Pesquisa (9%)",
     "KMIsVEOcaLM (246) e tb0nwpl9mFw (142)", "Dia seguinte à decisão de 04/11: comunicado, reação das taxas em 24 h.",
     "Comunicado do Copom (bcb.gov.br); data: conferir em bcb.gov.br/controleinflacao/calendarioreunioescopom"),
    ("2026-11-07", L, "FII", "Fundos imobiliários para iniciantes: de onde vem a renda",
     "fundos imobiliários", "", "kipRQb0ksus (busca de FII, 2023)",
     "TROCA da v2 (era 'recompra de ações', sem nenhum termo de busca e com o assunto que menos rende): como o FII "
     "gera e distribui renda, sem indicar fundos.", "Lei 8.668/1993; Lei 14.754/2023; IFIX (B3)"),
    # ------------------------------------------------------------------ semana 6
    ("2026-11-09", S, "imposto e regras", "Imposto sobre dividendos acima de R$ 50 mil por mês: quem paga",
     "imposto dividendos 2026", "BAIXO: qnWje5V23Ps, 521 views da Pesquisa (5%)", "",
     "Retenção de 10% só acima de R$ 50 mil por mês da mesma empresa (Lei 15.270/2025).", "Lei 15.270/2025"),
    ("2026-11-10", L, "renda mensal", "Renda mensal com Tesouro: juros semestrais e RendA+",
     "Tesouro renda mensal", "MÉDIO: Tesouro tem de 7% a 16% das views pela Pesquisa; renda mensal, de 19% a 49%", "",
     "Como transformar o Tesouro em renda (cupons, RendA+), com a conta do imposto.", "Tesouro Direto (regras dos títulos)"),
    ("2026-11-11", S, "FII", "FII ou aluguel: quanto rende R$ 100 mil em cada um", "FII ou imóvel",
     "MÉDIO: FII vive de Pesquisa nos Shorts (49%, vitalício)", "", "A conta simples do rendimento líquido.",
     "IFIX; índice de aluguel (FipeZap)"),
    ("2026-11-12", L, "FII", "Fundo imobiliário ou imóvel alugado: a conta de 2026", "FII ou imóvel",
     "MÉDIO: vídeos de FII, 35.246 views da Pesquisa (14%)", "Gjw4crGh6Xg (92)",
     "Rendimento, custo, vacância, imposto e liquidez lado a lado.", "IFIX (B3); FipeZap; Lei 14.754/2023"),
    ("2026-11-14", L, "tesouro e renda fixa", "CDB prefixado ou pós-fixado: qual rende mais em 2026",
     "cdb prefixado", "", "7CdwOTT7U3o (CDB prefixado, 2018: 3.928 views da Pesquisa)",
     "TROCA da v2 (era o cobre: commodities tem n = 1 e nenhum termo de busca): a conta prefixado × pós com a curva "
     "de juros de hoje; responde 'cdb prefixado ou pós fixado'.", "Taxas DI futuro (B3); Lei 11.033/2004; FGC"),
    # ------------------------------------------------------------------ semana 7
    ("2026-11-16", S, "comportamento e família", "Perfil de investidor: 3 perguntas antes de investir",
     "perfil de investidor", "BAIXO: Short 'Perfil de investidor' (15 inscritos, 12 mil views intencionais)", "",
     "As perguntas de prazo, objetivo e tolerância a queda.", "—"),
    ("2026-11-17", L, "renda mensal", "ETF de dividendos mensais: quanto a taxa tira da renda",
     "taxa de administração ETF", "BAIXO: sem vídeo do canal com essa palavra", "",
     "A conta de 10 anos com taxas diferentes; responde 'essa taxa de 1,50 é alta?'.", "Lâminas dos ETFs"),
    ("2026-11-18", S, "juntar dinheiro e aposentadoria", "Juros compostos: por que 1 centavo dobrando todo dia não existe",
     "juros compostos", "ALTO: Shorts de juntar dinheiro vivem de busca (33% vitalício); responde 194 comentários", "",
     "A conta do 2³⁰ e a do mundo real.", "—"),
    ("2026-11-19", L, "cripto", "Bitcoin depois do 'alerta': o que mudou desde fevereiro", "bitcoin caiu",
     "MÉDIO: vídeos de bitcoin, 55% das views pela Pesquisa (antigos); JDtxzQthFlk: 2%", "JDtxzQthFlk (224)",
     "Os argumentos de fevereiro com os dados de hoje; 'posso perder mais do que investi?'.",
     "Preço do BTC; regra de declaração (Receita)"),
    ("2026-11-21", L, "crise e macro", "Bolha de inteligência artificial: o que dizem os números", "bolha IA",
     "BAIXO: vídeos de crise com 2% a 6% das views pela Pesquisa", "PWotyrtMXBs (84)",
     "Lucros, investimento e preço das empresas de IA, sem prever topo.", "Resultados trimestrais; FRED"),
    # ------------------------------------------------------------------ semana 8
    ("2026-11-23", S, "tesouro e renda fixa", "Reserva de emergência: onde deixar e onde não deixar",
     "reserva de emergência", "BAIXO: mZ6ohk9JCVY sem dado de Pesquisa (fora do top 300)", "",
     "Liquidez diária, perto de 100% do CDI e FGC.", "fgc.org.br"),
    ("2026-11-24", L, "renda mensal", "Selic caindo: o que acontece com a sua renda mensal", "renda mensal Selic",
     "BAIXO: sem vídeo igual", "", "O que muda nos dividendos, nos FIIs e na renda fixa quando o juro cai, com histórico.",
     "BCB (Selic histórica); IFIX"),
    ("2026-11-25", S, "ETF e exterior", "Taxa de administração do ETF: quanto tira em 10 anos", "taxa ETF",
     "BAIXO: ETF e exterior nos Shorts: 24% das views pela Pesquisa (vitalício)", "",
     "0,5% contra 1,5% ao ano em 10 anos; corte do longo de 17/11.", "Lâminas"),
    ("2026-11-26", L, "FII", "Fundos imobiliários caíram em 2026: e a renda deles?",
     "fundos imobiliários caíram", "MÉDIO: vídeos de FII, 14% das views pela Pesquisa", "8xsUtGCE-vI ('ACABOU O SONHO?')",
     "Cotas × rendimentos distribuídos: o que caiu e o que não caiu.", "IFIX; relatórios gerenciais"),
    ("2026-11-28", L, "tesouro e renda fixa", "Reserva de emergência em 2026: CDB, Tesouro Selic ou conta",
     "reserva de emergência", "BAIXO: mZ6ohk9JCVY, fora do top 300 de tráfego", "",
     "A conta líquida de cada opção, liquidez e FGC. Sem indicar instituição.", "Taxas do dia; fgc.org.br"),
]
# Termo de busca real de cada pauta (TERMOS.md): (termo exibido, família de termos somada). None = nenhum termo nos
# dados; a família ainda é procurada para provar a ausência.
TERMOS = {
    "2026-10-05": ("o que é lci e lca", r"o ?que e lci|lci e lca|lca e lci|lci ou cdb|cdb ou lci|lca ou cdb|^lci$|^lca$"),
    "2026-10-06": ("etfs que pagam dividendos mensais", r"etfs?.*dividendos? mensa|dividendos mensais"),
    "2026-10-07": ("como juntar 1 milhão de reais", r"1 milh|um milh|primeiro milh|1000 reais por mes"),
    "2026-10-08": (None, r"tesouro|ipca|\bntn"),
    "2026-10-13": ("dividendos mensais", r"dividendos? mensa|dividendos? todo mes"),
    "2026-10-15": ("crise financeira", r"crise|recess|colapso"),
    "2026-10-20": ("dividendos sinteticos", r"dividendos? sint|dividendos? turbinad|dividendos? com opc"),
    "2026-10-22": ("lci e lca", r"\blci\b|\blca\b"),
    "2026-10-26": ("fgc", r"\bfgc\b"),
    "2026-10-27": ("etf dividendos", r"etfs?.*dividend"),
    "2026-10-28": ("qual investimento rende mais", r"qual (investimento|cdb) rende mais"),
    "2026-10-29": ("recessão", r"recess|crise"),
    "2026-10-31": ("etf bitcoin", r"etfs? (de )?(bitcoin|cripto)|bitcoin etf|\b(hash|qbtc|bith|coin)11"),
    "2026-11-03": ("investir 1000 reais por mes", r"1000 reais por mes|renda passiva|renda mensal"),
    "2026-11-05": (None, r"copom|selic"),
    "2026-11-07": ("fundos imobiliarios", r"fundos? imobiliari|\bfiis?\b"),
    "2026-11-10": (None, r"tesouro|renda mensal"),
    "2026-11-12": ("fundo imobiliario", r"fundos? imobiliari|\bfiis?\b"),
    "2026-11-14": ("cdb prefixado", r"cdbs? (pre|pos)|prefixad"),
    "2026-11-17": ("etf dividendos mensais", r"etfs?.*dividend"),
    "2026-11-19": ("bitcoin", r"bitcoin|criptomoeda"),
    "2026-11-21": (None, r"\bia\b|inteligencia artificial|bolha"),
    "2026-11-23": ("melhor cdb liquidez diaria", r"liquidez diaria|reserva de emergencia|qual cdb rende"),
    "2026-11-24": (None, r"selic|renda mensal"),
    "2026-11-26": ("fundos imobiliarios", r"fundos? imobiliari|\bfiis?\b"),
    "2026-11-28": ("melhor cdb liquidez diaria", r"liquidez diaria|reserva de emergencia|qual cdb rende"),
}
COLS = ["data", "dia", "formato", "assunto", "titulo", "termo_busca", "views_pesquisa_6m", "views_pesquisa_vitalicio",
        "demanda", "continuacao_de", "angulo", "inscritos_esperados", "faixa_p25_p75", "base_do_esperado",
        "fontes_a_conferir"]


def demanda(T, data_):
    """Termo, views 6m (texto), views vitalício (família, só termos de investimento) e o texto da demanda."""
    if data_ not in TERMOS:
        return "", "", "", "sem termo associado (Short de alcance)"
    termo, fam = TERMOS[data_]
    ts = [t for t in T.casar(fam) if not T.categoria(t).startswith("amplo")]
    vit = T.vitalicio(ts)
    seis = T.texto_6m(ts) if ts else "—"
    if not ts:
        return "", "—", 0, "nenhum termo nos dados (nem no top 25 mensal, nem nos 50 vídeos de busca)"
    donos = Counter(T.dono(t) for t in ts if T.dono(t))
    dono = donos.most_common(1)[0][0] if donos else "—"
    return (termo or "", seis, vit, f"{len(ts)} termos da família, {vit:,} views da Pesquisa no vitalício "
            f"(sobretudo em {dono}); 6 meses: {seis}".replace(",", "."))


def montar(d):
    linhas = []
    cache = {}
    T = termos.Termos()
    for data_, fmt, assunto, titulo, chave, volume, cont, angulo, fontes in PAUTAS:
        k = (fmt, assunto)
        if k not in cache:
            cache[k] = temas.esperado_por_assunto(d, fmt, assunto)
        e, e25, e75, n, janela = cache[k]
        dt = date.fromisoformat(data_)
        linhas.append({"data": data_, "dia": DIAS[dt.weekday()], "formato": fmt, "assunto": assunto, "titulo": titulo,
                       "palavra_chave": chave, "continuacao_de": cont, "angulo": angulo,
                       "inscritos_esperados": round(e, 1), "faixa_p25_p75": f"{e25:.1f}–{e75:.1f}",
                       "_e": e, "_e25": e25, "_e75": e75,
                       "base_do_esperado": f"{assunto}, {fmt}s, {janela} (n = {n})", "fontes_a_conferir": fontes})
        tb, v6, vv, dem = demanda(T, data_)
        linhas[-1].update(termo_busca=tb, views_pesquisa_6m=v6, views_pesquisa_vitalicio=vv, demanda=dem)
    return linhas


def por_semana(linhas, ini=date(2026, 10, 5)):
    sem = defaultdict(lambda: {"longos": 0, "shorts": 0, "e": 0.0, "e25": 0.0, "e75": 0.0})
    for r in linhas:
        k = (date.fromisoformat(r["data"]) - ini).days // 7
        s = sem[k]
        s["longos" if r["formato"] == L else "shorts"] += 1
        s["e"] += r["_e"]
        s["e25"] += r["_e25"]
        s["e75"] += r["_e75"]
    return dict(sorted(sem.items()))


def meta_semanal_novos(p, mes):
    """Inscritos de vídeos novos por semana no plano de META.md (sem defasagem), com a rampa de produção."""
    f = me.RAMPA.get(mes, 1.0)
    return (f * (p["novos"] - p["novos_shorts"]) + p["novos_shorts"]) / 4.33


def br(x, casas=0):
    s = f"{x:,.{casas}f}"
    return s.replace(",", "X").replace(".", ",").replace("X", ".")


def markdown(d, linhas):
    b = mo.base(d)
    p = mo.plano(d, b, me.PLANO_LONGOS, me.PLANO_SHORTS)
    sem = por_semana(linhas)
    ini = date(2026, 10, 5)
    mix = Counter(r["assunto"] for r in linhas if r["formato"] == L)
    esp = {a: temas.esperado_por_assunto(d, L, a)[0] for a in mix}
    mix_md = "\n".join(["  | assunto | longos nas 8 semanas | inscritos esperados por longo |", "  |---|---|---|"]
                       + [f"  | {a} | {n} | {br(esp[a])} |" for a, n in mix.most_common()])
    out = [f"""# Calendário de 8 semanas: v2 (05/10 a 29/11/2026)

Gerado por `calendario_v2.py`. Todas as colunas estão em `CALENDARIO-8-SEMANAS.csv`; a v1 ficou em
`CALENDARIO-8-SEMANAS_v1.md`.

**O que mudou da v1:**
- **Escolha dos assuntos:** pelo ranking de **inscritos esperados por vídeo** (`TEMAS.md`), não por intuição.
- **Volume:** 3 longos por semana a partir de 26/10, para chegar ao plano de 12 por mês de `META.md`.
- **Mix:**

{mix_md}

- **Viraram Short:** "juntar 1 milhão" (como longo, 14 por vídeo; como Short, vive de busca) e "JCP 17,5%" (imposto
  rende 16 por longo).
- **Os 10 top:** 9 continuam cobertos, todos justificados pelo ranking:
  - renda mensal: Fb0l4KEq27o, TY8oLvUt2Qg e IB1mBcF00jc;
  - tesouro: dHYQtxnMSrw, e KMIsVEOcaLM com tb0nwpl9mFw no Copom;
  - crise: IcN3m7whpl8 e tpobf1e1OtM;
  - cripto: JDtxzQthFlk.
  - O cobre (lt2LWbwu3mc) saiu na revisão por termos: commodities tem n = 1 e nenhum termo de busca.

**Revisão por termos de busca reais (`TERMOS.md`):**
- **Títulos:** os longos ganharam o termo real mais próximo, no começo do título quando coube, com até ~60 caracteres.
  As colunas `termo_busca`, `views_pesquisa_6m` e `views_pesquisa_vitalicio` do CSV substituem o "volume provável" da v1.
- **Duas trocas de tema:**
  - **07/11:** "recompra de ações", sem nenhum termo e no assunto que menos rende, virou **"Fundos imobiliários para
    iniciantes"** (fundos imobiliários: 1,4 mil views da Pesquisa no vitalício; FII rende 45 por longo, contra 30 de
    ações).
  - **14/11:** o cobre virou **"CDB prefixado ou pós-fixado"** (cdb prefixado: 3,9 mil views da Pesquisa, o maior termo
    de renda fixa do canal).
- **Pautas sem termo de busca, mantidas:**
  - Tesouro IPCA+ (08/10), Copom (05/11), renda mensal com Tesouro (10/11), bolha de IA (21/11) e Selic caindo (24/11).
  - Tesouro e Copom não aparecem em nenhum termo, mas são o assunto que mais traz inscritos, e vivem da página inicial.
  - Trocar essas pautas derrubaria a soma das semanas abaixo da meta. Para elas, o título é pensado para a
    Navegação (número concreto, sem clickbait), não para a busca.
  - O `--termos-recentes 180` vai mostrar se os vídeos de 2026 sobre Tesouro recebem alguma busca.
- **Copom:** a reunião é em 03 e 04/11. Sai um Short no dia 04/11 (antes da decisão) e o longo em 05/11.

**Regras:**
- 19 h para longos; Shorts às segundas e quartas.
- Não recomendar ativo nem citar corretora.
- Fora: dívida, cartão de crédito e política.

## Soma semanal × meta semanal

Os inscritos esperados de cada pauta são inscritos vitalícios do vídeo (chegam ao longo de 1 a 3 meses). A meta semanal
é o plano de vídeos novos de `META.md`: {br(p['novos'])} por mês em regime, ÷ 4,33, com a rampa de outubro.

| semana | longos | Shorts | inscritos esperados (faixa p25–p75) | meta semanal de vídeos novos | diferença |
|---|---|---|---|---|---|"""]
    tot_e = tot_m = 0.0
    for k, s in sem.items():
        ini_s = ini + timedelta(days=7 * k)
        mt = meta_semanal_novos(p, f"{ini_s:%Y-%m}")
        tot_e += s["e"]
        tot_m += mt
        out.append(f"| {ini_s:%d/%m}–{(ini_s + timedelta(days=6)):%d/%m} | {s['longos']} | {s['shorts']} | "
                   f"**{br(s['e'])}** ({br(s['e25'])}–{br(s['e75'])}) | {br(mt)} | {br(s['e'] - mt)} |")
    out.append(f"| **8 semanas** | {sum(s['longos'] for s in sem.values())} | {sum(s['shorts'] for s in sem.values())} | "
               f"**{br(tot_e)}** ({br(sum(s['e25'] for s in sem.values()))}–{br(sum(s['e75'] for s in sem.values()))}) "
               f"| {br(tot_m)} | {br(tot_e - tot_m)} |")
    falta = tot_m - tot_e
    rm = temas.esperado_por_assunto(d, L, "renda mensal")[0]
    te = temas.esperado_por_assunto(d, L, "tesouro e renda fixa")[0]
    geral = mo.ranking(d, L, "12 meses")[1]["esperado"]
    n_te = sum(1 for r in linhas if r["formato"] == L and r["assunto"] == "tesouro e renda fixa")
    out.append(f"""
**Leitura:**
- **Semanas fortes e fracas:** em geral, as semanas com um longo de Tesouro ficam acima da meta, e as sem Tesouro,
  abaixo.
- **Saldo das 8 semanas:** {'faltam' if falta > 0 else 'sobram'} cerca de **{br(abs(falta))} inscritos** em relação ao
  plano.
- **Cuidado:** a folga depende do Tesouro, que tem só 5 vídeos de base. Se os {n_te} longos de Tesouro renderem como
  a mediana geral dos longos ({br(geral)} cada, e não {br(te)}), as 8 semanas ficam em ~{br(tot_e - n_te * (te - geral))},
  contra a meta de {br(tot_m)}.""")
    pess = tot_m - (tot_e - n_te * (te - geral))
    if pess > 0:
        out.append(f"""- **Mais volume:** nesse cenário pessimista, faltam ~{br(pess)} inscritos. A saída seria acrescentar
  **{br(pess / rm, 1)} longos de renda mensal** nas 8 semanas (cerca de 1 a cada 2 semanas), no lugar de um longo de crise.""")
    if falta > 0:
        out.append(f"""- **Para fechar a diferença**, há duas opções:
  - **+{br(falta / rm, 1)} longos de renda mensal** nas 8 semanas, a {br(rm)} cada;
  - ou **+{br(falta / te, 1)} de Tesouro e renda fixa**, a {br(te)} cada. É o assunto que mais rende, mas só tem 5
    vídeos de base, e a pauta de Tesouro depende de fato novo (taxa, Copom).
  - O 3º longo semanal já é um aumento: 12 por mês é o máximo que o canal publicou num mês. Se não der para
    sustentar, o 3º longo é o primeiro a sair, e a data da meta escorrega (`META.md`).""")
    out.append("""
## Pautas

| data | formato | assunto | título | termo de busca real | Pesquisa 6 meses | Pesquisa vitalício (família) | continuação de | inscritos esperados (p25–p75) |
|---|---|---|---|---|---|---|---|---|""")
    for r in linhas:
        out.append(f"| {r['data'][8:]}/{r['data'][5:7]} {r['dia']} | {r['formato']} | {r['assunto']} | **{r['titulo']}** | "
                   f"{r['termo_busca'] or '— (sem termo)'} | {r['views_pesquisa_6m'] or '—'} | "
                   f"{br(r['views_pesquisa_vitalicio']) if r['views_pesquisa_vitalicio'] != '' else '—'} | "
                   f"{r['continuacao_de'] or '—'} | "
                   f"{br(r['_e'], 1 if r['formato'] == S else 0)} ({br(r['_e25'], 1)}–{br(r['_e75'], 1)}) |")
    out.append("""
## Ângulo e fontes de cada pauta

""")
    for r in linhas:
        out.append(f"- **{r['data'][8:]}/{r['data'][5:7]} · {r['titulo']}** — {r['angulo']} *Conferir:* {r['fontes_a_conferir']}. "
                   f"*Esperado:* {r['base_do_esperado']}. *Busca:* {r['demanda']}.")
    out.append("""
**Busca:**
- **Fonte:** termos reais de `auditoria-canal/dados/termos_busca_*.csv` (TERMOS.md).
- **Vitalício:** soma da família de termos de investimento nos 50 vídeos com mais busca.
- **6 meses:** top 25 mensal do canal; "fora do top 25" quer dizer menos views que o corte do mês.
""")
    return "\n".join(out)


def main():
    d = mo.carregar()
    linhas = montar(d)
    with open(AQUI / "CALENDARIO-8-SEMANAS.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(linhas)
    (AQUI / "CALENDARIO-8-SEMANAS.md").write_text(markdown(d, linhas), encoding="utf-8")
    print(f"ok: {len(linhas)} pautas em CALENDARIO-8-SEMANAS.md e .csv")


if __name__ == "__main__":
    main()
