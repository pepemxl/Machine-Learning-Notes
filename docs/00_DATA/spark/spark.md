# Spark

Apache Spark is a technology that superseded Hadoop's MapReduce as the preferred big data processing platform. Spark is similar to Hadoop in that it's a distributed, general-purpose computing platform. But Spark's unique design, which allows for keeping large amounts of data in memory, offers tremendous
performance improvements. Spark programs can be 100X faster than their MapReduce counterparts.


Spark combines **MapReduce-like capabilities** for batch programming, realtime data-processing functions, SQL-like handling of structured data, graph algorithms, and machine learning, all in a single framework. 


## Applications in Spark

- Application in Spark consists of a `driver program` and `executors` on the cluster.
- A `cluster manager` is an external service for acquiring resources on the cluster. It can be the Spark built-in cluster manager.
- Driver program is the process running the `main()` function of the application and creating the `SparkContext`.
- An `executor` is a process launched for an application on a worker node. The executor runs tasks and keeps data in
memory or in disk storage across them. Each application has its own executors.
- A `Job` is a parallel computation consisting of multiple tasks that gets spawned in response to a Spark action
- Each job gets divided into smaller sets of tasks, called `stages`, that depend on each other similar to the map and reduce stages in MapReduce.
- A `task unit` is a task of work  that will be sent to one executor.
- `Worker node` is node that can run an application code in the cluster.


## Integration Spacrk with Iceberg and Kafka

Integration **Apache Spark**, **Apache Iceberg** and **Apache Kafka** permits  to build moder architectures to proccess data, combining **real time data streaming (Kafka)**, **distributed processing (Spark)** and **gestion of analytic tables (Iceberg)**.

```
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