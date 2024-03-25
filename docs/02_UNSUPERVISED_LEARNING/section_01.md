# Inttroduction

While **supervised learning** requires users to help the machine to learn from labeling data, **unsupervised learning** doesn't use the same labeled training sets neither data. Instead, the machine looks for less obvious patterns in the data. This machine learning type is very helpful when you need to identify patterns and use data to make decisions. Common algorithms used in unsupervised learning include **Hidden Markov models**, **k-means**, **hierarchical clustering**, and **Gaussian mixture models**.

Using the example from supervised learning, let's say you didn't know which customers did or didn't default on loans. Instead, you'd provide the machine with borrower information and it would look for patterns between borrowers before grouping them into several clusters.

This type of machine learning is widely used to create predictive models. Common applications also include clustering, which creates a model that groups objects together based on specific properties, and association, which identifies the rules existing between the clusters. A few example use cases include:

Creating customer groups based on purchase behavior

Grouping inventory according to sales and/or manufacturing metrics

Pinpointing associations in customer data (for example, customers who buy a specific style of handbag might be interested in a specific style of shoe)

These are classic example that you will find searching for examples.




# Clusters

A cluster is a set of groups of instances of a dataset that have been automatically classified together according to a distance measure computed using the fields of the dataset.

Clusters can handle numeric, categorical, text and items fields as inputs:

- Numeric fields: the Eucledian distance is computed between the instances numeric values.
- Categorical fields: a common way to handle categorical data is to take each category as a new field and assign 0 or 1 depending on the category. 
- Text and item fields: each instance is assigned a vector of terms and then cosine similarity is computed to determine closeness between instances.

For categorial field with 20 categories will become 20 separate binary fields. Big Data usually uses a technique called k-prototypes which modifies the distance function to operate as though the categories were transformed to binary values.


Each cluster group is represented by a centroid or center that is computed using the mean for each numeric field and the mode for each categorical field. For text and items fields each centroid contains the terms or items which minimize the average cosine distance between the centroid and the points in its neighborhood.

To create a cluster, you can select an arbitrary number of clusters and also select an arbitrary subset of fields from your dataset as input_fields. You can use scales to select how each field influences the distance measure used to group instances together.






