"""Tabelas de referência conferidas à mão para a varredura automática.

EMPRESAS: raiz do ticker (4 letras) -> nomes/apelidos que identificam a empresa no texto.
  Base: nome de pregão do COTAHIST (B3) + cadastro da CVM (cad_cia_aberta.csv), já em site-ativos/cache.
  Só entram nomes inequívocos (ex.: "Itaúsa" para ITSA, "Santander" para SANB).
REGRAS_IR: regras em vigor em out/2026, com a fonte primária. Usadas para checar afirmações dos posts.
"""

EMPRESAS = {
    "ITSA": ["itaúsa", "itausa"],
    "ITUB": ["itaú unibanco", "itau unibanco", "banco itaú", "itaú", "itau"],
    "SANB": ["santander"],
    "BBDC": ["bradesco"],
    "BBAS": ["banco do brasil"],
    "BPAC": ["btg pactual", "btg"],
    "ROXO": ["nubank", "nu holdings"],
    "PETR": ["petrobras"],
    "VALE": ["vale s.a", "mineradora vale"],
    "ABEV": ["ambev"],
    "WEGE": ["weg"],
    "TAEE": ["taesa"],
    "EGIE": ["engie"],
    "CPLE": ["copel"],
    "CMIG": ["cemig"],
    "SBSP": ["sabesp"],
    "CSMG": ["copasa"],
    "SAPR": ["sanepar"],
    "VIVT": ["vivo", "telefônica brasil", "telefonica brasil"],
    "TIMS": ["tim brasil", "tim s.a"],
    "EQTL": ["equatorial"],
    "AXIA": ["axia", "eletrobras"],
    "ELET": ["eletrobras"],
    "ISAE": ["isa energia", "isa cteep", "cteep"],
    "TRPL": ["isa cteep", "cteep", "transmissão paulista"],
    "ALUP": ["alupar"],
    "CPFE": ["cpfl"],
    "ENEV": ["eneva"],
    "AURE": ["auren"],
    "UGPA": ["ultrapar"],
    "VBBR": ["vibra"],
    "BBSE": ["bb seguridade"],
    "CXSE": ["caixa seguridade"],
    "PSSA": ["porto seguro"],
    "IRBR": ["irb"],
    "KLBN": ["klabin"],
    "SUZB": ["suzano"],
    "RAIL": ["rumo"],
    "RENT": ["localiza"],
    "MGLU": ["magazine luiza", "magalu"],
    "LREN": ["lojas renner", "renner"],
    "RADL": ["raia drogasil", "raiadrogasil"],
    "RDOR": ["rede d'or", "rede dor"],
    "HYPE": ["hypera"],
    "SMFT": ["smart fit", "smartfit"],
    "EMBJ": ["embraer"],
    "EMBR": ["embraer"],
    "BRAV": ["brava energia", "brava"],
    "PASS": ["compass"],
    "CSAN": ["cosan"],
    "RAIZ": ["raízen", "raizen"],
    "SAUD": ["bradsaúde", "bradsaude"],
    "ODPV": ["odontoprev"],
    "SLCE": ["slc agrícola", "slc agricola"],
    "SMTO": ["são martinho", "sao martinho"],
    "BMEB": ["banco mercantil", "mercantil do brasil"],
    "WEST": ["westwing"],
    "AUAU": ["petz", "cobasi"],
    "PETZ": ["petz"],
    "SIMH": ["simpar"],
    "RANI": ["irani"],
    "LOGG": ["log commercial", "log cp"],
    "BRCO": ["bresco"],
    "TRXF": ["trx real estate", "trx"],
    "KNCR": ["kinea rendimentos"],
    "KNRI": ["kinea renda imobiliária", "kinea renda imobiliaria"],
    "HGLG": ["cshg logística", "cshg logistica"],
    "XPML": ["xp malls"],
    "XPLG": ["xp log"],
    "VISC": ["vinci shopping"],
    "MXRF": ["maxi renda"],
    "BTLG": ["btg pactual logística", "btg logística"],
    "MBRF": ["mbrf", "marfrig", "brf"],
    "TOTS": ["totvs"],
    "VIVA": ["vivara"],
    "ALOS": ["allos"],
    "CURY": ["cury"],
    "TEND": ["tenda"],
    "PLPL": ["plano & plano", "plano e plano"],
    "DXCO": ["dexco"],
    "ALPA": ["alpargatas"],
    "VAMO": ["vamos"],
    "MOTV": ["motiva", "ccr"],
    "GGPS": ["gps participações"],
    "TUPY": ["tupy"],
    "ARZZ": ["arezzo"],
    "BHIA": ["casas bahia"],
    "PCAR": ["pão de açúcar", "gpa"],
    "XPBR": ["xp inc"],
    "TSLA": ["tesla"],
    "NIKE": ["nike"],
    "COCA": ["coca-cola", "coca cola"],
    "AAPL": ["apple"],
    "NVDC": ["nvidia"],
    "MELI": ["mercado livre"],
    "AURA": ["aura minerals"],
    "EQPA": ["equatorial pará", "equatorial para"],
    "UNIP": ["unipar"],
    "BRSR": ["banrisul"],
    "CGAS": ["comgás", "comgas"],
    "JALL": ["jalles machado", "jalles"],
    "TTEN": ["3tentos"],
    "AGRO": ["brasilagro"],
    "BLAU": ["blau farmacêutica", "blau"],
    "VULC": ["vulcabras"],
    "DASA": ["dasa"],
    "TFCO": ["track & field", "track and field"],
    "HBSA": ["hidrovias"],
    "CAML": ["camil"],
    "SOJA": ["boa safra"],
    "PGMN": ["pague menos"],
    "BEES": ["banestes"],
    "JHSF": ["jhsf"],
    "IGTI": ["iguatemi"],
    "ENGI": ["energisa"],
    "PMAM": ["paranapanema"],
    "GOLD": ["ouro"],
}

# Nomes que só valem como empresa quando aparecem colados ao ticker (muito genéricos para o resto do texto).
AMBIGUOS = {"vale s.a", "mineradora vale", "itaú", "itau", "btg", "trx", "vamos", "ouro", "brava", "cury", "blau",
            "dasa", "tim s.a", "vivo", "gpa", "ccr", "brf", "jalles", "weg"}

# Regras de IR e fatos de mercado em vigor em 02/10/2026, conferidos na fonte primária.
REGRAS_IR = {
    "isencao_acoes_20mil": {
        "regra": "Ganho em ações no mercado à vista é isento quando o TOTAL DE VENDAS no mês é de até R$ 20 mil "
                 "(não o lucro). Não vale para day trade, ETF, FII nem BDR.",
        "fonte": "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2005/lei/l11196.htm (art. 38) e "
                 "https://normas.receita.fazenda.gov.br/sijut2consulta/link.action?idAto=67494 (IN RFB 1.585/2015, art. 59)",
    },
    "dividendos_2026": {
        "regra": "Lei 15.270/2025 (26/11/2025): desde jan/2026, IRRF de 10% sobre dividendos pagos pela MESMA empresa à "
                 "mesma pessoa física acima de R$ 50 mil no mês (sobre o total do mês); IRPF mínimo de até 10% para "
                 "renda anual acima de R$ 600 mil (cheio a partir de R$ 1,2 milhão). Abaixo disso, dividendo segue isento.",
        "fonte": "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15270.htm",
    },
    "jcp": {
        "regra": "IRRF sobre JCP passou de 15% para 17,5% em pagamentos/créditos desde 01/01/2026 (LC 224/2025).",
        "fonte": "https://www.planalto.gov.br/ccivil_03/leis/lcp/lcp224.htm",
    },
    "fii_isencao": {
        "regra": "Rendimento de FII é isento para PF se: cotas negociadas só em bolsa/balcão organizado, fundo com 100 "
                 "ou mais cotistas e o cotista com menos de 10% das cotas/rendimentos (Lei 14.754/2023 subiu de 50 "
                 "para 100 cotistas e trocou o limite). Ganho de capital na venda de cota: 20%.",
        "fonte": "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14754.htm (art. 3º da Lei 11.033 com nova redação)",
    },
    "come_cotas": {
        "regra": "Come-cotas em maio e novembro: 15% (longo prazo) ou 20% (curto prazo). Desde 2024 alcança também "
                 "fundos exclusivos (Lei 14.754/2023). ETF de renda variável e FII não têm come-cotas.",
        "fonte": "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2023/lei/l14754.htm",
    },
    "tabela_regressiva": {
        "regra": "Renda fixa: 22,5% até 180 dias; 20% de 181 a 360; 17,5% de 361 a 720; 15% acima de 720 dias.",
        "fonte": "https://www.planalto.gov.br/ccivil_03/_ato2004-2006/2004/lei/l11033.htm (art. 1º)",
    },
    "lci_lca": {
        "regra": "LCI/LCA seguem isentas para PF em 2026 (a MP 1.303/2025, que taxaria novas emissões em 5%, caducou "
                 "em 08/10/2025). Prazo mínimo sem correção por índice de preços: 6 meses para LCI e LCA desde a "
                 "Res. CMN 5.215 (mai/2025); antes 9 meses (Res. 5.119/2024 e 5.154/2024). Corrigidas pelo IPCA: "
                 "LCI 36 meses, LCA 12 meses. Os antigos 90 dias não valem desde fev/2024.",
        "fonte": "https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o%20CMN&numero=5215",
    },
    "fgc": {
        "regra": "FGC: até R$ 250 mil por CPF por instituição (conglomerado) e teto global de R$ 1 milhão a cada 4 anos.",
        "fonte": "https://www.fgc.org.br/garantia-fgc/sobre-a-garantia-fgc",
    },
    "isencao_irpf_5mil": {
        "regra": "Lei 15.270/2025: isenção de IRPF para rendimentos tributáveis de até R$ 5 mil por mês desde jan/2026 "
                 "(redução parcial até R$ 7.350).",
        "fonte": "https://www.planalto.gov.br/ccivil_03/_ato2023-2026/2025/lei/L15270.htm",
    },
    "day_trade": {
        "regra": "Day trade: 20% sobre o lucro, IRRF de 1%; operações comuns em ações: 15%.",
        "fonte": "https://www.planalto.gov.br/ccivil_03/leis/l8981.htm e IN RFB 1.585/2015",
    },
}

# Selic meta (SGS 432) vem do SQLite do site-ativos; dados de IPCA/CDI também.
