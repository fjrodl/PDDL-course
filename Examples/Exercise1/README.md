# Exercise 

This PDDL domain definition models a scenario where robots can move between locations, keep track of the distance they have traveled, and visit charging stations to get reloaded. The domain includes both instantaneous and durative actions to handle different aspects of robot navigation and recharging.


### Explanation

1. **Domain Definition**:
   - **Requirements**: 
     - `:typing`: Allows the use of types in the domain definition.
     - `:fluents`: Allows the use of numeric fluents, which can change over time.
     - `:durative-actions`: Allows the definition of actions that take time to execute.
     - `:duration-inequalities`: Allows the use of inequalities in specifying the duration of actions.
     - `:negative-preconditions`: Allows the use of negative conditions in action preconditions.
   - **Types**: Defines two types: `robot` and `location`.
   - **Predicates**:
     - `(at ?x - robot ?y - location)`: Indicates that a robot is at a specific location.
     - `(navigating ?x - robot ?y ?z - location)`: Indicates that a robot is navigating from one location to another.
     - `(loaded ?v - robot)`: Indicates that a robot is loaded (possibly with energy or cargo).
     - `(link ?x ?y - location)`: Indicates that a link exists between two locations.
   - **Functions**:
     - `(distanceTravelled ?v - robot)`: The total distance the robot has traveled from the origin.
     - `(distance ?x ?y - location)`: The distance between two locations.
     - `(speed ?v - robot)`: The speed of the robot while navigating.
   - **Actions**:
     - **Durative Action** `drive`: A robot drives from one location to another.
       - **Parameters**: `?v` (robot), `?a` (starting location), `?b` (destination location).
       - **Duration**: Unconstrained duration (up to 10,000 units of time).
       - **Condition**: 
         - At the start: The robot is at the starting location and a link exists between the two locations.
         - Over the duration: The robot is navigating from the start to the destination location.
       - **Effect**: 
         - At the start: The distance traveled by the robot is reset to 0.
         - During the action: The distance traveled by the robot increases based on its speed.
         - At the start: The robot starts navigating from the start to the destination location and is no longer at the starting location.
     - **Action** `arrive`: A robot arrives at the destination location.
       - **Parameters**: `?v` (robot), `?a` (starting location), `?b` (destination location).
       - **Precondition**: 
         - The distance traveled by the robot is at least the distance between the two locations.
         - The robot is navigating from the start to the destination location.
       - **Effect**: 
         - The robot is no longer navigating.
         - The robot is now at the destination location.
     - **Action** `visitChargingStation`: A robot visits a charging station to get loaded.
       - **Parameters**: `?v` (robot).
       - **Precondition**: 
         - The distance traveled by the robot is between 10 and 20 units.
         - The robot is not already loaded.
       - **Effect**: The robot becomes loaded.


## Exercises

 1. What happen when you remove part of your links between locations?

 2. What happen if you play with distances?

 ## Execution


  $ popf DomainRobot.pddl ProblemRobot.pddl

