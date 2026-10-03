"""Peças comuns do OUTLIER → ENCAIXE: config, caminhos, texto normalizado, nicho, credenciais e o cliente mínimo da
API do YouTube (usado só no Mac, por coletar.py e descobrir_canais.py). Só biblioteca padrão."""
from __future__ import annotations

import glob
import json
import os
import re
import sys
import unicodedata
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

AQUI = Path(__file__).resolve().parent
RAIZ = AQUI.parent                      # raiz do IPADTEST
CONFIG_PADRAO = AQUI / "config.json"
YT_API = "https://www.googleapis.com/youtube/v3"


# ------------------------------------------------------------------------------------------------ config e caminhos
def carregar_config(p=None):
    p = Path(p or os.environ.get("OUTLIERS_CONFIG") or CONFIG_PADRAO)
    return json.loads(p.read_text(encoding="utf-8"))


def caminho(p, raiz=RAIZ):
    """'~' expandido; relativo = relativo à raiz do IPADTEST."""
    if p in (None, ""):
        return None
    q = Path(str(p)).expanduser()
    return q if q.is_absolute() else Path(raiz) / q


def primeiro_existente(lista, raiz=RAIZ):
    """Primeiro caminho que existe. Aceita glob ('video-radar-*.md' pega o mais recente pelo nome)."""
    for item in ([lista] if isinstance(lista, str) else lista or []):
        p = caminho(item, raiz)
        if p is None:
            continue
        if any(c in str(p) for c in "*?["):
            achados = sorted(glob.glob(str(p)))
            if achados:
                return Path(achados[-1])
        elif p.exists():
            return p
    return None


# ------------------------------------------------------------------------------------------------ texto
def norm(s):
    s = unicodedata.normalize("NFKD", str(s or "")).encode("ascii", "ignore").decode()
    return re.sub(r"\s+", " ", s.lower()).strip()


RE_TICKER = re.compile(r"(?<![A-Za-z0-9])([A-Z]{4}(?:3|4|5|6|11|31|32|33|34|35|39))(?![A-Za-z0-9])")


def tickers(texto):
    return sorted(set(RE_TICKER.findall(str(texto or "").upper())))


def classificar_nicho(titulo, descricao, regras):
    """('dentro', nicho) | ('fora', motivo) | ('fora', 'sem nicho do canal').

    Ordem: 1) 'fora' no título; 2) 'dentro' no título; 3) só se o título for neutro, a descrição decide, de novo com
    'fora' antes de 'dentro'. A descrição vem cheia de link de patrocínio ("cartão", "conta digital"), então ela não
    derruba um título que já é claramente do nicho."""
    fora, dentro = regras.get("fora") or {}, regras.get("dentro") or {}
    for alvo in (norm(titulo), norm(descricao)):
        if not alvo:
            continue
        for motivo, rx in fora.items():
            if re.search(rx, alvo):
                return "fora", motivo
        for nicho, rx in dentro.items():
            if re.search(rx, alvo):
                return "dentro", nicho
    return "fora", "sem nicho do canal"


def dmy(d):
    return f"{d:%d/%m}"


def iso(dt):
    return dt.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def ler_data(s):
    if not s:
        return None
    try:
        d = datetime.fromisoformat(str(s).replace("Z", "+00:00"))
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def ler_json(p, padrao=None):
    try:
        return json.loads(Path(p).read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return padrao


def gravar_json(p, d):
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_suffix(p.suffix + ".tmp")
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    tmp.replace(p)


# ------------------------------------------------------------------------------------------------ credenciais
def ler_env_arquivo(p):
    out = {}
    try:
        for linha in Path(p).expanduser().read_text(encoding="utf-8").splitlines():
            linha = linha.strip()
            if "=" in linha and not linha.startswith("#"):
                k, _, v = linha.partition("=")
                k = k.strip()
                if k.startswith("export "):
                    k = k[7:].strip()
                out[k] = v.strip().strip('"').strip("'")
    except OSError:
        pass
    return out


def credencial(nome, env=None, arquivos=()):
    """Primeiro o ambiente, depois os arquivos (o primeiro que tiver ganha). Nunca imprime o valor."""
    env = os.environ if env is None else env
    if env.get(nome):
        return env[nome]
    for a in arquivos or ():
        v = ler_env_arquivo(a).get(nome)
        if v:
            return v
    return ""


# ------------------------------------------------------------------------------------------------ gate
def importar_gate(cfg):
    """gate_qualidade.py do investir-e-cocar, por import (IEC_PIPELINE no ambiente vence a config). None se não achar."""
    dirs = [os.environ.get("IEC_PIPELINE")] + list((cfg.get("caminhos") or {}).get("gate_dir") or [])
    for d in dirs:
        p = caminho(d) if d else None
        if p and (p / "gate_qualidade.py").is_file():
            if str(p) not in sys.path:
                sys.path.insert(0, str(p))
            try:
                import gate_qualidade  # noqa: WPS433
                return gate_qualidade
            except Exception:  # gate quebrado não derruba a proposta: cai na checagem mínima
                return None
    return None


# ------------------------------------------------------------------------------------------------ YouTube (Mac)
class YouTube:
    """Cliente mínimo da Data API v3 com contagem de unidades. transporte(url) -> dict (os testes trocam)."""

    CUSTO = {"search": 100, "playlistItems": 1, "videos": 1, "channels": 1}

    def __init__(self, chave, transporte=None, timeout=20):
        self.chave = chave
        self.unidades = 0
        self.chamadas = {}
        self.timeout = timeout
        self.transporte = transporte or self._get

    def _get(self, url):
        req = urllib.request.Request(url, headers={"User-Agent": "IEC-outliers/1.0"})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:
            return json.loads(r.read().decode("utf-8"))

    def chamar(self, recurso, **params):
        params["key"] = self.chave
        url = f"{YT_API}/{recurso}?" + urllib.parse.urlencode(params)
        self.unidades += self.CUSTO.get(recurso, 1)
        self.chamadas[recurso] = self.chamadas.get(recurso, 0) + 1
        try:
            return self.transporte(url)
        except Exception as e:
            raise RuntimeError(str(e).replace(self.chave, "***")) from None

    def em_lotes(self, recurso, ids, part, **extra):
        out = []
        ids = list(dict.fromkeys(i for i in ids if i))
        for k in range(0, len(ids), 50):
            d = self.chamar(recurso, part=part, id=",".join(ids[k:k + 50]), maxResults=50, **extra)
            out += d.get("items", [])
        return out


def duracao_s(iso_dur):
    m = re.match(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso_dur or "")
    if not m:
        return None
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return d * 86400 + h * 3600 + mi * 60 + s


def faixa_por_inscritos(n):
    if n is None:
        return ""
    if n > 500_000:
        return "grande"
    if n >= 50_000:
        return "médio"
    if n >= 5_000:
        return "pequeno"
    return "micro"
