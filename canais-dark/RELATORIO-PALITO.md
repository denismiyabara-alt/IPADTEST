# Canais "dark" de homem palito em PT-BR: mercado, nichos e produção

Pesquisa de 03/10/2026 para o Denis Miyabara. O canal do Mossad é outro formato (documentário) e está em `RELATORIO-MOSSAD.md`.

**Como ler os números.** Cada dado traz a fonte e a data. Quase todos os sites de estatística (Social Blade, vidIQ, HypeAuditor, OutlierKit) e as páginas oficiais do YouTube estavam **bloqueados** nesta sessão. Por isso, onde está escrito **[só busca]**, o número veio do resumo do buscador que cita aquela página, e não da página aberta. "Calculado" é uma conta feita a partir de números com fonte. "Estimativa" diz o método. Nenhum número foi inventado. Onde não achei o dado, está escrito "não medido".

---

## Resumo

- **O formato funciona nos EUA, mas o que estoura é o roteiro.** OverSimplified tem 9,65 mi de inscritos com só 33 vídeos (~43 mi de views por vídeo, calculado), e Sam O'Nella tem 4,8 mi com 69 vídeos. Os dois postam pouco e se apoiam em humor e em narrativa. O Infographics Show (15,6 mi) é o oposto: mais de 9 vídeos por semana e ~1,1 mi de views por vídeo. **O palito é barato de desenhar. O roteiro é que custa.**
- **Em PT-BR não achei um canal de palito explicando história ou golpes** (busca, sem ferramenta de canal). O buraco existe, mas tem dois rivais novos: os canais "faça um palito com IA" (o nicho virou tutorial de renda passiva, inclusive em PT) e a **dublagem automática do YouTube**, aberta a todos os criadores desde 04/02/2026, que leva os canais americanos para o português.
- **O risco nº 1 é a política de conteúdo inautêntico** (15/07/2025), que tira da monetização o canal feito em massa a partir de molde. Palito + voz sintética é exatamente o perfil que o YouTube está caçando. A defesa é a mesma do Faz a Conta: roteiro autoral, fatos conferidos e cenas que mudam de verdade de um vídeo para o outro. **Não pode virar fábrica.**
- **Comece por 2 nichos:** (1) **História contada com humor** e (2) **Golpes famosos da história** (como o golpe funcionava, sem pessoa física viva). Evite "curiosidades" e "o que acontece se" (saturados e com o maior risco de "molde"). "Dinheiro explicado" já é o Faz a Conta: não abra outro canal disso.
- **Produção:** o Faz a Conta **já tem um palito em SVG/GSAP** (`megasena/build_hf.py`, com cabeça, braços, pernas, bocas e reações). Falta ganhar cotovelo e joelho e um banco de ações (andar, correr, apontar, se esconder). O vídeo de 8 min custa ~1 h 30 de máquina no Mac de 16 GB (voz ~80 min, render ~7 a 10 min) e cerca de 6 a 10 h de trabalho humano (estimativa). O custo em dinheiro é perto de zero.
- **A voz** é uma voz própria do canal, desenhada por texto no Qwen3-TTS VoiceDesign, **sem áudio de referência de pessoa real**. Não é a do Denis: no Faz a Conta, o `synth_qwen_clone.py` clona a voz dele (`REF = "ref_denis_OFICIAL.wav"`), e isso não pode ir para um canal anônimo.

---

## 1. Mercado nos EUA: os maiores canais de palito e de animação simples

| Canal | Inscritos (data) | Views totais / vídeos | Views por vídeo | Frequência | Estilo | Fonte |
|---|---|---|---|---|---|---|
| Kurzgesagt | 25,6 mi (set/2026) | não medido | não medido | baixa | animação vetorial "flat", ciência | [HypeAuditor](https://hypeauditor.com/youtube/UCsXVk37bltHxD1rDPwtNM8Q/) [só busca] |
| The Infographics Show | 15,6 mi | 6,9 bi | ~1,1 mi (média citada) | 9+ por semana | bonecos simples, "o que acontece se", comparações, histórias de sobrevivência | [HypeAuditor](https://hypeauditor.com/youtube/UCfdNM3NAhaBOXCafH7krzrA/), [youtubers.me](https://us.youtubers.me/the-infographics-show/youtube-videos-stats) [só busca] |
| Psych2Go | 13,2 mi (set/2026) | não medido | não medido | alta | animação simples, psicologia e saúde mental | [HypeAuditor](https://hypeauditor.com/youtube/UCkJEpR7JmS36tajD34Gp4VA/) [só busca] |
| OverSimplified | 9,65 mi (2026) | 1,4 bi / 33 vídeos | **~43 mi (calculado)**; o maior, WW2 parte 1, tem 104 mi | 1 por ano ou menos | **palito**, humor, piadas recorrentes, vídeos longos em partes | [Social Blade](https://socialblade.com/youtube/handle/oversimplified), [Fandom](https://youtube.fandom.com/wiki/OverSimplified) [só busca] |
| Simple History | 5,08 mi (jan/2026) | 1,64 bi / 1.265 vídeos | ~1,3 mi (calculado) | semanal | bonecos simples, guerra e história, curtos | [vidIQ](https://vidiq.com/youtube-stats/channel/UC510QYlOlKNyhy_zdQxnGYw/) [só busca] |
| Sam O'Nella Academy | 4,8 mi+ | 769,5 mi / 69 vídeos (set/2026) | ~11 mi (calculado) | rara; ficou ~3 anos parado | **palito tosco**, humor ácido, história pouco conhecida | [Plugged In](https://www.pluggedin.com/youtube-reviews/sam-onella-academy/), [vidIQ](https://vidiq.com/youtube-stats/channel/@samonellaacademy/) [só busca] |
| Casually Explained | 4,2 mi (set/2026) | 525 mi / 107 vídeos | ~4,9 mi (calculado) | rara | **palito** com narração monótona e seca, comportamento | [HypeAuditor](https://hypeauditor.com/youtube/UCr3cBLTYmIK9kY0F_OdFWFQ/), [youtubers.me](https://us.youtubers.me/casually-explained/youtube-videos-stats) [só busca] |
| Economics Explained | 2,86 mi | 362,5 mi | não medido | semanal | gráficos e ilustração, economia | [vidIQ](https://vidiq.com/youtube-stats/channel/UCZ4AMrDcNrfy3X6nsU8-rPg/) [só busca] |
| MagnatesMedia | ~1,9 mi | não medido | não medido | não medido | documentário de negócios, golpes e fraudes | [creatordb](https://creatordb.app/creatorstats/magnatesmedia/) [só busca] |
| Hoog | 1,0 mi (18/08/2025) | não medido | não medido | não medido | ilustração simples, ensaios sobre a Europa | [Fandom](https://youtube.fandom.com/wiki/Hoog) [só busca] |
| Alan Becker (referência de palito, não explicativo) | 34 mi | não medido | não medido | — | palito de ação, sem narração | [Bloop Animation](https://www.bloopanimation.com/6-stick-figure-animators-you-should-know/) [só busca] |

Canais de **palito para true crime** existem (Stickman Crimes, Stickman Crime, Stickman Horror Stories, True Crimes Animated), mas a busca não trouxe os inscritos ([busca](https://www.youtube.com/@StickmanCrimesReal)). Não medi.

### Estrutura de roteiro dos que dão certo (padrão observado)

1. **Gancho em 10 a 20 s com a promessa do vídeo**, e não com a apresentação do canal. Exemplo: "Napoleão perdeu para… o inverno, e para ele mesmo".
2. **Um narrador com personalidade.** O deadpan do Casually Explained, o humor ácido do Sam O'Nella e as piadas recorrentes do OverSimplified são o produto. O desenho é suporte ([Async sobre o OverSimplified](https://async.com/blog/who-is-oversimplified/) [só busca]).
3. **Personagens com "vontade".** Cada figura histórica vira um palito com um desejo e um defeito (ambicioso, teimoso, medroso). A história anda por conflito, e não por data.
4. **Ritmo de piada a cada 20 a 40 s**, muitas vezes com a imagem contradizendo a narração ("ele estava calmo", e o palito está pegando fogo). Essa é a regra do gênero, observada; não há estudo de retenção público que dê o número.
5. **Série em partes** (OverSimplified: WW2 parte 1 e 2, Napoleão 1 e 2). As duas partes de Napoleão ocuparam o 1º e o 2º lugar dos Em Alta ao mesmo tempo em mai/2021 ([Fandom](https://youtube.fandom.com/wiki/OverSimplified) [só busca]).

### O que faz o vídeo estourar

- **Tema grande e conhecido, ângulo inesperado.** O maior vídeo do OverSimplified é sobre a Segunda Guerra (104 mi). O Sam O'Nella vai pelo fato obscuro ("o homem mais faminto da história").
- **Raridade com qualidade.** O OverSimplified posta menos de 1 vídeo por ano, e cada um vira evento. O Infographics Show faz o contrário (volume) e tem uma média 40 vezes menor por vídeo (calculado: 43 mi contra 1,1 mi).
- **Título e miniatura com um palito e uma situação absurda**, legível no celular.
- **Não é a animação.** A tendência de 2025/26 é o palito feito por IA em massa ("o nicho do palito com IA está explodindo", vídeos-tutorial no YouTube, [exemplo](https://www.youtube.com/watch?v=YoDCFb65gJ0); ferramentas como o [StickReel](https://stickreel.com/) [só busca]). Em PT também já há o tutorial "automatizei um canal de boneco palito com IA (fatura US$ 11 mil/mês)" ([YouTube](https://www.youtube.com/watch?v=iZcu2-xyMc4) [só busca], número do próprio vendedor do método, **não verificado**). **Isso é concorrência de volume e alvo da política de conteúdo inautêntico**, não um modelo a copiar.

---

## 2. O que já existe em PT-BR

| Canal | Inscritos (data) | Formato | Relação com o palito | Fonte |
|---|---|---|---|---|
| Fatos Desconhecidos | 22,86 mi (abr/2026) | apresentadores + edição, curiosidades | domina "curiosidades" | [HypeAuditor](https://hypeauditor.com/youtube/UCbAiIkPobUFy71zlmwVw3jw/) [só busca] |
| Ciência Todo Dia | 7,76 mi (2026) | apresentador, "e se…" de física | ocupa "o que acontece se" com ciência | [busca](https://www.nsctotal.com.br/educacao/jovem-balneario-camboriu-ensina-ciencia-youtube-reune-milhoes-inscritos) [só busca] |
| Nerdologia | 3,4 mi (2026) | animação + narração de historiador (história às terças) | o mais perto do formato de história animada | [Wikipédia PT](https://pt.wikipedia.org/wiki/Nerdologia), [usepora](https://www.usepora.com.br/influenciador/nerdologia) [só busca] |
| Minutos Psíquicos | ~1,75 mi | **animação narrada** de psicologia, vídeos de até 10 min | concorrente direto em "psicologia" | [Psicologias do Brasil](https://www.psicologiasdobrasil.com.br/em-pouco-minutos-canal-do-youtube-ensina-psicologia-de-maneira-facil-e-ludica/) [só busca] |
| Fabiano Cruz | 1,4 mi | palito de luta (cultura pop) | palito, mas sem narração | [Bloop Animation](https://www.bloopanimation.com/6-stick-figure-animators-you-should-know/) [só busca] |
| Buenas Ideias | 600 mil+ | Eduardo Bueno com o rosto, história do Brasil | história com humor, com rosto | [Quero Bolsa](https://querobolsa.com.br/revista/8-canais-do-youtube-para-quem-ama-historia) [só busca] |
| Show de Informações (Infographics Show em PT) | não medido | **dublagem oficial** do Infographics Show (Linguana) | o gigante americano já fala português | [YouTube](https://www.youtube.com/@showdeinformacoes-infographics) [só busca] |
| True crime BR (Crime e Mistério S/A, Freak TV, Investigação Criminal, Crimes.com) | não medido | apresentador com o rosto | crimes, sem palito | [SP Diário](https://spdiario.com.br/noticias/entretenimento/top-10-canais-de-true-crime-brasileiros-que-vao-te-viciar-no-youtube.html) [só busca] |
| TV Palitinho, O Palito Cor de Rosa, Palitomania | não medido | palito de humor e cotidiano | palito sem conteúdo explicativo | [busca](https://www.youtube.com/@tvpalitinho) [só busca] |

**O buraco:** a busca não mostrou nenhum canal brasileiro de **palito narrado explicando história ou golpes** no estilo OverSimplified/Sam O'Nella. **Ressalva:** sem acesso ao YouTube por ferramenta, isso é ausência na busca, e não prova de que não existe. Antes de gravar, procure no próprio YouTube por "história em palitinho", "boneco palito história", "golpe animado" e "resumo animado" (filtro: canal) e anote o que achar.

**Dublagem automática.** O YouTube abriu a dublagem automática por IA a todos os criadores em 04/02/2026, em 27 idiomas, e o português está entre os 8 com a "Expressive Speech", que imita a entonação ([Winbuzzer](https://winbuzzer.com/2026/02/05/youtube-ai-auto-dubbing-all-creators-27-languages-xcxwbn/), [India TV](https://www.indiatvnews.com/technology/news/youtube-auto-dubbing-feature-expands-to-all-users-now-supports-27-languages-2026-02-05-1029070) [só busca]). Na prática, o OverSimplified e o Simple History **podem aparecer dublados** para o brasileiro. O canal nacional só ganha com o que a dublagem não faz: **assunto brasileiro, piada brasileira e referência local**.

---

## 3. RPM em PT-BR (estimativa)

| Referência | Faixa | Fonte | Tipo |
|---|---|---|---|
| Brasil, média geral | R$ 3 a R$ 10 por mil views | [Minha Contabilidade Online](https://www.minhacontabilidadeonline.com.br/post-blog/quanto-o-youtube-paga-por-visualizacao/) [só busca] | estimativa de terceiro |
| Brasil, educação | R$ 7 a R$ 14 por mil | mesma fonte [só busca] | estimativa de terceiro |
| Conteúdo em português/espanhol da América Latina | US$ 0,50 a US$ 2 "típico"; US$ 2 a 4 "bom" | [VloggingPro / Fluxnote](https://vloggingpro.com/youtube-cpm/) [só busca] | estimativa de terceiro |
| CPM médio no Brasil em 2026 | ~US$ 2,80 (finanças ~US$ 4,50; games ~US$ 1,30) | [Fluxnote](https://fluxnote.io/guides/youtube-cpm-brazil) [só busca] | CPM (antes do corte do YouTube), não RPM |
| EUA, história e documentário (comparação) | US$ 6 a 14 de RPM (típico ~US$ 9) | [Learning Revolution / Fluxnote](https://fluxnote.io/blog/youtube-rpm-by-niche-2026) [só busca] | estimativa de terceiro |

**Faixa de trabalho para os canais de palito em PT-BR: R$ 3 a R$ 10 por mil views (estimativa).** Método: a faixa geral do Brasil, cruzada com os US$ 0,50 a 2 da América Latina (a cerca de R$ 5 por dólar, ≈ R$ 2,50 a R$ 10). Golpes e dinheiro puxam para cima, porque atraem anunciante financeiro; curiosidade e "e se" puxam para baixo. **Âncora real:** o RPM do Investir e Coçar no Studio. É finanças, logo mais alto que história, mas é o único número medido de público brasileiro que o Denis tem. Use-o como teto.

**Conta de sanidade (estimativa):** 100 mil views por mês a R$ 3–10 por mil = **R$ 300 a R$ 1.000 por mês**. O canal só paga a hora de roteiro com dezenas de milhares de views por vídeo. Antes da monetização, o YouTube exige 1.000 inscritos e 4.000 horas de exibição em 12 meses (ou 10 mi de views de Shorts) ([vidIQ](https://vidiq.com/blog/post/youtube-partner-program-guide/), [Tella](https://www.tella.com/blog/how-to-join-youtube-partner-program) [só busca]). Uma fonte diz que a exigência sobe para 8.000 horas em 01/02/2027 ([busca](https://www.analyticsinsight.net/apps/youtube-partner-program-eligibility-requirements)), mas **não confirmei** na página oficial (bloqueada).

---

## 4. Os nichos avaliados

Escala de risco de política: **baixo** (roteiro autoral resolve), **médio** (exige cuidado em todo vídeo) e **alto** (o formato em si atrai a política).

### 4.1 História contada com humor (estilo Sam O'Nella / OverSimplified, com assunto brasileiro)

- **Tema:** episódios da história do Brasil e do mundo contados como comédia de personagens. Por exemplo: a Revolta da Vacina, a Guerra do Paraguai em 2 partes, a fuga da família real, o Encilhamento, "o dia em que o Brasil declarou guerra por um navio".
- **Demanda:** o Nerdologia separa um dia da semana para história (3,4 mi de inscritos); o Buenas Ideias vive de história do Brasil com humor (600 mil+). Nos EUA, é o nicho de palito que mais rende por vídeo (OverSimplified ~43 mi por vídeo, calculado). Google Trends e as sugestões de busca **não foram medidos** (bloqueados).
- **Concorrência BR:** com rosto (Buenas Ideias) ou com animação séria (Nerdologia). No palito com humor, não achei ninguém (só busca). O americano dublado é o rival, e perde em assunto brasileiro.
- **RPM:** R$ 3 a R$ 10 por mil (estimativa acima).
- **Risco de política: baixo a médio.** Baixo se cada roteiro é autoral e tem fonte; médio pela violência (guerra em desenho) e pelos temas raciais da história brasileira (escravidão), que pedem cuidado de tom: **humor nunca às custas da vítima.**
- **Veredito: começar.**

### 4.2 "O que acontece se…"

- **Tema:** hipóteses ("e se a Terra parasse de girar", "e se você não dormisse por 11 dias").
- **Demanda:** alta e comprovada nos EUA (Infographics Show, 15,6 mi).
- **Concorrência BR:** Ciência Todo Dia (7,76 mi) faz "e se" de física com apresentador; o próprio Infographics Show já tem a versão dublada oficial ("Show de Informações").
- **RPM:** baixo a médio (público jovem e amplo).
- **Risco de política: alto.** É o formato mais copiado pelas fábricas de IA, com título-molde, roteiro-molde e cena-molde. Foi esse perfil que o YouTube atingiu em jan/2026, quando baniu 11 canais de "AI slop" e esvaziou outros 6, que somavam 4,72 bi de views e 35 mi de inscritos segundo o levantamento da Kapwing ([Tubefilter](https://www.tubefilter.com/2026/01/29/youtube-ai-slop-channel-crackdown-bans/), [Android Headlines](https://www.androidheadlines.com/2026/01/youtube-wiped-ai-slop-erasing-4-7-billion-views-from-low-quality-content.html) [só busca]).
- **Veredito: evitar.**

### 4.3 Psicologia e comportamento (estilo Casually Explained / Psych2Go)

- **Tema:** comportamento do dia a dia, vieses e hábitos. "Por que você procrastina", "o efeito Dunning-Kruger no grupo da família".
- **Demanda:** Psych2Go 13,2 mi e Casually Explained 4,2 mi nos EUA; no Brasil, Minutos Psíquicos ~1,75 mi.
- **Concorrência BR:** o Minutos Psíquicos já ocupa a animação narrada de psicologia, feita por psicólogo. O humor seco do Casually Explained em PT está livre (só busca).
- **RPM:** médio. Saúde mental às vezes cai em "não adequado para a maioria dos anunciantes", mesmo quando é legítima ([Marvelous](https://www.heymarvelous.com/blog/youtube-demonetization) [só busca]).
- **Risco de política: médio.** A política de desinformação médica vale para ansiedade, depressão e afins ([YouTube Help](https://support.google.com/youtube/answer/13813322?hl=en) [só busca]). Regra: nada de diagnóstico nem de tratamento; só comportamento e estudos citados.
- **Veredito: terceira opção.** Bom se o tom for humor de comportamento (Casually Explained), e não "saúde mental".

### 4.4 Dinheiro e economia explicados

- **O choque:** o **Faz a Conta já é um canal de palito** (o `build_hf.py` do megasena desenha o palito com bocas e reações) sobre contas e dinheiro, e o Investir e Coçar é finanças com o rosto do Denis. Um terceiro canal de "dinheiro explicado" disputaria a mesma busca, o mesmo público e a mesma voz editorial.
- **Concorrência:** Economics Explained (2,86 mi) nos EUA; no Brasil, os próprios canais do Denis.
- **RPM:** o mais alto da lista (finanças: CPM ~US$ 4,50 no Brasil, [Fluxnote](https://fluxnote.io/guides/youtube-cpm-brazil) [só busca]).
- **Risco:** de política, baixo; **reputacional e regulatório, alto.** O Denis é sócio de escritório ligado a banco: conteúdo anônimo de dinheiro, se ligado a ele, vira comunicação não identificada sobre investimento.
- **Veredito: evitar como canal novo.** Se quiser história econômica (hiperinflação, Plano Real, a bolha das tulipas), **ponha no Faz a Conta** como série. Se um dia separar, a única diferenciação limpa é **só história econômica antes de 2000**, sem produto, sem ativo e sem recomendação.

### 4.5 Crimes e golpes famosos

- **Tema:** **golpes** históricos e como funcionavam. Ponzi (1920), Madoff, a Enron, o "homem que vendeu a Torre Eiffel" (Victor Lustig), a fraude das tulipas, os bilhetes premiados falsos. **Crime violento fica fora** (true crime com vítima de homicídio pede outro nível de cuidado e é dominado por apresentadores).
- **Demanda:** 33,4% dos brasileiros (~56 mi) caíram em golpe financeiro virtual em 12 meses (Datafolha para o Fórum Brasileiro de Segurança Pública, [InfoMoney](https://www.infomoney.com.br/brasil/datafolha-golpes-virtuais-atingem-1-3-dos-brasileiros-e-envolvem-r-112-bi-em-1-ano/), ago/2025 [só busca]); foram 2,2 mi de estelionatos registrados em 2025 ([O Tempo](https://www.otempo.com.br/brasil/2026/7/23/em-sete-anos-crime-de-estelionato-quintuplicou-brasileiros-sofreram-258-golpes-por-hora-em-2025), 23/07/2026 [só busca]). Nos EUA, o MagnatesMedia (~1,9 mi) vive de fraudes e quedas.
- **Concorrência BR:** o true crime brasileiro é de apresentador e de crime violento. **Golpe histórico em palito não apareceu** (só busca).
- **RPM:** médio a alto (anunciante de banco, segurança e finanças), estimativa.
- **Risco de política: médio. Risco jurídico: o maior da lista.** Difamação e calúnia (Código Penal, arts. 138 a 140). Regras: só caso com **condenação definitiva** ou de pessoa morta há muito tempo; nunca pessoa física viva sem condenação; nunca empresa ou banco em atividade sem decisão judicial publicada, citada na tela; **vítima sem nome** (só o número de lesados); e o vídeo ensina o mecanismo para a pessoa se proteger, sem dar o passo a passo do golpe.
- **Veredito: começar** (segundo canal). Casa com a credibilidade do Denis sem precisar do nome dele.

### 4.6 Curiosidades

- **Concorrência:** o Fatos Desconhecidos tem 22,86 mi (abr/2026), e o formato "10 fatos" é o mais fácil de virar molde.
- **Risco de política: alto** (lista + voz sintética + banco de imagem é a definição de inautêntico).
- **Veredito: evitar.**

### Quadro final

| Nicho | Demanda (sinal) | Concorrência BR em palito | RPM (estimativa) | Risco de política | Decisão |
|---|---|---|---|---|---|
| História com humor | alta (EUA); média (BR) | não achei | R$ 3–10/mil | baixo a médio | **começar** |
| Golpes famosos | alta (BR: 1 em 3 caiu em golpe) | não achei | médio a alto | médio (+ risco jurídico) | **começar** |
| Psicologia e comportamento | alta | Minutos Psíquicos | médio | médio | 3ª opção |
| "O que acontece se" | alta | dublado do Infographics + Ciência Todo Dia | baixo a médio | alto | evitar |
| Dinheiro explicado | alta | os canais do Denis | alto | baixo (política) / alto (reputação) | evitar; vai pro Faz a Conta |
| Curiosidades | alta | Fatos Desconhecidos | baixo a médio | alto | evitar |

**Por que esses 2 primeiro:** (1) é onde a busca não achou concorrente em palito e onde o americano dublado não chega (assunto brasileiro, ou golpe contado com contexto brasileiro); (2) os dois aproveitam o que o stack já faz bem, que é **conferir fato** (a trava de "números conferidos" do `fazer.py` vira trava de "fatos conferidos"); (3) a pauta não acaba (centenas de episódios históricos e de golpes documentados); e (4) o risco de "molde" é controlável, porque cada história pede cenário e personagem diferentes.

---

## 5. Política do YouTube em 2026: as regras para os canais de palito

As páginas oficiais (support.google.com) estavam bloqueadas; os links são os oficiais encontrados na busca, e o resumo vem das reportagens citadas.

1. **Conteúdo inautêntico** (antes "repetitivo"; renomeado em 15/07/2025): fica fora da monetização o conteúdo "produzido em massa ou repetitivo", feito de molde com pouca variação ([Search Engine Journal](https://www.searchenginejournal.com/youtube-targets-mass-produced-content-in-monetization-update/550337/), [Social Media Today](https://www.socialmediatoday.com/news/youtube-clarifies-monetization-update-inauthentic-repeated-content/752892/) [só busca]; página oficial: [Políticas de monetização do YPP](https://support.google.com/youtube/answer/1311392)). Em jun/2026, a Hollywood Reporter registrou que canais faceless sem IA também foram atingidos ([THR](https://www.hollywoodreporter.com/business/digital/faceless-creators-youtube-ai-damage-1236617586/) [só busca]).
   **Regra:** cada vídeo tem roteiro escrito para ele, com fonte; no máximo 1 vídeo por semana por canal no começo; cada episódio traz pelo menos 3 cenários ou props novos (o teste de cenas confere); título e miniatura nunca saem de molde de texto; nada de cron. Alguns blogs falam em limiares ("narração abaixo de 30% do tempo", "20% de variação de roteiro") ([exemplo](https://aituber.app/blog/faceless-youtube-channels-demonetized-2026/)); **não são oficiais** e não devem ser tratados como regra.
2. **Conteúdo reutilizado:** usar material de terceiros sem transformação. O palito desenhado em código e o roteiro próprio não caem aqui. **Regra:** nada de trecho de filme, de série ou de outro canal.
3. **Rótulo de conteúdo alterado ou sintético:** obrigatório quando o conteúdo **realista** pode ser confundido com pessoa, lugar ou evento real; animação claramente irreal não precisa ([Blog do YouTube](https://blog.youtube/news-and-events/disclosing-ai-generated-content/), [PPC Land](https://ppc.land/youtube-introduces-mandatory-disclosure-for-ai-content/) [só busca]). **Regra:** o palito não exige o rótulo. Mesmo assim, a descrição de todo vídeo diz "Narração com voz sintética criada para o canal", e nenhum vídeo usa imagem realista gerada por IA de pessoa real.
4. **Violência em desenho:** a violência em animação claramente fictícia é monetizável; a violência real em contexto educativo ou histórico depende do contexto, e o foco no sangue ou no ferimento não é adequado para anunciantes ([Diretrizes para anunciantes](https://support.google.com/youtube/answer/6162278?hl=en), [Violência](https://support.google.com/youtube/answer/2802008?hl=en) [só busca]). Em jan/2026, o YouTube afrouxou a regra para temas sensíveis dramatizados e não gráficos ([TechCrunch](https://techcrunch.com/2026/01/16/youtube-relaxes-monetization-guidelines-for-some-controversial-topics/) [só busca]). **Regra:** morte sai de cena (corte, "X" no olho, silhueta); sem sangue nem detalhe de ferimento; guerra é mapa e seta.
5. **Semelhança e voz de pessoa real:** o YouTube tem a "detecção de semelhança" para criadores e trata o uso de rosto ou voz por IA como questão de privacidade, com pedido de remoção ([YouTube Help](https://support.google.com/youtube/answer/16440338?hl=en), [MediaNama, set/2026](https://www.medianama.com/2026/09/223-youtube-likeness-detection-voices-clones/) [só busca]). **Regra:** item 7.

---

## 6. Produção: o palito em código, no stack do Faz a Conta

### 6.1 O que já existe e o que falta

O `faz-a-conta/megasena/build_hf.py` já desenha um palito em SVG (`<svg id="stick">`) com grupos `st-flip > st-jump > st-breath`, a cabeça `st-head` com 4 bocas (`bc-neutro`, `bc-feliz`, `bc-triste`, `bc-choque`), os braços `st-armL/R` e as pernas `st-legL/R`, **cada membro com um segmento só**. Há um filtro de "boil" (traço que treme), 5 poses (`idle`, `shrug`, `hands`, `point`, `cheer`) e reações automáticas à cena: tranco quando a tela treme, pulo no carimbo, alavanca, cabeça seguindo o número. O GSAP gira cada grupo em torno da articulação com `svgOrigin`.

**Falta, para contar história:** cotovelo e joelho (andar e correr pedem 2 segmentos), **vários palitos** em cena (personagens), acessórios (chapéu, bigode, coroa, maleta), cenário e câmera.

### 6.2 Esqueleto proposto (`palito/esqueleto.py`, gera o SVG)

```
raiz (quadril, x,y)        ← translada (andar, correr, cair)
├─ tronco                  ← inclina (agachar, correr)
│  ├─ pescoço > cabeça     ← olhar, susto; bocas e olhos trocam por opacity
│  ├─ ombroE > braçoE > antebraçoE > mãoE(prop)
│  └─ ombroD > braçoD > antebraçoD > mãoD(prop)   ← apontar, segurar a maleta
├─ coxaE > canelaE
└─ coxaD > canelaD
```

- Cada nó é um `<g>` com a articulação na origem local (o `svgOrigin` fica fixo por osso); a rotação é sempre relativa ao pai. Assim, a pose é só um **dicionário de ângulos**.
- **Identidade do personagem por acessório e cor de traço**, e não por anatomia: `personagem("napoleao", chapeu="bicorne", cor="#1d3557")`. Os acessórios entram em `cabeça` ou em `mão`.
- **Poses** (`palito/poses.json`): `idle`, `apontar`, `shrug`, `pensar` (mão no queixo), `susto`, `agachar`, `espiar` (agachado, cabeça para o lado), `esconder` (agachar + translado para trás do prop + opacity parcial), `carregar`, `cair`, `vitória`, `sentar`. Os limites de ângulo por articulação ficam no JSON e são conferidos em teste (joelho não dobra para a frente).
- **Banco de ações** (`palito/acoes.js`, gerado pelo Python, como o `reacoes()` de hoje): `acao(id, nome, T, D, opcoes)` emite os `tl.to(...)` na timeline mestre.
  - `andar`: ciclo de 4 poses-chave (contato, passagem, contato, passagem) com `repeat` calculado de D, mais translado da raiz com `ease:'none'` e um sobe-e-desce de 6 px no quadril.
  - `correr`: ciclo de 4 poses com o tronco inclinado 15°, passo maior, braços opostos às pernas.
  - `apontar(alvo)`: gira o braço até o ângulo do alvo (calculado em Python, pela posição do alvo na cena).
  - `esconder(prop)`: corre até o prop, agacha, a cabeça espia 2 vezes.
  - `falar`: alterna as bocas no tempo das sílabas fortes, lidas do `beats.json` da voz (o Faz a Conta já sincroniza a boca com as pausas).
  - `entrar` / `sair` (pela borda), `virar` (`scaleX:-1` no `st-flip`), `cair`, `levantar`.
- **Determinismo:** o HyperFrames renderiza quadro a quadro, buscando a posição na timeline. Então tudo fica numa timeline GSAP pausada: sem `Math.random()` em tempo de execução (o "aleatório" sai do Python com semente fixa) e sem `requestAnimationFrame` próprio. É a mesma regra das cenas de hoje.

### 6.3 Cenários e peças

- **Câmera:** `#stage` com zoom e pan (já usado nos zooms de punchline).
- **Mapa:** SVG simplificado gerado em Python a partir do Natural Earth, que é de domínio público ([naturalearthdata.com](https://www.naturalearthdata.com/about/terms-of-use/), termos não abertos nesta sessão; conferir). O palito anda por cima do mapa e a seta da rota se desenha (`stroke-dashoffset`, como a linha do `motion/grafico_cotacao`).
- **Linha do tempo:** eixo horizontal com anos que acendem; a câmera corre por ele.
- **Props:** porta, mesa, trono, navio, cofre, carta e saco de dinheiro, todos SVG de traço único, para combinar com o "boil".
- **Balões e cartelas:** reaproveitar `fala()`, `card()`, `big()` e `slam()` do `cenas_hf.py`. O `card(titulo, fonte)` vira a **fonte na tela** de cada fato.

### 6.4 Formato de roteiro e de cenas (adaptando o FORMATO-EPISODIO.md)

O `roteiro.md` continua igual; muda o nome e o conteúdo do quadro. A trava do `fazer.py` funciona sem mudar o código, porque só olha a coluna `status`.

```markdown
# O HOMEM QUE VENDEU A TORRE EIFFEL (DUAS VEZES)

## Números conferidos

| id | fato ou número | fonte | status |
|---|---|---|---|
| ano | 1925 | [livro/reportagem com autor e ano] | conferido |
| vezes | duas vezes | [mesma] | a conferir |

## Notas

Tom: humor seco, nunca às custas da vítima. Vítimas sem nome.
Personagens: lustig (chapéu-coco, bigode), comprador (cartola).

## B0 — GANCHO
* cena: lustig de pé na frente da torre; câmera abre do bigode para a torre
Em mil novecentos e vinte e cinco, um homem vendeu a Torre Eiffel.
Para um ferro-velho.  ⏸
E depois vendeu de novo.  ⏸ {0.95}
```

**Estrutura de episódio (8 a 12 min):**

| Bloco | Tempo | Função |
|---|---|---|
| B0 Gancho | 0:00–0:30 | a promessa absurda e verdadeira |
| B1 Quem era | 0:30–2:00 | personagem com desejo e defeito |
| B2 O plano | 2:00–4:30 | o mecanismo (no golpe: como funcionava) |
| B3 Deu certo | 4:30–6:30 | escalada; piada recorrente |
| B4 Deu errado | 6:30–8:30 | a queda e a consequência real |
| B5 Fecho | 8:30–9:30 | o que isso ensina hoje (no golpe: como se proteger) e as fontes na tela |
| B6 Tela final | ~22 s | como no Faz a Conta |

O `cenas_hf.py` mantém o formato atual (`cenas_<b>()` → `(C, P)`, cena presa a **trecho da frase**) e ganha o `P` de personagens: `{frase: [("lustig", "andar", {"de":200,"ate":900}), ("comprador","susto")]}`.

### 6.5 Tempo e custo por vídeo no Mac de 16 GB

**Base medida** (`TESTE-RENDER.md`, megasena, 03/10/2026): voz de 1 bloco de 16 frases em ~10 min; conferência (Whisper large-v3, 95 frases) em 2 min 23 s; render de 8 blocos + emenda em 6 min 42 s para um final de 496,5 s; efeitos em 20 s e mix em 20 s. O pico de memória foi de 2,05 GB.

**Taxas calculadas:** render ≈ 402 s ÷ 496,5 s ≈ **0,81 s de máquina por segundo de vídeo**; voz ≈ 10 min por bloco de ~59 s de fala (474 s de fala ÷ 8 blocos, tirando a tela final de 22 s) ≈ **10 min de máquina por minuto de fala** (medido em 1 bloco só; é a medida mais fraca).

**Vídeo de palito de 9 min (8 min 30 s de fala + tela final), estimativa:**

| Etapa | Máquina | Como estimei |
|---|---|---|
| voz | ~85 min | 8,5 min de fala × 10 min |
| conferência | ~2,5 min | proporcional às 95 frases medidas |
| render | 7 a 11 min | 540 s × 0,81 = 7,3 min; até 1,5× com mais personagens e ciclos de andar |
| efeitos + mix | ~1 min | medido: 40 s para 8 min |
| **total de máquina** | **~1 h 35 a 1 h 40** | roda à noite, um job pesado por vez (a trava do `fazer.py`) |

| Trabalho humano (estimativa, não medida) | Horas |
|---|---|
| pesquisa e conferência de fatos | 2 a 3 |
| roteiro com humor (a parte que decide o vídeo) | 2 a 3 |
| direção de cenas (`cenas_hf.py`) | 2 a 4 nos primeiros; 1 a 2 quando o banco de ações estiver maduro |
| revisão do vídeo + miniatura + título | 1 |
| **total** | **~6 a 10 h por vídeo** |

**Custo em dinheiro:** perto de zero. Voz, Whisper e render são locais; a trilha pode vir da Biblioteca de Áudio do YouTube, que é grátis. A energia é desprezível: supondo ~40 W de consumo do Mac sob carga (suposição, não medido) × 1,7 h ≈ 0,07 kWh, ou centavos de real. **O custo real é a hora do roteiro.**

### 6.6 O que dá para automatizar e o que exige revisão humana

| Automatiza | Exige humano |
|---|---|
| voz, conferência por ASR, render, emenda, efeitos e mix (o `fazer.py` já faz) | **escolher a pauta** e o ângulo |
| trava: não grava enquanto houver fato `a conferir` | **conferir cada fato na fonte** e trocar para `conferido` |
| poses, ciclos de andar e correr, sincronia da boca com o `beats.json` | **o humor** (piada boa não sai de molde) |
| teste de cenas: toda cena aponta para uma frase que existe; ângulos dentro do limite; 3+ props novos por episódio | revisão editorial (vítima, difamação, tom) com a lista da seção 8 |
| folha de quadros (`quadros.png`) para revisão rápida | assistir ao vídeo inteiro antes de publicar |
| rascunho de pesquisa e de roteiro com o Claude | título e miniatura |

---

## 7. A voz própria de cada canal (sem clonar ninguém)

**Situação hoje:** o `synth_qwen_clone.py` do Faz a Conta usa o modelo `Qwen3-TTS-12Hz-1.7B-Base` com a referência `ref_denis_OFICIAL.wav`, ou seja, **clona a voz do Denis** com consentimento dele, e sobe 2 semitons. Isso fica no Faz a Conta. **Nos canais novos não**, por duas razões: a regra (nenhuma voz de pessoa real) e o anonimato (a voz denunciaria o dono).

**Como fazer:**

1. **Modelo:** `Qwen3-TTS-12Hz-1.7B-VoiceDesign`, que cria a voz a partir de uma **descrição em texto**, fala português e tem licença Apache 2.0 ([README do Qwen3-TTS](https://raw.githubusercontent.com/QwenLM/Qwen3-TTS/main/README.md), aberto nesta sessão; licença: [Simon Willison, 22/01/2026](https://simonwillison.net/2026/Jan/22/qwen3-tts/) [só busca]).
2. **Descrição só de atributos acústicos.** Proibido citar nome de pessoa, personagem, dublador, locutor ou "voz parecida com…". Exemplo para o canal de história:
   `"Adult male voice, around 35, Brazilian Portuguese native, medium-high pitch, light and slightly nasal, fast and playful pace, ironic but warm, clear diction, informal storyteller, not a radio announcer."`
   Para golpes: `"Adult female voice, around 40, Brazilian Portuguese native, medium-low pitch, dry and calm, deadpan humor, precise diction, unhurried."`
   As vozes têm que ser **diferentes entre si e diferentes da do Faz a Conta** (grave e sarcástica, 45 anos), para os canais não se confundirem.
3. **Fixar a voz.** O VoiceDesign não é determinístico (o próprio cabeçalho do `synth_qwen_clone.py` diz isso). Então: gere ~20 candidatas com a mesma descrição e sementes fixas, escolha uma, gere com ela **3 a 5 min de fala neutra** e guarde como `voz-mestra.wav`. Daí em diante, o `Base` clona **essa voz sintética** (que não é de ninguém), e o timbre fica igual em todos os episódios. O resto do harness (3 takes, portão de ASR ≥ 0,90, dicionário de pronúncia) continua igual.
4. **Provar que não imita ninguém:**
   - registrar em `canais-dark/<canal>/VOZ.md` a descrição, a semente, o modelo, a data e o hash do `voz-mestra.wav` (proveniência);
   - medir a semelhança de locutor (embedding de voz, por exemplo ECAPA do SpeechBrain, local) entre a voz-mestra e (a) a referência do Denis e (b) as outras vozes dos canais; ficar abaixo de um limiar definido no primeiro teste (por exemplo, a semelhança entre duas pessoas diferentes conhecidas). Não baixe voz de famoso para comparar;
   - teste cego com 5 pessoas: "essa voz lembra alguém conhecido?". Se 2 ou mais disserem o mesmo nome, descarte e gere outra;
   - nunca usar a voz para "interpretar" pessoa real (sem imitação de sotaque de político, de celebridade etc.).
5. **Transparência:** a descrição de cada vídeo diz "Narração com voz sintética criada para este canal".
6. **Alternativa licenciada:** uma voz de catálogo de serviço comercial de TTS com licença de uso comercial no YouTube serve, mas tem custo mensal e a mesma voz aparece em milhares de canais (piora o "inautêntico"). **A voz desenhada local é melhor e grátis.**

---

## 8. Linha editorial (vale para os dois canais de palito)

1. **Entra:** fato com fonte (livro com autor e ano, reportagem de referência, processo ou documento oficial). Cada fato do roteiro está no quadro com o status `conferido`.
2. **Não entra:** teoria da conspiração, "dizem que", política partidária atual, político vivo como personagem, religião como alvo de piada, estereótipo étnico ou racial, e piada com vítima.
3. **Vítimas:** sem nome, salvo se forem figuras públicas históricas; mortes fora de cena; nunca a punchline.
4. **Golpes:** só condenação definitiva ou caso histórico; empresa em atividade só com decisão judicial citada na tela; o vídeo explica o mecanismo e como se proteger, e não ensina a aplicar.
5. **Fonte na tela:** a cartela `card(titulo, fonte)` em todo fato forte, e a lista de fontes na descrição.
6. **Revisão antes de publicar:** o Denis (ou um revisor) assiste ao vídeo inteiro com a lista acima; uma segunda leitura do roteiro por um sub-agente que não o escreveu (como na recomendação 3 do `motion/PESQUISA-EDICAO-CLAUDE.md`).
7. **Comentários:** ligar "reter comentários potencialmente impróprios para revisão" e uma lista de palavras bloqueadas ([TechCrunch sobre as ferramentas](https://techcrunch.com/2020/12/03/youtube-introduces-new-features-to-address-toxic-comments/) [só busca]); apagar ódio sem responder; corrigir erro factual com comentário fixado e errata na descrição.

---

## 9. O nome do Denis

**Recomendação: não associar.** Os canais saem sem o nome dele, sem a voz dele e sem divulgação cruzada com o Investir e Coçar ou o Faz a Conta. Motivos: (1) o humor de palito não combina com a imagem de educador financeiro; (2) no canal de golpes, qualquer menção a instituição financeira ligada a ele vira conflito de interesse. **Não é anonimato de fachada:** a conta é dele (ou do CNPJ dele), e se alguém perguntar, ele não nega. **Antes de lançar,** ele deve consultar o compliance do escritório e do banco sobre atividades externas e comunicação (as regras de assessor de investimento são da CVM e do código de conduta da instituição; não li esses textos nesta sessão).

---

## 10. Plano dos primeiros 30 dias e critério de 90 dias

**Semanas 1–2 (sem publicar):** esqueleto com cotovelo e joelho, 12 poses, 6 ações (andar, correr, apontar, esconder, falar, cair), 2 personagens com acessório, mapa e linha do tempo; teste de cenas; voz própria de cada canal, com `VOZ.md`. Busca manual de concorrentes no YouTube (seção 2).
**Semana 3:** 2 pilotos (1 de história, 1 de golpe), de 8 a 10 min. Revisão completa. Mostrar a 5 pessoas fora da bolha.
**Semana 4:** publicar os 2 pilotos e 2 Shorts de corte de cada um.
**Ritmo depois:** 1 longo a cada 2 semanas por canal (qualidade > volume; o OverSimplified prova que dá) + 2 Shorts por longo.

**Critério em 90 dias (por canal, a partir do 1º vídeo):**
- **Continuar** se: pelo menos 1 vídeo passa de 20 mil views em 30 dias **e** a retenção média é ≥ 40% (o Investir e Coçar tem 36,9% a 41,0% de média assistida no `auditoria-canal/RELATORIO.md`) **e** o custo humano caiu para ≤ 6 h por vídeo.
- **Parar ou mudar de nicho** se: nenhum vídeo passa de 5 mil views em 30 dias, ou se aparecer aviso de monetização por conteúdo inautêntico ou reutilizado.
- Os limiares de views são **escolha de gestão**, não benchmark de mercado (não há dado público confiável para canal novo em PT).

---

## 11. Domínios bloqueados nesta sessão (a liberar para refazer com dado direto)

socialblade.com · vidiq.com · hypeauditor.com · outlierkit.com · playboard.co · vidpros.com · tubeanalytics.net · fluxnote.io · support.google.com · trends.google.com · suggestqueries.google.com · google.com · duckduckgo.com · en.wikipedia.org · pt.wikipedia.org · commons.wikimedia.org · api.wikimedia.org · archive.org · huggingface.co · github.com (403; o raw.githubusercontent.com abriu) · qwen.ai · naturalearthdata.com (não testado).

**youtube.com** respondeu, mas a leitura automática das páginas de canal (para tirar inscritos e views dos vídeos) foi **negada pela trava de permissão** da sessão. Não contornei. Os números de canal acima vêm todos da busca. Para medir direito (views médias dos últimos 10 vídeos, duração, frequência), libere a leitura de canal do YouTube ou use a YouTube Data API com a chave do Denis.
