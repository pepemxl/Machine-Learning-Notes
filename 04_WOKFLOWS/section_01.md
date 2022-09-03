# Machine Learning
## Feature Store Systems

A Feature Store System(FSS) is an specialized database system for datasets and features that can support feature store tasks.
- Storage of raw datasets
- Generation of features based on datasets and rules
- Feature Discovery
- Feature Computation, backfills and logging
- Generation of feature metrics 
- Works as a offline feature store or a online
feature store.
- It can make use of a ML Feature Engineering Framework.
- Feature Sharing and Reuse
- Feature versioning
- Feature Lineage
- Feature Metadata
- Feature Quality
- Ensure consistency between Training Data and Serving Data
- Pipeline monitoring
    - development
    - automation
    - alerting
    
All these aspects are desired aspects in a ML environment. We need to start to divide creation of models in three types:

- Research
- Development
- Product

Many times we have some percentage of uncertainty how well will a model work with our data, it can need a few experiments or go from dozens to thousands of experiments, depending on our system and the type of model these experiments can be automatized or should be performed semi-manually.

Specialized systems are created to work with production data, it become an advantage at the moment to produtionize a model, however  each run of the experiment has many common expensive steps, that are repeated in production environments because are not suppose to repeat process in the same data. 

Loading data become an expensive process and it does not scale well with the incremment of the data, these kind of bottle necks make the process slow.

Data Protection Regulation(DPR) makes harder the work, now it is needed to aggregate or transform data in order to protect users information, however this reduce the capacity to reuse data in intermediate states. Now those states become volatiles, and its licycle is very short. 


