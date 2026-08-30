# Big Data

**Big data** designa conjuntos de datos cuyo volumen, velocidad o variedad superan la
capacidad de las herramientas tradicionales de procesamiento y almacenamiento. La frontera no
es un número absoluto: es el punto en que **una sola máquina deja de ser suficiente** y hay
que repartir el trabajo entre varias.

Ver también [Dimensiones de la analítica](dimensiones_analitica.md), donde se describen las
V del big data (volumen, velocidad, variedad y valencia).

## Qué cambia al escalar

Cuando los datos no caben en una máquina, varios supuestos se rompen:

- **El movimiento de datos domina el coste.** Mover un terabyte por la red es más caro que
  recalcularlo. Por eso los sistemas distribuidos llevan *el cómputo a los datos*, y no al
  revés.
- **Los fallos son la norma.** Con cientos de nodos, que alguno falle durante un job deja de
  ser excepcional. El sistema debe tolerarlo sin reiniciar todo.
- **El orden deja de ser gratis.** Ordenar, unir o desduplicar exige *shuffle*: redistribuir
  datos entre nodos. Es la operación más cara de cualquier pipeline distribuido.

## Modelos de procesamiento

| Modelo | Latencia | Uso típico |
|---|---|---|
| **Batch** | Minutos a horas | Reportes, entrenamiento de modelos, ETL nocturno |
| **Micro-batch** | Segundos | Métricas casi en tiempo real, dashboards |
| **Streaming** | Milisegundos | Detección de fraude, alertas, personalización |

## Stacks habituales

- **SMACK** — Spark, Mesos, Akka, Cassandra, Kafka.
- **Ecosistema Hadoop** — HDFS, YARN, Hive, HBase.
- **ELK** — Elasticsearch, Logstash, Kibana.
- **Lakehouse** — Spark o Trino sobre formatos de tabla abiertos (Iceberg, Delta, Hudi).

Ver el detalle en [Proyectos generales de ML](../09_SYSTEMS/proyectos_generales_de_ml.md).

## Herramientas en estas notas

- [Spark](spark/spark.md) y [PySpark](spark/pyspark.md) — procesamiento distribuido.
- [Bases de datos](introduccion_bases_de_datos.md) — dónde aterrizan los datos.
- [OpenTSDB](databases/opentsdb.md) y [Goku](databases/goku.md) — series de tiempo a escala.
- [Clustering en Big Data](../02_UNSUPERVISED_LEARNING/clustering_en_big_data.md) — cómo
  cambian los algoritmos cuando los datos no caben en memoria.
