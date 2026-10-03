#!/usr/bin/env python3
"""Visao de revisao de bruto/render: fala + gaps + flags de corte.
uso: python3 timeline.py master.json  > timeline.txt
Flags:
  PATO      marcador de regravacao (pato/pata, e as variantes que o Whisper inventa)
  GAP-PAL   silencio dentro de um segmento (o Whisper estica uma palavra e engole o vazio)
  ENGOLIDO? segmento longo com poucas palavras — costuma esconder pato
"""
import json, re, sys

src = sys.argv[1] if len(sys.argv) > 1 else "master.json"
segs = json.load(open(src))["segments"]

# ponytail: o Whisper erra a 1a palavra do marcador (ja vi "fato", "do lado", "pata").
# a cor sozinha nunca aparece na fala do canal, entao ela e o gancho confiavel.
PATO = re.compile(r"\bp[ai]t[oa]s?\b|\b(vermelh|amarel)[oa]s?\b", re.I)
prev_end = 0.0
for s in segs:
    st, en, tx = s["start"], s["end"], s["text"].strip()
    if st - prev_end > 1.5:
        print(f"        ~~~ GAP {st-prev_end:.1f}s ({prev_end:.1f}->{st:.1f}) ~~~")
    flags = []
    if PATO.search(tx):
        flags.append("PATO")
    if en - st > 8 and len(tx.split()) < 12:
        flags.append(f"ENGOLIDO? {en-st:.1f}s/{len(tx.split())}pal")
    print(f"[{st:8.2f}-{en:8.2f}] {tx}" + ("   <<< " + " ".join(flags) if flags else ""))
    # vazio escondido dentro do segmento: so aparece nos timestamps de palavra
    pw = None
    for w in s.get("words", []):
        if pw and w["start"] - pw["end"] > 1.5:
            print(f"        !!! GAP-PAL {w['start']-pw['end']:.1f}s ({pw['end']:.1f}->{w['start']:.1f})"
                  f"  ...{pw['word'].strip()} | {w['word'].strip()}...")
        pw = w
    prev_end = en
