# Matemáticas para Machine Learning

Para entender mejor cómo funciona el machine learning y cómo elegir los modelos aplicables en
cada situación, conviene tener nociones de **teoría del aprendizaje**. Podemos considerarla una
combinación de análisis estadístico y funcional, aunque hay bastante más y muchas áreas
colindantes.

Aprender de estas abstracciones ayuda a decidir estrategias para atacar problemas reales.
Dicho esto, hay muchos otros factores que determinan la calidad de los resultados de un modelo,
y que a menudo hacen del machine learning **más un arte que una ciencia**. Aunque muchos
resultados podrían justificarse, en la industria rara vez hay tiempo para entender en
profundidad por qué funcionan —y en la academia ocurre algo parecido: ambas necesitan
resultados para sobrevivir, lo que deja poco espacio para una comprensión más honda.

> *"Cualquier tecnología suficientemente avanzada es indistinguible de la magia."*
> — Arthur C. Clarke

Para una comprensión profunda convendría repasar:

- Álgebra lineal
- Estadística
- Espacios de Hilbert
- Espacios de Sobolev
- Variedades (*manifolds*)
- Regularización
- Cuadraturas

Hay muchos más temas y áreas completas que podrían considerarse, pero recorrerlos todos
llevaría una vida.

## Teoría del aprendizaje computacional

La **teoría del aprendizaje computacional** es el campo que se ocupa de aplicar métodos
matemáticos formales a los sistemas de aprendizaje. Abarca:

- [Supervisado](../01_SUPERVISED_LEARNING/introduccion.md)
- [No supervisado](../02_UNSUPERVISED_LEARNING/introduccion.md)
- En línea (*online*)
- [Por refuerzo](../03_REINFORCEMENT_LEARNING/introduccion.md)

Hoy el supervisado es la técnica más usada: cada punto \((X,y)\) de un conjunto de
entrenamiento \(\mathbb{X}\times Y\) asocia una entrada con una salida. El problema de
aprendizaje consiste en **inferir la función que mapea** entrada a salida, de modo que la
función aprendida sirva para predecir la salida a partir de entradas futuras.

## Estimación de densidad

La **estimación de densidad** camina en la frontera entre el aprendizaje no supervisado, la
ingeniería de features y el modelado de datos.

Un grupo amplio de técnicas útiles son los **modelos de mezcla**, como las **mezclas de
gaussianas**, y los enfoques basados en vecindad, como la **estimación de densidad por kernel**
(*kernel density estimation*).

Las mezclas de gaussianas se tratan con más detalle en el contexto del
[clustering](../02_UNSUPERVISED_LEARNING/introduccion.md), porque la técnica también sirve como
esquema de agrupamiento no supervisado.

La estimación de densidad es un concepto muy simple, y casi todo el mundo conoce ya una técnica
habitual: **el histograma**. Su principal problema, sin embargo, es que **la elección de los
intervalos** (*binning*) tiene un efecto desproporcionado sobre la visualización resultante. De
ahí la necesidad de una forma más precisa y automática de representar la densidad.

## En esta sección

- [Forward propagation](forward_propagation.md)
- [Funciones de base radial](funciones_de_base_radial.md)
