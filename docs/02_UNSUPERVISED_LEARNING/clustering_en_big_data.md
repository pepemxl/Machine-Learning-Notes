# Clustering en Big Data

El clustering es un método no supervisado muy popular y una herramienta esencial para el
análisis de [Big Data](../00_DATA/big_data.md).

Se puede usar de dos formas: como **paso de preprocesamiento** para reducir la dimensionalidad
antes de ejecutar el algoritmo de aprendizaje, o como **herramienta estadística** para
descubrir patrones útiles dentro de un dataset.

Los métodos de clustering se basan en **optimización iterativa**. Aunque son efectivos para
extraer patrones útiles, consumen recursos de cómputo masivos y tienen costes computacionales
altos, debido a la elevada dimensionalidad de las aplicaciones de datos actuales.

## Los retos del clustering a gran escala

Los retos se caracterizan en tres componentes principales:

1. **Volumen**. Como la escala de los datos generados por las tecnologías modernas crece
   exponencialmente, los métodos de clustering se vuelven computacionalmente caros y no
   escalan a datasets muy grandes.

2. **Velocidad**. Se refiere al ritmo al que los datos entran al sistema. Manejar datos de alta
   velocidad exige desarrollar métodos de clustering **más dinámicos**, capaces de derivar
   información útil en tiempo real.

3. **Variedad**. Los datos actuales son heterogéneos y en su mayoría no estructurados, lo que
   hace que gestionarlos, fusionarlos y gobernarlos sea extremadamente complicado.

## Familias de métodos

### Clustering basado en k-means

- Machine learning
- Difuso (*fuzzy*)
- Estadística
- Escalable

### Clustering jerárquico

- Minería de datos
- Machine learning
- Escalable

### Clustering basado en densidad

- Grafos
- Machine learning
- Minería de datos
- Escalable

## Ver también

- [Introducción al aprendizaje no supervisado](introduccion.md)
- [PySpark](../00_DATA/spark/pyspark.md) — procesamiento distribuido para aplicar estos métodos
  a escala.
