#!/usr/bin/python3

from stop_words import STOP_WORDS
from html.parser import HTMLParser

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed =[]
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ' '.join(self.fed)

def strip_html_tags(cadena):
    '''
    Elimina los tags HTML de una cadena.
    '''
    s = MLStripper()
    s.feed(cadena)
    return s.get_data()

def foldear_tildes(cadena):
    ''' 
    Elimina las tildes de una cadena en minúsculas. 
    Ej: descripción -> descripcion
    '''
    
    acentos = {'á':'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u', 'ü':'u'}
    return ''.join([ acentos.get(c, c) for c in cadena ])

def foldear_simbolos(descripcion):
    '''
    Convierte todos los caracteres no-alfabéticos en espacios.
    '''
    
    return ''.join([ p if p.isalpha() else ' ' for p in descripcion ])

def procesar_descripcion(descripcion, stemmer):
    '''
    Procesa una descripción de aviso del set de datos de Navent.
    El procesamiento se compone de:
    - Eliminar tags HTML
    - Convertir a minúsculas
    - Convertir letras con tilde en letras sin tilde
    - Convertir cualquier caracter no alfabético en espacios
    - Eliminar stop words
    - Eliminar sufijos

    El resultado devuelto es una lista con las palabras de la descripción
    ya procesadas, en el orden en que aparecían.
    '''

    descripcion = strip_html_tags(descripcion).lower()
    descripcion = foldear_simbolos(foldear_tildes(descripcion))
    
    resultado = []
    for palabra in descripcion.split():
        if palabra in STOP_WORDS:
            continue
        resultado.append(palabra)

    return stemmer.stemWords(resultado)

