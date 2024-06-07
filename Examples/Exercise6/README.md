# Durative Actions

Durative actions in PDDL allow for the modeling of actions that take time to execute, with conditions and effects specified at different points in time. This enables more realistic and complex planning scenarios, particularly in domains where the timing and duration of actions are critical. By defining the duration, conditions, and effects of actions, planners can generate plans that respect temporal constraints and ensure the successful achievement of goals.


## Step by Step

Durative actions are actions that have a duration, meaning they take time to execute. In contrast to instantaneous actions, durative actions are particularly useful in temporal planning, where the timing and duration of actions are important. PDDL2.1 introduced the concept of durative actions to handle such scenarios.
Key Concepts of Durative Actions in PDDL

    Duration: Specifies how long the action takes.
    Conditions: Conditions that must hold at specific times during the action's execution (e.g., at the start, end, or throughout the action).
    Effects: Changes to the state that occur at specific times during the action's execution.

### Syntax of Durative Actions in PDDL

Durative actions are defined using the :durative-action keyword. The definition includes parameters, duration, conditions, and effects.




#### Breakdown of Durative Actions
move Action

    Parameters: ?r - robot ?from - location ?to - location
    Duration: = ?duration 5
        The action takes 5 time units to complete.
    Condition:
        at start (at ?r ?from): The robot must be at the starting location at the beginning of the action.
        over all (not (= ?from ?to)): Throughout the action's duration, the starting location and the destination must be different.
    Effect:
        at start (not (at ?r ?from)): At the start of the action, the robot is no longer at the starting location.
        at end (at ?r ?to): At the end of the action, the robot is at the destination location.

pick_up Action

    Parameters: ?r - robot ?obj - object ?loc - location
    Duration: = ?duration 2
        The action takes 2 time units to complete.
    Condition:
        at start (at ?r ?loc): The robot must be at the location at the beginning of the action.
        at start (at ?obj ?loc): The object must be at the location at the beginning of the action.
    Effect:
        at start (not (at ?obj ?loc)): At the start of the action, the object is no longer at the location.
        at end (holding ?r ?obj): At the end of the action, the robot is holding the object.

put_down Action

    Parameters: ?r - robot ?obj - object ?loc - location
    Duration: = ?duration 2
        The action takes 2 time units to complete.
    Condition:
        at start (holding ?r ?obj): The robot must be holding the object at the beginning of the action.
    Effect:
        at start (not (holding ?r ?obj)): At the start of the action, the robot is no longer holding the object.
        at end (at ?obj ?loc): At the end of the action, the object is at the location.

#### Temporal Planning with Durative Actions

In temporal planning, actions overlap in time, and their interactions must be carefully managed. Planners that handle durative actions use advanced scheduling techniques to ensure that all conditions and constraints are satisfied throughout the execution timeline.

### Explanation

Explanation

    Domain Definition:
        Types: There are three types: robot, location, and object.
        Predicates:
            `(at ?obj - (either robot object) ?loc - location)`: Indicates that an object (either a robot or a generic object) is at a certain location.
            `(holding ?r - robot ?obj - object)`: Indicates that a robot is holding an object.
        Durative Actions:
            `move`: Represents a robot moving from one location to another. It takes 5 time units and has conditions and effects at the start and end of the action.
            `pick_up`: Represents a robot picking up an object. It takes 2 time units and has conditions and effects at the start and end of the action.
            `put_down`: Represents a robot putting down an object. It takes 2 time units and has conditions and effects at the start and end of the action.

    Problem Definition:
        `Objects`: There is one robot (robot1), three locations (loc1, loc2, loc3), and one object (box1).
        `Initial State`: The robot and the box are both at loc1.
        `Goal State`: The box should be at loc3, and the robot should also end up at loc3.

### Test

You can test it with 
 ./SMTPlan

 ./popf 
