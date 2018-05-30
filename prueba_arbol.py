import csv
import pandas as pd
import numpy as np

RUTA_BASE = '/home/luciano/orga-datos/datos_preprocesados/'
RUTA_POSTULANTES    = RUTA_BASE + 'postulantes.csv'
RUTA_VISTAS         = RUTA_BASE + 'fiuba_3_vistas.csv'
RUTA_POSTULACIONES  = RUTA_BASE + 'fiuba_4_postulaciones.csv'
RUTA_AVISOS_DETALLE = RUTA_BASE + 'fiuba_6_avisos_detalle.csv'

def cargar_vistas():
    '''
    Genera a partir del archivo de vistas un diccionario donde
    las claves son los ID de postulante y los valores un set con 
    cada id de aviso que vio.
    '''
    salida = {}
    with open(RUTA_VISTAS) as entrada:
        for id_aviso, _, id_postulante in csv.reader(entrada):
            avisos_por_postulante = salida.get(id_postulante, set())
            avisos_por_postulante.add(id_aviso)
            salida[id_postulante] = avisos_por_postulante
    
    return salida

def cargar_postulaciones():
    '''
    Genera a partir del archivo de postulaciones un diccionario donde
    las claves son los ID de postulante y los valores un set con cada
    id de aviso al que se postuló
    '''
    salida = {}
    with open(RUTA_POSTULACIONES) as entrada:
        for id_aviso, id_postulante, _ in csv.reader(entrada):
            avisos_por_postulante = salida.get(id_postulante, set())
            avisos_por_postulante.add(id_aviso)
            salida[id_postulante] = avisos_por_postulante
    
    return salida

def cargar_avisos():
    '''
    Devuelve un diccionario donde las claves son ID de aviso y los 
    valores una tupla con los siguientes features:
    [nombre_zona, tipo_de_trabajo, nombre_area]
    '''
    salida = {}
    with open(RUTA_AVISOS_DETALLE) as entrada:
        for fila in csv.reader(entrada):
            id_aviso, zona, tipo, area = fila[0], fila[4], fila[7], fila[9]
            salida[id_aviso] = (zona, tipo, area)
    
    return salida

ORDEN_EDUCACION = ['Otro', 'Secundario', 'Terciario/Técnico', 'Universitario', 'Posgrado', 'Doctorado', 'Master']
ORDEN_EN_ARCHIVO = ['Doctorado', 'Master', 'Otro', 'Posgrado', 'Secundario', 'Terciario/Técnico', 'Universitario']
def procesar_postulante(fila):
    '''
    Extrae la información de un registro del archivo de
    postulantes.
    '''
    anio_nacimiento = fila[-2].split('-')[0]
    if anio_nacimiento.isdigit():
        return (int(anio_nacimiento), fila[-1])

    return (30, fila[-1])
    

def cargar_postulantes():
    '''
    Devuelve un diccionario donde las claves son ID de postulante
    y los valores una tupla con los siguientes features:
    [edad, sexo, maximo_nivel_educativo]
    '''
    salida = {}
    with open(RUTA_POSTULANTES) as entrada:
        for fila in csv.reader(entrada):
            id_postulante = fila[0]
            salida[id_postulante] = procesar_postulante(fila)
    
    return salida
import random
    
def obtener_muestra(poblacion, k_max):
    '''
    Devuelve una lista con k_max o menos elementos elegidos aleatoriamente
    de poblacion.
    '''
    if len(poblacion) >= k_max:
        return random.sample(poblacion, k_max)
    return list(poblacion)
    
def generar_dataset():
    postulantes    = cargar_postulantes()
    print('Postulantes cargados')
    avisos         = cargar_avisos()
    print('Avisos cargados')
    vistas         = cargar_vistas()
    print('Vistas cargadas')
    postulaciones  = cargar_postulaciones()
    print('Postulaciones cargadas')
    
    with open('/home/luciano/orga-datos/set_entrenamiento.csv', 'w') as salida:
        wrt = csv.writer(salida)
        wrt.writerow(['idaviso', 'idpostulante', 'sepostulo'])
        for postulante, data in postulantes.items():
            vistos = vistas.get(postulante, set())
            postulados = postulaciones.get(postulante, set())
            vistos = vistos - postulados
            muestra_vistos = obtener_muestra(vistos, 3)
            muestra_postulados = obtener_muestra(postulados, 3)
            
            for id_aviso in muestra_vistos:
                if not id_aviso in avisos:
                    continue
                wrt.writerow([id_aviso, postulante, '0'])
            
            for id_aviso in muestra_postulados:
                if not id_aviso in avisos:
                    continue
                wrt.writerow([id_aviso, postulante, '1'])
            
            
    
    
    