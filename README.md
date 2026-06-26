# Cognitive Architectures, Task Planning, and PDDL

> **ACM SIGSOFT Summer School for Software Engineering in Robotics**

| Edition | Year | Location | Link |
|:-------:|:----:|:--------:|------|
| I | 2024 | Brussels | [Summer School Website](https://scivenia.com/en/event/summer-school-for-software-engineering-in-robotics_993) |
| II | 2025 | Delft | [Summer School Website](https://scivenia.com/en/event/acm-sigsoft-summer-school-for-software-engineering-in-robotic) |
| III | 2026 | TBA | [Summer School Website](https://www.scivenia.com/en/event/summer-school-for-software-engineering-in-robotics-III) |

---

## Table of Contents

- [Cognitive Architectures, Task Planning, and PDDL](#cognitive-architectures-task-planning-and-pddl)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
    - [Course Structure](#course-structure)
  - [Exercises](#exercises)
    - [Exercise 1: Basic Planning](#exercise-1-basic-planning)
    - [Exercise 2: Navigation \& Fluents](#exercise-2-navigation--fluents)
    - [Exercise 3: Metrics in Planning](#exercise-3-metrics-in-planning)
    - [Exercise 4: Comparing Planners](#exercise-4-comparing-planners)
    - [Exercise 5: Cybersecurity \& Complexity](#exercise-5-cybersecurity--complexity)
    - [Exercise 6: Durative Actions](#exercise-6-durative-actions)
    - [Exercise 7: ROS 2 Integration](#exercise-7-ros-2-integration)
    - [Exercise 8: PlanSys2 \& Behavior Trees](#exercise-8-plansys2--behavior-trees)
  - [General Questions](#general-questions)
    - [Understanding Preconditions and Effects](#understanding-preconditions-and-effects)
    - [Action Execution](#action-execution)
    - [Coordination and Planning](#coordination-and-planning)
    - [Error Handling and Recovery](#error-handling-and-recovery)
    - [Efficiency and Optimization](#efficiency-and-optimization)
    - [Domain and Problem Definition](#domain-and-problem-definition)
    - [Practical Application](#practical-application)
    - [Advanced Topics](#advanced-topics)
  - [Requirements \& Setup](#requirements--setup)
    - [Installing Dependencies](#installing-dependencies)
    - [Merlin Docker](#merlin-docker)
  - [Acknowledgments](#acknowledgments)
    - [AURORAS Project](#auroras-project)
    - [DMARCE Project](#dmarce-project)
    - [SELF-AIR Project](#self-air-project)

---

## Overview

This course covers **task planning** for autonomous robots using the **Planning Domain Definition Language (PDDL)**. You will learn how to:

- Model robotic domains and problems in PDDL
- Use different planners (FF, POPF, VHPOP, SMTPlan) and compare their behavior
- Understand planning concepts: STRIPS, ADL, durative actions, metrics, and the Sussman anomaly
- Integrate PDDL planning with **ROS 2** using PlanSys2 and Behavior Trees

### Course Structure

| Component | Description |
|-----------|-------------|
| **Slides/** | Lecture slides covering PDDL fundamentals, planning algorithms, and robotics integration |
| **Examples/** | Hands-on exercises from basic STRIPS planning to full ROS 2 integration |
| **Planners/** | Pre-compiled planners (FF, POPF, VHPOP, SMTPlan) ready to use |
| **Scripts/** | Helper scripts for installation and setup |
| **Images/** | Course figures and diagrams |

---

## Exercises

The `Examples/` directory contains eight exercises that progressively introduce PDDL concepts and tools. Each exercise includes a `README.md` with detailed instructions and suggested experiments.

| # | Exercise | Topic | Difficulty | Key Concepts |
|:-:|----------|-------|:----------:|--------------|
| 1 | [Basic Planning](Examples/Exercise1/) | Robot coordination | ⭐ | STRIPS, ADL, types, predicates, planner compatibility |
| 2 | [Navigation & Fluents](Examples/Exercise2/) | Robot navigation | ⭐ | Numeric fluents, durative actions, charging |
| 3 | [Metrics in Planning](Examples/Exercise3/) | IPC Rover benchmark | ⭐⭐ | Plan metrics, planner comparison |
| 4 | [Comparing Planners](Examples/Exercise4/) | Sussman anomaly | ⭐⭐ | POPF vs VHPOP, timing analysis |
| 5 | [Cybersecurity](Examples/Exercise5/) | IPC 2012 domain | ⭐⭐ | Domain-specific complexity |
| 6 | [Durative Actions](Examples/Exercise6/) | Temporal planning | ⭐⭐ | PDDL2.1, step-by-step walkthrough |
| 7 | [ROS 2 Integration](Examples/Exercise7/) | SMTPlan + ROS 2 | ⭐⭐⭐ | tiago_simulator, action performers |
| 8 | [PlanSys2 & BTs](Examples/Exercise8/) | PlanSys2 framework | ⭐⭐⭐ | Behavior trees, Doxygen documentation |

---

### Exercise 1: Basic Planning

This introductory exercise demonstrates how robots can be coordinated to move objects between locations. You will explore actions with preconditions and effects, and observe how different planners handle STRIPS vs ADL features.

**Goal:** Understand the basics of PDDL domains, problems, and planner compatibility.

---

### Exercise 2: Navigation & Fluents

Classic robot navigation between rooms. You will modify the connectivity graph between locations and observe how these changes affect planner solutions.

**Goal:** Understand how topology and numeric fluents influence planning outcomes.

---

### Exercise 3: Metrics in Planning

Example extracted from the IPC competition Rover domain. You will test multiple planners and observe how plan metrics affect the generated solutions.

**Goal:** Understand the concept of metrics in PDDL problem files and compare planner behavior.

---

### Exercise 4: Comparing Planners

PDDL domain and problem for a robot gripper assembling blocks. This exercise demonstrates the **Sussman anomaly** — a classic planning challenge where subgoals interfere with each other.

**Goal:** Observe the Sussman anomaly and compare POPF vs VHPOP planner behavior.

---

### Exercise 5: Cybersecurity & Complexity

Domain extracted from IPC 2012, modeling a cybersecurity scenario. This exercise shows how planning complexity varies across domains.

**Goal:** Understand how domain-specific characteristics affect planning complexity.

**Reference:** [IPC 2008 Cybersecurity Domain](https://github.com/potassco/pddl-instances/tree/master/ipc-2008/domains/cyber-security-sequential-satisficing-strips/domains)

---

### Exercise 6: Durative Actions

In-depth exploration of durative actions in PDDL2.1. Durative actions model operations that take time, with conditions and effects specified at different time points (`at start`, `at end`, `over all`).

**Goal:** Follow a step-by-step example of temporal planning with durative actions.

---

### Exercise 7: ROS 2 Integration

Basic PDDL integration with ROS 2. This exercise introduces how to connect a PDDL planner (SMTPlan) with a ROS 2 robot simulator (tiago_simulator), including configuration, launching, and adapting solver paths.

**Goal:** Understand the basics of integrating PDDL planning with ROS 2 nodes and simulators.

---

### Exercise 8: PlanSys2 & Behavior Trees

Advanced exercise using PlanSys2 for interacting with PDDL and robot behaviors. You will work with the PlanSys2 CLI and explore the patrolling example. The exercise also covers Behavior Tree integration and Doxygen documentation generation.

**Goal:** Get familiar with high-level tools for PDDL integration in practical robotics.

**References:**
- [PlanSys2 Build Instructions](https://plansys2.github.io/build_instructions/index.html)
- [PlanSys2 Tutorials](https://github.com/PlanSys2/ros2_planning_system_examples/tree/humble)

---

## General Questions

These questions reinforce the key concepts presented during the session and encourage critical thinking about robot coordination, planning, and execution.

### Understanding Preconditions and Effects
1. Explain the role of preconditions and effects in robot actions.
2. How do preconditions ensure the proper execution of an action?

### Action Execution
3. Describe the sequence of actions required for a robot to move an object from one location to another.
4. What happens if the preconditions for an action are not met?

### Coordination and Planning
5. How do multiple robots coordinate their actions to avoid conflicts?
6. Discuss how the planner decides the order of actions to achieve the goal state.

### Error Handling and Recovery
7. What should happen if a robot encounters an unexpected obstacle while moving?
8. How can the system recover from an action failure?

### Efficiency and Optimization
9. How can you optimize actions to minimize the time or energy spent in moving objects?
10. What strategies can be used to handle multiple goals simultaneously?

### Domain and Problem Definition
11. Explain the difference between a domain and a problem in PDDL.
12. How would you modify the domain to include a new type of action or object?

### Practical Application
13. Provide an example of a real-world scenario where such a robot coordination system could be used.
14. What are some potential challenges in implementing this system in the real world?

### Advanced Topics
15. Discuss the use of numeric fluents in planning.
16. How do durative actions differ from instantaneous actions, and when would you use them?

---

## Requirements & Setup

### Installing Dependencies

Run the setup script to install the required dependencies:

```bash
./Scripts/setup.sh
```

The script handles:
- Compiling POPF from source
- Installing PlanSys2 from package
- Setting up additional robot simulators (e.g., TurtleBot)

### Merlin Docker

For the Merlin-based exercises:

1. Install **rocker** (allows you to open the display locally instead of in a browser):
   ```bash
   # Follow the installation instructions in the repository
   ```

2. Launch the Merlin container following the instructions in `Examples/Exercise7/`.

---

## Acknowledgments


### AURORAS Project

**Advanced Autonomy for Robots Applied to the Primary Sector (AURORAS)**

![AURORAS Logo](https://project-auroras.github.io/auroras/logos/tituloblanco.png)

Grant AURORAS are PERMAP PID2024-161761OB-C21 and PLANNAV PID2024-161761OB-C22 funded by MICIU/AEI/10.13039/501100011033 and by ERDF/EU. 

![EU Funding Logo](https://raw.githubusercontent.com/DMARCE-PROJECT/DMARCE-PROJECT.github.io/main/logos/micin-uefeder-aei.png)

---


### DMARCE Project

**Decision Making in Autonomous Robots: Cybersecurity and Explainability**

![DMARCE Logo](https://user-images.githubusercontent.com/3810011/192087445-9aa45366-1fec-41f5-a7c9-fa612901ecd9.png)

EDMAR PID2021-126592OB-C21 & CASCAR PID2021-126592OB-C22 funded by MCIN/AEI/10.13039/501100011033 and by ERDF A way of making Europe.

![EU Funding Logo](https://raw.githubusercontent.com/DMARCE-PROJECT/DMARCE-PROJECT.github.io/main/logos/micin-uefeder-aei.png)

---

### SELF-AIR Project

**Supporting Extensive Livestock Farming with the use of Autonomous Intelligent Robots**

<img src="https://raw.githubusercontent.com/shepherd-robot/.github/main/profile/robotics_wolf_minimal.png" alt="SELF-AIR Logo" width="50%">

Grant TED2021-132356B-I00 funded by MCIN/AEI/10.13039/501100011033 and by the "European Union NextGenerationEU/PRTR".

![EU NextGeneration Logo](https://raw.githubusercontent.com/shepherd-robot/.github/main/profile/micin-financiadoUEnextgeneration-prtr-aei.png)
