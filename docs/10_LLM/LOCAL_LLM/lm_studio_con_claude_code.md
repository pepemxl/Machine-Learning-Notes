# LM Studio con Claude Code

Claude Code puede comunicarse con LM Studio a través del endpoint compatible con Anthropic
`POST /v1/messages`.

Ver: [Anthropic-compatible Messages endpoint](https://lmstudio.ai/docs/developer/anthropic-compat/messages).

Para otras vías de ejecutar modelos en local —Ollama, proxies— ver
[LLMs locales](llms_locales.md).

## 1) Arrancar el servidor local de LM Studio

Asegúrate de que LM Studio esté corriendo como servidor (puerto `1234` por defecto).

Puedes arrancarlo desde la aplicación, o desde la terminal con `lms`:

```bash
lms server start --port 1234
```

## 2) Configurar Claude Code

Define estas variables de entorno para que el CLI `claude` apunte a tu LM Studio local:

```bash
export ANTHROPIC_BASE_URL=http://localhost:1234
export ANTHROPIC_AUTH_TOKEN=lmstudio
```

Nota: si tienes activada la opción *Require Authentication*, pon en `ANTHROPIC_AUTH_TOKEN` tu
token de API de LM Studio. Más información en
[Authentication](https://lmstudio.ai/docs/developer/core/authentication).

## 3) Ejecutar Claude Code contra un modelo local

```bash
claude --model openai/gpt-oss-20b
```

!!! tip "Consejo"
    Usa un modelo —y una configuración de servidor y modelo— con **más de ~25k de longitud de
    contexto**. Herramientas como Claude Code consumen mucho contexto.

## 4) Si *Require Authentication* está activado

Si activaste *Require Authentication* en LM Studio, crea un token de API y define:

```bash
export LM_API_TOKEN=<LMSTUDIO_TOKEN>
export ANTHROPIC_AUTH_TOKEN=$LM_API_TOKEN
```

Con *Require Authentication* activado, LM Studio acepta tanto la cabecera `x-api-key` como
`Authorization: Bearer <token>`.

Si tienes problemas, puedes acudir al [Discord de LM Studio](https://discord.gg/lmstudio).

## Ver también

- [Introducción a LM Studio](../llmstudio/introduccion_lm_studio.md)
- [Requerimientos de hardware](../requerimientos_de_hardware.md)
