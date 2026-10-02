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
        self.rec = Counter(an.norm(r["termo"]) for r in self.recentes for _ in range(int(r["views"])))

    # -- números de um termo (ou de uma família de termos, por regex)
    def casar(self, padrao):
        rx = re.compile(padrao)
        todos = set(self.vit) | {t for d in self.mes.values() for t in d}
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
        o = self.origem.get(t)
        return o.most_common(1)[0][0] if o else None

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
        a = self.assunto(t)
        return "investimento" if a in FOCO else "outros"

    def texto_6m(self, termos):
        soma, pres, teto = self.seis_meses(termos)
        if pres == 6:
            return br(soma)
        if pres == 0:
            return f"fora do top 25 (≤ {br(teto)})"
        return f"{br(soma)} em {pres} {'mês' if pres == 1 else 'meses'} (+ ≤ {br(teto)} nos outros)"

    def linhas(self):
        todos = set(self.vit) | {t for d in self.mes.values() for t in d}
        out = []
        for t in todos:
            dono = self.dono(t)
            v = self.videos.get(dono, {}) if dono else {}
            soma, pres, teto = self.seis_meses([t])
            out.append({"termo": t, "categoria": self.categoria(t), "assunto": self.assunto(t),
                        "video": dono or "—", "ano": v.get("publicado_em_brt", "")[:4] or "—",
                        "seis_meses": soma, "meses_presente": pres, "teto": teto, "texto_6m": self.texto_6m([t]),
                        "vitalicio": self.vit.get(t, 0), "canal_total": self.mes.get("total", {}).get(t, 0)})
        return sorted(out, key=lambda r: (-r["seis_meses"], -r["vitalicio"]))


def br(x):
    return f"{x:,.0f}".replace(",", ".")


def markdown(T):
    L = T.linhas()
    amplos = [r for r in L if r["categoria"] == "amplo (1 centavo)"]
    bancos = [r for r in L if r["categoria"].startswith("bancos")]
    inv = sorted([r for r in L if r["categoria"] == "investimento"], key=lambda r: (-r["seis_meses"], -r["vitalicio"]))
    tot6 = sum(sum(d.values()) for m, d in T.mes.items() if m in MESES_6)
    amplo6 = sum(r["seis_meses"] for r in amplos)
    inv6 = sum(r["seis_meses"] for r in inv)
    cortes = " · ".join(f"{m[5:]}/{m[2:4]}: {T.corte[m]}" for m in MESES_6)
    out = [f"""# Termos de busca: o que o público procura e acha no canal

Gerado por `termos.py` a partir de `auditoria-canal/dados/termos_busca_canal.csv` (25 termos por mês, de out/25 a
set/26) e de `termos_busca_por_video.csv` (25 termos de cada um dos 50 vídeos com mais views da Pesquisa, no
vitalício).

**Limite dos dados:**
- **Corte mensal:** um termo fora do top 25 de um mês teve menos views que o 25º. Nos últimos 6 meses, o corte foi
  {cortes}.
- **Teto:** para um termo que nunca entrou no top 25, as views dos 6 meses são no máximo a soma desses cortes.

## Leitura (5 linhas)

1. **A busca do canal hoje é o Short do "1 centavo".** Nos últimos 6 meses, os termos amplos de dinheiro ("como ganhar
   dinheiro na internet", "como ficar rico" etc.) somam {br(amplo6)} das {br(tot6)} views dos top 25 mensais
   ({br(100 * amplo6 / tot6)}%). Eles quase não convertem: o Short traz cerca de 1 inscrito por mil views.
2. **Investimento quase não aparece nos top 25 recentes.** Os únicos termos de investimento nos últimos 6 meses são
   {', '.join(f'"{r["termo"]}" ({br(r["seis_meses"])})' for r in inv if r['seis_meses'])}: {br(inv6)} views ao todo.
3. **A demanda de investimento que o canal já captou é de cauda longa e está em vídeos antigos:**
   - LCI, LCA e CDB, com o Short de abr/25;
   - ETFs que pagam dividendos mensais (2024);
   - ETF de bitcoin (2024);
   - CDB prefixado (2018);
   - dividendos sintéticos (2022);
   - fundos imobiliários (2023);
   - "como juntar 1 milhão" (Shorts de 2022 e 2024).
4. **Tesouro, IPCA+, Copom e Selic não aparecem em nenhum termo**, nem no top 25 mensal nem nos 50 vídeos de busca. Os
   vídeos de Tesouro, que são os que mais trazem inscritos (TEMAS.md), vivem da página inicial, não da busca.
5. **Bancos e apps** (Next, Nubank, Banco Original, C6, Pix) ainda são o maior bloco do catálogo de busca, mas estão
   fora do foco. Para medir o que os vídeos de 2026 recebem de busca, falta rodar `exportar.py --termos-recentes 180`
   no Mac (comando no fim).

## Termos de investimento (fora o amplo e o catálogo de bancos)

| termo | assunto | vídeo que recebe a busca (ano) | Pesquisa, últimos 6 meses (top 25 do canal) | Pesquisa, vitalício (no vídeo) |
|---|---|---|---|---|"""]
    for r in inv[:60]:
        out.append(f"| {r['termo']} | {r['assunto']} | `{r['video']}` ({r['ano']}) | {r['texto_6m']} | {br(r['vitalicio'])} |")
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
## Para fechar a lacuna dos últimos 6 meses (no Mac)

```sh
cd ~/IPADTEST && git pull && cd auditoria-canal \\
  && set -a && source ~/.config/investirecocar/credentials.env && set +a \\
  && python3 exportar.py --termos-recentes 180 \\
  && cd .. && git add auditoria-canal/dados/termos_busca_recentes.csv auditoria-canal/dados/LEIAME_DADOS.md \\
  && git commit -m "auditoria-canal: termos de busca recentes" && git push
```

O comando pega os 25 termos de cada vídeo publicado nos últimos 180 dias e dos 50 com mais busca, só no período,
em cerca de 120 consultas ao Analytics. Com ele, a coluna dos 6 meses passa a vir por vídeo, e não do top 25 do canal,
que o "1 centavo" domina.
""")
    return "\n".join(out)


if __name__ == "__main__":
    T = Termos()
    (AQUI / "TERMOS.md").write_text(markdown(T), encoding="utf-8")
    print("ok: TERMOS.md")
