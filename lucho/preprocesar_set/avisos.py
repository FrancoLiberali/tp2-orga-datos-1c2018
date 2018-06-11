'''
Carga los detalles de los avisos laborales.
Permite obtener la información de un aviso según su ID.
'''

import csv

from rutas import RUTA_AVISOS_DETALLE


def cargar_avisos():
    '''
    Carga el archivo CSV de avisos.
    Devuelve un diccionario de la forma {id_aviso: {"detalle": "valor"}}
    '''

    avisos_cargados = {}
    with open(RUTA_AVISOS_DETALLE) as entrada:
        lector = csv.DictReader(entrada)
        for fila in lector:
            avisos_cargados[fila['idaviso']] = fila

    return avisos_cargados

def get(id_aviso):
    '''
    Devuelve un aviso según su ID.
    Si el aviso no existe lanza KeyError.
    '''
    
    return avisos[id_aviso]

avisos = cargar_avisos()

