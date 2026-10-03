import json,sys
W=[w for s in json.load(open("master.json"))["segments"] for w in s.get("words",[])]
for jan in sys.argv[1:]:
    a,b=map(float,jan.split("-")); print(f"--- {a}-{b}")
    print(" ".join(f"{w['word'].strip()}[{w['start']:.2f}-{w['end']:.2f}]" for w in W if a<=w['start']<=b))
