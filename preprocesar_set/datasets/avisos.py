'''
Carga los detalles de los avisos laborales.
Permite obtener la información de un aviso según su ID.
'''

import pandas as pd

from rutas import RUTA_AVISOS_DETALLE

def cargar_avisos():
    '''
    Carga el archivo CSV de avisos.
    Devuelve un diccionario de la forma {id_aviso: {"detalle": "valor"}}
    '''
    print('Cargando avisos...', end='', flush=True)
    df = pd.read_csv(RUTA_AVISOS_DETALLE)
    print('OK')
    return df.set_index('idaviso')

def get(id_aviso):
    '''
    Devuelve un aviso según su ID.
    Si el aviso no existe lanza KeyError.
    '''
    
    return df.loc[id_aviso].to_dict()

def exists(id_aviso):
    '''
    Devuelve True si hay datos sobre el aviso.
    '''

    return id_aviso in df.index

df = cargar_avisos()

