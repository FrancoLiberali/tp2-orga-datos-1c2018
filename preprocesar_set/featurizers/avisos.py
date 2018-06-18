#!/usr/bin/python3

'''
Genera features para el aviso según quienes vieron el mismo.
- edad_prom = Promedio de edad de los postulantes que vieron el anuncio
- sexo_prom = Promedio de sexo 
- nivel_educativo_prom = Promedio de nivel educativo
'''

import datasets.avisos as avisos
import datasets.postulantes as postulantes
import datasets.vistas as vistas
import datasets.postulaciones as postulaciones

import pandas as pd
import numpy as np
    
NIVEL_EDUC_MEDIO = 2
SEXO_MEDIO = 0
EDAD_MEDIA = 30

class Avisos:

    def get_name(self):
        return 'Edad, sexo y educación promedio de los avisos'

    def featurize(self, df):
        df_data = pd.merge(df[['idaviso']].drop_duplicates(), postulaciones.df, on='idaviso', how='inner').drop_duplicates()
        df_data = pd.merge(df_data, postulantes.df_genero_edad, on='idpostulante', how='inner')
        df_data = pd.merge(df_data, postulantes.df_educacion, on='idpostulante', how='inner')
        df_data = df_data.drop(axis=1, labels=['idpostulante'])
        
        def promedio_pesado(reg):
            FACTOR = 5
            total = len(reg) + FACTOR
            nivel_educ = (np.sum(reg['nivel_educativo']) + FACTOR * NIVEL_EDUC_MEDIO) / total
            edad = (np.sum(reg['edad']) + FACTOR * EDAD_MEDIA) / total
            sexo = (np.sum(reg['sexo']) + FACTOR * SEXO_MEDIO) / total
            return {'nivel_educativo': nivel_educ, 'edad': edad, 'sexo': sexo}

        df_data = df_data.groupby('idaviso').aggregate(promedio_pesado)\
                         .reset_index()\
                         .rename(columns={'edad': 'edad_media', 'sexo':'sexo_medio', 
                            'nivel_educativo': 'nivel_educativo_medio'})
        df_data = pd.merge(df, df_data, on='idaviso', how='left')
        df_data['hay_informacion_media_aviso'] = 1
        no_tienen_informacion_media = (df_data['edad_media'].isna()) | (df_data['sexo_medio'].isna()) | (df_data['nivel_educativo_medio'].isna())
        features_a_cero = ('edad_media', 'sexo_medio', 'nivel_educativo_medio', 'hay_informacion_media_aviso')
        df_data.loc[no_tienen_informacion_media, features_a_cero] = 0
        
        return df_data
        
