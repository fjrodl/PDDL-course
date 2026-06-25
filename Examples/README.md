# PDDL Exercises

This directory contains a collection of exercises for learning PDDL (Planning Domain Definition Language) and related tools. Each exercise builds on the previous ones, progressing from basic concepts to advanced robotics integration.

| Exercise | Topic | Description |
|----------|-------|-------------|
| [Exercise 1](Exercise1/) | Basic Planning | Robot coordination with STRIPS and ADL features |
| [Exercise 2](Exercise2/) | Navigation & Fluents | Robot navigation with numeric fluents and durative actions |
| [Exercise 3](Exercise3/) | Metrics in Planning | IPC Rover benchmark — comparing planners with metrics |
| [Exercise 4](Exercise4/) | Comparing Planners | Sussman anomaly and planner behavior analysis |
| [Exercise 5](Exercise5/) | Cybersecurity | IPC 2012 cybersecurity domain and complexity |
| [Exercise 6](Exercise6/) | Durative Actions | Step-by-step temporal planning with PDDL2.1 |
| [Exercise 7](Exercise7/) | ROS 2 Integration | Connecting PDDL planners with ROS 2 simulators |
| [Exercise 8](Exercise8/) | PlanSys2 & BTs | PlanSys2 framework and behavior trees |

## Running the Exercises

Most exercises can be run using the planners provided in the `Planners/` directory:

```bash
# Example with POPF
../../Planners/popf domain.pddl problem.pddl

# Example with SMTPlan
../../Planners/SMTPlan domain.pddl problem.pddl
```

See each exercise's README for specific instructions and suggested experiments.
