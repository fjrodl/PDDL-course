#Exercise 2

The "Rover" domain in the International Planning Competition (IPC) is a classic benchmark problem used to evaluate planners. This example involves a rover navigating a grid world to perform tasks while accounting for various constraints such as time and resource consumption. 


1. **Numeric**:
   - Numeric fluents are used to represent quantities or numerical values that change over time. In the context of the Rover domain, these could represent parameters such as energy levels, resource amounts, or distances traveled.

2. **Simple Time**:
   - Simple time is a basic form of temporal reasoning where actions are assumed to take constant time durations. This simplifies the modeling of actions' effects on the timeline.
   - It's called "simple" time because actions are assumed to have fixed durations, without the complexity of specifying variable or durative actions with flexible durations.

3. **STRIPS**:
   - STRIPS (Stanford Research Institute Problem Solver) is a classical planning formalism that represents states, actions, and goals using first-order logic.
   - In the Rover domain, STRIPS is used to define the states, actions, and preconditions/effects of actions.

4. **Time**:
   - Time constraints are incorporated into the planning domain, meaning actions must be executed within specified time bounds or deadlines.
   - The planner needs to consider the temporal aspects of actions and their effects when generating plans.


# Exercises

 1. Run Exercise2/SimpleTime STRover.pddl pfile1. First with popf and then with SMTPlan

 2. What are the differences when launching these exercises. Provide an answer based on metrics (number of actions, time of execution, etc)

 3. What is the main difference between pfile1 in Numeric and pfile1 in SimpleTime? And between domains?

 4. 



