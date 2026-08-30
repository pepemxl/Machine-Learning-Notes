# Máquinas de Vectores de Soporte

En la década de 1990 se desarrolló un nuevo tipo de algoritmo de aprendizaje basado en
resultados de la **teoría del aprendizaje estadístico**: la máquina de vectores de soporte
(*Support Vector Machine*, SVM).

Esto dio origen a una nueva clase de máquinas de aprendizaje, teóricamente elegantes, que usan
el concepto central de las SVM —los **kernels**— para una variedad de tareas de aprendizaje.

Las máquinas de kernel proporcionan un **marco modular** que se adapta a distintas tareas y
dominios mediante la elección de la función kernel y del algoritmo base. Han sustituido a las
redes neuronales en diversos campos, incluyendo ingeniería, recuperación de información y
bioinformática.

## La idea del kernel

Un kernel calcula el producto interno entre dos puntos **en un espacio de características de
alta dimensión, sin construir explícitamente ese espacio**. Es lo que se conoce como el
*kernel trick*, y es lo que permite que una SVM separe linealmente datos que no son linealmente
separables en su espacio original.

Kernels habituales:

| Kernel | Expresión | Cuándo usarlo |
|---|---|---|
| Lineal | \(\langle x, x' \rangle\) | Muchas features, datos casi separables |
| Polinómico | \((\gamma \langle x, x' \rangle + r)^d\) | Interacciones entre features |
| RBF (gaussiano) | \(\exp(-\gamma \|x - x'\|^2)\) | Opción por defecto, fronteras no lineales |
| Sigmoide | \(\tanh(\gamma \langle x, x' \rangle + r)\) | Poco usado en la práctica |

Ver [Funciones de base radial](../05_MATH/funciones_de_base_radial.md) para el detalle del
kernel RBF.

## Variantes

- **SVC** — clasificación.
- **SVR** — regresión.
- **One-Class SVM** — [detección de anomalías](../02_UNSUPERVISED_LEARNING/deteccion_de_anomalias.md).

## Referencias

- Schölkopf, B. y Smola, A. *Learning with Kernels* (2002). Es la introducción de referencia a
  las SVM y a los métodos de kernel: parte de lo básico pero llega hasta los resultados de
  investigación, y da los conceptos necesarios para que alguien con formación matemática
  básica pueda entrar en el mundo del machine learning con algoritmos de kernel bien
  fundamentados y fáciles de usar.
- Cortes, C. y Vapnik, V. *Support-Vector Networks*, Machine Learning (1995).
