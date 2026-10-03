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

TETO   = 6.0   # Denis, 11/09: cartela dura a frase do numero, nao o assunto inteiro
MIN    = 3.0
JANELA = 9.0
# peca G (grafico de serie): a linha precisa de tempo pra se desenhar e o numero pousa em 62% da duracao.
# Menos de 5 s nao da tempo de ler; mais de 10 s a linha fica parada. (Denis aprovou o grafico em 03/10.)
LIMITES = {"G": (5.0, 10.0)}

def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")

from pecas import PECAS

segs = json.load(open(sys.argv[1] if len(sys.argv) > 1 else "rendercorte.json"))["segments"]
txt  = [(s["start"], s["end"], norm(s["text"])) for s in segs]

achados, faltando = [], []
for pid, peca, anc, atraso, *resto in PECAS:
    depois = resto[0] if resto else 0.0          # 5o campo opcional: so procurar a partir daqui
    rx = re.compile(anc)
    hit = next((t for t in txt if t[0] >= depois and rx.search(t[2])), None)
    if not hit:
        faltando.append((pid, anc)); continue
    achados.append([pid, peca, round(hit[0] + atraso, 2)])

achados.sort(key=lambda a: a[2])
plano = {}
for i, (pid, peca, entra) in enumerate(achados):
    lim = achados[i+1][2] if i + 1 < len(achados) else 1e9
    # fim da FRASE que carrega o numero: o segmento da ancora; se ele e curtinho, o seguinte junto
    seg = next(((a, e) for a, e, _ in txt if a <= entra <= e), None) or (entra, entra)
    fim_fala = seg[1]
    if fim_fala - entra < 2.5:
        prox = [e for a, e, _ in txt if seg[1] <= a <= seg[1] + 0.8]
        if prox: fim_fala = prox[0]
    alvo = min(fim_fala, lim - 0.6)
    mn, teto = LIMITES.get(peca, (MIN, TETO))
    if peca == "G":
        if lim - 0.6 - entra < mn:
            raise SystemExit(f"✗ grafico {pid} entra em {entra:.1f}s e a proxima peca entra {lim - entra:.1f}s depois: "
                             f"precisa de {mn:.0f} s. De atraso a proxima peca ou mude a ancora em pecas.py.")
    dur = max(mn, min(teto, alvo - entra))
    plano[pid] = {"peca": peca, "entra": entra, "dur": round(dur, 1)}

json.dump(plano, open("plano.json", "w"), indent=1, ensure_ascii=False)
cob = sum(p["dur"] for p in plano.values())
print(f"{len(plano)} pecas | {cob:.0f}s de imagem")
for pid, p in sorted(plano.items(), key=lambda kv: kv[1]["entra"]):
    print(f"  {p['peca']} {p['entra']:8.2f} +{p['dur']:5.1f}s  {pid}")
if faltando:
    print(f"\n✗ {len(faltando)} ancoras nao acharam a frase:")
    for pid, anc in faltando: print(f"  {pid}: /{anc}/")
