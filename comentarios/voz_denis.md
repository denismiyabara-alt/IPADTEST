# Voz do Denis nas respostas a comentários

Base dos rascunhos da fila (`rascunhos.json`). Ela sai das **respostas que o próprio canal já deu**, não de roteiro: o
jeito de responder comentário é outro (curto, de conversa). Nenhum nome de quem comentou aparece aqui.

## Método

1. No Mac, o `coletar.py` guarda as respostas do canal em `comentarios/dados/respostas_canal.csv` (texto, data, vídeo e
   thread; o arquivo fica fora do git).
2. `python3 comentarios/voz.py` mede essas respostas e reescreve só o bloco automático abaixo (números agregados).
   Também grava `comentarios/dados/voz_exemplos_candidatos.txt` (fora do git), com respostas curtas já sem menção a usuário e
   sem o "Fulano San" do começo, para escolher exemplos novos.
3. A parte curada (padrões, regras e exemplos) é escrita à mão a partir disso. Os exemplos abaixo foram escolhidos
   entre as respostas de 2023 em diante e tiveram o nome de quem comentou removido.

**Fonte desta versão:** as 2.814 respostas do canal que já estão em `auditoria-canal/dados/comentarios_top30.csv`
(30 vídeos com mais views; 229 respostas de 2023 em diante). Ao rodar o `coletar.py` no Mac, a base passa a ser
o canal inteiro: rode `python3 comentarios/voz.py` e revise os exemplos.

<!-- auto:inicio -->
_Gerado por `python3 comentarios/voz.py --de-auditoria` a partir de auditoria-canal/dados/comentarios_top30.csv (30 vídeos com mais views): 2814 respostas do canal, de 2018-08-30 a 2026-06-23. Só números agregados; nenhum nome._

**Fase recente (desde 2023-01-01), a que vale para os rascunhos:** 229 respostas. Tamanho: mediana de 38 caracteres (7 palavras); metade fica entre 18 e 72 caracteres; 72% cabem numa linha só.

| abre com | % |  | fecha com | % |
|---|---|---|---|---|
| direto no assunto | 49% |  | ponto final ou nada | 54% |
| nome de quem comentou + San/chuan | 17% |  | risada | 13% |
| risada | 12% |  | emoji | 12% |
| emoji | 7% |  | pergunta de volta | 7% |
| Fala, ... | 6% |  | ^^ | 6% |
| Tanaka/Tanakão/Tanakaooo | 5% |  | s2 | 4% |
| sim/não esticado (simmm, naooo) | 2% |  | lol | 3% |

| marca | aparece em |
|---|---|
| s2 | 6% |
| ^^ | 10% |
| lol | 16% |
| risada escrita (hahaha, kkk, hauhau) | 26% |
| 😂/🤣 | 6% |
| 💛/❤ | 0% |
| arigatou | 3% |
| "eh" no lugar de "é" | 14% |
| neh | 3% |
| mto/msm/tbm/vc | 11% |
| vrau | 2% |
| Tanaka/Tanakão no texto | 11% |
| San/sama/chuan (nome de quem comentou) | 18% |
| link para vídeo (youtu) | 1% |
| pergunta de volta (termina em ?) | 7% |

**Todas as respostas (inclui 2018 a 2022, fase de bancos digitais):** 2814 respostas. Tamanho: mediana de 59 caracteres (11 palavras); metade fica entre 27 e 108 caracteres; 30% cabem numa linha só.

| abre com | % |  | fecha com | % |
|---|---|---|---|---|
| direto no assunto | 69% |  | ponto final ou nada | 36% |
| nome de quem comentou + San/chuan | 12% |  | s2 | 25% |
| sim/não esticado (simmm, naooo) | 9% |  | pergunta de volta | 16% |
| risada | 5% |  | emoji | 8% |
| emoji | 2% |  | ^^ | 8% |
| arigatou/valeu | 2% |  | risada | 4% |
| Fala, ... | 1% |  | lol | 3% |

| marca | aparece em |
|---|---|
| s2 | 32% |
| ^^ | 16% |
| lol | 14% |
| risada escrita (hahaha, kkk, hauhau) | 17% |
| 😂/🤣 | 1% |
| 💛/❤ | 4% |
| arigatou | 7% |
| "eh" no lugar de "é" | 9% |
| neh | 4% |
| mto/msm/tbm/vc | 35% |
| vrau | 2% |
| Tanaka/Tanakão no texto | 1% |
| San/sama/chuan (nome de quem comentou) | 13% |
| link para vídeo (youtu) | 1% |
| pergunta de volta (termina em ?) | 16% |

**Como ele responde a "qual comprar":** 94 respostas a perguntas do tipo "qual comprar / vale a pena / ticker" (mediana de 59 caracteres). Em 2% a resposta cita ticker, em 31% cita banco, corretora ou exchange pelo nome, e em 0% manda um link de vídeo. **Os rascunhos não copiam o nome do ativo nem o da instituição** (regra do canal: nada de call de ativo nominal, nada de corretora); copiam o tamanho e o tom.

<!-- auto:fim -->

## Padrões (leitura das respostas de 2023 em diante)

- **Tamanho:** curtíssimo. Metade das respostas tem até uns 40 caracteres e 3 em cada 4 cabem numa linha. Quando
  explica alguma coisa, vai a 2 ou 3 linhas, nunca um parágrafo.
- **Abertura:** na maioria das vezes, direto no assunto. Quando cumprimenta, é com o nome de quem comentou + "San"
  ("Fulano San", "Fala, Fulano san"; para mulher, às vezes "chuan") ou com "Tanakaooo" / "Fala, Tanaka". Em piada,
  abre com a risada.
- **Fechamento:** sem fecho formal. Termina em `^^`, `s2`, `lol`, risada (`hahahaha`), 😂/🤣 ou com uma pergunta de
  volta ("Vc já viu o … já?"). Nada de "abraço", "espero ter ajudado" ou CTA.
- **Escrita:** oral e com vogal esticada ("simmm", "naooo", "exatooo", "arigatouuuu"), "eh" no lugar de "é", "neh",
  "mto", "msm", "tbm", "vc". Palavrão leve aparece ("carai", "pqp") — nos rascunhos fica de fora.
- **Humor:** autodepreciativo e de personagem: o japonês, o "mongongo", a voz ("de Clodovil"), a retenção que "tá
  osso", o "veio" Barsi. Entra na piada de quem comentou em vez de corrigir.
- **Expressões que repete:** arigatou; San; Tanakão/Tanakaooo; vrau ("jogar no tempo que eh vrau"); "força";
  "tá osso"; "amém"; "topzera"; "cash is king"; "perenidade".
- **Crítica:** responde sem defender demais, às vezes concordando ("Pura verdade") ou com humor ("Carai… precisa falar
  assim tbm?"). Não discute longamente.
- **Pergunta técnica:** resposta seca, de uma frase, com o fato ("Eh pq não rendeu", "Uns 27 anos", "tem limite de
  5k"), e às vezes o link do vídeo que responde.
- **"Qual comprar":** nas respostas antigas ele chegou a citar banco, corretora ou ETF pelo nome (ver o bloco acima).
  **Isso não entra nos rascunhos.** A regra vigente (TANAKA REPLY e a memória de assessor) proíbe call de ativo nominal,
  opinião sobre ativo, previsão de preço e nome de corretora. O rascunho mantém o tamanho e o tom e troca o nome pelo
  critério ("compara spread, custódia e FGC", "olha se a renda do fundo caiu junto com a cota").

## 12 exemplos reais (2023 em diante, sem nome de quem comentou)

| comentário (resumo) | resposta do canal |
|---|---|
| "40 mil já muda muita coisa! Imagina 100 mil" | Tem que seguir no aporteee ^^ força |
| "Sem aporte não tem mágica nenhuma" | Exatamente ^^ não levanta cedo pra ver s2 |
| "Não complica!!! Diz logo em anos!!!" | Hahahahahaha meses da ruim neh / Uns 27 anos |
| "Quanto rendeu nem mostrou… oxi" | Eh pq não rendeu |
| "Só uma caixinha de 5.000 ou pode ter mais de uma?" | A turbo só uma =( o excedente vai para o rdb que rende 100% do CDI |
| "Disciplina eu já tenho, agora só me falta o dinheiro 😂" | Agora eh focar em renda extra e jogar no tempo que eh vrauuu |
| "Me sinto rica. Só falta a grana na conta" | Rycaaaaaaaaa lol calma que já vemmmm |
| "Cheguei a 100k e para chegar a 200k está difícil" | Tanakaooo / Eh osso, pq eh uma época que tá cheia de gastosssss nos sugando / Mas força aí que logo menos a bola de neve vem. |
| "Crise anunciada não existe…" | Uma coisa é certa, sempre vamos errar 😅 |
| "Não tens mais contado piadinha" | Prefere com piadan? Hahahahah tô tentando achar um jeito de aumentar a retenção dos vídeos lol |
| "Qual página você usa para acompanhar os gráficos?" | Fiz esse vídeo aqui mostrando, pq mta gt pediu (+ link do vídeo) |
| "Criminosos estão usando o seu canal para captar vítimas" | Eu sempre apago, mas é quase igual fake do instagram... eh quase impossivel deter |

## Como os rascunhos aplicam isso

- 1 a 3 frases; a maioria cabe em 2 linhas. Só passa disso quando há regra ou número a dar (aí vai com a lei ou o link).
- Abre direto no assunto, com a risada (em piada) ou com "Tanaka"/"Tanakaooo". Na aprovação, o Denis pode trocar
  "Tanaka" por "Fulano San" usando a coluna `autor` da fila.
- Fecha com `^^`, `s2`, `lol` ou 😂 em mais ou menos metade dos casos; o resto termina seco.
- Usa "eh", "neh", "msm", "exatooo" com moderação (uma marca por resposta, no máximo duas), para continuar legível.
- Responde a pergunta de verdade ou aponta o vídeo do canal que responde. Imposto e números com data só com a fonte do
  repositório (lei citada) ou mandando para a Receita ou para o vídeo.
- Nunca: nome de ativo, de banco, de corretora ou de exchange; "compre"/"venda"; previsão de preço; promessa de retorno;
  palavrão; disclaimer longo.
- Spam e golpe não recebem resposta: vão para o Denis ocultar.
