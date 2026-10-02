# Pautas do canal (a partir da auditoria)

Pautas de 05/10 a 29/11/2026, montadas com os números de `auditoria-canal/RELATORIO.md` (ações 3, 4, 5, 6, 8 e 9).

| arquivo | o que é |
|---|---|
| `CALENDARIO-8-SEMANAS.md` / `.csv` | 16 longos em 8 semanas: série de renda mensal às terças, continuações dos 10 top ou pautas de busca às quintas, e o vídeo do Copom em 05/11. Cada pauta traz título, palavra-chave, volume provável (com a base), o número que a justifica e as fontes a conferir. |
| `calendario.py` | fonte única das pautas; regera o `.csv` e o `.md` |
| `SHORTS-MES.md` | 16 Shorts (8 em outubro e 8 em novembro) de produto e renda, com gancho do 1º segundo, ideia e de qual longo sai o corte |
| `PERGUNTAS-SEM-RESPOSTA.md` | as 765 perguntas sem resposta do canal, por tema, e 20 rascunhos de resposta para o Denis aprovar |
| `perguntas.csv` | as 765 perguntas, uma por linha (tema, vídeo, id do comentário, likes, data e texto), sem autor e sem @menções |
| `perguntas.py` | regera o `perguntas.csv` e documenta o critério ("pergunta" e "sem resposta") |

Para regerar, com os dados em `auditoria-canal/dados/`:

```sh
cd pautas-canal && python3 perguntas.py && python3 calendario.py
```

**Regras de todas as pautas:**
- tom simples e direto, sem clichê;
- não recomendar ativo nem citar corretora;
- fora: dívida, cartão de crédito e política;
- conferir as fontes indicadas antes de gravar ou publicar.
