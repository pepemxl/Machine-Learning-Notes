# Linear Regressions


As we discused previously in order to fit regularized 
linear models we use variants of [gradient descent](https://en.wikipedia.org/wiki/Gradient_descent).

Gradient descent is an algorithm for finding a local minimum of a differentiable function $f\in C^{1}(U_{a})$. 

The idea is to take repeated steps in the opposite direction of the gradient $\nabla{f}$, because this is the direction of steepest descent.

Given the point $a_{0} = a$ we iterate 

$a_{n+1} = a_{n}-\lambda_{n}\cdot\nabla{f(a_{n})}$, $\lambda \in \mathbb{R}$.

then for $\lambda_{n} << 1$ we know that $$f(a_{n})\geq f(a_{n+1}) $$
we obtained a monotonic sequence, that will finish in a local minimum.
 
If our function $f$ is convex or $\nabla{f}$ is Lipschitz  in a point $x$ we can define 
$$\lambda_{n} = \frac{(x_{n}-x_{n-1})^{T}|\nabla{f}(x_{n})-\nabla{f}(x_{n-1})|}{||\nabla{f}(x_{n})-\nabla{f}(x_{n-1})||^{2}}$$

to secure convergence to a local minimum.



## Linear System

Consider a linear system problem 

$$A\mathbf{x}-\mathbf{b} = 0$$

If the system matrix $A$ is real symmetric and positive-definite, an objective function is defined as the quadratic function, with minimization of

$$F(\mathbf{x}) = \mathbf{x}^{T}A\mathbf{x} -2\mathbf{x}^{T}\mathbf{b}$$
then,
$$\nabla F(\mathbf{x}) = 2(A\mathbf{x} -\mathbf{b} )$$

For a general real matrix $A$, linear least squares define

$$F(\mathbf{x} )=\left\|A\mathbf{x} - \mathbf{b} \right\|^{2}$$
then,
$$\nabla F(\mathbf{x}) = 2A^{T}(A\mathbf{x} -\mathbf{b} )$$


## 


