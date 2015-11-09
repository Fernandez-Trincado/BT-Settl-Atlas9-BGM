#!/usr/bin/python


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Created by: J. G. Fernandez-Trincado                                                                                                                                    //
# Last update: 2015, November 09                                                                                                                                          //
# Program: Atmosphere models                                                                                                                                              //
# Re-computing grids from France Allard and Atlas9 model                                                                                                                  // 
#                                                                                                                                                                         //
import numpy as np           
import scipy as sc
import pylab as plt
from scipy.interpolate import interp1d
import os 
import sys

# Input ...
# Col1  ,   Col2,    Col3,    Col4, Col5  ---> Col6 to Coln = colours ... / Columns indicating the position on variables below. 
# 'Teff', 'logg', '[M/H]', '[a/H]', 'V'   ---> XXX6 to XXXn = colours ... / Standard input ...

system_filt  = {
'Johnson_2MASS'        : ['U-B', 'B-V', 'V-R', 'V-I', 'V-K', 'R-I', 'I-K', 'J-H', 'H-K', 'K-L', 'J-K', 'J-L', 'J-L2', 'K-M'],                                                         # System: Johnson + 2MASS
'SDSS_2MASS_SPITZER'   : ['J'  ,   'g', 'u-g', 'g-r', 'r-i', 'i-z', 'J-H', 'J-K', 'H-K', 'K-[3.6]', 'K-[4.5]', 'K-[5.8]', 'K-[8.0]', 'K-[24]', 'K-[70]', 'K-[160]'],                  # System: SDSS + 2MASS + SPITZER 
'SDSS'                 : ['g'  , 'u-g', 'g-r', 'r-i', 'i-z'],                                                                                                                         # System: SDSS 
'MEGCAM_WIRCAM_SPITZER': ['U-G', 'G-R', 'R-I', 'I-Z', 'J-Y', 'J-H', 'H-Ks', 'J-Ks', 'Ks-[3.6]', 'Ks-[4.5]', 'Ks-[5.8]', 'Ks-[8.0]', 'Ks-[24]', 'Ks-[70]', 'Ks-[160]', 'G', 'J', 'Ks'] # System: MEGACAM + WIRCAM + SPITZER
#  'GAIA': 'in preparation',in collaboration with Carme Jordi and France Allard model 
}

BTSettlmodel_ = { 'BJ2MASS':'BTSettlmodel_color_Johnson_2MASS.dat' , 'BSJ2MASSSP':'BTSettlmodel_color_SDSS_2MASS_SPITZER.dat', 'BSDSS':'BTSettlmodel_color_SDSS.dat', 'BMWS':'BTSettlmodel_color_Megacam_wircam_SPITZER.dat'}
Atlas_model_  = { 'AJ2MASS':'ATLAS9model_color_Johnson_2MASS.dat'  , 'ASJ2MASSSP':'ATLAS9model_color_SDSS_2MASS_SPITZER.dat' , 'ASDSS':'ATLAS9model_color_SDSS.dat' , 'AMWS':'ATLAS9model_color_Megacam_wircam_SPITZER.dat'}


#system_ = system_filt['Johnson_2MASS']                # Johnson + 2MASS ...
#Atlas   = sc.genfromtxt( Atlas_model_['AJ2MASS'])     # Atlas9 model   , Johnson + 2MASS ...
#BTSettl = sc.genfromtxt(BTSettlmodel_['BJ2MASS'])     # BTSettl model  , Johnson + 2MASS ...

#system_ = system_filt['SDSS_2MASS_SPITZER']           # SDSS + 2MASS +  SPTIZER
#Atlas   = sc.genfromtxt( Atlas_model_['ASJ2MASSSP'])  # Atlas9 model, SDSS + 2MASS +  SPTIZER ...
#BTSettl = sc.genfromtxt(BTSettlmodel_['BSJ2MASSSP'])  # BTSettl model, SDSS + 2MASS +  SPTIZER ...

#system_ = system_filt['SDSS']                         # 2MASS ...
#Atlas   = sc.genfromtxt( Atlas_model_['ASDSS'])       # Atlas9 model   , 2MASS ...
#BTSettl = sc.genfromtxt(BTSettlmodel_['BSDSS'])       # BTSettl model  , 2MASS ...

system_ = system_filt['MEGCAM_WIRCAM_SPITZER']         # Megacam + wircam + SPITZER ...
Atlas   = sc.genfromtxt( Atlas_model_['AMWS'])         # Atlas9 model, Megacam + wircam + SPITZER ...
BTSettl = sc.genfromtxt(BTSettlmodel_['BMWS'])         # BTSettl model, Megacam + wircam + SPITZER ...


#///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#Program ...

#out_stand     = ['# Teff','logg', '[M/H]', '[a/H]', 'Bol', 'BC_V' , 'V']                 # Standard output ...
out_stand     = ['# Teff','logg', '[M/H]', 'Bol', '[a/H]', 'BC_V']                 # Standard output ...
seq_name      = np.column_stack((np.append(out_stand, system_)))
seq_system    = np.column_stack(( np.append(['# 1'],np.arange( 2, len(system_)+ len(out_stand) + 1)))) # Sequence on standard output ...

# Standard, grid and output file ......................................................................................................................................

file_      = ['p10.dat', 'p05.dat', 'p00.dat', 'm05.dat', 'm10.dat', 'm15.dat', 'm20.dat', 'm25.dat', 'm30.dat', 'm35.dat', 'm40.dat', 'm45.dat']
alpha_grid = [  0., 0.2, 0.4]
FeH_grid   = [ 1.0, 0.5, 0.0, -0.5, -1.0, -1.5, -2.0, -2.5, -3.0, -3.5, -4.0, -4.5]
Logg_grid  = [-0.5,  0., 0.5,  1.0,  1.5,  2.0,  2.5,  3.0,  3.5,  4.0,  4.5,  5.0, 5.5, 6.0]
Vsun       = -38.449  # Constant ...
Teff_step  =  np.arange(100,60000,50) # Teff = 200 K to Teff= 50000 K, with step = 50 K 




for out_ in  np.arange(len(file_)):

	files_out = open(file_[out_],'a')
	sc.savetxt(files_out, seq_name   , fmt='%14s')	
	sc.savetxt(files_out, seq_system , fmt='%14s')


for alpha in np.arange(len(alpha_grid)):

	mask_alph_Atlas   = (Atlas[:,3]   == alpha_grid[alpha]) # alpha - Atlas model
	mask_alph_BTSettl = (BTSettl[:,3] == alpha_grid[alpha]) # alpha - BTSettl model

	if len(BTSettl[mask_alph_BTSettl,3]) == 0.:

		if len(Atlas[mask_alph_Atlas,3]) == 0.: pass

		else:

			for metal in np.arange(len(FeH_grid)):

				mask_met_Atlas   = ( Atlas[mask_alph_Atlas,2]      == FeH_grid[metal] )
				
				if len(Atlas[mask_alph_Atlas,2][mask_met_Atlas]) == 0.: pass

				else:
					for log_ in np.arange(len(Logg_grid)):

						mask_log_Atlas   = (Atlas[mask_alph_Atlas,1][mask_met_Atlas]        ==  Logg_grid[log_]  )

						if len(Atlas[mask_alph_Atlas,2][mask_met_Atlas][mask_log_Atlas])==0: pass

						else:

							Teff_            = Atlas[mask_alph_Atlas,0][mask_met_Atlas][mask_log_Atlas]
							Logg_            = Atlas[mask_alph_Atlas,1][mask_met_Atlas][mask_log_Atlas]
							Met_             = Atlas[mask_alph_Atlas,2][mask_met_Atlas][mask_log_Atlas]
							Malpha_          = Atlas[mask_alph_Atlas,3][mask_met_Atlas][mask_log_Atlas]
							V_               = Atlas[mask_alph_Atlas,4][mask_met_Atlas][mask_log_Atlas]
							BC_V             = -10.*np.log10(Teff_/5777.) - ( V_ - Vsun )
							Bol              = BC_V  
							#Matrix_          = np.array([Logg_, Met_,Malpha_, Bol, BC_V, V_]).T
							Matrix_          = np.array([Logg_, Met_, Bol, Malpha_, BC_V]).T							

							Matrix_end       = np.column_stack((Matrix_, Atlas[mask_alph_Atlas,5:len(system_)+5][mask_met_Atlas][mask_log_Atlas]  ))
							mask_step        = ( Teff_step >= np.min(Teff_) ) & ( Teff_step <= np.max(Teff_))
							step_intTeff     = Teff_step[mask_step]
							vector           = step_intTeff

							#print alpha_grid[alpha], FeH_grid[metal], Logg_grid[log_]
							
							for color_ in np.arange(len(system_)+5):
							
							        X_teff        = np.sort(Teff_)
							        Y_color       = Matrix_end[:,color_][np.argsort(Teff_)]
							        inter_lieal   = interp1d(X_teff, Y_color, kind='linear')
							        Xteff_new     = step_intTeff
							        Ycolor_new    = inter_lieal(step_intTeff)
							        vector        = np.column_stack((vector, Ycolor_new))
							
							files_out = open(file_[metal],'a')
							sc.savetxt(files_out,vector, fmt='%10.3f')			

	else:


		if len(Atlas[mask_alph_Atlas,3]) == 0.: 

			for metal in np.arange(len(FeH_grid)):

				mask_met_BTSettl = ( BTSettl[mask_alph_BTSettl,2]  == FeH_grid[metal] )

				if len(BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl]) == 0.: pass

				else:

					for log_ in np.arange(len(Logg_grid)):

						mask_log_BTSettl = (BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl]  ==  Logg_grid[log_]  )

						if len(BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl][mask_log_BTSettl]) == 0.: pass

						else:

							Teff_            = BTSettl[mask_alph_BTSettl,0][mask_met_BTSettl][mask_log_BTSettl]
							Logg_            = BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl][mask_log_BTSettl]
							Met_             = BTSettl[mask_alph_BTSettl,2][mask_met_BTSettl][mask_log_BTSettl]
							Malpha_          = BTSettl[mask_alph_BTSettl,3][mask_met_BTSettl][mask_log_BTSettl]
							V_               = BTSettl[mask_alph_BTSettl,4][mask_met_BTSettl][mask_log_BTSettl]
							BC_V             = -10.*np.log10(Teff_/5777.) - ( V_ - Vsun )
							Bol              = BC_V
							#Matrix_          = np.array([Logg_, Met_,Malpha_, Bol, BC_V, V_]).T
							Matrix_          = np.array([Logg_, Met_, Bol, Malpha_, BC_V]).T							

							Matrix_end       = np.column_stack((Matrix_, BTSettl[mask_alph_BTSettl,5:len(system_)+5][mask_met_BTSettl][mask_log_BTSettl] ))
							mask_step        = ( Teff_step >= np.min(Teff_) ) & ( Teff_step <= np.max(Teff_))
							step_intTeff     = Teff_step[mask_step]
							vector           = step_intTeff

							#print alpha_grid[alpha], FeH_grid[metal], Logg_grid[log_]
							
							for color_ in np.arange(len(system_)+5):
							
							        X_teff        = np.sort(Teff_)
							        Y_color       = Matrix_end[:,color_][np.argsort(Teff_)]
							        inter_lieal   = interp1d(X_teff, Y_color, kind='linear')
							        Xteff_new     = step_intTeff
							        Ycolor_new    = inter_lieal(step_intTeff)
							        vector        = np.column_stack((vector, Ycolor_new))
							
							files_out = open(file_[metal],'a')
							sc.savetxt(files_out,vector, fmt='%10.3f')

		else:

			for metal in np.arange(len(FeH_grid)):

				mask_met_Atlas   = ( Atlas[mask_alph_Atlas,2]      == FeH_grid[metal] )
				mask_met_BTSettl = ( BTSettl[mask_alph_BTSettl,2]  == FeH_grid[metal] )

				if len(BTSettl[mask_alph_BTSettl,2][mask_met_BTSettl]) == 0.:

					if len(Atlas[mask_alph_Atlas,2][mask_met_Atlas]) == 0.: pass

					else:

						for log_ in np.arange(len(Logg_grid)):
						
							mask_log_Atlas   = (Atlas[mask_alph_Atlas,1][mask_met_Atlas]        ==  Logg_grid[log_]  )

							if len(Atlas[mask_alph_Atlas,2][mask_met_Atlas][mask_log_Atlas])==0: pass

							else:
	
								Teff_            = Atlas[mask_alph_Atlas,0][mask_met_Atlas][mask_log_Atlas]
								Logg_            = Atlas[mask_alph_Atlas,1][mask_met_Atlas][mask_log_Atlas]
								Met_             = Atlas[mask_alph_Atlas,2][mask_met_Atlas][mask_log_Atlas]
								Malpha_          = Atlas[mask_alph_Atlas,3][mask_met_Atlas][mask_log_Atlas]
								V_               = Atlas[mask_alph_Atlas,4][mask_met_Atlas][mask_log_Atlas]
								BC_V             = -10.*np.log10(Teff_/5777.) - ( V_ - Vsun )
								Bol              = BC_V  
								#Matrix_          = np.array([Logg_, Met_,Malpha_, Bol, BC_V, V_]).T
								Matrix_          = np.array([Logg_, Met_, Bol, Malpha_, BC_V]).T								

								Matrix_end       = np.column_stack((Matrix_, Atlas[mask_alph_Atlas,5:len(system_)+5][mask_met_Atlas][mask_log_Atlas]  ))
								mask_step        = ( Teff_step >= np.min(Teff_) ) & ( Teff_step <= np.max(Teff_))
								step_intTeff     = Teff_step[mask_step]
								vector           = step_intTeff

								#print alpha_grid[alpha], FeH_grid[metal], Logg_grid[log_]
								
								for color_ in np.arange(len(system_)+5):
								
								        X_teff        = np.sort(Teff_)
								        Y_color       = Matrix_end[:,color_][np.argsort(Teff_)]
								        inter_lieal   = interp1d(X_teff, Y_color, kind='linear')
								        Xteff_new     = step_intTeff
								        Ycolor_new    = inter_lieal(step_intTeff)
								        vector        = np.column_stack((vector, Ycolor_new))
								
								files_out = open(file_[metal],'a')
								sc.savetxt(files_out,vector, fmt='%10.3f')

				else: 

					if len(Atlas[mask_alph_Atlas,2][mask_met_Atlas]) == 0.: 

						for log_ in np.arange(len(Logg_grid)):

							mask_log_BTSettl = (BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl]  ==  Logg_grid[log_]  )

							if len(BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl][mask_log_BTSettl]) == 0.: pass
					
							else:

								Teff_            = BTSettl[mask_alph_BTSettl,0][mask_met_BTSettl][mask_log_BTSettl]
								Logg_            = BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl][mask_log_BTSettl]
								Met_             = BTSettl[mask_alph_BTSettl,2][mask_met_BTSettl][mask_log_BTSettl]
								Malpha_          = BTSettl[mask_alph_BTSettl,3][mask_met_BTSettl][mask_log_BTSettl]
								V_               = BTSettl[mask_alph_BTSettl,4][mask_met_BTSettl][mask_log_BTSettl]
								BC_V             = -10.*np.log10(Teff_/5777.) - ( V_ - Vsun )
								Bol              = BC_V
								#Matrix_          = np.array([Logg_, Met_,Malpha_, Bol, BC_V, V_]).T
								Matrix_          = np.array([Logg_, Met_, Bol, Malpha_, BC_V]).T								

								Matrix_end       = np.column_stack((Matrix_, BTSettl[mask_alph_BTSettl,5:len(system_)+5][mask_met_BTSettl][mask_log_BTSettl] ))
								mask_step        = ( Teff_step >= np.min(Teff_) ) & ( Teff_step <= np.max(Teff_))
								step_intTeff     = Teff_step[mask_step]
								vector           = step_intTeff



								#print alpha_grid[alpha], FeH_grid[metal], Logg_grid[log_]
								
								for color_ in np.arange(len(system_)+5):
								
								        X_teff        = np.sort(Teff_)
								        Y_color       = Matrix_end[:,color_][np.argsort(Teff_)]
								        inter_lieal   = interp1d(X_teff, Y_color, kind='linear')
								        Xteff_new     = step_intTeff
								        Ycolor_new    = inter_lieal(step_intTeff)
								        vector        = np.column_stack((vector, Ycolor_new))
								
								files_out = open(file_[metal],'a')
								sc.savetxt(files_out,vector, fmt='%10.3f')

					else:

						for log_ in np.arange(len(Logg_grid)):

							mask_log_Atlas   = (Atlas[mask_alph_Atlas,1][mask_met_Atlas]        ==  Logg_grid[log_]  )
							mask_log_BTSettl = (BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl]  ==  Logg_grid[log_]  )

							if len(BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl][mask_log_BTSettl]) == 0.:							

								if len(Atlas[mask_alph_Atlas,1][mask_met_Atlas][mask_log_Atlas]) == 0.: pass

								else:
		
									Teff_         = Atlas[mask_alph_Atlas,0][mask_met_Atlas][mask_log_Atlas]
									Logg_         = Atlas[mask_alph_Atlas,1][mask_met_Atlas][mask_log_Atlas]
									Met_          = Atlas[mask_alph_Atlas,2][mask_met_Atlas][mask_log_Atlas]
									Malpha_       = Atlas[mask_alph_Atlas,3][mask_met_Atlas][mask_log_Atlas]
									V_            = Atlas[mask_alph_Atlas,4][mask_met_Atlas][mask_log_Atlas]
									BC_V          = -10.*np.log10(Teff_/5777.) - ( V_ - Vsun )
									Bol           = BC_V  
									#Matrix_       = np.array([Logg_, Met_,Malpha_, Bol, BC_V, V_]).T
									Matrix_          = np.array([Logg_, Met_, Bol, Malpha_, BC_V]).T

									Matrix_end    = np.column_stack((Matrix_, Atlas[mask_alph_Atlas,5:len(system_)+5][mask_met_Atlas][mask_log_Atlas]  ))
									mask_step     = ( Teff_step >= np.min(Teff_) ) & ( Teff_step <= np.max(Teff_))
									step_intTeff  = Teff_step[mask_step]
									vector        = step_intTeff

									#print alpha_grid[alpha], FeH_grid[metal], Logg_grid[log_]
									
									for color_ in np.arange(len(system_)+5):
									
									        X_teff        = np.sort(Teff_)
									        Y_color       = Matrix_end[:,color_][np.argsort(Teff_)]
									        inter_lieal   = interp1d(X_teff, Y_color, kind='linear')
									        Xteff_new     = step_intTeff
									        Ycolor_new    = inter_lieal(step_intTeff)
									        vector        = np.column_stack((vector, Ycolor_new))
									
									files_out = open(file_[metal],'a')
									sc.savetxt(files_out,vector, fmt='%10.3f')									

							else:

								if len(Atlas[mask_alph_Atlas,1][mask_met_Atlas][mask_log_Atlas]) == 0.:
						
								
									Teff_         = BTSettl[mask_alph_BTSettl,0][mask_met_BTSettl][mask_log_BTSettl]
									Logg_         = BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl][mask_log_BTSettl]
									Met_          = BTSettl[mask_alph_BTSettl,2][mask_met_BTSettl][mask_log_BTSettl]
									Malpha_       = BTSettl[mask_alph_BTSettl,3][mask_met_BTSettl][mask_log_BTSettl]
									V_            = BTSettl[mask_alph_BTSettl,4][mask_met_BTSettl][mask_log_BTSettl]
									BC_V          = -10.*np.log10(Teff_/5777.) - ( V_ - Vsun )
									Bol           = BC_V                            
									#Matrix_       = np.array([Logg_, Met_,Malpha_, Bol, BC_V, V_]).T
									Matrix_          = np.array([Logg_, Met_, Bol, Malpha_, BC_V]).T									

									Matrix_end    = np.column_stack((Matrix_, BTSettl[mask_alph_BTSettl,5:len(system_)+5][mask_met_BTSettl][mask_log_BTSettl] ))
									mask_step     = ( Teff_step >= np.min(Teff_) ) & ( Teff_step <= np.max(Teff_))
									step_intTeff  = Teff_step[mask_step]
									vector        = step_intTeff

									#print alpha_grid[alpha], FeH_grid[metal], Logg_grid[log_]
									
									for color_ in np.arange(len(system_)+5):
									
									        X_teff        = np.sort(Teff_)
									        Y_color       = Matrix_end[:,color_][np.argsort(Teff_)]
									        inter_lieal   = interp1d(X_teff, Y_color, kind='linear')
									        Xteff_new     = step_intTeff
									        Ycolor_new    = inter_lieal(step_intTeff)
									        vector        = np.column_stack((vector, Ycolor_new))

									files_out = open(file_[metal],'a')
									sc.savetxt(files_out,vector, fmt='%10.3f')


								else: 

									
									min_B, max_B  = np.min(BTSettl[mask_alph_BTSettl,0][mask_met_BTSettl][mask_log_BTSettl]), np.max(BTSettl[mask_alph_BTSettl,0][mask_met_BTSettl][mask_log_BTSettl])
									min_A, max_A  = np.min(Atlas[mask_alph_Atlas,0][mask_met_Atlas][mask_log_Atlas]) , np.max(Atlas[mask_alph_Atlas,0][mask_met_Atlas][mask_log_Atlas])	
									mask_g        = (Atlas[mask_alph_Atlas,0][mask_met_Atlas][mask_log_Atlas] < min_B) | ( Atlas[mask_alph_Atlas,0][mask_met_Atlas][mask_log_Atlas] > max_B)
	
									Teff_         = np.append(BTSettl[mask_alph_BTSettl,0][mask_met_BTSettl][mask_log_BTSettl], Atlas[mask_alph_Atlas,0][mask_met_Atlas][mask_log_Atlas][mask_g])
									Logg_         = np.append(BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl][mask_log_BTSettl], Atlas[mask_alph_Atlas,1][mask_met_Atlas][mask_log_Atlas][mask_g]) 
									Met_          = np.append(BTSettl[mask_alph_BTSettl,2][mask_met_BTSettl][mask_log_BTSettl], Atlas[mask_alph_Atlas,2][mask_met_Atlas][mask_log_Atlas][mask_g]) 
									Malpha_       = np.append(BTSettl[mask_alph_BTSettl,3][mask_met_BTSettl][mask_log_BTSettl], Atlas[mask_alph_Atlas,3][mask_met_Atlas][mask_log_Atlas][mask_g]) 							
									V_            = np.append(BTSettl[mask_alph_BTSettl,4][mask_met_BTSettl][mask_log_BTSettl], Atlas[mask_alph_Atlas,4][mask_met_Atlas][mask_log_Atlas][mask_g])
									BC_V          = -10.*np.log10(Teff_/5777.) - ( V_ - Vsun )
									Bol           = BC_V				
									#Matrix_       = np.array([Logg_, Met_,Malpha_, Bol, BC_V, V_]).T
									Matrix_          = np.array([Logg_, Met_, Bol, Malpha_, BC_V]).T
									colour_matrix = np.row_stack((BTSettl[mask_alph_BTSettl,5:len(system_)+5][mask_met_BTSettl][mask_log_BTSettl], Atlas[mask_alph_Atlas,5:len(system_)+5][mask_met_Atlas][mask_log_Atlas][mask_g] )) 
	
									Matrix_end    = np.column_stack((Matrix_, colour_matrix ))							
									mask_step     = ( Teff_step >= np.min(Teff_) ) & ( Teff_step <= np.max(Teff_))
									step_intTeff  = Teff_step[mask_step]
									vector        = step_intTeff

									#print alpha_grid[alpha], FeH_grid[metal], Logg_grid[log_]
									
									for color_ in np.arange(len(system_)+5):
									
										X_teff        = np.sort(Teff_)
										Y_color       = Matrix_end[:,color_][np.argsort(Teff_)]  
										inter_lieal   = interp1d(X_teff, Y_color, kind='linear')
										Xteff_new     = step_intTeff
										Ycolor_new    = inter_lieal(step_intTeff)
										vector        = np.column_stack((vector, Ycolor_new))

									files_out = open(file_[metal],'a')
									sc.savetxt(files_out,vector, fmt='%10.3f')
# End program ...
