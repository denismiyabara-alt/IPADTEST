"""Caminhos e parâmetros fixos do pipeline. Tudo pode ser trocado por variável de ambiente."""
import os
from datetime import date
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent          # site-ativos/ (futuro repo iec-ativos)
CACHE = Path(os.environ.get("IEC_CACHE", RAIZ / "cache"))
RAW = CACHE / "raw"                                     # arquivos baixados (CSV extraídos, JSON)
DB = Path(os.environ.get("IEC_DB", CACHE / "dados.sqlite"))
SAIDA = Path(os.environ.get("IEC_SAIDA", RAIZ / "saida"))
TEMPLATES = RAIZ / "templates"
# Fonte única das ferramentas: a pasta do plugin (no repo iec-ativos vira vendor/iec-ferramentas).
PLUGIN = Path(os.environ.get("IEC_PLUGIN", RAIZ.parent / "wordpress-plugin" / "iec-ferramentas"))
COTACOES_LINKADAS = Path(os.environ.get("IEC_COTACOES", RAIZ / "dados" / "referencia" / "cotacoes-linkadas.txt"))
SEO_VARREDURA = Path(os.environ.get("IEC_VARREDURA", RAIZ.parent / "seo" / "varredura.json"))

SITE_URL = os.environ.get("IEC_SITE_URL", "https://investirecocaresocomecar.com.br").rstrip("/")
SITE_NOME = "Investir e Coçar"
EMAIL_ERROS = os.environ.get("IEC_EMAIL_ERROS", "contato@investirecocaresocomecar.com.br")

# Data de corte: hoje, salvo IEC_HOJE=AAAA-MM-DD (útil para reproduzir uma execução).
HOJE = date.fromisoformat(os.environ["IEC_HOJE"]) if os.environ.get("IEC_HOJE") else date.today()

ANOS_DFP = list(range(HOJE.year - 5, HOJE.year))        # 5 exercícios fechados
ANOS_ITR = list(range(HOJE.year - 3, HOJE.year + 1))    # 12+ trimestres
ANOS_FII = list(range(HOJE.year - 2, HOJE.year + 1))    # 24+ informes mensais
ANOS_COTAHIST = list(range(HOJE.year - 5, HOJE.year + 1))  # 5 anos para o gráfico de preço

USER_AGENT = "iec-ativos/0.1 (+https://investirecocaresocomecar.com.br)"
PAUSA_POR_HOST = 1.0   # segundos entre requisições ao mesmo host

AVISO_CURTO = "Dados públicos calculados automaticamente. Não é recomendação de compra ou venda."
AVISO_COMPLETO = ("Esta página reúne dados públicos da CVM, da B3 e do Banco Central, calculados "
                  "automaticamente. Não é recomendação de compra ou venda, nem análise de valores "
                  "mobiliários. Os números podem ter atraso ou erro: confira nos documentos oficiais, "
                  "linkados em cada tabela, antes de decidir.")
