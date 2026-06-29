(define (problem waypoint_mission_problem)
  (:domain waypoint_mission)

  (:objects
    turtlebot - robot
    start wp1 wp2 wp3 wp4 wp5 - waypoint
  )

  (:init
    (robot_at turtlebot start)
    (visited start)

    (connected start wp1)
    (connected wp1 wp2)
    (connected wp2 wp3)
    (connected wp3 wp4)
    (connected wp4 wp5)

    (next start wp1)
    (next wp1 wp2)
    (next wp2 wp3)
    (next wp3 wp4)
    (next wp4 wp5)
  )

  (:goal
    (and
      (visited wp1)
      (visited wp2)
      (visited wp3)
      (visited wp4)
      (visited wp5)
      (robot_at turtlebot wp5)
    )
  )
)
