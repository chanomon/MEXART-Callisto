#!/usr/bin/env python
## autor: Elizandro Huipe Domratcheva  ; hdomeli@gmail.com
#Código en python 3para hacer la curva de luz de los dos intrumentos
#Para ejecutar, se debe tener instalados los paquetes indicados abajo
#Adicionalmente se deben tener los archivos *mexcut.dat y *.fit en 
#la misma carpeta que ejecutar este script
#Para escalar la señal de los dos instrumentos, 
#multiplicar o restar/sumar en la linea 170 y 172

import os
from readcol import fgetcols 
import numpy as np
from math import fmod
from math import exp
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import dates
from astropy.io import fits
from sunpy.time import parse_time
import pylab as plb
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import datetime as dt
from dec_to_time import dec_to_time as dtt
from read_cut import read_cut
from datetime import timedelta
from math import floor
from scipy.stats import mode

mpl.rcParams["savefig.directory"] = './'


# In[23]:


def _parse_header_time(date, time): 
    """ Return datetime object from date and time fields of header. """ 
    if time is not None: 
        date = date +'T' + time
    return parse_time(date)

def movingaverage(interval, window_size):
    window = np.ones(int(window_size))/float(window_size) 
    return np.convolve(interval, window, 'same')


# In[31]:





#########################################################################
##parte de MEXART
#########################################################################
######################################################################
##obtencion de la fecha a partir del nombre del archivo
######################################################################
path = './'		#checar path, #se tiene que correr en la carpeta contenedora de los archivos
files = []

for file in os.listdir('./'):
    if file.endswith("mexcut.dat"):	#checar que canal se esta usando 
        mexartf=file
#print 'number of mexart files'+str(len(files))
#files= sorted(files) #se ordenan los archivos

stream_time = []
stream_v = []
splits = mexartf.split('-')
yyyy = (splits[0])
m = (splits[1])
d = (splits[2])

#############################################
##Abrir archivo recortado para graficarlo
#############################################
        
with open(path+mexartf, "rb") as f:
        
        content = f.readlines()    

mex_time=[]
mex_v=[]
for line in content:
        str_time, str_v = line.split()
        mex_time.append(float(str_time))
        mex_v.append(float(str_v))#escalamiento para comparar con callisto
#print mex_time[0]
#print mex_v[0]
first_time=dtt(mex_time[0])
datetime = []
ftsplit=first_time.split(':')
hh,mm,ss,ms=int(ftsplit[0]),int(ftsplit[1]),int(ftsplit[2][0:2]),int(ftsplit[2][3:])
start_object = dt.datetime(year = int(yyyy),month=int(m),day=int(d),hour=hh,minute=mm,second=ss,microsecond=ms)
datetime.append(start_object)
for i in range(len(mex_time)):
    if i==len(mex_time)-1:
        break
    else:	
        delta = dt.timedelta(microseconds=(mex_time[i+1]-mex_time[i])*3600*1000000)
        datetime.append(datetime[i]+delta)
                
#################################################################
#Parte de Callisto
#################################################################
file_path=[]
for file in os.listdir('./'):
    if file.endswith(".fit"):
            file_path.append(file)

callisto=[]
t_callisto=[]
findex0=89
findex1=98
for f in file_path:
        
	#f_path=i#raw_input('Enter your input file   ')
	
    fl = fits.open( f)
    data = fl[0].data
    axes = fl[1]
    header = fl[0].header
    time= axes.data['time'][0]
    frequencies =  axes.data['frequency'][0]
    start = _parse_header_time( header['DATE-OBS'], header.get('TIME-OBS',header.get('TIME$_OBS'))) 
    end = _parse_header_time(header['DATE-END'], header.get('TIME-END', header.get('TIME$_END')))
	
	
    start_time = header.get('TIME-OBS',header.get('TIME$_OBS'))
	
    start_object = dt.datetime(year = int(yyyy),month=int(m),day=int(d),hour=int(start_time[0:2]),minute=int(start_time[3:5]),second=int(start_time[6:8]),microsecond=1000*int(start_time[-3:]))#checar tiempo de inicio
	
    x_time=[]
    delta = dt.timedelta(microseconds=((time[1]-time[0])*1000000))
    x_time.append(start_object+delta)
    for i in range(len(time)):
        if i==len(time)-1:
            break
        else:	
            delta = dt.timedelta(microseconds=(time[i+1]-time[i])*1000000)
            x_time.append(x_time[i]+delta)
	        #str(b.hour) + ':' + str(b.minute) + ':' + str(b.second) + '.' + str(b.microsecond)
	        #x_time.append(new_time)#new_time)# - .07)		se hae una lista de datetimes
	        #print new_time#datetime.timedelta(seconds=float(tick))
                        
    light_curve=[]
    exclude=[]
        
    for index in range(len(data[0])):
        suma=0.0
        for j in range(findex0,findex1):#131,133 #(126,138)para ver frecuencias de puschino
            suma = suma + data[j][index]
        callisto.append((suma))   # se resta para poner la senal de Callisto a 0
        t_callisto.append(x_time[index])


call=[]		
mexart=[]
fcall=[]
fmex=[]

for i in mex_v:
	fmex.append(floor(i)) 
for i in callisto:
	fcall.append(floor(i))
bgmex=int(mode(fmex)[0])
bgcall=int(mode(fcall)[0])
for i in mex_v:
	mexart.append((i-bgmex)) ########################################################3
for i in callisto:
	call.append((i-bgcall))	###############################################
	
labelchain='callisto ['+"%.1f" % frequencies[findex1]+' - '+"%.1f" % frequencies[findex0]+' MHz]'
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.plot(t_callisto,call,'r',label=labelchain,linewidth=1.5)
plt.plot(datetime,mexart,'b',label='MEXART [138.6-140.6 MHz]',linewidth=0.5)	

#ax.xaxis.set_major_locator(dates.MinuteLocator(interval=3))
ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))
plt.xticks(rotation=45)
plt.legend()
plt.title('MEXART + CALLISTO '+yyyy+'-'+m+'-'+d)
plt.xlabel('UTC time')
plt.ylabel('intensity')
plt.subplots_adjust(bottom=.2)
plt.grid()
plt.show()

