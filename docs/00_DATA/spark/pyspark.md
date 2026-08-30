# PySpark


**PySpark** es la biblioteca de Python para **Apache Spark**, un framework de procesamiento distribuido diseñado para manejar big data de manera eficiente.

## **¿Qué es PySpark?**

- Es la **API de Python para Spark**, permitiendo a los desarrolladores usar Spark con sintaxis de Python.
- Proporciona una interfaz fácil para trabajar con **datos distribuidos** usando DataFrames y SQL.
- Permite integrar librerías de Python (como NumPy, Pandas y scikit-learn) en pipelines de Spark.

### **Diferencias entre PySpark y Apache Spark**

| **Aspecto**       | **Apache Spark** (Core)                          | **PySpark**                                  |
|-------------------|------------------------------------------------|---------------------------------------------|
| **Lenguaje**      | Escrito principalmente en **Scala** (y Java)   | **API de Python** para Spark                |
| **Sintaxis**      | Usa código Scala/Java/R                        | Usa código Python                           |
| **Rendimiento**   | Más rápido (ejecución nativa en JVM)          | Un poco más lento (comunicación Python-JVM) |
| **Uso de Pandas** | No tiene integración directa con Pandas        | Permite usar **Pandas API** (pandas-on-Spark) |
| **Facilidad**     | Requiere conocimiento de Scala/Java           | Más accesible para científicos de datos     |
| **Ecosistema**    | Incluye Spark SQL, MLlib, Streaming, GraphX    | Accede a las mismas funcionalidades desde Python |

### **Ejemplo de Código en PySpark**

```python title="Ejemplo" linenums="1"
from pyspark.sql import SparkSession

# Iniciar una sesión de Spark
spark = SparkSession.builder.appName("Ejemplo").getOrCreate()

# Leer un archivo CSV distribuido
df = spark.read.csv("datos.csv", header=True)

# Filtrar datos y mostrar resultado
df.filter(df["edad"] > 30).show()
```

## RDD

Un **RDD (Resilient Distributed Dataset)** es la estructura de datos fundamental de Apache Spark. Representa una colección **distribuida**, **inmutable** y **tolerante a fallos** de elementos que pueden procesarse en paralelo.

### **Características clave de los RDDs**

1. **Distribuido:** Los datos se dividen en particiones y se distribuyen en los nodos del clúster.
2. **Resiliente (Tolerante a fallos):** Si un nodo falla, Spark puede reconstruir los datos usando el **linaje (lineage)** (registro de transformaciones).
3. **Inmutable:** No se modifican, sino que se crean nuevos RDDs mediante transformaciones.
4. **Lazy Evaluation:** Las operaciones no se ejecutan hasta que se llama a una **acción** (ej: `collect()`, `count()`).



### ** ¿Cómo crear un RDD en PySpark?**

Hay **dos formas principales** de crear un RDD:

#### **1. Desde una colección de Python (list, tuple, etc.)**

Usando `sparkContext.parallelize()`.

```python title="Ejemplo de RDD" linenums="1"
from pyspark.sql import SparkSession

# Iniciar SparkSession
spark = SparkSession.builder.appName("RDD Example").getOrCreate()

# Crear un RDD desde una lista
data = [1, 2, 3, 4, 5]
rdd = spark.sparkContext.parallelize(data)

print(rdd.collect())  # Salida: [1, 2, 3, 4, 5]
```

- **Particionamiento:** Opcionalmente, podemos definir el número de particiones:
  ```python title="Ejemplo de RDD con número de particiones" linenums="1"
  rdd = spark.sparkContext.parallelize(data, numSlices=3)
  ```

#### **2. Desde un archivo externo (HDFS, S3, local, etc.)**

Usando `sparkContext.textFile()`.
```python  title="Ejemplo de RDD" linenums="1"
# Leer un archivo de texto (cada línea es un elemento del RDD)
rdd_text = spark.sparkContext.textFile("ruta/al/archivo.txt")

# Leer todos los archivos de un directorio
rdd_multi = spark.sparkContext.wholeTextFiles("ruta/al/directorio/*")
```

### ** Operaciones básicas con RDDs**

#### **Transformaciones (Lazy, crean nuevos RDDs)**

```python  title="Ejemplo de map filter reduce" linenums="1"
# Filtrado
rdd_filtered = rdd.filter(lambda x: x > 2)  # [3, 4, 5]

# Mapeo (transformación elemento a elemento)
rdd_squared = rdd.map(lambda x: x * x)  # [1, 4, 9, 16, 25]

# Reducción (acción)
suma = rdd.reduce(lambda a, b: a + b)  # 15
```

#### **Acciones (Ejecutan las transformaciones pendientes)**

```python  title="Ejemplo de RDD con evaluación lazy" linenums="1"
print(rdd.count())      # Número de elementos: 5
print(rdd.first())      # Primer elemento: 1
print(rdd.take(3))      # Toma los primeros 3: [1, 2, 3]
```

### **RDD vs DataFrames**

| **RDD**                          | **DataFrame**                     |
|----------------------------------|-----------------------------------|
| Trabaja con datos **sin esquema** | Datos **estructurados (columnas)** |
| Más bajo nivel (requiere código manual) | Optimizado (Catalyst Optimizer) |
| Menos eficiente en consultas SQL | Alto rendimiento en SQL y filtros |
| Ideal para datos no estructurados | Ideal para datos tabulares |

- Los **RDDs** son la base de Spark, pero en PySpark se usan más **DataFrames** (por su optimización).
- Son útiles cuando necesitas **control fino** sobre las operaciones o trabajas con datos **no estructurados**.
- Se crean desde colecciones de Python o archivos externos usando `parallelize()` o `textFile()`.


## Dataframes


### **Snippet para Leer un CSV en PySpark DataFrame**

Ejemplo de cómo cargar un archivo CSV en un DataFrame de PySpark, con opciones comunes para manejar encabezados, esquemas y delimitadores:

#### **1. Lectura básica (con encabezado)**
```python
from pyspark.sql import SparkSession

# Iniciar una sesión de Spark
spark = SparkSession.builder.appName("LeerCSV").getOrCreate()

# Leer el archivo CSV (asumiendo que tiene encabezado)
df = spark.read.csv("ruta/al/archivo.csv", header=True, inferSchema=True)

# Mostrar el esquema y los datos
df.printSchema()
df.show(5)
```

#### **2. Lectura con opciones personalizadas**
```python
# Definir manualmente el esquema (opcional)
from pyspark.sql.types import StructType, StructField, StringType, IntegerType

schema = StructType([
    StructField("nombre", StringType(), nullable=True),
    StructField("edad", IntegerType(), nullable=True),
    StructField("ciudad", StringType(), nullable=True)
])

# Leer CSV con configuración avanzada
df = spark.read.csv(
    "ruta/al/archivo.csv",
    header=True,
    schema=schema,          # Usar esquema definido
    sep=";",                # Delimitador (ej: ; en lugar de ,)
    encoding="UTF-8",       # Codificación
    nullValue="NA"          # Tratar "NA" como nulos
)

df.show(5)
```

#### **3. Lectura desde múltiples archivos CSV**
```python
# Leer todos los CSVs de un directorio
df = spark.read.csv(
    "ruta/al/directorio/*.csv",
    header=True,
    inferSchema=True
)
```

#### **4. Guardar el DataFrame como CSV**
```python
# Guardar el DataFrame en un archivo CSV
df.write.csv(
    "ruta/destino/",
    header=True,       # Incluir encabezado
    mode="overwrite"   # Sobrescribir si existe
)
```

| **Parámetro**    | **Descripción**                                                                 |
|------------------|-------------------------------------------------------------------------------|
| `header=True`    | Usa la primera fila como nombres de columnas.                                |
| `inferSchema=True`| Infiere automáticamente el tipo de datos (puede ser lento en archivos grandes). |
| `sep=";"`        | Define el delimitador (por defecto es `,`).                                  |
| `schema`         | Permite definir manualmente el esquema para mayor control.                   |
| `mode="overwrite"`| Comportamiento al guardar: `overwrite`, `append`, `ignore`, `error`.         |



### **Diferencia entre `read.csv` y `read.format("csv")`**

También puedes usar la sintaxis más genérica:
```python
df = spark.read.format("csv").option("header", "true").load("ruta/al/archivo.csv")
```
- **Ventaja:** Más flexible para integración con otros formatos (JSON, Parquet, etc.).



## **Filtrado en PySpark: Métodos y Ejemplos Prácticos**

En PySpark, podemos filtrar DataFrames o RDDs usando **condiciones lógicas**.

### **1. Filtrado en DataFrames (Recomendado)**
Los DataFrames ofrecen operaciones optimizadas (Catalyst Optimizer) para filtrado.

#### **Método 1: Usando `filter()` o `where()`**
Ambos son equivalentes (elige el que prefieras).

```python title="Ejemplo de Filter"
from pyspark.sql import SparkSession

spark = SparkSession.builder.appName("Filtrado").getOrCreate()

# Ejemplo: DataFrame de empleados
data = [("Juan", 25, "IT"), ("Ana", 30, "Marketing"), ("Luis", 22, "IT")]
df = spark.createDataFrame(data, ["nombre", "edad", "departamento"])

# Filtrar empleados de IT
df_filtrado = df.filter(df["departamento"] == "IT")
df_filtrado.show()
```

```bash title="Salida"
+------+---+-------------+
|nombre|edad|departamento|
+------+---+-------------+
|  Juan| 25|           IT|
|  Luis| 22|           IT|
+------+---+-------------+
```

#### **Método 2: Filtrado con SQL-like (expresiones condicionales)**

```python title="Ejemplo con condicional más complejo"
from pyspark.sql.functions import col

# Filtrar mayores de 25 años y que no sean de Marketing
df_filtrado = df.filter((col("edad") > 25) & (col("departamento") != "Marketing"))
df_filtrado.show()
```

#### **Método 3: Usando SQL directo**

```python
df.createOrReplaceTempView("empleados")

# Consulta SQL con WHERE
df_filtrado = spark.sql("SELECT * FROM empleados WHERE edad > 22 AND departamento = 'IT'")
df_filtrado.show()
```

#### **2. Filtrado en RDDs (Programación funcional)**

Si trabajas con RDDs (menos común en PySpark moderno), usa `filter()` con funciones lambda.

```python
# Crear un RDD
rdd = spark.sparkContext.parallelize([1, 2, 3, 4, 5])

# Filtrar números pares
rdd_filtrado = rdd.filter(lambda x: x % 2 == 0)
print(rdd_filtrado.collect())  # Salida: [2, 4]
```


#### **3. Filtrado Avanzado (Funciones útiles)**

| Operador | Ejemplo                          | Descripción                     |
|----------|----------------------------------|---------------------------------|
| `&`      | `(col("edad") > 20) & (col("edad") < 30)` | AND lógico                     |
|  `\|`       | `(col("dep") == "IT") \| (col("dep") == "HR")` | OR lógico                      |
| `~`      | `~(col("nombre").like("%A%"))`   | NOT (inversión de condición)   |

#### **Funciones de columnas útiles:**

```python
from pyspark.sql.functions import col, isnull, like

# Filtrar valores nulos
df.filter(isnull(col("nombre"))).show()

# Filtrar nombres que empiezan con "A"
df.filter(col("nombre").like("A%")).show()

# Filtrar usando una lista de valores
df.filter(col("departamento").isin(["IT", "HR"])).show()
```

#### **4. Rendimiento en Filtrados**

- **Evita `collect()`:** Trae todos los datos al driver (puede causar OOM).
- **Usa `select()` antes del filtro:** Reduce el ancho de los datos.
  ```python
  df.select("nombre", "edad").filter(col("edad") > 25).show()
  ```
- **Particionado:** Si filtramos por una columna usada en `partitionBy`, Spark optimiza el proceso.


#### **Ejemplo Completo: Pipeline de Filtrado**

```python
# Leer CSV
df = spark.read.csv("empleados.csv", header=True, inferSchema=True)

# Pipeline de filtrado
resultado = (
    df
    .select("nombre", "edad", "salario")
    .filter((col("edad") > 25) & (col("salario") > 50000))
    .orderBy("edad")
)

resultado.show()
```

- **DataFrames:** Usa `filter()`/`where()` con sintaxis SQL-like (óptimo para Spark SQL).
- **RDDs:** Usa `filter()` con funciones lambda (útil para datos no estructurados).
- **Optimización:** Combina filtros con `select()` y evita operaciones costosas como `collect()`.



## **Contar el Número de Filas (Rows) en un DataFrame de PySpark**

En PySpark, hay varias formas de contar las filas de un DataFrame. Las principales son:

#### **1. Usar `count()` (Recomendado)**

```python
# Crear un DataFrame de ejemplo
from pyspark.sql import SparkSession
spark = SparkSession.builder.appName("ContarFilas").getOrCreate()

data = [("Juan", 25), ("Ana", 30), ("Luis", 22)]
df = spark.createDataFrame(data, ["nombre", "edad"])

# Contar filas
num_filas = df.count()
print("Número de filas:", num_filas)  # Salida: 3
```
**Ventaja:**
- Es el método **más eficiente** porque Spark optimiza esta operación.

---

#### **2. Usar `len()` con `collect()` (No recomendado para datos grandes)**
```python
# ¡Cuidado! collect() trae TODOS los datos al driver (puede causar OOM)
num_filas = len(df.collect())
print("Número de filas:", num_filas)  # Salida: 3
```
**Problema:**
- `collect()` carga **todos los datos en memoria del driver**, lo que es ineficiente y peligroso con datasets grandes.


#### **3. Usar SQL Directo**
```python
df.createOrReplaceTempView("personas")
num_filas = spark.sql("SELECT COUNT(*) FROM personas").collect()[0][0]
print("Número de filas:", num_filas)  # Salida: 3
```


#### **4. Usar `groupBy().count()` (Útil para conteos agrupados)**
```python
# Si necesitas contar filas por grupo (ej: departamento)
df_conteo = df.groupBy("departamento").count()
df_conteo.show()
```

#### **¿Cuál es la forma más eficiente?**

- ✅ `df.count()` Siempre la mejor opción.
- ❌ `len(df.collect())` Evítalo en producción (riesgo de `OutOfMemoryError`).


#### **Ejemplo Práctico con un CSV**

```python
# Leer un archivo CSV y contar filas
df = spark.read.csv("datos.csv", header=True)
print("Total de filas:", df.count())
```

## **Manejo de Data Faltante (Valores Nulos/NaN) en PySpark**

En PySpark, los valores faltantes se representan como **`null`** (en columnas numéricas o de string) o **`NaN`** (solo en columnas numéricas).

### **1. Detección de Valores Faltantes**

#### **a) `isNull()` y `isNotNull()` (Filtrar filas con nulos)**

```python
from pyspark.sql.functions import col

# Filtrar filas donde 'edad' es NULL
df_filtrado = df.filter(col("edad").isNull())

# Filtrar filas donde 'nombre' NO es NULL
df_no_nulos = df.filter(col("nombre").isNotNull())
```

#### **b) `na.count()` (Contar nulos por columna)**

```python
# Contar nulos en cada columna
df.na.count().show()
```

#### **c) `dropna()` (Eliminar filas con nulos)**

```python
# Eliminar filas donde TODAS las columnas son nulas
df_sin_nulos = df.na.drop(how="all")

# Eliminar filas donde AL MENOS UNA columna es nula (por defecto)
df_sin_nulos = df.na.drop()

# Eliminar filas donde 'edad' o 'salario' son nulos
df_sin_nulos = df.na.drop(subset=["edad", "salario"])
```


### **2. Imputación de Valores Faltantes**

#### **a) `fill()` (Rellenar con un valor constante)**

```python
# Rellenar nulos en columna numérica
df_rellenado = df.na.fill({"edad": 0, "salario": 1000})

# Rellenar nulos en strings
df_rellenado = df.na.fill({"departamento": "Desconocido"})
```

#### **b) `fill()` con la media, mediana o moda**

```python
from pyspark.sql.functions import mean

# Calcular la media de 'edad' y rellenar nulos
media_edad = df.select(mean(col("edad"))).collect()[0][0]
df_rellenado = df.na.fill({"edad": media_edad})
```

#### **c) Usando `Imputer` (Scikit-learn style)**

```python
from pyspark.ml.feature import Imputer

imputer = Imputer(
    inputCols=["edad", "salario"],
    outputCols=["edad_imputada", "salario_imputado"],
    strategy="median"  # "mean", "median", or "mode"
)

df_imputado = imputer.fit(df).transform(df)
```


### **3. Manejo Avanzado**

#### **a) Reemplazar valores específicos (no solo nulos)**

```python
df_limpio = df.na.replace("N/A", "Desconocido", subset=["departamento"])
```

#### **b) Usar `when()` + `otherwise()` para lógica condicional**

```python
from pyspark.sql.functions import when

df_transformado = df.withColumn(
    "edad_ajustada",
    when(col("edad").isNull(), 0).otherwise(col("edad"))
```

#### **c) Eliminar columnas con muchos nulos**

```python
# Eliminar columnas donde >50% son nulos
from pyspark.sql.functions import count, when, lit

total_filas = df.count()
umbral = 0.5 * total_filas

columnas_a_eliminar = [
    col_name for col_name in df.columns
    if df.filter(col(col_name).isNull()).count() > umbral
]

df_limpio = df.drop(*columnas_a_eliminar)
```


### **4. Guardar DataFrame con Nulos**

PySpark mantiene los `null` al guardar en formatos como CSV, Parquet o JSON:
```python
df.write.csv("data_limpia.csv", header=True, nullValue="NULL")
```

| **Escenario**               | **Solución Recomendada**                     |
|-----------------------------|---------------------------------------------|
| Eliminar filas con nulos    | `df.na.drop()`                              |
| Rellenar con valor constante| `df.na.fill({"col": valor})`                |
| Imputación automática       | `Imputer(strategy="mean"/"median"/"mode")`  |
| Reemplazar valores específicos | `df.na.replace("old", "new")`           |
| Manejo condicional          | `when(col(...).isNull(), ...).otherwise(...)`|


### **Ejemplo Completo**

```python
# Paso 1: Eliminar filas donde 'salario' es nulo
df_limpio = df.na.drop(subset=["salario"])

# Paso 2: Rellenar 'edad' con la mediana
from pyspark.ml.feature import Imputer
imputer = Imputer(inputCols=["edad"], outputCols=["edad_imputada"], strategy="median")
df_final = imputer.fit(df_limpio).transform(df_limpio)

# Paso 3: Reemplazar "N/A" en 'departamento'
df_final = df_final.na.replace("N/A", "Desconocido", ["departamento"])
```


## ¿Qué es una SparkSession?

**SparkSession** es el punto de entrada principal para interactuar con las funcionalidades de Spark en PySpark. Es una clase unificada que reemplaza a los antiguos:

- `SparkContext` (para RDDs)
- `SQLContext` (para DataFrames/Datasets)
- `HiveContext` (para operaciones con Hive)

Proporciona una interfaz única para:

- Crear DataFrames
- Registrar DataFrames como tablas
- Ejecutar consultas SQL
- Configurar opciones de Spark
- Acceder a las funcionalidades de Spark SQL

### Creación de una SparkSession en PySpark

#### Forma básica:

```python
from pyspark.sql import SparkSession

# Crear una SparkSession
spark = SparkSession.builder \
    .appName("MiAplicacionSpark") \
    .getOrCreate()

# Verificar la creación
print(spark)
```

### Con configuración adicional:

```python
spark = SparkSession.builder \
    .appName("AnalisisDeDatos") \
    .master("local[4]")  # Usar 4 núcleos locales \
    .config("spark.executor.memory", "4g") \
    .config("spark.driver.memory", "2g") \
    .enableHiveSupport() \  # Para soporte de Hive
    .getOrCreate()
```

### En un entorno de producción (típicamente en un cluster):

```python
spark = SparkSession.builder \
    .appName("ProcesamientoBatch") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
```

## Características importantes:

1. **Singleton**: Normalmente solo hay una SparkSession por aplicación JVM.

2. **Métodos útiles**:
   ```python
   spark.version  # Versión de Spark
   spark.catalog  # Para manejar metadatos
   spark.read  # Para leer datos
   spark.sql("SELECT 1")  # Ejecutar consultas SQL
   spark.stop()  # Detener la sesión
   ```

3. **Entornos especiales**:
   - Jupyter Notebooks: SparkSession puede estar pre-creada como `spark`
   - Databricks: Similar a Jupyter, ya existe una sesión configurada

## Buenas prácticas:

- Usar `getOrCreate()` en lugar de `create()` para evitar múltiples sesiones
- Cerrar la sesión con `spark.stop()` cuando ya no sea necesaria
- Configurar adecuadamente los recursos según el entorno (local vs cluster)

La SparkSession es fundamental para cualquier aplicación PySpark, ya que proporciona todas las herramientas necesarias para trabajar con datos distribuidos.




