''' 
Obtiene información sobre los avisos.
'''

import csv
from rutas import *

avisos = {}

total_areas = 0

with open(RUTA_DATOS_PROCESADOS + 'avisos_detalle.csv') as entrada:
    lector = csv.reader(entrada)
    columnas = next(lector)
    for columna in columnas:
        if columna.startswith('nombre_area'):
            total_areas += 1
    
    for fila in lector:
        data_aviso = {}
        for i, columna in enumerate(columnas):
            if i == 0:
                continue
            if columna.startswith('nombre_area'):
                if fila[i] == '1':
                    data_aviso['area'] = columna[12:]
                else:
                    continue
            if fila[i].isdigit():
                data_aviso[columna] = int(fila[i])
            else:
                try:
                    data_aviso[columna] = float(fila[i])
                except ValueError:
                    data_aviso[columna] = fila[i]
        avisos[fila[0]] = data_aviso

    

def get(id_aviso):
    return avisos[id_aviso]

