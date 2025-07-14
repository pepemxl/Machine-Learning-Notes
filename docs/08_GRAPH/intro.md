# Graph Algorithm for Data Science

1. Graph modeling and construction
    - Identify relationships between data points
    - Describe a graph structure
    - Import data into a graph database
2. Graph query language
    - Identify graph patterns
    - Transverse connections
    - Aggregate data
    - Perform exploratory data analysis
3. Graph algorithms and inferred networks
    - Find the most important or critical nodes
    - Group node into comunities
    - Identify similar nodes
    - Analyze indirect relationships
4. Graph Machine Learning
    - Extract features from graphs
    - Predict node labels
    - Predict new connections


## What is a Graph?

Usually people missunderstand the term **graph** thinking that every chart is a graph.


Graph analytics is based on Graph Theory.

The typical problem to understand this are is the problem of the briges of koinsigner

The matrhematical definition of a graph $G$ is a pair $(V,E)$ where $V$ is a set of vertices and $E$ is a set of edges.

The computer science defintion of a graph is an abstract data type:

1. Has a data structure to represent the mathematical graph
2. Supports a number of operations
    - add_edge
    - add_vertex
    - get_neighboors

we have some ways to represent a graph maybe the most common is a matrix, called the adjacency matrix or matrix of adjacencies.


Facebook is a classical example where all data existing there can be easier represented as a graph. This is a social network.


Tweets are a Graph

- Many kind of node in the graph
    - Users
    - Tweets
    - Likes
    - Urls
    - Media
        - Image
        - Video
    - Hashtags
- Many kind of edges (actions)
    - Users **creates** Tweets
    - A tweet is **in response** to another
    - A tweet **retweets** another
    - User **mentions** User
    - Tweet **contains** hashtag
    - User **follows** User

Tipical problems studied using graph are:

- Social Networks
- Biological Networks
    - Ilnes connected by genes
- Smart Cities
    - optimizing traffic models
    - planning smart hubs
    - 
- Threat Detection


## Why we do analytics?

- Uncocer characteristics of datasets based on its matehmatical properties.
- Answer specific questions from  multiple data sets.
- Develop a mathematical model for predicting the behavior of some variables.
- Detect emergent phenomena and explain its contributing factors.

## Graphs and the V's of Big Data

The three well known **V's** are:

- **Volume**
- **Velocity**
- **Variety**

the lesser known **V** is:

- **Valence**: Degree of interdependency among data. The idea is we increase the valence (Heterogenity) of a graph we increase the connections of a graph. 





## References

- [Schema Org](https://schema.org/)
- [RDFLib is a pure Python package for working with RDF](https://rdflib.readthedocs.io/en/stable/index.html)
- [A Survey on Knowledge Graph Embedding: Approaches, Applications and Benchmarks](https://www.mdpi.com/2079-9292/9/5/750) by Yuanfei Dai 