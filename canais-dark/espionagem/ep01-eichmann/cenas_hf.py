"""Cenas do episodio 1 (A captura de Eichmann). Cada cena = (trecho da frase, peca).
A cena entra na frase que contem o trecho e fica ate a proxima. Trecho que sumir do roteiro.md = erro no build.
Imagens: so as da licencas-ep01.csv (o teste confere). Sem imagem livre = peca REC (selo RECONSTITUICAO).
Morte contada, nunca mostrada: a execucao e so texto sobre preto (peca preto).
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from build_hf import (arquivo, cartela_ato, datilo, documento, linha_tempo, lista_fontes, mapa_sf,  # noqa: E402
                      placar, planta, preto, rota, silhueta, titulo, video)

LINHA = [("1906", "nascimento"), ("1932", "entra na SS"), ("1942", "Wannsee"), ("1944", "Hungria"),
         ("1945", "desaparece"), ("1950", "Argentina"), ("1960", "captura"), ("1961", "julgamento"), ("1962", "execução")]
EUROPA_SUL = (60, -45, -70, 30)          # caixa lat_max, lat_min, lon_min, lon_max
ATLANTICO = (45, -45, -70, 45)
HUNGRIA = (56, 42, 5, 30)

CENAS = {
    "b0": [
        ("Onze de maio de mil novecentos e sessenta", datilo("11 DE MAIO DE 1960")),
        ("Já é noite em San Fernando", mapa_sf(noite=True)),
        ("Em volta dele", mapa_sf(noite=True, carros=True)),
        ("Os documentos dele dizem", arquivo("eichmann-passaporte-cruz-vermelha.jpg", foco=(0.3, 0.5))),
        ("Naquela noite, o ônibus de sempre chega", mapa_sf(noite=True, carros=True, relogio=("19:40", "20:05"))),
        ("Adolf Eichmann.", arquivo("eichmann-julgamento-1961.jpg")),
        ("Esta é a história", titulo("A captura de Eichmann", "BUENOS AIRES · 1960")),
    ],
    "b1": [
        ("Para entender essa caçada", cartela_ato("I. O burocrata")),
        ("Otto Adolf Eichmann nasceu", linha_tempo(LINHA, 0)),
        ("Em janeiro de mil novecentos e quarenta e dois", datilo("WANNSEE · 20 JAN. 1942", rec=True)),
        ("Na Hungria", rota([("Budapeste", 47.5, 19.04), ("Auschwitz", 50.03, 19.2)], HUNGRIA)),
        ("O Holocausto matou", linha_tempo(LINHA, 3)),
        ("Mas em maio de mil novecentos e quarenta e cinco", linha_tempo(LINHA, 4)),
    ],
    "b2": [
        ("No fim da guerra", cartela_ato("II. Ricardo Klement")),
        ("Em mil novecentos e cinquenta, atravessou", rota([("Norte da Alemanha", 53, 10), ("Gênova", 44.4, 8.9),
                                                             ("Buenos Aires", -34.6, -58.4)], EUROPA_SUL)),
        ("Em Gênova, conseguiu", arquivo("eichmann-passaporte-cruz-vermelha.jpg", zoom="out")),
        ("Com ele, embarcou", linha_tempo(LINHA, 5)),
        ("A família chegou usando o sobrenome verdadeiro", datilo("EICHMANN")),
    ],
    "b3": [
        ("A pista que levou", cartela_ato("III. A pista")),
        ("Klaus, o filho mais velho", silhueta("banco")),
        ("Em mil novecentos e cinquenta e sete", datilo("FRITZ BAUER · PROCURADOR-GERAL DE HESSE", classe="nome")),
        ("Lá, o caso foi para o Mossad", arquivo("isser-harel-1969.jpg")),
        ("Em mil novecentos e cinquenta e oito, um agente", mapa_sf(noite=False)),
        ("Arquivos da CIA abertos", documento("cia-memo-dulles-1953.jpg", caixa=(0.25, 0.362, 0.53, 0.112))),
        ("O texto diz que o único caminho legal", documento(
            "cia-memo-dulles-1953.jpg", caixa=(0.25, 0.362, 0.53, 0.112),
            traducao="\"Se o nosso pessoal encontrar Eichmann, o único caminho legal seria informar o governo alemão, "
                     "que poderia então pedir a extradição. (...) Qualquer ação da Agência teria de ser secreta e ilegal.\" "
                     "CIA, 9 out. 1953 (tradução do canal)")),
        ("Um memorando de março", documento("cia-memo-1958-clemens.jpg",
                                            traducao="Março de 1958: \"Eichmann vive na Argentina com o nome de Clemens\" (CONFERIR NO MAC a página e a citação).")),
    ],
    "b4": [
        ("Quem reacendeu o caso", cartela_ato("IV. As flores")),
        ("Alguém da vizinhança", mapa_sf(noite=False)),
        ("Vinte e um de março de mil novecentos e sessenta", datilo("21 DE MARÇO DE 1960")),
        ("Naquela noite, os agentes viram", silhueta("flores")),
        ("Eram bodas de prata", datilo("21 DE MARÇO DE 1935 · 25 ANOS")),
    ],
    "b5": [
        ("Harel montou uma equipe", cartela_ato("V. Onze de maio")),
        ("Na noite de onze de maio", mapa_sf(noite=True, carros=True, relogio=("19:40", "20:05"))),
        ("Pouco depois, na casa", planta()),
    ],
    "b6": [
        ("Eichmann ficou cerca de dez dias", cartela_ato("VI. O voo")),
        ("A delegação viajaria", arquivo("britannia-el-al-1958.jpg")),
        ("Harel e parte da equipe", documento("harel-cartao-el-al.jpg")),
        ("O avião decolou", rota([("Buenos Aires", -34.6, -58.4), ("Dakar", 14.7, -17.4), ("Lod", 31.95, 34.9)], ATLANTICO)),
    ],
    "b7": [
        ("No dia seguinte", cartela_ato("VII. A soberania")),
        ("No mesmo dia, um tribunal", documento("ordem-prisao-1960-05-23.jpg")),
        ("A Argentina levou o caso", documento("resolucao-138-onu.jpg",
                                               traducao="Resolução 138, 23 de junho de 1960: pede a Israel \"reparação adequada\" (tradução do canal).")),
        ("Foram oito votos", placar("8", "0", "2", "a Argentina não votou")),
    ],
    "b8": [
        ("O julgamento começou", arquivo("eichmann-julgamento-1961.jpg")),
        ("Eram três juízes", arquivo("juizes-julgamento-1961.jpg")),
        ("A acusação era chefiada", arquivo("hausner-servatius-1961.jpg")),
        ("A defesa sustentou", arquivo("eichmann-cabine-anotacoes-1961.jpg")),
        ("A acusação chamou", arquivo("dinur-testemunha-1961.jpg")),
        ("O julgamento foi filmado", video("cinejornal-1961-eichmann.mp4")),
        ("Em quinze de dezembro", arquivo("sentenca-1961-12-15.jpg")),
        ("Adolf Eichmann foi enforcado", preto(["31 DE MAIO / 1º DE JUNHO DE 1962", "PRISÃO DE RAMLA"])),
    ],
    "b9": [
        ("Mais de sessenta anos depois", cartela_ato("O que se sabe", "e o que não se sabe")),
        ("O que não está em disputa", linha_tempo(LINHA, 8)),
        ("Os milhões de pessoas", preto(["Os deportados não tiveram tribunal."])),
        ("As fontes deste episódio", lista_fontes([
            "Neal Bascomb, Hunting Eichmann (2009)", "Isser Harel, The House on Garibaldi Street (1975)",
            "Peter Z. Malkin e Harry Stein, Eichmann in My Hands (1990)", "Hannah Arendt, Eichmann em Jerusalém (1963)",
            "CIA, name file de Eichmann, NARA RG 263", "ONU, Conselho de Segurança, Resolução 138 (1960)",
            "USHMM e Yad Vashem, gravações do julgamento (1961)"])),
    ],
}
