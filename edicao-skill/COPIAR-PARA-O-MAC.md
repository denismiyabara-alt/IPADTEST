# O que o Mac copia de volta (gráfico de série, 03/10/2026)

Origem: o clone do IPADTEST no Mac (`~/IPADTEST`, ou onde estiver), depois de `git pull` na branch
`claude/friendly-shannon-jjlw8c`. Destino: a skill viva, `~/.claude/skills/edicao-investir-cocar/`.

| origem (repo IPADTEST) | destino (`~/.claude/skills/edicao-investir-cocar/`) | |
|---|---|---|
| `edicao-skill/SKILL.md` | `SKILL.md` | alterado: seção 2 e nova 2b |
| `edicao-skill/molde-burry/README.md` | `molde-burry/README.md` | alterado |
| `edicao-skill/molde-burry/plano.py` | `molde-burry/plano.py` | alterado: `LIMITES["G"]` (5–10 s) |
| `edicao-skill/molde-burry/mapa.py` | `molde-burry/mapa.py` | alterado: lê `graficos.json`; não apara antes do pouso |
| `edicao-skill/molde-burry/montar.py` | `molde-burry/montar.py` | alterado: fonte da peça G; `MONTAR_VCODEC` |
| `edicao-skill/molde-burry/sfx.py` | `molde-burry/sfx.py` | alterado: evento "impacto" do pouso |
| `edicao-skill/molde-burry/broll/gerar.py` | `molde-burry/broll/gerar.py` | alterado: pula as cenas `grafico` |
| `edicao-skill/molde-burry/broll/grafico.py` | `molde-burry/broll/grafico.py` | **novo** |
| `edicao-skill/molde-burry/tests/test_peca_grafico.py` | `molde-burry/tests/test_peca_grafico.py` | **novo** |
| `edicao-skill/molde-burry/exemplos/trxf11-cota/GRAFICO-SELIC.md` | `molde-burry/exemplos/trxf11-cota/GRAFICO-SELIC.md` | **novo** |

Os outros arquivos de `edicao-skill/` não mudaram desde o snapshot 40f15b8.

```bash
R=~/IPADTEST/edicao-skill; S=~/.claude/skills/edicao-investir-cocar
cp "$R/SKILL.md" "$S/SKILL.md"
for f in README.md plano.py mapa.py montar.py sfx.py broll/gerar.py broll/grafico.py tests/test_peca_grafico.py \
         exemplos/trxf11-cota/GRAFICO-SELIC.md; do
  mkdir -p "$S/molde-burry/$(dirname $f)"; cp "$R/molde-burry/$f" "$S/molde-burry/$f"; done
```

Num projeto **em andamento**, que já tem cópias dos scripts, copie também `plano.py`, `mapa.py`, `montar.py` e
`sfx.py` para a raiz do projeto, e `broll/gerar.py` e `broll/grafico.py` para `videos/broll/`.

## O que fica em motion/ (não vai para a skill)

`motion/` é o componente, e a skill só o chama: `grafico_cotacao/` (`especificacao.py`, `serie.py`, `gerar.py` e
`quadro.mjs`), `comum/estilo.py` (o módulo comum com a biblioteca: a PAL e as fontes, lidas do `broll/gerar.py`), `package.json` (gsap,
fontes OFL Montserrat e Archivo Black, hyperframes 0.8.78), `tests/` e `exemplos/`. No Mac:

```bash
export IEC_MOTION=~/IPADTEST/motion      # ponha no ~/.zshrc: é onde a skill acha o componente
# opcional: o motion lê a PAL de edicao-skill/molde-burry/broll/gerar.py do clone; para ler a da skill viva:
export IEC_MOLDE_BURRY_GERAR=~/.claude/skills/edicao-investir-cocar/molde-burry/broll/gerar.py
(cd "$IEC_MOTION" && npm install)        # uma vez
```

Sem `IEC_MOTION`, o `grafico.py` tenta `~/IPADTEST/motion`. Se não achar, para com uma mensagem que diz o que fazer.
O dado vem do cache do site-ativos (`IPADTEST/site-ativos/cache/`) ou de `$IEC_SITE_ATIVOS`.

## Testes

```bash
cd ~/IPADTEST && IEC_MOTION=$PWD/motion python3 -m pytest -q edicao-skill/molde-burry/tests motion/tests
```
No Mac, o `montar.py` usa o `h264_videotoolbox`. O teste usa `MONTAR_VCODEC=libx264` por padrão, e você pode exportar
`MONTAR_VCODEC=h264_videotoolbox` para testar o encoder do Mac.
