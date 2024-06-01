# PDDL-course

ACM SIGSOFT Summer School for Software Engineering in Robotics


[Summer School  website](https://scivenia.com/en/event/summer-school-for-software-engineering-in-robotics_993)


## Exercises Block PDDL


### Exercise 0 

This basic exercise that shows how robots can be coordinated to move objects between locations, using actions with preconditions and effects to achieve a specified goal state

### Exercise 1

Classic example of a robot navigating between rooms.

The student needs to play between the cost of navigation in order to understand the effects on planner solutions.


### Exercise 2

Example extracted from IPC competition. It is possible to see the robot behavior in different contexts. The examples present approaches associated to a possible rover. 

Goal: to test all planners

### Exercise 3

Example of a PDDL domain and problem for a robot gripper for assembling blocks. 

Goal: to observe the sussan anomaly. 

Tools: popf vs vhpop


### Exercise 4: Complexity

Example of a PDDL domain and problem for a specific field, cybersecurty. Extracted from IPC 2012.

Goal: to observe the complexity associate to some specific domains. 


[References](https://github.com/potassco/pddl-instances/tree/master/ipc-2008/domains/cyber-security-sequential-satisficing-strips/domains)

### Exercise 5. 

In-depth view of durative actions in PDDL. It  allows the modeling of actions that take time to execute, with conditions and effects specified at different points in time. 


Goal: to follow a step by step example of durative actions. 


### Exercise 6. 

Using PlanSys 2 for interacting with PDDL and robot behaviors. 


Goal: get familiar with high level tools of interaction and integration of PDDL in practicasl robotics.  interaction with plansys cli and patrolling example. 


[Reference 1: PlanSys Web PAge](https://plansys2.github.io/build_instructions/index.html)
[Reference 2: Examples](https://github.com/PlanSys2/ros2_planning_system_examples/tree/humble)


### Exercise 7.

MERLIN 2. It is a cognitive architecture called MERLIN2 fully compatible with ROS 2. It provides a cognitive architecture framework that suits the hybrid architecture paradigm but it also includes generic architectural tools for managing symbolic knowledge and scheduling robot behaviors.


Goal: get familiar with alternative cognitive architecture. Particularly hybrid approaches

[Reference : Paper](https://www.softwareimpacts.com/article/S2665-9638(23)00014-3/fulltext)

[Reference : Paper](https://merlin2.readthedocs.io/en/latest/index.html)
