  1 #!/usr/bin/python
  2 
  3 
  4 #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  5 # Created by: J. G. Fernandez-Trincado                                                                                                                                    //
  6 # Last update: 2015, December 16                                                                                                                                          //
  7 # Program: Atmosphere models                   
  8 
  9 import numpy as np
 10 import scipy as sc
 11 import pylab as plt
 12 import urllib2
 13 
 14 
 15 # France Allard data ...
 16 
 17 BTSETTL_files = [
 18 'colmag.BT-Settl.server.JOHNSON.Vega',
 19 'colmag.BT-Settl.server.2MASS.Vega',
 20 'colmag.BT-Settl.server.SDSS.Vega',
 21 'colmag.BT-Settl.server.SPITZER.Vega',
 22 'colmag.BT-Settl.server.GAIA.Vega'
 23 ]
 24 
 25 BTSurl        = 'https://phoenix.ens-lyon.fr/Grids/BT-Settl/CIFIST2011bc/COLORS/'
 26 
 27 BJ = sc.genfromtxt(urllib2.urlopen(BTSurl+BTSETTL_files[0]),comments='!',skip_header=19,names=True,usecols=("Teff","Logg","MH","aH","U","B","V","R","i","RI","IJ","KL","KLL","KM")) # Johnson system ...
 28 #B2 = sc.genfromtxt(urllib2.urlopen(BTSurl+BTSETTL_files[1]),comments='!',skip_header=19,names=True,usecols=("Teff","Logg","MH","aH","J","H","K"))                                   # 2MASS system ...
 29 
 30 #minTeff, maxTeff = np.min(BJ['Teff']), np.max(BJ['Teff'])
 31         
 32 for alpha in [0.,0.2,0.4]: # alpha range 
 33                 
 34         for MH_  in [ 1.0, 0.5, 0.0, -0.5, -1.0, -1.5, -2.0, -2.5, -3.0, -3.5, -4.0, -4.5]: # metallicity range 
 35                         
 36                 for LOGG in [-0.5,  0., 0.5,  1.0,  1.5,  2.0,  2.5,  3.0,  3.5,  4.0,  4.5,  5.0, 5.5, 6.0]: # logg range
 37                         
 38                         mask =  (BJ['aH']==alpha) & (BJ['MH']==MH_) & (BJ['Logg']==LOGG)
 39                         
 40                         if (np.size(BJ['aH'][mask]) == 0): pass
 41                                 
 42                         else:
 43 
 44                                 print BJ['Teff'][mask]
