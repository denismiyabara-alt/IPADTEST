/* Calculadora de preço justo (Bazin e Graham) · Investir e Coçar */
(function(){
"use strict";

var RAIZ = document.getElementById("preco-justo");
if (!RAIZ) return;

function $(id){ return document.getElementById(id); }
function num(id){ var v=parseFloat(String($(id).value).replace(",", ".")); return isFinite(v)?v:NaN; }
var brl=new Intl.NumberFormat("pt-BR",{style:"currency",currency:"BRL"});
var nf2=new Intl.NumberFormat("pt-BR",{minimumFractionDigits:2,maximumFractionDigits:2});
function pct(x){ return nf2.format(x*100)+"%"; }

function margem(el, justo, preco){
  var m=justo/preco-1;
  el.textContent = m>=0 ? pct(m)+" acima da cotação" : pct(-m)+" abaixo da cotação";
  el.className="fine "+(m>=0?"pos":"neg");
  return m;
}

function calcular(){
  var preco=num("g-preco"), dpa=num("g-dpa"), taxa=num("g-taxa")/100, lpa=num("g-lpa"), vpa=num("g-vpa"), msg="";
  if (![preco,dpa,taxa,lpa,vpa].every(isFinite)) msg="Preencha todos os campos com números.";
  else if (preco<=0) msg="A cotação precisa ser maior que zero.";
  else if (dpa<0) msg="Dividendos não podem ser negativos.";
  else if (taxa<=0) msg="O dividend yield mínimo precisa ser maior que zero.";
  $("g-err").hidden=!msg; $("g-err").textContent=msg;
  if (msg){
    ["g-bazin","g-graham","g-dy","g-pl","g-pvp"].forEach(function(id){ $(id).textContent="—"; });
    $("g-bazin-m").textContent=""; $("g-graham-m").textContent=""; $("g-story").hidden=true;
    return;
  }
  $("g-story").hidden=false;

  var bazin=dpa/taxa, mB=null, mG=null;
  if (dpa>0){ $("g-bazin").textContent=brl.format(bazin); mB=margem($("g-bazin-m"), bazin, preco); }
  else { $("g-bazin").textContent="Não se aplica"; $("g-bazin-m").textContent="Sem dividendos nos últimos 12 meses."; $("g-bazin-m").className="fine"; }

  var grahamOk = lpa>0 && vpa>0, graham = grahamOk ? Math.sqrt(22.5*lpa*vpa) : 0;
  if (grahamOk){ $("g-graham").textContent=brl.format(graham); mG=margem($("g-graham-m"), graham, preco); }
  else { $("g-graham").textContent="Não se aplica"; $("g-graham-m").textContent="Precisa de LPA e VPA positivos."; $("g-graham-m").className="fine"; }

  $("g-dy").textContent=pct(dpa/preco);
  $("g-pl").textContent=lpa>0 ? nf2.format(preco/lpa) : "Prejuízo";
  $("g-pvp").textContent=vpa>0 ? nf2.format(preco/vpa) : "VPA negativo";

  var acima=[mB,mG].filter(function(m){ return m!==null && m>0; }).length;
  var validos=[mB,mG].filter(function(m){ return m!==null; }).length;
  var s=$("g-story");
  if (!validos){ s.className="story"; s.textContent="Nenhum dos dois métodos se aplica com esses números. Isso já é uma informação: a empresa não paga dividendos ou não tem lucro e patrimônio positivos."; }
  else if (acima===validos){ s.className="story"; s.textContent="Pelos métodos que se aplicam, a cotação está abaixo do preço calculado. Isso indica que pode haver desconto, não que a ação vai subir: confira dívida, setor e se o lucro é recorrente."; }
  else if (acima===0){ s.className="story bad"; s.textContent="Pelos métodos que se aplicam, a cotação está acima do preço calculado. O mercado pode estar pagando por um crescimento que esses métodos não enxergam, ou a ação pode estar cara."; }
  else { s.className="story"; s.textContent="Os dois métodos discordam. Isso é comum: Bazin olha só os dividendos e Graham só o lucro e o patrimônio. Entenda por que eles divergem antes de tirar conclusões."; }
}

["g-preco","g-dpa","g-taxa","g-lpa","g-vpa"].forEach(function(id){ $(id).addEventListener("input",calcular); });
calcular();
})();
