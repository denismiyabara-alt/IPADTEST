#!/usr/bin/env python3
"""Calendário v3, o OFICIAL (05/10 a 29/11/2026), aprovado pelo Denis em 03/10/2026. Gera CALENDARIO.md e .csv.

Parte do v2 (calendario_v2.PAUTAS, que continua gerando o histórico CALENDARIO-8-SEMANAS.md e .csv) e aplica a
proposta aprovada (serie/PROPOSTA-CALENDARIO-V3.md):
1. entram os 6 episódios da série de renda mensal, às quartas, com o título PROVISÓRIO (ainda passa pelo empacotador e
   pelo teste A/B);
2. saem as 7 pautas fora do nicho (07/10, 21/10, 16/11, 18/11, 21/11, 23/11 e 28/11), trocadas pelos Shorts derivados
   dos episódios ou pelos próprios episódios;
3. o Tesouro do Copom de 03-04/11 vira a versão PRÉ do molde (serie/MOLDE-TESOURO-COPOM.md), na terça 03/11, 19h; a
   pauta de renda mensal que estava na terça vai para a quinta 05/11, que ficou livre;
4. nenhuma semana com mais de 3 longos: na semana com 4, sai o longo de menor número de inscritos esperados (fora os
   episódios e o Copom, que são fixos) ou ele é empurrado para a próxima semana com vaga dentro da janela; sem vaga,
   vai para a fila de dezembro. A regra roda aqui, não à mão.

Inscritos esperados: o mesmo modelo do v2 (temas.esperado_por_assunto, de modelo.py). É ESTIMATIVA, não previsão.

uso: python3 calendario_v3.py
"""
import csv
from collections import Counter, defaultdict
from datetime import date, timedelta
from pathlib import Path

import calendario_v2 as v2
import meta as me
import modelo as mo
import temas
import termos
from modelo import an

AQUI = Path(__file__).resolve().parent
L, S = v2.L, v2.S
DIAS = v2.DIAS
INICIO, FIM = date(2026, 10, 5), date(2026, 11, 29)
MAX_LONGOS_SEMANA = 3
SERIE = "renda mensal"                      # assunto planejado de todos os itens da série
PROVISORIO = "provisório (empacotador + teste A/B)"

TROCAS = AQUI / "trocas.json"   # trocas aprovadas, na ordem; fonte de verdade das mudanças sobre o v2


def carregar_trocas(caminho=TROCAS):
    import json
    return json.loads(Path(caminho).read_text(encoding="utf-8"))["trocas"]


def _fora_do_nicho(trocas=None):
    """As 7 pautas fora do nicho (data → título no v2), lidas das trocas marcadas com fora_do_nicho."""
    trocas = trocas if trocas is not None else carregar_trocas()
    return {p["data"]: p["titulo"] for t in trocas if t.get("fora_do_nicho") for p in t["pautas"]}


FORA_DO_NICHO = _fora_do_nicho()

# Fontes que valem para toda a série (SERIE-RENDA-MENSAL.md).
F_SERIE = "regras de 2026 da série (LC 224/2025; Lei 14.754/2023; Lei 15.270/2025; Res. CMN 5.215; fgc.org.br; Lei 11.033/2004)"

# Itens da série: (data, formato, título, termo exibido, família de termos, continuação, ângulo, fontes, episódio)
SERIE_ITENS = [
    ("2026-10-07", S, "Recebeu 1% ao mês e a cota caiu 1%: quanto ganhou?", None, None,
     "Fb0l4KEq27o (637); trocar o link pelo Ep. 1 em 14/10",
     "Short pré-estreia do Ep. 1: a conta do retorno total em 40 s.", "IPCA 12 meses (SGS 13522)", "Ep. 1 (Short)"),
    ("2026-10-14", L, "ETF que paga dividendos mensais: a renda saiu da cota?", "etfs que pagam dividendos mensais",
     r"etfs?.*dividendos? mensa|dividendos mensais", "Fb0l4KEq27o (637) e c9Obo6F5_NU",
     "Ep. 1: retorno total = cota + rendimentos; o passo a passo para refazer com o histórico da B3, sem lista de ETFs.",
     "SGS 13522 (IPCA 12 meses); B3 (séries históricas e eventos corporativos); " + F_SERIE, "Ep. 1"),
    ("2026-10-21", L, "Dividendos altos demais: 4 contas antes de confiar na renda", "dividendos",
     r"^dividendos$|dividendos? todo mes", "TY8oLvUt2Qg (324)",
     "Ep. 2: efeito preço, payout, lucro que não se repete e histórico de 5 anos; exemplos hipotéticos.",
     "RAD da CVM e RI, se usar empresa real; " + F_SERIE, "Ep. 2"),
    ("2026-10-21", S, "O dividend yield dobrou e a empresa não pagou nada a mais", None, None, "Ep. 2 (mesmo dia)",
     "Short do Ep. 2: a conta do efeito preço em 35 s, publicado depois do longo.", "—", "Ep. 2 (Short)"),
    ("2026-10-28", L, "Gastar ou reinvestir os dividendos: a conta de 10 anos", "dividendos mensais",
     r"dividendos? mensa|1 milh|um milh", "IB1mBcF00jc (131)",
     "Ep. 3: R$ 100 mil a 0,6% ao mês, gastar × reinvestir × meio-termo, ano a ano.", "só aritmética (1,006¹²⁰ = 2,05); " + F_SERIE,
     "Ep. 3"),
    ("2026-11-11", L, "LCI e LCA para renda mensal: a escada de vencimentos", "lci e lca", r"\blci\b|\blca\b",
     "Q1WMbZZn2Ik (Short) e dHYQtxnMSrw (421)",
     "Ep. 4: 12 degraus de R$ 10 mil, prazo mínimo de 6 meses, LCI × CDB líquido e FGC. Refazer o exemplo se o Copom de "
     "04/11 mudar a Selic.", "SGS 4389 (CDI) e 432 (Selic); " + F_SERIE, "Ep. 4"),
    ("2026-11-16", S, "LCI e LCA não pagam todo mês. Mas dá para fazer vencer uma por mês", None, None, "Ep. 4 (11/11)",
     "Short do Ep. 4: o desenho dos 12 degraus.", "Res. CMN 5.215", "Ep. 4 (Short)"),
    ("2026-11-18", L, "Renda mensal e inflação: quanto reinvestir para não encolher", "tesouro ipca",
     r"tesouro|ipca|\bntn", "dHYQtxnMSrw (421) e KMIsVEOcaLM (246)",
     "Ep. 5: R$ 1.000 hoje compram R$ 661 em 10 anos com IPCA de 4,22%; reinvestir = inflação ÷ rendimento.",
     "SGS 13522; CSV do Tesouro Transparente; Focus mais recente; " + F_SERIE, "Ep. 5"),
    ("2026-11-18", S, "R$ 100 mil, 10 anos: gastar a renda ou reinvestir?", None, None, "Ep. 3 (28/10)",
     "Short do Ep. 3: as duas colunas em 30 s (mesmo tema de juros compostos do Short que saiu).", "—", "Ep. 3 (Short)"),
    ("2026-11-23", S, "R$ 1.000 de renda hoje compram quanto em 10 anos?", None, None, "Ep. 5 (18/11)",
     "Short do Ep. 5: a conta e a regra de bolso.", "SGS 13522", "Ep. 5 (Short)"),
    ("2026-11-25", L, "Renda todo mês com Tesouro e FII: a grade de 12 meses", "tesouro direto",
     r"tesouro|fundos? imobiliari|dividendos? todo mes", "TY8oLvUt2Qg (324) e KMIsVEOcaLM (246)",
     "Ep. 6: grade de 12 meses com cupons do Tesouro, FII e ações; mostra os meses vazios. Fecha a série.",
     "Tesouro Direto (meses de cupom); Lei 8.668/1993; " + F_SERIE, "Ep. 6"),
]
# O Short do Ep. 6 ("Recebe todo mês? Veja quais meses ficam vazios") fica para seg 30/11, fora da janela.

# Copom de 03-04/11: versão PRÉ do molde, na terça 03/11, 19h (motivo em markdown()).
COPOM_PRE = ("2026-11-03", L, "tesouro e renda fixa", "Tesouro Direto antes do Copom: o que olhar no IPCA+ hoje",
             "Copom novembro 2026", "MÉDIO: vídeos de Copom/Selic, 11.321 views da Pesquisa (9%)",
             "KMIsVEOcaLM (246), tb0nwpl9mFw (142) e dHYQtxnMSrw (421)",
             "VERSÃO PRÉ do molde (MOLDE-TESOURO-COPOM.md): o que o mercado espera (Focus de 30/10, divulgado na "
             "terça 03/11 por causa de Finados: conferir), o que observar no comunicado e as taxas da manhã de terça. "
             "Sem prever a decisão.",
             "Focus (bcb.gov.br/publicacoes/focus); CSV do Tesouro Transparente e site do Tesouro Direto; datas: conferir "
             "em bcb.gov.br/controleinflacao/calendarioreunioescopom")
COPOM_SHORT = ("2026-11-04", S, "tesouro e renda fixa", "Copom hoje: 3 números para olhar no seu Tesouro", "Copom hoje",
               "MÉDIO: vídeos de Copom/Selic do canal, 11.321 views da Pesquisa (9%)", "longo pré de 03/11",
               "Corte do longo pré de 03/11 com as taxas da manhã de quarta (o [*_ANTES] definitivo do molde); "
               "link para o longo. Sem prever a decisão.", "Taxas do Tesouro do dia")

# Termos de busca das pautas novas ou que mudaram de data (as outras usam calendario_v2.TERMOS).
TERMOS_NOVOS = {
    ("2026-11-03", L): ("tesouro direto", r"tesouro|ipca|\bntn|copom|selic"),
}


def _pauta(t, origem, assunto_manual=None, ep=""):
    data_, fmt, assunto, titulo, chave, volume, cont, angulo, fontes = t
    return {"data": data_, "formato": fmt, "assunto_planejado": assunto, "titulo": titulo, "palavra_chave": chave,
            "volume": volume, "continuacao_de": cont, "angulo": angulo, "fontes_a_conferir": fontes, "origem": origem,
            "assunto_manual": assunto_manual, "serie_ep": ep,
            "status_titulo": PROVISORIO if ep else "definido no v2" if origem.startswith("v2") else "novo",
            "termo": None, "trocas": []}


def catalogo():
    """Pautas que não estão no v2 e podem entrar por troca: itens da série e o Copom pré (chave: formato, título)."""
    cat = {}
    for data_, fmt, titulo, termo, fam, cont, angulo, fontes, ep in SERIE_ITENS:
        q = _pauta((data_, fmt, SERIE, titulo, termo or "", "", cont, angulo, fontes), "série de renda mensal",
                   assunto_manual=SERIE, ep=ep)
        q["termo"] = (termo, fam) if termo else None
        cat[("serie", fmt, titulo)] = q
    q = _pauta(COPOM_PRE, "Copom (versão pré)")
    q["termo"] = TERMOS_NOVOS[("2026-11-03", L)]
    cat[("copom", L, COPOM_PRE[3])] = q
    return cat


def pautas_v2():
    out = []
    for t in v2.PAUTAS:
        p = _pauta(t, "v2")
        p["termo"] = v2.TERMOS.get(t[0])
        out.append(p)
    return out


class TrocaInvalida(ValueError):
    pass


def _achar(linhas, ref, tid):
    ach = [r for r in linhas if (r["data"], r["formato"], r["titulo"]) == (ref["data"], ref["formato"], ref["titulo"])]
    if len(ach) != 1:
        raise TrocaInvalida(f"{tid}: pauta não encontrada (ou repetida): {ref}")
    return ach[0]


def aplicar_trocas(trocas, linhas, avaliar=lambda r: r):
    """Aplica as trocas na ordem. Devolve (linhas, fila de dezembro, log). `avaliar` calcula o esperado de uma pauta
    nova. O log guarda, para cada troca, o esperado total antes e depois e, nas da regra dos 3 longos, a semana antes."""
    cat = catalogo()
    fila, log = [], []
    linhas = [avaliar(r) for r in linhas]
    for t in trocas:
        tid, op = t["id"], t["op"]
        antes = sum(r.get("_e", 0) for r in linhas)
        snap = None
        if t.get("regra_3_longos"):
            k = semana(t["regra_3_longos"])
            snap = [dict(r) for r in sorted(linhas, key=lambda r: r["data"]) if r["formato"] == L and semana(r["data"]) == k]
        if op == "sai":
            for ref in t["pautas"]:
                r = _achar(linhas, ref, tid)
                linhas.remove(r)
                r["trocas"].append(tid)
                if t["destino"] == "fila de dezembro":
                    fila.append(r)
        elif op == "entra":
            for it in t["itens"]:
                if t["fonte"] == "fila":
                    ach = [r for r in fila if (r["formato"], r["titulo"]) == (it["formato"], it["titulo"])]
                    if len(ach) != 1:
                        raise TrocaInvalida(f"{tid}: não está na fila de dezembro: {it}")
                    r = ach[0]
                    fila.remove(r)
                    r["origem"] += f" (voltou da fila em {_d(it['data'])}; era {_d(r['data'])})"
                else:
                    r = avaliar(dict(cat[(t["fonte"], it["formato"], it["titulo"])], trocas=[]))
                r["data"] = it["data"]
                r["trocas"].append(tid)
                linhas.append(r)
        elif op == "move":
            r = _achar(linhas, t["pauta"], tid)
            r["origem"] += f" (movida de {_d(r['data'])})"
            r["data"] = t["para"]
            r["trocas"].append(tid)
        elif op == "titulo":
            r = _achar(linhas, t["pauta"], tid)
            r["titulo"] = t["novo"]
            r["origem"] += " (título trocado)"
            r["trocas"].append(tid)
            avaliar(r)
        elif op == "edita":
            r = _achar(linhas, t["pauta"], tid)
            r.update(t.get("campos", {}))
            if t.get("acrescenta_ao_angulo"):
                r["angulo"] += " " + t["acrescenta_ao_angulo"]
            r["trocas"].append(tid)
        elif op == "absorve":
            alvo = _achar(linhas, t["alvo"], tid)
            nomes = []
            for ref in t["pautas"]:
                r = _achar(linhas, ref, tid)
                linhas.remove(r)
                nomes.append(f"{_d(r['data'])} \"{r['titulo']}\"")
            alvo["angulo"] += " BLOCOS ABSORVIDOS (" + tid + "): " + "; ".join(t["blocos"]) + "."
            alvo["continuacao_de"] += "; absorve " + " e ".join(nomes)
            alvo["trocas"].append(tid)
        else:
            raise TrocaInvalida(f"{tid}: operação desconhecida {op!r}")
        for r in linhas:
            r["dia"] = DIAS[date.fromisoformat(r["data"]).weekday()]
            if not INICIO <= date.fromisoformat(r["data"]) <= FIM:
                raise TrocaInvalida(f"{tid}: data fora da janela: {r['data']}")
        log.append({"troca": t, "antes": antes, "depois": sum(r.get("_e", 0) for r in linhas), "semana_antes": snap})
    linhas.sort(key=lambda r: (r["data"], r["formato"] == S))
    return linhas, fila, log


def semana(data_):
    return (date.fromisoformat(data_) - INICIO).days // 7


def fixa(r):
    """Episódios da série e o Copom não saem pela regra dos 3 longos (aprovados pelo Denis)."""
    return bool(r["serie_ep"]) or r["origem"].startswith("Copom")


def aplicar_limite(linhas):
    """Nenhuma semana com mais de 3 longos: tira o de menor esperado (entre os não fixos) e tenta empurrar para a
    próxima semana com vaga, no mesmo dia da semana; sem vaga na janela, vai para a fila de dezembro."""
    decisoes = []
    while True:
        cont = Counter(semana(r["data"]) for r in linhas if r["formato"] == L)
        cheias = sorted(k for k, n in cont.items() if n > MAX_LONGOS_SEMANA)
        if not cheias:
            return linhas, decisoes
        k = cheias[0]
        cands = [r for r in linhas if r["formato"] == L and semana(r["data"]) == k and not fixa(r)]
        fraco = min(cands, key=lambda r: (r["_e"], r["data"]))
        destino = None
        for k2 in range(k + 1, semana(FIM.isoformat()) + 1):
            if cont.get(k2, 0) < MAX_LONGOS_SEMANA:
                dt = date.fromisoformat(fraco["data"]) + timedelta(days=7 * (k2 - k))
                if dt <= FIM and not any(r["data"] == dt.isoformat() and r["formato"] == L for r in linhas):
                    destino = dt.isoformat()
                    break
        semana_txt = f"{INICIO + timedelta(days=7 * k):%d/%m}"
        outros = sorted((r for r in linhas if r["formato"] == L and semana(r["data"]) == k), key=lambda r: r["data"])
        dec = {"semana": semana_txt, "longos": [(r["data"], r["titulo"], r["_e"], fixa(r)) for r in outros],
               "sai": fraco["titulo"], "data": fraco["data"], "esperado": fraco["_e"], "assunto": fraco["assunto"]}
        if destino:
            dec["acao"] = f"empurrado para {destino[8:]}/{destino[5:7]}"
            fraco["origem"] += f" (empurrada de {fraco['data'][8:]}/{fraco['data'][5:7]})"
            fraco["data"] = destino
            fraco["dia"] = DIAS[date.fromisoformat(destino).weekday()]
        else:
            dec["acao"] = "sai da janela (fila de dezembro): nenhuma semana seguinte até 29/11 tem vaga"
            linhas.remove(fraco)
        dec["_pauta"] = fraco
        decisoes.append(dec)


def demanda(T, termo):
    """Igual a calendario_v2.demanda, com o termo passado direto (as datas mudaram)."""
    if not termo:
        return "", "", "", "sem termo associado (Short de alcance)"
    texto, fam = termo
    ts = [t for t in T.casar(fam) if not T.categoria(t).startswith("amplo")]
    if not ts:
        return "", "—", 0, "nenhum termo nos dados (nem no top 25 mensal, nem nos 50 vídeos de busca)"
    vit = T.vitalicio(ts)
    seis = T.texto_6m(ts)
    donos = Counter(T.dono(t) for t in ts if T.dono(t))
    dono = donos.most_common(1)[0][0] if donos else "—"
    return (texto or "", seis, vit, f"{len(ts)} termos da família, {vit:,} views da Pesquisa no vitalício "
            f"(sobretudo em {dono}); 6 meses: {seis}".replace(",", "."))


COLS = ["data", "dia", "formato", "assunto", "assunto_pelo_titulo", "titulo", "status_titulo", "serie_ep", "origem",
        "trocas_aplicadas",
        "termo_busca", "views_pesquisa_6m", "views_pesquisa_vitalicio", "demanda", "continuacao_de", "angulo",
        "inscritos_esperados", "faixa_p25_p75", "base_do_esperado", "fontes_a_conferir"]


def montar(d, T=None, trocas=None):
    """Calendário oficial: v2 + trocas.json, conferido pela regra dos 3 longos. Devolve (linhas, decisões da regra
    automática, fila de dezembro, log das trocas)."""
    T = T or termos.Termos()
    trocas = trocas if trocas is not None else carregar_trocas()
    cache = {}

    def avaliar(r):
        r["assunto_pelo_titulo"] = an.assunto(r["titulo"])
        r["assunto"] = an.assunto(r["titulo"], r["assunto_manual"])
        k = (r["formato"], r["assunto"])
        if k not in cache:
            cache[k] = temas.esperado_por_assunto(d, *k)
        e, e25, e75, n, janela = cache[k]
        r.update(inscritos_esperados=round(e, 1), faixa_p25_p75=f"{e25:.1f}–{e75:.1f}", _e=e, _e25=e25, _e75=e75,
                 base_do_esperado=f"{r['assunto']}, {r['formato']}s, {janela} (n = {n}) · ESTIMATIVA")
        tb, v6, vv, dem = demanda(T, r["termo"])
        r.update(termo_busca=tb, views_pesquisa_6m=v6, views_pesquisa_vitalicio=vv, demanda=dem)
        return r

    linhas, fila, log = aplicar_trocas(trocas, pautas_v2(), avaliar)
    linhas, decisoes = aplicar_limite(linhas)          # salvaguarda: com as trocas de hoje, não sobra nada a fazer
    for dec in decisoes:
        p = dec.pop("_pauta", None)
        if p is not None and p not in linhas:
            fila.append(p)
    for r in linhas:
        r["trocas_aplicadas"] = " ".join(r["trocas"])
    linhas.sort(key=lambda r: (r["data"], r["formato"] == S))
    return linhas, decisoes, fila, log


def por_mes(linhas):
    m = defaultdict(lambda: {"longos": 0, "shorts": 0, "e": 0.0, "e25": 0.0, "e75": 0.0})
    for r in linhas:
        x = m[r["data"][:7]]
        x["longos" if r["formato"] == L else "shorts"] += 1
        x["e"] += r["_e"]
        x["e25"] += r["_e25"]
        x["e75"] += r["_e75"]
    return dict(sorted(m.items()))


def liquidos_por_mes(b, mes_e, chave="e"):
    """Inscritos líquidos do mês como em META.md: catálogo + vídeos novos (com a defasagem 60/25/15%) − perdas."""
    meses = list(mes_e)
    out = {}
    for i, m in enumerate(meses):
        novos = sum(mes_e[meses[i - k]][chave] * w for k, w in enumerate(me.DEFASAGEM) if i - k >= 0)
        out[m] = {"novos": novos, "liquidos": b["catalogo"] + novos - b["perdas_6m"]}
    return out


br = v2.br


def _pascoa(a):
    """Domingo de Páscoa (algoritmo de Meeus/Jones/Butcher)."""
    c, n = divmod(a, 100)
    g = a % 19
    h = (19 * g + c - c // 4 - (8 * c + 13) // 25 + 15) % 30
    i = h - (h // 28) * (1 - (h // 28) * (29 // (h + 1)) * ((21 - g) // 11))
    j = (a + a // 4 + i + 2 - c + c // 4) % 7
    m = 3 + (i - j + 40) // 44
    return date(a, m, i - j + 28 - 31 * (m // 4))


def feriados(anos=range(2018, 2027)):
    """Feriados nacionais e os pontos facultativos nacionais em que o país para (Carnaval e Corpus Christi)."""
    out = {}
    for a in anos:
        fixos = [(1, 1), (4, 21), (5, 1), (9, 7), (10, 12), (11, 2), (11, 15), (12, 25)] + ([(11, 20)] if a >= 2024 else [])
        for m, d_ in fixos:
            out[date(a, m, d_)] = True
        p = _pascoa(a)
        for k in (-48, -47, -2, 60):
            out[p + timedelta(days=k)] = True
    return out


def longos_em_feriado(d, ref=date(2026, 9, 2), formato=L):
    """Inscritos por vídeo publicado em feriado × nos outros dias (vitalício e últimos 12 meses), 30+ dias de vida."""
    import statistics as st
    fer = feriados()
    dia = lambda v: v["publicado"].date() if hasattr(v["publicado"], "hour") else v["publicado"]
    out = {}
    for nome, ini in (("vitalício", date(2018, 1, 1)), ("12 meses", ref - timedelta(days=336))):
        vs = [v for v in d.v.values() if v["formato"] == formato and v["publicado"] and ini <= dia(v) <= ref]
        f = [an.ganhos(v) or 0 for v in vs if dia(v) in fer]
        o = [an.ganhos(v) or 0 for v in vs if dia(v) not in fer]
        out[nome] = (len(f), st.median(f) if f else None, len(o), st.median(o))
    return out


def _d(data_):
    return f"{data_[8:]}/{data_[5:7]}"


def markdown(d, linhas, decisoes, fila, log):
    b = mo.base(d)
    p = mo.plano(d, b, me.PLANO_LONGOS, me.PLANO_SHORTS)
    metas = {r["mes"]: r for r in me.metas_mensais(b, p)}
    sem = v2.por_semana(linhas, INICIO)
    v2l = v2.montar(d)
    sem2 = v2.por_semana(v2l, INICIO)
    tot2 = sum(r["_e"] for r in v2l)
    tot3 = sum(r["_e"] for r in linhas)
    rm = temas.esperado_por_assunto(d, L, "renda mensal")[0]
    te = temas.esperado_por_assunto(d, L, "tesouro e renda fixa")[0]
    ae = temas.esperado_por_assunto(d, L, "ações e empresas")[0]
    geral = mo.ranking(d, L, "12 meses")[1]["esperado"]
    nl = sum(1 for r in linhas if r["formato"] == L)
    ns = len(linhas) - nl
    nl2 = sum(1 for r in v2l if r["formato"] == L)
    ns2 = len(v2l) - nl2
    sai_e = sum(r["_e"] for r in v2l if FORA_DO_NICHO.get(r["data"]) == r["titulo"])
    cop = next(r for r in linhas if r["origem"].startswith("Copom"))
    fer = longos_em_feriado(d)
    fv, f12 = fer["vitalício"], fer["12 meses"]
    fs = longos_em_feriado(d, formato=S)["vitalício"]

    trocas = [x["troca"] for x in log]
    n_trocas = len(trocas)
    out = [f"""# Calendário oficial: v3 (05/10 a 29/11/2026)

**Aprovado pelo Denis em 03/10/2026, com o ajuste do mesmo dia.** Gerado por `calendario_v3.py`: parte do v2 e aplica,
na ordem, as {n_trocas} trocas aprovadas de `trocas.json` (com data, motivo e quem aprovou). Para trocar uma pauta,
acrescente uma troca no fim de `trocas.json` e rode o script. Todas as colunas estão em `CALENDARIO.csv` (a coluna
`trocas_aplicadas` diz quais trocas mexeram em cada pauta).

**Histórico:** o v2 continua em `CALENDARIO-8-SEMANAS.md` e `.csv` (gerados por `calendario_v2.py`, sem mudança) e o
v1 em `CALENDARIO-8-SEMANAS_v1.*`. A proposta está em `serie/PROPOSTA-CALENDARIO-V3.md`.

**Inscritos esperados são ESTIMATIVA, não previsão:** views intencionais medianas do assunto × inscritos por mil, nos
últimos 12 meses (`modelo.py`, `TEMAS.md`). São inscritos vitalícios de cada vídeo, que chegam ao longo de 1 a 3 meses.

## O que mudou do v2 para o v3

1. **Série de renda mensal aprovada:** 6 episódios às quartas, 19h (14/10, 21/10, 28/10, 11/11, 18/11 e 25/11).
   **Os títulos são provisórios:** ainda passam pelo empacotador e pelo teste A/B (coluna `status_titulo`).
2. **Saem as 7 pautas fora do nicho** (tabela abaixo), trocadas pelos Shorts derivados dos episódios ou pelos episódios.
3. **Copom de 03-04/11: Tesouro ANTES da decisão**, na **terça 03/11, 19h**, com a versão pré do molde. A pauta de renda
   mensal que estava na terça 03/11 vai para a quinta 05/11, que era do longo pós.
4. **Nenhuma semana com mais de 3 longos** (tabela abaixo).
5. **ETF de dividendos mensais só no Ep. 1** (ajuste de 03/10): o tema estava em 4 longos em 5 semanas. O de 06/10 vai
   para depois da série; os de 20/10 (opções) e 17/11 (taxa) viram blocos do Ep. 1. O TRXF11 volta em 20/10 e o FII
   para iniciantes passa de sáb 07/11 para ter 17/11.
6. **Total:** {nl} longos e {ns} Shorts (v2: {nl2} e {ns2}).

### As 7 pautas fora do nicho

| data | saiu (v2) | entrou (v3) |
|---|---|---|"""]
    por_data = defaultdict(list)
    for r in linhas:
        por_data[r["data"]].append(r)
    for data_, tit in FORA_DO_NICHO.items():
        fmt = next(r["formato"] for r in v2l if r["data"] == data_ and r["titulo"] == tit)
        novo = [r for r in por_data[data_] if r["formato"] == fmt and r["serie_ep"]]
        if novo:
            ent = f"{novo[0]['serie_ep']}: \"{novo[0]['titulo']}\""
        else:
            ep = next(r for r in linhas if r["serie_ep"] and r["formato"] == L and semana(r["data"]) == semana(data_))
            ent = f"nada no dia; o longo da semana passa a ser o {ep['serie_ep']} ({_d(ep['data'])})"
        out.append(f"| {_d(data_)} {DIAS[date.fromisoformat(data_).weekday()]} | {fmt}: \"{tit}\" | {ent} |")
    out.append("\nO Short do Ep. 6 (\"Recebe todo mês? Veja quais meses ficam vazios\") fica para seg 30/11, fora da janela.")

    out.append("""
### Semanas com 4 longos: a decisão

Regra aprovada: numa semana com mais de 3 longos, sai o de **menor número de inscritos esperados** pelo modelo, ou ele é
empurrado para a próxima semana com vaga. Os episódios da série e o Copom são fixos (aprovados com data).
""")
    regra = [x for x in log if x["troca"].get("regra_3_longos")]
    for x in regra:
        t = x["troca"]
        sai = {(p_["data"], p_["titulo"]) for p_ in t["pautas"]}
        out.append(f"**Semana de {_d(t['regra_3_longos'])}** ({len(x['semana_antes'])} longos, troca {t['id']}):\n\n"
                   "| data | longo | inscritos esperados | fixo? | decisão |\n|---|---|---|---|---|")
        for r in x["semana_antes"]:
            acao = f"**sai para a {t['destino']}**" if (r["data"], r["titulo"]) in sai else "fica"
            out.append(f"| {_d(r['data'])} | {r['titulo']} | {br(r['_e'])} | {'sim' if fixa(r) else 'não'} | {acao} |")
        out.append("")
    if decisoes:
        out.append(f"A regra automática ainda mexeu em {len(decisoes)} pauta(s): "
                   + "; ".join(f"{dec['sai']} ({dec['acao']})" for dec in decisoes) + ".")
    out.append("""Nas duas semanas, o mais fraco é um longo de FII (45 esperados contra 91 de renda mensal e 195 de Tesouro), e
nenhuma semana seguinte até 29/11 tinha vaga. Os dois foram para a fila de dezembro e depois voltaram por outras trocas:
o FII ou imóvel de 12/11 para 06/10 (T10) e o TRXF11 de 31/10 para 20/10 (T15). A proposta sugeria tirar o CDB
prefixado de 14/11, mas pelo modelo ele é o mais forte da semana (Tesouro e renda fixa, 195).""")

    absorve = next((x["troca"] for x in log if x["troca"]["op"] == "absorve"), None)
    out.append(f"""
### ETF de dividendos mensais só no Ep. 1 (briefing do Ep. 1 e ajuste de 03/10)

No v2, o ETF de dividendos mensais era tema de 4 longos em 5 semanas (06/10, 20/10, 27/10 e 17/11), mais o Ep. 1 em
14/10: saturação e canibalização do termo "etfs que pagam dividendos mensais". Agora, dentro da janela, ele só é tema
de longo no Ep. 1. O 27/10 fica porque é comparação com FII (o imposto de cada um), com título novo e guardrail.

| data | antes | depois | troca e motivo |
|---|---|---|---|
| ter 06/10 | "ETFs que pagam dividendos mensais: o que mudou em 2026" (renda mensal, 91) | **fila de dezembro** (depois da série; vira o balanço do ano) | T09: sai 8 dias antes do Ep. 1, com o mesmo termo de busca |
| ter 06/10 | (vaga) | **"Fundo imobiliário ou imóvel alugado: a conta de 2026"** (FII, 45), que tinha saído de 12/11 pela regra | T10: o melhor da fila sem ETF de dividendos. O canal fez "Fundos Imobiliários ou Imóveis" em 26/06/2026 (14 inscritos): o ângulo de 2026 (Lei 14.754/2023, vacância, liquidez) tem de ficar claro no título final |
| qua 14/10 | Ep. 1 | **Ep. 1 com 2 blocos a mais** | T14: {'; '.join(absorve['blocos']) if absorve else ''}. O que cada bloco traz está no briefing do Ep. 1, seção "Blocos absorvidos (decisão de 03/10)" |
| ter 20/10 | "ETF de dividendos mensais com opções: de onde vem a renda" (91) | **"TRXF11: o que aconteceu com a renda desde agosto"** (FII, 45) | T14 + T15: as opções viram bloco do Ep. 1; o TRXF11 volta da fila ("trxf11" é o termo de investimento mais buscado do canal nos últimos 6 meses, 1.516 views da Pesquisa) |
| ter 27/10 | "ETF de dividendos mensais ou fundo imobiliário: o que sobra" | **"ETF de dividendos mensais ou FII: imposto e renda de cada um"** | T11 + T12: o título do v2 usava "o que sobra", como a promessa do Ep. 1; o imposto detalhado é deste vídeo |
| sáb 07/11 | "Fundos imobiliários para iniciantes: de onde vem a renda" (45) | **vaga** (a semana de 02/11 fica com 2 longos: o Copom e a renda mensal) | T16 |
| ter 17/11 | "ETF de dividendos mensais: quanto a taxa tira da renda" (91) | **"Fundos imobiliários para iniciantes: de onde vem a renda"** (movido de 07/11) | T14 + T16: a taxa vira bloco do Ep. 1. A fila de dezembro só tinha o ETF de dividendos, que não pode voltar; mover não muda o total, mas põe o vídeo na terça (o melhor dia, 10,4 inscritos por mil, contra sábado sem histórico) e tira a semana de 16/11 de 89 abaixo da meta semanal |
| qua 25/11 | Short "Taxa de administração do ETF" (corte do 17/11) | o mesmo Short, agora corte do bloco de taxa do Ep. 1 | T17 |

**Atenção:** com o TRXF11 em 20/10 e o FII para iniciantes em 17/11, há 4 longos de FII na janela (06/10, 20/10, 17/11 e
26/11), nenhum na mesma semana de outro.

### Fila de dezembro
""")
    for r in fila:
        out.append(f"- {r['titulo']} ({r['formato']}, {r['assunto']}, {br(r['_e'])} esperados; era {_d(r['data'])}; "
                   f"trocas {', '.join(r['trocas'])})")
    if not fila:
        out.append("- vazia")

    out.append("""
### Trocas aprovadas (`trocas.json`)

| troca | aprovada por | operação | o quê | efeito no esperado das 8 semanas | motivo |
|---|---|---|---|---|---|""")
    for x in log:
        t = x["troca"]
        if t["op"] in ("sai",):
            oq = "; ".join(f"{_d(p_['data'])} {p_['titulo']}" for p_ in t["pautas"]) + f" → {t['destino']}"
        elif t["op"] == "entra":
            oq = "; ".join(f"{_d(i_['data'])} {i_['titulo']}" for i_ in t["itens"]) + f" (de: {t['fonte']})"
        elif t["op"] == "move":
            oq = f"{t['pauta']['titulo']}: {_d(t['pauta']['data'])} → {_d(t['para'])}"
        elif t["op"] == "titulo":
            oq = f"{_d(t['pauta']['data'])}: \"{t['pauta']['titulo']}\" → \"{t['novo']}\""
        elif t["op"] == "absorve":
            oq = "; ".join(f"{_d(p_['data'])} {p_['titulo']}" for p_ in t["pautas"]) + f" → blocos do {_d(t['alvo']['data'])}"
        else:
            oq = f"{_d(t['pauta']['data'])} {t['pauta']['titulo']}"
        ef = x["depois"] - x["antes"]
        out.append(f"| {t['id']} | {t['aprovada_por']} | {t['op']} | {oq} | {'+' if ef >= 0 else '−'}{br(abs(ef))} | "
                   f"{t['motivo']} |")

    out.append(f"""
## Copom de 03-04/11: Tesouro antes da decisão

**Data escolhida: terça 03/11/2026, 19h** (1º dia da reunião), com a versão pré do `serie/MOLDE-TESOURO-COPOM.md`.
Título provisório: "{cop['titulo']}".

Por que terça e não segunda 02/11:
- **02/11 é feriado (Finados).** Longos publicados em feriado nacional (ou Carnaval e Corpus Christi) renderam
  menos: mediana de {br(fv[1])} inscritos por vídeo em {fv[0]} longos, contra {br(fv[3])} nos {br(fv[2])} dos outros dias
  (vitalício, com 30 dias ou mais de vida). Nos últimos 12 meses há só {f12[0]} {'longo' if f12[0] == 1 else 'longos'} em feriado, com
  {br(f12[1])} inscritos de mediana, contra {br(f12[3])}. Amostra pequena, mas nada a favor do feriado. (Nos Shorts o
  feriado não muda nada: mediana de {br(fs[1])} em {fs[0]} Shorts, contra {br(fs[3])}; por isso o Short de seg 12/10,
  feriado de Nossa Senhora Aparecida, fica.)
- **Segunda é o dia que menos converte:** 6,0 inscritos por mil views intencionais, contra 10,4 da terça
  (`PROPOSTA-CALENDARIO-V3.md`, 80 longos de 12 meses).
- **O Focus de segunda não sai no feriado.** O relatório de referência 30/10 sai no 1º dia útil, terça 03/11 (conferir
  em bcb.gov.br/publicacoes/focus). Um vídeo de segunda teria de usar o Focus de 23/10, de 10 dias antes; o de terça
  19h já usa o de 30/10, que é o [FOCUS_*] do molde.
- **É o padrão que funcionou:** 3 dos 4 longos de Tesouro em semana de Copom saíram na terça, 1º dia da reunião
  (`KMIsVEOcaLM` 246, `tb0nwpl9mFw` 142 e `p9wkMT4RV40` 69 inscritos); o 4º, na quarta da decisão (`dHYQtxnMSrw`, 421).
- **Custo:** a pauta de renda mensal de 03/11 ("Dividendos mensais de R$ 1.000…") vai para a quinta 05/11, 19h, que
  ficou livre com a saída do longo pós. A semana continua com 3 longos.

O Short de quarta 04/11 ("Copom hoje…") vira um corte do longo pré, com as taxas da manhã de quarta. No dia seguinte à
decisão não há vídeo novo: comunicado e reação das taxas vão num comentário fixado no longo de 03/11 e num post na
comunidade (quinta, depois da abertura do Tesouro Direto).

### Regra para 08-09/12 (fora da janela)

Medida: inscritos do longo pré de 03/11 nos 7 primeiros dias (Studio, de 03/11 a 09/11).

- **Se fizer 69 inscritos ou mais em 7 dias, repetir o pré:** longo na terça 08/12, 19h, e Short pós na quinta 10/12.
- **Se fizer menos de 69, testar o pós:** Short pré na quarta 09/12 e longo pós na quinta 10/12, 19h (versão pós do
  molde).
- **Por que 69:** é o total do pré-Copom mais fraco do ano (`p9wkMT4RV40`, setembro), medido com 16 dias de vida na
  exportação de 02/10. Passar disso em 7 dias é ficar acima do pior caso conhecido em menos da metade do tempo. O
  esperado do modelo é {br(te)} no vitalício.
- O padrão de 2027 sai da comparação das duas reuniões (inscritos e views intencionais de 7 dias), como no molde.

### Conferência das datas no BCB (03/10/2026)

- **Não consegui ler o calendário oficial.** A página
  https://www.bcb.gov.br/controleinflacao/calendarioreunioescopom responde (HTTP 200), mas é um app Angular. A rota
  `api/paginasite/sitebcb/controleinflacao/calendarioreunioescopom` devolve só o componente `bcb-pagina-tipo0`.
  O componente consulta `api/servico/sitebcb/hub?tipo='calendarioreunioescopom'&listsite=controleinflacao`, que voltou
  vazio (`{{"conteudo":[]}}`), assim como `paginatipo` e `conteudosite`.
- **Endpoints tentados na API do site:** `copom/calendario`, `copom/agenda`, `copom/reunioes`, `copom/calendarioreunioes`,
  `copom/proximasreunioes` e `copom/datasreunioes` deram HTTP 500; `calendariocopom` e `agendacopom` deram HTTP 400.
- **O que respondeu:** `copom/comunicados?quantidade=1` (281ª reunião, 16/09/2026) e `copom/atas?quantidade=1` (281ª,
  "15-16 setembro, 2026", ata em 22/09). Nenhum dos dois traz reuniões futuras.
- **Continua valendo "conferir no bcb.gov.br"** para 03-04/11 e 08-09/12. A fonte de hoje é a imprensa
  (`MOLDE-TESOURO-COPOM.md`, seção 6). Nenhum bloqueio foi contornado.

## Inscritos esperados (estimativa)

### v2 × v3

| | v2 | v3 | diferença |
|---|---|---|---|
| longos / Shorts nas 8 semanas | {nl2} / {ns2} | {nl} / {ns} | {nl - nl2:+d} / {ns - ns2:+d} |
| inscritos esperados (central) | {br(tot2)} | **{br(tot3)}** | **{'+' if tot3 >= tot2 else '−'}{br(abs(tot3 - tot2))}** |
| faixa p25–p75 | {br(sum(r['_e25'] for r in v2l))} a {br(sum(r['_e75'] for r in v2l))} | {br(sum(r['_e25'] for r in linhas))} a {br(sum(r['_e75'] for r in linhas))} | |

A conta, troca por troca, está na coluna "efeito" da tabela de trocas acima ({br(tot2)} do v2 + a soma dos efeitos
= {br(tot3)}).

### Contra a meta mensal (META.md)

Mesma conta do `META.md`: inscritos líquidos do mês = catálogo ({br(b['catalogo'])}) + vídeos novos − perdas
({br(b['perdas_6m'])}). Os vídeos novos entram com a defasagem do `meta.py` (60% no mês da publicação, 25% no seguinte e
15% no outro). Outubro conta só os vídeos da janela (de 05/10 em diante).

| mês | longos | Shorts | inscritos esperados dos vídeos do mês (vitalício) | entram no mês (com defasagem) | líquidos estimados | meta (META.md) | diferença |
|---|---|---|---|---|---|---|---|""")
    pm = por_mes(linhas)
    liq = liquidos_por_mes(b, pm)
    liq25 = liquidos_por_mes(b, pm, "e25")
    liq75 = liquidos_por_mes(b, pm, "e75")
    for m, x in pm.items():
        mt = metas[m]["liquidos"]
        out.append(f"| {m[5:]}/{m[2:4]} | {x['longos']} | {x['shorts']} | {br(x['e'])} ({br(x['e25'])}–{br(x['e75'])}) | "
                   f"{br(liq[m]['novos'])} | **{br(liq[m]['liquidos'])}** ({br(liq25[m]['liquidos'])}–"
                   f"{br(liq75[m]['liquidos'])}) | {br(mt)} | {'+' if liq[m]['liquidos'] >= mt else '−'}"
                   f"{br(abs(liq[m]['liquidos'] - mt))} |")
    acima = [m for m in pm if liq[m]["liquidos"] >= metas[m]["liquidos"]]
    p25_abaixo = [m for m in pm if liq25[m]["liquidos"] < metas[m]["liquidos"]]
    nomes = {"2026-10": "outubro", "2026-11": "novembro"}
    out.append(f"""
**Leitura:**
- Na estimativa central, {' e '.join(nomes[m] for m in acima) or 'nenhum mês'} {'fica' if len(acima) == 1 else 'ficam'} acima da
  meta mensal. Na faixa p25 (pessimista), {' e '.join(nomes[m] for m in p25_abaixo) or 'nenhum mês'}
  {'fica' if len(p25_abaixo) == 1 else 'ficam'} abaixo.
- Outubro tem {pm['2026-10']['longos']} longos na janela, mais o de 01/10 já publicado; o plano do `META.md` contava 9 (rampa de 75%).
- Uma parte dos inscritos de novembro chega em dezembro e janeiro (defasagem). Não conta aqui, mas entra na meta de
  dezembro ({br(metas['2026-12']['liquidos'])}).
- **Cenário pessimista:** se renda mensal e Tesouro renderem como a mediana geral dos longos ({br(geral)} por vídeo, e
  não {br(rm)} e {br(te)}), as 8 semanas ficam em ~{br(tot3 - sum(r['_e'] - geral for r in linhas if r['formato'] == L and r['assunto'] in ('renda mensal', 'tesouro e renda fixa')))}.
- **Risco do título provisório:** pela regra de assunto do título, os títulos provisórios do Ep. 2 e do Ep. 3 caem em
  "ações e empresas" ({br(ae)} por longo), não em renda mensal. Se o título final ficar assim e o vídeo render como o
  assunto do título, a série perde ~{br(2 * (rm - ae))}. A coluna `assunto_pelo_titulo` mostra isso.
- **Validação:** depois do Ep. 3 (28/10), comparar os inscritos de 7 dias dos 3 episódios com os {br(rm)} esperados.
  Se a mediana ficar abaixo de {br(geral)} (a mediana geral), rever a série antes do Ep. 4.

### Por semana

A meta semanal é o plano de vídeos novos de `META.md` ÷ 4,33, com a rampa de outubro (o mesmo do v2).

| semana | longos | Shorts | v2 | v3 (faixa p25–p75) | meta semanal de vídeos novos | v3 − meta |
|---|---|---|---|---|---|---|""")
    tm = 0.0
    for k, s in sem.items():
        ini_s = INICIO + timedelta(days=7 * k)
        mt = v2.meta_semanal_novos(p, f"{ini_s:%Y-%m}")
        tm += mt
        out.append(f"| {ini_s:%d/%m}–{(ini_s + timedelta(days=6)):%d/%m} | {s['longos']} | {s['shorts']} | "
                   f"{br(sem2[k]['e'])} | **{br(s['e'])}** ({br(s['e25'])}–{br(s['e75'])}) | {br(mt)} | "
                   f"{'+' if s['e'] >= mt else '−'}{br(abs(s['e'] - mt))} |")
    out.append(f"| **8 semanas** | {nl} | {ns} | {br(tot2)} | **{br(tot3)}** | {br(tm)} | "
               f"{'+' if tot3 >= tm else '−'}{br(abs(tot3 - tm))} |")

    out.append("""
## As 8 semanas

| data | formato | título | série | assunto | termo de busca real | Pesquisa 6 meses | continuação de | inscritos esperados (p25–p75) |
|---|---|---|---|---|---|---|---|---|""")
    ultima = None
    for r in linhas:
        k = semana(r["data"])
        if k != ultima:
            ini_s = INICIO + timedelta(days=7 * k)
            out.append(f"| **semana {k + 1} · {ini_s:%d/%m}–{(ini_s + timedelta(days=6)):%d/%m}** | | | | | | | | |")
            ultima = k
        tit = f"**{r['titulo']}**" + (" *(provisório)*" if r["serie_ep"] else "")
        out.append(f"| {_d(r['data'])} {r['dia']} | {r['formato']} | {tit} | {r['serie_ep'] or '—'} | {r['assunto']} | "
                   f"{r['termo_busca'] or '— (sem termo)'} | {r['views_pesquisa_6m'] or '—'} | "
                   f"{r['continuacao_de'] or '—'} | "
                   f"{br(r['_e'], 1 if r['formato'] == S else 0)} ({br(r['_e25'], 1)}–{br(r['_e75'], 1)}) |")
    out.append("""
**Regras:** longos às 19h; Shorts às segundas e quartas (e no dia do episódio, quando é o Short dele). Não recomendar
ativo nem citar corretora. Fora: dívida, cartão de crédito e política. Conferir as fontes antes de gravar.

## Ângulo e fontes de cada pauta
""")
    for r in linhas:
        out.append(f"- **{_d(r['data'])} · {r['titulo']}** ({r['origem']}) — {r['angulo']} *Conferir:* "
                   f"{r['fontes_a_conferir']}. *Esperado:* {r['base_do_esperado']}. *Busca:* {r['demanda']}.")
    return "\n".join(out) + "\n"


def main():
    d = mo.carregar()
    linhas, decisoes, fila, log = montar(d)
    with open(AQUI / "CALENDARIO.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLS, extrasaction="ignore")
        w.writeheader()
        w.writerows(linhas)
    (AQUI / "CALENDARIO.md").write_text(markdown(d, linhas, decisoes, fila, log), encoding="utf-8")
    nl = sum(1 for r in linhas if r["formato"] == L)
    print(f"ok: {len(linhas)} pautas ({nl} longos, {len(linhas) - nl} Shorts) em CALENDARIO.md e .csv; "
          f"{len(log)} trocas de trocas.json; {len(decisoes)} decisão(ões) da regra automática; fila: {len(fila)}")


if __name__ == "__main__":
    main()
