(define (domain waypoint_mission)
  (:requirements :strips :typing :durative-actions)

  (:types robot waypoint)

  (:predicates
    (robot_at ?r - robot ?w - waypoint)
    (connected ?from ?to - waypoint)
    (next ?from ?to - waypoint)
    (visited ?w - waypoint)
  )

  (:durative-action navigate
    :parameters (?r - robot ?from ?to - waypoint)
    :duration (= ?duration 1)
    :condition (and
      (at start (robot_at ?r ?from))
      (at start (connected ?from ?to))
      (at start (next ?from ?to))
    )
    :effect (and
      (at start (not (robot_at ?r ?from)))
      (at end (robot_at ?r ?to))
      (at end (visited ?to))
    )
  )
)
