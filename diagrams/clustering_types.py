# -*- coding: utf-8 -*-

from urllib.request import urlretrieve
import os

from diagrams import Cluster, Diagram, Edge, Node
from diagrams.custom import Custom


from diagrams.programming.language import Python
from diagrams.programming.flowchart import Action
from diagrams.programming.flowchart import Collate
from diagrams.programming.flowchart import Database
from diagrams.programming.flowchart import Decision
from diagrams.programming.flowchart import Delay
from diagrams.programming.flowchart import Display
from diagrams.programming.flowchart import Document
from diagrams.programming.flowchart import InputOutput
from diagrams.programming.flowchart import Inspection
from diagrams.programming.flowchart import InternalStorage
from diagrams.programming.flowchart import LoopLimit
from diagrams.programming.flowchart import ManualInput
from diagrams.programming.flowchart import ManualLoop
from diagrams.programming.flowchart import Merge
from diagrams.programming.flowchart import MultipleDocuments
from diagrams.programming.flowchart import OffPageConnectorLeft
from diagrams.programming.flowchart import OffPageConnectorRight
from diagrams.programming.flowchart import Or
from diagrams.programming.flowchart import PredefinedProcess
from diagrams.programming.flowchart import Preparation
from diagrams.programming.flowchart import Sort
from diagrams.programming.flowchart import StartEnd
from diagrams.programming.flowchart import StoredData
from diagrams.programming.flowchart import SummingJunction

cluster_attr = {
    "label":"", 
    "bgcolor":"transparent",
    "penwidth":"0",
}

graph_attr = {
    # "label":"", 
    labelloc:"t",
    # "bgcolor":"transparent",
    # "penwidth":"0",
    # comment:"By Jose Alonzo",
    # body:"By Jose Alonzo",
}


with Diagram(name="Taxonomy of Clustering Methods", 
             filename="taxonomy_clustering",
             # directory=os.path.abspath("../images"),
             show=False, 
             outformat='png', 
             direction='TB',
             graph_attr=graph_attr,
             ):#, graph_attr=cluster_attr):
    root = StartEnd("Clustering", labelloc="c", width="2", height="2",)
    Hierarchical = Action("Hierarchical", labelloc="c")
    Partitional = Action("Partitional", labelloc="c")
    root >>  Hierarchical
    root >>  Partitional
    # root - Edge(tailport="s", headport="n",) >>  Hierarchical
    # root - Edge(tailport="s", headport="n",) >> Partitional
    Single_Link = Action("Single Link", labelloc="c")
    Complete_Link = Action("Complete Link", labelloc="c")
    Hierarchical >> Single_Link
    Hierarchical >> Complete_Link
    Square_error = Action("Square error", labelloc="c")
    Partitional >> Square_error
    K_means = Action("K-means", labelloc="c")
    Square_error >> K_means
    Graph_Theory = Action("Graph Theory", labelloc="c")
    Partitional >> Graph_Theory
    Mixture_Resolving = Action("Mixture Resolving", labelloc="c", width="3")
    Partitional >> Mixture_Resolving
    Expectation_Maximization = Action("Expectation\n Maximization", labelloc="c", width="6", height="2")
    Mixture_Resolving >> Expectation_Maximization
    # e1 = Action("Action")
    # e2 = Collate("Collate")
    # e3 = Database("Database")
    # e4 = Decision("Decision")
    # e5 = Delay("Delay")
    # e6 = Display("Display")
    # e7 = Document("Document")
    # e8 = InputOutput("InputOutput")
    # e9 = Inspection("Inspection")
    # e10 = InternalStorage("InternalStorage")
    # e11 = LoopLimit("LoopLimit")
    # e12 = ManualInput("ManualInput")
    # e13 = ManualLoop("ManualLoop")
    # e14 = Merge("Merge")
    # e15 = MultipleDocuments("MultipleDocuments")
    # e16 = OffPageConnectorLeft("OffPageConnectorLeft")
    # e17 = OffPageConnectorRight("OffPageConnectorRight")
    # e18 = Or("Or")
    # e19 = PredefinedProcess("PredefinedProcess")
    # e20 = Preparation("Preparation")
    # e21 = Sort("Sort")
    # e22 = StartEnd("StartEnd")
    # e23 = StoredData("StoredData")
    # e24 = SummingJunction("SummingJunction")
