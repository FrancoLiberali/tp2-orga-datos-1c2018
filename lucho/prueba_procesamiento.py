import csv

RUTA_BASE = '/home/luciano/orga-datos/datos_preprocesados/'
RUTA_POSTULANTES    = RUTA_BASE + 'postulantes.csv'
RUTA_VISTAS         = RUTA_BASE + 'fiuba_3_vistas.csv'
RUTA_POSTULACIONES  = RUTA_BASE + 'fiuba_4_postulaciones.csv'
RUTA_AVISOS_DETALLE = RUTA_BASE + 'fiuba_6_avisos_detalle.csv'

TMP_DIR = '/home/luciano/orga-datos/tmp'

def cargar_vistas(avisos, postulantes):
    '''
    Genera a partir del archivo de vistas un set donde cada elemento
    es una tupla (id_aviso, id_postulante)
    '''
    salida = set()
    with open(RUTA_VISTAS) as entrada:
        for id_aviso, _, id_postulante in csv.reader(entrada):
            if not id_aviso in avisos:
                continue
            if not id_postulante in postulantes:
                continue
            salida.add((id_aviso, id_postulante))
            
    return salida

def cargar_postulaciones(avisos, postulantes):
    '''
    Genera a partir del archivo de postulaciones un set donde cada
    elemento es una tupla (id_aviso, id_postulante)
    '''
    salida = set()
    with open(RUTA_POSTULACIONES) as entrada:
        for id_aviso, id_postulante, _ in csv.reader(entrada):
            if not id_aviso in avisos:
                continue
            if not id_postulante in postulantes:
                continue
            salida.add((id_aviso, id_postulante))
    
    return salida

def cargar_avisos():
    '''
    Devuelve un set donde cada elemento es un id de aviso.
    '''
    salida = set()
    with open(RUTA_AVISOS_DETALLE) as entrada:
        for fila in csv.reader(entrada):
            salida.add(fila[0])
    
    return salida

def cargar_postulantes():
    '''
    Devuelve un set donde cada elemento es un id de postulante.
    '''
    salida = set()
    with open(RUTA_POSTULANTES) as entrada:
        for fila in csv.reader(entrada):
            salida.add(fila[0])
    
    return salida


def generar_df():
    avisos = cargar_avisos()
    postulantes = cargar_postulantes()
    vistas = cargar_vistas(avisos, postulantes)
    postulaciones = cargar_postulaciones(avisos, postulantes)
    
    