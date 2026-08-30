# MLflow: Seguimiento de Experimentos

**MLflow** es una plataforma abierta para gestionar el ciclo de vida del machine learning. Su
componente más usado, y el motivo por el que la mayoría llega a ella, es el **seguimiento de
experimentos**: registrar de forma sistemática qué se probó, con qué parámetros y qué resultado
dio.

Nació en Databricks y hoy es un proyecto de la Linux Foundation, con licencia Apache 2.0.

## El problema

Entrenar un modelo es un proceso de prueba y error. Se cambian hiperparámetros, features y
algoritmos decenas de veces, y sin registro sistemático acaba pasando siempre lo mismo:

- *"Este modelo daba 0.91 la semana pasada. ¿Qué le cambié?"*
- Una hoja de cálculo con resultados que alguien dejó de actualizar.
- Un modelo en producción del que nadie sabe con qué configuración se entrenó.
- Dos personas del equipo repitiendo el mismo experimento sin saberlo.

MLflow resuelve esto haciendo que **el registro sea una línea de código**, no una tarea aparte que
hay que acordarse de hacer.

## Los cuatro componentes

| Componente | Para qué |
|---|---|
| **Tracking** | Registrar parámetros, métricas, artefactos y etiquetas de cada ejecución |
| **Models** | Empaquetar el modelo en un formato estándar con sus dependencias |
| **Model Registry** | Versionar los modelos y marcar cuál está en producción |
| **Projects** | Empaquetar el código para que sea reejecutable |

Esta página cubre Tracking; el resto está en
[MLflow en la práctica](mlflow_en_practica.md).

## Conceptos

- **Experiment** — una agrupación de ejecuciones que persiguen el mismo objetivo, por ejemplo
  `riesgo-credito`.
- **Run** — una ejecución concreta. Tiene un identificador, parámetros, métricas, artefactos,
  etiquetas y un estado.
- **Parámetros** — las entradas: hiperparámetros, versión del dataset. Se registran una vez.
- **Métricas** — las salidas numéricas. **Admiten varios valores en el tiempo**, lo que permite
  registrar la pérdida por época y obtener una curva.
- **Artefactos** — cualquier archivo: el modelo, gráficas, matrices de confusión, informes.
- **Tags** — metadatos libres para filtrar: equipo, rama de git, tipo de ejecución.

La distinción parámetro/métrica importa: un parámetro es lo que **decides**, una métrica es lo que
**obtienes**.

## Configurar el backend

```bash
pip install mlflow
```

Lo primero es decidir dónde se guardan los datos:

```python
import mlflow

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("riesgo-credito")
```

!!! warning "El backend de ficheros ya no es la opción por defecto viable"
    Casi todos los tutoriales empiezan sin configurar nada, lo que dejaba los datos en un
    directorio `./mlruns`. **Desde MLflow 3, ese backend está en modo mantenimiento y lanza una
    excepción**:

    ```text
    MlflowException: The filesystem tracking backend (e.g., './mlruns') is in
    maintenance mode and will not receive further updates. Please migrate to a
    database backend (e.g., 'sqlite:///mlflow.db')...
    ```

    Usa un backend de base de datos —`sqlite:///mlflow.db` en local— o, si de verdad necesitas el
    de ficheros, la variable de entorno `MLFLOW_ALLOW_FILE_STORE=true`. Para migrar datos
    existentes hay una herramienta: `mlflow migrate-filestore`.

## Registrar una ejecución

```python
import mlflow
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, roc_auc_score

mlflow.set_tracking_uri("sqlite:///mlflow.db")
mlflow.set_experiment("riesgo-credito")

with mlflow.start_run(run_name="rf-depth5"):
    params = {"algoritmo": "random_forest", "n_estimators": 50, "max_depth": 5}
    mlflow.log_params(params)
    mlflow.set_tag("equipo", "riesgo")

    modelo = RandomForestClassifier(n_estimators=50, max_depth=5, random_state=42)
    modelo.fit(X_tr, y_tr)

    pred = modelo.predict(X_te)
    mlflow.log_metric("accuracy", accuracy_score(y_te, pred))
    mlflow.log_metric("roc_auc", roc_auc_score(y_te, modelo.predict_proba(X_te)[:, 1]))

    mlflow.sklearn.log_model(modelo, name="modelo", input_example=X_te[:3])
```

El gestor de contexto `start_run()` se encarga de cerrar la ejecución y de marcarla como fallida
si salta una excepción.

El `input_example` no es opcional en la práctica: de él MLflow infiere la **firma** del modelo
—tipos y formas de entrada y salida— que después sirve para validar las peticiones en producción.

## Consultar los resultados

La API devuelve las ejecuciones como un `DataFrame`, así que comparar es trivial:

```python
df = mlflow.search_runs(
    experiment_names=["riesgo-credito"],
    order_by=["metrics.roc_auc DESC"],
)
print(df[["tags.mlflow.runName", "params.algoritmo",
          "metrics.accuracy", "metrics.roc_auc"]])
```

Sobre tres ejecuciones reales del ejemplo:

```text
tags.mlflow.runName    params.algoritmo  metrics.accuracy  metrics.roc_auc
             logreg logistic_regression            0.8336         0.923771
          rf-depth5       random_forest            0.8232         0.916277
         rf-depth15       random_forest            0.8088         0.896510
```

Se lee de inmediato: la regresión logística gana al bosque, y subir la profundidad de 5 a 15
empeora el resultado por sobreajuste.

`search_runs` acepta filtros con una sintaxis parecida a SQL:

```python
mlflow.search_runs(
    experiment_names=["riesgo-credito"],
    filter_string="metrics.roc_auc > 0.92 and params.algoritmo = 'random_forest'",
)
```

## Autologging

Escribir un `log_param` por hiperparámetro es tedioso y se olvida. El **autologging** registra
todo automáticamente:

```python
mlflow.sklearn.autolog()

with mlflow.start_run(run_name="con-autolog"):
    RandomForestClassifier(n_estimators=30, max_depth=4, random_state=0).fit(X_tr, y_tr)
```

Sin una sola llamada a `log_*`, esa ejecución capturó:

- **19 parámetros** — todos los del estimador: `bootstrap`, `ccp_alpha`, `class_weight`,
  `criterion`, `max_depth`, etc.
- **6 métricas** de entrenamiento — `training_accuracy_score`, `training_f1_score`,
  `training_log_loss`, `training_roc_auc`, `training_precision_score`, `training_recall_score`.
- **4 artefactos** — `training_confusion_matrix.png`, `training_roc_curve.png`,
  `training_precision_recall_curve.png` y `estimator.html`.
- El modelo empaquetado, con su firma.

Hay autologging para scikit-learn, PyTorch, TensorFlow, XGBoost, LightGBM, Spark MLlib y
Transformers, entre otros. `mlflow.autolog()` los activa todos.

La contrapartida es que registra **métricas de entrenamiento**, no de validación. Las que
realmente importan siguen siendo tuyas:

```python
mlflow.log_metric("test_roc_auc", roc_auc_score(y_te, modelo.predict_proba(X_te)[:, 1]))
```

## Ejecuciones anidadas

Un barrido de hiperparámetros genera muchas ejecuciones que conviene agrupar:

```python
with mlflow.start_run(run_name="barrido-max-depth") as padre:
    for d in [3, 6, 12]:
        with mlflow.start_run(run_name=f"depth-{d}", nested=True):
            modelo = RandomForestClassifier(max_depth=d, random_state=0).fit(X_tr, y_tr)
            mlflow.log_param("max_depth", d)
            mlflow.log_metric("accuracy", modelo.score(X_te, y_te))
```

Las hijas quedan colgando de la padre en la interfaz, y se recuperan filtrando por
`tags.mlflow.parentRunId`. Resultado del barrido real:

```text
max_depth  3  -> accuracy 0.8264
max_depth  6  -> accuracy 0.8248
max_depth 12  -> accuracy 0.8184
```

## La interfaz web

```bash
mlflow ui --backend-store-uri sqlite:///mlflow.db
```

Levanta en `http://127.0.0.1:5000` una interfaz donde comparar ejecuciones lado a lado, graficar
métricas y navegar los artefactos. `mlflow server` es la variante para uso compartido, y desde
MLflow 3 también toma `sqlite:///mlflow.db` por defecto.

## Ver también

- [MLflow en la práctica](mlflow_en_practica.md) — modelos, registro y despliegue.
- [Pipelines y experimentos con DVC](dvc_pipelines_y_experimentos.md) — el otro enfoque.
- [Ray Tune](ray_bibliotecas_ia.md#ray-tune) — búsqueda de hiperparámetros a escala.
- [Sistemas de machine learning](sistemas_de_machine_learning.md)

## Referencias

- [mlflow.org](https://mlflow.org/) · [documentación](https://mlflow.org/docs/latest/)
- [mlflow/mlflow](https://github.com/mlflow/mlflow)
