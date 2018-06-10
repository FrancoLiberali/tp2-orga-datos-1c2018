'''
Convierte los datos de los postulantes en un vector:
(edad, sexo, nivel_educativo, interes_en_area[])
edad: entero, edad del participante. Se filtran > EDAD_MAX
sexo: entero, 1 para hombre, -1 para mujer, 0 si no indica.
nivel_educativo: entero entre 0 y 12. Detalle en constante ESCALA_NIVEL EDUCATIVO.
interes_en_area[]: una columna por cada area de anuncio posible.
    El valor de esta columna es Snorm(a).
    S(a) := 2 * Cant postulaciones en area + 1 * Cant vistas en area.
    Snorm(a) := S(a) normalizado

Genera un archivo CSV vector_postulantes.csv con cada id de postulante y sus coordenadas.
'''

import pandas as pd
import numpy as np

RUTA_ENTRADA = '/home/luciano/orga-datos/datos_preprocesados/postulantes.csv'
RUTA_SALIDA  = '/home/luciano/orga-datos/datos_procesados/vector_postulantes_v3.csv'
RUTA_FILTRADA = '/home/luciano/orga-datos/datos_filtrados/'

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

import csv

RUTA_BASE = '/home/luciano/orga-datos/datos_preprocesados/'
RUTA_POSTULANTES    = RUTA_BASE + 'postulantes.csv'
RUTA_VISTAS         = RUTA_BASE + 'fiuba_3_vistas.csv'
RUTA_POSTULACIONES  = RUTA_BASE + 'fiuba_4_postulaciones.csv'
RUTA_AVISOS_DETALLE = RUTA_BASE + 'fiuba_6_avisos_detalle.csv'

TMP_DIR = '/home/luciano/orga-datos/tmp'

def cargar_vistas():
    '''
    Genera a partir del archivo de vistas un diccionario donde cada clave es
    un id de postulante y cada valor es un set con los avisos vistos
    '''
    salida = {}
    with open(RUTA_FILTRADA + 'vistas.csv') as entrada:
        rdr = csv.reader(entrada)
        next(rdr)
        for id_aviso, id_postulante in rdr:
            vistas = salida.get(id_postulante, set())
            vistas.add(id_aviso)
            salida[id_postulante] = vistas
            
    return salida

def cargar_postulaciones():
    '''
    Genera a partir del archivo de postulaciones un diccionario donde cada
    clave es un id de postulante y cada valor es un set con los avisos a los
    que se postuló.
    '''
    salida = {}
    with open(RUTA_FILTRADA + 'postulaciones.csv') as entrada:
        rdr = csv.reader(entrada)
        next(rdr)
        for id_aviso, id_postulante in rdr:
            postulaciones = salida.get(id_postulante, set())
            postulaciones.add(id_aviso)
            salida[id_postulante] = postulaciones
    
    return salida

def cargar_avisos():
    '''
    Devuelve un diccionario donde cada clave es un id de aviso y cada elemento
    es un nombre de área.
    '''
    salida = {}
    with open(RUTA_AVISOS_DETALLE) as entrada:
        for fila in csv.reader(entrada):
            salida[fila[0]] = fila[9]
    
    return salida

MEDIA_EDAD = 30

def convertir_fechanacimiento_en_edad(fecha_nacimiento):    
    fecha_nacimiento_splitted = fecha_nacimiento.split('-')
    if len(fecha_nacimiento_splitted) != 3 or not fecha_nacimiento_splitted[0].isdigit():
        return MEDIA_EDAD
    
    return 2018 - int(fecha_nacimiento_splitted[0])

def convertir_sexo_en_polar(sexo):
    if sexo == 'MASC':
        return 1
    elif sexo == 'FEM':
        return -1

    return 0

def convertir_nivel_educativo_en_numerica(info_postulante):
    NIVELES_EDUCATIVOS = ['Universitario', 'Secundario', 'Terciario/Técnico', 'Posgrado', 'Master', 'Doctorado']
    ESTADOS_POSIBLES = set(('Abandonado', 'En Curso', 'Graduado'))
    niveles_educativos_postulante = [0]
    for nivel in NIVELES_EDUCATIVOS:
        if info_postulante[nivel] not in ESTADOS_POSIBLES:
            continue
        niveles_educativos_postulante.append(ESCALA_NIVEL_EDUCATIVO[(nivel, info_postulante[nivel])])

    return max(niveles_educativos_postulante)

def vectorizar_postulantes():
    #avisos = cargar_avisos()

    import avisos
    print('Avisos cargados')

    cols_areas = [ c[12:] for c in pd.get_dummies(pd.read_csv(RUTA_AVISOS_DETALLE, usecols=['nombre_area']), columns=['nombre_area']).columns ]
    
    d_pv_por_area = {}

    omitidos_postulaciones = 0
    omitidos_vistas = 0
    total_vistas = 0
    total_postulaciones = 0

    print('Procesando postulaciones')
    for id_postulante, postulaciones in cargar_postulaciones().items():
        pv_por_area = d_pv_por_area.get(id_postulante, {})
        for id_aviso in postulaciones:
            total_postulaciones += 1
            if not id_aviso in avisos:
                omitidos_postulaciones += 1
                continue
            area_aviso = avisos[id_aviso]
            pv = pv_por_area.get(area_aviso, [0, 0])
            pv[0] += 1
            pv_por_area[area_aviso] = pv
        d_pv_por_area[id_postulante] = pv_por_area

    print('OK - {}/{} omitidos ({} %)'.format(omitidos_postulaciones, total_postulaciones, (omitidos_postulaciones * 100) / total_postulaciones))

    print('Procesando vistas')
    for id_postulante, vistas in cargar_vistas().items():
        pv_por_area = d_pv_por_area.get(id_postulante, {})
        for id_aviso in vistas:
            total_vistas += 1
            if not id_aviso in avisos:
                omitidos_vistas += 1
                continue
            area_aviso = avisos[id_aviso]
            pv = pv_por_area.get(area_aviso, [0, 0])
            pv[1] += 1
            pv_por_area[area_aviso] = pv
        d_pv_por_area[id_postulante] = pv_por_area

    print('OK - {}/{} omitidos ({} %)'.format(omitidos_vistas, total_vistas, (omitidos_vistas * 100) / total_vistas))

    print('Guardando...')
    with open(RUTA_ENTRADA) as entrada, open(RUTA_SALIDA, 'w') as salida:
        lector = csv.DictReader(entrada)
        escritor = csv.writer(salida)
        escritor.writerow(['idpostulante', 'edad', 'sexo', 'educacion', 'areas'])
        for info_postulante in lector:
            id_postulante = info_postulante['idpostulante']
            nivel_educativo = convertir_nivel_educativo_en_numerica(info_postulante)
            edad = convertir_fechanacimiento_en_edad(info_postulante['fechanacimiento'])
            sexo = convertir_sexo_en_polar(info_postulante['sexo'])

            fila_procesada = [id_postulante, edad, sexo, nivel_educativo]
            if id_postulante in d_pv_por_area:
                for area in d_pv_por_area[id_postulante]:
                    p, v = d_pv_por_area[id_postulante][area]
                    fila_procesada.append(area)
                    fila_procesada.append(p)
                    fila_procesada.append(v)

            escritor.writerow(fila_procesada)

    print('OK')
                    

            
# id, edad, sexo, educacion, P, V, d_prom_brc, d_prom_salta,
#  carga_horaria_prom, longevidad_prom, educ_prom_vista,
#  sexo_prom_vista, edad_prom_vista, areas

# P = cantidad de postulaciones
# V = cantidad de vistas




