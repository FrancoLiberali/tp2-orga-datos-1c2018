#!/usr/bin/python3

print('Cargando datos...', end='')
import avisos
import postulantes
import vistas
import postulaciones
print('OK')


class Featurizer:
    '''
    Genera un feature a partir de una combinación aviso-postulante
    '''

    def featurize(self, id_aviso, id_postulante):
        '''
        Dado un aviso y un postulante, devuelve una lista con las características
        generadas.
        '''
        raise NotImplementedError
    
    def get_columns(self):
        '''
        Devuelve una lista con los nombres de las características generadas por
        este featurizer.
        '''
        raise NotImplementedError

class InformacionBasicaPostulante(Featurizer):
    '''
    Genera tres features que refieren a la información básica del postulante.
    - edad: Edad del postulante, por defecto: .EDAD_MEDIA
    - sexo: Sexo del postulante -1 si es mujer, 1 si es hombre, 0 por defecto.
    - educacion: Nivel educativo del postulante, de 0 a 10 basado en 
        ESCALA_EDUCATIVA, por defecto .NIVEL_EDUCATIVO_MEDIO
    Si no se tiene la edad del postulante, devuelve EdadPostulante.EDAD_MEDIA.
    '''

    # Se considera Abandonado y En curso como "incompleto"; Graduado como "completo".
    # La métrica induce una distancia. Terciario tiene menos influencia que el resto
    # debido a que es muy similar a secundario.
    ESCALA_EDUCATIVA = {
        ('Otro', 'Abandonado'): 0, # Jardin de infantes
        ('Otro', 'En Curso'): 0, #
        ('Otro', 'Graduado'): 0, #
        ('Secundario', 'Abandonado'): 1, # Sec incompleto
        ('Secundario', 'En Curso'): 1, # Sec incompleto
        ('Secundario', 'Graduado'): 2, # Sec completo
        ('Terciario/Técnico', 'Abandonado'): 2,
        ('Terciario/Técnico', 'En Curso'): 2,
        ('Terciario/Técnico', 'Graduado'): 2.5,
        ('Universitario', 'Abandonado'): 3,
        ('Universitario', 'En Curso'): 3,
        ('Universitario', 'Graduado'): 4,
        ('Posgrado', 'Abandonado'): 5,
        ('Posgrado', 'En Curso'): 5,
        ('Posgrado', 'Graduado'): 6,
        ('Master', 'Abandonado'): 7,
        ('Master', 'En Curso'): 7,
        ('Master', 'Graduado'): 8,
        ('Doctorado', 'Abandonado'): 9,
        ('Doctorado', 'En Curso'): 9,
        ('Doctorado', 'Graduado'): 10
    }

    TITULOS = ['Otro', 'Secundario', 'Terciario/Técnico', 'Universitario', 'Posgrado',
        'Master', 'Doctorado']

    EDAD_MEDIA = 30
    EDAD_MIN = 14
    EDAD_MAX = 90

    def get_nivel_educativo(self, postulante):
        '''
        Devuelve el nivel educativo del postulante según la escala
        educativa.
        '''

        titulos = [0]

        for titulo in self.TITULOS:
            titulos.append(self.ESCALA_EDUCATIVA.get((titulo, postulante[titulo]), 0))
        
        return max(titulos)

    def get_edad(self, postulante):
        '''
        Devuelve la edad del postulante.
        '''
        fecha_splitted = postulante['fechanacimiento'].split('-')
        if len(fecha_splitted) != 3:
            return self.EDAD_MEDIA
        
        anio, _, _ = fecha_splitted

        try:
            edad = 2018 - int(anio)
        except ValueError:
            return self.EDAD_MEDIA
        
        if self.EDAD_MIN < edad < self.EDAD_MAX:
            return edad
        
        return self.EDAD_MEDIA

    
    def get_sexo(self, postulante):
        '''
        Devuelve el sexo del postulante.
        '''
        if postulante['sexo'] == 'MASC':
            return 1
        
        if postulante['sexo'] == 'FEM':
            return -1
        
        return 0

    def featurize(self, id_aviso, id_postulante):
        postulante = postulantes.get(id_postulante)

        return [ self.get_edad(postulante), self.get_sexo(postulante), 
            self.get_nivel_educativo(postulante) ]

    def get_columns(self):
        return [ 'edad_postulante', 'sexo_postulante', 'eduacion_postulante' ]

class CantidadVistasPostulacionesPostulante(Featurizer):
    '''
    Genera dos features que refieren a la cantidad de vistas y postulaciones del
    postulante.
    - cantidad_vistas: Cuantos anuncios vio el postulante.
    - cantidad_postulaciones: A cuantos anuncios se postuló el postulante.
    '''
    
    def featurize(self, id_aviso, id_postulante):
        cantidad_vistas = len(vistas.get(id_postulante))
        cantidad_postus = len(postulaciones.get(id_postulante))

        return [cantidad_vistas, cantidad_postus]
    
    def get_columns(self):
        return [ 'cantidad_vistas', 'cantidad_postulaciones' ]

class CantidadPVEnFeaturesDelAnuncio(Featurizer):
    '''
    Genera features que refieren a la cantidad de vistas y postulaciones en el 
    área, zona y tipo de trabajo del anuncio.
    - cant_vistas_{feature}: Cantidad de vistas en las que coincide con {feature} del anuncio
    - cant_postulaciones_{feature}: Cantidad de postulaciones en las que coincide con {feature} del anuncio
    '''

    PREFIJO_VISTAS = 'cant_vistas_'
    PREFIJO_POSTULACIONES = 'cant_postulaciones_'
    FEATURES = ('nombre_area', 'nombre_zona', 'tipo_de_trabajo', 'denominacion_empresa')

    def calcular_cantidades(self, aviso_actual, otros_avisos):
        '''
        Calcula la cantidad de postulaciones en avisos que coincidan en
        los features indicados por la constante .FEATURES
        Devuelve un diccionario {feature: cantidad}
        '''
        cantidades = {}
        for id_aviso in otros_avisos:
            if id_aviso == aviso_actual['idaviso']:
                continue
            for feature in self.FEATURES:
                if avisos.get(id_aviso)[feature] == aviso_actual[feature]:
                    cantidades[feature] = cantidades.get(feature, 0) + 1
        return cantidades
    
    def featurize(self, id_aviso, id_postulante):
        aviso = avisos.get(id_aviso)
        cantidades_vistas = self.calcular_cantidades(aviso, vistas.get(id_postulante))
        cantidades_postus = self.calcular_cantidades(aviso, postulaciones.get(id_postulante))

        features = []

        for feature in self.FEATURES:
            features.append(cantidades_postus[feature])
            features.append(cantidades_vistas[feature])

        return features

    def get_columns(self):
        columnas = []
        for feature in self.FEATURES:
            for prefijo in (self.PREFIJO_POSTULACIONES, self.PREFIJO_VISTAS):
                columnas.append(prefijo + feature)
        return columnas