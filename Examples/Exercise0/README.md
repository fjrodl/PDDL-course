# Basic 
This basic exercise  shows how robots can be coordinated to move objects between locations, using actions with preconditions and effects to achieve a specified goal state


## Explanation

###   Domain Definition:
        Requirements:
            :strips: Standard requirement for basic planning.
            :typing: Allows the use of types in the domain definition.
            :negative-preconditions: Allows the use of negative conditions in action preconditions.
            :disjunctive-preconditions: Allows the use of disjunctions (logical OR) in action preconditions.
            :equality: Allows the use of equality and inequality in conditions.
        Types: Defines three types: robot, location, and object.
        Predicates:
            (at ?obj - (either robot object) ?loc - location): Indicates that a robot or object is at a specific location.
            (holding ?r - robot ?obj - object): Indicates that a robot is holding an object.
        Actions:
            move: A robot moves from one location to another.
                Parameters: ?r (robot), ?from (starting location), ?to (destination location).
                Precondition: The robot is at the starting location, and the starting and destination locations are different.
                Effect: The robot is no longer at the starting location and is now at the destination.
            pick_up: A robot picks up an object.
                Parameters: ?r (robot), ?obj (object), ?loc (location).
                Precondition: The robot and the object are at the same location.
                Effect: The object is no longer at the location and the robot is holding the object.
            put_down: A robot puts down an object.
                Parameters: ?r (robot), ?obj (object), ?loc (location).
                Precondition: The robot is holding the object.
                Effect: The robot is no longer holding the object and the object is at the location.
            visit: A robot visits one of two locations.
                Parameters: ?r (robot), ?loc1 (first location), ?loc2 (second location).
                Precondition: The robot is at either of the two locations.
                Effect: The robot is no longer at the first location and is now at the second location.

###    Problem Definition:
        Objects: Defines two robots (robot1, robot2), three locations (loc1, loc2, loc3), and two objects (box1, box2).
        Initial State:
            robot1 is at loc1.
            robot2 is at loc2.
            box1 is at loc1.
            box2 is at loc3.
        Goal State:
            robot1 should be at loc2.
            box1 should be at loc2.
            box2 should be at loc1.

## Execution

    ../../Planners/ff -o domain.pddl -f problem.pddl

    ../../Planners/SMTPlan domain.pddl problem.pddl

#### Planner issues  
$ pdddl  domain.pddl  problem.pddl 

    Constructing lookup tables: [10%] [20%] [30%] [40%] [50%] [60%] [70%]A problem has been encountered, and the planner has to terminate.
    -----------------------------------------------------------------
    Unfortunately, at present, the planner does not fully support ADL
    unless in the rules for derived predicates.  Only two aspects of
    ADL can be used in action definitions:
    - forall conditions, containing a simple conjunct of propositional and
    numeric facts;
    - Conditional (when... ) effects, and then only with numeric conditions
    and numeric consequences on values which do not appear in the
    preconditions of actions.

    To use this planner with your problem, you will have to reformulate it to
    avoid ADL.  Alternatively, if you have a particularly compelling case
    for them, please contact the authors to discuss it with them, who may be able to
    extend the planner to meet your needs.


