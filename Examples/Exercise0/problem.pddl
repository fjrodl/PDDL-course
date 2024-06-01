(define (problem exercise0-problem-robot)
  (:domain exercise0)
  
  (:objects
    robot1 robot2 - robot
    loc1 loc2 loc3 - location
    box1 box2 - object)

  (:init
    (at robot1 loc1)
    (at robot2 loc2)
    (at box1 loc1)
    (at box2 loc3))

  (:goal
    (and
      (at robot1 loc2)
      (at box1 loc2)
      (at box2 loc1)))
)
