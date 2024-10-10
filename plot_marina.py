# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 10:13:44 2024

@author: Cosette K
xbeach port
"""

import numpy as np
from scipy import interpolate
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d, Axes3D 
from matplotlib import cm
import sys
import os
from netCDF4 import Dataset


from xbTools.grid.creation import xgrid, ygrid
from xbTools.grid.extension import seaward_extend, lateral_extend
from xbTools.general import wave_functions
from xbTools.xbeachtools import XBeachModelSetup

from xbTools.general.executing_runs import xb_run_script_win


path_sim = os.path.join('F:\Curso_Delft\my_runs\port_paentenderle')
simName  = 'run01'

Hm0 = 2
Tp = 10

    
## load data


model_path = os.path.join(path_sim,simName)
graficas_folder = os.path.join(model_path, 'graficas')
# Crea la carpeta "graficas" si no existe
if not os.path.exists(graficas_folder):
    os.makedirs(graficas_folder)
    

fname = os.path.join(model_path,'xboutput.nc')
nc = Dataset(fname, "r", format="NETCDF4")
globalx       = nc.variables['globalx'][:]
globaly       = nc.variables['globaly'][:]
zs            = nc.variables['zs'][:]
point_zs      = nc.variables['point_zs'][:]
pointx      = nc.variables['pointx'][:]
pointy      = nc.variables['pointy'][:]
pointtime   = nc.variables['pointtime'][:]
zs_var      = nc.variables['zs_var'][:]

plt.figure()
plt.plot(pointtime, point_zs)
plt.ylabel('Hrms [m]')
plt.xlabel('x [m]')
path_pointtime_vs_Hrms = os.path.join(graficas_folder, 'pointtime_vs_Hrms.png')
plt.savefig(path_pointtime_vs_Hrms)  
plt.show()


Hrms = np.abs(np.sqrt(8 * zs_var))

plt.figure()
plt.pcolor(globalx, globaly, Hrms[0, :, :])
plt.plot(pointx[4], pointy[4], 'ro')
plt.plot(globalx[132, :], globaly[132, :], 'r-')
plt.xlabel('cross-shore distance [m]')
plt.ylabel('longshore distance [m]')
plt.title('Hrms')
plt.colorbar()
path_Hrms_pcolor = os.path.join(graficas_folder, 'Hrms_pcolor.png')
plt.savefig(path_Hrms_pcolor) 
plt.show()



plt.figure()
plt.plot(globalx[0, :], Hrms[0, 132, :])
plt.xlabel('cross-shore distance [m]')
plt.ylabel('Hrms [m]')
path_Hrms_along_position_132 = os.path.join(graficas_folder, 'Hrms_along_position_132.png')
plt.savefig(path_Hrms_along_position_132)  
plt.show()
