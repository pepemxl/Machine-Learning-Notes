# Model Control Protocol

In november of 2024 Anthropic introduce MCP [https://www.anthropic.com/news/model-context-protocol](https://www.anthropic.com/news/model-context-protocol) which now is an standard.

You can find it in [https://github.com/modelcontextprotocol](https://github.com/modelcontextprotocol)


## Protocols

A **protocol** is a set of **rules and conventions** that define how systems communicate and exchange data. Unlike an **API**, an **implementation specific interface**, a protocol establishes a universal standard for interactions.

- **HTTP (Hypertext Transfer Protocol)**: Defines how web browsers and servers communicate.
- **OAuth (Open Authorization Protocol)**: A standard for secure authentication across different platforms.

Protocols ensure interoperability instead of every system reinventing how data should be exchanged, a protocol standardizes the process, reducing complexity and making integrations more scalable.


## Model Context Protocol (MCP)

Model Context Protocol (MCP) is an open standard developed by Anthropic to streamline how AI models access and interact with external data sources.

Instead of requiring AI systems to rely on custom API integrations, manually structured requests, and authentication per service, MCP provides a unified framework for AI agents to retrieve, process, and act on structured data in a standardized way.

MCP defines how AI models should request and consume external data whether from databases, APIs, cloud storage, or enterprise applications without needing developers to hardcode API-specific logic for each source.


## MCP’s Client-Server Architecture

MCP is built on a client-server model that structures how AI models retrieve and interact with external data sources.

MCP clients are AI agents, applications, or any system that requests structured data.
MCP servers act as intermediaries, fetching data from various APIs, databases, or enterprise systems and returning it in a consistent format.

Instead of AI models making direct API requests, MCP servers handle the complexity of authentication, data retrieval, and response normalization. This means AI agents no longer need to manage multiple API credentials, different request formats, or inconsistent response structures.

For example, if an AI model needs to pull information from multiple services like Google Drive, Slack, and a database, it does not query each API separately. It sends a single structured request to an MCP server, which processes the request, gathers data from the necessary sources, and returns a well-organized response.

## MCP Request/Response Lifecycle

A typical MCP interaction follows a structured request/response cycle that eliminates redundant API calls and standardizes data retrieval.

1. The AI agent sends a structured request to the MCP server. Instead of crafting individual API requests, the agent defines what data it needs in a uniform format.

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
    ‍```

2. The MCP server processes the request by validating authentication, checking permissions, and determining which external systems to query.


3. Queries are executed in parallel, meaning data from multiple services is retrieved at the same time rather than sequentially, reducing overall latency, same idea to GraphQL approach or asynchronous process to fetch data through batches.


4. Responses from different sources are standardized into a structured format that AI models can easily process.

    ```json
    {
    "github": {
        "recent_commits": [
        {
            "author": "Carlos",
            "message": "Refactored AI pipeline",
            "timestamp": "2025-07-20T10:00:00Z"
        }
        ]
    },
    "slack": {
        "unread_messages": [
        {
            "user": "Carlos",
            "text": "Hey, can you review the PR?",
            "timestamp": "2025-07-20T10:00:00Z"
        }
        ]
    }
    }
    ```


Unlike raw API responses that require manual parsing, MCP ensures that all retrieved data follows a predictable, structured format, making it easier for AI models to understand and utilize.


## Query Execution and Response Aggregation

MCP is designed to optimize how AI models interact with external systems by introducing a structured execution process.

```mermaid
flowchart LR;
    llm_node["AI Model<br/> Receives Data"]:::aiNode --> validation_node["Request Validation<br/>Check Permissions"]:::validationNode
    validation_node --> routing_node["Query Routing<br/>Determine Service"]:::routingNode
    routing_node --> service_node1["Service 1"]:::serviceNode
    routing_node --> service_node2["Service 2"]:::serviceNode
    routing_node --> service_noden["Service N"]:::serviceNode
    service_node1 --> response_node["Response Aggregation"]:::aggregationNode
    service_node2 --> response_node
    service_noden --> response_node
    response_node --> consolidation_node["Consolidated Response"]:::consolidationNode
    consolidation_node --> llm_node

    classDef aiNode fill:#4B0082,stroke:#9370DB,color:white,stroke-width:2px;
    classDef validationNode fill:#228B22,stroke:#32CD32,color:white;
    classDef routingNode fill:#4169E1,stroke:#1E90FF,color:white;
    classDef serviceNode fill:#FF8C00,stroke:#FFA500,color:black;
    classDef aggregationNode fill:#8B0000,stroke:#B22222,color:white;
    classDef consolidationNode fill:#9932CC,stroke:#BA55D3,color:white;
```


## Limitations of MCP

Model Context Protocol (MCP) is an important step toward making AI models more capable of interacting with external systems in a structured and scalable way. 

- Authentication Challenges
- Unclear Identity Management


MCP simplifies AI interactions, but authentication and structured API access remain key challenges.


## MCP Architecture

### Main Components

```mermaid
---
config:
  theme: neo-dark
  layout: elk
  look: classic
---
flowchart TB
 subgraph subGraph0["Cliente MCP"]
        A["Claude Desktop<br>(Host App)"]
  end
    A -- Protocolo MCP --> B["Servidor MCP 1"] & C["Servidor MCP 2"]
    B --> D["Sistema Archivos"]
    C --> E["Base Datos"]
    style A fill:#2962FF,stroke:#333,stroke-width:2px
    style B fill:#AA00FF,stroke:#333,stroke-width:2px
    style C fill:#AA00FF,stroke:#333,stroke-width:2px
    style D fill:#FFF9C4,stroke:#333,stroke-width:2px,color:#000000
    style E fill:#FFF9C4,stroke:#333,stroke-width:2px,color:#000000
```

### 1. **MCP Client**
- Host application that runs the AI model (e.g., Claude Desktop)
- Discovers and connects to MCP servers
- Manages multiple simultaneous server connections
- Presents available tools and resources to the model

### 2. **MCP Server**
- Lightweight program that exposes specific capabilities
- Can provide:
  - **Resources**: Data or content (files, databases, APIs)
  - **Tools**: Functions that the model can invoke
  - **Prompts**: Predefined prompt templates
- Communicates with the client through the MCP protocol

## MCP Configuration in Claude Desktop

### Step 1: Claude Desktop Installation

1. Download Claude Desktop from the official Anthropic website
2. Install the application on your operating system
3. Sign in with your Anthropic account

### Step 2: Configuring the `claude_desktop_config.json` file

MCP server configuration is done through a JSON file located at:

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

### Step 3: Configuration File Structure

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/allowed/directory"
      ]
    },
    "github": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-github"
      ],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "your_token_here"
      }
    },
    "postgres": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-postgres",
        "postgresql://user:password@localhost/database"
      ]
    }
  }
}
```

### Step 4: Examples of Common MCP Servers

#### Filesystem Server
Allows Claude to read/write files in specific directories:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "D:\\MyProjects",
        "C:\\Documents"
      ]
    }
  }
}
```

#### Git Server
Allows operations with Git repositories:

```json
{
  "mcpServers": {
    "git": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-git",
        "/path/to/repository"
      ]
    }
  }
}
```

#### Brave Search Server
Allows web searches:

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
        "BRAVE_API_KEY": "your_api_key"
      }
    }
  }
}
```

### Step 5: Restart Claude Desktop

After modifying the configuration file:
1. Completely close Claude Desktop
2. Restart the application
3. MCP servers will load automatically

### Step 6: Verify Connection

In Claude Desktop:
- Look for the 🔌 (plug) icon or available tools
- Claude will inform you which MCP tools are available
- You can ask: "What tools do you have available?"

## Creating a Custom MCP Server

### Basic Example (Node.js/TypeScript)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Create server
const server = new Server(
  {
    name: "my-example-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "get_weather",
        description: "Gets the current weather for a city",
        inputSchema: {
          type: "object",
          properties: {
            city: {
              type: "string",
              description: "City name",
            },
          },
          required: ["city"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "get_weather") {
    const city = request.params.arguments?.city;
    // Logic to get weather
    return {
      content: [
        {
          type: "text",
          text: `The weather in ${city} is sunny, 72°F`,
        },
      ],
    };
  }
  throw new Error("Tool not found");
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
}

main();
```

### Configure Custom Server

```json
{
  "mcpServers": {
    "my-weather-server": {
      "command": "node",
      "args": ["/path/to/my-server.js"]
    }
  }
}
```

## MCP vs Other Tools (Cursor, Copilot, etc.)

### Distinctive Features of MCP

| Feature | MCP | Cursor | GitHub Copilot |
|---------|-----|--------|----------------|
| **Protocol** | Open standard | Proprietary | Proprietary |
| **Extensibility** | Unlimited custom servers | Limited to predefined integrations | Limited to code context |
| **Data Access** | Any source via servers | Project files | Code and comments |
| **Interoperability** | Works with any MCP client | Cursor only | VS Code/compatible IDEs only |
| **User Control** | Full control over exposed data | Application-dependent | Limited |
| **Use Cases** | Universal (conversational AI + code) | Primarily coding | Code autocompletion |

### MCP Advantages

#### 1. **Standardization**
- Single protocol for all integrations
- Any developer can create compatible servers
- No vendor lock-in

#### 2. **Security and Control**
```
User explicitly defines:
├── What data Claude can access
├── What operations it can perform
├── Which directories are allowed
└── Which APIs it can call
```

#### 3. **Composability**
- Multiple servers can work together
- Claude can combine information from different sources
- Example: Read DB + Access files + Query API in a single task

#### 4. **Flexibility**
```python
# Cursor: Limited to project files
cursor.read("file.py")

# MCP: Access to anything you expose
mcp_filesystem.read("D:\\project\\file.py")
mcp_database.query("SELECT * FROM users")
mcp_api.fetch("https://external-api.com/data")
mcp_custom.anything()
```

### Comparison Claude with Cursor

#### Strengths

- Polished user experience
- Intelligent autocompletion
- Native VS Code integration
- Advanced code refactoring

#### Limitations

- Closed ecosystem
- Limited integrations
- Primarily focused on code
- Difficult deep customization


### MCP with Claude Desktop


#### Strengths

- Open and extensible protocol
- Unlimited integrations via servers
- Natural conversation + code execution
- Granular permission control
- Community can create servers

#### Limitations

- Requires manual configuration
- Less polished for pure coding
- Initial learning curve



## MCP Server Ecosystem

### Official Anthropic Servers

1. **@modelcontextprotocol/server-filesystem** - File access
2. **@modelcontextprotocol/server-github** - GitHub integration
3. **@modelcontextprotocol/server-gitlab** - GitLab integration
4. **@modelcontextprotocol/server-postgres** - PostgreSQL databases
5. **@modelcontextprotocol/server-sqlite** - SQLite databases
6. **@modelcontextprotocol/server-google-drive** - Google Drive
7. **@modelcontextprotocol/server-slack** - Slack integration
8. **@modelcontextprotocol/server-brave-search** - Web search

### Community Servers

The community is creating servers for:
- Third-party APIs (Stripe, Twilio, etc.)
- Cloud services (AWS, Azure, GCP)
- Development tools (Docker, Kubernetes)
- Databases (MongoDB, Redis, MySQL)
- And many more...

## Best Practices

### Security

```json
{
  "mcpServers": {
    "secure-filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        // ✅ Specify only necessary directories
        "/path/specific/project",
        // ❌ NEVER use paths like "/" or "C:\\"
      ]
    }
  }
}
```

### Environment Variables

Use environment variables for sensitive data:

```json
{
  "mcpServers": {
    "external-api": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-api"],
      "env": {
        "API_KEY": "${API_KEY_FROM_ENV_VARIABLE}"
      }
    }
  }
}
```

### Organization

```json
{
  "mcpServers": {
    // Development
    "dev-filesystem": { ... },
    "dev-database": { ... },
    
    // Production
    "prod-filesystem": { ... },
    "prod-database": { ... },
    
    // Utilities
    "git": { ... },
    "search": { ... }
  }
}
```

## Debugging and Troubleshooting

### Check Claude Desktop Logs

**Windows:**
```
%APPDATA%\Claude\logs\
```

**macOS:**
```
~/Library/Logs/Claude/
```

### Common Errors

1. **"MCP server won't connect"**
   - Verify that Node.js is installed
   - Confirm the path in `args` is correct
   - Review logs for specific errors

2. **"Permission denied"**
   - Ensure the directory exists
   - Verify operating system permissions
   - Use absolute paths instead of relative ones

3. **"Environment variables not loading"**
   - Define variables in the server's `env` object
   - Restart Claude Desktop after changes


MCP represents a paradigm shift in how AI applications interact with external data and tools. Unlike proprietary solutions like Cursor or Copilot, MCP offers:

- **Openness**: Standard protocol that anyone can implement
- **Flexibility**: Create servers for any use case
- **Control**: You decide what the AI can access
- **Future**: Growing ecosystem of integrations

If you're looking for an AI solution that can adapt to any workflow, MCP + Claude Desktop is a powerful and extensible option.

## Additional Resources

- **Official documentation**: https://modelcontextprotocol.io
- **MCP GitHub**: https://github.com/modelcontextprotocol
- **Server examples**: https://github.com/modelcontextprotocol/servers
- **Protocol specification**: https://spec.modelcontextprotocol.io