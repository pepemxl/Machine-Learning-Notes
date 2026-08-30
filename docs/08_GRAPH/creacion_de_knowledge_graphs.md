# Creación de Knowledge Graphs

La creación de conocimiento consiste en **anotar semánticamente** contenido, datos y servicios
provenientes de fuentes heterogéneas mediante una **ontología**. Este paso se divide en dos
tareas principales:

- **Bottom-Up**: una tarea ligera de ingeniería de ontologías, llamada *especificación de
  dominio*, que crea patrones específicos del dominio.
- **Top-Down**: una tarea de generación de instancias a gran escala, como aplicación de esos
  patrones específicos del dominio.

## Modelado bottom-up: especificación de dominio

Tomamos [Schema.org](https://schema.org/) como ontología de referencia para knowledge graphs,
por ser un estándar industrial *de facto* para anotaciones en la web. Estas anotaciones son
bloques de construcción naturales para un knowledge graph, y usar una ontología tan extendida
aumenta el impacto del grafo resultante.

Antes de que empiece el proceso de generación de conocimiento hay que **analizar los dominios**
que el knowledge graph pretende describir, para identificar las entidades del dominio y sus
relaciones, y mapearlas después a Schema.org.

Este proceso es bastante desafiante por la propia naturaleza del vocabulario: Schema.org cubre
muchos dominios con cientos de tipos y propiedades, pero su cobertura **para dominios concretos
es muy superficial**. Esta situación exige adaptar Schema.org a dominios y tareas específicas.
A ese proceso de adaptación lo llamamos **especificación de dominio**.

## Ver también

- [Definiciones de Knowledge Graph](definiciones_knowledge_graph.md)
- [Desarrollo orientado a ontologías](../11_JARVIS/desarrollo_orientado_a_ontologias.md)
