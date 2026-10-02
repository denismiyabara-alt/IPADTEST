/* Calculadora LCI e LCA × CDB · Investir e Coçar */
(function(){
"use strict";

var RAIZ = document.getElementById("calc-lci-lca");
if (!RAIZ) return;

function $(id){ return document.getElementById(id); }
function num(id){ var v=parseFloat(String($(id).value).replace(",", ".")); return isFinite(v)?v:NaN; }
var brl=new Intl.NumberFormat("pt-BR",{style:"currency",currency:"BRL"});
var nf1=new Intl.NumberFormat("pt-BR",{minimumFractionDigits:1,maximumFractionDigits:1});
var nf2=new Intl.NumberFormat("pt-BR",{minimumFractionDigits:2,maximumFractionDigits:2});

/* Tabela regressiva do IR em renda fixa, por dias corridos */
function aliquota(dias){ return dias<=180 ? 0.225 : dias<=360 ? 0.20 : dias<=720 ? 0.175 : 0.15; }

/* Rendimento bruto de um título a "pct" do CDI por "dias" corridos */
function rendimento(pct, cdi, dias){
  var diaria=Math.pow(1+cdi, 1/252)-1, du=dias*252/365;
  return Math.pow(1+diaria*pct, du)-1;
}

/* % do CDI que um CDB precisa pagar para empatar com a LCI/LCA, depois do IR */
function cdbEquivalente(pctLci, cdi, dias){
  var alvo=rendimento(pctLci, cdi, dias), ir=aliquota(dias), lo=0, hi=pctLci*3;
  for (var k=0; k<100; k++){
    var mid=(lo+hi)/2;
    if (rendimento(mid, cdi, dias)*(1-ir) < alvo) lo=mid; else hi=mid;
  }
  return (lo+hi)/2;
}

function prazoTexto(d){
  if (d%365===0) return (d/365)+(d===365?" ano":" anos");
  return d+" dias";
}

function calcular(){
  var taxa=num("l-taxa")/100, cdb=num("l-cdb")/100, dias=num("l-dias"), cdi=num("l-cdi")/100, valor=num("l-valor");
  var msg="";
  if (![taxa,cdb,dias,cdi,valor].every(isFinite)) msg="Preencha todos os campos com números.";
  else if (taxa<=0 || cdb<=0) msg="As taxas precisam ser maiores que zero.";
  else if (dias<30 || dias>3650 || Math.round(dias)!==dias) msg="Use um prazo inteiro entre 30 e 3.650 dias.";
  else if (cdi<=0 || cdi>0.5) msg="Use um CDI entre 0,1% e 50% ao ano.";
  else if (valor<=0) msg="O valor investido precisa ser maior que zero.";
  $("l-err").hidden=!msg; $("l-err").textContent=msg;
  if (msg){
    ["l-equiv","l-ir","l-liq-lci","l-liq-cdb","l-dif"].forEach(function(id){ $(id).textContent="—"; });
    $("l-label").textContent=""; $("l-equiv-nota").textContent=""; $("l-story").hidden=true; $("l-tabela").innerHTML="";
    return;
  }
  $("l-story").hidden=false;

  var ir=aliquota(dias), eq=cdbEquivalente(taxa, cdi, dias);
  var lci=valor*(1+rendimento(taxa, cdi, dias));
  var brutoCdb=valor*rendimento(cdb, cdi, dias), cdbLiq=valor+brutoCdb*(1-ir);
  var dif=cdbLiq-lci;

  $("l-label").textContent="Para empatar com a LCI/LCA a "+nf1.format(taxa*100)+"% do CDI em "+prazoTexto(dias)+", o CDB precisa pagar";
  $("l-equiv").textContent=nf1.format(eq*100)+"% do CDI";
  $("l-equiv-nota").textContent="Pela conta rápida (dividir pelo IR) daria "+nf1.format(taxa/(1-ir)*100)+"% do CDI.";
  $("l-ir").textContent=nf1.format(ir*100)+"%";
  $("l-liq-lci").textContent=brl.format(lci);
  $("l-liq-cdb").textContent=brl.format(cdbLiq);
  $("l-dif").textContent=(dif>=0?"+":"−")+brl.format(Math.abs(dif));
  $("l-dif").className="v "+(Math.abs(dif)<0.005?"":(dif>0?"pos":"neg"));

  var s=$("l-story");
  if (Math.abs(dif)<0.005){ s.className="story"; s.textContent="Empate técnico: os dois terminam com o mesmo valor líquido."; }
  else if (dif>0){ s.className="story"; s.textContent="O CDB a "+nf1.format(cdb*100)+"% do CDI ganha: termina com "+brl.format(dif)+" a mais, mesmo pagando "+nf1.format(ir*100)+"% de IR sobre o rendimento."; }
  else { s.className="story"; s.textContent="A LCI/LCA ganha: termina com "+brl.format(-dif)+" a mais. Para o CDB valer a pena, ele teria de pagar pelo menos "+nf1.format(eq*100)+"% do CDI."; }

  var linhas="";
  [90,180,181,360,361,720,721,1095,1825].forEach(function(d){
    linhas+="<tr><td>"+prazoTexto(d)+"</td><td>"+nf1.format(aliquota(d)*100)+"%</td><td>"+nf2.format(cdbEquivalente(taxa,cdi,d)*100)+"% do CDI</td></tr>";
  });
  $("l-tabela").innerHTML=linhas;
}

["l-taxa","l-cdb","l-dias","l-cdi","l-valor"].forEach(function(id){ $(id).addEventListener("input",calcular); });
calcular();
})();
