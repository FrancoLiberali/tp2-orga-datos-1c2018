from html.parser import HTMLParser

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

def foldear_simbolos(cadena):
    ''' 
    Elimina los acentos de una cadena en minúsculas. 
    Ej: descripción -> descripcion
    '''
    acentos = {'á':'a', 'é':'e', 'í':'i', 'ó':'o', 'ú':'u', 'ü':'u'}
    cadena = list(cadena)
    for i in range(len(cadena)):
        if not cadena[i].isalfa():
            cadena[i] = ' '
        else:
            cadena[i] = acentos.get(cadena[i], cadena[i])
    
    return ''.join(cadena)

def es_palabra_inutil(palabra):
    '''
    Devuelve True si palabra es una palabra que no aporta
    contenido.
    '''
    return palabra in set(['el', 'la', 'los', 
        'les', 'que', 'para', 'las', 'como', 'donde', 'a', 'y', 
        'o', 'por', 'pero', 'sobre', 'sin', 'en', 'con', 'tras',
        'contra', 'queres', 'trabajo', 'se', 'de', 'requisito', 'requisitos',
        'plata', 'del', 'un', 'al', 'una'])

def parse(descripcion):
    '''
    Normaliza una descripción de aviso del set de datos de Navent.
    Elimina tags HTML, pasa a minúsculas y la convierte a tokens.
    '''
    resultado = []
    
    for palabra in strip_html_tags(descripcion).lower().split():
        if es_palabra_inutil(palabra):
            continue
            
        resultado.extend(foldear_simbolos(palabra).split())
    
    return ' '.join(resultado)
    
    