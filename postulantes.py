'''
Convierte los datos de los postulantes en un vector de tres coordenadas:
(edad, sexo, nivel_educativo)
edad: entero, edad del participante. Se filtran > EDAD_MAX
sexo: entero, 1 para hombre, -1 para mujer, 0 si no indica.
nivel_educativo: entero entre 0 y 12. Detalle en constante ESCALA_NIVEL EDUCATIVO.

Genera un archivo CSV vector_postulantes.csv con cada id de postulante y sus coordenadas.
'''

import pandas as pd
import numpy as np

RUTA_ENTRADA = '/home/luciano/orga-datos/datos_preprocesados/postulantes.csv'
RUTA_SALIDA  = '/home/luciano/orga-datos/datos_procesados/vector_postulantes.csv'

EDAD_MAX = 90

# Se considera Abandonado y En curso como "incompleto"; Graduado como "completo".
# La métrica induce una distancia. Terciario tiene menos influencia que el resto
# debido a que es muy similar a secundario.
ESCALA_NIVEL_EDUCATIVO = {
    ('Otro', 'Abandonado'): 0, # Jardin de infantes
    ('Otro', 'En Curso'): 0, #
    ('Otro', 'Graduado'): 0, #
    ('Secundario', 'Abandonado'): 1, # Sec incompleto
    ('Secundario', 'En Curso'): 1, # Sec incompleto
    ('Secundario', 'Graduado'): 2, # Sec completo
    ('Terciario/Técnico', 'Abandonado'): 2,
    ('Terciario/Técnico', 'En Curso'): 2,
    ('Terciario/Técnico', 'Graduado'): 2.5,
    ('Universitario', 'Abandonado'): 3,
    ('Universitario', 'En Curso'): 3,
    ('Universitario', 'Graduado'): 4,
    ('Posgrado', 'Abandonado'): 5,
    ('Posgrado', 'En Curso'): 5,
    ('Posgrado', 'Graduado'): 6,
    ('Master', 'Abandonado'): 7,
    ('Master', 'En Curso'): 7,
    ('Master', 'Graduado'): 8,
    ('Doctorado', 'Abandonado'): 9,
    ('Doctorado', 'En Curso'): 9,
    ('Doctorado', 'Graduado'): 10
}

def vectorizar_postulantes():
    postulantes = pd.read_csv(RUTA_ENTRADA)
    
    # Potencial problema: Los que no tienen edad tiran el promedio para abajo
    
    postulantes['edad'] = postulantes['fechanacimiento'].map(lambda x: 2018 - int(x.split('-')[0]) if isinstance(x, str) else 0)
    postulantes = postulantes[postulantes['edad'] <= EDAD_MAX]
    postulantes = postulantes.drop(axis=1, labels=['fechanacimiento'])    
    
    postulantes['sexo'] = postulantes['sexo'].map(lambda x: {'MASC': 1, 'FEM': -1, 'NO_DECLARA': 0, '0.0': 0, '0': 0}[x] if isinstance(x, str) else 0)

    for c in postulantes.columns[1:8]:
        postulantes[c] = postulantes[c].map(lambda x: 0 if x == '0' else ESCALA_NIVEL_EDUCATIVO[(c, x)])

    postulantes['nivel_educativo'] = np.max(postulantes[['Universitario', 'Secundario', 'Terciario/Técnico', 'Posgrado', 'Master', 'Doctorado']], axis=1)
    postulantes = postulantes.drop(axis=1, labels=['Universitario', 'Secundario', 'Terciario/Técnico', 'Posgrado', 'Master', 'Doctorado', 'Otro'])
    postulantes.to_csv(RUTA_SALIDA, index = False)