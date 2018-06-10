import csv

RUTA_AVISOS_DETALLE = '/home/luciano/orga-datos/datos_preprocesados/fiuba_6_avisos_detalle.csv'
RUTA_VISTAS = '/home/luciano/orga-datos/datos_preprocesados/fiuba_3_vistas.csv'
RUTA_VISTAS_SALIDA = '/home/luciano/orga-datos/v3/fiuba_3_vistas.csv'
RUTA_POSTULACIONES = '/home/luciano/orga-datos/datos_preprocesados/fiuba_4_postulaciones.csv'
RUTA_POSTULACIONES_SALIDA = '/home/luciano/orga-datos/v3/fiuba_4_postulaciones.csv'

def cargar_avisos():
    '''
    Devuelve un set donde cada elemento es un id de aviso.
    '''
    salida = set()
    with open(RUTA_AVISOS_DETALLE) as entrada:
        rdr = csv.reader(entrada)
        next(rdr)
        for id_aviso, *_ in rdr:
            salida.add(id_aviso)
    
    return salida

def limpiar_vistas(avisos):
    with open(RUTA_VISTAS) as entrada, open(RUTA_VISTAS_SALIDA, 'w') as salida:
        rdr = csv.reader(entrada)
        header = next(rdr)
        wrt = csv.writer(salida)
        wrt.writerow(header)

        I_AVISO = header.index('idAviso')

        for fila in rdr:
            if not fila[I_AVISO] in avisos:
                continue

            wrt.writerow(fila)
        
def limpiar_postulaciones(avisos):
    with open(RUTA_POSTULACIONES) as entrada, open(RUTA_POSTULACIONES_SALIDA, 'w') as salida:
        rdr = csv.reader(entrada)
        header = next(rdr)
        wrt = csv.writer(salida)
        wrt.writerow(header)

        I_AVISO = header.index('idaviso')

        for fila in rdr:
            if not fila[I_AVISO] in avisos:
                continue

            wrt.writerow(fila)
        
def limpiar_interacciones():
    print('Cargando avisos...')
    avisos = cargar_avisos()
    print('OK')

    print('Limpiando vistas...')
    limpiar_vistas(avisos)
    print('OK')

    print('Limpiar postulaciones...')
    limpiar_postulaciones(avisos)
    print('OK')
