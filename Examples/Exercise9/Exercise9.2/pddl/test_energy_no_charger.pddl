(define (problem test_energy_no_charger)
  (:domain robot_transport_energy)

  (:objects
    room1 room_mid room2 - location
    box - object
  )

  (:init
    (robot_at room1)
    (object_at box room1)
    (connected room1 room_mid)
    (connected room_mid room1)
    (connected room_mid room2)
    (connected room2 room_mid)
    (battery_high)
    (hand_empty)
  )

  (:goal
    (and
      (object_at box room2)
    )
  )
)
