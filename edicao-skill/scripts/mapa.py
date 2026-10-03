#!/usr/bin/env python3
"""Calcula a janela de cada cartela dentro da sua peca e escreve o mapa de insercao.
ponytail: mapa derivado dos geradores — mudou a duracao la, o mapa acompanha sozinho."""
import json

GERADORES = {"A": ("videos/trxf11-broll-dados/gerar.py", "FR", 2),
             "B": ("videos/trxf11-broll-materias/gerar.py", "CENAS", 7),
             "C": ("videos/trxf11-broll-frases/gerar.py", "FR", 2)}
OVER = 0.3

# onde cada cartela entra no FINAL (segundos)
ENTRA = {
 "01-1960":4.0, "02-093":21.0, "m0-nota093":26.6, "03-queda":43.0, "m7-grafico":55.0, "m1-fatos":66.0,
 "m2-iguatemi":90.0, "04-iguatemi":105.0, "m3-guarulhos":112.0, "05-guarulhos":125.0, "06-abl":147.0,
 "07-caprate":188.0, "08-degraus":220.0, "09-preco-emissao":242.0, "10-tela-vs-oferta":257.0,
 "g01-mesa":288.3, "g02-recompra":320.7, "g03-aaa":334.2, "11-ocupacao":348.0, "m4-keleti-08":358.0,
 "g04-toplinha":370.0, "g05-ativosbons":398.0, "g06-atipico":409.8, "g07-escala":428.5, "g08-precoerrado":450.7,
 "12-taxas":472.0, "m5-nota":499.0, "g09-entra":537.0, "13-performance":564.0, "g10-aluguelvelho":600.6,
 "g11-inquilino":626.0, "g12-contra":661.5, "g13-relogios":685.1, "g14-salataxa":712.9, "14-escala-taxa":732.0,
 "g15-obra":749.9, "g16-permuta":854.1, "g17-caixa":880.0, "g18-regua":910.7, "15-cdi":935.0,
 "g19-troca":942.2, "g20-junho":972.8, "g21-teto":980.7, "16-13a":1015.0, "g22-diluicao":1030.3,
 "m6-keleti-14":1066.0, "17-ntnb":1077.0, "g23-troca2":1119.2, "g24-risco":1130.2, "18-veredito":1139.0,
 "g25-mercado":1147.7, "g26-nemroubada":1163.6, "g27-tresperguntas":1187.6, "g28-socio":1208.0, "g29-alibaba":1248.6,
}

janelas = {}
for peca, (caminho, var, idx) in GERADORES.items():
    ns = {}
    exec(open(caminho).read().split("os.makedirs")[0], ns)
    t = 0.0
    for it in ns[var]:
        janelas[it[0]] = (peca, round(t, 2), round(t + it[idx], 2), it[idx])
        t += it[idx] - OVER

cart = []
for cid, entra in ENTRA.items():
    if cid not in janelas: raise SystemExit(f"cartela {cid} nao existe no gerador")
    p, ini, fim, dur = janelas[cid]
    cart.append((p, ini, fim, entra, cid, dur))
cart.sort(key=lambda c: c[3])

# a cartela nao pode invadir a proxima nem passar do fim do video
for i, c in enumerate(cart):
    lim = cart[i+1][3] if i+1 < len(cart) else 1344.34
    sobra = (c[3] + c[5]) - (lim - 0.5)
    if sobra > 0:
        cart[i] = (c[0], c[1], round(c[2]-sobra, 2), c[3], c[4], round(c[5]-sobra, 2))
        print(f"  aparado: {c[4]} -{sobra:.1f}s (encostava na proxima)")

# PORTAO: a cartela nao pode sair enquanto ele ainda fala do assunto (erro do TRXF11)
import os
reprovas = []
if os.path.exists("final.json"):
    segs = json.load(open("final.json"))["segments"]
    for i, c in enumerate(cart):
        entra, sai = c[3], c[3] + c[5]
        lim = cart[i+1][3] if i+1 < len(cart) else 1344.34
        fim_fala = max([s["end"] for s in segs
                        if entra - 2 <= s["start"] <= min(lim - 0.8, entra + 9)] or [0])
        buraco = min(lim, fim_fala) - sai
        # ate 2,5s o corte de volta pro Denis le como edicao normal; acima disso
        # a cartela sai no meio do raciocinio (o defeito do TRXF11, de 6 a 12s)
        if buraco > 2.5:
            reprovas.append(f"  {c[4]}: sai em {sai:.1f}s, fala ate {min(lim, fim_fala):.1f}s "
                            f"(buraco de {buraco:.1f}s)")
if reprovas:
    print(f"\n✗ {len(reprovas)} cartelas saem antes da fala acabar — NAO RENDERIZAR:")
    print("\n".join(reprovas))
    raise SystemExit(1)
print("✓ nenhuma cartela sai antes da fala acabar")

with open("cartelas.json", "w") as fh:
    json.dump([{"peca":c[0],"ini":c[1],"fim":c[2],"entra":c[3],"id":c[4]} for c in cart], fh, indent=1)
cob = sum(c[5] for c in cart)
print(f"{len(cart)} cartelas · {cob:.0f}s de imagem = {cob/1344.34*100:.1f}% do video")
