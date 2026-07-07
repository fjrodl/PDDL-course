# Exercise 7: ROS 2 Integration

Basic PDDL integration with ROS 2. This exercise introduces how to connect a PDDL planner (SMTPlan) with a ROS 2 robot simulator (tiago_simulator), including configuration, launching, and adapting solver paths.

**Goal:** Understand the basics of integrating PDDL planning with ROS 2 nodes and simulators.

## Requirements

- **tiago_simulator** — [Official URJC repository](https://github.com/jmguerreroh/tiago_simulator)
- SMTPlan binary (available in `Planners/`)

## Setup

### 1. Configure the Simulator

Check that the simulator is using the apartment as a world:

```bash
cd <tiago_simulator_path>/tiago_simulator/config
```

Edit the configuration to use the AWS house:

```yaml
tiago_simulator:
  world: aws_house
  robot_position:
    x: 0.0
    y: 0.0
    z: 0.0
    roll: 0.0
    pitch: 0.0
    yaw: 0.0
  tiago_arm: no-arm
```

### 2. Launch the Simulator

```bash
source /usr/share/gazebo/setup.bash

ros2 launch tiago_simulator simulation.launch.py
ros2 launch tiago_simulator navigation.launch.py
```

### 3. Configure the PDDL Node

Edit `src/my_pddl_package/my_pddl_package/basic_pddl_node.py` and adapt the paths:

```python
SOLVER_PATH = "<ROUTE_TO_YOUR_PLANNER>/SMTPlan"
PATH_PDDL_FILES = "<ROUTE_TO_YOUR_FOLDER_WITH_DOMAIN_AND_PROBLEM>"
DOMAIN_PDDL_FILE = "domain.pddl"
PROBLEM_PDDL_FILE = "problem.pddl"
```

### 4. Build and Run

```bash
colcon build
source install/setup.bash
ros2 run my_pddl_package basic_pddl_node.py
```

## Files

- `src/my_pddl_package/` — ROS 2 package with the PDDL planner node
  - `basic_pddl_node.py` — Main node calling SMTPlan and executing the plan
  - `domains_and_problems/` — PDDL domain and problem files
  - `waypoints/waypoints.yaml` — Waypoint configuration
