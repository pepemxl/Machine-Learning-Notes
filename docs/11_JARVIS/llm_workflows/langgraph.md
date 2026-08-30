# LangGraph

**LangGraph** es una biblioteca de código abierto desarrollada por **LangChain** para construir aplicaciones impulsadas por modelos de lenguaje (LLMs) que requieren flujos de trabajo complejos, con estados y ciclos. A diferencia de los enfoques lineales tradicionales de LangChain (como las cadenas secuenciales), LangGraph permite crear aplicaciones con **grafos dirigidos** donde los nodos representan acciones o pasos, y las aristas definen transiciones condicionales. Es especialmente útil para aplicaciones que necesitan interacciones dinámicas, como agentes de IA, flujos conversacionales o pipelines de procesamiento iterativo.


LangGraph es una biblioteca de Python que se usa para orquestar cómo los LLMs interactúan con datos, herramientas externas y estados.

## Características Clave de LangGraph

1. **Estructura de Grafos**:
   - Los flujos de trabajo se modelan como grafos dirigidos.
   - **Nodos**: Representan tareas, como invocar un LLM, ejecutar una herramienta (ej. búsqueda web), o procesar datos.
   - **Aristas**: Definen transiciones entre nodos, que pueden ser condicionales (basadas en lógica o resultados del LLM).

2. **Gestión de Estado**:
   - Usa un **StateGraph** para mantener un estado persistente (como un diccionario) que se actualiza a medida que el flujo avanza.
   - Ideal para aplicaciones donde el contexto o los datos cambian dinámicamente (ej. conversaciones multi-turno).

3. **Ciclo y Feedback**:
   - Soporta ciclos!!!, permitiendo que el flujo regrese a nodos anteriores si es necesario (por ejemplo, para refinar una respuesta del LLM).
   - Útil para agentes de IA que toman decisiones iterativas o requieren retroalimentación.

4. **Integración con LangChain**:
   - Se basa en el ecosistema de LangChain, por lo que se integra con herramientas como retrievers, bases de datos vectoriales, y APIs de LLMs (como OpenAI, Anthropic, o modelos locales en LM Studio).
   - Soporta herramientas externas, como búsquedas en la web o ejecución de código.

5. **Flexibilidad**:
   - Permite personalizar flujos complejos, como agentes que combinan planificación, ejecución de herramientas y revisión de resultados.
   - Compatible con cualquier LLM que LangChain soporte (GPT-5, Claude, LLaMA, Grok, etc.).

## Ejemplo Práctico

Imagina que quieres crear un agente que genera código, lo valida ejecutándolo y lo mejora iterativamente:
- Con **LangGraph**, defines un grafo donde:
  - Nodo 1: Genera código usando un LLM (ej. Grok desde LM Studio).
  - Nodo 2: Ejecuta el código en un entorno local (usando herramientas de LangChain).
  - Nodo 3: Evalúa el resultado y, si hay errores, regresa al Nodo 1 para corregir.
  - Aristas condicionales: Decide si continuar o iterar basado en el éxito del código.
- **Codex CLI** podría generar el código inicial directamente en la terminal, pero no gestiona el flujo iterativo.
- **Cursor CLI** podría revisar el código en un pipeline CI/CD, pero no orquesta ciclos complejos.
- **LM Studio** podría ejecutar el modelo localmente para generar el código, pero no ofrece la lógica de grafo.

### Código de Ejemplo (LangGraph)

```python
from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI

# Definir el estado
from typing import Dict
class State(Dict):
    code: str
    error: str

# Nodo para generar código
def generate_code(state: State) -> State:
    llm = ChatOpenAI(model="gpt-5")  # O cualquier modelo, ej. vía LM Studio
    prompt = "Genera un script Python para calcular el factorial."
    response = llm.invoke([HumanMessage(content=prompt)])
    state["code"] = response.content
    return state

# Nodo para validar código
def validate_code(state: State) -> State:
    try:
        exec(state["code"])
        state["error"] = ""
    except Exception as e:
        state["error"] = str(e)
    return state

# Definir el grafo
workflow = StateGraph(State)
workflow.add_node("generate", generate_code)
workflow.add_node("validate", validate_code)
workflow.add_edge("generate", "validate")
workflow.add_conditional_edges("validate", 
    lambda state: "generate" if state["error"] else END,
    {"generate": "generate", END: END}
)
workflow.set_entry_point("generate")

# Compilar y ejecutar
app = workflow.compile()
result = app.invoke({"code": "", "error": ""})
print(result["code"])
```

Usemos un entorno local con LM Studio. Para ello usaremos LM Studio para ejecutar un modelo local y conectarlo a LangGraph mediante la API local de LM Studio.
- Configuramos LM Studio para servir un modelo como servidor HTTP.
- Usa LangChain para conectar LangGraph al endpoint de LM Studio (en lugar de OpenAI o Anthropic).

