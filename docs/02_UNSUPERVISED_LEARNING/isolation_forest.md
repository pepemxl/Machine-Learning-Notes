# Isolation Forest

El algoritmo **Isolation Forest** aprovecha un hecho sencillo: las observaciones anómalas son
**pocas y significativamente distintas** de las observaciones `normales`. Por tanto, son más
fáciles de **aislar**.

Esa es la diferencia de fondo con los métodos de la
[detección de anomalías](deteccion_de_anomalias.md) clásica: en lugar de modelar qué es normal
y medir la desviación, Isolation Forest mide **cuánto cuesta separar un punto del resto**.

## Cómo funciona

El bosque se construye a base de **árboles de decisión**, y cada árbol tiene acceso a una
submuestra de los datos de entrenamiento.

Para crear una rama del árbol:

- Se selecciona una **feature al azar**.
- Se elige un **valor de corte aleatorio** para esa feature (entre su mínimo y su máximo).
- Si la observación tiene un valor menor que el corte, sigue la rama izquierda; en caso
  contrario, la derecha.

El proceso continúa hasta que **un único punto queda aislado**, o hasta alcanzar la profundidad
máxima especificada.

La intuición es que un punto anómalo queda aislado tras **pocos cortes**, mientras que un punto
normal, rodeado de muchos otros, requiere muchos más. La profundidad promedio a la que un punto
queda aislado, a lo largo de todos los árboles, es su **puntuación de anomalía**.

## Algunas limitaciones

La intuición nos dice que las anomalías serán *outliers* radiales respecto a los puntos
centrales comunes. Sin embargo, la forma en que se construyen los árboles de decisión —y cómo
opera Isolation Forest— revela problemas causados por dividir las features **únicamente
mediante cortes aleatorios paralelos a los ejes**.

Si visualizamos un gráfico 2D de anomalías y trazamos la puntuación de anomalía, se aprecia
cómo los valores se ven afectados **en franjas verticales y horizontales**. Queda claro
entonces que nuestra partición del espacio de features condiciona la puntuación: los cortes
solo pueden ser perpendiculares a los ejes, así que el modelo tiende a marcar como sospechosas
regiones rectangulares en lugar de radiales.

De ahí que tenga sentido plantear un **esquema de partición distinto**. La variante
**Extended Isolation Forest** aborda justamente esto, permitiendo cortes con pendiente
arbitraria en lugar de solo paralelos a los ejes.

## Notebooks

- [Isolation Forest](Examples/Isolation%20Forest.ipynb)
- [Isolation Forest Feature Selection](Examples/Isolation%20Forest%20Feature%20Selection.ipynb)

## Referencias

- Liu, F. T., Ting, K. M. y Zhou, Z.-H. *Isolation Forest*, ICDM (2008).
- Hariri, S., Kind, M. C. y Brunner, R. J. *Extended Isolation Forest* (2018).
