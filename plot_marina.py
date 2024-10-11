# -*- coding: utf-8 -*-
"""
Created on Thu Feb 22 10:13:44 2024

@author: Cosette K
xbeach marina 2D
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from netCDF4 import Dataset
import matplotlib.colors as mcolors
from mpl_toolkits.mplot3d import Axes3D  # Importar para gráficas en 3D

# Restablecer la configuración de la fuente a la predeterminada
plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': 'TTInterphasesPro-Md'})

# Definir los colores para la escala de colores
color_map = mcolors.LinearSegmentedColormap.from_list('custom', ['#041D52', '#AFEFF5'], N=256)
bottom_color_map = mcolors.LinearSegmentedColormap.from_list('custom_bottom', ['#654321', '#CC9966'], N=256)

# Ruta donde se encuentran los archivos de salida de XBeach
path_sim = "E:/XBeach/halloween/nauka/2d/nonh/5"
post_python_folder = os.path.join(path_sim, "post_python")
export_folder_3d = os.path.join(post_python_folder, "3d_wl")

# Crear la carpeta "3d_wl" si no existe
if not os.path.exists(export_folder_3d):
    os.makedirs(export_folder_3d)

# Cargar archivo de salida de XBeach
fname = os.path.join(path_sim, 'xboutput.nc')
nc = Dataset(fname, "r", format="NETCDF4")

# Obtener datos de elevación del agua y del fondo para cada paso de tiempo
elevation_data_all = nc.variables['zs'][:]  # Dimensiones: (time, ny, nx)
bottom_data_all = nc.variables['zb'][:]      # Dimensiones: (time, ny, nx)

# Obtener coordenadas globales
globalx = nc.variables['globalx'][:]
globaly = nc.variables['globaly'][:]

# Reducir el tamaño de los datos si es necesario
step = 10  # Ajustar el tamaño de reducción
globalx_reduced = globalx[::step, ::step]
globaly_reduced = globaly[::step, ::step]

# Crear y exportar la gráfica 3D para cada paso de tiempo
num_timesteps = elevation_data_all.shape[0]
for t in range(num_timesteps):
    # Obtener el paso de tiempo actual para elevación y fondo
    elevation_data = elevation_data_all[t, ::step, ::step]
    bottom_data = bottom_data_all[t, ::step, ::step]
    
    # Crear la figura 3D
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')
    
    # Crear la superficie 3D de elevación del agua
    surf_water = ax.plot_surface(globalx_reduced, globaly_reduced, elevation_data, cmap=color_map, edgecolor='none', alpha=0.7)
    
    # Crear la superficie 3D del fondo marino
    surf_bottom = ax.plot_surface(globalx_reduced, globaly_reduced, bottom_data, cmap=bottom_color_map, edgecolor='none', alpha=0.7)
    
    # Configuración de etiquetas
    ax.set_xlabel('Coordenada X', fontname='TTInterphasesPro-DmBd', fontsize=14, labelpad=10)
    ax.set_ylabel('Coordenada Y', fontname='TTInterphasesPro-DmBd', fontsize=14, labelpad=10)
    ax.set_zlabel('Altura (m)', fontname='TTInterphasesPro-DmBd', fontsize=14, labelpad=10)
    
    # Ajuste de la escala de colores para la elevación del agua
    cbar = fig.colorbar(surf_water, ax=ax, shrink=0.5, aspect=10, pad=0.1)
    cbar.set_label('Nivel de agua (m)', fontname='TTInterphasesPro-DmBd', fontsize=12)
    
    # Guardar la figura en la carpeta de exportación "3d_wl"
    plt.savefig(os.path.join(export_folder_3d, f'Elevacion_y_Fondo_3D_paso_de_tiempo_{t}.png'))
    
    # Mostrar la figura en pantalla
    plt.show()

    # Cerrar la figura para liberar memoria
    plt.close()

print("Figuras 3D de elevación del agua y fondo marino exportadas exitosamente a la carpeta '3d_wl' en 'post_python'.")
