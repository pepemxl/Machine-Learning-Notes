# Pipelines y Experimentos con DVC

El versionado de datos está en [DVC](dvc.md). Esta página cubre las otras dos mitades de la
herramienta: los **pipelines reproducibles** y el **seguimiento de experimentos**.

## Pipelines

Un pipeline de DVC se declara en `dvc.yaml` como una lista de **stages**. Cada stage tiene un
comando, sus dependencias, sus salidas y, opcionalmente, parámetros y métricas.

```bash
dvc stage add -n preparar \
    -p preparar.test_size \
    -d src/preparar.py -d data/train.csv \
    -o data/prep_train.csv -o data/prep_test.csv \
    python3 src/preparar.py

dvc stage add -n entrenar \
    -p entrenar \
    -d src/entrenar.py -d data/prep_train.csv -d data/prep_test.csv \
    -M metrics.json \
    python3 src/entrenar.py
```

Que genera:

```yaml
# dvc.yaml
stages:
  preparar:
    cmd: python3 src/preparar.py
    deps:
      - data/train.csv
      - src/preparar.py
    params:
      - preparar.test_size
    outs:
      - data/prep_test.csv
      - data/prep_train.csv
  entrenar:
    cmd: python3 src/entrenar.py
    deps:
      - data/prep_test.csv
      - data/prep_train.csv
      - src/entrenar.py
    params:
      - entrenar
    metrics:
      - metrics.json:
          cache: false
```

Los distintos tipos de dependencia:

| Clave | Significado |
|---|---|
| `deps` | Archivos de los que depende el stage: datos y **también el código** |
| `outs` | Lo que produce. DVC los versiona y los añade a `.gitignore` |
| `params` | Entradas desde `params.yaml`. Un cambio invalida el stage |
| `metrics` | Salidas que son métricas. Con `cache: false` van a Git, por ser pequeñas |
| `plots` | Salidas para graficar: curvas de aprendizaje, matrices de confusión |

Los stages **no declaran orden**: igual que en [Kedro](kedro.md), el DAG se deduce de que las
salidas de uno son las entradas de otro.

```bash
dvc dag
```

```text
       +----------+
       | preparar |
       +----------+
             *
             *
       +----------+
       | entrenar |
       +----------+
```

### Ejecutar

```bash
dvc repro
```

```text
Running stage 'preparar':
> python3 src/preparar.py
Running stage 'entrenar':
> python3 src/entrenar.py
Updating lock file 'dvc.lock'
```

Al terminar, `dvc.lock` guarda el hash de cada dependencia, parámetro y salida. Ese archivo **sí**
va a Git: es el que hace la ejecución reproducible.

```yaml
# dvc.lock (fragmento)
stages:
  preparar:
    cmd: python3 src/preparar.py
    deps:
      - path: data/train.csv
        hash: md5
        md5: 4b315748f1d42310c3ef8ca821fefc20
        size: 206469
    params:
      params.yaml:
        preparar.test_size: 0.25
```

### Reproducción incremental

Esta es la característica que justifica montar el pipeline. `dvc repro` compara los hashes de
`dvc.lock` con el estado actual y **solo ejecuta lo que cambió**.

Sin cambios, no se ejecuta nada:

```text
$ dvc repro
Stage 'preparar' didn't change, skipping
Stage 'entrenar' didn't change, skipping
```

Y al cambiar **solo** un parámetro del segundo stage —`n_estimators` de 50 a 200—:

```text
$ dvc repro
Stage 'preparar' didn't change, skipping
Running stage 'entrenar':
> python3 src/entrenar.py
```

`preparar` se salta porque ni sus datos, ni su código, ni sus parámetros cambiaron. DVC lo sabe
porque los tiene todos hasheados.

!!! note "Contraste con `--only-missing-outputs` de Kedro"
    [Kedro](kedro_en_produccion.md#ejecucion-incremental) tiene una opción de aspecto parecido,
    pero solo comprueba si el archivo de salida **existe**. DVC compara **hashes de todas las
    dependencias**, código incluido, así que detecta que un artefacto está *desactualizado*, no
    solo que falta. Es una diferencia de fondo: DVC hace compilación incremental de verdad; la
    opción de Kedro sirve para reanudar una ejecución interrumpida.

## Métricas y parámetros

```bash
dvc metrics show
```

```text
Path          accuracy    roc_auc
metrics.json  0.8424      0.9256
```

Lo interesante es comparar contra otro commit:

```bash
dvc metrics diff HEAD~1
```

```text
Path          Metric    HEAD~1    workspace    Change
metrics.json  accuracy  0.8416    0.8424       0.0008
metrics.json  roc_auc   0.92497   0.9256       0.00063
```

```bash
dvc params diff HEAD~1
```

```text
Path         Param                  HEAD~1    workspace
params.yaml  entrenar.n_estimators  50        200
```

Puestos juntos, responden a la pregunta que importa en una revisión de código: **qué cambió y qué
efecto tuvo**. Duplicar los árboles subió la precisión 0.0008, que probablemente no compensa el
coste.

## Experimentos

Durante el ajuste de un modelo se prueban decenas de configuraciones. Hacer un commit por cada
una llena el historial de ruido; no hacerlo pierde los resultados.

`dvc exp` resuelve esto con ejecuciones que **no crean commits** en el historial:

```bash
dvc exp run -S entrenar.max_depth=3
dvc exp run -S entrenar.max_depth=8
dvc exp run -S entrenar.max_depth=15
```

`-S` sobrescribe un parámetro sin editar `params.yaml`.

```bash
dvc exp show --only-changed
```

```text
 Experiment                 Created    accuracy   roc_auc   entrenar.max_depth
 workspace                  -            0.8312   0.91098   15
 main                       01:30 PM     0.8424    0.9256   5
 ├── da30eab [adunc-quiz]   01:30 PM     0.8312   0.91098   15
 ├── 55ce8f0 [sooty-rale]   01:30 PM     0.8416   0.92295   8
 └── ee453a2 [paler-alap]   01:30 PM     0.8408   0.91999   3
```

La tabla se lee de un vistazo: `max_depth=5` es el mejor, y a partir de 8 el modelo empeora por
sobreajuste. Cada experimento tiene un nombre generado y un identificador.

Mientras tanto, el historial de Git sigue limpio:

```text
$ git log --oneline
fa77001 n_estimators=200
3984d67 pipeline con señal
5ed19b7 train.csv v2 (5000 filas)
```

Los tres experimentos no aparecen: viven en referencias aparte hasta que decidas conservarlos.

```bash
dvc exp apply 55ce8f0        # trae ese experimento al espacio de trabajo
dvc exp branch 55ce8f0 mejor # o lo convierte en una rama
dvc exp remove -A            # descarta todos
```

## DVC y Kedro

Se solapan en la parte de pipelines, pero resuelven problemas distintos y se combinan bien:

| | **DVC** | **Kedro** |
|---|---|---|
| Enfoque | Reproducibilidad y versionado | Estructura del código |
| Unidad | Un comando de shell | Una función Python |
| Datos | Los versiona | Los declara en el catálogo |
| Incremental | Por hashes de dependencias | Solo por existencia del archivo |
| Experimentos | Integrados | Vía plugins |

Una combinación habitual es usar Kedro para estructurar el proyecto y DVC para versionar los
datos y capturar experimentos, con un stage de DVC que invoca `kedro run`.

## Qué NO hace DVC

- **No programa ejecuciones.** No es un orquestador; `dvc repro` corre ahí mismo. Para ejecución
  periódica hace falta Airflow o similar, igual que con
  [Kedro](kedro.md#lo-que-kedro-no-es).
- **No sirve modelos.** Ver [ONNX Runtime](onnx_runtime.md) o
  [Ray Serve](ray_bibliotecas_ia.md#ray-serve).
- **No distribuye el cómputo.** Cada stage corre en una máquina. Ver [Ray](ray.md).
- **No registra qué pasó en producción.** Eso es [OpenLineage](openlineage.md).

## Errores frecuentes

- **Olvidar `dvc push`.** El commit de Git viaja, los datos no, y el equipo se encuentra punteros
  que no puede resolver.
- **No poner el código en `deps`.** Si un stage no depende de su propio `.py`, cambiar el
  algoritmo no dispara la reejecución y `dvc.lock` miente.
- **Cachear métricas.** Van con `cache: false` para que queden en Git y `dvc metrics diff` pueda
  compararlas entre commits.
- **Rastrear el mismo archivo con `dvc add` y como `outs` de un stage.** Solo una de las dos
  cosas: si lo produce un stage, es suyo.
- **Confundir experimentos con commits.** `dvc exp` es para explorar; cuando un resultado importa,
  hay que promoverlo con `dvc exp branch` o un commit normal.

## Ver también

- [DVC](dvc.md) — versionado de datos y almacenamiento remoto.
- [Kedro en producción](kedro_en_produccion.md)
- [OpenLineage](openlineage.md)
- [Ray Tune](ray_bibliotecas_ia.md#ray-tune) — para búsquedas de hiperparámetros más grandes.
- [MLflow](mlflow.md) — el enfoque alternativo; ver
  [la comparación](mlflow_en_practica.md#mlflow-frente-a-dvc).

## Referencias

- [Documentación de DVC](https://dvc.org/doc)
- [Guía de experimentos](https://dvc.org/doc/user-guide/experiment-management)
- [iterative/dvc](https://github.com/iterative/dvc)
