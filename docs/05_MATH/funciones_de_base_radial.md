# Funciones de Base Radial

En machine learning, el **kernel de función de base radial** —o kernel RBF— es una función
kernel muy usada en algoritmos de aprendizaje kernelizados. En particular, es habitual en la
clasificación con [máquinas de vectores de soporte](../01_SUPERVISED_LEARNING/support_vector_machines.md).

## Definición

El kernel RBF sobre dos muestras $x_{1}, x_{2} \in \mathbb{R}^{n}$ se define como:

$$K(x_{1}, x_{2}) = \exp\left(-\frac{\|x_{1} - x_{2}\|^{2}}{2\sigma^{2}}\right)$$

Es frecuente reparametrizarlo con $\gamma = \frac{1}{2\sigma^{2}}$:

$$K(x_{1}, x_{2}) = \exp\left(-\gamma \|x_{1} - x_{2}\|^{2}\right)$$

El valor del kernel decrece con la distancia entre las muestras y está acotado en el intervalo
$(0, 1]$. Vale exactamente 1 cuando $x_{1} = x_{2}$, y tiende a 0 conforme se alejan. Por eso se
interpreta como una **medida de similitud**.

## Por qué se llama radial

Porque su valor depende únicamente de la **distancia** entre los puntos, no de su dirección:

$$K(x_{1}, x_{2}) = \phi(\|x_{1} - x_{2}\|)$$

Todas las muestras a la misma distancia del centro reciben el mismo valor, de ahí la simetría
radial.

## El espacio de características implícito

La propiedad notable del kernel RBF es que corresponde a un producto interno en un espacio de
características de **dimensión infinita**. Desarrollando la exponencial en serie de Taylor
aparecen términos de todos los grados polinómicos.

Esto es el *kernel trick* en su forma más potente: se opera implícitamente en un espacio
infinito-dimensional **sin construirlo nunca**, porque solo se necesita el valor del kernel
entre pares de puntos.

## El parámetro gamma

$\gamma$ controla el alcance de influencia de cada muestra de entrenamiento:

| Valor de $\gamma$ | Efecto |
|---|---|
| Bajo | Influencia amplia; frontera de decisión suave; riesgo de *underfitting* |
| Alto | Influencia local; frontera muy flexible; riesgo de *overfitting* |

En `scikit-learn`, el valor por defecto `gamma='scale'` usa
$\gamma = \frac{1}{n_{features} \cdot \mathrm{Var}(X)}$, lo que hace que el kernel sea robusto a
la escala de los datos. Aun así, **normalizar las features sigue siendo recomendable**, porque
la distancia euclídea que hay dentro del kernel es sensible a que una feature domine por
magnitud.

## Otros usos

Además de las SVM, las funciones de base radial aparecen en:

- **Redes RBF** — redes neuronales con RBF como función de activación en la capa oculta.
- **Interpolación RBF** — reconstrucción de superficies a partir de puntos dispersos.
- **Procesos gaussianos** — el kernel RBF es el *squared exponential*, el más común como función
  de covarianza.
