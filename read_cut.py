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

###############################################################
#Periodo de tiempo
##############################################################
path = './'
start='22:00'
end='22:14'

hh_start, mm_start = start.split(':')
hh_end, mm_end = end.split(':')

# los tiempos se pasan a horas decimales
start_flag=float(hh_start)+ float(mm_start)/60.0
end_flag=float(hh_end)+ float(mm_end)/60.0

#print 'start: ',start_flag
#print 'end:  ', end_flag


#########################################################################
##parte de MEXART
#########################################################################



######################################################################
##obtencion de la fecha a partir del nombre del archivo
######################################################################
for file in os.listdir(path):
	if file.endswith("TMSERIES.txt"):	#checar que canal se esta usando 
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
	for i in range(10):
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
'''   
    
#################################################################
#Parte de Callisto
#################################################################

callisto=[]
t_callisto=[]
file_path=['MEXART_20150929_191556_59.fit', 'MEXART_20150929_193056_59.fit']
for i in file_path:
        
	file_path=i#raw_input('Enter your input file   ')
	
	fl = fits.open( file_path)
	data = fl[0].data
	axes = fl[1]
	header = fl[0].header
	time= axes.data['time'][0]
	start = _parse_header_time( header['DATE-OBS'], header.get('TIME-OBS',header.get('TIME$_OBS'))) 
	end = _parse_header_time(header['DATE-END'], header.get('TIME-END', header.get('TIME$_END')))
	
	
	start_time = header.get('TIME-OBS',header.get('TIME$_OBS'))
	end_time = header.get('TIME-END', header.get('TIME$_END'))
	#print type(start_time), type(end_time)
	
	x_time = []
	#format = '%Y-%m-%d %H:%M:%S'
	
	for tick in time:
		
	        b = start + datetime.timedelta(microseconds=float(tick)*1000000.0) #se obtiene el delta de tiempo para todos los tiempos
	        #print b#!/usr/bin/env python
		
	        
	
	        new_time = b.hour + b.minute / 60. + b.second / 3600. + b.microsecond / 3600000000.	#se obtiene tiempo en decimales
	        #str(b.hour) + ':' + str(b.minute) + ':' + str(b.second) + '.' + str(b.microsecond)
	        x_time.append(new_time)#new_time)# - .07)		se hae una lista de datetimes
	        #print new_time#datetime.timedelta(seconds=float(tick))
                        
	
        
	for index in range(len(data[0])):
		suma=0.0

		for j in range(131,133):#131,133
			suma = suma + data[j][index]
		
                callisto.append(suma)   
                t_callisto.append(x_time[index])
##################################################################
#cortar datos de callisto para el periodo de tiempo indicado y guardando para curva de luz
##################################################################
call = []
t_call = []
h = open(path+year+'-'+month+'-'+day+'-callcut.dat','w')
for i in range(len(callisto)):
	h.write(str(t_callisto[i]) +'\t'+ str(callisto[i])+'\n')

h.close()



'''
