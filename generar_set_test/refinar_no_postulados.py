#!/usr/bin/python3

'''
Intenta buscar pares idaviso,idpostulante cuya probabilidad de ser postulados sea muy baja.

La idea general es hacer algo del estilo aprendizaje semi-supervisado. Partimos de un set de entrenamiento
basado en postulaciones y vistas no postuladas y predecimos algunas postulaciones al azar mediante un random forest.
Rearmamos el set con los mismos datos más algunos cuya prediccion fue "no se postula", se reentrena y repite.
Se detiene después de una determinada cantidad de iteraciones.
'''

import math

import pandas as pd
import numpy as np

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import roc_auc_score

DATASET_SAMPLE_SIZE = 500000

# Porcentaje del set de entrenamiento que se usa para validar
TEST_SIZE_PERCENT = 0.2

# Semilla aleatoria fija para mantener la ejecución determinista.
RANDOM_SEED = 12

# Mínima cantidad de no postulados para agregar en una iteración
MIN_SAMPLES_NO_POSTULADOS = 10

entrenamiento = pd.read_csv('/home/luciano/orga-datos/training-set-no-random-preprocesado.csv')
no_postulados = pd.read_csv('/home/luciano/orga-datos/training-set-no-postulados-random-preprocesado.csv')

X = entrenamiento.drop(axis=1, labels=['idaviso', 'idpostulante', 'sepostulo'])
y = entrenamiento['sepostulo']

no_postulados_set = no_postulados.drop(axis=1, labels=['idaviso', 'idpostulante'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE_PERCENT, random_state=RANDOM_SEED)

clasificador = RandomForestClassifier(
        n_estimators=10, 
        criterion='entropy', 
        max_features='sqrt', 
        min_samples_split=20, 
        n_jobs=-1, 
        random_state=RANDOM_SEED, 
        verbose=10
    )

clasificador.fit(X_train, y_train)

print('Score contra el set de entrenamiento original')
print('Score vs set train:', clasificador.score(X_train, y_train))
print('Score vs set test:', clasificador.score(X_test, y_test))

iteracion = 0
MAX_ITERACIONES = 10
no_postulados['sepostulo'] = 0
no_postulados['sepostulo_acum'] = 0

# En cada iteración la probabilidad de aceptar un no-postulado es menor, con base en 0.5 y asintótica en 0.1
BASE = 0.5
prob = lambda x: math.e ** -( ((1.5 * x)/MAX_ITERACIONES) - math.log(BASE) ) 

for iteracion in range(MAX_ITERACIONES + 1):
    print('Iteracion actual:', iteracion, 'de', MAX_ITERACIONES)
    np_sepostulo = pd.DataFrame(clasificador.predict_proba(no_postulados_set)[:, 1], columns=['sepostulo'])
    no_postulados['sepostulo_acum'] += np_sepostulo['sepostulo']
    no_postulados['sepostulo'] = no_postulados['sepostulo_acum'] / (iteracion + 1)
    
    prob_no_postulado = prob(iteracion)
    print('Probabilidad de ser 0 para agarrar un no-postulado:', prob_no_postulado)
    print(len(no_postulados[no_postulados['sepostulo'] < prob_no_postulado]))
    # Prevenir que el umbral elimine todos los resultados
    assert len(no_postulados[no_postulados['sepostulo'] < prob_no_postulado]) > MIN_SAMPLES_NO_POSTULADOS
    # Si este assert falla: Verificar UMBRAL_PROB_NO_POSTULADO, MIN_SAMPLES_NO_POSTULADOS, total_iteraciones
    
    no_post_to_concat = no_postulados[no_postulados['sepostulo'] < prob_no_postulado]

    if len(no_post_to_concat) > DATASET_SAMPLE_SIZE:
        no_post_to_concat = no_post_to_concat.sample(n=DATASET_SAMPLE_SIZE)

    nuevo_entrenamiento = pd.concat([entrenamiento, no_post_to_concat.drop(axis=1, labels=['sepostulo_acum'])])
    
    nuevo_entrenamiento.loc[nuevo_entrenamiento['sepostulo'] < prob_no_postulado, 'sepostulo'] = 0
    
    nuevo_entrenamiento['sepostulo'] = nuevo_entrenamiento['sepostulo'].astype('int')
    
    X = nuevo_entrenamiento.drop(axis=1, labels=['idaviso', 'idpostulante', 'sepostulo'])
    y = nuevo_entrenamiento['sepostulo']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE_PERCENT, random_state=RANDOM_SEED)
    
    clasificador.fit(X_train, y_train)
    
    print('Score vs set train:', clasificador.score(X_train, y_train))
    print('Score vs set test:', clasificador.score(X_test, y_test))

np_sepostulo = pd.DataFrame(clasificador.predict_proba(no_postulados_set)[:, 1], columns=['sepostulo'])

no_postulados['sepostulo_acum'] += np_sepostulo['sepostulo']
no_postulados['sepostulo'] = no_postulados['sepostulo_acum'] / (MAX_ITERACIONES + 2)
no_postulados_al_set = no_postulados[no_postulados['sepostulo'] < 0.1].sample(n=DATASET_SAMPLE_SIZE)
no_postulados_al_set['sepostulo'] = 0
no_postulados_al_set.to_csv('/home/luciano/orga-datos/no-postulados-random-confirmados.csv', index=False)
set_test_completo = pd.concat([entrenamiento, no_postulados_al_set.drop(axis=1, labels=['sepostulo_acum'])])
set_test_completo = set_test_completo.sample(frac=1)
set_test_completo.to_csv('/home/luciano/orga-datos/training-set-final.csv', index=False)