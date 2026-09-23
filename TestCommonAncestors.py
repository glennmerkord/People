#=======================
# testCommonAncestors.py
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
		
		match1 = people.find_person( search1)
		if len( match1) == 0:
			print( "\nPerson not found!")
			continue
		elif len( match1) > 1:
			print( "\nMultiple persons, be more specific!")
			continue
		else:
			break
		#end if
	#end while
	
#	print( "\nAncestors of", match1[0].name.fullname.replace("/","") + "\n")
#	for ancestor in match1[0].find_ancestors():
#		print( ancestor)
#	#end for
	
	while True:
		search2 = input( "\nPerson 2: ").lower()
		if search2 == "":
			sys.exit()
		#end if
		
		match2 = people.find_person( search2)
		if len( match2) == 0:
			print( "\nPerson not found!")
			continue
		elif len( match2) > 1:
			print( "\nMultiple persons, be more specific!")
			continue
		else:
			break
		#end if
	#end while
	
	common_ancestor_list = people._get_common_ancestor_list( match1[0], match2[0])
	if len( common_ancestor_list) == 0:
		print( "\nNo common ancestors!")
	else:
#		print( "\nCommon ancestors of " + match1[0].name.fullname.replace("/","") + " and " + match2[0].name.fullname.replace("/","") + "\n")
#		for ancestor in common_ancestor_list:
#			print( ancestor)
#		#end for
		pass
	#end if
	
	mrca_list = people._get_mrca_list( match1[0], match2[0])
	if len( mrca_list) == 0:
		print( "\nNo common ancestors!")
	else:
		print( "\nMost recent common ancestors of " + match1[0].name.fullname.replace("/","") + " and " + match2[0].name.fullname.replace("/","") + "\n")
		for mrca in mrca_list:
			print( mrca)
		#end for
		pass
	#end if
	
#end while

sys.exit()