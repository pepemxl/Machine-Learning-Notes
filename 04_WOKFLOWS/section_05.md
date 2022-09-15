# Workflows, State Machines and Queues

To perform our ML task we need mechanisms to schedule task that can take seconds or several days, we have two types of systems related with data processing:

1. Data Intensive Systems
2. Compute Intensive Systems

Each one of them has its own problems, and ways to perform optimizations, unfortunately many systems are born as a Data Intesive Systems and they are reused as Compute Intesive Systems with theirs respectively problems, with out a previous analysis. Our current competitive culture don't let chance to analyze things enough before to launch an MVP. Then is needed to do several adjustement during the road.

There exist this false feeling that use distributed systems solves whatever problem of scalability, however, 


# Task Queue System

- Queue priorities
- Delayed tasks (run tasks after a timedelta eta)
- Scheduled cron periodic tasks
- Broadcast tasks (run a task on all workers)
- Task soft and hard timeout limits
- Optionally retry tasks on soft timeouts
- Combats memory leaks by restarting workers when max_mem_percent reached
- Super minimal and maintainable

## Some feature useful

- sending code stats email reports
- permit to recover status of queue from jupyter notebook
- create gantt for jupyter-notebook


# State Machines

The usual way to create pipelines in machine learning is creating dags in workflows, it permits create complex pipelines, other way to create pipelines less complex, but more flexible is through state machines.

A workflow is a model of a process in your application. It may be the process of how a blog post goes from draft to review and publish. Another example is when a user submits a series of different forms to complete a task. Such processes are best kept away from your models and should be defined in configuration.

A definition of a workflow consists of places and actions to get from one place to another. The actions are called **transitions**. A workflow also needs to know each object's position in the workflow. The marking store writes the current place to a property on the object.

The simplest workflow looks like this. It contains two places and one transition.

p_A >> trans_1 >> p_B

A state machine is a subset of a workflow and its purpose is to hold a state of your model. The most important differences between them are:

- Workflows can be in more than one place at the same time, whereas state machines can't.
- In order to apply a transition, workflows require that the object is in all the previous places of the transition, whereas state machines only require that the object is at least in one of those places.

## Finite State Machines (FSM)

An Finite State Machine or State Machine is a mathematical model of computation.

It ($\Sigma$) consists of a finite set of states(S), transitions($\gamma$), events(E), and actions(A).

$$\Sigma = (S,A,E,\gamma)$$

We use actions for representing what the agent does that causes changes in its world whereas events are used for representing things that occur outside of the agent’s control, they might be the actions of other agents or part of the dynamics of the world.

In practice (implementation) we will use event for both event and action, for simplicity.

### Example

A simple example of an Finite State Machine for a door. We have two **states** `{opened, closed}`, two **actions/events** `{open, close}` and the following transitions.

|Current State|Action/Event|New State|
|---|---|---|
|closed|open|opened|
|closed|close|closed|
|opened|open|opened|
|opened|close|closed|


## Hierarchical Finite State Machine
HFSM resolves the issues that we have seen in FSM by improving the following:

- Modularity and reusability
- Hierarchical construct

HFSM introduces the following concepts:

- Parent State Machine: A state machine that a state belongs to
- Child State Machine: A state machine owned by a state that is started when the state is entered and stopped when the state is exited

## State Machine Terminology

There are many ways to define state machines, however common vocabulary used is the next:

- State: The basic unit that composes a state machine. A state machine can be in one state at any particular time.
- Entry Action: An activity executed when entering the state
- Exit Action: An activity executed when exiting the state
- Transition: A directed relationship between two states that represents the complete response of a state machine to an occurrence of an event of a particular type.
- Shared Transition: A transition that shares a source state and trigger with one or more transitions, but has a unique condition and action.
- Trigger: A triggering activity that causes a transition to occur.
- Condition: A constraint that must evaluate to true after the trigger occurs in order for the transition to complete.
- Transition Action: An activity that is executed when performing a certain transition.
- Conditional Transition: A transition with an explicit condition.
- Self-transition: A transition that transits from a state to itself.
- Initial State: A state that represents the starting point of the state machine.
- Final State: A state that represents the completion of the state machine.

## State Machines in Machine Learning Systems

Individual states can make decisions based on their input, perform actions, and pass output to other states. In AWS Step Functions you define your workflows in the Amazon States Language. The Step Functions console provides a graphical representation of that state machine to help visualize your application logic.



