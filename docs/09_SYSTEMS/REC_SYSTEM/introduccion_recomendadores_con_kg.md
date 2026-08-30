# Recomendadores Basados en Knowledge Graphs

Al organizar los datos en formato de grafo, la tarea de recomendación se convierte en una tarea
de **predicción de enlaces** (*link prediction*).

## Knowledge Graphs

El término *Knowledge Graph* fue popularizado por Google en 2012 para describir su base de
conocimiento estructurada como grafo, que contenía cientos de millones de entidades y
relaciones. Desde entonces ha desempeñado un papel central en su motor de búsqueda, ofreciendo
respuestas detalladas mediante un panel lateral con información específica sobre las entidades
mencionadas en las consultas del usuario.

De forma más general, un knowledge graph es una **base de conocimiento estructurada como
grafo** que almacena información factual en forma de relaciones entre entidades (o valores
literales). Esto permite modelar entidades del mundo real y sus relaciones, y en consecuencia
da soporte a motores de búsqueda, sistemas de comprensión del lenguaje natural y, más
recientemente, sistemas de recomendación.

Ver [Definiciones de Knowledge Graph](../../08_GRAPH/definiciones_knowledge_graph.md) para la
formalización.

## Recomendadores basados en knowledge graphs

En los últimos años se han usado knowledge graphs en sistemas de recomendación para superar dos
problemas que afectan a los métodos de **filtrado colaborativo** (CF):

- La **escasez** (*sparsity*) de las interacciones usuario-ítem.
- El problema del **arranque en frío** (*cold start*).

Lo consiguen aprovechando las propiedades de ítems y usuarios y representándolas en **una única
estructura de datos**. En lugar de depender solo de qué usuarios interactuaron con qué ítems, el
grafo aporta contexto —atributos, categorías, relaciones entre ítems— que permite recomendar
incluso cuando hay pocas interacciones observadas.

## Ver también

- [GNNs y Transformers](gnn_y_transformers.md) — arquitecturas que operan sobre este tipo de
  grafos.
- [PYMK — People You May Know](../PYMK/pymk.md)
- [Bases de datos vectoriales](../../00_DATA/databases/bases_de_datos_vectoriales.md)
