# -*- coding: utf-8 -*-
# id -> (tipo, dados).  Duracao vem do plano.json (derivada da fala).
# Numeros = roteiro v3.0 (29/09) + notas [TELA] do .md v2 (fnet 27/08, 10/09, 23-28/09; tela de 29/09).
# Onde a fala errou o numero, a cartela escreve o certo (Denis 15/09: "erro de numero corrige na escrita").
# Tipos: num · barras · formula · frase · quote · balao · cupom · lista · fluxo · duas
T = {
# ---------- BLOCO 0 — gancho ----------
"01-pediu-5bi": ("num", dict(rot="TRXF11 · 13ª EMISSÃO · O PEDIDO", val=5, dec=0, pre="R$ ", suf=" bi",
    sub="em cota nova, pros próprios cotistas", cor="ink")),
"02-deram-40mi": ("barras", dict(rot="13ª EMISSÃO · RODADA DOS COTISTAS", linhas=[
    ("pedido", 5000, "R$ 5 bi", "gray"), ("subscrito", 40.2, "R$ 40 mi", "red")], carimbo="0,8%")),
"03-chapeu": ("balao", dict(txt="O fundo passou o chapéu. O chapéu voltou quase vazio.", sub="")),
"04-outro-comprador": ("frase", dict(rot="A COTA NOVA ACHOU OUTRO COMPRADOR", l1="não é o cotista", l2="quem compra agora é quem vende prédio pro fundo", cor="red")),
"05-guarda-093": ("num", dict(rot="GUARDA ESSE NÚMERO · DIVIDENDO POR COTA", val=0.93, dec=2, pre="R$ ", suf="",
    sub="todo mês — é ele que está em jogo", cor="verde", pe="POR MÊS")),
"06-tres-casos": ("lista", dict(rot="OS R$ 0,93 PESAM DIFERENTE PRA QUEM…", itens=["pensa em comprar mais", "pensa em vender", "já é cotista e vai ficar"])),
# ---------- BLOCO 1 — a queda ----------
"07-tombo": ("barras", dict(rot="COTA DO TRXF11 NA BOLSA", linhas=[
    ("fim de julho", 91, "R$ 91", "gray"), ("3 semanas depois", 70, "R$ 70", "red")], carimbo="TOMBO", base=60)),
"08-oferta-anuncio": ("frase", dict(rot="AGOSTO", l1="oferta de R$ 5 bi", l2="o dinheiro pra sair comprando prédio")),
"09-desistiu-3bi": ("num", dict(rot="NO ÚLTIMO VÍDEO · O FUNDO DESISTIU DE", val=3.17, dec=2, pre="R$ ", suf=" bi",
    sub="Pátio Victor Malzoni + portfólio Cyrela", cor="ink")),
"10-novela": ("balao", dict(txt="Parecia último capítulo de novela. Todo mundo se abraçando.", sub="não era")),
"11-comprou-de-novo": ("barras", dict(rot="SETEMBRO · O FUNDO VOLTOU ÀS COMPRAS", linhas=[
    ("desistiu (ago)", 3.17, "R$ 3,17 bi", "gray"), ("assinou (set)", 3.32, "R$ 3,32 bi", "red")],
    nota="compromissos assinados — parte ainda com condição pra fechar")),
"12-cota-hoje": ("barras", dict(rot="COTA DO TRXF11 NA BOLSA", linhas=[
    ("fim de julho", 91, "R$ 91", "gray"), ("após a desistência", 80, "~R$ 80", "gray"), ("hoje, 29/09", 72, "R$ 72", "red")], base=60)),
"13-ninguem-cancelou": ("frase", dict(rot="A OFERTA DE R$ 5 BI", l1="ninguém cancelou", l2="continua aberta", cor="red")),
# ---------- BLOCO 2 — a ficha do caixa ----------
"14-preco-fixo": ("duas", dict(rot="A MESMA COTA, DOIS PREÇOS", a="R$ 94", asub="cota nova (preço da oferta)", b="R$ 72", bsub="cota na bolsa, hoje", rodape="o preço da oferta não se mexe com a bolsa")),
"15-quermesse": ("fluxo", dict(rot="A QUERMESSE DO TRXF11", caixas=[
    ("FICHA", "a cota", ""), ("CAIXA", "a oferta do fundo · R$ 94", "gray"), ("PORTA", "a bolsa · R$ 72", "red")])),
"16-quantas": ("balao", dict(txt="Quantas fichas você compra no caixa?", sub="nenhuma — os cotistas fizeram a mesma conta")),
"17-dist-22": ("formula", dict(rot="A DISTÂNCIA ENTRE O CAIXA E A PORTA", partes=["94", "−", "72"], res="R$ 22 por ficha",
    sub="cota nova × cota na bolsa, 29/09")),
"18-festa-junina": ("balao", dict(txt="Comprou ficha demais… e no fim da noite tava na porta vendendo pela metade.", sub="")),
# ---------- BLOCO 3 — o papel que se chama encerramento ----------
"19-papel-1009": ("frase", dict(rot="10 DE SETEMBRO · SITE DA B3", l1="“Anúncio de Encerramento”", l2="o nome do papel")),
"20-le-texto": ("duas", dict(rot="LÊ O TEXTO, NÃO O TÍTULO", a="encerrou", asub="a vez dos cotistas", b="abriu", bsub="a vez do investidor profissional", rodape="")),
"21-profissional": ("frase", dict(rot="INVESTIDOR PROFISSIONAL", l1="R$ 10 mi+", l2="gestora, fundo, gente com muito dinheiro aplicado")),
"22-ate-fev": ("frase", dict(rot="A VEZ DO PROFISSIONAL VAI ATÉ", l1="fev/2027", l2="ou até a cota nova acabar · 52,6 milhões de cotas à venda")),
"23-so-convidados": ("duas", dict(rot="A QUERMESSE TROCOU A PLACA", a="FECHADO", asub="", b="só convidados", bsub="e o caixa continua funcionando", rodape="")),
# ---------- BLOCO 4 — quem paga com prédio ----------
"24-fluxo-predio": ("fluxo", dict(rot="COMO QUEM VENDE PRÉDIO COMPRA COTA NOVA", caixas=[
    ("FUNDO", "quer o prédio, não tem o dinheiro", ""), ("PAGA EM COTA", "cada cota contada a R$ 94", "gray"),
    ("VENDEDOR", "sai com cota do TRXF11", "red")])),
"25-compensacao": ("frase", dict(rot="NO FATO RELEVANTE, O NOME DE CARTÓRIO", l1="compensação de créditos", l2="uma dívida apaga a outra — nenhum real sai do fundo")),
"26-pastel": ("balao", dict(txt="A festa comprou a barraca de pastel e pagou o dono em ficha.", sub="")),
"27-engenhoso": ("frase", dict(rot="JUSTIÇA SEJA FEITA", l1="engenhoso", l2="o cotista não quis a ficha — o fundo achou quem quisesse", cor="verde")),
"28-1bi-3dias": ("num", dict(rot="EM 3 DIAS · SEMANA PASSADA · EM COTA NOVA", val=1.1, dec=1, pre="R$ ", suf=" bi",
    sub="pegos ou prometidos por quem vendeu prédio", cor="red", pe="MAIOR PARTE AINDA É PROMESSA")),
# ---------- BLOCO 5 — a conta da Berrini ----------
"29-berrini": ("num", dict(rot="ESCRITÓRIOS NA AV. BERRINI · SÃO PAULO", val=250, dec=0, pre="~R$ ", suf=" mi",
    sub="quem vendeu: outro fundo imobiliário, o HAAA11", cor="ink")),
"30-cotas-haaa": ("num", dict(rot="O HAAA11 RECEBEU", val=1010000, dec=0, pre="", suf="",
    sub="cotas novas do TRXF11 — contadas a R$ 94", cor="ink", pe="COTAS")),
"31-conta-22mi": ("formula", dict(rot="A CONTA DA FICHA · BERRINI", partes=["R$ 22", "×", "1.010.000"], res="≈ R$ 22 mi",
    sub="pagou R$ 95,3 mi em cota · na bolsa hoje valem R$ 72,7 mi")),
"32-sacola": ("balao", dict(txt="O HAAA11 saiu da quermesse com uma sacola de ficha do tamanho de um prédio.", sub="")),
"33-tres-respostas": ("lista", dict(rot="QUEM PAGA OS R$ 22 DE CADA COTA?", itens=["1 · o preço do prédio", "2 · o prazo", "3 · o próprio fundo"])),
"34-r1-preco": ("frase", dict(rot="RESPOSTA 1 · O PREÇO", l1="prédio mais caro", l2="pra compensar a ficha contada cara — quem paga é o cotista", cor="red")),
"35-r2-prazo": ("num", dict(rot="RESPOSTA 2 · O PRAZO · O RESTO DO PREÇO DA BERRINI", val=9.2, dec=2, pre="IPCA + ", suf="%",
    sub="ao ano, em parcelas até 2033 — R$ 154 mi na parcela final", cor="red")),
"36-r3-protecao": ("num", dict(rot="RESPOSTA 3 · PROTEÇÃO DE PREÇO AO VENDEDOR · TETO", val=205, dec=0, pre="R$ ", suf=" mi",
    sub="se ele vender a cota abaixo de R$ 94, o fundo paga a diferença · em até 18 meses", cor="red")),
"37-3-por-cota": ("barras", dict(rot="NO PIOR CASO, POR COTA", linhas=[
    ("proteção", 3, "~R$ 3", "red"), ("dividendo/mês", 0.93, "R$ 0,93", "verde")], carimbo="3,5 MESES DE DIVIDENDO")),
"38-contrario": ("frase", dict(rot="E VALE O CONTRÁRIO", l1="lucro volta", l2="se o vendedor vender acima, uma parte volta pro fundo", cor="verde")),
"39-nao-crime": ("frase", dict(rot="NENHUMA DAS TRÊS É CRIME", l1="tá na regra", l2="pagar prédio com cota está na regra da oferta desde o 1º dia")),
# ---------- PUBLI — Grana ----------
"40-imposto": ("duas", dict(rot="VENDEU COM LUCRO NO MÊS", a="ação", asub="isento até R$ 20 mil em vendas", b="FII", bsub="sem teto: 20% do lucro", rodape="")),
"41-darf": ("frase", dict(rot="QUEM EMITE A GUIA", l1="o DARF é seu", l2="um quinto do lucro na venda de cota de FII", cor="red")),
"42-prejuizo": ("frase", dict(rot="VENDEU NO PREJUÍZO EM AGOSTO?", l1="abate depois", l2="prejuízo em FII compensa lucro futuro em FII — se estiver registrado")),
"43-grana": ("lista", dict(rot="GRANA · PARCEIRO E INVESTIDO PELA B3", itens=[
    "puxa suas guias da bolsa desde 2020", "aponta o pendente com juro e multa", "quita no app ou no site, sem gerar guia",
    "faz a conta do imposto todo mês e avisa", "otimiza o IR e deixa a declaração pronta"])),
"44-multa": ("frase", dict(rot="IMPOSTO ESQUECIDO", l1="juro + multa", l2="continua correndo — o dividendo entra e a multa come", cor="red")),
"45-cupom": ("cupom", dict(cod="DESENROLADENIS", off="R$ 90 OFF", sub="histórico desde 2020 + declaração conferida · até 30/09 · link na descrição")),
# ---------- BLOCO 6 — o lado do fundo ----------
"46-predios-bons": ("lista", dict(rot="O ARGUMENTO A FAVOR · OS PRÉDIOS", itens=["galpão da Shopee e da DHL", "a sede da BRF", "shoppings da Iguatemi", "quase nenhum imóvel vazio"])),
"47-div-093": ("num", dict(rot="DIVIDENDO DO TRXF11 · HÁ MAIS DE 1 ANO", val=0.93, dec=2, pre="R$ ", suf="",
    sub="por cota, todo mês (fora os extras)", cor="verde")),
"48-conta-ninguem": ("frase", dict(rot="A CONTA QUE QUASE NINGUÉM FAZ", l1="uma cota nova só", l2="usada pra pagar um pedaço do galpão do Espírito Santo")),
"49-entra-sai": ("barras", dict(rot="POR COTA NOVA, POR MÊS", linhas=[
    ("entra de aluguel", 0.67, "R$ 0,67", "gray"), ("sai de dividendo", 0.93, "R$ 0,93", "red")], carimbo="−R$ 0,26")),
"50-cap-rate": ("formula", dict(rot="CAP RATE · A SALA DE R$ 100 MIL", partes=["10 mil", "÷", "100 mil"], res="= 10% ao ano",
    sub="aluguel de um ano ÷ preço do prédio")),
"51-galpao-es": ("formula", dict(rot="GALPÃO DO ESPÍRITO SANTO · CAP RATE 8,6%", partes=["94", "×", "8,6%", "÷ 12"], res="≈ R$ 0,67/mês",
    sub="≈ R$ 8 de aluguel por ano, por cota nova")),
"52-iguatemi": ("barras", dict(rot="ALUGUEL POR COTA NOVA, POR MÊS", linhas=[
    ("galpão ES (8,57%)", 0.67, "R$ 0,67", "gray"), ("Iguatemi (8,02%)", 0.63, "R$ 0,63", "gray"), ("dividendo", 0.93, "R$ 0,93", "red")],
    nota="conta do canal: R$ 94 × cap rate ÷ 12 · cap rates dos fatos relevantes")),
"53-12pct": ("num", dict(rot="A RESPOSTA DO FUNDO · IGUATEMI", val=12, dec=0, pre="+", suf="% a.a.",
    sub="retorno sobre o dinheiro que sai agora — o resto do preço fica parcelado", cor="ink")),
"54-cdi": ("frase", dict(rot="PARCELA PAGA DEPOIS", l1="não sai de graça", l2="as da Iguatemi vêm corrigidas pelo CDI", cor="red")),
"55-puxa-baixo": ("frase", dict(rot="CADA COTA NOVA", l1="puxa pra baixo", l2="o dividendo de todo mundo — não amanhã, mas é essa conta que decide", cor="red")),
"56-brc": ("num", dict(rot="SEGUNDA (28/09) · VENDEU 15 IMÓVEIS AO BRC RENDA URBANA", val=207, dec=0, pre="R$ ", suf=" mi",
    sub="recebeu tudo em cota do BRC", cor="ink", pe="FICHA DO VIZINHO")),
# ---------- BLOCO 7 — a conta da ficha ----------
"57-conta-ficha": ("lista", dict(rot="A CONTA DA FICHA · 3 PASSOS", itens=[
    "1 · procura “compensação de créditos”", "2 · cotas × preço da BOLSA (a porta)", "3 · compara com o que foi pago em cota"])),
"58-quem-pagou": ("lista", dict(rot="PERGUNTA: QUEM PAGOU A DIFERENÇA?", itens=["foi o preço do prédio?", "foi o prazo?", "foi a proteção ao vendedor?"])),
"59-berrini-deu": ("duas", dict(rot="NA BERRINI, A CONTA DA FICHA DEU", a="R$ 22", asub="por cota", b="R$ 22 mi", bsub="no pacote", rodape="")),
# ---------- BLOCO 8 — comprar, vender ou ficar ----------
"60-093-volta": ("num", dict(rot="O NÚMERO LÁ DO COMEÇO", val=0.93, dec=2, pre="R$ ", suf="",
    sub="por mês — é por ele que cada um decide", cor="verde", pe="POR COTA")),
"61-vp": ("barras", dict(rot="COMPRAR MAIS · VALOR PATRIMONIAL", linhas=[
    ("cota na bolsa", 72, "R$ 72", "gray"), ("prédio dentro da cota", 96, "~R$ 96", "verde")],
    nota="pela avaliação do próprio fundo", base=50)),
"62-15pct": ("formula", dict(rot="O CUIDADO · DIVIDEND YIELD", partes=["0,93 × 12", "÷", "72"], res="≈ 15% ao ano",
    sub="se só se segura com venda de imóvel: é fotografia, não filme")),
"63-aluguel-venda": ("duas", dict(rot="DE ONDE VÊM OS R$ 0,93", a="aluguel", asub="repete todo mês", b="venda de imóvel", bsub="não se repete", rodape="")),
"64-trava-45": ("num", dict(rot="VENDER · A COTA DOS VENDEDORES DE PRÉDIO FICA TRAVADA", val=45, dec=0, pre="~", suf=" dias",
    sub="depois disso, mais gente vendendo na porta", cor="red")),
"65-um-quarto": ("formula", dict(rot="O CONTRA-ARGUMENTO", partes=["72", "÷", "96"], res="¼ de desconto",
    sub="vender agora é vender prédio abaixo da conta do próprio fundo")),
"66-ficar": ("lista", dict(rot="SE VOCÊ VAI FICAR", itens=["conta da ficha em todo fato relevante", "separa aluguel de venda de imóvel", "fevereiro: quanto a oferta vendeu"])),
"67-quem-fecha": ("frase", dict(rot="DIVIDENDO BOM E PRÉDIO BOM NÃO FECHAM A CONTA", l1="quem fecha é você", l2="quanto a ficha valia na porta")),
# ---------- cauda (ad-lib) ----------
"68-montanha-russa": ("fluxo", dict(rot="O TRXF11 EM 2026", caixas=[
    ("QUERIDINHO", "", ""), ("OFERTA DERRETEU", "", "red"), ("DESISTIU", "", "gray"), ("COMPROU DE NOVO", "", "red")])),
"69-susto": ("frase", dict(rot="QUEM GOSTA DE FII", l1="não quer susto", l2="normalmente é quem gosta de renda fixa")),
"70-comenta": ("balao", dict(txt="Você é cotista do TRXF11? Vendeu, segurou, vai ficar?", sub="conta aqui nos comentários")),
}
