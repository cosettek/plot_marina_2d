# -*- coding: utf-8 -*-
import numpy as np
import matplotlib.pyplot as plt
import os
from netCDF4 import Dataset
from matplotlib.colors import LinearSegmentedColormap
from mpl_toolkits.mplot3d import Axes3D  # Importar para gráficas en 3D

# Crear un mapa de colores personalizado para el terreno
terrain_colors = [
    (0, "#004182"),   # Más de 10 m de profundidad (color azul oscuro)
    (0.3, "#D7FFFF"), # Entre 0 y 10 m de profundidad (color azul claro)
    (0.95, "#E1C9B0"),  # Entre 0 y 3 m de altura (color beige)
    (0.97, "#808000"), # Entre 3 y 10 m de altura (color verde oliva)
    (1, "#495E04")     # Más de 10 m de altura (color verde oscuro)
]
terrain_cmap = LinearSegmentedColormap.from_list("terrain_cmap", terrain_colors)

# Usar un color sólido para el agua
solid_water_color = "#041D52"  # Color azul oscuro sólido para el agua

# Ruta donde se encuentran los archivos de salida de XBeach
path_sim = "E:/XBeach/halloween/nauka/2d/nonh/5"
export_folder_3d = os.path.join(path_sim, "post_python", "3d_wl")

if not os.path.exists(export_folder_3d):
    os.makedirs(export_folder_3d)

# Cargar archivo de salida de XBeach
fname = os.path.join(path_sim, 'xboutput.nc')
nc = Dataset(fname, "r", format="NETCDF4")

# Obtener datos de elevación del agua y del fondo para cada paso de tiempo
elevation_data_all = nc.variables['zs'][:]
bottom_data_all = nc.variables['zb'][:]
globalx = nc.variables['globalx'][:]
globaly = nc.variables['globaly'][:]

# Reducción (ajustar el valor para suavizar la superficie)
step = 4  # Aumentar la resolución para suavizar la malla
globalx_reduced = globalx[::step, ::step]
globaly_reduced = globaly[::step, ::step]

# Zoom a la costa
xmin, xmax = 475750, 476750
ymin, ymax = 2.33100e6, 2.33250e6

# Gráfico
num_timesteps = elevation_data_all.shape[0]
for t in range(num_timesteps):
    elevation_data = elevation_data_all[t, ::step, ::step]
    bottom_data = bottom_data_all[t, ::step, ::step]
    
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Superficie de agua con color sólido y transparencia ajustada, sin bordes
    ax.plot_surface(globalx_reduced, globaly_reduced, elevation_data, color=solid_water_color, alpha=0.8, edgecolor='none', antialiased=True)
    
    # Superficie del terreno sin bordes, con interpolación suave
    ax.plot_surface(globalx_reduced, globaly_reduced, bottom_data, cmap=terrain_cmap, alpha=1, edgecolor='none', antialiased=True)
    
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(ymin, ymax)
    ax.set_xlabel('Coordenada X')
    ax.set_ylabel('Coordenada Y')
    ax.set_zlabel('Altura (m)')
    
    # Ajuste de vista
    ax.view_init(elev=40, azim=130)

    plt.savefig(os.path.join(export_folder_3d, f'vista_estilizada_paso_{t}.png'))
    plt.show()
    plt.close()

print("Exportación completada a la carpeta '3d_wl'.")
