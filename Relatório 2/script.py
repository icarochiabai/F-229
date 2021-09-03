import numpy as np
import pandas as pd
import math
from matplotlib import pyplot as plt

def gerarGraficos1(dados):
    g = dados['a'].mean()
    k = 10/100 #k = 10cm

    fig, subplots = plt.subplots(1, 2, sharex=True, sharey=True)

    D = np.linspace(0.01, 0.2, 100)

    for k in range(0, 11):
        T = 2*math.pi*pow((D + pow(k/100, 2)/D)/g, 1/2)

        subplots[0].plot(D, T, label=f"k = {k/100} m")
        subplots[1].plot(D, T, label=f"k = {k/100} m", alpha=0.3)

    for subplot in subplots:
        subplot.tick_params(right=True, top=True, direction='in')
        subplot.legend(loc="lower right")
    subplots[1].plot(D, 2*math.pi*pow(D/g, 1/2), label="Pêndulo simples", color="k")

    subplots[0].set_ylabel("Período (s)")
    fig.text(0.5, 0.04, "Distancia (m)", ha="center")
    fig.suptitle("Periodo em função da distancia")

    plt.subplots_adjust(wspace=0)
    plt.show()

def pegarPeriodo(dados):
    maiorValor1 = 0
    menorValor1 = 10
    maiorValorIndex = 0
    menorValorIndex = 0

    for i in list(range(len(dados.index))):
        if dados[" rad"][i] > maiorValor1:
            maiorValor1 = dados[" rad"][i]
            maiorValorIndex = i
        elif dados[" rad"][i] < menorValor1:
            menorValor1 = dados[" rad"][i]
            menorValorIndex = i

    for i in list(range(menorValorIndex, len(dados.index))):
        if dados[" rad"][i] > menorValor1:
            menorValor1 = dados[" rad"][i]
            menorValorIndex = i

    return (abs(dados["t"][menorValorIndex] - dados["t"][maiorValorIndex]))

def gerarGraficos2(g):
    # Y = Ax + B
    d = np.linspace(0, 0.16, 100) # Valores para D
    for k in range(0, 11):
        A = 4 * pow(math.pi, 2) / g
        B = 4 * pow(math.pi, 2) * pow(k/100, 2) / g
        plt.plot(pow(d, 2), A * pow(d, 2) + B, label=f"k = {k/100} m")

    plt.legend(loc="lower right")
    plt.title("Linearização da equação modelo")
    plt.ylabel("Distancia * Período² (m * s²)")
    plt.xlabel("Distancia² (m²)")
    plt.tick_params(top=True, right=True, direction="in")
    plt.show()

def gerarGraficos3():
    g = pd.read_csv("data f229/gravidade")["a"].mean()

    D = np.linspace(0.01, 0.2, 100)

    for k in range(6, 8):
        T = 2*math.pi*pow((D + pow(k/100, 2)/D)/g, 1/2)

        plt.plot(D, T, label=f"Comportamento teórico para k = {k/100} m", alpha=0.3)

    d = []
    t = []
    for i in range(1, 8):
        df = pd.read_csv(f"data f229/Data {i}")
        t.append(pegarPeriodo(df))
        d.append(i/100)
    plt.plot(d, t, label="Comportamento obtido")

    plt.xlabel("Distancia (m)")
    plt.ylabel("Período (s)")
    plt.legend(loc="lower right")
    plt.title("Comparação obtido x teórico")

    plt.show()
# gerarGraficos1(pd.read_csv('data f229/gravidade'))
# gerarGraficos2(pd.read_csv("data f229/gravidade")["a"].mean())
gerarGraficos3()
