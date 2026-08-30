# Q-Learning y Diferencia Temporal

Los métodos de **diferencia temporal** (*temporal difference*, TD) son el corazón del RL
model-free: aprenden directamente de la experiencia, sin modelo del entorno, y **sin
esperar a que termine el episodio**.

## De Monte Carlo a TD

Para estimar $V(s)$ a partir de experiencia hay dos enfoques.

**Monte Carlo** espera a que el episodio acabe y usa el retorno real $G_t$:

$$V(S_t) \leftarrow V(S_t) + \alpha \left[ G_t - V(S_t) \right]$$

Es insesgado pero tiene varianza alta, y no sirve para tareas que nunca terminan.

**TD(0)** no espera: usa su propia estimación del siguiente estado como sustituto del
retorno. A esto se le llama ***bootstrapping***.

$$V(S_t) \leftarrow V(S_t) + \alpha \big[ \underbrace{R_{t+1} + \gamma V(S_{t+1})}_{\text{objetivo TD}} - V(S_t) \big]$$

El término entre corchetes es el **error TD**:

$$\delta_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t)$$

TD introduce sesgo (la estimación se apoya en otra estimación) pero reduce mucho la
varianza, y aprende en línea, paso a paso.

## Q-Learning

Q-Learning aplica la misma idea a la función de valor de acción, con el $\max$ de la
ecuación de optimalidad de Bellman:

$$Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha \left[ R_{t+1} + \gamma \max_{a} Q(S_{t+1}, a) - Q(S_t, A_t) \right]$$

Lo notable es el $\max$: el objetivo se calcula con la **mejor** acción del siguiente
estado, no con la que el agente vaya a tomar realmente. Eso hace a Q-Learning
**off-policy** — aprende sobre la política greedy mientras se comporta con otra
(por ejemplo $\varepsilon$-greedy).

Bajo condiciones suaves (todo par estado-acción se visita infinitas veces y la tasa de
aprendizaje decrece adecuadamente), Q-Learning converge a $Q^*$.

### Implementación tabular

```python
import numpy as np

def q_learning(entorno, n_episodios=5000, alpha=0.1, gamma=0.99,
               epsilon=1.0, epsilon_min=0.01, decaimiento=0.995):
    """Q-Learning tabular sobre un entorno con espacios discretos."""
    Q = np.zeros((entorno.observation_space.n, entorno.action_space.n))

    for _ in range(n_episodios):
        estado, _ = entorno.reset()
        terminado = False

        while not terminado:
            # Politica de comportamiento: epsilon-greedy
            if np.random.random() < epsilon:
                accion = entorno.action_space.sample()
            else:
                accion = int(np.argmax(Q[estado]))

            siguiente, recompensa, terminado, truncado, _ = entorno.step(accion)

            # Objetivo off-policy: usa el max, no la accion que se tomara
            objetivo = recompensa + gamma * np.max(Q[siguiente]) * (not terminado)
            Q[estado, accion] += alpha * (objetivo - Q[estado, accion])

            estado = siguiente
            terminado = terminado or truncado

        epsilon = max(epsilon_min, epsilon * decaimiento)

    return Q
```

## SARSA

**SARSA** es la variante **on-policy**. El nombre viene de la tupla que usa:
$(S_t, A_t, R_{t+1}, S_{t+1}, A_{t+1})$.

$$Q(S_t, A_t) \leftarrow Q(S_t, A_t) + \alpha \left[ R_{t+1} + \gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t) \right]$$

La única diferencia con Q-Learning es que en lugar de $\max_a Q(S_{t+1},a)$ usa
$Q(S_{t+1}, A_{t+1})$, donde $A_{t+1}$ es la acción **que el agente realmente tomará**.

### Q-Learning vs. SARSA

| | Q-Learning | SARSA |
|---|---|---|
| Tipo | Off-policy | On-policy |
| Objetivo | $\max_a Q(s',a)$ | $Q(s', a')$ |
| Converge a | Política óptima | Política óptima *dada la exploración* |
| Comportamiento | Más agresivo | Más conservador |

El ejemplo canónico es el **cliff walking**: un camino corto al borde de un precipicio y
uno largo y seguro. Q-Learning aprende la ruta óptima al borde, pero como sigue explorando
con $\varepsilon$-greedy, se cae de vez en cuando y acumula peor recompensa durante el
entrenamiento. SARSA, que aprende teniendo en cuenta su propia exploración, elige la ruta
segura. **SARSA aprende una política que sabe que es imperfecta; Q-Learning aprende la
política ideal e ignora que no la ejecuta.**

## Q-Learning doble

El $\max$ de Q-Learning introduce un **sesgo de sobreestimación**: como $Q$ tiene ruido,
tomar el máximo sistemáticamente selecciona las estimaciones sobreestimadas.

$$\mathbb{E}\left[\max_a Q(s,a)\right] \geq \max_a \mathbb{E}\left[Q(s,a)\right]$$

**Double Q-Learning** lo corrige manteniendo dos tablas y separando la *selección* de la
acción de su *evaluación*:

$$Q_1(S_t,A_t) \leftarrow Q_1(S_t,A_t) + \alpha \left[ R_{t+1} + \gamma\, Q_2\big(S_{t+1}, \arg\max_a Q_1(S_{t+1},a)\big) - Q_1(S_t,A_t) \right]$$

En cada paso se elige al azar cuál de las dos tablas actualizar. La misma idea reaparece
en [Double DQN](deep_reinforcement_learning.md).

## Hiperparámetros

- **$\alpha$ (tasa de aprendizaje)**: típicamente $0.1$–$0.5$ en tabular. Muy alta,
  inestable; muy baja, lentísima.
- **$\gamma$ (descuento)**: $0.9$–$0.99$. Con horizontes largos, acercarse a $0.99$.
- **$\varepsilon$ (exploración)**: empezar en $1.0$ y decaer hasta $0.01$–$0.05$.

## Limitaciones del enfoque tabular

La tabla $Q$ tiene tamaño $|S| \times |A|$. Eso funciona en rejillas pequeñas, pero:

- El **espacio de estados explota** combinatoriamente.
- Con estados **continuos** la tabla directamente no existe.
- **No hay generalización**: lo aprendido en un estado no dice nada sobre estados
  parecidos.

La solución es reemplazar la tabla por un aproximador de funciones — una red neuronal.
Eso es [deep reinforcement learning](deep_reinforcement_learning.md).

## Referencias

- Watkins, C. y Dayan, P. *Q-learning*, Machine Learning (1992).
- Hasselt, H. van. *Double Q-learning*, NIPS (2010).
- Sutton y Barto, capítulo 6.
