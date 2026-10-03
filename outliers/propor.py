#!/usr/bin/env python3
"""PROPOSTA: para cada outlier, o ângulo do Denis (AMPLIANDO o outlier, sem contradizer), 3 títulos de até 60
caracteres que passam no gate, o gancho na voz do canal, o dado-chave com a fonte primária e o ENCAIXE no calendário.

Sem LLM: tudo sai de regras e modelos de texto a partir do diagnóstico. Ângulo, títulos e gancho são RASCUNHO e o
card diz isso. O que é dado (múltiplo, views, vaga, inscritos esperados) vem dos arquivos.

Encaixe:
- notícia quente (evento + até 48 h): Short rápido, gravar até o prazo; o calendário não muda;
- senão: a vaga do CALENDARIO.csv de MENOR inscritos_esperados nas próximas `semanas` semanas (a partir de amanhã),
  no mesmo formato do outlier; NUNCA um episódio da série (serie_ep preenchida) nem o Copom (calendario.protegidas_regex
  em origem, título ou ângulo), nem uma vaga que já recebeu troca (trocas.json).

Grava outliers/saida/propostas.json (lido pelo encaixar.py, pelo entregar.py e pelo resumo da manhã) e propostas.md.

uso:
  python3 propor.py [--entrada radar] [--agora 2026-10-05T08:00] [--hoje 2026-10-05] [--sem-modelo] [--saida dir]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

import comum as c
import detectar
import diagnosticar as dg

RASCUNHO = "RASCUNHO (gerado por regra, sem LLM: revisar antes de usar)"
LIMITE_TITULO = 60

TEMA_TITULO = {"o parecer da CVM": "Parecer da CVM", "a Selic": "Selic", "o Tesouro IPCA+": "Tesouro IPCA+",
               "o Tesouro Direto": "Tesouro Direto", "a renda fixa": "Renda fixa", "o imposto": "Imposto",
               "a inflação": "Inflação", "o ETF": "ETF", "os dividendos": "Dividendos",
               "os fundos imobiliários": "Fundos imobiliários", "a bolsa": "Bolsa"}
NICHO_TEMA = {"FII": "Fundos imobiliários", "renda mensal": "Renda mensal", "Tesouro e renda fixa": "Tesouro Direto",
              "ações": "Ações", "investimento geral": "Investimentos"}
EMPRESAS = {"cemig": "Cemig", "petrobras": "Petrobras", "vale": "Vale", "itau": "Itaú", "bradesco": "Bradesco",
            "banco do brasil": "Banco do Brasil", "santander": "Santander", "taesa": "Taesa", "klabin": "Klabin",
            "sanepar": "Sanepar", "eletrobras": "Eletrobras", "weg": "WEG", "ambev": "Ambev", "copel": "Copel",
            "isa cteep": "ISA CTEEP", "bb seguridade": "BB Seguridade", "caixa seguridade": "Caixa Seguridade"}
ONDE_ENTIDADE = {"a bolsa": "na sua carteira", "a Selic": "no seu Tesouro", "a inflação": "na sua renda"}
# (onde mexe, objeto, a conta do Denis)
NICHO_BOLSO = {
    "FII": ("na sua cota", "o seu FII", "o rendimento por cota antes e depois, e o que isso dá em R$ 100 mil no fundo"),
    "renda mensal": ("na sua renda", "a sua renda mensal", "quanto patrimônio dá R$ 1.000 por mês, líquido de imposto"),
    "Tesouro e renda fixa": ("no seu Tesouro", "o seu Tesouro", "quanto R$ 100 mil rendem no título, líquidos de IR, até o vencimento"),
    "ações": ("nos seus dividendos", "os seus dividendos", "o dividendo por ação vezes R$ 100 mil investidos, com o histórico de pagamento"),
    "investimento geral": ("na sua carteira", "a sua carteira", "o efeito numa carteira de R$ 100 mil"),
}
NICHO_FONTE = {
    "FII": ("rendimento por cota, P/VP e vacância", "relatório gerencial e informe mensal do fundo (fnet.b3.com.br)"),
    "renda mensal": ("rendimento mensal líquido e o IPCA do período", "informes dos ativos (B3/CVM) e SGS 13522 (IPCA)"),
    "Tesouro e renda fixa": ("a taxa do título na data", "tesourodireto.com.br (preços e taxas)"),
    "ações": ("dividendo por ação e data-com", "aviso aos acionistas na CVM (rad.cvm.gov.br) e o RI da empresa"),
    "investimento geral": ("o número central do vídeo, com data", "a fonte oficial do número (B3, CVM, BCB ou IBGE)"),
}
MODELOS_TITULO = [
    "{tema}: quanto muda {onde} em reais",
    "{tema}: a conta para quem tem R$ 100 mil",
    "O que muda {onde} com {tema_min}: a conta",
    "{tema} na prática: a renda de R$ 100 mil",
    "{tema}: o que isso faz com {objeto}",
    "{tema} em reais: a conta de R$ 100 mil",
]


# ------------------------------------------------------------------------------------------------ texto da proposta
def empresa(titulo):
    t = c.norm(titulo)
    for k, v in EMPRESAS.items():
        if re.search(rf"\b{k}\b", t):
            return v
    return None


def tema_de(o, diag):
    tks = diag["tema"]["tickers"]
    if tks:
        return tks[0]
    emp = empresa(o.get("titulo"))
    if emp:
        return emp
    ents = diag["tema"]["entidades"]
    if ents:
        return TEMA_TITULO.get(ents[0], ents[0])
    return NICHO_TEMA.get(o.get("nicho"), "Investimentos")


def titulo_passa(t, gate):
    """(passa, motivo). Até 60 caracteres e sem problema no gate (BLOQUEANTE, CORRETORA ou RECOMENDACAO)."""
    if len(t) > LIMITE_TITULO:
        return False, f"{len(t)} caracteres"
    if gate is None:
        if re.search(r"vale a pena|melhor(es)? |comprar agora|hora de (comprar|vender)|\bXP\b|\bBTG\b", t, re.I):
            return False, "checagem mínima (gate indisponível)"
        return True, "checagem mínima (gate indisponível)"
    r = gate.avaliar(gate.Post(t, "", "md", None))
    ruins = [p["codigo"] for p in r["problemas"] if p["nivel"] == gate.BLOQ or p["codigo"] in ("CORRETORA", "RECOMENDACAO_TEXTO")]
    return (not ruins), (", ".join(ruins) if ruins else "gate OK")


def titulos(o, diag, gate, n=3):
    tema = tema_de(o, diag)
    onde, objeto, _ = NICHO_BOLSO.get(o.get("nicho"), NICHO_BOLSO["investimento geral"])
    ents = diag["tema"]["entidades"]
    if ents and not diag["tema"]["tickers"] and ents[0] in ONDE_ENTIDADE:
        onde = ONDE_ENTIDADE[ents[0]]
    tema_min = tema if tema.isupper() or tema[:1].isupper() and tema[1:2].isupper() else tema[:1].lower() + tema[1:]
    if tema in ("Parecer da CVM",):
        tema_min = "o parecer da CVM"
    out, recusados = [], []
    nome_proprio = bool(diag["tema"]["tickers"] or empresa(o.get("titulo")))
    if nome_proprio:
        tema_min = tema
    modelos = [m for m in MODELOS_TITULO if nome_proprio or "{tema_min}" not in m]
    for m in modelos + [x.replace("{tema}", NICHO_TEMA.get(o.get("nicho"), "Investimentos")) for x in MODELOS_TITULO if "{tema_min}" not in x]:
        t = m.format(tema=tema, tema_min=tema_min, onde=onde, objeto=objeto)
        t = t[0].upper() + t[1:]
        if t in out:
            continue
        ok, motivo = titulo_passa(t, gate)
        if ok:
            out.append(t)
        else:
            recusados.append((t, motivo))
        if len(out) == n:
            break
    return out, recusados


def angulo_denis(o, diag):
    tema = tema_de(o, diag)
    _, objeto, conta = NICHO_BOLSO.get(o.get("nicho"), NICHO_BOLSO["investimento geral"])
    txt = (f"Ampliar, não contradizer: {o['canal']} mostrou que \"{tema}\" tem demanda agora ({o['multiplo']}× o normal "
           f"do canal). O vídeo do Denis parte da MESMA premissa (ângulo de {diag['angulo']['tipo']}) e vai um passo além: "
           f"{conta}, para quem tem de R$ 50 a 100 mil (o Tanaka), com o dado primário na tela.")
    if diag["angulo"]["tipo"] == "comparação":
        txt += " O frame de comparação é NO-GO no canal: o título do Denis vira a conta, não \"X ou Y\"."
    par = diag["parecidos_no_canal"]
    if par:
        p = par[0]
        txt += (f" O canal já fez \"{p['titulo']}\" ({p['publicado']}): é continuação, não repetição (double-down); "
                f"citar e linkar no vídeo novo.")
    return txt


def gancho_denis(o, diag):
    tema = tema_de(o, diag)
    onde, _, _ = NICHO_BOLSO.get(o.get("nicho"), NICHO_BOLSO["investimento geral"])
    ev = diag["timing"]["evento"]
    abre = f"{tema} virou o assunto da semana" + (" por causa de uma notícia" if ev else "") + "."
    return (f"{abre} Quem explicou o que aconteceu, explicou bem. Faltava a conta: com R$ 100 mil, quanto isso muda "
            f"{onde}, por mês, em reais. Eu fiz essa conta com o dado oficial, e o número é este.")


def dado_chave(o, diag):
    ents = diag.get("_entidades") or []
    if ents:
        _, _, dado, fonte = ents[0]
    else:
        dado, fonte = NICHO_FONTE.get(o.get("nicho"), NICHO_FONTE["investimento geral"])
    extra = ""
    if diag["tema"]["tickers"]:
        extra = f" Conferir também o código {', '.join(diag['tema']['tickers'])} no gate (universo B3)."
    return {"dado": dado, "fonte_primaria": fonte, "nota": ("Não usar o número do vídeo do concorrente como fonte: "
                                                             "ele é o ponto de partida, não a prova." + extra)}


# ------------------------------------------------------------------------------------------------ calendário
def ler_calendario(p):
    p = Path(p)
    if not p.is_file():
        return []
    with open(p, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def ler_trocas(p):
    d = c.ler_json(p, None)
    if isinstance(d, dict):
        return d.get("trocas") or []
    if isinstance(d, list):
        return d
    return []


def _float(s):
    try:
        return float(str(s).replace(",", "."))
    except (TypeError, ValueError):
        return None


def protegida(r, rx):
    """Episódio da série ou Copom: nunca sai."""
    if (r.get("serie_ep") or "").strip():
        return True
    alvo = c.norm(" ".join(r.get(k) or "" for k in ("origem", "titulo", "angulo")))
    return bool(re.search(rx, alvo))


def escolher_vaga(linhas, formato, hoje, semanas=3, trocas=(), rx_protegidas="copom"):
    """A pauta de menor inscritos esperados entre amanhã e hoje + 7×semanas, no formato, fora das protegidas e das
    vagas que já receberam outlier (troca com "proposta" no trocas.json, ou par data/título em `trocas`)."""
    fim = hoje + timedelta(days=7 * semanas)
    ids_outlier = {t.get("id") for t in trocas if t.get("proposta")}
    ja = set()
    for t in trocas:
        for k in ("sai", "entra", "novo"):
            if t.get(k) and t.get("data"):
                ja.add((t["data"], c.norm(t[k])))
    cands = []
    for r in linhas:
        try:
            d = date.fromisoformat(r["data"])
        except (KeyError, ValueError):
            continue
        if not (hoje < d <= fim) or r.get("formato") != formato or protegida(r, rx_protegidas):
            continue
        if (r["data"], c.norm(r.get("titulo"))) in ja or ids_outlier & set((r.get("trocas_aplicadas") or "").split()):
            continue
        e = _float(r.get("inscritos_esperados"))
        if e is None:
            continue
        cands.append((e, r["data"], r))
    if not cands:
        return None
    e, _, r = min(cands, key=lambda x: (x[0], x[1]))
    return r


_MODELO = {}


def esperado_do_tema(titulo, formato):
    """Inscritos esperados pelo modelo do pautas-canal para o assunto do título novo (ESTIMATIVA). None se falhar."""
    try:
        if "d" not in _MODELO:
            sys.path.insert(0, str(c.RAIZ / "pautas-canal"))
            import modelo as mo
            import temas
            _MODELO.update(d=mo.carregar(), mo=mo, temas=temas)
        an = _MODELO["mo"].an
        assunto = an.assunto(titulo)
        e, e25, e75, n, janela = _MODELO["temas"].esperado_por_assunto(_MODELO["d"], formato, assunto)
        return {"assunto": assunto, "esperado": round(e, 1), "faixa": f"{e25:.1f}–{e75:.1f}", "base": f"{janela}, n = {n}"}
    except Exception:
        return None


def encaixe(o, diag, cfg, hoje, usar_modelo=True, titulo_novo="", usadas=()):
    cc = cfg.get("calendario") or {}
    if diag["timing"]["quente"]:
        prazo = c.ler_data(diag["timing"]["prazo_ate"])
        return {"tipo": "short_rapido", "prazo_ate": diag["timing"]["prazo_ate"],
                "texto": (f"Short rápido: notícia quente (\"{diag['timing']['evento']}\"). Gravar e publicar até "
                          f"{prazo.astimezone(timezone(timedelta(hours=-3))):%d/%m %H:%M} (48 h). O calendário não muda.")}
    linhas = ler_calendario(c.caminho(cc.get("csv")))
    trocas = ler_trocas(c.caminho(cc.get("trocas"))) + list(usadas)
    fmt = o.get("formato") or "longo"
    r = escolher_vaga(linhas, fmt, hoje, int(cc.get("semanas", 3)), trocas, cc.get("protegidas_regex", "copom"))
    if r is None:
        return {"tipo": "sem_vaga", "texto": f"Nenhuma vaga de {fmt} trocável nas próximas {cc.get('semanas', 3)} semanas "
                                             "(só série, Copom ou trocas já feitas). Fica como ideia no Trello."}
    novo = esperado_do_tema(titulo_novo, fmt) if usar_modelo and titulo_novo else None
    d = date.fromisoformat(r["data"])
    txt = (f"Trocar a pauta de {r.get('dia', '')} {c.dmy(d)} (\"{r.get('titulo')}\", {r.get('inscritos_esperados')} "
           f"inscritos esperados pelo modelo, a menor de {fmt} nas próximas {cc.get('semanas', 3)} semanas fora da série "
           f"e do Copom).")
    if novo:
        txt += f" Tema novo ({novo['assunto']}) no modelo: {novo['esperado']} esperados ({novo['base']}). ESTIMATIVA."
        if novo["esperado"] <= (_float(r.get("inscritos_esperados")) or 0):
            txt += " O modelo não vê ganho na troca: a aposta é a demanda que o outlier mostrou, não a média do assunto."
    return {"tipo": "troca", "data": r["data"], "dia": r.get("dia", ""), "formato": fmt, "sai": r.get("titulo", ""),
            "sai_esperado": _float(r.get("inscritos_esperados")), "sai_assunto": r.get("assunto", ""),
            "esperado_tema_novo": novo, "texto": txt}


# ------------------------------------------------------------------------------------------------ montagem
def propor_um(o, denis, cfg, agora, hoje, gate, usar_modelo=True, usadas=(), disputa_vaga=True):
    diag = dg.diagnosticar(o, denis, cfg, agora)
    tits, recusados = titulos(o, diag, gate)
    if disputa_vaga or diag["timing"]["quente"]:
        enc = encaixe(o, diag, cfg, hoje, usar_modelo, tits[0] if tits else "", usadas)
    else:
        enc = {"tipo": "ideia", "texto": "Fica como ideia: só as propostas de maior pontuação disputam vaga no "
                                         "calendário (deteccao.max_trocas)."}
    if enc["tipo"] == "troca":
        enc["entra"] = tits[0] if tits else o["titulo"][:LIMITE_TITULO]
    p = {"id": f"OUT-{o['video_id']}", "video_id": o["video_id"], "gerada_em": c.iso(agora),
         "outlier": {k: o.get(k) for k in ("titulo", "canal", "channel_id", "inscritos", "views", "multiplo", "idade_h",
                                            "publicado", "nicho", "formato", "base", "n_comparacao",
                                            "mediana_mesma_idade", "pontuacao", "url")},
         "diagnostico": {k: v for k, v in diag.items() if not k.startswith("_")},
         "angulo": angulo_denis(o, diag), "titulos": tits, "titulos_recusados": recusados,
         "gancho": gancho_denis(o, diag), "dado_chave": dado_chave(o, diag), "encaixe": enc, "rascunho": RASCUNHO}
    p["linha_resumo"] = linha_resumo(p)
    return p


def linha_resumo(p):
    o, e = p["outlier"], p["encaixe"]
    if e["tipo"] == "short_rapido":
        dest = "Short rápido"
    elif e["tipo"] == "troca":
        dest = f"proposta: trocar o de {c.dmy(date.fromisoformat(e['data']))}"
    else:
        dest = "ideia no Trello"
    mult = f"{o['multiplo']:g}x"
    return f"🔥 Outlier: {o['titulo']} ({o['canal']}, {mult}) → {dest}"


def card(p):
    o, d, e = p["outlier"], p["diagnostico"], p["encaixe"]
    nome = f"🔥 Outlier: {o['titulo'][:80]} ({o['canal']}, {o['multiplo']:g}x)"
    par = d["parecidos_no_canal"]
    linhas = [
        f"**{p['rascunho']}.** Dado é dado; ângulo, títulos e gancho são sugestão.", "",
        f"**Outlier:** [{o['titulo']}]({o['url']}) · {o['canal']}" + (f" ({o['inscritos']:,} inscritos)".replace(",", ".") if o.get("inscritos") else ""),
        f"{o['multiplo']:g}× a mediana do canal na mesma idade · {o['views']:,} views".replace(",", ".") if o.get("views") is not None
        else f"{o['multiplo']:g}× (radar)",
        f"Idade: {o['idade_h']} h · nicho: {o['nicho']} · formato: {o['formato']} · base: {o['base']} · pontuação {o['pontuacao']}", "",
        "**Por que estourou**"] + [f"- {x}" for x in d["por_que_estourou"]] + [
        "", "**O canal já fez parecido?**"] + ([
            f"- [{x['titulo']}]({x['url']}) ({x['publicado']}): {x['views_intencionais'] if x['views_intencionais'] is not None else '?'} "
            f"views intencionais, {x['inscritos'] if x['inscritos'] is not None else '?'} inscritos (similaridade {x['similaridade']})"
            for x in par] or ["- Não achei nada parecido em videos.csv."]) + [
        "", "**Ângulo do Denis (rascunho)**", p["angulo"],
        "", "**Títulos (até 60 caracteres, passaram no gate)**"] + [f"{i}. {t}" for i, t in enumerate(p["titulos"], 1)] + [
        "", "**Gancho (rascunho, voz do canal)**", p["gancho"],
        "", "**Dado-chave a conferir**", f"{p['dado_chave']['dado']}. Fonte primária: {p['dado_chave']['fonte_primaria']}. "
        f"{p['dado_chave']['nota']}",
        "", "**Encaixe**", e["texto"]]
    if e["tipo"] == "troca":
        linhas += ["", f"Para aprovar: `python3 outliers/encaixar.py aprovar {p['id']} --quem Denis`"]
    linhas += ["", f"video_id: {p['video_id']} · proposta: {p['id']}"]
    return nome, "\n".join(linhas)


def propor(cfg, entrada=None, agora=None, hoje=None, usar_modelo=True, gate="auto"):
    agora = agora or datetime.now(timezone.utc)
    hoje = hoje or agora.astimezone(timezone(timedelta(hours=-3))).date()
    det = detectar.detectar(cfg, entrada, agora)
    denis = dg.carregar_denis(cfg)
    gate = c.importar_gate(cfg) if gate == "auto" else gate
    n = int(cfg["deteccao"].get("max_propostas", 5))
    props, usadas = [], []          # duas propostas não disputam a mesma vaga: a segunda pega a próxima menor
    for o in det["outliers"][:n]:
        p = propor_um(o, denis, cfg, agora, hoje, gate, usar_modelo, usadas,
                      disputa_vaga=len(usadas) < int(cfg["deteccao"].get("max_trocas", 2)))
        if p["encaixe"]["tipo"] == "troca":
            usadas.append({"data": p["encaixe"]["data"], "sai": p["encaixe"]["sai"], "entra": ""})
        props.append(p)
    return {"gerado_em": c.iso(agora), "hoje": hoje.isoformat(), "entrada": det.get("entrada"), "fonte": det.get("fonte"),
            "erro": det.get("erro"), "gate": "gate_qualidade.py" if gate else "checagem mínima (gate indisponível)",
            "propostas": props, "descartes": det.get("descartes", [])}


def markdown(r):
    l = [f"# Outliers → encaixe · {r['hoje']}", "", f"Entrada: `{r['entrada']}` ({r['fonte']}). Gate: {r['gate']}.", ""]
    if r.get("erro"):
        l.append(f"**Erro:** {r['erro']}")
    if not r["propostas"]:
        l.append("Nenhum outlier no nicho hoje.")
    for p in r["propostas"]:
        nome, desc = card(p)
        l += [f"## {nome}", "", desc, ""]
    if r["descartes"]:
        l += ["## Descartados", ""] + [f"- {d.get('canal')}: {d.get('titulo')} → {d['motivo']}" for d in r["descartes"]]
    return "\n".join(l) + "\n"


def main(argv=None):
    ap = argparse.ArgumentParser(description="Gera as propostas (ângulo, títulos, gancho, dado e encaixe).")
    ap.add_argument("--config")
    ap.add_argument("--entrada")
    ap.add_argument("--agora", help="AAAA-MM-DDTHH:MM (UTC se não tiver fuso)")
    ap.add_argument("--hoje", help="AAAA-MM-DD (padrão: data de Brasília de --agora)")
    ap.add_argument("--sem-modelo", action="store_true", help="não calcula o esperado do tema novo (mais rápido)")
    ap.add_argument("--saida", help="pasta (padrão: caminhos.saida)")
    a = ap.parse_args(argv)
    cfg = c.carregar_config(a.config)
    agora = c.ler_data(a.agora) if a.agora else None
    hoje = date.fromisoformat(a.hoje) if a.hoje else None
    r = propor(cfg, a.entrada, agora, hoje, not a.sem_modelo)
    saida = c.caminho(a.saida) if a.saida else c.caminho(cfg["caminhos"]["saida"])
    c.gravar_json(saida / "propostas.json", r)
    arq_p = c.caminho(cfg["caminhos"]["estado"]) / "propostas.json"      # arquivo de todas (o encaixar.py lê daqui)
    arq = c.ler_json(arq_p, {}) or {}
    for p in r["propostas"]:
        arq[p["id"]] = p
    c.gravar_json(arq_p, arq)
    (saida / "propostas.md").write_text(markdown(r), encoding="utf-8")
    print(f"{len(r['propostas'])} proposta(s), {len(r['descartes'])} descarte(s) -> {saida / 'propostas.json'}")
    for p in r["propostas"]:
        print("  " + linha_resumo(p))
    return 0


if __name__ == "__main__":
    sys.exit(main())
