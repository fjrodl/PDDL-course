(define (problem robot-task)
  (:domain robot-world)
  (:objects
    robot1 - robot
    loc1 loc2 loc3 - location
    box1 - object)
  (:init
    (at robot1 loc1)
    (at box1 loc1))
  (:goal
    (and (at box1 loc3) (at robot1 loc3)))
)
