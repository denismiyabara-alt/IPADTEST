/* Simulador de renda mensal com FIIs · Investir e Coçar */
(function(){
"use strict";

var RAIZ = document.getElementById("renda-fii");
if (!RAIZ) return;

function $(id){ return document.getElementById(id); }
function num(id){ var v=parseFloat(String($(id).value).replace(",", ".")); return isFinite(v)?v:NaN; }

/* ---------- Formatação ---------- */
var brl=new Intl.NumberFormat("pt-BR",{style:"currency",currency:"BRL"});
var brl0=new Intl.NumberFormat("pt-BR",{style:"currency",currency:"BRL",maximumFractionDigits:0});
var nf1=new Intl.NumberFormat("pt-BR",{maximumFractionDigits:1});
var nf2=new Intl.NumberFormat("pt-BR",{minimumFractionDigits:2,maximumFractionDigits:2});
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

/* ---------- Simulação mês a mês ----------
   Rendimento do mês = patrimônio do mês anterior × DY. Aporte entra no fim do mês.
   Reinvestindo: rendimento volta para o patrimônio.
   Sem reinvestir: rendimento é sacado e só os aportes aumentam o patrimônio. */
function simular(inicial, dy, aporte, meses, inflacao){
  var pr=inicial, ps=inicial, sacado=0, sacadoHoje=0, investidoHoje=inicial, recebidoR=0, cruza=null;
  var serie=[{m:0, rendaR:inicial*dy, rendaS:inicial*dy, patR:pr, patS:ps, sacado:0, sacadoHoje:0, defl:1}];
  var deflMensal=Math.pow(1+inflacao, 1/12);
  for (var t=1; t<=meses; t++){
    var rr=pr*dy, rs=ps*dy;
    pr+=rr+aporte;
    ps+=aporte;
    sacado+=rs;
    sacadoHoje+=rs/Math.pow(deflMensal,t);
    investidoHoje+=aporte/Math.pow(deflMensal,t);
    recebidoR+=rr;
    if (cruza===null && aporte>0 && rr>=aporte) cruza=t;
    serie.push({m:t, rendaR:rr, rendaS:rs, patR:pr, patS:ps, sacado:sacado, sacadoHoje:sacadoHoje, defl:Math.pow(deflMensal,t)});
  }
  return {serie:serie, cruza:cruza, investido:inicial+aporte*meses, investidoHoje:investidoHoje, recebidoR:recebidoR};
}

/* ---------- Gráfico ---------- */
var NS="http://www.w3.org/2000/svg";
function el(tag, attrs, txt){ var e=document.createElementNS(NS,tag); for (var k in attrs) e.setAttribute(k,attrs[k]); if (txt!=null) e.textContent=txt; return e; }
function css(v){ return getComputedStyle(RAIZ).getPropertyValue(v).trim(); }
function larg(svg){ return Math.max(320, Math.round(svg.parentNode.clientWidth-36)); }
function passoBonito(max, alvo){
  var bruto=max/alvo, pot=Math.pow(10,Math.floor(Math.log10(bruto))), n=bruto/pot;
  return (n<=1?1:n<=2?2:n<=2.5?2.5:n<=5?5:10)*pot;
}

function desenhar(svg, serie, aporte, real){
  svg.innerHTML="";
  var W=larg(svg), H=Math.round(Math.min(320,W*0.6)), L=W<480?58:70, R=W<480?70:84, T=14, B=30;
  svg.setAttribute("viewBox","0 0 "+W+" "+H);
  var n=serie.length-1;
  function val(p,k){ return real ? p[k]/p.defl : p[k]; }
  var ymax=aporte;
  serie.forEach(function(p){ ymax=Math.max(ymax, val(p,"rendaR"), val(p,"rendaS")); });
  if (ymax<=0) ymax=1;
  var passo=passoBonito(ymax, 4); ymax=Math.ceil(ymax/passo)*passo;
  function X(m){ return L+m/n*(W-L-R); }
  function Y(v){ return T+(1-v/ymax)*(H-T-B); }

  for (var v=0; v<=ymax+1e-9; v+=passo){
    svg.appendChild(el("line",{x1:L,x2:W-R,y1:Y(v),y2:Y(v),stroke:css(v===0?"--axis":"--grid"),"stroke-width":1}));
    svg.appendChild(el("text",{x:L-8,y:Y(v)+4,"text-anchor":"end"},compacto(v)));
  }
  var anos=n/12, pAno=anos<=10?1:anos<=20?2:5;
  for (var a=0; a<=anos; a+=pAno){
    svg.appendChild(el("text",{x:X(a*12),y:H-B+18,"text-anchor":"middle"},a===0?"hoje":a+(W<480?"":(a===1?" ano":" anos"))));
  }

  if (aporte>0){
    var ya=Y(aporte);
    svg.appendChild(el("line",{x1:L,x2:W-R,y1:ya,y2:ya,stroke:css("--amber"),"stroke-width":1.5,"stroke-dasharray":"5 4"}));
  }

  function linha(k, cor, larguraTraco){
    var d=serie.map(function(p,i){ return (i?"L":"M")+X(p.m).toFixed(1)+" "+Y(val(p,k)).toFixed(1); }).join(" ");
    svg.appendChild(el("path",{d:d,fill:"none",stroke:cor,"stroke-width":larguraTraco,"stroke-linejoin":"round"}));
    var u=serie[n], x=X(u.m), y=Y(val(u,k));
    svg.appendChild(el("circle",{cx:x,cy:y,r:4.5,fill:cor,stroke:css("--surface"),"stroke-width":2}));
    return {x:x,y:y,v:val(u,k),cor:cor};
  }
  var fimS=linha("rendaS", css("--serie2"), 2);
  var fimR=linha("rendaR", css("--accent"), 2.75);

  var yR=fimR.y, yS=fimS.y;
  if (Math.abs(yR-yS)<16){ if (yR<=yS){ yS=yR+16; } else { yR=yS+16; } }
  [[fimR,yR],[fimS,yS]].forEach(function(par){
    var t=el("text",{x:par[0].x+8,y:par[1]+4,"font-weight":"700"},compacto(par[0].v));
    t.style.fill=css("--text"); svg.appendChild(t);
  });
}

/* ---------- Tela ---------- */
function calcular(){
  var inicial=num("f-inicial"), dyPct=num("f-dy"), aporte=num("f-aporte"), anos=num("f-anos"), infPct=num("f-inflacao");
  var real=$("f-real").checked, err=$("f-err"), msg="";
  if (![inicial,dyPct,aporte,anos,infPct].every(isFinite)) msg="Preencha todos os campos com números.";
  else if (inicial<0 || aporte<0) msg="Valor investido e aporte não podem ser negativos.";
  else if (inicial===0 && aporte===0) msg="Coloque algum valor inicial ou aporte mensal.";
  else if (dyPct<=0 || dyPct>5) msg="Use um dividend yield entre 0,01% e 5% ao mês.";
  else if (anos<1 || anos>30 || Math.round(anos)!==anos) msg="O prazo precisa ser um número inteiro de 1 a 30 anos.";
  else if (infPct<0 || infPct>30) msg="Use uma inflação entre 0% e 30% ao ano.";
  err.hidden=!msg; err.textContent=msg;
  if (msg){
    ["f-renda","f-renda-hoje","f-renda-sem","f-pat","f-investido","f-cruza"].forEach(function(id){ $(id).textContent="—"; });
    $("f-label").textContent=""; $("f-inf-nota").textContent=""; $("f-modo").textContent=""; $("f-story").hidden=true; $("f-tabela").innerHTML=""; $("f-graf").innerHTML="";
    return;
  }
  $("f-story").hidden=false;

  var meses=anos*12, dy=dyPct/100, inf=infPct/100;
  var r=simular(inicial, dy, aporte, meses, inf), u=r.serie[meses];

  var d=real?u.defl:1, sacadoFim=real?u.sacadoHoje:u.sacado;
  $("f-label").textContent="Renda do último mês, reinvestindo, depois de "+tempo(meses);
  $("f-renda").textContent=brl.format(u.rendaR);
  $("f-renda-hoje").textContent=brl.format(u.rendaR/u.defl);
  $("f-inf-nota").textContent="Dinheiro de hoje desconta inflação de "+nf1.format(infPct)+"% ao ano, acumulada até o último mês.";
  $("f-modo").textContent=real?"Detalhes em dinheiro de hoje":"Detalhes em valores nominais";
  $("f-renda-sem").textContent=brl.format(u.rendaS/d);
  $("f-pat").textContent=brl0.format(u.patR/d);
  $("f-investido").textContent=brl0.format(real?r.investidoHoje:r.investido);
  $("f-cruza").textContent = aporte<=0 ? "Sem aporte" : (r.cruza===null ? "Não chega no prazo" : tempo(r.cruza));

  var mult=u.rendaS>0 ? u.rendaR/u.rendaS : 0, s=$("f-story"), em=real?" (em dinheiro de hoje)":" (valores nominais)";
  s.textContent="Reinvestindo, a renda chega a "+brl.format(u.rendaR/d)+" por mês, "+nf2.format(mult)+" vezes os "+brl.format(u.rendaS/d)+" de quem gastou tudo"+em+". "+
    "Quem gastou recebeu "+brl0.format(sacadoFim)+" ao longo do caminho; quem reinvestiu terminou com "+brl0.format((u.patR-u.patS)/d)+" a mais de patrimônio"+em+". "+
    (r.cruza===null ? (aporte>0 ? "No prazo escolhido, a renda ainda não passa o aporte." : "") : "A partir de "+tempo(r.cruza)+", o fundo põe na sua carteira mais do que você.");

  $("f-graf-titulo").textContent="Renda mensal ao longo do tempo"+(real?" (dinheiro de hoje)":" (nominal)");
  $("f-tab-titulo").textContent="Ano a ano"+(real?" (dinheiro de hoje)":" (nominal)");
  desenhar($("f-graf"), r.serie, aporte, real);

  var linhas="";
  for (var a=1; a<=anos; a++){
    var p=r.serie[a*12], d=real?p.defl:1;
    linhas+="<tr><td>"+a+"</td><td>"+brl.format(p.rendaR/d)+"</td><td>"+brl.format(p.rendaS/d)+"</td><td>"+brl0.format(p.patR/d)+"</td><td>"+brl0.format(real?p.sacadoHoje:p.sacado)+"</td></tr>";
  }
  $("f-tabela").innerHTML=linhas;
}

["f-inicial","f-dy","f-aporte","f-anos","f-inflacao","f-real"].forEach(function(id){
  $(id).addEventListener("input",calcular);
  $(id).addEventListener("change",calcular);
});
var rt; window.addEventListener("resize",function(){ clearTimeout(rt); rt=setTimeout(calcular,120); });
calcular();
})();
