#!/usr/bin/python3

'''
Genera features para el aviso según quienes vieron el mismo.
- edad_prom = Promedio de edad de los postulantes que vieron el anuncio
- sexo_prom = Promedio de sexo 
- nivel_educativo_prom = Promedio de nivel educativo
'''

import datasets.avisos as avisos
import datasets.vistas as vistas
import datasets.postulaciones as postulaciones

    
FEATURES = ('edad', 'sexo', 'nivel_educativo')

class Avisos:
    def inicializar(self):
        '''
        Precalcula el promedio de edad, sexo y nivel_educativo para cada
        aviso.
        '''
        pass

    def get_promedio_feature(self, feature):
        '''
        Calcula el promedio de un determinado feature.
        '''

    def featurize(self, id_aviso, id_postulante):
        aviso = avisos.get(id_aviso)
        return []

    def get_columns(self):
        return []