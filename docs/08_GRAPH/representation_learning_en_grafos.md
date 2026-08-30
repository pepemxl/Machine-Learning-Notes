# Representation Learning en Grafos

El *representation learning* sobre grafos busca convertir nodos, aristas o grafos completos en
**vectores densos** (*embeddings*) que preserven la estructura del grafo, de modo que se puedan
alimentar a modelos de machine learning convencionales.

## Métodos de embedding de nodos

Basados en recorridos aleatorios sobre el grafo:

- **DeepWalk** — genera recorridos aleatorios y los trata como "frases" para entrenar un modelo
  tipo *word2vec*.
- **Node2Vec** — generaliza DeepWalk con dos parámetros que interpolan entre exploración en
  anchura (estructura local, roles) y en profundidad (comunidades).

## Redes neuronales de grafos (GNN)

Aprenden agregando información del vecindario de cada nodo, capa a capa:

- **GCN** (*Graph Convolutional Network*) — agregación promediada sobre vecinos.
- **GraphSAGE** — muestrea un subconjunto de vecinos, lo que permite escalar e **inferir sobre
  nodos no vistos** durante el entrenamiento.
- **GAT** (*Graph Attention Network*) — pondera a cada vecino mediante atención.

Ver [GNNs y Transformers](../09_SYSTEMS/REC_SYSTEM/gnn_y_transformers.md) para su aplicación en
sistemas de recomendación.

## Graph Transformers

Aplican atención global sobre todo el grafo en lugar de limitarse al vecindario inmediato, lo
que evita el problema del *over-smoothing* de las GNN profundas, a costa de un coste cuadrático
en el número de nodos.

## Knowledge graphs y razonamiento

Embeddings pensados para tripletas (sujeto, predicado, objeto):

- **TransE** — modela la relación como una traslación en el espacio de embeddings:
  $h + r \approx t$.
- **BetaE** — permite consultas lógicas complejas, incluida la negación, sobre el grafo.

## Escalar a grafos grandes

Los retos principales al crecer:

- **Consistencia** entre particiones del grafo.
- **Muestreo de vecindario** para acotar el coste por nodo.
- **Particionamiento** que minimice las aristas cortadas entre máquinas.

Ver [Clustering en Big Data](../02_UNSUPERVISED_LEARNING/clustering_en_big_data.md) y
[PySpark](../00_DATA/spark/pyspark.md).
