  #!/usr/bin/python                                                                                                                                                                                                                    


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////                                                         
# Created by: J. G. Fernandez-Trincado                                                                                                                                    //                                                         
# Last update: 2015, December 16                                                                                                                                          //                                                         
# Program: Atmosphere models                                                                                                                                                                                                         

import numpy as np
import scipy as sc
import pylab as plt
import urllib2


# France Allard data ...                                                                                                                                                                                                             

BTSETTL_files = [
'colmag.BT-Settl.server.JOHNSON.Vega',
'colmag.BT-Settl.server.2MASS.Vega',
'colmag.BT-Settl.server.SDSS.Vega',
'colmag.BT-Settl.server.SPITZER.Vega',
'colmag.BT-Settl.server.GAIA.Vega'
]

BTSurl        = 'https://phoenix.ens-lyon.fr/Grids/BT-Settl/CIFIST2011bc/COLORS/'

BJ = sc.genfromtxt(urllib2.urlopen(BTSurl+BTSETTL_files[0]),comments='!',skip_header=19,names=True,usecols=("Teff","Logg","MH","aH","U","B","V","R","i","RI","IJ","KL","KLL","KM")) # Johnson system ...                             
#B2 = sc.genfromtxt(urllib2.urlopen(BTSurl+BTSETTL_files[1]),comments='!',skip_header=19,names=True,usecols=("Teff","Logg","MH","aH","J","H","K"))                                   # 2MASS system ...                              

#minTeff, maxTeff = np.min(BJ['Teff']), np.max(BJ['Teff'])                                                                                                                                                                           

for alpha in [0.,0.2,0.4]: # alpha range                                                                                                                                                                                             

        for MH_  in [ 1.0, 0.5, 0.0, -0.5, -1.0, -1.5, -2.0, -2.5, -3.0, -3.5, -4.0, -4.5]: # metallicity range                                                                                                                      

                for LOGG in [-0.5,  0., 0.5,  1.0,  1.5,  2.0,  2.5,  3.0,  3.5,  4.0,  4.5,  5.0, 5.5, 6.0]: # logg range                                                                                                           

                        mask =  (BJ['aH']==alpha) & (BJ['MH']==MH_) & (BJ['Logg']==LOGG)

                        if (np.size(BJ['aH'][mask]) == 0): pass

                        else:

                                print BJ['Teff'][mask]
