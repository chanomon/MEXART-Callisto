#!/usr/bin/env python

from astropy.io import fits
###########Este programa imprime las frecuencias con el numero de los canales

file_path = raw_input('nombre del fit  ')
fl = fits.open( file_path)#checar que evento se esta analizando
freqs = fl[1].data['frequency'][0]

for i in range(len(freqs)):
	print '%i %f'%(i,freqs[i])
