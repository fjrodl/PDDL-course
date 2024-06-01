(define (domain execise0)
  (:requirements :strips :typing :negative-preconditions :disjunctive-preconditions :equality)
  (:types robot location object)
  (:predicates
    (at ?obj - (either robot object) ?loc - location)
    (holding ?r - robot ?obj - object))
  (:action move
    :parameters (?r - robot ?from - location ?to - location)
    :precondition (and (at ?r ?from) (not (= ?from ?to)))
    :effect (and (not (at ?r ?from)) (at ?r ?to)))
  (:action pick_up
    :parameters (?r - robot ?obj - object ?loc - location)
    :precondition (and (at ?r ?loc) (at ?obj ?loc))
    :effect (and (not (at ?obj ?loc)) (holding ?r ?obj)))
  (:action put_down
    :parameters (?r - robot ?obj - object ?loc - location)
    :precondition (holding ?r ?obj)
    :effect (and (not (holding ?r ?obj)) (at ?obj ?loc)))
  (:action visit
    :parameters (?r - robot ?loc1 - location ?loc2 - location)
    :precondition (or (at ?r ?loc1) (at ?r ?loc2))
    :effect (and (not (at ?r ?loc1)) (at ?r ?loc2)))
)
