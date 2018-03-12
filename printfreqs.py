#!/usr/bin/env python
#This program prints frecuencies of each list index in of the frequencies list, usefull for the analysis.
from astropy.io import fits
###########Este programa imprime las frecuencias con el numero de los canales
def printfreqs(fitpath):
	
	fl = fits.open(fitpath)#checar que evento se esta analizando
	freqs = fl[1].data['frequency'][0]

	for i in range(len(freqs)):
		print '%i %f'%(i,freqs[i])
