/* Quiz de perfil de investidor · Investir e Coçar */
(function(){
"use strict";

var RAIZ = document.getElementById("perfil-inv");
if (!RAIZ) return;

function $(id){ return document.getElementById(id); }
var TOTAL = 7;

var PERFIS = {
  conservador: {
    nome: "Bunda na parede",
    texto: "Tanaka, você entra na bolsa igual banheiro de rodoviária: de costas pra parede e já procurando a saída. Tesouro Selic, CDB de banco grande e olhe lá. Dorme tranquilo. A inflação também, comendo seu dinheiro devagarinho enquanto você ronca.",
    links: [["/o-que-e-tesouro-selic/","O que é Tesouro Selic"],["/o-que-e-cdb/","O que é CDB"],["/o-que-e-fgc/","O que é o FGC"]]
  },
  moderado: {
    nome: "Bundão",
    texto: "Você até comprou FII. Caiu 3% e no mesmo dia você mandou print no grupo da família perguntando se era golpe. Coragem pra entrar você tem. Pra ficar, ainda não.",
    links: [["/o-que-e-tesouro-ipca/","O que é Tesouro IPCA+"],["/o-que-e-fii/","O que é FII"],["/o-que-e-etf/","O que é ETF"]]
  },
  arrojado: {
    nome: "Furico aberto",
    texto: "Ibovespa caiu 30%, você aportou. Caiu mais 10%, você aportou de novo e ainda chamou de promoção. Ou você é gênio, ou é o Tanacão mais sem noção da B3. Seu extrato daqui a 10 anos vai contar qual dos dois.",
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
    $("p-texto").hidden=true; $("p-alerta").hidden=true; $("p-guia").hidden=true; $("p-lead").hidden=true;
    return;
  }
  var chave = pontos<=11 ? "conservador" : pontos<=16 ? "moderado" : "arrojado", p=PERFIS[chave];
  $("p-label").textContent="Seu nível de cagaço, com "+pontos+" de 21 pontos:";
  $("p-perfil").textContent=p.nome;
  $("p-perfil").className="big pos";
  $("p-texto").textContent=p.texto; $("p-texto").hidden=false;

  var alerta="";
  if (resp[2]===1) alerta="Atenção: você ainda não tem reserva de emergência. Antes de buscar rentabilidade, monte essa reserva em algo seguro e com resgate rápido.";
  else if (resp[1]===1 && chave!=="conservador") alerta="Atenção: você vai precisar do dinheiro em até 1 ano. Para esse prazo, oscilação pode virar prejuízo na hora de resgatar, qualquer que seja o seu perfil.";
  $("p-alerta").textContent=alerta; $("p-alerta").hidden=!alerta;

  $("p-links").innerHTML=p.links.map(function(l){ return '<li><a href="'+esc(l[0])+'">'+esc(l[1])+'</a></li>'; }).join("");
  $("p-guia").hidden=false;
  $("p-perfil-campo").value=p.nome; $("p-lead-nome").textContent=p.nome; $("p-lead").hidden=false;
}

// ponytail: POST no-cors direto no formulário do Brevo; não dá pra ler a resposta, então confia no envio.
$("p-form").addEventListener("submit", function(e){
  e.preventDefault();
  var email=$("p-email"), msg=$("p-lead-msg");
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())){
    msg.textContent="Confere o e-mail: parece que faltou alguma coisa."; msg.className="fine neg"; msg.hidden=false; return;
  }
  $("p-enviar").disabled=true;
  fetch(this.action, { method:"POST", mode:"no-cors", body:new FormData(this) })
    .then(function(){ msg.textContent="Feito. Confere a sua caixa de entrada (e o spam, vai que)."; msg.className="fine pos"; $("p-form").hidden=true; })
    .catch(function(){ msg.textContent="Não deu pra enviar agora. Tenta de novo daqui a pouco."; msg.className="fine neg"; $("p-enviar").disabled=false; })
    .then(function(){ msg.hidden=false; });
});

RAIZ.addEventListener("change", function(e){ if (e.target && e.target.type==="radio") calcular(); });
calcular();
})();
