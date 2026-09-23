	#================
	# relationship.py
	#================
	
	import People
	
	def determine_relationship( common_ancestor: CommonAncestor):
		
		ancestor		= common_ancestor.ancestor.person
		person_a		= common_ancestor.person_a
		distance_a		= common_ancestor.distance_a
		path_a			= common_ancestor.path_a
		person_b		= common_ancestor.person_b
		distance_b		= common_ancestor.distance_b
		path_b			= common_ancestor.path_b
		
		#===================================================================
		# look at children of person_a and person_b (second element in path)
		# if father and mother of both children are the same
		# relationship is "f" (full), otherwise relationship is "h" (half)
		# if any parent is None, relationship is "u" (unknown)
		#===================================================================
		
		if distance_a > 0:
			child_a			= common_ancestor.path[1]		# child  of person_a
			father_a		= child_a.father				# father of child_a
			mother_a		= child_a.mother				# mother of child_a
		else:
			child_a			= None
			father_a		= None
			mother_a		= None
		#end if
		
		if distance_b > 0:
			child_b			= common_ancestor.path[1]		# child  of person_b
			father_b		= child_b.father				# father of child_b
			mother_b		= child_b.mother				# mother of child_b
		else:
			child_b			= None
			father_b		= None
			mother_b		= None
		#end if	
		
		half_status			= "u"
		if distance_a == 0 or distance_b == 0:
			half_status = "f"
		elif:
			if father_a != None & mother_a != None & father_b != None & mother_b != None
				if father_a != father_b and mother_a != mother_b:
					half_status = "h"
				#end if
			#end if
		#end if
		
		while True:
			if distance_a == 0:		# person a is direct ancestor of person b, no possibility of half relationship
				break
			elif distance_b == 0:	# person b is direct ancestor of person_a, no possibility of half relationship
				break
			elif distance_a == 1:	# person a is uncle/aunt, person b is nephew/niece, possible half relationship
				break
			elif distance_b == 1:	# person b is uncle/aunt, person a is nephew/niece, possible half relationship
				break
			#end if
		#end while
	#end def