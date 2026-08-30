# Kedro

**Kedro** es un framework de Python para estructurar proyectos de ciencia de datos. No ejecuta
nada en paralelo ni programa tareas: lo que aporta es **disciplina de ingeniería** sobre código
que casi siempre nace como un notebook.

Fue creado por QuantumBlack (McKinsey) y hoy lo aloja la **Linux Foundation** (LF AI & Data),
con licencia Apache 2.0.

## El problema que resuelve

Un proyecto de ML típico empieza en un notebook y acumula, sin darse cuenta:

- **Rutas embebidas en el código.** `pd.read_csv("/home/ana/datos/v3_final.csv")` funciona en un
  portátil y en ningún otro sitio.
- **Orden de ejecución implícito.** Las celdas hay que correrlas en un orden concreto que solo
  conoce quien lo escribió.
- **Configuración mezclada con lógica.** El `test_size`, la ruta del bucket y la contraseña de la
  base de datos conviven con el `fit()`.
- **Nada testeable.** No hay funciones: hay celdas.

Kedro ataca esto con una idea central: **separar el qué del dónde**. Las funciones dicen qué
cálculo hacer; un catálogo en YAML dice de dónde salen y a dónde van los datos. La misma función
lee de un CSV local en desarrollo y de S3 en producción, sin cambiar una línea.

## Los tres conceptos

### Node

Un **node** envuelve una función de Python **normal y pura**, y le pone nombre a sus entradas y
salidas. La función no sabe nada de Kedro:

```python
# src/demo/pipelines/credito/nodes.py
import pandas as pd


def limpiar(clientes: pd.DataFrame) -> pd.DataFrame:
    """Imputa los ingresos faltantes con la mediana."""
    df = clientes.copy()
    df["ingresos"] = df["ingresos"].fillna(df["ingresos"].median())
    return df


def construir_features(clientes: pd.DataFrame) -> pd.DataFrame:
    df = clientes.copy()
    df["ingresos_por_anio"] = df["ingresos"] / (df["antiguedad"] + 1)
    df["es_joven"] = (df["edad"] < 30).astype(int)
    return df
```

Que las funciones no importen Kedro no es casualidad: es lo que permite **testearlas con pytest
como funciones normales**, sin levantar el framework.

### Pipeline

Un **pipeline** es una lista de nodes. Lo importante es que **no declaras el orden**: Kedro
deduce el DAG haciendo coincidir los nombres de salida de unos nodes con los de entrada de otros.

```python
# src/demo/pipelines/credito/pipeline.py
from kedro.pipeline import Node, Pipeline

from .nodes import construir_features, entrenar, evaluar, limpiar


def create_pipeline(**kwargs) -> Pipeline:
    return Pipeline(
        [
            Node(func=limpiar,
                 inputs="clientes_crudos",
                 outputs="clientes_limpios",
                 name="limpiar_datos"),
            Node(func=construir_features,
                 inputs="clientes_limpios",
                 outputs="features",
                 name="construir_features"),
            Node(func=entrenar,
                 inputs=["features", "params:modelo"],
                 outputs="entrenamiento",
                 name="entrenar_modelo"),
            Node(func=evaluar,
                 inputs="entrenamiento",
                 outputs="metricas",
                 name="evaluar_modelo"),
        ]
    )
```

`construir_features` se ejecuta después de `limpiar` porque consume `clientes_limpios`, que es lo
que aquella produce. Reordenar la lista no cambia nada. Si creas un ciclo, Kedro lo detecta y
falla antes de ejecutar.

El prefijo **`params:`** es especial: inyecta un bloque del archivo de parámetros como argumento.

### DataCatalog

El **catálogo** es donde vive todo el I/O. Es un YAML que asocia cada nombre lógico usado en el
pipeline con un tipo de dataset y una ubicación:

```yaml
# conf/base/catalog.yml
clientes_crudos:
  type: pandas.CSVDataset
  filepath: data/01_raw/clientes.csv

clientes_limpios:
  type: pandas.ParquetDataset
  filepath: data/02_intermediate/clientes_limpios.parquet

features:
  type: pandas.ParquetDataset
  filepath: data/05_model_input/features.parquet

metricas:
  type: json.JSONDataset
  filepath: data/08_reporting/metricas.json
```

Hay datasets para pandas, Spark, Polars, Parquet, SQL, imágenes, MLflow, Delta y muchos más, en
el paquete `kedro-datasets`. Los `filepath` admiten `s3://`, `gs://` o `abfs://` sin cambiar el
código.

!!! warning "Lo que no está en el catálogo no se guarda"
    Si un nombre aparece en el pipeline pero **no** en `catalog.yml`, Kedro lo trata como un
    `MemoryDataset`: existe solo durante la ejecución y desaparece al terminar.

    En el pipeline de arriba, `entrenamiento` no está declarado. Funciona —pasa del nodo de
    entrenamiento al de evaluación— pero el modelo entrenado **no se persiste en ningún sitio**.
    Es cómodo para resultados intermedios, y una fuente de sorpresas cuando esperabas un
    artefacto en disco.

### Parámetros

```yaml
# conf/base/parameters.yml
modelo:
  test_size: 0.25
  random_state: 42
  max_iter: 500
```

Se inyectan con `params:modelo` y llegan a la función como un diccionario. Ningún número mágico
queda dentro del código.

## Estructura del proyecto

```bash
pip install kedro "kedro-datasets[pandas]"
kedro new --name=demo --tools=none --example=n
```

Genera:

```text
demo/
├── conf/
│   ├── base/               # configuración versionada
│   │   ├── catalog.yml
│   │   └── parameters.yml
│   └── local/              # configuración de la máquina — en .gitignore
│       └── credentials.yml
├── data/                   # capas 01_raw ... 08_reporting
├── notebooks/
├── src/demo/
│   ├── pipelines/
│   ├── pipeline_registry.py
│   └── settings.py
├── pyproject.toml
└── requirements.txt
```

Dos convenciones que importan:

- **`conf/base` frente a `conf/local`.** Lo primero se versiona; lo segundo no, y es donde van
  credenciales y rutas de tu máquina. La separación viene impuesta por la plantilla, no depende
  de que alguien se acuerde.
- **Las capas de `data/`** —`01_raw`, `02_intermediate`, `03_primary`, `04_feature`,
  `05_model_input`, `06_models`, `07_model_output`, `08_reporting`— son solo una convención de
  nombres, pero hacen evidente en qué punto del flujo está cada artefacto. **`01_raw` es
  inmutable**: nunca se sobrescribe.

### Registrar el pipeline

```python
# src/demo/pipeline_registry.py
from kedro.pipeline import Pipeline

from demo.pipelines import credito


def register_pipelines() -> dict[str, Pipeline]:
    credito_pipeline = credito.create_pipeline()
    return {"__default__": credito_pipeline, "credito": credito_pipeline}
```

`__default__` es el que se ejecuta cuando no se especifica ninguno.

## Ejecutar

```bash
kedro run
```

Sobre el pipeline anterior, con 500 filas de datos sintéticos:

```text
Running node: limpiar_datos: limpiar([clientes_crudos]) -> [clientes_limpios]
Running node: construir_features: construir_features([clientes_limpios]) -> [features]
Running node: entrenar_modelo: entrenar([features;params:modelo]) -> [entrenamiento]
Running node: evaluar_modelo: evaluar([entrenamiento]) -> [metricas]
Pipeline execution completed successfully in 0.2 sec.
```

Y los artefactos quedan en su capa:

```text
data/01_raw/clientes.csv
data/02_intermediate/clientes_limpios.parquet
data/05_model_input/features.parquet
data/08_reporting/metricas.json
```

```json
{"accuracy": 0.984, "roc_auc": 0.9888, "n_test": 125}
```

Nótese que `entrenamiento` no aparece: era un `MemoryDataset`.

## Inspeccionar el proyecto

```bash
kedro registry list                  # pipelines registrados
kedro catalog describe-datasets      # que datasets usa cada pipeline y de que tipo
```

`describe-datasets` es especialmente útil porque separa los datasets declarados de los que caen
por defecto en `MemoryDataset`:

```text
credito:
  datasets:
    kedro_datasets.pandas.csv_dataset.CSVDataset:  [clientes_crudos]
    kedro_datasets.pandas.parquet_dataset.ParquetDataset:  [clientes_limpios, features]
    kedro_datasets.json.json_dataset.JSONDataset:  [metricas]
  defaults:
    kedro.io.MemoryDataset:  [entrenamiento]
```

## Lo que Kedro no es

Es la confusión más frecuente: **Kedro no es un orquestador**. No tiene planificador, ni
reintentos, ni alertas, ni interfaz de operación. `kedro run` ejecuta el pipeline una vez, ahí
mismo.

Para programar ejecuciones se despliega sobre [Airflow, Dagster o similares](kedro_en_produccion.md#despliegue-a-orquestadores).
Kedro y Airflow no compiten: **Kedro estructura el código, Airflow decide cuándo corre**.

## Ver también

- [Kedro en producción](kedro_en_produccion.md) — entornos, runners, despliegue y visualización.
- [Sistemas de machine learning](sistemas_de_machine_learning.md)
- [Workflows, máquinas de estado y colas](workflows_maquinas_de_estado_y_colas.md)
- [Feature stores](feature_stores.md)

## Referencias

- [Documentación de Kedro](https://docs.kedro.org/)
- [kedro-org/kedro](https://github.com/kedro-org/kedro)
- [Catálogo de datasets disponibles](https://docs.kedro.org/projects/kedro-datasets/)
