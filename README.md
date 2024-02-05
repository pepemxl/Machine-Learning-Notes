# Machine-Learning-Notes

Notes of some topic of Machine Learning Techniques.

1. Supervised Learning
    1. [Definition](./01_SUPERVISED_LEARNING/section_01.md)
    2. [Decision Trees](./01_SUPERVISED_LEARNING/section_01.md)
        1. Random Forest
    3. SVM
    4. Neural Networks
        1. CNN
        2. GNN
    5. Semi-Unsupervised Learning
2. Unsupervised Learning
    1. Clustering
3. Reinforcement Learning
4. Machine Learning Systems
    1. Dataflow Systems
    2. Compute Features
    3. Fetch Labels
    4. Train
    5. Evaluate Estimators
    6. Offline/Online predictions
    7. Hyperparameter Sweeping
    8. Feature Importance
    9. Metrics


## General Machine Learning Projects

Machine Learning projects needs in general the next steps:

1. Data Collection
2. Data Pre-processing
3. Building Datasets
4. Model Training Online/Offline
5. Model Deployment
6. Prediction
7. Monitoring Models
8. Maintenance, Diagnosis, and Retraining

In order to achieve all these steps we need enough tools in our stack, we will incorporate 
enough tools to achieve.

In many large business or startups we deploy machine learning projects going through the next stages:

1. Machine learning frameworks
    - Open AI
    - Tensorflow
    - **Pytorch**
    - SageMaker
    - GridAI
2. Distributed compute
    - Dask
    - **Spark**
    - Databricks
3. Model evaluation and experiment tracking
    - **MLFlow**
    - neptune.ai
    - Comet
4. Model deployment
    - OctoML
    - **BentoML**
5. Model monitoring and management
    - Fidler
    - Cortex
6. End-to-end platform solutions
    - nvidia
    - databricks
    - SageMaker


## Big Data Stacks

- SMACK
- Hadoop Ecosystem
- ELK Stack
- Flink Stack
- Lambda Architecture
- Microsoft Azure Stack

## SMACK
- Spark
- Mesos
- Akka
- Cassandra
- Kafka


Spark: Apache Spark is an in-memory data processing framework that facilitates distributed processing and analysis of large data sets efficiently.

Mesos: Apache Mesos is a cluster management system that enables efficient resource allocation between applications and services in a distributed environment.

Akka: Akka is a toolkit and runtime for building concurrent and distributed systems based on the actor model, which are independent processing units that communicate with each other.

Cassandra: Apache Cassandra is a highly scalable and fault-tolerant distributed database used to manage large volumes of data distributed across multiple nodes.

Kafka: Apache Kafka is a distributed event streaming platform that facilitates real-time data ingestion and processing through event streams.


## Review of Projects

- Geolocation Analysis for Transportation Applications
    - Proximity Service
    - Nearby Friends
- Visual Search System
- Google Street View Blurring System
- Youtube Video Search
- Harmful Content Detection
- Video Recommendation System
- Event Recommendation System
- Ad Click Prediction on Social Platforms
- Similar Listings on Vacation Rental Platforms
- Personalized News Feed
- People You May Know


### Requirements

- hydra: `pip install hydra-core --upgrade`



