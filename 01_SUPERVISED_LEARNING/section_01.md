# Introduction


Machine Learning can be divided into 2 large categories:

1. Supervised Learning
2. Unsupervised Learning

however we can include other 2 small categories:

3. Semi-supervised Learning
4. Reinforcement Learning

For now we will focus in supervised and unsupervised learning.

![ML Taxonomy](../diagrams/ml_taxonomy.png)



## Supervised Learning

**Supervised learning** is maybe the most utilized machine learning method in the last years. Common algorithms used during supervised learning includes 
- **linear regression**,
- **decision trees**, 
- **support vector machines**, and 
- **neural networks**.

In **Supervised Learning** every point $(X,y)$ in a training dataset $\mathbb{X}\times Y$, where the input maps to an output. 


![Training Set](../diagrams/training_set.png)


The learning problem consists of inferring the function that maps between the input and the output, such that the learned function can be used to predict the output from future input.

This machine learning type got its name because the machine is “supervised” while it's learning, which means that you’re feeding the algorithm information to help it learn. The outcome you provide the machine is labeled data, and the rest of the information you give is used as input features.

Supervised learning is effective for a variety of business purposes, including sales forecasting, inventory optimization, and fraud detection. Some classic examples of use cases include:

- Predicting real estate prices
- Classifying whether bank transactions are fraudulent or not
- Finding disease risk factors
- Determining whether loan applicants are low-risk or high-risk
- Predicting the failure of industrial equipment's mechanical parts

Supervised machine learning drives a several business applications and it is the reason because nowadays is considered one of the most important categories.

### Supervised Methods Approach

Consider a set $\Omega$ and a subset $D\subset \Omega$, where $D$ is fully labeled.

Given the set of labels $L$ with a mapping function 

$$\begin{array}{cccc}
\mathcal{L}: & D & \longrightarrow & L \\
& \omega & \longmapsto & l_{\omega} \\
\end{array}$$

we want to extend this function $\mathcal{L}$ to the full set $\Omega$,

$$\begin{array}{cccc}
\widehat{\mathcal{L}}: & \Omega & \longrightarrow & L^{*} \\
& \omega & \longmapsto & l_{\omega} \\
\end{array}$$

such that $ \widehat{\mathcal{L}}_{|_{D}} = \mathcal{L} $


## Applying Maths

There are many simple and complex ways to achieve this goal, that usually involves statistics and/or differential equations with linear/nonlinear optimizations which can be convex/non-convex problems, where deterministic and stochastic algorithms are used to create applications in images, speech recognition, recommendation systems, search engines and more.

Our prefered algorithms have the next charateristics:
- scale well with the number of variables
- parallelize well

In real problems the time is a key factor to achieve success. Then is needed to define thresholds between complexity and accuracy based on time available. Maybe a very complex strategy has the best results, but cost several times more to built this strategy.

In supervised learning base principle is Empirical Risk Minimization (ERM), this is a principle in statistical learning theory which defines a family of learning algorithms and is used to give theoretical bounds on their performance.

The core idea is that we cannot know exactly how well an algorithm will work in practice (the actual "risk") because we don't know the true distribution of data that the algorithm will work on, but we can instead measure its performance on a known set of training data (the "empirical" risk).

In many cases supervised methods are mapping each element in a dataset $D \subset \Omega$ into another space where exist some order or at least a partial order, it means we have some structure that permit us to group elements, this is a very oversimplified consecuence of Dvoretzky's theorem . 

Consider a partition 
$\Omega=\bigcup_{i=1}^{k}\Omega_{i}$ and functions $\{f_{i}\}$

$$\begin{array}{cccc}
f_{i}: & \Omega_{i} & \longrightarrow & U_{i}\\
& \omega & \longmapsto & x
\end{array}
$$

We are creating features from our dataset, which can be created only using numerical values based on each $\omega \in \Omega_{i}$ or they can be aggregated values that depends on all values in $\Omega_{i}$.

To achieve this goal we dotate of more structure to our dataset adding some metrics or indicators, it means we create functions that goes from our dataset to another espace that we will call **spaces of features**, where a measurement can be defined or at least categorized.


We will recall this 
$$\mathbb{X}=\bigcup_{i=1}^{k}U_{i}$$
our space of features. Hopefully $\mathbb{X}$ can be dotated with a nice structure capable to perform statistical inference.


We always can map categories to values in $\mathbb{R}$, then our features $\{f_{1}, ...,f_{m}\}$ are functions:

$$f_{i}:D\cap \Omega_{i} \longrightarrow U_{i}\subset\mathbb{R}^{m_{i}}$$


now we want to find maps $\{g_{i}\}$ such that:

$$\begin{array}{cccc}
g_{i}: & U_{i}\subset \mathbb{X} & \longrightarrow & V_{i}\subset L^{*}\\
& x = f_{i}(\omega) & \longmapsto & l_{x}
\end{array}$$

then

$$\widehat{\mathcal{L}}_{|_{\Omega_{i}}} = g_{i}\circ f_{i}$$


With this approach we have created two apparently different problems, 
firstly find suitable $\{f_{i}\}$ that will create our **space of features** and as second problem find $\{g_{i}\}$ that maps our new features with the labels of our fully labeled dataset $D$.

Both problems represents a challenge where several computational and statistical techniques are implemented, there are some techniques using very deep mathematical theory, however many impresive results make used of heuristics.


# General ML Workflow

The input data for training the model is preprocessed,then features are created. Once the machine learning model is trained, it can be used to make predictions on the unseen data. 


## GIGO Principle

An important principle that should be remembered always is GIGO (Garbage In Garbage Out), unfortunately very often ML practitioners use supervised methods without pay enough attention to creation of features, using incorrectly techniques of clustering that finish generating swaping and masking effects on our features, making features unable to create good models, always is hard to get a good labeling process, but if bad decision are took while features are created it will become many times harder to obtain a good model.

## New Trends in MLOps

It has been clear for many data scientist that ignore data and pretend that ML models will learn patterns in its owns will be feasible without an special attention in data.

Then Data Focus MLOps has started to be a trend.






## Supervised Learning Models

In Supervied Learning we have two large groups:
- Classification Models
- Regression Models

Each group can be divided in subgroups:
Classification and Regression models have versions of each one of them
because it is feasible convert classification models into regression models and viceversa:
- Linear
- Support Vector Machines
    - SVC
    - SVM
    - SVR
- Tree
    - Decision
    - Extra
- Random Forest
    - Extra
    - LGBM
    - Random Forest
    - XGBRF
- Boosting
    - LBGM
    - XGB
- Other


List of some models found in Scikit-Learn library for each group:
1. Classification
    - Linear
        - LogisticRegression
        - LogisticRegressionCV
        - PassiveAggressiveClassifier
        - Perceptron
        - RidgeClassifier
        - RidgeClassifierCV
        - SGDClassifier
2. Regression
    - Linear
        - ARDRegression
        - BayesianRidge
        - ElasticNet
        - ElasticNetCV
        - GammaRegressor
        - HuberRegressor
        - Lars
        - LarsCV
        - Lasso
        - LassoCV
        - LassoLars
        - LassoLarsCV
        - LassoLarsIC
        - LinearRegression
        - OrthogonalMatchingPursuit
        - OrthogonalMatchingPursuitCV
        - PassiveAggressiveRegressor
        - PoissonRegressor
        - RANSACRegressor
        - Ridge
        - RidgeCV
        - SGDRegressor
        - TheilSenRegressor
        - TweedieRegressor

- Linear Regression Model
- Logistic Regression Model
- Decision Trees
- Random Forest
- Boosted Grandient Algorithms
- Support Vector Machines
- Neural Networks
- Graph Neural Networks





