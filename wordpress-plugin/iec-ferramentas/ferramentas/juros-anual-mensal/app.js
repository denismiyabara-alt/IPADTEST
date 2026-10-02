/* Conversor de juros anual, mensal e diário · Investir e Coçar */
(function(){
"use strict";

var RAIZ = document.getElementById("juros-conv");
if (!RAIZ) return;

function $(id){ return document.getElementById(id); }
function num(id){ var v=parseFloat(String($(id).value).replace(",", ".")); return isFinite(v)?v:NaN; }
var nf2=new Intl.NumberFormat("pt-BR",{minimumFractionDigits:2,maximumFractionDigits:2});
var nf4=new Intl.NumberFormat("pt-BR",{minimumFractionDigits:4,maximumFractionDigits:4});
function pct(x, f){ return (f||nf2).format(x*100)+"%"; }

var NOME={12:"ao ano", 6:"ao semestre", 1:"ao mês"};

function calcular(){
  var taxa=num("j-taxa")/100, meses=Number($("j-periodo").value), msg="";
  if (!isFinite(taxa)) msg="Digite uma taxa.";
  else if (taxa<0 || taxa>10) msg="Use uma taxa entre 0% e 1.000%.";
  $("j-err").hidden=!msg; $("j-err").textContent=msg;
  if (msg){
    ["j-principal","j-ano","j-sem","j-mes","j-du"].forEach(function(id){ $(id).textContent="—"; });
    $("j-label").textContent=""; $("j-errado").textContent=""; $("j-story").hidden=true;
    return;
  }
  $("j-story").hidden=false;

  var anual=Math.pow(1+taxa, 12/meses)-1;
  var mensal=Math.pow(1+anual, 1/12)-1, semestral=Math.pow(1+anual, 1/2)-1, du=Math.pow(1+anual, 1/252)-1;
  $("j-ano").textContent=pct(anual);
  $("j-sem").textContent=pct(semestral);
  $("j-mes").textContent=pct(mensal);
  $("j-du").textContent=pct(du, nf4);

  var s=$("j-story");
  if (meses===1){
    var simples=taxa*12;
    $("j-label").textContent=pct(taxa)+" ao mês equivalem a";
    $("j-principal").textContent=pct(anual)+" ao ano";
    $("j-errado").textContent="Multiplicando por 12, daria "+pct(simples)+": "+nf2.format((anual-simples)*100)+" pontos a menos que a realidade.";
    s.textContent="Em 12 meses, cada R$ 1.000 vira "+nf2.format(1000*(1+anual))+" reais, e não "+nf2.format(1000*(1+simples))+". Num empréstimo, essa diferença sai do seu bolso.";
  } else {
    var errada=taxa/meses;
    $("j-label").textContent=pct(taxa)+" "+NOME[meses]+" equivalem a";
    $("j-principal").textContent=pct(mensal)+" ao mês";
    $("j-errado").textContent="Dividindo por "+meses+", daria "+pct(errada)+" ao mês: uma taxa maior que a real.";
    var comErro=Math.pow(1+errada, 12)-1;
    s.textContent="Se você usar "+pct(errada)+" ao mês, no fim do ano chega a "+pct(comErro)+", e não aos "+pct(anual)+" de verdade. Em simulação de longo prazo, esse erro vira bola de neve.";
  }
}

["j-taxa","j-periodo"].forEach(function(id){ $(id).addEventListener("input",calcular); $(id).addEventListener("change",calcular); });
calcular();
})();
