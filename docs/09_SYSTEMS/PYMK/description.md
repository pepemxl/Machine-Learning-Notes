# PYMK People You May Know

People You May Know is a list of users/things with whom you may want to connect, based on things you have in common, such a mutual friend, school, or workplace.


```mermaid
    C4Context
      title People You May Know
      Boundary(b0, "Know Each Other"){
        Person(p1, "P1")
        Person(p2, "P2")
        Person(p3, "P3")
      }
      Container(s1, "Object", $borderColor="#d73027")      
      Person(p4, "P4")
      BiRel(p1, p2, "know")
      BiRel(p1, p3, "know")
      BiRel(p2, p3, "know")
      Rel(p3, p4, "know")
      Rel(p1, s1, "know")
      UpdateElementStyle(p1, $fontColor="red", $bgColor="grey", $borderColor="red")
      UpdateElementStyle(p2, $fontColor="red", $bgColor="grey", $borderColor="red")
      UpdateElementStyle(p3, $fontColor="red", $bgColor="grey", $borderColor="red")
      UpdateRelStyle(p1, p2, $textColor="blue", $lineColor="blue", $offsetX="5")
      UpdateRelStyle(p1, p3, $textColor="blue", $lineColor="blue", $offsetX="5")
      UpdateRelStyle(p2, p3, $textColor="blue", $lineColor="blue", $offsetX="5")
      UpdateRelStyle(p3, p4, $textColor="orange", $lineColor="orange", $offsetX="5")
      UpdateRelStyle(p1, s1, $textColor="orange", $lineColor="orange", $offsetX="5")
      UpdateElementStyle(b0, $fontColor="red", $borderColor="red", $legendTitleColor ="red")
      UpdateLayoutConfig($c4ShapeInRow="3", $c4BoundaryInRow="1")
```



### 1. Problem Formulation
Recommend a list of users/things that you may want to connect with. For any ML recommender system shold be addresed the next questions:
* Clarifying questions
  * What is the primary business objective of the system? 
  * What's the primary use case of the system?
  * Are there specific factors needs to be considered for recommendations?
  * Are friendships/connections symmetrical?
  * What is the scale of the system? (users, connections)
  * can we assume the social graph is not very dynamic?
  * Do we need continual training? 
  * How do we collect negative samples? (not clicked, negative feedback). 
  * How fast the system needs to be? 
  * Is personalization needed? Yes 
  
## 
* Use case(s) and business goal
  * use case: PYMMK: recommend a list of users to connect with on social media app (e.g. facebook, linkedin)
  * business objective: maximize number of formed connections 

* Requirements;
    * Scalability: 1 B total users, on avg. 10000 connection per user     
  
* Constraints:
    * Privacy and compliance with data protection regulations.
    
* Data: Sources and Availability:

* Assumptions:
    * symmetric friendships
  
* ML Formulation:
    * Objective: 
      * maximize number of formed connections 
    * I/O: I: user_id, O: ranked list of recommended users sorted by the relevance to the user 
    * ML Category: two options: 
      * Ranking problem: 
        * pointwise LTR - binary classifier (user_i, user_j) -> p(connection)
        * cons: doesn't capture social connections 
      * Graph representation (edge prediction)
        * supplement with graph info (nodes, edges)
        * input: social graph, predict edge b/w nodes 

### 2. Metrics  
* Offline 
  * GNN model: binary classification -> ROC-AUC 
  * Recommendation system: binary relationships -> mAP 
  
* Online 
  * No of friend requests sent over X time 
  * No of friend requests accepted over X time 
  
### 3. Architectural Components  
* High level architecture 
  * Node-level predictions 
  * Edge-level predictions 
  
### 4. Data Collection and Preparation
* Data Sources
  * Users, 
    * demographics, edu and work backgrounds, skills, etc
    * note: standardized data (e.g. cs / computer science)
  * User-user connections,  
  * User-user interactions, 

* Labelling

### 5. Feature Engineering

* Feature selection
    
  * User: 
    * ID, username
    * Demographics (Age, gender, location)
    * Account/Network info: No of connections, followers, following, requests, etc, account age
    * Interaction history (No of likes, shares, comments)
    * Context (device, time of day, etc)
    
  * User-user connections: 
    * Connection: IDs(user1, user2), connection type, timestamp, location 
    * edu and work affinity: major similarity, companies in common, industry similarity, etc 
    * social affinity: No. mutual connections (time discounted)
  * User-user interactions:  
    * IDs(u user1, user2), interaction type, timestamp 




### 6. Model Development and Offline Evaluation

* Model selection 
  * We choose GNN 
    * operate on graph data 
    * predict prob of edge 
    * input: graph (node and edge features)
    * output: embedding of each node
    * use similarities b/w node embeddings for edge prediction 


* Model Training 
  * snapshot of G at t. model predict connections at t+1
  * Dataset 
    * create a snapshot at time t
    * compute node and edge features 
    * create labels using snapshot at t + 1 (if connection formed, positive) 
  * Model eval and HP tuning 
  * Iterations 
  
### 7. Prediction Service
* Prediction pipeline 
  * Candidate generation 
    * Friends of Friends (FoF) - rule based - from 1B to 1K.1K = 1M candidates -> FoF service  
  * Scoring service (using GNN model -> embeddings -> similarity scores)
  * sort by score 
* pre-compute PYMK tables for each / active users and store in DB 
* re-rank based on business logic 
  
### 8. Online Testing and Deployment  
* A/B Test 
* Deployment and release 

### 9. Scaling, Monitoring, and Updates 
* Scaling (SW and ML systems)
* Monitoring 
* Updates 

### 10. Other topics  
* add a lightweight ranker 
* bias problem 
* delayed feedback problem (user accepts after days)
* personalized random walk (for baseline)





# PYMK LinkedIn case

1. **Existing connections**: The algorithm may analyze your current connections and **suggest people who have connections in common with you**.
2. **Work and education history**: LinkedIn also takes into account your work and educational history. It may suggest people who have worked at the same companies or attended the same educational institutions.
3. **Skills and experiences**: Skills and professional experiences added to your profile are considered. LinkedIn might suggest people with similar skills or related work experiences.
4. **Groups and events**: Participation in LinkedIn groups and events can influence connection suggestions. If you belong to the same groups or have attended similar events, connections may be suggested based on shared interests.
5. **Location**: Geographic location is also a factor. LinkedIn might suggest connections working in the same geographical area or industry.
6. **Mutual connections**: If several of your connections are already connected with a specific person, it's more likely that this person will appear in your suggestions.
7. **Previous interactions**: Past interactions on the platform, such as profile visits or messages, can also influence suggestions.



