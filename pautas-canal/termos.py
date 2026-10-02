#!/usr/bin/env python3
"""Termos de busca reais (auditoria-canal/dados/termos_busca_*.csv) → TERMOS.md e funções para o calendário.

O que os dados têm (exportar.py --termos-busca, 02/10/2026):
  termos_busca_canal.csv      25 termos com mais views da Pesquisa por mês (out/25 a set/26) e no período todo;
  termos_busca_por_video.csv  25 termos de cada um dos 50 vídeos com mais views da Pesquisa (vitalício).
Limite: um termo que ficou fora do top 25 de um mês tem, naquele mês, menos views que o 25º (o "corte").

Classificação de cada termo:
  amplo (1 centavo)   o vídeo que recebeu a busca é o Short do "1 centavo" (aDL4MMF6AnE), ou o termo é genérico de
                      dinheiro ("como ganhar dinheiro", "como ficar rico", "renda extra"...);
  bancos e apps       catálogo antigo de bancos digitais, apps e assuntos fora do foco (Next, Nubank, Pix...);
  investimento        o resto, com o assunto dado por analisar.assunto(termo).
uso: python3 termos.py
"""
import csv
import re
from collections import Counter, defaultdict
from pathlib import Path

import modelo as mo
from modelo import an

AQUI = Path(__file__).resolve().parent
DADOS = mo.DADOS
SHORT_1_CENTAVO = "aDL4MMF6AnE"
MESES_6 = ["2026-04", "2026-05", "2026-06", "2026-07", "2026-08", "2026-09"]
AMPLOS = re.compile(r"ganhar dinheiro|fazer dinheiro|ficar rico|ser rico|^rico$|milionari|renda extra|conseguir dinheiro|"
                    r"economizar|guardar dinheiro|juntar dinheiro|multiplicar dinheiro|^dinheiro$|^investimentos?$|"
                    r"^como investir( dinheiro)?$|investir e cocar|ganhar muito dinheiro")
BANCOS = re.compile(r"\bnext|nubank|\bnu bank|original|\bc6|6c bank|picpay|pic pay|mercado pago|mercado coin|\bpix\b|"
                    r"\bpag\b|meu pag|agora invest|click conta|bradesco|banco inter|\binter\b|sousmile|sou smile|smilink|"
                    r"aparelho|veloe|taggy|sem parar|conectcar|\blula|humberto|apple pay|caixinha|cofrinho|"
                    r"\bconta\b|banco para menor|bancos? (digital|para)|cartao|cartão|me poupe|agibank|maxima|"
                    r"banco do brasil|caixa economica|itau|alo protegido|urubu|golpe")
FOCO = {"renda mensal", "tesouro e renda fixa", "FII", "ETF e exterior", "cripto", "ações e empresas",
        "imposto e regras", "juntar dinheiro e aposentadoria", "crise e macro", "commodities"}


def ler(nome):
    p = DADOS / nome
    return list(csv.DictReader(open(p, encoding="utf-8"))) if p.exists() else []


class Termos:
    def __init__(self):
        self.canal = ler("termos_busca_canal.csv")
        self.por_video = ler("termos_busca_por_video.csv")
        self.recentes = ler("termos_busca_recentes.csv")
        self.videos = {r["id"]: r for r in ler("videos.csv")}
        self.mes = defaultdict(dict)
        for r in self.canal:
            self.mes[r["periodo"]][an.norm(r["termo"])] = int(r["views"])
        self.corte = {p: min(d.values()) for p, d in self.mes.items() if d}
        self.vit = Counter()
        self.origem = defaultdict(Counter)
        for r in self.por_video:
            t = an.norm(r["termo"])
            self.vit[t] += int(r["views"])
            self.origem[t][r["video_id"]] += int(r["views"])
        self.rec = Counter()
        self.origem_rec = defaultdict(Counter)
        for r in self.recentes:
            t = an.norm(r["termo"])
            self.rec[t] += int(r["views"])
            self.origem_rec[t][r["video_id"]] += int(r["views"])

    # -- números de um termo (ou de uma família de termos, por regex)
    def casar(self, padrao):
        rx = re.compile(padrao)
        todos = set(self.vit) | set(self.rec) | {t for d in self.mes.values() for t in d}
        return sorted(t for t in todos if rx.search(t))

    def seis_meses(self, termos):
        """(views conhecidas nos meses em que algum termo entrou no top 25, nº de meses presentes, teto se ausente)."""
        soma, presentes, teto = 0, 0, 0
        for m in MESES_6:
            v = sum(self.mes[m].get(t, 0) for t in termos)
            if v:
                soma += v
                presentes += 1
            else:
                teto += self.corte.get(m, 0)
        return soma, presentes, teto

    def vitalicio(self, termos):
        return sum(self.vit.get(t, 0) for t in termos)

    def recentes_views(self, termos):
        return sum(self.rec.get(t, 0) for t in termos) if self.recentes else None

    def dono(self, t):
        o = self.origem.get(t) or self.origem_rec.get(t)
        return o.most_common(1)[0][0] if o else None

    def dono_recente(self, t):
        o = self.origem_rec.get(t)
        return o.most_common(1)[0][0] if o else None

    def assunto_termo(self, t):
        """Ticker sozinho ('trxf11', 'rara11', 'suzb3') herda o assunto do título do vídeo que recebe a busca."""
        if re.fullmatch(r"[a-z]{4}\d{1,2}", t):
            vid = self.dono_recente(t) or self.dono(t)
            tit = self.videos.get(vid, {}).get("titulo", "") if vid else ""
            if tit:
                return an.assunto(tit)
        return self.assunto(t)

    @staticmethod
    def assunto(t):
        """analisar.assunto com dois ajustes para termos curtos: tickers de ETF terminados em 11 e opções."""
        if re.search(r"\b(spyi|qqqi|hash|qbtc|bith|coin|bova|ndiv|divd|ivvb|nasd|gold|ethe)11\b", t):
            return "cripto" if re.search(r"hash|qbtc|bith|coin|ethe", t) else "ETF e exterior"
        if re.search(r"\bopcoe?s\b|opcoes", t) and "dividend" not in t:
            return "ações e empresas"
        return an.assunto(t)

    def categoria(self, t):
        dono = self.dono(t)
        if dono == SHORT_1_CENTAVO or AMPLOS.search(t):
            return "amplo (1 centavo)"
        if BANCOS.search(t):
            return "bancos, apps e outros (catálogo)"
        dono_rec = self.dono_recente(t)
        if dono_rec == SHORT_1_CENTAVO:
            return "amplo (1 centavo)"
        a = self.assunto_termo(t)
        return "investimento" if a in FOCO else "outros"

    def texto_6m(self, termos):
        if self.recentes:
            return br(self.recentes_views(termos))
        soma, pres, teto = self.seis_meses(termos)
        if pres == 6:
            return br(soma)
        if pres == 0:
            return f"fora do top 25 (≤ {br(teto)})"
        return f"{br(soma)} em {pres} {'mês' if pres == 1 else 'meses'} (+ ≤ {br(teto)} nos outros)"

    def linhas(self):
        todos = set(self.vit) | set(self.rec) | {t for d in self.mes.values() for t in d}
        out = []
        for t in todos:
            dono = self.dono(t)
            v = self.videos.get(dono, {}) if dono else {}
            soma, pres, teto = self.seis_meses([t])
            vr = self.dono_recente(t)
            out.append({"termo": t, "categoria": self.categoria(t), "assunto": self.assunto_termo(t),
                        "recente": self.rec.get(t, 0), "video_rec": vr or "—",
                        "titulo_rec": self.videos.get(vr, {}).get("titulo", "")[:55] if vr else "",
                        "pub_rec": self.videos.get(vr, {}).get("publicado_em_brt", "")[:10] if vr else "",
                        "video": dono or "—", "ano": v.get("publicado_em_brt", "")[:4] or "—",
                        "seis_meses": soma, "meses_presente": pres, "teto": teto, "texto_6m": self.texto_6m([t]),
                        "vitalicio": self.vit.get(t, 0), "canal_total": self.mes.get("total", {}).get(t, 0)})
        return sorted(out, key=lambda r: (-r["seis_meses"], -r["vitalicio"]))


def br(x):
    return f"{x:,.0f}".replace(",", ".")


def familias(T):
    """Views recentes (desde 04/04) e vitalícias por família de assunto de investimento."""
    fams = [("Tesouro Direto e IPCA+", r"tesouro|ipca|\bntn"), ("LCI, LCA e CDB", r"\blci|\blca|\bcdb"),
            ("ETFs e dividendos mensais", r"etfs?.*dividend|dividendos? mensa"), ("FII (incl. tickers de FII)", None),
            ("ações por ticker", None), ("Barsi", r"barsi"), ("juntar 1 milhão", r"1 milh|um milh|primeiro milh"),
            ("bitcoin e cripto", r"bitcoin|cripto|\bbtc"), ("bolha da IA", r"bolha (da |de )?ia"),
            ("Copom e Selic", r"copom|selic"), ("crise e recessão", r"crise|recess")]
    out = []
    for nome, rx in fams:
        if nome.startswith("FII"):
            ts = [t for t in set(T.rec) | set(T.vit) if T.categoria(t) == "investimento" and T.assunto_termo(t) == "FII"]
        elif nome == "ações por ticker":
            ts = [t for t in set(T.rec) | set(T.vit) if re.fullmatch(r"[a-z]{4}[3-6]", t)]
        else:
            ts = [t for t in T.casar(rx) if not T.categoria(t).startswith("amplo")]
        out.append((nome, T.recentes_views(ts) or 0, T.vitalicio(ts), len(ts)))
    return sorted(out, key=lambda x: -x[1])


def markdown(T):
    L = T.linhas()
    amplos = [r for r in L if r["categoria"] == "amplo (1 centavo)"]
    bancos = [r for r in L if r["categoria"].startswith("bancos")]
    inv = sorted([r for r in L if r["categoria"] == "investimento"], key=lambda r: (-r["seis_meses"], -r["vitalicio"]))
    rec_tot = sum(T.rec.values())
    cat_rec = Counter()
    for t, v in T.rec.items():
        cat_rec[T.categoria(t)] += v
    top = sorted([r for r in L if r["categoria"] == "investimento" and r["recente"]], key=lambda r: -r["recente"])[:20]
    desde = T.recentes[0]["desde"] if T.recentes else "—"
    nvid = len({r["video_id"] for r in T.recentes})
    out = [f"""# Termos de busca: o que o público procura e acha no canal

Gerado por `termos.py` a partir de três exportações de `auditoria-canal/dados/`:
- **`termos_busca_recentes.csv`:** 25 termos por vídeo, de {desde} a 01/10/2026, em {nvid} vídeos (os publicados no
  período e os 50 com mais busca). **É a fonte dos "últimos 6 meses".**
- **`termos_busca_por_video.csv`:** 25 termos de cada um dos 50 vídeos com mais busca, no vitalício.
- **`termos_busca_canal.csv`:** 25 termos do canal por mês, de out/25 a set/26.

**Filtros**, iguais aos de antes:
- fora os termos que chegam pelo Short do "1 centavo";
- fora os genéricos de dinheiro ("como ganhar dinheiro"...);
- fora os de bancos e apps do catálogo (Next, Nubank, Pix...).
- Um ticker sozinho ("trxf11", "suzb3") herda o assunto do vídeo que recebe a busca.

## Leitura (5 linhas)

1. **O "1 centavo" ainda domina:** desde {desde}, {br(cat_rec['amplo (1 centavo)'])} das {br(rec_tot)} views da Pesquisa
   ({br(100 * cat_rec['amplo (1 centavo)'] / rec_tot)}%) vêm dele e dos termos amplos. Investimento soma {br(cat_rec['investimento'])}
   ({br(100 * cat_rec['investimento'] / rec_tot)}%); bancos e apps, {br(cat_rec['bancos, apps e outros (catálogo)'])}.
2. **Tesouro agora aparece.** "tesouro direto", "ipca + 8", "tesouro ipca" e "tesouro ipca+ 2032" somam ~1 mil views
   no período, quase todas no vídeo de jun/26 (KMIsVEOcaLM). Ficam atrás de tickers de ações, FII, LCI/LCA/CDB e
   Barsi (tabela de famílias). **Copom e Selic quase não são buscados** (15 views).
3. **Tickers são a busca recente mais forte de investimento:**
   - o FII trxf11 (1.516, o termo nº 1, do vídeo de ago/26);
   - ações (pass3, suzb3, saud3, rani3, bbas3), todas em vídeos de 2026.
   - Quem busca o ticker acha o vídeo do canal sobre aquele ativo, e isso é demanda de cauda longa. Mas ações rendem
     poucos inscritos por vídeo (TEMAS.md).
4. **ETFs que pagam dividendos mensais seguem com demanda** (~420 views no período, pelo vídeo de 2024). Barsi e
   "juntar 1 milhão" também, em vídeos antigos.
5. **Crise, recessão, bitcoin, ETF de bitcoin, dividendos sintéticos e CDB prefixado quase não têm busca recente**
   (de 3 a 56 views). Esses assuntos vivem de Navegação (crise) ou de vídeos antigos (CDB prefixado, 2018).

## Top 20 termos de investimento nos últimos 6 meses ({desde} a 01/10/2026)

| # | termo | assunto | views da Pesquisa no período | vídeo que recebe a busca |
|---|---|---|---|---|"""]
    for k, r in enumerate(top, 1):
        out.append(f"| {k} | {r['termo']} | {r['assunto']} | {br(r['recente'])} | `{r['video_rec']}` ({r['pub_rec']}) {r['titulo_rec']} |")
    out.append("""
## Famílias de investimento: período × vitalício

| família | views no período | views no vitalício (50 vídeos de busca) | termos |
|---|---|---|---|""")
    for nome, rec, vit, n in familias(T):
        out.append(f"| {nome} | {br(rec)} | {br(vit)} | {n} |")
    out.append("""
## Termos de investimento: tabela completa (os 60 maiores no período)

| termo | assunto | vídeo que recebe a busca (ano) | Pesquisa, últimos 6 meses (por vídeo) | Pesquisa, vitalício (no vídeo) |
|---|---|---|---|---|""")
    inv = sorted(inv, key=lambda r: (-r["recente"], -r["vitalicio"]))
    for r in inv[:60]:
        out.append(f"| {r['termo']} | {r['assunto']} | `{r['video']}` ({r['ano']}) | {br(r['recente'])} | {br(r['vitalicio'])} |")
    out.append("""
## Termos que são pergunta curta → o Short (ou longo) do calendário v2 que responde

| termo | views da Pesquisa (vitalício) | categoria | pauta do calendário v2 |
|---|---|---|---|""")
    import calendario_v2 as cal
    titulos = {p_[0]: (p_[1], p_[3]) for p_ in cal.PAUTAS}
    perg = [r for r in L if not r["categoria"].startswith("amplo") and r["vitalicio"] >= 40
            and re.search(r"^(o ?que|como|qual|quais|quanto|quando|onde|vale a pena)\b|vale a pena$|\bou\b", r["termo"])
            and r["categoria"] == "investimento"]
    for r in sorted(perg, key=lambda r: -r["vitalicio"])[:25]:
        alvo = [d_ for d_, (t_, fam) in cal.TERMOS.items() if re.search(fam, r["termo"])]
        alvo.sort(key=lambda d_: (titulos[d_][0] != "short", d_))
        txt = (f"{alvo[0][8:]}/{alvo[0][5:7]} ({titulos[alvo[0]][0]}): {titulos[alvo[0]][1]}" if alvo
               else "sem pauta: candidato a Short")
        out.append(f"| {r['termo']} | {br(r['vitalicio'])} | {r['assunto']} | {txt} |")
    out.append(f"""
## Termos amplos (Short do "1 centavo" e genéricos de dinheiro): os 15 maiores

| termo | vídeo | Pesquisa, últimos 6 meses | vitalício (no vídeo) |
|---|---|---|---|""")
    for r in sorted(amplos, key=lambda r: -r["seis_meses"])[:15]:
        out.append(f"| {r['termo']} | `{r['video']}` | {r['texto_6m']} | {br(r['vitalicio'])} |")
    out.append(f"""
## Bancos, apps e outros do catálogo antigo: os 15 maiores (fora do foco)

| termo | vídeo (ano) | Pesquisa, últimos 6 meses | vitalício |
|---|---|---|---|""")
    for r in sorted(bancos, key=lambda r: -(r["seis_meses"] * 100 + r["vitalicio"]))[:15]:
        out.append(f"| {r['termo']} | `{r['video']}` ({r['ano']}) | {r['texto_6m']} | {br(r['vitalicio'])} |")
    out.append("""
**Para atualizar**, rode `exportar.py --termos-recentes 180` no Mac, como na última vez, suba o
`termos_busca_recentes.csv` e regere com `python3 termos.py && python3 calendario_v2.py`.
""")
    return "\n".join(out)


if __name__ == "__main__":
    T = Termos()
    (AQUI / "TERMOS.md").write_text(markdown(T), encoding="utf-8")
    print("ok: TERMOS.md")
