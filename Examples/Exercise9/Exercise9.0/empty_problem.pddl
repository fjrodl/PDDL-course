(define (problem empty)
  (:domain robot)

  (:objects
    robot1 - robot
    kitchen - room
  )

  (:init
    (robot_at robot1 kitchen)
  )

  (:goal
    (robot_at robot1 kitchen)
  )
)