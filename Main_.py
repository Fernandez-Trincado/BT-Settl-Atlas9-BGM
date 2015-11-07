  1 #!/usr/bin/python
  2 
  3 
  4 #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
  5 # Created by: J. G. Fernandez-Trincado                                                                                                                                    //
  6 # Last update: 2015, November 06                                                                                                                                          //
  7 # Program: Atmosphere models                                                                                                                                              //
  8 # Re-computing grids from France Allard and Atlas9 model                                                                                                                  // 
  9 #                                                                                                                                                                         //
 10 import numpy as np
 11 import scipy as sc
 12 import pylab as plt
 13 from scipy.interpolate import interp1d
 14 import os
 15 import sys
 16 
 17 # Input ...
 18 # Col1  ,   Col2,    Col3,    Col4, Col5  ---> Col6 to Coln = colours ... / Columns indicating the position on variables below. 
 19 # 'Teff', 'logg', '[M/H]', '[a/H]', 'V'   ---> XXX6 to XXXn = colours ... / Standard input ...
 20 
 21 system_filt  = {
 22 'Johnson_2MASS'        : ['U-B', 'B-V', 'V-R', 'V-I', 'V-K', 'R-I', 'I-K', 'J-H', 'H-K', 'J-K'],   # System: Johnson + 2MASS
 23 'SDSS_2MASS_SPITZER'   : 'in construction',                                                        # System: SDSS + 2MASS + SPITZER 
 24 'MEGCAM_WIRCAM_SPITZER': 'in construction'                                                         # System: MEGACAM + WIRCAM + SPITZER
 25 }
 26 
 27 BTSettlmodel_ = { 'BJ2MASS':'BTSettlmodel_Johnson_2MASS.dat', 'BSJ2MASSSP':'BTSettlmodel_SDSS_Johnson_2MASS_SPITZER.dat'  }
 28 Atlas_model_  = { 'AJ2MASS':'Atlasmodel_Johnson_2MASS.dat'  , 'ASJ2MASSSP':'Atlasmodel_SDSS_Johnson_2MASS_SPITZER.dat'}
 29 
 30 # Write the combination of filters ... 
 31 system_ = system_filt['Johnson_2MASS']
 32 Atlas   = sc.genfromtxt( Atlas_model_['AJ2MASS'])  # Atlas9 model
 33 BTSettl = sc.genfromtxt(BTSettlmodel_['BJ2MASS'])  # BTSettl model
 34 
 35 #///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
 36 #Program ...
 37 
 38 out_stand     = ['# Teff','logg', '[M/H]', '[a/H]', 'Bol', 'BC_V' , 'V']                 # Standard output ...
 39 seq_name      = np.column_stack((np.append(out_stand, system_)))
 40 seq_system    = np.column_stack(( np.append(['# 1'],np.arange( 2, len(system_)+ len(out_stand) + 1)))) # Sequence on standard output ...
 41 
 42 # Standard, grid and output file ......................................................................................................................................
 43 
 44 file_      = ['p10.dat', 'p05.dat', 'p00.dat', 'm05.dat', 'm10.dat', 'm15.dat', 'm20.dat', 'm25.dat', 'm30.dat', 'm35.dat', 'm40.dat', 'm45.dat']
 45 alpha_grid = [  0., 0.2, 0.4]
 46 FeH_grid   = [ 1.0, 0.5, 0.0, -0.5, -1.0, -1.5, -2.0, -2.5, -3.0, -3.5, -4.0, -4.5]
 47 Logg_grid  = [-0.5,  0., 0.5,  1.0,  1.5,  2.0,  2.5,  3.0,  3.5,  4.0,  4.5,  5.0, 5.5, 6.0]
 48 Vsun       = -38.449  # Constant ...
 49 Teff_step  =  np.arange(100,60000,50) # Teff = 200 K to Teff= 50000 K, with step = 50 K 
 50 
 51 for out_ in  np.arange(len(file_)):
 52 
 53         files_out = open(file_[out_],'a')
 54         sc.savetxt(files_out, seq_name   , fmt='%14s')
 55         sc.savetxt(files_out, seq_system , fmt='%14s')
 56 
 57 
 58 for alpha in np.arange(len(alpha_grid)):
 59 
 60         mask_alph_Atlas   = (Atlas[:,3]   == alpha_grid[alpha]) # alpha - Atlas model
 61         mask_alph_BTSettl = (BTSettl[:,3] == alpha_grid[alpha]) # alpha - BTSettl model
 62 
 63         if len(BTSettl[mask_alph_BTSettl,3]) == 0.:
 64 
 65                 if len(Atlas[mask_alph_Atlas,3]) == 0.: pass
 66 
 67                 else:
 68 
 69                         for metal in np.arange(len(FeH_grid)):
 70 
 71                                 mask_met_Atlas   = ( Atlas[mask_alph_Atlas,2]      == FeH_grid[metal] )
 72 
 73                                 if len(Atlas[mask_alph_Atlas,2][mask_met_Atlas]) == 0.: pass
 74 
 75                                 else:
 76                                         for log_ in np.arange(len(Logg_grid)):
 77 
 78                                                 mask_log_Atlas   = (Atlas[mask_alph_Atlas,1][mask_met_Atlas]        ==  Logg_grid[log_]  )
 79 
 80                                                 if len(Atlas[mask_alph_Atlas,2][mask_met_Atlas][mask_log_Atlas])==0: pass
 81 
 82                                                 else:
 83 
 84                                                         Teff_            = Atlas[mask_alph_Atlas,0][mask_met_Atlas][mask_log_Atlas]
 85                                                         Logg_            = Atlas[mask_alph_Atlas,1][mask_met_Atlas][mask_log_Atlas]
 86                                                         Met_             = Atlas[mask_alph_Atlas,2][mask_met_Atlas][mask_log_Atlas]
 87                                                         Malpha_          = Atlas[mask_alph_Atlas,3][mask_met_Atlas][mask_log_Atlas]
 88                                                         V_               = Atlas[mask_alph_Atlas,4][mask_met_Atlas][mask_log_Atlas]
 89                                                         BC_V             = -10.*np.log10(Teff_/5777.) - ( V_ - Vsun )
 90                                                         Bol              = BC_V
 91                                                         Matrix_          = np.array([Logg_, Met_,Malpha_, Bol, BC_V, V_]).T
 92 
 93                                                         Matrix_end       = np.column_stack((Matrix_, Atlas[mask_alph_Atlas,5:len(system_)+5][mask_met_Atlas][mask_log_Atlas]  ))
 94                                                         mask_step        = ( Teff_step >= np.min(Teff_) ) & ( Teff_step <= np.max(Teff_))
 95                                                         step_intTeff     = Teff_step[mask_step]
 96                                                         vector           = step_intTeff
 97 
 98                                                         #print alpha_grid[alpha], FeH_grid[metal], Logg_grid[log_]
 99 
100                                                         for color_ in np.arange(len(system_)+6):
101 
102                                                                 X_teff        = np.sort(Teff_)
103                                                                 Y_color       = Matrix_end[:,color_][np.argsort(Teff_)]
104                                                                 inter_lieal   = interp1d(X_teff, Y_color, kind='linear')
105                                                                 Xteff_new     = step_intTeff
106                                                                 Ycolor_new    = inter_lieal(step_intTeff)
107                                                                 vector        = np.column_stack((vector, Ycolor_new))
108 
109                                                         files_out = open(file_[metal],'a')
110                                                         sc.savetxt(files_out,vector, fmt='%10.3f')
111 
112         else:
113 
114 
115                 if len(Atlas[mask_alph_Atlas,3]) == 0.:
116 
117                         for metal in np.arange(len(FeH_grid)):
118 
119                                 mask_met_BTSettl = ( BTSettl[mask_alph_BTSettl,2]  == FeH_grid[metal] )
120 
121                                 if len(BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl]) == 0.: pass
122 
123                                 else:
124 
125                                         for log_ in np.arange(len(Logg_grid)):
126 
127                                                 mask_log_BTSettl = (BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl]  ==  Logg_grid[log_]  )
128 
129                                                 if len(BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl][mask_log_BTSettl]) == 0.: pass
130 
131                                                 else:
132 
133                                                         Teff_            = BTSettl[mask_alph_BTSettl,0][mask_met_BTSettl][mask_log_BTSettl]
134                                                         Logg_            = BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl][mask_log_BTSettl]
135                                                         Met_             = BTSettl[mask_alph_BTSettl,2][mask_met_BTSettl][mask_log_BTSettl]
136                                                         Malpha_          = BTSettl[mask_alph_BTSettl,3][mask_met_BTSettl][mask_log_BTSettl]
137                                                         V_               = BTSettl[mask_alph_BTSettl,4][mask_met_BTSettl][mask_log_BTSettl]
138                                                         BC_V             = -10.*np.log10(Teff_/5777.) - ( V_ - Vsun )
139                                                         Bol              = BC_V
140                                                         Matrix_          = np.array([Logg_, Met_,Malpha_, Bol, BC_V, V_]).T
141 
142                                                         Matrix_end       = np.column_stack((Matrix_, BTSettl[mask_alph_BTSettl,5:len(system_)+5][mask_met_BTSettl][mask_log_BTSettl] ))
143                                                         mask_step        = ( Teff_step >= np.min(Teff_) ) & ( Teff_step <= np.max(Teff_))
144                                                         step_intTeff     = Teff_step[mask_step]
145                                                         vector           = step_intTeff
146 
147                                                         #print alpha_grid[alpha], FeH_grid[metal], Logg_grid[log_]
148 
149                                                         for color_ in np.arange(len(system_)+6):
150 
151                                                                 X_teff        = np.sort(Teff_)
152                                                                 Y_color       = Matrix_end[:,color_][np.argsort(Teff_)]
153                                                                 inter_lieal   = interp1d(X_teff, Y_color, kind='linear')
154                                                                 Xteff_new     = step_intTeff
155                                                                 Ycolor_new    = inter_lieal(step_intTeff)
156                                                                 vector        = np.column_stack((vector, Ycolor_new))
157 
158                                                         files_out = open(file_[metal],'a')
159                                                         sc.savetxt(files_out,vector, fmt='%10.3f')
160 
161                 else:
162 
163                         for metal in np.arange(len(FeH_grid)):
164 
165                                 mask_met_Atlas   = ( Atlas[mask_alph_Atlas,2]      == FeH_grid[metal] )
166                                 mask_met_BTSettl = ( BTSettl[mask_alph_BTSettl,2]  == FeH_grid[metal] )
167 
168                                 if len(BTSettl[mask_alph_BTSettl,2][mask_met_BTSettl]) == 0.:
169 
170                                         if len(Atlas[mask_alph_Atlas,2][mask_met_Atlas]) == 0.: pass
171 
172                                         else:
173 
174                                                 for log_ in np.arange(len(Logg_grid)):
175 
176                                                         mask_log_Atlas   = (Atlas[mask_alph_Atlas,1][mask_met_Atlas]        ==  Logg_grid[log_]  )
177 
178                                                         if len(Atlas[mask_alph_Atlas,2][mask_met_Atlas][mask_log_Atlas])==0: pass
179 
180                                                         else:
181 
182                                                                 Teff_            = Atlas[mask_alph_Atlas,0][mask_met_Atlas][mask_log_Atlas]
183                                                                 Logg_            = Atlas[mask_alph_Atlas,1][mask_met_Atlas][mask_log_Atlas]
184                                                                 Met_             = Atlas[mask_alph_Atlas,2][mask_met_Atlas][mask_log_Atlas]
185                                                                 Malpha_          = Atlas[mask_alph_Atlas,3][mask_met_Atlas][mask_log_Atlas]
186                                                                 V_               = Atlas[mask_alph_Atlas,4][mask_met_Atlas][mask_log_Atlas]
187                                                                 BC_V             = -10.*np.log10(Teff_/5777.) - ( V_ - Vsun )
188                                                                 Bol              = BC_V
189                                                                 Matrix_          = np.array([Logg_, Met_,Malpha_, Bol, BC_V, V_]).T
190 
191                                                                 Matrix_end       = np.column_stack((Matrix_, Atlas[mask_alph_Atlas,5:len(system_)+5][mask_met_Atlas][mask_log_Atlas]  ))
192                                                                 mask_step        = ( Teff_step >= np.min(Teff_) ) & ( Teff_step <= np.max(Teff_))
193                                                                 step_intTeff     = Teff_step[mask_step]
194                                                                 vector           = step_intTeff
195 
196                                                                 #print alpha_grid[alpha], FeH_grid[metal], Logg_grid[log_]
197 
198                                                                 for color_ in np.arange(len(system_)+6):
199 
200                                                                         X_teff        = np.sort(Teff_)
201                                                                         Y_color       = Matrix_end[:,color_][np.argsort(Teff_)]
202                                                                         inter_lieal   = interp1d(X_teff, Y_color, kind='linear')
203                                                                         Xteff_new     = step_intTeff
204                                                                         Ycolor_new    = inter_lieal(step_intTeff)
205                                                                         vector        = np.column_stack((vector, Ycolor_new))
206 
207                                                                 files_out = open(file_[metal],'a')
208                                                                 sc.savetxt(files_out,vector, fmt='%10.3f')
209 
210                                 else:
211 
212                                         if len(Atlas[mask_alph_Atlas,2][mask_met_Atlas]) == 0.:
213 
214                                                 mask_log_BTSettl = (BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl]  ==  Logg_grid[log_]  )
215 
216                                                 for log_ in np.arange(len(Logg_grid)):
217 
218                                                         if len(BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl][mask_log_BTSettl]) == 0.: pass
219 
220                                                         else:
221 
222                                                                 Teff_            = BTSettl[mask_alph_BTSettl,0][mask_met_BTSettl][mask_log_BTSettl]
223                                                                 Logg_            = BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl][mask_log_BTSettl]
224                                                                 Met_             = BTSettl[mask_alph_BTSettl,2][mask_met_BTSettl][mask_log_BTSettl]
225                                                                 Malpha_          = BTSettl[mask_alph_BTSettl,3][mask_met_BTSettl][mask_log_BTSettl]
226                                                                 V_               = BTSettl[mask_alph_BTSettl,4][mask_met_BTSettl][mask_log_BTSettl]
227                                                                 BC_V             = -10.*np.log10(Teff_/5777.) - ( V_ - Vsun )
228                                                                 Bol              = BC_V
229                                                                 Matrix_          = np.array([Logg_, Met_,Malpha_, Bol, BC_V, V_]).T
230 
231                                                                 Matrix_end       = np.column_stack((Matrix_, BTSettl[mask_alph_BTSettl,5:len(system_)+5][mask_met_BTSettl][mask_log_BTSettl] ))
232                                                                 mask_step        = ( Teff_step >= np.min(Teff_) ) & ( Teff_step <= np.max(Teff_))
233                                                                 step_intTeff     = Teff_step[mask_step]
234                                                                 vector           = step_intTeff
235 
236 
237 
238                                                                 #print alpha_grid[alpha], FeH_grid[metal], Logg_grid[log_]
239 
240                                                                 for color_ in np.arange(len(system_)+6):
241 
242                                                                         X_teff        = np.sort(Teff_)
243                                                                         Y_color       = Matrix_end[:,color_][np.argsort(Teff_)]
244                                                                         inter_lieal   = interp1d(X_teff, Y_color, kind='linear')
245                                                                         Xteff_new     = step_intTeff
246                                                                         Ycolor_new    = inter_lieal(step_intTeff)
247                                                                         vector        = np.column_stack((vector, Ycolor_new))
248 
249                                                                 files_out = open(file_[metal],'a')
250                                                                 sc.savetxt(files_out,vector, fmt='%10.3f')
251 
252                                         else:
253 
254                                                 for log_ in np.arange(len(Logg_grid)):
255 
256                                                         mask_log_Atlas   = (Atlas[mask_alph_Atlas,1][mask_met_Atlas]        ==  Logg_grid[log_]  )
257                                                         mask_log_BTSettl = (BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl]  ==  Logg_grid[log_]  )
258 
259                                                         if len(BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl][mask_log_BTSettl]) == 0.:
260 
261                                                                 if len(Atlas[mask_alph_Atlas,1][mask_met_Atlas][mask_log_Atlas]) == 0.: pass
262 
263                                                                 else:
264 
265                                                                         Teff_         = Atlas[mask_alph_Atlas,0][mask_met_Atlas][mask_log_Atlas]
266                                                                         Logg_         = Atlas[mask_alph_Atlas,1][mask_met_Atlas][mask_log_Atlas]
267                                                                         Met_          = Atlas[mask_alph_Atlas,2][mask_met_Atlas][mask_log_Atlas]
268                                                                         Malpha_       = Atlas[mask_alph_Atlas,3][mask_met_Atlas][mask_log_Atlas]
269                                                                         V_            = Atlas[mask_alph_Atlas,4][mask_met_Atlas][mask_log_Atlas]
270                                                                         BC_V          = -10.*np.log10(Teff_/5777.) - ( V_ - Vsun )
271                                                                         Bol           = BC_V
272                                                                         Matrix_       = np.array([Logg_, Met_,Malpha_, Bol, BC_V, V_]).T
273 
274                                                                         Matrix_end    = np.column_stack((Matrix_, Atlas[mask_alph_Atlas,5:len(system_)+5][mask_met_Atlas][mask_log_Atlas]  ))
275                                                                         mask_step     = ( Teff_step >= np.min(Teff_) ) & ( Teff_step <= np.max(Teff_))
276                                                                         step_intTeff  = Teff_step[mask_step]
277                                                                         vector        = step_intTeff
278 
279                                                                         #print alpha_grid[alpha], FeH_grid[metal], Logg_grid[log_]
280 
281                                                                         for color_ in np.arange(len(system_)+6):
282 
283                                                                                 X_teff        = np.sort(Teff_)
284                                                                                 Y_color       = Matrix_end[:,color_][np.argsort(Teff_)]
285                                                                                 inter_lieal   = interp1d(X_teff, Y_color, kind='linear')
286                                                                                 Xteff_new     = step_intTeff
287                                                                                 Ycolor_new    = inter_lieal(step_intTeff)
288                                                                                 vector        = np.column_stack((vector, Ycolor_new))
289 
290                                                                         files_out = open(file_[metal],'a')
291                                                                         sc.savetxt(files_out,vector, fmt='%10.3f')
292 
293                                                         else:
294 
295                                                                 if len(Atlas[mask_alph_Atlas,1][mask_met_Atlas][mask_log_Atlas]) == 0.:
296 
297 
298                                                                         Teff_         = BTSettl[mask_alph_BTSettl,0][mask_met_BTSettl][mask_log_BTSettl]
299                                                                         Logg_         = BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl][mask_log_BTSettl]
300                                                                         Met_          = BTSettl[mask_alph_BTSettl,2][mask_met_BTSettl][mask_log_BTSettl]
301                                                                         Malpha_       = BTSettl[mask_alph_BTSettl,3][mask_met_BTSettl][mask_log_BTSettl]
302                                                                         V_            = BTSettl[mask_alph_BTSettl,4][mask_met_BTSettl][mask_log_BTSettl]
303                                                                         BC_V          = -10.*np.log10(Teff_/5777.) - ( V_ - Vsun )
304                                                                         Bol           = BC_V
305                                                                         Matrix_       = np.array([Logg_, Met_,Malpha_, Bol, BC_V, V_]).T
306 
307                                                                         Matrix_end    = np.column_stack((Matrix_, BTSettl[mask_alph_BTSettl,5:len(system_)+5][mask_met_BTSettl][mask_log_BTSettl] ))
308                                                                         mask_step     = ( Teff_step >= np.min(Teff_) ) & ( Teff_step <= np.max(Teff_))
309                                                                         step_intTeff  = Teff_step[mask_step]
310                                                                         vector        = step_intTeff
311 
312                                                                         #print alpha_grid[alpha], FeH_grid[metal], Logg_grid[log_]
313 
314                                                                         for color_ in np.arange(len(system_)+6):
315 
316                                                                                 X_teff        = np.sort(Teff_)
317                                                                                 Y_color       = Matrix_end[:,color_][np.argsort(Teff_)]
318                                                                                 inter_lieal   = interp1d(X_teff, Y_color, kind='linear')
319                                                                                 Xteff_new     = step_intTeff
320                                                                                 Ycolor_new    = inter_lieal(step_intTeff)
321                                                                                 vector        = np.column_stack((vector, Ycolor_new))
322 
323                                                                         files_out = open(file_[metal],'a')
324                                                                         sc.savetxt(files_out,vector, fmt='%10.3f')
325 
326 
327                                                                 else:
328 
329 
330                                                                         min_B, max_B  = np.min(BTSettl[mask_alph_BTSettl,0][mask_met_BTSettl][mask_log_BTSettl]), np.max(BTSettl[mask_alph_BTSettl,0][mask_met_BTSettl][mask_log_BTSettl])
331                                                                         min_A, max_A  = np.min(Atlas[mask_alph_Atlas,0][mask_met_Atlas][mask_log_Atlas]) , np.max(Atlas[mask_alph_Atlas,0][mask_met_Atlas][mask_log_Atlas])
332                                                                         mask_g        = (Atlas[mask_alph_Atlas,0][mask_met_Atlas][mask_log_Atlas] < min_B) | ( Atlas[mask_alph_Atlas,0][mask_met_Atlas][mask_log_Atlas] > max_B)
333 
334                                                                         Teff_         = np.append(BTSettl[mask_alph_BTSettl,0][mask_met_BTSettl][mask_log_BTSettl], Atlas[mask_alph_Atlas,0][mask_met_Atlas][mask_log_Atlas][mask_g])
335                                                                         Logg_         = np.append(BTSettl[mask_alph_BTSettl,1][mask_met_BTSettl][mask_log_BTSettl], Atlas[mask_alph_Atlas,1][mask_met_Atlas][mask_log_Atlas][mask_g])
336                                                                         Met_          = np.append(BTSettl[mask_alph_BTSettl,2][mask_met_BTSettl][mask_log_BTSettl], Atlas[mask_alph_Atlas,2][mask_met_Atlas][mask_log_Atlas][mask_g])
337                                                                         Malpha_       = np.append(BTSettl[mask_alph_BTSettl,3][mask_met_BTSettl][mask_log_BTSettl], Atlas[mask_alph_Atlas,3][mask_met_Atlas][mask_log_Atlas][mask_g])
338                                                                         V_            = np.append(BTSettl[mask_alph_BTSettl,4][mask_met_BTSettl][mask_log_BTSettl], Atlas[mask_alph_Atlas,4][mask_met_Atlas][mask_log_Atlas][mask_g])
339                                                                         BC_V          = -10.*np.log10(Teff_/5777.) - ( V_ - Vsun )
340                                                                         Bol           = BC_V
341                                                                         Matrix_       = np.array([Logg_, Met_,Malpha_, Bol, BC_V, V_]).T
342                                                                         colour_matrix = np.row_stack((BTSettl[mask_alph_BTSettl,5:len(system_)+5][mask_met_BTSettl][mask_log_BTSettl], Atlas[mask_alph_Atlas,5:len(system_)+5][mask_met_Atlas][mask_log_Atlas][mask_g] ))
343 
344                                                                         Matrix_end    = np.column_stack((Matrix_, colour_matrix ))
345                                                                         mask_step     = ( Teff_step >= np.min(Teff_) ) & ( Teff_step <= np.max(Teff_))
346                                                                         step_intTeff  = Teff_step[mask_step]
347                                                                         vector        = step_intTeff
348 
349                                                                         #print alpha_grid[alpha], FeH_grid[metal], Logg_grid[log_]
350 
351                                                                         for color_ in np.arange(len(system_)+6):
352 
353                                                                                 X_teff        = np.sort(Teff_)
354                                                                                 Y_color       = Matrix_end[:,color_][np.argsort(Teff_)]
355                                                                                 inter_lieal   = interp1d(X_teff, Y_color, kind='linear')
356                                                                                 Xteff_new     = step_intTeff
357                                                                                 Ycolor_new    = inter_lieal(step_intTeff)
358                                                                                 vector        = np.column_stack((vector, Ycolor_new))
359 
360                                                                         files_out = open(file_[metal],'a')
361                                                                         sc.savetxt(files_out,vector, fmt='%10.3f')
362 # End program ...
