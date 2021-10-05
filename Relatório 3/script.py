import numpy as np
from numpy.core.fromnumeric import mean
from numpy.lib.shape_base import vsplit
import pandas as pd
import math
from matplotlib import pyplot as plt
import lmfit

def calibracao(dados):
    fig, ax1 = plt.subplots()
    ax1.plot(dados["frequency (Hz)"], dados["audio amplitude (a.u.)"])
    ax1.set_xlabel("Frequencia (Hz)")
    ax1.set_ylabel("Amplitude (a.u.)")
    plt.show()
    plt.close("all")
    
def graficoGeral(calibracao, tuboaa, tuboaf, tuboff, lim, tipo):
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()

    ax1.grid()
    ax2.grid()
    ax3.grid()

    fig1.set_size_inches(6, 4)
    fig2.set_size_inches(6, 4)
    fig3.set_size_inches(6, 4)
    
    ax1.plot(calibracao["frequency (Hz)"], calibracao["audio amplitude (a.u.)"], c='r', label="Calibração", alpha=0.8)
    ax1.scatter(tuboaa["frequency (Hz)"], tuboaa["audio amplitude (a.u.)"]/calibracao["audio amplitude (a.u.)"], label="Dados brutos", alpha=0.8, s=4)
    
    ax1.set_xlim(0, lim)
    if tipo == 1:
        ax1.set_title("Tubo Aberto-Aberto")
    else:
        ax1.set_title("Helmholtz 1.5L")

    ax1.set_ylabel("Amplitude (a.u.)")
    ax1.set_xlabel("Frequência (Hz)")

    ax1.legend(loc="upper left")

    if tipo == 1:
        fig1.savefig("Tubo AA.png")
    else:
        fig1.savefig("Helmholtz 1.5L.png")

    plt.close(fig=fig1)

    ax2.plot(calibracao["frequency (Hz)"], calibracao["audio amplitude (a.u.)"], c='r', label="Calibração", alpha=0.8)
    ax2.scatter(tuboaf["frequency (Hz)"], tuboaf["audio amplitude (a.u.)"]/calibracao["audio amplitude (a.u.)"], label="Dados brutos", alpha=0.8, s=4)
    
    ax2.set_xlim(0, lim)

    if tipo == 1:
        ax2.set_title("Tubo Aberto-Fechado")
    else:
        ax2.set_title("Helmholtz 1.0L")

    ax2.set_ylabel("Amplitude (a.u.)")
    ax2.set_xlabel("Frequência (Hz)")
    
    ax2.legend(loc="upper left")

    if tipo == 1:
        fig2.savefig("Tubo AF.png")
    else:
        fig2.savefig("Helmholtz 1.0L.png")

    plt.close(fig=fig2)

    ax3.plot(calibracao["frequency (Hz)"], calibracao["audio amplitude (a.u.)"], c='r', label="Calibração", alpha=0.8)
    ax3.scatter(tuboff["frequency (Hz)"], tuboff["audio amplitude (a.u.)"]/calibracao["audio amplitude (a.u.)"], label="Dados brutos", alpha=0.8, s=4)
    
    ax3.set_xlim(0, lim)

    if tipo == 1:
        ax3.set_title("Tubo Fechado-Fechado")
    else:
        ax3.set_title("Helmholtz 0.5L")
    
    ax3.set_ylabel("Amplitude (a.u.)")
    ax3.set_xlabel("Frequência (Hz)")
    
    ax3.legend(loc="upper left")

    if tipo == 1:
        fig3.savefig("Tubo FF.png")
    else:
        fig3.savefig("Helmholtz 0.5L.png")

    plt.close(fig=fig3)

def graficoEsperado(comprimento, diametro, v_som, picos, m, tubo, calibracao, nome):
    lim = 3000

    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    ax1.grid()
    ax2.grid()

    fig1.set_size_inches(6, 4)
    fig2.set_size_inches(6, 4)

    ax1.scatter(calibracao["frequency (Hz)"], tubo["audio amplitude (a.u.)"]/calibracao["audio amplitude (a.u.)"], s=2, c='orange', label="Dados brutos")
    comprimento_efetivo = comprimento+0.6*m*diametro/2
    n=v_som/(2*(comprimento_efetivo))
    print(f"Frequencia do modo fundamental: {n:.1f} Hz")

    ul = 0.0005
    ur = ul

    uL = pow(ul, 2) + 0.36*pow(m, 2)*pow(ur, 2)

    frequencias=[]
    err_frequencias=[]
    modelo = lmfit.models.LorentzianModel()

    for pico in picos:
        modelo.set_param_hint('amplitude',value=100,min=10,max=40000)
        modelo.set_param_hint('center',value=pico,min=pico-20,max=pico+20)
        modelo.set_param_hint('sigma',value=20,min=5,max=40)


        param=modelo.make_params()
        resultado=modelo.fit(tubo["audio amplitude (a.u.)"]/calibracao["audio amplitude (a.u.)"],x=calibracao["frequency (Hz)"],params=param)
        
        # print(resultado.fit_report())
        # print(resultado.best_values)
        
        #print(f'Amplitude {resultado.best_values["amplitude"]:.2f}, Center {resultado.best_values["center"]:.2f} +/- {resultado.params["center"].stderr:.2f}, FWHM {2*resultado.best_values["sigma"]:.2f}, estimated n: {resultado.best_values["center"]/n:.2f}')

        ax1.plot(calibracao["frequency (Hz)"],resultado.best_fit)
        frequencias.append(resultado.best_values["center"])
        err_frequencias.append(resultado.params['center'].stderr)

    ax1.set_title("Fit Lorentziano para os picos dos dados brutos")
    ax1.set_xlim(0, lim)
    ax1.set_xlabel("Frequência (Hz)")
    ax1.set_ylabel("Amplitude (a.u.)")
    ax1.legend(loc="upper left")
    fig1.savefig(f"{nome} Lorentz.png")
    plt.close(fig=fig1)
    
    if nome != "Tubo AF":
        indices = np.arange(1, len(frequencias) + 1, 1)
    else:
        indices = []
        impar = 0
        while len(indices) != len(frequencias):
            if impar % 2 != 0:
                indices.append(impar)
            impar += 1

    ax2.errorbar(indices, frequencias, yerr=err_frequencias, label=f"Frequência x índices", ecolor="k", capthick=1, capsize=3, fmt="o")

    (a, b), cov = np.polyfit(indices, frequencias, 1, cov=True)
    erros = np.sqrt(np.diag(cov))


    poly = np.poly1d([a, b])

    if nome != "Tubo AF":
        vsound = a * comprimento_efetivo * 2
        uv = 4 * pow(comprimento_efetivo, 2) * pow(erros[0], 2) + 4*pow(a,2)*uL
        uv = math.sqrt(uv)
    else:
        print("ASODKASOD")
        vsound = a * comprimento_efetivo * 4
        uv = 16 * pow(comprimento_efetivo, 2) * pow(erros[0], 2) + 16*pow(a,2)*uL
        uv = math.sqrt(uv)

    ax2.plot(indices, poly(indices), label=f"Fit linear\ny = ({round(a, 1)} +- {round(erros[0], 1)})x + ({round(b, 1)} +- {round(erros[1], 1)})\nVelocidade do som: {round(vsound, 1)} +- {round(uv, 1)}", c="r")
    print(f"{vsound} +- {uv}")
    
    ax2.set_title("Fit linear para os picos das frequências")
    ax2.legend(loc="upper left")
    ax2.set_xlabel("Índice")
    ax2.set_ylabel("Frequência (Hz)")
    fig2.savefig(f"{nome} Linear.png")
    plt.close(fig=fig2)

    return [vsound, uv]

def velIncerteza(v1, v2, v3, uv1, uv2, uv3):
    uv = (pow(uv1, 2) + pow(uv2, 2) + pow(uv3, 2))/9
    uv = math.sqrt(uv)
    vm = mean([v1, v2, v3])
    
    s = math.sqrt((abs(v1 - vm) + abs(v2 - vm) + abs(v3 - vm))/2)

    uv = math.sqrt(pow(uv, 2) + pow(s, 2))

    print(f"Vel. Média: {vm} +- {uv}")

def graficoDB(calibracao, tuboaa, tuboaf, tuboff, lim):
    tubos = [tuboaa, tuboaf, tuboff]

    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()
    fig3, ax3 = plt.subplots()

    ax1.grid()
    ax2.grid()
    ax3.grid()

    fig1.set_size_inches(6, 4)
    fig2.set_size_inches(6, 4)
    fig3.set_size_inches(6, 4)

    y1 = []
    y2 = []
    y3 = []

    for i in range(len(tuboaa)):
        y1.append(10 * math.log10(tuboaa["audio amplitude (a.u.)"][i]/calibracao["audio amplitude (a.u.)"][i]))
    ax1.plot(calibracao["frequency (Hz)"], y1)
    
    ax1.set_ylabel("Amplitude (dB)")
    ax1.set_xlabel("Frequência (Hz)")
    ax1.set_title("Intensidade sonora em decibéis para o tubo Aberto-Aberto")

    fig1.savefig("Tubo AA Db.png")
    plt.close(fig=fig1)

    for i in range(len(tuboaf)):
        y2.append(10 * math.log10(tuboaf["audio amplitude (a.u.)"][i]/calibracao["audio amplitude (a.u.)"][i]))
    ax2.plot(calibracao["frequency (Hz)"], y2)

    ax2.set_ylabel("Amplitude (dB)")
    ax2.set_xlabel("Frequência (Hz)")
    ax2.set_title("Intensidade sonora em decibéis para o tubo Aberto-Fechado")

    fig2.savefig("Tubo AF Db.png")
    plt.close(fig=fig2)
    
    for i in range(len(tuboff)):
        y3.append(10 * math.log10(tuboff["audio amplitude (a.u.)"][i]/calibracao["audio amplitude (a.u.)"][i]))
    ax3.plot(calibracao["frequency (Hz)"], y3)
    
    ax3.set_ylabel("Amplitude (dB)")
    ax3.set_xlabel("Frequência (Hz)")
    ax3.set_title("Intensidade sonora em decibéis para o tubo Fechado-Fechado")

    fig3.savefig("Tubo FF Db.png")
    plt.close(fig=fig3)
    

tubo1 = {
    "comprimento": 0.77,
    "diametro": 0.02,
    "v_som": 343.56,
    "picos": {
        "aberto aberto": [220, 360, 550, 750, 980, 1160, 1350, 1570, 1780, 2010, 2240, 2460, 2680, 2900],
        "aberto fechado": [240, 430, 665, 880, 1070, 1330, 1500, 1725, 1932, 2162, 2378, 2608, 2811],
        "fechado fechado": [215, 470, 660, 910, 1170, 1430, 1640, 1880, 2080, 2350, 2600, 2830]
    }
}

calibracao = pd.read_csv("dados/calibracao.csv")
tuboaa = pd.read_csv("dados/tubo aberto aberto.csv")
tuboaf = pd.read_csv("dados/tubo aberto fechado.csv")
tuboff = pd.read_csv("dados/tubo fechado fechado.csv")


calibracaoH = pd.read_csv("dados/helmholtz calibracao.csv")
H1_5 = pd.read_csv("dados/helmholtz 1.5L.csv")
H1_0 = pd.read_csv("dados/helmholtz 1.0L.csv")
H0_5 = pd.read_csv("dados/helmholtz 0.5L.csv")

graficoGeral(calibracao, tuboaa, tuboaf, tuboff, 3000, 1)
graficoGeral(calibracaoH, H1_5, H1_0, H0_5, 3000, 2)

graficoDB(calibracao, tuboaa, tuboaf, tuboff, 3000)

v1, uv1= graficoEsperado(tubo1["comprimento"], tubo1["diametro"], tubo1["v_som"], tubo1["picos"]["aberto aberto"], 2, tuboaa, calibracao, "Tubo AA")
v2, uv2= graficoEsperado(tubo1["comprimento"], tubo1["diametro"], tubo1["v_som"], tubo1["picos"]["aberto fechado"], 1, tuboaf, calibracao, "Tubo AF")
v3, uv3= graficoEsperado(tubo1["comprimento"], tubo1["diametro"], tubo1["v_som"], tubo1["picos"]["fechado fechado"], 0, tuboff, calibracao, "Tubo FF")
velIncerteza(v1, v2, v3, uv1, uv2, uv3)