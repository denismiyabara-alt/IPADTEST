/* IR na venda de cotas de FII · Investir e Coçar */
(function(){
"use strict";

/* ---------- Cálculos (funções puras, testadas em tests/calculos.test.js) ---------- */
var ALIQUOTA=0.20;          /* Lei 8.668/1993, art. 18 */
var DEDO_DURO=0.00005;      /* 0,005% sobre o valor de venda, Lei 11.033/2004, art. 2º */
var DARF_MINIMO=10;         /* DARF abaixo de R$ 10 não é pago: soma ao mês seguinte */

function irVendaFii(p){
  var valorVenda=p.venda*p.qtd;
  var resultado=(p.venda-p.pm)*p.qtd-(p.custos||0);
  var prej=Math.max(0, p.prejuizo||0), compensado=0, base=0, resto=prej;
  if (resultado>0){
    compensado=Math.min(prej, resultado);
    base=resultado-compensado;
    resto=prej-compensado;
  } else {
    resto=prej-resultado; /* resultado negativo aumenta o prejuízo a compensar */
  }
  var ir=base*ALIQUOTA;
  var dedo=valorVenda*DEDO_DURO;
  if (dedo<=1) dedo=0;           /* retenção de R$ 1 ou menos é dispensada */
  var darf=Math.max(0, ir-dedo);
  return {valorVenda:valorVenda, resultado:resultado, compensado:compensado, base:base, ir:ir,
          dedoDuro:dedo, darf:darf, pagarAgora: darf>=DARF_MINIMO, prejuizoRestante:resto};
}

/* Domingo de Páscoa (algoritmo de Meeus/Jones/Butcher), para a Sexta-feira Santa */
function pascoa(ano){
  var a=ano%19, b=Math.floor(ano/100), c=ano%100, d=Math.floor(b/4), e=b%4, f=Math.floor((b+8)/25),
      g=Math.floor((b-f+1)/3), h=(19*a+b-d-g+15)%30, i=Math.floor(c/4), k=c%4,
      l=(32+2*e+2*i-h-k)%7, m=Math.floor((a+11*h+22*l)/451),
      mes=Math.floor((h+l-7*m+114)/31), dia=((h+l-7*m+114)%31)+1;
  return new Date(Date.UTC(ano, mes-1, dia));
}
function feriadoNacional(dt){
  var md=String(dt.getUTCMonth()+1).padStart(2,"0")+"-"+String(dt.getUTCDate()).padStart(2,"0");
  if (["01-01","04-21","05-01","09-07","10-12","11-02","11-15","11-20","12-25"].indexOf(md)>=0) return true;
  var sexta=pascoa(dt.getUTCFullYear()); sexta.setUTCDate(sexta.getUTCDate()-2);
  return dt.getTime()===sexta.getTime();
}

/* Vencimento do DARF: último dia útil do mês seguinte ao da venda. Entrada e saída em "AAAA-MM-DD". */
function vencimentoDarf(dataVendaISO){
  var p=String(dataVendaISO).split("-"), ano=+p[0], mes=+p[1]; /* mes 1..12; o seguinte é "mes" em base 0 */
  var dt=new Date(Date.UTC(ano, mes+1, 0)); /* último dia do mês seguinte */
  while (dt.getUTCDay()===0 || dt.getUTCDay()===6 || feriadoNacional(dt)) dt.setUTCDate(dt.getUTCDate()-1);
  return dt.toISOString().slice(0,10);
}

var CALC={irVendaFii:irVendaFii, vencimentoDarf:vencimentoDarf, pascoa:pascoa};
if (typeof document==="undefined"){ if (typeof module==="object" && module && module.exports) module.exports=CALC; return; }

/* ---------- Tela ---------- */
var RAIZ = document.getElementById("ir-fii-venda");
if (!RAIZ) return;

function $(id){ return document.getElementById(id); }
function num(id){ var v=parseFloat(String($(id).value).replace(",", ".")); return isFinite(v)?v:NaN; }
var brl=new Intl.NumberFormat("pt-BR",{style:"currency",currency:"BRL"});
function br(iso){ var p=iso.split("-"); return p[2]+"/"+p[1]+"/"+p[0]; }
function hojeISO(){
  var d=new Date(), m=d.getMonth()+1, dia=d.getDate();
  return d.getFullYear()+"-"+(m<10?"0":"")+m+"-"+(dia<10?"0":"")+dia;
}
if (!$("fv-data").value) $("fv-data").value=hojeISO();

function calcular(){
  var p={pm:num("fv-pm"), venda:num("fv-venda"), qtd:num("fv-qtd"), custos:num("fv-custos"), prejuizo:num("fv-prejuizo")};
  var data=$("fv-data").value, msg="";
  if (![p.pm,p.venda,p.qtd,p.custos,p.prejuizo].every(isFinite)) msg="Preencha todos os campos com números (use 0 se não houver custos ou prejuízo).";
  else if (p.pm<=0 || p.venda<=0) msg="Os preços precisam ser maiores que zero.";
  else if (p.qtd<1 || Math.round(p.qtd)!==p.qtd) msg="A quantidade precisa ser um número inteiro de cotas.";
  else if (p.custos<0 || p.prejuizo<0) msg="Custos e prejuízo anterior não podem ser negativos.";
  else if (!/^\d{4}-\d{2}-\d{2}$/.test(data)) msg="Escolha a data da venda.";
  $("fv-err").hidden=!msg; $("fv-err").textContent=msg;
  if (msg){
    ["fv-darf","fv-lucro","fv-comp","fv-ir","fv-dedo","fv-resto"].forEach(function(id){ $(id).textContent="—"; });
    $("fv-label").textContent=""; $("fv-venc").textContent=""; $("fv-story").hidden=true;
    return;
  }
  $("fv-story").hidden=false;

  var r=irVendaFii(p), venc=vencimentoDarf(data);
  $("fv-lucro").textContent=(r.resultado<0?"−":"")+brl.format(Math.abs(r.resultado));
  $("fv-lucro").className="v "+(r.resultado>0?"pos":r.resultado<0?"neg":"");
  $("fv-comp").textContent=brl.format(r.compensado);
  $("fv-ir").textContent=brl.format(r.ir);
  $("fv-dedo").textContent=brl.format(r.dedoDuro);
  $("fv-resto").textContent=brl.format(r.prejuizoRestante);

  var s=$("fv-story");
  if (r.resultado<=0){
    $("fv-label").textContent="Nesta venda não há imposto a pagar";
    $("fv-darf").textContent="R$ 0,00"; $("fv-darf").className="big";
    $("fv-venc").textContent="";
    s.textContent = r.resultado<0
      ? "A venda deu prejuízo de "+brl.format(-r.resultado)+". Anote: ele pode ser abatido de lucros em vendas futuras de FII. O total a compensar fica em "+brl.format(r.prejuizoRestante)+"."
      : "A venda empatou: sem lucro, sem imposto.";
    return;
  }
  $("fv-label").textContent = r.pagarAgora ? "DARF a pagar (código 6015)" : "DARF abaixo de R$ 10: não se paga agora";
  $("fv-darf").textContent=brl.format(r.darf);
  $("fv-darf").className="big "+(r.pagarAgora?"neg":"");
  $("fv-venc").textContent = r.pagarAgora
    ? "Vencimento: "+br(venc)+", último dia útil do mês seguinte ao da venda."
    : "Some este valor ao DARF do mês seguinte e pague quando o total passar de R$ 10.";
  s.textContent="Lucro de "+brl.format(r.resultado)+
    (r.compensado>0 ? ", menos "+brl.format(r.compensado)+" de prejuízo anterior, dá "+brl.format(r.base)+" de base e " : ", com ")+
    brl.format(r.ir)+" de IR (20%)."+
    (r.dedoDuro>0 ? " Descontando os "+brl.format(r.dedoDuro)+" já retidos na venda, o DARF fica em "+brl.format(r.darf)+"." : " Não houve retenção na fonte (o dedo-duro deu R$ 1 ou menos), então o DARF é o IR inteiro.");
}

["fv-pm","fv-venda","fv-qtd","fv-custos","fv-prejuizo","fv-data"].forEach(function(id){
  $(id).addEventListener("input",calcular);
  $(id).addEventListener("change",calcular);
});
calcular();
})();
