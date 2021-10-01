# -*- coding: utf-8 -*-
"""
Created on Thu Oct 22 15:49:42 2020

@author: Christoph
"""
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import lmfit

cal1= pd.read_csv('dados/calibracao.csv')
#cal2= pd.read_csv('cal1.csv')
#cal3= pd.read_csv('cal3.csv')

tube1=pd.read_csv('dados/tubo aberto aberto.csv')
#tube2=pd.read_csv('tube2.csv')

tube = tube1['audio amplitude (a.u.)'].iloc[1:150]

cal = cal1['audio amplitude (a.u.)'].iloc[1:150]
frequ = cal1['frequency (Hz)'].iloc[1:150]


#Plot data as normal I vs f

fig,ax2 = plt.subplots(1,1)
ax2.plot(frequ,tube,label="Tube") 
ax2.plot(frequ,cal,label="Calibration") 
ax2.set_ylabel('Amplitude (arb. u.)',fontsize=12)
ax2.set_xlabel('Frequency (Hz)',fontsize=12)
ax2.legend(fontsize='small')


fig,ax4 = plt.subplots(1,1)
ax4.plot(frequ,tube/cal,label="Tubasdasdsae") 
ax4.set_ylabel('Amplitude/Calibration (arb. u.)',fontsize=12)
ax4.set_xlabel('Frequency (Hz)',fontsize=12)
ax4.legend(fontsize='small')
#Plot in db

in_db=10*np.log(tube/cal)

fig,ax1 = plt.subplots(1,1)
ax1.plot(frequ,in_db) 
ax1.set_ylabel('Amplitude (dB)',fontsize=12)
ax1.set_xlabel('Frequency (Hz)',fontsize=12)

#ax1.legend(fontsize='small')

plt.tight_layout()
plt.show()

#Fit a Lorenzian on every peak to get the freuquency center
#
# Position is saved in a array together with uncertainty


#print('parameter names: {}'.format(model.param_names))

length_tube= 1.12
diameter_tube = 0.02
m=2
length_corr=(length_tube+0.6*m*diameter_tube/2)
n=346.6*1/(2*(length_corr))
print(f'Fundamental mode at {n:.1f} Hz')

peaks = [143,288,443,587,730,891,1041,1190,1351,1495,1654,1811,1966,2115,2270,2420,2581,2742,2901] 
pos=[]
err_pos=[]

model=lmfit.models.LorentzianModel()

for peak in peaks:
    model.set_param_hint('amplitude',value=100,min=10,max=40000)
    model.set_param_hint('center',value=peak,min=peak-15,max=peak+15)
    model.set_param_hint('sigma',value=15,min=5,max=30)


    param=model.make_params()
    result=model.fit(tube/cal,x=frequ,params=param)
    
    print(result.fit_report())
   # print(result.best_values)
    
    print(f'Amplitude {result.best_values["amplitude"]:.2f}, Center {result.best_values["center"]:.2f} +/- {result.params["center"].stderr:.2f}, FWHM {2*result.best_values["sigma"]:.2f}, estimated n: {result.best_values["center"]/n:.2f}')
    ax4.plot(frequ,result.best_fit)
    pos.append(result.best_values["center"])
    err_pos.append(result.params['center'].stderr)

#Plot data against the harmony index n, make a fit and calculate  the velocity of sound

pos_array=np.array(pos)
index = np.arange(1,20,1)
#Plot data against the harmony index n, make a fit and calculate  the velocity of sound

pos_array=np.array(pos)

print('Mode spacing:')
with np.printoptions(precision=2, suppress=True):
    print(np.diff(pos_array))

index = np.arange(1,20,1)

model2=lmfit.models.LinearModel()
pars = model2.guess(pos_array, x=index)
result2=model2.fit(pos_array,pars,x=index)

speed_of_sound=result2.best_values["slope"]*(2*(length_corr))
un_sos=np.sqrt((2*(length_tube))**2*result2.params['slope'].stderr**2+(4*result2.best_values["slope"])**2*0.005**2+(4*result2.best_values["slope"]*0.6)**2*0.002**2)

#Adapt for the type of resonace used (open-open, closed-open etc...
print(f'Velocity of sound {speed_of_sound:.2f}+/- {un_sos:.2f}')


fig,ax3 = plt.subplots(1,1)

ax3.errorbar(index,pos_array,xerr=0.5,yerr=err_pos,fmt='o',elinewidth=1,capsize=3,capthick=1,ms=3,c='b',ecolor='black')
ax3.plot(index,result2.best_fit,label="Fit")
ax3.plot(index, 346.6*index/(2*(length_tube)),label='Theory')

ax3.text(.4,.20, f' Slope:{result2.best_values["slope"]:.2f} +/- {result2.params["slope"].stderr:.2f} \n Speed of sound: {speed_of_sound:.1f} +/- {un_sos:.2f}',fontsize=12,horizontalalignment='left',
         verticalalignment='top', transform=ax1.transAxes)


ax3.set_ylabel('Position (Hz)',fontsize=12)
ax3.set_xlabel('Index',fontsize=12)
ax3.legend(fontsize=12)




