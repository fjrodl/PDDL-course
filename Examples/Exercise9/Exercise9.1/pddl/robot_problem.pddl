(define (problem robot_problem)
  (:domain robot_transport)

  (:objects
    room1 room2 - location
    box - object
  )

  (:init
    (robot_at room1)
    (object_at box room1)
    (connected room1 room2)
    (connected room2 room1)
    (hand_empty)
  )

  (:goal
    (and
      (object_at box room2)
    )
  )
)
