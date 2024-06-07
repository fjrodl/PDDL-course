(define (domain example_robotics)
(:requirements :typing :fluents :durative-actions :duration-inequalities :negative-preconditions)
(:types robot location)
(:predicates
	(at ?x - robot ?y - location)
	(navigating ?x - robot ?y ?z - location) ; Robot is navigating from ?y to ?z
	(loaded ?v - robot) ; Is the robot loaded 
	(link ?x ?y - location) ; link exists between two locations
)

(:functions
	(distanceTravelled ?v - robot) ; The total distance the robot traveled from the origin
	(distance ?x ?y - location) ; Distance between two locations
	(speed ?v - robot) ; Speed while navigating on a regular link
)

(:durative-action drive
	:parameters (?v - robot ?a ?b - location)
	:duration (<= ?duration 10000) ; this is basically un-constrained duration. The planner will decide when to stop navigating.
	:condition (and
		(at start (at ?v?a))
		(at start (link ?a ?b))
		(over all (navigating ?v ?a ?b))
	)
	:effect (and
		(at start (assign (distanceTravelled ?v) 0))
		(increase (distanceTravelled ?v) (* #t (speed ?v)))
		(at start (navigating ?v ?a ?b)) (at start (not (at ?v ?a)))
	)
)

(:action arrive
	:parameters (?v - robot ?a ?b - location)
	:precondition (and
		(>= (distanceTravelled ?v) (distance ?a ?b))
		(navigating ?v ?a ?b))
	:effect (and
		(not (navigating ?v ?a ?b))
		(at ?v ?b)
	)
)

(:action visitChargingStation ; robot needs refreshing...
	:parameters (?v - robot)
	:precondition (and
		(>= (distanceTravelled ?v) 10)
		(<= (distanceTravelled ?v) 20)
		(not (loaded ?v))
	)
	:effect
		(loaded ?v)
	)
)

