'''
Carga las postulaciones.
Permite obtener los avisos a los que se postuló un postulante según su ID.
'''

import csv

from rutas import RUTA_POSTULACIONES


def cargar_postulaciones():
    '''
    Carga el archivo CSV de postulaciones.
    Devuelve un diccionario de la forma {id_postulante: set(id_aviso, ...)}
    '''

    postulaciones_cargadas = {}

    with open(RUTA_POSTULACIONES) as entrada:
        lector = csv.reader(entrada)
        next(lector)
        for id_aviso, id_postulante, _ in lector:
            postulaciones_por_postulante = postulaciones_cargadas.get(id_postulante, set())
            postulaciones_por_postulante.add(id_aviso)
            postulaciones_cargadas[id_postulante] = postulaciones_por_postulante

    return postulaciones_cargadas

def get(id_postulante):
    '''
    Devuelve las postulaciones de un postulante según su ID.
    Si el postulante no existe devuelve un set vacío.
    '''

    if not id_postulante in postulaciones:
        return set()
    return postulaciones[id_postulante]

postulaciones = cargar_postulaciones()
