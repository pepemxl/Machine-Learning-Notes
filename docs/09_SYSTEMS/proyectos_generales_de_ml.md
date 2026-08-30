# Proyectos Generales de Machine Learning

## Ciclo de vida del machine learning

```mermaid
flowchart LR
    subgraph "Ciclo de vida completo de ML"
        direction LR
        
        subgraph "Preparación"
            A1[Datos<br>📊] --> A2[Preprocesar<br>🔧] --> A3[Dataset<br>📁]
        end
        
        subgraph "Desarrollo"
            B1[Entrenar<br>🧠] --> B2[Desplegar<br>🚀]
        end
        
        subgraph "Producción"
            C1[Predecir<br>🔮] --> C2[Monitorear<br>📈]
        end
        
        subgraph "Mantenimiento"
            D1[Mantener<br>🛠️]
        end
        
        A3 --> B1
        B2 --> C1
        C2 --> D1
        D1 -->|Reentrenar| B1
        C2 -->|Retroalimentación| A1
    end
    
    style A1 fill:#e6f3ff
    style A2 fill:#e6f3ff
    style A3 fill:#e6f3ff
    style B1 fill:#e6ffe6
    style B2 fill:#e6ffe6
    style C1 fill:#fff0e6
    style C2 fill:#fff0e6
    style D1 fill:#ffe6e6
```

En general, los proyectos de machine learning requieren los siguientes pasos:

1. Recolección de datos
2. Preprocesamiento
3. Construcción de datasets
4. Entrenamiento del modelo (online / offline)
5. Despliegue del modelo — ver [ONNX](../04_WORKFLOWS/onnx.md) y
   [ONNX Runtime](../04_WORKFLOWS/onnx_runtime.md)
6. Predicción
7. Monitoreo de modelos
8. Mantenimiento, diagnóstico y reentrenamiento


```mermaid
flowchart TD
    Start([Inicio del proyecto ML]) --> Collect
    subgraph "Ciclo continuo de ML"
        Collect[1. Recolección de datos] --> Preprocess
        Preprocess[2. Preprocesamiento] --> Build
        Build[3. Construir datasets] --> Train
        Train[4. Entrenamiento] --> Deploy
        Deploy[5. Despliegue] --> Predict
        Predict[6. Predicción] --> Monitor
        Monitor[7. Monitoreo] --> Maintain
        Maintain[8. Mantenimiento] --> Collect
    end
    
    Monitor -->|Disparador| Retrain[Reentrenar modelo]
    Retrain --> Train
    
    Maintain -->|Optimizar| Improve[Mejoras del sistema]
    Improve --> Deploy
```



Para cubrir todos estos pasos necesitamos herramientas suficientes en nuestro stack.

En muchas grandes empresas y startups, los proyectos de machine learning se despliegan atravesando las siguientes etapas:

1. Frameworks de machine learning
    - Open AI
    - Tensorflow
    - **Pytorch**
    - SageMaker
    - GridAI
2. Cómputo distribuido
    - Dask
    - **Spark**
    - Databricks
3. Evaluación de modelos y seguimiento de experimentos
    - **MLFlow**
    - neptune.ai
    - Comet
4. Despliegue de modelos
    - OctoML
    - **BentoML**
5. Monitoreo y gestión de modelos
    - Fidler
    - Cortex
6. Plataformas integrales (*end-to-end*)
    - nvidia
    - databricks
    - SageMaker


## Stacks de Big Data

- SMACK
- Hadoop Ecosystem
- ELK Stack
- Flink Stack
- Lambda Architecture
- Microsoft Azure Stack

## SMACK
- Spark
- Mesos
- Akka
- Cassandra
- Kafka


**Spark**: framework de procesamiento de datos en memoria que facilita el procesamiento distribuido y el análisis eficiente de grandes volúmenes de datos.

**Mesos**: sistema de gestión de clústeres que permite asignar recursos de forma eficiente entre aplicaciones y servicios en un entorno distribuido.

**Akka**: toolkit y entorno de ejecución para construir sistemas concurrentes y distribuidos basados en el modelo de actores, unidades de procesamiento independientes que se comunican entre sí.

**Cassandra**: base de datos distribuida, altamente escalable y tolerante a fallos, usada para gestionar grandes volúmenes de datos repartidos entre múltiples nodos.

**Kafka**: plataforma distribuida de streaming de eventos que facilita la ingesta y el procesamiento de datos en tiempo real mediante flujos de eventos.


## Revisión de proyectos: Big Data + ML + Minería de datos

- Análisis de geolocalización para aplicaciones de transporte
    - Servicio de proximidad
    - Amigos cercanos
- Sistema de búsqueda visual
- Sistema de difuminado de Google Street View
- Búsqueda de video en YouTube
- Detección de contenido dañino
- Sistema de recomendación de video
- Sistema de recomendación de eventos
- Predicción de clics en anuncios en plataformas sociales
- Anuncios similares en plataformas de alquiler vacacional
- Feed de noticias personalizado
- [People You May Know](PYMK/pymk.md)