#!/usr/bin/python3

'''
Realiza la conversión del set id, idaviso, idpostulante en vectores
para poder predecir mediante algoritmos de machine learning.
'''

import csv
import sys
import os

from featurizers.informacion_basica import InformacionBasica
from featurizers.cantidad_pv import CantidadesPV
from featurizers.cantidades_por_feature import CantidadesPorFeature
from featurizers.descripciones.descripciones import Descripciones
from featurizers.vistas_por_aviso import VistasPorAviso
from featurizers.avisos import Avisos

import pandas as pd
import numpy as np


import gc

FEATURIZERS = (
    InformacionBasica(),
    Avisos(),
    VistasPorAviso(),
    CantidadesPV(),
    CantidadesPorFeature(),
    Descripciones()
)

from historiador import log

def preprocesar_set(ruta_entrada, ruta_salida, cacho=100000):
    '''
    Preprocesa un set de entrenamiento/test/predicción en formato CSV.
    Se requiere que el mismo tenga una columna idaviso y una columna
    idpostulante. El resto de las columnas serán dejadas intactas en 
    el resultado.

    El procesamiento se realizará en partes de tamaño "cacho".
    '''

    log('Calculando cantidad de líneas...', end='', flush=True)
    cantidad_lineas = -1 # Eliminar header
    with open(ruta_entrada) as entrada:
        for _ in entrada:
            cantidad_lineas += 1
    log('OK', no_mostrar_hora=True)
    
    lineas_actual = 0

    while lineas_actual < cantidad_lineas:
        lineas_actual = procesar_fragmento(ruta_entrada, lineas_actual, cacho, cantidad_lineas, FEATURIZERS, ruta_salida)
        log('GC collected {} objects'.format(gc.collect()))
        
    log('Finalizado')

def procesar_fragmento(ruta_entrada, lineas_actual, cacho, cantidad_lineas, featurizers, ruta_salida):
    df = pd.read_csv(ruta_entrada, nrows=cacho, skiprows=range(1, lineas_actual+1))

    log('Procesando líneas {} - {} de {}'.format(lineas_actual, lineas_actual + cacho, cantidad_lineas))
    
    for i, featurizer in enumerate(FEATURIZERS):
        log('Ejecutando: ', featurizer.get_name(), '...', sep='', end='', flush=True)
        df_f = featurizer.featurize(df[['idaviso', 'idpostulante']].copy())
        df_f.to_csv(ruta_salida + '.{}.tmp'.format(i), index=False)
        log('OK', no_mostrar_hora=True)
        log('len(df_t) =', len(df_f))

    log('Guardando fragmento...', end='', flush=True)
    flush_featurizers(df, ruta_salida, lineas_actual, FEATURIZERS)
    log('OK', no_mostrar_hora=True)
    
    return lineas_actual + cacho

def flush_featurizers(df, ruta_salida, linea_actual, FEATURIZERS):
    df_d = df[['idaviso', 'idpostulante']]
    for i in range(len(FEATURIZERS)):
        df_d = pd.merge(\
            df_d, pd.read_csv(ruta_salida + '.{}.tmp'.format(i)),\
            on=['idaviso', 'idpostulante'], how='left')
    
    df = pd.merge(df_d, df, on=['idaviso', 'idpostulante'], how='left')

    log('flush_featurizers: len(df) =', len(df), no_mostrar_hora=True)

    if linea_actual == 0:
        df.to_csv(ruta_salida, index=False)
    else:
        df.to_csv(ruta_salida, index=False, mode='a', header=False)
    
    for i in range(len(FEATURIZERS)):
        os.remove(ruta_salida + '.{}.tmp'.format(i))


def main():
    '''
    Preprocesa un set de entrenamiento.

    Uso:

    ./preprocesar_set entrada.csv salida.csv [tamaño del cacho]

    El tamaño del cacho indica cuantas líneas se toman al mismo tiempo para
    procesar. Un tamaño más grande significa menos tiempo de procesamiento
    pero más consumo de memoria. Por defecto se usa tamaño = 100.000, que 
    funciona bien con 4GB de ram.
    '''
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print(main.__doc__, file=sys.stderr)
        return 1
    
    ruta_entrada = sys.argv[1]
    ruta_salida = sys.argv[2]
    cantidad_lineas = 100000
    if len(sys.argv) == 4:
        cantidad_lineas = int(sys.argv[3])
    
    print('Preprocesando...')
    preprocesar_set(ruta_entrada, ruta_salida, cantidad_lineas)
    print('OK')
    return 0


if __name__ == "__main__":
    sys.exit(main())


