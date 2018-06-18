'''
Carga las postulaciones.
Permite obtener los avisos a los que se postuló un postulante según su ID.
'''

import pandas as pd

from rutas import RUTA_POSTULACIONES


def cargar_postulaciones():
    '''
    Carga el archivo CSV de postulaciones.
    Devuelve un DataFrame
    '''
    print('Cargando postulaciones...', end='', flush=True)
    df = pd.read_csv(RUTA_POSTULACIONES, usecols=['idaviso', 'idpostulante'])
    print('OK')
    return df

df = cargar_postulaciones()
