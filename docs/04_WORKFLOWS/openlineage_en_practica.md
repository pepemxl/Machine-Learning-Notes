# OpenLineage en la Práctica

El modelo de eventos está en [OpenLineage](openlineage.md). Esta página cubre lo que hace falta
para que el linaje aparezca solo: qué integraciones existen, dónde se recogen los eventos y qué
se puede hacer con ellos.

## Integraciones

La regla general es que **no escribas eventos a mano** si tu herramienta ya los emite. Las
integraciones extraen el linaje del plan de ejecución real, que es mucho más fiable que cualquier
declaración manual.

| Herramienta | Paquete | Cómo funciona |
|---|---|---|
| **Apache Airflow** | `apache-airflow-providers-openlineage` | Integrado desde Airflow 2.7. Extrae linaje de los operadores soportados |
| **Apache Spark** | `io.openlineage:openlineage-spark` (Maven) | Un *listener* que lee el plan lógico de Spark |
| **dbt** | `openlineage-dbt` | Envuelve la ejecución (`dbt-ol run`) y lee los artefactos que dbt genera |
| **Flink, Dagster, Trino, Great Expectations** | varios | Integraciones mantenidas en el repositorio del proyecto |
| **Cualquier cosa** | `openlineage-python`, `openlineage-java` | Emisión manual con el cliente |

### Airflow

```bash
pip install apache-airflow-providers-openlineage
```

```ini
# airflow.cfg
[openlineage]
transport = {"type": "http", "url": "http://marquez:5000"}
namespace = produccion
```

No hace falta tocar los DAG. El proveedor engancha en el ciclo de vida de las tareas y usa el
facet `parent` para anidar cada tarea bajo su DAG, de modo que el linaje se ve tanto al nivel del
DAG completo como al de tarea individual.

### Spark

```python
spark = (SparkSession.builder
    .config("spark.jars.packages", "io.openlineage:openlineage-spark_2.12:1.8.0")
    .config("spark.extraListeners", "io.openlineage.spark.agent.OpenLineageSparkListener")
    .config("spark.openlineage.transport.type", "http")
    .config("spark.openlineage.transport.url", "http://marquez:5000")
    .config("spark.openlineage.namespace", "produccion")
    .getOrCreate())
```

Esta es la integración más valiosa de todas, porque el listener lee el **plan lógico** de Spark.
Eso significa que obtiene el linaje —incluido el de columnas— de cualquier DataFrame o consulta
SQL, sin que nadie declare nada. Ver [PySpark](../00_DATA/spark/pyspark.md).

### dbt

```bash
pip install openlineage-dbt
dbt-ol run
```

`dbt-ol` envuelve al comando de dbt y traduce sus artefactos (`manifest.json`, `run_results.json`)
a eventos OpenLineage. Como dbt ya conoce el grafo de modelos, el linaje sale completo y con
detalle de columnas.

## Marquez: recoger y explorar

Los eventos hay que enviarlos a algún sitio. **Marquez** es la implementación de referencia del
API de OpenLineage: un servidor de metadatos con base de datos y una interfaz web para navegar el
grafo.

```bash
git clone https://github.com/MarquezProject/marquez
cd marquez && ./docker/up.sh
```

Levanta la API en el puerto **5000** y la interfaz en el **3000**. A partir de ahí, cualquier
productor apunta su transporte HTTP a `http://localhost:5000` y el grafo se va construyendo solo.

No es la única opción: **DataHub**, **Atlan**, **Microsoft Purview**, **Google Dataplex** y
**Astronomer** consumen OpenLineage. Esa es justamente la ventaja de emitir en un estándar
abierto: cambiar de catálogo no obliga a reinstrumentar los pipelines.

## Qué se puede responder con el linaje

Una vez el grafo existe, resuelve cuatro clases de pregunta que antes costaban horas:

**Análisis de impacto** (hacia adelante). *"Vamos a borrar esta columna, ¿qué se rompe?"* Se
recorre el grafo desde el dataset hacia sus consumidores.

**Análisis de causa raíz** (hacia atrás). *"Este número está mal, ¿de dónde viene?"* Se recorre en
sentido contrario hasta las fuentes.

**Cumplimiento normativa.** *"¿A dónde ha llegado esta columna con datos personales?"* Es donde el
facet `columnLineage` resulta insustituible: el linaje a nivel de tabla no basta, porque diría que
un dataset entero está contaminado cuando quizá solo lo está un campo. Enlaza con lo que se
describe en [descubrimiento de datos](descubrimiento_de_datos.md).

**Detección de datos obsoletos.** Comparando el `nominalTime` de los runs con la hora real se
identifica qué informes se construyeron con datos que no habían llegado.

## Linaje en proyectos de ML

En un pipeline de machine learning el linaje responde a la pregunta que más cuesta contestar seis
meses después: **"¿con qué datos exactamente se entrenó este modelo?"**

Conviene registrar como datasets no solo las tablas, sino también:

- El **conjunto de entrenamiento** concreto, con su versión.
- El **modelo** resultante como dataset de salida.
- Las **métricas** de evaluación.

Así, el modelo en producción queda conectado hacia atrás con las features, las tablas crudas y el
commit del código que lo generó, vía el facet `sourceCodeLocation`. Es lo que permite reproducir
un entrenamiento o auditar una decisión.

### Con Kedro

**No existe una integración oficial de OpenLineage para Kedro.** La vía natural es un
[hook](kedro_en_produccion.md#hooks): `before_node_run` y `after_node_run` dan exactamente los
puntos donde emitir `START` y `COMPLETE`, y el catálogo ya sabe qué datasets entran y salen de
cada nodo.

```python
# src/demo/hooks.py — esquema de la idea
import uuid

from kedro.framework.hooks import hook_impl


class HooksDeLinaje:
    @hook_impl
    def before_node_run(self, node, inputs):
        self._runs[node.name] = str(uuid.uuid4())
        # emitir RunEvent(START) con node.inputs como InputDataset

    @hook_impl
    def after_node_run(self, node, outputs):
        # emitir RunEvent(COMPLETE) con node.outputs como OutputDataset
        ...
```

El trabajo real está en traducir los nombres del catálogo de Kedro a las
[convenciones de nombres](openlineage.md#convenciones-de-nombres) de OpenLineage. Si no se hace
bien, el linaje de Kedro no encajará con el que emitan Spark o Airflow.

## Errores frecuentes

- **Nombrar los datasets de forma inconsistente** entre herramientas. Es el fallo número uno: el
  grafo queda partido en trozos que no se conectan, y el linaje resultante es inservible.
  Acuerda las convenciones **antes** de instrumentar.
- **Emitir solo el evento `COMPLETE`.** Sin `START` no hay duración, y los runs que fallan no
  dejan rastro: precisamente los que más interesan.
- **Olvidar `FAIL`.** Un run que aborta sin emitir nada aparece como eternamente en ejecución.
- **Creer que el linaje sustituye a la documentación.** Dice qué pasó, no *por qué*. El facet
  `documentation` y el `ownership` son los que aportan esa mitad.
- **Instrumentarlo todo desde el principio.** Empieza por los pipelines críticos, comprueba que el
  grafo tiene sentido, y extiéndelo después.

## Ver también

- [OpenLineage](openlineage.md) — el modelo de eventos y los facets.
- [Descubrimiento de datos](descubrimiento_de_datos.md)
- [Kedro en producción](kedro_en_produccion.md) — los hooks donde engancharlo.
- [Sistemas de machine learning](sistemas_de_machine_learning.md)

## Referencias

- [Integraciones de OpenLineage](https://openlineage.io/docs/)
- [Marquez](https://marquezproject.ai/) · [MarquezProject/marquez](https://github.com/MarquezProject/marquez)
- [apache-airflow-providers-openlineage](https://pypi.org/project/apache-airflow-providers-openlineage/)
