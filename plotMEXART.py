#!/usr/bin/env python

import datetime as dt
from dec_to_time import dec_to_time as dtt
from datetime import timedelta

def read_cutMEX(start,end,mexartf):
###############################################################
#Periodo de tiempo
##############################################################

	######################################################################
	##obtencion de la fecha a partir del nombre del archivo
	######################################################################
        print mexartf
	splits = mexartf.split('-')
	year = splits[0]
	month = splits[1]
	day = splits[2]

        
        
	hh_start, mm_start = start.split(':')
	hh_end, mm_end = end.split(':')
	#
	## los tiempos se pasan a horas decimales
	start_flag=float(hh_start)+ float(mm_start)/60.0
	end_flag=float(hh_end)+ float(mm_end)/60.0

        with open(mexartf, "rb") as f:

        print('imprimiendo header')
	for i in range(10): #checar donde empiezan los datos en casos cercanos a los extremos de tiempo
		f.readline()
		print f.readline(),i
	
	content = f.readlines()
	print 'empezando a leer datos de mexart'

        g = open(raw_input('escribe el nombre del nuevo archivo de MEXART con el siguiente formato yyyymmdd.txt'  ))
        
	for line in content:
	       	str_time, str_v = line.split()
	        time = float(str_time)
	       	v = float(str_v)
	       	if start_flag <= time and time <= end_flag:
	        		g.write(str_time +'\t'+ str_v+'\n')
	
	g.close()
	print 'se leyeron datos y se guardo recorte de datos de MEXART'

def readplot_shortMEXART(shortmexarfile):
        shortmexartfile.split(".")
        date = splits[0]
        yyyy = int((date[0:4]))
        mm = int(date[4:6])
        dd = int(date[6:8])
##################
        with open(shortmexartfile, "rb") as f:
        
        content = f.readlines()    

        mex_time=[]
        mex_v=[]
        for line in content:
                """
                str_time, str_v = line.split()
                mex_v.append(float(str_v))#escalamiento para comparar con callisto
                hh = float(str_time)//1
                mf = float(str_time)%1 * 60
                mm = (mf)//1
                sf = mf%1 * 60
                ss = sf // 1
                ms = sf%1*1000000 #geting microseconds
                """
                ##lo estaba haciendo como en las lineas comentadas pero seria mas rapido calcular las diferecias entre los microsegundos y sumarlo al timepo anterior no?
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
