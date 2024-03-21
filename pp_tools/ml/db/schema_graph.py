from enum import Enum
import networkx as nx
import os
from typing import Optional
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer, 
    String,
    Table,
    UniqueConstraint
)
from sqlalchemy import create_engine
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy.orm import sessionmaker
if __name__  == '__main__':
    import sys
    package_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..'))
    sys.path.append(package_path)
from pp_tools.common.logger import get_logger
from pp_tools.common.environment_variables import get_env_var
from pp_tools.db.schema_base import Base
from pp_tools.db.utils import get_url_object


log = get_logger(__file__, "INFO")


class NodeType(Enum):
    TEAM = 'team', ""
    MANAGER = 'manager', ""
    DEVELOPER = 'developer', ""
    LIBRARY = 'library', ""
    MODULE = 'module', ""
    FILE = 'file', ""
    FUNCTION = 'function', ""
    NONE = 'none', ""

    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, value: str, description: str = None):
        self._description = description
    
    def __str__(self):
        return self.value

    @property
    def description(self):
        return self._description


class RelationshipType(Enum):
    TEAM = 'team', ""
    MANAGER = 'manager', ""
    DEVELOPER = 'developer', ""
    LIBRARY = 'library', ""
    MODULE = 'module', ""
    FILE = 'file', ""
    FUNCTION = 'function', ""
    NONE = 'none', ""
    
    def __new__(cls, *args, **kwds):
        obj = object.__new__(cls)
        obj._value_ = args[0]
        return obj

    def __init__(self, value: str, description: str = None):
        self._description = description
    
    def __str__(self):
        return self.value

    @property
    def description(self):
        return self._description



class TblNodes(Base):
    """
        Table to storage all nodes on our knowledge graph
    """
    __tablename__ = 'tbl_nodes'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='Primary Key'
    )
    name = Column(String(128))
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        comment='Date created'
    )


class TblEdges(Base):
    """
        Table to storage relationships between nodes of our knowledge graph
    """
    __tablename__ = 'tbl_edges'

    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='Primary Key'
    )
    source_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('tbl_nodes.id'),
        nullable=False,
        comment='Source Node Id'
    )
    target_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('tbl_nodes.id'),
        nullable=False,
        comment='Target Node Id'
    )
    graph_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey('tbl_graphs.id')
    )
    graph = relationship("TblGraphs", back_populates="tbl_edges")
    source = relationship("TblNodes", foreign_keys=[source_id])
    target = relationship("TblNodes", foreign_keys=[target_id])


class TblGraphs(Base):
    __tablename__ = 'tbl_graphs'
    
    id: Mapped[int] = mapped_column(
        primary_key=True,
        autoincrement=True,
        nullable=False,
        comment='Primary Key'
    )
    # name = Mapped[str] = mapped_column(
    #     String(45),
    #     nullable=False,
    #     comment='graph name'
    # )
    name = Column(String(45))
    # nodes = relationship("TblNodes", back_populates="tbl_graphs")
    nodes = mapped_column('nodes', graph_node_association, back_populates="tbl_graphs")
    # edges = relationship("TblEdges", back_populates="tbl_graphs")
    edges = relationship("TblEdges")
    created_at: Mapped[DateTime] = mapped_column(
        DateTime,
        nullable=False,
        comment='Date created'
    )



def test():
    url_connect = get_url_object(drivername="mysql", DBAPI="pymysql")
    engine = create_engine(url_connect)
    # Create tables
    Base.metadata.create_all(engine)

    # Create a session
    Session = sessionmaker(bind=engine)
    session = Session()

    # Create graphs
    # graph1 = TblGraphs(name='Graph 1')
    # graph2 = TblGraphs(name='Graph 2')
    # session.add_all([graph1, graph2])
    # session.commit()

    # # Add nodes to graph 1
    # node1_g1 = TblNodes(name='Node 1 for Graph 1', graph=graph1)
    # node2_g1 = TblNodes(name='Node 2 for Graph 1', graph=graph1)
    # session.add_all([node1_g1, node2_g1])
    # session.commit()

    # # Add nodes to graph 2
    # node1_g2 = TblNodes(name='Node 1 for Graph 2', graph=graph2)
    # node2_g2 = TblNodes(name='Node 2 for Graph 2', graph=graph2)
    # session.add_all([node1_g2, node2_g2])
    # session.commit()

    # # Add edges to graph 1
    # edge1_g1 = TblEdges(source=node1_g1, target=node2_g1, graph=graph1)
    # session.add(edge1_g1)
    # session.commit()

    # # Add edges to graph 2
    # edge1_g2 = TblEdges(source=node1_g2, target=node2_g2, graph=graph2)
    # session.add(edge1_g2)
    # session.commit()

    # # Query the graphs
    # graphs = session.query(TblGraphs).all()
    # for graph in graphs:
    #     print(f"Graph: {graph.name}")
    #     print("Nodes:")
    #     for node in graph.nodes:
    #         print(f"- {node.name}")
    #     print("Edges:")
    #     for edge in graph.edges:
    #         print(f"- {edge.source.name} --> {edge.target.name}")

    # Close session
    session.close()


if __name__ == '__main__':
    test()