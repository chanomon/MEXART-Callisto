#!/usr/bin/env python

#file_path=["MEXART_20151104_133000_59.fit"]
#start='13:30'
#end='13:45'
#    if file.endswith("-0.TMSERIES.txt"):	#checar que canal se esta usando 
#        mex_v.append(float(str_v)+5.6)#*10.0)

import os
from readcol import fgetcols 
import numpy as np
from math import fmod
from math import exp
import matplotlib.pyplot as plt
from matplotlib import dates
from astropy.io import fits
from sunpy.time import parse_time
import pylab as plb
from scipy.optimize import curve_fit
from scipy import asarray as ar,exp
import datetime as dt
from dec_to_time import dec_to_time as dtt

from datetime import timedelta


def _parse_header_time(date, time): 
	""" Return datetime object from date and time fields of header. """ 
	if time is not None: 
		date = date +'T' + time
	return parse_time(date)

def movingaverage(interval, window_size):
	        window = np.ones(int(window_size))/float(window_size) 
	        return np.convolve(interval, window, 'same')

###############################################################
#Periodo de tiempo
##############################################################
path = './'		#checar path, #se tiene que correr en la carpeta contenedora de los archivos

files = []
'''
start='16:00:50'
end='16:14:10'

hh_start, mm_start ,ss_start= start.split(':')
hh_end, mm_end, ss_start = end.split(':')

# los tiempos se pasan a horas decimales
start_flag=float(hh_start)+ float(mm_start)/60.0 + float(ss_start)/3600.
end_flag=float(hh_end)+ float(mm_end)/60.0 + float(ss_start)/3600.

print 'start: ',start_flag
print 'end:  ', end_flag
'''
	
	


#########################################################################
##parte de MEXART
#########################################################################



######################################################################
##obtencion de la fecha a partir del nombre del archivo
######################################################################

for file in os.listdir(path):
    if file.endswith("mexcut.dat"):	#checar que canal se esta usando 
        files.append(file)
#print 'number of mexart files'+str(len(files))
files= sorted(files) #se ordenan los archivos

#fig = plt.figure()
#ax = plt.subplot(111)

stream_time = []
stream_v = []
for file in files:
    splits = file.split('-')
    yyyy = (splits[0])
    print splits
    m = (splits[1])
    d = (splits[2])

######################################################################
##Comentar a partir de aqui para no volver a recortar datos de MEXART
######################################################################
'''
##################################################################
## seccion que guarda el recorte de los datos en un archivo nuevo
##################################################################

    g = open(path+year+'-'+month+'-'+day+'-event.dat','w')
    
    with open(path+file, "rb") as f:
        for i in range(10):
            f.readline()
        content = f.readlines()
    print 'empezando a leer datos de mexart'    
    stream_by_day_time=[]
    stream_by_day_v=[]
    for line in content:
        str_time, str_v = line.split()
        time = float(str_time)
        v = float(str_v)
        if start_flag <= time and time <= end_flag:
            g.write(str_time +'\t'+ str_v+'\n')
            stream_by_day_time.append(time)
            stream_by_day_v.append(v)
    #stream_time.append(stream_by_day_time)
    #stream_v.append(stream_by_day_v)
    g.close()
    for i in range(len(stream_by_day_v)):
    	stream_by_day_v[i]=(stream_by_day_v[i]+6.4)*3.0	#correccion de voltaje
    plt.plot(stream_by_day_time,stream_by_day_v,linewidth=1.5,label='MEXART',color='r')
#333333333333333333333333333333    
#Termina parte que debe estar comentada
#333333333333333333333333333333
'''
	

#############################################
##Abrir archivo recortado para graficarlo
#############################################

for file in os.listdir(path):
    if file.endswith("mexcut.dat"):	#checar que canal se esta usando 
        mexartf=file
with open(path+mexartf, "rb") as f:
        
        content = f.readlines()    

mex_time=[]
mex_v=[]
for line in content:
        str_time, str_v = line.split()
        mex_time.append(float(str_time))
        mex_v.append(((float(str_v)+6.36)*45.0)-128+54)#escalamiento para comparar con callisto
#print mex_time[0]
#print mex_v[0]
first_time=dtt(mex_time[0])
datetime = []
hh,mm,ss,ms=int(first_time[0:2]),int(first_time[3:5]),int(first_time[6:8]),int(first_time[9:])
start_object = dt.datetime(year = int(yyyy),month=int(m),day=int(d),hour=hh,minute=mm,second=ss,microsecond=ms)
datetime.append(start_object)
for i in range(len(mex_time)):
	if i==len(mex_time)-1:
			break
	else:	
		delta = dt.timedelta(microseconds=(mex_time[i+1]-mex_time[i])*3600*1000000)
		datetime.append(datetime[i]+delta)

#Parte de Callisto
#################################################################

callisto=[]
t_callisto=[]
file_path=["MEXART_20180301_220000_59.fit"]
for i in file_path:
        
	file_path=i#raw_input('Enter your input file   ')
	
	fl = fits.open( file_path)
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
		#x_time[i]=x_time[i]#+0.07-0.0007	#correccion de tiempo en callisto
		for j in range(143,183):#131,133 #(126,138)para ver frecuencias de puschino
			suma = suma + data[j][index]
				#print "excluding"	
		#light_curve.append(suma)#-284.0)  #se comenta esta linea para ahorrar un paso
                callisto.append((suma/100 -286)*5+1090)   # se resta para poner la senal de Callisto a 0
                t_callisto.append(x_time[index])


################## rms de MEXART
'''
plt.plot(mex_v)
plt.show()
irms=int(raw_input('indice inicio rms	'))
frms=int(raw_input('indice final rms	'))

max_mex = max(mex_v)    
max_mex_t = datetime[mex_v.index(max_mex)]
rms_mex = np.std(mex_v[irms:frms])
StoN = max_mex/rms_mex
print 'el max de intensidad es:  ',max_mex
print 'el tiempo del max es:  ',max_mex_t
print 's/n es:	', StoN
print 'el rms de mexart es:	', rms_mex    
'''



fig = plt.figure()
ax = fig.add_subplot(1,1,1)
plt.plot(t_callisto,callisto,'r',label='callisto',linewidth=1.5)
plt.plot(datetime,mex_v,'b',label='MEXART',linewidth=1.5)	

#ax.xaxis.set_major_locator(dates.MinuteLocator(interval=3))
ax.xaxis.set_major_formatter(dates.DateFormatter('%H:%M:%S'))
plt.xticks(rotation=45)



plt.legend()
plt.title('MEXART + CALLISTO '+yyyy+'-'+m+'-'+d)
plt.xlabel('UTC time')
plt.ylabel('intensity')
plt.subplots_adjust(bottom=.2)
plt.grid()
#fig.savefig("plot-mexart-data.eps", format="eps")

plt.show()


