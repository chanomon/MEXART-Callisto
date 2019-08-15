# MEXART-Callisto
Tools to obtain spectra from callisto and compare it with a radio signal of single frequency
This repo let's you compare two radio sginals, one of the Callisto radiospectrograph and another general signal.
In this case is made up for comparing with MEXART radioantenna signal.
For this program to work you need the data of the same time period, the period of observation could be contained in many files so 
you need all the data files in the same directory where the scripts are located to work.

read-cut.py cuts a piece of the MEXART data, this because MEXART data (one data comprise miliseconds) 
is very dense in time compared with the Callisto data (4 data per second ).
This scripts are made to work with the MEXART data structure.

to create spectrums just run in terminal 'python newspec.py' later, the url or the fit file path will required
