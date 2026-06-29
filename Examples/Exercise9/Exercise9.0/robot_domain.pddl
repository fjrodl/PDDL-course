(define (domain robot)

  (:requirements :strips :typing)

  (:types
    robot room object
  )

  (:predicates
    (robot_at ?r - robot ?rm - room)
    (object_at ?o - object ?rm - room)
    (gripper_empty ?r - robot)
    (holding ?r - robot ?o - object)
  )

  (:action move
    :parameters (?r - robot ?from - room ?to - room)
    :precondition
      (robot_at ?r ?from)
    :effect
      (and
        (not (robot_at ?r ?from))
        (robot_at ?r ?to)
      )
  )

  (:action pick
    :parameters (?r - robot ?o - object ?rm - room)
    :precondition
      (and
        (robot_at ?r ?rm)
        (object_at ?o ?rm)
        (gripper_empty ?r)
      )
    :effect
      (and
        (holding ?r ?o)
        (not (object_at ?o ?rm))
        (not (gripper_empty ?r))
      )
  )

  (:action place
    :parameters (?r - robot ?o - object ?rm - room)
    :precondition
      (and
        (robot_at ?r ?rm)
        (holding ?r ?o)
      )
    :effect
      (and
        (object_at ?o ?rm)
        (gripper_empty ?r)
        (not (holding ?r ?o))
      )
  )

)