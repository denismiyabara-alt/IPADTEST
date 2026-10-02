/* Simulador de marcação a mercado NTN-B · Investir e Coçar */
(function(){
"use strict";

var RAIZ = document.getElementById("sim-ntnb");
if (!RAIZ) return;

/* ---------- Datas e dias úteis ---------- */
var DAY = 86400000;
function dnum(y,m,d){ return Math.round(Date.UTC(y,m-1,d)/DAY); }
function parts(n){ var t=new Date(n*DAY); return {y:t.getUTCFullYear(), m:t.getUTCMonth()+1, d:t.getUTCDate()}; }
function parseISO(s){ if(!s) return null; var p=s.split("-").map(Number); if(p.length!==3||p.some(isNaN)) return null; return dnum(p[0],p[1],p[2]); }
function toISO(n){ var p=parts(n); return p.y+"-"+String(p.m).padStart(2,"0")+"-"+String(p.d).padStart(2,"0"); }
function fmtDate(n){ var p=parts(n); return String(p.d).padStart(2,"0")+"/"+String(p.m).padStart(2,"0")+"/"+p.y; }
function addMonths(n,k){ var p=parts(n); var m=p.m-1+k; var y=p.y+Math.floor(m/12); m=((m%12)+12)%12; return dnum(y,m+1,p.d); }

function easter(y){
  var a=y%19,b=Math.floor(y/100),c=y%100,d=Math.floor(b/4),e=b%4,f=Math.floor((b+8)/25),
      g=Math.floor((b-f+1)/3),h=(19*a+b-d-g+15)%30,i=Math.floor(c/4),k=c%4,
      l=(32+2*e+2*i-h-k)%7,m=Math.floor((a+11*h+22*l)/451),
      mo=Math.floor((h+l-7*m+114)/31),da=((h+l-7*m+114)%31)+1;
  return dnum(y,mo,da);
}

var Y0=1999, Y1=2080, START=dnum(Y0,1,1), END=dnum(Y1,1,1);
var holidays = new Set();
for (var y=Y0; y<Y1; y++){
  [[1,1],[4,21],[5,1],[9,7],[10,12],[11,2],[11,15],[12,25]].forEach(function(md){ holidays.add(dnum(y,md[0],md[1])); });
  /* Consciência Negra: feriado nacional desde 2024 */
  if (y>=2024) holidays.add(dnum(y,11,20));
  var e=easter(y);
  /* Carnaval (segunda e terça), Sexta-feira Santa e Corpus Christi */
  holidays.add(e-48);
  holidays.add(e-47);
  holidays.add(e-2);
  holidays.add(e+60);
}
function isBD(n){ var w=((n+4)%7+7)%7; return w!==0 && w!==6 && !holidays.has(n); }
var cum = new Int32Array(END-START+1);
for (var i=0;i<END-START;i++) cum[i+1]=cum[i]+(isBD(START+i)?1:0);
function inRange(n){ return n>=START && n<END; }
function du(a,b){ return cum[b-START]-cum[a-START]; }
function nextBD(n){ while(!isBD(n)) n++; return n; }

/* ---------- Títulos ---------- */
var TITULOS = [
  {id:"b27", nome:"IPCA+ com Juros Semestrais 2027", venc:"2027-05-15", cupom:true},
  {id:"b28", nome:"IPCA+ com Juros Semestrais 2028", venc:"2028-08-15", cupom:true},
  {id:"b29", nome:"IPCA+ com Juros Semestrais 2029", venc:"2029-05-15", cupom:true},
  {id:"b30", nome:"IPCA+ com Juros Semestrais 2030", venc:"2030-08-15", cupom:true},
  {id:"b32", nome:"IPCA+ com Juros Semestrais 2032", venc:"2032-08-15", cupom:true},
  {id:"b33", nome:"IPCA+ com Juros Semestrais 2033", venc:"2033-05-15", cupom:true},
  {id:"b35", nome:"IPCA+ com Juros Semestrais 2035", venc:"2035-05-15", cupom:true},
  {id:"b40", nome:"IPCA+ com Juros Semestrais 2040", venc:"2040-08-15", cupom:true},
  {id:"b45", nome:"IPCA+ com Juros Semestrais 2045", venc:"2045-05-15", cupom:true},
  {id:"b50", nome:"IPCA+ com Juros Semestrais 2050", venc:"2050-08-15", cupom:true},
  {id:"b55", nome:"IPCA+ com Juros Semestrais 2055", venc:"2055-05-15", cupom:true},
  {id:"b60", nome:"IPCA+ com Juros Semestrais 2060", venc:"2060-08-15", cupom:true},
  {id:"p29", nome:"IPCA+ 2029 (sem cupom)", venc:"2029-05-15", cupom:false},
  {id:"p35", nome:"IPCA+ 2035 (sem cupom)", venc:"2035-05-15", cupom:false},
  {id:"p45", nome:"IPCA+ 2045 (sem cupom)", venc:"2045-05-15", cupom:false}
];
TITULOS.forEach(function(t){ t.vencN=parseISO(t.venc); t.curto=(t.cupom?"NTN-B ":"Principal ")+t.venc.slice(0,4); });

/* Cupom semestral: (1,06^0,5 − 1) × 100 */
var CUPOM = 2.956301;

/* ---------- Precificação ---------- */
/* Fluxos (em % do VNA) com data de pagamento posterior à liquidação */
function fluxos(settle, venc, cupom){
  var out=[];
  if (!cupom){ out.push({data:nextBD(venc), valor:100}); return out; }
  var d=venc, first=true;
  while (true){
    var pag=nextBD(d);
    if (pag<=settle) break;
    out.push({data:pag, valor: first ? 100+CUPOM : CUPOM, cupom:true});
    first=false;
    d=addMonths(d,-6);
  }
  return out.reverse();
}
function cotacao(settle, venc, cupom, taxa, truncar){
  var y=taxa/100, s=0;
  fluxos(settle,venc,cupom).forEach(function(f){ s+=f.valor/Math.pow(1+y, du(settle,f.data)/252); });
  return truncar ? Math.floor(s*1e4)/1e4 : s;
}
function duration(settle, venc, cupom, taxa){
  var y=taxa/100, pv=0, tpv=0;
  fluxos(settle,venc,cupom).forEach(function(f){
    var t=du(settle,f.data)/252, v=f.valor/Math.pow(1+y,t); pv+=v; tpv+=t*v;
  });
  var mac=tpv/pv; return {mac:mac, mod:mac/(1+y)};
}

/* ---------- Formatação ---------- */
var nf2=new Intl.NumberFormat("pt-BR",{minimumFractionDigits:2,maximumFractionDigits:2});
var brl=new Intl.NumberFormat("pt-BR",{style:"currency",currency:"BRL"});
function pct(x,sinal){ var s=nf2.format(x*100)+"%"; return (sinal && x>0?"+":"")+s; }
function pp(x){ return (x>0?"+":"")+nf2.format(x)+" p.p."; }
function cls(el,x){ el.classList.toggle("neg",x<0); el.classList.toggle("pos",x>0); }
function $(id){ return document.getElementById(id); }
function num(id){ var v=parseFloat(String($(id).value).replace(",", ".")); return isFinite(v)?v:NaN; }

/* ---------- Selects ---------- */
function preencher(sel, padrao){
  var html = TITULOS.map(function(t){ return '<option value="'+t.id+'"'+(t.id===padrao?" selected":"")+'>'+t.nome+'</option>'; }).join("");
  html += '<option value="custom">Outro vencimento…</option>';
  $(sel).innerHTML = html;
}
function tituloSel(prefix){
  var id=$(prefix+"-titulo").value;
  $(prefix+"-custom").hidden = id!=="custom";
  if (id!=="custom"){ var t=TITULOS.filter(function(x){return x.id===id;})[0]; return {vencN:t.vencN, cupom:t.cupom, nome:t.nome}; }
  var v=parseISO($(prefix+"-venc").value), c=$(prefix+"-tipo").value==="1";
  return {vencN:v, cupom:c, nome:"Título "+(c?"com":"sem")+" cupom "+(v?fmtDate(v):"")};
}

/* ---------- Hoje ---------- */
var hj=new Date(); var HOJE=dnum(hj.getFullYear(),hj.getMonth()+1,hj.getDate());

/* ---------- Gráficos SVG ---------- */
var NS="http://www.w3.org/2000/svg";
function el(tag, attrs, txt){ var e=document.createElementNS(NS,tag); for (var k in attrs) e.setAttribute(k,attrs[k]); if (txt!=null) e.textContent=txt; return e; }
function css(v){ return getComputedStyle(RAIZ).getPropertyValue(v).trim(); }

function larg(svg){ return Math.max(320, Math.round(svg.parentNode.clientWidth-36)); }
function desenharCurva(svg, pontos, marcador){
  svg.innerHTML="";
  var W=larg(svg),H=Math.round(Math.min(300,W*0.62)),L=46,R=14,T=16,B=32;
  svg.setAttribute("viewBox","0 0 "+W+" "+H);
  var xs=pontos.map(function(p){return p[0];}), ys=pontos.map(function(p){return p[1];});
  var x0=Math.min.apply(null,xs), x1=Math.max.apply(null,xs);
  var ymax=Math.max.apply(null,ys.map(Math.abs)); ymax=Math.max(ymax,0.01);
  var passos=[0.01,0.02,0.05,0.1,0.2], passo=passos[passos.length-1];
  for (var q=0;q<passos.length;q++){ if (Math.ceil(ymax/passos[q])*2<=8){ passo=passos[q]; break; } }
  ymax=Math.ceil(ymax/passo)*passo;
  function X(v){ return L+(v-x0)/(x1-x0)*(W-L-R); }
  function Y(v){ return T+(ymax-v)/(2*ymax)*(H-T-B); }
  for (var v=-ymax; v<=ymax+1e-9; v+=passo){
    svg.appendChild(el("line",{x1:L,x2:W-R,y1:Y(v),y2:Y(v),stroke:css(Math.abs(v)<1e-9?"--axis":"--grid"),"stroke-width":1}));
    svg.appendChild(el("text",{x:L-8,y:Y(v)+4,"text-anchor":"end"},(v>1e-9?"+":"")+Math.round(v*100)+"%"));
  }
  var px=W<480?2:1;
  for (var t=Math.ceil(x0); t<=x1; t++){
    if (t%px) continue;
    svg.appendChild(el("line",{x1:X(t),x2:X(t),y1:T,y2:H-B,stroke:css(t===0?"--axis":"--grid"),"stroke-width":1}));
    svg.appendChild(el("text",{x:X(t),y:H-B+18,"text-anchor":"middle"},(t>0?"+":"")+t+(W<480?"":" p.p.")));
  }
  var d=pontos.map(function(p,i){ return (i?"L":"M")+X(p[0]).toFixed(1)+" "+Y(p[1]).toFixed(1); }).join(" ");
  svg.appendChild(el("path",{d:d,fill:"none",stroke:css("--accent"),"stroke-width":2.5,"stroke-linejoin":"round"}));
  if (marcador){
    var mx=X(marcador[0]), my=Y(marcador[1]);
    svg.appendChild(el("line",{x1:mx,x2:mx,y1:my,y2:Y(0),stroke:css("--muted"),"stroke-dasharray":"3 3"}));
    svg.appendChild(el("circle",{cx:mx,cy:my,r:6,fill:css(marcador[1]<0?"--neg":"--pos"),stroke:css("--surface"),"stroke-width":2}));
    var lbl=el("text",{x:mx+(mx>W/2?-10:10),y:marcador[1]<0?my+22:my-12,"text-anchor":mx>W/2?"end":"start","font-weight":"700"},pct(marcador[1],true));
    lbl.style.fill=css("--text"); svg.appendChild(lbl);
  }
}

function desenharBarras(svg, itens){
  svg.innerHTML="";
  var W=larg(svg),L=112,R=58,T=4,linha=24,H=T+itens.length*linha+4;
  svg.setAttribute("viewBox","0 0 "+W+" "+H);
  var vmax=Math.max.apply(null,itens.map(function(i){return Math.abs(i.v);}))||1;
  itens.forEach(function(it,k){
    var y=T+k*linha, w=Math.abs(it.v)/vmax*(W-L-R);
    var t1=el("text",{x:L-8,y:y+linha/2+4,"text-anchor":"end"},it.label); svg.appendChild(t1);
    svg.appendChild(el("rect",{x:L,y:y+4,width:Math.max(w,1),height:linha-8,rx:3,fill:css(it.destaque?(it.v<0?"--neg":"--pos"):"--axis"),opacity:it.destaque?1:.55}));
    var t2=el("text",{x:L+w+6,y:y+linha/2+4,"font-weight":it.destaque?"700":"400"},pct(it.v,true));
    if (it.destaque) t2.style.fill=css("--text");
    svg.appendChild(t2);
  });
}

/* ---------- Aba 1 ---------- */
function calcChoque(){
  var t=tituloSel("c"), taxa=num("c-taxa"), dy=num("c-choque");
  $("c-choque-val").textContent=pp(dy);
  var settle=nextBD(HOJE);
  if (!t.vencN || !inRange(t.vencN) || t.vencN<=settle || !isFinite(taxa) || taxa<=-50){
    $("c-var").textContent="—"; $("c-story").textContent="Confira o vencimento e a taxa."; return;
  }
  var c0=cotacao(settle,t.vencN,t.cupom,taxa,false), c1=cotacao(settle,t.vencN,t.cupom,taxa+dy,false);
  var v=c1/c0-1, dur=duration(settle,t.vencN,t.cupom,taxa);
  var v1=cotacao(settle,t.vencN,t.cupom,taxa+1,false)/c0-1;
  $("c-label").textContent="Variação no preço do "+t.nome+" se a taxa for de "+nf2.format(taxa)+"% para "+nf2.format(taxa+dy)+"%";
  $("c-var").textContent=pct(v,true); cls($("c-var"),v);
  $("c-cot0").textContent=nf2.format(Math.floor(c0*1e4)/1e4)+"%";
  $("c-cot1").textContent=nf2.format(Math.floor(c1*1e4)/1e4)+"%";
  $("c-dur").textContent=nf2.format(dur.mac)+" anos";
  $("c-dv").textContent=pct(v1,true);
  var s=$("c-story");
  if (Math.abs(dy)<1e-9){ s.className="story"; s.textContent="Taxa parada, preço parado. Mexe no controle pra ver o estrago (ou a festa)."; }
  else if (dy>0){ s.className="story bad"; s.textContent="A taxa subiu "+nf2.format(dy)+" p.p. e o seu título perdeu "+pct(-v)+" de valor na hora. Se você levar até o vencimento, essa perda some. Se precisar vender agora, ela vira realidade."; }
  else { s.className="story"; s.textContent="A taxa caiu "+nf2.format(-dy)+" p.p. e o seu título valorizou "+pct(v)+". Quem vender agora embolsa um ganho acima do que foi contratado."; }

  var pts=[]; for (var x=-3; x<=3.0001; x+=0.1){ pts.push([x, cotacao(settle,t.vencN,t.cupom,taxa+x,false)/c0-1]); }
  desenharCurva($("c-curve"), pts, [dy, v]);

  var choque = Math.abs(dy)<1e-9 ? 1 : dy;
  $("c-bars-title").textContent="Se a taxa "+(choque>0?"subir ":"cair ")+nf2.format(Math.abs(choque))+" p.p., quanto cada título "+(choque>0?"cai":"sobe")+"?";
  var sel=$("c-titulo").value;
  var itens=TITULOS.filter(function(x){return x.vencN>settle;}).map(function(x){
    var a=cotacao(settle,x.vencN,x.cupom,taxa,false), b=cotacao(settle,x.vencN,x.cupom,taxa+choque,false);
    return {label:x.curto, v:b/a-1, destaque:x.id===sel};
  });
  desenharBarras($("c-bars"), itens);
}

/* ---------- Aba 2 ---------- */
function resultado(t, s0, s1, tc, tv, ipca, valor){
  var vna=function(n){ return 1000*Math.pow(1+ipca/100, du(s0,n)/252); };
  var pu0=1000*cotacao(s0,t.vencN,t.cupom,tc,true)/100;
  var pu1=vna(s1)*cotacao(s1,t.vencN,t.cupom,tv,true)/100;
  var qtd=valor/pu0, cupons=0, caixa=[];
  if (t.cupom) fluxos(s0,t.vencN,true).forEach(function(f){
    if (f.data>s0 && f.data<=s1){ var c=qtd*vna(f.data)*CUPOM/100; cupons+=c; caixa.push([du(s0,f.data)/252, c]); }
  });
  var venda=qtd*pu1, total=venda+cupons, ret=total/valor-1, anos=du(s0,s1)/252;
  caixa.push([anos, venda]);
  /* TIR (base 252): considera quando cada cupom entrou no bolso */
  function vpl(i){ return caixa.reduce(function(s,f){ return s+f[1]/Math.pow(1+i,f[0]); },0)-valor; }
  var lo=-0.99, hi=10;
  for (var k=0;k<200;k++){ var mid=(lo+hi)/2; if (vpl(mid)>0) lo=mid; else hi=mid; }
  var aa=(lo+hi)/2, realAA=(1+aa)/(1+ipca/100)-1;
  return {venda:venda, cupons:cupons, total:total, ganho:total-valor, ret:ret, aa:aa, realAA:realAA, anos:anos};
}
function calcOperacao(){
  var t=tituloSel("o"), valor=num("o-valor"), tc=num("o-tc"), tv=num("o-tv"), ipca=num("o-ipca");
  var dc=parseISO($("o-dc").value), dv=parseISO($("o-dv").value), err=$("o-err");
  var msg="";
  if (!t.vencN || !inRange(t.vencN)) msg="Escolha um vencimento válido.";
  else if (!dc || !dv || !inRange(dc) || !inRange(dv)) msg="Preencha as datas de compra e venda.";
  else if (nextBD(dv)<=nextBD(dc)) msg="A venda precisa ser depois da compra.";
  else if (nextBD(dv)>=nextBD(t.vencN)) msg="A venda precisa ser antes do vencimento. No vencimento não tem marcação a mercado: você recebe IPCA + a taxa contratada.";
  else if (![valor,tc,tv,ipca].every(isFinite) || valor<=0) msg="Confira os números digitados.";
  err.hidden=!msg; err.textContent=msg;
  if (msg){ ["o-res","o-venda","o-cupons","o-aa","o-real"].forEach(function(id){ $(id).textContent="—"; }); $("o-res-pct").textContent=""; $("o-story").hidden=true; $("o-table").innerHTML=""; return; }
  $("o-story").hidden=false;

  var s0=nextBD(dc), s1=nextBD(dv);
  var r=resultado(t,s0,s1,tc,tv,ipca,valor);
  var base=resultado(t,s0,s1,tc,tc,ipca,valor);
  var efeito=r.total-base.total;

  $("o-res").textContent=(r.ganho>0?"+":"")+brl.format(r.ganho); cls($("o-res"),r.ganho);
  $("o-res-pct").textContent=pct(r.ret,true)+" em "+nf2.format(r.anos)+" anos · total bruto de "+brl.format(r.total);
  $("o-venda").textContent=brl.format(r.venda);
  $("o-cupons").textContent=t.cupom?brl.format(r.cupons):"Sem cupom";
  $("o-aa").textContent=pct(r.aa,true);
  $("o-real").textContent="IPCA "+(r.realAA>=0?"+ ":"− ")+nf2.format(Math.abs(r.realAA*100))+"%";

  var s=$("o-story"), dtx=tv-tc;
  var intro="Você comprou a IPCA + "+nf2.format(tc)+"% e vendeu com o mercado pagando IPCA + "+nf2.format(tv)+"%. ";
  if (Math.abs(dtx)<1e-9){ s.className="story"; s.textContent=intro+"Taxa igual, sem efeito de marcação: sua rentabilidade real ficou perto do contratado."; }
  else if (dtx>0){ s.className="story bad"; s.textContent=intro+"Como a taxa subiu, seu título ficou menos atraente e você vendeu com desconto. A marcação a mercado te custou "+brl.format(-efeito)+" em relação a vender na mesma taxa da compra."+(r.ganho<0?" Resultado: prejuízo nominal num título do governo.":""); }
  else { s.className="story"; s.textContent=intro+"Como a taxa caiu, seu título ficou mais disputado e você vendeu com ágio. A marcação a mercado te deu "+brl.format(efeito)+" a mais do que vender na mesma taxa da compra."; }

  function linha(nome, x, forte){
    var c=x.ganho<0?"neg":"pos";
    return "<tr"+(forte?' style="font-weight:700"':"")+"><td>"+nome+'</td><td class="'+c+'">'+(x.ganho>0?"+":"")+brl.format(x.ganho)+"</td><td>"+pct(x.realAA,true)+"</td></tr>";
  }
  $("o-table").innerHTML =
    linha("Sua operação (taxa "+nf2.format(tv)+"%)", r, true) +
    linha("Se a taxa não mudasse ("+nf2.format(tc)+"%)", base, false) +
    '<tr><td>Efeito da marcação a mercado</td><td class="'+(efeito<0?"neg":"pos")+'">'+(efeito>0?"+":"")+brl.format(efeito)+"</td><td></td></tr>";
}

/* ---------- Inicialização ---------- */
preencher("c-titulo","b35"); preencher("o-titulo","b35");
$("c-venc").value="2040-08-15"; $("o-venc").value="2040-08-15";
$("o-dc").value=toISO(addMonths(HOJE,-24)); $("o-dv").value=toISO(HOJE);

RAIZ.querySelectorAll(".tab").forEach(function(b){
  b.addEventListener("click",function(){
    RAIZ.querySelectorAll(".tab").forEach(function(x){ x.setAttribute("aria-selected", x===b?"true":"false"); });
    RAIZ.querySelectorAll(".panel").forEach(function(p){ p.classList.toggle("active", p.id==="panel-"+b.dataset.tab); });
    if (b.dataset.tab==="choque") calcChoque(); else calcOperacao();
  });
});
["c-titulo","c-venc","c-tipo","c-taxa","c-choque"].forEach(function(id){ $(id).addEventListener("input",calcChoque); });
["o-titulo","o-venc","o-tipo","o-valor","o-dc","o-tc","o-dv","o-tv","o-ipca"].forEach(function(id){ $(id).addEventListener("input",calcOperacao); });
var rt; window.addEventListener("resize",function(){ clearTimeout(rt); rt=setTimeout(calcChoque,120); });

calcChoque(); calcOperacao();

})();
