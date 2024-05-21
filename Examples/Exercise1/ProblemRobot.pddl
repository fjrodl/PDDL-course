(define (problem trucksp0)
(:domain example_robotics)
   
(:objects
	garden laundryroom livingroom corridor office garage bathroom1 bathroom2 kitchen bedroom1 bedroom2 - location
	Leia - robot
)
 
(:init
    (link bathroom1 bedroom1)
	(link garden bedroom1)
	(link garden bedroom2)
	(link bedroom1 livingroom)
	(link corridor bedroom2 )
	(link corridor bathroom2 )
    (link corridor office )
    (link corridor garage )
    (link corridor livingroom )
    (link livingroom kitchen)

    (link  bedroom1 bathroom1)
	(link  bedroom1 garden)
	(link  bedroom2 garden)
	(link  livingroom bedroom1)
	(link  bedroom2 corridor)
	(link  bathroom2 corridor)
    (link  office corridor)
    (link  garage corridor)
    (link  livingroom corridor)
    (link  kitchen livingroom)


	(= (distance bathroom1 bedroom1) 5)
	(= (distance garden bedroom1 ) 15)
	(= (distance garden bedroom2 ) 15)
	(= (distance bedroom1 livingroom ) 20)
	(= (distance corridor bedroom2 ) 7)
	(= (distance corridor bathroom2 ) 10)
	(= (distance corridor office ) 15)
	(= (distance corridor garage ) 25)
	(= (distance corridor livingroom ) 20)
	(= (distance livingroom kitchen ) 20)
	
	
	(= (distance  bedroom1 bathroom1) 5)
	(= (distance  bedroom1 garden) 15)
	(= (distance  bedroom2 garden) 15)
	(= (distance  livingroom bedroom1) 20)
	(= (distance  bedroom2 corridor) 7)
	(= (distance  bathroom2 corridor) 10)
	(= (distance  office corridor) 15)
	(= (distance  garage corridor) 25)
	(= (distance  livingroom corridor) 20)
	(= (distance  kitchen livingroom) 20)
	
	;(refreshed Leia)
	; (trucking Leia)

	(= (speed Leia) 30)
	(= (distancetravelled Leia) 0)

	(at Leia bathroom1)
)

(:goal (and 
		(at Leia bedroom2)
	)
)
)