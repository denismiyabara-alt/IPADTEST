# Exceções às regras de roteiro (decisões do Denis)

Regras que os juízes e checadores NÃO devem tratar como violação. Cada uma tem data e o caso que a originou.

## 1. Cenários por empresa não são recomendação (03/10/2026, roteiro Mounjaro v2)

Um bloco "COMPRAR, VENDER OU FICAR" (ou parecido) que descreve **o que cada empresa enfrenta** — riscos, catalisadores, o que mudaria a tese — é cenário, e cenário o canal sempre traz. Pode ficar como capítulo do YouTube e na tela.

Continua proibido: dizer ao espectador o que fazer com o dinheiro dele ("compre", "venda", "vale a pena entrar", "eu colocaria"), preço-alvo e ranking de "melhor ação".

## 2. Corretora estrangeira como fato de mercado pode ser citada (03/10/2026, roteiro IPO Anthropic/SpaceX)

A regra "não citar corretora" vale para **corretora/plataforma brasileira** (concorrente da EQI e de quem o Denis é sócio). Corretoras americanas (Schwab, Fidelity, Robinhood, SoFi, E*Trade e afins) podem aparecer na fala ou na tela **como fato de mercado** — por exemplo, quem distribuiu ações de um IPO nos EUA.

Continua proibido: indicar qualquer corretora como caminho para o espectador investir ("abre conta na X", "pela Y você compra").

## Onde isso já está no código

- `investir-e-cocar/pipeline/gate_qualidade.py` (checar_corretora): a lista `CORRETORAS` só tem corretoras brasileiras, então as americanas não disparam o aviso. Não acrescentar nomes estrangeiros a essa lista.
- `score_roteiro.py` não checa corretora nem o título "comprar, vender ou ficar".
