#!/usr/bin/python3

'''
[Jowi]
Genera features indicando si el usuario vio/se postulo al aviso o no y cuantas veces lo vio.
- num_postulaciones = Cantidad de veces que el usuario se postuló al aviso (debería ser booleano?)
- num_vistas = Cantidad de veces que el usuario vio el aviso
'''

import datasets.vistas as vistas
import datasets.postulaciones as postulaciones

import pandas as pd
import numpy as np
    

class VistasPorAviso:

    def get_name(self):
        return 'Vistas por aviso'

    def featurize(self, df):
        test1 = pd.merge(df[['idaviso', 'idpostulante']], vistas.df, on=['idaviso', 'idpostulante'], how='inner')
        test1['num_vistas'] = 1
        test1 = test1.groupby(['idaviso', 'idpostulante']).agg('count').reset_index()
        test1 = pd.merge(df[['idaviso', 'idpostulante']], test1, on=['idaviso', 'idpostulante'], how='left')
        test1['num_vistas'] = test1['num_vistas'].fillna(0).astype('int')

        test2 = pd.merge(df[['idaviso', 'idpostulante']], postulaciones.df, on=['idaviso', 'idpostulante'], how='inner')
        test2['num_postulaciones'] = 1
        test2 = test2.groupby(['idaviso', 'idpostulante']).agg('count').reset_index()
        test2 = pd.merge(df[['idaviso', 'idpostulante']], test2, on=['idaviso', 'idpostulante'], how='left')
        test2['num_postulaciones'] = test2['num_postulaciones'].fillna(0).astype('int')

        return pd.merge(test1, test2, on=['idaviso', 'idpostulante'], how='inner')

        
