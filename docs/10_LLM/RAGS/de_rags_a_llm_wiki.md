# De Rags a LLM-wiki

Pero a medida que avanzamos por 2026, las grietas del enfoque de “RAG para todo” se han vuelto demasiado grandes para ignorarlas. La fragmentación en chunks destruye estructuras complejas de tablas, la recuperación vectorial es inherentemente probabilística (puedes obtener el chunk correcto, o puedes obtener uno desactualizado), y mantener sincronizados los embeddings con datos que se actualizan rápidamente es una pesadilla operativa absoluta.

Para resolver esto, Google Cloud silenció el ruido de “RAG para todo” al abrir el código de Open Knowledge Format (OKF v0.1). No es una nueva base de datos en la nube, ni un framework para LLM, ni un SDK. En cambio, es una especificación portátil y neutral respecto al proveedor que formaliza el paradigma de “LLM Wiki”, es decir, el concepto exacto de un “cerebro” estructurado e interconectado que investigadores de IA como Andrej Karpathy han defendido durante años.

OKF cambia nuestra estrategia: dejamos de hacer búsqueda probabilística sobre archivos no estructurados y pasamos a una navegación determinista a través de un grafo de conocimiento vivo, legible por humanos y agentes.

## ¿Qué es exactamente Open Knowledge Format (OKF)?

OKF estandariza cómo se estructuran el conocimiento organizacional, la lógica de negocio y los esquemas de backend, de modo que cualquier agente de IA pueda recorrerlos y entenderlos de forma nativa, sin capas de traducción personalizadas.

En lugar de una base de datos costosa y de caja negra, una colección OKF —llamada Knowledge Bundle— es simplemente un directorio estándar de archivos Markdown de texto plano envueltos en frontmatter YAML.

## La anatomía de un bundle OKF

En un bundle OKF, las rutas de directorio definen la identidad única de un concepto. En lugar de volcar archivos crudos en un índice, la información se compila en “Concepts” hiperenfocados y singulares (por ejemplo, un contrato de API interno, una métrica financiera o un esquema de base de datos).

```plaintext
company_brain/
├── index.md               # Directorio raíz para divulgación progresiva
├── engineering/
│   ├── index.md
│   └── service_mesh.md    # Concepto de arquitectura
└── analytics/
    ├── index.md
    ├── tables/
    │   ├── customers.md   # Archivo de concepto individual de base de datos
    │   └── billing.md
    └── metrics/
        └── active_users.md # Definición precisa de negocio
```

Cada archivo de concepto sigue un diseño estricto pero mínimo: un bloque de frontmatter YAML al inicio (que requiere exactamente un campo: `type`), seguido de un cuerpo Markdown de forma libre.

Aquí hay un ejemplo de un archivo OKF auténtico que describe una métrica crítica de negocio:

```yaml
---
type: metric
id: analytics/metrics/active_users
title: Weekly Active Users (WAU)
owner: data-eng@company.com
updated_at: 2026-06-15
citations:
  - source: "https://github.com/internal-org/dbt/models/wau.sql"
---
# Weekly Active Users (WAU)
El conteo total de IDs de usuario únicos que han activado al menos una transacción principal de backend dentro de una ventana móvil de 7 días.

## Reglas de cálculo
Excluimos explícitamente cuentas internas de QA y pruebas:
`WHERE user_id NOT IN (SELECT user_id FROM staging.internal_testers)`

## Componentes relacionados
- Ver [[analytics/tables/customers]] para los mapeos principales de dimensiones de usuario.
- Ver [[analytics/tables/billing]] para correlacionar el uso con ciclos de suscripción activos.
```

## Los tres pilares de OKF

OKF funciona donde los wikis empresariales tradicionales y RAG fallan por tres principios arquitectónicos:

**Formato sobre plataforma:** OKF no requiere cuentas en la nube, software pesado ni SDKs a medida. Es totalmente nativo de git. Puedes versionarlo, auditarlo mediante pull requests y rastrear con precisión cómo cambia el conocimiento de tu empresa con el tiempo.

**El LLM como bibliotecario del wiki:** Históricamente, los humanos son malos manteniendo documentación; se degrada casi de inmediato. En el paradigma OKF, agentes de IA en segundo plano actúan como motores de mantenimiento. Cuando un desarrollador actualiza el código o los esquemas de base de datos, un agente modifica automáticamente los archivos Markdown OKF relevantes, corrige los enlaces cruzados y registra la actualización en `log.md` del bundle.

**Determinismo estricto mediante enlaces de grafo:** En lugar de usar matemáticas de similitud coseno para adivinar qué datos se relacionan con una consulta, OKF usa enlaces Markdown explícitos (`[[concept_path]]`). Esto convierte una carpeta estándar de archivos en un grafo de conocimiento absoluto y determinista que un agente de IA puede recorrer lógicamente.

## Escenario real: RAG vs. OKF

Veamos cómo cambia esto los flujos de trabajo cotidianos de un agente analista de datos de IA dentro de una empresa.

### El objetivo

Le preguntas a tu agente de IA: **“Escribe una consulta SQL ejecutiva calculando nuestro Churn Rate para Q2.”**

### La vieja forma RAG

El agente convierte tu consulta en un embedding vectorial.

Busca en una base de datos vectorial que contiene miles de chunks de PDFs, páginas de Confluence y registros históricos de Slack.

La base devuelve tres chunks: una diapositiva de PowerPoint de 2023, un wiki de ingeniería antiguo y una conversación entre dos ingenieros de datos discutiendo cómo calcular churn.

El LLM combina estas definiciones conflictivas, se confunde y escribe una consulta SQL rota que toma datos del esquema equivocado.

### La forma OKF

El agente lee el `index.md` raíz del bundle OKF de la empresa.

Navega directamente a `analytics/metrics/churn_rate.md`.

Extrae el fragmento SQL absoluto y auditado, junto con la lógica estructural.

Sigue el enlace Markdown explícito `[[analytics/tables/customers]]` dentro del archivo para consultar al instante las definiciones actuales del esquema y las claves de unión.

El agente genera una consulta perfectamente exacta en el primer intento, citando el archivo exacto, la fecha de la última actualización y el ingeniero responsable.

## Cara a cara: RAG vs. OKF

- **Estructura principal**
  - **RAG:** chunks vectoriales segmentados y fragmentados.
  - **OKF:** Markdown estructurado + frontmatter YAML.

- **Motor de recuperación**
  - **RAG:** probabilístico (vecino más cercano matemático).
  - **OKF:** determinista (recorrido explícito de enlaces de grafo).

- **Interfaz humana**
  - **RAG:** baja (requiere consultar una base de datos de ingeniería).
  - **OKF:** alta (legible de forma nativa en GitHub u Obsidian).

- **Mantenimiento**
  - **RAG:** costo alto (reindexación, deriva de embeddings).
  - **OKF:** costo bajo (commits de git y pull requests).

- **Caso de uso óptimo**
  - **RAG:** archivos masivos, no estructurados y crudos.
  - **OKF:** definiciones y reglas de negocio canónicas, de alto impacto.

## La pila moderna de IA

RAG no está desapareciendo por completo; más bien, su papel está cambiando. Pedirle a un sistema probabilístico que encuentre tu identificador fiscal legal o la definición de “Revenue” de tu empresa es, fundamentalmente, una mala decisión de diseño. OKF reemplaza a RAG para esas verdades corporativas absolutas y de alto impacto.

De cara al futuro, los equipos están construyendo una arquitectura híbrida en la que un router de IA actúa como controlador de tráfico:

```text
[ Solicitud del usuario ]
                      │
                      ▼
               ┌──────────────┐
               │  Router IA   │
               └──────┬───────┘
                      │
       ┌──────────────┴──────────────┐
       ▼                             ▼
[ Bundle OKF ]               [ Pipeline RAG ]
(Reglas base, esquemas,      (PDFs archivados, tickets
 runbooks, precisión)         de clientes, exploración a escala)
```

Al usar OKF para la precisión determinista y RAG para buscar datos históricos amplios, las organizaciones están construyendo sistemas de IA que son a la vez muy capaces y notablemente estables. OKF no eliminó la recuperación; simplemente les dio a los agentes de IA un mapa estandarizado para encontrar lo que necesitan.

Para un desglose técnico completo paso a paso de Open Knowledge Format, revisa este [desglose técnico detallado de la especificación OKF y la construcción de bundles](https://www.youtube.com/watch?v=T33iI6izAKw). Este recurso en video explica el diseño estructural del estándar, revisa la especificación en GitHub y muestra cómo puedes empezar a organizar conocimiento para agentes de IA usando archivos Markdown planos.