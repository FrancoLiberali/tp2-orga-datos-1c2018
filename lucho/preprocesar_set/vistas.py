'''
Carga las vistas.
Permite obtener los avisos que vio un postulante según su ID.
'''

import csv

from rutas import RUTA_VISTAS

vistas = cargar_vistas()

def cargar_vistas():
    '''
    Carga el archivo CSV de vistas.
    Devuelve un diccionario de la forma {id_postulante: {id_aviso: cantidad de veces visto}}
    '''

    vistas_cargadas = {}

    with open(RUTA_VISTAS) as entrada:
        lector = csv.reader(entrada)
        next(lector)

        for id_aviso, _, id_postulante in lector:
            vistas_por_postulante = vistas_cargadas.get(id_postulante, {})
            vistas_por_postulante[id_aviso] = vistas_por_postulante.get(id_aviso, 0) + 1
            vistas_cargadas[id_postulante] = vistas_por_postulante

    return vistas_cargadas

def get(id_postulante):
    '''
    Devuelve las vistas de un postulante según su ID.
    Si el postulante no existe lanza KeyError.
    '''
    
    return vistas[id_postulante]