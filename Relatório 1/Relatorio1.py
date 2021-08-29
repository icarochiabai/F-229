import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import decimal
from decimal import Decimal

ctx = decimal.getcontext()
ctx.rounding = decimal.ROUND_UP

# config = {
# 'axes.spines.right': True,
# 'axes.spines.top': True,
# 'axes.edgecolor': '.4',
# 'axes.labelcolor': '.0',
# 'axes.titlesize': 'large',
# 'axes.labelsize': 'medium',
# 'figure.autolayout': True,
# 'figure.figsize': (width, width/2),
# 'font.family': ['serif'],
# 'font.size': 10.0,
# 'grid.linestyle': '-',
# 'legend.facecolor': '.9',
# 'legend.frameon': True,
# 'savefig.transparent': True,
# 'text.color': '.0',
# 'xtick.labelsize': 'small',
# 'ytick.labelsize': 'small',
# }

def get_dados():
    data = []
    for i in range(1, 25):
        data.append(pd.read_csv(f'{i}data.csv'))
    return data

def get_espacamento(data, coluna, threshold):
    data = data[(data[str(coluna)] >= data[str(coluna)].values[-1] + threshold) & (data[str(coluna)] <= data[str(coluna)].values[0] - threshold)]
    return data.index[0], data.index[-1]

def generate_graphs1(data, th):
    plt.tick_params(right=True, top=True, direction='in')
    for i in range(len(data)):
        fig, ax = plt.subplots()

        x, y = [
            data[i]['tempo'],
            data[i]['altura']
        ]

        left, right = get_espacamento(data[i], 'altura', th)

        (a, b, c), cov = np.polyfit(x.tolist()[left:right+1], y.tolist()[left:right+1], 2, cov=True)
        erros = np.sqrt(np.diag(cov))

        poly = np.poly1d([a, b, c])
        
        ax.tick_params(right=True, top=True, direction='in')
        ax.errorbar(
            x,
            y,
            xerr=1/24,
            yerr=1/1000,
            color="b",
            fmt="o",
            capsize=3,
            capthick=1,
            ecolor="black",
            label="Dados coletados",
            alpha=0.5,
            zorder=1
            )

        ax.plot(
            x.tolist()[left:right+1],
            poly(x.tolist()[left:right+1]),
            'r',
            label=f"Ajuste polinomial\n({float(round(Decimal(a), 3))} ± {float(round(Decimal(erros[0]), 3))})x² + ({float(round(Decimal(b), 2))} ± {float(round(Decimal(erros[1]), 2))})x + ({float(round(Decimal(c), 1))} ± {float(round(Decimal(erros[2]), 1))})",
            zorder=2
            )

        ax.set_title(f"Altura H{5 - i//6} C{i%6 +1}")
        ax.set_xlabel("Tempo [s]")
        ax.set_ylabel("Altura [m]")
        ax.legend(loc="lower left")
        ax.set_ylim(0)

        fig.set_size_inches(8, 6)
        fig.tight_layout()
        fig.savefig(f'Grafico H{5 - i//6}C{i%6 +1}.png')
        plt.close(fig=fig)    

def generate_graphs2(data, th):
    massas = {
        "A": 49.4/1000,
        "B": 49.2/1000,
        "1": 29.7/1000,
        "7": 15.6/1000,
        "D": 29.5/1000,
        "F": 18.5/1000,
        "G": 15.0/1000,
        "m1": 893.8/1000,
        "m2": 893.2/1000,
        "m3": 1934.6/1000
    }

    configuracoes = {
        "C1": {
            "m1": massas["m1"] + massas["A"] + massas["1"] + massas["7"] + massas["F"],
            "m2": massas["m2"] + massas["B"] + massas["D"] + massas["G"]
        },

        "C2": {
            "m1": massas["m1"] + massas["A"] + massas["1"] + massas["7"] + massas["G"],
            "m2": massas["m2"] + massas["B"] + massas["D"] + massas["F"]
        },

        "C3": {
            "m1": massas["m1"] + massas["A"] + massas["1"] + massas["F"] + massas["G"],
            "m2": massas["m2"] + massas["B"] + massas["D"] + massas["7"]
        },

        "C4": {
            "m1": massas["m1"] + massas["A"] + massas["1"] + massas["B"] + massas["F"],
            "m2": massas["m2"] + massas["D"] + massas["7"] + massas["G"]
        },

        "C5": {
            "m1": massas["m1"] + massas["A"] + massas["1"] + massas["D"] + massas["B"],
            "m2": massas["m2"] + massas["F"] + massas["7"] + massas["G"]
        },

        "C6": {
            "m1": massas["m1"] + massas["A"] + massas["D"] + massas["1"] + massas["7"],
            "m2": massas["m2"] + massas["B"] + massas["F"] + massas["G"]
        }
    }

    fig, ax = plt.subplots()
    ax.tick_params(right=True, top=True, direction='in')

    for j in range(4):
        if j == 0:
            cor="C0"
        elif j == 1:
            cor="C1"
        elif j == 2:
            cor="C2"
        elif j == 3:
            cor="C3"

        aceleracoes = []
        deltamassa = []
        xerr = []
        for i in range(6):
            x, y = [data[i + 6*j]["tempo"], data[i + 6*j]["altura"]]

            left, right = get_espacamento(data[i + 6*j], 'altura', th)

            (a, b, c), cov = np.polyfit(x.tolist()[left:right+1], y.tolist()[left:right+1], 2, cov=True)
            erros = np.sqrt(np.diag(cov))
            xerr.append(erros[0])
            
            deltamassa.append(configuracoes[f"C{i+1}"]["m1"] - configuracoes[f"C{i+1}"]["m2"])
            aceleracoes.append(abs(2*a))

        
        (a, b), cov = np.polyfit(aceleracoes, deltamassa, 1, cov=True)
        erros = np.sqrt(np.diag(cov))
        poly = np.poly1d([a, b])

        ax.errorbar(
            aceleracoes,
            deltamassa,
            xerr=xerr,
            yerr=0.0003,
            label=f"H{5-j}: ({round(Decimal(a), 2)} ± {round(Decimal(erros[0]), 2)}) x + ({round(Decimal(b), 3)} ± {round(Decimal(erros[1]), 3)})",
            color=cor,
            fmt="o",
            capsize=3,
            ecolor="black",
            alpha=0.5)

        ax.plot(
            aceleracoes,
            deltamassa,
            'yo',
            aceleracoes,
            poly(aceleracoes),
            alpha=0.5
        )
        

    ax.legend(loc="lower right")
    ax.set_title("Aceleração para cada situação")
    ax.set_xlabel("Aceleração [m/s²]")
    ax.set_ylabel("m1 - m2 [kg]")

    fig.set_size_inches(8, 6)
    fig.tight_layout()
    fig.savefig(f'Grafico Aceleracao x Massa.png')
    plt.close(fig=fig)    
        
def calcular(data, th, opcao):
    massas = {
        "A": 49.4/1000,
        "B": 49.2/1000,
        "1": 29.7/1000,
        "7": 15.6/1000,
        "D": 29.5/1000,
        "F": 18.5/1000,
        "G": 15.0/1000,
        "m1": 893.8/1000,
        "m2": 893.2/1000,
        "m3": 1934.6/1000
    }

    configuracoes = {
        "C1": {
            "m1": massas["m1"] + massas["A"] + massas["1"] + massas["7"] + massas["F"],
            "m2": massas["m2"] + massas["B"] + massas["D"] + massas["G"]
        },

        "C2": {
            "m1": massas["m1"] + massas["A"] + massas["1"] + massas["7"] + massas["G"],
            "m2": massas["m2"] + massas["B"] + massas["D"] + massas["F"]
        },

        "C3": {
            "m1": massas["m1"] + massas["A"] + massas["1"] + massas["F"] + massas["G"],
            "m2": massas["m2"] + massas["B"] + massas["D"] + massas["7"]
        },

        "C4": {
            "m1": massas["m1"] + massas["A"] + massas["1"] + massas["B"] + massas["F"],
            "m2": massas["m2"] + massas["D"] + massas["7"] + massas["G"]
        },

        "C5": {
            "m1": massas["m1"] + massas["A"] + massas["1"] + massas["D"] + massas["B"],
            "m2": massas["m2"] + massas["F"] + massas["7"] + massas["G"]
        },

        "C6": {
            "m1": massas["m1"] + massas["A"] + massas["D"] + massas["1"] + massas["7"],
            "m2": massas["m2"] + massas["B"] + massas["F"] + massas["G"]
        }
    }
    g = 9.80665
    R = 10.005/200
    M = configuracoes["C1"]["m1"] + configuracoes["C1"]["m2"]

    uR = 0.00005
    uM = 0.0003

    coisa = []
    coisa_erros = []

    for j in range(4):
        aceleracoes = []
        deltamassa = []
        xerr = []
        for i in range(6):
            x, y = [data[i + 6*j]["tempo"], data[i + 6*j]["altura"]]

            left, right = get_espacamento(data[i + 6*j], 'altura', th)

            (a1, b1, c1), cov = np.polyfit(x.tolist()[left:right+1], y.tolist()[left:right+1], 2, cov=True)
            erros = np.sqrt(np.diag(cov))
            xerr.append(erros[0])
            
            deltamassa.append(configuracoes[f"C{i+1}"]["m1"] - configuracoes[f"C{i+1}"]["m2"])
            aceleracoes.append(abs(2*a1))

        
        (a2, b2), cov = np.polyfit(aceleracoes, deltamassa, 1, cov=True)
        erros = np.sqrt(np.diag(cov))
        if opcao == "inercia":
            num = 4
            inercia = a2 * g * pow(R, 2) - M * pow(R, 2)
            coisa.append(float(round(Decimal(inercia), num)))

            uI = pow((g*pow(R, 2)), 2) * pow(erros[0], 2) + (2*a2*g*R-2*M*R)*pow(uR, 2) + pow(pow(-R, 2), 2)*pow(uM, 2)
            uI = float(round(Decimal(pow(uI, 1/2)), 4))
            coisa_erros.append(uI)
        elif opcao == "torque":
            num = 4
            torque = b2 * g * R
            coisa.append(float(round(Decimal(torque), num)))

            uT = pow(g*R*erros[1], 2) + pow(b2*g*uR, 2)
            uT = float(round(Decimal(pow(uT, 1/2)), 4))
            coisa_erros.append(uT)

    return [coisa, coisa_erros]

def calcularAceleracoes(data, th):
    acels = []
    acels_sig = []
    for i in range(len(data)):
        x, y = [
                data[i]['tempo'],
                data[i]['altura']
            ]

        left, right = get_espacamento(data[i], 'altura', th)

        dT = x.tolist()[left:right+1][-1] - x.tolist()[left:right+1][0]
        dH = abs(y.tolist()[left:right+1][-1] - y.tolist()[left:right+1][0])
        acels.append(float(round(Decimal(2 * dH/pow(dT, 2)), 1)))

        ua = 4 * pow(10, -6)/pow(dT, 4) + 27.2 * pow(dH, 2) * pow(10, -3)/pow(dT, -3)
        ua = float(round(Decimal(pow(ua, 1/2)), 1))

        acels_sig.append(ua)
    return [acels, acels_sig]
    
def calcularVelocidadeAngular(data, th):
    def media(lista):
        soma = 0
        for i in lista:
            soma += i
        return soma/len(lista)

    ws = []
    wsig = []
    for i in range(len(data)):
        x, y = [
                data[i]['tempo'],
                data[i]['altura']
            ]

        left, right = get_espacamento(data[i], 'altura', th)

        dT = (x.tolist()[left:right+1][-1] - x.tolist()[left:right+1][0])/60 # em minutos
        dH = abs(y.tolist()[left:right+1][-1] - y.tolist()[left:right+1][0])
        
        n = dH/31.4
        ws.append(2*3.14*n/dT)
        
        uH = 1/1000
        uT = (1/24)/60

        uw = pow(uH, 2)/pow(5*dT, 2) + pow(dH, 2)*pow(uT, 2)/(pow(5, 2) * pow(dT, 4)) 
        wsig.append(uw)

    return [round(media(ws), 4), round(media(wsig), 4)]

def generate_graphs3(inercia, torque):
    # Deixar a ordem crescente
    y = [2, 3, 4, 5]
    inercias = inercia[0][::-1]
    inercieaserr = inercia[1][::-1]

    torques = torque[0][::-1]
    torqueserr = torque[1][::-1]

    fig, (ax1, ax2) = plt.subplots(1, 2, sharey=True)
    ax1.tick_params(right=True, top=True, direction='in')
    ax2.tick_params(right=True, top=True, direction='in')

    ax1.set_yticks([])
    ax1.set_xlabel("Momento de inércia [kg*m²]")
    ax2.set_xlabel("Torque [N*m]")
    ax2.set_yticks([])
    for i in range(len(inercias)):
        ax1.errorbar(inercias[i], y[i], xerr=inercieaserr[i], fmt='o', capsize=3, ecolor='k', label=f"Altura H{i+2}")

    M = 1.9346
    uM = pow(10, -4)
    uR = 5*pow(10,-5)
    R = 10.005/200
    
    I = M*pow(R,2)
    uI = pow(R, 4)*pow(uM, 2) + 4*pow(R,2)*pow(M,2)*pow(uR, 2)
    uI = pow(uI, 1/2)

    ax1.errorbar(I, 6, xerr=uI, fmt='o', capsize=3, ecolor='k', label="Valor teórico previsto")
    ax1.legend(loc="lower right")


    for i in range(len(torques)):
        ax2.errorbar(torques[i], y[i], xerr=torqueserr[i], fmt='o', capsize=3, ecolor='k', label=f"Altura H{i+2}")

    T = 0.1/1000
    ax2.errorbar(T, 6, fmt='o', capsize=3, ecolor='k', label="Valor teórico previsto")

    ax2.legend(loc="lower right")
    
    plt.suptitle("Valores obtidos")
    fig.set_size_inches(12, 6)
    fig.tight_layout()
    fig.savefig(f'Gráfico de I e T.png')
    plt.close(fig=fig)

dados = get_dados()
th = 0.5/100
generate_graphs1(dados, th)
generate_graphs2(dados, th)
generate_graphs3(calcular(dados, th, "inercia"), calcular(dados, th, "torque"))
aceleracoes = calcularAceleracoes(dados, th)
print("Acelerações:")
for i in range(len(aceleracoes[0])):
    print(f"H{5-(i//6)} C{(i%6)+1}:", aceleracoes[0][i], "±", aceleracoes[1][i], "m/s²")

w = calcularVelocidadeAngular(dados, th)
print("Vel. Ang.:", w[0], "±", w[1], "RPM")
inercias = calcular(dados, th, "inercia")
print("Inércias:")
for i in range(len(inercias[0])):
    print(f"H{5-i}:", inercias[0][i], "±", inercias[1][i], "kg*m²")

torques = calcular(dados, th, "torque")
print("Torque:")
for i in range(len(torques[0])):
    print(f"H{5-i}:", torques[0][i], "±", torques[1][i], "N*m")
