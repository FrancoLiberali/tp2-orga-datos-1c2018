#!/usr/bin/python3

'''
Genera los features score_descripcion y distancia_descripciones.
score_descripcion se define de la siguiente forma:
- De las descripciones de los anuncios se obtienen las 500 palabras más importantes.
- Se calcula el peso de cada palabra en el anuncio via TF-IDF.
- Se suma el TF-IDF de cada palabra que el usuario vio (revisando
    en los anuncios que vio/se postuló anteriormente).
- El score_descripcion se calcula como la suma del producto del TF-IDF de cada palabra
    del anuncio por el resultado de cada palabra para el usuario.
    score_descripcion = sum ( tfidf(Pi) * sum(tfidf(Pjk))), donde Pi = palabra i del anuncio,
    Pjk = Palabra j del anuncio k visto por el postulante.

distancia_descripciones se define de la siguiente forma:
- Distancia de jaccard entre las descripciones, reducido en palabras.

NOTA: Este módulo puede tomar un tiempo en inicializarse ya que debe preprocesar las descripciones
'''

import Stemmer

import datasets.avisos as avisos
import datasets.postulantes as postulantes
import datasets.vistas as vistas
import datasets.postulaciones as postulaciones
import pandas as pd
import numpy as np
from multiprocessing import Pool as ThreadPool, cpu_count
import featurizers.descripciones.descripciones_helper as desc_helper

class Descripciones:

    def __init__(self, porcentaje = 0.01):
        print('Inicializando Descripciones...')
        self.factor = len(avisos.df) * float(porcentaje)
        self.lexico = {}

        print(' - Preprocesando descripciones...', end='', flush=True)
        df = pd.DataFrame(paralelizar_procesar_descripciones(avisos.df['descripcion'], self.lexico))
        print('OK')

        print(' - Eliminando palabras menos frecuentes...', end='', flush=True)
        df = paralelizar_remover_menos_frecuentes(df['descripcion'], self.lexico, self.factor)
        print('OK')

        print('OK')
        self.df_descripciones = df
        self.postulantes_procesados = {}
        
    def generar_data_postulante(self, id_postulante):
        '''
        Devuelve un diccionario con las palabras que más vio el usuario
        y sus frecuencias.
        '''
        df = pd.merge(self.df_descripciones, \
            vistas.df.loc[vistas.df['idpostulante'] == id_postulante], on='idaviso', how='inner')
        
        data_postulante = {}
        
        def obtener_palabras(desc):
            for palabra in desc.split():
                data_postulante[palabra] = data_postulante.get(palabra, 0) + 1
            
            return desc

        df['descripcion'].map(obtener_palabras)

        return data_postulante


    def featurize(self, id_aviso, id_postulante):
        if not id_postulante in self.postulantes_procesados:
            self.postulantes_procesados[id_postulante] = self.generar_data_postulante(id_postulante)

        if id_aviso not in self.df_descripciones.index:
            return [ 0 ]
        
        descripcion = set(self.df_descripciones.loc[id_aviso]['descripcion'].split())

        descripcion_postulante = self.postulantes_procesados[id_postulante]
        score_descripcion = 0
        
        for palabra in descripcion_postulante:
            if palabra in descripcion:
                score_descripcion += descripcion_postulante[palabra]
        
        return [ score_descripcion ]


    def get_columns(self):
        return [ 'score_descripcion' ]


def parallel_map_procesar(data):
    serie, lexico = data
    return serie.map(lambda x: procesar_descripcion(x, Stemmer.Stemmer('spanish'), lexico))

def procesar_descripcion(desc, stemmer, lexico):
    res = desc_helper.procesar_descripcion(desc, stemmer)
    for palabra in res:
        lexico[palabra] = lexico.get(palabra, 0) + 1
    return ' '.join(res)

def paralelizar_procesar_descripciones(series, lexico):
    lexicos = [{} for _ in range(cpu_count())]

    # Un Stemmer por hilo y un diccionario léxico por hilo para prevenir race conditions
    series_split = [(serie, lexicos[i]) for i, serie in enumerate(np.array_split(series, cpu_count()))]
    with ThreadPool(cpu_count()) as pool:
        data = pd.concat(pool.map(parallel_map_procesar, series_split))
    
    # Acá se reunen los diccionarios léxicos en uno
    for d in lexicos:
        for k, v in d.items():
            lexico[k] = lexico(k, 0) + v

    return data

def parallel_map_remover(data):
    serie, lexico, factor = data
    return serie.map(lambda x: remover_palabras_menos_frecuentes(x, lexico, factor))

def remover_palabras_menos_frecuentes(desc, lexico, factor):
    res = desc.split()
    res = [ palabra for palabra in res if lexico[palabra] >= factor ]
    return ' '.join(res)

def paralelizar_remover_menos_frecuentes(series, lexico, factor):
    series_split = [(serie, lexico, factor) for i, serie in enumerate(np.array_split(series, cpu_count()))]
    with ThreadPool(cpu_count()) as pool:
        data = pd.concat(pool.map(parallel_map_remover, series_split))
    
    return data