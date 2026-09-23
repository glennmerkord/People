#==================
# TestFindPeople.py
#==================

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

while True:
	
	search_string = input( "\nEnter search terms: ").lower()
	if search_string == "":
		break
	#end if
	search_terms = search_string.lower().split()

	matches = people.find_person( search_terms)
	if len( matches) == 0:
		print( "\nNo matches!")
	else:
		print( "")
		for person in matches:
			print( person.name.fullname)
		#end for
	#end if
	
	if len( matches) == 1:
		ancestor_map = People.build_ancestor_map( matches[0])
		People.print_ancestor_map( ancestor_map)
	
#end while

sys.exit()