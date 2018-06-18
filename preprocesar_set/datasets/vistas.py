'''
Carga las vistas.
Permite obtener los avisos que vio un postulante según su ID.
'''

import pandas as pd

from rutas import RUTA_VISTAS


def cargar_vistas():
    '''
    Carga el archivo CSV de vistas.
    Devuelve un diccionario de la forma {id_postulante: {id_aviso: cantidad de veces visto}}
    '''

    print('Cargando vistas...', end='', flush=True)
    df = pd.read_csv(RUTA_VISTAS, usecols=['idAviso', 'idpostulante']).rename(columns={'idAviso':'idaviso'})
    print('OK')
    return df

df = cargar_vistas()
