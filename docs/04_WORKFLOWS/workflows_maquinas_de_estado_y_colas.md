# Workflows, Máquinas de Estado y Colas

Para ejecutar nuestras tareas de ML necesitamos mecanismos capaces de planificar trabajos que
pueden durar desde segundos hasta varios días. Hay dos tipos de sistemas relacionados con el
procesamiento de datos:

1. **Sistemas intensivos en datos** (*data intensive*)
2. **Sistemas intensivos en cómputo** (*compute intensive*)

Cada uno tiene sus propios problemas y sus formas de optimizar. Por desgracia, muchos sistemas
nacen como intensivos en datos y se reutilizan como intensivos en cómputo —arrastrando los
problemas correspondientes— sin un análisis previo. La cultura competitiva actual no deja
margen para analizar lo suficiente antes de lanzar un MVP, así que hay que hacer varios ajustes
sobre la marcha.

Existe además la falsa sensación de que **usar sistemas distribuidos resuelve cualquier problema
de escalabilidad**. No es así: distribuir añade coordinación, latencia de red y modos de fallo
nuevos, y solo compensa cuando el cuello de botella es realmente de capacidad.

## Sistema de colas de tareas

Características deseables en un sistema de colas:

- Prioridades de cola.
- **Tareas diferidas** (ejecutar tras un `timedelta` o *eta*).
- Tareas periódicas programadas tipo *cron*.
- **Tareas de difusión** (*broadcast*): ejecutar una tarea en todos los *workers*.
- Límites de tiempo de espera **suaves y duros** por tarea.
- Reintento opcional de tareas al superar el tiempo suave.
- Mitigación de fugas de memoria reiniciando *workers* al alcanzar `max_mem_percent`.
- Ser mínimo y mantenible.

### Funcionalidades útiles adicionales

- Envío de reportes de estadísticas por correo.
- Recuperar el estado de la cola desde un Jupyter notebook.
- Generar diagramas de Gantt en Jupyter.

## Máquinas de estado

La forma habitual de crear pipelines en machine learning es construir **DAGs** en un motor de
workflows, lo que permite pipelines complejos. Otra vía, menos compleja pero **más flexible**,
es usar máquinas de estado.

Un **workflow** es un modelo de un proceso de tu aplicación. Puede ser el recorrido de un post
de blog desde borrador a revisión y publicación, o el de un usuario que rellena una serie de
formularios distintos para completar una tarea. Estos procesos conviene mantenerlos **fuera de
los modelos** y definirlos en configuración.

La definición de un workflow consta de **lugares** (*places*) y de acciones para pasar de uno a
otro. Esas acciones se llaman **transiciones**. Además, el workflow necesita conocer la
posición de cada objeto: el *marking store* escribe el lugar actual en una propiedad del
objeto.

El workflow más simple posible contiene dos lugares y una transición:

```text
p_A >> trans_1 >> p_B
```

Una **máquina de estado** es un subconjunto de un workflow, y su propósito es mantener el
estado de tu modelo. Las diferencias más importantes son:

- Los **workflows pueden estar en más de un lugar a la vez**; las máquinas de estado no.
- Para aplicar una transición, los workflows exigen que el objeto esté en **todos** los lugares
  previos de la transición; las máquinas de estado solo exigen que esté en **al menos uno**.

## Máquinas de estado finitas (FSM)

Una **máquina de estado finita** es un modelo matemático de computación.

Consiste ($\Sigma$) en un conjunto finito de estados ($S$), transiciones ($\gamma$), eventos
($E$) y acciones ($A$).

$$\Sigma = (S,A,E,\gamma)$$

Usamos **acciones** para representar lo que el agente hace y que provoca cambios en su mundo,
mientras que los **eventos** representan cosas que ocurren fuera de su control: pueden ser
acciones de otros agentes o parte de la dinámica del entorno.

En la práctica, al implementar se suele usar *evento* para ambos casos, por simplicidad.

### Ejemplo

Una máquina de estado finita sencilla para una puerta. Tenemos dos **estados**
`{abierta, cerrada}`, dos **acciones/eventos** `{abrir, cerrar}` y las siguientes transiciones:

| Estado actual | Acción/Evento | Nuevo estado |
|---|---|---|
| cerrada | abrir | abierta |
| cerrada | cerrar | cerrada |
| abierta | abrir | abierta |
| abierta | cerrar | cerrada |

## Máquinas de estado finitas jerárquicas (HFSM)

Las HFSM resuelven los problemas de las FSM mejorando:

- **Modularidad y reutilización**
- **Construcción jerárquica**

Introducen los siguientes conceptos:

- **Máquina de estado padre**: aquella a la que pertenece un estado.
- **Máquina de estado hija**: la que posee un estado, y que arranca al entrar en ese estado y
  se detiene al salir de él.

## Terminología

Hay muchas formas de definir máquinas de estado, pero el vocabulario común es este:

- **Estado**: la unidad básica que compone la máquina. Una máquina de estado puede estar en un
  solo estado en un momento dado.
- **Acción de entrada**: actividad que se ejecuta al entrar en el estado.
- **Acción de salida**: actividad que se ejecuta al salir del estado.
- **Transición**: relación dirigida entre dos estados que representa la respuesta completa de
  la máquina ante la ocurrencia de un evento de un tipo determinado.
- **Transición compartida**: transición que comparte estado origen y disparador con una o más
  transiciones, pero tiene condición y acción propias.
- **Disparador** (*trigger*): la actividad que provoca que ocurra la transición.
- **Condición**: restricción que debe evaluarse como verdadera después del disparador para que
  la transición se complete.
- **Acción de transición**: actividad que se ejecuta al realizar una transición concreta.
- **Transición condicional**: transición con una condición explícita.
- **Auto-transición**: transición que va de un estado a sí mismo.
- **Estado inicial**: representa el punto de partida de la máquina.
- **Estado final**: representa la finalización de la máquina.

## Máquinas de estado en sistemas de ML

Los estados individuales pueden **tomar decisiones** según su entrada, **ejecutar acciones** y
**pasar su salida** a otros estados.

En AWS Step Functions los workflows se definen en el *Amazon States Language*, y la consola
proporciona una representación gráfica de la máquina de estado que ayuda a visualizar la lógica
de la aplicación.

## Ver también

- [Sistemas de machine learning](sistemas_de_machine_learning.md)
- [LangGraph](../11_JARVIS/llm_workflows/langgraph.md) — grafos de estado aplicados a
  workflows con LLMs.
