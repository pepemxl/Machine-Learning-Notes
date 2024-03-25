# -*- coding: utf-8 -*-

from urllib.request import urlretrieve
import os

from diagrams import Cluster, Diagram, Edge
from diagrams.custom import Custom

from diagrams.onprem.analytics import Spark
from diagrams.onprem.analytics import Hive
from diagrams.onprem.analytics import Presto
from diagrams.onprem.analytics import Hadoop
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Cassandra
from diagrams.onprem.database import Mariadb
from diagrams.onprem.database import Mongodb
from diagrams.onprem.database import Mysql
from diagrams.onprem.database import PostgreSQL



from diagrams.programming.language import Python
from diagrams.aws.database import RDS
from diagrams.gcp.analytics import BigQuery, Dataflow, PubSub
from diagrams.gcp.iot import IotCore
from diagrams.azure.storage import Azurefxtedgefiler



with Diagram("ML Development On Node", show=False):
    # with Cluster("Service Cluster"):
    #     grpcsvc = [
    #         Server("grpc1"),
    #         Server("grpc2"),
    #         Server("grpc3")
    #         ]
    # with Cluster("Databases"):
    #     db_cassandra = Cassandra("Cassandra")
    #     db_mariadb = Mariadb("Mariadb")
    #     db_mongo = Mongodb("Mongo")
    #     db_mysql = Mysql("MySQL")
    #     db_postgre = PostgreSQL("PostGre")
    #     databases = [
    #         db_cassandra,
    #         db_mariadb,
    #         db_mongo,
    #         db_mysql,
    #         db_postgre]
    with Cluster("System"):
        with Cluster("Source of Data"):
            source_data = [
                IotCore("core1"),
                IotCore("core2"),
                IotCore("core3")
                ]
            
        with Cluster("Data Lake"):
            db_presto = Presto("Presto")
            db_hive = Hive("Hive")
            db_hadoop = Hadoop("Hadoop")
            data_input = [
                db_presto,
                db_hive,
                db_hadoop
                ]


    with Cluster("Node"):
        cpu_server = Server("Node")
        with Cluster("Storage /home/<user>/FSS"):
            with Cluster("INPUT"):
                node_storage = Azurefxtedgefiler("Datasets")
                node_storage_features = Azurefxtedgefiler("Features")
                node_storage_conf = Azurefxtedgefiler("Configurations")
                ml_inputs = [
                    node_storage, 
                    node_storage_features
                    ]
            with Cluster("OUTPUT"):
                node_storage_out_stats = Azurefxtedgefiler("Data Stats")
                node_storage_out_reports = Azurefxtedgefiler("Reports")
                node_storage_out_reports_summary = Azurefxtedgefiler("Summary Results")
                node_storage_out_logs = Azurefxtedgefiler("Logs")
                ml_oututs = [
                    node_storage_out_reports,
                    node_storage_out_reports_summary
                    ]
        with Cluster("Compute"):
            with Cluster("EDA"):
                compute_eda = Python("Exploratory Data Analysis")
                compute_report = Python("Report Generation")
            with Cluster("Features Generation"):
                compute_features_generation = Python("Features Generation")
            with Cluster("Clustering"):
                compute_clustering = Python("Clustering")
            with Cluster("General Analysis"):
                compute_general_analysis = Python("Features Analysis")
                compute_model_analysis = Python("Model Analysis")
            with Cluster("Labeling"):
                compute_labeling = Python("labeling")
            with Cluster("ML"):
                ml_supervised = Python("ML Supervised")
                ml_unsupervised = Python("ML Unsupervised")
            
    source_data - Edge(color="gray", style="dashed") >> db_hive
    # db_hive >> 
    db_presto - Edge(color="darkgreen") >> cpu_server
    cpu_server - Edge(color="darkgreen") >> node_storage 
    cpu_server - Edge(color="darkgreen") >> node_storage_features
    node_storage - Edge(color="darkgreen") >> compute_eda
    node_storage_features - Edge(color="darkgreen") >> compute_eda
    node_storage - Edge(color="brown") >> compute_features_generation
    node_storage_features - Edge(color="darkgreen", style="bold") >> ml_supervised
    compute_labeling - Edge(color="darkgreen", style="bold") >> ml_supervised
    # >> data_analysis
    # data_input >> Edge(color="darkgreen") << cpu_server 
    # 
    from diagrams.elastic.observability import Logs
    Logs("logs")
    from diagrams.generic.storage import Storage
    Storage("s1")

