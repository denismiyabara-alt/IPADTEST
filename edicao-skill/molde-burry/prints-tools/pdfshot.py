# ponytail: print recortado de PDF + bbox do trecho (pdftotext -bbox-layout / pdftoppm -r 130)
# uso: python3 pdfshot.py pdf pagina id "trecho grifo" "texto_topo" "texto_fim" [ocorrencia_grifo]
import sys, subprocess, re, json
from PIL import Image
pdf, page, oid, grifo, top, end = sys.argv[1:7]
occ = int(sys.argv[7]) if len(sys.argv) > 7 else 0
page = int(page); DPI = 130; S = DPI / 72
OUT = "/Users/denal/Downloads/trxf11-cotista-recusou/prints"
xml = subprocess.run(["pdftotext", "-f", str(page), "-l", str(page), "-bbox-layout", pdf, "-"], capture_output=True, text=True).stdout
pw, ph = map(float, re.search(r'<page width="([\d.]+)" height="([\d.]+)"', xml).groups())
words = [(float(a), float(b), float(c), float(d), w) for a, b, c, d, w in
         re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', xml)]

def find(txt, n=0):
    toks = txt.split(); hits = []
    mark = [k for k, s in enumerate(toks) if s.startswith("[") and s.endswith("]")]  # [tok] = so esse entra no bbox
    toks = [s.strip("[]") if k in mark else s for k, s in enumerate(toks)]
    for i in range(len(words) - len(toks) + 1):
        if all(words[i + k][4] == toks[k] for k in range(len(toks))):
            hits.append([words[i + k] for k in (mark or range(len(toks)))])
    if len(hits) <= n: sys.exit(f"NAO ACHOU: {txt!r} (achou {len(hits)})")
    ws = hits[n]; find.ws = ws; return [min(w[0] for w in ws), min(w[1] for w in ws), max(w[2] for w in ws), max(w[3] for w in ws)]

g = find(grifo, occ); gws = find.ws; t, e = find(top), find(end)
pad = 34  # ~2 linhas de contexto; borda puxada pra nao cortar linha no meio
x0, x1 = 30, pw - 30  # largura cheia da coluna
y0, y1 = min(t[1], g[1]) - pad, max(e[3], g[3]) + pad
y0 = max(0, min([y0] + [w[1] - 3 for w in words if w[1] < y0 < w[3]]))
y1 = min(ph, max([y1] + [w[3] + 3 for w in words if w[1] < y1 < w[3]]))
subprocess.run(["pdftoppm", "-r", str(DPI), "-f", str(page), "-l", str(page), "-png", "-singlefile", pdf, f"/tmp/claude-501/pg-trxf"], check=True)
im = Image.open("/tmp/claude-501/pg-trxf.png").crop(tuple(round(v * S) for v in (x0, y0, x1, y1)))
im.save(f"{OUT}/{oid}.png")
W, H = x1 - x0, y1 - y0
bb = [round((g[0] - x0) / W, 4), round((g[1] - y0) / H, 4), round((g[2] - x0) / W, 4), round((g[3] - y0) / H, 4)]
lin = []  # uma caixa por linha do grifo
for w in gws:
    l = next((z for z in lin if abs(z[1] - w[1]) < 3), None)
    if l: l[0] = min(l[0], w[0]); l[2] = max(l[2], w[2]); l[3] = max(l[3], w[3])
    else: lin.append(list(w[:4]))
linhas = [[round((q[0] - x0) / W, 4), round((q[1] - y0) / H, 4), round((q[2] - x0) / W, 4), round((q[3] - y0) / H, 4)] for q in lin]
print(json.dumps({"id": oid, "bbox": bb, "linhas": linhas, "w": im.width, "h": im.height}))
