# MLflow en la Práctica

El seguimiento de experimentos está en [MLflow](mlflow.md). Esta página cubre lo que viene
después: empaquetar el modelo, versionarlo, promoverlo a producción y encajar MLflow con el
resto de herramientas.

## MLflow Models

Cuando registras un modelo con `log_model`, MLflow no guarda solo los pesos: crea un **directorio
autodescriptivo** con un archivo `MLmodel` que declara cómo cargarlo y qué dependencias necesita.

```python
info = mlflow.sklearn.log_model(modelo, name="modelo", input_example=X_te[:3])
print(info.model_uri)     # models:/m-1496054ca6ef4f40b418a0e54320cfb8
```

### Flavors

Un mismo modelo se guarda en varios **flavors** —formas de cargarlo— a la vez. El más importante
es `python_function`: la interfaz genérica que cualquier herramienta puede usar sin saber con qué
framework se entrenó.

```python
import mlflow

modelo = mlflow.pyfunc.load_model(info.model_uri)
modelo.predict(X_te[:5])
```

Ese es el punto: quien sirve el modelo **no necesita saber si es scikit-learn, PyTorch o XGBoost**.
Hay flavors para sklearn, pytorch, tensorflow, xgboost, lightgbm, spark, [onnx](onnx.md),
transformers y más.

### Firma del modelo

La **firma** describe los tipos y formas de entrada y salida. Se infiere del `input_example` y se
guarda en el `MLmodel`. En producción, MLflow valida las peticiones contra ella y falla con un
error claro en vez de producir predicciones silenciosamente erróneas.

Registrar el modelo sin `input_example` es el atajo que más caro sale después.

## Model Registry

El registro es donde los modelos dejan de ser artefactos de experimentos y pasan a ser
**versiones gobernadas**.

```python
mlflow.sklearn.log_model(
    modelo,
    name="modelo",
    registered_model_name="riesgo-credito",
    input_example=X_te[:3],
)
```

Cada vez que se registra bajo el mismo nombre se crea una versión nueva:

```python
c = mlflow.MlflowClient()
versiones = c.search_model_versions("name='riesgo-credito'")
# [(2, 'dc4aec63'), (1, 'd40d76f0')]
```

Cada versión conserva el `run_id` que la produjo, así que desde el modelo en producción siempre se
puede llegar a los parámetros, las métricas y el código que lo generaron.

### Alias, no stages

```python
c.set_registered_model_alias("riesgo-credito", "champion", version=2)

modelo = mlflow.pyfunc.load_model("models:/riesgo-credito@champion")
modelo.predict(X_te[:5])          # [1, 1, 1, 0, 0]
```

El código de producción referencia **`@champion`**, no un número de versión. Promover un modelo
nuevo es mover el alias; volver atrás es moverlo de vuelta. No hay que desplegar nada.

!!! warning "Los *stages* están obsoletos"
    Mucha documentación antigua usa `transition_model_version_stage()` con etapas
    `Staging`/`Production`. Sigue funcionando, pero emite:

    ```text
    ``transition_model_version_stage`` is deprecated since 2.9.0.
    Model registry stages will be removed in a future major release.
    ```

    Usa **alias**. Son más flexibles: puedes tener `champion`, `challenger` y `baseline` a la vez,
    y no estás limitado a un conjunto fijo de nombres.

## Despliegue

Con el modelo en el registro hay varias salidas:

```bash
# Servidor REST local
mlflow models serve -m "models:/riesgo-credito@champion" --port 5001

# Imagen Docker
mlflow models build-docker -m "models:/riesgo-credito@champion" -n riesgo-api
```

O cargarlo dentro de tu propio servicio, que es lo más habitual:

```python
modelo = mlflow.pyfunc.load_model("models:/riesgo-credito@champion")
```

Esto encaja bien con [Ray Serve](ray_bibliotecas_ia.md#ray-serve): el *deployment* carga el modelo
por alias en su constructor, una vez por réplica.

Para inferencia de alto rendimiento, la ruta suele ser exportar a
[ONNX](onnx.md) y servir con [ONNX Runtime](onnx_runtime.md); MLflow tiene un flavor `onnx` para
guardar el modelo ya convertido.

## MLflow frente a DVC

Ambos registran experimentos, y la pregunta de cuál usar aparece siempre. Resuelven **mitades
distintas** del problema:

| | **MLflow** | **DVC** |
|---|---|---|
| Registro | Servidor con base de datos | Archivos en el repositorio Git |
| Experimentos | Runs con métricas y artefactos | Commits ligeros, `dvc exp` |
| Versionado de datos | No | **Sí**, es su núcleo |
| Reproducción | No reejecuta nada | `dvc repro` incremental por hashes |
| Registro de modelos | **Sí**, con alias y versiones | No |
| Interfaz | Web, comparación visual | CLI, `dvc exp show` |
| Colaboración | Servidor central compartido | A través de Git |

La combinación habitual es usar **DVC para versionar datos y reproducir el pipeline**, y
**MLflow para registrar métricas y gobernar los modelos**. Un stage de DVC entrena y, dentro,
el código llama a `mlflow.log_metric`.

Ver [DVC](dvc.md) y [pipelines y experimentos con DVC](dvc_pipelines_y_experimentos.md).

## Integración con Kedro

[Kedro](kedro.md) no trae MLflow de serie, pero encaja de dos formas:

- Con el plugin de la comunidad **`kedro-mlflow`**, que añade datasets de MLflow al catálogo y
  registra parámetros automáticamente.
- Con un [hook](kedro_en_produccion.md#hooks) propio, que abre un run en `before_pipeline_run` y
  lo cierra al terminar.

Es el mismo punto de extensión donde se engancha [OpenLineage](openlineage_en_practica.md#con-kedro).

## Buenas prácticas

- **Registra la versión de los datos, no solo los hiperparámetros.** Un run sin saber sobre qué
  datos corrió no es reproducible. Si usas DVC, registra el hash del `.dvc`; si no, al menos la
  ruta y la fecha.
- **Etiqueta con el commit de git.** `mlflow.set_tag("git_sha", sha)` cierra el círculo entre
  resultado y código.
- **Separa métricas de entrenamiento y de validación** en el nombre. El autologging solo registra
  las primeras, y confundirlas lleva a celebrar modelos sobreajustados.
- **Un experimento por objetivo**, no por persona ni por día. Los experimentos existen para
  comparar dentro de ellos.
- **Nunca metas credenciales en parámetros o tags.** Quedan en la base de datos del servidor y son
  visibles para todo el equipo.
- **No registres todos los modelos en el registro.** El registro es para candidatos a producción;
  los cientos de runs de un barrido se quedan en el tracking.

## Limitaciones

- **No orquesta ni programa.** Igual que [Kedro](kedro.md#lo-que-kedro-no-es) y
  [DVC](dvc_pipelines_y_experimentos.md#que-no-hace-dvc), hace falta Airflow o similar.
- **No versiona datos.** Puedes subir un dataset como artefacto, pero es un mal sustituto de DVC.
- **El servidor es estado que hay que operar.** En equipo necesita una base de datos y
  almacenamiento de artefactos con copias de seguridad; si se pierde, se pierde el historial.
- **El autologging captura mucho ruido.** Diecinueve parámetros por modelo llenan la tabla de
  comparación de columnas irrelevantes.

## Ver también

- [MLflow](mlflow.md) — seguimiento de experimentos.
- [DVC](dvc.md) · [ONNX](onnx.md) · [Ray Serve](ray_bibliotecas_ia.md#ray-serve)
- [Feast en la práctica](feast_en_practica.md) — de dónde salen las features en inferencia.
- [Proyectos generales de ML](../09_SYSTEMS/proyectos_generales_de_ml.md)

## Referencias

- [Documentación de MLflow](https://mlflow.org/docs/latest/)
- [Model Registry](https://mlflow.org/docs/latest/ml/model-registry/)
- [mlflow/mlflow](https://github.com/mlflow/mlflow)
