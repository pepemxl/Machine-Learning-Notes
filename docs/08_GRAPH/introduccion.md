# Algoritmos de Grafos para Ciencia de Datos

1. **Modelado y construcción del grafo**
    - Identificar relaciones entre puntos de datos
    - Describir una estructura de grafo
    - Importar datos a una base de datos de grafos
2. **Lenguaje de consulta de grafos**
    - Identificar patrones en el grafo
    - Recorrer conexiones
    - Agregar datos
    - Realizar análisis exploratorio
3. **Algoritmos de grafos y redes inferidas**
    - Encontrar los nodos más importantes o críticos
    - Agrupar nodos en comunidades
    - Identificar nodos similares
    - Analizar relaciones indirectas
4. **Machine learning sobre grafos**
    - Extraer features de los grafos
    - Predecir etiquetas de nodos
    - Predecir nuevas conexiones

## ¿Qué es un grafo?

Es habitual confundir el término **grafo** pensando que cualquier gráfica lo es. No es el caso:
la analítica de grafos se basa en la **teoría de grafos**.

El problema típico para entender el área es el de los **puentes de Königsberg**.

La definición matemática de un grafo $G$ es un par $(V,E)$, donde $V$ es un conjunto de
**vértices** y $E$ un conjunto de **aristas**.

La definición desde ciencias de la computación es la de un **tipo de dato abstracto**:

1. Tiene una estructura de datos que representa el grafo matemático.
2. Soporta un conjunto de operaciones:
    - `add_edge`
    - `add_vertex`
    - `get_neighbors`

Hay varias formas de representar un grafo. Quizá la más común sea una matriz, llamada **matriz
de adyacencia**.

## Ejemplos

**Facebook** es el ejemplo clásico: todos los datos que existen ahí se representan más fácilmente
como un grafo. Es una red social.

**Los tuits también son un grafo:**

- Muchos tipos de nodo:
    - Usuarios
    - Tuits
    - *Likes*
    - URLs
    - Media
        - Imagen
        - Video
    - Hashtags
- Muchos tipos de arista (acciones):
    - Un usuario **crea** un tuit
    - Un tuit está **en respuesta** a otro
    - Un tuit **retuitea** a otro
    - Un usuario **menciona** a otro usuario
    - Un tuit **contiene** un hashtag
    - Un usuario **sigue** a otro usuario

## Problemas típicos

Los problemas que habitualmente se estudian con grafos son:

- **Redes sociales**
- **Redes biológicas**
    - Enfermedades conectadas por genes
- **Ciudades inteligentes**
    - Optimización de modelos de tráfico
    - Planificación de nodos de transporte
- **Detección de amenazas**

## ¿Por qué hacemos analítica?

- Descubrir características de los datasets a partir de sus propiedades matemáticas.
- Responder preguntas específicas que cruzan múltiples conjuntos de datos.
- Desarrollar un modelo matemático para predecir el comportamiento de ciertas variables.
- Detectar fenómenos emergentes y explicar los factores que contribuyen a ellos.

## Los grafos y las V del Big Data

Las tres V conocidas son:

- **Volumen**
- **Velocidad**
- **Variedad**

Y la menos conocida:

- **Valencia**: el grado de interdependencia entre los datos. La idea es que al aumentar la
  valencia (la heterogeneidad) de un grafo, aumentamos sus conexiones.

Ver [Dimensiones de la analítica](../00_DATA/dimensiones_analitica.md).

## En esta sección

- [Definiciones de Knowledge Graph](definiciones_knowledge_graph.md)
- [Creación de Knowledge Graphs](creacion_de_knowledge_graphs.md)
- [Grafo de código](grafo_de_codigo.md)
- [Apache TinkerPop](apache_tinkerpop.md) y [Gremlin](gremlin.md)
- [Servidores MCP con KGs](servidores_mcp_con_kgs.md)
- [Proyectos Apache para KG](proyectos_apache_para_kg.md)
- [Knowledge Graphs y blockchain](knowledge_graphs_y_blockchain.md)

## Referencias

- [Schema.org](https://schema.org/)
- [RDFLib, paquete Python puro para trabajar con RDF](https://rdflib.readthedocs.io/en/stable/index.html)
- Dai, Y. et al. [*A Survey on Knowledge Graph Embedding: Approaches, Applications and Benchmarks*](https://www.mdpi.com/2079-9292/9/5/750)
