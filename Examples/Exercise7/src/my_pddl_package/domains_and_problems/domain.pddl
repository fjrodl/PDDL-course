(define (domain actionplanner4pathgenerator)	       
	(:requirements :strips :negative-preconditions :disjunctive-preconditions) 
	; popf does not allow disjunctive-preconditions  https://planning.wiki/ref/planners/popf
	; you should use Exercise 2 for an option with popf
	(:constants robot)

	(:predicates (location ?waypoint_x);it defines the locations (waypoints)
				(at ?local_robot ?waypoint_x);Is your local robot in waypoint x
				(connect ?waypoint_x ?waypoint_y); Are your waypoints connected
				)

	(:action go-to
		:parameters (?waypoint_x ?waypoint_y)
		:precondition (and (location ?waypoint_x) (location ?waypoint_y) (or (connect ?waypoint_x ?waypoint_y) (connect ?waypoint_y ?waypoint_x)) (at robot ?waypoint_x))
		:effect (and (at robot ?waypoint_y) (not (at robot ?waypoint_x))))
	)

