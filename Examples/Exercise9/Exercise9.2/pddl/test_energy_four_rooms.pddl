(define (problem test_energy_four_rooms)
  (:domain robot_transport_energy)

  (:objects
    room1 room2 room3 room4 - location
    box - object
  )

  (:init
    (robot_at room1)
    (object_at box room1)
    (connected room1 room2)
    (connected room2 room1)
    (connected room2 room3)
    (connected room3 room2)
    (connected room3 room4)
    (connected room4 room3)
    (charger_at room2)
    (charger_at room3)
    (battery_high)
    (hand_empty)
  )

  (:goal
    (and
      (object_at box room4)
    )
  )
)
