#!/usr/bin/python3
'''
Genera dos features que refieren a la cantidad de vistas y postulaciones del
postulante.
- cantidad_vistas: Cuantos anuncios vio el postulante.
- cantidad_postulaciones: A cuantos anuncios se postuló el postulante.
'''

import datasets.vistas as vistas
import datasets.postulaciones as postulaciones
import pandas as pd

class CantidadesPV:
    def get_name(self):
        return 'Cantidades de vistas y postulaciones totales'
    
    def featurize(self, df):
        df = pd.merge(df, \
            vistas.df.groupby('idpostulante').agg('count').rename(columns={'idaviso': 'cantidad_vistas'}), \
            on='idpostulante', how='left')
        
        df['cantidad_vistas'] = df['cantidad_vistas'].fillna(0).astype('int')
        
        df = pd.merge(df, \
            postulaciones.df.groupby('idpostulante').agg('count')\
            .rename(columns={'idaviso': 'cantidad_postulaciones'}), \
            on='idpostulante', how='left')
        
        df['cantidad_postulaciones'] = df['cantidad_postulaciones'].fillna(0).astype('int')

        return df
