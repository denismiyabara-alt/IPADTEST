"""Downloads com cache em disco, pedido condicional e no máximo 1 requisição por segundo por host.

Cada arquivo baixado ganha um `<arquivo>.meta.json` com url, ETag, Last-Modified, sha256,
tamanho e data do download. Esse meta vira a linha de `fonte_arquivo` no SQLite.
Para em 403/429 (como a varredura SEO), sem insistir.
"""
import hashlib
import json
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

from . import config

_ultimo_por_host: dict[str, float] = {}


class Bloqueado(RuntimeError):
    """O servidor respondeu 403 ou 429: parar o pipeline em vez de insistir."""


def _esperar(host: str) -> None:
    falta = config.PAUSA_POR_HOST - (time.monotonic() - _ultimo_por_host.get(host, 0.0))
    if falta > 0:
        time.sleep(falta)
    _ultimo_por_host[host] = time.monotonic()


def meta_de(destino: Path) -> dict:
    p = destino.with_name(destino.name + ".meta.json")
    return json.loads(p.read_text()) if p.exists() else {}


def _gravar_meta(destino: Path, meta: dict) -> None:
    destino.with_name(destino.name + ".meta.json").write_text(json.dumps(meta, ensure_ascii=False, indent=1))


def baixar(url: str, destino: Path, *, forcar: bool = False, tentativas: int = 3) -> tuple[Path, bool]:
    """Baixa `url` em `destino` em streaming. Devolve (destino, mudou).

    Se já houver meta e o servidor responder 304, não baixa de novo. Se o arquivo foi apagado
    depois de extraído (ZIP grande), o meta continua valendo para o pedido condicional.
    """
    destino.parent.mkdir(parents=True, exist_ok=True)
    meta = meta_de(destino)
    cab = {"User-Agent": config.USER_AGENT}
    if meta and not forcar:
        if meta.get("etag"):
            cab["If-None-Match"] = meta["etag"]
        if meta.get("last_modified"):
            cab["If-Modified-Since"] = meta["last_modified"]
    host = urlparse(url).hostname or ""
    erro = None
    for n in range(tentativas):
        _esperar(host)
        try:
            req = urllib.request.Request(url, headers=cab)
            with urllib.request.urlopen(req, timeout=120) as r:
                tmp = destino.with_name(destino.name + ".parcial")
                h = hashlib.sha256()
                tam = 0
                with open(tmp, "wb") as f:
                    while True:
                        bloco = r.read(1 << 20)
                        if not bloco:
                            break
                        f.write(bloco)
                        h.update(bloco)
                        tam += len(bloco)
                tmp.replace(destino)
                _gravar_meta(destino, {
                    "url": url,
                    "arquivo": destino.name,
                    "etag": r.headers.get("ETag"),
                    "last_modified": r.headers.get("Last-Modified"),
                    "sha256": h.hexdigest(),
                    "bytes": tam,
                    "baixado_em": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                })
                return destino, True
        except urllib.error.HTTPError as e:
            if e.code == 304:
                return destino, False
            if e.code in (403, 429):
                raise Bloqueado(f"{url}: HTTP {e.code}. Parando para não insistir.") from e
            if e.code == 404:
                raise FileNotFoundError(url) from e
            erro = e
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            erro = e
        time.sleep(2 * (n + 1))
    raise RuntimeError(f"falha ao baixar {url}: {erro}")


def baixar_texto(url: str, destino: Path, *, idade_max_h: float = 12) -> Path:
    """Para respostas pequenas (API do BCB): reaproveita o cache se tiver menos de `idade_max_h` horas."""
    if destino.exists() and (time.time() - destino.stat().st_mtime) < idade_max_h * 3600:
        return destino
    baixar(url, destino, forcar=True)
    return destino
