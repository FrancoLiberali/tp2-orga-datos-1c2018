'''
Convierte un set de entrenamiento/test/predicción en un vector para utilizar
con un algoritmo de ML.
'''

import csv
from rutas import *
import avisos

RUTA_POSTULANTES  = '/home/luciano/orga-datos/datos_procesados/vector_postulantes_v3.csv'

def generar_data_areas(areas):
    '''
    Dada una lista con los siguientes elementos:
    area, cantidad_postulaciones, cantidad_vistas[, area, cantidad_p ...]
    Devuelve un diccionario donde la clave es el área y el valor es
    2 * cantidad_post + cantidad_vistas
    '''
    data_areas = {}
    for i in range(0, len(areas), 3):
        area, p, v = areas[i:i+3]
        data_areas[area] = 2 * convertir(p) + convertir(v)

    return data_areas

def convertir(valor):
    '''
    Intenta convertir valor a entero o float. Si ambos fallan devuelve str.
    '''
    if valor.isdigit():
        return int(valor)
    
    try:
        return float(valor)
    except ValueError:
        return valor

def cargar_postulantes():
    postulantes = {}

    with open(RUTA_POSTULANTES) as entrada:
        lector = csv.reader(entrada)
        columnas = next(lector)[1:]
        for id_postulante, *detalles in lector:
            postulantes[id_postulante] = {}
            for i, columna in enumerate(columnas):
                postulantes[id_postulante][columna] = convertir(detalles[i])

            postulantes[id_postulante]['areas'] = generar_data_areas(detalles[len(columnas):])

    return postulantes

def calcular_lscore(area_aviso, areas_postulante, total_areas):
    '''
    Calcula el L score. El mismo determina una correlación entre
    el área del aviso y las áreas que el postulante acostumbra.
    Un valor cercano a 0 indica que no hay correlación mientras que un
    valor cercano a 1 indica una correlación fuerte.
    '''
    F = 0.1
    total = sum(areas_postulante.values()) + (F * total_areas)
    if not area_aviso in areas_postulante:
        return (F * total_areas) / total

    return areas_postulante[area_aviso] / total
        

def generar_vector(aviso, postulante):
    lscore = calcular_lscore(aviso['area'], postulante['areas'], avisos.total_areas)
    dist_brc = abs(postulante['d_brc_prom_p'] - aviso['dist_a_brc'])
    dist_salta = abs(postulante['d_salta_prom_p'] - aviso['dist_a_salta'])
    longevidad = 1 if round(postulante['longevidad_prom_p']) == aviso['longevidad'] else 0
    carga = postulante['carga_horaria_prom_p'] / aviso['carga_horaria']
    edad = postulante['edad'] / aviso['prom_edad']
    sexo = postulante['sexo'] * aviso['prom_sexo']
    educ = postulante['educacion'] - aviso['prom_nivel_educativo']
    return [lscore, dist_brc, dist_salta, longevidad, carga, edad, sexo, educ]
    

def preprocesar_set(ruta_entrada, ruta_salida):
    postulantes = cargar_postulantes()

    with open(ruta_entrada) as entrada, open(ruta_salida, 'w') as salida:
        lector = csv.reader(entrada)
        columnas = next(lector)
        ID_AVISO = columnas.index('idaviso')
        ID_POSTU = columnas.index('idpostulante')
        escritor = csv.writer(salida)
        escritor.writerow(columnas + ['lscore', 'dist_brc', 'dist_salta', 'longevidad', 'carga', 'edad', 'sexo', 'educacion'])
        for fila in lector:
            aviso = avisos.get(fila[ID_AVISO])
            postulante = postulantes[fila[ID_POSTU]]
            vector = generar_vector(aviso, postulante)
            escritor.writerow(fila + vector)






















        
