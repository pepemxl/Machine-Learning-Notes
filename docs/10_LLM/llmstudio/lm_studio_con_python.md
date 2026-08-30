# LM Studio con Python


Para simplificar el uso interactivo, `lmstudio-python` ofrece una **API de conveniencia** que
gestiona sus recursos mediante *hooks* de `atexit`, permitiendo usar una sesión de cliente
síncrona por defecto a lo largo de varios comandos interactivos.

Esta API aparece en los ejemplos de la documentación bajo la pestaña
`Python (convenience API)`, junto a los ejemplos de `Python (scoped resource API)`, que usan
sentencias `with` para garantizar una liberación determinista de los recursos de comunicación
de red.

La API de conveniencia permite usar el REPL estándar de Python —o alternativas más flexibles
como los Jupyter Notebooks— para interactuar con los modelos cargados en LM Studio. Por
ejemplo:

```shell
  title: "Python REPL"
  variants:
    "Interactive chat session":
      language: python
      code: |
        >>> import lmstudio as lms
        >>> loaded_models = lms.list_loaded_models()
        >>> for idx, model in enumerate(loaded_models):
        ...     print(f"{idx:>3} {model}")
        ...
          0 LLM(identifier='qwen2.5-7b-instruct')
        >>> model = loaded_models[0]
        >>> chat = lms.Chat("You answer questions concisely")
        >>> chat = lms.Chat("You answer questions concisely")
        >>> chat.add_user_message("Tell me three fruits")
        UserMessage(content=[TextData(text='Tell me three fruits')])
        >>> print(model.respond(chat, on_message=chat.append))
        Banana, apple, orange.
        >>> chat.add_user_message("Tell me three more fruits")
        UserMessage(content=[TextData(text='Tell me three more fruits')])
        >>> print(model.respond(chat, on_message=chat.append))
        Mango, strawberry, avocado.
        >>> chat.add_user_message("How many fruits have you told me?")
        UserMessage(content=[TextData(text='How many fruits have you told me?')])
        >>> print(model.respond(chat, on_message=chat.append))
        You asked for three initial fruits and three more, so I've listed a total of six fruits.
```

Aunque no está pensada principalmente para este uso, la API de concurrencia estructurada
asíncrona del SDK es compatible con el REPL asíncrono de Python que se lanza con
`python -m asyncio`. Por ejemplo:

```shell2
  title: "Python REPL"
  variants:
    "Asynchronous chat session":
      language: python
      code: |
        # Nota: asume el uso del REPL asincrono "python -m asyncio" (o equivalente)
        # Requiere el SDK de Python 1.5.0 o posterior
        >>> from contextlib import AsyncExitStack
        >>> import lmstudio as lms
        >>> resources = AsyncExitStack()
        >>> client = await resources.enter_async_context(lms.AsyncClient())
        >>> loaded_models = await client.llm.list_loaded()
        >>> for idx, model in enumerate(loaded_models):
        ...     print(f"{idx:>3} {model}")
        ...
          0 AsyncLLM(identifier='qwen2.5-7b-instruct-1m')
        >>> model = loaded_models[0]
        >>> chat = lms.Chat("You answer questions concisely")
        >>> chat.add_user_message("Tell me three fruits")
        UserMessage(content=[TextData(text='Tell me three fruits')])
        >>> print(await model.respond(chat, on_message=chat.append))
        Apple, banana, and orange.
        >>> chat.add_user_message("Tell me three more fruits")
        UserMessage(content=[TextData(text='Tell me three more fruits')])
        >>> print(await model.respond(chat, on_message=chat.append))
        Mango, strawberry, and pineapple.
        >>> chat.add_user_message("How many fruits have you told me?")
        UserMessage(content=[TextData(text='How many fruits have you told me?')])
        >>> print(await model.respond(chat, on_message=chat.append))
        You asked for three fruits initially, then three more, so I've listed six fruits in total.

```

## Ver también

- [Introducción a LM Studio](introduccion_lm_studio.md)
- [Instalación de LM Studio](instalacion_lm_studio.md)
- [LM Studio con Claude Code](../LOCAL_LLM/lm_studio_con_claude_code.md)
