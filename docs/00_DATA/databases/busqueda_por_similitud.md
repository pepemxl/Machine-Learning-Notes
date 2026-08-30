# Búsqueda por Similitud

La **búsqueda por similitud** consiste en encontrar, dado un vector de consulta, los $k$ vectores
más parecidos dentro de una colección. Es la operación que sostiene los sistemas de
[recomendación](../../09_SYSTEMS/REC_SYSTEM/introduccion_recomendadores_con_kg.md), la búsqueda
semántica y la recuperación en las arquitecturas
[RAG](../../10_LLM/RAGS/chatbot_rag_con_langchain.md).

## Por qué no basta con la fuerza bruta

La versión exacta del problema —**k-NN**— es trivial de escribir: calcula la distancia de la
consulta a los $N$ vectores y quédate con los $k$ menores. Su coste es $O(N \cdot d)$.

Con 10 000 documentos y 768 dimensiones eso es perfectamente viable. Con 100 millones de
vectores, cada consulta requiere 76 800 millones de operaciones. No hay servidor que sirva eso
con latencia interactiva.

De ahí que se renuncie a la exactitud: **ANN** (*approximate nearest neighbor*) devuelve
*casi siempre* los vecinos correctos, a cambio de ser órdenes de magnitud más rápido.

## Medir el error: recall

Como el resultado es aproximado, hace falta una métrica de calidad. La estándar es el
**recall@k**: qué fracción de los $k$ vecinos verdaderos aparece entre los $k$ devueltos.

$$\text{recall@}k = \frac{|\text{devueltos}_k \cap \text{verdaderos}_k|}{k}$$

Un recall de 0.95 en top-10 significa que, de media, 9.5 de los 10 vecinos reales estaban en la
respuesta. Para búsqueda semántica eso suele ser indistinguible de la perfección; para
*deduplicación* exacta, no.

Calcular el recall exige conocer la verdad de referencia, así que se mide **una vez, offline**,
sobre una muestra de consultas y con fuerza bruta como referencia.

## Métricas de distancia

Elegir mal la métrica invalida los resultados con independencia del índice.

| Métrica | Fórmula | Orden | Cuándo |
|---|---|---|---|
| **L2** (euclídea) | $\|x - y\|_2$ | Menor = más cercano | Vectores donde la magnitud significa algo |
| **IP** (producto interno) | $x \cdot y$ | Mayor = más similar | Recomendadores con factores latentes |
| **COSINE** | $\frac{x \cdot y}{\|x\|\|y\|}$ | Mayor = más similar | Embeddings de texto. La opción por defecto |
| **HAMMING** | Bits distintos | Menor = más cercano | Vectores binarios |
| **JACCARD** | Intersección / unión | Menor = más cercano | Conjuntos, huellas binarias |

Dos consecuencias prácticas:

- **Los resultados se ordenan en sentidos opuestos.** Con L2 la lista va de menor a mayor; con
  COSINE e IP, de mayor a menor. Si asumes un orden y usas el otro, obtienes los vectores *más
  lejanos*.
- **Sobre vectores normalizados, COSINE e IP son equivalentes**, y ordenan igual que L2. Muchos
  modelos de embeddings ya devuelven vectores normalizados; en ese caso da lo mismo cuál uses,
  pero la métrica del índice debe coincidir con la que asumes al interpretar.

La regla útil: **usa la misma métrica con la que se entrenó el modelo de embeddings**. Para casi
todos los modelos de texto modernos, eso es coseno.

## Familias de índices

### FLAT — sin índice

Fuerza bruta. Recall 1.0 por definición, sin parámetros que ajustar y sin coste de construcción.

Es la elección **correcta** por debajo de unos 100 000 vectores: a esa escala el escaneo completo
tarda milisegundos y evitas toda la complejidad. También es la referencia contra la que se mide
el recall de los demás.

### IVF — particionado por clusters

Agrupa los vectores en `nlist` clusters con k-means. En la búsqueda, compara la consulta con los
centroides, escoge los `nprobe` clusters más prometedores y solo escanea esos.

- `nlist` — número de clusters. Se fija al **construir**. Heurística habitual: $\sqrt{N}$.
- `nprobe` — clusters a escanear. Se fija en **cada consulta**. Es el mando de recall.

Su punto débil es estructural: si el vecino real cae en un cluster que no se escaneó, se pierde
para siempre. Con `nprobe = nlist` degenera en fuerza bruta.

### HNSW — grafo navegable

Construye un **grafo multicapa** de vecindad. Las capas superiores tienen pocos nodos y enlaces
largos —permiten saltar lejos rápido—; las inferiores son densas y afinan. La búsqueda desciende
por capas siguiendo siempre el vecino más cercano a la consulta.

- `M` — enlaces por nodo. Se fija al construir. Más `M`, mejor recall y más memoria.
- `efConstruction` — esfuerzo al construir. Más alto, mejor grafo y construcción más lenta.
- `ef` — tamaño de la lista de candidatos en la búsqueda. Es el mando de recall.

Es el índice **por defecto razonable** para la mayoría de casos: excelente relación
recall/latencia. Su coste es la memoria, ya que el grafo entero debe residir en RAM.

### Cuantización — comprimir los vectores

Reducen la memoria a costa de precisión, y se combinan con las familias anteriores:

- **SQ** (*scalar quantization*) — cada dimensión de `float32` a `int8`. Reduce ~4x con pérdida
  pequeña.
- **PQ** (*product quantization*) — divide el vector en subvectores y sustituye cada uno por el
  índice de su centroide en un diccionario. Reduce 10–50x, con pérdida notable.

### DiskANN — más allá de la RAM

Mantiene el grafo en **SSD** y solo un resumen en memoria. Permite servir miles de millones de
vectores en una máquina, a costa de latencia mayor. Tiene sentido cuando el conjunto no cabe en
RAM y replicarlo saldría más caro que el disco.

## El compromiso recall / latencia

Los parámetros de búsqueda no son detalles de afinado: mueven el recall de forma drástica.

Las cifras siguientes están **medidas**, no estimadas: 20 000 vectores de 64 dimensiones, 50
consultas, recall@10 contra fuerza bruta con NumPy, sobre Milvus Lite 3.2.1.

**HNSW** (`M=16`, `efConstruction=200`) — variando `ef`:

| `ef` | recall@10 | ms/consulta |
|---|---|---|
| 10 | 0.506 | 0.48 |
| 32 | 0.786 | 0.51 |
| 64 | 0.908 | 0.50 |
| 128 | 0.972 | 0.50 |
| 256 | 0.994 | 0.49 |

**IVF_FLAT** (`nlist=256`) — variando `nprobe`:

| `nprobe` | recall@10 | ms/consulta |
|---|---|---|
| 1 | 0.066 | 0.51 |
| 4 | 0.180 | 0.51 |
| 16 | 0.484 | 0.51 |
| 64 | 0.930 | 0.53 |
| 256 | 1.000 | 1.18 |

**FLAT** (exacto): recall 1.000 en 3.51 ms/consulta.

Tres lecturas:

1. **El mando de recall funciona y es enorme.** En HNSW, cambiar `ef` de 10 a 256 lleva el
   recall de 0.51 a 0.99. Un `ef` mal puesto tira la mitad de los resultados buenos, en silencio.
2. **IVF con `nprobe` bajo es casi inútil.** Con `nprobe=1` sobre 256 clusters, el recall es
   0.066. La configuración por defecto de un índice IVF rara vez sirve tal cual.
3. **A esta escala, HNSW alcanza recall 0.99 en ~1/7 del tiempo de FLAT.** Y la diferencia de
   latencia entre valores de `ef` es despreciable con 20 000 vectores: el coste de subir el
   recall solo se nota al crecer $N$. Con millones de vectores, esas columnas de milisegundos se
   separan mucho.

!!! warning "Estas cifras no son una tabla de rendimiento universal"
    Con 20 000 vectores las latencias están dominadas por sobrecarga fija, no por la búsqueda. La
    conclusión transferible es **la forma de las curvas de recall**, no los milisegundos.
    Mide siempre con tus propios datos, tu dimensionalidad y tu volumen.

## Filtrado y búsqueda vectorial

Un caso muy común es *"los 10 productos más similares **de la categoría X**"*. Combinar filtro y
ANN tiene truco, y hay dos estrategias con fallos opuestos:

- **Post-filtrado** — busca $k$ vecinos y luego descarta los que no cumplen. Rápido, pero si el
  filtro es selectivo puedes acabar con **menos de $k$ resultados**, o ninguno.
- **Pre-filtrado** — determina primero el subconjunto válido y busca solo ahí. Correcto, pero si
  el subconjunto es grande se acerca a la fuerza bruta.

Los motores serios implementan **filtrado durante el recorrido** del índice, evaluando el
predicado mientras navegan el grafo o los clusters. Es lo que hace
[Milvus](milvus.md#busqueda-con-filtros), y es la razón para usar una base de datos vectorial en
lugar de una librería de índices suelta.

## Cómo elegir

| Situación | Índice |
|---|---|
| Menos de ~100 000 vectores | **FLAT**. No te compliques |
| Caso general, cabe en RAM | **HNSW** |
| Prioridad a la memoria sobre el recall | **IVF_SQ8** o **IVF_PQ** |
| No cabe en RAM | **DiskANN** |
| Inserciones muy frecuentes | **IVF** reconstruye mejor que HNSW |
| Hay GPU y el volumen es grande | Índices GPU (`GPU_CAGRA`, `GPU_IVF_FLAT`) |

## Ver también

- [Milvus](milvus.md) — una implementación completa de todo esto.
- [Bases de datos vectoriales](bases_de_datos_vectoriales.md)
- [GNNs y Transformers](../../09_SYSTEMS/REC_SYSTEM/gnn_y_transformers.md) — de dónde salen los
  embeddings en un recomendador.

## Referencias

- Malkov, Y. A. y Yashunin, D. A. [*Efficient and robust approximate nearest neighbor search
  using HNSW graphs*](https://arxiv.org/abs/1603.09320) (2016).
- Jégou, H., Douze, M. y Schmid, C. *Product Quantization for Nearest Neighbor Search*, IEEE
  TPAMI (2011).
- [ann-benchmarks.com](https://ann-benchmarks.com/) — comparativas reproducibles entre
  bibliotecas ANN.
