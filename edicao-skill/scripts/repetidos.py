#!/usr/bin/env python3
# ponytail: acha repeticao sem marcador — mesma sequencia de 5 palavras dita 2x em ate 90s
import json, re, sys
from collections import defaultdict
segs = json.load(open(sys.argv[1] if len(sys.argv)>1 else "render03.json"))["segments"]
words = [(w["start"], re.sub(r"\W+","",w["word"]).lower())
         for s in segs for w in s.get("words",[]) if re.sub(r"\W+","",w["word"])]
seen = defaultdict(list)
for i in range(len(words)-4):
    key = " ".join(w for _, w in words[i:i+5])
    seen[key].append(words[i][0])
for key, ts in seen.items():
    for a, b in zip(ts, ts[1:]):
        if b - a < 90:
            print(f"{a:8.2f} -> {b:8.2f} ({b-a:5.1f}s)  \"{key}\"")
