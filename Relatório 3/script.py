import numpy as np
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
    
def graficoGeral(calibracao, tuboaa, tuboaf, tuboff, lim):
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
    ax1.plot(tuboaa["frequency (Hz)"], tuboaa["audio amplitude (a.u.)"]/calibracao["audio amplitude (a.u.)"], label="Tudo aberto-aberto", alpha=0.8)
    
    ax1.set_xlim(0, lim)
    ax1.set_ylabel("Audio amplitude (a.u.)")
    ax1.set_xlabel("Frequency (Hz)")

    ax1.legend(loc="upper left")
    fig1.savefig("1.png")
    plt.close(fig=fig1)

    ax2.plot(calibracao["frequency (Hz)"], calibracao["audio amplitude (a.u.)"], c='r', label="Calibração", alpha=0.8)
    ax2.plot(tuboaf["frequency (Hz)"], tuboaf["audio amplitude (a.u.)"]/calibracao["audio amplitude (a.u.)"], label="Tudo aberto-fechado", alpha=0.8)
    
    ax2.set_xlim(0, lim)
    ax2.set_ylabel("Audio amplitude (a.u.)")
    ax2.set_xlabel("Frequency (Hz)")
    
    ax2.legend(loc="upper left")
    fig2.savefig("2.png")
    plt.close(fig=fig2)

    ax3.plot(calibracao["frequency (Hz)"], calibracao["audio amplitude (a.u.)"], c='r', label="Calibração", alpha=0.8)
    ax3.plot(tuboff["frequency (Hz)"], tuboff["audio amplitude (a.u.)"]/calibracao["audio amplitude (a.u.)"], label="Tudo fechado-fechado", alpha=0.8)
    
    ax3.set_xlim(0, lim)
    ax3.set_ylabel("Audio amplitude (a.u.)")
    ax3.set_xlabel("Frequency (Hz)")
    
    ax3.legend(loc="upper left")
    fig3.savefig("3.png")
    plt.show()
    plt.close(fig=fig3)


def graficoEsperado(comprimento, diametro, v_som, picos, m, tubo, calibracao):
    fig1, ax1 = plt.subplots()
    fig2, ax2 = plt.subplots()

    ax1.scatter(calibracao["frequency (Hz)"], tubo["audio amplitude (a.u.)"]/calibracao["audio amplitude (a.u.)"], s=2, c='orange')
    comprimento_efetivo = comprimento+0.6*m*diametro/2
    n=v_som/(2*(comprimento_efetivo))
    print(f"Frequencia do modo fundamental: {n:.1f} Hz")

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
        
        print(f'Amplitude {resultado.best_values["amplitude"]:.2f}, Center {resultado.best_values["center"]:.2f} +/- {resultado.params["center"].stderr:.2f}, FWHM {2*resultado.best_values["sigma"]:.2f}, estimated n: {resultado.best_values["center"]/n:.2f}')

        ax1.plot(calibracao["frequency (Hz)"],resultado.best_fit)
        frequencias.append(resultado.best_values["center"])
        err_frequencias.append(resultado.params['center'].stderr)

    indices = np.arange(1, len(frequencias) + 1, 1)
    ax2.scatter(indices, frequencias)

    (a, b), cov = np.polyfit(indices, frequencias, 1, cov=True)
    erros = np.sqrt(np.diag(cov))

    poly = np.poly1d([a, b])
    ax2.scatter(indices, poly(indices))
    print(a, b, erros)
    print(a * comprimento_efetivo * 2)
    plt.show()



tubo1 = {
    "comprimento": 0.77,
    "diametro": 0.02,
    "v_som": 343.56,
    "picos": {
        "aberto aberto": [210, 370, 560, 750, 980, 1140, 1320, 1570, 1780, 2010, 2240, 2460, 2680, 2900],
        "aberto fechado": [240, 430, 665, 880, 1070, 1330, 1500, 1725, 1932, 2162, 2378, 2608, 2811],
        "fechado fechado": [215, 470, 660, 910, 1170, 1430, 1640, 1880, 2080, 2350, 2600, 2830]
    }
}

calibracao = pd.read_csv("dados/calibracao.csv")[:]
tuboaa = pd.read_csv("dados/tubo aberto aberto.csv")
tuboaf = pd.read_csv("dados/tubo aberto fechado.csv")
tuboff = pd.read_csv("dados/tubo fechado fechado.csv")
# graficoGeral(calibracao, tuboaa, tuboaf, tuboff, 3000)

# graficoEsperado(tubo1["comprimento"], tubo1["diametro"], tubo1["v_som"], tubo1["picos"]["aberto aberto"], 2, tuboaa, calibracao)
# graficoEsperado(tubo1["comprimento"], tubo1["diametro"], tubo1["v_som"], tubo1["picos"]["aberto fechado"], 1, tuboaf, calibracao)
graficoEsperado(tubo1["comprimento"], tubo1["diametro"], tubo1["v_som"], tubo1["picos"]["fechado fechado"], 0, tuboff, calibracao)
