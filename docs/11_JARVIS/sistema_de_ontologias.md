# Sistema de Ontologías

Una **ontología** es una especificación formal y explícita de una conceptualización
compartida: define qué tipos de entidades existen en un dominio, qué propiedades tienen y cómo
se relacionan entre sí.

En el contexto de [JARVIS](introduccion.md), el sistema de ontologías es la capa que da
vocabulario común a los agentes: sin ella, cada componente inventa sus propios nombres para las
mismas cosas y la integración se vuelve manual.

## Componentes

| Componente | Función |
|---|---|
| **Clases** (*tipos*) | Las categorías de entidades del dominio |
| **Propiedades** | Atributos de las entidades y relaciones entre ellas |
| **Individuos** (*instancias*) | Las entidades concretas |
| **Axiomas** | Restricciones que deben cumplirse (cardinalidad, disyunción, dominio y rango) |
| **Razonador** | Deriva hechos nuevos a partir de los axiomas y los hechos existentes |

## Lenguajes y estándares

- **RDF** — el modelo de datos base: tripletas sujeto-predicado-objeto.
- **RDFS** — vocabulario para jerarquías de clases y propiedades.
- **OWL** — lógica descriptiva completa; permite razonamiento automático.
- **SHACL** — validación de estructura, complementaria al razonamiento.
- **SPARQL** — lenguaje de consulta sobre RDF.

Ver [Cypher](../10_LLM/RAGS/cypher.md) para el enfoque equivalente en bases de datos de
*property graph*.

## Ontología vs. esquema de base de datos

La diferencia no es solo de formato:

- Un **esquema** describe cómo se almacenan los datos, y opera bajo el *supuesto de mundo
  cerrado*: lo que no está, es falso.
- Una **ontología** describe qué significan, y opera bajo el *supuesto de mundo abierto*: lo
  que no está, simplemente se desconoce.

Esa diferencia es la que permite el razonamiento: de "todo empleado tiene un departamento" y
"Ana es empleada" se deriva que Ana tiene un departamento, aunque no esté registrado.

## Aplicación en el proyecto

- Dar a los agentes un modelo compartido de vulnerabilidades, activos y métricas.
- Permitir consultas que atraviesen fuentes distintas sin escribir integraciones a medida.
- Habilitar razonamiento sobre impacto: qué servicios se ven afectados por una vulnerabilidad
  dada.

## Ver también

- [Desarrollo orientado a ontologías](desarrollo_orientado_a_ontologias.md)
- [Definiciones de Knowledge Graph](../08_GRAPH/definiciones_knowledge_graph.md)
