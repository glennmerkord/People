import sys

import shlex

import People

while True:
	
	while True:
		string = input( "\nEnter first person name (in quotes), sex, and distance: ")
		if string == "":
			sys.exit()
		#end if
		
		parts = shlex.split( string)
		if len( parts) == 3:
			(name_a, sex_a, str_a) = parts
			try:
				distance_a = int( str_a)
			except ValueError:
				print( "\nDistance must be an integer!")
			else:
				if sex_a == "m" or sex_a == "f":
					break
				else:
					print( "\nSex must be \"m\" or \"f\" !")
				#end if
			#end try
		else:
			print( "\nNot enough or too many values!")
		#end if
	#end while
	
	while True:
		string = input( "\nEnter second person name (in quotes), sex, and distance: ")
		if string == "":
			sys.exit()
		#end if
		
		parts = shlex.split( string)
		if len( parts) == 3:
			( name_b, sex_b, str_b) = parts
			try:
				distance_b = int( str_b)
			except ValueError:
				print( "\nDistance must be an integer!")
			else:
				if sex_b == "m" or sex_b == "f":
					break
				else:
					print( "\nSex must be \"m\" or \"f\" !")
				#end if
			#end try
		else:
			print( "\nNot enough or too many values!")
		#end if  
	#end while
	
	People._print_standard_relationship_descriptions( name_a, sex_a, distance_a, name_b, sex_b, distance_b, "f")
	
	
#end while