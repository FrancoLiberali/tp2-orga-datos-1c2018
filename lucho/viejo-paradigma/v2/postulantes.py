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

EDAD_MIN = 14
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
        return 0
    
    edad = 2018 - int(fecha_nacimiento_splitted[0])
    if EDAD_MIN < edad < EDAD_MAX:
        return edad

    return 0

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
    import avisos
    print('Avisos cargados')

    cols_areas = [ c[12:] for c in pd.get_dummies(pd.read_csv(RUTA_AVISOS_DETALLE, usecols=['nombre_area']), columns=['nombre_area']).columns ]
    
    data_postulantes = {}

    print('Procesando postulaciones')
    for id_postulante, postulaciones in cargar_postulaciones().items():
        data_postulante = data_postulantes.get(id_postulante, {})
        for id_aviso in postulaciones:
            data_aviso = data_postulante.get(id_aviso, [0, 0])
            data_aviso[0] += 1
            data_postulante[id_aviso] = data_aviso
        data_postulantes[id_postulante] = data_postulante

    print('Procesando vistas')
    for id_postulante, vistas in cargar_vistas().items():
        data_postulante = data_postulantes.get(id_postulante, {})
        for id_aviso in vistas:
            data_aviso = data_postulante.get(id_aviso, [0, 0])
            data_aviso[1] += 1
            data_postulante[id_aviso] = data_aviso
        data_postulantes[id_postulante] = data_postulante


    print('Guardando...')

    ne_inferidos = 0
    e_inferidos = 0
    s_inferidos = 0
    ne_no_inferidos = 0
    e_no_inferidos = 0
    s_no_inferidos = 0
    
    with open(RUTA_ENTRADA) as entrada, open(RUTA_SALIDA, 'w') as salida:
        lector = csv.DictReader(entrada)
        escritor = csv.writer(salida)
        escritor.writerow(['idpostulante', 'edad', 'sexo', 'educacion', 'cantidad_post',
            'cantidad_vistas', 'd_brc_prom_p', 'd_brc_prom_v', 'd_salta_prom_p', 'd_salta_prom_v',
            'carga_horaria_prom_p', 'carga_horaria_prom_v', 'longevidad_prom_p', 'longevidad_prom_v',
            'educ_prom_p', 'educ_prom_v', 'sexo_prom_p', 'sexo_prom_v', 'edad_prom_p', 'edad_prom_v'])
        for info_postulante in lector:
            id_postulante = info_postulante['idpostulante']
            nivel_educativo = convertir_nivel_educativo_en_numerica(info_postulante)
            edad = convertir_fechanacimiento_en_edad(info_postulante['fechanacimiento'])
            sexo = convertir_sexo_en_polar(info_postulante['sexo'])
            info = []

            if id_postulante in data_postulantes:
                if nivel_educativo == 0:
                    nivel_educativo = inferir_desde_datos(data_postulantes[id_postulante], avisos, 'nivel_educativo')
                    if nivel_educativo == 0:
                        ne_no_inferidos += 1
                        nivel_educativo = 2
                    else:
                        ne_inferidos += 1
                        
                if edad == 0:
                    edad = inferir_desde_datos(data_postulantes[id_postulante], avisos, 'edad')
                    if edad == 0:
                        e_no_inferidos += 1
                        edad = 30
                    else:
                        e_inferidos += 1
                    
                if sexo == 0:
                    sexo = inferir_desde_datos(data_postulantes[id_postulante], avisos, 'sexo', 3)
                    if sexo == 3:
                        s_no_inferidos += 1
                    else:
                        s_inferidos += 1
                    
                info = generar_informacion_sobre_postulante(data_postulantes[id_postulante], avisos)

            if nivel_educativo == 0:
                ne_no_inferidos += 1
                nivel_educativo = 2
            if edad == 0:
                e_no_inferidos += 1
                edad = 30
            if sexo == 3:
                s_no_inferidos += 1
                sexo = 0

            fila_procesada = [id_postulante, edad, sexo, nivel_educativo] + info
            escritor.writerow(fila_procesada)

    print('ne_inferidos:', ne_inferidos, '-', 'ne_no_inferidos:', ne_no_inferidos)
    print('e_inferidos:', e_inferidos, '-', 'e_no_inferidos:', e_no_inferidos)
    print('s_inferidos:', s_inferidos, '-', 's_no_inferidos:', s_no_inferidos)

    print('OK')
                    
def inferir_desde_datos(data_postulante, avisos, columna, defecto=0):
    '''
    Intenta inferir el dato faltante del postulante desde sus avisos vistos
    y postulados.
    Si la inferencia falla se devuelve el valor por defecto.
    Se buscará en la columna prom_{columna} de cada aviso.
    '''

    columna = 'prom_' + columna

    data_prom = 0
    total = 0
    
    P = 0
    V = 1

    FACTOR_VISTA = 1 # Importancia de la vista
    FACTOR_POSTU = 3 # Importancia de la postulación

    # La inferencia se considera válida cuando se encontró una cantidad de
    # información equivalente a la que aportarían MINIMO_VISTA vistas y
    # MINIMO_POSTU postulaciones.
    # Esto no significa que haya exactamente 2 postulaciones y 2 vistas.
    # Puede haber 3 postulaciones y 0 vistas y la cantidad de información
    #  "es" equivalente [esta equivalencia depende de FACTOR_VISTA y FACTOR_POSTU].
    MINIMO_VISTA = 2
    MINIMO_POSTU = 2

    for id_aviso, pv in data_postulante.items():
        aviso = avisos.get(id_aviso)
        if aviso[columna]:
            data_prom += aviso[columna] * pv[V] * FACTOR_VISTA
            data_prom += aviso[columna] * pv[P] * FACTOR_POSTU
            total += (pv[V] * FACTOR_VISTA) + (pv[P] * FACTOR_POSTU)

    if total < (MINIMO_VISTA * FACTOR_VISTA + MINIMO_POSTU * FACTOR_POSTU):
        return defecto

    return data_prom / total

def generar_informacion_sobre_postulante(data_postulante, avisos):
    '''
    Genera información sobre un postulante basandose en los
    anuncios que vió y los que se postuló.
    data_postulante = { id_anuncio: (cantidad_vistas, cantidad_postulaciones) }
    Devuelve una lista con los siguientes elementos:
    P, V, d_brc_prom, d_salta_prom, carga_horaria_prom, longevidad_prom,
    educ_prom, sexo_prom, edad_prom, [areas, Pa, Va]*
    Todas las columnas terminadas en _prom valen por dos:
    _prom_postulaciones, _prom_vistas
    '''
    P = 0
    V = 1
    
    pv_total = [0, 0]
    d_brc_prom = [0, 0]
    d_salta_prom = [0, 0]
    carga_horaria_prom = [0, 0]
    longevidad_prom = [0, 0]
    educ_prom = [0, 0]
    sexo_prom = [0, 0]
    edad_prom = [0, 0]

    areas = {}

    for id_aviso, pv in data_postulante.items():
        aviso = avisos.get(id_aviso)
        pv_por_area = areas.get(aviso['area'], [0, 0])
        for i in [P, V]:
            pv_total[i] += pv[i]
            d_brc_prom[i] += aviso['dist_a_brc'] * pv[i]
            d_salta_prom[i] += aviso['dist_a_salta'] * pv[i]
            carga_horaria_prom[i] += aviso['carga_horaria'] * pv[i]
            longevidad_prom[i] += aviso['longevidad'] * pv[i]
            educ_prom[i] += aviso['prom_nivel_educativo'] * pv[i]
            sexo_prom[i] += aviso['prom_sexo'] * pv[i]
            edad_prom[i] += aviso['prom_edad'] * pv[i]
            pv_por_area[i] += pv[i]
        areas[aviso['area']] = pv_por_area

    for i in [P, V]:
        if pv_total[i] == 0:
            continue
        d_brc_prom[i] = d_brc_prom[i] / pv_total[i]
        d_salta_prom[i] = d_salta_prom[i] / pv_total[i]
        carga_horaria_prom[i] = carga_horaria_prom[i] / pv_total[i]
        longevidad_prom[i] = longevidad_prom[i] / pv_total[i]
        educ_prom[i] = educ_prom[i] / pv_total[i]
        sexo_prom[i] = sexo_prom[i] / pv_total[i]
        edad_prom[i] = edad_prom[i] / pv_total[i]

    v_areas = []
    for area, pv in areas.items():
        v_areas.append(area)
        v_areas.append(pv[P])
        v_areas.append(pv[V])

    return pv_total + d_brc_prom + d_salta_prom + carga_horaria_prom +\
        longevidad_prom + educ_prom + sexo_prom + edad_prom + v_areas

    
            
# id, edad, sexo, educacion, P, V, d_prom_brc, d_prom_salta,
#  carga_horaria_prom, longevidad_prom, educ_prom_vista,
#  sexo_prom_vista, edad_prom_vista, areas

# P = cantidad de postulaciones
# V = cantidad de vistas

# Pa = cantidad de postulaciones en el área
# Va = cantidad de vistas en el área



