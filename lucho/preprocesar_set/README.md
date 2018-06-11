## Preprocesador de set de entrenamiento/test/predicción

Este programa es un intento de normalizar la forma en que convertimos un set de test/entrenamiento/predicción
en algo admisible para un algoritmo de machine learning. 

La base del programa es el archivo `featurizer.py`, que es donde se encuentran los diferentes creadores de features. Esta armado de una forma lo suficientemente general como para que agregar un feature no sea más que agregar el código que lo genere y simplemente se agregue la columna en el archivo final sin tener que recrear todo o recurrir a pandas.

El programa carga en memoria los archivos de postulaciones, vistas, detalles de avisos y detalles de postulantes con lo cual podría llegar a tener un uso elevado de memoria.

Para agregar un nuevo feature alcanza con crear una clase que herede de `Featurizer` e implemente los métodos `featurize` y `get_columns`. El método `featurize` va a ser llamado por cada par aviso-postulante y es donde la conversión sucede. Dentro de este método se tiene disponible información sobre las vistas, postulaciones, avisos y postulantes. El resultado del llamado debe ser una lista con los features devueltos, en un orden específico que debe mantenerse en cada llamado a `featurize`. El método `get_columns` devuelve una lista con el nombre de cada feature, en el mismo orden en que `featurize` devuelve los resultados.

Una vez creada la clase, se debe agregar una instancia de la misma en la constante `FEATURIZERS` dentro del archivo `preprocesar_set.py` y con esto ya deberían generarse los nuevos features junto con los anteriores. Esa constante define que featurizers se usan y por consiguiente que features van a quedar en el archivo final. Si el featurizer requiere parámetros iniciales pueden ser pasados al crear la instancia dentro de esta constante.

El uso del programa es el siguiente:

`python3 preprocesar_set.py ruta_entrada ruta_salida [cantidad_lineas_entrada]`

Donde:
- `ruta_entrada` es la ruta al archivo CSV que contiene los pares idaviso, idpostulante.
- `ruta_salida` es la ruta al archivo CSV de salida con los features generados.
- `cantidad_lineas_entrada` es un parámetro opcional que indica cuántas líneas hay en el archivo de entrada. No se determina directamente desde el archivo de entrada para ahorrar tiempo si el archivo es muy grande. Se puede utilizar la salida de `cat ruta_entrada | wc -l` (Linux).

Este programa requiere que exista en la carpeta un archivo `rutas.py` con las siguientes constantes definidas:
- `RUTA_AVISOS_DETALLE`: La ruta al archivo `fiuba_6_avisos_detalle.csv`.
- `RUTA_POSTULANTES_DETALLE`: La ruta al archivo `postulantes.csv`, generado por un notebook dentro de la carpeta `viejo-paradigma`.
- `RUTA_POSTULACIONES`: La ruta al archivo `fiuba_4_postulaciones.csv`.
- `RUTA_VISTAS`: La ruta al archivo `fiuba_3_vistas.csv`