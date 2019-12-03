#!/usr/bin/env python3


import os
#from readcol import fgetcols 
import numpy as np
from math import fmod
from math import exp
import matplotlib.pyplot as plt
from astropy.io import fits
import datetime as dt
from datetime import time,date,datetime
from matplotlib import dates as mdates
import matplotlib.ticker as ticker
from matplotlib.dates import AutoDateLocator
import matplotlib as mpl

mpl.rcParams["savefig.directory"] = './'
######################
#parametros del archivo
######################
files =input('escribe la url del espectro Callisto   ')
xtime=[]
specs=[]

fl = fits.open(files)
file_name=files[-29:]
axes = fl[1]
time= axes.data['time'][0]
spectrum=fl[0].data
header = fl[0].header
freqs =  axes.data['frequency'][0]
instrument = header.get('INSTRUME',header.get('INSTRUME'))
start_time = header.get('TIME-OBS',header.get('TIME$_OBS'))
start_object = datetime.strptime(file_name[7:15]+' '+str(start_time)+'000', '%Y%m%d %H:%M:%S.%f')#checar tiempo de inicio

delta = dt.timedelta(microseconds=((time[1]-time[0])*1000000))
xtime.append(start_object+delta)
for i in range(len(time)):
	if i==len(time)-1:
		break
	else:	
		delta = dt.timedelta(microseconds=(time[i+1]-time[i])*1000000)
		xtime.append(xtime[i]+delta)

print(type(spectrum))
########################
#transformacion del espectro
########################
#dates = []

#for i in xtime:
#	dates.append(str(i)[11:19])
nobgdata = spectrum - spectrum.mean(axis=1, keepdims=True) - 1.#4 # subtract mean and add offset (1...50)
nobgdata = nobgdata.clip(-20,50) #(-5,140) limit peak values en esta linea se cambia la escala de colores
data = spectrum#.clip(135,180)
nobgdata = nobgdata * 2500.0/255.0/25.4 # digit->dB
data = data * 2500.0/255.0/25.4

fig = plt.figure()
ax = fig.add_subplot(111)

#plt.xticks(range(len(dates)), dates)

#nobgdata=nobgdata.clip(-20,50)
x_lims = mdates.date2num(xtime)
plt.imshow(nobgdata[:][:192],extent=[x_lims[0],x_lims[-1],round(freqs[-9],2),round(freqs[0],2)],aspect='auto',cmap='jet')#,vmin=0,vmax=10)#nobgdata[:][:192]
ax.xaxis_date()
date_format = mdates.DateFormatter('%H:%M:%S')
#freq_format = ticker.FixedFormatter(freqs)
ax.xaxis.set_major_formatter(date_format)
#ax.yaxis.set_major_formatter(freq_format)
plt.xlabel('Time [UT]')
plt.ylabel('Frequency [MHz]')
#ax.set_yticks(freqs)
#plt.yticks(range(len(freqs)), freqs)2
#ax.set_yticklabels(freqs)
ax.xaxis.set_major_locator(mdates.SecondLocator(interval=180))
#ax.yaxis.set_major_locator(ticker.MultipleLocator(20))
ax.tick_params(axis='x', labelsize=14)
ax.tick_params(axis='y', labelsize=14)


'''
if dates:
        plt.xticks(range(len(dates)), dates)
        plt.yticks(range(len(freqs)), freqs)

	ax.yaxis.set_major_locator(mticker.MultipleLocator(200))
'''
#ax.set_xticklabels(dates)
#ax.set_yticklabels(freqs)
#ax.set_aspect('auto')
#(dates.DateFormatter('%H:%M:%S'))
plt.xticks(rotation=37)
plt.subplots_adjust(bottom=.2)
plt.subplots_adjust(left = .2)
plt.title(instrument+' Radio flux density '+str(start_object)[:10])
plt.grid(linewidth=0.3,linestyle='--',color='black')
plt.show()







