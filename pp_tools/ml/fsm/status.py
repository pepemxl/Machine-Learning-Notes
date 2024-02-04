"""
Resource Status Code Summary

The creation of resources involves a computational task that can last a few seconds or a few days depending on the size of the data.
Some transitions depends on some conditions while other doesn't, consequently, in order that state transitions create a new state 
it may launch an asynchronous task and return immediately. 
In order to know the completion status of this task/transition, each resource has a status field that reports the current state of the 
state/transition. This status is useful to monitor the progress during their creation. 

The possible states for a task are:
| Code | Status | Semantics |
| --- | --- | --- |
| 0 | Waiting | The resource is waiting for another resource to be finished before BigML.io can start processing it. |
| 1 | Queued | The task that is going to create the resource has been accepted but has been queued because there are other tasks using the system. |
| 2 | Started | The task to create the resource has been is started and you should expect partial results soon. |
| 3 | In Progress | The task has computed the first partial resource but still needs to do more computations. |
| 4 | Summarized | This status is specific to datasets. It happens when the dataset has been computed but its data has not been serialized yet. The dataset is final but you cannot use it yet to create a model or if you use it the model will be waiting until the dataset is finished. |
| 5 | Finished | The task is completed and the resource is final. |
| -1 | Faulty | The task has failed. We either could not process the task as you requested it or have an internal issue. |
| -2 | Unknown | The task has reached a state that we cannot verify at this time. This a status you should never see unless that our devserver suffers a outage or connection problem. |
"""
