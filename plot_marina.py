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
import rasterio
from rasterio.plot import show

# Restablecer la configuración de la fuente a la predeterminada
plt.rcParams.update({'font.family': 'sans-serif', 'font.sans-serif': 'TTInterphasesPro-Md'})

# Definir los colores para la escala de colores
color_map = mcolors.LinearSegmentedColormap.from_list('custom', ['#041D52', '#AFEFF5'], N=256)

# Ruta donde se encuentran los archivos de salida de XBeach
path_sim = "E:/XBeach/halloween/nauka/2d/nonh/5"
post_python_folder = os.path.join(path_sim, "post_python")
export_folder = os.path.join(post_python_folder, "for_premiere")

# Crear la carpeta "for_premiere" si no existe
if not os.path.exists(export_folder):
    os.makedirs(export_folder)

# Cargar archivo de salida de XBeach
fname = os.path.join(path_sim, 'xboutput.nc')
nc = Dataset(fname, "r", format="NETCDF4")

# Obtener datos de elevación del agua en cada paso de tiempo
elevation_data_all = nc.variables['zs'][:]

# Obtener coordenadas globales
globalx = nc.variables['globalx'][:]
globaly = nc.variables['globaly'][:]

# Definir el rango de zoom
xmin_zoom, xmax_zoom = 475750, 477000
ymin_zoom, ymax_zoom = 2.33125e6, 2.33260e6

# Ruta al archivo GeoTIFF
tif_file = "E:/XBeach/halloween/nauka/2d/nonh/nauca.tif"

# Cargar la imagen georreferenciada
with rasterio.open(tif_file) as src:
    img = src.read()
    extent = [src.bounds.left, src.bounds.right, src.bounds.bottom, src.bounds.top]

# Si la imagen tiene tres bandas (RGB), reorganizar para que sea (altura, ancho, bandas)
if img.shape[0] == 3:
    img = img.transpose(1, 2, 0)

# Oscurecer la imagen multiplicando por un factor (ej. 0.5 para 50% de brillo)
darken_factor = 0.8
img = img.astype(float) * darken_factor  # Convertir a float para evitar problemas de desbordamiento

# Asegurarse de que la imagen oscurecida se mantenga dentro del rango de valores válidos [0, 255]
img = np.clip(img, 0, 255).astype(np.uint8)

# Crear y exportar la gráfica 2D para cada paso de tiempo
for t in range(len(elevation_data_all)):
    elevation_data = elevation_data_all[t, :, :]
    
    # Crear la figura con un tamaño específico
    fig, ax = plt.subplots(figsize=(8, 8))
    
    # Mostrar la imagen georreferenciada con sus colores originales
    ax.imshow(img, extent=extent)
    
    # Crear el gráfico 2D de la región de zoom
    mesh = ax.pcolormesh(globalx, globaly, elevation_data, cmap=color_map, vmin=-0.5, vmax=0.5, alpha=0.9)  # Fijar la escala de color y agregar transparencia
    
    # Configurar la fuente para los textos y aumentar el tamaño de letra
    ax.set_xlabel('Coordenada X', fontname='TTInterphasesPro-DmBd', fontsize=14, labelpad=10) # Añadir labelpad para espaciado adicional
    ax.set_ylabel('Coordenada Y', fontname='TTInterphasesPro-DmBd', fontsize=14, labelpad=10) # Añadir labelpad para espaciado adicional
    
    # Configurar los límites de los ejes para el zoom
    ax.set_xlim(xmin_zoom, xmax_zoom)
    ax.set_ylim(ymin_zoom, ymax_zoom)
    
    # Ajustar la escala de colores y aumentar el tamaño de letra
    cbar = plt.colorbar(mesh, ax=ax, label='Nivel de agua (m)', shrink=0.9)
    cbar.ax.yaxis.label.set_fontname('TTInterphasesPro-DmBd')  # Configurar la fuente para el texto de la escala de colores
    cbar.ax.yaxis.label.set_fontsize(14)  # Aumentar el tamaño de letra
    cbar.ax.yaxis.set_label_coords(3.5, 0.5)  # Ajustar la posición de la etiqueta de la escala de colores
    
    ax.set_aspect('equal', adjustable='box')
    ax.grid(True)
    
    # Guardar la figura en la carpeta de exportación
    plt.savefig(os.path.join(export_folder, f'Elevacion_paso_de_tiempo_{t}.png'))
    
    # Mostrar la figura en pantalla
    plt.show()

    # Cerrar la figura para liberar memoria
    plt.close()

print("Figuras de zoom exportadas exitosamente a la carpeta 'for_premiere' en 'post_python'.")
