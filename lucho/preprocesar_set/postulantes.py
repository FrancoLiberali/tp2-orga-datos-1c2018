'''
Carga los detalles de los postulantes.
Permite obtener la información de un postulante según su ID.
'''

import csv

from rutas import RUTA_POSTULANTES_DETALLE


def cargar_postulantes():
    '''
    Carga el archivo CSV de postulantes.
    Devuelve un diccionario de la forma {id_postulante: {"detalle": "valor"}}
    '''
    postulantes_cargados = {}
    with open(RUTA_POSTULANTES_DETALLE) as entrada:
        lector = csv.DictReader(entrada)
        for fila in lector:
            postulantes_cargados[fila['idpostulante']] = fila

    return postulantes_cargados

def get(id_postulante):
    '''
    Devuelve un postulante según su ID.
    Si el postulante no existe lanza KeyError.
    '''
    
    return postulantes[id_postulante]

postulantes = cargar_postulantes()
