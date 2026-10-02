"""Gera posts-para-refresh.csv: posts antigos linkados pelas páginas do MVP com título a revisar.

Fonte: a mesma do build (gerar.posts_do_canal, que lê seo/varredura.csv) e os tickers de cache/selecao.json.
Critério: título com "vale a pena", "melhor"/"melhores" ou nome de corretora; entram também, marcados como
"extra", títulos com outros termos da regra 7.1 ("comprar", "oportunidade").
Os títulos sugeridos são escritos à mão (SUGESTOES) depois de ler o post salvo em seo/_html; post novo sem
sugestão sai com "PENDENTE".

    python3 scripts/posts_para_refresh.py
"""
import csv
import json
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ))
from iec_ativos import config, gerar, seo  # noqa: E402

TERMOS = [("vale a pena", r"vale a pena"), ("melhor", r"\bmelhor(es)?\b")]
EXTRAS = [("extra: comprar (regra 7.1)", r"\bcomprar\b"), ("extra: oportunidade (regra 7.1)", r"oportunidade")]
CORRETORAS = seo.CORRETORAS + [r"\bBTG\b", r"\bXP\b"]

# url (sem domínio) -> (título sugerido, palavra-chave principal, datado?, observação). Escritos depois de ler
# o texto salvo em seo/_html (títulos, intertítulos e abertura de cada post).
SUGESTOES = {
    "/petr4-65-por-cento-lucro-estatais-vale-a-pena-investir/":
        ("PETR4: Petrobras concentra 65% do lucro das estatais", "PETR4",
         "talvez: números de 2025 e tensão Irã x EUA de jul/2026; revisar após o próximo balanço",
         "intertítulos também usam 'vale a pena' e 'PETR4 x CDB: qual rende mais'; URL tem 'vale-a-pena' (manter, ou 301)"),
    "/vale3-cobre-ia-vale-a-pena-investir/":
        ("VALE3 em 2026: cobre, IA e o motivo da alta da ação", "VALE3",
         "sim: alta de 50,6% em 12 meses e queda de julho/2026 no texto",
         "intertítulos com 'é hora de vender?' e 'o preço está caro?' (regra 7.1); URL tem 'vale-a-pena'"),
    "/vale3-dividendos-prejuizo-e-oportunidades-de-investimento/":
        ("VALE3 no 4T24: prejuízo contábil e dividendos da Vale", "VALE3 dividendos",
         "sim: post de fev/2025 sobre o 4T24; atualizar com resultado recente ou deixar claro que é histórico",
         "texto cita bancos recomendando compra e a corretora; intertítulo 'Vale a pena investir?'"),
    "/itub3-ou-itub4-qual-e-melhor/":
        ("ITUB3 ou ITUB4: diferenças entre a ação ON e a PN", "ITUB3 ou ITUB4", "não",
         "mesmo tema de /itub3-ou-itub4-qual-comprar/ (publicados com horas de diferença): juntar os dois e 301; "
         "a 'resposta direta' do texto aponta uma das ações (recomendação)"),
    "/itub3-ou-itub4-qual-comprar/":
        ("ITUB3 x ITUB4: liquidez, voto e dividendos do Itaú", "ITUB3 x ITUB4",
         "não pelo conteúdo; o ano 2026 do título pode sair",
         "mesmo tema de /itub3-ou-itub4-qual-e-melhor/: juntar os dois e 301; texto diz qual comprar (recomendação)"),
    "/itsa4-ou-itub4-qual-a-melhor-acao-para-investir/":
        ("ITSA4 ou ITUB4: diferenças entre Itaúsa e Itaú Unibanco", "ITSA4 ou ITUB4",
         "sim: post de nov/2024 com indicadores da época",
         "ERRO no texto: chama ITSA4 de 'Banco Santander Brasil' (ITSA4 é a Itaúsa); corrigir antes do título"),
    "/banco-do-brasil-bbas3-corte-dividendo-payout-2026/":
        ("BBAS3: corte do payout de 45% para 30% e os dividendos", "BBAS3 dividendos",
         "sim: lucro e payout de jul/2026; atualizar a cada resultado",
         "intertítulo 'Vale a pena continuar com BBAS3'; título atual tem 2026"),
    "/bbas3-roe-abaixo-selic-banco-do-brasil-dividendos-2026/":
        ("BBAS3 no 1T26: ROE do Banco do Brasil abaixo da Selic", "BBAS3 ROE",
         "sim: ROE de 7,3% do 1T26; atualizar com o último trimestre",
         "o título atual se repete 4 vezes no topo do texto; FAQ 'devo vender BBAS3?' (regra 7.1)"),
    "/ambev-abev3-volta-carteira-btg-13-anos/":
        ("ABEV3: ROIC de 31% e o que mudou na Ambev em 13 anos", "ABEV3",
         "sim: escrito antes do resultado do 2T26",
         "o post inteiro gira em torno da recomendação de uma corretora (nome no título, na URL e no texto); "
         "reescrever sem ela ou tirar o link da página de ABEV3"),
    "/trxf11-faria-lima-dos-galpoes-vale-o-hype/":
        ("TRXF11: o galpão de R$ 1,43 bilhão em Guarulhos", "TRXF11",
         "sim: yield de 12,89% de jul/2026 no texto",
         "intertítulos com 'vale mais a pena que renda fixa?' e 'boa entrada'"),
    "/kncr11-subscricao-vale-a-pena/":
        ("KNCR11: 12ª emissão de cotas a R$ 103,54", "KNCR11 emissão",
         "sim: emissão de out/2025, já encerrada; dizer no topo que é histórico ou atualizar",
         "intertítulo 'Preço atrativo: uma oportunidade?' (regra 7.1)"),
}

ANO = re.compile(r"\b20\d\d\b")
SEO_HTML = config.SEO_VARREDURA.with_name("_html")


def motivos(titulo: str) -> list[str]:
    m = [nome for nome, pat in TERMOS if re.search(pat, titulo, re.I)]
    if any(re.search(p, titulo) for p in CORRETORAS):
        m.append("nome de corretora")
    if m:
        return m
    return [nome for nome, pat in EXTRAS if re.search(pat, titulo, re.I)]


def main():
    sel = json.loads((config.CACHE / "selecao.json").read_text())
    tickers = [a["ticker"] for a in sel["acoes"]] + [a["ticker"] for a in sel["fiis"]]
    posts: dict[str, dict] = {}
    for t in tickers:
        for p in gerar.posts_do_canal(t):
            posts.setdefault(p["url"], {"titulo": p["titulo"], "ativos": []})["ativos"].append(t)
    linhas = []
    for url, p in posts.items():
        mot = motivos(p["titulo"])
        if not mot:
            continue
        caminho = re.sub(r"^https?://[^/]+", "", url)
        sug, chave, datado, obs = SUGESTOES.get(caminho, ("PENDENTE", "", "", "post novo: escrever sugestão"))
        anos = sorted(set(ANO.findall(p["titulo"])))
        salvo = SEO_HTML / (caminho.strip("/") + ".html")
        pub = re.search(r'article:published_time" content="(\d{4}-\d\d-\d\d)', salvo.read_text(errors="ignore")) \
            if salvo.exists() else None
        linhas.append({"url": url, "titulo_atual": p["titulo"], "motivo": "; ".join(mot),
                       "ativos_que_linkam": " ".join(p["ativos"]), "titulo_sugerido": sug,
                       "caracteres_sugerido": len(sug), "palavra_chave_principal": chave,
                       "publicado_em": pub.group(1) if pub else "",
                       "ano_no_titulo": " ".join(anos) or "não",
                       "datado_atualizar_conteudo": datado or "conferir conteúdo",
                       "base_da_sugestao": "texto salvo em seo/_html" if salvo.exists() else "título e URL (conferir conteúdo)",
                       "observacao": obs})
    destino = RAIZ / "posts-para-refresh.csv"
    with open(destino, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas[0]))
        w.writeheader()
        w.writerows(linhas)
    print(f"{len(linhas)} posts em {destino.name} (de {len(posts)} posts linkados)")


if __name__ == "__main__":
    main()
