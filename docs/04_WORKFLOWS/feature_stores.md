# Feature Stores

Un **Feature Store System** (FSS) es un sistema de base de datos especializado en datasets y
*features*, capaz de soportar las tareas propias de un almacén de features:

- Almacenamiento de datasets crudos.
- Generación de features a partir de datasets y reglas.
- **Descubrimiento** de features.
- Cómputo de features, *backfills* y registro.
- Generación de métricas sobre las features.
- Funcionamiento como almacén **offline** u **online**.
- Uso de un framework de ingeniería de features de ML.
- **Compartición y reutilización** de features.
- Versionado de features.
- Linaje (*lineage*) de features.
- Metadatos de features.
- Calidad de las features.
- **Garantizar la consistencia** entre los datos de entrenamiento y los de servicio.
- Monitoreo de pipelines:
    - desarrollo,
    - automatización,
    - alertas.

Todos estos son aspectos deseables en un entorno de ML.

## Tres tipos de creación de modelos

Conviene empezar dividiendo la creación de modelos en tres categorías:

- **Investigación**
- **Desarrollo**
- **Producto**

Muchas veces existe un grado de incertidumbre sobre qué tan bien funcionará un modelo con
nuestros datos. Puede requerir unos pocos experimentos, o pasar de decenas a miles de ellos.
Según el sistema y el tipo de modelo, esos experimentos se pueden automatizar o deben
realizarse de forma semi-manual.

## El coste de repetir trabajo

Se crean sistemas especializados para trabajar con datos de producción, lo que resulta una
ventaja a la hora de productivizar un modelo. Sin embargo, **cada ejecución del experimento
repite pasos costosos comunes** en entornos de producción, porque no está previsto reutilizar
el procesamiento sobre los mismos datos.

La **carga de datos** se convierte en un proceso caro que no escala bien con el incremento del
volumen. Este tipo de cuellos de botella ralentiza todo el proceso.

## El impacto de la regulación

La regulación de protección de datos (**DPR**) complica el trabajo: ahora es necesario agregar
o transformar los datos para proteger la información de los usuarios. Pero eso **reduce la
capacidad de reutilizar los datos en estados intermedios**: esos estados pasan a ser volátiles
y su ciclo de vida se vuelve muy corto.

## Datos crudos

Hay dos enfoques habituales para llevar los datos crudos al almacén:

- **ETL** (*Extract, Transform, Load*) — se transforma antes de cargar.
- **ELT** (*Extract, Load, Transform*) — se carga primero y se transforma en destino,
  aprovechando la capacidad de cómputo del almacén.

## Ver también

- [Sistemas de machine learning](sistemas_de_machine_learning.md)
- [Descubrimiento de datos](descubrimiento_de_datos.md)
