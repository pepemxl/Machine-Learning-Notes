# Bases de Datos

Los modelos de bases de datos han crecido enormemente con los desarrollos tecnológicos
recientes. Quedaron atrás los días en que las empresas y organizaciones dependían
únicamente de bases de datos relacionales para almacenar y gestionar su información.

Hoy existen muchos usos para las bases de datos, lo que ha dado origen a casos muy
especializados que conviven con los tradicionales.

Se pueden clasificar según varios criterios: modelo de datos, estructura de almacenamiento,
forma de acceso y uso previsto. Estos son los tipos más comunes.

## 1. Bases de datos relacionales (RDBMS)

Organizan los datos en **tablas con filas y columnas**. Usan SQL (*Structured Query
Language*) para consultar y gestionar la información.

- MySQL
- PostgreSQL
- SQL Server
- DB2
- Oracle
- SQLite

## 2. Bases de datos NoSQL

Agrupan un amplio conjunto de tecnologías **no relacionales**, diseñadas para manejar datos
no estructurados, semiestructurados o estructurados. Ofrecen flexibilidad, escalabilidad y
mejor rendimiento que las relacionales en ciertos casos de uso.

- MongoDB
- Cassandra
- Redis
- Couchbase

## 3. Bases de datos de grafos

Optimizadas para almacenar y consultar **estructuras de grafo**. Representan los datos como
nodos, aristas y propiedades interconectadas. Son adecuadas para aplicaciones que requieren
análisis de relaciones complejas, como redes sociales y
[sistemas de recomendación](../09_SYSTEMS/REC_SYSTEM/introduccion_recomendadores_con_kg.md).

- Neo4j
- Amazon Neptune
- JanusGraph
- [Apache HugeGraph](../08_GRAPH/apache_hugegraph.md)

Ver también la sección de [grafos](../08_GRAPH/introduccion.md), y
[Apache TinkerPop](../08_GRAPH/apache_tinkerpop.md), la capa de abstracción que permite
consultar varios de estos motores con el mismo lenguaje.

## 4. Bases de datos columnares

Almacenan los datos **por columnas en lugar de por filas**, lo que acelera las consultas
analíticas y de reporte. Encajan bien en cargas **OLAP** (*Online Analytical Processing*),
donde son frecuentes las agregaciones sobre grandes volúmenes.

- Apache Cassandra
- ClickHouse
- Google BigQuery

## 5. Bases de datos documentales

Guardan los datos en formato semiestructurado, como documentos JSON o BSON. Cada documento
puede tener su propia estructura, lo que las hace flexibles para datos heterogéneos. Se usan
mucho en gestores de contenido, analítica en tiempo real y aplicaciones con esquemas que
cambian con frecuencia.

- MongoDB
- Couchbase
- Firebase Firestore

## 6. Bases de datos vectoriales

Almacenan **embeddings** —vectores de alta dimensión— e implementan
[búsqueda por similitud](databases/busqueda_por_similitud.md) aproximada sobre ellos. Son la
pieza que sostiene la búsqueda semántica, los recomendadores y la recuperación en las
arquitecturas RAG.

- [Milvus](databases/milvus.md)
- Qdrant, Weaviate, Chroma
- `pgvector` (extensión de PostgreSQL)

Ver [bases de datos vectoriales](databases/bases_de_datos_vectoriales.md).

## 7. Bases de datos espaciales

Diseñadas para almacenar y consultar **datos espaciales**, como información geográfica
(**GIS**) y geometrías. Soportan tipos y operaciones espaciales para analizar y visualizar
relaciones en el espacio.

- PostGIS (extensión de PostgreSQL)
- MongoDB (con indexación geoespacial)
- Oracle Spatial

## 8. Bases de datos de series de tiempo

Especializadas en **series temporales**: puntos de datos indexados u ordenados por tiempo.
Están optimizadas para almacenar y consultar datos con marca temporal de forma eficiente.
Se usan en IoT, monitoreo y sistemas de *trading*.

- InfluxDB
- Prometheus
- TimescaleDB
- [OpenTSDB](databases/opentsdb.md)
- [Goku](databases/goku.md)

Ver también la sección de [series de tiempo](../12_TIME_SERIES/introduccion.md).

## Hacia los knowledge graphs

A medida que crecen la cantidad y la complejidad de los datos, hace falta una forma más
flexible y dinámica de representar y analizar las **relaciones** entre puntos de datos. Ahí
entran los **knowledge graphs**, una topología moderna de gestión de datos que gana
popularidad rápidamente entre las organizaciones orientadas a datos.

Ver [Definiciones de Knowledge Graph](../08_GRAPH/definiciones_knowledge_graph.md).
