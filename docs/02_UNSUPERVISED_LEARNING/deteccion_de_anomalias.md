# Detección de Anomalías

Existen muchos modelos de machine learning capaces de detectar anomalías. El más adecuado
depende de las características concretas de los datos y del **tipo de anomalía** que quieras
detectar. Los modelos más comunes se agrupan en tres familias.

## Modelos basados en densidad

Identifican como anomalías los puntos que están **en zonas menos densas** que su entorno.

- **One-Class SVM** (OCSVM) — ver
  [máquinas de vectores de soporte](../01_SUPERVISED_LEARNING/support_vector_machines.md).
- **Local Outlier Factor** (LOF).

## Modelos basados en distancia

Identifican como anomalías los puntos que están **lejos de la mayoría** de los datos.

- **K-Nearest Neighbors** (KNN).
- **K-Means clustering**.

## Modelos probabilísticos

Modelan el **comportamiento normal** de los datos e identifican como anomalías los puntos que
no se ajustan a ese comportamiento esperado.

- **Modelos de mezcla de gaussianas** (GMM).
- **Modelos de Markov**.

## Cómo elegir

En última instancia, el mejor enfoque depende de las características específicas de los datos y
del tipo de anomalía buscada. Suele ser útil **probar varios modelos distintos y comparar su
rendimiento** para determinar cuál funciona mejor en tu situación concreta.

Ver [Isolation Forest](isolation_forest.md) para un método basado en aislamiento, que parte de
un supuesto distinto a los tres anteriores.
