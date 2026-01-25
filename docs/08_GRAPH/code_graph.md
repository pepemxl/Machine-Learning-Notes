# Code Graph

Enabling Large Language Models (LLMs) to reason over selected code snippets within their context size is relatively straightforward. By copying and pasting the code snippet with some prompt engineering, LLMs often handle the request quite well. For example, GitHub Coplit Chat already allows you to generate 
- unit test, 
- fixing bugs, or 
- explain a manually selected code snippet. 

However, how can we extend it to the scope of the whole codebase? Can we also skip the manual selection of code snippet and allow the LLM to figure it out? Building a knowledge graph over the codebase has the potential to tackle these challenges.

## CodeGraph Context for Coding Copilots

The flow will be something like:

```mermaid
flowchart LR
    A[("Raw Data<br/><small>JSON/CSV/Logs</small>")]:::raw_node --> B["Tasks<br/><small>Cleaning & Processing</small>"]:::tasks_node
    B --> C[("DataPoints<br/><small>Structured Entities</small>")]:::datapoints_node
    C --> D[("Graph Network<br/><small>Relationships</small>")]:::graph_node
    C --> E("fa:fa-tasks Vector Storage<br/><small>Embeddings</small>"):::vector_node
    D & E --> F["Intelligent Search<br/><small>Semantic + Graph</small>"]:::search_node

    classDef raw_node fill:#6A5ACD,stroke:#9370DB,color:white;
    classDef tasks_node fill:#20B2AA,stroke:#00FA9A,color:black;
    classDef datapoints_node fill:#FF6347,stroke:#FF7F50,color:white;
    classDef graph_node fill:#4169E1,stroke:#1E90FF,color:white;
    classDef vector_node fill:#32CD32,stroke:#00FF7F,color:black;
    classDef search_node fill:#FF4500,stroke:#FF6347,color:white;

    style A icon:fa-database;
    style B icon:fa-tasks;
    style C icon:fa-map-pin;
    style D icon:fa-map;
    style E icon:fa-cube;
    style F icon:fa-search;
```

## Custom Ontologies and Reasoners for Domain "awareness"

Let mix some domain driven development with LLMs and code guidelines.

### Code "awarness"

Different static and dynamic analysis of the source code already build graph over source code for machine code optimization or vulnerability detection. 

### Simple Knowledge Graph

Here, we will showcase how a simple knowledge graph over a codebase can be built that allows a LLM to reason over the whole codebase. 

In the example graph, we use blue node to represent a file/directory, and green node to represent an AST node. Between file nodes we have HAS_FILE edges between the parent directory and the child file. Between file nodes and AST nodes we have HAS_AST edges between the source code files and the root AST node. Between the AST nodes we have HAS_PARENT edges between the parent and child AST nodes. 


Lets start to test [Cognee](https://github.com/topoteretes/cognee) which has develppe a Data to Memory process.

In thisc ase **data to memory** is the process of converting and ingesting your raw data into Cognee’s memory system.

Node Sets provide a simple yet powerful tagging mechanism that helps in managing the growing complexity of your knowledge base as you add more content.

- **Chunking** is how cognee breaks down large datasets into manageable pieces for efficient processing and analysis.
- **Memory Processing** encompasses the computational workflows that transform raw data into structured, queryable knowledge.
- **Tasks** are the building blocks of cognee’s data processing pipeline.
- **Pipelines** are the data processing workflows that transform raw information into structured knowledge graphs.
- **DataPoints** are the fundamental units of information that carry 
metadata and relationships.
- **Search Memory** enables you to query and retrieve information from your knowledge graphs.

