### Trabajo Práctico N° 2: Predicción de postulaciones a avisos laborales

FIUBA - 75.06 - Organización de Datos

Flujo de trabajo para ejecutar el algoritmo:

- Ejecutar `preprocesamiento.ipynb` para unir los archivos provistos por navent (fiuba_*) de cada período en un solo archivo por tipo de información.
- Ejecutar `generar_set_test` para crear el set de test/train inicial y el set de no-postulados random
- Ejecutar `preprocesar_set` para generar los features en los dos CSV creados anteriormente y en el set a predecir.
- Ejecutar `generar_set_test/refinamiento` para refinar el set de no-postulados via aprendizaje semi-supervisado
- Ejecutar `submit-final.ipynb` para entrenar el algoritmo y generar el submit.

