"""Limpa as bordas de cada frase. O take do Qwen abre e fecha com um baque grave (~125 Hz, o "bum"
entre as cenas) e comeca em volume cheio (o "tic"). Nas bordas: passa-altas 150 Hz com transicao
suave pro original + fade curto. O meio da frase fica intocado (a voz nao emagrece).
Uso: python3 suavizar_bordas.py b0 b1 ...   (reaplicar e seguro: o grave ja removido nao volta)
"""
import sys, json, numpy as np, soundfile as sf
from scipy.signal import butter, sosfiltfilt

BORDA, IN, OUT, CORTE = 0.150, 0.015, 0.030, 150

def limpar(seg, sr):
    """seg = uma frase isolada. Devolve copia limpa."""
    s = seg.copy(); n = len(s)
    if n < int(.05*sr): return s
    hp = sosfiltfilt(butter(4, CORTE, "highpass", fs=sr, output="sos"), s)
    b = min(int(BORDA*sr), n // 2)
    mix = np.ones(n)                                  # 1 = versao filtrada, 0 = original
    mix[b:n-b] = 0
    rampa = np.linspace(1, 0, b // 3)                 # ultimo terco da borda volta pro original
    mix[b - len(rampa):b] = rampa; mix[n-b:n-b+len(rampa)] = rampa[::-1]
    s = mix*hp + (1-mix)*s
    n1, n2 = min(int(IN*sr), n), min(int(OUT*sr), n)
    s[:n1] *= np.linspace(0, 1, n1); s[n-n2:] *= np.linspace(1, 0, n2)
    return s

def tirar_estouro(seg, sr):
    """O take do Qwen abre com um estouro (~600 Hz, 30-40 ms) e cai quase a zero antes da fala.
    Silencia do inicio ate o vale depois do estouro (fade de 10 ms). Sem estouro (>0,03) nao mexe."""
    w = int(.01*sr); n = min(len(seg) // w, 15)
    if n < 4: return seg, False
    env = np.array([np.sqrt(np.mean(seg[k*w:(k+1)*w]**2)) for k in range(n)])
    p = int(np.argmax(env[:5]))
    if env[p] < 0.03: return seg, False
    vale = p + int(np.argmin(env[p:])) if p < n - 1 else p
    if env[vale] > env[p] * 0.35: return seg, False      # nao caiu: e fala, nao estouro
    s = seg.copy(); fim = (vale + 1) * w
    s[:fim] = 0; k = min(w, len(s) - fim); s[fim:fim+k] *= np.linspace(0, 1, k)
    return s, True

def desbaquear(a, sr, limiar=0.025, corte=150):
    """Acha baques graves (<120 Hz) em qualquer ponto da voz e tira o grave SO ali (~0,2 s, com crossfade).
    O Qwen solta um 'bum' na ultima silaba de muitas frases, 0,2-0,6 s antes do fim."""
    lp = sosfiltfilt(butter(4, 120, "lowpass", fs=sr, output="sos"), a)
    w = int(.03*sr); env = np.sqrt(np.convolve(lp**2, np.ones(w)/w, "same"))
    hp = sosfiltfilt(butter(4, corte, "highpass", fs=sr, output="sos"), a)
    mix = (env > limiar).astype(float)
    mix = np.convolve(mix, np.ones(int(.08*sr)), "same") > 0          # alarga a janela ~80 ms
    k = int(.03*sr); mix = np.convolve(mix.astype(float), np.ones(k)/k, "same")   # crossfade 30 ms
    return mix*hp + (1-mix)*a, int((np.diff((env > limiar).astype(int)) == 1).sum())

def suavizar(a, sr, ini, fim):
    i, j = int(ini*sr), min(int(fim*sr), len(a))
    a[i:j], _ = tirar_estouro(limpar(a[i:j], sr), sr)

if __name__ == "__main__":
    for b in sys.argv[1:]:
        a, sr = sf.read(f"voz_{b}.wav"); m = json.load(open(f"voz_{b}.beats.json"))
        for f in m["frases"]: suavizar(a, sr, f["ini"], f["fim"])
        a, n = desbaquear(a, sr)
        sf.write(f"voz_{b}.wav", a, sr); print(f"{b}: {len(m['frases'])} frases limpas, {n} baques tirados")
