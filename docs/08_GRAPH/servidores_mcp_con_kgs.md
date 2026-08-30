# MCP servers usando KGs

El **Knowledge Graph MCP Server** es una implementación del **Model Context Protocol (MCP)**, un estándar abierto desarrollado por Anthropic que permite a modelos de inteligencia artificial, como Claude, interactuar con fuentes de datos externas, herramientas y sistemas de almacenamiento de manera segura y estructurada. Este servidor en particular está diseñado para proporcionar memoria persistente a Claude (o cualquier otro modelo de IA compatible con MCP) mediante el uso de grafos de conocimiento locales.

## ¿Qué es el Knowledge Graph MCP Server?

El Knowledge Graph MCP Server es un servidor que utiliza una estructura de grafo de conocimiento para almacenar y gestionar información estructurada, permitiendo a Claude (u otros modelos de IA compatibles con MCP) mantener un contexto persistente a lo largo de múltiples sesiones de conversación. Este servidor organiza los datos en tres componentes principales:

1. Entidades: Representan nodos en el grafo, como personas, organizaciones o eventos, con propiedades como nombres y tipos. Por ejemplo: `{ "entityName": "John_Smith", "type": "Person", "observations": ["Speaks fluent Spanish", "Graduated in 2019"] }`.[](https://github.com/shaneholloman/mcp-knowledge-graph)[](https://www.mcpservers.ai/servers/modelcontextprotocol/Knowledge%2520Graph%2520Memory)
2. Relaciones: Definen conexiones dirigidas entre entidades, siempre en voz activa, describiendo cómo interactúan o se relacionan. Por ejemplo, "John_Smith trabaja_en Empresa_X".
3. Observaciones: Son datos específicos asociados a una entidad, como hechos o atributos (e.g., "Prefers morning meetings").

Esta estructura permite almacenar información de manera organizada y recuperarla de forma eficiente, lo que mejora la capacidad de Claude para recordar información relevante sobre los usuarios o contextos a lo largo del tiempo.

### Características principales
El Knowledge Graph MCP Server ofrece una serie de funcionalidades que lo hacen ideal para gestionar memoria persistente:
- Memoria persistente: Almacena información en un grafo de conocimiento local (generalmente en un archivo JSON, como `memory.jsonl`), lo que permite a Claude recordar detalles de interacciones pasadas, como la identidad del usuario, sus preferencias, comportamientos, metas o relaciones (hasta 3 grados de separación).[](https://github.com/shaneholloman/mcp-knowledge-graph)[](https://playbooks.com/mcp/modelcontextprotocol-knowledge-graph-memory)
- Herramientas dinámicas: Proporciona un conjunto de herramientas generadas automáticamente para interactuar con el grafo, incluyendo:
  - `create_entities`: Crear nuevas entidades.
  - `create_relations`: Definir relaciones entre entidades.
  - `add_observations`: Añadir hechos a entidades existentes.
  - `delete_entities`, `delete_observations`, `delete_relations`: Eliminar nodos, hechos o conexiones.
  - `read_graph`: Recuperar la estructura completa del grafo.
  - `search_nodes`: Buscar entidades por nombre, tipo o contenido de observaciones.
  - `open_nodes`: Recuperar entidades específicas y sus relaciones.[](https://www.marktechpost.com/2025/04/26/implementing-persistent-memory-using-a-local-knowledge-graph-in-claude-desktop/)[](https://glama.ai/mcp/servers/%40modelcontextprotocol/knowledge-graph-memory-server)
- Personalización de la ruta de almacenamiento: Permite especificar una ruta personalizada para el archivo de almacenamiento del grafo (e.g., `/Users/shaneholloman/Dropbox/shane/db/memory.jsonl`). Si no se especifica, usa una ruta predeterminada como `memory.jsonl` en el directorio del servidor.[](https://github.com/shaneholloman/mcp-knowledge-graph)[](https://www.mcp.bar/server/shaneholloman/mcp-knowledge-graph)
- Compatibilidad multiplataforma: Aunque está optimizado para Claude, el servidor es compatible con cualquier modelo de IA que soporte MCP o capacidades de llamada a funciones, como GPT o Llama.[](https://github.com/shaneholloman/mcp-knowledge-graph)[](https://www.mcp.bar/server/shaneholloman/mcp-knowledge-graph)
- Búsqueda semántica y estructurada: Integra capacidades de búsqueda avanzada, a veces combinadas con embeddings vectoriales (como en implementaciones con SQLite o PouchDB), para recuperar información relevante de manera eficiente.[](https://www.pulsemcp.com/servers/modelcontextprotocol-knowledge-graph-memory)[](https://www.pulsemcp.com/servers/itseasy21-knowledge-graph)
- Integración con bases de datos de grafos: Algunas implementaciones permiten conectar el servidor con bases de datos como Neo4j para consultas más complejas mediante Cypher o con Redis Graph para almacenamiento de grafos a gran escala.[](https://www.pulsemcp.com/servers/shaneholloman-knowledge-graph)[](https://neo4j.com/blog/developer/knowledge-graphs-claude-neo4j-mcp/)

### ¿Cómo funciona?
El Knowledge Graph MCP Server sigue un flujo de trabajo estructurado para gestionar la memoria persistente:
1. Identificación del usuario: Por defecto, asume que interactúa con un usuario genérico (`default_user`). Si es necesario, el servidor intenta identificar al usuario para asociar la información correctamente.[](https://playbooks.com/mcp/modelcontextprotocol-knowledge-graph-memory)[](https://mcpservers.org/servers/modelcontextprotocol/memory)
2. Recuperación de memoria: Al iniciar una conversación, el servidor ejecuta la acción de "recordar" (indicada con el mensaje "Remembering...") y recupera información relevante del grafo de conocimiento, como datos previos sobre el usuario o el contexto.[](https://github.com/shaneholloman/mcp-knowledge-graph)[](https://www.mcpservers.ai/servers/modelcontextprotocol/Knowledge%2520Graph%2520Memory)
3. Recolección de información: Durante la interacción, el servidor detecta y categoriza nueva información en:
   - Identidad básica (edad, género, ubicación, etc.).
   - Comportamientos (intereses, hábitos).
   - Preferencias (estilo de comunicación, idioma).
   - Metas (objetivos, aspiraciones).
   - Relaciones (hasta 3 grados de separación).[](https://github.com/shaneholloman/mcp-knowledge-graph)[](https://mcpservers.org/servers/modelcontextprotocol/memory)
4. Actualización del grafo: Si se detecta nueva información, el servidor:
   - Crea nuevas entidades para organizaciones, personas o eventos recurrentes.
   - Establece relaciones entre entidades.
   - Almacena hechos como observaciones.[](https://github.com/shaneholloman/mcp-knowledge-graph)[](https://www.mcp.bar/server/shaneholloman/mcp-knowledge-graph)
5. Interacción con Claude: Claude utiliza las herramientas del servidor (como `search_nodes` o `read_graph`) para consultar el grafo y generar respuestas contextualizadas. Por ejemplo, si un usuario menciona que prefiere reuniones matutinas, esta observación se almacena y puede recuperarse en futuras interacciones para personalizar la respuesta.

El servidor se configura típicamente mediante un archivo JSON (e.g., `claude_desktop_config.json`) que especifica el comando para ejecutarlo (como `npx` con argumentos) y las herramientas permitidas automáticamente. Por ejemplo:
```json
{
  "mcpServers": {
    "memory": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-memory"],
      "autoapprove": ["create_entities", "create_relations", "add_observations", "delete_entities", "delete_observations", "delete_relations", "read_graph", "search_nodes", "open_nodes"]
    }
  }
}
```
Este archivo conecta Claude Desktop al servidor y define cómo interactúa con el grafo.[](https://www.marktechpost.com/2025/04/26/implementing-persistent-memory-using-a-local-knowledge-graph-in-claude-desktop/)[](https://playbooks.com/mcp/modelcontextprotocol-knowledge-graph-memory)

### Implementaciones y tecnologías
El Knowledge Graph MCP Server puede implementarse con diferentes tecnologías de almacenamiento, dependiendo de la implementación específica:
- JSON local: La implementación básica almacena el grafo en un archivo JSON (e.g., `memory.jsonl`), ideal para configuraciones locales y simples.[](https://github.com/shaneholloman/mcp-knowledge-graph)[](https://www.mcp.bar/server/shaneholloman/mcp-knowledge-graph)
- Neo4j: Permite consultas avanzadas mediante Cypher, ideal para grafos complejos y aplicaciones que requieren relaciones profundas. Por ejemplo, se ha usado para modelar currículos educativos sin escribir código, extrayendo entidades y relaciones directamente desde conversaciones con Claude.[](https://neo4j.com/blog/developer/knowledge-graphs-claude-neo4j-mcp/)
- Redis Graph: Ofrece almacenamiento de grafos a gran escala para aplicaciones que necesitan alto rendimiento y contextos complejos.[](https://www.pulsemcp.com/servers/modelcontextprotocol-knowledge-graph-memory)[](https://www.pulsemcp.com/servers/shaneholloman-knowledge-graph)
- SQLite con embeddings vectoriales: Integra búsqueda semántica para recuperar información basada en similitud, útil para aplicaciones de personalización avanzada.[](https://www.pulsemcp.com/servers/modelcontextprotocol-knowledge-graph-memory)[](https://www.pulsemcp.com/servers/itseasy21-knowledge-graph)
- PouchDB: Proporciona almacenamiento ligero para relaciones y observaciones, ideal para aplicaciones locales con necesidades de sincronización.[](https://www.pulsemcp.com/servers/itseasy21-knowledge-graph)[](https://www.pulsemcp.com/servers/estav-knowledge-graph-memory)
- Markdown local: Algunas implementaciones almacenan el grafo en archivos Markdown, integrándose con herramientas como Obsidian para gestionar conocimiento personal.[](https://www.pulsemcp.com/servers/modelcontextprotocol-knowledge-graph-memory)[](https://glama.ai/mcp/servers/%40modelcontextprotocol/knowledge-graph-memory-server)

### Casos de uso
El Knowledge Graph MCP Server es versátil y se utiliza en diversos escenarios:
- Personalización de conversaciones: Claude puede recordar preferencias del usuario (e.g., idioma preferido, horarios) y adaptar sus respuestas en consecuencia.[](https://mcp.so/server/mcp-knowledge-graph)[](https://www.pulsemcp.com/servers/itseasy21-knowledge-graph)
- Gestión de conocimiento académico: Almacena relaciones entre cursos, asignaturas y exámenes, como en el caso de modelar un currículo escolar con Neo4j.[](https://neo4j.com/blog/developer/knowledge-graphs-claude-neo4j-mcp/)
- Juegos de rol basados en texto: Proyectos como MemoryMesh usan el servidor para gestionar mundos de RPG, creando entidades como NPCs, ubicaciones y artefactos.[](https://github.com/CheMiguel23/MemoryMesh)
- Gestión de proyectos: Almacena entidades y relaciones de proyectos (e.g., tareas, hitos) para proporcionar contexto a asistentes de IA en desarrollo de software.[](https://www.pulsemcp.com/servers/modelcontextprotocol-knowledge-graph-memory)[](https://www.pulsemcp.com/servers/estav-knowledge-graph-memory)
- Análisis de datos estructurados: Permite a Claude consultar grafos para responder preguntas complejas, como relaciones entre usuarios o análisis de redes sociales.[](https://www.pulsemcp.com/servers/itseasy21-knowledge-graph)[](https://www.pulsemcp.com/servers/shaneholloman-knowledge-graph)

### Ejemplo práctico: Configuración con Claude Desktop
Para configurar el Knowledge Graph MCP Server con Claude Desktop:
1. Instalar Node.js: Requerido para ejecutar el servidor con `npx`. Descarga la última versión desde nodejs.org.[](https://www.marktechpost.com/2025/04/26/implementing-persistent-memory-using-a-local-knowledge-graph-in-claude-desktop/)
2. Configurar el servidor: Edita o crea el archivo `claude_desktop_config.json` en el directorio de Claude con la configuración mencionada anteriormente.[](https://www.marktechpost.com/2025/04/26/implementing-persistent-memory-using-a-local-knowledge-graph-in-claude-desktop/)[](https://playbooks.com/mcp/modelcontextprotocol-knowledge-graph-memory)
3. Ejecutar el servidor: Usa el comando `npx -y @modelcontextprotocol/server-memory` o especifica una ruta personalizada con `--memory-path`.[](https://playbooks.com/mcp/modelcontextprotocol-knowledge-graph-memory)[](https://www.mcp.bar/server/shaneholloman/mcp-knowledge-graph)
4. Personalizar instrucciones: Añade un prompt en el campo "Custom Instructions" de Claude.ai para definir cómo Claude usa el grafo. Por ejemplo:
   ```
   Siempre comienza diciendo "Remembering..." y recupera información relevante de tu grafo de conocimiento. Almacena nueva información en categorías como identidad, comportamientos, preferencias, metas y relaciones.
   ```
  [](https://www.mcpservers.ai/servers/modelcontextprotocol/Knowledge%2520Graph%2520Memory)[](https://glama.ai/mcp/servers/%40modelcontextprotocol/knowledge-graph-memory-server)
5. Interacción: Claude usará las herramientas del servidor automáticamente para consultar o actualizar el grafo durante las conversaciones.

### Ventajas y limitaciones
Ventajas:
- Persistencia: Permite a Claude mantener un contexto coherente a lo largo de múltiples sesiones, mejorando la personalización.[](https://www.marktechpost.com/2025/04/26/implementing-persistent-memory-using-a-local-knowledge-graph-in-claude-desktop/)[](https://www.pulsemcp.com/servers/itseasy21-knowledge-graph)
- Accesibilidad: No requiere conocimientos avanzados de programación para configurar y usar, especialmente con integraciones como Neo4j.[](https://neo4j.com/blog/developer/knowledge-graphs-claude-neo4j-mcp/)
- Flexibilidad: Compatible con múltiples bases de datos y adaptable a diferentes casos de uso, desde juegos hasta gestión de proyectos.[](https://www.pulsemcp.com/servers/modelcontextprotocol-knowledge-graph-memory)[](https://github.com/CheMiguel23/MemoryMesh)
- Búsqueda avanzada: La integración con embeddings vectoriales y bases de datos de grafos permite búsquedas semánticas y relacionales.[](https://www.pulsemcp.com/servers/itseasy21-knowledge-graph)[](https://www.pulsemcp.com/servers/estav-knowledge-graph-memory)

Limitaciones:
- Escalabilidad: Las implementaciones basadas en JSON local pueden tener limitaciones de almacenamiento para grafos grandes.[](https://mcp.so/server/mcp-memory-py)
- Seguridad: Los usuarios deben ser cuidadosos con las credenciales de bases de datos en la configuración del servidor.[](https://neo4j.com/blog/developer/knowledge-graphs-claude-neo4j-mcp/)
- Complejidad de consultas: Consultas muy complejas pueden requerir optimización manual, especialmente en bases de datos como Neo4j.[](https://neo4j.com/blog/developer/knowledge-graphs-claude-neo4j-mcp/)
- Dependencia de Claude Desktop: Algunas implementaciones están optimizadas para Claude Desktop, lo que puede limitar su uso en otras plataformas sin ajustes.[](https://www.marktechpost.com/2025/04/26/implementing-persistent-memory-using-a-local-knowledge-graph-in-claude-desktop/)[](https://playbooks.com/mcp/modelcontextprotocol-knowledge-graph-memory)

### Proyectos relacionados en Apache

Aunque el Knowledge Graph MCP Server no es un proyecto de Apache, podría integrarse con proyectos de la Apache Software Foundation para potenciar sus capacidades:

- Apache AGE: Podría usarse como base de datos de grafos para almacenar el grafo de conocimiento, permitiendo consultas híbridas relacionales y de grafos.
- Apache Jena: Ideal para grafos de conocimiento basados en RDF y SPARQL, útil para aplicaciones de web semántica.
- Apache Kafka o NiFi: Para alimentar datos en tiempo real al servidor MCP, integrando flujos de datos externos con el grafo.

El Knowledge Graph MCP Server es una herramienta poderosa para dotar a Claude (y otros modelos compatibles con MCP) de memoria persistente mediante grafos de conocimiento locales. Su capacidad para almacenar entidades, relaciones y observaciones, junto con herramientas dinámicas para gestionar el grafo, lo hace ideal para aplicaciones que requieren contexto a largo plazo, como personalización de conversaciones, gestión de proyectos o análisis de datos estructurados. 

Implementaciones con tecnologías como Neo4j o SQLite ofrecen flexibilidad para diferentes necesidades, desde configuraciones locales ligeras hasta sistemas de grafos a gran escala.
