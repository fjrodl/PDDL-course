(define (problem test_same_room_goal)
  (:domain robot_transport)

  (:objects
    room1 - location
    box - object
  )

  (:init
    (robot_at room1)
    (object_at box room1)
    (hand_empty)
  )

  (:goal
    (and
      (object_at box room1)
    )
  )
)
