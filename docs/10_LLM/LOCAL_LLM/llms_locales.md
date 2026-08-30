# Local LLMs

Vamos a empezar con Claude Code en un entorno completamente local.

El "Claude Code" oficial está diseñado para conectarse a los servidores de Anthropic. Sin embargo, gracias a que herramientas como Ollama y vLLM ahora ofrecen una API compatible con la de Anthropic, podemos "engañar" a Claude Code para que, en lugar de ir a internet, hable con un modelo que se ejecuta en tu propia máquina.

## Método 1: La Vía Rápida con Ollama

Este es el método más popular para empezar. Usaremos **Ollama** como servidor local y configuraremos Claude Code para que se conecte a él.

**Paso 1: Instalar y preparar Ollama**

Primero, necesitas instalar Ollama y descargar un modelo. Es crucial que el modelo que elijas **soporte "tool calling" (llamada de herramientas)** , de lo contrario, Claude Code no podrá leer archivos ni ejecutar comandos .

```bash
# 1. Instalar Ollama
curl -fsSL https://ollama.ai/install.sh | sh

# 2. Verifica que esté corriendo (debería responder "Ollama is running")
curl http://localhost:11434

# 3. DESCARGAR UN MODELO APTO. Por ejemplo 'gpt-oss:20b'.
ollama pull gpt-oss:20b
```
**Selección del modelo:** No todos los modelos funcionan. Por ejemplo, `qwen3-coder:30b` es excelente para código pero **carece de soporte para "tools"** . Modelos como `gpt-oss:20b` o `qwen3:32b` sí lo tienen . Puedes verificar las capacidades de un modelo con:
```bash
ollama show gpt-oss:20b
# Busca "tools" en la lista de capacidades
```

**Paso 2: Instalar Claude Code (de forma global, como vimos antes)**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**Paso 3: Configurar las variables de entorno**

Aquí viene la magia. Le decimos a Claude Code que use nuestro servidor local de Ollama en lugar del de Anthropic.

Puedes hacerlo de dos maneras:
*   **Opción A (Variables de entorno):** Ejecuta estos comandos en tu terminal antes de usar `claude`.
    ```bash
    export ANTHROPIC_BASE_URL="http://localhost:11434"
    export ANTHROPIC_API_KEY="ollama"       # Ollama no requiere clave, pero el cliente la pide
    export ANTHROPIC_AUTH_TOKEN="ollama"    # Ídem
    ```
*   **Opción B (Configuración global de Claude Code):** Para no tener que escribir las variables cada vez, créate el archivo de configuración `~/.claude/settings.json` .
    ```json
    {
      "env": {
        "ANTHROPIC_BASE_URL": "http://localhost:11434",
        "ANTHROPIC_API_KEY": "ollama",
        "ANTHROPIC_AUTH_TOKEN": "ollama"
      }
    }
    ```

**Paso 4: ¡Ejecutar!**
```bash
claude --model gpt-oss:20b
```
Si todo ha ido bien, Claude Code se iniciará y usará el modelo local. Para asegurarte de que es completamente local, **desconéctate de internet y haz una prueba** .

### 🧪 Método 2: Proxies y Herramientas Especializadas (Para usuarios avanzados)

La comunidad ha creado herramientas que actúan como un puente más sofisticado, solucionando problemas de compatibilidad y ofreciendo más opciones.

*   **AnyClaude-Local **: Es un "proxy" escrito en TypeScript (para Bun/Node.js) que intercepta las llamadas de Claude Code y las dirige a backends locales como **LM Studio** o **vLLM-MLX** (ideal para Apple Silicon). Es una opción muy robusta si buscas algo más configurable.
    ```bash
    # Requiere Bun instalado
    git clone https://github.com/akaszubski/anyclaude-local.git
    cd anyclaude-local
    bun install
    bun run build
    bun install -g $(pwd) # Instala el comando 'anyclaude' globalmente
    anyclaude # Listo!
    ```

*   **Claude Code Go **: Esta es una **reimplementación completa** de Claude Code en Go. No es un proxy, sino una versión independiente que ya viene configurada para trabajar con LM Studio. Si te gusta la idea de usar un binario compilado y liviano, esta es tu opción.

### ⚠️ Expectativas y Realidades

Es emocionante poder hacer esto, pero es importante ser realista. Un modelo local no se comportará igual que el Claude 3.5 Sonnet de pago.

*   **Velocidad:** La inferencia local es significativamente más lenta. Una respuesta simple puede tomar **minutos** en lugar de segundos, especialmente si no tienes una GPU potente .
*   **Fiabilidad del Modelo:** Los modelos pequeños (7B-14B) pueden tener problemas para seguir las instrucciones complejas de Claude Code .
    *   Pueden generar explicaciones que no coinciden con el código que escriben .
    *   Algunos modelos no soportan "tool calling", lo que hace que Claude Code falle al intentar leer un archivo .
    *   En ocasiones, en lugar de ejecutar una herramienta, el modelo puede limitarse a imprimir el código JSON de la herramienta que intenta usar .
*   **Modelos Probados:** En diversas pruebas, los modelos que mejor se han comportado (con soporte para herramientas y razonamiento) son `gpt-oss:20b` y `qwen3:32b`. Otros como `qwen2.5-coder` (en varias versiones) y `llama3.1` han mostrado problemas de inconsistencia y velocidad .

### Tabla Comparativa de Métodos

| Método | Backend Local | Complejidad | Ventajas | Desventajas |
| :--- | :--- | :--- | :--- | :--- |
| **Ollama + ENV Vars**  | Ollama | Baja | Sencillo, rápido de configurar. | Dependencia de que el modelo en Ollama sea 100% compatible. |
| **vLLM**  | vLLM | Media | Muy potente, ideal para producción y GPUs NVIDIA. Soporte nativo de tool calling. | Configuración más compleja (Docker, flags específicos). |
| **AnyClaude-Local**  | LM Studio / vLLM-MLX | Media | Muy flexible, soporta múltiples backends, auto-limpieza. | Requiere Bun, es una capa adicional de complejidad. |
| **Claude Code Go**  | LM Studio | Baja | Binario independiente, reimplementación en Go, rápido. | Proyecto independiente, puede no estar tan actualizado como el oficial. |

En resumen, mi recomendación es que empieces con **Ollama y el modelo `gpt-oss:20b`** . Es la vía más directa para que experimentes y veas cómo se comporta en tu equipo y con tus proyectos. Ajusta tus expectativas sobre la velocidad y prepárate para probar algunos comandos para ver qué tan bien entiende el modelo tus instrucciones.

¿Tienes una GPU potente en tu equipo o planeas ejecutarlo principalmente en CPU? Con eso podremos afinar mejor la recomendación del modelo.