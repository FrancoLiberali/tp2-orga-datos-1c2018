'''
Carga los detalles de los postulantes.
Permite obtener la información de un postulante según su ID.
'''

import pandas as pd

from rutas import RUTA_POSTULANTES_GENERO_EDAD, RUTA_POSTULANTES_EDUCACION


def cargar_postulantes():
    '''
    Carga el archivo CSV de postulantes.
    Devuelve un DataFrame de pandas con indice = idpostulante
    '''
    print('Cargando postulantes...', end='', flush=True)
    df_genero_edad = pd.read_csv(RUTA_POSTULANTES_GENERO_EDAD)\
        .drop_duplicates(subset=['idpostulante'], keep='last').set_index('idpostulante')
    df_educacion   = pd.read_csv(RUTA_POSTULANTES_EDUCACION)
    print('OK')
    return df_genero_edad, df_educacion

df_genero_edad, df_educacion = cargar_postulantes()
