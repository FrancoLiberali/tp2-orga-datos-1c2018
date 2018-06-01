from stop_words import ESP_STOP_WORDS as BASE_STOP_WORDS, ENG_STOP_WORDS
from html.parser import HTMLParser

STOP_WORDS = set([
    'experiencia', 'empresa', 'busqueda', 'años', 'requisitos', 'excluyente', 'tareas',
 'importante', 'zona', 'manejo', 'equipo', 'cliente', 'clientes', 'conocimientos', 'disponibilidad',
 'laboral', 'area', 'lunes', 'gestion', 'desarrollo', 'viernes', 'principales', 'personal', 'contratacion',
 'hs', 'empresas', 'servicios', 'adecco', 'horario', 'condiciones', 'capacidad', 'time', 'responsabilidades',
 'contar', 'control', 'excelente', 'edad', 'productos', 'atencion', 'nivel', 'seguimiento',
 'puesto', 'posicion', 'orientacion', 'analisis', 'persona', 'cv', 'office', 'calidad', 'avanzado',
 'preferentemente'
]).union(BASE_STOP_WORDS.union(ENG_STOP_WORDS))

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.strict = False
        self.convert_charrefs= True
        self.fed = []
    def handle_data(self, d):
        self.fed.append(d)
    def get_data(self):
        return ' '.join(self.fed)

def strip_html_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


def foldear_acentos(cadena):
    ''' 
    Elimina los acentos de una cadena en minúsculas. 
    Ej: descripción -> descripcion
    '''
    acentos = {'á':'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u', 'ü':'u'}
    return ''.join([ acentos.get(c, c) for c in cadena ])

def foldear_simbolos(cadena):
    '''
    Convierte todos los caracteres que no sean alfanuméricos
    '''
    return ''.join([ c if c.isalnum() else ' ' for c in cadena ])

def es_palabra_inutil(palabra):
    '''
    Devuelve True si palabra es una palabra que no aporta
    contenido.
    '''
    return palabra in STOP_WORDS

def parse(descripcion):
    '''
    Normaliza una descripción de aviso del set de datos de Navent.
    Elimina tags HTML, pasa a minúsculas y la convierte a tokens.
    '''
    resultado = []
    
    for palabra in foldear_simbolos(foldear_acentos(strip_html_tags(descripcion).lower())).split():
        if es_palabra_inutil(palabra):
            continue
        
        resultado.append(palabra)
    
    return ' '.join(resultado)
    
    