from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# Create a SQLite in-memory database
engine = create_engine('sqlite:///:memory:', echo=True)
Base = declarative_base()


class Graph(Base):
    __tablename__ = 'graphs'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    nodes = relationship("Node", back_populates="graph")
    edges = relationship("Edge", back_populates="graph")


class Node(Base):
    __tablename__ = 'nodes'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    graph_id = Column(Integer, ForeignKey('graphs.id'))
    graph = relationship("Graph", back_populates="nodes")


class Edge(Base):
    __tablename__ = 'edges'
    id = Column(Integer, primary_key=True)
    source_id = Column(Integer, ForeignKey('nodes.id'))
    target_id = Column(Integer, ForeignKey('nodes.id'))
    graph_id = Column(Integer, ForeignKey('graphs.id'))
    graph = relationship("Graph", back_populates="edges")

    source = relationship("Node", foreign_keys=[source_id])
    target = relationship("Node", foreign_keys=[target_id])

# Create tables
Base.metadata.create_all(engine)

# Create a session
Session = sessionmaker(bind=engine)
session = Session()

# Create graphs
graph1 = Graph(name='Graph 1')
graph2 = Graph(name='Graph 2')
session.add_all([graph1, graph2])
session.commit()

# Add nodes to graph 1
node1_g1 = Node(name='Node 1 for Graph 1', graph=graph1)
node2_g1 = Node(name='Node 2 for Graph 1', graph=graph1)
session.add_all([node1_g1, node2_g1])
session.commit()

# Add nodes to graph 2
node1_g2 = Node(name='Node 1 for Graph 2', graph=graph2)
node2_g2 = Node(name='Node 2 for Graph 2', graph=graph2)
session.add_all([node1_g2, node2_g2])
session.commit()

# Add edges to graph 1
edge1_g1 = Edge(source=node1_g1, target=node2_g1, graph=graph1)
session.add(edge1_g1)
session.commit()

# Add edges to graph 2
edge1_g2 = Edge(source=node1_g2, target=node2_g2, graph=graph2)
session.add(edge1_g2)
session.commit()

# Query the graphs
graphs = session.query(Graph).all()
for graph in graphs:
    print(f"Graph: {graph.name}")
    print("Nodes:")
    for node in graph.nodes:
        print(f"- {node.name}")
    print("Edges:")
    for edge in graph.edges:
        print(f"- {edge.source.name} --> {edge.target.name}")

# Close session
session.close()
