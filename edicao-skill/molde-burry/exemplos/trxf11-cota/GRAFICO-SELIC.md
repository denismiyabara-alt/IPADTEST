# Exemplo pronto: gráfico da Selic desde 2020 no vídeo do TRXF11 cota nova

## A frase escolhida

Nenhuma frase do TRXF11 nem do Burry fala da Selic. As candidatas que falam de juros são estas:

| âncora (pecas.py) | o que o Denis diz | por que sim ou não |
|---|---|---|
| `54-cdi`: `corrigidas pelo cdi` | as parcelas da Iguatemi "vêm corrigidas pelo CDI" (a cartela é "não sai de graça") | **escolhida.** O CDI anda colado na Selic, e o gráfico mostra o tamanho da correção: a taxa saiu de 2% e passou de 13% |
| `d3h`: `juro gordissimo` | a parcela final da Berrini, em IPCA + 9,20% | é IPCA+, não Selic. O gráfico certo ali seria o IPCA (`SGS:13522`) |
| `69-susto`: `quem gosta de renda fixa` | o perfil de quem gosta de FII | não fala de taxa |

O gráfico **substitui** a cartela de frase `54-cdi`, na mesma âncora: duas peças na mesma frase estouram o mapa.

## Comandos (no Mac, na pasta do projeto do TRXF11, a que tem `final.json` e `pecas.py`)

```bash
cd "<pasta do projeto TRXF11>"
export IEC_MOTION=~/IPADTEST/motion            # pasta motion/ do clone do IPADTEST; 1ª vez: (cd $IEC_MOTION && npm install)

cat >> pecas.py <<'EOF'
# 4a peca (03/10): grafico da Selic no lugar da cartela de frase 54-cdi, na mesma ancora
PECAS = [p for p in PECAS if p[0] != "54-cdi"] + [("54-selic", "G", r"corrigidas pelo cdi", 0.0)]
EOF
cat >> videos/broll/cenas.py <<'EOF'
T["54-selic"] = ("grafico", dict(serie="SGS:432", periodo="2020-01-01:", rotulo="Selic: de 2% a 15%",
                                 kicker="O CDI anda colado na Selic", destaques="extremos"))
EOF

python3 plano.py final.json                               # o 54-selic sai como peça G, de 5 a 10 s
(cd videos/broll && python3 grafico.py --render)          # ~10–20 s; gera graficos/renders/54-selic.mp4
python3 mapa.py && python3 montar.py && python3 sfx.py    # o pouso do número entra no sfx.wav como "impacto"
```

- **O render do broll não precisa ser refeito.** As janelas das outras peças no `janelas.json` continuam válidas, e o
  `mapa.py` só lê as janelas dos ids que estão no plano. Se você mudou outras peças, rode `python3 gerar.py` e o render
  do broll como sempre.
- **Se o `plano.py` disser "precisa de 5 s"**, a peça seguinte (provavelmente o print `d4h`, em "nao sai de graca") entra
  cedo demais. Dê `1.5` de atraso a ela em `pecas.py`, ou ancore o gráfico em "juro gordissimo" e troque a série para
  o IPCA de 12 meses (`serie="SGS:13522"`).
- Para desfazer, apague as linhas acrescentadas no fim de `pecas.py` e de `videos/broll/cenas.py`.
- Antes de gravar a cena, confira o número que o Denis falou: o gráfico termina no último dado do cache (13,75% em
  02/10/2026). A fala ganha da cartela em diferença de arredondamento.
