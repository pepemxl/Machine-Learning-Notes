# Knowledge Graph Creation


Knowledge create refers to semantically annotating content, data and services from 
heterogeneous sources with an ontology. This step can be split into two major tasks:

- **Bottom-Up**: A lightweight ontology engineering task called domain specification that creates domain-specific patterns.
- **Top-Down**: A large scale instance generation task as an application of the domain-specific patterns.


## Bottom-Up Domain Specification Modeling

We take [Schema.org](https://schema.org/) as a reference ontology for knowledge graphs as it is a de-facto industrial standard for annotations on the web. These annotations are natural building blocks for knowledge graphs and usage of such a widespread ontology would increase the impact of a knowledge graph. Before the knowledge generation process starts, the domain(s) the knowledge graph is supposed to describe must be analyzed to figure out the domain entities and their relationships and then mapped to Schema.org. This process is quite challenging due to the nature of the vocabulary. Schema.org covers many domains with hundreds of types and properties, however, its coverage for specific domains is very shallow. This situation calls for an adaptation of Schema.org for specific domains and tasks. We call this adaptation process domain specification



