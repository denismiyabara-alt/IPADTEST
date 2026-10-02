/* Calculadora de JCP líquido · Investir e Coçar */
(function(){
"use strict";

/* ---------- Cálculos (funções puras, testadas em tests/calculos.test.js) ---------- */
var INICIO_2026="2026-01-01";
var LIMITE_DIVIDENDO=50000;

/* Alíquota do IR na fonte sobre JCP: 15% até 31/12/2025 (Lei 9.249/1995, art. 9º),
   17,5% para pagamento ou crédito a partir de 01/01/2026 (LC 224/2025). Data em "AAAA-MM-DD". */
function aliquotaJcp(dataISO){ return String(dataISO)<INICIO_2026 ? 0.15 : 0.175; }

function jcp(bruto, dataISO){
  var a=aliquotaJcp(dataISO), ir=bruto*a;
  return {bruto:bruto, aliquota:a, ir:ir, liquido:bruto-ir};
}

/* Dividendo do mesmo valor pago por uma empresa a uma pessoa física num mês.
   Até 2025: isento. A partir de 01/01/2026 (Lei 15.270/2025): isento até R$ 50 mil no mês;
   acima disso, 10% retidos sobre o total do mês. */
function dividendo(totalMes, dataISO){
  var a = (String(dataISO)>=INICIO_2026 && totalMes>LIMITE_DIVIDENDO) ? 0.10 : 0;
  var ir=totalMes*a;
  return {bruto:totalMes, aliquota:a, ir:ir, liquido:totalMes-ir};
}

var CALC={aliquotaJcp:aliquotaJcp, jcp:jcp, dividendo:dividendo};
if (typeof document==="undefined"){ if (typeof module==="object" && module && module.exports) module.exports=CALC; return; }

/* ---------- Tela ---------- */
var RAIZ = document.getElementById("jcp-liquido");
if (!RAIZ) return;

function $(id){ return document.getElementById(id); }
function num(id){ var v=parseFloat(String($(id).value).replace(",", ".")); return isFinite(v)?v:NaN; }
var brl=new Intl.NumberFormat("pt-BR",{style:"currency",currency:"BRL"});
var brl4=new Intl.NumberFormat("pt-BR",{style:"currency",currency:"BRL",minimumFractionDigits:2,maximumFractionDigits:4});
var nf1=new Intl.NumberFormat("pt-BR",{maximumFractionDigits:1});

function hojeISO(){
  var d=new Date(), m=d.getMonth()+1, dia=d.getDate();
  return d.getFullYear()+"-"+(m<10?"0":"")+m+"-"+(dia<10?"0":"")+dia;
}
if (!$("jcp-data").value) $("jcp-data").value=hojeISO();

function forma(){ var r=RAIZ.querySelector('input[name="jcp-forma"]:checked'); return r ? r.value : "acao"; }

function calcular(){
  var porAcao=forma()==="acao";
  $("jcp-campos-acao").hidden=!porAcao; $("jcp-campos-total").hidden=porAcao;
  var vAcao=num("jcp-por-acao"), qtd=num("jcp-qtd"), total=num("jcp-total"), data=$("jcp-data").value;
  var msg="";
  if (porAcao && (!isFinite(vAcao) || !isFinite(qtd))) msg="Preencha o valor por ação e a quantidade.";
  else if (porAcao && (vAcao<=0 || qtd<1 || Math.round(qtd)!==qtd)) msg="Use um valor por ação maior que zero e uma quantidade inteira de ações.";
  else if (!porAcao && (!isFinite(total) || total<=0)) msg="Coloque um valor total maior que zero.";
  else if (!/^\d{4}-\d{2}-\d{2}$/.test(data)) msg="Escolha a data do crédito ou do pagamento.";
  $("jcp-err").hidden=!msg; $("jcp-err").textContent=msg;
  if (msg){
    ["jcp-liq","jcp-bruto","jcp-ir","jcp-div","jcp-dif"].forEach(function(id){ $(id).textContent="—"; });
    $("jcp-label").textContent=""; $("jcp-liq-acao").textContent=""; $("jcp-story").hidden=true;
    return;
  }
  $("jcp-story").hidden=false;

  var bruto=porAcao ? vAcao*qtd : total, j=jcp(bruto, data), d=dividendo(bruto, data), dif=d.liquido-j.liquido;
  var antes=data<INICIO_2026;
  $("jcp-label").textContent="Cai na sua conta, depois do IR de "+nf1.format(j.aliquota*100)+"%";
  $("jcp-liq").textContent=brl.format(j.liquido);
  $("jcp-liq-acao").textContent = porAcao ? "São "+brl4.format(vAcao*(1-j.aliquota))+" líquidos por ação, para "+brl4.format(vAcao)+" brutos." : "";
  $("jcp-bruto").textContent=brl.format(j.bruto);
  $("jcp-ir-k").textContent="IR retido ("+nf1.format(j.aliquota*100)+"%)";
  $("jcp-ir").textContent="−"+brl.format(j.ir);
  $("jcp-div").textContent=brl.format(d.liquido);
  $("jcp-dif").textContent=brl.format(dif);

  var s=$("jcp-story");
  if (d.aliquota>0){
    s.textContent="Como passa de R$ 50 mil no mês, um dividendo desse valor também teria 10% retidos ("+brl.format(d.ir)+"), mas ainda sobraria "+brl.format(dif)+" a mais do que no JCP. Os 10% do dividendo são antecipação e entram no ajuste da declaração anual.";
  } else {
    s.textContent="Um dividendo do mesmo valor chegaria inteiro: "+brl.format(d.liquido)+". O JCP deixa "+brl.format(j.ir)+" com a Receita"+
      (antes ? ", pela alíquota de 15% que valia até 31/12/2025." : ". Antes de 2026, com a alíquota de 15%, a retenção seria de "+brl.format(bruto*0.15)+".");
  }
}

RAIZ.querySelectorAll('input[name="jcp-forma"]').forEach(function(r){ r.addEventListener("change",calcular); });
["jcp-por-acao","jcp-qtd","jcp-total","jcp-data"].forEach(function(id){
  $(id).addEventListener("input",calcular);
  $(id).addEventListener("change",calcular);
});
calcular();
})();
