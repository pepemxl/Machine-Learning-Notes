# Repository Guidelines

Repositorio de **notas de curso** sobre machine learning, publicadas como sitio MkDocs,
más una librería Python de apoyo (`pp_tools`). El contenido es el producto principal;
el código es instrumental.

## Estructura del proyecto

- `docs/` — **el curso**. Markdown organizado por tema con prefijo numérico:
  - `00_DATA` (análisis de datos, bases de datos, Spark), `01_SUPERVISED_LEARNING`,
    `02_UNSUPERVISED_LEARNING`, `03_REINFORCEMENT_LEARNING`, `04_WORKFLOWS`, `05_MATH`,
    `06_TORCH`, `07_NLP`, `08_GRAPH`, `09_SYSTEMS`, `10_LLM`, `11_JARVIS`,
    `12_TIME_SERIES`, `13_PROBLEMS`, `PROYECTOS`.
  - `docs/images/` — imágenes; `docs/diagrams/` — scripts que las generan
    (ver `docs/diagrams/README.md`); `docs/javascripts/` — bootstrap de MathJax.
  - Notebooks `.ipynb` conviven con el Markdown y se renderizan vía `mkdocs-jupyter`.
- `mkdocs.yml` — configuración del sitio, `nav` y `not_in_nav`.
- `pp_tools/` — librería Python: `common/` (logging, config, utils), `db/`, `io/`,
  `ml/` (graph, db, metrics, models, time_series, plot, fsm, pipeline), `agents/`,
  `code_tools/`, `mcp/`, `models/`, `tests/`.
- `src/containers/docs/` — Dockerfile y `requirements.txt` para servir la documentación.
- `Makefile` — instalación, build y publicación.
- `.github/workflows/docs.yml` — CI: `mkdocs build --strict`.

> No existen `pp_tools-mcp/`, `pp_tools-frontend/`, `alembic/`, `distributed/`,
> `examples/` ni `notebooks/` en la raíz. Este proyecto **no** usa `uv` ni `ruff`.

## Build, test y desarrollo

Python 3.10, `venv` + `poetry` vía Makefile.

```bash
make install          # crea ./venv, instala requirements y poetry install
source venv/bin/activate
```

Documentación:

```bash
make serve_doc        # mkdocs serve  -> http://127.0.0.1:8000
make build_doc        # mkdocs build --strict  (lo mismo que corre el CI)
make up_docs          # build + run en Docker, puerto 8080
```

Tests:

```bash
pytest pp_tools/tests/ -v
```

## Convenciones de la documentación

Es la parte que más importa cuidar.

- **Un solo `#` de nivel 1 por página**, como primera línea.
- **Todo bloque de código lleva lenguaje**: ```` ```python ````, ```` ```bash ````,
  ```` ```sql ````; usa ```` ```text ```` para árboles de ficheros, ASCII art y salidas.
- **Toda página nueva entra en el `nav`** de `mkdocs.yml`. Si es un borrador, se declara
  en `not_in_nav` — nunca se deja suelta, porque entonces es inalcanzable desde el sitio.
- **Matemáticas**: `$...$` inline y `$$...$$` en bloque (arithmatex + MathJax 3).
  No añadas `mdx_math`: entra en conflicto con arithmatex.
- **Diagramas**: bloques ```` ```mermaid ````, renderizados por `mermaid2`.
- **Enlaces internos** relativos y a archivos `.md` reales (el build estricto los valida).
  Los enlaces a documentación externa van con URL absoluta completa.
- **Imágenes** en `docs/images/`, referenciadas con ruta relativa.
- **Nombres de archivo descriptivos** en español y sin acentos (`regresion_lineal.md`,
  `deteccion_de_anomalias.md`). Ya no quedan nombres `section_NN.md`.
- Al **renombrar o mover** una página, añade la ruta antigua a `redirect_maps` en
  `mkdocs.yml` (plugin `redirects`) para no romper las URLs publicadas.

## Idioma

**Todo el contenido está en español.** El repositorio se consolidó en un único idioma: ya no
existen sufijos `.es.md` ni páginas duplicadas en inglés.

Se mantienen en inglés, deliberadamente, los términos técnicos de uso establecido (*feature*,
*embedding*, *shuffle*, *prompt*) y los prompts afinados sobre ese idioma, como
`11_JARVIS/prompts/puzzle_solver.md`: traducirlos cambiaría el comportamiento del modelo.

## Antes de commitear

```bash
mkdocs build --strict     # debe terminar con exit 0 y cero warnings
```

Falla ante enlaces rotos, entradas del `nav` que apuntan a archivos inexistentes, y
páginas fuera del `nav` no declaradas en `not_in_nav`. El CI ejecuta exactamente esto.

## Commits y PRs

- Asunto imperativo y breve (≤ 72 caracteres).
- Un tema por commit; separa cambios de contenido de cambios de configuración.
- Si tocas `mkdocs.yml`, di en el cuerpo qué páginas entran o salen del `nav`.

## Contexto

Hay un diagnóstico y plan de mejoras en `LOCAL_DATA/plan_mejoras_2026_08_29.md`
(no versionado). Consúltalo antes de reorganizar `docs/`.
