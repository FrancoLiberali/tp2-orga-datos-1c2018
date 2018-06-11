#!/usr/bin/python3

'''
Realiza la conversión del set id, idaviso, idpostulante en vectores
para poder predecir mediante algoritmos de machine learning.
'''

import csv
import sys

import featurizer

FEATURIZERS = (
    featurizer.InformacionBasicaPostulante(),
    featurizer.CantidadVistasPostulacionesPostulante(),
)

COLUMNAS_CARACTERISTICAS = sum([f.get_columns() for f in FEATURIZERS], [])

def preprocesar_set(ruta_entrada, ruta_salida, cantidad_lineas = 0):
    '''
    Preprocesa un set de entrenamiento/test/predicción en formato CSV.
    Se requiere que el mismo tenga una columna idaviso y una columna
    idpostulante. El resto de las columnas serán dejadas intactas en 
    el resultado.

    Si se indica un valor distinto de cero para cantidad_lineas, se
    indicará el progreso del preprocesamiento.
    '''

    linea_actual = 0
    porcentaje_anterior = 0

    with open(ruta_entrada) as entrada, open(ruta_salida, 'w') as salida:
        lector = csv.reader(entrada)
        escritor = csv.writer(salida)
        
        encabezado = next(lector)
        
        ID_POSTULANTE = encabezado.index('idpostulante')
        ID_AVISO      = encabezado.index('idaviso')

        escritor.write(encabezado + COLUMNAS_CARACTERISTICAS)

        for fila in lector:
            id_aviso, id_postulante = fila[ID_AVISO], fila[ID_POSTULANTE]
            caracteristicas = convertir_par_a_caracteristicas(id_aviso, id_postulante, FEATURIZERS)

            escritor.writerow(fila + caracteristicas)
            linea_actual += 1
            if cantidad_lineas != 0:
                porcentaje = linea_actual * 10000 // cantidad_lineas
                if porcentaje != porcentaje_anterior:
                    print('%.2f' % porcentaje / 100)
                    porcentaje_anterior = porcentaje

def convertir_par_a_caracteristicas(id_aviso, id_postulante, featurizers):
    '''
    Realiza la conversión de un par aviso-postulante a un vector de 
    características. Cada característica está generada por un featurizer.
    Un featurizer es una objeto de la clase Featurizer que implementa el método
    featurize [ver featurize.py].

    Esta función devuelve una lista con todas las características numéricas
    generadas por los featurizers.
    '''
    caracteristicas = []

    for f in featurizers:
        caracteristicas += f.featurize(id_aviso, id_postulante)

    return caracteristicas
            

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


