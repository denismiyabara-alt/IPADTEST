/* Quiz "Qual é o seu nível de cagaço?" · Investir e Coçar · uma pergunta por vez */
(function(){
"use strict";

var RAIZ = document.getElementById("perfil-inv");
if (!RAIZ) return;

function $(id){ return document.getElementById(id); }
var TOTAL = 7, passo = 0, resp = {};

var PERFIS = {
  conservador: {
    nome: "Bunda na parede", emoji: "🧱",
    texto: "Tanaka, você entra na bolsa igual banheiro de rodoviária: de costas pra parede e já procurando a saída. Tesouro Selic, CDB de banco grande e olhe lá. Dorme tranquilo. A inflação também, comendo seu dinheiro devagarinho enquanto você ronca.",
    links: [["/o-que-e-tesouro-selic/","O que é Tesouro Selic"],["/o-que-e-cdb/","O que é CDB"],["/o-que-e-fgc/","O que é o FGC"]]
  },
  moderado: {
    nome: "Bundão", emoji: "🍑",
    texto: "Você até comprou FII. Caiu 3% e no mesmo dia você mandou print no grupo da família perguntando se era golpe. Coragem pra entrar você tem. Pra ficar, ainda não.",
    links: [["/o-que-e-tesouro-ipca/","O que é Tesouro IPCA+"],["/o-que-e-fii/","O que é FII"],["/o-que-e-etf/","O que é ETF"]]
  },
  arrojado: {
    nome: "Furico aberto", emoji: "🚀",
    texto: "Ibovespa caiu 30%, você aportou. Caiu mais 10%, você aportou de novo e ainda chamou de promoção. Ou você é gênio, ou é o Tanacão mais sem noção da B3. Seu extrato daqui a 10 anos vai contar qual dos dois.",
    links: [["/o-que-e-acao-on-pn/","Ações ON e PN"],["/o-que-e-pl-acoes/","O que é P/L"],["/o-que-e-ifix/","O que é IFIX"]]
  }
};

function esc(t){ return String(t).replace(/[&<>"]/g,function(c){ return {"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]; }); }

// Leva o topo do quiz pra tela (o resultado nunca fica escondido embaixo).
function topo(){
  var r = $("pq-card").getBoundingClientRect();
  if (r.top < 0 || r.top > window.innerHeight * 0.3) {
    window.scrollTo({ top: window.pageYOffset + r.top - 80, behavior: "smooth" });
  }
}

function mostrar(n){
  passo = n;
  var ps = RAIZ.querySelectorAll(".pq-passo");
  for (var i = 0; i < ps.length; i++) { ps[i].hidden = Number(ps[i].getAttribute("data-passo")) !== n; }
  $("pq-barra").style.width = ((n - 1) / TOTAL * 100) + "%";
  $("pq-voltar").hidden = n === 1;
  topo();
}

function resultado(){
  var pontos = 0;
  for (var i = 1; i <= TOTAL; i++) { pontos += resp[i] || 0; }
  var chave = pontos <= 11 ? "conservador" : pontos <= 16 ? "moderado" : "arrojado", p = PERFIS[chave];
  $("pq-perguntas").hidden = true;
  $("pq-resultado").hidden = false;
  $("pq-emoji").textContent = p.emoji;
  $("p-perfil").textContent = p.nome;
  $("p-label").textContent = "Seu nível de cagaço, com " + pontos + " de 21 pontos:";
  $("p-texto").textContent = p.texto;
  $("pq-ponteiro").style.left = Math.max(3, Math.min(97, (pontos - 7) / 14 * 100)) + "%";

  var alerta = "";
  if (resp[2] === 1) alerta = "Atenção: você ainda não tem reserva de emergência. Antes de buscar rentabilidade, monte essa reserva em algo seguro e com resgate rápido.";
  else if (resp[1] === 1 && chave !== "conservador") alerta = "Atenção: você vai precisar do dinheiro em até 1 ano. Para esse prazo, oscilação pode virar prejuízo na hora de resgatar, qualquer que seja o seu nível.";
  $("p-alerta").textContent = alerta; $("p-alerta").hidden = !alerta;

  $("p-links").innerHTML = p.links.map(function(l){ return '<li><a href="'+esc(l[0])+'">'+esc(l[1])+'</a></li>'; }).join("");
  $("p-perfil-campo").value = p.nome; $("p-lead-nome").textContent = p.nome;
  var msg = "Fiz o quiz do Investir e Coçar e meu nível de cagaço é " + p.nome + " " + p.emoji + ". Qual é o seu? " + location.href.split("#")[0];
  $("pq-zap").href = "https://wa.me/?text=" + encodeURIComponent(msg);
  topo();
}

RAIZ.addEventListener("click", function(e){
  var b = e.target.closest ? e.target.closest(".pq-op") : null;
  if (!b) return;
  var box = b.parentNode, irmaos = box.querySelectorAll(".pq-op");
  for (var i = 0; i < irmaos.length; i++) { irmaos[i].classList.remove("sel"); }
  b.classList.add("sel");
  resp[passo] = Number(b.getAttribute("data-v"));
  setTimeout(function(){ if (passo < TOTAL) { mostrar(passo + 1); } else { resultado(); } }, 180);
});

$("pq-comecar").addEventListener("click", function(){ $("pq-capa").hidden = true; $("pq-perguntas").hidden = false; mostrar(1); });
$("pq-voltar").addEventListener("click", function(){ if (passo > 1) { mostrar(passo - 1); } });
$("pq-refazer").addEventListener("click", function(){
  resp = {}; var s = RAIZ.querySelectorAll(".pq-op.sel"); for (var i = 0; i < s.length; i++) { s[i].classList.remove("sel"); }
  $("pq-resultado").hidden = true; $("pq-perguntas").hidden = false; mostrar(1);
});

// ponytail: POST no-cors direto no formulário do Brevo; não dá pra ler a resposta, então confia no envio.
$("p-form").addEventListener("submit", function(e){
  e.preventDefault();
  var email = $("p-email"), msg = $("p-lead-msg");
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value.trim())) {
    msg.textContent = "Confere o e-mail: parece que faltou alguma coisa."; msg.className = "fine neg"; msg.hidden = false; return;
  }
  $("p-enviar").disabled = true;
  fetch(this.action, { method: "POST", mode: "no-cors", body: new FormData(this) })
    .then(function(){ msg.textContent = "Feito. Confere a sua caixa de entrada (e o spam, vai que)."; msg.className = "fine pos"; $("p-form").hidden = true; })
    .catch(function(){ msg.textContent = "Não deu pra enviar agora. Tenta de novo daqui a pouco."; msg.className = "fine neg"; $("p-enviar").disabled = false; })
    .then(function(){ msg.hidden = false; });
});
})();
