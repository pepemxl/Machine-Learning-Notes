# Ejemplos de PySpark y SQL



```python linenums="1" title="Example"
df \
.groupby(['column1', 'column2']) \
.count() \
.where('count > 1') \
.sort('count', ascending=False) \
.show()
```
```python linenums="1" title="Example"
df.dropDuplicates(['id', 'name']).show()

```
```python linenums="1" title="Example"
from pyspark.sql.functions import udf
from pyspark.sql.types import IntegerType

def my_func(x):
    return x + 1

my_udf = udf(my_func, IntegerType())
df = df.withColumn('new_column', my_udf(df['column']))
```
```python linenums="1" title="Example"
text_file=sc.textFile(" ")
counts=text_file.flatMap(lambda line:line.split(" "))
                                  .map(lambda word: (word,1))
                                  .reduceByKey(lambda a,b=a+b)
counts.saveAsTextFile("")
```

```bash
Input
Col 1 Col 2 Col 3
a aa 1
a aa 2
b bb 5
b bb 3
b bb 4

Escribe el código PySpark que produzca la siguiente salida

Col 1 Col 2 Col 3
a aa [1,2]
b bb [5,3,4]
```

```python linenums="1" title="Example"
from pyspark.sql.functions import collect_list

# Datos de entrada como lista de tuplas
data = [
    ("a", "aa", 1),
    ("a", "aa", 2),
    ("b", "bb", 5),
    ("b", "bb", 3),
    ("b", "bb", 4)
]

# Crear un DataFrame con los datos de entrada
input_df = spark.createDataFrame(data, ["Col 1", "Col 2", "Col 3"])

# Agrupar por "Col 1" y "Col 2", y agregar "Col 3" en una lista
output_df = input_df.groupBy("Col 1", "Col 2").agg(
    collect_list("Col 3").alias("Col 3")
)

# Mostrar el DataFrame resultante
output_df.show(truncate=False)
```

```bash
I have the following as input
Input
Name Sport
Alice Badminton, Tennis
Greg Cricket, Baseball
Julie Swimming, Basket ball
Alan Tennis, Swimming
Xian Badminton, Baseball

Escribe el código PySpark que produzca la siguiente salida
Output
Name Sport
Alice Badminton
Xian Badminton
Alice Tennis
Alan Tennis
Greg Baseball
Xian Baseball
Julie Swimming
Alan Swimming
Greg Cricket
Julie Basket ball
```


```python linenums="1" title="Example"
from pyspark.sql.functions import col, split, explode, trim

# Datos de entrada como lista de tuplas
data = [
    ("Alice", "Badminton, Tennis"),
    ("Greg", "Cricket, Baseball"),
    ("Julie", "Swimming, Basket ball"),
    ("Alan", "Tennis, Swimming"),
    ("Xian", "Badminton, Baseball")
]

# Crear un DataFrame con los datos de entrada
input_df = spark.createDataFrame(data, ["Name", "Sport"])

# Un solo `withColumn` para dividir, expandir y limpiar la columna `Sport`
output_df = input_df.withColumn(
    "Sport",
    trim(explode(split(col("Sport"), ",")))  # Chain split, explode, and trim
)

# Mostrar el DataFrame resultante
output_df.show()
```


```bash
Entrada —
id
6
7
8

Salida —
id
6
7
7
8
8
8
```


```python linenums="1" title="Example"
df = spark.createDataFrame([(6,), (7,), (8,)], ["id"])

output_df = df.selectExpr("explode(sequence(6, id)) as id")
```

```python linenums="1" title="Example"

```

```python linenums="1" title="Example"

```

```python linenums="1" title="Example"

```

### Consulta SQL: clientes que compraron en 3 días consecutivos

```python linenums="1" title="Example"
WITH SalesData AS (
 SELECT 
 customer_id, 
 sale_date, 
 LAG(sale_date, 1) OVER (PARTITION BY customer_id ORDER BY sale_date) AS prev_day_1,
 LAG(sale_date, 2) OVER (PARTITION BY customer_id ORDER BY sale_date) AS prev_day_2
 FROM sales_table
)
SELECT DISTINCT customer_id
FROM SalesData
WHERE sale_date = DATEADD(DAY, 1, prev_day_1) 
AND prev_day_1 = DATEADD(DAY, 1, prev_day_2);
```

### Consulta: proyectos con mayor ratio de presupuesto por empleado, a partir de dos tablas relacionadas (`projects` y `employees`)

```python linenums="1" title="Example"
WITH ProjectEmployeeCount AS (
    SELECT 
        p.project_id,
        p.budget,
        COUNT(e.employee_id) AS employee_count
    FROM 
        projects p
    LEFT JOIN 
        employees e
    ON 
        p.project_id = e.project_id
    GROUP BY 
        p.project_id, p.budget
),
BudgetPerEmployeeRatio AS (
    SELECT 
        project_id,
        budget,
        employee_count,
        CASE 
            WHEN employee_count = 0 THEN NULL -- Handle division by zero
            ELSE budget / employee_count 
        END AS budget_per_employee_ratio
    FROM 
        ProjectEmployeeCount
)
SELECT 
    project_id,
    budget,
    employee_count,
    budget_per_employee_ratio
FROM 
    BudgetPerEmployeeRatio
WHERE 
    budget_per_employee_ratio = (
        SELECT 
            MAX(budget_per_employee_ratio)
        FROM 
            BudgetPerEmployeeRatio
        WHERE 
            budget_per_employee_ratio IS NOT NULL -- Exclude projects with no employees
    );
```


### Los 3 pedidos más recientes de cada cliente

```python linenums="1" title="Example"
WITH RankedOrders AS (
  SELECT
    customer_id,
    order_id,
    order_date,
    ROW_NUMBER() OVER (
      PARTITION BY customer_id
      ORDER BY order_date DESC, order_id DESC -- Tiebreaker for deterministic ordering
    ) AS order_rank
  FROM
    orders
)
SELECT
  customer_id,
  order_id,
  order_date
FROM
  RankedOrders
WHERE
  order_rank <= 3
ORDER BY
  customer_id,
  order_rank;
```




### Media móvil de ventas a 30 días por producto

```python linenums="1" title="Example"
WITH DailySales AS (
  -- Aggregate sales to handle multiple entries per day
  SELECT
    product_id,
    sale_date,
    SUM(sale_amount) AS daily_total  -- Compress same-day sales
  FROM
    sales
  GROUP BY
    product_id, sale_date
)
SELECT
  product_id,
  sale_date,
  daily_total,
  AVG(daily_total) OVER (
    PARTITION BY product_id
    ORDER BY sale_date
    RANGE BETWEEN INTERVAL '29' DAY PRECEDING AND CURRENT ROW  -- True 30-day window
  ) AS moving_avg_30d
FROM
  DailySales
ORDER BY
  product_id, sale_date
```
