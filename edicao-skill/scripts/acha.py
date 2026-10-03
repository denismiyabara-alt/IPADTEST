#!/usr/bin/env python3
# ponytail: acha o timestamp de uma frase no FINAL (para sincronizar B-roll)
import json, re, sys, unicodedata
def norm(s):
    s = unicodedata.normalize("NFD", s.lower())
    return re.sub(r"[^a-z0-9 ]", "", "".join(c for c in s if unicodedata.category(c) != "Mn"))
segs = json.load(open("final.json"))["segments"]
alvo = norm(" ".join(sys.argv[1:]))
for s in segs:
    if alvo in norm(s["text"]):
        m = int(s["start"]//60); print(f"{s['start']:8.2f}  ({m}:{s['start']%60:05.2f})  {s['text'].strip()}")
