import numpy as np
import pandas as pd
import math
from matplotlib import pyplot as plt

def calibracao(dados):
    fig, ax1 = plt.subplots()
    ax1.plot(dados["frequency (Hz)"], dados["audio amplitude (a.u.)"])
    ax1.set_xlabel("Frequencia (Hz)")
    ax1.set_ylabel("Amplitude (a.u.)")
    plt.show()
    plt.close("all")
def graficoGeral(calibracao, tuboaa, tuboaf, tuboff, lim):
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()

    fig1.set_size_inches(6, 4)
    fig2.set_size_inches(6, 4)
    fig3.set_size_inches(6, 4)
    
    ax1.plot(calibracao["frequency (Hz)"], calibracao["audio amplitude (a.u.)"], c='r', label="Calibração", alpha=0.8)
    ax1.plot(tuboaa["frequency (Hz)"], tuboaa["audio amplitude (a.u.)"], label="Tudo aberto-aberto", alpha=0.8)
    
    ax1.set_xlim(0, lim)
    ax1.set_ylabel("Audio amplitude (a.u.)")
    ax1.set_xlabel("Frequency (Hz)")

    ax1.legend(loc="upper left")
    fig1.savefig("1.png")
    plt.close(fig=fig1)

    ax2.plot(calibracao["frequency (Hz)"], calibracao["audio amplitude (a.u.)"], c='r', label="Calibração", alpha=0.8)
    ax2.plot(tuboaf["frequency (Hz)"], tuboaf["audio amplitude (a.u.)"], label="Tudo aberto-fechado", alpha=0.8)
    
    ax2.set_xlim(0, lim)
    ax2.set_ylabel("Audio amplitude (a.u.)")
    ax2.set_xlabel("Frequency (Hz)")
    
    ax2.legend(loc="upper left")
    fig2.savefig("2.png")
    plt.close(fig=fig2)

    ax3.plot(calibracao["frequency (Hz)"], calibracao["audio amplitude (a.u.)"], c='r', label="Calibração", alpha=0.8)
    ax3.plot(tuboff["frequency (Hz)"], tuboff["audio amplitude (a.u.)"], label="Tudo fechado-fechado", alpha=0.8)
    
    ax3.set_xlim(0, lim)
    ax3.set_ylabel("Audio amplitude (a.u.)")
    ax3.set_xlabel("Frequency (Hz)")
    
    ax3.legend(loc="upper left")
    fig3.savefig("3.png")
    plt.close(fig=fig3)

def graficoEsperado(comprimento, tubo):
    t = np.linspace(0, 5, 100)
    x = np.linspace(0, comprimento, 100)
    y = []
    f = max(tubo["frequency (Hz)"])

    for i in range(100):
        y.append(math.cos(x[i] * n * math.pi / comprimento) * math.sin(2 * math.pi * f * t[i]))
    plt.plot(x, y, label=f"Frequencia: {f}")
    plt.xlabel("x")
    plt.ylabel("y")
    plt.legend(loc="lower right")
    plt.show()


calibracao = pd.read_csv("dados/calibracao.csv")
tuboaa = pd.read_csv("dados/tubo aberto aberto.csv")
tuboaf = pd.read_csv("dados/tubo aberto fechado.csv")
tuboff = pd.read_csv("dados/tubo fechado fechado.csv")
graficoGeral(calibracao, tuboaa, tuboaf, tuboff, 1800)
#graficoEsperado(1.177, tuboff)
