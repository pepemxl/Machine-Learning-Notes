# Isolation Forest

Isolation Forest algorithm utilizes the fact that anomalous observations are few and significantly different from `normal` observations.

The forest is built on the basis of decision trees, each of the trees having access to a sub-sample of the training data. 

In order to create a branch in the tree,
- a random feature is selected.
    - a random split value ( between min and max value) is chosen for that feature. 
    - If the given observation has a lower value of this feature then the one selected it follows the left branch, otherwise the right one. 

This process is continued until a single point is isolated or specified maximum depth is reached.


## Some drawbacks

Our intuition tells that anomalies will be radial outliers of central common points, however, the nature creation of decision trees and how works Isolation Forest led us some conclusion about problems caused by only spliting features by random values. 

If we visualize a 2D plot of anomalies


and plot anomaly score we can notice how anomaly score values in verticals and horizontals are affected by this decision, then it is clear the our partition of the freatue space affects our anomaly score, is where make sense to create a new partition.

