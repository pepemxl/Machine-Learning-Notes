# Instalación de LM Studio


`lmstudio` es una librería publicada en PyPI que permite usar `lmstudio-python` en tus propios
proyectos. Es de código abierto y se desarrolla en GitHub; puedes encontrar el código fuente
[aquí](https://github.com/lmstudio-ai/lmstudio-python).

## Instalar `lmstudio-python`

Al estar publicado en PyPI, `lmstudio-python` se puede instalar con `pip` o con tu gestor de
dependencias preferido. A continuación se muestran `pdm` y `uv`, pero otras herramientas de
gestión de proyectos Python ofrecen comandos equivalentes para añadir dependencias.

```lms_code_snippet
  variants:
    pip:
      language: bash
      code: |
        pip install lmstudio
    pdm:
      language: bash
      code: |
        pdm add lmstudio
    uv:
      language: bash
      code: |
        uv add lmstudio
```

## Personalizar el host y el puerto TCP del servidor

Todos los ejemplos de la documentación asumen que la API del servidor corre en local en uno de
los puertos por defecto de la aplicación. Nota: en versiones del SDK anteriores a la 1.5.0, el
SDK además requería que el servidor HTTP REST opcional estuviera habilitado.

La ubicación de red de la API se puede sobrescribir pasando una cadena `"host:puerto"` al crear
la instancia del cliente.

```lms_code_snippet
  variants:
    "Python (convenience API)":
      language: python
      code: |
        import lmstudio as lms
        SERVER_API_HOST = "localhost:1234"

        # This must be the *first* convenience API interaction (otherwise the SDK
        # implicitly creates a client that accesses the default server API host)
        lms.configure_default_client(SERVER_API_HOST)

        # Note: the dedicated configuration API was added in lmstudio-python 1.3.0
        # For compatibility with earlier SDK versions, it is still possible to use
        # lms.get_default_client(SERVER_API_HOST) to configure the default client

    "Python (scoped resource API)":
      language: python
      code: |
        import lmstudio as lms
        SERVER_API_HOST = "localhost:1234"

        # When using the scoped resource API, each client instance
        # can be configured to use a specific server API host
        with lms.Client(SERVER_API_HOST) as client:
            model = client.llm.model()

            for fragment in model.respond_stream("What is the meaning of life?"):
                print(fragment.content, end="", flush=True)
            print() # Advance to a new line at the end of the response

    "Python (asynchronous API)":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms
        SERVER_API_HOST = "localhost:1234"

        # When using the asynchronous API, each client instance
        # can be configured to use a specific server API host
        async with lms.AsyncClient(SERVER_API_HOST) as client:
            model = await client.llm.model()

            for fragment in await model.respond_stream("What is the meaning of life?"):
                print(fragment.content, end="", flush=True)
            print() # Advance to a new line at the end of the response
```

### Comprobar que el servidor especificado está corriendo

*Versión mínima del SDK de Python*: **1.5.0**

Aunque el patrón de conexión más habitual es dejar que el SDK lance una excepción si no puede
conectarse al servidor indicado, el SDK también permite ejecutar la comprobación directamente,
sin crear antes una instancia de cliente:

```lms_code_snippet
  variants:
    "Python (synchronous API)":
      language: python
      code: |
        import lmstudio as lms
        SERVER_API_HOST = "localhost:1234"

        if lms.Client.is_valid_api_host(SERVER_API_HOST):
            print(f"An LM Studio API server instance is available at {SERVER_API_HOST}")
        else:
            print("No LM Studio API server instance found at {SERVER_API_HOST}")

    "Python (asynchronous API)":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms
        SERVER_API_HOST = "localhost:1234"

        if await lms.AsyncClient.is_valid_api_host(SERVER_API_HOST):
            print(f"An LM Studio API server instance is available at {SERVER_API_HOST}")
        else:
            print("No LM Studio API server instance found at {SERVER_API_HOST}")
```


### Determinar el puerto local por defecto



Cuando no se especifica un host, el SDK consulta varios puertos de la interfaz local de
*loopback* buscando una instancia del servidor en ejecución. Este escaneo se repite con cada
nueva instancia de cliente. En lugar de dejar que el SDK lo haga de forma implícita, se puede
ejecutar el escaneo explícitamente y pasar los datos obtenidos al crear los clientes:

```lms_code_snippet
  variants:
    "Python (synchronous API)":
      language: python
      code: |
        import lmstudio as lms

        api_host = lms.Client.find_default_local_api_host()
        if api_host is not None:
            print(f"An LM Studio API server instance is available at {api_host}")
          else:
            print("No LM Studio API server instance found on any of the default local ports")

    "Python (asynchronous API)":
      language: python
      code: |
        # Note: assumes use of an async function or the "python -m asyncio" asynchronous REPL
        # Requires Python SDK version 1.5.0 or later
        import lmstudio as lms

        api_host = await lms.AsyncClient.find_default_local_api_host()
        if api_host is not None:
            print(f"An LM Studio API server instance is available at {api_host}")
          else:
            print("No LM Studio API server instance found on any of the default local ports")
```

## Ver también

- [Introducción a LM Studio](introduccion_lm_studio.md)
- [LM Studio con Python](lm_studio_con_python.md)
