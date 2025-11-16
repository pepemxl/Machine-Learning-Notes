# Protocolo de Contexto de Modelo

En noviembre de 2024, Anthropic introdujo MCP [https://www.anthropic.com/news/model-context-protocol](https://www.anthropic.com/news/model-context-protocol), que ahora es un estándar.

Puedes encontrarlo en [https://github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)


## Protocolos

Un **protocolo** es un conjunto de **reglas y convenciones** que definen cómo los sistemas se comunican e intercambian datos. A diferencia de una **API**, una **interfaz específica de implementación**, un protocolo establece un estándar universal para las interacciones.

- **HTTP (Protocolo de Transferencia de Hipertexto)**: Define cómo los navegadores web y los servidores se comunican.
- **OAuth (Protocolo de Autorización Abierta)**: Un estándar para la autenticación segura entre diferentes plataformas.

Los protocolos aseguran la interoperabilidad: en lugar de que cada sistema reinvente cómo se deben intercambiar los datos, un protocolo estandariza el proceso, reduciendo la complejidad y haciendo las integraciones más escalables.


## Protocolo de Contexto de Modelo (MCP)

El Protocolo de Contexto de Modelo (MCP) es un estándar abierto desarrollado por Anthropic para optimizar cómo los modelos de IA acceden e interactúan con fuentes de datos externas.

En lugar de requerir que los sistemas de IA dependan de integraciones de API personalizadas, solicitudes estructuradas manualmente y autenticación por servicio, MCP proporciona un marco unificado para que los agentes de IA recuperen, procesen y actúen sobre datos estructurados de manera estandarizada.

MCP define cómo los modelos de IA deben solicitar y consumir datos externos, ya sea de bases de datos, APIs, almacenamiento en la nube o aplicaciones empresariales, sin necesidad de que los desarrolladores codifiquen lógica específica de API para cada fuente.


## Arquitectura Cliente-Servidor de MCP

MCP está construido sobre un modelo cliente-servidor que estructura cómo los modelos de IA recuperan e interactúan con fuentes de datos externas.

Los clientes MCP son agentes de IA, aplicaciones o cualquier sistema que solicita datos estructurados.
Los servidores MCP actúan como intermediarios, obteniendo datos de varias APIs, bases de datos o sistemas empresariales y devolviéndolos en un formato consistente.

En lugar de que los modelos de IA hagan solicitudes directas a las APIs, los servidores MCP manejan la complejidad de la autenticación, recuperación de datos y normalización de respuestas. Esto significa que los agentes de IA ya no necesitan gestionar múltiples credenciales de API, diferentes formatos de solicitud o estructuras de respuesta inconsistentes.

Por ejemplo, si un modelo de IA necesita obtener información de múltiples servicios como Google Drive, Slack y una base de datos, no consulta cada API por separado. Envía una única solicitud estructurada al servidor MCP, que procesa la solicitud, recopila datos de las fuentes necesarias y devuelve una respuesta bien organizada.

## Ciclo de Vida de Solicitud/Respuesta en MCP

Una interacción típica de MCP sigue un ciclo de solicitud/respuesta estructurado que elimina llamadas redundantes a las APIs y estandariza la recuperación de datos.

1. El agente de IA envía una solicitud estructurada al servidor MCP. En lugar de crear solicitudes individuales a las APIs, el agente define qué datos necesita en un formato uniforme.

    ```json
    {
    "request_id": "xyz-123",
    "queries": [
        {
        "source": "github",
        "action": "get_recent_commits",
        "repo": "company/project"
        },
        {
        "source": "slack",
        "action": "fetch_unread_messages",
        "channel": "social"
        }
    ]
    }
    ```

2. El servidor MCP procesa la solicitud validando la autenticación, verificando permisos y determinando qué sistemas externos consultar.


3. Las consultas se ejecutan en paralelo, lo que significa que los datos de múltiples servicios se recuperan al mismo tiempo en lugar de secuencialmente, reduciendo la latencia general, misma idea que el enfoque de GraphQL o procesos asíncronos para obtener datos por lotes.


4. Las respuestas de diferentes fuentes se estandarizan en un formato estructurado que los modelos de IA pueden procesar fácilmente.

    ```json
    {
    "github": {
        "recent_commits": [
        {
            "author": "Carlos",
            "message": "Refactorizado pipeline de IA",
            "timestamp": "2025-07-20T10:00:00Z"
        }
        ]
    },
    "slack": {
        "unread_messages": [
        {
            "user": "Carlos",
            "text": "Oye, ¿puedes revisar el PR?",
            "timestamp": "2025-07-20T10:00:00Z"
        }
        ]
    }
    }
    ```


A diferencia de las respuestas de API sin procesar que requieren análisis manual, MCP asegura que todos los datos recuperados sigan un formato predecible y estructurado, facilitando que los modelos de IA los comprendan y utilicen.


## Ejecución de Consultas y Agregación de Respuestas

MCP está diseñado para optimizar cómo los modelos de IA interactúan con sistemas externos mediante la introducción de un proceso de ejecución estructurado.

```mermaid
flowchart LR;
    llm_node["Modelo de IA<br/> Recibe Datos"]:::aiNode --> validation_node["Validación de Solicitud<br/>Verificar Permisos"]:::validationNode
    validation_node --> routing_node["Enrutamiento de Consultas<br/>Determinar Servicio"]:::routingNode
    routing_node --> service_node1["Servicio 1"]:::serviceNode
    routing_node --> service_node2["Servicio 2"]:::serviceNode
    routing_node --> service_noden["Servicio N"]:::serviceNode
    service_node1 --> response_node["Agregación de Respuestas"]:::aggregationNode
    service_node2 --> response_node
    service_noden --> response_node
    response_node --> consolidation_node["Respuesta Consolidada"]:::consolidationNode
    consolidation_node --> llm_node

    classDef aiNode fill:#4B0082,stroke:#9370DB,color:white,stroke-width:2px;
    classDef validationNode fill:#228B22,stroke:#32CD32,color:white;
    classDef routingNode fill:#4169E1,stroke:#1E90FF,color:white;
    classDef serviceNode fill:#FF8C00,stroke:#FFA500,color:black;
    classDef aggregationNode fill:#8B0000,stroke:#B22222,color:white;
    classDef consolidationNode fill:#9932CC,stroke:#BA55D3,color:white;
```


## Limitaciones de MCP

El Protocolo de Contexto de Modelo (MCP) es un paso importante hacia hacer que los modelos de IA sean más capaces de interactuar con sistemas externos de manera estructurada y escalable.

- Desafíos de Autenticación
- Gestión de Identidad Poco Clara


MCP simplifica las interacciones de IA, pero la autenticación y el acceso estructurado a las APIs siguen siendo desafíos clave.


## Arquitectura de MCP

### Componentes Principales

```
┌─────────────────┐
│  Claude Desktop │  ← Cliente MCP
│   (Host App)    │
└────────┬────────┘
         │
         ├─── Protocolo MCP ───┐
         │                      │
    ┌────▼────┐            ┌───▼────┐
    │ Servidor│            │Servidor│
    │  MCP 1  │            │ MCP 2  │
    └────┬────┘            └───┬────┘
         │                     │
    ┌────▼────┐           ┌───▼─────┐
    │Sistema  │           │  Base   │
    │Archivos │           │  Datos  │
    └─────────┘           └─────────┘
```

### 1. **Cliente MCP**
- Aplicación host que ejecuta el modelo de IA (ej: Claude Desktop)
- Descubre y se conecta a servidores MCP
- Gestiona múltiples conexiones de servidores simultáneamente
- Presenta herramientas y recursos disponibles al modelo

### 2. **Servidor MCP**
- Programa ligero que expone capacidades específicas
- Puede proporcionar:
  - **Recursos**: Datos o contenido (archivos, bases de datos, APIs)
  - **Herramientas**: Funciones que el modelo puede invocar
  - **Prompts**: Plantillas predefinidas de prompts
- Se comunica con el cliente a través del protocolo MCP

## Configuración de MCP en Claude Desktop

### Paso 1: Instalación de Claude Desktop

1. Descarga Claude Desktop desde el sitio oficial de Anthropic
2. Instala la aplicación en tu sistema operativo
3. Inicia sesión con tu cuenta de Anthropic

### Paso 2: Configuración del archivo `claude_desktop_config.json`

La configuración de servidores MCP se realiza mediante un archivo JSON ubicado en:

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**macOS:**
```
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Linux:**
```
~/.config/Claude/claude_desktop_config.json
```

### Paso 3: Estructura del archivo de configuración

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/ruta/a/directorio/permitido"
      ]
    },
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "tu_token_aqui"
      }
    },
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://usuario:contraseña@localhost/basedatos"
      ]
    }
  }
}
```

### Paso 4: Ejemplos de Servidores MCP Comunes

#### Servidor de Sistema de Archivos
Permite a Claude leer/escribir archivos en directorios específicos:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "D:\\MisProyectos",
        "C:\\Documentos"
      ]
    }
  }
}
```

#### Servidor de Git
Permite operaciones con repositorios Git:

```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-git",
        "/ruta/a/repositorio"
      ]
    }
  }
}
```

#### Servidor de Brave Search
Permite búsquedas web:

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-brave-search"
      ],
      "env": {
        "BRAVE_API_KEY": "tu_api_key"
      }
    }
  }
}
```

### Paso 5: Reiniciar Claude Desktop

Después de modificar el archivo de configuración:
1. Cierra completamente Claude Desktop
2. Reinicia la aplicación
3. Los servidores MCP se cargarán automáticamente

### Paso 6: Verificar la conexión

En Claude Desktop:
- Busca el ícono de 🔌 (enchufe) o herramientas disponibles
- Claude te informará qué herramientas MCP están disponibles
- Puedes preguntar: "¿Qué herramientas tienes disponibles?"

## Creación de un Servidor MCP Personalizado

### Ejemplo Básico (Node.js/TypeScript)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Crear servidor
const server = new Server(
  {
    name: "mi-servidor-ejemplo",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Listar herramientas disponibles
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "obtener_clima",
        description: "Obtiene el clima actual de una ciudad",
        inputSchema: {
          type: "object",
          properties: {
            ciudad: {
              type: "string",
              description: "Nombre de la ciudad",
            },
          },
          required: ["ciudad"],
        },
      },
    ],
  };
});

// Manejar llamadas a herramientas
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "obtener_clima") {
    const ciudad = request.params.arguments?.ciudad;
    // Lógica para obtener clima
    return {
      content: [
        {
          type: "text",
          text: `El clima en ${ciudad} es soleado, 22°C`,
        },
      ],
    };
  }
  throw new Error("Herramienta no encontrada");
});

// Iniciar servidor
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main();
```

### Configurar el servidor personalizado

```json
{
  "mcpServers": {
    "mi-servidor-clima": {
      "command": "node",
      "args": ["/ruta/a/mi-servidor.js"]
    }
  }
}
```

## MCP vs Otras Herramientas (Cursor, Copilot, etc.)

### Características Distintivas de MCP

| Característica | MCP | Cursor | GitHub Copilot |
|----------------|-----|--------|----------------|
| **Protocolo** | Estándar abierto | Propietario | Propietario |
| **Extensibilidad** | Servidores personalizados ilimitados | Limitado a integraciones predefinidas | Limitado a contexto de código |
| **Acceso a Datos** | Cualquier fuente mediante servidores | Archivos del proyecto | Código y comentarios |
| **Interoperabilidad** | Funciona con cualquier cliente MCP | Solo Cursor | Solo VS Code/IDEs compatibles |
| **Control del Usuario** | Total control sobre qué datos se exponen | Dependiente de la aplicación | Limitado |
| **Casos de Uso** | Universal (IA conversacional + código) | Principalmente coding | Autocompletado de código |

### Ventajas de MCP

#### 1. **Estandarización**
- Protocolo único para todas las integraciones
- Cualquier desarrollador puede crear servidores compatibles
- No hay lock-in de proveedor

#### 2. **Seguridad y Control**
```
Usuario define explícitamente:
├── Qué datos puede acceder Claude
├── Qué operaciones puede realizar
├── Qué directorios están permitidos
└── Qué APIs puede llamar
```

#### 3. **Composabilidad**
- Múltiples servidores pueden trabajar juntos
- Claude puede combinar información de diferentes fuentes
- Ejemplo: Leer DB + Acceder archivos + Consultar API en una sola tarea

#### 4. **Flexibilidad**
```python
# Cursor: Limitado a archivos del proyecto
cursor.read("archivo.py")

# MCP: Acceso a cualquier cosa que expongas
mcp_filesystem.read("D:\\proyecto\\archivo.py")
mcp_database.query("SELECT * FROM usuarios")
mcp_api.fetch("https://api.externa.com/datos")
mcp_custom.cualquier_cosa()
```

### Comparación con Cursor

#### Cursor
```
Fortalezas:
✓ Experiencia de usuario pulida
✓ Autocompletado inteligente
✓ Integración nativa con VS Code
✓ Refactorización de código avanzada

Limitaciones:
✗ Ecosistema cerrado
✗ Integraciones limitadas
✗ Principalmente enfocado en código
✗ Difícil personalización profunda
```

#### MCP con Claude Desktop
```
Fortalezas:
✓ Protocolo abierto y extensible
✓ Integraciones ilimitadas vía servidores
✓ Conversación natural + ejecución de código
✓ Control granular de permisos
✓ Comunidad puede crear servidores

Limitaciones:
✗ Requiere configuración manual
✗ Menos pulido para coding puro
✗ Curva de aprendizaje inicial
```

### Caso de Uso: Comparación Práctica

**Tarea:** "Analiza todos los archivos Python en mi proyecto, consulta la base de datos de usuarios, y genera un reporte en Google Docs"

#### Con Cursor:
```
❌ No puede acceder a la base de datos directamente
❌ No puede escribir en Google Docs
📝 Necesitas: Múltiples pasos manuales, copiar/pegar
```

#### Con MCP + Claude:
```
✅ Servidor filesystem lee archivos Python
✅ Servidor postgres consulta la base de datos
✅ Servidor google-docs crea el reporte
📝 Todo en una conversación fluida
```

## Ecosistema de Servidores MCP

### Servidores Oficiales de Anthropic

1. **@modelcontextprotocol/server-filesystem** - Acceso a archivos
2. **@modelcontextprotocol/server-github** - Integración con GitHub
3. **@modelcontextprotocol/server-gitlab** - Integración con GitLab
4. **@modelcontextprotocol/server-postgres** - Bases de datos PostgreSQL
5. **@modelcontextprotocol/server-sqlite** - Bases de datos SQLite
6. **@modelcontextprotocol/server-google-drive** - Google Drive
7. **@modelcontextprotocol/server-slack** - Integración con Slack
8. **@modelcontextprotocol/server-brave-search** - Búsqueda web

### Servidores de la Comunidad

La comunidad está creando servidores para:
- APIs de terceros (Stripe, Twilio, etc.)
- Servicios en la nube (AWS, Azure, GCP)
- Herramientas de desarrollo (Docker, Kubernetes)
- Bases de datos (MongoDB, Redis, MySQL)
- Y muchos más...

## Mejores Prácticas

### Seguridad

```json
{
  "mcpServers": {
    "filesystem-seguro": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        // ✅ Especifica solo directorios necesarios
        "/ruta/proyecto/especifico",
        // ❌ NUNCA uses rutas como "/"  o "C:\\"
      ]
    }
  }
}
```

### Variables de Entorno

Usa variables de entorno para datos sensibles:

```json
{
  "mcpServers": {
    "api-externa": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-api"],
      "env": {
        "API_KEY": "${API_KEY_DE_VARIABLE_ENTORNO}"
      }
    }
  }
}
```

### Organización

```json
{
  "mcpServers": {
    // Desarrollo
    "dev-filesystem": { ... },
    "dev-database": { ... },
    
    // Producción
    "prod-filesystem": { ... },
    "prod-database": { ... },
    
    // Utilidades
    "git": { ... },
    "search": { ... }
  }
}
```

## Debugging y Solución de Problemas

### Verificar logs de Claude Desktop

**Windows:**
```
%APPDATA%\Claude\logs\
```

**macOS:**
```
~/Library/Logs/Claude/
```

### Errores Comunes

1. **"Servidor MCP no se conecta"**
   - Verifica que Node.js está instalado
   - Confirma que la ruta en `args` es correcta
   - Revisa los logs para ver errores específicos

2. **"Permisos denegados"**
   - Asegúrate de que el directorio existe
   - Verifica permisos del sistema operativo
   - Usa rutas absolutas en lugar de relativas

3. **"Variables de entorno no se cargan"**
   - Define variables en el objeto `env` del servidor
   - Reinicia Claude Desktop después de cambios

MCP representa un cambio de paradigma en cómo las aplicaciones de IA interactúan con datos y herramientas externas. A diferencia de soluciones propietarias como Cursor o Copilot, MCP ofrece:

- **Apertura**: Protocolo estándar que cualquiera puede implementar
- **Flexibilidad**: Crea servidores para cualquier caso de uso
- **Control**: Tú decides qué puede acceder la IA
- **Futuro**: Ecosistema creciente de integraciones

Si buscas una solución de IA que pueda adaptarse a cualquier flujo de trabajo, MCP + Claude Desktop es una opción poderosa y extensible.

## Recursos Adicionales

- **Documentación oficial**: https://modelcontextprotocol.io
- **GitHub de MCP**: https://github.com/modelcontextprotocol
- **Ejemplos de servidores**: https://github.com/modelcontextprotocol/servers
- **Especificación del protocolo**: https://spec.modelcontextprotocol.io