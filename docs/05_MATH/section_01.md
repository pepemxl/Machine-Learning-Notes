# Maths

In order to understand better how machine learning works and how select models applyable in each situation, it is important to get some insights from learning theory, we can consider learning theory as a combination of statistical and functional analysis but there are more things there and many siblings areas.

Learning insights from these abstractions will help you to decide strategies to tackle actual problems, finally there are many other factors that determine the quality of your model results, and many times make machine learning more an art than science, regardless many results could be justified, usually for some results in industry there is no time to understand deeper why it works including academy both need results in order to survive denying room for a better understanding.


**''Any sufficiently advanced technology is indistinguishable from magic.''**, Arthur C. Clarke

In order to have a deep understanding, you would perform an overview of
- Linear Algebra
- Statistics
- Hilbert Spaces
- Sobolev Spaces
- Manifolds
- Regularization
- Quadratures

there are many more math topics and full areas that could be considered, however it will take a life to go under all those topics.


# Learning Theory

Computational learning theory is a field of study concerned with the use of formal mathematical methods applied to learning systems.

These involves
- Supervised
- Unsupervised
- Online
- Reinforcement

nowadays supervised is the most used technique, where every point $(X,y)$ in a training dataset $\mathbb{X}\times Y$, where the input maps to an output. The learning problem consists of inferring the function that maps between the input and the output, such that the learned function can be used to predict the output from future input.



# Density Estimation

**Density estimation** walks the line between unsupervised learning, feature engineering, and data modeling. A large group of useful density estimations techniques is mixture models such as **Gaussian Mixtures**, and neighbor based approaches such as the **kernel density estimation**.

**Gaussian Mixtures** are discussed more fully in the context of **clustering**, because the technique is also useful as an unsupervised clustering scheme/technique.

Density estimation is a very simple concept, and most people are already familiar with one common density estimation technique: **the histogram**. A major problem with histograms, however, is that the choice of binning can have a disproportionate effect on the resulting visualization. We want an more accurate/acutomatic way to represent density 