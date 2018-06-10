'''
El objetivo de este archivo es generar un set de datos consistente.

En el set de datos original se detectó que hay vistas a avisos de los cuales no
tenemos datos. La idea es generar nuevos sets de datos de la siguiente forma:
avisos.csv:
    Toda la información sobre todos los avisos. Eliminados tags HTML de
    descripciones.
    id_aviso, titulo, descripcion, zona, tipo, nivel_laboral, area, empresa

postulantes.csv:
    Toda la información disponible sobre los postulantes.
    id_aviso, edad, sexo, nivel_educativo

vistas.csv:
    Todas las vistas para las cuales existen datos del aviso y postulante
    en cuestión.
    id_aviso, id_postulante

postulaciones.csv:
    Todas las postulaciones para las cuales existen datos del aviso y
    postulante en cuestión.
    id_aviso, id_postulante

vistas_na.csv:
    Todas las vistas para las cuales falta información sobre el aviso.
    id_aviso, id_postulante

vistas_np.csv:
    Todas las vistas para las cuales falta información sobre el postulante.
    id_aviso, id_postulante

vistas_n.csv:
    Todas las vistas para las cuales falta información sobre el postulante y
    el aviso.
    id_aviso, id_postulante

postulaciones_na.csv: [Análogo vistas]
postulaciones_np.csv: [Análogo vistas]
postulaciones_n.csv: [Análogo vistas]
'''

import csv
from rutas import *

RUTA_SALIDA = '/home/luciano/orga-datos/datos_filtrados/'

def cargar_avisos():
    '''
    Devuelve un diccionario donde cada clave es un id de aviso y cada elemento
    es un nombre de área.
    '''
    salida = {}
    with open(RUTA_AVISOS_DETALLE) as entrada:
        rdr = csv.reader(entrada)
        next(rdr)
        for fila in rdr:
            salida[fila[0]] = fila[9]
    
    return salida

def cargar_postulantes():
    '''
    Devuelve un set donde cada elemento es un id de postulante.
    '''
    salida = set()
    with open(RUTA_POSTULANTES) as entrada:
        rdr = csv.reader(entrada)
        next(rdr)
        for fila in rdr:
            salida.add(fila[0])
    
    return salida

def generar_vistas(avisos, postulantes):
    '''
    Genera los archivos vistas.csv, vistas_na.csv, vistas_np.csv y vistas_n.csv
    '''

    with open(RUTA_VISTAS) as entrada, \
         open(RUTA_SALIDA + 'vistas.csv', 'w') as vistas, \
         open(RUTA_SALIDA + 'vistas_n.csv', 'w') as vistas_n, \
         open(RUTA_SALIDA + 'vistas_na.csv', 'w') as vistas_na, \
         open(RUTA_SALIDA + 'vistas_np.csv', 'w') as vistas_np:
        rdr = csv.reader(entrada)
        w_vistas = csv.writer(vistas)
        w_vistas_n = csv.writer(vistas_n)
        w_vistas_na = csv.writer(vistas_na)
        w_vistas_np = csv.writer(vistas_np)

        next(rdr)
        header = ['idaviso', 'idpostulante']
        w_vistas.writerow(header)
        w_vistas_n.writerow(header)
        w_vistas_na.writerow(header)
        w_vistas_np.writerow(header)
        
        for id_aviso, _, id_postulante in rdr:
            if not id_aviso in avisos and not id_postulante in postulantes:
                w_vistas_n.writerow([id_aviso, id_postulante])
            elif not id_aviso in avisos:
                w_vistas_na.writerow([id_aviso, id_postulante])
            elif not id_postulante in postulantes:
                w_vistas_np.writerow([id_aviso, id_postulante])
            else:
                w_vistas.writerow([id_aviso, id_postulante])
        

def generar_postulaciones(avisos, postulantes):
    '''
    Genera los archivos postulaciones.csv, postulaciones_na.csv, postulaciones_np.csv y postulaciones_n.csv
    '''

    with open(RUTA_POSTULACIONES) as entrada, \
         open(RUTA_SALIDA + 'postulaciones.csv', 'w') as postulaciones, \
         open(RUTA_SALIDA + 'postulaciones_n.csv', 'w') as postulaciones_n, \
         open(RUTA_SALIDA + 'postulaciones_na.csv', 'w') as postulaciones_na, \
         open(RUTA_SALIDA + 'postulaciones_np.csv', 'w') as postulaciones_np:
        rdr = csv.reader(entrada)
        w_postulaciones = csv.writer(postulaciones)
        w_postulaciones_n = csv.writer(postulaciones_n)
        w_postulaciones_na = csv.writer(postulaciones_na)
        w_postulaciones_np = csv.writer(postulaciones_np)

        next(rdr)
        header = ['idaviso', 'idpostulante']
        w_postulaciones.writerow(header)
        w_postulaciones_n.writerow(header)
        w_postulaciones_na.writerow(header)
        w_postulaciones_np.writerow(header)
        
        for id_aviso, id_postulante, _ in rdr:
            if id_aviso not in avisos and id_postulante not in postulantes:
                w_postulaciones_n.writerow([id_aviso, id_postulante])
            elif not id_aviso in avisos:
                w_postulaciones_na.writerow([id_aviso, id_postulante])
            elif not id_postulante in postulantes:
                w_postulaciones_np.writerow([id_aviso, id_postulante])
            else:
                w_postulaciones.writerow([id_aviso, id_postulante])
        




def normalizar_set_postulados(avisos, postulantes):
    '''
    Separa el archivo de postulados en 4 archivos:
    postulados.csv [postulaciones donde se conoce aviso y postulante]
    postulados_n.csv [postulaciones donde se desconoce aviso y postulante]
    postulados_na.csv [postulaciones donde se conoce el postulante pero no el aviso]
    postulados_np.csv [postulaciones donde se conoce el aviso pero no el postulante]
    '''
    
    with open('/home/luciano/orga-datos/datos_procesados/postulados.orig.csv') as entrada, \
         open(RUTA_DATOS_PROCESADOS + 'postulados.csv', 'w') as postulaciones, \
         open(RUTA_DATOS_PROCESADOS + 'postulados_n.csv', 'w') as postulaciones_n, \
         open(RUTA_DATOS_PROCESADOS + 'postulados_na.csv', 'w') as postulaciones_na, \
         open(RUTA_DATOS_PROCESADOS + 'postulados_np.csv', 'w') as postulaciones_np:
        rdr = csv.reader(entrada)
        w_postulaciones = csv.writer(postulaciones)
        w_postulaciones_n = csv.writer(postulaciones_n)
        w_postulaciones_na = csv.writer(postulaciones_na)
        w_postulaciones_np = csv.writer(postulaciones_np)

        header = next(rdr)
        w_postulaciones.writerow(header)
        w_postulaciones_n.writerow(header)
        w_postulaciones_na.writerow(header)
        w_postulaciones_np.writerow(header)
        
        for fila in rdr:
            if fila[0] not in avisos and fila[1] not in postulantes:
                w_postulaciones_n.writerow(fila)
            elif not fila[0] in avisos:
                w_postulaciones_na.writerow(fila)
            elif not fila[1] in postulantes:
                w_postulaciones_np.writerow(fila)
            else:
                w_postulaciones.writerow(fila)


def separar_set_kaggle(avisos, postulantes):
    '''
    Separa el archivo de kaggle en 4 archivos:
    kaggle.csv [postulaciones donde se conoce aviso y postulante]
    kaggle_n.csv [postulaciones donde se desconoce aviso y postulante]
    kaggle_na.csv [postulaciones donde se conoce el postulante pero no el aviso]
    kaggle_np.csv [postulaciones donde se conoce el aviso pero no el postulante]
    '''
    
    with open('/home/luciano/orga-datos/datos_procesados/kaggle.orig.csv') as entrada, \
         open(RUTA_DATOS_PROCESADOS + 'kaggle.csv', 'w') as postulaciones, \
         open(RUTA_DATOS_PROCESADOS + 'kaggle_n.csv', 'w') as postulaciones_n, \
         open(RUTA_DATOS_PROCESADOS + 'kaggle_na.csv', 'w') as postulaciones_na, \
         open(RUTA_DATOS_PROCESADOS + 'kaggle_np.csv', 'w') as postulaciones_np:
        rdr = csv.reader(entrada)
        w_postulaciones = csv.writer(postulaciones)
        w_postulaciones_n = csv.writer(postulaciones_n)
        w_postulaciones_na = csv.writer(postulaciones_na)
        w_postulaciones_np = csv.writer(postulaciones_np)

        header = next(rdr)
        w_postulaciones.writerow(header)
        w_postulaciones_n.writerow(header)
        w_postulaciones_na.writerow(header)
        w_postulaciones_np.writerow(header)
        
        for fila in rdr:
            if fila[1] not in avisos and fila[2] not in postulantes:
                w_postulaciones_n.writerow(fila)
            elif not fila[1] in avisos:
                w_postulaciones_na.writerow(fila)
            elif not fila[2] in postulantes:
                w_postulaciones_np.writerow(fila)
            else:
                w_postulaciones.writerow(fila)


    







    
    







    
