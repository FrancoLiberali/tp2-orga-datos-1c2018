#!/usr/bin/python3

'''
Genera features que refieren a la cantidad de vistas y postulaciones en el 
área, zona y tipo de trabajo del anuncio.
- cant_vistas_{feature}: Cantidad de vistas en las que coincide con {feature} del anuncio
- cant_postulaciones_{feature}: Cantidad de postulaciones en las que coincide con {feature} del anuncio
'''


import datasets.avisos as avisos
import datasets.postulantes as postulantes
import datasets.vistas as vistas
import datasets.postulaciones as postulaciones
import pandas as pd
import numpy as np


PREFIJO_VISTAS = 'cant_vistas_'
PREFIJO_POSTULACIONES = 'cant_postulaciones_'
FEATURES = ('nombre_area', 'nombre_zona', 'tipo_de_trabajo', 'denominacion_empresa')

class CantidadesPorFeature:

    def get_name(self):
        return 'Cantidades de postulaciones y vistas por coincidencia de features'

    def featurize(self, df):
        df_tmp = pd.merge(df, avisos.df[list(FEATURES)], left_on='idaviso', right_index=True, how='left')
        df_tmp = self.contar_interacciones(df_tmp, vistas, PREFIJO_VISTAS)
        df_tmp = self.contar_interacciones(df_tmp, postulaciones, PREFIJO_POSTULACIONES)
        return df_tmp.drop(axis=1, labels=list(FEATURES))

    def contar_interacciones(self, df_tmp, interacciones, prefijo):
        i_data = pd.merge(interacciones.df, df_tmp[['idpostulante']], on='idpostulante', how='inner')
        i_data = pd.merge(i_data, avisos.df[list(FEATURES)], left_on='idaviso', right_index=True, how='inner')
        
        for feature in FEATURES:
            gb = i_data.groupby('idpostulante')[feature].value_counts()
            df_tmp[prefijo + feature] = df_tmp['idpostulante'] + '-' + df_tmp[feature]

            def get_cant(x):
                if not isinstance(x, str):
                    return 0
                postu, *area = x.split('-')
                clave = (postu, '-'.join(area))
                if clave in gb.index:
                    return gb[clave]
                return 0
            df_tmp[prefijo + feature] = df_tmp[prefijo + feature].map(get_cant)
        
        return df_tmp
