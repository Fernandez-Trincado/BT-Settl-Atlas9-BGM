#!/usr/bin/python                                                                                                                                                                                                                                                                                                                  
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\
----------------------------------------------------------------------------------------------------                                                                                                                                                                                                                               
# Created by: J. G. Fernandez-Trincado                                                                                                                                                                                                                                                                                             
# Last update: 2015, December 16                                                                                                                                                                                                                                                                                                   
# Program: Atmosphere models                                                                                                                                                                                                                                                                                                       
# This program was developed and maintained by J. G. Fernandez-Trincado.                                                                                                                                                                                                                                                           
# If you need some support to run this program, or if you have some comments and suggestions, please do not hesitate to contact me to: jfernandez@obs-besancon.fr or jfernandezt87@gmail.com                                                                                                                                       
# Description: "MaincoloursPy.py" was developed to compile colour grids from the France Allard model available online. Main colour files can be constructed from source files, which will be used by the Besancon galaxy model.                                                                                                    
# Instructions:                                                                                                                                                                                                                                                                                                                    
# System requirements:                                                                                                                                                                                                                                                                                                             
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\
----------------------------------------------------------------------------------------------------                                                                                                                                                                                                                               

import numpy as np
import scipy as sc
import pylab as plt
import urllib2

BTSETTL_files = [
'colmag.BT-Settl.server.JOHNSON.Vega',
'colmag.BT-Settl.server.2MASS.Vega',
'colmag.BT-Settl.server.SDSS.Vega',
'colmag.BT-Settl.server.SPITZER.Vega',
'colmag.BT-Settl.server.GAIA.Vega'
]

BTSurl = 'https://phoenix.ens-lyon.fr/Grids/BT-Settl/CIFIST2011bc/COLORS/'

B1 = sc.genfromtxt(urllib2.urlopen(BTSurl+BTSETTL_files[0]),comments='!',skip_header=19,names=True,usecols=("Teff","Logg","MH","aH","U","B","V","R","RI","IJ","JK","KL","KLL","KM")) # Johnson system ...                                                                                                                          
B2 = sc.genfromtxt(urllib2.urlopen(BTSurl+BTSETTL_files[1]),comments='!',skip_header=19,names=True,usecols=("Teff","Logg","MH","aH","J","H","K"))                                    # 2MASS system ...                                                                                                                            

# Sequence of system filters. For example: Johnson + 2MASS + NAME ; where NAME: is another filter system ...                                                                                                                                                                                                                       
# "master_":                                                                                                                                                                                                                                                                                                                       

master_  = [
{'Teff':B1['Teff'], 'Logg':B1['Logg'],'MH':B1['MH'],'aH':B1['aH'],'UB':B1['U']-B1['B'], 'BV':B1['B']-B1['V'], 'VR':B1['V']-B1['R'], 'VI':B1['V']-B1['R']-B1['RI'],'VK':B1['V']- B1['R']-B1['RI']-B1['IJ']-B1['JK'],'IK':B1['IJ']+B1['JK'],'JL':B1['JK']+B1['KL'],'JL2':B1['JK']+B1['KLL'],'KM':B1['KM']}, # Johnson                
{'Teff':B2['Teff'], 'Logg':B2['Logg'],'MH':B2['MH'],'aH':B2['aH'],'JH':B2['J']-B2['H'], 'HK':B2['H']-B2['K'], 'JK':B2['J']-B2['K']}                                                                                                                                                                       # 2MASS                  
]

files_out = open('Main.txt','a')

for alpha in np.unique(B1['aH']): # alpha range                                                                                                                                                                                                                                                                                    

        for MH in np.unique(B1['MH']): # metallicity range                                                                                                                                                                                                                                                                         

                for LOGG in np.unique(B1['Logg']): # logg range                                                                                                                                                                                                                                                                    

                        for TEFF in np.unique(B1['Teff']):  # Teff range, reference Johnson                                                                                                                                                                                                                                        

                                outdata = []

                                for l in np.arange(len(master_)):

                                        mask = (master_[l]['Teff']==TEFF) & (master_[l]['aH']==alpha) & (master_[l]['MH']==MH) & (master_[l]['Logg']==LOGG) # Reference for mater files                                                                                                                                            

                                        if (np.size(master_[l]['Teff'][mask]) != 0 ):

                                                key = master_[l].keys()

                                                for k in np.arange(len(key)):

                                                        outdata = np.append( outdata , master_[l][key[k]][mask])

                                        else: pass

                                if np.size(outdata) != 0:

                                        outdata = np.column_stack((outdata))
                                        sc.savetxt(files_out, outdata, fmt='%10.3f')
                                else: pass


