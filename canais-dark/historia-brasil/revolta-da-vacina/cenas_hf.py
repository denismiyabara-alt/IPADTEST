"""Cenas do episódio A GUERRA CONTRA A VACINA (Revolta da Vacina, 1904).
Cada cena = (html, js) presa a um TRECHO da frase (não ao índice): se o roteiro.md mudar e o trecho
sumir, dá erro em vez de cair na frase errada. Com uma palavra no 3º campo, a cena entra quando
essa palavra é dita. Palito: {trecho: (pose, lado)}, lado E/D/C (a cena fica do outro lado).
Números e datas na tela: só os do quadro do roteiro.md (tests/test_episodio.py confere).
Sem partido, sem político vivo, sem vacina de hoje. O B5 (mortos e presos) não tem piada.
"""
import ast
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
CANAL = os.path.dirname(HERE)
if CANAL not in sys.path:
    sys.path.insert(0, CANAL)
from pecas import (MEDALHA, MOSQUITO, RATO, SERINGA, ano, calendario, cardapio, carimbo, contador,  # noqa: E402
                   duelo, ficha, junta, linha_tempo, lista, multidao, napoleao, no_momento, placa, prop,
                   ratos, recorte, recortes, titulo)


# ---------- de frase para índice ----------
def frases(bloco):
    py = os.path.join(HERE, "blocos.py")
    if os.path.exists(py):
        arvore = ast.parse(open(py, encoding="utf-8").read())
        blocos = next(ast.literal_eval(n.value) for n in arvore.body
                      if isinstance(n, ast.Assign) and any(getattr(t, "id", "") == "BLOCOS" for t in n.targets))
        return [t for t, _ in blocos[bloco]]
    import roteiro
    return [t for t, _ in roteiro.ler(os.path.join(HERE, "roteiro.md")).blocos[bloco]]


def indice(textos, trecho):
    achadas = [k for k, t in enumerate(textos) if trecho in t]
    if len(achadas) != 1:
        raise ValueError(f"trecho {trecho!r}: {len(achadas)} frases batem (precisa ser exatamente 1)")
    return achadas[0]


def dirigir(bloco, cenas, palito=None, cauda=None):
    textos = frases(bloco)
    C, P = {}, {}
    for item in cenas:
        k = indice(textos, item[0])
        if k in C:
            raise ValueError(f"{bloco}: duas cenas na frase {k}")
        cena = item[1]
        if len(item) > 2:
            cena = no_momento(cena, textos[k].index(item[2]) / len(textos[k]))
        C[k] = cena
    for trecho, est in (palito or {}).items():
        P[indice(textos, trecho)] = est
    return (C, P) if cauda is None else (C, P, cauda)


FONTE_MS = "Ministério da Saúde, PNI 50 anos (2023)"
FONTE_ANVISA = "Anvisa, Almanaque Visa É nº 1 (2008)"


# ---------- b0 — o inimigo ----------
def cenas_b0():
    return dirigir("b0", [
        ("passou uma semana", ano("v00", 1904, "Rio de Janeiro · uma semana em pé de guerra")),
        ("Teve motim", multidao("v01", 14, 5, "motim · prisões · até uma escola militar")),
        ("E o inimigo", titulo("O INIMIGO:", sid="v02")),
        ("era uma vacina", junta(prop(SERINGA.replace("{sid}", "v03s"), "v03"), carimbo("UMA VACINA", sid="v03k", pequeno=True))),
        ("Parece piada", ficha("Revolta da Vacina · 10 a 16/11/1904", FONTE_MS, "v04")),
    ], {"passou uma semana": ("apontar", "E"), "era uma vacina": ("shrug", "E"), "Parece piada": ("maos", "E")})


# ---------- b1 — a cidade ----------
def cenas_b1():
    return dirigir("b1", [
        ("era a capital", recorte("RIO DE JANEIRO", "capital federal", "1903", "v10")),
        ("túmulo dos estrangeiros", carimbo("TÚMULO DOS<br>ESTRANGEIROS", "o apelido da cidade", "v11", pequeno=True)),
        ("uns quatro mil", contador("v12", 0, 4000, 0, "≈ ", "", "imigrantes mortos por doença · 1897 a 1906", "tijolo", 1.4), "quatro mil"),
        ("rodízio", cardapio("RODÍZIO DO RIO", ["febre amarela", "peste bubônica", "varíola"], "v13")),
        ("o governo chamou", ano("v14", 1903, "o governo chama um médico")),
        ("O nome dele", ficha("OSWALDO CRUZ", FONTE_ANVISA, "v15", nota="diretor-geral de Saúde Pública (≈ ministro da Saúde) · nasc. 05/08/1872")),
        ("Currículo", lista([("medicina aos 15 anos", True), ("laboratório no porão", True), ("Instituto Pasteur, Paris", True)], "v16")),
        ("a maioria de nós", titulo("AOS 15:", "nós montando uma desculpa pra faltar na aula", "sepia", "v17")),
        ("rapaz de trinta anos", contador("v18", 0, 30, 0, "", " anos", "e uma capital inteira pra desinfetar", "", 1.0)),
    ], {"era a capital": ("apontar", "E"), "túmulo": ("susto", "E"), "uns quatro mil": ("serio", "E"), "rodízio": ("shrug", "E"),
        "O nome dele": ("apontar", "D"), "a maioria de nós": ("pensar", "D"), "rapaz de trinta": ("maos", "D")})


# ---------- b2 — mosquito e rato ----------
def cenas_b2():
    return dirigir("b2", [
        ("pela febre amarela", prop(MOSQUITO, "v20", "febre amarela: transmitida por mosquito")),
        ("brigadas mata-mosquitos", ficha("BRIGADAS MATA-MOSQUITOS", FONTE_ANVISA, "v21", nota="homens de uniforme · casas e quintais · fim da água parada")),
        ("abrir a porta", placa("FISCALIZAÇÃO", "abra a porta · mostre a caixa d'água", "v22")),
        ("sem ninguém te explicar", carimbo("SEM EXPLICAÇÃO", sid="v23")),
        ("Guarda essa parte", titulo("GUARDA<br>ESSA PARTE", cor="sepia", sid="v24")),
        ("peste bubônica", prop(RATO, "v25", "peste bubônica: a pulga do rato")),
        ("comprar rato morto", placa("COMPRA-SE RATO", "Diretoria-Geral de Saúde Pública", "v26")),
        ("criar rato em casa", ratos("v27", 12, "a criação")),
        ("Tem documento", ficha("A COMPRA DE RATOS", "Biblioteca Virtual Oswaldo Cruz (Fiocruz), Campanha contra a Peste", "v28")),
    ], {"pela febre amarela": ("apontar", "E"), "abrir a porta": ("susto", "E"), "Guarda essa parte": ("pensar", "E"),
        "peste bubônica": ("apontar", "D"), "criar rato": ("shrug", "D"), "Tem documento": ("maos", "D")})


# ---------- b3 — a lei ----------
def cenas_b3():
    return dirigir("b3", [
        ("a vez da varíola", titulo("VARÍOLA", cor="tijolo", sid="v30")),
        ("Edward Jenner", linha_tempo("v31", [1798, 1904], "Edward Jenner · mais de cem anos de vacina")),
        ("saiu a lei", ficha("LEI Nº 1.261 · 31/10/1904", "Câmara dos Deputados, Legislação Informatizada", "v32", "LEI", nota="vacinação e revacinação contra a varíola obrigatórias")),
        ("sem anestesia", carimbo("OBRIGATÓRIA", sid="v33")),
        ("atestado de vacina", lista([("escola", True), ("emprego", True), ("viagem", True), ("casamento", True)], "v34")),
        ("Quer casar?", titulo("QUER CASAR?", "primeiro mostra o braço", sid="v35")),
    ], {"a vez da varíola": ("serio", "E"), "Edward Jenner": ("apontar", "E"), "sem anestesia": ("susto", "E"),
        "atestado de vacina": ("apontar", "E"), "Quer casar?": ("shrug", "E")})


# ---------- b4 — a propaganda ----------
def cenas_b4():
    return dirigir("b4", [
        ("ninguém fez campanha", lista([("campanha explicando a vacina", False), ("campanha contra", True)], "v40")),
        ("Os jornais caíram", recortes("v41", ["OS JORNAIS: CONTRA", "O CONGRESSO PROTESTA", "LIGA CONTRA A VACINAÇÃO OBRIGATÓRIA"])),
        ("O Malho", recorte("GUERRA VACCINO-OBRIGATEZA!", "O Malho", "29/10/1904", "v42")),
        ("deu um apelido", napoleao("v43", "“o Napoleão da seringa e lanceta”")),
        ("até elegante", titulo("ELEGANTE.", cor="sepia", sid="v44")),
        ("o desenhista", duelo("v45", ("GOVERNO", "a ciência", True), ("OPOSIÇÃO", "o desenhista", False))),
        ("Adivinha", titulo("?", "quem ganhou a discussão", "tijolo", "v46")),
    ], {"ninguém fez campanha": ("shrug", "D"), "O Malho": ("apontar", "D"), "até elegante": ("pensar", "D"),
        "o desenhista": ("maos", "C"), "Adivinha": ("shrug", "D")})


# ---------- b5 — a revolta (sem piada) ----------
def cenas_b5():
    return dirigir("b5", [
        ("não era só a vacina", lista([("fiscal entrando em casa", True), ("ordem sem explicação", True), ("vacina obrigatória", True)], "v50")),
        ("almanaque da Anvisa", ficha("“atuação autoritária” · “violenta reação popular”", FONTE_ANVISA, "v51")),
        ("o Rio explodiu", calendario("v52", "NOVEMBRO DE 1904", list(range(10, 17)), list(range(10, 17)))),
        ("No dia treze", titulo("13/11", "a revolta toma as ruas", sid="v53")),
        ("No dia catorze", titulo("14/11", "a Escola Militar da Praia Vermelha se levanta", sid="v54")),
        ("cerca de trinta mortos", ficha("cerca de 30 mortos · mais de 900 detidos", FONTE_MS, "v55", "SALDO")),
        ("derrotou a revolta", carimbo("SUSPENSA", "a obrigatoriedade da vacina", "v56")),
        ("ninguém ganhou", titulo("NINGUÉM<br>GANHOU.", "e a varíola continuou lá", "sepia", "v57")),
    ], {"não era só a vacina": ("serio", "E"), "o Rio explodiu": ("serio", "E"), "cerca de trinta": ("serio", "E"),
        "derrotou a revolta": ("pensar", "E"), "ninguém ganhou": ("shrug", "E")})


# ---------- b6 — o fim da história ----------
def cenas_b6():
    return dirigir("b6", [
        ("a parte boa", titulo("A PARTE BOA", sid="v60")),
        ("febre amarela estava erradicada", ano("v61", 1907, "febre amarela erradicada do Rio")),
        ("medalha de ouro", prop(MEDALHA.replace("{l1}", "BERLIM").replace("{l2}", "1907"), "v62", "Congresso Internacional de Higiene e Demografia")),
        ("condecorado", napoleao("v63", "condecorado · sem invadir ninguém", medalha=True)),
        ("nova epidemia", ano("v64", 1908, "nova epidemia de varíola", "tijolo")),
        ("foi sozinha", multidao("v65", 11, 0, "fila no posto de vacinação · ninguém precisou obrigar", fila=True)),
        ("O que a lei não conseguiu", duelo("v66", ("1904", "a lei", False), ("1908", "o susto", True))),
        ("Manguinhos", ficha("INSTITUTO OSWALDO CRUZ", FONTE_ANVISA, "v67", nota="Manguinhos, rebatizado com o nome dele · 1909")),
        ("Isso, sim, é atestado", carimbo("ATESTADO", "isso, sim", "v68")),
        ("últimos casos", ano("v69", 1977, "os últimos casos de varíola no mundo")),
    ], {"a parte boa": ("vitoria", "D"), "medalha de ouro": ("apontar", "D"), "nova epidemia": ("susto", "D"),
        "foi sozinha": ("maos", "D"), "Manguinhos": ("apontar", "D"), "últimos casos": ("vitoria", "D")})


# ---------- b7 — o fecho ----------
def cenas_b7():
    return dirigir("b7", [
        ("Resumindo", duelo("v70", ("A VACINA", "tinha razão", True), ("O RESTO", "errou feio", False))),
        ("Mandou sem explicar", lista([("explicar", False), ("convencer", False), ("comprar rato", True)], "v71")),
        ("A vacina venceu", junta(titulo("A VACINA VENCEU.", sid="v72"), carimbo("COMUNICAÇÃO: GOLEADA", sid="v72k", pequeno=True))),
        ("único que entendeu", prop(RATO, "v73", "o único que entendeu o plano", entrada="lado")),
        ("Tem documento", ficha("FONTES NA DESCRIÇÃO", "Ministério da Saúde · Anvisa · Fiocruz · Câmara dos Deputados", "v74", "ARQUIVO")),
    ], {"Resumindo": ("maos", "E"), "Mandou sem explicar": ("shrug", "E"), "único que entendeu": ("pensar", "E"),
        "Tem documento": ("idle", "E")}, cauda=3.0)
