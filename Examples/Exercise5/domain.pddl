(define 
  (domain robot-world)
  (:requirements :strips :typing :durative-actions :equality)
  (:types robot location object)
  (:predicates
    (at ?obj - (either robot object) ?loc - location)
    (holding ?r - robot ?obj - object))
  
  (:durative-action move
    :parameters (?r - robot ?from - location ?to - location)
    :duration (= ?duration 10)
    :condition (and (at start (at ?r ?from)) (over all (not (= ?from ?to))))
    :effect (and (at start (not (at ?r ?from)))
                 (at end (at ?r ?to))))

  (:durative-action pick_up
    :parameters (?r - robot ?obj - object ?loc - location)
    :duration (= ?duration 2)
    :condition (and (at start (at ?r ?loc)) (at start (at ?obj ?loc)))
    :effect (and (at start (not (at ?obj ?loc))) (at end (holding ?r ?obj))))

  (:durative-action put_down
    :parameters (?r - robot ?obj - object ?loc - location)
    :duration (= ?duration 3)
    :condition (at start (holding ?r ?obj))
    :effect (and (at start (not (holding ?r ?obj))) (at end (at ?obj ?loc))))
)
