# Trabajo práctico 2 - Organización de Datos

Los notebooks que están acá (los nuevos al menos) usan un archivo `rutas.py` para evitar
el hardcodeo de las rutas y tener que modificar los notebooks cada vez. 

Este archivo está en `.gitignore` así que no se va a pushear. Mi archivo `rutas.py` tiene 
el siguiente aspecto:

```python
RUTA_HOME             = '/home/luciano/orga-datos/'
RUTA_BASE             = RUTA_HOME + 'datos_preprocesados/'
RUTA_DATOS_PROCESADOS = RUTA_HOME + 'datos_procesados/'
RUTA_TMP              = RUTA_HOME + 'tmp/'

RUTA_POSTULANTES    = RUTA_BASE + 'postulantes.csv'
RUTA_VISTAS         = RUTA_BASE + 'fiuba_3_vistas.csv'
RUTA_POSTULACIONES  = RUTA_BASE + 'fiuba_4_postulaciones.csv'
RUTA_AVISOS_DETALLE = RUTA_BASE + 'fiuba_6_avisos_detalle.csv'

RUTA_VECTOR_POSTULANTES = RUTA_DATOS_PROCESADOS + 'vector_postulantes.csv'
RUTA_SET_ENTRENAMIENTO  = RUTA_TMP + 'set_entrenamiento.csv'
RUTA_SET_NO_POSTULADOS  = RUTA_TMP + 'set_no_postulados.csv'

RUTA_SUBMITS = RUTA_TMP + 'submits/'
```