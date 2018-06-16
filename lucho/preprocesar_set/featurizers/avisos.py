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

    
FEATURES = ('edad', 'sexo', 'nivel_educativo')

class Avisos:

    def get_name(self):
        return 'Edad, sexo y educación promedio de los avisos'

    def featurize(self, df):
        df_avisos = pd.merge(df[['idaviso']].drop_duplicates(), postulaciones.df, on='idaviso', how='left')
        
