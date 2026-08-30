# Forward Propagation

La **propagación hacia adelante** (*forward propagation*) es el paso en que una red neuronal
calcula su salida a partir de una entrada, capa por capa. Es la mitad del entrenamiento; la
otra es la retropropagación (*backpropagation*), que calcula los gradientes.

## El cálculo capa por capa

Para una capa $l$ con matriz de pesos $W^{[l]}$, vector de sesgos $b^{[l]}$ y función de
activación $g^{[l]}$:

$$Z^{[l]} = W^{[l]} A^{[l-1]} + b^{[l]}$$

$$A^{[l]} = g^{[l]}\left(Z^{[l]}\right)$$

donde $A^{[0]} = X$ es la entrada. La salida de la red es $A^{[L]}$, con $L$ el número de
capas.

Cada capa hace dos cosas: una **transformación afín** ($Z$) y una **no linealidad** ($A$). Sin
la segunda, componer capas lineales daría otra transformación lineal, y la profundidad no
aportaría nada.

## Funciones de activación

| Función | Expresión | Rango | Notas |
|---|---|---|---|
| Sigmoide | $\frac{1}{1+e^{-z}}$ | $(0,1)$ | Satura; se usa en la salida binaria |
| Tanh | $\tanh(z)$ | $(-1,1)$ | Centrada en cero; también satura |
| ReLU | $\max(0, z)$ | $[0,\infty)$ | La opción por defecto en capas ocultas |
| Leaky ReLU | $\max(\alpha z, z)$ | $\mathbb{R}$ | Evita neuronas muertas |
| Softmax | $\frac{e^{z_i}}{\sum_j e^{z_j}}$ | $(0,1)$, suma 1 | Salida multiclase |

## Implementación

```python
import numpy as np

def relu(z):
    return np.maximum(0, z)

def softmax(z):
    z_est = z - np.max(z, axis=0, keepdims=True)   # estabilidad numerica
    exp_z = np.exp(z_est)
    return exp_z / np.sum(exp_z, axis=0, keepdims=True)


def forward_propagation(X, parametros):
    """
    X: array (n_features, n_muestras)
    parametros: dict con 'W1','b1','W2','b2',... por capa.
    Devuelve la salida y la cache necesaria para backpropagation.
    """
    cache = {'A0': X}
    A = X
    n_capas = len(parametros) // 2

    for l in range(1, n_capas + 1):
        W, b = parametros[f'W{l}'], parametros[f'b{l}']
        Z = W @ A + b
        A = softmax(Z) if l == n_capas else relu(Z)
        cache[f'Z{l}'], cache[f'A{l}'] = Z, A

    return A, cache
```

Guardar la *cache* no es un detalle de implementación: la retropropagación necesita los valores
intermedios $Z^{[l]}$ y $A^{[l]}$ para calcular los gradientes sin recalcular el paso hacia
adelante.

## Ver también

- [Matemáticas para machine learning](matematicas_para_machine_learning.md)
- [Regresión lineal](../01_SUPERVISED_LEARNING/regresion_lineal.md) — el descenso de gradiente
  que consume estos gradientes.
