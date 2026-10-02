# Pautas do canal (a partir da auditoria)

Meta, temas e pautas de 05/10 a 29/11/2026, montados com os números de `auditoria-canal/` (relatório e dados).

| arquivo | o que é |
|---|---|
| `META.md` / `meta.csv` | **desdobramento da meta de 200 mil:** árvore (ganhos − perdas; catálogo + vídeos novos × inscritos esperados por vídeo), os 3 prazos (31/12/2026, 30/06/2027 e 31/12/2027), o cenário recomendado, as metas mensais e semanais com o valor de hoje e a sensibilidade das alavancas |
| `TEMAS.md` | ranking de assuntos por **inscritos esperados por vídeo** (longos e Shorts; 12 meses e vitalício; com n, faixa p25–p75 e origem do tráfego), a conferência das regras e o que falta para medir a demanda de busca |
| `CALENDARIO-8-SEMANAS.md` / `.csv` | **calendário v2:** 21 longos e 16 Shorts escolhidos pelo ranking, com os inscritos esperados de cada pauta e a soma semanal contra a meta |
| `CALENDARIO-8-SEMANAS_v1.md` / `.csv` | calendário v1, mantido para comparação |
| `SHORTS-MES.md` | ideias de Shorts da v1, com ganchos. Para datas e assuntos, vale o calendário v2 |
| `PERGUNTAS-SEM-RESPOSTA.md` / `perguntas.csv` | as 765 perguntas sem resposta do canal, por tema, e 20 rascunhos de resposta para o Denis aprovar |
| `modelo.py` | modelo comum: carga dos dados, ranking por assunto, base de hoje, cenários e plano |
| `meta.py` (+ `meta_md.py`), `temas.py`, `calendario_v2.py`, `calendario_v1.py`, `perguntas.py` | geram os arquivos acima |
| `tests/` | testes (`python3 -m pytest tests -q`) |

Para regerar tudo, com os dados em `auditoria-canal/dados/`:

```sh
cd pautas-canal && python3 temas.py && python3 meta.py && python3 calendario_v2.py && python3 perguntas.py
```

**Assunto:** a classificação de cada vídeo sai do título, pelas regras `ASSUNTOS` em `auditoria-canal/analisar.py`. Para
mudar a classificação, edite essas regras e regere.

**Regras de todas as pautas:**
- tom simples e direto, sem clichê;
- não recomendar ativo nem citar corretora;
- fora: dívida, cartão de crédito e política;
- conferir as fontes indicadas antes de gravar ou publicar.
