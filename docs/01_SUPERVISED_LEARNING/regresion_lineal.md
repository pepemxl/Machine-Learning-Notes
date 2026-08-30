# Linear Regressions

## Building a Linear Regression Model

**Linear regression** refers to modeling the relationship between a set of independent variables \(\mathbb{X}\) and the output or dependent variables \(y\). 

$$ y = ax+b $$

If the input variables contains \(n\) independent variables, this is known as **multivariable linear regression**. 

$$ y = a_{0}+a_{1}x_{1}+a_{2}x_{2}+\cdots + a_{n}x_{n} $$


## Math behind a linear regression model

As we discused previously in order to fit regularized 
linear models we use variants of [gradient descent](https://en.wikipedia.org/wiki/Gradient_descent).

Gradient descent is an algorithm for finding a local minimum of a differentiable function \(f\in C^{1}(U_{a})\). 

The idea is to take repeated steps in the opposite direction of the gradient \(\nabla{f}\), because this is the direction of steepest descent.

Given the point \(a_{0} = a\) we iterate 

$$a_{n+1} = a_{n}-\lambda_{n}\cdot\nabla{f(a_{n})},\, \lambda \in \mathbb{R}$$

then for \(\lambda_{n} << 1\) we know that $$f(a_{n})\geq f(a_{n+1}) $$
we obtained a monotonic sequence, that will finish in a local minimum.
 
If our function \(f\) is convex or \(\nabla{f}\) is Lipschitz  in a point \(x\) we can define 
$$\lambda_{n} = \frac{(x_{n}-x_{n-1})^{T}|\nabla{f}(x_{n})-\nabla{f}(x_{n-1})|}{||\nabla{f}(x_{n})-\nabla{f}(x_{n-1})||^{2}}$$

to secure convergence to a local minimum.


## Linear System

Consider a linear system problem 

$$A\mathbf{x}-\mathbf{b} = 0$$

If the system matrix \(A\) is real symmetric and positive-definite, an objective function is defined as the quadratic function, with minimization of

$$F(\mathbf{x}) = \mathbf{x}^{T}A\mathbf{x} -2\mathbf{x}^{T}\mathbf{b}$$
then,
$$\nabla F(\mathbf{x}) = 2(A\mathbf{x} -\mathbf{b} )$$

For a general real matrix \(A\), linear least squares define

$$F(\mathbf{x} )=\left\|A\mathbf{x} - \mathbf{b} \right\|^{2}$$
then,
$$\nabla F(\mathbf{x}) = 2A^{T}(A\mathbf{x} -\mathbf{b} )$$


## Stochastic Gradient Descent (SGD)

The name Stochastic Gradient Descent Classifier might mislead some user to think that SGD is a classifier. But that’s not the case! SGD Classifier is a linear classifier optimized by the SGD!!!. 

These are two different concepts. While SGD is a optimization method, Logistic Regression or linear Support Vector Machine are machine learning algorithms or models. 

You can think of that a machine learning model defines a loss function, and the optimization method minimizes/maximizes its loss function.



