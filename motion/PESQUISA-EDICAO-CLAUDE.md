# Edição de vídeo com Claude: o que funciona lá fora (pesquisa de out/2026)

Para o Investir e Coçar e o Faz a Conta. Data da pesquisa: 03/10/2026.

**Como ler.** Cada link tem uma marca:
- **[aberto]**: abri a página e os números (stars, versão) saíram dela.
- **[só busca]**: o domínio estava bloqueado ou não foi aberto, e a informação veio do resumo do buscador. Trate como indício, não como fato conferido.

Stars do GitHub são da data da pesquisa e medem atenção, não qualidade.

## O que o canal já tem (para não reinventar)

Lido em `investir-e-cocar/.claude/skills/edicao-investir-cocar`, `investir-e-cocar/memory` e `faz-a-conta/`:

- **Corte**: regra do pato com `mlx_whisper large-v3-turbo` e timestamps por palavra. O `silencedetect` delimita os cortes e a auditoria roda em loop até zerar. Faz o mesmo que as skills de "rough cut" de fora, só que com auditoria, e elas não têm.
- **B-roll em três peças** (dados, prints de fonte primária com push-in calculado, frases). Cada peça é ancorada numa **frase** do roteiro e a duração sai da fala (`plano.py`, `mapa.py`). A montagem usa `concat` e conta em frames inteiros.
- **Motion library em Remotion** (`NumberRoller`, `PushIn`, `PathDraw`, `TypewriterReveal`, `BRoll` com duotone, `Cue` por timestamp absoluto) e o **molde Burry em HyperFrames** (`gen.py` com tabela `SCENES`, `reveal`, `sceneOut`, `roller`, e `snapshot --at` antes do render).
- **Faz a Conta**: orquestrador `fazer.py` (roteiro → voz → conferência → render HyperFrames → SFX → mix). Tem trava de números conferidos, retomada por bloco e `cenas_hf.py` presa a trecho de frase.
- **Regra existente**: a cada ~28 s de câmera pura entra zoom lento, palavra na tela, gráfico ou corte. Hoje isso é manual. Memes e o corte fino são feitos no CapCut por cima do master.

Por isso, o que interessa de fora é o que **fecha buracos** dessa lista. Ferramenta que só refaz o que já existe fica de fora.

---

## 1. Os casos

### 1. Remotion Agent Skills (oficial)
- **Link**: https://github.com/remotion-dev/skills [aberto]. Documentação: https://www.remotion.dev/docs/ai/skills [só busca, domínio bloqueado].
- **O que faz**: são 11 skills mantidas pela própria Remotion (`/remotion-best-practices`, `-create`, `-markup`, `-render`, `-captions`, `-maps`, `-docs` e outras). Instala com `npx skills add remotion-dev/skills`.
- **Stack**: Remotion (React) e Claude Code. O MCP antigo da Remotion foi **descontinuado** em favor da skill `/remotion-docs` [só busca: https://www.remotion.dev/docs/ai/mcp].
- **Maturidade**: produto oficial, 4,8k stars.
- **O que copiar**: instalar no projeto Remotion da motion library. As regras de timing e de legenda evitam os erros que hoje estão em `feedback_remotion_gotchas.md`.
- **Esforço**: 10 min.
- **Licença**: grátis para pessoa física e empresa com até 3 funcionários [só busca: https://www.reactvideoeditor.com/blog/is-remotion-free].

### 2. HyperFrames (HeyGen): catálogo de blocos e skills
- **Link**: https://github.com/heygen-com/hyperframes [aberto]. Bloco de gráfico: https://hyperframes.heygen.com/catalog/blocks/data-chart [só busca, domínio bloqueado].
- **O que faz**: transforma HTML, CSS e GSAP em MP4 determinístico, com Puppeteer e FFmpeg. Tem uma skill-roteadora `/hyperframes` e a `/hyperframes-audio` (EQ, compressão, ducking e envelopes). O **catálogo** traz blocos de gráfico, legenda, transição, lower-third e kinetic type, que se instalam com `npx hyperframes add data-chart` ou `hyperframes add captions` [só busca].
- **Maturidade**: produto open source (Apache 2.0), 55,9k stars, lançado em 17/04/2026.
- **O que copiar**: o canal já usa HyperFrames na versão 0.6.40. O que falta é **olhar o catálogo** antes de escrever bloco à mão. O `data-chart` e o `captions` podem virar peças do molde Burry. A skill de áudio pode substituir parte do `mixar.py`, desde que se compare o resultado em LUFS antes.
- **Esforço**: baixo para testar; médio para adaptar ao visual papel/Inter.

### 3. Remotion: template de legenda estilo TikTok (palavra por palavra)
- **Link**: https://github.com/remotion-dev/template-tiktok [aberto]. Anúncio: https://x.com/JNYBGR/status/1760997350107976051 [só busca].
- **O que faz**: o Whisper.cpp transcreve e o `createTikTokStyleCaptions()` (do `@remotion/captions`) agrupa as palavras em "páginas". Cada página entra numa `Sequence` que destaca a palavra que está sendo dita.
- **Maturidade**: template oficial, 282 stars. O modelo padrão é o `medium.en`; para português, troque por um modelo sem `.en` em `whisper-config.mjs`.
- **O que copiar**: a função de paginação. O canal já tem o JSON por palavra do `mlx_whisper` e só precisa converter para o formato `Caption` (`startMs`/`endMs`). Não precisa do Whisper.cpp.
- **Esforço**: baixo.
- **Ressalva**: legenda queimada em vídeo longo de finanças é discutível (veja a seção 3), e o canal não faz mais Shorts. O uso mais provável é a **palavra-chave isolada na tela** dentro do punch-in (recomendação 1), não a legenda corrida.

### 4. video-use (Browser Use): edição pela transcrição, com autoavaliação
- **Link**: https://github.com/browser-use/video-use [aberto]. Fork com Whisper local em MLX: https://github.com/dentaco/video-use [só busca].
- **O que faz**: entrega ao agente a **transcrição** (que faz o papel do DOM) em vez de frames. A ideia vem do browser-use, que dá ao modelo a estrutura da página. Um arquivo `takes_packed.md` de ~12 KB tem as palavras com tempo. Nos pontos de decisão, o agente gera **filmstrips em PNG** (forma de onda com as palavras). O pipeline é transcrever → empacotar → raciocinar → EDL → render → autoavaliar nas bordas de corte. Animações saem de sub-agentes em paralelo (HyperFrames, Remotion, Manim ou PIL).
- **Stack**: ffmpeg e ElevenLabs Scribe (pago) na versão oficial.
- **Maturidade**: uso real, 27,9k stars segundo a busca [só busca; a página aberta não mostrou o número].
- **O que copiar**: **o filmstrip nas bordas de corte e de inserção** e o `project.md` como memória da edição. O canal confere hoje com amostragem de frames e contact sheet. Gerar o filmstrip automático em cada uma das ~55 inserções e fazer o Claude olhar só esses PNGs barateia a conferência visual.
- **Esforço**: baixo a médio. Não troque a transcrição: o `large-v3-turbo` local já é medido e é grátis.

### 5. claude-code-video-toolkit (Digital Samba)
- **Link**: https://github.com/digitalsamba/claude-code-video-toolkit [aberto].
- **O que faz**: workspace completo, com roteiro, voz (Qwen3-TTS), imagem (FLUX.2), música (ACE-Step), vídeo de IA (LTX-2) e render em Remotion. Os modelos rodam em GPU alugada (Modal/RunPod). O README estima ~US$ 0,01 de voz, ~US$ 0,02 por imagem e ~US$ 0,23 por clipe de vídeo. Tem templates de explainer 9:16, demo e sprint review.
- **Maturidade**: uso real, 2,2k stars, 252 commits.
- **O que copiar**: o **ciclo de vida por sessão** (fases planejamento → assets → áudio → edição → render, registradas em arquivo) e o sistema de **brand profiles**. O `fazer.py` do Faz a Conta já faz o equivalente, e melhor. A ideia aproveitável é o tema de marca em arquivo único, para os dois canais não divergirem.
- **Esforço**: baixo (só a ideia). Adotar o toolkit inteiro seria trocar um pipeline que já funciona.

### 6. motion-video-skill: motion no ritmo da batida (HyperFrames)
- **Link**: https://github.com/bestagentkits/motion-video-skill [aberto].
- **O que faz**: gera vídeo de motion em 1080p30 com cortes na batida. O `fit-beat-grid.py` calcula o BPM e uma tabela de energia por compasso. As legendas karaokê usam alinhamento forçado. As **checagens são mensuráveis**: música dentro de ±2 ms da batida, música 4–6 dB abaixo da voz, ~−14 LUFS e true peak ≤ −1 dBFS.
- **Stack**: HyperFrames, GSAP e a CLI `multix` (Gemini e ElevenLabs para voz, SFX e música).
- **Maturidade**: demo bem feita, 109 stars.
- **O que copiar**: **as checagens de áudio como teste automático** no `mixar.py` do Faz a Conta (loudness, true peak e música abaixo da voz). Cortar na batida faz pouco sentido no vídeo longo de finanças, que corta pela fala. Pode servir na vinheta ou num episódio montado só com música.
- **Esforço**: baixo para as checagens; médio para a grade de batida.

### 7. claude-shorts: cortes verticais com zoom automático
- **Link**: https://github.com/AgriciDaniel/claude-shorts [aberto].
- **O que faz**: pipeline de 10 etapas que tira shorts de um vídeo longo. O Claude pontua cada trecho em 5 dimensões (força do gancho, coerência, emoção, densidade de valor e payoff). O reenquadramento e o zoom se ajustam ao conteúdo, com MediaPipe para achar o rosto. Os cortes encaixam no fim de palavra ou no silêncio. Há 3 estilos de legenda (Bold, Bounce, Clean).
- **Stack**: ffmpeg, faster-whisper, MediaPipe, Remotion e Claude.
- **Maturidade**: uso real em pequena escala, 217 stars.
- **O que copiar**: a **rubrica de 5 dimensões** para escolher trecho, Para escolher **trechos de vídeo longo** (gancho, cold open), não para Shorts: Shorts foi descartado como aposta em 28/jul/2026 (`project_yt_shorts_sunset_28jul`: RPM de R$ 0,12 contra R$ 38,50 do long-form). O crop por rosto fica de fora.
- **Esforço**: médio.

### 8. Zoom dinâmico por ênfase da fala (padrão recorrente)
- **Links**:
  - https://github.com/0xpratzyy/cutroom [aberto]: punch-in e push-in suavizado, além de legenda com palavras de ênfase escolhidas pelo Claude via MCP. 0 stars, 10 commits, testado só com vídeo sintético. É **demo**.
  - https://chrislema.com/claude-code-skills-for-video-editing [só busca, domínio bloqueado]: pipeline em skills que classifica cada trecho em "normal", "ênfase" e "crítico". Ênfase leva zoom de 1,25× e crítico, de 1,6×.
- **O que faz**: o agente lê a transcrição, marca as palavras de ênfase e gera keyframes de zoom/crop no ffmpeg.
- **O que copiar**: **isso automatiza a regra dos 28 s de câmera pura**, que hoje é manual. O canal já tem a transcrição por palavra e a contabilidade em frames inteiros. Falta só um `zoom.py` que leia os trechos sem cartela no `cartelas.json` e escolha 1 ou 2 palavras de ênfase em cada um.
- **Esforço**: baixo a médio.

### 9. DaVinci Resolve MCP (samuelgursky)
- **Link**: https://github.com/samuelgursky/davinci-resolve-mcp [aberto].
- **O que faz**: dá ao agente acesso à API oficial de scripting: timeline, marcadores de revisão, Fusion, Fairlight e fila de render. O próprio README diz que a saída é uma **"first-pass assembly"** que precisa de revisão humana e que a ferramenta não julga qualidade de edição.
- **Stack**: Python. Funciona com Resolve **Studio** (pago) ou com o **gratuito** por uma ponte que roda dentro do menu Scripts.
- **Maturidade**: uso real, 3,3k stars, versão 4.8.26, 361/361 métodos da API cobertos.
- **O que copiar**: só faz sentido se o Denis migrar o acabamento do CapCut para o Resolve. Um uso concreto é o agente jogar **marcadores** na timeline em cada inserção do `plano.json`, para a revisão humana pular de um ponto a outro.
- **Esforço**: médio (instalar e aprender o Resolve).

### 10. After Effects por MCP/ExtendScript
- **Links**:
  - https://github.com/a-y-ibrahim/after-effects-mcp [aberto]: 57 ferramentas por ExtendScript e painel CEP. Renderiza em background com `aerender`. A ferramenta `see-frame` devolve o frame como imagem para o agente se corrigir. Acessa propriedades por `matchName`, o que evita problema com AE em outro idioma. 21 stars.
  - https://github.com/Jrocchetti/after-effects-mcp [aberto]: mais de 70 ferramentas, com templates de lower third, title card e transição. 0 stars.
  - Há pelo menos mais 6 servidores parecidos (kumoproductions, Immersive-Media-Technologies, LiamcKerr e outros) [só busca].
- **Maturidade**: demo a uso real inicial. **Fragmentado**: muitos forks com o mesmo texto de README.
- **O que copiar**: nada agora. O canal não usa AE, e HTML/React faz o mesmo motion sem licença Adobe e com versionamento em git. Só vale se aparecer um template .aep comprado que precise de preenchimento em lote.
- **Esforço**: alto (licença, Windows/macOS, painel CEP).

### 11. CapCut por draft JSON (VectCutAPI e capcut-mcp)
- **Links**:
  - https://github.com/sun-guannan/VectCutAPI [aberto]: API e skills que geram drafts do CapCut internacional e do JianYing (legenda, PiP, voz, filtros). 2,3k stars. O agente de edição MCP e o render na nuvem **não** são open source.
  - https://github.com/JmsLdrn/capcut-mcp [aberto]: lê e edita drafts do CapCut desktop. Detecta o caminho no macOS. 8 stars. O README avisa que o formato é proprietário e muda entre versões, que efeitos e animações são "best-effort" e que o CapCut precisa estar fechado durante a edição.
  - Criptografia: https://gist.github.com/renezander030/521e6c6e8590a2a6e917009d9313bc55 [só busca]. Segundo o resumo, o JianYing 6.0+ criptografa o `draft_content.json` e o CapCut internacional não.
- **O que copiar**: é **o mais próximo do fluxo real do Denis**, que termina no CapCut. Uma ideia: o agente gera um **draft com marcadores e textos já posicionados** (memes e cortes finos sugeridos), e o Denis só ajusta. Antes, teste com uma cópia de projeto na versão instalada no Mac.
- **Esforço**: médio, com **risco de quebra a cada atualização do CapCut**.

### 12. short-video-maker: o faceless "clássico" por MCP
- **Link**: https://github.com/gyoridavid/short-video-maker [aberto].
- **O que faz**: recebe texto e devolve um short vertical, com TTS Kokoro, legenda pelo Whisper, fundo do Pexels e música por humor, tudo renderizado em Remotion. Funciona por MCP ou REST.
- **Maturidade**: uso real, 1,4k stars. **Só fala inglês** (o kokoro-js não tem outra língua) e só usa vídeo do Pexels.
- **O que copiar**: nada de estética. É a referência do que **não** fazer: vídeo de banco de imagem com legenda é exatamente o "template com pouca variação" da política de conteúdo inautêntico do YouTube (seção 3). Serve só como exemplo de interface MCP/REST, se um dia o orquestrador virar serviço.
- **Esforço**: n/a.

### 13. B-roll ancorado no SRT com diretor e revisor separados
- **Link**: https://github.com/erduo1998-cell/erduo-broll-loop-engineering [aberto].
- **O que faz**: lê o SRT e gera B-roll em HyperFrames, com Remotion como alternativa. O trabalho se divide entre um **Diretor** independente (direção visual), um **Criador** com contexto limpo, o render e um **Revisor** independente de estética, que devolve correções locais. Usa 152 "shot cards" como dicionário. Divide os planos pelo sentido da fala, não um por legenda.
- **Maturidade**: v1.1.0, 203 stars. Documentação principal em chinês. O Claude Code é marcado como "experimental"; o host principal é o Codex.
- **O que copiar**: **o revisor com contexto limpo**. Quem escreveu a cena não aprova a cena, a mesma regra que o canal já aplica ao título ("nunca deixar quem escreveu o roteiro escolher o próprio título"). Aplique o revisor ao `snapshot --at` do HyperFrames.
- **Esforço**: baixo (é um sub-agente a mais).

### 14. Kinocut: ffmpeg com guardrails por MCP
- **Link**: https://github.com/KyaniteLabs/kinocut [aberto].
- **O que faz**: um MCP e uma CLI que embrulham o ffmpeg em ferramentas tipadas, com validação prévia. Gera "Video Receipts" (registro com hashes de cada edição), tem integração com HyperFrames e um motor de workflow que retoma de onde parou.
- **Maturidade**: uso real, 181 stars, versão 1.16.0 (203 ferramentas MCP).
- **O que copiar**: a ideia do **recibo com hash por etapa**. É o que a seção 6 da skill faz à mão, com o SHA do áudio e a comparação de streams. Dá para gravar o recibo automaticamente em cada render.
- **Esforço**: baixo (a ideia); não precisa da ferramenta.

### 15. Prompt-to-motion-graphics (template oficial Remotion) e conector oficial da Adobe
- **Links**:
  - https://github.com/remotion-dev/template-prompt-to-motion-graphics [aberto]: kit em Next.js para montar um **SaaS** de motion: chat, código Remotion gerado e preview ao vivo, com classificador que rejeita prompt que não é de motion. 259 stars.
  - Conector "Adobe for creativity" no Claude (abr/2026) [só busca: https://www.usecarly.com/blog/adobe-mcp/]: mais de 50 ferramentas, mas no **nível do Express e do Firefly**, não do Premiere ou do AE desktop completos.
- **O que copiar**: nada para o canal. O primeiro é para quem vende ferramenta; o segundo não edita timeline de verdade.
- **Esforço**: n/a.

### Casos extras, só para registro
- **Rough cut de talking head**: https://github.com/vincentventalon/claude-code-video-editing-skill [aberto]. Usa ffmpeg e whisper.cpp, com "ilhas de som" e "fica a última tomada". 3 stars, sem legenda nem B-roll. **O pipeline do pato já é mais completo** (tem auditoria em loop).
- **Edição com marca e motion**: https://github.com/adukhan98/video-edit [aberto]. Gera motion em HyperFrames, exportado em ProRes 4444 com alfa, e baixa B-roll com yt-dlp filtrando Creative Commons. 0 stars, 2 commits: **demo**. A ideia de **motion com canal alfa** sobreposto ao talking head é boa.
- **Faceless de finanças automático**: https://github.com/Rohan5commit/finance-video-agent [aberto]. Notícias (Currents), cotações (Twelve Data), LLM, Kokoro, Remotion e upload, num cron pelo GitHub Actions. 0 stars, sem canal ou views comprovados, e o README não mostra gráfico animado de verdade. **É hype de arquitetura.**
- **Manim por agente**: https://github.com/vumichien/manim-skill e https://github.com/AmitSubhash/3brown1blue [só busca]. Explainer estilo 3Blue1Brown. Pode servir para a "conta" do Faz a Conta (juros compostos desenhados), mas o HyperFrames já resolve.
- **Premiere por MCP**: https://github.com/leancoderkavy/premiere-pro-mcp e outros (bot202102, averav2, hoodtronik, todos com o mesmo README) [só busca]. São ponte CEP, independentes e não oficiais da Adobe.
- **Lista curada**: https://github.com/zhuyansen/awesome-claude-video-skills [aberto]. Tem 180 repos com nota de segurança. Foi daqui que saíram vários dos casos acima.

---

## 2. Tabela: caso × o que copiar × esforço × impacto provável na retenção

O impacto é uma **estimativa qualitativa** minha. Nenhum desses repos publica dado de retenção.

| # | Caso | O que copiar | Esforço | Impacto na retenção |
|---|---|---|---|---|
| 8 | Zoom por ênfase (cutroom, Chris Lema) | `zoom.py`: punch-in de 1,1–1,25× nas palavras de ênfase, só nos trechos de câmera pura sem cartela | Baixo–médio | **Alto**: ataca a câmera pura (no TRXF11, ~59% do vídeo, já que a cobertura de imagem foi de 41%) |
| 2 | HyperFrames catálogo | Bloco `data-chart` para série de juros, IPCA e cotação; `captions` | Baixo–médio | **Alto**: gráfico em movimento segura mais que número parado |
| 4 | video-use | Filmstrip automático em cada borda de corte e de inserção, mais revisão visual | Baixo–médio | Médio (indireto: menos erro que escapa) |
| 13 | erduo B-roll | Revisor de estética com contexto limpo antes do render cheio | Baixo | Médio (indireto) |
| 1 | Remotion Skills | Instalar no projeto da motion library | Muito baixo | Baixo (indireto: menos bug) |
| 3 | template-tiktok | Paginação palavra por palavra a partir do JSON do mlx_whisper, usada só para a palavra-chave na tela | Baixo | Baixo/incerto no longo (Shorts descartado) |
| 6 | motion-video-skill | Checagens de loudness, true peak e música −4 a −6 dB no mix | Baixo | Médio (áudio ruim derruba retenção) |
| 11 | CapCut draft | Draft pré-montado com memes e marcadores para o acabamento | Médio (frágil) | Médio: acelera a etapa manual, não muda o vídeo |
| 7 | claude-shorts | Rubrica de 5 dimensões para escolher o gancho do vídeo longo | Baixo | Médio (gancho) |
| 14 | Kinocut | Recibo com hash por etapa | Baixo | Nenhum direto (confiabilidade) |
| 5 | Digital Samba toolkit | Tema de marca num arquivo único para os dois canais | Baixo | Baixo |
| 9 | DaVinci MCP | Marcadores de revisão a partir do `plano.json` | Médio | Baixo |
| 10 | After Effects MCP | Nada agora | Alto | Baixo |
| 12 | short-video-maker | Nada (contraexemplo) | n/a | Negativo, se imitado |
| 15 | Prompt-to-motion / Adobe | Nada | n/a | n/a |

---

## 3. Hype × realidade

**"Um prompt e sai um vídeo viral."** Os posts de X que circulam são de motion abstrato ou de demo de produto, curtos e sem fala para sincronizar. Exemplos: o lançamento das skills da Remotion (https://x.com/Remotion/status/2013626968386765291), o "fiz em 10 minutos" de https://x.com/zolihonig/status/2033911539913167145 e o "o único prompt que você precisa" de https://x.com/RoundtableSpace/status/2105209785335373948 [todos só busca, x.com não aberto]. O próprio post de https://x.com/timkochjar/status/2092278549679886507 diz "não quer dizer que seja fácil" [só busca]. **Na prática**: um vídeo longo de finanças com 50+ inserções sincronizadas com a fala é engenharia de timing (âncora em frase, frames inteiros, auditoria). Foi isso que o canal levou meses para acertar, e nenhum desses posts mostra isso.

**"Edição autônoma do bruto ao final."** Os projetos mais sérios dizem o contrário no próprio README. O DaVinci MCP chama a saída de "first-pass assembly" que exige revisão humana. O video-use só funciona porque **autoavalia** as bordas de corte. A edição autônoma sem conferência é exatamente o que gerou a deriva de +0,84 s e as 52 de 53 cartelas saindo cedo no TRXF11.

**MCP de After Effects, Premiere e CapCut.** Há dezenas de repos, muitos com **o mesmo README e 0 a 20 stars** (forks renomeados). Eles dependem de painel CEP, licença Adobe e, no CapCut, de um formato **proprietário que muda a cada versão**: o capcut-mcp avisa e o gist sobre criptografia do JianYing confirma [só busca]. **A manutenção é o custo escondido.** HTML/React em git não quebra quando a Adobe ou a ByteDance atualiza o app.

**Faceless automático com cron.** Repos como o finance-video-agent e o short-video-maker montam a fábrica (notícia → LLM → TTS → stock → upload), mas **nenhum mostra canal com audiência**. O YouTube renomeou em 15/07/2025 a política de "conteúdo repetitivo" para "conteúdo inautêntico", que tira da monetização vídeo produzido em massa a partir de template com pouca variação [só busca: https://gulfnews.com/technology/youtube-updates-monetisation-policies-ai-and-repetitive-content-ban-begins-july-15-1.500192660]. Faceless não é proibido; **template sem curadoria é**. O Faz a Conta passa porque tem roteiro próprio e números conferidos. Não pode virar cron.

**Custo "de centavos".** O Digital Samba estima ~US$ 0,23 por clipe de vídeo de IA e ~US$ 0,80 por um explainer de 52 s. Parece barato, mas: (a) a GPU alugada e os tokens do Claude para iterar não entram nessa conta; (b) clipe de vídeo gerado por IA em canal de finanças com rosto real piora a credibilidade, e a memória `feedback_broll_limites_e_armadilhas_geradores.md` já registra os limites. O custo real é **tempo de iteração e revisão**, não o render.

**Render.** O HyperFrames e o Remotion renderizam com Chrome headless, frame a frame. Funciona e é determinístico, mas é **pesado numa máquina de 16 GB**, e o canal já mediu isso (trava de memória no `fazer.py`, "uma coisa pesada por vez"). Os posts de "render em segundos" são de clipes de 10–15 s. O `snapshot --at` antes do render cheio é a prática certa, e o canal já usa.

**Transcrição paga.** O video-use oficial depende do ElevenLabs Scribe. O `mlx_whisper large-v3-turbo` local foi medido no canal (1,9 GB de pico, 5,5 min para 49 min de áudio, 0,12 s de deriva) e é grátis. Não vale trocar.

**Legenda palavra por palavra em tudo.** Funciona em short vertical, onde o som costuma estar desligado, mas o canal descartou Shorts. Em vídeo longo de finanças, com B-roll de dados e prints na tela, legenda queimada **disputa a atenção com o número** e polui os prints de fonte primária. Nenhum dos casos traz dado de retenção em vídeo longo. Se usar, teste A/B num vídeo antes.

---

## 4. Três recomendações para o canal

**1. Punch-in automático por ênfase nos trechos de câmera pura.** Ganho maior e esforço menor.
Um `scripts/zoom.py` lê o `cartelas.json` (onde já tem imagem) e o JSON por palavra do `mlx_whisper`. Em cada trecho de câmera pura com mais de ~8 s, o Claude escolhe 1 ou 2 palavras de ênfase: o número, o "mas", o punch. O script aplica um push-in de 1,1–1,25×, que entra suavizado e sai no fim da frase, com `crop`+`scale` no ffmpeg, na **contabilidade em frames inteiros que a skill já exige**. Isso automatiza a regra dos 28 s, que hoje depende do CapCut. Inspiração: casos 7 e 8. Não precisa de ferramenta nova.

**2. Uma quarta peça de B-roll: gráfico de série que se desenha.**
Hoje as peças de dados mostram **1 número por cena**. Falta a **série**: Selic, IPCA, cotação, dividendo por ano. Dado de fonte primária (API SGS do Banco Central, ou balanço/RI para empresa) → CSV conferido → componente com linha que se desenha (o `IFIXMiniChart`/`PathDraw` da motion library já é a base), ou o bloco `data-chart` do catálogo HyperFrames adaptado ao visual papel. Mesma regra do Faz a Conta: **o número só entra se estiver conferido**. Inspiração: caso 2. Esforço médio, e o componente se reaproveita em todos os vídeos.

**3. Revisor visual com contexto limpo, usando filmstrip, antes do render cheio.**
Depois do `plano.py`/`mapa.py`, gere automaticamente um **filmstrip** em cada borda de inserção: frame de entrada, frame de saída, forma de onda e as palavras ditas ali. Um **sub-agente que não escreveu o plano** confere três coisas: a cartela sai junto com a fala? o print está legível? o número na tela é o número falado? Isso pega cedo, de forma barata, a classe de erro que custou mais caro no TRXF11 (cartela saindo antes da fala). Inspiração: casos 4 e 13. Esforço baixo.

**O que não fazer agora**: MCP de After Effects ou Premiere, faceless em cron, vídeo gerado por IA como B-roll e trocar o Whisper local por API paga.

---

## Domínios a liberar

Bloqueados pelo proxy durante a pesquisa (não contornei; a informação desses links veio do resumo da busca):

- `www.remotion.dev`: documentação oficial (Agent Skills, MCP descontinuado, templates, licença)
- `hyperframes.heygen.com`: catálogo de blocos do HyperFrames (data-chart, captions)
- `www.reddit.com`: relatos de uso (não consegui nenhuma thread com dado de retenção)
- `chrislema.com`: post sobre zoom por ênfase em 3 níveis
- `cutback.video`: post "what works, what breaks"
- `charliehills.substack.com`: post sobre motion com Claude Code

Não abertos (só resultado de busca, não testei o fetch): `x.com` e `usecarly.com`.
