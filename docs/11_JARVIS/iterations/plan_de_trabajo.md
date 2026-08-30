# Plan de Trabajo

### Cómo crear un plan de trabajo y seguimiento en archivos Markdown para agentes de código en un proyecto

Trabajar con **agentes de código IA** (como los de CrewAI, AutoGen, Claude Code, Cursor o GitHub Copilot) requiere un contexto claro y persistente. Los archivos Markdown (.md) son ideales porque son legibles por humanos y máquinas, versionables en Git y fáciles de actualizar.

La mejor práctica es estructurar el proyecto con una carpeta dedicada (por ejemplo, `context/` o `.project/`) que contenga varios archivos MD para separar el plan, las tareas y el seguimiento. Esto evita perder contexto entre sesiones y permite que los agentes lean/actualicen automáticamente.

#### Estructura recomendada de archivos Markdown

Crea una carpeta `context/` en la raíz del proyecto con estos archivos:

1. **01-requirements.md** → Requisitos y objetivos del proyecto.
2. **02-analysis.md** → Análisis inicial (arquitectura actual, dependencias, mejoras).
3. **03-plan.md** → Plan de trabajo detallado (fases, timeline).
4. **04-backlog.md** o **tasks.md** → Lista de tareas con seguimiento (backlog y progreso).
5. **AGENTS.md** (en la raíz) → Instrucciones generales para los agentes IA (estándar recomendado).

Opcional: **progress.md** para resúmenes diarios o **report.md** para informes finales.

#### Ejemplo paso a paso para crear el plan

1. **Define los requisitos (01-requirements.md)**

```markdown
# Requisitos del Proyecto

## Objetivo General
Crear una aplicación web para gestión de tareas con autenticación y base de datos.

## Funcionalidades Principales
- Registro e inicio de sesión de usuarios.
- Crear, editar y eliminar tareas.
- Dashboard con estadísticas.

## Requisitos No Funcionales
- Tecnologías: Python (FastAPI), React, PostgreSQL.
- Debe ser responsive y seguro (JWT).
- Tests unitarios > 80% cobertura.

## Público Objetivo
Usuarios individuales para productividad personal.
```

2. **Haz un análisis inicial (02-analysis.md)**

Los agentes IA pueden generar esto automáticamente leyendo el código existente.

```markdown
# Análisis del Proyecto

## Arquitectura Actual
- Backend: FastAPI en /api/
- Frontend: React en /frontend/
- Base de datos: SQLite (migrar a PostgreSQL)

## Tecnologías Utilizadas
- Python 3.12, React 18, Tailwind CSS

## Áreas de Mejora
- Añadir autenticación.
- Implementar tests faltantes.
```

3. **Crea el plan de trabajo (03-plan.md)**

```markdown
# Plan de Trabajo

## Fases del Proyecto
### Fase 1: Setup y Autenticación (Semana 1-2)
- Configurar entorno.
- Implementar JWT.

### Fase 2: CRUD de Tareas (Semana 3)
- Backend endpoints.
- Frontend interfaz.

### Fase 3: Dashboard y Tests (Semana 4)
- Estadísticas.
- Tests e2e.

## Timeline Estimado
- Inicio: 01/01/2026
- Entrega MVP: 31/01/2026

## Riesgos
- Dependencias de base de datos.
- Mitigación: Usar mocks en tests.
```

4. **Backlog y seguimiento de tareas (04-backlog.md)**

Usa checkboxes de Markdown para tracking visual. Los agentes pueden actualizar estados automáticamente (ej.: cambiar [ ] a [x]).

```markdown
# Backlog y Progreso

## Seguimiento General
- Progreso total: 0% (actualizar al finalizar fases)
- Tareas completadas: 0/15

## Tareas

### Backlog
- [ ] Configurar proyecto base
- [ ] Implementar modelo User en DB
- [ ] Endpoint de login

### En Progreso
- [ ] (ninguna)

### Completadas
- [x] Análisis inicial (01/01/2026 - Detalles: Revisado arquitectura)

## Instrucciones para Agentes
Al completar una tarea:
- Marca como [x]
- Añade fecha y resumen.
- Actualiza % de progreso.
```

#### Mejores prácticas para agentes de código

- **AGENTS.md** (en raíz del repo): Archivo estándar que todos los agentes modernos leen (Cursor, Claude, Copilot, etc.).

```markdown
# Instrucciones para Agentes IA

## Comandos Principales
- Build: `npm run build`
- Tests: `pytest`
- Lint: `ruff check`

## Estilo de Código
- Usa black para formateo.
- Siempre añade tests.

## Límites
- Nunca modifiques archivos fuera de /src/
- Pregunta antes de cambios mayores.
- Al finalizar tarea, actualiza context/04-backlog.md
```

- **Workflow con agentes**:
  1. Pide al agente que lea la carpeta `context/`.
  2. Asigna una tarea del backlog.
  3. Al terminar, instrúyelo: "Actualiza el estado en 04-backlog.md y resume el trabajo realizado".
  4. Revisa y commitea.

- **Ventajas de Markdown**:
  - Fácil de versionar con Git.
  - Visual en GitHub/VS Code.
  - Los agentes lo procesan bien (tablas, listas, diagramas Mermaid).

