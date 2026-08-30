# Knowledge Graph para developers.

Este proyecto consiste en crear un **Knowledge Graph** a partir de una API desarrollada en un monorepo en Python, que contiene código mixto de APIs, como pueden ser:

- **REST**, 
- **GraphQL**,
- **gRPC**,
- **WebSocket**,
- **Webhook**,
- **MQTT**,
- **SOAP**,
- **Apache Kafka**,
- **Falcor**,
- **JSON-RPC** / **XML-RPC**

junto con lógica de negocio, lo cual implica 

- analizar el código fuente, 
- definir y extraer entidades, relaciones y metadatos relevantes, y estructurarlos en un grafo.


| Protocolo       | Cuando usarlo                                  | Ejemplo de Uso                  |
|-----------------|-----------------------------------------------|----------------------------------|
| **gRPC**        | Microservicios, alta velocidad               | Backend en Go llamando a Rust    |
| **WebSocket**   | Tiempo real                                  | Chat, trading                   |
| **Webhook**     | Eventos asincrónicos                         | Notificaciones de pagos (Stripe) |
| **MQTT**        | IoT, baja energía                            | Sensores en una fábrica          |
| **SOAP**        | Sistemas legacy (empresas)                   | Bancos, hospitales               |
| **Kafka**       | Procesamiento de eventos a gran escala       | Logs de aplicaciones distribuidas|
| **JSON-RPC**    | APIs simples y ligeras                      | Blockchain (Ethereum)            |


## Definir el caso de uso y el propósito del grafo de conocimiento

Antes de construir el grafo, es crucial entender qué información quieres capturar y cómo se usará. En este caso, el grafo de conocimiento podría:
- Mapear **dependencias** entre módulos, clases, funciones y endpoint/operación de la API (REST y GraphQL).
- Representar la **lógica de negocio** (reglas, procesos, flujos de datos).
- Documentar las **relaciones** entre endpoints, esquemas GraphQL, modelos de datos y funciones de negocio.
- Facilitar el análisis de código, la detección de código muerto, o la integración con asistentes de IA (como Claude con MCP).

Responder preguntas como:

- ¿Qué funciones de negocio son utilizadas por un endpoint específico de REST o operación en GraphQL?
- ¿Qué dependencias existen entre módulos en el monorepo?
- ¿Cómo se conectan los esquemas de GraphQL con las tablas de la base de datos?

### **2. Herramientas y tecnologías recomendadas**

Para construir el grafo, usaremos herramientas que analicen el código fuente, manejen grafos y se integren con APIs. 

Lista de herramientas relevantes:

- **Análisis de código Python**: 
  - **Doxygen**: Doxygen tiene soporte integrado para generar diagramas de herencia para clases C++, sin embargo puede ser usada para Python.
  - **libcst** o **ast**: Para analizar el árbol de sintaxis abstracta (AST) del código Python y extraer clases, funciones, importaciones, etc.
  - **pydeps**: Para analizar dependencias entre módulos en el monorepo.
  - **pylint** o **flake8**: Para identificar código muerto o dependencias no utilizadas.

- **Manejo de APIs REST y GraphQL**:
  - **Ariadne** o **Graphene**: Si tu monorepo usa estas bibliotecas para GraphQL, puedes inspeccionar sus esquemas y resolvers.
  - **Flask** o **FastAPI**: Para endpoints REST, puedes analizar las rutas y sus funciones asociadas.
  - **requests** o **gql**: Para consumir y analizar las APIs internamente si necesitas extraer datos dinámicos.

- **Bases de datos de grafos**:
  - **Apache AGE**: Extensión de PostgreSQL para grafos, ideal para combinar datos relacionales y de grafos.[](https://neo4j.com/blog/knowledge-graph/how-to-build-knowledge-graph/)
  - **Neo4j**: Popular base de datos de grafos, con soporte para Python a través de `neo4j` o `py2neo`.
  - **Cognee**: Herramienta para crear grafos de conocimiento desde repositorios Python, con soporte para bases de datos de grafos como FalkorDB.[](https://www.cognee.ai/blog/deep-dives/repo-to-knowledge-graph)
  - **Apache TinkerPop (Gremlin)**: Framework para consultas de grafos, compatible con varias bases de datos de grafos.

- **Procesamiento de lenguaje natural (NLP) y embeddings**:
  - **spaCy** o **NLTK**: Para extraer entidades y relaciones si el código contiene comentarios o documentación en texto natural.
  - **PyKEEN** o **AmpliGraph**: Para generar embeddings de grafos de conocimiento, útiles para análisis semántico.[](https://memgraph.com/blog/best-python-packages-tools-for-knowledge-graphs)
  - **OpenAIEmbeddings** (con modelos como GPT): Para generar embeddings de código o documentación.[](https://neo4j.com/blog/news/graphrag-python-package/)

- **Otras herramientas**:
  - **NetworkX**: Biblioteca Python para crear y visualizar grafos localmente.
  - **Cognee**: Simplifica la creación de grafos de conocimiento desde repositorios Python, con soporte para bases de datos relacionales, de grafos y vectoriales.[](https://www.cognee.ai/blog/deep-dives/repo-to-knowledge-graph)

---

### **3. Pasos para crear el grafo de conocimiento**
A continuación, detallo un proceso estructurado para construir el grafo de conocimiento desde el monorepo:

#### **Paso 1: Analizar la estructura del monorepo**
- **Objetivo**: Identificar módulos, clases, funciones, endpoints REST y esquemas GraphQL.
- **Acciones**:
  - Usa **libcst** para recorrer el código fuente y extraer:
    - **Módulos**: Archivos Python y sus importaciones.
    - **Clases y funciones**: Definiciones de clases, métodos y funciones independientes.
    - **Endpoints REST**: Si usas Flask o FastAPI, identifica decoradores como `@app.route` o `@app.get`.
    - **Esquemas GraphQL**: Busca definiciones de tipos (`GraphQLObjectType`) o resolvers en Ariadne/Graphene.
  - Usa **pydeps** para mapear dependencias entre módulos:
    ```bash
    pip install pydeps
    pydeps /ruta/al/monorepo --show-deps
    ```
    Esto genera un grafo de dependencias que puedes exportar como JSON o DOT.

- **Ejemplo con libcst**:
  ```python
  import libcst as cst
  from libcst.metadata import FullyQualifiedNameProvider, PositionProvider
  import os

  class CodeVisitor(cst.CSTVisitor):
      METADATA_DEPENDENCIES = {FullyQualifiedNameProvider, PositionProvider}

      def visit_FunctionDef(self, node):
          print(f"Función encontrada: {node.name.value}")
      def visit_ClassDef(self, node):
          print(f"Clase encontrada: {node.name.value}")

  for root, _, files in os.walk("/ruta/al/monorepo"):
      for file in files:
          if file.endswith(".py"):
              with open(os.path.join(root, file), "r") as f:
                  source = f.read()
              module = cst.parse_module(source)
              wrapper = cst.MetadataWrapper(module)
              wrapper.visit(CodeVisitor())
  ```
  Esto identifica funciones y clases en el monorepo.

#### **Paso 2: Extraer entidades y relaciones**
- **Entidades**:
  - **Módulos**: Archivos Python (e.g., `api/rest/endpoints.py`).
  - **Clases**: Modelos de datos o controladores (e.g., `User`, `Order`).
  - **Funciones**: Lógica de negocio (e.g., `calculate_price`).
  - **Endpoints REST**: Rutas como `/users/{id}`.
  - **Tipos GraphQL**: Tipos como `UserType`, `Query`, `Mutation`.
  - **Resolvers GraphQL**: Funciones que resuelven consultas o mutaciones.

- **Relaciones**:
  - **Importaciones**: Un módulo importa otro (e.g., `endpoints.py` -> `models.py`).
  - **Llamadas**: Una función llama a otra (e.g., `get_user` -> `validate_user`).
  - **Uso de datos**: Un endpoint usa un modelo o una función de negocio.
  - **Dependencias GraphQL**: Un resolver depende de una función o modelo.

- **Herramienta sugerida**: Usa **Cognee** para automatizar la extracción de entidades y relaciones desde el código fuente. Cognee crea un grafo de dependencias y lo transforma en un grafo de conocimiento, almacenándolo en una base de datos de grafos como Neo4j o FalkorDB.[](https://www.cognee.ai/blog/deep-dives/repo-to-knowledge-graph)

- **Ejemplo con Cognee**:
  ```python
  from cognee import CodeFile, add, graph

  # Definir una clase para representar archivos de código
  class CodeFile:
      def __init__(self, name, source_code, depends_on=None):
          self.name = name
          self.source_code = source_code
          self.depends_on = depends_on or []

  # Añadir archivos al grafo
  code_files = [
      CodeFile("endpoints.py", "from models import User\n@app.get('/users')", depends_on=["models.py"]),
      CodeFile("models.py", "class User: pass", depends_on=[]),
      CodeFile("resolvers.py", "from models import User\nUserType", depends_on=["models.py"])
  ]

  for file in code_files:
      add(file)

  # Generar el grafo
  graph()
  ```
  Esto crea nodos para los archivos y relaciones para las dependencias (`depends_on`).

#### **Paso 3: Almacenar el grafo en una base de datos**
- **Opción 1: Apache AGE** (extensión de PostgreSQL para grafos):
  - Configura una base de datos PostgreSQL con la extensión AGE instalada.
  - Crea un grafo con nodos para entidades (módulos, clases, funciones, endpoints, tipos GraphQL) y relaciones (importaciones, llamadas, uso).
  - Usa Cypher para insertar datos:
    ```cypher
    CREATE (m1:Module {name: 'endpoints.py'})
    CREATE (m2:Module {name: 'models.py'})
    CREATE (m1)-[:IMPORTS]->(m2)
    ```
  - Conecta desde Python usando `psycopg2` o el driver de AGE:
    ```python
    from age import GraphDatabase

    driver = GraphDatabase.driver("postgresql://user:pass@localhost:5432/dbname")
    with driver.session() as session:
        session.run("CREATE (m1:Module {name: 'endpoints.py'})")
        session.run("CREATE (m1)-[:IMPORTS]->(m2:Module {name: 'models.py'})")
    ```

- **Opción 2: Neo4j**:
  - Usa el driver de Neo4j para Python:
    ```python
    from neo4j import GraphDatabase

    driver = GraphDatabase.driver("neo4j://localhost:7687", auth=("neo4j", "password"))
    def create_module(tx, name):
        tx.run("CREATE (m:Module {name: $name})", name=name)

    with driver.session() as session:
        session.write_transaction(create_module, "endpoints.py")
    ```
  - Neo4j es ideal para grafos complejos y tiene una interfaz visual (Neo4j Browser) para explorar el grafo.[](https://neo4j.com/blog/knowledge-graph/how-to-build-knowledge-graph/)

- **Opción 3: NetworkX** (para prototipos locales):
  - Si no necesitas una base de datos persistente, usa NetworkX para crear y visualizar el grafo en memoria:
    ```python
    import networkx as nx
    import matplotlib.pyplot as plt

    G = nx.DiGraph()
    G.add_node("endpoints.py")
    G.add_node("models.py")
    G.add_edge("endpoints.py", "models.py", type="IMPORTS")
    nx.draw(G, with_labels=True)
    plt.show()
    ```

#### **Paso 4: Extraer lógica de negocio**
- **Objetivo**: Identificar reglas de negocio y flujos de datos en el código.
- **Acciones**:
  - Usa **libcst** para analizar funciones y métodos que implementen lógica de negocio (e.g., validaciones, cálculos, transformaciones).
  - Extrae comentarios o docstrings con **spaCy** para identificar reglas semánticas:
    ```python
    import spacy

    nlp = spacy.load("en_core_web_sm")
    docstring = "Calculates the total price of an order based on items and discounts."
    doc = nlp(docstring)
    for ent in doc.ents:
        print(ent.text, ent.label_)  # e.g., "order" (ENTITY), "price" (ENTITY)
    ```
  - Crea nodos para reglas de negocio y relaciones con funciones o endpoints:
    ```cypher
    CREATE (r:Rule {name: 'CalculateTotalPrice'})
    CREATE (f:Function {name: 'calculate_price'})
    CREATE (r)-[:IMPLEMENTED_BY]->(f)
    ```

#### **Paso 5: Integrar con APIs REST y GraphQL**
- **REST**:
  - Analiza decoradores de Flask/FastAPI para identificar rutas y sus funciones asociadas.
  - Crea nodos para endpoints y relaciones con funciones de negocio:
    ```python
    from flask import Flask

    app = Flask(__name__)
    @app.route('/users/<id>')
    def get_user(id):
        return {"id": id}

    # Extraer rutas
    for rule in app.url_map.iter_rules():
        print(f"Endpoint: {rule.endpoint}, Path: {rule}")
        # Añadir al grafo
        with driver.session() as session:
            session.run("CREATE (e:Endpoint {path: $path})", path=str(rule))
    ```

- **GraphQL**:
  - Si usas Ariadne o Graphene, analiza el esquema para extraer tipos y resolvers:
    ```python
    from ariadne import gql, make_executable_schema

    type_defs = gql("""
        type Query {
            user(id: ID!): User
        }
        type User {
            id: ID!
            name: String!
        }
    """)
    # Extraer tipos
    schema = make_executable_schema(type_defs, [])
    for type_name in schema.type_map:
        print(f"Tipo GraphQL: {type_name}")
        # Añadir al grafo
        with driver.session() as session:
            session.run("CREATE (t:GraphQLType {name: $name})", name=type_name)
    ```
  - Conecta resolvers a funciones de negocio:
    ```cypher
    CREATE (t:GraphQLType {name: 'User'})
    CREATE (f:Function {name: 'get_user'})
    CREATE (t)-[:RESOLVED_BY]->(f)
    ```

#### **Paso 6: Generar embeddings (opcional)**
- Usa **PyKEEN** o **AmpliGraph** para generar embeddings de nodos y relaciones, útiles para búsquedas semánticas o detección de patrones:
  ```python
  from pykeen.models import TransE
  from pykeen.triples import TriplesFactory

  triples = [
      ('endpoints.py', 'IMPORTS', 'models.py'),
      ('UserType', 'RESOLVED_BY', 'get_user')
  ]
  tf = TriplesFactory.from_labeled_triples(triples)
  model = TransE(triples_factory=tf)
  model.train()
  ```
  Esto genera representaciones vectoriales para entidades y relaciones, que pueden integrarse con un servidor MCP para consultas avanzadas.[](https://memgraph.com/blog/best-python-packages-tools-for-knowledge-graphs)

#### **Paso 7: Visualizar y consultar el grafo**
- **Visualización**:
  - Usa Neo4j Browser o NetworkX para visualizar el grafo.
  - Ejemplo con NetworkX:
    ```python
    nx.draw(G, with_labels=True, node_color='lightblue', edge_color='gray')
    plt.show()
    ```

- **Consultas**:
  - Usa Cypher (en Neo4j o AGE) para responder preguntas:
    ```cypher
    MATCH (e:Endpoint)-[:USES]->(f:Function)
    WHERE e.path = '/users/{id}'
    RETURN f.name
    ```
    Esto devuelve las funciones usadas por un endpoint específico.

- **Integración con MCP** (opcional):
  - Configura un **Knowledge Graph MCP Server** para conectar el grafo con Claude:
    ```bash
    npx -y @modelcontextprotocol/server-memory --memory-path ./knowledge_graph.jsonl
    ```
  - Usa un archivo de configuración como:
    ```json
    {
      "mcpServers": {
        "knowledge_graph": {
          "command": "npx",
          "args": ["-y", "@modelcontextprotocol/server-memory", "--memory-path", "./knowledge_graph.jsonl"],
          "autoapprove": ["create_entities", "read_graph", "search_nodes"]
        }
      }
    }
    ```
  - Claude puede consultar el grafo para responder preguntas como "Qué funciones usa el endpoint /users?".

---

### **4. Ejemplo práctico: Estructura del grafo**
Supongamos que tu monorepo tiene:
- `endpoints.py`: Define un endpoint REST `/users` que usa `get_user`.
- `resolvers.py`: Define un resolver GraphQL `user` que usa `get_user`.
- `models.py`: Contiene la clase `User`.
- `business_logic.py`: Contiene la función `get_user`.

El grafo podría representarse como:
- **Nodos**: `endpoints.py` (Module), `resolvers.py` (Module), `models.py` (Module), `get_user` (Function), `User` (Class), `/users` (Endpoint), `UserType` (GraphQLType).
- **Relaciones**:
  - `endpoints.py` -> `IMPORTS` -> `models.py`
  - `resolvers.py` -> `IMPORTS` -> `models.py`
  - `/users` -> `USES` -> `get_user`
  - `UserType` -> `RESOLVED_BY` -> `get_user`
  - `get_user` -> `USES` -> `User`

En Cypher (Neo4j/AGE):
```cypher
CREATE (e:Endpoint {path: '/users'})
CREATE (r:GraphQLType {name: 'UserType'})
CREATE (f:Function {name: 'get_user'})
CREATE (c:Class {name: 'User'})
CREATE (m1:Module {name: 'endpoints.py'})
CREATE (m2:Module {name: 'resolvers.py'})
CREATE (m3:Module {name: 'models.py'})
CREATE (m1)-[:IMPORTS]->(m3)
CREATE (m2)-[:IMPORTS]->(m3)
CREATE (e)-[:USES]->(f)
CREATE (r)-[:RESOLVED_BY]->(f)
CREATE (f)-[:USES]->(c)
```

---

### **5. Integración con Knowledge Graph MCP Server**
Para conectar el grafo con un **Knowledge Graph MCP Server** y permitir consultas persistentes por parte de Claude:
1. **Almacenar el grafo localmente**:
   - Exporta el grafo a un archivo JSONL (`knowledge_graph.jsonl`) con nodos y relaciones.
   - Ejemplo:
     ```json
     {"entity": {"name": "endpoints.py", "type": "Module"}}
     {"relation": {"from": "endpoints.py", "to": "models.py", "type": "IMPORTS"}}
     ```

2. **Configurar el servidor MCP**:
   - Ejecuta el servidor con:
     ```bash
     npx -y @modelcontextprotocol/server-memory --memory-path ./knowledge_graph.jsonl
     ```
   - Configura Claude Desktop para usar el servidor (ver configuración en la respuesta anterior).

3. **Consultas con Claude**:
   - Usa prompts como:
     ```
     Remembering... Consulta el grafo de conocimiento para encontrar qué funciones usa el endpoint /users.
     ```
   - Claude usará herramientas como `search_nodes` o `read_graph` para devolver respuestas basadas en el grafo.

---

### **6. Mejores prácticas**
- **Automatización**: Usa scripts para actualizar el grafo automáticamente al cambiar el código (e.g., con Git hooks).
- **Escalabilidad**: Usa Neo4j o Apache AGE para grafos grandes; NetworkX para prototipos pequeños.
- **Validación**: Verifica la integridad del grafo con pruebas unitarias (e.g., pytest).
- **Documentación**: Incluye comentarios y docstrings en el código para facilitar la extracción de lógica de negocio con NLP.
- **Seguridad**: Restringe el acceso al servidor MCP y a las bases de datos con autenticación.

---

### **7. Recursos adicionales**
- **Tutorial de Cognee**: Guía para crear grafos desde repositorios Python.[](https://www.cognee.ai/blog/deep-dives/repo-to-knowledge-graph)
- **Neo4j GraphRAG**: Ejemplo de creación de grafos con Python y Neo4j.[](https://neo4j.com/blog/news/graphrag-python-package/)
- **GraphQL con Python**: Guía para analizar esquemas GraphQL con Ariadne o Graphene.[](https://www.apollographql.com/blog/complete-api-guide)[](https://www.activestate.com/blog/how-to-build-a-graphql-server-in-python-with-graphene/)
- **Apache AGE**: Documentación para usar AGE con PostgreSQL: https://age.apache.org/
- **PyKEEN**: Biblioteca para embeddings de grafos: https://pykeen.github.io/

---

### **8. Conclusión**
Crear un grafo de conocimiento desde un monorepo con APIs REST y GraphQL implica analizar el código con herramientas como **libcst** y **pydeps**, extraer entidades (módulos, clases, funciones, endpoints, tipos GraphQL) y relaciones (importaciones, usos, resolvers), y almacenarlas en una base de datos de grafos como **Apache AGE** o **Neo4j**. Herramientas como **Cognee** simplifican el proceso, y la integración con un **Knowledge Graph MCP Server** permite a modelos como Claude consultar el grafo para proporcionar respuestas contextuales. Este enfoque es escalable y puede adaptarse para análisis de código, documentación automática o integración con asistentes de IA.

Si necesitas un ejemplo de código más detallado para un caso específico (e.g., un endpoint REST o un resolver GraphQL particular) o ayuda con la configuración de alguna herramienta, indícalos y puedo profundizar.[](https://neo4j.com/blog/news/graphrag-python-package/)[](https://www.activestate.com/blog/how-to-build-a-graphql-server-in-python-with-graphene/)[](https://www.cognee.ai/blog/deep-dives/repo-to-knowledge-graph)


