# Desarrollo Orientado a Ontologías

Al optimizar componentes **de forma aislada**, resulta cada vez más difícil **sincronizar los
cambios entre múltiples componentes desintegrados**. Como consecuencia, las mejoras a nivel de
componente no han logrado traducirse en mejoras a nivel de sistema.

Las mejoras introducidas en los componentes de la arquitectura empresarial estándar no han
producido mejoras en el conjunto. El rendimiento real del sistema se aleja cada vez más de su
rendimiento potencial.

A pesar de que se les vendió modularidad, los clientes de este complejo software-industrial han
recibido un producto **fragmentado y desintegrado**. En lugar de habilitar agilidad, estas
inversiones han dado lugar a arquitecturas empresariales rígidas. Y esa rigidez técnica se
filtra hacia la cultura organizacional en general, generando estancamiento.

## La alternativa: la ontología como capa común

La propuesta del desarrollo orientado a ontologías es invertir el orden: en lugar de integrar
componentes *a posteriori*, se define primero un **modelo semántico compartido** —la
ontología— que describe las entidades del negocio, sus propiedades y sus relaciones. Los
componentes se construyen contra ese modelo, no unos contra otros.

La ventaja es que un cambio en el modelo se propaga de forma explícita, en vez de requerir
sincronización manual entre sistemas que no comparten vocabulario.

Ver [Definiciones de Knowledge Graph](../08_GRAPH/definiciones_knowledge_graph.md) y
[Creación de Knowledge Graphs](../08_GRAPH/creacion_de_knowledge_graphs.md) para la
formalización de este tipo de modelos.

## Referencias

- [Connecting AI to decisions with the Palantir Ontology](https://blog.palantir.com/connecting-ai-to-decisions-with-the-palantir-ontology-c73f7b0a1a72)
- [Ontology-Oriented Software Development](https://blog.palantir.com/ontology-oriented-software-development-68d7353fdb12)
