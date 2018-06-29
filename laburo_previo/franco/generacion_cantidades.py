# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np

def generar_cantidades(ruta, nombre):
    entrenamiento = pd.read_csv(ruta)
    
    vistas = pd.read_csv('../../datos_preprocesados/fiuba_3_vistas.csv')
    vistas = vistas[['idAviso','idpostulante']]
    
    cant_vistas = vistas.groupby(['idAviso', 'idpostulante']).size().reset_index(name='cant_vistas')
    entrenamiento = pd.merge(entrenamiento, cant_vistas, left_on=['idaviso','idpostulante'], right_on = ['idAviso', 'idpostulante'], how='left')
    entrenamiento = entrenamiento.drop(axis=1, labels=['idAviso'])
    entrenamiento = entrenamiento.fillna(0, axis=1)
    
    empresa_area = pd.read_csv('../../datos_preprocesados/fiuba_6_avisos_detalle.csv', usecols=['idaviso','denominacion_empresa','nombre_area'])
    vistas = pd.merge(vistas, empresa_area, left_on='idAviso', right_on='idaviso')
    vistas = vistas.drop(labels='idAviso', axis=1)
    
    cant_vistas_empresa = (vistas[['idpostulante', 'denominacion_empresa']]).groupby(['idpostulante', 'denominacion_empresa']).size().reset_index(name='cant_vistas_empresa')
    
    empresas = empresa_area[['idaviso','denominacion_empresa']]
    entrenamiento = pd.merge(entrenamiento,empresas, on='idaviso')
    entrenamiento = pd.merge(entrenamiento, cant_vistas_empresa, on=['idpostulante','denominacion_empresa'], how='left')
    entrenamiento = entrenamiento.fillna(0, axis=1)
    
    cant_vistas_area = (vistas[['idpostulante', 'nombre_area']]).groupby(['idpostulante', 'nombre_area']).size().reset_index(name='cant_vistas_area')
    
    areas = empresa_area[['idaviso','nombre_area']]
    entrenamiento = pd.merge(entrenamiento, areas, on='idaviso')
    
    entrenamiento = pd.merge(entrenamiento, cant_vistas_area, on=['idpostulante','nombre_area'], how='left')
    entrenamiento = entrenamiento.fillna(0, axis=1)
    
    postulaciones = pd.read_csv('../../tmp/set_entrenamiento.csv') # El set tiene filtrado que avisos se vieron y que avisos se postularon.
    postulaciones = postulaciones[postulaciones['sepostulo'] == 1]
    postulaciones = postulaciones.drop(labels='sepostulo', axis = 1)
    postulaciones = pd.merge(postulaciones, empresa_area, on='idaviso')
    
    cant_postulaciones_empresa = (postulaciones[['idpostulante', 'denominacion_empresa']]).groupby(['idpostulante', 'denominacion_empresa']).size().reset_index(name='cant_postulaciones_empresa')
    entrenamiento = pd.merge(entrenamiento, cant_postulaciones_empresa, on=['idpostulante','denominacion_empresa'], how='left')
    entrenamiento = entrenamiento.fillna(0, axis=1)
    entrenamiento = entrenamiento.drop(labels='denominacion_empresa',axis=1)
    
    cant_postulaciones_area = (postulaciones[['idpostulante', 'nombre_area']]).groupby(['idpostulante', 'nombre_area']).size().reset_index(name='cant_postulaciones_area')
    entrenamiento = pd.merge(entrenamiento, cant_postulaciones_area, on=['idpostulante','nombre_area'], how='left')
    entrenamiento = entrenamiento.fillna(0, axis=1)
    entrenamiento = entrenamiento.drop(labels='nombre_area',axis=1)
    
    entrenamiento['cant_vistas'] = entrenamiento['cant_vistas'].astype('int64')
    entrenamiento['cant_vistas_empresa'] = entrenamiento['cant_vistas_empresa'].astype('int64')
    entrenamiento['cant_vistas_area'] = entrenamiento['cant_vistas_area'].astype('int64')
    entrenamiento['cant_postulaciones_empresa'] = entrenamiento['cant_postulaciones_empresa'].astype('int64')
    entrenamiento['cant_postulaciones_area'] = entrenamiento['cant_postulaciones_area'].astype('int64')
    
    ruta_salida = '../../datos_procesados/' + nombre
    entrenamiento.to_csv(ruta_salida, index=False)
    
#generar_cantidades('../../test_final_100k.csv','to_kaggle.csv')
#generar_cantidades('../../tmp/set_entrenamiento.csv','entrenamiento.csv')
generar_cantidades('../../tmp/set_no_postulados.csv','no_postulados.csv')
