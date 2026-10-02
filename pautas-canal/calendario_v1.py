#!/usr/bin/env python3
"""Gera CALENDARIO-8-SEMANAS_v1.csv e a tabela do CALENDARIO-8-SEMANAS_v1.md a partir das pautas abaixo (fonte única).

Volume provável (sem inventar número): a regra usa só os dados do próprio canal, em
auditoria-canal/dados/trafego_por_video.csv (origem YT_SEARCH, vitalício, 300 vídeos com mais views):
  ALTO  = um vídeo do canal com a mesma palavra-chave trouxe ≥ 20 mil views da Pesquisa do YouTube,
          ou ≥ 40% das views dele vieram da Pesquisa;
  MÉDIO = ≥ 3 mil views da Pesquisa ou 10% a 40% das views vindas da Pesquisa;
  BAIXO = abaixo disso (o vídeo vive de Navegação/Início, não de busca).
A API não deu os termos buscados; a palavra-chave é a do título do vídeo de referência. Nenhuma fonte externa
de volume de busca foi usada.

uso: python3 calendario.py   (reescreve o CSV e imprime a tabela em Markdown)
"""
import csv
from pathlib import Path

AQUI = Path(__file__).resolve().parent
YT = "https://youtu.be/"

COLS = ["data", "dia", "formato", "serie", "continuacao_de", "tema", "titulo", "palavra_chave", "volume",
        "base_do_volume", "angulo", "por_que", "fontes_a_conferir"]

PAUTAS = [
    # ---------------------------------------------------------------- semana 1
    dict(data="2026-10-06", dia="terça", formato="longo (15-20 min)", serie="Renda mensal #1 (ação 3)",
         continuacao_de="Fb0l4KEq27o (6 ETFs que mais pagaram dividendos mensais em 2025; 637 inscritos)",
         tema="ETFs que pagam todo mês",
         titulo="ETFs que pagam dividendos mensais na B3: o que mudou em 2026",
         palavra_chave="ETF dividendos mensais", volume="ALTO",
         base_do_volume="Y4WHQiKcv1g (ETFs que pagam mensalmente na B3): 26.783 views da Pesquisa (44%); "
                        "QjiF99_cINk: 11.812 (14%); OSNXkhCSDb0: 9.859 (23%)",
         angulo="Não repetir a lista de 2025: mostrar o que aconteceu com cada ETF daquela lista em 2026 (frequência "
                "real de pagamento, rendimento dos últimos 12 meses, taxa de administração, patrimônio) e responder "
                "as 3 dúvidas que mais aparecem nos comentários: taxa, imposto na venda e se precisa declarar.",
         por_que="Renda mensal converte 14,5 inscritos por mil views intencionais contra 8,2 do resto (n = 6); "
                 "o original foi o vídeo do ano com mais inscritos (637).",
         fontes_a_conferir="B3 (lista de ETFs listados e histórico de proventos); regulamento e lâmina de cada "
                           "ETF (taxa de administração e política de distribuição); regra de IR de ETF na venda."),
    dict(data="2026-10-08", dia="quinta", formato="longo", serie="Continuação do top (ação 5)",
         continuacao_de="dHYQtxnMSrw (NTN-B IPCA+7%, jan/26; 421 inscritos)",
         tema="Tesouro IPCA+ e marcação a mercado",
         titulo="Tesouro IPCA+ a 7% em janeiro: quanto ganhou ou perdeu quem comprou",
         palavra_chave="Tesouro IPCA+ marcação a mercado", volume="BAIXO",
         base_do_volume="dHYQtxnMSrw: 2.072 views da Pesquisa (7%); KMIsVEOcaLM: 1.791 (9%). Vive de Navegação.",
         angulo="Prestação de contas do vídeo de janeiro: preço do título na compra e hoje, cupons, o que a "
                "marcação fez com quem vendeu antes e com quem segura até o vencimento.",
         por_que="Tesouro/IPCA+ tem mediana de 142 inscritos por vídeo (n = 5) e 11,0 por mil views "
                 "intencionais; o original fez 421.",
         fontes_a_conferir="Tesouro Direto (preços e taxas históricos do título usado no vídeo); "
                           "simulador do Tesouro; IPCA acumulado (IBGE)."),
    # ---------------------------------------------------------------- semana 2
    dict(data="2026-10-13", dia="terça", formato="longo", serie="Renda mensal #2 (ação 3)",
         continuacao_de="TY8oLvUt2Qg (Receba dividendos todos os meses de ações; 324 inscritos, 49% das views pela busca)",
         tema="Calendário de dividendos com ações",
         titulo="Ações que pagam dividendos todo mês? Como montar um calendário de proventos",
         palavra_chave="ações que pagam dividendos todo mês", volume="ALTO",
         base_do_volume="TY8oLvUt2Qg: 49% das views vieram da Pesquisa (9.095 views)",
         angulo="Mostrar que 'todo mês' é calendário, não promessa: em que meses cada setor costuma pagar, "
                "data com e data de pagamento, e por que o valor varia. Sem lista de compra: o espectador monta "
                "o calendário com os dados públicos.",
         por_que="Original converteu 18,0 inscritos por mil views intencionais (o 2º melhor entre os 10 top do ano) e é o "
                 "vídeo recente mais buscado do canal.",
         fontes_a_conferir="B3 (eventos corporativos: data com e pagamento dos últimos 12 meses); "
                           "regra do JCP em 2026 (17,5%, LC 224/2025)."),
    dict(data="2026-10-15", dia="quinta", formato="longo", serie="Continuação do top (ação 5)",
         continuacao_de="IcN3m7whpl8 (O gráfico que acertou as crises de 1929, 2008 e 2020; 357 inscritos)",
         tema="Indicador de crise, revisado",
         titulo="O gráfico que 'acertou' 1929, 2008 e 2020: 9 meses depois, o que ele mostrou",
         palavra_chave="sinal de crise 2026", volume="BAIXO",
         base_do_volume="IcN3m7whpl8: 1.161 views da Pesquisa (4%); tpobf1e1OtM: 624 (2%). Vídeos de crise vivem "
                        "de Navegação.",
         angulo="Revisão honesta: o que o indicador marcava em janeiro, o que marca hoje, o que aconteceu com a "
                "bolsa e os juros no período e quantas vezes ele deu alarme falso na história.",
         por_que="Original: 357 inscritos e 12,4 por mil views intencionais; continuação aproveita a demanda "
                 "provada (top 10 = 58% dos inscritos dos longos do ano).",
         fontes_a_conferir="A série do indicador usado no vídeo original (conferir qual é e a fonte); "
                           "Ibovespa e S&P 500 no período."),
    # ---------------------------------------------------------------- semana 3
    dict(data="2026-10-20", dia="terça", formato="longo", serie="Renda mensal #3 (ação 3)",
         continuacao_de="IB1mBcF00jc (ETF JEPI39 paga dividendos mensais; 131 inscritos)",
         tema="ETF de opções cobertas",
         titulo="ETF que paga todo mês com opções: de onde vem o dinheiro e do que você abre mão",
         palavra_chave="ETF opções cobertas dividendos mensais", volume="BAIXO",
         base_do_volume="IB1mBcF00jc: 1.126 views da Pesquisa (5,5%)",
         angulo="Explicar a mecânica (venda de opções cobertas), por que a renda é alta e o ganho de alta fica "
                "limitado, e comparar com um ETF de dividendos comum. Sem indicar compra.",
         por_que="Linha de renda mensal (14,5 por mil views intencionais); pergunta repetida nos comentários: "
                 "'essa taxa é alta?' e 'posso perder mais do que investi?'.",
         fontes_a_conferir="Regulamento/prospecto do ETF e do BDR; histórico de distribuições; regra de IR de BDR "
                           "de ETF."),
    dict(data="2026-10-22", dia="quinta", formato="longo", serie="Busca (ação 8)", continuacao_de="",
         tema="CDB × LCI",
         titulo="CDB ou LCI em 2026: a conta que decide (com imposto e prazo)",
         palavra_chave="CDB ou LCI", volume="ALTO",
         base_do_volume="Q1WMbZZn2Ik (Short 'O que rende mais CDB ou LCI/LCA?'): 57.527 views da Pesquisa (77%)",
         angulo="A conta da taxa equivalente (LCI isenta × CDB com IR regressivo), a carência mínima, a liquidez e "
                "o FGC; responder a pergunta '80 mil em LCI por 12 meses?' sem recomendar produto.",
         por_que="45 perguntas sem resposta sobre rendimento; a busca é a origem com maior CTR nos longos "
                 "(12,3% contra 7,2% da Navegação).",
         fontes_a_conferir="Lei 11.033/2004 (tabela regressiva e isenção de LCI/LCA); resolução do CMN sobre "
                           "prazos mínimos de LCI/LCA (conferir a vigente); regras do FGC (fgc.org.br)."),
    # ---------------------------------------------------------------- semana 4
    dict(data="2026-10-27", dia="terça", formato="longo", serie="Renda mensal #4 (ação 3)", continuacao_de="",
         tema="FII e imposto",
         titulo="FII isento de imposto? A regra dos 100 cotistas e o que muda para você",
         palavra_chave="FII isento de imposto", volume="MÉDIO",
         base_do_volume="Vídeos de FII do canal: 35.246 views da Pesquisa somadas (14% das views deles)",
         angulo="Quando o rendimento mensal do FII é isento para pessoa física (Lei 14.754/2023: 100 cotistas, "
                "cotas em bolsa, menos de 10%), por que o ganho na venda paga 20% e como conferir isso no "
                "relatório do fundo.",
         por_que="Plano de renda converteu 11,7 inscritos por mil views nos últimos 12 meses; pergunta sem "
                 "resposta sobre ganho de capital em FII.",
         fontes_a_conferir="Lei 14.754/2023 e Lei 8.668/1993 (art. 3º); Receita Federal (Perguntas e Respostas "
                           "IRPF 2026)."),
    dict(data="2026-10-29", dia="quinta", formato="longo", serie="Continuação do top (ação 5)",
         continuacao_de="tpobf1e1OtM (A crise já está acontecendo; 345 inscritos)",
         tema="Sinais de crise, revisados",
         titulo="Os sinais de crise de novembro de 2025: o que aconteceu com cada um",
         palavra_chave="crise 2026", volume="BAIXO",
         base_do_volume="tpobf1e1OtM: 624 views da Pesquisa (2%)",
         angulo="Pegar cada sinal citado no vídeo original e mostrar o dado de hoje, sem repetir o alarme: o que "
                "confirmou, o que não confirmou e o que fazer com a reserva enquanto isso.",
         por_que="Original: 345 inscritos (4º do ano), 10,4 por mil views intencionais.",
         fontes_a_conferir="Os dados de cada sinal do vídeo original (BCB/SGS, IBGE, Fed/FRED)."),
    # ---------------------------------------------------------------- semana 5 (Copom 03-04/11)
    dict(data="2026-11-03", dia="terça", formato="longo", serie="Renda mensal #5 (ação 3)", continuacao_de="",
         tema="Quanto investir para ter renda mensal",
         titulo="Quanto investir para receber R$ 1.000 por mês: Tesouro, FII e ETF lado a lado",
         palavra_chave="quanto investir para ter renda de 1000 por mês", volume="MÉDIO",
         base_do_volume="Sem vídeo com a mesma palavra; os mais próximos ('juntar 1 milhão') têm 70% a 81% das "
                        "views pela busca, mas 'renda passiva' tem só 505 (2,9%). Fica no meio.",
         angulo="A conta do capital necessário em três classes, com rendimento líquido de imposto e o que acontece "
                "com a renda se a inflação ou a Selic mudarem. Sem indicar ativos.",
         por_que="Plano de renda é o tema com mais inscritos por mil views nos últimos 12 meses (11,7).",
         fontes_a_conferir="Taxas do Tesouro Direto do dia; IFIX e dividend yield médio (B3); regras de IR "
                           "(JCP 17,5%; FII; ETF)."),
    dict(data="2026-11-05", dia="quinta", formato="longo", serie="Copom (ação 4)",
         continuacao_de="KMIsVEOcaLM (Tesouro IPCA+ antes do Copom; 246) e tb0nwpl9mFw (Não invista no Tesouro "
                        "sem saber disso; 142)",
         tema="Decisão do Copom de 03-04/11",
         titulo="Copom de novembro: o que a decisão muda no Tesouro IPCA+ e no prefixado",
         palavra_chave="Copom novembro 2026", volume="MÉDIO",
         base_do_volume="Vídeos de Copom/Selic do canal: 11.321 views da Pesquisa (9%); Kwf4IvhOb9s (quanto "
                        "rende com a Selic): 2.748 (16%)",
         angulo="Sai no dia seguinte à decisão (quarta, 04/11): o que o comunicado disse, como as taxas do "
                "Tesouro reagiram em 24 h e o que isso faz com quem tem IPCA+, prefixado e Selic.",
         por_que="Tesouro/IPCA+: mediana de 142 inscritos por vídeo (n = 5), 11,0 por mil views intencionais.",
         fontes_a_conferir="Comunicado do Copom de 04/11 (bcb.gov.br); taxas do Tesouro Direto de 04 e 05/11; "
                           "Boletim Focus. Data da reunião: conferir em bcb.gov.br/controleinflacao/calendarioreunioescopom."),
    # ---------------------------------------------------------------- semana 6
    dict(data="2026-11-10", dia="terça", formato="longo", serie="Renda mensal #6 (ação 3)", continuacao_de="",
         tema="JCP e imposto em 2026",
         titulo="JCP com 17,5% de imposto: quanto sobra do provento em 2026",
         palavra_chave="JCP imposto 2026", volume="BAIXO",
         base_do_volume="3sfCQWv2kIQ (dividendos e JCP vão acabar?): 962 views da Pesquisa (4%); qnWje5V23Ps "
                        "(dividendos tributados): 521 (5%)",
         angulo="O que é JCP, por que a empresa paga, a alíquota de 17,5% (LC 224/2025) e a diferença para o "
                "dividendo; quando o dividendo passa a ter retenção (acima de R$ 50 mil por mês da mesma empresa, "
                "Lei 15.270/2025).",
         por_que="Renda mensal; 37 perguntas sem resposta sobre imposto e declaração nos comentários, com "
                 "pedidos explícitos de vídeo.",
         fontes_a_conferir="LC 224/2025; Lei 15.270/2025; Receita Federal."),
    dict(data="2026-11-12", dia="quinta", formato="longo", serie="Continuação do top (ação 5)",
         continuacao_de="lt2LWbwu3mc (O cobre é o novo petróleo?; 255 inscritos)",
         tema="Cobre, um ano depois",
         titulo="Cobre, um ano depois: o que aconteceu com o preço e por que importa para a bolsa",
         palavra_chave="cobre", volume="MÉDIO",
         base_do_volume="lt2LWbwu3mc: 2.346 views da Pesquisa (15%)",
         angulo="Revisar a tese de outubro de 2025 com o preço e a demanda de hoje (energia, data centers), e "
                "explicar como o investidor brasileiro fica exposto ao tema, sem indicar ativo.",
         por_que="Original: 16,7 inscritos por mil views intencionais (3º melhor do ano).",
         fontes_a_conferir="Preço do cobre (LME/CME); relatórios da IEA ou do USGS sobre demanda."),
    # ---------------------------------------------------------------- semana 7
    dict(data="2026-11-17", dia="terça", formato="longo", serie="Renda mensal #7 (ação 3)", continuacao_de="",
         tema="Custo do ETF de renda",
         titulo="ETF de dividendos mensais: quanto a taxa de administração tira da sua renda",
         palavra_chave="taxa de administração ETF", volume="BAIXO",
         base_do_volume="Sem vídeo do canal com essa palavra; a dúvida aparece nos comentários de Y4WHQiKcv1g "
                        "('essa taxa de 1,50 é alta?')",
         angulo="A conta de 10 anos com taxas diferentes, onde a taxa aparece (no preço, não na corretagem) e o "
                "que mais pesa na venda (IR sobre o ganho).",
         por_que="Pergunta sem resposta em vídeos de ETF; renda mensal converte 14,5 por mil views intencionais.",
         fontes_a_conferir="Lâminas e regulamentos dos ETFs; B3 (emolumentos)."),
    dict(data="2026-11-19", dia="quinta", formato="longo", serie="Continuação do top (ação 5)",
         continuacao_de="JDtxzQthFlk (Morte do bitcoin?; 224 inscritos)",
         tema="Bitcoin, revisado",
         titulo="Bitcoin depois do 'alerta': o que mudou desde fevereiro (e o que não mudou)",
         palavra_chave="bitcoin caiu", volume="MÉDIO",
         base_do_volume="Vídeos de bitcoin do canal: 268.961 views da Pesquisa (55%), quase todas de vídeos "
                        "antigos; JDtxzQthFlk: 753 (2%)",
         angulo="Revisar os argumentos do vídeo de fevereiro com os dados de hoje e responder as perguntas dos "
                "comentários: 'posso perder mais do que investi?', 'preciso declarar?'.",
         por_que="Original: 224 inscritos, 32 mil views intencionais (alcance alto, conversão 6,9 por mil).",
         fontes_a_conferir="Preço e volatilidade do BTC; regra de declaração de criptoativos da Receita "
                           "(conferir valor mínimo vigente)."),
    # ---------------------------------------------------------------- semana 8
    dict(data="2026-11-24", dia="terça", formato="longo", serie="Renda mensal #8 (ação 3)", continuacao_de="",
         tema="Declarar a renda mensal",
         titulo="Recebi dividendos e rendimentos todo mês: como declarar no IR 2027",
         palavra_chave="como declarar dividendos imposto de renda", volume="MÉDIO",
         base_do_volume="Vídeos de imposto de renda do canal: 10.317 views da Pesquisa (31% das views deles)",
         angulo="Onde entra cada provento (isentos, tributação exclusiva, JCP), o informe de rendimentos e os "
                "erros comuns; prepara o público para a temporada de IR.",
         por_que="Pedidos explícitos nos comentários ('faz um vídeo explicando como declarar do zero', 24 likes).",
         fontes_a_conferir="Receita Federal: Perguntas e Respostas IRPF (versão vigente); LC 224/2025; "
                           "Lei 15.270/2025; Lei 14.754/2023."),
    dict(data="2026-11-26", dia="quinta", formato="longo", serie="Busca (ação 8)", continuacao_de="",
         tema="Juros compostos com a conta certa",
         titulo="Quanto tempo para juntar 1 milhão guardando R$ 1.000 por mês (a conta honesta)",
         palavra_chave="juntar 1 milhão", volume="ALTO",
         base_do_volume="tbKsF2qyakU: 46.026 views da Pesquisa (70%); wYb9_xSNFV8: 34.237 (81%)",
         angulo="A conta com juro real (6% ao ano: ~R$ 535 mil em 22 anos; 1 milhão em ~30 anos) e nominal "
                "(10% ao ano: ~23 anos), o efeito da inflação e do imposto. Responde quem disse nos comentários "
                "que 'demora 80 anos' e os 194 comentários de dúvida sobre o Short do 1 centavo.",
         por_que="Palavra-chave mais buscada do canal fora de bancos; 101 perguntas sem resposta sobre começar e "
                 "juros compostos.",
         fontes_a_conferir="Selic e IPCA atuais (BCB, IBGE); tabela regressiva de IR (Lei 11.033/2004)."),
]


CABECALHO = """# Calendário de 8 semanas: v1 (substituída pela v2 em CALENDARIO-8-SEMANAS.md)

Gerado por `calendario_v1.py` (a fonte das pautas). A mesma tabela, com todas as colunas, está em
`CALENDARIO-8-SEMANAS_v1.csv`. Os números vêm de `auditoria-canal/RELATORIO.md`.

**Ritmo:** 2 longos por semana, sempre às 19 h, que é o horário de quase todo o canal. Dia e hora não
separaram top de fracos.
- **Terça:** série de renda mensal (ação 3).
- **Quinta:** continuação de um dos 10 top (ação 5) ou pauta de busca (ação 8).
- **Copom (ação 4):** a reunião é em 03 e 04/11, e o vídeo sai na quinta, 05/11, dia seguinte à decisão.

**Calendário do Copom em 2026:** 27-28/01, 17-18/03, 28-29/04, 16-17/06, 04-05/08, 15-16/09,
**03-04/11** e 08-09/12.
- **Na janela:** só a de novembro. A seguinte, de 08-09/12, já fica fora; o vídeo dela seria em 10/12.
- **Fonte:** comunicado do BC de 24/06/2025, repercutido pelo Estadão Conteúdo
  (https://www.dgabc.com.br/Noticia/4241688/bc-divulga-calendario-de-reunioes-do-copom-em-2026) e por
  https://boletimnacional.com.br/2026/02/19/calendario-copom-2026-datas-das-reunioes-e-divulgacao-das-atas/.
- **Conferir:** a página do BCB (www.bcb.gov.br/controleinflacao/calendarioreunioescopom) não abriu daqui,
  porque é carregada por JavaScript.
- **Coerência com o canal:** o vídeo KMIsVEOcaLM ("veja antes do Copom") saiu em 16/06/2026, o primeiro dia
  da reunião de junho.

**Os 10 top viram continuação assim:**
- Fb0l4KEq27o, TY8oLvUt2Qg e IB1mBcF00jc entram na própria série de renda mensal.
- KMIsVEOcaLM e tb0nwpl9mFw viram o vídeo do Copom.
- dHYQtxnMSrw, IcN3m7whpl8, tpobf1e1OtM, lt2LWbwu3mc e JDtxzQthFlk ganham uma quinta cada.

**Feriados no período:** 12/10, 02/11, 15/11 e 20/11. Nenhum cai em dia de vídeo longo.

**Volume provável** (ação 8). Não é número de busca inventado: a regra usa só o tráfego do próprio canal
(origem YT_SEARCH, vitalício, nos 300 vídeos com mais views). A API não devolveu os termos buscados.

| volume | regra (vídeo do canal com a mesma palavra-chave) |
|---|---|
| ALTO | ≥ 20 mil views da Pesquisa ou ≥ 40% das views pela Pesquisa |
| MÉDIO | ≥ 3 mil views da Pesquisa ou de 10% a 40% das views pela Pesquisa |
| BAIXO | abaixo disso (o vídeo vive da página inicial) |

Para ter os termos reais: no Studio, abra Origem do tráfego > Pesquisa do YouTube nos vídeos de referência
(ou use a dimensão `insightTrafficSourceDetail` com `insightTrafficSourceType==YT_SEARCH` no exportador).

**Regras de pauta:**
- tom simples e direto, sem clichê;
- não recomendar ativo nem citar corretora;
- fora: dívida, cartão de crédito e política;
- conferir as fontes da última coluna antes de gravar.

## Resumo

| data | série | título | palavra-chave | volume | por que (número do relatório) |
|---|---|---|---|---|---|
"""


def markdown():
    linhas = [CABECALHO.rstrip("\n")]
    for p in PAUTAS:
        linhas.append(f"| {p['data'][8:]}/{p['data'][5:7]} {p['dia'][:3]} | {p['serie']} | **{p['titulo']}** | "
                      f"{p['palavra_chave']} | {p['volume']} | {p['por_que']} |")
    linhas += ["", "## Pautas em detalhe", ""]
    for p in PAUTAS:
        linhas += [f"### {p['data'][8:]}/{p['data'][5:7]} ({p['dia']}) · {p['serie']} · {p['formato']}", "",
                   f"- **Título:** {p['titulo']}",
                   f"- **Palavra-chave:** {p['palavra_chave']} · **volume provável:** {p['volume']} ({p['base_do_volume']})"]
        if p["continuacao_de"]:
            linhas.append(f"- **Continuação de:** {p['continuacao_de']}")
        linhas += [f"- **Ângulo:** {p['angulo']}", f"- **Por que esta pauta:** {p['por_que']}",
                   f"- **Conferir antes de gravar:** {p['fontes_a_conferir']}", ""]
    return "\n".join(linhas)


def main():
    with open(AQUI / "CALENDARIO-8-SEMANAS_v1.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS)
        w.writeheader()
        w.writerows(PAUTAS)
    (AQUI / "CALENDARIO-8-SEMANAS_v1.md").write_text(markdown(), encoding="utf-8")
    print(f"ok: {len(PAUTAS)} pautas em CALENDARIO-8-SEMANAS_v1.csv e .md")


if __name__ == "__main__":
    main()
