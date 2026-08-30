# Prompting

El **prompt** es la entrada que le das a un [LLM](introduccion.md). Diseñarlo bien es la forma
más barata de mejorar los resultados: no requiere reentrenar nada ni cambiar de modelo.

## Anatomía de un prompt

| Elemento | Función |
|---|---|
| **Rol / sistema** | Fija el comportamiento y las restricciones generales |
| **Instrucción** | Qué hay que hacer, en imperativo y sin ambigüedad |
| **Contexto** | Los datos sobre los que operar |
| **Ejemplos** | Demostraciones del formato o del razonamiento esperado |
| **Formato de salida** | Cómo debe estructurarse la respuesta |

## Técnicas

**Zero-shot** — solo la instrucción, sin ejemplos. Es el punto de partida: pruébalo antes de
complicar nada.

**Few-shot** — se incluyen unos pocos ejemplos de entrada y salida. Es especialmente efectivo
para fijar un **formato** concreto. Basta con 2–5 ejemplos; más suele aportar poco y consume
contexto.

**Chain-of-thought** — se pide al modelo que razone paso a paso antes de responder. Mejora
notablemente las tareas de razonamiento aritmético y lógico. Los modelos de razonamiento
recientes lo hacen de forma nativa, por lo que forzarlo explícitamente ya no siempre ayuda.

**Descomposición** — dividir una tarea compleja en varias llamadas más simples y encadenarlas.
Cada paso se verifica por separado, lo que hace el sistema mucho más depurable que un único
prompt monolítico.

## Buenas prácticas

- **Sé específico sobre el formato de salida.** Si necesitas JSON, muestra el esquema exacto.
- **Pon las instrucciones antes del contexto largo**, y repítelas brevemente al final si el
  contexto es muy extenso.
- **Usa delimitadores claros** (etiquetas XML, triple comilla) para separar instrucciones de
  datos. Esto además reduce la superficie de *prompt injection*.
- **Di qué hacer, no qué evitar.** "Responde solo con el nombre" funciona mejor que "no
  añadas explicaciones".
- **Da una salida de escape.** Indica explícitamente qué responder cuando el modelo no sabe,
  para reducir alucinaciones.
- **Itera midiendo.** Sin un conjunto de casos de prueba, cualquier cambio en el prompt es una
  corazonada.

## Riesgos

- **Prompt injection** — texto en los datos de entrada que el modelo interpreta como
  instrucción. Nunca trates el contenido recuperado —de un
  [RAG](RAGS/chatbot_rag_con_langchain.md), de una web, de un archivo— como instrucciones de
  confianza.
- **Sobreajuste al ejemplo** — si todos tus ejemplos comparten un patrón accidental, el modelo
  lo copiará.
- **Deriva entre modelos** — un prompt afinado para un modelo no se transfiere necesariamente a
  otro. Reevalúa al cambiar de versión.

## Ver también

- [Manejo de contexto en MCP](MCP/manejo_de_contexto.md)
- [Prompt: Puzzle Solver](../11_JARVIS/prompts/puzzle_solver.md) — un ejemplo completo.
