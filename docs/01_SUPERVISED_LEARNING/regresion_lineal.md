# Regresión Lineal

## Construcción de un modelo de regresión lineal

La **regresión lineal** modela la relación entre un conjunto de variables independientes
\(\mathbb{X}\) y la salida o variable dependiente \(y\).

$$ y = ax+b $$

Si las variables de entrada contienen \(n\) variables independientes, hablamos de **regresión
lineal multivariable**.

$$ y = a_{0}+a_{1}x_{1}+a_{2}x_{2}+\cdots + a_{n}x_{n} $$

## Las matemáticas detrás del modelo

Como vimos antes, para ajustar modelos lineales regularizados usamos variantes del
[descenso de gradiente](https://en.wikipedia.org/wiki/Gradient_descent).

El descenso de gradiente es un algoritmo para encontrar un **mínimo local** de una función
diferenciable \(f\in C^{1}(U_{a})\).

La idea es dar pasos sucesivos en la dirección opuesta al gradiente \(\nabla{f}\), porque esa
es la dirección de máximo descenso.

Dado el punto \(a_{0} = a\), iteramos

$$a_{n+1} = a_{n}-\lambda_{n}\cdot\nabla{f(a_{n})},\, \lambda \in \mathbb{R}$$

Entonces, para \(\lambda_{n} << 1\) sabemos que

$$f(a_{n})\geq f(a_{n+1}) $$

Obtenemos una sucesión monótona que terminará en un mínimo local.

Si nuestra función \(f\) es convexa, o \(\nabla{f}\) es Lipschitz en un punto \(x\), podemos
definir

$$\lambda_{n} = \frac{(x_{n}-x_{n-1})^{T}|\nabla{f}(x_{n})-\nabla{f}(x_{n-1})|}{||\nabla{f}(x_{n})-\nabla{f}(x_{n-1})||^{2}}$$

para asegurar la convergencia a un mínimo local.

## Sistemas lineales

Consideremos el problema de un sistema lineal

$$A\mathbf{x}-\mathbf{b} = 0$$

Si la matriz del sistema \(A\) es real, simétrica y definida positiva, se define una función
objetivo cuadrática cuya minimización es

$$F(\mathbf{x}) = \mathbf{x}^{T}A\mathbf{x} -2\mathbf{x}^{T}\mathbf{b}$$

y entonces

$$\nabla F(\mathbf{x}) = 2(A\mathbf{x} -\mathbf{b} )$$

Para una matriz real general \(A\), los mínimos cuadrados lineales definen

$$F(\mathbf{x} )=\left\|A\mathbf{x} - \mathbf{b} \right\|^{2}$$

y entonces

$$\nabla F(\mathbf{x}) = 2A^{T}(A\mathbf{x} -\mathbf{b} )$$

## Descenso de gradiente estocástico (SGD)

El nombre *SGD Classifier* puede llevar a pensar que SGD es un clasificador. **No lo es.**
El `SGDClassifier` es un clasificador lineal **optimizado mediante** SGD.

Son dos conceptos distintos: mientras SGD es un **método de optimización**, la regresión
logística o las [máquinas de vectores de soporte](support_vector_machines.md) lineales son
**algoritmos o modelos** de machine learning.

Una forma útil de verlo: el modelo de machine learning define una **función de pérdida**, y el
método de optimización la minimiza o maximiza.

Ver también [Matemáticas para machine learning](../05_MATH/matematicas_para_machine_learning.md).
