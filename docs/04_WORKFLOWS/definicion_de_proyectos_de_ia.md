# Definición de Proyectos de IA

## El sesgo centrado en el modelo y el principio GIGO

Es muy común prestar demasiada atención a los modelos de ML y descuidar otras partes
importantes en la construcción de sistemas de machine learning. A este fenómeno se le suele
llamar **sesgo centrado en el modelo** (*model centric bias*).

Va de la mano del principio **GIGO** (*Garbage In, Garbage Out*), descrito en la
[introducción al aprendizaje supervisado](../01_SUPERVISED_LEARNING/introduccion.md): si los
datos y las features son malos, ningún modelo lo compensará.

## El enfoque formal

El enfoque de manual para hacer análisis de datos es una serie de pasos:

1. Recolectar datos con un proceso ETL o ELT.
2. Realizar análisis exploratorio de datos (**EDA**) sobre esas colecciones.
3. Formular hipótesis a partir del EDA.
4. Probar modelos sobre ellas para confirmar o descartar las hipótesis.

Ver [Las seis fases del análisis de datos](../00_DATA/fases_analisis_datos.md) y
[Kedro](kedro.md), que impone esta estructura en el propio proyecto.

## El enfoque real

El enfoque que se sigue en muchos proyectos de IA es algo más complejo. Normalmente se parte de
**datos preexistentes que fueron creados con fines de aplicación**, no de análisis. El proceso
es más bien:

1. Definir objetivos.
2. Revisar los modelos existentes con el único fin de determinar cuáles pueden ayudar a
   alcanzar ese objetivo.

La diferencia importa: en el enfoque formal los datos se recogen **para** la pregunta; en el
real, la pregunta se adapta a los datos que ya existen. Eso condiciona qué hipótesis son
verificables y cuánta confianza merecen los resultados.
