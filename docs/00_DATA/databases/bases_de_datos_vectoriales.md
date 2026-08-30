# Bases de Datos Vectoriales

Una **base de datos vectorial** es un tipo de base de datos diseñada específicamente para
almacenar y gestionar **datos vectoriales**.

En computación, un vector suele referirse a una colección ordenada de elementos, cada uno
identificado por un índice. En el contexto de las bases de datos, sin embargo, un vector
normalmente designa una construcción matemática que representa puntos de datos en un
**espacio multidimensional**.

En una base de datos vectorial los datos se almacenan y consultan según su representación
vectorial, lo que permite recuperar y analizar de forma eficiente datos espaciales:
información geográfica, imágenes, o cualquier otro dato representable como vector.

Estas bases de datos emplean **técnicas especializadas de indexación y optimización de
consultas** para manejar eficientemente la alta dimensionalidad de los vectores. Se usan
habitualmente en sistemas de información geográfica (GIS), machine learning, visión por
computadora y sistemas de recomendación.

Ver [Búsqueda por similitud](busqueda_por_similitud.md) para el detalle de cómo funcionan esos
índices, y [Milvus](milvus.md) para una implementación completa.

En el contexto de los [LLMs](../../10_LLM/introduccion.md), son la pieza que sostiene la
recuperación semántica en las arquitecturas
[RAG](../../10_LLM/RAGS/chatbot_rag_con_langchain.md): los documentos se convierten en
*embeddings* y la base vectorial encuentra los más cercanos a la consulta.
