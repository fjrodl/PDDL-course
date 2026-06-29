(define (problem test_two_objects)
  (:domain robot_transport)

  (:objects
    room1 room2 - location
    box1 box2 - object
  )

  (:init
    (robot_at room1)
    (object_at box1 room1)
    (object_at box2 room1)
    (connected room1 room2)
    (connected room2 room1)
    (hand_empty)
  )

  (:goal
    (and
      (object_at box1 room2)
      (object_at box2 room2)
    )
  )
)
