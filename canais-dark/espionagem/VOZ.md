# A voz do canal

**Voz criada por descrição, com o Qwen3-TTS VoiceDesign. Nenhum áudio de referência de pessoa nenhuma: não é clone.**

## Modelo

| Item | Valor | Situação |
|---|---|---|
| Modelo | `mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16` | nome lido no README do mlx-audio em 03/10/2026 (tabela "Available Models" do Qwen3-TTS). **CONFERIR NO MAC** que baixa: `python3 -c "from mlx_audio.tts.utils import load_model; load_model('mlx-community/Qwen3-TTS-12Hz-1.7B-VoiceDesign-bf16')"`. Se o nome mudar, passar em `VOZ_MODELO=...` sem mexer no código |
| Chamada | `model.generate_voice_design(text=..., language=..., instruct=...)` | mesma fonte (README do Qwen3-TTS dentro do mlx-audio); na linha de comando é `mlx_audio.tts.generate --instruct "..."` |
| Idioma | `Portuguese` | **CONFERIR NO MAC** a string aceita (variável `VOZ_IDIOMA`) |
| Semente | `7` (provisória) | escolher no Mac com `--candidatas` (abaixo) e anotar aqui |
| Licença do modelo | Apache 2.0 (Qwen3-TTS) | conforme o relatório de viabilidade; conferir no card do modelo |

## O texto exato da instrução

Está em `synth_voz.py` (constante `INSTRUCAO`). Se mudar lá, mudar aqui e regravar o episódio inteiro.

```
Adult male narrator, about 55 years old, native Brazilian Portuguese speaker with a neutral accent (no regional accent, not European Portuguese). Low, grave, warm voice with a slightly husky texture and medium-low pitch. Calm, serious documentary delivery at a slow, measured pace, with clear pauses between sentences. Precise diction, restrained emotion, steady volume. Not a movie-trailer voice, not a radio announcer, no dramatic emphasis, no whispering, no sarcasm, no smile in the voice.
```

Em português, para quem revisa: narrador homem, uns 55 anos, brasileiro, sotaque neutro (sem sotaque regional e sem sotaque de Portugal); voz grave, quente, levemente rouca, tom médio-baixo; leitura séria de documentário, lenta e pausada; dicção precisa, emoção contida, volume estável; **sem** voz de trailer, **sem** locutor de rádio, sem ênfase dramática, sem sussurro, sem ironia, sem sorriso na voz.

A descrição foi escrita em inglês porque o VoiceDesign foi treinado com instruções em inglês e chinês; o idioma da fala vem do parâmetro de idioma e do texto.

## Por que ela não lembra a voz pessoal do responsável nem a voz do outro canal

1. **Não há referência.** A voz do outro canal da casa é um clone da voz pessoal do responsável (modelo `Base` + gravação de referência + deslocamento de tom). Aqui o modelo é outro (`VoiceDesign`) e não recebe gravação nenhuma: a voz sai só do texto acima. Não existe caminho técnico para ela herdar o timbre de alguém.
2. **A descrição é o oposto da outra.** A do outro canal pedia homem de ~45 anos, seco, irônico, conversacional. Esta pede ~55 anos, grave e levemente rouca, lenta, séria, sem ironia, sem tom de conversa. Idade, ritmo, textura e intenção diferentes.
3. **Prova medida, não opinião** (fazer uma vez, no Mac, antes do 1º episódio):
   - `python3 synth_voz.py --candidatas` → 12 candidatas em `candidatas/` (sementes 1 a 12, mesmo parágrafo). Ouvir e escolher; anotar a semente aqui.
   - `VOZ_SEMENTE=<escolhida> python3 synth_voz.py --mestra` → `voz-mestra.wav` (fica fora do git).
   - `VOZ_COMPARAR="<voz pessoal>.wav,<voz do outro canal>.wav" python3 comparar_voz.py` → semelhança de locutor (resemblyzer, roda local). Tem que ficar **abaixo de 0,75** contra as duas (limiar provisório: calibrar no primeiro teste e anotar aqui). Os caminhos das vozes de comparação ficam só na linha de comando, nunca no repositório.
   - Teste cego com 3 a 5 pessoas que conhecem as outras vozes: "lembra alguém?". Se alguém reconhecer, trocar a semente.
4. **Citação não é imitação.** Falas de pessoas reais ("Un momentito, señor", "Eu sou Adolf Eichmann") são lidas como citação, no mesmo tom neutro, sem sotaque imitado.

## O script e o portão

- `synth_voz.py b0 b1 …` (rodado na pasta do episódio) grava `voz_bN.wav` + `voz_bN.beats.json`.
- Para cada frase: até 3 takes (`VOZ_TAKES`), cada um com semente `SEMENTE + 1000·k`; cada take é transcrito pelo Whisper (`mlx-community/whisper-large-v3-mlx`) e passa pelo **portão** (`portao.py`): nota de texto **e** nota de números ≥ 0,90. Datas por extenso no roteiro ("mil novecentos e sessenta") batem com os algarismos do Whisper ("1960"); data trocada reprova sozinha (`python3 portao.py --teste`, 12 casos do episódio).
- **Portão de timbre (opcional):** se existir `voz-mestra.wav` e o pacote `resemblyzer`, cada take também precisa ter semelhança ≥ 0,80 (`VOZ_TIMBRE_MIN`) com a voz-mestra. É assim que se segura o mesmo timbre do começo ao fim sem clonar: o VoiceDesign varia entre frases, e o take que fugiu do timbre é descartado.
- `conferir.py b0 …` audita de novo os blocos já gravados (não regera nada) e sai com erro se alguma frase reprovar.
- O texto que vai ao TTS passa pelo `pronuncia.txt` (nomes estrangeiros escritos como se falam); o portão compara com o texto original.
- Limite conhecido do portão: em frase muito curta, a troca de uma letra pode passar (ex.: "bodas" × "bolas" = 0,95). Frases curtas: ouvir.

## Transparência

A descrição de todo vídeo diz: **"Narração com voz sintética criada para este canal. As cenas marcadas como reconstituição são animações."** O roteiro do episódio 1 também fala isso no fim.
