/* Quanto tempo para juntar R$ 1 milhão · Investir e Coçar */
(function(){
"use strict";

/* ---------- Cálculos (funções puras, testadas em tests/calculos.test.js) ---------- */

/* Taxa mensal equivalente: (1 + i)^(1/12) − 1 */
function taxaMensal(anual){ return Math.pow(1+anual, 1/12)-1; }

/* Saldo mês a mês. O rendimento incide sobre o saldo do mês anterior e o aporte entra no fim do mês. */
function serie(inicial, aporte, anual, meses){
  var im=taxaMensal(anual), s=inicial, out=[s];
  for (var t=1; t<=meses; t++){ s=s*(1+im)+aporte; out.push(s); }
  return out;
}

/* Saldo depois de "meses" meses, pela fórmula fechada (mesmo resultado da série) */
function saldoFinal(inicial, aporte, anual, meses){
  var im=taxaMensal(anual);
  if (im===0) return inicial+aporte*meses;
  var f=Math.pow(1+im, meses);
  return inicial*f+aporte*(f-1)/im;
}

/* Primeiro mês em que o saldo chega à meta. null se não chegar em "max" meses. */
function mesesAteMeta(inicial, aporte, anual, meta, max){
  max=max||1200;
  if (inicial>=meta) return 0;
  var im=taxaMensal(anual), s=inicial;
  for (var t=1; t<=max; t++){ s=s*(1+im)+aporte; if (s>=meta-1e-6) return t; }
  return null;
}

/* Aporte mensal para sair de "inicial" e chegar à "meta" em "meses" meses. 0 se o inicial já basta. */
function aporteNecessario(inicial, meta, anual, meses){
  var im=taxaMensal(anual);
  var falta=meta-(im===0 ? inicial : inicial*Math.pow(1+im, meses));
  if (falta<=0) return 0;
  return im===0 ? falta/meses : falta*im/(Math.pow(1+im, meses)-1);
}

var CALC={taxaMensal:taxaMensal, serie:serie, saldoFinal:saldoFinal, mesesAteMeta:mesesAteMeta, aporteNecessario:aporteNecessario};
if (typeof document==="undefined"){ if (typeof module==="object" && module && module.exports) module.exports=CALC; return; }

/* ---------- Tela ---------- */
var RAIZ = document.getElementById("um-milhao");
if (!RAIZ) return;

function $(id){ return document.getElementById(id); }
function num(id){ var v=parseFloat(String($(id).value).replace(",", ".")); return isFinite(v)?v:NaN; }
var brl=new Intl.NumberFormat("pt-BR",{style:"currency",currency:"BRL"});
var brl0=new Intl.NumberFormat("pt-BR",{style:"currency",currency:"BRL",maximumFractionDigits:0});
var nf1=new Intl.NumberFormat("pt-BR",{maximumFractionDigits:1});
var nf3=new Intl.NumberFormat("pt-BR",{minimumFractionDigits:3,maximumFractionDigits:3});
function compacto(v){
  var a=Math.abs(v);
  if (a>=1e6) return "R$ "+nf1.format(v/1e6)+" mi";
  if (a>=1e3) return "R$ "+nf1.format(v/1e3)+" mil";
  return "R$ "+Math.round(v);
}
function tempo(meses){
  var a=Math.floor(meses/12), m=meses%12, p=[];
  if (a) p.push(a+(a===1?" ano":" anos"));
  if (m) p.push(m+(m===1?" mês":" meses"));
  return p.join(" e ")||"0 meses";
}

/* ---------- Gráfico ---------- */
var NS="http://www.w3.org/2000/svg";
function el(tag, attrs, txt){ var e=document.createElementNS(NS,tag); for (var k in attrs) e.setAttribute(k,attrs[k]); if (txt!=null) e.textContent=txt; return e; }
function css(v){ return getComputedStyle(RAIZ).getPropertyValue(v).trim(); }
function larg(svg){ return Math.max(300, Math.round(svg.parentNode.clientWidth-36)); }
function passoBonito(max, alvo){
  var bruto=max/alvo, pot=Math.pow(10,Math.floor(Math.log10(bruto))), n=bruto/pot;
  return (n<=1?1:n<=2?2:n<=2.5?2.5:n<=5?5:10)*pot;
}

function desenhar(svg, saldos, guardado, meta){
  svg.innerHTML="";
  var W=larg(svg), H=Math.round(Math.min(320,W*0.6)), L=W<480?78:84, R=16, T=14, B=30;
  svg.setAttribute("viewBox","0 0 "+W+" "+H);
  var n=saldos.length-1; if (n<1) n=1;
  var ymax=Math.max(meta, saldos[saldos.length-1]);
  var passo=passoBonito(ymax, 4); ymax=Math.ceil(ymax/passo)*passo;
  function X(m){ return L+m/n*(W-L-R); }
  function Y(v){ return T+(1-v/ymax)*(H-T-B); }
  for (var v=0; v<=ymax+1e-9; v+=passo){
    svg.appendChild(el("line",{x1:L,x2:W-R,y1:Y(v),y2:Y(v),stroke:css(v===0?"--axis":"--grid"),"stroke-width":1}));
    svg.appendChild(el("text",{x:L-8,y:Y(v)+4,"text-anchor":"end"},compacto(v)));
  }
  var anos=n/12, pAno=anos<=10?1:anos<=20?2:anos<=50?5:10;
  for (var a=0; a<=anos+1e-9; a+=pAno){
    svg.appendChild(el("text",{x:X(a*12),y:H-B+18,"text-anchor":X(a*12)>W-R-24?"end":"middle"},a===0?"hoje":a+(W<480?"":(a===1?" ano":" anos"))));
  }
  svg.appendChild(el("line",{x1:L,x2:W-R,y1:Y(meta),y2:Y(meta),stroke:css("--amber"),"stroke-width":1.5,"stroke-dasharray":"5 4"}));
  function linha(vals, cor, w){
    var d=vals.map(function(y,i){ return (i?"L":"M")+X(i).toFixed(1)+" "+Y(y).toFixed(1); }).join(" ");
    svg.appendChild(el("path",{d:d,fill:"none",stroke:cor,"stroke-width":w,"stroke-linejoin":"round"}));
  }
  linha(guardado, css("--serie2"), 2);
  linha(saldos, css("--accent"), 2.75);
  var u=saldos.length-1;
  svg.appendChild(el("circle",{cx:X(u),cy:Y(saldos[u]),r:4.5,fill:css("--accent"),stroke:css("--surface"),"stroke-width":2}));
}

function limpar(){
  ["um-tempo","um-bolso","um-juros","um-final","um-inv"].forEach(function(id){ $(id).textContent="—"; });
  $("um-label").textContent=""; $("um-tempo-nota").textContent=""; $("um-inv-nota").textContent="";
  $("um-story").hidden=true; $("um-tabela").innerHTML=""; $("um-graf").innerHTML="";
}

function calcular(){
  var aporte=num("um-aporte"), inicial=num("um-inicial"), taxaPct=num("um-taxa"), meta=num("um-meta"), anos=num("um-anos");
  var msg="";
  if (![aporte,inicial,taxaPct,meta,anos].every(isFinite)) msg="Preencha todos os campos com números.";
  else if (aporte<0 || inicial<0) msg="Aporte e valor inicial não podem ser negativos.";
  else if (taxaPct<0 || taxaPct>20) msg="Use um rendimento real entre 0% e 20% ao ano.";
  else if (meta<=0) msg="A meta precisa ser maior que zero.";
  else if (anos<1 || anos>60 || Math.round(anos)!==anos) msg="O prazo do cálculo inverso precisa ser um número inteiro de 1 a 60 anos.";
  else if (aporte===0 && inicial<meta && taxaPct===0) msg="Sem aporte e sem rendimento, o dinheiro não cresce. Coloque algum aporte ou rendimento.";
  $("um-err").hidden=!msg; $("um-err").textContent=msg;
  if (msg){ limpar(); return; }
  $("um-story").hidden=false;

  var taxa=taxaPct/100, n=mesesAteMeta(inicial, aporte, taxa, meta, 1200);
  $("um-label").textContent="Para chegar a "+brl0.format(meta)+" guardando "+brl.format(aporte)+" por mês, a "+nf1.format(taxaPct)+"% ao ano acima da inflação, você leva";

  /* Cálculo inverso: não depende de chegar à meta */
  var inv=aporteNecessario(inicial, meta, taxa, anos*12);
  $("um-inv").textContent=brl.format(inv);
  $("um-inv-nota").textContent = inv===0
    ? "O que você já tem, rendendo "+nf1.format(taxaPct)+"% ao ano real, chega sozinho a "+brl0.format(meta)+" em "+anos+(anos===1?" ano":" anos")+"."
    : "Partindo de "+brl0.format(inicial)+" e rendendo "+nf1.format(taxaPct)+"% ao ano real (cerca de "+nf3.format(taxaMensal(taxa)*100)+"% ao mês), em "+anos+(anos===1?" ano":" anos")+". Em dinheiro de hoje.";

  if (n===null){
    ["um-tempo","um-bolso","um-juros","um-final"].forEach(function(id){ $(id).textContent="—"; });
    $("um-tempo").textContent="Mais de 100 anos";
    $("um-tempo-nota").textContent="";
    $("um-story").textContent="Com esses números a meta não chega em 100 anos. Tente aumentar o aporte ou ver o cálculo inverso abaixo.";
    $("um-tabela").innerHTML=""; $("um-graf").innerHTML="";
    return;
  }

  var saldos=serie(inicial, aporte, taxa, n), guardado=saldos.map(function(_,i){ return inicial+aporte*i; });
  var fim=saldos[n], bolso=inicial+aporte*n, juros=fim-bolso;
  $("um-tempo").textContent= n===0 ? "Você já chegou" : tempo(n);
  $("um-tempo-nota").textContent= n===0 ? "O valor que você já tem é igual ou maior que a meta." : "São "+n+" meses, ou cerca de "+nf1.format(n/12)+" anos.";
  $("um-bolso").textContent=brl0.format(bolso);
  $("um-juros").textContent=brl0.format(juros);
  $("um-final").textContent=brl0.format(fim);
  var pj=fim>0 ? juros/fim*100 : 0;
  $("um-story").textContent = n===0 ? "Sua meta já foi alcançada. Que tal colocar uma meta maior?" :
    "Dos "+brl0.format(fim)+" do fim, "+nf1.format(pj)+"% vieram dos juros e "+nf1.format(100-pj)+"% saíram do seu bolso. "+
    (aporte>0 ? "Guardando "+brl.format(aporte+100)+" por mês (R$ 100 a mais), o prazo cai para "+tempo(mesesAteMeta(inicial, aporte+100, taxa, meta, 1200))+"." : "");

  desenhar($("um-graf"), saldos, guardado, meta);

  var linhas="";
  for (var a=1; a<=Math.ceil(n/12); a++){
    var s=serie(inicial, aporte, taxa, a*12)[a*12], g=inicial+aporte*a*12;
    linhas+="<tr><td>"+a+"</td><td>"+brl0.format(g)+"</td><td>"+brl0.format(s-g)+"</td><td>"+brl0.format(s)+"</td></tr>";
  }
  $("um-tabela").innerHTML=linhas;
}

RAIZ.querySelectorAll(".cenarios button").forEach(function(b){
  b.addEventListener("click", function(){ $("um-taxa").value=b.getAttribute("data-taxa"); calcular(); });
});
["um-aporte","um-inicial","um-taxa","um-meta","um-anos"].forEach(function(id){ $(id).addEventListener("input",calcular); });
var rt; window.addEventListener("resize",function(){ clearTimeout(rt); rt=setTimeout(calcular,120); });
calcular();
})();
