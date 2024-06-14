# Cognitive Architectures, Task Planning, and PDDL

ACM SIGSOFT Summer School for Software Engineering in Robotics


[Summer School  website](https://scivenia.com/en/event/summer-school-for-software-engineering-in-robotics_993)

# Table of Contents
1. [Examples](#introduction)
    1. [Exercise 1: Starting (I)](#exercise1)
    2. [Exercise 2: Starting (II)](#exercise2)
    3. [Exercise 3: Metrics in Planning](#exercise3)
    4. [Exercise 4: Comparing Planners (I)](#exercise4)
    5. [Exercise 5: Comparing Planners (II) ](#exercise5)
    6. [Exercise 6: Durative Actions](#exercise6)
    7. [Exercise 7: From 0 to hero (I): basic exercise](#exercise7)
    8. [Exercise 8: From 0 to hero (II): PlanSys2 and BT's](#exercise8)
    9. [Exercise 9: From 0 to hero (III): Merlin2 an Hybrid Cognitive Architecture (Planner + FSM-YASMIN) ](#exercise9) 
2. [General Questions](#questionnaire)
3. [Requirements and Traversal Tooling](#Requirements)
4. [Acknowledgments](#Acknowledgments)


## Examples - Task Planning with PDDL  <a name="introduction"></a>

The "Examples" folder contains a collection of exercises oriented towards learning PDDL (Planning Domain Definition Language) and other associated tools devoted to manage PDDL. These exercises are designed to reinforce the concepts covered in the lessons (check slides folder) and provide practical experience with PDDL and its applications. 


### Exercise 1 <a name="exercise1"></a>

This basic exercise that shows how robots can be coordinated to move objects between locations, using actions with preconditions and effects to achieve a specified goal state

### Exercise 2 <a name="exercise2"></a>

Classic example of a robot navigating between rooms.

The student needs to play adding links between locations in order to understand the effects on planner solutions. 


### Exercise 3 <a name="exercise3"></a>

Example extracted from IPC competition. It is possible to see the robot behavior in different contexts. The examples present approaches associated to a possible rover. 

Goal: to test all planners and to understand the concept "Metrics" in a problem file. 

### Exercise 4 <a name="exercise4"></a>

Example of a PDDL domain and problem for a robot gripper for assembling blocks. 

Goal: to observe the Sussman anomaly. 

Tools: popf vs vhpop


### Exercise 5: Complexity <a name="exercise5"></a>

Example of a PDDL domain and problem for a specific field, cybersecurty. Extracted from IPC 2012.

Goal: to observe the complexity associate to some specific domains. 


[References](https://github.com/potassco/pddl-instances/tree/master/ipc-2008/domains/cyber-security-sequential-satisficing-strips/domains)

### Exercise 6: From 0 to hero (I): basic exercise.  <a name="exercise6"></a>

In-depth view of durative actions in PDDL. It  allows the modeling of actions that take time to execute, with conditions and effects specified at different points in time. 


Goal: to follow a step by step example of durative actions. 

### Exercise 7: From 0 to hero (I): basic exercise.  <a name="exercise7"></a>

In-depth view of durative actions in PDDL. It  allows the modeling of actions that take time to execute, with conditions and effects specified at different points in time. 


Goal: to follow a step by step example of durative actions. 


###  Exercise 8: From 0 to hero (II): PlanSys2 and BT's <a name="exercise8"></a>

Using PlanSys 2 for interacting with PDDL and robot behaviors. 


Goal: get familiar with high level tools of interaction and integration of PDDL in practicasl robotics.  interaction with plansys cli and patrolling example. 
If you also want to test BT's with Plansys, the third official tutorial is for you. 


[Reference 1: PlanSys Web PAge](https://plansys2.github.io/build_instructions/index.html)
[Reference 2: Tutorials ](https://github.com/PlanSys2/ros2_planning_system_examples/tree/humble)

#### Extra: Generate documentation from huge source code projects using Doxygen

You can find instructions on the folder Exercise 6

### Exercise 9: From 0 to hero (III): Merlin2 an Hybrid Cognitive Architecture (Planner + FSM-YASMIN) <a name="exercise9"></a>

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

Install the script for the dependencies. 

You will find also:
- How to compile POPF
- How to install plansys from package
- How to install other robots such as turtlebot

Merlin docker:
- Double check in the repository how to install rocker (allows you to open the display locally instead of browser)
- 


## Acknowledgments <a name="Acknowledgments"></a>


### DMARCE Project

Decision Making in Autonomous Robots: Cybersecurity and Explainability (DMARCE).

![DMARCE_logo drawio](https://user-images.githubusercontent.com/3810011/192087445-9aa45366-1fec-41f5-a7c9-fa612901ecd9.png)


DMARCE (EDMAR+CASCAR) Project: EDMAR PID2021-126592OB-C21 -- CASCAR PID2021-126592OB-C22 funded by MCIN/AEI/10.13039/501100011033 and by ERDF A way of making Europe 

![DMARCE_EU eu_logo](https://raw.githubusercontent.com/DMARCE-PROJECT/DMARCE-PROJECT.github.io/main/logos/micin-uefeder-aei.png)

### SELF-AIR Project

Supporting Extensive Livestock Farming with the use of Autonomous Intelligent Robots 

<img src="https://raw.githubusercontent.com/shepherd-robot/.github/main/profile/robotics_wolf_minimal.png" alt= "SELF_AIR_logo" width="50%" height="50%">


Grant TED2021-132356B-I00 funded by MCIN/AEI/10.13039/501100011033 and by the “European Union NextGenerationEU/PRTR"

![SELF_AIR_EU eu_logo](https://raw.githubusercontent.com/shepherd-robot/.github/main/profile/micin-financiadoUEnextgeneration-prtr-aei.png)

