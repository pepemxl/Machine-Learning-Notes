# Machine Learning Notes

Notas de trabajo sobre análisis de datos, machine learning, sistemas de ML y LLMs,
publicadas como sitio estático con [MkDocs](https://www.mkdocs.org/) y el tema
[Material](https://squidfunk.github.io/mkdocs-material/).

El contenido vive en [`docs/`](docs/). El índice completo del curso está en
[`docs/index.md`](docs/index.md).

## Contenido

| Sección | Tema |
|---|---|
| `docs/00_DATA` | Análisis de datos, bases de datos, Spark / PySpark |
| `docs/01_SUPERVISED_LEARNING` | Árboles de decisión, regresión lineal, SVM |
| `docs/02_UNSUPERVISED_LEARNING` | Clustering, detección de anomalías, Isolation Forest |
| `docs/03_REINFORCEMENT_LEARNING` | MDPs, Q-Learning, deep reinforcement learning |
| `docs/04_WORKFLOWS` | ML Systems, feature stores, workflows y colas |
| `docs/05_MATH` | Fundamentos matemáticos |
| `docs/06_TORCH` | Ejemplos en PyTorch (código, sin notas todavía) |
| `docs/07_NLP` | Procesamiento de lenguaje natural |
| `docs/08_GRAPH` | Grafos y knowledge graphs |
| `docs/09_SYSTEMS` | Sistemas de recomendación, PYMK |
| `docs/10_LLM` | LLMs, MCP, RAGs, LM Studio, modelos locales |
| `docs/11_JARVIS` | Proyecto JARVIS, ontologías, LangGraph |
| `docs/12_TIME_SERIES` | Series de tiempo |
| `docs/13_PROBLEMS` | Problemas prácticos (Titanic) |
| `docs/PROYECTOS` | Proyectos completos |

## Levantar la documentación

Con Python local:

```bash
pip install -r src/containers/docs/requirements.txt
make serve_doc          # http://127.0.0.1:8000
```

Con Docker (live-reload, puerto 8080):

```bash
make up_docs            # build + run
```

## Build

```bash
make build_doc          # mkdocs build --strict
```

El build corre en **modo estricto**: cualquier enlace roto o referencia inválida en el
`nav` hace fallar la construcción. Ejecútalo antes de commitear cambios en `docs/`.

## Convenciones

- **El contenido se escribe en español.** El repositorio está consolidado en un solo idioma.
- Cada página empieza con un único encabezado `#` de nivel 1.
- Todo bloque de código lleva lenguaje (```` ```python ````, ```` ```bash ````, …).
- Las páginas nuevas se añaden al `nav` de [`mkdocs.yml`](mkdocs.yml). Los borradores
  se declaran en `not_in_nav` en lugar de quedarse sueltos.
- **Nombres de archivo descriptivos** en español, sin acentos (`regresion_lineal.md`). Si
  renombras una página, añade la ruta antigua a `redirect_maps` en `mkdocs.yml`.
- Fórmulas con `$...$` (inline) y `$$...$$` (bloque), renderizadas con MathJax 3.
- Diagramas con bloques ```` ```mermaid ````.

## Estructura del repositorio

- `docs/` — contenido del curso (Markdown, notebooks, imágenes, diagramas).
- `mkdocs.yml` — configuración del sitio y navegación.
- `pp_tools/` — librería Python de apoyo (grafos, base de datos, utilidades ML).
- `src/containers/docs/` — imagen Docker para servir la documentación.
- `Makefile` — tareas de instalación, build y publicación.
