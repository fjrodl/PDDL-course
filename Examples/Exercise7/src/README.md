# Basics


This package should be used just for teaching reasons. **PLEASE USE PLANSYS 2 instead for real projects**,  


### Basic Example - PDDL 

Requeriments:

It is necessary to run tiago_simulator

[Official URJC repository](https://github.com/jmguerreroh/tiago_simulator)


#### Launching procedure

 Check that the simulator is using the apartment as a world. 

``$ cd <it_will_be_somewhere>/tiago_simulator/config``

Change for the AWS house if it is different

```tiago_simulator:
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


Running the simulator :

```
$ source  /usr/share/gazebo/setup.bash (remember to source gazebo for avoiding issues)

$ ros2 launch tiago_simulator simulation.launch.py

$ ros2 launch tiago_simulator navigation.launch.py
```


#### Launching this package

1. Use STMPlan for solving the problem included in this example. ADapt routes in the *basic_pddl_node.py*. You should create a ROS 2 launch and adapt the parameters

```
SOLVER_PATH = "<ROUTE_TO_YOUR_PLANNER>/SMTPlan"
PATH_PDDL_FILES = "ROUTE TO YOUR FOLDER WITH DOMAIN AND SOLVER"
DOMAIN_PDDL_FILE = "domain.pddl"
PROBLEM_PDDL_FILE = "problem.pddl"
``` 
2. Compile with colcon

```
$ colcon build

$ source install/setup.bash
```


3. Running 

```
$ ros2 run my_pddl_example basic_pddl_node.py
