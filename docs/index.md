# Data Science

Machine learning, data mining and data analysis are related fields within the broader domain of data science, but they have different focuses and methodologies. Here's a brief overview of each:

1. **Data Analysis:**
   Data analysis involves examining, cleaning, transforming, and modeling data to extract insights and make informed decisions. It focuses on understanding patterns, trends, and relationships within datasets through statistical and visualization techniques. Data analysis often involves descriptive and inferential statistics, hypothesis testing, exploratory data analysis (EDA), and data visualization.

2. **Machine Learning:**
   Machine learning is a subset of artificial intelligence (AI) that focuses on developing algorithms and models that allow computers to learn from data and make predictions or decisions without being explicitly programmed. Machine learning algorithms use statistical techniques to identify patterns in data and make predictions or decisions based on those patterns. It involves training models on labeled datasets to learn patterns and relationships, which can then be used to make predictions on new, unseen data.

3. **Data Mining:**
    Data mining is the process of discovering patterns, relationships, and insights from large datasets using techniques from statistics, machine learning, and database systems. It involves extracting useful information and knowledge from data that may not be immediately obvious or explicitly stated. Data mining techniques are often used to uncover hidden patterns, anomalies, trends, or associations within data.

    Some common data mining techniques include:

    1. **Association Rule Learning:** Identifying relationships or associations between variables in a dataset. For example, identifying products that are frequently purchased together in a transaction dataset.

    2. **Clustering:** Grouping similar data points together based on their characteristics or attributes. Clustering algorithms aim to find natural groupings or clusters in the data.

    3. **Classification:** Assigning categorical labels or classes to data points based on their features. Classification algorithms learn to predict the class labels of new data points based on the patterns observed in the training data.

    4. **Regression:** Predicting continuous numerical values based on the relationship between independent and dependent variables in the data. Regression analysis aims to model and analyze the relationships between variables.

    5. **Anomaly Detection:** Identifying unusual or abnormal observations in a dataset that deviate from normal behavior. Anomaly detection techniques aim to flag potential outliers or anomalies that may require further investigation.

In summary, while data analysis focuses on exploring and understanding data to gain insights, machine learning focuses on building models that can learn from data and make predictions or decisions. Data mining is another related field within data science, but it has a slightly different focus and methodology compared to both data analysis and machine learning.

Data analysis is often a precursor to machine learning, as it involves preparing and analyzing data before training machine learning models. Additionally, machine learning techniques are often used within the context of data analysis to uncover deeper insights or automate decision-making processes.


Data mining involves using a variety of techniques to extract valuable insights and knowledge from large datasets. It often complements data analysis and machine learning by providing additional tools and methods for exploring and understanding data, identifying patterns, and making data-driven decisions.

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


## Review of Projects Big Data + ML + Data Mining

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


## Review of Projects Big Data + ML + Data Mining

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








