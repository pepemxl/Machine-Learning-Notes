# Spark

Apache Spark is a technology that superseded Hadoop's MapReduce as the preferred big data processing platform. Spark is similar to Hadoop in that it's a distributed, general-purpose computing platform. But Spark's unique design, which allows for keeping large amounts of data in memory, offers tremendous
performance improvements. Spark programs can be 100X faster than their MapReduce counterparts.

- Application in Spark consists of a `driver program` and `executors` on the cluster.
- A `cluster manager` is an external service for acquiring resources on the cluster. It can be the Spark built-in cluster manager.
- Driver program is the process running the `main()` function of the application and creating the `SparkContext`.
- An `executor` is a process launched for an application on a worker node. The executor runs tasks and keeps data in
memory or in disk storage across them. Each application has its own executors.
- A `Job` is a parallel computation consisting of multiple tasks that gets spawned in response to a Spark action
- Each job gets divided into smaller sets of tasks, called `stages`, that depend on each other similar to the map and reduce stages in MapReduce.
- A `task unit` is a task of work  that will be sent to one executor.
- `Worker node` is node that can run an application code in the cluster.



