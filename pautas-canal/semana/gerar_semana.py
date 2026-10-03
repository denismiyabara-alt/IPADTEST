#!/usr/bin/env python3
"""Pacote da semana: tudo o que sai de segunda a domingo, num arquivo só, para o Denis aprovar de uma vez.

Uso (todo domingo, até as 10h):
    python3 pautas-canal/semana/gerar_semana.py 2026-10-04
        -> pautas-canal/semana/2026-10-04.md (semana de seg 05/10 a dom 11/10)

Fontes (só leitura; biblioteca padrão):
- Investir e Coçar: pautas-canal/CALENDARIO.csv, pautas-canal/roteiros/, pautas-canal/briefings/
- Decisões abertas fixas: pautas-canal/semana/decisoes_abertas.csv (marque status=resolvida quando o Denis decidir)
- Faz a Conta: pautas-canal/semana/faz_a_conta_agenda.csv + repo faz-a-conta (TITULO.md, descricao.txt, roteiro.md)
- Shorts Barsi Perene e Louise: repo barsi-cortes (agenda_lote*.tsv; agenda da Louise, se existir)
- Cards X/IG: esteira-social/cards/INDICE.csv
- Canais dark: canais-dark/historia-brasil/ e canais-dark/espionagem/
"""
import argparse
import csv
import json
import os
import re
import subprocess
import sys
from datetime import date, timedelta
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parents[1]
DIAS = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
OK, REV, FALTA = "✅", "⏳", "❌"
MAX = 150  # caracteres por item

CANAIS_DARK = [("historia-brasil", "História do Brasil com humor (piloto)"),
               ("espionagem", "Espionagem, Ep. 1 \"A captura de Eichmann (1960)\" (piloto)")]


# ---------------------------------------------------------------- utilidades
def semana(domingo):
    seg = domingo + timedelta(days=1)
    return seg, domingo + timedelta(days=7)


def dia(d):
    return f"{DIAS[d.weekday()]} {d:%d/%m}"


def curto(txt, n=MAX):
    t = re.sub(r"\*\*|`|__", "", txt)
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)
    t = re.sub(r"\s+", " ", t).strip(" -—")
    return t if len(t) <= n else t[: n - 1].rstrip(" ,;:") + "…"


def versao_num(txt):
    """Maior versão citada no texto ('v1.5 ... v1.7' -> (1, 7); 'v5' -> (5,))."""
    vs = [tuple(int(x) for x in m.split(".")) for m in re.findall(r"\bv(\d+(?:\.\d+)?)", txt or "")]
    return max(vs) if vs else None


def vtxt(v):
    return "v" + ".".join(map(str, v)) if v else "?"


def frontmatter(texto):
    m = re.match(r"---\n(.*?)\n---", texto, re.S)
    campos = {}
    if m:
        for linha in m.group(1).splitlines():
            mm = re.match(r"([A-Za-z_]+):\s*(.*)", linha)
            if mm:
                campos[mm.group(1)] = mm.group(2).strip().strip('"')
    return campos


def git_show(repo, ref, caminho):
    if not ref:
        return None
    try:
        r = subprocess.run(["git", "-C", str(repo), "show", f"{ref}:{caminho}"],
                           capture_output=True, text=True, timeout=20)
        return r.stdout if r.returncode == 0 else None
    except (OSError, subprocess.SubprocessError):
        return None


def ler(repo, caminho, ref=None):
    """Lê do ref do git (se der) ou do disco. None se não existir."""
    t = git_show(repo, ref, caminho)
    if t is not None:
        return t
    p = Path(repo) / caminho
    return p.read_text(encoding="utf-8") if p.is_file() else None


def achar_repo(nome, explicito=None):
    cands = [explicito, os.environ.get(nome.upper().replace("-", "_") + "_DIR")]
    try:
        comum = subprocess.run(["git", "-C", str(RAIZ), "rev-parse", "--path-format=absolute", "--git-common-dir"],
                               capture_output=True, text=True, timeout=10).stdout.strip()
        if comum:
            cands.append(Path(comum).parent.parent / nome)
    except (OSError, subprocess.SubprocessError):
        pass
    cands += [RAIZ.parent / nome, Path.home() / nome, Path("/home/user") / nome]
    for c in cands:
        if c and Path(c).is_dir():
            return Path(c)
    return None


def rel(alvo):
    return os.path.relpath(alvo, AQUI).replace(os.sep, "/")


# ---------------------------------------------------------------- pendências
def secoes(texto):
    """[(titulo, nivel, corpo)] por cabeçalho markdown."""
    partes, atual = [], None
    for linha in texto.splitlines():
        m = re.match(r"(#{1,4})\s+(.*)", linha)
        if m:
            atual = [m.group(2), len(m.group(1)), []]
            partes.append(atual)
        elif atual:
            atual[2].append(linha)
    return [(t, n, "\n".join(c)) for t, n, c in partes]


def itens_lista(corpo):
    """Itens numerados ou com marcador, juntando as linhas de continuação."""
    itens, atual, codigo = [], None, False
    for linha in corpo.splitlines():
        if linha.strip().startswith("```"):
            codigo = not codigo  # bloco de código: não entra no resumo do item
            continue
        if codigo:
            continue
        if re.match(r"(\d+\.|-|\*)\s+", linha):
            atual = [re.sub(r"^(\d+\.|-|\*)\s+", "", linha)]
            itens.append(atual)
        elif atual and linha.startswith((" ", "\t")) and linha.strip() and not linha.strip().startswith("```"):
            atual.append(linha.strip())
        elif not linha.strip() or linha.startswith("```") or linha.startswith("|"):
            atual = None
    return [" ".join(i) for i in itens]


def eh_tarefa(txt):
    return bool(re.match(r"\s*(\*\*)?(Rodar|Atualizar)", txt) or re.search(r"\brodar\b|\bno Mac\b", txt, re.I))


def pendencias(texto, versao_atual=None):
    """Validações pendentes do Denis num roteiro/notas/briefing.
    Retorna [(tipo, texto)] com tipo 'validar' ou 'tarefa'."""
    achados = []
    # 1. frontmatter: pendente_do_denis com "[ ]"
    for m in re.finditer(r'^\s*-\s*"?\[ \]\s*(.*?)"?\s*$', texto.split("\n---", 2)[0] if texto.startswith("---") else "", re.M):
        achados.append(m.group(1))
    # 2. seções de validação
    for titulo, _, corpo in secoes(texto):
        if re.search(r"Valida[çc][õo]es.*Denis|O que fica pro Denis", titulo, re.I):
            achados += itens_lista(corpo)
    # 3. frases soltas
    for m in re.finditer(r"\*\*(?:Denis valida|Validação do Denis):\*\*\s*(.+?)(?:\n\s*\n|$)", texto, re.S):
        achados.append(m.group(1))
    for m in re.finditer(r"^Validação nova do Denis:\s*(.+)$", texto, re.M):
        achados.append(m.group(1))
    saida, vistos = [], set()
    for a in achados:
        a = a.strip()
        if not a or re.match(r"(\*\*)?Resolvid", a):
            continue
        v = versao_num(a)
        if versao_atual and v and v < versao_atual and eh_tarefa(a):
            continue  # tarefa de versão já superada
        chave = curto(a, 60).lower()
        if chave in vistos:
            continue
        vistos.add(chave)
        saida.append(("tarefa" if eh_tarefa(a) else "validar", a))
    return saida


def ouvinte(texto):
    """Último teste do ouvinte: (versão ouvida, 'passou'/'reprovou', média)."""
    melhor = None
    linhas = texto.splitlines()
    for i, l in enumerate(linhas):
        if l.startswith("#") and re.search(r"uvinte-frio", l, re.I):
            m1 = re.search(r"\bv(\d+(?:\.\d+)?)", l)  # a versão ouvida é a 1ª do cabeçalho
            v = tuple(int(x) for x in m1.group(1).split(".")) if m1 else None
            janela = " ".join(linhas[i:i + 4])
            res = "reprovou" if re.search(r"REPROV", janela) else ("passou" if re.search(r"PASSA|PASSOU", janela) else None)
            media = re.search(r"[Mm]édia (\d+,\d+)", janela)
            if v and res and (melhor is None or v >= melhor[0]):
                melhor = (v, res, media.group(1) if media else None)
    return melhor


def juiz(texto):
    nota = None
    linhas = texto.splitlines()
    for i, l in enumerate(linhas):
        if l.startswith("#") and re.search(r"Juiz-roteiro", l, re.I):
            m = re.search(r"\b(\d+)/10\b", " ".join(linhas[i:i + 3]))
            if m:
                nota = m.group(1)
    return nota


# ---------------------------------------------------------------- Investir e Coçar
def roteiros_da_data(d, short=False):
    pasta = RAIZ / "pautas-canal" / "roteiros"
    prin, extras = None, []
    for p in sorted(pasta.glob(f"{d.isoformat()}-*.md")):
        if p.name.endswith("-short.md") != short:
            continue
        if re.search(r"-(notas|CONFERENCIA|EMPACOTAMENTO)\.md$", p.name):
            extras.append(p)
        else:
            prin = prin or p
    return prin, extras


def briefing_da_data(d, fm=None):
    if fm and fm.get("briefing"):
        cam = fm["briefing"].split(" ")[0]
        for base in (RAIZ, RAIZ / "pautas-canal"):
            if (base / cam).is_file():
                return base / cam
    ps = sorted((RAIZ / "pautas-canal" / "briefings").glob(f"{d.isoformat()}-*briefing*.md"))
    return ps[0] if ps else None


def investir(seg, dom, abafa=None):
    linhas, decidir, tarefas = [], [], []
    cal = RAIZ / "pautas-canal" / "CALENDARIO.csv"
    with open(cal, encoding="utf-8") as f:
        itens = [r for r in csv.DictReader(f) if seg.isoformat() <= r["data"] <= dom.isoformat()]
    itens.sort(key=lambda r: (r["data"], r["formato"] != "longo"))
    for r in itens:
        d = date.fromisoformat(r["data"])
        fmt = "Longo" if r["formato"] == "longo" else "Short"
        cab = f"**{dia(d)} · {fmt}** — {r['titulo']}"
        if r.get("serie_ep"):
            cab += f" _({r['serie_ep']})_"
        if r["formato"] != "longo":
            rs, _ = roteiros_da_data(d, short=True)
            if not rs:
                linhas.append(f"- {cab} — {FALTA} falta roteiro (só a pauta) · [pauta](../SHORTS-MES.md)")
                continue
            vs = versao_num(frontmatter(rs.read_text(encoding="utf-8")).get("versao", ""))
            vtx = f"roteiro v{vs}" if vs else "roteiro escrito"
            linhas.append(f"- {cab} — {REV} {vtx}, falta ouvinte-frio na versão final · [roteiro]({rel(rs)})")
            continue
        rot, extras = roteiros_da_data(d)
        brief = briefing_da_data(d)
        if not rot:
            st = f"{FALTA} falta roteiro" + (f" · [briefing]({rel(brief)})" if brief else " e briefing")
            linhas.append(f"- {cab} — {st}")
            if brief:
                for tipo, t in pendencias(brief.read_text(encoding="utf-8")):
                    if abafa and abafa.search(t):
                        continue
                    (tarefas if tipo == "tarefa" else decidir).append((dia(d), t, rel(brief)))
            continue
        texto = rot.read_text(encoding="utf-8")
        fm = frontmatter(texto)
        notas = [p for p in extras if p.name.endswith("-notas.md")]
        tudo = texto + "\n" + "\n".join(p.read_text(encoding="utf-8") for p in notas)
        v = versao_num(fm.get("versao", ""))
        brief = briefing_da_data(d, fm)
        pend = [x for x in pendencias(tudo, v) if not (abafa and abafa.search(x[1]))]
        ouv, nota = ouvinte(tudo), juiz(tudo)
        partes = [f"roteiro {vtxt(v)}"]
        if nota:
            partes.append(f"juiz {nota}/10")
        pronto = True
        if ouv:
            vo, res, media = ouv
            m = f" ({media})" if media else ""
            if vo < (v or vo):
                partes.append(f"ouvinte {res} a {vtxt(vo)}{m}: falta ouvir a {vtxt(v)}")
                pronto = False
            else:
                partes.append(f"ouvinte {res} a {vtxt(vo)}{m}")
                pronto = pronto and res == "passou"
        else:
            partes.append("sem teste do ouvinte")
            pronto = False
        nval = sum(1 for t, _ in pend if t == "validar")
        if nval:
            partes.append(f"{nval} conferências suas (topo)")
            pronto = False
        links = [f"[roteiro]({rel(rot)})"] + [f"[notas]({rel(p)})" for p in notas]
        if brief:
            links.append(f"[briefing]({rel(brief)})")
        linhas.append(f"- {cab} — {OK if pronto else REV} " + " · ".join(partes) + " · " + " ".join(links))
        destino = rel(notas[0]) if notas else rel(rot)
        for tipo, t in pend:
            (tarefas if tipo == "tarefa" else decidir).append((dia(d), t, destino))
    if not itens:
        linhas.append("- nada no calendário nesta semana")
    return linhas, decidir, tarefas


def decisoes_fixas():
    p = AQUI / "decisoes_abertas.csv"
    if not p.is_file():
        return [], []
    with open(p, encoding="utf-8") as f:
        todas = list(csv.DictReader(f))
    abertas = [r for r in todas if r["status"].strip().lower() == "aberta"]
    # resolvida também abafa: as cópias nos roteiros/notas viram ruído depois da decisão
    cobre = [r["cobre"] for r in todas if r.get("cobre")]
    return abertas, cobre


# ---------------------------------------------------------------- Faz a Conta
def faz_a_conta(seg, dom, repo, ref):
    p = AQUI / "faz_a_conta_agenda.csv"
    with open(p, encoding="utf-8") as f:
        agenda = list(csv.DictReader(f))
    linhas, fila = [], []
    if repo is None:
        linhas.append(f"- {FALTA} repo faz-a-conta não encontrado nesta máquina (passe --faz-a-conta CAMINHO)")
    for r in agenda:
        d = date.fromisoformat(r["data"])
        ep = r["episodio"]
        if dom < d <= dom + timedelta(days=7):
            fila.append(f"{dia(d)} {ep}")
        if not (seg <= d <= dom) or repo is None:
            continue
        tit_md = ler(repo, f"{ep}/TITULO.md", ref)
        desc = ler(repo, f"{ep}/descricao.txt", ref)
        rot = ler(repo, f"{ep}/roteiro.md", ref)
        titulo = None
        if tit_md:
            m = re.search(r"\*\*(.+?)\*\*\s*\(recomendado\)", tit_md)
            titulo = m.group(1) if m else None
        resumo = curto(desc.strip().splitlines()[0], 110) if desc and desc.strip() else None
        falta = []
        if not rot:
            falta.append("roteiro")
        else:
            n = len(re.findall(r"\|\s*a conferir\s*\|", rot))
            if n:
                falta.append(f"{n} números a conferir")
        if not tit_md:
            falta.append("título")
        if not desc:
            falta.append("descrição")
        gravado = any((repo / ep).glob("*.mp4")) if (repo / ep).is_dir() else False
        if r["status"].strip() == "agendado":
            st = f"{OK} agendado {r['horario']}".rstrip()
        elif gravado:
            st = f"{REV} gravado, falta agendar"
        else:
            st = f"{FALTA} pendente: falta " + ", ".join(falta + ["gerar o vídeo"])
        nome = titulo or ep
        linhas.append(f"- **{dia(d)}** — {nome} — {st}" + (f" · _{resumo}_" if resumo else "")
                      + f" · `faz-a-conta/{ep}/`")
    if fila:
        linhas.append(f"- Semana seguinte: " + " · ".join(fila))
    return linhas


# ---------------------------------------------------------------- Barsi Perene e Louise
def barsi(seg, dom, repo, ref):
    if repo is None:
        return [f"- {FALTA} repo barsi-cortes não encontrado nesta máquina"], [
            "- agenda não encontrada no repo — onde fica?"]
    nomes = sorted({p.name for p in repo.glob("agenda*.tsv")})
    por_dia = {}
    for nome in nomes:
        if "louise" in nome.lower():
            continue
        texto = ler(repo, nome, ref) or ""
        for l in texto.splitlines():
            c = l.split("\t")
            m = re.match(r"(\d\d)/(\d\d)\s+(\d+h)", c[0]) if c else None
            if not m or len(c) < 2:
                continue
            mes = int(m.group(2))
            ano = seg.year + (1 if mes < seg.month - 6 else 0)  # agenda sem ano: dezembro -> janeiro
            d = date(ano, mes, int(m.group(1)))
            if not (seg <= d <= dom):
                continue
            ident = c[1].strip()
            titulo = c[2].strip() if len(c) > 2 else ""
            if not ident or "PENDENTE" in l.upper():
                st = FALTA
            elif "@" in ident:
                st = REV
            else:
                st = OK
            curto_t = re.sub(r"\s*#shorts.*$", "", titulo)
            por_dia.setdefault(d, {})[m.group(3)] = (st, curto(curto_t, 48))
    bl = []
    for d in sorted(por_dia):
        slots = por_dia[d]
        sts = {s for s, _ in slots.values()}
        geral = FALTA if FALTA in sts else (REV if REV in sts else OK)
        bl.append(f"- **{dia(d)}** {geral} " + " · ".join(f"{h} {t}" for h, (_, t) in sorted(slots.items())))
    if not bl:
        bl.append("- agenda não encontrada no repo — onde fica?")
    else:
        bl.append(f"  _{OK} já subido e agendado · {REV} cortado, falta subir · {FALTA} vaga sem corte. "
                  f"Fonte: `barsi-cortes/agenda_lote*.tsv`_")
    # Louise: agenda fixa em pautas-canal/semana/louise_agenda.csv (decisão de 03/10/2026)
    ag = RAIZ / "pautas-canal" / "semana" / "louise_agenda.csv"
    if ag.is_file():
        with ag.open(encoding="utf-8") as f:
            rows = [r for r in csv.DictReader(f) if seg.isoformat() <= r["data"] <= dom.isoformat()]
        if rows:
            st_map = {"agendado": OK, "subido": OK, "a subir": REV}
            lou = [f"- **{dia(date.fromisoformat(r['data']))}** {st_map.get(r['status'], FALTA)} {r['hora']} "
                   f"{r['corte']} ({r['status']})" for r in rows]
            lou.append(f"  _Canal {rows[0]['canal']}. Fonte: `pautas-canal/semana/louise_agenda.csv`_")
            return bl, lou
    lo = [p for p in repo.rglob("*") if p.is_file() and "louise" in p.name.lower()
          and re.search(r"agenda|fila|calend", p.name, re.I) and ".git" not in p.parts]
    if lo:
        lou = [f"- agenda em `{p.relative_to(repo)}` (formato ainda não lido pelo gerador)" for p in lo]
    else:
        lou = ["- agenda não encontrada no repo — onde fica?"]
        pk = repo / "picks" / "louise_lote1.json"
        if pk.is_file():
            try:
                n = len(json.loads(pk.read_text(encoding="utf-8")))
                lou.append(f"- {REV} {n} cortes escolhidos sem data (`barsi-cortes/picks/louise_lote1.json`)")
            except (ValueError, TypeError):
                pass
    return bl, lou


# ---------------------------------------------------------------- Cards X/IG
def cards(seg, dom):
    p = RAIZ / "esteira-social" / "cards" / "INDICE.csv"
    if not p.is_file():
        return [f"- {FALTA} esteira-social/cards/INDICE.csv não encontrado"]
    with open(p, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    s, e = seg.isoformat(), dom.isoformat()
    out = []
    for r in rows:
        datas = [r.get("instagram_data", ""), r.get("x_data", "")]
        if not any(s <= x <= e for x in datas if x):
            continue
        gate = r.get("gate_resultado", "")
        jp, lf = r.get("juiz_post", ""), r.get("leitor_frio", "")
        if gate.upper().startswith("BLOQ") or r.get("autoexame", "OK") != "OK":
            st = f"{FALTA} barrado na checagem"
        elif jp.upper().startswith("APROV") and lf.upper().startswith("PASS"):
            st = f"{OK} aprovado"
        else:
            st = f"{REV} checagem {gate or '?'}, falta juiz e leitor"
        d_ig = date.fromisoformat(r["instagram_data"]) if r.get("instagram_data") else None
        d_x = date.fromisoformat(r["x_data"]) if r.get("x_data") else None
        quando = f"IG {d_ig:%d/%m} {r.get('instagram_horario', '')}" if d_ig else ""
        if d_x:
            quando += f" · X {d_x:%d/%m} {r.get('x_horario', '')}"
        out.append(f"- **{quando.strip(' ·')}** — {curto(r.get('mensagem_capa', ''), 95)} — {st} · "
                   f"[card](../../esteira-social/cards/{r['arquivo']})")
    return out or ["- nenhum card nesta semana"]


# ---------------------------------------------------------------- Canais dark
def canais_dark():
    out = []
    base = RAIZ / "canais-dark"
    for pasta, nome in CANAIS_DARK:
        p = base / pasta
        if not p.is_dir() or not any(p.iterdir()):
            out.append(f"- **{nome}** — {REV} em produção (pasta `canais-dark/{pasta}/` ainda não existe)")
            continue
        arquivos = [x for x in p.rglob("*") if x.is_file()]
        tem = lambda pad: [x for x in arquivos if re.search(pad, x.name, re.I)]  # noqa: E731
        roteiro, como, voz, conf = tem(r"roteiro"), tem(r"COMO-RODAR"), tem(r"^VOZ"), tem(r"CONFERIR")
        falta = [n for n, lst in (("roteiro", roteiro), ("COMO-RODAR", como), ("VOZ", voz)) if not lst]
        pend = 0
        for c in conf:
            t = c.read_text(encoding="utf-8", errors="ignore")
            pend += len(re.findall(r"\[ \]", t)) or len(itens_lista(t))
        marcado = not pend and any(  # pendências marcadas dentro do roteiro/quadro/planilha
            "CONFERIR NO MAC" in x.read_text(encoding="utf-8", errors="ignore")
            for x in arquivos if x.suffix in (".md", ".csv"))
        mac = None
        if como:
            t = como[0].read_text(encoding="utf-8", errors="ignore")
            m = re.search(r"```[a-z]*\n(.*?)```", t, re.S)
            if m:
                cmds = [l.strip() for l in m.group(1).splitlines() if l.strip() and not l.strip().startswith("#")]
                mac = cmds[0] if cmds else None
        st = OK if not falta and not pend and not marcado else REV
        partes = [f"{len(arquivos)} arquivos"]
        if falta:
            partes.append("falta " + ", ".join(falta))
        if pend:
            partes.append(f"{pend} itens a conferir no Mac")
        elif marcado:
            partes.append("tem fatos marcados CONFERIR NO MAC (a voz só grava depois)")
        links = [f"[{x.name}]({rel(x)})" for x in (como + voz + roteiro + conf)[:4]]
        linha = f"- **{nome}** — {st} " + " · ".join(partes)
        if mac:
            linha += f" · Mac roda: `{curto(mac, 70)}`"
        out.append(linha + (" · " + " ".join(links) if links else ""))
    return out


# ---------------------------------------------------------------- montagem
def montar(domingo, faz_repo=None, faz_ref=None, barsi_repo=None, barsi_ref=None):
    seg, dom = semana(domingo)
    fixas, cobre = decisoes_fixas()
    padrao = re.compile("|".join(f"(?:{c})" for c in cobre), re.I) if cobre else None
    ic, decidir_ext, tarefas = investir(seg, dom, padrao)
    L = [f"# Pacote da semana: {dia(seg)} a {dia(dom)}/{dom.year}", "",
         f"Para aprovar de uma vez. Gerado de `pautas-canal/semana/gerar_semana.py {domingo.isoformat()}`. "
         f"{OK} pronto · {REV} em revisão · {FALTA} falta.", "",
         "## DECIDIR ANTES DE GRAVAR", ""]
    n = 0
    for r in fixas:
        n += 1
        det = r["detalhe"]
        link = f"[detalhe]({det})" if det.startswith((".", "/")) or det.endswith(".md") and ":" not in det else f"`{det}`"
        L.append(f"{n}. **{r['video']}** — {curto(r['texto'], 220)} {link}")
    if decidir_ext:
        L += ["", "**Conferir na fonte (a sua validação, tirada dos roteiros):**", ""]
        for d, t, link in decidir_ext:
            n += 1
            L.append(f"{n}. **{d}** — {curto(t)} [detalhe]({link})")
    if not fixas and not decidir_ext:
        L.append("- nada pendente")
    if tarefas:
        L += ["", "_Tarefas no Mac antes de gravar (não precisa decidir):_", ""]
        L += [f"- {d}: {curto(t, 110)}" for d, t, _ in tarefas]
    fac_repo = faz_repo if faz_repo is not None else achar_repo("faz-a-conta")
    bar_repo = barsi_repo if barsi_repo is not None else achar_repo("barsi-cortes")
    bl, lou = barsi(seg, dom, bar_repo, barsi_ref)
    L += ["", "## Investir e Coçar", ""] + ic
    L += ["", "## Faz a Conta (sai 18h)", ""] + faz_a_conta(seg, dom, fac_repo, faz_ref)
    L += ["", "## Shorts Barsi Perene", ""] + bl
    L += ["", "## Shorts Louise", ""] + lou
    L += ["", "## Cards Instagram e X", ""] + cards(seg, dom)
    L += ["", "## Canais dark", ""] + canais_dark()
    L += ["", "---", f"Próximo pacote: `python3 pautas-canal/semana/gerar_semana.py {(domingo + timedelta(days=7)).isoformat()}`", ""]
    return "\n".join(L)


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("domingo", help="data do domingo, AAAA-MM-DD")
    ap.add_argument("--faz-a-conta", help="pasta do repo faz-a-conta")
    ap.add_argument("--faz-a-conta-ref", default="faz-a-conta-cenas", help="branch lido com git show (vazio = disco)")
    ap.add_argument("--barsi", help="pasta do repo barsi-cortes")
    ap.add_argument("--barsi-ref", default="", help="branch lido com git show (vazio = disco)")
    ap.add_argument("--saida", help="arquivo de saída (padrão: pautas-canal/semana/AAAA-MM-DD.md); '-' = tela")
    a = ap.parse_args(argv)
    domingo = date.fromisoformat(a.domingo)
    if domingo.weekday() != 6:
        ap.error(f"{a.domingo} não é domingo")
    fac = achar_repo("faz-a-conta", a.faz_a_conta)
    bar = achar_repo("barsi-cortes", a.barsi)
    texto = montar(domingo, fac, a.faz_a_conta_ref or None, bar, a.barsi_ref or None)
    if a.saida == "-":
        sys.stdout.write(texto)
        return 0
    saida = Path(a.saida) if a.saida else AQUI / f"{domingo.isoformat()}.md"
    saida.write_text(texto, encoding="utf-8")
    print(saida)
    return 0


if __name__ == "__main__":
    sys.exit(main())
