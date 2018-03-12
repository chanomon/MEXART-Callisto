#!/usr/bin/env python

def dec_to_time(decimal):
	hours = int(decimal)
	decmin = (decimal % 1)*60.
	minutes = int(decmin)
	decsec = ( decmin % 1 ) * 60.
	seconds = ( int(decsec))
	microseconds = ( decsec%1 ) * 1000000
	return ("%d:%02d:%02d.%06d" % (hours, minutes, seconds,microseconds))
