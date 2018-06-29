import csv

RUTA_BASE = '../../datos_preprocesados/'
RUTA_POSTULANTES    = '../../datos_procesados/vector_postulantes.csv'
RUTA_VISTAS         = RUTA_BASE + 'fiuba_3_vistas.csv'
RUTA_POSTULACIONES  = RUTA_BASE + 'fiuba_4_postulaciones.csv'
RUTA_AVISOS_DETALLE = RUTA_BASE + 'fiuba_6_avisos_detalle.csv'

TMP_DIR = '../../tmp'

def cargar_vistas():
    '''
    Genera a partir del archivo de vistas un set donde cada elemento
    es una tupla (id_aviso, id_postulante)
    '''
    salida = set()
    with open(RUTA_VISTAS) as entrada:
        for id_aviso, _, id_postulante in csv.reader(entrada):
            salida.add((id_aviso, id_postulante))
            
    return salida

def cargar_postulaciones():
    '''
    Genera a partir del archivo de postulaciones un set donde cada
    elemento es una tupla (id_aviso, id_postulante)
    '''
    salida = set()
    with open(RUTA_POSTULACIONES) as entrada:
        for id_aviso, id_postulante, _ in csv.reader(entrada):
            salida.add((id_aviso, id_postulante))
    
    return salida

def cargar_avisos():
    '''
    Devuelve un set donde cada elemento es un id de aviso.
    '''
    salida = set()
    with open(RUTA_AVISOS_DETALLE, encoding="utf8") as entrada:
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

def generar_dataset():
    postulantes    = cargar_postulantes()
    print('Postulantes cargados')
    avisos         = cargar_avisos()
    print('Avisos cargados')
    vistas         = cargar_vistas()
    print('Vistas cargadas')
    postulaciones  = cargar_postulaciones()
    print('Postulaciones cargadas')
    
    with open(TMP_DIR + '/set_entrenamiento.csv', 'w') as salida, \
         open(TMP_DIR + '/err.log', 'w') as errores:
        wrt = csv.writer(salida)
        wrt.writerow(['idaviso', 'idpostulante', 'sepostulo'])
        
        for id_aviso, id_postulante in postulaciones:
            if not id_aviso in avisos:
                errores.write(' '.join(['El aviso', id_aviso, 'no tiene descripcion']) + '\n')
                continue
            if not id_postulante in postulantes:
                errores.write(' '.join(['El postulante', id_postulante, 'no tiene datos']) + '\n')
                continue
            wrt.writerow([id_aviso, id_postulante, '1'])
        
        print('Postulaciones escritas')
        
        for id_aviso, id_postulante in vistas:
            if (id_aviso, id_postulante) in postulaciones:
                continue # Si se postuló, omitirlo
            if not id_aviso in avisos:
                errores.write(' '.join(['El aviso', id_aviso, 'no tiene descripcion']) + '\n')
                continue
            if not id_postulante in postulantes:
                errores.write(' '.join(['El postulante', id_postulante, 'no tiene datos']) + '\n')
                continue
            wrt.writerow([id_aviso, id_postulante, '0'])
        
        print('Vistas escritas')
        
generar_dataset()