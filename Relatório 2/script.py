import numpy as np
import pandas as pd
import math
from matplotlib import pyplot as plt
from pandas.core.construction import array

def gerarGraficos1(dados):
    g = dados['a'].mean()
    print(g)
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
    fig.set_size_inches(12, 6)
    fig.savefig("Gráfico 1")
    plt.close(fig=fig)

def gerarGraficos2(g):
    # Y = Ax + B
    d = np.linspace(0, 0.16, 100) # Valores para D
    fig, ax1 = plt.subplots()

    for k in range(1, 13):
        A = 4 * pow(math.pi, 2) / g
        B = 4 * pow(math.pi, 2) * pow(k/100, 2) / g
        ax1.plot(pow(d, 2), A * pow(d, 2) + B, label=f"k = {k/100} m")


    ax1.legend(loc="lower right")
    ax1.set_title("Linearização da equação modelo")
    ax1.set_ylabel("Distancia * Período² (m * s²)")
    ax1.set_xlabel("Distancia² (m²)")
    ax1.tick_params(top=True, right=True, direction="in")
    fig.set_size_inches(6, 4)
    fig.savefig("Gráfico 2")
    plt.close(fig=fig)

def gerarGraficos3():
    fig, ax1 = plt.subplots()
    for k in range(10, 12):
        g = pd.read_csv("data f229/gravidade")["a"].mean()

        D = np.linspace(0.01, 0.2, 100)
        T = 2*math.pi*pow((D + pow(k/100, 2)/D)/g, 1/2)
        ax1.plot(D, T, label=f"Comportamento teórico para k = {k/100} m", alpha=0.3)

    d = []
    t = []
    df = pd.read_csv(f"data f229/Data")
    for i in range(len(df)):
        t.append(df["t"][i])
        d.append(df["d"][i])
        print(df["d"][i], df["t"][i])
    ax1.plot(d, t, label="Comportamento obtido")

    ax1.set_xlabel("Distancia (m)")
    ax1.set_ylabel("Período (s)")
    ax1.set_xlim([0, 0.1])
    ax1.legend(loc="upper right")
    ax1.set_title("Comparação obtido x teórico")

    fig.set_size_inches(6, 4)
    fig.savefig("Gráfico 3")

    plt.close(fig=fig)

def gerarGraficos4():
    d = []
    t = []
    fig, g1 = plt.subplots()

    df = pd.read_csv(f"data f229/Data")
    for i in range(len(df)):
        t.append(df["t"][i])
        d.append(df["d"][i])
        #td = 2*math.pi*math.sqrt((D/100 + pow(11/100, 2)/(D/100))/10)
        #t.append(td)

    y = []
    x = []

    for i in range(len(d)):
        y.append(d[i] * pow(t[i], 2))
        x.append(pow(d[i], 2))
    
    g1.errorbar(x, y, xerr=pegarIncertezas2(), yerr=pegarIncertezas1(), linestyle='', fmt='', capsize=3, capthick=1, ecolor='k')
    g1.scatter(x, y, alpha=0.8)

    (a, b), cov = np.polyfit(x, y, 1, cov=True)
    erros = np.sqrt(np.diag(cov))

    poly = np.poly1d([a, b])
    g = (4 * pow(math.pi, 2)) / a
    k = math.sqrt(b/a)

    ug = pow(erros[0], 2) * 4 * pow(math.pi, 2) / 16
    uk = math.sqrt((b * pow(erros[0], 2) / (4 * pow(a, 3))) + b * pow(erros[1], 2)/ (4 * pow(b, 2) * a))
    g1.plot(x, poly(x), color="r", label=f"Ajuste polinomial linear\nr: ({round(a, 1)} +- {round(erros[0], 1)})x + ({round(b, 3)} +- {round(erros[1], 3)})\ng estimada: {round(g, 1)} +- {round(ug, 1)}\nk estimado: {round(k, 3)} +- {round(uk, 3)}")
    
    g1.set_xlabel("Distancia² (m²)")
    g1.set_ylabel("Distancia * Periodo² (m*s²)")
    g1.legend(loc="upper left")
    g1.set_title("Ajuste para os dados obtidos")

    fig.set_size_inches(6, 4)
    fig.tight_layout()
    fig.savefig(f"Gráfico 4")
    
    plt.close(fig=fig)

def gerarGraficos5():
    fig, g1 = plt.subplots()
    g = round(pd.read_csv("data f229/gravidade")["a"].mean(), 1)
    k = 0.1

    df = pd.read_csv(f"data f229/Data")
    
    g1.errorbar(df["d"], df["t"], xerr=0.0005, yerr=0.03, label="Dados experimentais", fmt='o', capsize=3, capthick=1, ecolor='k', alpha=0.8)

    d1, t1 = [[], []]
    d2, t2 = [[], []]
    for d in df["d"]:
        d1.append(d)
        t1.append(2 * math.pi * math.sqrt(d/g))

        d2.append(d)
        t2.append(2 * math.pi * math.sqrt((d + pow(k, 2)/d)/g))

    g1.plot(d1, t1, label=f"Equação modelo do pêndulo simples. g = {g}")
    g1.plot(d2, t2, label=f"Equação modelo do pêndulo físico. g = {g} k = {k}")

    g1.set_xlabel("Distancia (m)")
    g1.set_ylabel("Periodo (s)")
    g1.legend(loc="upper right")
    g1.set_title("Comparação entre as equações modelos e o experimento")
    fig.set_size_inches(6, 4)
    fig.tight_layout()
    fig.savefig(f"Gráfico 5")
    
    plt.close(fig=fig)

def gerarGraficos6():
    valor = 200
    for i in range(9):
        t = np.linspace(0, 5, valor)
        os = []
        df = pd.read_csv(f"data f229/Data {i+1}")
        ang = df["θ"][0]
        plt.plot(df["t"][:valor], df["θ"][:valor], label="Comportamento obtido")
        for x in t:
            os.append(ang * math.cos(pegarVelAng()[i] * x))
        plt.plot(t, os, label="Comportamento esperado")
        plt.title(f"Comportamento da posição angular para a distância D = {i+1} cm")
        plt.legend(loc="lower right")
        plt.ylabel("Ângulo (radianos)")
        plt.xlabel("Tempo (s)")
        plt.xlim(0, 5)
        plt.savefig(f"Grafico angulo {i}")
        plt.close('all')
        
def pegarIncertezas1():
    dt2 = []
    df = pd.read_csv("data f229/Data")
    for i in range(len(df)):
        termo1 = 2.5 * pow(10, -7) * pow(df["t"][i], 4)
        termo2 = 3.6 * pow(10, -3) * pow(df["t"][i], 2) * pow(df["d"][i], 2)
        u = math.sqrt(termo1 + termo2)
        dt2.append(u)

    return dt2

def pegarIncertezas2():
    d2 = []
    df = pd.read_csv("data f229/Data")
    for i in range(len(df)):
        termo1 = pow(10, -6) * pow(df["d"][i], 2)
        u = math.sqrt(termo1)
        d2.append(u)

    return d2

def pegarVelAng():
    ws = []
    df = pd.read_csv("data f229/Data")
    for i in range(len(df)):
        w = 2 * math.pi / df["t"][i]
        ws.append(w)
    return ws

def pegarIncertezas3():
    r1 = 7.5/200 
    r2 = 7.1/200
    l = 33/100
    u = 1/2000
    termo1 = pow(r1/(2*math.sqrt(pow(r1, 2) + pow(r2, 2) + pow(l, 2)/3)), 2) * pow(u, 2)
    termo2 = pow(r2/(2*math.sqrt(pow(r1, 2) + pow(r2, 2) + pow(l, 2)/3)), 2) * pow(u, 2)
    termo3 = pow(l/(2*math.sqrt(3) * math.sqrt(3*pow(r1, 2) + 3*pow(r2, 2) + pow(l, 2))), 2) * pow(u, 2)

    uk = math.sqrt(termo1 + termo2 + termo3)
    return round(uk, 4)

gerarGraficos1(pd.read_csv('data f229/gravidade'))
gerarGraficos2(pd.read_csv("data f229/gravidade")["a"].mean())
gerarGraficos3()
gerarGraficos4()
gerarGraficos5()
gerarGraficos6()