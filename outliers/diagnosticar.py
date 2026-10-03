#!/usr/bin/env python3
"""DIAGNÓSTICO: por que o outlier estourou e se o canal do Denis já fez algo parecido.

Tudo por regra (sem LLM):
- tema: nicho (detectar.py), tickers do título e as entidades de ENTIDADES (CVM, Copom, Tesouro IPCA+...);
- ângulo: o enquadramento do título (veredito/alerta, pergunta, conta/número, lista, relato pessoal, comparação,
  explicação), pela primeira regra de ANGULOS que casar;
- gancho do título: caixa alta, número, pergunta, palavra de tensão e tamanho;
- timing: título/descrição com cara de evento (config "noticia") e a idade do vídeo; "data_evento" do radar, se vier,
  manda no prazo. Notícia quente = evento + até prazo_h (48 h) desde a publicação (ou desde o evento);
- parecidos no canal do Denis: auditoria-canal/dados/videos.csv por similaridade de título (cosseno de conjuntos de
  palavras, ticker com peso 3, entidade com peso 2), com views intencionais (engagedViews) e inscritos
  (subscribersGained) do analytics_por_video.csv.

uso: python3 diagnosticar.py [--entrada radar] [--agora ...]   (roda o detectar.py e imprime o diagnóstico)
"""
from __future__ import annotations

import argparse
import csv
import json
import math
import re
import sys
from datetime import timedelta

import comum as c

# (regex sem acento, rótulo curto para título, dado-chave a conferir, fonte primária)
ENTIDADES = [
    (r"parecer|\bcvm\b", "o parecer da CVM", "o que o texto do parecer permite e proíbe, e a data de vigência",
     "texto do parecer no site da CVM (gov.br/cvm), não o resumo de quem comentou"),
    (r"copom|selic", "a Selic", "a decisão e o comunicado do Copom (taxa, votação e a frase sobre os próximos passos)",
     "comunicado e ata do Copom em bcb.gov.br; série SGS 432 para a Selic na data"),
    (r"ipca\+|ipca \+|tesouro ipca|\bntn-?b", "o Tesouro IPCA+", "a taxa real do título na data e o preço unitário",
     "taxas e preços do Tesouro Direto (tesourodireto.com.br, histórico de preços e taxas)"),
    (r"tesouro selic|tesouro prefixado|tesouro direto|\btesouro\b", "o Tesouro Direto",
     "a taxa do título na data", "tesourodireto.com.br (preços e taxas do dia)"),
    (r"\blci\b|\blca\b|\bcdb\b|\bcdi\b|renda fixa", "a renda fixa", "a taxa líquida de imposto no prazo",
     "tabela regressiva de IR (Lei 11.033/2004) e a taxa CDI do dia (SGS 4389)"),
    (r"imposto|\bir\b|tributa|isenc|isento", "o imposto", "a regra vigente e a alíquota, com a data",
     "a lei em planalto.gov.br e a página da Receita Federal sobre o tema"),
    (r"ipca|inflacao", "a inflação", "o IPCA de 12 meses na data", "IBGE / SGS 13522"),
    (r"etf", "o ETF", "taxa de administração, rendimento distribuído e retorno total",
     "regulamento e informe do ETF na B3 e no site da gestora"),
    (r"dividendo|provento|\bjcp\b|\bdy\b", "os dividendos", "o valor por ação/cota, a data-com e o pagamento",
     "aviso aos acionistas / fato relevante (rad.cvm.gov.br) e o RI da empresa"),
    (r"fundos? imobiliari|\bfiis?\b|\bifix\b", "os fundos imobiliários", "rendimento por cota, P/VP e vacância",
     "relatório gerencial e informe mensal do fundo (fnet.b3.com.br) e o IFIX na B3"),
    (r"bolsa|ibovespa", "a bolsa", "o Ibovespa na data e o fluxo estrangeiro", "B3 (índices e fluxo de investidores)"),
]

ANGULOS = [
    ("comparação", r"\bvs\.?\b|versus| ou (o |a )?\w+\?|qual (e )?(o|a) melhor|melhor que", "dois caminhos lado a lado"),
    ("veredito/alerta", r"acabou|cuidado|alerta|atencao|urgente|nunca|ultima chance|armadilha|perig|fim d|assustador|"
                        r"despenc|desab|colaps|quebr|risco", "fecha a questão e cria urgência"),
    ("relato pessoal", r"\bvendi\b|\bcomprei\b|\bminha\b|\bmeus?\b|\beu\b|recebi|ganhei|perdi|estou comprando",
     "decisão de alguém de carne e osso, com o próprio dinheiro"),
    ("lista", r"^\d+\s|\b\d+ (acoes|fiis|fundos|motivos|erros|dicas|regras|ativos)", "promete um recorte enxuto"),
    ("conta/número", r"r\$|\d+ ?%|\bquanto\b|\d+ mil|bilh|milh", "número concreto no título"),
    ("pergunta", r"\?", "abre uma dúvida que o espectador já tem"),
    ("explicação", r"o que (e|muda|diz)|entenda|explica|como funciona|por que", "explica um fato"),
]

TENSAO = r"acabou|cuidado|alerta|urgente|nunca|segredo|verdade|ninguem|assustador|choc|absurd|despenc|explod|dispar|"\
         r"farra|armadilha|ultima|perig|risco|erro|quebr"

STOP = set("a o os as de da do das dos e em no na nos nas um uma uns umas que para pra por com sem se seu sua seus suas "
           "ao aos mais menos como ja nao sim e ou the of to and is it voce voces isso esse essa este esta ta "
           "vai vao pode quando onde qual quais quem hoje agora tudo todo toda ser foi sao".split())


def palavras(t):
    return [w for w in re.findall(r"[a-z0-9+]+", c.norm(t)) if len(w) > 2 and w not in STOP]


def entidades(texto):
    t = c.norm(texto)
    return [e for e in ENTIDADES if re.search(e[0], t)]


def vetor(titulo):
    v = {w: 1.0 for w in palavras(titulo)}
    for tk in c.tickers(titulo):
        v["$" + tk] = 3.0
    for e in entidades(titulo):
        v["#" + e[1]] = 2.0
    return v


def similaridade(a, b):
    va, vb = vetor(a), vetor(b)
    if not va or not vb:
        return 0.0
    dot = sum(va[k] * vb[k] for k in va.keys() & vb.keys())
    return dot / (math.sqrt(sum(x * x for x in va.values())) * math.sqrt(sum(x * x for x in vb.values())))


# ------------------------------------------------------------------------------------------------ canal do Denis
def _int(s):
    try:
        return int(float(s))
    except (TypeError, ValueError):
        return None


def carregar_denis(cfg):
    cam = cfg.get("caminhos") or {}
    vp, ap_ = c.caminho(cam.get("videos_denis")), c.caminho(cam.get("analytics_denis"))
    an = {}
    if ap_ and ap_.is_file():
        with open(ap_, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                an[r["video_id"]] = r
    out = []
    if vp and vp.is_file():
        with open(vp, encoding="utf-8") as f:
            for r in csv.DictReader(f):
                a = an.get(r["id"], {})
                out.append({"video_id": r["id"], "titulo": r.get("titulo", ""), "formato": r.get("formato", ""),
                            "publicado": (r.get("publicado_em_brt") or "")[:10], "views": _int(r.get("views")),
                            "views_intencionais": _int(a.get("engagedViews")),
                            "inscritos": _int(a.get("subscribersGained"))})
    return out


def parecidos(titulo, denis, limiar=0.25, n=3, formato=None):
    """Mesmo formato quando ele é conhecido (Short antigo com 1 inscrito não diz nada sobre um longo)."""
    base = [v for v in denis if not formato or v["formato"] == formato] or denis
    cands = [(similaridade(titulo, v["titulo"]), v) for v in base]
    cands = [(s, v) for s, v in cands if s >= limiar]
    cands.sort(key=lambda x: (-x[0], -(x[1]["inscritos"] or 0)))
    return [{**v, "similaridade": round(s, 2), "url": f"https://youtu.be/{v['video_id']}"} for s, v in cands[:n]]


# ------------------------------------------------------------------------------------------------ diagnóstico
def gancho(titulo):
    t = titulo or ""
    letras = [ch for ch in t if ch.isalpha()]
    caixa = sum(ch.isupper() for ch in letras) / len(letras) if letras else 0
    traços = []
    if caixa > 0.6:
        traços.append("título em caixa alta")
    if re.search(r"\d", t):
        traços.append("número no título")
    if "?" in t:
        traços.append("pergunta")
    m = re.search(TENSAO, c.norm(t))
    if m:
        traços.append(f'palavra de tensão ("{m.group(0)}")')
    if c.tickers(t):
        traços.append("ticker nomeado (" + ", ".join(c.tickers(t)) + ")")
    traços.append(f"{len(t)} caracteres")
    return traços


def angulo(titulo):
    t = c.norm(titulo)
    for nome, rx, porque in ANGULOS:
        if re.search(rx, t):
            return {"tipo": nome, "porque": porque}
    return {"tipo": "afirmação", "porque": "afirma um fato sem enquadramento forte"}


def timing(o, cfg, agora):
    nc = cfg.get("noticia") or {}
    texto = c.norm(f"{o.get('titulo')} {o.get('descricao') or ''}")
    m = re.search(nc.get("regex", "$^"), c.norm(o.get("titulo"))) or re.search(nc.get("regex", "$^"), texto)
    pub = c.ler_data(o.get("publicado"))
    ev = c.ler_data(o.get("data_evento"))
    inicio = ev or pub
    prazo = (inicio + timedelta(hours=float(nc.get("prazo_h", 48)))) if inicio else None
    quente = bool(m) and prazo is not None and agora <= prazo
    return {"evento": m.group(0) if m else None, "data_evento": o.get("data_evento"), "quente": quente,
            "prazo_ate": c.iso(prazo) if prazo else None}


def diagnosticar(o, denis, cfg, agora):
    sim = cfg.get("similaridade") or {}
    ents = entidades(f"{o.get('titulo')} {o.get('descricao') or ''}")
    ang = angulo(o.get("titulo"))
    tm = timing(o, cfg, agora)
    par = parecidos(o.get("titulo"), denis, sim.get("limiar", 0.25), sim.get("max_parecidos", 3), o.get("formato"))
    porque = [f"tema de {o.get('nicho')}" + (f" com {', '.join(c.tickers(o.get('titulo')))}" if c.tickers(o.get('titulo')) else "")
              + (f" e {ents[0][1]}" if ents else ""),
              f"ângulo de {ang['tipo']}: {ang['porque']}",
              "gancho: " + "; ".join(gancho(o.get("titulo")))]
    if tm["evento"]:
        porque.append(f"timing de notícia (\"{tm['evento']}\")" + (", ainda quente" if tm["quente"] else ", já esfriou"))
    return {"tema": {"nicho": o.get("nicho"), "tickers": c.tickers(o.get("titulo")),
                     "entidades": [e[1] for e in ents]},
            "angulo": ang, "gancho": gancho(o.get("titulo")), "timing": tm, "por_que_estourou": porque,
            "parecidos_no_canal": par, "_entidades": ents}


def main(argv=None):
    import detectar
    from datetime import datetime, timezone
    ap = argparse.ArgumentParser(description="Diagnóstico dos outliers detectados.")
    ap.add_argument("--config")
    ap.add_argument("--entrada")
    ap.add_argument("--agora")
    a = ap.parse_args(argv)
    cfg = c.carregar_config(a.config)
    agora = c.ler_data(a.agora) if a.agora else datetime.now(timezone.utc)
    r = detectar.detectar(cfg, a.entrada, agora)
    denis = carregar_denis(cfg)
    for o in r["outliers"]:
        d = diagnosticar(o, denis, cfg, agora)
        d.pop("_entidades")
        print(json.dumps({"outlier": o["titulo"], **d}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
