# -*- coding: utf-8 -*-
# id -> (tipo, dados).  Duracao vem do plano.json (derivada da fala).
# Numeros = roteiro v1.1 atualizado 27/09 (placar 12 meses ate 25/09, retorno total em reais).
# Tipos: num · barras · formula · frase · quote · balao · cupom · lista · fluxo · duas
T = {
# ---------- BLOCO 0 ----------
"01-ero": ("num", dict(rot="R$ 10 MIL · 12 MESES ATÉ 25/09 · COM DIVIDENDOS", val=19.9, dec=1, pre="R$ ", suf=" mil",
    sub="Ero Copper — a mineradora do Burry", cor="verde", de="R$ 10 mil", foto="burry")),
"02-pmam": ("num", dict(rot="OS MESMOS R$ 10 MIL · 12 MESES ATÉ 25/09", val=2.9, dec=1, pre="R$ ", suf=" mil",
    sub="Paranapanema (PMAM3) — a empresa em que o Barsi é acionista", cor="red", de="R$ 10 mil", desce=True, foto="barsi")),
"03-diferenca": ("barras", dict(rot="R$ 10 MIL INVESTIDOS · 12 MESES", linhas=[
    ("Ero (Burry)", 19.9, "R$ 19,9 mil", "verde"), ("Paranapanema (Barsi)", 2.9, "R$ 2,9 mil", "red")],
    carimbo="R$ 17 MIL DE DIFERENÇA")),
"04-cobre-44": ("num", dict(rot="COBRE · FUTURO COMEX · 12 MESES ATÉ 25/09", val=44, dec=0, pre="+", suf="%",
    sub="em dólar — o mesmo metal pros dois", cor="cobre")),
"05-duas-pontas": ("duas", dict(rot="QUEM COMPRA COBRE PELA B3", a="ponta 1", asub="dobrou", b="ponta 2", bsub="derreteu",
    rodape="você está numa das duas — e pode não saber qual")),
# ---------- BLOCO 1 ----------
"06-grande-aposta": ("frase", dict(rot="MICHAEL BURRY", l1="A Grande Aposta", l2="acertou a crise de 2008 — agora comprou cobre", foto="burry")),
"07-woohoos": ("quote", dict(txt="“I am largely ignoring the ‘woo-hoos’”", trad="“estou basicamente ignorando a euforia” — com a IA",
    fonte="Michael Burry · 21/09/2026")),
"08-bonito": ("quote", dict(txt="“I think of copper, and how it gets prettier as it ages”",
    trad="“penso no cobre, que fica mais bonito conforme envelhece”", fonte="Cassandra Unchained · 21/09/2026")),
"09-estrada": ("fluxo", dict(rot="A MESMA ESTRADA DE CAMINHÃO · BAHIA", caixas=[
    ("MINA", "Ero · Caraíba, Jaguarari-BA", ""), ("CONCENTRADO", "pedra moída com cobre dentro", "gray"),
    ("FORNO", "Paranapanema · Dias d'Ávila-BA", "red")])),
"10-fiado": ("frase", dict(rot="TRADUÇÃO", l1="FIADO", l2="a mina do Burry ficou com uma conta a receber do forno do Barsi", cor="red")),
"11-rj": ("frase", dict(rot="RECUPERAÇÃO JUDICIAL", l1="prazo do juiz", l2="pra renegociar a dívida sem quebrar de vez")),
"12-550-zero": ("barras", dict(rot="PARANAPANEMA · COBRE REFINADO NA BAHIA", linhas=[
    ("abr–jun 2025", 550, "550 t", "gray"), ("abr–jun 2026", 0.001, "0 t", "red")], carimbo="FORNO DESLIGADO")),
# ---------- BLOCO 2 ----------
"13-barsi-fatia": ("barras", dict(rot="LUIZ BARSI NA PARANAPANEMA", linhas=[
    ("abr/2025", 5, "5%", "gray"), ("set/2026", 1.26, "1,26%", "red")], carimbo="SEM REGISTRO DE VENDA", pct=True, foto="barsi")),
"14-diluicao": ("num", dict(rot="MAIO/2026 · DÍVIDA VIROU AÇÃO", val=139.6, dec=1, pre="", suf=" mi",
    sub="ações novas entregues a credores, a R$ 0,61 cada", cor="ink", pe="O NOME DISSO: DILUIÇÃO")),
"15-escoria": ("barras", dict(rot="PAGAR DÍVIDA COM O RESTO DO FORNO", linhas=[
    ("dívida quitada", 849.7, "R$ 849,7 mi", "ink"), ("valor da escória", 36, "R$ 36 mi", "cobre")],
    nota="4,5 milhões de toneladas de escória (silicato de ferro)")),
"16-carro": ("balao", dict(txt="Tem gente que paga dívida entregando o carro.", sub="a Paranapanema entregou o resto do forno")),
# ---------- BLOCO 3 ----------
"17-boi-acougue": ("duas", dict(rot="A MINA E O FORNO", a="dono do boi", asub="Ero — tira da terra", b="dono do açougue",
    bsub="Paranapanema — compra e passa adiante", rodape="", fa="burry", fb="barsi")),
"18-cobre-683": ("num", dict(rot="COBRE · COMEX · 22/09/2026", val=6.83, dec=2, pre="US$ ", suf="",
    sub="por libra (1 libra ≈ 454 g) — maior fechamento em 12 meses", cor="cobre")),
"19-sobra": ("formula", dict(rot="A SOBRA POR LIBRA · ERO", partes=["6,83", "−", "2,25"], res="≈ US$ 4,58",
    sub="preço − custo previsto pra 2026 (US$ 2,15 a 2,35)")),
"20-picanha": ("balao", dict(txt="A picanha dobrou. O açougueiro cobra o dobro pra cortar o bife?", sub="")),
"21-premio": ("barras", dict(rot="PARANAPANEMA · 2º TRI/2026 · DE CADA R$ 10 FATURADOS", linhas=[
    ("prêmio (o corte)", 42.8, "R$ 4,28", "red"), ("o resto", 57.2, "R$ 5,72", "gray")],
    nota="prêmio = o que ela cobra ACIMA do preço do metal — não sobe com o cobre")),
"22-balcao": ("frase", dict(rot="NÃO FOI O COBRE", l1="o lado do balcão", l2="que separou o Burry do Barsi", cor="red")),
# ---------- BLOCO 4 ----------
"23-vale-cobre": ("frase", dict(rot="A MANCHETE DO COBRE SUBINDO", l1="…e a Vale?", l2="todo mundo olhou pra ela primeiro")),
"24-vale-4x": ("barras", dict(rot="VALE · LUCRO DA OPERAÇÃO (EBITDA) 2025", linhas=[
    ("minério de ferro", 76.7, "R$ 76,7 bi", "ink"), ("cobre + níquel", 18.5, "R$ 18,5 bi", "cobre")], carimbo="4 PRA 1")),
"25-placar-vale": ("barras", dict(rot="OS MESMOS R$ 10 MIL · 12 MESES ATÉ 25/09", linhas=[
    ("o cobre (COMEX)", 14.2, "R$ 14,2 mil", "cobre"), ("CPER (só o metal)", 13.3, "R$ 13,3 mil", "gray"),
    ("Vale c/ dividendos", 13.0, "R$ 13,0 mil", "ink")], nota="a Vale ficou abaixo do próprio metal", base=10)),
"26-copx": ("num", dict(rot="COPX · ETF DE 40 MINERADORAS DE COBRE", val=15.3, dec=1, pre="R$ ", suf=" mil",
    sub="os mesmos R$ 10 mil, 12 meses até 25/09", cor="verde", de="R$ 10 mil")),
"27-bdr": ("frase", dict(rot="BCPX39 · NA B3", l1="BDR = recibo", l2="comprado em real, representa o COPX lá fora")),
# ---------- PUBLI ----------
"28-div-30": ("barras", dict(rot="DIVIDENDO DO COPX · DEZ/2025 · POR COTA", linhas=[
    ("pago lá fora", 1.67, "US$ 1,67", "gray"), ("chega aqui", 1.17, "~US$ 1,17", "red")], carimbo="30% FICAM NOS EUA")),
"29-isencao": ("frase", dict(rot="ISENÇÃO DE R$ 20 MIL POR MÊS", l1="não vale pra BDR", l2="vale só pra ação brasileira", cor="red")),
"30-grana": ("lista", dict(rot="GRANA · PARCEIRA E INVESTIDORA: B3", itens=[
    "confere seus DARFs desde 2020", "calcula juros e multa", "paga no app, sem emitir guia",
    "calcula o IR de cada mês e avisa", "monta a declaração sozinho"])),
"31-cupom": ("cupom", dict(cod="DESENROLADENIS", off="R$ 90 OFF", sub="histórico desde 2020 + Declaração 2027 · até 30/09 · link na descrição")),
# ---------- BLOCO 5 ----------
"32-predio": ("duas", dict(rot="A POSIÇÃO DO BURRY, SEGUNDO O MEME", a="vendido", asub="no prédio (data center / IA)",
    b="comprado", bsub="na fiação (o cobre lá dentro)", rodape="")),
"33-18anos": ("barras", dict(rot="QUANTO DEMORA PRA FICAR PRONTO", linhas=[
    ("data center", 3, "2 a 3 anos", "gray"), ("mina nova", 18, "~18 anos", "cobre")],
    nota="segundo Torsten Slok (Apollo): nenhuma grande jazida nova no ano passado")),
"34-queda30": ("formula", dict(rot="SE O COBRE CAIR 30%", partes=["6,83 × 0,7", "=", "4,78"], res="4,78 − 2,25 = 2,53",
    sub="sobra por libra, em US$ (conta hipotética)")),
"35-metade": ("barras", dict(rot="A SOBRA DA MINA POR LIBRA", linhas=[
    ("hoje", 4.58, "US$ 4,58", "verde"), ("cobre −30%", 2.53, "US$ 2,53", "red")], carimbo="−45%")),
# ---------- BLOCO 6 ----------
"36-pergunta": ("frase", dict(rot="ANTES DE COMPRAR QUALQUER COISA COM COBRE NO NOME", l1="a pergunta do boi", l2="três perguntas")),
"37-p1": ("lista", dict(rot="PERGUNTA 1", itens=["dono do boi ou do açougue?", "Ero: tira da terra", "Paranapanema: compra e passa adiante"])),
"38-p2": ("lista", dict(rot="PERGUNTA 2", itens=["quanto boi tem nessa fazenda?", "Vale: minério 4 × 1 cobre+níquel", "BCPX39: só boi, em 40 fazendas"])),
"39-p3": ("lista", dict(rot="PERGUNTA 3", itens=["se a carne cair 30%, quem paga?", "o dono do boi, primeiro", "e dobrado: o pasto não barateia"])),
"40-boi-balcao": ("duas", dict(rot="ANTES DE PAGAR POR COBRE", a="o boi", asub="ou", b="o balcão?", bsub="", rodape="")),
}

# ---------- 27/09 noite: Denis "precisamos deixar o video mais preenchido" ----------
T.update({
"41-placar-qi": ("frase", dict(rot="ESSE PLACAR NÃO MEDE", l1="quem é mais esperto", l2="o Barsi não desaprendeu; o Burry não virou gênio numa segunda-feira")),
"42-estatua": ("frase", dict(rot="COBRE + TEMPO", l1="fica verde", l2="a Estátua da Liberdade é de cobre — o verde é a pátina", cor="verde")),
"43-duas-minas": ("duas", dict(rot="AS MINAS DA ERO NO BRASIL", a="Caraíba", asub="Jaguarari · Bahia", b="Tucumã", bsub="Pará", rodape="")),
"44-fora-rj": ("frase", dict(rot="O FIADO DA ERO", l1="fora da RJ", l2="a conta que a Paranapanema deve pra Ero ficou fora do plano de recuperação")),
"45-logica-barsi": ("frase", dict(rot="A LÓGICA DO BARSI", l1="dividendo + paciência", l2="a Paranapanema está testando a paciência dele", foto="barsi")),
"46-diluicao": ("barras", dict(rot="DILUIÇÃO · AS MESMAS AÇÕES, NUM BOLO MAIOR", linhas=[
    ("antes", 5, "5%", "gray"), ("depois", 1.26, "1,26%", "red")], nota="o Barsi não vendeu: entrou mais ação no bolo")),
"47-mesmo-ligado": ("frase", dict(rot="E SE O FORNO ESTIVESSE LIGADO?", l1="outro jeito de ganhar", l2="o forno nunca ganhou como a mina")),
"48-dono-boi": ("lista", dict(rot="O DONO DO BOI", itens=["pasto, ração, veterinário", "custo quase igual todo ano", "carne cara: a diferença cai no bolso"])),
"49-custo-preco": ("barras", dict(rot="POR LIBRA DE COBRE · ERO", linhas=[
    ("custo", 2.25, "US$ 2,25", "gray"), ("preço", 6.83, "US$ 6,83", "cobre")], carimbo="CHAMPANHE")),
"50-acougue": ("frase", dict(rot="O DONO DO AÇOUGUE", l1="compra e vende", l2="a carne sobe na etiqueta e sobe junto na nota do fornecedor", cor="red")),
"51-corte": ("frase", dict(rot="O QUE FICA COM O AÇOUGUEIRO", l1="o corte", l2="o serviço — não o preço da carne")),
"52-vale-boi": ("frase", dict(rot="A VALE É DONA DE BOI?", l1="é, mas…", l2="o boi divide a fazenda com o minério de ferro")),
"53-voltou": ("balao", dict(txt="Foi atrás do cobre e voltou pra casa com minério de ferro.", sub="")),
"54-div-inteiro": ("barras", dict(rot="DE CADA US$ 1 DE DIVIDENDO", linhas=[
    ("ação brasileira", 1.0, "cai inteiro", "verde"), ("COPX via BDR", .70, "US$ 0,70", "red")], nota="30% ficam retidos nos EUA")),
"55-darf": ("frase", dict(rot="QUEM EMITE A GUIA", l1="o DARF é seu", l2="vendeu BDR com lucro: 15%, sem isenção", cor="red")),
"56-b3-grana": ("frase", dict(rot="GRANA", l1="B3", l2="parceira e investidora do app")),
"57-multa": ("frase", dict(rot="IMPOSTO ESQUECIDO", l1="juros + multa", l2="o Grana mostra cada pendência já calculada", cor="red")),
"58-dividendo-multa": ("frase", dict(rot="NA SUA CABEÇA A CARTEIRA CRESCE", l1="a multa também", l2="é o dividendo entrando pra pagar multa", cor="red")),
"59-ia-esfria": ("balao", dict(txt="Se a IA esfriar, quem compra o cobre?", sub="")),
"60-pasto": ("frase", dict(rot="QUANDO A CARNE CAI", l1="o pasto não cai", l2="o custo da mina fica parado", cor="red")),
"61-ero-vs-cobre": ("barras", dict(rot="12 MESES ATÉ 25/09 · EM DÓLAR", linhas=[
    ("Ero Copper", 104, "+104%", "verde"), ("o cobre", 44, "+44%", "cobre")], nota="mineradora sobe mais que o metal — e cai mais também")),
"62-burry-barsi": ("duas", dict(rot="A MESMA ESTRADA", a="Burry", asub="comprou o boi", b="Barsi", bsub="sócio do açougue — diluído, paciente", rodape="", fa="burry", fb="barsi")),
"63-gargalo": ("duas", dict(rot="OS GARGALOS DA IA", a="energia", asub="todo mundo falando", b="cobre", bsub="data center é cheio de fio", rodape="")),
"64-quem-onde": ("duas", dict(rot="COMO CADA UM ESTÁ NO COBRE", a="mineração", asub="Burry · Ero", b="refino", bsub="Barsi · Paranapanema", rodape="", fa="burry", fb="barsi")),
})
