

#!/usr/bin/python                                                                                                                                                                                                                                                                                                                                                                                                     
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\
-----------------                                                                                                                                                                                                                                                                                                                                                                                                     
# Created by: J. G. Fernandez-Trincado                                                                                                                                                                                                                                                                                                                                                                                
# Last update: 2015, December 16                                                                                                                                                                                                                                                                                                                                                                                      
# Program: Atmosphere models                                                                                                                                                                                                                                                                                                                                                                                          
# This program was developed and maintained by J. G. Fernandez-Trincado.                                                                                                                                                                                                                                                                                                                                              
# If you need some support to run this program, or if you have some comments and suggestions, please do not hesitate to contact me to: jfernandez@obs-besancon.fr or jfernandezt87@gmail.com                                                                                                                                                                                                                          
# Description: "MaincoloursPy.py" was developed to compile colour grids from the France Allard model available online. Main colour files can be constructed from source files, which will be used by the Besancon galaxy model.                                                                                                                                                                                       
# Instructions:                                                                                                                                                                                                                                                                                                                                                                                                       
# System requirements:                                                                                                                                                                                                                                                                                                                                                                                                
# -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------\
-----------------                                                                                                                                                                                                                                                                                                                                                                                                     

import numpy as np
import scipy as sc
import pylab as plt
import urllib2

BTSETTL_files = [
'colmag.BT-Settl.server.JOHNSON.Vega',    # Johnson filters                                                                                                                                                                                                                                                                                                                                                           
'colmag.BT-Settl.server.2MASS.Vega',      # 2MASS filters                                                                                                                                                                                                                                                                                                                                                             
'colmag.BT-Settl.server.SDSS.Vega',       # SDSS  filters                                                                                                                                                                                                                                                                                                                                                             
'colmag.BT-Settl.server.SPITZER.Vega',    # SPITZER filters                                                                                                                                                                                                                                                                                                                                                           
'colmag.BT-Settl.server.GAIA.Vega',       # GAIA filters                                                                                                                                                                                                                                                                                                                                                              
'colmag.BT-Settl.server.CFHT.Vega',       # WIRCAM + MEGACAM filters                                                                                                                                                                                                                                                                                                                                                  
'NAME-next1',
'NAME-next2',
'NAME-next3',
'NAME-next4',
'NAME-next5'
]

BTSurl = 'https://phoenix.ens-lyon.fr/Grids/BT-Settl/CIFIST2011bc/COLORS/'

# Reading data ...                                                                                                                                                                                                                                                                                                                                                                                                    
# The system read by default the system filters in "BTSETTL_files", is the users need another system it can be add manually in "BTSETTL_files", i.e., you only need to append the file name in a new line.                                                                                                                                                                                                            

B1 = sc.genfromtxt(urllib2.urlopen(BTSurl+BTSETTL_files[0]),comments='!',skip_header=19,names=True,usecols=("Teff","Logg","MH","aH","U","B","V","R","RI","IJ","JK","KL","KLL","KM"))              # Johnson filters                                                                                                                                                                                                   
B2 = sc.genfromtxt(urllib2.urlopen(BTSurl+BTSETTL_files[1]),comments='!',skip_header=19,names=True,usecols=("Teff","Logg","MH","aH","J","H","K"))                                                 # 2MASS filters                                                                                                                                                                                                     
B3 = sc.genfromtxt(urllib2.urlopen(BTSurl+BTSETTL_files[2]),comments='!',skip_header=19,names=True,usecols=("Teff","Logg","MH","aH","u","g","r","i" ,"z"))                                        # SDSS  filters                                                                                                                                                                                                     
B4 = sc.genfromtxt(urllib2.urlopen(BTSurl+BTSETTL_files[3]),comments='!',skip_header=19,names=True,usecols=("Teff","Logg","MH","aH","IRAC1","IRAC2","IRAC3","IRAC4","MIPS24","MIPS70","MIPS160")) # SPITZER filters                                                                                                                                                                                                   
B5 = sc.genfromtxt(urllib2.urlopen(BTSurl+BTSETTL_files[4]),comments='!',skip_header=19,names=True,usecols=("Teff","Logg","MH","aH","G_RSV","G","G_BP","G_RP"))                                   # GAIA filters                                                                                                                                                                                                      
B6 = sc.genfromtxt(urllib2.urlopen(BTSurl+BTSETTL_files[5]),comments='!',skip_header=19,names=True,usecols=("Teff","Logg","MH","aH","U","G","R","I",10,11,12,13,14))                              # (U,G,R,I,Z',Y',J',H',Ks'), WIRCAM + MEGACAM filters                                                                                                                                                               

# Creating the master file ...                                                                                                                                                                                                                                                                                                                                                                                        

master_  = [
{'Teff':B1['Teff'], 'Logg':B1['Logg'],'MH':B1['MH'],'aH':B1['aH'],'U':B1['U'], 'B':B1['B'], 'V':B1['V'], 'R':B1['R'],'I':B1['R']-B1['RI'],'L':B1['R']-B1['RI']-B1['IJ']-B1['JK']-B1['KL'],'LL':B1['R']-B1['RI']-B1['IJ']-B1['JK']-B1['KLL'],'M':B1['R']-B1['RI']-B1['IJ']-B1['JK']-B1['KM']},  # Johnson                                                                                                              
{'Teff':B2['Teff'], 'Logg':B2['Logg'],'MH':B2['MH'],'aH':B2['aH'],'J':B2['J'], 'H':B2['H'], 'K':B2['K']},                                                                                                                                                           # 2MASS                                                                                                                                           
{'Teff':B3['Teff'], 'Logg':B3['Logg'],'MH':B3['MH'],'aH':B3['aH'],'u':B3['u'],'g':B3['g'],'r':B3['r'],'i':B3['i'] ,'z':B3['z']},
{'Teff':B4['Teff'], 'Logg':B4['Logg'],'MH':B4['MH'],'aH':B4['aH'],'36':B4['IRAC1'],'45':B4['IRAC2'],'58':B4['IRAC3'],'80':B4['IRAC4'],'24':B4['MIPS24'],'70':B4['MIPS70'],'160':B4['MIPS160']},
{'Teff':B5['Teff'], 'Logg':B5['Logg'],'MH':B5['MH'],'aH':B5['aH'],'G_RSV':B5['G_RSV'],'G':B5['G'],'G_BP':B5['G_BP'],'G_RP':B5['G_RP']},
{'Teff':B6['Teff'], 'Logg':B6['Logg'],'MH':B6['MH'],'aH':B6['aH'],'U2':B6['U'],'G2':B6['G'],'R2':B6['R'],'I2':B6['I'],'Z2':B6['PR'],'Y2':B6['Z_1'],'J2':B6['Y'],'H2':B6['J'],'Ks2':B6['H']}
]

header = []
init_  = 0

for ml in np.arange(len(master_)):

        hkey = master_[ml].keys()
        header = np.append(header, hkey)

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

                                        if np.size(outdata) != np.size(header): pass
                                        else:
                                                init_ += 1
                                                if init_ == 1:     sc.savetxt(files_out, outdata, fmt='%10.3f',header=' '.join(header.tolist()))
                                                else:              sc.savetxt(files_out, outdata, fmt='%10.3f')

                                else: pass















