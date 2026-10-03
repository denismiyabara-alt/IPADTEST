# ponytail: junta saidas do pdfshot/shot.mjs + metadados -> prints/prints.json
import json
FN="https://fnet.bmfbovespa.com.br/fnet/publico/exibirDocumento?id="
ent=json.load(open('fontes/dados.json'))['data']; ent={x['id']:x['dataEntrega'] for x in ent}
pdfid={"FR-13a-emissao.pdf":1277980,"NOTA-TECNICA-13a.pdf":1298710,"FR-shoppings-iguatemi.pdf":1280507}
jobs={j[0]:j for j in json.load(open('pdf_jobs.json'))}
web={j['id']:j for j in json.load(open('web_jobs.json'))}
out={}
for f in ['pdf_out.jsonl','web_all.jsonl']:
    for l in open(f):
        if l.startswith('{') and 'bbox' in l: r=json.loads(l); out[r['id']]=r
TIPO={1277980:"FATO RELEVANTE (13ª emissão)",1302616:"COMUNICADO AO MERCADO",1315144:"COMUNICADO (rotulado 'Anúncio de Encerramento' no fnet)",1277920:"ANÚNCIO DE INÍCIO",1302626:"MATERIAL PUBLICITÁRIO 13ª EMISSÃO",1298710:"NOTA TÉCNICA 13ª EMISSÃO",1309800:"RELATÓRIO GERENCIAL AGO/26",1313621:"COMUNICADO AO MERCADO (MoU Dasa)",1301577:"COMUNICADO AO MERCADO",1280507:"FATO RELEVANTE (Iguatemi, MoU)"}
M={ # id: (legenda, obs)
"d1a-13a-5bi":("o fundo pediu até R$ 5 bilhões na 13ª emissão","O FR escreve 'R$ 5.000.000.11,50' (erro de digitação do próprio documento; a pág. 1 traz R$ 5.000.000.011,50). fnet 1277980, entregue 05/08 19:19."),
"d1b-13a-preco-94":("cota nova: R$ 94,39 com o custo de entrada",""),
"d1c-27ago-preferencia-40mi":("cotistas compraram R$ 40,1 milhões na fase de preferência","R$ 40.141.424,08 = 425.272 cotas. O total de ~R$ 40,2 mi do roteiro soma as sobras (R$ 89.481,72, print d2b). O 0,8% é conta do canal (40,23 mi / 5,0 bi), não aparece no documento."),
"d1d-27ago-titulo":("27/08: acaba a vez dos cotistas (direito de preferência)",""),
"d2a-10set-titulo":("10/09: 'encerramento' das sobras... e início de outro período de subscrição","Título real do PDF: 'Encerramento do período de exercício do direito de subscrição de sobras e montante adicional e início do período de subscrição'. O rótulo 'Anúncio de Encerramento' é do cadastro no fnet (prints d2h/d2i)."),
"d2b-10set-sobras-948":("nas sobras, só 948 cotas","948 cotas = R$ 89.481,72."),
"d2c-10set-investidores-profissionais":("o que sobrou vai para Investidores Profissionais","Frase começa no fim da pág. 1 ('que poderão ser destinadas à') e continua na pág. 2; o print é da pág. 2."),
"d2d-10set-restam-52mi":("sobraram 52.624.178 cotas novas",""),
"d2e-10set-180-dias":("prazo: até 180 dias do Anúncio de Início (05/08) → ~01/02/2027","A data 01/02/2027 é conta do canal; o documento só diz 180 dias do Anúncio de Início."),
"d2f-10set-encerramento-da-distribuicao":("o encerramento de verdade ainda vai ter anúncio próprio","Até 29/09 não há anúncio de encerramento da distribuição na lista do fnet (conferido no JSON do fnet)."),
"d2g-anuncio-inicio-05ago":("Anúncio de Início: 05/08/2026","Crop grande (cabeçalho do anúncio); grifo na data do registro."),
"d2h-fnet-rotulo-anuncio-encerramento":("no site da B3, o papel de 10/09 está rotulado 'Anúncio de Encerramento'","Grade do fnet por CNPJ (50 linhas). Linha: Oferta Pública de Distribuição de Cotas · Anúncio de Encerramento · 10/09/2026 · entrega 10/09/2026 20:34. Texto pequeno (grade larga): dar zoom."),
"d2i-fnet-entrega-10set-2034":("entregue em 10/09/2026, 20h34","Mesma grade do d2h, grifo na data/hora de entrega."),
"d3a-berrini-titulo":("24/09: TRXF11 conclui aquisição de edifícios corporativos","fnet 1327288 (há cópia idêntica 1327296, marcada 'Cancelado' na grade do fnet — reenvio)."),
"d3b-berrini-340mi":("investimento total: R$ 340,25 milhões","Total inclui Thera (HAAA11) + Ed. Morumbi e HOFC (HOFC11)."),
"d3c-berrini-thera":("escritórios na Av. Eng. Luiz Carlos Berrini, 105 (Thera Corporate)",""),
"d3d-berrini-compensacao":("pago 'mediante compensação de créditos'",""),
"d3e-berrini-1010000-cotas":("o HAAA11 recebeu 1.010.000 cotas novas",""),
"d3f-berrini-parcela-inicial-95mi":("parcela paga em cota: R$ 95,33 milhões","95.333.900 / 1.010.000 = R$ 94,39 por cota (conferido). Preço do Thera = 95,33 + 154,01 = R$ 249,3 mi ('uns 250 milhões' ok)."),
"d3g-berrini-parcela-final-154mi":("o resto: R$ 154 milhões, em 84 meses",""),
"d3h-berrini-2033-ipca-920":("corrigido por IPCA + 9,20% ao ano",""),
"d3i-berrini-vence-2033":("saldo vence em 20 de outubro de 2033",""),
"d4a-viana-cap-857":("galpão de Viana/ES: cap rate de 8,57% ao ano","Roteiro diz 'oito vírgula seis' (arredondado) e usa 8,57% na cartela: bate."),
"d4b-viana-compensados-337mi":("até R$ 337,1 milhões em cota do fundo",""),
"d4c-viana-compensados-texto":("'poderão ser compensados com créditos'","É CVC com condições resolutivas: ainda não concluído."),
"d4d-viana-643mi":("preço total: R$ 643,6 milhões","O documento escreve o valor sem 'R$' ('643.556.977,53')."),
"d4e-brf-cap-1025":("sede da BRF: cap rate de 10,25% ao ano",""),
"d4f-brf-compensados-93mi":("até R$ 93,1 milhões em cota do fundo",""),
"d4g-brf-titulo":("escritura definitiva: imóvel locado para BRF, Curitiba",""),
"d4h-iguatemi-306mi-taxa-di":("saldo da Iguatemi (R$ 306,7 mi) corrigido pela Taxa DI","O valor pago em cotas (até R$ 350,5 mi) fica na pág. 2 logo acima (não grifado)."),
"d4i-iguatemi-titulo":("compromisso de compra de frações de shoppings Iguatemi","CVC sujeito a condição (financiamento, segundo a imprensa)."),
"d4j-hire11-compensacao-82mi":("HIRE11: R$ 82,6 milhões prioritariamente em cota da 13ª emissão","Acordo de investimento de 24/09 (entregue 25/09 09:24)."),
"d4k-logrecife-75mi":("LOG Recife II (Shopee): R$ 75 milhões...","Continua na pág. 2 (print d4k2)."),
"d4k2-logrecife-compensados":("...'compensados com créditos' da subscrição de cotas",""),
"d4l-extrema-cyrela-voltou":("galpão de Extrema 'integrou a negociação anteriormente anunciada' (Cyrela)","Compra de R$ 424,32 mi, fnet 1327152; é ativo do portfólio Cyrela cancelado em 31/08."),
"d5a-protecao-titulo":("material da oferta: 'Mecanismo de proteção de preço'","Material publicitário, fnet 1302626, entregue 27/08/2026 19:06, pág. 21."),
"d5b-protecao-205mi":("cenário limite do mecanismo: ≈ R$ 205 milhões (≈1,6% do ativo)","Na mesma página, o quadro 'Disciplina de preço' fala em 'menos de 1,7% do ativo total' — dois números no mesmo slide (1,6% e 1,7%). A conta de R$ 3,28/cota é do canal."),
"d5c-protecao-ganho-volta":("'Havendo ganho na venda, o TRXF11 recebe compensação proporcional'",""),
"d5d-protecao-6-18-meses":("ajuste pago em janelas de 6 a 18 meses",""),
"d7a-lockup-45-dias-material":("lock-up médio de 45 dias","Material da oferta, pág. 19. 'Médio' e 'termos indicativos': não é trava individual confirmada por negócio."),
"d7b-lockup-45-dias-nota-tecnica":("Nota Técnica: 'Lock-up médio de 45 dias a partir da liquidação'","Nota Técnica fnet 1298710 (entregue 24/08), pág. 13."),
"d6a-brc-titulo":("28/09: documentos definitivos para venda de imóveis",""),
"d6b-brc-207mi":("vendidos ao BRC por R$ 207.252.400,00",""),
"d6c-brc-pago-em-cotas":("pago com cotas do BRC (compensação de créditos)","O FR não diz literalmente '100% em cotas'; diz que o valor total foi pago por compensação com a subscrição de cotas do BRC."),
"d6d-brc-lucro-051":("lucro estimado: R$ 0,51 por cota","Mesmo parágrafo traz a TIR de 38,49% (roteiro diz não usar)."),
"d6e-brc-15-imoveis":("venda de 15 imóveis","Lista dos 15 imóveis logo abaixo no mesmo print."),
"d8a-rg-cota-patrimonial-9661":("cota patrimonial: R$ 96,61 (31/08)","Relatório gerencial de agosto (data-base 31/08). O roteiro usa R$ 96,62 (Investidor10, print p1c) — diferença de 1 centavo."),
"d8b-rg-vacancia-05":("vacância física: 0,5%",""),
"d8c-rg-rendimento-093":("rendimento no mês: R$ 0,93",""),
"d9a-dasa-77mi":("prédio Dasa: venda por R$ 77 milhões à vista","É MoU (memorando), não venda concluída."),
"d9b-dasa-1223-acima-laudo":("12,23% acima do último laudo",""),
"d9c-dasa-11a-emissao-compensacao":("comprado na 11ª emissão com compensação de créditos",""),
"d10-goiania-41mi":("16/09: escritura de venda de imóvel (Setor Bueno, Goiânia)","FR conjunto TRXF11/TRXB11, fnet 1322394."),
"d10b-goiania-41mi":("vendido por R$ 41 milhões","Pág. 2 do FR de 16/09."),
"d11a-nt-yield-on-cost":("Nota Técnica 6.1: yield on cost = resultado sobre o capital efetivamente desembolsado","Grifo termina em '(parcelamento,'."),
"d11b-iguatemi-yoc-1234":("Iguatemi: yield on cost de 12,34% durante o pagamento","ATENÇÃO: no mesmo quadro o FR de 07/08 (fnet 1280507) traz cap rate de 8,02% a.a., não 7,3% como está no roteiro (bloco 6 e cartela). Não achei 7,3% nesse documento — conferir de onde veio o 7,3 antes de gravar."),
"d12a-desiste-lajes-27ago":("27/08: TRXF11 desiste do portfólio de lajes (Pátio Victor Malzoni)","O comunicado não traz o valor (R$ 1,03 bi vem da imprensa/FR anterior)."),
"d12b-desiste-cyrela-31ago":("31/08: desiste do portfólio da Cyrela","Fato relevante 31/08 09:26, fnet 1304485. Crop alto (título no topo, Cyrela no fim)."),
"p1-i10-cotacao-grafico-6m":("TRXF11 em 6 meses: de ~R$ 91 para ~R$ 72 (cotação padrão)","Print de 29/09 à tarde: R$ 72,25 (roteiro usa R$ 71,94 da manhã; diferença muda '22,45' para 22,14/cota). Gráfico sem valores pontuais de 31/07 (91,10) e 26/08 (70,11); eixo mínimo R$ 68,71. Cotação padrão, não ajustada."),
"p1b-i10-pvp-075":("P/VP: 0,75",""),
"p1c-i10-vp-9662-vacancia":("valor patrimonial por cota: R$ 96,62","Mesmo card mostra vacância 0,50% e último rendimento R$ 0,93."),
"p2-i10-dividendos-093":("dividendo de R$ 0,93 por cota, todo mês","Tabela mostra de 31/03 a 31/08 (data com); linhas mais antigas ficam esmaecidas pelo site. Extra de R$ 1,50: data com 30/06, pago 14/07."),
"p2b-i10-dividendo-extra-150":("extra de R$ 1,50 (pago em julho)","Extra de R$ 1,00 (data com 30/12/2025, pago 15/01) está fora do recorte visível."),
"p3-i10-haaa11":("HAAA11 (Hedge AAA), o vendedor da Berrini","Cotação R$ 56,00 em 29/09, liquidez diária R$ 2,54 mil."),
"m01-sd-emissao-10bi":("Seu Dinheiro, 06/08: emissão de até R$ 10 bilhões","R$ 10 bi = R$ 5 bi + lote adicional de 100%. O roteiro fala em 5 bi (montante inicial)."),
"m02-radar-despenca":("Radar FII: 'TRXF11 despenca com 13ª emissão bilionária'","Sem data visível no recorte."),
"m03-infomoney-queda-20":("InfoMoney, 21/08: queda de 20% em 12 meses",""),
"m04-sd-desiste-malzoni":("Seu Dinheiro, 27/08: desiste de quase R$ 1 bilhão (Pátio Victor Malzoni)",""),
"m05-infomoney-cyrela-2bi":("InfoMoney/Reuters: Cyrela confirma desistência de R$ 2 bi","Manchete diz R$ 2 bi; roteiro usa R$ 2,14 bi."),
"m06-empiricus-948-sobras":("Empiricus: 948 cotas nas sobras",""),
"m06b-empiricus-investidores-profissionais":("52,6 milhões de cotas seguem para investidores profissionais",""),
"m07-infomoney-340mi":("InfoMoney, 14/09: compra de dois corporativos por R$ 340,3 mi",""),
"m08-sd-340mi-cotas-caem":("Seu Dinheiro, 14/09: cotas caem após compra de R$ 340 mi",""),
"m09-mt-138bi":("Money Times, 24/09: mais de R$ 1,38 bilhão em compras",""),
"m10-mt-iguatemi":("Money Times, 24/09: avança na compra de shoppings da Iguatemi",""),
"m11-sd-283bi":("Seu Dinheiro, 24/09: paga R$ 2,83 bilhões, mas FII cai","R$ 2,83 bi é soma do portal (inclui pagamentos a prazo); roteiro usa ~R$ 3,3 bi assinados em setembro."),
"m11b-sd-queda-27-no-ano":("queda de 27% em 2026",""),
"m12-infomoney-brc-207":("InfoMoney: conclui venda de 15 imóveis por R$ 207,25 mi",""),
"m13-arevista-brc-detalhe":("'a operação não representa entrada imediata de dinheiro no caixa'","Recorte pega o fim do título cortado no topo ('um detalhe'); A Revista, 28-29/09."),
"m14-suno-brc-junho":("Suno, 11/06: o acordo com o BRC vem de junho","Mostra que a venda ao BRC foi acertada em 10-11/06 (proposta vinculante); 28/09 foi o fechamento."),
"m15-clubefii-condicoes":("Clube FII News: parte dos negócios ainda depende de condições",""),
"r1-receita-fii-20":("Receita Federal: venda de cota de FII, alíquota de 20%","Página da Receita 'Fundos de Investimento no Brasil'. ATENÇÃO: o mesmo texto da Receita tem um parágrafo acima (fora do recorte) dizendo que lucros distribuídos por FII têm IR de 20% na fonte — não usar."),
"r2-receita-isencao-so-acoes-ouro":("isenção de R$ 20 mil vale só para ações e ouro","A página não cita FII na isenção; a lista de isentos só traz ações e ouro (a leitura 'FII não tem' é inferência pela ausência)."),
"r3-receita-darf-ultimo-dia-util":("DARF até o último dia útil do mês seguinte (código 6015)",""),
"r4-receita-compensacao-perdas":("prejuízo compensa ganho no mesmo mês ou nos seguintes","A página é de ações/operações comuns; que perda de FII só compensa ganho de FII não está neste recorte."),
}
res=[]
for oid,(leg,obs) in M.items():
    r=out.get(oid)
    if not r: print("SEM PRINT",oid); continue
    if oid in jobs:
        j=jobs[oid]; pdf=j[1]; fid=pdfid.get(pdf) or int(pdf[1:-4]); e=ent.get(fid,"")
        fonte=f"FNET B3 · {TIPO.get(fid,'FATO RELEVANTE')} · entregue {e} · pág. {j[2]}".replace("entregue  ·","·")
        url=FN+str(fid); trecho=j[3]
    else:
        j=web[oid]; url=j['url']; trecho=j['grifo']
        dom=url.split('/')[2].replace('www.','')
        fonte={'fnet.bmfbovespa.com.br':'FNET B3 · grade de documentos do TRXF11','investidor10.com.br':'INVESTIDOR10 · 29/09/2026','gov.br':'RECEITA FEDERAL · gov.br'}.get(dom,dom.upper())
    res.append(dict(id=oid,arquivo=oid+".png",url=url,fonte=fonte,trecho_citado=trecho,bbox_trecho=r['bbox'],bbox_linhas=r['linhas'],largura_px=r['w'],altura_px=r['h'],obs=obs,legenda=leg))
json.dump(res,open('../prints/prints.json','w'),ensure_ascii=False,indent=1)
print(len(res),"prints; faltando:",[k for k in out if k not in M])
