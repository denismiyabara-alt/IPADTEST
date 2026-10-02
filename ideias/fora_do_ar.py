"""Os 30 longos fora do ar que mais trouxeram inscritos, com a classificação para a decisão do Denis.

Uso: python3 ideias/fora_do_ar.py   (lê auditoria-canal/dados/, grava ideias/fora-do-ar-top30.csv)
"""
import csv
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "auditoria-canal"))
import analisar as A  # noqa: E402

# Classificação feita à mão a partir do título (id → (classe, tema perene a regravar)).
# "regravar" = o assunto continua sendo buscado e dá para fazer sem recomendar ativo.
# Os demais são chamadas de compra/venda ou notícias de 2019–2022: não voltam ao ar.
PERENE = {
    "U53EJSYX-ew": "onde deixar a reserva em 2026: rendimento da conta, CDB de liquidez diária e FGC (ângulo de investimento)",
    "k08bpBRzm3U": "cheque especial e os dias sem juros: como os bancos cobram",
    "es9ap7LDRXo": "quanto rende R$ 100, R$ 1.000 e R$ 10.000 hoje (CDI, poupança, conta remunerada)",
    "sZtR98so5Ek": "como investir em empresas americanas pela B3: BDR, custos e IR",
    "-lWZgsVR3T0": "desdobramento de ações: o que muda (e o que não muda) para quem tem a ação",
    "aWC2feyFI1E": "follow-on: o que é, por que dilui e o que o acionista pode fazer",
    "XRl_3LjuuN4": "follow-on: o que é, por que dilui e o que o acionista pode fazer",
}
# Regra do Denis: o Investir e Coçar não faz dívida, cartão nem finanças pessoais. Esses vão para o Faz a Conta
# (ou só ficam no canal principal com ângulo de investimento).
DESTINO = {
    "k08bpBRzm3U": "Faz a Conta (dívida: fora do nicho do canal principal)",
    "U53EJSYX-ew": "canal principal só com ângulo de investimento; senão, Faz a Conta",
}


def main():
    d = A.Dados(RAIZ / "auditoria-canal" / "dados")
    lo = [r for r in d.fora_do_publico if r["formato"] == "longo"]
    top = sorted(lo, key=lambda r: -(A.num(r.get("inscritos_ganhos")) or 0))[:30]
    saida = RAIZ / "ideias" / "fora-do-ar-top30.csv"
    with open(saida, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["posicao", "video_id", "publicado", "titulo", "views", "inscritos", "classe", "regravar_como", "destino", "decisao_denis"])
        for i, r in enumerate(top, 1):
            vid = r["video_id"]
            classe = "tema perene: regravar atualizado" if vid in PERENE else "recomendação ou notícia datada: fica fora"
            w.writerow([i, vid, r.get("publicado", ""), r.get("titulo", "").strip(), int(A.num(r.get("views")) or 0),
                        int(A.num(r.get("inscritos_ganhos")) or 0), classe, PERENE.get(vid, ""),
                        DESTINO.get(vid, "canal principal" if vid in PERENE else ""), ""])
    print(f"{len(lo)} longos fora do ar; top 30 em {saida.relative_to(RAIZ)}; {sum(v in PERENE for v in (r['video_id'] for r in top))} perenes")


if __name__ == "__main__":
    main()
