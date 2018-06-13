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
from multiprocessing import Pool as ThreadPool, cpu_count, Lock

import featurizers.descripciones.descripciones_helper as desc_helper

import time

class Descripciones:

    def __init__(self, porcentaje = 0.01):
        print('Inicializando Descripciones...')
        self.factor = len(avisos.df) * float(porcentaje)
        lexico = {}

        print(' - Preprocesando descripciones...', end='', flush=True)
        df = pd.DataFrame(paralelizar_procesar_descripciones(avisos.df['descripcion'], lexico))
        print('OK')

        print(' - Recalculando lexico...', end='', flush=True)
        lexico = {}
        def calcular_frecuencia_lexico(desc):
            for palabra in desc.split():
                lexico[palabra] = lexico.get(palabra, 0) + 1
            return desc
        df['descripcion'] = df['descripcion'].map(calcular_frecuencia_lexico)
        print('OK')

        print(' - Eliminando palabras menos frecuentes...', end='', flush=True)
        df = paralelizar_remover_menos_frecuentes(df['descripcion'], lexico, self.factor)
        print('OK')

        
        self.df_descripciones = {id_aviso: set(desc.split()) for id_aviso, desc in df.to_dict().items()}
        self.vistas_gb = vistas.df.groupby('idpostulante')
        self.postulaciones_gb = postulaciones.df.groupby('idpostulante')
        print('OK')
        
    def generar_data_postulante(self, id_postulante):
        '''
        Devuelve un diccionario con las palabras que más vio el usuario
        y sus frecuencias.
        '''
        data_postulante = {}

        
        def obtener_palabras(id_aviso):
            if id_aviso not in self.df_descripciones:
                return id_aviso
            
            for palabra in self.df_descripciones[id_aviso]:
                data_postulante[palabra] = data_postulante.get(palabra, 0) + 1
            
            return id_aviso

        if id_postulante in self.vistas_gb.groups:
            self.vistas_gb.get_group(id_postulante)['idaviso'].map(obtener_palabras)
        if id_postulante in self.postulaciones_gb.groups:
            self.postulaciones_gb.get_group(id_postulante)['idaviso'].map(obtener_palabras)
        
        return data_postulante


    def featurize(self, df):
        print('Featurizing descripciones...')
        print(' - Etapa 1/2: str-concat...', end='', flush=True)
        df['desc_score'] = df['idpostulante'] + '-' + df['idaviso'].astype('str')
        print('OK')
        print(' - Etapa 2/2: featurize...', end='', flush=True)
        #df = paralelizar_featurize(df, self)
        # Desactivar MT llamando a la función parallel_featurize (que es la que ejecuta cada thread)
        # en el thread principal
        df = parallel_featurize((df, self))
        print('OK')
        return df
        


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

def parallel_featurize(data):
    df, self = data
    def calcular_score(data):
        if not isinstance(data, str):
            return 0
        id_postulante, id_aviso = data.split('-')
        id_aviso = int(id_aviso)

        if id_aviso not in self.df_descripciones:
            return 0
        
        descripcion_aviso = self.df_descripciones[id_aviso]
        score_descripcion = [0]
        
        def sumar_scores(id_aviso):
            if id_aviso not in self.df_descripciones:
                return
            
            for palabra in self.df_descripciones[id_aviso]:
                if palabra in descripcion_aviso:
                    score_descripcion[0] += 1
            

        if id_postulante in self.vistas_gb.groups:
            self.vistas_gb.get_group(id_postulante)['idaviso'].map(sumar_scores)
        #if id_postulante in self.postulaciones_gb.groups:
        #    self.postulaciones_gb.get_group(id_postulante)['idaviso'].map(sumar_scores)
        
        return score_descripcion[0]
    
    df['desc_score'] = df['desc_score'].map(calcular_score)

    return df

def init_pool_featurize(l):
    global pp_lock
    pp_lock = l

def paralelizar_featurize(df, self):
    lock = Lock()
    df_split = [(df, self) for df in np.array_split(df, cpu_count())]
    with ThreadPool(cpu_count(), initializer=init_pool_featurize, initargs=(lock,)) as pool:
        data = pd.concat(pool.map(parallel_featurize, df_split))
    
    return data