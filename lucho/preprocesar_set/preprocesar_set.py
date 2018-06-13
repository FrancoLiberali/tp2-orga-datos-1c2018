#!/usr/bin/python3

'''
Realiza la conversión del set id, idaviso, idpostulante en vectores
para poder predecir mediante algoritmos de machine learning.
'''

import csv
import sys

from featurizers.informacion_basica import InformacionBasica
from featurizers.cantidad_pv import CantidadesPV
from featurizers.cantidades_por_feature import CantidadesPorFeature
from featurizers.descripciones.descripciones import Descripciones

import pandas as pd
import numpy as np

FEATURIZERS = (
    InformacionBasica(),
    CantidadesPV(),
    CantidadesPorFeature(),
    Descripciones()
)

def preprocesar_set(ruta_entrada, ruta_salida, cantidad_lineas = 0, cacho=10000):
    '''
    Preprocesa un set de entrenamiento/test/predicción en formato CSV.
    Se requiere que el mismo tenga una columna idaviso y una columna
    idpostulante. El resto de las columnas serán dejadas intactas en 
    el resultado.

    Si se indica un valor distinto de cero para cantidad_lineas, se
    indicará el progreso del preprocesamiento.
    '''

    
    df = pd.read_csv(ruta_entrada)

    for i, featurizer in enumerate(FEATURIZERS):
        print('Featurizer', i)
        df = featurizer.featurize(df)
    
    df.to_csv(ruta_salida, index=False)


def main():
    '''
    Preprocesa un set de entrenamiento.

    Uso:

    ./preprocesar_set entrada.csv salida.csv [cantidad lineas entrada]

    Si se especifica la cantidad de líneas en el archivo de entrada
    mostrará el progreso del procesamiento.
    '''
    if len(sys.argv) < 3 or len(sys.argv) > 4:
        print(main.__doc__, file=sys.stderr)
        return 1
    
    ruta_entrada = sys.argv[1]
    ruta_salida = sys.argv[2]
    cantidad_lineas = 0
    if len(sys.argv) == 4:
        cantidad_lineas = int(sys.argv[3])
    
    print('Preprocesando...')
    preprocesar_set(ruta_entrada, ruta_salida, cantidad_lineas)
    print('OK')
    return 0


if __name__ == "__main__":
    sys.exit(main())


