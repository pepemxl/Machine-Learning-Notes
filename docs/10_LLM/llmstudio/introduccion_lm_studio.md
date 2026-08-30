# Introducción a LM Studio

`lmstudio-python` ofrece un conjunto de APIs para interactuar con [LLMs](../introduccion.md), modelos de embeddings y flujos agénticos.

## Instalar el SDK

`lmstudio-python` está disponible como paquete de PyPI. Puedes instalarlo con `pip`.

```bash
pip install lmstudio
```

Para el código fuente y contribuir al proyecto, visita [lmstudio-python](https://github.com/lmstudio-ai/lmstudio-python) en GitHub.

## Funcionalidades

- Usar LLMs para [responder en chats](https://lmstudio.ai/docs/python/llm-prediction/chat-completion) o predecir [completados de texto](https://lmstudio.ai/docs/python/llm-prediction/completion).
- Definir funciones como herramientas y convertir los LLMs en [agentes autónomos](https://lmstudio.ai/docs/python/agent/act) que se ejecutan completamente en local.
- [Cargar](https://lmstudio.ai/docs/python/manage-models/loading), [configurar](https://lmstudio.ai/docs/python/llm-prediction/parameters) y [descargar](https://lmstudio.ai/docs/python/manage-models/loading) modelos de memoria.
- Generar embeddings de texto, y más.

## Ejemplo rápido: chatear con un modelo Llama

```python title="Python (convenience API)" linenums="1"
import lmstudio as lms

model = lms.llm("qwen/qwen3-4b-2507")
result = model.respond("What is the meaning of life?")

print(result)
```

```python title="Python (scoped resource API)" linenums="1"
import lmstudio as lms

with lms.Client() as client:
    model = client.llm.model("qwen/qwen3-4b-2507")
    result = model.respond("What is the meaning of life?")

    print(result)
```

```python title="Python (asynchronous API)" linenums="1"
# Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
# Requires Python SDK version 1.5.0 or later
import lmstudio as lms

async with lms.AsyncClient() as client:
    model = await client.llm.model("qwen/qwen3-4b-2507")
    result = await model.respond("What is the meaning of life?")

    print(result)
```


### Obtener modelos locales

El código anterior requiere el modelo [qwen3-4b-2507](https://lmstudio.ai/models/qwen/qwen3-4b-2507).
Si no lo tienes, ejecuta el siguiente comando en la terminal para descargarlo.

```bash
lms get qwen/qwen3-4b-2507
```

Más información sobre `lms get` en la [documentación del CLI de LM Studio](https://lmstudio.ai/docs/cli/get).

## ¿Conveniencia interactiva, gestión determinista de recursos o concurrencia estructurada?

Como se ve en el ejemplo anterior, hay **tres enfoques distintos** para trabajar con el SDK de
Python de LM Studio.

El primero es la **API de conveniencia interactiva** (aparece como *Python (convenience API)* en
los ejemplos), centrada en usar una instancia de cliente por defecto para interacciones cómodas
en un prompt síncrono de Python, o al usar Jupyter notebooks.

El segundo es la **API síncrona de recursos con ámbito** (*Python (scoped resource API)*), que
usa gestores de contexto para garantizar que los recursos asignados —como las conexiones de
red— se liberen de forma determinista, en lugar de quedar potencialmente abiertos hasta que
termine el proceso completo.

El último es la **API asíncrona de concurrencia estructurada** (*Python (asynchronous API)*),
diseñada para programas asíncronos que siguen los principios de la
["concurrencia estructurada"](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/),
de modo que las tareas en segundo plano que gestionan las conexiones del SDK con el servidor de
la API se manejen correctamente. Las aplicaciones asíncronas que no sigan esos principios
tendrán que apoyarse en acceso por hilos a la API síncrona con ámbito, en lugar de intentar usar
la API asíncrona nativa del SDK. La versión 1.5.0 del SDK es la primera que soporta
completamente la API asíncrona.

Algunos ejemplos son comunes a la API de conveniencia interactiva y a la API síncrona con
ámbito; esos aparecen listados como *Python (synchronous API)*.

## Timeouts en la API síncrona

*Versión mínima del SDK de Python*: **1.5.0**

A partir de la versión 1.5.0 del SDK, la API síncrona expira por defecto tras **60 segundos sin
actividad** mientras espera una respuesta o una notificación de evento en streaming desde el
servidor de la API.

El número de segundos de espera se puede ajustar con la función
`lmstudio.set_sync_api_timeout()`. Fijar el timeout a `None` lo desactiva por completo,
restaurando el comportamiento de versiones anteriores del SDK.

El timeout actual se puede consultar con la función `lmstudio.get_sync_api_timeout()`.

## Timeouts en la API asíncrona

*Versión mínima del SDK de Python*: **1.5.0**

Como las corrutinas asíncronas admiten cancelación, la API asíncrona no implementa un soporte
específico de timeout. En su lugar deben usarse los mecanismos generales de timeout asíncrono,
como [`asyncio.wait_for()`](https://docs.python.org/3/library/asyncio-task.html#asyncio.wait_for)
o [`anyio.move_on_after()`](https://anyio.readthedocs.io/en/stable/cancellation.html#timeouts).



