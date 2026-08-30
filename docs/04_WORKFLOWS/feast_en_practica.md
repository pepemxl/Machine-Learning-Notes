# Feast en la Práctica

Los conceptos están en [Feast](feast.md). Esta página muestra las dos operaciones que justifican
la herramienta, ejecutadas sobre un repositorio real, y cómo encaja en producción.

## El join point-in-time

Este es el núcleo. Partimos de un histórico donde el `score_riesgo` de cada cliente **cambia con
el tiempo**:

```text
 cliente_id event_timestamp  score_riesgo  ingresos_medios
          1      2026-01-01          0.21           1000.0
          1      2026-01-11          0.51           1500.0
          1      2026-01-21          0.91           2000.0
          2      2026-01-01          0.22           2000.0
          2      2026-01-11          0.52           3000.0
          2      2026-01-21          0.92           4000.0
```

Y de un conjunto de etiquetas donde **cada observación ocurrió en un momento distinto**:

```python
import datetime as dt

import pandas as pd
from feast import FeatureStore

store = FeatureStore(repo_path=".")

entity_df = pd.DataFrame({
    "cliente_id": [1, 1, 1, 2, 2],
    "event_timestamp": [
        dt.datetime(2026, 1, 5),
        dt.datetime(2026, 1, 15),
        dt.datetime(2026, 1, 25),
        dt.datetime(2026, 1, 5),
        dt.datetime(2026, 1, 25),
    ],
    "impago": [0, 1, 0, 1, 0],
})

training = store.get_historical_features(
    entity_df=entity_df,
    features=["clientes_stats:score_riesgo", "clientes_stats:ingresos_medios"],
).to_df()
```

El resultado real:

```text
 cliente_id           event_timestamp  impago  score_riesgo  ingresos_medios
          1 2026-01-05 00:00:00+00:00       0          0.21           1000.0
          1 2026-01-15 00:00:00+00:00       1          0.51           1500.0
          1 2026-01-25 00:00:00+00:00       0          0.91           2000.0
          2 2026-01-05 00:00:00+00:00       1          0.22           2000.0
          2 2026-01-25 00:00:00+00:00       0          0.92           4000.0
```

Léase con atención la columna `score_riesgo` del cliente 1: **0.21, 0.51, 0.91**. Cada fila
recibió el valor vigente **en su propia fecha**, no el último conocido.

Un `JOIN` por `cliente_id` habría puesto 0.91 en las tres filas, incluida la del 5 de enero
—usando un score calculado dieciséis días **después** del hecho que se quiere predecir—. Ese
modelo daría métricas excelentes en validación y fallaría en producción.

**Feast hace este join correctamente por defecto, y ese es el motivo principal para adoptarlo.**

## Materializar y servir

En entrenamiento interesa el valor histórico; en producción, el **último** valor y con latencia
baja. Para eso se copian los datos del offline store al online store:

```bash
feast materialize 2026-01-01T00:00:00 2026-02-01T00:00:00
```

```text
Materializing 1 feature views from 2026-01-01 to 2026-02-01 into the sqlite online store.
clientes_stats:
```

En operación se usa la variante incremental, que arranca donde terminó la anterior:

```bash
feast materialize-incremental $(date -u +"%Y-%m-%dT%H:%M:%S")
```

Y ya se pueden pedir features para inferencia:

```python
respuesta = store.get_online_features(
    features=["clientes_stats:score_riesgo", "clientes_stats:ingresos_medios"],
    entity_rows=[{"cliente_id": 1}, {"cliente_id": 2}],
).to_dict()
```

```text
{'cliente_id': [1, 2],
 'score_riesgo': [0.91, 0.92],
 'ingresos_medios': [2000.0, 4000.0]}
```

Aquí sí devuelve los **valores más recientes** —0.91 y 0.92—, que es lo correcto al servir: en el
momento de predecir quieres el estado actual del cliente.

Esa es la asimetría que hay que tener clara:

| Operación | Devuelve | Para |
|---|---|---|
| `get_historical_features` | El valor **vigente en cada timestamp** | Entrenar sin fuga |
| `get_online_features` | El **último** valor | Predecir en producción |

Y en producción conviene pedir por **feature service**, no por lista de features:

```python
servicio = store.get_feature_service("scoring_v1")
respuesta = store.get_online_features(
    features=servicio, entity_rows=[{"cliente_id": 1}]
).to_dict()
```

Así el modelo depende de un contrato con nombre y versión, no de una lista que alguien puede
cambiar sin darse cuenta.

!!! note "Sobre la latencia"
    Sobre SQLite local, `get_online_features` tarda **0.13 ms** de media en caliente, frente a
    ~138 ms en la primera llamada por la inicialización del store. No son cifras representativas
    de producción: en un despliegue real el online store es Redis o DynamoDB, con la red de por
    medio. Lo transferible es que **hay que calentar el store** antes de medir, y que el coste de
    la primera llamada no es despreciable en un servicio que arranca en frío.

## Despliegue

```bash
feast serve                  # servidor REST de features online
feast ui                     # interfaz web para explorar el registro
```

Lo habitual, sin embargo, es **embeber el `FeatureStore` en el servicio de inferencia**: se
instancia una vez al arrancar y se consulta en cada petición. Encaja bien con
[Ray Serve](ray_bibliotecas_ia.md#ray-serve), donde el constructor del *deployment* es el sitio
natural para crearlo, y con un modelo cargado desde
[MLflow](mlflow_en_practica.md#model-registry):

```python
class Scoring:
    def __init__(self):
        self.store = FeatureStore(repo_path="/app/feature_repo")
        self.modelo = mlflow.pyfunc.load_model("models:/riesgo-credito@champion")
        self.servicio = self.store.get_feature_service("scoring_v1")

    async def __call__(self, request):
        datos = await request.json()
        f = self.store.get_online_features(
            features=self.servicio,
            entity_rows=[{"cliente_id": datos["cliente_id"]}],
        ).to_dict()
        ...
```

En producción, `feast apply` y `feast materialize-incremental` se ejecutan desde el orquestador
—Airflow o similar—, igual que el resto de pipelines.

## Cuándo usar Feast

Compensa cuando se cumplen **varias** de estas condiciones:

- Hay **varios modelos** que comparten features. Si solo hay uno, el coste operativo no se
  amortiza.
- Los modelos sirven **en línea** y hay riesgo real de divergencia entre entrenamiento y
  producción.
- Las features tienen **historia** y los conjuntos de entrenamiento se construyen con etiquetas
  fechadas. Sin esto, el join point-in-time —su mayor virtud— no aporta nada.
- Varios equipos necesitan **descubrir y reutilizar** features ajenas.

No compensa cuando:

- El modelo es **batch** y se reentrena entero cada vez. Una consulta SQL bien escrita basta.
- Las features son **estáticas** y no cambian con el tiempo: no hay fuga temporal que evitar.
- El equipo es pequeño y hay un solo modelo. Feast añade un registro, dos almacenes y un proceso
  de materialización que hay que operar.

## Limitaciones

- **No calcula features.** Es un error de expectativa muy común. Las transformaciones y
  agregaciones las hace tu pipeline —[Spark](../00_DATA/spark/pyspark.md),
  [Kedro](kedro.md), dbt— y Feast sirve el resultado. Las *on-demand feature views* permiten
  transformaciones ligeras en el momento de la consulta, pero no sustituyen a un pipeline.
- **La materialización es un proceso más que operar.** Si falla, el online store sirve datos
  rancios en silencio. El TTL mitiga esto, pero hay que vigilarlo.
- **No versiona los datos.** Ver [DVC](dvc.md).
- **No hay monitoreo de deriva incluido.** Detectar que la distribución de una feature cambió es
  responsabilidad de otro sistema.

## Ver también

- [Feast](feast.md) — conceptos y definición del repositorio.
- [Feature stores](feature_stores.md)
- [MLflow en la práctica](mlflow_en_practica.md) · [Ray Serve](ray_bibliotecas_ia.md#ray-serve)
- [OpenLineage](openlineage.md) — trazar de dónde salen las features.

## Referencias

- [Documentación de Feast](https://docs.feast.dev/)
- [feast-dev/feast](https://github.com/feast-dev/feast)
