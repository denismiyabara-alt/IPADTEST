/* Comparador de renda fixa · Investir e Coçar */
(function(){
"use strict";

var RAIZ = document.getElementById("calc-rf");
if (!RAIZ) return;

function $(id){ return document.getElementById(id); }
function num(id){ var v=parseFloat(String($(id).value).replace(",", ".")); return isFinite(v)?v:NaN; }
var brl=new Intl.NumberFormat("pt-BR",{style:"currency",currency:"BRL"});
var nf2=new Intl.NumberFormat("pt-BR",{minimumFractionDigits:2,maximumFractionDigits:2});
function pct(x){ return nf2.format(x*100)+"%"; }
function esc(t){ return String(t).replace(/[&<>"]/g,function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); }

function aliquota(dias){ return dias<=180 ? 0.225 : dias<=360 ? 0.20 : dias<=720 ? 0.175 : 0.15; }
function posFixado(pct, cdi, anos){ return Math.pow(1+(Math.pow(1+cdi,1/252)-1)*pct, 252*anos)-1; }

function calcular(){
  var valor=num("r-valor"), meses=num("r-meses"), cdi=num("r-cdi")/100, ipca=num("r-ipca")/100;
  var cdb=num("r-cdb")/100, lci=num("r-lci")/100, pre=num("r-pre")/100, real=num("r-real")/100, msg="";
  if (![valor,meses,cdi,ipca,cdb,lci,pre,real].every(isFinite)) msg="Preencha todos os campos com números (use 0 para não comparar um produto).";
  else if (valor<=0) msg="O valor investido precisa ser maior que zero.";
  else if (meses<1 || meses>360 || Math.round(meses)!==meses) msg="Use um prazo inteiro de 1 a 360 meses.";
  else if (cdb<0 || lci<0 || pre<0) msg="As taxas não podem ser negativas.";
  else if (!(cdb>0 || lci>0 || pre>0 || real!==0)) msg="Informe a taxa de pelo menos um produto.";
  $("r-err").hidden=!msg; $("r-err").textContent=msg;
  if (msg){
    $("r-vencedor").textContent="—"; $("r-label").textContent=""; $("r-vencedor-nota").textContent="";
    $("r-barras").innerHTML=""; $("r-tabela").innerHTML=""; $("r-story").hidden=true; $("r-ir-nota").textContent="";
    return;
  }
  $("r-story").hidden=false;

  var anos=meses/12, dias=Math.round(meses*365.25/12), ir=aliquota(dias);
  var produtos=[];
  if (cdb>0) produtos.push({nome:"CDB "+nf2.format(cdb*100)+"% do CDI", bruto:posFixado(cdb,cdi,anos), ir:true});
  if (pre>0) produtos.push({nome:"Prefixado "+pct(pre), bruto:Math.pow(1+pre,anos)-1, ir:true});
  if (real!==0) produtos.push({nome:"IPCA + "+pct(real), bruto:Math.pow((1+ipca)*(1+real),anos)-1, ir:true});
  if (lci>0) produtos.push({nome:"LCI/LCA "+nf2.format(lci*100)+"% do CDI", bruto:posFixado(lci,cdi,anos), ir:false});
  produtos.forEach(function(p){
    p.imposto = p.ir && p.bruto>0 ? valor*p.bruto*ir : 0;
    p.liquido = valor*(1+p.bruto)-p.imposto;
    p.aa = Math.pow(p.liquido/valor, 1/anos)-1;
  });
  produtos.sort(function(a,b){ return b.liquido-a.liquido; });
  var top=produtos[0], seg=produtos[1];

  $("r-label").textContent="Quem deixa mais dinheiro no bolso em "+meses+(meses===1?" mês":" meses");
  $("r-vencedor").textContent=top.nome;
  $("r-vencedor-nota").textContent="Termina com "+brl.format(top.liquido)+" líquidos ("+pct(top.aa)+" ao ano depois do IR).";

  var maior=Math.max.apply(null, produtos.map(function(p){ return p.liquido-valor; }).concat([0.01]));
  $("r-barras").innerHTML=produtos.map(function(p,i){
    var w=Math.max(0,(p.liquido-valor)/maior*100);
    return '<div class="barra'+(i===0?" top":"")+'"><div class="nome">'+esc(p.nome)+'</div><div class="trilho"><div class="cheio" style="width:'+w.toFixed(1)+'%"></div><span class="val">+'+esc(brl.format(p.liquido-valor))+'</span></div></div>';
  }).join("");

  var s=$("r-story");
  if (seg){
    var dif=top.liquido-seg.liquido;
    s.textContent=dif<0.01 ? "Empate: "+top.nome+" e "+seg.nome+" terminam com o mesmo valor." :
      top.nome+" fica "+brl.format(dif)+" à frente de "+seg.nome+", se o CDI ficar em "+pct(cdi)+" e a inflação em "+pct(ipca)+" ao ano. Mude esses dois números para ver o resultado virar.";
  } else {
    s.textContent="Informe a taxa de mais um produto para comparar.";
  }

  $("r-tabela").innerHTML=produtos.map(function(p){
    return "<tr><td>"+esc(p.nome)+"</td><td>"+brl.format(valor*(1+p.bruto))+"</td><td>"+(p.ir?brl.format(p.imposto):"Isento")+"</td><td>"+brl.format(p.liquido)+"</td><td>"+pct(p.aa)+"</td></tr>";
  }).join("");
  $("r-ir-nota").textContent="Prazo estimado em "+dias+" dias corridos: alíquota de IR de "+nf2.format(ir*100)+"% sobre o rendimento.";
}

["r-valor","r-meses","r-cdi","r-ipca","r-cdb","r-lci","r-pre","r-real"].forEach(function(id){ $(id).addEventListener("input",calcular); });
calcular();
})();
