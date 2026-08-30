# Machine Learning Notes

Notas de trabajo sobre **análisis de datos, machine learning, sistemas de ML y LLMs**.
Cada sección es autocontenida; el orden sugerido va de los fundamentos de datos hacia
los sistemas en producción.

---

## Los tres campos y cómo se relacionan

**Análisis de datos**. Examina, limpia, transforma y modela datos para extraer información y
tomar decisiones. Se apoya en estadística descriptiva e inferencial, pruebas de hipótesis,
análisis exploratorio (EDA) y visualización.

**Machine learning**. Subcampo de la inteligencia artificial dedicado a construir algoritmos
que aprenden de los datos y hacen predicciones sin ser programados explícitamente para cada
caso. Entrena modelos sobre conjuntos de datos para aprender patrones y aplicarlos después a
datos nuevos.

**Minería de datos**. Descubre patrones, relaciones e información en grandes volúmenes de datos
combinando estadística, machine learning y sistemas de bases de datos. Sus técnicas habituales
son las reglas de asociación, el *clustering*, la clasificación, la regresión y la detección de
anomalías.

El análisis de datos suele ser **precursor** del machine learning: prepara y valida los datos
antes de entrenar. A su vez, las técnicas de ML se usan dentro del análisis para descubrir
señales más profundas o automatizar decisiones. La minería de datos **complementa** a ambos,
aportando métodos adicionales de exploración.

---

## Mapa del curso

### 00 · Análisis de datos
- [Las seis fases del análisis de datos](00_DATA/fases_analisis_datos.md)
- [Dimensiones de la analítica](00_DATA/dimensiones_analitica.md)
- [Big Data](00_DATA/big_data.md) ·
  [Tipos de memoria y almacenamiento](00_DATA/memory/tipos_de_memoria_y_almacenamiento.md)
- Bases de datos: [introducción](00_DATA/introduccion_bases_de_datos.md) ·
  [OpenTSDB](00_DATA/databases/opentsdb.md) ·
  [Goku](00_DATA/databases/goku.md) ·
  [vectoriales](00_DATA/databases/bases_de_datos_vectoriales.md)
- [Búsqueda por similitud](00_DATA/databases/busqueda_por_similitud.md) ·
  [Milvus](00_DATA/databases/milvus.md)
- Spark: [Spark](00_DATA/spark/spark.md) ·
  [PySpark](00_DATA/spark/pyspark.md) ·
  [ejemplos](00_DATA/spark/ejemplos_pyspark.md) ·
  [preguntas](00_DATA/spark/preguntas.md)

### 01 · Aprendizaje supervisado
- [Introducción y árboles de decisión](01_SUPERVISED_LEARNING/introduccion.md)
- [Regresión lineal](01_SUPERVISED_LEARNING/regresion_lineal.md)
- [Máquinas de vectores de soporte](01_SUPERVISED_LEARNING/support_vector_machines.md)

### 02 · Aprendizaje no supervisado
- [Introducción y clustering](02_UNSUPERVISED_LEARNING/introduccion.md)
- [Clustering en Big Data](02_UNSUPERVISED_LEARNING/clustering_en_big_data.md)
- [Detección de anomalías](02_UNSUPERVISED_LEARNING/deteccion_de_anomalias.md)
- [Isolation Forest](02_UNSUPERVISED_LEARNING/isolation_forest.md)

### 03 · Aprendizaje por refuerzo
- [Introducción](03_REINFORCEMENT_LEARNING/introduccion.md)
- [Procesos de decisión de Markov](03_REINFORCEMENT_LEARNING/procesos_de_decision_de_markov.md)
- [Q-Learning](03_REINFORCEMENT_LEARNING/q_learning.md)
- [Deep Reinforcement Learning](03_REINFORCEMENT_LEARNING/deep_reinforcement_learning.md)

### 04 · Workflows
- [Sistemas de machine learning](04_WORKFLOWS/sistemas_de_machine_learning.md)
- [Feature stores](04_WORKFLOWS/feature_stores.md)
- [Definición de proyectos de IA](04_WORKFLOWS/definicion_de_proyectos_de_ia.md)
- [Descubrimiento de datos](04_WORKFLOWS/descubrimiento_de_datos.md)
- [Workflows, máquinas de estado y colas](04_WORKFLOWS/workflows_maquinas_de_estado_y_colas.md)
- [DVC](04_WORKFLOWS/dvc.md) ·
  [pipelines y experimentos con DVC](04_WORKFLOWS/dvc_pipelines_y_experimentos.md)
- [OpenLineage](04_WORKFLOWS/openlineage.md) ·
  [OpenLineage en la práctica](04_WORKFLOWS/openlineage_en_practica.md)
- [Kedro](04_WORKFLOWS/kedro.md) · [Kedro en producción](04_WORKFLOWS/kedro_en_produccion.md)
- [Ray](04_WORKFLOWS/ray.md) · [bibliotecas de IA de Ray](04_WORKFLOWS/ray_bibliotecas_ia.md)
- [Feast](04_WORKFLOWS/feast.md) · [Feast en la práctica](04_WORKFLOWS/feast_en_practica.md)
- [MLflow](04_WORKFLOWS/mlflow.md) · [MLflow en la práctica](04_WORKFLOWS/mlflow_en_practica.md)
- [ONNX](04_WORKFLOWS/onnx.md) · [ONNX Runtime](04_WORKFLOWS/onnx_runtime.md)

### 05 · Matemáticas
- [Matemáticas para machine learning](05_MATH/matematicas_para_machine_learning.md)
- [Forward propagation](05_MATH/forward_propagation.md)
- [Funciones de base radial](05_MATH/funciones_de_base_radial.md)

### 07 · NLP
- [Detección de patrones de nombres](07_NLP/deteccion_de_patrones_de_nombres.md)
- [Sistemas de detección](07_NLP/sistemas_de_deteccion.md)

### 08 · Grafos
- [Introducción a algoritmos de grafos](08_GRAPH/introduccion.md)
- [Definiciones de Knowledge Graph](08_GRAPH/definiciones_knowledge_graph.md)
- [Creación de Knowledge Graphs](08_GRAPH/creacion_de_knowledge_graphs.md)
- [Grafo de código](08_GRAPH/grafo_de_codigo.md)
- [Representation learning en grafos](08_GRAPH/representation_learning_en_grafos.md)
- [Apache TinkerPop](08_GRAPH/apache_tinkerpop.md) · [Gremlin](08_GRAPH/gremlin.md)
- [Servidores MCP con KGs](08_GRAPH/servidores_mcp_con_kgs.md)
- [Proyectos Apache para KG](08_GRAPH/proyectos_apache_para_kg.md)
- [Knowledge Graphs y blockchain](08_GRAPH/knowledge_graphs_y_blockchain.md)

### 09 · Sistemas de ML
- [Proyectos generales de ML](09_SYSTEMS/proyectos_generales_de_ml.md)
- [PYMK — People You May Know](09_SYSTEMS/PYMK/pymk.md)
- Recomendadores:
  [basados en KG](09_SYSTEMS/REC_SYSTEM/introduccion_recomendadores_con_kg.md) ·
  [GNNs y Transformers](09_SYSTEMS/REC_SYSTEM/gnn_y_transformers.md)

### 10 · LLM
- [Introducción a los LLMs](10_LLM/introduccion.md)
- [LLMs open source](10_LLM/llms_open_source.md) ·
  [requerimientos de hardware](10_LLM/requerimientos_de_hardware.md) ·
  [prompting](10_LLM/prompting.md)
- MCP: [introducción](10_LLM/MCP/introduccion_mcp.md) ·
  [clientes](10_LLM/MCP/clientes_mcp.md) ·
  [servidor de filesystem](10_LLM/MCP/servidor_mcp_filesystem.md) ·
  [manejo de contexto](10_LLM/MCP/manejo_de_contexto.md)
- RAGs: [chatbot con LangChain](10_LLM/RAGS/chatbot_rag_con_langchain.md) ·
  [documentación técnica](10_LLM/RAGS/rag_para_documentacion_tecnica.md) ·
  [de RAGs a LLM-Wiki](10_LLM/RAGS/de_rags_a_llm_wiki.md) ·
  [LangChain](10_LLM/RAGS/langchain.md) ·
  [Cypher](10_LLM/RAGS/cypher.md)
- [LM Studio](10_LLM/llmstudio/introduccion_lm_studio.md) ·
  [LLMs locales](10_LLM/LOCAL_LLM/llms_locales.md)

### 11 · JARVIS
- [Introducción](11_JARVIS/introduccion.md)
- [Plan de trabajo](11_JARVIS/iterations/plan_de_trabajo.md)
- [Desarrollo orientado a ontologías](11_JARVIS/desarrollo_orientado_a_ontologias.md) ·
  [sistema de ontologías](11_JARVIS/sistema_de_ontologias.md)
- [LangGraph](11_JARVIS/llm_workflows/langgraph.md)
- [Prompt: Puzzle Solver](11_JARVIS/prompts/puzzle_solver.md)

### 12 · Series de tiempo
- [Introducción](12_TIME_SERIES/introduccion.md)

### 13 · Problemas
- [Titanic](13_PROBLEMS/titanic/titanic.md)

### Proyectos
- [Knowledge Graph para developers](PROYECTOS/KG_CODE/knowledge_graph_para_developers.md)

---

## En construcción

- **Torch (06)** — solo hay código de ejemplo en `docs/06_TORCH/codes/`, sin notas todavía.
- **Métricas y evaluación de modelos** — pendiente de desarrollar dentro de
  [Sistemas de ML](09_SYSTEMS/proyectos_generales_de_ml.md).
