# LangChain

**LangChain** es un framework para desarrollar aplicaciones potenciadas por modelos grandes de
lenguaje ([LLMs](../introduccion.md)).

LangChain simplifica cada etapa del ciclo de vida de una aplicación con LLM:

- **Desarrollo**: construir la aplicación usando los bloques y componentes de código abierto de
  LangChain. Se arranca rápido gracias a las integraciones de terceros y a las plantillas.
- **Puesta en producción**: usar LangSmith para inspeccionar, monitorear y evaluar tus cadenas,
  de modo que puedas optimizar continuamente y desplegar con confianza.
- **Despliegue**: convertir cualquier cadena en una API con LangServe.

## Librerías

Concretamente, el framework se compone de las siguientes librerías de código abierto:

- **`langchain-core`** — abstracciones base y el *LangChain Expression Language*.
- **`langchain-community`** — integraciones de terceros.
    - **Paquetes de socios** (por ejemplo `langchain-openai`, `langchain-anthropic`): algunas
      integraciones se han separado en paquetes ligeros propios que solo dependen de
      `langchain-core`.
- **`langchain`** — cadenas, agentes y estrategias de recuperación que conforman la arquitectura
  cognitiva de la aplicación.
- **`langgraph`** — construir aplicaciones multi-actor robustas y con estado, modelando los pasos
  como nodos y aristas de un grafo. Ver [LangGraph](../../11_JARVIS/llm_workflows/langgraph.md).
- **`langserve`** — desplegar cadenas de LangChain como APIs REST.

## Ecosistema

El ecosistema más amplio incluye:

- **LangSmith**: una plataforma para desarrolladores que permite depurar, probar, evaluar y
  monitorear aplicaciones con LLM, integrándose de forma nativa con LangChain.

## Ver también

- [Chatbot RAG con LangChain](chatbot_rag_con_langchain.md)
- [RAG para documentación técnica](rag_para_documentacion_tecnica.md)
