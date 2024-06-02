# PDDL-course

ACM SIGSOFT Summer School for Software Engineering in Robotics


[Summer School  website](https://scivenia.com/en/event/summer-school-for-software-engineering-in-robotics_993)

# Table of Contents
1. [Exercises](#introduction)
    1. [Exercise 0](#exercise0)
    2. [Exercise 1](#exercise1)
    3. [Exercise 2](#exercise2)
    4. [Exercise 3](#exercise3)
    5. [Exercise 4](#exercise4)
    6. [Exercise 5](#exercise5)
    7. [Exercise 6](#exercise6)
    8. [Exercise 7](#exercise7)
2. [General Questions](#questionnaire)
3. [Requirements](#Requirements)
4. [Acknowledgments](#Acknowledgments)


## Exercises - Task Planning with PDDL  <a name="introduction"></a>



### Exercise 0 <a name="exercise0"></a>

This basic exercise that shows how robots can be coordinated to move objects between locations, using actions with preconditions and effects to achieve a specified goal state

### Exercise 1 <a name="exercise1"></a>

Classic example of a robot navigating between rooms.

The student needs to play between the cost of navigation in order to understand the effects on planner solutions.


### Exercise 2 <a name="exercise2"></a>

Example extracted from IPC competition. It is possible to see the robot behavior in different contexts. The examples present approaches associated to a possible rover. 

Goal: to test all planners

### Exercise 3 <a name="exercise3"></a>

Example of a PDDL domain and problem for a robot gripper for assembling blocks. 

Goal: to observe the sussan anomaly. 

Tools: popf vs vhpop


### Exercise 4: Complexity <a name="exercise4"></a>

Example of a PDDL domain and problem for a specific field, cybersecurty. Extracted from IPC 2012.

Goal: to observe the complexity associate to some specific domains. 


[References](https://github.com/potassco/pddl-instances/tree/master/ipc-2008/domains/cyber-security-sequential-satisficing-strips/domains)

### Exercise 5.  <a name="exercise5"></a>

In-depth view of durative actions in PDDL. It  allows the modeling of actions that take time to execute, with conditions and effects specified at different points in time. 


Goal: to follow a step by step example of durative actions. 


### Exercise 6. <a name="exercise6"></a>

Using PlanSys 2 for interacting with PDDL and robot behaviors. 


Goal: get familiar with high level tools of interaction and integration of PDDL in practicasl robotics.  interaction with plansys cli and patrolling example. 


[Reference 1: PlanSys Web PAge](https://plansys2.github.io/build_instructions/index.html)
[Reference 2: Examples](https://github.com/PlanSys2/ros2_planning_system_examples/tree/humble)


### Exercise 7. <a name="exercise7"></a>

MERLIN 2. It is a cognitive architecture called MERLIN2 fully compatible with ROS 2. It provides a cognitive architecture framework that suits the hybrid architecture paradigm but it also includes generic architectural tools for managing symbolic knowledge and scheduling robot behaviors.


Goal: get familiar with alternative cognitive architecture. Particularly hybrid approaches

[Reference : Paper](https://www.softwareimpacts.com/article/S2665-9638(23)00014-3/fulltext)

[Reference : Read The Doc](https://merlin2.readthedocs.io/en/latest/index.html)

[Reference : Installation](https://merlin2.readthedocs.io/en/latest/Installation.html)

[Reference : Docker](https://github.com/MERLIN2-ARCH/merlin2_docker)

## General Questions <a name="questionnaire"></a>

These questions can help you grasping the key concepts presented during the session and encourage you to think critically about robot coordination, planning, and execution.

1. **Understanding Preconditions and Effects**:
   - Explain the role of preconditions and effects in robot actions.
   - How do preconditions ensure the proper execution of an action?

2. **Action Execution**:
   - Describe the sequence of actions required for a robot to move an object from one location to another.
   - What happens if the preconditions for an action are not met?

3. **Coordination and Planning**:
   - How do multiple robots coordinate their actions to avoid conflicts?
   - Discuss how the planner decides the order of actions to achieve the goal state.

4. **Error Handling and Recovery**:
   - What should happen if a robot encounters an unexpected obstacle while moving?
   - How can the system recover from an action failure?

5. **Efficiency and Optimization**:
   - How can you optimize the actions to minimize the time or energy spent in moving objects?
   - What strategies can be used to handle multiple goals simultaneously?

6. **Domain and Problem Definition**:
   - Explain the difference between a domain and a problem in PDDL.
   - How would you modify the domain to include a new type of action or object?

7. **Practical Application**:
   - Provide an example of a real-world scenario where such a robot coordination system could be used.
   - What are some potential challenges in implementing this system in the real world?

8. **Advanced Topics**:
   - Discuss the use of numeric fluents in planning.
   - How do durative actions differ from instantaneous actions, and when would you use them?

## Requirements <a name="Requirements"></a>

Install the next script for the dependencies

## Acknowledgments <a name="Acknowledgments"></a>