# Como rodar o piloto no Mac (domingo à tarde)

Episódio: **A GUERRA CONTRA A VACINA** (`revolta-da-vacina/`), com 8 blocos, 59 frases e 779 palavras. A duração estimada é de **5 min 50 s** com a tela final, pela régua de 0,067 s por caractere do canal irmão; a voz real pode mudar isso em ±15%.

Tudo roda local: a voz no `mlx_audio`, a conferência no Whisper e o render no HyperFrames. A trava de "um job pesado por vez" é a **mesma** do canal irmão, então não dá para rodar os dois canais ao mesmo tempo, e isso é de propósito.

## Resumo (copie e cole)

```sh
cd ~/IPADTEST && git pull                       # (ou onde o repositório estiver)
cd canais-dark/historia-brasil
npm install                                     # 1x: GSAP, fontes OFL e o HyperFrames 0.8.78 (~1 min)
python3 -m pytest -q tests                      # esperado: 20 passed (~5 s)
# passo 2: conferir os 3 fatos e trocar o status no roteiro.md (~10 min, à mão)
~/.venvs/voice-clone/bin/python voz/desenhar_voz.py candidatas --n 20     # passo 3 (~20 a 30 min)
~/.venvs/voice-clone/bin/python voz/desenhar_voz.py mestra --semente N    # (~1 min)
python3 fazer.py revolta-da-vacina              # passo 5: voz → conferência → render → efeitos → mix (~1 h 10)
open revolta-da-vacina/REVOLTA-DA-VACINA-final.mp4
```

## Passo a passo

### 1. Instalar (uma vez, ~5 min)

- Node 22 ou mais novo (`node --version`) e depois `npm install` nesta pasta. O render usa o `node_modules/.bin/hyperframes` local, e não o `npx` com download.
- Rode `node_modules/.bin/hyperframes doctor`. Se ele reclamar do navegador, rode `node_modules/.bin/hyperframes browser ensure`. No Mac com o Chrome instalado, ele já acha sozinho.
- Python do sistema: `python3 -m pip install numpy soundfile scipy pytest`. Também precisa de `ffmpeg` e `ffprobe`, que já estão no Mac do canal irmão.
- Ambiente da voz, o mesmo do canal irmão (`~/.venvs/voice-clone`):
  `~/.venvs/voice-clone/bin/pip install -U "mlx-audio>=0.5.7" mlx-whisper`
  A 0.5.7 é a versão em que conferi `generate_voice_design` e `--instruct`. **CONFERIR NO MAC** se o upgrade não quebra o canal irmão. Na dúvida, crie um ambiente novo e aponte `HB_PY_GEN=~/.venvs/<novo>/bin/python`.
- Testes: `python3 -m pytest -q tests` deve dar **20 passed**. Eles validam o roteiro e o portão de números, a trava, as cenas, os números na tela, a montagem do HTML com JS válido, os efeitos e a ausência de nomes proibidos.

### 2. Conferir os 3 fatos que o proxy bloqueou (~10 min, à mão)

O `fazer.py` **não grava voz** enquanto houver linha "CONFERIR NO MAC" no quadro do `revolta-da-vacina/roteiro.md`. Abra cada URL no navegador:

| id | o que conferir | URL |
|---|---|---|
| `lei-1261` | Lei nº 1.261, de 31/10/1904, torna obrigatórias a vacinação e a revacinação contra a varíola em toda a República | https://www2.camara.leg.br/legin/fed/lei/1900-1909/lei-1261-31-outubro-1904-584180-publicacaooriginal-106938-pl.html |
| `ratos-compra` | a Diretoria-Geral de Saúde Pública comprava rato morto, e houve gente que criava rato para vender | https://oswaldocruz.fiocruz.br/index.php/biografia/trajetoria-cientifica/na-diretoria-geral-de-saude-publica/campanha-contra-a-peste |
| `atestado` | o regulamento exigia atestado de vacina para matrícula, emprego, viagem e casamento | http://www.ccms.saude.gov.br/revolta/revolta.html (se não abrir, vale outra página oficial da Fiocruz ou do MS sobre a Revolta da Vacina) |

Tentativa de 07/10/2026 (proxy mais aberto): o **Planalto abriu, mas não publica a Lei nº 1.261/1904** (não está no quadro de leis anteriores a 1960 nem nos Decretos do Poder Legislativo; o endereço direto dá 404). Câmara, Senado, LexML, Fiocruz (oswaldocruz, portal, agência, arca) e o CCMS continuam barrados. Os 3 continuam para o Mac. A legenda de O Malho ganhou uma segunda transcrição que bate (Commons), então o zoom na p. 13 virou opcional.

- **Bateu?** Troque `CONFERIR NO MAC` por `conferido` e escreva na coluna de fonte o que viu e a data.
- **Não bateu?** Use a **reserva** que está nas Notas do roteiro (as falas de troca já estão escritas) e apague a linha do quadro.
- Aproveite e **dê zoom na p. 13** do PDF "PNI 50 anos" (https://www.gov.br/saude/pt-br/centrais-de-conteudo/publicacoes/svsa/vacinacao-imunizacao-pni/programa-nacional-de-imunizacoes-50-anos.pdf). Confira se a legenda da charge de O Malho diz mesmo "o Napoleão da seringa e lanceta". No PDF, a imagem está em baixa resolução.
- Rode `python3 fazer.py revolta-da-vacina --status`. Deve aparecer `números conferidos: 26/26` (ou menos linhas, se usou alguma reserva).

### 3. Criar a voz do canal (uma vez, ~25 a 35 min)

```sh
~/.venvs/voice-clone/bin/python voz/desenhar_voz.py candidatas --n 20
```
- O script gera `voz/candidatas/cand_00.wav` … `cand_19.wav` e o `ouvido.tsv` (o que o Whisper entendeu e a nota). São cerca de 20 a 30 min no Mac de 16 GB: 20 amostras de ~8 s mais o Whisper. É uma estimativa, porque o VoiceDesign nunca foi medido nesse Mac.
- Ouça as de nota ≥ 0,90 e escolha **uma**, pelos critérios do `VOZ.md`: soa como a descrição, não tem defeito e **não lembra ninguém**.
- `~/.venvs/voice-clone/bin/python voz/desenhar_voz.py mestra --semente N` grava `voz/voz-mestra.wav`, com ~25 s de fala neutra. Se o timbre não for o da candidata, use `--de-candidata N`.
- Prova de que não imita ninguém (opcional, mas recomendado antes de publicar):
  `python3 voz/comparar_voz.py voz/voz-mestra.wav <referência do canal irmão> <um trecho publicado do canal irmão>`. Precisa do `pip install speechbrain torchaudio`, uma vez. Depois faça o teste cego com 5 pessoas.
- Preencha o **registro de proveniência** no `VOZ.md`: semente, data, sha256 e resultado do ECAPA.

### 4. Ouvir a pronúncia (~5 min)

O `pronuncia.txt` já troca Jenner por "Djéner", Pasteur por "Pastér" e Malho por "Málho" na hora de falar. Na primeira rodada, ouça os blocos b1 (Pasteur), b3 (Jenner) e b4 (O Malho e "vacino-obrigateza"). Se precisar ajustar, mude o `pronuncia.txt`: o `fazer.py` refaz só os blocos que têm a palavra.

### 5. Gravar, conferir, renderizar e mixar (~1 h 10 de máquina)

```sh
python3 fazer.py revolta-da-vacina
```

| Etapa | Tempo esperado no Mac de 16 GB | De onde vem a estimativa |
|---|---|---|
| roteiro → blocos.py | instantâneo | |
| voz (8 blocos, ~5 min 30 s de fala, até 3 takes por frase) | **~55 min** | régua medida no canal irmão: ~10 min de máquina por minuto de fala |
| conferência (Whisper, 59 frases) | **~1 min 30 s** | proporcional às 95 frases em 2 min 23 s do canal irmão |
| render (8 blocos + emenda) | **~6 a 10 min** | o canal irmão faz 0,81 s de máquina por segundo de vídeo; aqui as cenas têm mais textura (fibra, grão e íris), então conte até 1,5× isso. Medido no container (4 núcleos, sem GPU): bloco b3 de 34,3 s em 2 min 41 s |
| efeitos + mix | **~1 min** | medido no canal irmão: 40 s para 8 min |
| **total** | **~1 h 05 a 1 h 10** | |

- Ele retoma de onde parou. Se uma frase reprovar na conferência, use `cd revolta-da-vacina && python3 trocar_frase.py b2 6` (regrava só a frase 6 do b2) e depois rode o `fazer.py` de novo.
- **Trilha (opcional):** ponha um `trilha.mp3` da Biblioteca de Áudio do YouTube em `revolta-da-vacina/` e rode `python3 fazer.py revolta-da-vacina --refazer mix`. A trilha abaixa sob a voz, corta seco nas pausas de punchline e o total sai em −14 LUFS.

### 6. Conferir o vídeo antes de publicar (~15 min)

```sh
cd revolta-da-vacina
ffmpeg -v error -y -i REVOLTA-DA-VACINA-final.mp4 -vf "fps=1/10,scale=480:-1,tile=6x6" -frames:v 1 quadros.png && open quadros.png
```
- Assista ao vídeo inteiro. A lista editorial está no RELATORIO-PALITO, seção 8:
  - a piada nunca é com vítima;
  - o B5 é sério;
  - nenhuma comparação com vacina de hoje;
  - nenhum político vivo.
- Confira os números na tela contra o quadro do roteiro (o teste já garante que todo número da tela está no quadro).
- Título e miniatura: `revolta-da-vacina/TITULO.md`. Descrição com as fontes: `revolta-da-vacina/descricao.txt`. Ela já diz "Narração com voz sintética criada para este canal".
- O nome **TEM DOCUMENTO** é provisório (ver `IDENTIDADE.md`). Procure no YouTube antes de criar o canal.

## Testes mínimos (o que o `pytest` garante)

1. O roteiro tem 750 a 1.200 palavras e de 5 a 8 min. Não há número em algarismo na fala, e só os 3 fatos marcados estão pendentes, cada um com URL.
2. O **portão de números** aceita cada uma das 59 frases na forma em que o Whisper escreve ("mil novecentos e quatro" vira "1904"). O autoteste do portão reprova número trocado (1906 ouvido como 1916; 30 como 13).
3. A **trava**: o `fazer.py` para com "conferir no mac" e, com tudo conferido, gera o `blocos.py` e mostra `cenas_hf.py: 8/8 blocos`.
4. As **cenas montam**: toda cena aponta para frase que existe e os ids são únicos. As poses ficam dentro dos limites das articulações. Todo número na tela está no quadro, e o B5 não tem carimbo na frase das mortes. O `build_hf.py` gera os 8 `index.html` com JS válido (`node --check`), sem CDN e sem Google Fonts. O `sfx.py` gera as trilhas.
5. **Nenhuma menção** ao dono do canal nem à empresa dele em nenhum arquivo, e nenhuma menção ao canal irmão no roteiro, na tela, na descrição, no título ou na voz. O palito não reaproveita o desenho do canal irmão, e o synth não tem referência de voz de pessoa real.
