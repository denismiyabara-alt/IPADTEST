#!/usr/bin/env python3
"""Junta a varredura automática (cache/varredura.json) com a checagem manual (achados_manuais.py) e gera
auditoria-fatos/achados.csv e auditoria-fatos/RELATORIO.md.

Uso: python3 auditoria-fatos/auditar.py tudo && python3 auditoria-fatos/relatorio.py

Da varredura automática entram no CSV só os tipos de alta precisão (marcados [varredura]):
  ticker_parado_antes/depois, ticker_inexistente (sem exceção conhecida), selic_datada, selic_errada, ipca_errado,
  ir_fii_50, lci_90, ir_jcp, div_isento_datado.
Os demais tipos (ticker_empresa por frase, ir_20mil_*, fgc_valor, div_aliquota, div_isento_sem_ressalva, ticker_futuro)
foram revistos à mão: os verdadeiros viraram achado manual; o resto era falso positivo e fica só em cache/varredura.json.
"""
import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

AQUI = Path(__file__).resolve().parent
sys.path.insert(0, str(AQUI))
import achados_manuais as M  # noqa: E402
from auditar import carregar_posts, texto  # noqa: E402

B3 = M.B3_COTAHIST
BCB432 = M.BCB_432
TIPOS_AUTO = {"ticker_parado_antes", "ticker_parado_depois", "ticker_inexistente", "selic_datada", "selic_errada",
              "ipca_errado", "ir_fii_50", "lci_90", "ir_jcp", "div_isento_datado"}
# falsos positivos conferidos à mão (post, valor do trecho)
IGNORAR = {(5057, "METB3"), (5057, "METB4"), (4845, "ITUB11"), (4848, "BBAS4"), (1068, "IMAB11"), (1083, "IMAB11"),
           (2408, "IMAB11"), (1198, "*selic*"), (4846, "*selic*"), (19405, "*selic*"), (3172, "*selic*"),
           (3561, "*selic*"), (3435, "ir_jcp"),
           (7626, "ODPV3"), (19466, "HAAA11"), (1313, "EMBR3"), (4538, "JEPQ39")}  # citam o código antigo/inexistente de propósito
GRAV = {"CRÍTICO": 3, "DATADO": 1, "DÚVIDA": 0.5}


def norm_ws(s):
    s = s.replace(" ", " ")
    s = re.sub(r"\s*\|\s*", " | ", s)
    return re.sub(r"\s+", " ", s).strip()


def main():
    posts = {p["id"]: p for p in carregar_posts() if not p["slug"].startswith("cotacao-")}
    textos = {pid: norm_ws(texto(p["content"]["rendered"]) + " " + texto(p["title"]["rendered"])) for pid, p in posts.items()}
    V = {r["id"]: r for r in json.loads((AQUI / "cache" / "varredura.json").read_text())}

    linhas, problemas_trecho = [], []
    cobertos = defaultdict(set)  # post -> tickers/tipos já cobertos à mão
    for a in M.A:
        pid = a["post_id"]
        t = norm_ws(a["trecho"])
        if t not in textos[pid]:
            problemas_trecho.append((pid, a["trecho"][:80]))
        for tk in re.findall(r"\b[A-Z]{4}\d{1,2}\b", a["trecho"] + " " + a["problema"]):
            cobertos[pid].add(tk)
        if "cotistas" in a["problema"]:
            cobertos[pid].add("ir_fii_50")
        if "LCI" in a["problema"] or "LCA" in a["problema"]:
            cobertos[pid].add("lci_90")
        if "JCP" in a["problema"]:
            cobertos[pid].add("ir_jcp")
        if "Lei 15.270" in a["problema"] or "dividendo" in a["problema"].lower():
            cobertos[pid].add("div_isento_datado")
        linhas.append(dict(post_id=pid, url=posts[pid]["link"], trecho=a["trecho"], problema=a["problema"], classe=a["classe"],
                           correcao_sugerida=a["correcao_sugerida"], fonte=a["fonte"], origem="manual"))

    for pid, r in V.items():
        vistos = set()
        for a in r["achados"]:
            tipo = a["tipo"]
            if tipo not in TIPOS_AUTO or (pid, tipo) in IGNORAR:
                continue
            if tipo.startswith("selic") and (pid, "*selic*") in IGNORAR:
                continue
            if tipo.startswith("ticker"):
                tk = a["trecho"]
                if (pid, tk) in IGNORAR or tk in cobertos[pid] or tk in M.LISTA_RF_EXTRA:
                    continue
            elif tipo in cobertos[pid]:
                continue
            chave = (tipo, a["problema"])
            if chave in vistos:
                continue
            vistos.add(chave)
            classe = a["classe"]
            if classe == "CRÍTICO?":
                classe = "CRÍTICO"
                prob = "[leve] " + a["problema"] if tipo.startswith("ticker") else a["problema"]
            else:
                prob = a["problema"]
            if tipo == "ir_jcp" and r["data"] >= "2026-01-01":
                classe, prob = "CRÍTICO", "JCP a 15% em post de 2026: desde 01/01/2026 é 17,5% (LC 224/2025)"
            fonte = {"selic_datada": BCB432, "selic_errada": BCB432, "ipca_errado": M.BCB_13522, "ir_fii_50": M.L14754,
                     "lci_90": M.CMN5215, "ir_jcp": M.LC224, "div_isento_datado": M.L15270}.get(tipo, B3)
            corr = {"selic_datada": "Tirar a Selic fixa do texto ou datar ('em DD/MM/AAAA, a meta era X%').",
                    "selic_errada": "Conferir a Selic da data na série 432 do BCB.",
                    "ipca_errado": "Tirar o IPCA fixo ou citar o IPCA 12m com mês e fonte.",
                    "ticker_parado_antes": "Trocar pelo código atual ou tirar.",
                    "ticker_parado_depois": "Atualizar o código (mudou ou deixou de negociar depois do post).",
                    "ticker_inexistente": "Conferir o código na B3; se não existir, tirar."}.get(tipo, "Atualizar a regra.")
            linhas.append(dict(post_id=pid, url=r["url"], trecho=a["trecho"][:220], problema="[varredura] " + prob, classe=classe,
                               correcao_sugerida=corr, fonte=fonte, origem="varredura"))

    # CSV
    campos = ["post_id", "url", "trecho", "problema", "classe", "correcao_sugerida", "fonte"]
    linhas.sort(key=lambda l: (-GRAV[l["classe"]], l["post_id"]))
    with open(AQUI / "achados.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos, extrasaction="ignore")
        w.writeheader()
        w.writerows(linhas)

    # por post
    por_post = defaultdict(list)
    for l in linhas:
        por_post[l["post_id"]].append(l)
    resumo = []
    for pid, ls in por_post.items():
        r = V[pid]
        c = Counter(l["classe"] for l in ls)
        grav = sum(GRAV[l["classe"]] for l in ls)
        trafego = r["trafego"]
        resumo.append(dict(pid=pid, r=r, c=c, grav=grav, score=grav * (1 + trafego), pior=max(ls, key=lambda l: GRAV[l["classe"]])["classe"]))
    resumo.sort(key=lambda x: (-GRAV[x["pior"]], -x["score"]))

    # duplicados (título quase igual ou slug -2/-3)
    freq = Counter(w for r in V.values() for w in set(re.findall(r"[a-zà-ú0-9]+", r["titulo"].lower())))

    def palavras(t):
        return set(w for w in re.findall(r"[a-zà-ú0-9]+", t.lower()) if len(w) > 2 and freq[w] <= 8)
    dups = []
    ids = sorted(V)
    for i, a in enumerate(ids):
        for b in ids[i + 1:]:
            pa, pb = palavras(V[a]["titulo"]), palavras(V[b]["titulo"])
            j = len(pa & pb) / max(1, len(pa | pb))
            sa, sb = V[a]["slug"], V[b]["slug"]
            base = re.sub(r"-\d$", "", sa) == re.sub(r"-\d$", "", sb)
            if (j >= 0.8 and len(pa & pb) >= 2) or base:
                dups.append((a, b, round(j, 2)))
    for a, b in M.DUPLICADOS_MANUAIS:
        if not any({a, b} == {x, y} for x, y, _ in dups):
            dups.append((a, b, "conferido"))

    # números do resumo
    n_posts = len(V)
    classes_post = Counter(x["pior"] for x in resumo)
    tem = lambda cl: sum(1 for x in resumo if x["c"][cl])
    ia_alto = [r for r in V.values() if r["ia"]["score"] >= 7]
    faq = sum(1 for r in V.values() if r["ia"]["faq"])
    sem_fonte = sum(1 for r in V.values() if r["ia"]["links_fonte"] == 0 and r["ia"]["numeros"] >= 10)
    recom_tit = [r for r in V.values() if r["recomenda_titulo"]]
    lote_nov24 = [r for r in V.values() if "2024-11-15" <= r["data"] <= "2024-11-16"]
    lote_mai26 = [r for r in V.values() if r["data"] == "2026-05-07"]
    conferidos = set(M.INTEGRAL) | set(M.DIRIGIDA)
    macro_velho = [r for r in lote_mai26 if any(a["tipo"] in ("selic_datada", "ipca_errado") for a in r["achados"])]
    ir_velho = [r for r in lote_mai26 if any(l["classe"] in ("CRÍTICO", "DATADO") and re.search(r"JCP|cotistas|LCI|LCA|15.270", l["problema"]) for l in por_post.get(r["id"], []))]

    md = []
    w = md.append
    w("# Auditoria de erros de fato nos posts do Investir e Coçar")
    w("")
    w("Data: 02/10/2026. Só leitura: posts baixados pela API pública do WordPress (`/wp-json/wp/v2/posts`), 1 req/s, sem login, nada enviado ao site.")
    w("Conferência contra fonte primária já baixada no repositório (`site-ativos/cache`: COTAHIST da B3 2021-2026, DFP/ITR e cadastro da CVM, séries 432/433/13522 do BCB) e leis no Planalto/Receita.")
    w("")
    w("## Resumo")
    w("")
    w(f"- **Posts lidos:** {n_posts} (todos os posts publicados menos os {468 - n_posts} `cotacao-*`, que já são noindex). Todos passaram pela varredura automática.")
    w(f"- **Checagem manual:** {len(conferidos)} posts ({len(M.INTEGRAL)} lidos na íntegra, {len(M.DIRIGIDA)} com leitura dirigida das linhas com números, tickers e regras de IR). Lista no fim.")
    w(f"- **Achados no `achados.csv`:** {len(linhas)} ({sum(1 for l in linhas if l['classe']=='CRÍTICO')} CRÍTICO, {sum(1 for l in linhas if l['classe']=='DATADO')} DATADO, {sum(1 for l in linhas if l['classe']=='DÚVIDA')} DÚVIDA); {sum(1 for l in linhas if l['origem']=='manual')} da checagem manual e {sum(1 for l in linhas if l['origem']=='varredura')} da varredura automática de alta precisão.")
    w(f"- **Posts com pelo menos um CRÍTICO:** {tem('CRÍTICO')}. Com DATADO: {tem('DATADO')}. Com DÚVIDA: {tem('DÚVIDA')}. Posts sem nenhum achado: {n_posts - len(resumo)} (sem achado não quer dizer conferido: veja a lista do que foi checado à mão).")
    w(f"- **Padrões de texto de IA sem revisão:** {len(ia_alto)} posts com pontuação alta (7+) no detector; {faq} com FAQ; {sem_fonte} com 10+ números e nenhum link para fonte primária. Dois lotes concentram o problema: **{len(lote_nov24)} posts publicados em 15-16/11/2024** (tabelas inventadas, tickers que não existem, FAQ repetitivo) e **{len(lote_mai26)} posts publicados em 07/05/2026** (glossário e guias): {len(macro_velho)} deles com Selic/IPCA escritos no texto ('Selic 14,75%, CDI 14,65%, IPCA 5,5%', já velhos no dia da publicação) e {len(ir_velho)} com regra de IR anterior a 2026.")
    w(f"- **Recomendação de compra/venda no título:** {len(recom_tit)} posts ('vale a pena', 'qual comprar', 'melhor ação', 'hora de comprar', 'carteira recomendada').")
    w(f"- **Possíveis duplicados:** {len(dups)} pares (lista abaixo).")
    w("")
    w("**Recomendação:** (1) tirar do ar ou redirecionar já o lote de nov/2024 que tem CRÍTICO (é texto de IA sem revisão: Santander como ITSA4, receita da Itaúsa de R$ 70 bi, BOVA11 'pagando dividendos', ETFs e FIIs que não existem); os destinos estão na tabela. "
      "(2) Corrigir em lote as regras de IR que mudaram: JCP 17,5% desde jan/2026 (LC 224/2025), dividendos acima de R$ 50 mil/mês com 10% na fonte (Lei 15.270/2025), FII com 100 cotistas (Lei 14.754/2023), prazo mínimo de LCI/LCA de 6 meses (Res. CMN 5.215/2025). "
      "(3) Tirar do glossário a Selic/CDI/IPCA escritos no texto (ou trocar por um bloco que leia a série do BCB). "
      "(4) Tirar o JEPQ39 de todos os posts: o produto não existe na B3. "
      "(5) Antes de publicar post de ação/FII/ETF, conferir todo ticker no COTAHIST/cadastro (o `auditar.py` faz isso em segundos).")
    w("")
    w("Gravidade x tráfego: a ordem abaixo usa a pior classe do post e, dentro dela, `soma das classes (CRÍTICO=3, DATADO=1, DÚVIDA=0,5) x (1 + proxy de tráfego)`. "
      "Proxy de tráfego = 2 se está no sitemap (todos os 325 estão) + links internos recebidos (`seo/varredura.csv`) + 3 x páginas do `site-ativos/saida` que linkam o post. "
      "É um proxy fraco: sem Search Console, o desempate real fica para quem tiver os cliques.")
    w("")
    w("## Os 10 piores")
    w("")
    w("| # | Post | Problema principal | Destino |")
    w("|---|---|---|---|")
    for i, x in enumerate([x for x in resumo if x["pior"] == "CRÍTICO"][:10], 1):
        r = x["r"]
        crit = [l for l in por_post[x["pid"]] if l["classe"] == "CRÍTICO"]
        prob = crit[0]["problema"].replace("|", "/")
        d = M.DESTINOS.get(x["pid"], ("corrigir", ""))
        w(f"| {i} | [{x['pid']}]({r['url']}) {r['titulo'][:70]} | {prob[:230]} ({len(crit)} CRÍTICO) | **{d[0]}**. {d[1]} |")
    w("")
    w("## Posts por gravidade x tráfego")
    w("")
    w("Classe = pior achado do post. C/D/? = número de achados CRÍTICO/DATADO/DÚVIDA. Detalhe de cada achado (trecho literal, correção e fonte) no `achados.csv`.")
    w("")
    for cl in ("CRÍTICO", "DATADO", "DÚVIDA"):
        grupo = [x for x in resumo if x["pior"] == cl]
        w(f"### {cl} ({len(grupo)} posts)")
        w("")
        w("| Post | Data | Tráfego | C/D/? | Principal | Destino |" if cl == "CRÍTICO" else "| Post | Data | Tráfego | C/D/? | Principal |")
        w("|---|---|---|---|---|---|" if cl == "CRÍTICO" else "|---|---|---|---|---|")
        for x in grupo:
            r = x["r"]
            top = max(por_post[x["pid"]], key=lambda l: GRAV[l["classe"]])
            prob = top["problema"].replace("|", "/")[:160]
            cdq = f"{x['c']['CRÍTICO']}/{x['c']['DATADO']}/{x['c']['DÚVIDA']}"
            base = f"| [{x['pid']}]({r['url']}) {r['titulo'][:60]} | {r['data']} | {r['trafego']} | {cdq} | {prob} |"
            if cl == "CRÍTICO":
                d = M.DESTINOS.get(x["pid"], ("corrigir", ""))
                base += f" {d[0]} |"
            w(base)
        w("")
    w("## Padrões encontrados")
    w("")
    w(f"1. **Lote de 15-16/11/2024 ({len(lote_nov24)} posts):** texto de IA publicado sem revisão. Frases curtas e repetitivas ('Ela é muito importante', 'Isso ajuda'), tabelas com números redondos e sem fonte, FAQ que repete o texto, e erros grosseiros: Santander como ITSA4, Moreira Salles como acionista da Itaúsa, receita da Itaúsa 9x maior que a real, BOVA11 pagando dividendos, BRTC11/BREN11/BCOM11/BOVD11/XDIV11/AREA11/MASA11 etc. (não existem), 'Empresa XYZ' com 5,8% ao mês. Vários foram revisados depois só na data (modified = 2026-09-01/02) sem mudar o conteúdo.")
    w(f"2. **Lote de 07/05/2026 ({len(lote_mai26)} posts; {len(macro_velho)} com macro velho, {len(ir_velho)} com IR desatualizado):** gerado em lote com macro fixo e velho (Selic 14,75% quando a meta era 14,5%; IPCA 5,5% quando o IPCA 12m era 4,39%) e regras de IR anteriores a 2026 (JCP 15%, dividendo isento sem ressalva, FII com 50 cotistas, LCI/LCA com 90 dias). Mesma estrutura em todos ('Resposta direta', 'Perguntas frequentes', tabela de exemplo).")
    w("3. **Produto inexistente:** JEPQ39 citado como BDR negociável em 8 posts (o 4538 já foi corrigido e diz que não existe). Também BNDW39, DVDY11, BOVA39, NAMO11, XRES11, ALBT34, LVHD34, IFIX11, ABNB34, CSDE3, BKCH11.")
    w("4. **Ticker que já tinha mudado na data do post:** TRPL4 (ISAE4 desde nov/2024), ARZZ3 (AZZA3), BCFF11 e MALL11 (encerrados), URET11, ENBR3, VIVT4.")
    w("5. **Regra de IR que mudou e o texto não acompanhou:** JCP 15% -> 17,5% (LC 224/2025), dividendos com IRRF de 10% acima de R$ 50 mil/mês (Lei 15.270/2025), 50 -> 100 cotistas (Lei 14.754/2023), prazo de LCI/LCA (Res. CMN 5.119, 5.154 e 5.215). Também há erro de regra que nunca foi verdade: LCI/LCA com IR, Tesouro isento, CDB a 27,5%, FII com ganho de 15% a 22,5%, tag along de 100% para ON, dividendo de BDR isento.")
    w("6. **Contradições entre posts do próprio site:** taxa do BOVA11 (0,10% x 0,30%), DY do Itaú em 2025 (3,1% x 12,1%), frequência de dividendos da Itaúsa (trimestral x semestral x 'mensal'), fatia na Aegea (13,27% x 14,0%). Os posts reescritos em set/2026 (993, 1028, 1053, 4538, 19466) estão certos e com fonte: servem de destino de 301 e de modelo.")
    w("7. **Recomendação de compra/venda:** títulos com 'vale a pena', 'qual comprar', 'melhor ação' e CTAs de 'ações para comprar agora'; posts do lote de 2024 com 'recomendação ITSA4 é positiva' e corretoras citadas pelo nome (1013, 1108, 4875).")
    w("8. **Duplicados:** mesmo assunto publicado mais de uma vez (abaixo); juntar com 301 para o mais completo.")
    w("")
    w("### Possíveis duplicados")
    w("")
    w("| Post A | Post B | Semelhança do título |")
    w("|---|---|---|")
    for a, b, j in dups:
        w(f"| [{a}]({V[a]['url']}) {V[a]['titulo'][:55]} | [{b}]({V[b]['url']}) {V[b]['titulo'][:55]} | {j} |")
    w("")
    w("### Recomendação de compra/venda no título")
    w("")
    w(", ".join(f"[{r['id']}]({r['url']})" for r in sorted(recom_tit, key=lambda r: r["id"])))
    w("")
    w("## O que foi checado a fundo e o que só passou pela varredura")
    w("")
    w(f"- **Leitura integral ({len(M.INTEGRAL)}):** " + ", ".join(str(i) for i in M.INTEGRAL) + ".")
    w(f"- **Leitura dirigida ({len(M.DIRIGIDA)}):** " + ", ".join(str(i) for i in M.DIRIGIDA) + ".")
    w("- **Notas de posts conferidos sem achado ou com achado pequeno:**")
    for pid, n in M.NOTAS_CONFERIDOS.items():
        w(f"  - {pid}: {n}")
    so_varr = sorted(set(V) - conferidos)
    w(f"- **Só varredura automática ({len(so_varr)}):** " + ", ".join(str(i) for i in so_varr) + ".")
    w("")
    w("A varredura automática (todos os posts) confere: ticker contra o COTAHIST à vista 2021-2026 (existe? parou de negociar antes/depois do post?), "
      "ticker colado ao nome de outra empresa, Selic citada contra a meta (SGS 432) na data do post, IPCA citado contra o IPCA 12m (SGS 13522), "
      "e frases de IR contra a tabela de regras de `referencia.py` (JCP, 50 cotistas, carência de LCI/LCA, isenção de R$ 20 mil, come-cotas, FGC). "
      "Ela não confere números de balanço, dividendos por ação, datas com, valuation nem notícias: isso só nos posts da checagem manual.")
    w("")
    w("Limitações: o COTAHIST não traz ETFs de renda fixa (IMAB11, B5P211...), por isso eles ficam fora da regra de 'ticker inexistente'; "
      "o prospecto do JEPI39 e alguns portais de notícia estão bloqueados pela rede do ambiente (não contornado), por isso o público-alvo do JEPI39 ficou como DÚVIDA; "
      "proventos por ação não estão no SQLite do site-ativos (tabela `provento` vazia), então DY e valores por ação dos posts não foram recalculados.")
    w("")
    w("## Reproduzir")
    w("")
    w("```sh")
    w("python3 auditoria-fatos/auditar.py tudo     # baixa os posts (cache/) e roda a varredura -> cache/varredura.json")
    w("python3 auditoria-fatos/relatorio.py        # junta com achados_manuais.py -> achados.csv e RELATORIO.md")
    w("python3 auditoria-fatos/dfp.py 61532644000115 3.01 3.11   # consulta DFP da CVM já baixada (ex.: Itaúsa)")
    w("```")
    w("")
    w("Arquivos: `auditar.py` (download e extração), `varredura.py` (checagens automáticas), `referencia.py` (apelidos de empresas e regras de IR com fonte), "
      "`achados_manuais.py` (o que foi conferido à mão, com fonte e destino), `relatorio.py` (este relatório), `dfp.py` (consulta às DFPs). Cache em `auditoria-fatos/cache/` (fora do git).")
    if problemas_trecho:
        w("")
        w("## Aviso: trechos que não bateram literalmente com o texto do post")
        for pid, t in problemas_trecho:
            w(f"- {pid}: {t}")
    (AQUI / "RELATORIO.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"{len(linhas)} achados; {len(resumo)} posts com achado; trechos sem match: {len(problemas_trecho)}")
    for p in problemas_trecho:
        print("  sem match:", p)


if __name__ == "__main__":
    main()
