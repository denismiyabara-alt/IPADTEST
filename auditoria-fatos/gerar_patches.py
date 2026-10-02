#!/usr/bin/env python3
"""Valida os patches escritos em patches_fonte.py contra o content.rendered em cache e grava
patches/<post_id>.json e patches/LOTE_<X>.json.

Uso: python3 auditoria-fatos/gerar_patches.py [A|B|C ...]   (sem argumento: todos os lotes)

Regras checadas para cada troca:
- o "de" é um trecho seguro (patchlib.problemas_do_de): sem aspas, travessões, reticências, &, <, >, quebras;
- o "de" está dentro de UM nó de texto do rendered e aparece 1 vez no texto visível; se aparecer de novo só dentro de
  <script> (FAQ em JSON-LD no próprio post), a troca leva "n" = total e troca todas;
- o "para" não tem aspas duplas, barra invertida nem quebra (não quebra o JSON-LD);
- aplicando as trocas em sequência, cada "de" mantém a contagem esperada.
"""
import html
import json
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
from auditar import carregar_posts  # noqa: E402
from patchlib import alternativas, localizar_no_rendered, problemas_do_de  # noqa: E402
import patches_fonte as F  # noqa: E402

SAIDA = AQUI / "patches"


def sem_scripts(h):
    return re.sub(r"(?is)<script[^>]*>.*?</script>", " ", h)


def validar(pid, item, rendered):
    erros, trocas = [], []
    txt_total = html.unescape(rendered)
    txt_visivel = html.unescape(sem_scripts(rendered))
    simulado = txt_total
    for de, para in item["trocas"]:
        p = problemas_do_de(de)
        if p:
            erros.append(f"de inseguro ({'; '.join(p)}): {de[:80]}")
            continue
        if re.search(r'["\\\n]', para):
            erros.append(f"para com aspas/barra/quebra: {para[:80]}")
        vis = txt_visivel.count(de)
        tot = txt_total.count(de)
        if vis != 1:
            erros.append(f"de aparece {vis}x no texto visível: {de[:80]}")
            continue
        n_tot, de_r = localizar_no_rendered(rendered, de)
        if de_r is None:
            erros.append(f"de cruza tags (não está num nó de texto): {de[:80]}")
            continue
        if simulado.count(de) != tot:
            erros.append(f"de alterado por troca anterior: {de[:80]}")
            continue
        simulado = simulado.replace(de, para)
        t = {"de": de, "para": para, "de_rendered": de_r}
        if tot != 1:
            t["n"] = tot
        if alternativas(de):
            t["alternativas"] = alternativas(de)
        trocas.append(t)
    return erros, trocas


def main(lotes):
    posts = {p["id"]: p for p in carregar_posts()}
    SAIDA.mkdir(exist_ok=True)
    total_erros = 0
    for lote in lotes:
        ids = F.LOTES[lote]
        n_trocas = 0
        for pid in ids:
            item = F.PATCHES[pid]
            erros, trocas = validar(pid, item, posts[pid]["content"]["rendered"])
            if erros:
                total_erros += len(erros)
                print(f"post {pid}:")
                for e in erros:
                    print("   ", e)
                continue
            dados = {"post_id": pid, "url": posts[pid]["link"], "lote": lote, "motivo": item["motivo"],
                     "trocas": trocas, "fonte": item["fonte"]}
            if item.get("manual"):
                dados["manual"] = item["manual"]
            (SAIDA / f"{pid}.json").write_text(json.dumps(dados, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
            n_trocas += len(trocas)
        (SAIDA / f"LOTE_{lote}.json").write_text(json.dumps(
            {"lote": lote, "descricao": F.DESCRICAO[lote], "post_ids": ids}, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"lote {lote}: {len(ids)} posts, {n_trocas} trocas")
    if total_erros:
        raise SystemExit(f"{total_erros} erros")


if __name__ == "__main__":
    main(sys.argv[1:] or list(F.LOTES))
