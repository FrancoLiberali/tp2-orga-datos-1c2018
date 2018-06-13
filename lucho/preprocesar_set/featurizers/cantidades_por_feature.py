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


PREFIJO_VISTAS = 'cant_vistas_'
PREFIJO_POSTULACIONES = 'cant_postulaciones_'
FEATURES = ('nombre_area', 'nombre_zona', 'tipo_de_trabajo', 'denominacion_empresa')

class CantidadesPorFeature:
    def featurize(self, df):
        data_postulantes = {}
        df_postulantes = df[['idpostulante']].drop_duplicates()
        
        def determinar_vistas(id_postulante):
            vistas_postulante = vistas.df[vistas.df['idpostulante'] == id_postulante]
            vistas_postulante

        df_postulantes['idpostulante'].map(determinar_vistas)
        
        
        def contar_cantidades(registro):
            for feature in FEATURES:
                registro[PREFIJO_VISTAS + feature] = \
                    vistas.df[vistas.df['idpostulante'] == registro['idpostulante']].groupby('')

        df_avisos.apply(contar_cantidades)
        
        return df