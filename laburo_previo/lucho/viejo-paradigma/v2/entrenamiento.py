RUTA_VISTAS = '/home/luciano/orga-datos/datos_filtrados/vistas.csv'
RUTA_POSTULACIONES = '/home/luciano/orga-datos/datos_filtrados/postulaciones.csv'
RUTA_SALIDA = '/home/luciano/orga-datos/datos_procesados/no_postulados.csv'

import csv
import avisos
import random

from preprocesar_set import cargar_postulantes, generar_vector

def cargar_vistas():
    '''
    Genera a partir del archivo de vistas un diccionario donde cada clave es
    un id de postulante y cada valor es un set con los avisos vistos
    '''
    salida = set()
    with open(RUTA_VISTAS) as entrada:
        for id_aviso, id_postulante in csv.reader(entrada):
            vistas.add((id_aviso, id_postulante))
            
    return salida

def cargar_postulaciones():
    '''
    Genera a partir del archivo de postulaciones un diccionario donde cada
    clave es un id de postulante y cada valor es un set con los avisos a los
    que se postuló.
    '''
    postulaciones = set()
    with open(RUTA_POSTULACIONES) as entrada:
        for id_aviso, id_postulante in csv.reader(entrada):
            postulaciones.add((id_aviso, id_postulante))
    
    return postulaciones


 
    

def generar_no_postulados():
    print('Cargando postulantes')
    postulantes = cargar_postulantes()
    print('OK')
    print('Cargando postulaciones')
    postulaciones = cargar_postulaciones()
    print('OK')

    avisos_keys = list(avisos.avisos.keys())
    postulantes_keys = list(postulantes.keys())

    cantidad = 0

    no_postulados_a = open(RUTA_SALIDA, 'w')
    no_postulados = csv.writer(no_postulados_a)
    no_postulados.writerow(['idaviso', 'idpostulante', 'sepostulo'])
    pares_creados = set()
    print('Generando...')
    while cantidad < 6000000:
        id_aviso = random.choice(avisos_keys)
        id_postulante = random.choice(postulantes_keys)

        if (id_aviso, id_postulante) in postulaciones:
            continue

        if (id_aviso, id_postulante) in pares_creados:
            continue

        v = generar_vector(avisos.get(id_aviso), postulantes[id_postulante])
        p = 0.05
        if v[1] > 500 or v[2] > 500:
            p += 0.2

        if v[3] == 0:
            p += 0.05

        if v[0] < 0.2:
            p += 0.1

        if v[4] > 2:
            p += 0.2

        if v[5] > 1.8:
            p += 0.1

        if v[6] < -0.7:
            p += 0.1

        if v[7] < -1:
            p += 0.1

        if random.random() < p:
            cantidad += 1
            no_postulados.writerow([id_aviso, id_postulante, '0'])
            pares_creados.add((id_aviso, id_postulante))

        if cantidad % 100000 == 0:
            print(cantidad, '/', 6000000)

    no_postulados_a.close()
    print('OK')
        
    


    
