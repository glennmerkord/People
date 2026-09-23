#=======================
# TestMRCAs.py
#=======================

import sys

import People

if len(sys.argv) < 2:
	print( "\nPlease enter a GEDCOM file name on the command line!")
	sys.exit()
#end if

file_name = sys.argv[1]

try:
	file = open( file_name, 'r', encoding='utf-8')
except:
	print( "\nThere was a problem opening file", file_name)
	sys.exit()
#end if

people	= People.People()

if not people.import_GEDCOM( file):
	print( "\nThere was a problem reading file", file_name)
	sys.exit()
#end if
		
#people._echo()

all_people = people.find_person( "everyone")
	
while True:
#	print()
#	for person in all_people:
#		print( person.name.fullname)
#	#end for
#	print()
	
	while True:
		search1 = input( "\nPerson 1: ").lower()
		if (search1 == ""):
			sys.exit()
		#end if
		
		person_a = people.find_person( search1)
		if len( person_a) == 0:
			print( "\nPerson not found!")
			continue
		elif len( person_a) > 1:
			print( "\nMultiple persons, be more specific!")
			continue
		else:
			break
		#end if
	#end while
	
#	print( "\nAncestors of", person_a[0].name.fullname.replace("/","") + "\n")
#	for ancestor in person_a[0].find_ancestors():
#		print( ancestor)
#	#end for
	
	while True:
		search2 = input( "\nPerson 2: ").lower()
		if search2 == "":
			sys.exit()
		#end if
		
		person_b = people.find_person( search2)
		if len( person_b) == 0:
			print( "\nPerson not found!")
			continue
		elif len( person_b) > 1:
			print( "\nMultiple persons, be more specific!")
			continue
		else:
			break
		#end if
	#end while
	
	mrca_relationships_list = people.get_mrca_relationships_list( person_a[0], person_b[0])
	
	for mrca_relationships in mrca_relationships_list:
		
		print( mrca_relationships.a_to_b_relationship_verbose)
		print( mrca_relationships.b_to_a_relationship_verbose)
		
	#end for
	
#end while

sys.exit()