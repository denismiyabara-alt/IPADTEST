"""Baixa as imagens da licencas-ep01.csv para <episodio>/imagens/. Nada entra no video sem linha na planilha.
    python3 baixar_imagens.py ep01-eichmann
Commons: pela API (imageinfo; .djvu sai como JPG da pagina 1; .ogv vira .mp4 sem audio via ffmpeg).
NARA: pela URL da pagina (medialz) listada em PAGINAS_NARA. Linha REC- = reconstituicao, nao baixa nada.
Depois de baixar: abrir a pagina de cada item, conferir a licenca e o selo dos EUA e salvar o print em prints/.
"""
import csv, json, os, subprocess, sys, time, urllib.parse, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
UA = {"User-Agent": "doc-licencas/0.1 (baixar_imagens.py)"}
PAGINAS_NARA = {   # arquivo -> URL da pagina escaneada (CONFERIR NO MAC a do memorando de 1958)
    "cia-memo-dulles-1953.jpg": "https://catalog.archives.gov/medialz/dc-metro/rg-263/640446/640446_Box31_Folder2/640446_Box31_Folder2-0012.jpg",
    "cia-memo-1958-clemens.jpg": None,
}


def _get(url, tent=5):
    for k in range(tent):
        try:
            return urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=90).read()
        except Exception as e:               # 429 do Commons: espera e tenta de novo
            print(f"    tentativa {k + 1}: {e}")
            time.sleep(15 * (k + 1))
    raise RuntimeError(f"nao baixou: {url}")


def commons(url_pagina):
    titulo = urllib.parse.unquote(url_pagina.split("/wiki/", 1)[1]).replace("_", " ")
    q = {"action": "query", "prop": "imageinfo", "iiprop": "url", "titles": titulo, "format": "json"}
    if titulo.lower().endswith((".djvu", ".pdf")):
        q.update(iiurlwidth="2400", iiurlparam="page1-2400px")
    d = json.loads(_get("https://commons.wikimedia.org/w/api.php?" + urllib.parse.urlencode(q)))
    ii = next(iter(d["query"]["pages"].values()))["imageinfo"][0]
    return ii.get("thumburl") or ii["url"]


def main(ep):
    destino = os.path.join(AQUI, ep, "imagens")
    os.makedirs(destino, exist_ok=True)
    for row in csv.DictReader(open(os.path.join(AQUI, "licencas-ep01.csv"), encoding="utf-8")):
        a, url = row["arquivo"], row["url_do_item"]
        if a.startswith("REC-") or os.path.exists(os.path.join(destino, a)):
            continue
        print(a)
        try:
            if "commons.wikimedia.org" in url:
                fonte = commons(url)
            elif a in PAGINAS_NARA:
                fonte = PAGINAS_NARA[a]
            else:
                fonte = None
            if not fonte:
                print("    PULADO: sem URL de arquivo (CONFERIR NO MAC; ver base_legal na planilha)")
                continue
            dados = _get(fonte)
            if a.endswith(".mp4") and fonte.endswith(".ogv"):
                open("/tmp/_esp.ogv", "wb").write(dados)
                subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", "/tmp/_esp.ogv", "-an", "-c:v", "libx264",
                                "-pix_fmt", "yuv420p", os.path.join(destino, a)], check=True)
            else:
                open(os.path.join(destino, a), "wb").write(dados)
            time.sleep(3)
        except Exception as e:
            print(f"    FALHOU: {e}")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "ep01-eichmann")
