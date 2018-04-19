#!/usr/bin/env python

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
#from dec_to_time import dec_to_time as dtt
#from read_cut import read_cut
from datetime import timedelta
from math import floor
from scipy.stats import mode

mpl.rcParams["savefig.directory"] = './'

def _parse_header_time(date, time): 
	""" Return datetime object from date and time fields of header. """ 
	if time is not None: 
		date = date +'T' + time
	return parse_time(date)
def movingaverage(interval, window_size):
	        window = np.ones(int(window_size))/float(window_size) 
	        return np.convolve(interval, window, 'same')

path = './'
with open(path+'fitlistcall140.txt', "rb") as f:#fitlistcall140.txt
    content = f.readlines()
pd = open(path+'peakdata.txt','a+')
for line in content:
    #SE NECESITA LEER EL ID DEL EVENTO PARA GENERAR FECHAS.
    eid = str(line.split()[0])
    fit =str(line.split()[1])
    yyyy = (eid[0:4])
    m = (eid[4:6])
    d = (eid[6:8])
    fitlist = [i for i in fit.split(',')]
    callisto=[]
    t_callisto=[]
    if int(eid) == 201709041719:
            findex0=106
            findex1=124
    elif int(eid) > 201511041343:
            findex0=89
            findex1=94
    elif int(eid) <= 201511041343:
            findex0=130
            findex1=135
    print eid,fitlist,type(fitlist)
    print findex0,findex1,'   findex'
    for f in fitlist:
        
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
    fcall=[]
    for i in callisto:
            fcall.append(floor(i))
    bgcall=int(mode(fcall)[0])
    for i in callisto:
            call.append((i-bgcall))
    plt.plot(call)
    plt.title(eid)
    plt.show()
    crms1=int(raw_input('primer indice para rms    '))
    crms2=int(raw_input('segundo indice para rms   '))
    cmaxi=int(raw_input('maximo de la senal   '))
    newbg=[floor(b) for b in call[crms1:crms2+1]]
    rmsbg=int(mode(newbg)[0])
    newcall=[ni-rmsbg for ni in call]
    crms=np.std(newcall)
    maxval = call[cmaxi]-rmsbg
    csn=(maxval/crms)
    print crms,'  rms'
    print maxval, '   max val'
    print t_callisto[cmaxi],'   max time'
    pd.write(eid+'\t'+"%.2f" % crms+'\t'+"%.2f" % maxval+'\t'+"%.2f" % csn+'\t'+str(t_callisto[cmaxi])+'\n')
    #lo que se escribe es idDelEvento, rmsDeCallisto, senalMaximaDelEvento, SNdeCallisto,tiempo del maximo.
    
        
        
        
        
