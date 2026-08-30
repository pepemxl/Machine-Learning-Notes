# Spark

**Apache Spark** es la tecnología que desplazó a MapReduce de Hadoop como plataforma
preferida para el procesamiento de big data. Se parece a Hadoop en que es una plataforma de
cómputo distribuida y de propósito general, pero su diseño —que permite **mantener grandes
volúmenes de datos en memoria**— ofrece mejoras de rendimiento enormes: un programa de Spark
puede ser hasta 100 veces más rápido que su equivalente en MapReduce.

Spark combina en un solo framework capacidades **similares a MapReduce** para procesamiento
por lotes, funciones de procesamiento en tiempo real, manejo de datos estructurados al estilo
SQL, algoritmos de grafos y machine learning.

Para cargas que no encajan en el modelo de dataflow —tareas heterogéneas, con estado o con
GPU— ver [Ray](../../04_WORKFLOWS/ray.md), que resuelve un problema distinto y a menudo
complementario.

## Aplicaciones en Spark

- Una **aplicación** en Spark consiste en un `driver program` y varios `executors` en el
  clúster.
- El `cluster manager` es un servicio externo que adquiere recursos en el clúster. Puede ser
  el gestor integrado de Spark.
- El **driver program** es el proceso que ejecuta la función `main()` de la aplicación y crea
  el `SparkContext`.
- Un `executor` es un proceso lanzado para una aplicación en un nodo *worker*. Ejecuta tareas
  y mantiene datos en memoria o en disco entre ellas. Cada aplicación tiene sus propios
  executors.
- Un `Job` es un cómputo paralelo compuesto de múltiples tareas, que se genera en respuesta a
  una **acción** de Spark.
- Cada job se divide en conjuntos más pequeños de tareas, llamados `stages`, que dependen
  entre sí de forma análoga a las etapas *map* y *reduce* de MapReduce.
- Una `task` es una unidad de trabajo que se envía a un executor.
- Un `worker node` es un nodo capaz de ejecutar código de la aplicación en el clúster.

## Integración de Spark con Iceberg y Kafka

La integración de **Apache Spark**, **Apache Iceberg** y **Apache Kafka** permite construir
arquitecturas modernas de procesamiento de datos, combinando **streaming en tiempo real
(Kafka)**, **procesamiento distribuido (Spark)** y **gestión de tablas analíticas
(Iceberg)**.

```text
Kafka (Streaming) → Spark (Processing) → Iceberg (Tabular storage)
```

- **Kafka**: Fuente de datos en tiempo real (eventos, logs, etc.).  
- **Spark Structured Streaming**: Procesa los datos en micro-lotes o continuamente.  
- **Iceberg**: Almacena los datos en formato tabular (con capacidades ACID, time travel, etc.).  

---

## **2. Configuración Paso a Paso**

### **2.1. Leer Datos desde Kafka con Spark**
Spark Structured Streaming puede consumir datos de Kafka directamente:  

```python
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("KafkaToIceberg") \
    .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
    .config("spark.sql.catalog.demo", "org.apache.iceberg.spark.SparkCatalog") \
    .config("spark.sql.catalog.demo.type", "hadoop") \
    .config("spark.sql.catalog.demo.warehouse", "/path/to/warehouse") \
    .getOrCreate()

# Leer datos desde Kafka
df_kafka = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka-broker:9092") \
    .option("subscribe", "mi-topico") \
    .option("startingOffsets", "earliest") \
    .load()

# Parsear los datos (ejemplo: JSON)
from pyspark.sql.functions import from_json, col

schema = "id INT, nombre STRING, fecha TIMESTAMP"
df_parsed = df_kafka.select(
    from_json(col("value").cast("string"), schema).alias("data")
).select("data.*")
```

### **2.2. Procesar los Datos en Spark**
Puedes aplicar transformaciones (filtros, agregaciones, joins, etc.):  

```python
df_processed = df_parsed.filter(col("id") > 100)
```

### **2.3. Escribir los Datos en Iceberg**
Iceberg soporta escritura en streaming y batch:  

```python
# Escribir en Iceberg (modo batch)
df_processed.write \
    .format("iceberg") \
    .mode("append") \
    .save("demo.db.tabla_eventos")

# O en streaming
df_processed.writeStream \
    .format("iceberg") \
    .outputMode("append") \
    .option("checkpointLocation", "/path/to/checkpoint") \
    .trigger(processingTime="1 minute") \
    .toTable("demo.db.tabla_eventos") \
    .start() \
    .awaitTermination()
```

---

## **3. Configuraciones Clave**
| Componente | Configuración Importante |
|------------|--------------------------|
| **Spark** | `spark.jars.packages`: Incluir dependencias de Kafka, Iceberg y conectores. |
| **Kafka** | `startingOffsets`, `failOnDataLoss`, `maxOffsetsPerTrigger`. |
| **Iceberg** | `write.format.iceberg`, `mergeSchema`, `partitionBy`. |

Ejemplo de configuración en `spark-submit`:  
```bash
spark-submit --packages \
org.apache.iceberg:iceberg-spark-runtime-3.3_2.12:1.3.0,\
org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.0
```

---

## **4. Ventajas de la Integración**
✅ **Tiempo real + histórico**: Kafka maneja streaming, Iceberg almacena datos históricos.  
✅ **Consultas SQL eficientes**: Iceberg soporta `time travel`, `schema evolution`.  
✅ **Escalabilidad**: Spark distribuye el procesamiento.  

---

## **5. Alternativas y Mejoras**
- **Usar Delta Lake o Apache Hudi** en lugar de Iceberg (similar funcionalidad ACID).  
- **Kafka Connect + Iceberg Sink**: Alternativa sin Spark.  
- **Optimización de particiones en Iceberg** para mejorar consultas.  

---

### **Conclusión**
Esta integración es poderosa para **pipelines de datos híbridos** (streaming + batch). Si necesitas detalles específicos (ej: manejo de esquemas, optimización de escritura), dime y te ayudo. 🚀
