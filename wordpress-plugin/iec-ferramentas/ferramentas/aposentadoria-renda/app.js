/* Simulador de aposentadoria: renda passiva e INSS · Investir e Coçar */
(function(){
"use strict";

/* ---------- Cálculos (funções puras, testadas em tests/calculos.test.js) ---------- */
var TETO_INSS_2026=8475.55; /* Portaria Interministerial MPS/MF nº 13/2026, conferido em 02/10/2026 */

function taxaMensal(anual){ return Math.pow(1+anual, 1/12)-1; }

/* Patrimônio que, retirando "retirada" ao ano, paga a renda que o INSS não cobre */
function patrimonioNecessario(rendaMensal, inssMensal, retirada){
  var cobrir=Math.max(0, rendaMensal-inssMensal);
  return cobrir*12/retirada;
}

/* Saldo mês a mês (rendimento sobre o saldo anterior, aporte no fim do mês) */
function serie(inicial, aporte, anual, meses){
  var im=taxaMensal(anual), s=inicial, out=[s];
  for (var t=1; t<=meses; t++){ s=s*(1+im)+aporte; out.push(s); }
  return out;
}

function saldoFinal(inicial, aporte, anual, meses){
  var im=taxaMensal(anual);
  if (im===0) return inicial+aporte*meses;
  var f=Math.pow(1+im, meses);
  return inicial*f+aporte*(f-1)/im;
}

function aporteNecessario(inicial, meta, anual, meses){
  var im=taxaMensal(anual);
  var falta=meta-(im===0 ? inicial : inicial*Math.pow(1+im, meses));
  if (falta<=0) return 0;
  return im===0 ? falta/meses : falta*im/(Math.pow(1+im, meses)-1);
}

function mesesAteMeta(inicial, aporte, anual, meta, max){
  if (inicial>=meta) return 0;
  var im=taxaMensal(anual), s=inicial;
  for (var t=1; t<=max; t++){ s=s*(1+im)+aporte; if (s>=meta-1e-6) return t; }
  return null;
}

/* Tudo de uma vez, para a tela e para os testes */
function simular(p){
  var meses=(p.alvo-p.idade)*12;
  var necessario=patrimonioNecessario(p.renda, p.inss, p.retirada);
  var projetado=saldoFinal(p.patrimonio, p.aporte, p.taxa, meses);
  var falta=Math.max(0, necessario-projetado);
  var aporteNec=aporteNecessario(p.patrimonio, necessario, p.taxa, meses);
  var chega=mesesAteMeta(p.patrimonio, p.aporte, p.taxa, necessario, Math.max(0,(100-p.idade)*12));
  return {meses:meses, necessario:necessario, projetado:projetado, falta:falta, aporteNecessario:aporteNec,
          idadeChega: chega===null ? null : p.idade+chega/12};
}

var CALC={TETO_INSS_2026:TETO_INSS_2026, taxaMensal:taxaMensal, patrimonioNecessario:patrimonioNecessario, serie:serie,
          saldoFinal:saldoFinal, aporteNecessario:aporteNecessario, mesesAteMeta:mesesAteMeta, simular:simular};
if (typeof document==="undefined"){ if (typeof module==="object" && module && module.exports) module.exports=CALC; return; }

/* ---------- Tela ---------- */
var RAIZ = document.getElementById("aposentadoria-renda");
if (!RAIZ) return;

function $(id){ return document.getElementById(id); }
function num(id){ var v=parseFloat(String($(id).value).replace(",", ".")); return isFinite(v)?v:NaN; }
var brl=new Intl.NumberFormat("pt-BR",{style:"currency",currency:"BRL"});
var brl0=new Intl.NumberFormat("pt-BR",{style:"currency",currency:"BRL",maximumFractionDigits:0});
var nf1=new Intl.NumberFormat("pt-BR",{maximumFractionDigits:1});
function compacto(v){
  var a=Math.abs(v);
  if (a>=1e6) return "R$ "+nf1.format(v/1e6)+" mi";
  if (a>=1e3) return "R$ "+nf1.format(v/1e3)+" mil";
  return "R$ "+Math.round(v);
}
function idadeTexto(x){
  var a=Math.floor(x+1e-9), m=Math.round((x-a)*12);
  if (m===12){ a++; m=0; }
  return a+" anos"+(m ? " e "+m+(m===1?" mês":" meses") : "");
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

function desenhar(svg, idade, hoje, nec, meta){
  svg.innerHTML="";
  var W=larg(svg), H=Math.round(Math.min(320,W*0.6)), L=W<480?78:84, R=16, T=14, B=30;
  svg.setAttribute("viewBox","0 0 "+W+" "+H);
  var n=hoje.length-1;
  var ymax=Math.max(meta, hoje[n], nec[n], 1);
  var passo=passoBonito(ymax, 4); ymax=Math.ceil(ymax/passo)*passo;
  function X(m){ return L+m/n*(W-L-R); }
  function Y(v){ return T+(1-v/ymax)*(H-T-B); }
  for (var v=0; v<=ymax+1e-9; v+=passo){
    svg.appendChild(el("line",{x1:L,x2:W-R,y1:Y(v),y2:Y(v),stroke:css(v===0?"--axis":"--grid"),"stroke-width":1}));
    svg.appendChild(el("text",{x:L-8,y:Y(v)+4,"text-anchor":"end"},compacto(v)));
  }
  var anos=n/12, pAno=anos<=10?1:anos<=20?2:anos<=50?5:10;
  for (var a=0; a<=anos+1e-9; a+=pAno){
    svg.appendChild(el("text",{x:X(a*12),y:H-B+18,"text-anchor":X(a*12)>W-R-24?"end":"middle"},(idade+a)+(W<480?"":" anos")));
  }
  if (meta>0) svg.appendChild(el("line",{x1:L,x2:W-R,y1:Y(meta),y2:Y(meta),stroke:css("--amber"),"stroke-width":1.5,"stroke-dasharray":"5 4"}));
  function linha(vals, cor, w){
    var d=vals.map(function(y,i){ return (i?"L":"M")+X(i).toFixed(1)+" "+Y(y).toFixed(1); }).join(" ");
    svg.appendChild(el("path",{d:d,fill:"none",stroke:cor,"stroke-width":w,"stroke-linejoin":"round"}));
  }
  linha(nec, css("--serie2"), 2);
  linha(hoje, css("--accent"), 2.75);
  svg.appendChild(el("circle",{cx:X(n),cy:Y(hoje[n]),r:4.5,fill:css("--accent"),stroke:css("--surface"),"stroke-width":2}));
}

function limpar(){
  ["ap-necessario","ap-proj","ap-falta","ap-aporte-nec","ap-idade-chega"].forEach(function(id){ $(id).textContent="—"; });
  $("ap-label").textContent=""; $("ap-necessario-nota").textContent=""; $("ap-story").hidden=true; $("ap-graf").innerHTML="";
}

function calcular(){
  var p={idade:num("ap-idade"), alvo:num("ap-alvo"), renda:num("ap-renda"), inss:num("ap-inss"),
         patrimonio:num("ap-patrimonio"), aporte:num("ap-aporte"), taxa:num("ap-taxa")/100, retirada:num("ap-retirada")/100};
  var msg="";
  if (![p.idade,p.alvo,p.renda,p.inss,p.patrimonio,p.aporte,p.taxa,p.retirada].every(isFinite)) msg="Preencha todos os campos com números.";
  else if (Math.round(p.idade)!==p.idade || Math.round(p.alvo)!==p.alvo || p.idade<14 || p.alvo>100) msg="Use idades inteiras, de 14 a 100 anos.";
  else if (p.alvo<=p.idade) msg="A idade para parar precisa ser maior que a sua idade hoje.";
  else if (p.renda<=0) msg="A renda desejada precisa ser maior que zero.";
  else if (p.inss<0 || p.patrimonio<0 || p.aporte<0) msg="INSS, patrimônio e aporte não podem ser negativos.";
  else if (p.taxa<0 || p.taxa>0.15) msg="Use um rendimento real entre 0% e 15% ao ano.";
  else if (p.retirada<0.01 || p.retirada>0.10) msg="Use uma retirada entre 1% e 10% ao ano.";
  $("ap-err").hidden=!msg; $("ap-err").textContent=msg;

  var aviso=$("ap-aviso");
  aviso.hidden=!(isFinite(p.inss) && p.inss>TETO_INSS_2026);
  aviso.textContent="O benefício informado passa do teto do INSS de 2026, de "+brl.format(TETO_INSS_2026)+" por mês. Confira o valor na sua simulação do Meu INSS.";
  if (msg){ limpar(); return; }
  $("ap-story").hidden=false;

  var r=simular(p);
  $("ap-label").textContent="Patrimônio necessário para tirar "+brl0.format(Math.max(0,p.renda-p.inss))+" por mês, com retirada de "+nf1.format(p.retirada*100)+"% ao ano";
  $("ap-necessario").textContent=brl0.format(r.necessario);
  $("ap-necessario-nota").textContent = p.inss>0
    ? "A renda de "+brl0.format(p.renda)+" menos os "+brl0.format(p.inss)+" do INSS. Em dinheiro de hoje."
    : "Sem contar com o INSS. Em dinheiro de hoje.";
  $("ap-proj-k").textContent="Você teria aos "+p.alvo;
  $("ap-proj").textContent=brl0.format(r.projetado);
  $("ap-falta").textContent= r.falta>0 ? brl0.format(r.falta) : "Nada";
  $("ap-falta").className="v "+(r.falta>0?"neg":"pos");
  $("ap-aporte-nec").textContent=brl.format(r.aporteNecessario);
  $("ap-idade-chega").textContent= r.idadeChega===null ? "Não chega até 100" : idadeTexto(r.idadeChega);

  var s=$("ap-story");
  if (r.necessario===0){
    s.textContent="Pelo valor informado, o INSS já cobre a renda desejada. Lembre que o benefício depende do seu histórico de contribuições: confira a sua estimativa.";
  } else if (r.falta>0){
    s.textContent="No ritmo de hoje, faltariam "+brl0.format(r.falta)+" aos "+p.alvo+" anos. Para fechar a conta, o aporte teria de ser "+brl.format(r.aporteNecessario)+" por mês, "+
      brl.format(r.aporteNecessario-p.aporte)+" a mais. Outras alavancas: parar um pouco depois, aceitar uma renda menor ou contar com mais rendimento (com mais risco).";
  } else {
    s.textContent="No ritmo de hoje, você passaria do necessário aos "+p.alvo+" anos, com "+brl0.format(r.projetado-r.necessario)+" de folga. Bastaria guardar "+brl.format(r.aporteNecessario)+" por mês nessas premissas, mas a folga ajuda se o rendimento vier menor.";
  }

  desenhar($("ap-graf"), p.idade, serie(p.patrimonio, p.aporte, p.taxa, r.meses), serie(p.patrimonio, r.aporteNecessario, p.taxa, r.meses), r.necessario);
}

["ap-idade","ap-alvo","ap-renda","ap-inss","ap-patrimonio","ap-aporte","ap-taxa","ap-retirada"].forEach(function(id){ $(id).addEventListener("input",calcular); });
var rt; window.addEventListener("resize",function(){ clearTimeout(rt); rt=setTimeout(calcular,120); });
calcular();
})();
