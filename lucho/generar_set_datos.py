import csv

import random
random.seed(12)

RUTA_BASE = '/home/luciano/orga-datos/v3/'
RUTA_POSTULANTES    = RUTA_BASE + 'sample_postulantes.csv'
RUTA_VISTAS         = RUTA_BASE + 'fiuba_3_vistas.csv'
RUTA_POSTULACIONES  = RUTA_BASE + 'fiuba_4_postulaciones.csv'
RUTA_AVISOS_DETALLE = RUTA_BASE + 'fiuba_6_avisos_detalle.csv'

def cargar_vistas(postulantes):
    '''
    Genera a partir del archivo de vistas un set donde cada elemento
    es una tupla (id_aviso, id_postulante).
    Solo se mantienen las vistas que refieren a un postulante en
    postulantes.
    '''
    salida = set()
    with open(RUTA_VISTAS) as entrada:
        rdr = csv.reader(entrada)
        next(rdr)
        for id_aviso, _, id_postulante in rdr:
            if not id_postulante in postulantes:
                continue
            salida.add((id_aviso, id_postulante))
            
    return salida

def cargar_postulaciones(postulantes):
    '''
    Genera a partir del archivo de postulaciones un set donde cada
    elemento es una tupla (id_aviso, id_postulante).
    Solo se mantienen las postulaciones de los postulantes que esten en
    postulantes.
    '''
    salida = set()
    with open(RUTA_POSTULACIONES) as entrada:
        rdr = csv.reader(entrada)
        next(rdr)
        for id_aviso, id_postulante, _ in rdr:
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
        rdr = csv.reader(entrada)
        next(rdr)
        for fila in rdr:
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


def generar_set():
    postulantes = cargar_postulantes()
    avisos = list(cargar_avisos())
    vistas = cargar_vistas(postulantes)
    postulaciones = cargar_postulaciones(postulantes)
    postulantes = list(postulantes)

    print('Hay', len(postulaciones), 'postulaciones en total')

    # Considero 45k postulaciones y 55k no postulaciones
    postulaciones_sampled = random.sample(list(postulaciones), 45000)

    # De las 55k no postulaciones tomo 45k vistas no convertidas
    # y 10k avisos random
    vistas_no_postuladas = random.sample(list(vistas.difference(postulaciones)), 45000)
    
    no_postulaciones_random = set()
    i = 0
    while i < 10000:
        no_postulacion = (random.choice(avisos), random.choice(postulantes))

        for grupo in [postulaciones, vistas, no_postulaciones_random]:
            if no_postulacion in grupo:
                continue

        no_postulaciones_random.add(no_postulacion)
        i += 1

    with open(RUTA_BASE + 'set_test.csv', 'w') as salida:
        wrt = csv.writer(salida)
        wrt.writerow(['idaviso', 'idpostulante', 'sepostulo'])
        for id_aviso, id_postulante in postulaciones_sampled:
            wrt.writerow([id_aviso, id_postulante, '1'])

        for id_aviso, id_postulante in vistas_no_postuladas:
            wrt.writerow([id_aviso, id_postulante, '0'])

        for id_aviso, id_postulante in no_postulaciones_random:
            wrt.writerow([id_aviso, id_postulante, '0'])
        













        
