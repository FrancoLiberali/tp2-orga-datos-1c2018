import pandas as pd
import numpy as np
from rutas import *
import csv

def generar_no_postulados():
    postulantes = pd.read_csv(RUTA_VECTOR_POSTULANTES)
    online = pd.read_csv(RUTA_AVISOS_ONLINE)
    with open(RUTA_SET_NO_POSTULADOS, 'w') as salida:
        wrt = csv.writer(salida)
        wrt.writerow(['idaviso', 'idpostulante', 'sepostulo'])
        postulantes = postulantes.sample(n=4000000, replace=True)['idpostulante'].values
        avisos = online.sample(n=4000000, replace=True)['idaviso'].values
        for i in range(0,4000000):
            if (i%100000 == 0):
                print(i)
            wrt.writerow([avisos[i], postulantes[i], '0'])
                
generar_no_postulados()

def ver_no_postulados_ya_estaban():
    no_postulados = pd.read_csv('../../tmp/set_no_postulados.csv')
    postulados = pd.read_csv('../../tmp/set_entrenamiento.csv')
    no_postulados = pd.merge(no_postulados,postulados, on=['idaviso', 'idpostulante'],how='left')
    no_postulados = no_postulados[(no_postulados['sepostulo_y'].isna())]
    no_postulados = no_postulados[['idaviso','idpostulante','sepostulo_x']]
    no_postulados = no_postulados.rename({'sepostulo_x':'sepostulo'},axis=1)
    no_postulados.to_csv('../../tmp/set_no_postulados.csv')
    
#ver_no_postulados_ya_estaban()
        