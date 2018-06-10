import csv

RUTA_BASE = '/home/luciano/orga-datos/datos_preprocesados/'
RUTA_POSTULANTES    = RUTA_BASE + 'postulantes.csv'
RUTA_VISTAS         = RUTA_BASE + 'fiuba_3_vistas.csv'
RUTA_POSTULACIONES  = RUTA_BASE + 'fiuba_4_postulaciones.csv'
RUTA_AVISOS_DETALLE = RUTA_BASE + 'fiuba_6_avisos_detalle.csv'

TMP_DIR = '/home/luciano/orga-datos/tmp'

import random

def cargar_vistas():
    '''
    Genera a partir del archivo de vistas un diccionario donde cada clave es
    un id de postulante y cada valor es un set con los avisos vistos
    '''
    salida = {}
    with open(RUTA_VISTAS) as entrada:
        for id_aviso, _, id_postulante in csv.reader(entrada):
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
    with open(RUTA_POSTULACIONES) as entrada:
        rdr = csv.reader(entrada)
        next(rdr)
        for id_aviso, id_postulante, _ in rdr:
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
        rdr = csv.reader(entrada)
        next(rdr)
        for fila in rdr:
            salida[fila[0]] = fila[9]
    
    return salida

def get_aviso_no_postulado(id_postulante, avisos_keys, postulaciones):
    if id_postulante not in postulaciones:
        return random.choice(avisos_keys)

    no_postulado = random.choice(avisos_keys)
    while no_postulado in postulaciones[id_postulante]:
        no_postulado = random.choice(avisos_keys)

    return no_postulado

RUTA_NUEVO = '/home/luciano/orga-datos/nuevo_set/'

def generar_dataset():
    avisos         = cargar_avisos()
    avisos_keys = list(avisos.keys())
    print('Avisos cargados')
    postulaciones  = cargar_postulaciones()
    print('Postulaciones cargadas')

    
    
    with open(RUTA_NUEVO + 'postulantes_for_sample.csv') as entrada,\
         open(RUTA_NUEVO + 'set_test.csv', 'w') as salida:
        rdr = csv.reader(entrada)
        next(rdr)
        wrt = csv.writer(salida)
        wrt.writerow(['idaviso', 'idpostulante', 'sepostulo'])

        postulaciones_total = 0
        
        for id_postulante, *detalles in rdr:
            if postulaciones_total > 50000:
                wrt.writerow([get_aviso_no_postulado(id_postulante, avisos_keys, postulaciones), id_postulante, '0'])
            elif id_postulante in postulaciones:
                postulaciones_total += 1
                wrt.writerow([random.choice(list(postulaciones[id_postulante])), id_postulante, '1'])
            else:
                wrt.writerow([get_aviso_no_postulado(id_postulante, avisos_keys, postulaciones), id_postulante, '0'])
