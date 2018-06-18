## Preprocesador de set de entrenamiento/test/predicción

Este programa es un intento de normalizar la forma en que convertimos un set de test/entrenamiento/predicción
en algo admisible para un algoritmo de machine learning. El objetivo del mismo es tomar un archivo CSV que tenga entre sus columnas `idaviso` e `idpostulante` y generar los features que correspondan de una forma sencilla y fácilmente modificable.

La base del programa es la carpeta `featurizers`, que es donde se encuentran los diferentes creadores de features. Esta armado de una forma lo suficientemente general como para que agregar un feature no sea más que agregar el código que lo genere y simplemente se agregue la columna en el archivo final sin tener que recrear todo.

El programa carga en memoria los archivos de postulaciones, vistas, detalles de avisos y detalles de postulantes con lo cual podría llegar a tener un uso elevado de memoria.

Para agregar un nuevo feature alcanza con crear una nueva clase que implemente el método `featurize`. Este método va a ser llamado una o más veces con un DataFrame con al menos dos columnas: `idaviso` e `idpostulante` y debe devolver otro DataFrame (o el mismo alterado) con las mismas columnas que tenía, más el/los features creados.

La información sobre avisos, postulantes, vistas y postulaciones se puede obtener importando `dataset.modulo` reemplazando "modulo" por lo que se necesite (avisos, postulantes, vistas o postulaciones). Este import carga en memoria el dataframe deseado si es que el mismo no fue cargado previamente. Para obtener el dataframe alcanza con hacer `dataset.modulo.df`. Para el módulo `aviso` el dataframe se encuentra indexado por `idaviso`. En el caso de postulantes hay dos dataframes (`fiuba_1_postulantes_educacion` y `fiuba_2_postulantes_genero_edad`) que se pueden acceder via `.df_educacion` y via `.df_genero_edad`. Ambos se encuentran indexados por `idpostulante`. La recomendación es **no** modificar estos dataframes, sino hacer copias/utilizar resultados de vistas. Los datos sobre vistas y postulaciones están en su respectivos módulos; a diferencia de los anteriores, estos no se encuentran indexados.

Una vez creado el módulo con la clase, se lo debe importar en `preprocesar_set.py` y luego agregar una instancia de la clase a la constante `FEATURIZERS`.

El uso del programa es el siguiente:

`python3 preprocesar_set.py ruta_entrada ruta_salida [cantidad_lineas_entrada]`

Donde:
- `ruta_entrada` es la ruta al archivo CSV que contiene los pares idaviso, idpostulante.
- `ruta_salida` es la ruta al archivo CSV de salida con los features generados.
- `cantidad_lineas_entrada` es un parámetro opcional que indica cuántas líneas hay en el archivo de entrada. No se determina directamente desde el archivo de entrada para ahorrar tiempo si el archivo es muy grande. Se puede utilizar la salida de `cat ruta_entrada | wc -l` (Linux).

El archivo de entrada *debe* tener una columna `idaviso` y una columna `idpostulante`. El resto de las columnas serán ignoradas durante el procesamiento pero no serán eliminadas; se agregarán al archivo final en el mismo orden en que estaban en el archivo original.

Este programa requiere que exista en la misma carpeta en que se encuentra `preprocesar_set.py` un archivo llamado `rutas.py` con las siguientes constantes definidas:
- `RUTA_AVISOS_DETALLE`: La ruta al archivo `fiuba_6_avisos_detalle.csv`.
- `RUTA_POSTULACIONES`: La ruta al archivo `fiuba_4_postulaciones.csv`.
- `RUTA_VISTAS`: La ruta al archivo `fiuba_3_vistas.csv`
- `RUTA_POSTULANTES_GENERO_EDAD`: La ruta al archivo `fiuba_2_postulantes_genero_edad.csv`
- `RUTA_POSTULANTES_EDUCACION`: La ruta al archivo `fiuba_1_postulantes_educacion.csv`