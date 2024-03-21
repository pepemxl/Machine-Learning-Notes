# Why knowledge graph?

Facts can be represented in form of triplets in either of the ways,
- HRT: <head, relation, tail>
- SPO: <subject, predicate, object>


## HRT

— Head or tail: these are entities that are real-world objects or abstract concepts which are represented as nodes
— Relation: these are the connection between entities which represented as edges

## Compared to Normal Graphs

- Heterogenous data: supports different types of entities (person, date, painting, etc) and relations (likes, born on, etc).
- Model real-world information: closer to our brain’s mental model of the world (represents information as a normal human does)
- Perform logical reasoning: traverse the graphs in a path to make logical connections (A’s father is B and B’s father is C, hence C is the grandfather of A)

## Creating custom Knowledge Graph

In spite of having several open-source KGs, we may have a requirement to create domain-specific KG for our use case. There, our base data (from which we want to create the KG), could be of multiple types — tabular, graphical, or text blob. 

- Facts creation: this is the first step where we parse the text/object and extract facts in triplet format like <H, R, T>. If we are processing text, we can leverage pre-processing steps like tokenization, stemming, or lemmatization, etc to clean the text. Next, we want to extract the entities and relations (facts) from the text. For entities, we can use Named entity recognition (NER) algorithms. For relation, we can use sentence dependency parsing techniques to find the relationship between any pair of entities. 
- Facts selection: Once we have extracted several facts, the next obvious steps could be:
    - to remove duplicates and 
    - identify relevant facts that could be added to a KG. 

To identify duplicates, we can use entity and relation disambiguation techniques. The idea is to consolidate the same facts or elements of a fact, in case of repetitions. 


## Build a knowledge graph


```python
# extract subject
source = [i[0] for i in entity_pairs]
# extract object
target = [i[1] for i in entity_pairs]
kg_df = pd.DataFrame({'source':source, 'target':target, 'edge':relations})
# create a directed-graph from a dataframe
G=nx.from_pandas_edgelist(
    kg_df, 
    "source", 
    "target", 
    edge_attr=True, 
    create_using=nx.MultiDiGraph()
)
# plot the nextwork
plt.figure(figsize=(12,12))
pos = nx.spring_layout(G)
nx.draw(G, with_labels=True, node_color='skyblue', edge_cmap=plt.cm.Blues, pos = pos)
plt.show()
# filter by type of relationship
G=nx.from_pandas_edgelist(
    kg_df[kg_df['edge']=="composed by"], 
    "source", 
    "target", 
    edge_attr=True, 
    create_using=nx.MultiDiGraph()
)
plt.figure(figsize=(12,12))
pos = nx.spring_layout(G, k = 0.5) # k regulates the distance between nodes
nx.draw(G, with_labels=True, node_color='skyblue', node_size=1500, edge_cmap=plt.cm.Blues, pos = pos)
plt.show()
```