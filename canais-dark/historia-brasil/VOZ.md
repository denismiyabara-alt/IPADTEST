# A voz do canal: desenhada por descrição, sem clonar ninguém

## A escolha

**Uma narradora de uns 38 anos, com jeito de professora de história de cursinho que gosta da turma.** A voz é média e quente, um pouco rouca, com dicção limpa e sotaque brasileiro neutro. O ritmo é ágil, de quem conta um causo verdadeiro. A ironia é seca, com uma pausa curta antes da piada e um sorriso na voz. Não é locutora de rádio nem âncora de telejornal.

### Texto exato da instrução do VoiceDesign (`voz/descricao.txt`, campo `instruct`)

```
Adult female voice, around 38 years old, native Brazilian Portuguese speaker with a neutral accent and no strong regional features.
Medium pitch, warm and slightly husky timbre, clear and crisp diction.
Brisk, lively storytelling rhythm, like a witty prep-school history teacher telling a true story to a class she likes:
ironic, dry sense of humor, small knowing pauses before the punchline, a hint of a smile in the voice.
Conversational and close to the microphone; never theatrical, not a radio announcer, not a news anchor, not a cartoon voice.
```

A instrução está em inglês porque os exemplos do modelo são em inglês e chinês. A fala sai em português porque o synth passa `language="portuguese"`. A instrução só descreve atributos acústicos e de estilo. Não cita pessoa, personagem, dublador ou "voz parecida com", e o teste `test_comando_do_mlx_audio` confere isso.

## Por que não lembra a voz do dono nem a do canal irmão

**O que o repositório faz-a-conta diz da voz de lá:**
- O `synth_qwen_clone.py` usa o modelo `Qwen/Qwen3-TTS-12Hz-1.7B-Base` e **clona a voz do dono do canal**, com o consentimento dele.
- A referência é uma narração corrida dele, de cerca de 23 minutos.
- Depois da clonagem, o script sobe o tom em **+2 semitons** com o `rubberband`, sem preservar os formantes.
- A descrição guardada no mesmo arquivo é: *"deep, low-pitched adult male voice… around 45 years old… chesty and resonant. Dry, deadpan, sarcastic delivery. Conversational, not a radio announcer."*
- O `RELATORIO-PALITO.md` resume essa voz como "grave e sarcástica, 45 anos".

**Esta voz difere em tudo o que dá para medir de ouvido:**

| | Canal irmão | Este canal |
|---|---|---|
| Origem | clone de pessoa real (o dono) | **descrição em texto**, sem áudio de ninguém |
| Sexo aparente | masculino | **feminino** |
| Idade aparente | ~45 | ~38 |
| Altura | grave (mesmo com +2 semitons) | média |
| Timbre | de peito, ressonante | quente, levemente rouco |
| Ritmo | seco e lento (deadpan) | ágil, de contadora de história |
| Humor | sarcasmo seco | ironia de professora, sorriso na voz |

A voz feminina é a separação mais forte possível da voz do dono, e é isso que protege o anonimato do canal. O `RELATORIO-PALITO.md` sugeria uma voz feminina para o futuro canal de golpes. Se esse canal sair, ele deve usar **outro perfil** (por exemplo, masculino de uns 60 anos, grave e pausado), para que os três canais nunca se confundam.

## Como a voz é fixada (`voz/desenhar_voz.py`)

O VoiceDesign não é determinístico: a mesma descrição gera vozes um pouco diferentes a cada chamada. Por isso:

1. **Candidatas.** O script gera 20 amostras da mesma frase de teste, com as sementes 0 a 19. Cada amostra passa pelo mesmo portão do synth (Whisper + nota de texto e números), e o resultado vai para o `voz/candidatas/ouvido.tsv`.
2. **Escolha de ouvido.** Considere só as amostras com nota ≥ 0,90. Prefira a que (a) soa como a descrição, (b) não tem chiado nem estalo e (c) **não lembra ninguém conhecido**.
3. **Voz-mestra.** Rode `mestra --semente N`, que gera cerca de 25 s de fala neutra com a mesma semente e grava `voz/voz-mestra.wav` e o `voz-mestra.txt` com o texto. Se o timbre mudar em relação à candidata (a semente pode não reproduzir igual no Mac: **CONFERIR NO MAC**), use `mestra --de-candidata N`, que copia a própria amostra.
4. **Episódios.** O `synth_voz.py`, no modo padrão `HB_MODO=mestra`, faz o modelo `Base` clonar a **voz-mestra**, que é sintética e não pertence a ninguém. Assim o timbre fica igual em todos os vídeos. O modo `HB_MODO=design` fala direto da descrição e serve só para testar a descrição, porque o timbre muda de frase para frase.

### Prova de que a voz não imita ninguém

- **Semelhança de locutor:** `python3 voz/comparar_voz.py voz/voz-mestra.wav <referência do canal irmão> <trecho publicado do canal irmão>` (ECAPA do SpeechBrain, roda local). O critério é ficar **abaixo de 0,50 contra cada referência**. O limiar é uma margem: calibre no primeiro uso comparando dois trechos da mesma pessoa, que devem dar mais de 0,70. Não baixe voz de famoso para comparar.
- **Teste cego** com 5 pessoas: "essa voz lembra alguém conhecido?". Se 2 ou mais disserem o mesmo nome, descarte a voz e gere outra.
- Nunca use a voz para "interpretar" pessoa real.
- A descrição de todo vídeo diz "Narração com voz sintética criada para este canal" (já está no `descricao.txt`).

### Registro de proveniência (preencher no Mac)

| campo | valor |
|---|---|
| modelo da voz | `mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16` (Apache-2.0, conforme o card do Hugging Face aberto em 03/10/2026) |
| modelo de clonagem | `Qwen/Qwen3-TTS-12Hz-1.7B-Base` (o mesmo que já roda no Mac) |
| mlx-audio | versão ≥ 0.5.7 (a versão em que conferi a API `generate_voice_design` e o `--instruct` do CLI) |
| descrição | `voz/descricao.txt` (o texto acima) |
| semente escolhida | _preencher_ |
| data | _preencher_ |
| sha256 do `voz-mestra.wav` | _preencher (o script imprime)_ |
| ECAPA contra o canal irmão | _preencher_ |
| teste cego (5 pessoas) | _preencher_ |

## O que foi conferido daqui e o que fica para o Mac

- **Conferido no pacote `mlx-audio` 0.5.7 (PyPI) e no Hugging Face:**
  - o modelo `mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16` existe;
  - o `config.json` dele traz `tts_model_type: voice_design` e os idiomas incluem `portuguese`;
  - a API Python é `model.generate_voice_design(text, instruct, language)`;
  - o CLI `python -m mlx_audio.tts.generate` aceita `--instruct`, `--ref_audio`, `--ref_text` e `--lang_code`.
- **Detalhe novo:** `lang_code` precisa ser `portuguese`. O `pt` que o canal irmão usa não está na tabela de idiomas do modelo e cai no modo automático.
- **CONFERIR NO MAC:**
  - (1) a versão do `mlx-audio` no ambiente `~/.venvs/voice-clone`; se for anterior à 0.5.7, rode `pip install -U mlx-audio`;
  - (2) se a semente reproduz o mesmo timbre;
  - (3) os nomes dos modelos continuam valendo. Eles são parâmetros (`HB_MODELO_DESIGN`, `HB_MODELO_BASE`, `HB_LANG`); se mudarem, troque pela variável, sem mexer no código.

## Portão de conferência (Whisper), mantido

O portão é o mesmo do canal irmão: `mlx-community/whisper-large-v3-mlx` ouve cada take, compara o **texto** e os **números** com o roteiro e só aceita nota ≥ 0,90. O script faz 3 takes por frase e fica com o melhor. Depois, o `conferir.py` audita o bloco inteiro, e o `fazer.py` trava se alguma linha começar com "!!". O `synth_voz.py --teste` roda o autoteste do portão: são 20 casos herdados e 8 casos com os números deste roteiro, incluindo dois que **têm de reprovar** (1906 ouvido como 1916; 30 ouvido como 13). O teste `test_portao_de_numeros_aceita_cada_frase_como_o_whisper_escreve` passa as 59 frases pelo portão na forma em que o Whisper escreve números.
