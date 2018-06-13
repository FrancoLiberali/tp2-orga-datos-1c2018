#!/usr/bin/python3

'''
Genera tres features que refieren a la información básica del postulante.
- edad: Edad del postulante, por defecto: .EDAD_MEDIA
- sexo: Sexo del postulante -1 si es mujer, 1 si es hombre, 0 por defecto.
- educacion: Nivel educativo del postulante, de 0 a 10 basado en 
    ESCALA_EDUCATIVA, por defecto .NIVEL_EDUCATIVO_MEDIO
Si no se tiene la edad del postulante, devuelve EdadPostulante.EDAD_MEDIA.
'''

import datasets.avisos as avisos
import datasets.postulantes as postulantes
import datasets.vistas as vistas
import datasets.postulaciones as postulaciones
import pandas as pd
import numpy as np
from multiprocessing import Pool as ThreadPool, cpu_count


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

class InformacionBasica:

    def __init__(self):
        '''
        Preprocesa la información de los postulantes.
        '''
        print('Inicializando Información Básica de Postulantes...')
        print(' - Convirtiendo sexo en [-1, 1]...', end='', flush=True)
        df = pd.DataFrame(postulantes.df_genero_edad[['sexo']])
        def convertir_sexo(s):
            if s == 'MASC':
                return 1
            if s == 'FEM':
                return -1
            
            return 0
        df['sexo'] = df['sexo'].map(convertir_sexo)
        print('OK')
        
        print(' - Convirtiendo fecha de nacimiento en edad...', end='', flush=True)
        def convertir_fecha_nacimiento(f):
            if not isinstance(f, str):
                return EDAD_MEDIA
            fecha_splitted = f.split('-')
            if len(fecha_splitted) != 3:
                return EDAD_MEDIA
            
            anio, _, _ = fecha_splitted

            try:
                edad = 2018 - int(anio)
            except ValueError:
                return EDAD_MEDIA
            
            if EDAD_MIN < edad < EDAD_MAX:
                return edad
            
            return EDAD_MEDIA

        df['edad_postulante'] = postulantes.df_genero_edad['fechanacimiento'].map(convertir_fecha_nacimiento)
        print('OK')
        
        print(' - Convirtiendo educación en número...')
        print(' - - Etapa 1/3: concat...', end='', flush=True)
        df['nivel_educativo'] = postulantes.df_educacion['nombre'] + '-' + postulantes.df_educacion['estado']
        print('OK')
        print(' - - Etapa 2/3: map...', end='', flush=True)
        df['nivel_educativo'] = df['nivel_educativo'].map(convertir_educacion_en_numero)
        print('OK')
        print(' - - Etapa 3/3: agg...', end='', flush=True)    
        df['educacion_postulante'] = df.groupby('idpostulante')['nivel_educativo'].agg('max')
        print('OK')
        
        print('OK')
        self.df_info = df.drop(axis=1, labels=['nivel_educativo']).rename(columns={'sexo': 'sexo_postulante'})
        

    def featurize(self, df):
        print('Featurizing información básica')
        return pd.merge(df, self.df_info, how='left', on='idpostulante')




def convertir_educacion_en_numero(nivel):
    return ESCALA_EDUCATIVA.get(nivel, 0)