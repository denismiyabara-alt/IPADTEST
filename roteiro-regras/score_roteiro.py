#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Portao N5 — parte mecanica da rubrica-roteiro-10.
Nao julga qualidade: MEDE o que da pra medir. Quem escreveu nao importa.
Uso: python3 score_roteiro.py <roteiro.md>   |   python3 score_roteiro.py --test
"""
import re, sys, io, unicodedata

ANTI_IA = ["ecossistema","jornada","mindset","plot twist","transformador","robusto"]
META = ["presta atenção","presta atencao","isso é importante","isso e importante",
        "guarda essa informação","quero destravar","o que eu vou te dizer agora",
        "repara no que isso significa","antes de começar","antes de comecar"]
RECAP = ["resumindo","recapitulando","em resumo","pra fechar, os pontos"]

# item 3: o numero do loop precisa se explicar na MESMA frase ("e dai?" tem resposta?).
# Sem isso ele e so um digito pra decorar — foi assim que "8,3%" e "107.527" passaram
# batido nos roteiros de 23/08/2026 que o Denis reprovou na leitura.
# So marcadores de SIGNIFICADO: o que o numero E ou o que ele FAZ.
# "e nao os cem mil" ficou de fora de proposito — dizer qual numero decorar nao e
# dizer o que ele significa. Foi exatamente assim que o 107.527 passou batido.
ANCORA = ["e quanto","e o que","e o dia","nao e valor","nao e um","vale mais","vale menos",
          "a menos","a mais","custou","custa","deixou de","perdeu","por mes","por ano",
          "de diferenca","e ele responde","e ele fecha","e a chave"]

# item 10: ferramenta portatil precisa de NOME. "faz tres contas" sem batismo nao gruda.
NOME_FERRAMENTA = r"(?:eu\s+)?chamo\s+(?:isso\s+)?de\s+\w+|(?:a|essa|minha)\s+(?:conta|pergunta|regra|prova)\s+d[eoa]\s+\w+"

def norm(t):
    # NFKD separa o acento em marca combinante; sem remover, "tres" nunca casa com "três".
    d = unicodedata.normalize("NFKD", t.lower())
    return "".join(ch for ch in d if not unicodedata.combining(ch))

# Secoes que NAO sao roteiro falado: repetem numero por desenho e nao podem
# contar contra o item 9. Descoberto no TRXF11 v9 (23/08/2026): a tabela de
# legendas de tela reprovava o arco linear sozinha.
NAO_FALADO = r"##\s*(DADOS A VERIFICAR|LEGENDAS DE TELA|MARCADORES DE GRAVA|CUIDADOS|CHECKLIST)"

def corpo(t):
    """So o texto que o Denis fala: sem frontmatter e sem secoes de apoio."""
    t = re.sub(r"^---\n.*?\n---\n", "", t, flags=re.S)
    partes = re.split(NAO_FALADO, t)
    return partes[0]

def blocos(t):
    ps = re.split(r"^##\s+", t, flags=re.M)[1:]
    return [p for p in ps if p.strip()]

def numeros(t):
    # numeros com peso: R$ x, x%, x mil/bi, ou 3+ digitos
    return re.findall(r"R\$\s?[\d.,]+|\d+[.,]?\d*\s?%|\d+[.,]?\d*\s?(?:mil|milh|bilh)"
                      r"|\b\d{1,3}(?:\.\d{3})+\b|\b\d{4,}\b", t)

# ---------------------------------------------------------------------------
# item 11 — PONTES. Adicionado 31/08/2026: a rubrica media o que estava DENTRO
# do bloco e nada media a costura ENTRE blocos. Resultado: "Hoje eu vou te
# mostrar tres coisas" e "E ai vem a parte que ninguem te explicou" passaram
# 10/10. Teste unico da doutrina (feedback_frases_conexao_watchtime):
# a frase CONTINUA o assunto ou DESCREVE o video? Descreveu, reprova.
# ---------------------------------------------------------------------------
ANUNCIO = [
    "vou te mostrar", "vou te contar", "vou te explicar", "a gente vai ver",
    "nesse video", "hoje eu vou", "eu vou te dizer agora",
    "e ai vem a parte", "agora a parte", "a parte que ninguem",
    "antes de te contar", "antes de falar", "agora que voce entende",
    "isso nos leva", "chega de", "vamos botar", "vamos falar de",
    "preciso ser justo", "preciso ser honesto", "preciso ser sincero",
    # 01/09/2026: as formas abaixo zeraram dois roteiros no julgamento a mao e
    # o portao devolveu ZERO. Todas descrevem o video em vez de continuar o assunto.
    "vou defender", "quero falar com", "o que fazer com isso", "vou percorrer",
    "que ninguem faz num video", "antes do fecho", "fecha comigo",
    "deixa eu te contar", "deixa eu te mostrar",
]

def _falas(bloco):
    """Todas as linhas realmente faladas de um bloco (pula heading, [TELA], tabela)."""
    for l in bloco.split("\n")[1:]:
        l = l.strip()
        if not l or l.startswith(("**[", "[", "|", "#", ">", "---", "*[", "*(")):
            continue
        if re.match(r"^\d+\.\s|^[-*]\s", l):
            continue
        yield l

def pontes(c):
    """Retorna (lista_de_anuncios, total_de_blocos).

    Le o bloco INTEIRO, nao so a primeira fala: em 01/09/2026 os dois roteiros
    zerados no julgamento tinham a ponte no meio do bloco ("E agora eu vou
    percorrer as quatro") e o portao devolveu zero. E le o BLOCO 0 tambem: a
    ponte que anuncia o video inteiro ("eu vou te mostrar os dois lados dessa
    conta... e entender isso e o video inteiro") mora justamente la.
    Uma acusacao por bloco — o defeito e a costura, nao cada frase."""
    bs = blocos(c)
    achados = []
    for b in bs:
        for f in _falas(b):
            nf = norm(f)
            hit = next((a for a in ANUNCIO if a in nf), None)
            if hit:
                achados.append((hit, f[:88]))
                break
    return achados, len(bs)

# ---------------------------------------------------------------------------
# item 12 — MOLDE REPETIDO entre roteiros. A rubrica julgava um arquivo por vez,
# entao uma formula na 5a aparicao passava 10/10 todas as vezes. Foi assim que
# "senao isso vira X" chegou a 5 videos. Nao usa lista fixa de proposito: a
# lista so pegaria o que ja nos queimou. Aqui qualquer sequencia de 5 palavras
# repetida em 3+ VIDEOS distintos acusa sozinha.
# ---------------------------------------------------------------------------
# Repeticao OBRIGATORIA nao e molde: o disclaimer e exigido por compliance e os
# dispositivos abaixo sao exigidos pela propria rubrica. Reprovar o que a regra
# manda repetir treina todo mundo a ignorar o portao.
# Numero falado repete por natureza num canal de financas ("oito por cento ao ano"
# bate em 20 videos). Shingle majoritariamente numerico nao e tique, e o falso
# positivo era sistematico — nao edge case.
NUMERAL = set("zero um uma dois duas tres quatro cinco seis sete oito nove dez onze doze treze "
              "quatorze catorze quinze dezesseis dezessete dezoito dezenove vinte trinta quarenta "
              "cinquenta sessenta setenta oitenta noventa cem cento duzentos trezentos quinhentos "
              "mil milhao milhoes bilhao bilhoes por cento reais real virgula e ao ano mes".split())

def _e_numerico(sh):
    ws = sh.split()
    return sum(w in NUMERAL for w in ws) >= len(ws) - 1

EXENTO = ["indicacao de compra", "compra nem de venda", "de compra ou de venda",
          "nao e recomendacao", "guarda esse numero", "fala tanaka",
          # Declaracao de conflito da EQI: obrigatoria pelo P3 e pelo compliance —
          # reprova-la seria mandar apagar justamente o que protege o Denis.
          # NAO entram aqui: copy de oferta ("pega o seu e-mail", "link na descricao").
          # Isso e texto de venda, repete por preguica e nao por exigencia — foi
          # isentado por engano em 31/08/2026 e o roteirista pegou. Isencao e so
          # pra frase que a REGRA manda repetir.
          # "da eqi que eu" fecha o buraco: a frase obrigatoria "E da EQI, que eu sou
          # socio." gera TRES shingles e so um deles ("...que eu sou socio") era isento.
          # A partir do 3o roteiro com a declaracao, os outros dois zeravam sozinhos.
          "que eu sou socio", "sou socio da eqi", "da eqi que eu"]

SUFIXOS = ("-teleprompter", "-leitura", "-fact-check", "-final", "-voz-denis",
           "-obsoleto", "-troca-embalagem", "-merchan")

# -vN nao vive so no fim: "investir-depois-dos-40-v2-teleprompter" e
# "investir-depois-dos-40-V4-3ALAVANCAS" tinham o -vN no MEIO e a versao antiga
# (ancorada em $) nao colapsava. Resultado: v2, V4, v5, FINAL e VOZ-DENIS do
# mesmo video contavam como 5 videos distintos e disparavam o eliminatorio
# "molde repetido em 3+ videos" sem repeticao nenhuma — confirmado em
# 01/09/2026 com "eu vou te mostrar os" e "quando o juro ta alto".
# Corta a partir do -vN: o que vem depois e rotulo de versao ("-3alavancas",
# "-lista"), nao tema. O tema mora ANTES do numero da versao.
_VERSAO = re.compile(r"-v\d+(?=-|$).*$")

def _slug(nome):
    """Agrupa versoes do MESMO video: tira data, sufixo de versao e -vN."""
    n = norm(nome).replace(".md", "")
    n = re.sub(r"^\d{4}-\d{2}-\d{2}-", "", n)
    n = _VERSAO.sub("", n)
    for suf in SUFIXOS:
        n = n.replace(suf, "")
    return n.strip("-")

def _falado(c):
    """So as linhas que o Denis fala: sem heading, sem [TELA]/[CAMERA], sem tabela.
    Sem isso o shingle pega 'bloco 0 gancho 0 00' de cabecalho e acusa 60 moldes
    falsos — foi o que aconteceu no primeiro run em 31/08/2026."""
    linhas = []
    for l in c.split("\n"):
        l = l.strip()
        if not l or l.startswith(("#", "**[", "[", "|", ">", "---", "*[", "*(")):
            continue
        if re.match(r"^[-*]\s|^\d+\.\s", l):
            continue
        linhas.append(l)
    return " ".join(linhas)

def _shingles(c, k=5):
    palavras = re.findall(r"[a-z0-9]+", norm(_falado(c)))
    return {" ".join(palavras[i:i+k]) for i in range(len(palavras) - k + 1)}

def moldes(path, c, minimo_videos=3):
    """Sequencias de 5 palavras deste roteiro que aparecem em 3+ videos distintos."""
    import os, glob
    d = os.path.dirname(os.path.abspath(path)) or "."
    meu = _slug(os.path.basename(path))
    alvo = _shingles(c)
    if not alvo:
        return []
    onde = {}
    for f in glob.glob(os.path.join(d, "*.md")):
        base = os.path.basename(f)
        # Arquivo DERIVADO nao e video: o texto dele ja esta no roteiro que o gerou,
        # entao contar os dois e contar o mesmo texto duas vezes. -MERCHAN- e bloco
        # que sera inserido; -LEITURA e a versao em algarismos; -DIRECAO-CENA e mapa
        # de edicao. Sem isso todo roteiro nasce com gemeo no acervo e o item vira
        # falso ZERA — pego pelo juiz em 31/08/2026, depois que o LEITURA passou a
        # ser gerado pra todo roteiro.
        if any(x in norm(base) for x in ("merchan", "leitura", "direcao-cena", "direcao_cena")):
            continue
        sl = _slug(base)
        if sl == meu:
            continue
        try:
            outro = _shingles(corpo(open(f, encoding="utf-8").read()))
        except Exception:
            continue
        for sh in alvo & outro:
            onde.setdefault(sh, set()).add(sl)
    reps = {sh: vs for sh, vs in onde.items()
            if len(vs) + 1 >= minimo_videos
            and not any(e in sh for e in EXENTO)
            and not _e_numerico(sh)}

    # Sem fusao de proposito: a versao de 31/08/2026 que juntava shingles com 4
    # palavras em comum costurava trechos NAO contiguos ("vinte e quatro reais e
    # aqui eu preciso ser justo") e a saida ficou ilegivel. Shingle cru se le
    # bem: 3 linhas vizinhas da mesma frase sao obviamente a mesma frase.
    return sorted(reps.items(), key=lambda x: (-len(x[1]), x[0]))


def avaliar(texto):
    c = corpo(texto); n = norm(c); bs = blocos(c); out = {}

    # ELIMINATORIOS
    elim = []
    for w in ANTI_IA:
        if w in n: elim.append(f"palavra anti-IA: '{w}'")
    if "tana" in n and re.search(r"\btan[áa]\b(?!ka|ca)", n): elim.append("'Taná' em vez de Tanaka")
    if not re.match(r"\s*(#[^\n]*\n+)*.{0,400}?fala,?\s*tanak?c?a", n, re.S):
        elim.append("nao abre com 'Fala, Tanaka'")
    if re.search(r"\b\d+\s?%\s+(da sua carteira|em renda fixa)", n) and "não é recomendação" not in n:
        elim.append("alocacao em % sem disclaimer")
    out["eliminatorios"] = elim

    # SIGLAS: o portao NAO consegue saber se um acronimo foi traduzido na fala.
    # Ele so LISTA os que aparecem, pra quem le decidir. Foi assim que "CRI" passou
    # batido e virou eliminatorio no julgamento (roteiro lucro-vs-caixa, 23/08/2026).
    siglas = sorted(set(re.findall(r"\b(?:CRI|CRA|DRE|DFC|DFP|ITR|FIDC|NOI|LCI|LCA|CDB|CDI|IPCA|IGPM|FGC|CVM|ABL|WALE|IFIX|EBITDA|ROE|LTV|FFO)\b", c)))
    out["siglas"] = siglas

    # item 8 — meta-discurso (0 ocorrencias = passa)
    m8 = [w for w in META if w in n]
    out[8] = (len(m8) == 0, f"meta-discurso: {m8}" if m8 else "nenhum meta-discurso")

    # item 3 — loop = numero ANCORADO, nao digito solto
    # a frase do loop vai ate o fim do periodo; o numero tem que vir com consequencia junto.
    mloop = re.search(r"guarda(?:\s+esse|\s+o)?\s+(?:numero|detalhe|contraste|raciocinio)"
                      r"(?:(?!\n\s*##).){0,260}", n, re.S)
    if not mloop:
        out[3] = (False, "nao achou loop aberto ('guarda esse numero...')")
        loop_nums = set()
    else:
        frase = mloop.group(0)
        loop_nums = {x.strip() for x in numeros(frase)}
        ancorado = any(a in frase for a in ANCORA)
        out[3] = (ancorado,
                  "loop ancorado na mesma frase" if ancorado
                  else f"numero solto no loop: {sorted(loop_nums) or 'nenhum'} — falta consequencia na mesma frase")

    # item 9 — arco linear: numero relevante em 2+ blocos
    reps = {}
    # o numero guardado no loop repete de proposito (callback) — nao e defeito.
    # So vale a isencao se o loop passou no item 3; loop solto nao ganha passe livre.
    if not out[3][0]: loop_nums = set()
    por_bloco = [{x.strip() for x in numeros(b)} for b in bs]
    for num in set(numeros(c)):
        k = num.strip()
        if k in loop_nums: continue
        if len(re.sub(r"\D","",k)) < 2: continue
        nb = sum(1 for toks in por_bloco if k in toks)
        if nb >= 2: reps[k] = nb
    out[9] = (len(reps) == 0, f"numeros em 2+ blocos: {reps}" if reps else "cada fato 1x")

    # item 10 — fecho e ferramenta, nao recap
    # o FECHO nem sempre e o ultimo bloco: vem tabela de tela/marcadores depois
    fecho = next((b for b in reversed(bs) if re.match(r"[^\n]*(FECHA|FECHO)", b, re.I)), bs[-1] if bs else "")
    fn = norm(fecho)
    achou = [w for w in RECAP if w in fn]
    tem_ferramenta = bool(re.search(r"(tres|3)\s+(perguntas|contas|numeros)|checklist|pergunta que|leve daqui e a pergunta", fn))
    nomeada = bool(re.search(NOME_FERRAMENTA, fn))
    acao = bool(re.search(r"\bdivid|\bdivide\b|\bsoma\b|\bsome\b|\bcompara\b|\bpega o\b", fn))
    tem_ferramenta = tem_ferramenta or acao
    out[10] = (not achou and tem_ferramenta and nomeada,
               (f"recap: {achou}; " if achou else "")
               + ("ferramenta nomeada" if tem_ferramenta and nomeada
                  else "ferramenta sem nome (batiza: 'a conta do X')" if tem_ferramenta
                  else "sem checklist/pergunta/3 numeros"))

    # item 2 — numero ancorado nos primeiros ~20s (1o bloco)
    b1 = bs[0] if bs else ""
    out[2] = (len(numeros(b1)) > 0, f"{len(numeros(b1))} numero(s) no bloco 1")

    # item 6 — quantas analogias (heuristica: marcadores de comparacao)
    ana = re.findall(r"é como (?:se|um|uma)|igual (?:a|ao|à)|pensa (?:no|na|que)|vira aquele", n)
    out[6] = (1 <= len(ana) <= 2, f"{len(ana)} marcador(es) de analogia (alvo: 1, esticada)")
    return out

def avisos_ouvido(c):
    """AVISOS (nao zeram): sinais mecanicos de frase escrita pro olho, nao pro ouvido.
    Regra desde 15/09/2026 (Denis: "os roteiros tao ficando muito confusos"). O portao nao
    mede compreensao — isso e o agente `ouvinte-frio`. Aqui so o que da pra contar:
    (a) frase com numero e mais de 25 palavras; (b) "isso/disso/dai/esse ai/ali" numa frase com
    numero (aponta pra conta que nao esta na frase); (c) frase que abre com "ele/ela" sem o nome."""
    NUM = re.compile(r"\d|\b(mil|milh|bilh|por cento|reais|cento|dez|vinte|trinta|quarenta|cinquenta|sessenta|setenta|oitenta|noventa|cem)\b", re.I)
    DEIT = re.compile(r"\b(isso|disso|nisso|da[ií]|dali|esse a[ií]|essa a[ií]|aqui ele|ali)\b", re.I)
    ELE = re.compile(r"^(e |s[oó] que |mas |a[ií] )?(ele|ela)\b", re.I)
    av = []
    for b in blocos(c):
        for l in _falas(b):
            for fr in re.split(r"(?<=[.!?])\s+", l):
                fr = fr.strip()
                if not fr: continue
                n = len(fr.split()); tem_num = bool(NUM.search(fr))
                if tem_num and n > 25: av.append(("longa+numero", n, fr))
                if tem_num and DEIT.search(fr): av.append(("isso/esse ai+numero", n, fr))
                if ELE.match(fr): av.append(("abre com ele/ela", n, fr))
    return av

def imprimir(r, path=None, c=None):
    print("ELIMINATORIOS:", "nenhum" if not r["eliminatorios"] else "")
    for e in r["eliminatorios"]: print("  X", e)
    print("\nITENS MECANICOS (6 de 10 — os outros 4 exigem julgamento):")
    ok = 0
    for i in (2,3,6,8,9,10):
        passou, msg = r[i]; ok += passou
        print(f"  [{'PASSA' if passou else 'FALHA'}] item {i:>2} — {msg}")
    if r.get("siglas"):
        print("\n⚠️  SIGLAS NA FALA (o portao NAO checa traducao — confira uma a uma):")
        print("   ", ", ".join(r["siglas"]))
        print("    jargao nao traduzido na hora e ELIMINATORIO pela rubrica.")

    # PONTES e MOLDE: eliminatorios, nao itens de nota (corrigido 31/08/2026).
    # Viraram "item 11" e "item 12" por engano numa primeira versao, o que
    # transformou a nota em 12/12 e matou o "nota 10", que e o nome do padrao.
    # Sao defeitos que BLOQUEIAM, nao dimensoes de qualidade que custam 1 ponto.
    extras = []
    if c is not None:
        anun, tot = pontes(c)
        if len(anun) > 1:
            extras.append(f"{len(anun)} de {tot} pontes ANUNCIAM em vez de continuar (teto: 1)")
            for a, tr in anun:
                extras.append(f"    > '{a}' em: {tr}...")
    if path is not None and c is not None:
        reps = moldes(path, c)
        if reps:
            extras.append(f"{len(reps)} sequencia(s) de 5 palavras repetidas em 3+ videos")
            for sh, vs in reps[:8]:
                extras.append(f"    > \"{sh}\" — tambem em: {', '.join(sorted(vs)[:3])}{' ...' if len(vs) > 3 else ''}")

    if extras:
        print("\nELIMINATORIOS DE COSTURA (pontes / molde repetido):")
        for e in extras: print("  X", e)
    else:
        print("\nELIMINATORIOS DE COSTURA: nenhum (pontes ok, zero molde repetido)")

    if c is not None:
        av = avisos_ouvido(c)
        if av:
            print(f"\nAVISOS DE OUVIDO ({len(av)}) — nao zeram; o teste de verdade e o agente ouvinte-frio:")
            for tipo, n, fr in av[:12]:
                print(f"  ~ [{tipo}, {n} palavras] {fr[:110]}{'...' if len(fr) > 110 else ''}")

    zerado = bool(r["eliminatorios"]) or bool(extras)
    print(f"\nparcial mecanico: {ok}/6" + ("  | ZERADO por eliminatorio" if zerado else ""))
    return ok, 6

def _test():
    ruim = """---
tema: x
---
## BLOCO 1 - HOOK
Fala, Tanaka! Se voce tem R$ 100 mil parado, rende R$ 930 por mes.
## BLOCO 2
Repara no que isso significa. O R$ 930 muda tudo. Isso e como se fosse um motor.
## BLOCO 3 - FECHA
Resumindo pra voce: R$ 930 por mes. Se inscreve no canal.
"""
    r = avaliar(ruim)
    assert not r[8][0], "devia pegar meta-discurso"
    assert not r[9][0], "devia pegar R$ 930 em 2+ blocos"
    assert not r[10][0], "devia pegar recap no fecho"
    assert r[2][0], "tem numero no bloco 1"
    assert not r["eliminatorios"], f"nao devia ter eliminatorio: {r['eliminatorios']}"

    bom = """## BLOCO 1 - HOOK
Fala, Tanaka! O aporte carrega 5 vezes mais que o juro ate os R$ 100 mil.
Guarda esse numero: 720. Nao e valor em real, e dia de calendario.
## BLOCO 2
O banco vira aquele parente que sabe que voce nao vai reclamar.
## BLOCO 3 - FECHA
Antes de comemorar marco, faz tres perguntas — eu chamo isso de conta da ladeira.
"""
    r2 = avaliar(bom)
    assert r2[8][0] and r2[9][0] and r2[10][0], f"roteiro bom nao devia falhar: {r2}"
    assert r2[3][0], "loop com consequencia na mesma frase devia passar"

    # item 3: numero solto no loop reprova (casos reais 23/08/2026)
    solto = """## BLOCO 1
Fala, Tanaka! Tem 58 empresas pagando acima de 10%. Guarda esse numero: 8,3%.
## FECHA
Faz tres perguntas — eu chamo isso de conta do rodizio."""
    r3 = avaliar(solto)
    assert not r3[3][0], "8,3% solto no loop devia reprovar o item 3"
    assert r3[10][0], "ferramenta nomeada devia passar"

    # item 10: ferramenta sem batismo nao basta
    sem_nome = """## BLOCO 1
Fala, Tanaka! O aporte pesa mais. Guarda esse numero: 720, que vale mais que 20 pontos.
## FECHA
A gente faz tres contas antes de assinar qualquer coisa."""
    r4 = avaliar(sem_nome)
    assert r4[3][0], "loop ancorado devia passar"
    assert not r4[10][0], "checklist sem nome devia reprovar o item 10"

    # regressao: acento nao pode quebrar o match (bug NFKD, 23/08/2026)
    acento = """## BLOCO 1
Fala, Tanaka! O aporte pesa 5 vezes mais.
## FECHA
A gente faz tres contas — eu chamo isso de conta da ladeira."""
    assert avaliar(acento)[10][0], "acento decomposto quebrou o item 10"
    acento2 = acento.replace("tres", "tr\u00eas")
    assert avaliar(acento2)[10][0], "'tres' com acento nao casou"
    # regressao: FECHO no meio, com tabela depois (caso TRXF11)
    tardio = """## BLOCO 1
Fala, Tanaka! O aporte pesa mais.
## FECHA
A gente faz tres contas — eu chamo isso de conta da ladeira.
## MARCADORES DE GRAVACAO
| 0:15 | dado |"""
    assert avaliar(tardio)[10][0], "nao achou o FECHO quando ha bloco depois dele"
    # regressao: "2.000" nao pode casar dentro de "12.000" (bug de substring, 24/08/2026)
    substr = """## BLOCO 1
Fala, Tanaka! Voce deposita 12.000 por ano. Guarda esse numero: 720, que vale mais que 20 pontos.
## BLOCO 2
Quem guarda 2.000 por mes chega mais tarde.
## FECHA
Pega o aporte e divide — eu chamo isso de conta da ladeira."""
    assert avaliar(substr)[9][0], "'2.000' nao pode contar como repeticao de '12.000'"

    # regressao: tabela de telas repete numero por desenho, nao pode reprovar item 9
    com_tabela = """## BLOCO 1
Fala, Tanaka! A cota caiu de R$ 91,10 pra R$ 71.
## BLOCO 2
E a emissao pediu R$ 10 bilhoes.
## FECHA
Faz tres contas — eu chamo isso de conta da ladeira.
## LEGENDAS DE TELA
| 0:05 | R$ 91,10 |
| 2:40 | R$ 91,10 · R$ 71 |"""
    assert avaliar(com_tabela)[9][0], "tabela de telas nao pode reprovar o arco linear"
    # siglas: o portao lista, nao julga
    comsigla = """## BLOCO 1
Fala, Tanaka! Entrou CRI novo e o CDI subiu.
## FECHA
Faz tres contas — eu chamo isso de conta da ladeira."""
    assert set(avaliar(comsigla)["siglas"]) == {"CRI", "CDI"}, "devia listar as siglas encontradas"
    assert avaliar(acento).get("siglas") == [], "texto sem sigla nao lista nada"
    # item 11: ponte que anuncia reprova; ponte que carrega objeto passa
    anuncia = """## BLOCO 1
Fala, Tanaka! O fundo caiu R$ 20.
## BLOCO 2
Hoje eu vou te mostrar tres coisas sobre isso.
## BLOCO 3
E ai vem a parte que ninguem te explicou direito."""
    a, tot = pontes(corpo(anuncia))
    assert len(a) == 2 and tot == 3, f"devia pegar 2 pontes que anunciam, veio {len(a)}/{tot}"

    # regressao 01/09/2026: ponte fora da PRIMEIRA linha e ponte no BLOCO 0.
    # A versao antiga lia so a primeira fala e pulava o bloco 0 — devolvia ZERO
    # nos dois roteiros que o juiz zerou a mao por esse mesmo eliminatorio.
    escondida = """## BLOCO 0 - GANCHO
Fala, Tanaka! O IBGE soltou o numero e a comida caiu.
Eu vou te mostrar os dois lados dessa conta, porque os dois sao verdade.
## BLOCO 1
O relatorio separa a historia em quatro fases. E eu vou percorrer as quatro.
## BLOCO 2
E agora eu vou fazer o que ninguem faz num video desses, que e defender quem errou.
## BLOCO 3
Antes do fecho, tres coisas que eu preciso dizer em voz alta.
## FECHO
Fecha comigo."""
    a3, _ = pontes(corpo(escondida))
    assert len(a3) == 5, f"ponte no meio do bloco / no bloco 0 tem que acusar: veio {a3}"

    carrega = """## BLOCO 1
Fala, Tanaka! O problema custou R$ 20.
## BLOCO 2
O problema nunca foi o predio.
## BLOCO 3
O problema e o tamanho e a velocidade."""
    a2, _ = pontes(corpo(carrega))
    assert a2 == [], f"ponte que carrega objeto nao podia acusar: {a2}"

    # item 12: _slug agrupa versoes do mesmo video
    assert _slug("2026-08-21-trxf11-maior-emissao-fii.md") == _slug("2026-08-24-trxf11-maior-emissao-fii-teleprompter.md"), "slug devia agrupar versoes"
    assert _slug("2026-09-01-trxf11-cancelou-3bi-teleprompter.md") != _slug("2026-08-21-trxf11-maior-emissao-fii.md"), "videos diferentes nao podem colidir"
    # regressao 01/09/2026: -vN no MEIO do nome nao colapsava e as versoes do
    # mesmo video contavam como 3+ videos distintos (falso "molde repetido").
    mesmo = {_slug(f) for f in (
        "2026-06-23-investir-depois-dos-40.md",
        "2026-07-09-investir-depois-dos-40-v2-teleprompter.md",
        "2026-07-09-investir-depois-dos-40-V4-3ALAVANCAS.md",
        "2026-08-10-investir-depois-dos-40-v5-fact-check.md",
        "2026-07-09-investir-depois-dos-40-VOZ-DENIS.md",
        "2026-07-09-investir-depois-dos-40-FINAL.md")}
    assert mesmo == {"investir-depois-dos-40"}, f"versoes do mesmo video nao colapsaram: {mesmo}"
    assert len(_shingles("um dois tres quatro cinco seis")) == 2, "shingles de 5 palavras"

    # Ancoragem CONGELADA nos dois roteiros de 01/09/2026 que o juiz zerou a mao
    # (7 e 3 pontes) e que o portao acusava com ZERO. Trechos copiados como
    # estavam naquele dia — NAO aponta pro arquivo vivo de proposito: roteiro
    # reprovado e reescrito (a Equatorial virou v2 no mesmo dia e zerou as 3
    # pontes), e um teste ancorado no arquivo passaria a falhar justamente
    # quando o portao funcionou.
    elnino_0901 = """## BLOCO 0 - GANCHO
Fala, Tanaka! No dia 26 de agosto o IBGE soltou o numero oficial. A comida caiu.
Eu vou te mostrar os dois lados dessa conta, porque os dois sao verdade ao mesmo tempo.
## BLOCO 1 - O PLACAR
Vamos ao placar. Quatro coisas que eu falei em julho, uma por uma.
Esse cenario continua de pe. E eu vou te explicar daqui a pouco por que.
## BLOCO 5 - RIBEIRAO PRETO
E antes que voce ache que nao aconteceu nada, deixa eu te contar o que houve no dia 24 de julho.
## BLOCO 6 - A GALINHA NO QUINTAL
Agora eu quero falar com uma pessoa especifica.
## BLOCO 7 - EU DEFENDO OS OUTROS
E agora eu vou defender os caras que eu passei o video inteiro contrariando.
## BLOCO 8 - O QUE OLHAR AGORA
Entao, o que fazer com isso daqui pra frente. Tres marcadores, e sao so tres.
## FECHO
Fecha comigo."""
    equatorial_0901 = """## BLOCO 1
Esse relatorio e do BTG Pactual, saiu no dia 25 de agosto.
## BLOCO 2 - FASE 1
O relatorio separa a historia em quatro fases. E eu vou percorrer as quatro.
## BLOCO 5 - EU DEFENDO O ERRO
E agora eu vou fazer o que ninguem faz num video desses, que e defender o cara que errou.
## BLOCO 7 - O QUE ISSO NAO E
Antes do fecho, tres coisas que eu preciso dizer em voz alta."""
    for nome, txt, esperado in (("elnino 01/09", elnino_0901, 7),
                                ("equatorial 01/09", equatorial_0901, 3)):
        a, _ = pontes(corpo(txt))
        assert len(a) == esperado, f"{nome}: o juiz contou {esperado} pontes, o portao veio com {len(a)}"

    print("ok: 14 casos, 29 asserts")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test": _test(); sys.exit(0)
    if len(sys.argv) < 2: print(__doc__); sys.exit(1)
    t = io.open(sys.argv[1], encoding="utf-8").read()
    got, alvo = imprimir(avaliar(t), sys.argv[1], corpo(t))
    sys.exit(0 if got == alvo else 1)
