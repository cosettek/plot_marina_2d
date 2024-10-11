# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 14:28:12 2024

@author: Poseidon
"""

from netCDF4 import Dataset

# Ruta al archivo NetCDF
file_path = "E:/XBeach/halloween/nauka/2d/nonh/5/xboutput.nc"  # Cambia la ruta según sea necesario

# Abrir el archivo NetCDF
nc = Dataset(file_path, "r")

# Listar las variables en el archivo
print("Variables en el archivo NetCDF:")
for var_name in nc.variables:
    var = nc.variables[var_name]
    print(f"{var_name}: {var.dimensions}, tamaño: {var.shape}")

# Cerrar el archivo
nc.close()
