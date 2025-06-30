(define (domain exercise0)
  (:requirements :strips :typing :negative-preconditions :disjunctive-preconditions :equality)

  (:types robot location object)

  (:predicates
    (at-robot ?r - robot ?loc - location)
    (at-object ?o - object ?loc - location)
    (holding ?r - robot ?o - object)
  )

  (:action move
    :parameters (?r - robot ?from - location ?to - location)
    :precondition (and (at-robot ?r ?from) (not (= ?from ?to)))
    :effect (and (not (at-robot ?r ?from)) (at-robot ?r ?to))
  )

  (:action pick_up
    :parameters (?r - robot ?o - object ?loc - location)
    :precondition (and (at-robot ?r ?loc) (at-object ?o ?loc))
    :effect (and (not (at-object ?o ?loc)) (holding ?r ?o))
  )

  (:action put_down
    :parameters (?r - robot ?o - object ?loc - location)
    :precondition (and (holding ?r ?o) (at-robot ?r ?loc))
    :effect (and (not (holding ?r ?o)) (at-object ?o ?loc))
  )
)