# Procesos de Decisión de Markov

El **proceso de decisión de Markov** (*Markov Decision Process*, MDP) es el marco
matemático sobre el que se formula casi todo el aprendizaje por refuerzo. Si un problema
se puede escribir como MDP, la teoría de RL aplica.

## Definición

Un MDP es una tupla $\mathcal{M} = (S, A, P, R, \gamma)$:

- $S$ — conjunto de **estados**.
- $A$ — conjunto de **acciones** (o $A(s)$, las disponibles en el estado $s$).
- $P(s' \mid s, a)$ — **función de transición**: probabilidad de pasar a $s'$ al ejecutar
  $a$ en $s$.
- $R(s, a, s')$ — **función de recompensa** esperada de esa transición.
- $\gamma \in [0,1]$ — **factor de descuento**.

## La propiedad de Markov

Es el supuesto que da nombre al modelo:

$$P(S_{t+1} \mid S_t, A_t) = P(S_{t+1} \mid S_0, A_0, \ldots, S_t, A_t)$$

En palabras: **el estado actual resume toda la historia relevante**. Para predecir el
futuro no necesitas saber cómo llegaste al estado actual.

Esto no es una propiedad del mundo, sino de tu **representación del estado**. Un mismo
problema puede cumplir o violar Markov según qué metas en el estado. Ejemplo clásico: una
sola imagen de un juego no te dice la velocidad de la pelota; cuatro imágenes consecutivas
apiladas, sí. Ese es exactamente el truco que usa DQN.

Cuando el agente no observa el estado completo, hablamos de un **POMDP** (*partially
observable MDP*), y hacen falta memoria (RNN) o filtros de creencia.

## Funciones de valor

Dada una política $\pi$, definimos dos funciones de valor.

**Valor de estado** — retorno esperado si partes de $s$ y sigues $\pi$:

$$V^{\pi}(s) = \mathbb{E}_{\pi}\left[ G_t \mid S_t = s \right]$$

**Valor de acción** — retorno esperado si partes de $s$, tomas $a$, y **después** sigues $\pi$:

$$Q^{\pi}(s,a) = \mathbb{E}_{\pi}\left[ G_t \mid S_t = s, A_t = a \right]$$

$Q$ es más útil en la práctica: permite elegir la mejor acción sin conocer el modelo del
entorno, simplemente tomando $\arg\max_a Q(s,a)$.

## Ecuaciones de Bellman

La observación clave de Bellman es que el valor se puede escribir **recursivamente**: el
valor de un estado es la recompensa inmediata más el valor descontado del siguiente.

Ecuación de Bellman para $V^{\pi}$:

$$V^{\pi}(s) = \sum_{a} \pi(a \mid s) \sum_{s'} P(s' \mid s,a) \left[ R(s,a,s') + \gamma V^{\pi}(s') \right]$$

Y para $Q^{\pi}$:

$$Q^{\pi}(s,a) = \sum_{s'} P(s' \mid s,a) \left[ R(s,a,s') + \gamma \sum_{a'} \pi(a' \mid s') Q^{\pi}(s',a') \right]$$

### Ecuaciones de optimalidad

La política óptima $\pi^*$ es la que maximiza el valor en **todos** los estados. Sus
funciones de valor satisfacen:

$$V^{*}(s) = \max_{a} \sum_{s'} P(s' \mid s,a)\left[ R(s,a,s') + \gamma V^{*}(s') \right]$$

$$Q^{*}(s,a) = \sum_{s'} P(s' \mid s,a)\left[ R(s,a,s') + \gamma \max_{a'} Q^{*}(s',a') \right]$$

La diferencia con las anteriores es el $\max$ en lugar de la esperanza sobre $\pi$. Una
vez tienes $Q^*$, la política óptima es inmediata:

$$\pi^{*}(s) = \arg\max_{a} Q^{*}(s,a)$$

Todo MDP finito tiene al menos una política óptima determinista.

## Programación dinámica

Cuando **conoces** $P$ y $R$ (es decir, tienes el modelo), puedes resolver el MDP
directamente. Los dos algoritmos clásicos son iteración de valor e iteración de política.

### Iteración de valor

Aplica la ecuación de optimalidad de Bellman como regla de actualización hasta converger:

```python
import numpy as np

def iteracion_de_valor(P, R, gamma=0.99, tol=1e-6):
    """
    P: array (n_estados, n_acciones, n_estados) con probabilidades de transicion.
    R: array (n_estados, n_acciones, n_estados) con recompensas esperadas.
    Devuelve (V, politica).
    """
    n_estados, n_acciones, _ = P.shape
    V = np.zeros(n_estados)

    while True:
        # Q[s,a] = sum_s' P(s'|s,a) [ R(s,a,s') + gamma V(s') ]
        Q = np.einsum('sat,sat->sa', P, R + gamma * V[None, None, :])
        V_nuevo = Q.max(axis=1)
        if np.max(np.abs(V_nuevo - V)) < tol:
            V = V_nuevo
            break
        V = V_nuevo

    Q = np.einsum('sat,sat->sa', P, R + gamma * V[None, None, :])
    return V, Q.argmax(axis=1)
```

Converge a $V^*$ porque el operador de Bellman es una **contracción** con factor $\gamma$
en la norma del supremo: cada iteración acerca la estimación al punto fijo al menos en un
factor $\gamma$.

### Iteración de política

Alterna dos fases hasta que la política deja de cambiar:

1. **Evaluación**: calcular $V^{\pi}$ para la política actual (resolviendo el sistema
   lineal o iterando).
2. **Mejora**: hacer la política *greedy* respecto a $V^{\pi}$.

Suele converger en menos iteraciones que iteración de valor, pero cada una es más cara.

## Por qué esto no basta

La programación dinámica requiere dos cosas que rara vez tienes:

1. **Conocer $P$ y $R$**. En un problema real no tienes el modelo del entorno.
2. **Barrer todos los estados**. Con $|S|$ grande —o continuo— es imposible.

De ahí salen las dos grandes ramas del RL práctico:

- **Métodos model-free** que aprenden de la experiencia sin conocer $P$:
  Monte Carlo y [diferencia temporal / Q-Learning](q_learning.md).
- **Aproximación de funciones** para no tabular todos los estados:
  [deep reinforcement learning](deep_reinforcement_learning.md).

## Resumen

| Concepto | Qué es |
|---|---|
| Propiedad de Markov | El estado resume la historia relevante |
| $V^{\pi}(s)$ | Retorno esperado desde $s$ siguiendo $\pi$ |
| $Q^{\pi}(s,a)$ | Retorno esperado desde $s$ tomando $a$, luego $\pi$ |
| Ecuación de Bellman | Descomposición recursiva del valor |
| Iteración de valor | Resuelve el MDP si conoces el modelo |
| POMDP | MDP con estado parcialmente observable |

## Referencias

- Sutton y Barto, *Reinforcement Learning: An Introduction*, capítulos 3 y 4.
- Puterman, M. *Markov Decision Processes: Discrete Stochastic Dynamic Programming* (1994).
