# Como rodar no Mac (canal de espionagem, episódio 1: A captura de Eichmann)

Tudo fica em `canais-dark/espionagem/`. Rode os comandos **dentro dessa pasta**, salvo onde diz "na pasta do episódio".

```
espionagem/
  COMO-RODAR.md  IDENTIDADE.md  VOZ.md  NOMES.md
  licencas-ep01.csv        ← uma linha por imagem e por reconstituição do ep. 1
  pronuncia.txt            ← grafia de pronúncia dos nomes estrangeiros (só para a voz)
  roteiro.py               ← lê/valida o roteiro.md (normalizador: número em algarismo vira aviso)
  portao.py                ← portão de conferência da voz (texto + números), testável sem Mac
  synth_voz.py             ← voz VoiceDesign + 3 takes + portão Whisper
  conferir.py              ← reaudita blocos já gravados
  comparar_voz.py          ← prova de que a voz não imita ninguém
  build_hf.py              ← identidade visual + peças HyperFrames
  baixar_imagens.py        ← baixa as imagens da planilha
  rodar.py                 ← pipeline (status / tudo / só render)
  fontes/                  ← Courier Prime e Barlow Condensed (OFL)
  quadros/                 ← 3 quadros de teste renderizados
  ep01-eichmann/roteiro.md  cenas_hf.py
  tests/test_espionagem.py
```

## 0. Instalar (uma vez)

```sh
python3 -m pip install -U mlx-audio mlx-whisper numpy soundfile scipy pytest
python3 -m pip install resemblyzer      # opcional: portão de timbre e comparar_voz.py
brew install ffmpeg node                 # se ainda não tiver
mkdir -p vendor && npm pack gsap@3.14.2 && tar xzf gsap-3.14.2.tgz && cp package/dist/gsap.min.js vendor/ && rm -rf package gsap-3.14.2.tgz
```

O último comando é opcional: sem `vendor/gsap.min.js`, o HTML usa o GSAP do jsDelivr.

## 1. Testes mínimos (1 s, sem voz e sem rede)

```sh
cd canais-dark/espionagem && python3 -m pytest tests -q
```

Conferem: o roteiro passa no normalizador de números (nenhum algarismo na voz, nenhuma frase começando com número), tem entre 2.000 e 2.600 palavras, toda `* fonte:` existe no quadro e todo fato do quadro é usado; o portão de voz acerta os 12 casos do episódio; as cenas dos 10 blocos montam; toda imagem citada nas cenas está na planilha; a planilha tem as colunas do modelo, nenhuma coluna vazia e nada NC/ND; a morte é só texto sobre preto; nenhum arquivo cita o dono ou os outros canais.

## 2. Conferir os fatos (trava da voz)

O `rodar.py` **não grava voz** enquanto houver fato no quadro `## Fatos conferidos` (fim do `ep01-eichmann/roteiro.md`) com status diferente de `conferido`. Hoje são **38 de 48 em `CONFERIR NO MAC`**; 10 estão conferidos: F31, F37, F43, F48 (03/10) e, em 07/10/2026, F01, F02, F03, F16, F33 e F34, todos em documento primário (CIA name file no NARA, págs. citadas no quadro; texto oficial da S/RES/138). O F49 é novo: a frase "os documentos liberados não mostram repasse a Israel" saiu do F16 porque é afirmação negativa (conferir em Bascomb ou cortar).

Para cada linha: abrir a fonte da coluna 3 (livro na página, documento na URL), anotar a página no lugar de "pág. CONFERIR" e trocar o status para `conferido`. Se o fato não se confirmar: corrigir a frase no roteiro (e o número na tela, se houver), ou cortar.

Pontos que exigem atenção especial:
- **F16** resolvido em 07/10/2026: despacho EGMA-32934, 19/03/1958, vol. 2 (NAID 139331937), págs. 77–78. **F33/F34** resolvidos pelo texto oficial da resolução.
- **F49** (sem repasse a Israel em 1958): conferir em Bascomb; sem página, cortar a frase.
- **F42** (contestação da tese de Arendt, fonte Stangneth): fora da bibliografia principal. Sem conferir, cortar as duas frases.
- **F46** ("única pena de morte por tribunal civil"): se não achar fonte, cortar a frase.
- **F05, F09, F15, F20, F22, F24, F25, F39, F45** têm divergência entre fontes descrita na coluna 3; o roteiro já usa a formulação mais prudente.

Depois: `python3 roteiro.py ep01-eichmann/roteiro.md` não pode mais listar fato "conferir no mac".

## 3. Imagens

```sh
python3 baixar_imagens.py ep01-eichmann      # baixa para ep01-eichmann/imagens/ (o Commons limita: o script espera e tenta de novo)
```

Para cada linha **sem** prefixo `REC-` da `licencas-ep01.csv`:
1. abrir `url_do_item`, confirmar a licença e (regra 5 do relatório) **o selo de domínio público nos EUA** além do de Israel;
2. salvar o print da página em `prints/<arquivo>.png` (com a data visível);
3. trocar `verificado_por` por quem conferiu e `data_verificacao` pela data;
4. se a base legal não se sustentar (marcadas na coluna `base_legal`: passaporte, cartão da El Al, ordem de prisão), **não usar**: trocar a cena no `cenas_hf.py` por uma peça REC.

Conferência de 07/10/2026 (páginas do Commons e catálogo do NARA lidos daqui): **6 confirmadas** (`cia-memo-dulles-1953`, `cia-memo-1958-clemens`, `resolucao-138-onu`, `eichmann-cabine-anotacoes-1961`, `dinur-testemunha-1961`, `cinejornal-1961-eichmann`) e **9 trocadas por REC** e tiradas da planilha, porque a página do Commons só traz o selo do país de origem (PD-Israel ou PD-AR-Photo) e nenhum selo dos EUA, que o próprio modelo do Commons exige: passaporte da Cruz Vermelha, Eichmann no julgamento (GPO D482-067), Isser Harel 1969, Britannia da El Al, cartão da El Al, ordem de prisão de 23/05/1960, juízes, Hausner e Servatius, sentença de 15/12/1961. Foto israelense de Estado de 1958–1969 só caiu em domínio público em Israel depois de 1996, então os EUA restauraram o copyright (URAA): o selo não existe. Uma foto equivalente com PD-author do GPO no Commons pode voltar, com linha nova na planilha. A cena virou nome ou cartela datilografada (`REC-cartelas-nomes`, `REC-cartela-*`), e "É este documento." saiu do B2. A fala do julgamento usa a foto da cabine (PD-author).

Pendências: os prints das páginas (`prints/`), e `julgamento-ushmm-sessao.mp4` (USHMM ainda barrado; hoje não entra em nenhuma cena). O cinejornal: `.ogv` vira `.mp4` sem áudio.

## 4. Voz (uma vez para o canal, depois por episódio)

```sh
python3 synth_voz.py --candidatas                       # 12 vozes em candidatas/ ; ouvir e escolher a semente
VOZ_SEMENTE=<n> python3 synth_voz.py --mestra           # voz-mestra.wav (fora do git)
VOZ_COMPARAR="/caminho/voz1.wav,/caminho/voz2.wav" python3 comparar_voz.py   # tem que dar "ok (diferente)"
```

Anotar a semente e o resultado da comparação em `VOZ.md`. Ouvir os nomes do `pronuncia.txt` numa candidata e ajustar a grafia se algum sair errado (ex.: "Harel" deve soar "Rarél").

## 5. Episódio

```sh
python3 rodar.py ep01-eichmann --status       # só lê
VOZ_SEMENTE=<n> python3 rodar.py ep01-eichmann
```

Faz, em ordem: `blocos.py` a partir do roteiro → voz bloco a bloco (`synth_voz.py`, 3 takes, portão) → `conferir.py` em todos os blocos (para se alguma frase reprovar) → `build_hf.py` + `npx hyperframes@0.8.78 render` por bloco → `ep01-eichmann-video.mp4`. Retoma de onde parou (bloco com `voz_bN.wav` não é regravado). Para refazer só cenas e render: `--so-render`.

Para ver uma cena antes de renderizar tudo (na pasta do episódio):

```sh
cd ep01-eichmann && python3 ../build_hf.py b3 --sem-voz && cd hf-b3 && npx --yes hyperframes@0.8.78 snapshot --at 138 --describe false
```

## 6. Antes de publicar

- Duração: o roteiro tem ~2.320 palavras; estimativa de **16,5 a 18 min** (144 a 160 palavras por minuto, com as pausas). Se a voz real passar de 18 min, cortar primeiro F42 (duas frases), depois a frase da F46.
- Assistir inteiro com a lista da linha editorial (relatório, seção 4.1): nada sobre o conflito atual, nenhum adjetivo sobre povos, morte só contada.
- Descrição do vídeo: bibliografia completa (coluna 3 do quadro), créditos das imagens (coluna `credito_na_tela`) e a frase "Narração com voz sintética criada para este canal. As cenas marcadas como reconstituição são animações."
- Trocar a marca d'água: `CANAL_NOME="<nome escolhido>"` no ambiente do `rodar.py` (ver `NOMES.md`).
