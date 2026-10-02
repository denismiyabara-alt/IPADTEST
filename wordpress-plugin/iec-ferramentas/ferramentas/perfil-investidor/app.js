/* Quiz de perfil de investidor · Investir e Coçar */
(function(){
"use strict";

var RAIZ = document.getElementById("perfil-inv");
if (!RAIZ) return;

function $(id){ return document.getElementById(id); }
var TOTAL = 7;

var PERFIS = {
  conservador: {
    nome: "Conservador",
    texto: "Você prioriza segurança e acesso ao dinheiro. Oscilação tira o seu sono, e tudo bem: o primeiro passo costuma ser uma reserva de emergência sólida em renda fixa com liquidez diária, antes de pensar em bolsa.",
    links: [["/o-que-e-tesouro-selic/","O que é Tesouro Selic"],["/o-que-e-cdb/","O que é CDB"],["/o-que-e-fgc/","O que é o FGC"]]
  },
  moderado: {
    nome: "Moderado",
    texto: "Você aceita algum sobe e desce em troca de ganhar da inflação. Perfis assim costumam manter a maior parte em renda fixa e reservar uma fatia menor para renda variável, como fundos imobiliários e ETFs, aumentando aos poucos conforme aprendem.",
    links: [["/o-que-e-tesouro-ipca/","O que é Tesouro IPCA+"],["/o-que-e-fii/","O que é FII"],["/o-que-e-etf/","O que é ETF"]]
  },
  arrojado: {
    nome: "Arrojado",
    texto: "Você tem prazo longo, folga no orçamento e estômago para quedas fortes. Perfis assim costumam ter uma fatia maior em ações, FIIs e ETFs, sem abrir mão de uma reserva de emergência em renda fixa.",
    links: [["/o-que-e-acao-on-pn/","Ações ON e PN"],["/o-que-e-pl-acoes/","O que é P/L"],["/o-que-e-ifix/","O que é IFIX"]]
  }
};

function esc(t){ return String(t).replace(/[&<>"]/g,function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); }

function calcular(){
  var pontos=0, respondidas=0, resp={};
  for (var i=1; i<=TOTAL; i++){
    var marcada=RAIZ.querySelector('input[name="p-q'+i+'"]:checked');
    if (marcada){ respondidas++; pontos+=Number(marcada.value); resp[i]=Number(marcada.value); }
  }
  $("p-progresso").textContent=respondidas+" de "+TOTAL+" respondidas";
  if (respondidas<TOTAL){
    $("p-label").textContent="Responda as 7 perguntas para ver o resultado.";
    $("p-perfil").textContent="—";
    $("p-texto").hidden=true; $("p-alerta").hidden=true; $("p-guia").hidden=true;
    return;
  }
  var chave = pontos<=11 ? "conservador" : pontos<=16 ? "moderado" : "arrojado", p=PERFIS[chave];
  $("p-label").textContent="Seu perfil, com "+pontos+" de 21 pontos:";
  $("p-perfil").textContent=p.nome;
  $("p-perfil").className="big pos";
  $("p-texto").textContent=p.texto; $("p-texto").hidden=false;

  var alerta="";
  if (resp[2]===1) alerta="Atenção: você ainda não tem reserva de emergência. Antes de buscar rentabilidade, monte essa reserva em algo seguro e com resgate rápido.";
  else if (resp[1]===1 && chave!=="conservador") alerta="Atenção: você vai precisar do dinheiro em até 1 ano. Para esse prazo, oscilação pode virar prejuízo na hora de resgatar, qualquer que seja o seu perfil.";
  $("p-alerta").textContent=alerta; $("p-alerta").hidden=!alerta;

  $("p-links").innerHTML=p.links.map(function(l){ return '<li><a href="'+esc(l[0])+'">'+esc(l[1])+'</a></li>'; }).join("");
  $("p-guia").hidden=false;
}

RAIZ.addEventListener("change", function(e){ if (e.target && e.target.type==="radio") calcular(); });
calcular();
})();
