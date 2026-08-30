# Como mantener el contexto en nuestros MCPs 

- https://claude.com/blog/using-claude-md-files
- https://www.anthropic.com/engineering/claude-code-best-practices


Para mantener el contexto en proyectos usando Claude Code entre sesiones y evitar pérdidas por resets de contexto.

Usaremos un archivo `CLAUDE.md` en la raíz del proyecto: Claude lo lee automáticamente al iniciar. 


1. Pon las instrucciones persistentes 
    - arquitectura
    - guidelines
2. Claude trabaja por directorio: Claude mantiene conversaciones separadas por carpeta para evitar contaminación de contexto.
3. Reiniciar sesiones: Usa `--resume` o el comando `/resume` para continuar una sesión anterior con su historial.
4. Checkpoints automáticos: Claude guarda estados antes de cambios, persistentes entre sesiones.
5. Para estado manual: Al final de cada sesión, pide a Claude que actualice un archivo como PROJECT_STATUS.md o .dev-notes.md con resumen de progreso, decisiones pendientes y tareas.

## Ejemplo 1

```bash title="Ejemplo"
# Bash commands
- npm run build: Build the project
- npm run typecheck: Run the typechecker

# Code style
- Use ES modules (import/export) syntax, not CommonJS (require)
- Destructure imports when possible (eg. import { foo } from 'bar')

# Workflow
- Be sure to typecheck when you’re done making a series of code changes
- Prefer running single tests, and not the whole test suite, for performance
```

Una buena practica es tener uno local que ignores en git mientras aprender a usarlo `CLAUDE.local.md`.

## Ejemplo 2

```bash title="Ejemplo" linenums="1"
# Project Context

When working with this codebase, prioritize readability over cleverness. Ask clarifying questions before making architectural changes.

## About This Project

FastAPI REST API for user authentication and profiles. Uses SQLAlchemy for database operations and Pydantic for validation.

## Key Directories

- `app/models/` - database models
- `app/api/` - route handlers
- `app/core/` - configuration and utilities

## Standards

- Type hints required on all functions
- pytest for testing (fixtures in `tests/conftest.py`)
- PEP 8 with 100 character lines

## Common Commands

uvicorn app.main:app --reload  # dev server
pytest tests/ -v               # run tests

## Notes

All routes use `/api/v1` prefix. JWT tokens expire after 24 hours.
```


## Sistema de Archivos de Contexto

```bash
proyecto/
├── context/
│   ├── proyecto.md        # Descripción general
│   ├── decisiones.md      # Decisiones técnicas
│   ├── arquitectura.md    # Estructura del proyecto
│   └── contexto_actual.md # Último estado
├── docs/
│   └── especificaciones.md
└── .claude-context       # Archivo para Claude Code tambien puede ser un directorio
```

## Archivo `.claude-context`

```markdown
# CONTEXTO DEL PROYECTO - [Nombre del Proyecto]

## ESTADO ACTUAL

- Últimos cambios: [Fecha]
- Progreso: [Descripción breve]
- Próximos pasos: [Lista]

## DECISIONES TÉCNICAS

1. [Decisión 1 con justificación]
2. [Decisión 2 con justificación]

## ESTRUCTURA CRÍTICA

bash
/proyecto
  ├── src/
  │   ├── modules/    # Lógica principal
  │   └── utils/      # Funciones helper
  └── config/         # Configuraciones


## CÓDIGO RELEVANTE

### Archivos importantes:

- `src/main.js`: Punto de entrada
- `config/settings.js`: Configuraciones clave

### Informacion de puntos tratados en la sesion anterior

- Fue creado X
- Fue actualizado Y

```


## Uso de Comentarios Contextuales
```javascript
// CONTEXTO: Este módulo maneja [función]
// RELACIONADO: src/modules/related.js
// DECISIÓN: Usamos X porque [razón]
// PENDIENTE: Implementar Y en la próxima iteración

class MiClase {
  // ... código
}
```

## Documentación por Sesión

Crea un archivo por sesión:
```text
context/sesiones/
├── 2024-01-15_sesion1.md
├── 2024-01-16_sesion2.md
└── resumen_progreso.md
```
