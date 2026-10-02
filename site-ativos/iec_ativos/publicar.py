"""Etapa 6: publicar. Destino configurável; nada é publicado sem comando explícito.

  pasta       (padrão) copia saida/ para uma pasta local, só os arquivos que mudaram (por hash).
  sftp        stub documentado: envia para a hospedagem (subpasta /acoes/, /fiis/... do domínio).
  cloudflare  stub documentado: Cloudflare Pages (plano B, subdomínio dados.).

Credenciais só por variável de ambiente (no GitHub Actions, em Secrets). Nada de senha no código.
  IEC_SFTP_HOST, IEC_SFTP_PORTA (22), IEC_SFTP_USUARIO, IEC_SFTP_CHAVE (caminho da chave), IEC_SFTP_PASTA
  CLOUDFLARE_API_TOKEN, CLOUDFLARE_ACCOUNT_ID, IEC_CF_PROJETO
Antes de publicar: rodar `validar` e `gerar`; páginas com teste bloqueante não estão em saida/ novas.
"""
import hashlib
import os
import shutil
from pathlib import Path

from . import config

IGNORAR = {"_relatorio.json", "paginas.csv"}  # relatórios internos não vão para o site


def _hash(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def arquivos_para_enviar(origem: Path, destino_hashes: dict[str, str]) -> list[str]:
    mudou = []
    for p in sorted(origem.rglob("*")):
        if p.is_file() and p.name not in IGNORAR:
            rel = p.relative_to(origem).as_posix()
            if destino_hashes.get(rel) != _hash(p):
                mudou.append(rel)
    return mudou


def publicar_pasta(para: str | None, simular=False) -> list[str]:
    if not para:
        raise SystemExit("Informe --para /caminho/da/pasta (ex.: uma cópia local do public_html).")
    dest = Path(para)
    atuais = {p.relative_to(dest).as_posix(): _hash(p) for p in dest.rglob("*") if p.is_file()} if dest.exists() else {}
    lista = arquivos_para_enviar(config.SAIDA, atuais)
    for rel in lista:
        print(("simular: " if simular else "copiando: ") + rel)
        if not simular:
            (dest / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(config.SAIDA / rel, dest / rel)
    print(f"{len(lista)} arquivos {'mudariam' if simular else 'copiados'}")
    return lista


def _exigir(*nomes):
    faltam = [n for n in nomes if not os.environ.get(n)]
    if faltam:
        raise SystemExit(f"Faltam variáveis de ambiente: {', '.join(faltam)}")


def publicar_sftp(simular=False):
    """Stub. Implementação prevista (quando o Denis confirmar a hospedagem e o acesso SFTP/SSH):
    1. ler os hashes publicados de `<IEC_SFTP_PASTA>/.iec-hashes.json` (gravado a cada envio);
    2. enviar só `arquivos_para_enviar(...)` com `sftp -b` ou `rsync -avz --checksum -e "ssh -i $IEC_SFTP_CHAVE"`;
    3. regravar `.iec-hashes.json`; 4. se usar Cloudflare na frente, limpar o cache das URLs alteradas.
    Conferir antes, na hospedagem, se uma pasta real /acoes/ tem prioridade sobre o WordPress (DESENHO 1)."""
    _exigir("IEC_SFTP_HOST", "IEC_SFTP_USUARIO", "IEC_SFTP_CHAVE", "IEC_SFTP_PASTA")
    lista = arquivos_para_enviar(config.SAIDA, {})
    print(f"[stub] enviaria {len(lista)} arquivos para {os.environ['IEC_SFTP_USUARIO']}@{os.environ['IEC_SFTP_HOST']}:"
          f"{os.environ['IEC_SFTP_PASTA']} (nada foi enviado)")
    raise SystemExit("Destino sftp ainda é stub: falta a decisão sobre a hospedagem.")


def publicar_cloudflare(simular=False):
    """Stub. Implementação prevista (plano B, subdomínio): `npx wrangler pages deploy saida
    --project-name $IEC_CF_PROJETO` com CLOUDFLARE_API_TOKEN e CLOUDFLARE_ACCOUNT_ID no ambiente. Nesse caso,
    gerar com IEC_BASE_ATIVOS=https://dados.investirecocaresocomecar.com.br para canonical, sitemap e
    redirecionamentos apontarem para o subdomínio."""
    _exigir("CLOUDFLARE_API_TOKEN", "CLOUDFLARE_ACCOUNT_ID", "IEC_CF_PROJETO")
    print(f"[stub] rodaria: npx wrangler pages deploy {config.SAIDA} --project-name {os.environ['IEC_CF_PROJETO']}")
    raise SystemExit("Destino cloudflare ainda é stub: falta a decisão sobre a hospedagem.")


def publicar(destino="pasta", para=None, simular=False):
    if destino == "pasta":
        return publicar_pasta(para, simular)
    if destino == "sftp":
        return publicar_sftp(simular)
    if destino == "cloudflare":
        return publicar_cloudflare(simular)
    raise SystemExit(f"destino desconhecido: {destino}")
