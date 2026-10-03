"""Regras de texto da fila de comentários: pergunta, spam/golpe, risco e tema. Sem rede, só biblioteca padrão.

Reaproveita a normalização e a regra PERGUNTA do auditoria-canal/analisar.py e os temas do pautas-canal/perguntas.py,
para que a fila conte pergunta do mesmo jeito que o relatório.
"""
import re
import sys
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[1]
for p in (RAIZ / "auditoria-canal", RAIZ / "pautas-canal"):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
import analisar as an  # noqa: E402
import perguntas as pg  # noqa: E402

norm = an.norm
sem_arroba = an.sem_arroba

# Além da regra do analisar.py ("?" ou começo com como/qual/quando/onde/quanto/vale a pena/devo...), contam como
# pergunta os começos com pode/posso/vale/e se/alguém e os pedidos explícitos de dúvida no meio do texto.
PERGUNTA_EXTRA = re.compile(
    r"^(pode|posso|podemos|vale|e se|alguem|me explica|explica|gostaria de saber|queria saber|preciso saber)\b|"
    r"\b(gostaria de saber|queria saber|alguem sabe|minha duvida|tenho uma duvida|fiquei com duvida|"
    r"me tira uma duvida|duvida:|como (eu )?faco|como funciona|qual a diferenca|vale a pena|devo (comprar|vender|"
    r"investir|tirar|declarar)|quanto rende|onde (eu )?(invisto|coloco|compro))\b")


def eh_pergunta(texto):
    t = norm(texto or "")
    if not t:
        return False
    return bool(an.PERGUNTA.search(t) or PERGUNTA_EXTRA.search(t))


# Spam e golpe: pede contato fora do YouTube, oferece mentoria/gestão, número de telefone, ou é a "isca" clássica
# dos robôs de cripto (pergunta genérica de lucro que puxa respostas de falsos gestores). Não recebe resposta:
# vai para o Denis ocultar.
SPAM = re.compile(
    # contato fora do YouTube
    r"wa\.me/|\bt\.me/|"
    r"\+ ?\d{2} ?\(?\d{2}\)? ?9?\d{4}[ -]?\d{4}|\(\d{2}\) ?9?\d{4}[ -]?\d{4}|\b0?\d{2} ?9\d{4}-?\d{4}\b|"
    r"me chama no (whats|zap|insta|telegram|direct|privado|pv)|(chama|chame|chamar) no (privado|pv|direct)|"
    r"(entre|entrar|entra) em contato (comigo|com ela\b|com ele\b|com a (sra|senhora|treinadora|especialista|coach)|"
    r"com o (sr|senhor|treinador|especialista))|como (alcanca|alcancar|chegar a|chego a|falar com) (la|lo|ela|ele)|"
    # oferta de mentoria, gestão, sinais
    r"(minha|nossa|faco|ofereco|oferecemos|faca a) mentoria|mentoria (gratuita|gratis|individual|vip)|"
    r"gestor(a)? de (conta|investimento|carteira)|trader profissional|agente de (negociacao|investimento)|"
    r"sinais (semanais|diarios|de trade)|lucros? (semanais|garantid)|retorno garantido|renda extra garantida|"
    r"indico a empresa|alguem (gostaria|quer) de trabalhar|trabalh(ar|e) (de )?home office|"
    # história de ganho rápido e a "isca" dos robôs de cripto
    r"(investi|comecei com|iniciei com|depositei).{0,40}\d.{0,120}(agora (estou|tenho)|em (apenas )?(uma|duas|tres|\d+) "
    r"semanas?|hoje tenho)|em pouco tempo (tenho|ja tenho|estou com)|"
    r"abordagem (cert|corret)|obter (um )?bons? lucros?|investimento mais lucrativo em cripto")
# Nome próprio depois de título de "especialista": é o padrão dos robôs ("Sra. Fulana Tal", "coach Fulana"). Com
# Sr./Sra. e um nome só ("Sr. Carlos", personagem de vídeo), exige também vocabulário de robô no texto.
NOME = r"[A-Z][a-zà-ú]+"
SPAM_TITULO = re.compile(r"\b(coach|treinadora|treinador|especialista|mentora|analista|gestora|expert|deputada)\.? "
                         + NOME)
SPAM_SR = re.compile(r"\b(Sra|Sr|Senhora|senhora)\.? " + NOME + r"(?P<sobrenome>\.? ?[A-Z]\.? ?|\s" + NOME + r")?")
VOCAB_ROBO = re.compile(r"negoci\w* com|trader|portf|lucr|estrateg|comerci|ganancia|contato|alcanc|investindo com|investi com|"
                        r"sinais|recomend|telegram")


# WhatsApp/Telegram só é spam com pedido de contato junto (reclamar do SAC pelo WhatsApp não é spam).
CANAL_EXTERNO = re.compile(r"whats ?app|\bzap\b|\bwpp\b|\bwhats\b|telegram|\binsta\b|instagram")
PEDE_CONTATO = re.compile(r"me chama|chama no|me chame|chamar no|me add|me adiciona|meu numero|meu contato|meu whats|"
                          r"meu zap|segue (o|meu)|grupo no|link|\bdm\b|privado|contato (dela|dele|comigo)|"
                          r"(ela|ele) esta (principalmente |ativa |ativo )?(no|em)|ativa en|nome de usuario|"
                          r"envi(e|ar) (uma )?mensagem|fal(e|ar) com (ela|ele)\b|\d{8,}")


def eh_spam(texto):
    texto = texto or ""
    t = norm(texto)
    if SPAM.search(t) or SPAM_TITULO.search(texto):
        return True
    if CANAL_EXTERNO.search(t) and PEDE_CONTATO.search(t) and not re.search(r"golpe|e real|sera que", t):
        return True
    for m in SPAM_SR.finditer(texto):
        if m.group("sobrenome") or VOCAB_ROBO.search(norm(texto)):
            return True
    return False


TICKER = re.compile(r"(?<![A-Za-z0-9])[A-Za-z]{4}(3|4|5|6|11|31|32|33|34|35|39)(?![A-Za-z0-9])")
RECOMENDACAO = re.compile(
    r"vale a pena (comprar|investir|entrar|colocar|aplicar)|qual (a |o )?(melhor|acao|fii|etf|bdr|cripto|moeda|banco|"
    r"corretora|investimento|fundo|cdb)|quais (as |os )?(melhores|acoes|fiis|etfs)|devo (comprar|vender|investir|"
    r"sair|entrar|colocar|aplicar|resgatar)|compro\b|o que (voce |vc )?acha d[aoe]|"
    r"recomenda|(me|voce|vc|voces) indica\b|indicacao|melhor (acao|fii|etf|banco|corretora|investimento|cdb|fundo|cripto)|"
    r"onde (eu )?(invisto|investir|coloco|aplico)|em que investir|hora de (comprar|vender)|ainda (vale|da tempo)|"
    r"(compensa|vale) (mais|investir)")
TRIBUTARIO = re.compile(r"imposto|irpf|declar|darf|tribut|isen[tc]|come.?cotas|receita federal|\biof\b|"
                        r"leao|\bjcp\b|taxad")
IR_SIGLA = re.compile(r"\bI\.?R\b\.?")  # "IR" maiúsculo; "ir" minúsculo é o verbo
RECLAMACAO = re.compile(
    r"pessim|horrivel|lixo|ridicul|vergonha|absurd|enganad|engana|mentira|mentiroso|clickbait|caca.?clique|"
    r"decepcion|nao funciona|nao consigo|nao recebi|ninguem responde|nao respond|bloquear(am)? minha|bloqueou minha|"
    r"reclam|propaganda|pago (pra|para) falar|patrocinad|enrola|perda de tempo|nao explic|so fala|piada|"
    r"conversa fiada|papo furado|roubo|roubad|sacanagem|nao tem logica|nao faz sentido|conta errada|esta errad|ta errad")


# Instituições pelo nome (corretoras, bancos, exchanges). Rascunho não cita nenhuma (regra do canal).
INSTITUICAO = re.compile(r"\b(xp|rico investimentos|corretora rico|(na|pela) rico|clear|btg|nu ?invest|easynvest|"
                         r"banco inter|inter invest|toro|modalmais|genial|orama|"
                         r"warren|avenue|nomad|c6( bank)?|itau|ion|bradesco|santander|mirae|guide|safra|binance|"
                         r"mercado bitcoin|foxbit|bitso|picpay|mercado pago|nubank|nuconta|next|caixa tem|pagbank)\b")


def riscos(texto):
    """Lista de riscos, na ordem de gravidade. spam/golpe exclui os demais (não recebe resposta)."""
    t = norm(texto or "")
    if eh_spam(texto):
        return ["spam/golpe"]
    out = []
    if TICKER.search(texto or "") or RECOMENDACAO.search(t):
        out.append("pede_recomendacao")
    if TRIBUTARIO.search(t) or IR_SIGLA.search(texto or ""):
        out.append("tributario")
    if RECLAMACAO.search(t):
        out.append("reclamacao")
    return out


def nota_risco(texto):
    return "; ".join(riscos(texto))


def tema(texto, video_id=""):
    return pg.tema(texto, video_id)


def fora_do_escopo(tema_):
    return pg.FORA in tema_
