#!/usr/bin/env python
##se recortan los archivos de mexart y de callisto para dejar
# solamente la parte del evento
import os
from readcol import fgetcols 
from matplotlib import dates
from astropy.io import fits
from sunpy.time import parse_time
from datetime import datetime




def _parse_header_time(date, time): 
	""" Return datetime object from date and time fields of header. """ 
	if time is not None: 
		date = date +'T' + time
	return parse_time(date)

def movingaverage(interval, window_size):
	        window = np.ones(int(window_size))/float(window_size) 
	        return np.convolve(interval, window, 'same')

def read_cut(start,end):
###############################################################
#Periodo de tiempo
##############################################################
	#path = './'
	#start='22:00'
	#end='22:14'
	
	hh_start, mm_start = start.split(':')
	hh_end, mm_end = end.split(':')
	#
	## los tiempos se pasan a horas decimales
	start_flag=float(hh_start)+ float(mm_start)/60.0
	end_flag=float(hh_end)+ float(mm_end)/60.0
	#
	print 'start: ',start_flag
	print 'end:  ', end_flag
	
	
	#########################################################################
	##parte de MEXART
	#########################################################################
	
	
	
	######################################################################
	##obtencion de la fecha a partir del nombre del archivo
	######################################################################
	for file in os.listdir():
		if file.endswith("TMSERIES.txt"):	#checar que canal se esta usando  y checar la terminacion del archivo
	        	mexartf=file
	
	stream_time = []
	stream_v = []
	
	splits = mexartf.split('-')
	year = splits[0]
	month = splits[1]
	day = splits[2]
	
	######################################################################
	##Comentar a partir de aqui para no volver a recortar datos de MEXART
	######################################################################
	
	##################################################################
	## leyendo datos, recortando parte del evento y guardando
	##################################################################
	
	g = open(path+year+'-'+month+'-'+day+'-mexcut.dat','w')
	    
	with open(mexartf, "rb") as f:
		for i in range(10): #checar donde empiezan los datos en casos cercanos a los extremos de tiempo
			f.readline()
			print f.readline(),i
	
	        content = f.readlines()
		print 'empezando a leer datos de mexart'    
	    	for line in content:
	        	str_time, str_v = line.split()
		        time = float(str_time)
	        	v = float(str_v)
	        	if start_flag <= time and time <= end_flag:
	        		g.write(str_time +'\t'+ str_v+'\n')
	
	g.close()
	print 'se leyeron y guardaron recorte de datos de MEXART'

	
