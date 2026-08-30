# Sistemas de Machine Learning (MLS)

Para crear un producto de IA que funcione hay que ensamblar un conjunto de elementos:

- Clúster de producción
- Recolección de datos
- Almacenamiento de datos
- Jobs de generación de features
- Clúster de cómputo para entrenamiento
- Pipelines de CI/CD
- Monitoreo
- Registro de experimentos (*experiment loggers*)

A todos estos ingredientes en conjunto los llamamos **sistemas de machine learning**.

## Dataflow

*Dataflow* es un concepto amplio, con significados distintos según la aplicación y el contexto.
En arquitectura de software, el flujo de datos se relaciona con el **procesamiento de flujos**
(*stream processing*) o la programación reactiva.

Normalmente representa la **transferencia de información** de una parte del sistema a otra. Los
flujos enlazan procesos, almacenes y terminadores. Los sistemas de dataflow más habituales son:

- Airflow
- Dagster
- Dataswarm
- Databricks

Hay muchas soluciones disponibles, pero cuál es la mejor depende de nuestros datos y de los
objetivos a alcanzar. Igual que un equipo de DevOps toma decisiones de arquitectura en función
de las propiedades deseadas del sistema para garantizar los requisitos, aquí también hacen
falta **patrones específicos** en la arquitectura.

## Ver también

- [Feature stores](feature_stores.md)
- [Definición de proyectos de IA](definicion_de_proyectos_de_ia.md)
- [Workflows, máquinas de estado y colas](workflows_maquinas_de_estado_y_colas.md)
- [Ray](ray.md) y sus [bibliotecas de IA](ray_bibliotecas_ia.md) — cómputo distribuido para
  entrenar, ajustar y servir
- [ONNX](onnx.md) y [ONNX Runtime](onnx_runtime.md) — cómo se empaqueta y se sirve el modelo
  una vez entrenado
- [Proyectos generales de ML](../09_SYSTEMS/proyectos_generales_de_ml.md)
