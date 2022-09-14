# State Machines

The usual way to create pipelines in machine learning is creating dags in workflows, it permits create complex pipelines, other way to create pipelines less complex, but more flexible is through state machines.

A workflow is a model of a process in your application. It may be the process of how a blog post goes from draft to review and publish. Another example is when a user submits a series of different forms to complete a task. Such processes are best kept away from your models and should be defined in configuration.

A definition of a workflow consists of places and actions to get from one place to another. The actions are called **transitions**. A workflow also needs to know each object's position in the workflow. The marking store writes the current place to a property on the object.

The simplest workflow looks like this. It contains two places and one transition.

p_A >> trans_1 >> p_B

A state machine is a subset of a workflow and its purpose is to hold a state of your model. The most important differences between them are:

- Workflows can be in more than one place at the same time, whereas state machines can't.
- In order to apply a transition, workflows require that the object is in all the previous places of the transition, whereas state machines only require that the object is at least in one of those places.


## State Machines in Machine Learning Systems

Individual states can make decisions based on their input, perform actions, and pass output to other states. In AWS Step Functions you define your workflows in the Amazon States Language. The Step Functions console provides a graphical representation of that state machine to help visualize your application logic.



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