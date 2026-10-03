#!/usr/bin/env python3
"""4a peca de B-roll: GRAFICO de serie que se desenha (Selic, IPCA, cotacao), ancorado em FRASE
como as outras. Roda de videos/broll/, igual ao gerar.py.

  cenas.py   "54-selic": ("grafico", dict(serie="SGS:432", periodo="2020-01-01:", rotulo="Selic: de 2% a 15%"))
  pecas.py   ("54-selic", "G", r"corrigidas pelo cdi", 0.0)          # peca "G" = grafico
  python3 plano.py final.json          # duracao 5-10 s, sai da fala (plano.py: LIMITES["G"])
  cd videos/broll && python3 grafico.py --render
  cd ../.. && python3 mapa.py && python3 montar.py && python3 sfx.py

Especificacao (dict da cena; o componente e o motion/grafico_cotacao):
  serie       "SGS:<n>" (BCB: 432 Selic, 433 IPCA, 13522 IPCA 12m, 12 CDI) ou "COTAHIST:<TICKER>" (B3)
  periodo     "2020-01-01:" | "2025-10-01:2026-10-01" | "12m" | "5a"
  rotulo      titulo na tela
  unidade     opcional: "%" | "R$" | "pontos" (padrao: SGS → %, COTAHIST → R$)
  comparador  opcional: "IBOV" | "IFIX" | "CDI" | "SGS:<n>"
  aviso       opcional: True → "Nao e recomendacao de investimento." na tela
  formato     opcional: "16:9" (padrao) | "9:16"
  kicker, destaques ("extremos" ou lista), cor_final ("vermelho" | "ouro"): opcionais

COMPLIANCE (no codigo): COTAHIST (acao/FII) sem comparador E sem aviso → recusado, nada e gerado.

Saidas: graficos/<id>/ (projeto HyperFrames) · graficos/renders/<id>.mp4 (com --render)
        graficos.json {id: {dur, mp4, pouso, final, fonte, eventos}} → lido pelo mapa.py, montar.py e sfx.py
O som do pouso NAO vai no mp4 (o montar.py usa o audio do corte): vai como evento "impacto" no sfx.py.

Onde fica o motion/: $IEC_MOTION (pasta motion do repo IPADTEST). Sem a variavel, tenta ~/IPADTEST/motion.
"""
import argparse, json, os, subprocess, sys

HYPERFRAMES = "hyperframes@0.8.78"
FPS = 30
DUR_MIN, DUR_MAX = 5.0, 10.0
SAIDA = "graficos"


def achar_motion():
    tentados = [os.environ.get("IEC_MOTION"), os.path.expanduser("~/IPADTEST/motion")]
    for c in tentados:
        if c and os.path.exists(os.path.join(c, "grafico_cotacao", "gerar.py")):
            return os.path.abspath(c)
    raise SystemExit("✗ nao achei o motion/ (componente do grafico). Defina IEC_MOTION=/caminho/IPADTEST/motion "
                     f"(tentei: {', '.join(t for t in tentados if t)}) e rode 'npm install' la uma vez.")


def carregar_motion():
    m = achar_motion()
    sys.path.insert(0, os.path.join(m, "grafico_cotacao"))
    import especificacao, gerar   # noqa: E402
    return m, especificacao, gerar


def graficos_do_plano(plano, cenas):
    """{id_base: dur} das pecas do plano cuja cena e do tipo 'grafico'."""
    out = {}
    for pid, p in plano.items():
        b = pid.split("@")[0]
        if b in cenas and cenas[b][0] == "grafico":
            out[b] = max(out.get(b, 0), p["dur"])
    return out


def preparar(plano, cenas, E, G):
    """Monta e valida TODOS os graficos antes de gerar qualquer um (plano errado nao gera nada)."""
    erros, prontos = [], {}
    for gid, dur in graficos_do_plano(plano, cenas).items():
        if dur < DUR_MIN:
            erros.append(f"{gid}: {dur:.1f}s no plano; grafico precisa de {DUR_MIN:.0f} a {DUR_MAX:.0f}s")
            continue
        try:
            dados = E.montar_entrada(cenas[gid][1], min(dur, DUR_MAX), som=False)
            G.validar(dados)
        except E.ErroCompliance as e:
            erros.append(f"{gid}: COMPLIANCE — {e}")
            continue
        except (E.ErroEspecificacao, G.DadosInvalidos) as e:
            erros.append(f"{gid}: {e}")
            continue
        prontos[gid] = dados
    if erros:
        raise SystemExit("✗ graficos recusados:\n  " + "\n  ".join(erros))
    return prontos


def renderizar(proj, mp4, dur):
    os.makedirs(os.path.dirname(mp4), exist_ok=True)
    r = subprocess.run(["npx", "--yes", HYPERFRAMES, "render", "-o", os.path.abspath(mp4)], cwd=proj,
                       capture_output=True, text=True)
    if r.returncode or not os.path.exists(mp4):
        raise SystemExit(f"✗ render de {proj} falhou:\n{r.stdout[-1500:]}\n{r.stderr[-1500:]}")
    n = int(subprocess.run(["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=nb_frames",
                            "-of", "default=nw=1:nk=1", mp4], capture_output=True, text=True).stdout.strip())
    if abs(n - round(dur * FPS)) > 1:
        raise SystemExit(f"✗ {mp4}: {n} frames, esperado {round(dur * FPS)}")


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--render", action="store_true", help="renderiza cada grafico (um por vez)")
    ap.add_argument("--so", help="so este id")
    ap.add_argument("--plano", default="../../plano.json")
    a = ap.parse_args(argv)
    sys.path.insert(0, os.getcwd())
    from cenas import T as CENAS
    plano = json.load(open(a.plano))
    motion, E, G = carregar_motion()
    prontos = preparar(plano, CENAS, E, G)
    if a.so:
        prontos = {k: v for k, v in prontos.items() if k == a.so}
    reg = json.load(open("graficos.json")) if os.path.exists("graficos.json") else {}
    for gid, dados in prontos.items():
        proj = os.path.join(SAIDA, gid)
        G.gerar_projeto(dados, proj)
        dur = dados["duracao"]
        mp4 = os.path.join(SAIDA, "renders", f"{gid}.mp4")
        if a.render:
            renderizar(proj, mp4, dur)
        pouso = round(dur * G.FRACAO_POUSO, 3)
        reg[gid] = {"dur": dur, "mp4": os.path.join("videos", "broll", mp4), "pouso": pouso,
                    "final": G.texto_valor(dados["serie"][-1]["valor"], G.validar(dados)["unidade"]),
                    "fonte": dados["fonte"], "eventos": [[pouso, "impacto", 0.55]]}
        print(f"  {gid}: {dados['titulo']} · {dur:.1f}s · final {reg[gid]['final']} · {dados['fonte']}"
              + (f" → {mp4}" if a.render else ""))
    reg = {k: v for k, v in reg.items() if k in graficos_do_plano(plano, CENAS)}   # grafico que saiu do plano sai daqui
    json.dump(reg, open("graficos.json", "w"), indent=1, ensure_ascii=False)
    print(f"{len(prontos)} grafico(s) · motion em {motion}")


if __name__ == "__main__":
    main()
