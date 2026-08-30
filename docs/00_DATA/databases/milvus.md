# Milvus

**Milvus** es una base de datos vectorial de código abierto, orientada a la
[búsqueda por similitud](busqueda_por_similitud.md) a gran escala. Está desarrollada por Zilliz
y es un proyecto graduado de la **LF AI & Data Foundation**, bajo licencia Apache 2.0.

Su motor de índices, **Knowhere**, envuelve implementaciones consolidadas —FAISS, HNSWlib,
DiskANN— y las expone tras una interfaz común. Lo que Milvus aporta por encima de una librería
de índices suelta es lo que hace falta para producción: persistencia, escalado horizontal,
control de consistencia, filtrado por campos escalares, y borrados y actualizaciones reales.

## Modelo de datos

| Concepto | Equivalente relacional | Descripción |
|---|---|---|
| **Collection** | Tabla | El contenedor principal |
| **Entity** | Fila | Un registro: su clave primaria, uno o varios vectores y campos escalares |
| **Field** | Columna | Con tipo: `FLOAT_VECTOR`, `VARCHAR`, `INT64`, `JSON`, `ARRAY`… |
| **Schema** | DDL | La definición de los campos de la colección |
| **Partition** | Partición | División lógica; permite acotar la búsqueda |
| **Segment** | — | Unidad física interna. Los *growing* reciben inserciones; al sellarse se indexan |
| **Index** | Índice | Se define **por campo vectorial**, con su tipo y su métrica |

Un detalle que distingue a Milvus de un índice ANN puro: una colección puede tener **varios
campos vectoriales** —por ejemplo el embedding del texto y el de la imagen— y buscar sobre ambos
combinando los resultados (*hybrid search*).

## Modos de despliegue

Los tres comparten la misma API cliente, así que se prototipa en el primero y se despliega en el
tercero sin reescribir el código.

| Modo | Cómo se arranca | Para qué |
|---|---|---|
| **Milvus Lite** | `pip install "pymilvus[milvus-lite]"` | Embebido en el proceso Python, guarda en un fichero local. Prototipos, tests y notebooks. Linux y macOS |
| **Standalone** | Un contenedor Docker (con etcd y MinIO) | Una sola máquina. Desarrollo y producción pequeña |
| **Distributed** | Kubernetes, vía Helm u operador | Producción a escala: los componentes escalan por separado |

En el modo distribuido la arquitectura está **desagregada**: la capa de acceso (*proxy*), la de
coordinación, los nodos de trabajo (consulta, datos, índice) y el almacenamiento son
independientes. El estado vive fuera de los nodos de cómputo —metadatos en etcd, log de
operaciones en Pulsar o Kafka, y los datos en almacenamiento de objetos tipo S3 o MinIO—, que es
lo que permite escalar la lectura sin tocar la escritura.

## Uso

```bash
pip install "pymilvus[milvus-lite]"
```

### Crear una colección

La vía rápida, para cuando solo necesitas id y vector:

```python
from pymilvus import MilvusClient

cli = MilvusClient("demo.db")          # fichero local con Milvus Lite
cli.create_collection("articulos", dimension=768)
```

Con Standalone o Distributed, lo único que cambia es la conexión:

```python
cli = MilvusClient(uri="http://localhost:19530", token="usuario:contraseña")
```

Para algo real conviene declarar el esquema y el índice de forma explícita:

```python
from pymilvus import MilvusClient, DataType

DIM = 8
cli = MilvusClient("demo.db")

esquema = cli.create_schema(auto_id=False, enable_dynamic_field=True)
esquema.add_field("id", DataType.INT64, is_primary=True)
esquema.add_field("vector", DataType.FLOAT_VECTOR, dim=DIM)
esquema.add_field("categoria", DataType.VARCHAR, max_length=64)
esquema.add_field("precio", DataType.FLOAT)

indice = cli.prepare_index_params()
indice.add_index(
    field_name="vector",
    index_type="HNSW",
    metric_type="COSINE",
    params={"M": 16, "efConstruction": 200},
)

cli.create_collection("articulos", schema=esquema, index_params=indice)
```

`enable_dynamic_field=True` permite insertar campos que **no están en el esquema**: se guardan en
un JSON interno y siguen sirviendo para filtrar. Es cómodo mientras el modelo de datos aún se
mueve.

### Insertar

```python
import numpy as np

rng = np.random.default_rng(0)
categorias = ["libro", "musica", "video"]

filas = [
    {
        "id": i,
        "vector": rng.normal(size=DIM).astype(np.float32).tolist(),
        "categoria": categorias[i % 3],
        "precio": float(round(5 + (i % 20) * 3.5, 2)),
        "stock": int(i % 7),            # campo dinamico: no esta en el esquema
    }
    for i in range(500)
]

r = cli.insert("articulos", filas)
print(r["insert_count"])        # 500
```

### Buscar

```python
consulta = rng.normal(size=DIM).astype(np.float32).tolist()

res = cli.search(
    "articulos",
    data=[consulta],
    limit=3,
    output_fields=["categoria", "precio"],
    search_params={"params": {"ef": 64}},      # el mando de recall de HNSW
)

for h in res[0]:
    print(h["id"], round(h["distance"], 4), h["entity"]["categoria"])
```

```text
63  0.9055 libro
320 0.9013 video
405 0.8643 libro
```

Con `COSINE` las distancias van **de mayor a menor**: el primero es el más parecido. Con `L2`
sería al revés. Ver [métricas de distancia](busqueda_por_similitud.md#metricas-de-distancia).

### Búsqueda con filtros

Aquí es donde una base de datos vectorial gana a un índice suelto: el predicado escalar se evalúa
**durante** el recorrido del índice, no después.

```python
res = cli.search(
    "articulos",
    data=[consulta],
    limit=3,
    filter='categoria == "libro" and precio < 30',
    output_fields=["categoria", "precio"],
)
```

Los campos dinámicos también se pueden filtrar, aunque no estén en el esquema:

```python
res = cli.search("articulos", data=[consulta], limit=2,
                 filter="stock > 5", output_fields=["stock"])
```

Y se puede consultar **sin vector**, como una base de datos normal:

```python
cli.query("articulos",
          filter='categoria == "video" and precio > 60',
          output_fields=["id", "precio"], limit=3)
```

### Actualizar y borrar

```python
cli.upsert("articulos", [{"id": 0, "vector": consulta,
                          "categoria": "libro", "precio": 1.0}])
cli.delete("articulos", ids=[1, 2, 3])
```

El borrado es **lógico**: marca la entidad como eliminada y deja de aparecer en los resultados,
pero el espacio no se recupera hasta la compactación. Con muchos borrados conviene compactar.

## Consistencia

Milvus es un sistema distribuido, así que hay un desfase entre insertar y poder buscar. Se
controla con el nivel de consistencia:

| Nivel | Garantía | Coste |
|---|---|---|
| `Strong` | Ve todo lo escrito antes de la consulta | El más lento |
| `Bounded` | Desfase acotado (por defecto) | Equilibrado |
| `Session` | Ve al menos lo que escribió esta sesión | Barato |
| `Eventually` | Sin garantías de orden | El más rápido |

El valor por defecto, `Bounded`, es el adecuado para búsqueda semántica. Si escribes y lees
inmediatamente en un test, usa `Strong` o el test fallará de forma intermitente.

## Limitaciones de Milvus Lite

Lite es cómodo para aprender y para tests, pero **no es Milvus completo**. Comprobado sobre
`pymilvus` 3.0.1 con `milvus-lite` 3.2.1, solo implementa estos índices:

```text
HNSW, HNSW_SQ, IVF_FLAT, IVF_SQ8, BRUTE_FORCE
```

Pedir cualquier otro —`IVF_PQ`, `DISKANN`, `SCANN`— **no da error al crear la colección**: Milvus
Lite lo acepta y recurre por dentro a búsqueda exhaustiva. Las consultas funcionan y devuelven
resultados correctos, pero no estás midiendo el índice que crees.

Consecuencia práctica: **no evalúes rendimiento ni recall de un índice en Lite** si vas a
desplegar en Standalone o Distributed. Úsalo para validar el código y el modelo de datos, y
compara índices sobre el modo de destino.

## Cuándo usar Milvus

Encaja cuando:

- El volumen supera lo que una librería en memoria sostiene cómodamente —a partir de unos pocos
  millones de vectores— y hace falta **persistencia y escalado horizontal**.
- Necesitas **filtrar por campos escalares** junto con la búsqueda vectorial.
- Hay **actualizaciones y borrados** frecuentes, no solo un índice que se reconstruye entero.

No encaja cuando:

- Tienes **menos de ~100 000 vectores**. Ahí FAISS en memoria, o incluso NumPy, resuelve con una
  fracción de la complejidad operativa.
- Tu carga es fundamentalmente **relacional o analítica** y el vector es un accesorio. Extensiones
  como `pgvector` sobre PostgreSQL evitan añadir otro sistema al stack.

## Ver también

- [Búsqueda por similitud](busqueda_por_similitud.md) — cómo funcionan los índices que usa.
- [Bases de datos vectoriales](bases_de_datos_vectoriales.md)
- [Chatbot RAG con LangChain](../../10_LLM/RAGS/chatbot_rag_con_langchain.md) — el caso de uso
  más habitual.
- [Introducción a bases de datos](../introduccion_bases_de_datos.md)

## Referencias

- [Documentación oficial de Milvus](https://milvus.io/docs)
- [milvus-io/milvus](https://github.com/milvus-io/milvus) — el repositorio.
- [zilliztech/knowhere](https://github.com/zilliztech/knowhere) — el motor de índices.
- Wang, J. et al. *Milvus: A Purpose-Built Vector Data Management System*, SIGMOD (2021).
