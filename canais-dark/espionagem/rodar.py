"""Pipeline do episodio no Mac: roteiro -> blocos.py -> voz -> conferencia -> cenas -> render -> video.
    python3 rodar.py ep01-eichmann --status      # so le: o que falta
    python3 rodar.py ep01-eichmann               # roda o que falta (retoma de onde parou)
    python3 rodar.py ep01-eichmann --so-render   # refaz cenas e render com a voz que ja existe
Trava: NAO grava voz enquanto houver fato no quadro com status diferente de "conferido"/"calculado".
"""
import os, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import roteiro  # noqa: E402

HYPERFRAMES = os.environ.get("HYPERFRAMES", "hyperframes@0.8.78")


def run(cmd, cwd):
    print("  $", " ".join(cmd))
    if subprocess.run(cmd, cwd=cwd).returncode != 0:
        raise SystemExit(f"PAROU em: {' '.join(cmd)}")


def main(ep, status=False, so_render=False):
    pasta = os.path.join(AQUI, ep)
    r = roteiro.ler(os.path.join(pasta, "roteiro.md"))
    pend = [n["id"] for n in r.numeros if n["status"] not in roteiro.STATUS_OK]
    blocos = r.ordem
    voz = [b for b in blocos if os.path.exists(os.path.join(pasta, f"voz_{b}.wav"))]
    ren = [b for b in blocos if os.path.exists(os.path.join(pasta, f"render_{b}.mp4"))]
    print(f"{r.titulo}: {len(blocos)} blocos · fatos pendentes: {len(pend)} {pend[:8]}{'…' if len(pend) > 8 else ''}")
    print(f"  voz: {len(voz)}/{len(blocos)} · render: {len(ren)}/{len(blocos)}")
    if status:
        return
    open(os.path.join(pasta, "blocos.py"), "w", encoding="utf-8").write(roteiro.para_blocos_py(r))
    if not so_render:
        faltam = [b for b in blocos if b not in voz]
        if faltam and pend:
            raise SystemExit("PAROU: há fatos 'CONFERIR NO MAC' no quadro. Confira, troque para 'conferido' e rode de novo.")
        for b in faltam:
            run([sys.executable, os.path.join(AQUI, "synth_voz.py"), b], pasta)
        run([sys.executable, os.path.join(AQUI, "conferir.py"), *blocos], pasta)
    for b in blocos:
        run([sys.executable, os.path.join(AQUI, "build_hf.py"), b], pasta)
        run(["npx", "--yes", HYPERFRAMES, "render", "-o", f"../render_{b}.mp4"], os.path.join(pasta, f"hf-{b}"))
    open(os.path.join(pasta, "concat.txt"), "w").write("".join(f"file 'render_{b}.mp4'\n" for b in blocos))
    run(["ffmpeg", "-v", "error", "-y", "-f", "concat", "-safe", "0", "-i", "concat.txt", "-c", "copy", f"{ep}-video.mp4"], pasta)
    print(f"ok: {ep}/{ep}-video.mp4")


if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    if not a:
        sys.exit(__doc__)
    main(a[0], status="--status" in sys.argv, so_render="--so-render" in sys.argv)
