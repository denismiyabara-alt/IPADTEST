#!/usr/bin/env python3
"""Ancora cada peca de B-roll numa FRASE do roteiro, nao num timecode.

ponytail: o mapa a mao quebrou duas vezes (6 cartelas reprovadas no portao, e
todos os timecodes invalidados quando o corte mudou de 0,60s pra 0,32s de respiro).
Aqui a entrada sai de uma regex na transcricao do corte e a duracao sai da fala:
da entrada ate o fim do ultimo segmento sobre o assunto, teto de 11s. Recortou de
novo? Roda de novo e tudo se reposiciona sozinho.

Saida: plano.json  { id: {"peca","entra","dur"} }
"""
import json, re, sys, unicodedata

TETO   = 11.0
MIN    = 3.5
JANELA = 9.0   # ate onde procurar o fim da fala sobre o assunto

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

# (id, peca, ancora, atraso)  — ancora = regex no texto do segmento (sem acento, minusculo)
#   peca A = cartelas   B = prints/manchetes/graficos
PECAS = [
 ("01-3bi",            "A", r"desistiu de comprar mais de 3 bilh", 1.6),
 ("h1-mt-primeiro",    "B", r"desistiu mesmo",                     0.4),
 ("02-cancelou-subiu", "A", r"a cota subiu no dia",                0.0),
 ("03-emissao-bolsa",  "A", r"a bolsa esta pagando",               0.0),
 ("g1-1m",             "B", r"em 100 cotas",                       0.3),
 ("04-extrato",        "A", r"o extrato de 5 dias",                0.0),
 ("05-2608",           "A", r"cai a compra do patio",              0.0),
 ("p3-blca11-motivo",  "B", r"protocolaram na bolsa",              0.0),
 ("06-2708",           "A", r"o preco respondeu",                  0.0),
 ("07-3108",           "A", r"o fundo cancela o pacote",           0.0),
 ("h2-im-cyre3",       "B", r"as lajes da oscar freire",           0.0),
 ("p4-cyrela-214",     "B", r"2 bilh(o|õ)es para a economia|2,14 estao no mesmo neg", 0.0),
 ("p5-cyrela-fr",      "B", r"avisar a bolsa por escrito",         0.0),
 ("08-824",            "A", r"8,24",                               0.0),
 ("09-319",            "A", r"3,19",                               0.0),
 ("10-3108-fecha",     "A", r"veio o segundo cancelamento",        0.0),
 ("11-acumulado", "A", r"soma os (4|quatro) preg", 0.0),
 ("g2-1d",             "B", r"o preco ja votou",                   0.0),
 ("12-cyre3",          "A", r"acao da cirela subiu|acao da cyrela subiu", 0.0),
 ("h3-mt-telhado",     "B", r"quem nao vendeu o predio comemorou", 0.0),
 ("13-merchan",        "A", r"tem um simulador que calcula",       0.0),
 ("14-moeda",          "A", r"minha tabela vale",                  0.0),
 ("p6-cyrela-cotas",   "B", r"transforma esse pedaco em dinheiro", 0.0),
 ("15-cai-trava",      "A", r"se o preco da cota cai muito",       0.0),
 ("16-liquidez",       "A", r"a liquidez diaria e quanto de cota", 0.0),
 ("p1-condicoes",      "B", r"palavra por palavra",                0.0),
 ("h4-sd-nubank",      "B", r"mudanca nas condicoes de mercado|condicao de mercado mudou", 0.0),
 ("p7-com-trxf11",     "B", r"apareceu a palavra que segura",      0.0),
 ("p2-distrato",       "B", r"memorando de entendimento",          0.0),
 ("17-semmulta",       "A", r"sem multa, sem sancao|levantar da mesa e ir embora", 0.0),
 ("18-fundo", "A", r"120 i?moveis", 0.0),
 ("31-oquee", "A", r"separar bem separado", 0.0),
 ("32-coincidencia", "A", r"chegaram na mesma conta", 0.0),
 ("33-deixou", "A", r"o fundo deixou de crescer", 0.0),
 ("34-boapraquem", "A", r"fosse uma coisa boa para o cotista", 0.0),
 ("35-naoarmadilha", "A", r"vinculante nao e uma", 0.0),
 ("36-recuou", "A", r"ele nao fechou, ele recuou", 0.0),
 ("37-sala", "A", r"a sala aparece de novo", 0.0),
 ("38-primeiraconta", "A", r"a primeira conta que voce tem", 0.0),
 ("p8-rg-imoveis",     "B", r"a cada 200 metros quadrados",        0.0),
 ("19-emissao13",      "A", r"13. emissao do fundo botou",         0.0),
 ("p9-rg-cotas",        "B", r"dobrar o tamanho do fundo",          0.0),
 ("20-diluicao",       "A", r"o nome e diluicao",                  0.0),
 ("21-2026",           "A", r"no ano a cota cai",                  0.0),
 ("g3-ytd",            "B", r"esse e o desconto",                  0.0),
 ("22-tabelas",        "A", r"a tabela da bolsa",                  0.0),
 ("23-afastam",        "A", r"quando elas se afastam",             0.0),
 ("24-parado", "A", r"era de fato ficar parado", 0.0),
 ("25-conta-moeda",    "A", r"a conta da moeda",                   0.0),
 ("26-emissao-tela",   "A", r"antes de olhar a foto do predio",    0.0),
 ("g4-noticias",       "B", r"essa conta e surreal|surreal de fazer", 0.0),
 ("27-duas-contas",    "A", r"a menos em cada cota",               0.0),
 ("28-mecanismo",      "A", r"duas pessoas diferentes",            0.0),
 ("29-diluido",        "A", r"quem esta sendo diluido",            0.0),
 ("30-moeda-lascada",  "A", r"quando esta lascada",                0.0),
]

segs = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "render02.json"))["segments"]
txt  = [(s["start"], s["end"], norm(s["text"])) for s in segs]

achados, faltando = [], []
for pid, peca, anc, atraso in PECAS:
    rx = re.compile(anc)
    hit = next((t for t in txt if rx.search(t[2])), None)
    if not hit:
        faltando.append((pid, anc)); continue
    achados.append([pid, peca, round(hit[0] + atraso, 2)])

achados.sort(key=lambda a: a[2])
plano = {}
for _ in range(4):          # empurrar uma entrada muda o limite da anterior: converge em 2-3 passadas
    plano = {}
    for i, (pid, peca, entra) in enumerate(achados):
        lim = achados[i+1][2] if i + 1 < len(achados) else 1e9
        proprio = max([e for a, e, _ in txt if a <= entra <= e] or [0])
        fim_fala = max([proprio] + [e for a, e, _ in txt
                                    if entra - 2 <= a <= min(lim - 0.8, entra + JANELA)])
        alvo = min(fim_fala, lim - 0.6)
        if alvo - entra > TETO:            # a fala e mais longa que o teto: entra mais tarde,
            entra = round(alvo - TETO, 2)  # pra sair junto com ela, nao no meio dela
            achados[i][2] = entra
        dur = max(MIN, min(TETO, alvo - entra))
        plano[pid] = {"peca": peca, "entra": entra, "dur": round(dur, 1)}
    achados.sort(key=lambda a: a[2])

json.dump(plano, open("plano.json", "w"), indent=1, ensure_ascii=False)
cob = sum(p["dur"] for p in plano.values())
print(f"{len(plano)} pecas | {cob:.0f}s de imagem")
for pid, p in sorted(plano.items(), key=lambda kv: kv[1]["entra"]):
    print(f"  {p['peca']} {p['entra']:8.2f} +{p['dur']:5.1f}s  {pid}")
if faltando:
    print(f"\n✗ {len(faltando)} ancoras nao acharam a frase:")
    for pid, anc in faltando: print(f"  {pid}: /{anc}/")
