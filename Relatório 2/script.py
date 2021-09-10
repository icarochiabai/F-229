import numpy as np
import pandas as pd
import math
from matplotlib import pyplot as plt

def gerarGraficos1(dados):
    g = dados['a'].mean()
    k = 10/100 #k = 10cm

    fig, subplots = plt.subplots(1, 2, sharex=True, sharey=True)

    D = np.linspace(0.01, 0.2, 100)

    for k in range(1, 13):
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
    maiorValor = 0
    menorValor = 10
    inicio = 0
    fim = 0
    periodos = []   
    for v in range(2):
        for i in list(range(inicio, len(dados.index))):
            if dados["θ"][i] > maiorValor:
                maiorValor = dados["θ"][i]
                inicio = i
            elif dados["θ"][i] < menorValor:
                menorValor = dados["θ"][i]  
                fim = i 
        for i in list(range(fim, len(dados.index))):
            if dados["θ"][i] > menorValor:
                menorValor = dados["θ"][i]
                fim = i
        periodos.append(abs(dados["t"][fim] - dados["t"][inicio]))
        inicio = fim
    return max(periodos)
def gerarGraficos2(g):
    # Y = Ax + B
    d = np.linspace(0, 0.16, 100) # Valores para D
    for k in range(1, 13):
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
    T = 2*math.pi*pow((D + pow(9.7/100, 2)/D)/g, 1/2)
    plt.plot(D, T, label=f"Comportamento teórico para k = {9.7/100} m", alpha=0.3)

    d = []
    t = []
    for i in range(1, 13):
        df = pd.read_csv(f"data f229/Data {i}")
        t.append(pegarPeriodo(df))
        d.append(i/100)
        print(pegarPeriodo(df), i/100)
    plt.plot(d, t, label="Comportamento obtido")

    plt.xlabel("Distancia (m)")
    plt.ylabel("Período (s)")
    plt.legend(loc="lower right")
    plt.title("Comparação obtido x teórico")

    plt.show()

def gerarGraficos4():
    d = []
    t = []

    for D in range(1, 13):
        df = pd.read_csv(f"data f229/Data {D}")
        t.append(pegarPeriodo(df))
        d.append(D/100)
        #td = 2*math.pi*math.sqrt((D/100 + pow(11/100, 2)/(D/100))/10)
        #t.append(td)

    y = []
    x = []
    for i in range(len(d)):
        y.append(d[i] * pow(t[i], 2))
        x.append(pow(d[i], 2))
    
    plt.scatter(x[1:], y[1:])

    (a, b), cov = np.polyfit(x[1:   ], y[1:], 1, cov=True)
    erros = np.sqrt(np.diag(cov))

    poly = np.poly1d([a, b])
    g = (4 * pow(math.pi, 2)) / a
    k = math.sqrt(b/a)
    plt.plot(x, poly(x), color="r", label=f"polyfit\nA: {a} +- {erros[0]}\nB: {b} +- {erros[1]}\ng: {g}\nk: {k}")
    
    plt.xlabel("Distancia² (m²)")
    plt.ylabel("Distancia * Periodo² (m*s²)")
    plt.legend(loc="upper left")
    plt.show()


#gerarGraficos1(pd.read_csv('data f229/gravidade'))
#gerarGraficos2(pd.read_csv("data f229/gravidade")["a"].mean())
#gerarGraficos3()
gerarGraficos4()
