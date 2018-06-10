import csv

RUTA_POSTULANTES = '/home/luciano/orga-datos/v3/postulantes.csv'

def cargar_postulantes():
    '''
    Devuelve un set donde cada elemento es un id de postulante.
    '''
    salida = set()
    with open(RUTA_POSTULANTES) as entrada:
        rdr = csv.reader(entrada)
        next(rdr)
        for id_postulante, *_ in rdr:
            salida.add(id_postulante)
    
    return salida

def verificar_postulantes():
    '''
    Verifica que el archivo postulantes.csv contenga a todos los postulantes
    que aparecen en *algun* archivo del set de Navent.
    '''

    RUTA_BASE = '/home/luciano/orga-datos/datos_preprocesados/'
    archivos = ['fiuba_1_postulantes_educacion.csv', 'fiuba_2_postulantes_genero_y_edad.csv',
        'fiuba_6_avisos_detalle.csv', 'fiuba_3_vistas.csv', 'fiuba_4_postulaciones.csv']

    print('Cargando postulantes')
    postulantes = cargar_postulantes()
    print('OK')

    for archivo in archivos:
        print('Verificando archivo {}...'.format(archivo))
        with open(RUTA_BASE + archivo) as entrada:
            rdr = csv.DictReader(entrada)
            for fila in rdr:
                if not 'idpostulante' in fila:
                    print('El archivo no tiene postulantes')
                    break

                if not fila['idpostulante'] in postulantes:
                    print('El postulante {} no está en postulantes.csv'.format(fila['idpostulante']))
