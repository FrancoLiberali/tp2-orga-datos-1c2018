'''
Carga los detalles de los postulantes.
Permite obtener la información de un postulante según su ID.
'''

import pandas as pd

from rutas import RUTA_POSTULANTES_GENERO_EDAD, RUTA_POSTULANTES_EDUCACION

# Se considera Abandonado y En curso como "incompleto"; Graduado como "completo".
# La métrica induce una distancia. Terciario tiene menos influencia que el resto
# debido a que es muy similar a secundario.
ESCALA_EDUCATIVA = {
    'Otro-Abandonado': 0, # Jardin de infantes
    'Otro-En Curso': 0, #
    'Otro-Graduado': 0, #
    'Secundario-Abandonado': 1, # Sec incompleto
    'Secundario-En Curso': 1, # Sec incompleto
    'Secundario-Graduado': 2, # Sec completo
    'Terciario/Técnico-Abandonado': 2,
    'Terciario/Técnico-En Curso': 2,
    'Terciario/Técnico-Graduado': 2.5,
    'Universitario-Abandonado': 3,
    'Universitario-En Curso': 3,
    'Universitario-Graduado': 4,
    'Posgrado-Abandonado': 5,
    'Posgrado-En Curso': 5,
    'Posgrado-Graduado': 6,
    'Master-Abandonado': 7,
    'Master-En Curso': 7,
    'Master-Graduado': 8,
    'Doctorado-Abandonado': 9,
    'Doctorado-En Curso': 9,
    'Doctorado-Graduado': 10
}

TITULOS = ['Otro', 'Secundario', 'Terciario/Técnico', 'Universitario', 'Posgrado',
    'Master', 'Doctorado']

EDAD_MEDIA = 30
EDAD_MIN = 14
EDAD_MAX = 90


def convertir_fecha_nacimiento_a_edad(fecha):
    if not isinstance(fecha, str):
        return EDAD_MEDIA
    fecha_splitted = fecha.split('-')
    if len(fecha_splitted) != 3:
        return EDAD_MEDIA
    
    anio, *_ = fecha_splitted

    try:
        edad = 2018 - int(anio)
    except ValueError:
        return EDAD_MEDIA
    
    if EDAD_MIN < edad < EDAD_MAX:
        return edad
    
    return EDAD_MEDIA

def cargar_postulantes():
    '''
    Carga el archivo CSV de postulantes.
    Devuelve un DataFrame de pandas con indice = idpostulante
    '''
    print('Cargando postulantes...', end='', flush=True)
    df_genero_edad = pd.read_csv(RUTA_POSTULANTES_GENERO_EDAD)\
        .drop_duplicates(subset=['idpostulante'], keep='last').set_index('idpostulante')
    
    df_genero_edad['sexo'] = df_genero_edad['sexo'].map(lambda x: {'MASC': 1, 'FEM': -1}.get(x, 0))
    df_genero_edad['fechanacimiento'] = df_genero_edad['fechanacimiento'].map(convertir_fecha_nacimiento_a_edad)
    df_genero_edad = df_genero_edad.rename(columns={'fechanacimiento': 'edad'}).reset_index()
    
    df_educacion = pd.read_csv(RUTA_POSTULANTES_EDUCACION)
    
    df_educacion['nivel_educativo'] = df_educacion['nombre'] + '-' + df_educacion['estado']
    df_educacion['nivel_educativo'] = df_educacion['nivel_educativo'].map(lambda x: ESCALA_EDUCATIVA.get(x, 0))
    df_educacion['terciario_completo'] = 0
    df_educacion.loc[(df_educacion['nombre'] == 'Terciario/Técnico') & (df_educacion['estado'] == 'Graduado'), 'terciario_completo'] = 1

    df_educacion_ = pd.merge(df_educacion[['idpostulante']].drop_duplicates(), \
        pd.DataFrame(df_educacion.groupby('idpostulante')[['nivel_educativo']].agg('max')), \
        left_on='idpostulante', right_index=True, how='left')

    df_educacion = pd.merge(df_educacion_, pd.DataFrame(df_educacion.groupby('idpostulante')[['terciario_completo']].agg('max')),\
        left_on='idpostulante', right_index=True, how='left').set_index('idpostulante')

    df_educacion['terciario_completo'] = df_educacion['terciario_completo'].fillna(0)

    print('OK')
    return df_genero_edad, df_educacion

df_genero_edad, df_educacion = cargar_postulantes()
