#!/usr/bin/python3

'''
Genera features a partir de descripciones.
'''

import Stemmer

import featurizer
import avisos
import vistas
import postulaciones

from descripciones import procesar_descripcion

class FeaturesDescripciones(featurizer.Featurizer):
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

    NOTA: Este módulo puede tomar un tiempo en inicializarse ya que debe determinar las 500
    palabras más importantes.
    '''

    def __init__(self, cantidad_palabras_importantes = 500, porcentaje = 0.01):
        '''
        '''
        self.palabras_importantes = set()
        self.lexico = {} # Palabra: frecuencia
        self.descripciones_procesadas = {} # aviso: descripcion
        self.postulantes_procesados = {} # postulante: {palabra, cantidad_veces}
        self.factor = len(avisos.avisos) * float(porcentaje)

        stemmer = Stemmer.Stemmer('spanish')

        for aviso in avisos.avisos:
            descripcion = procesar_descripcion(aviso['descripcion'], stemmer)
            
            for palabra in descripcion:
                self.lexico[palabra] = self.lexico.get(palabra, 0) + 1
            
            self.descripciones_procesadas[aviso['idaviso']] = descripcion
        
        for id_aviso, descripcion in self.descripciones_procesadas.items():
            self.descripciones_procesadas[id_aviso] = \
                [ w for w in descripcion if self.lexico[w] >= self.factor ]
        
        self.lexico = {}
        for id_aviso, descripcion in self.descripciones_procesadas.items():
            for palabra in descripcion:
                self.lexico[palabra] = self.lexico.get(palabra, 0)
            
            self.descripciones_procesadas[id_aviso] = ' '.join(descripcion)
            
        
    

    


