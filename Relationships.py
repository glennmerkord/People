#==========
# People.py
#==========

import fileinput

import traceback

from GEDCOM import GEDCOM_File

from Date   import Date

class Name:				pass
	# instance attribute fullname	: str
	# instance attribute givenname	: str
	# instance attribute surname	: str
	#
	# dunder method __init__( self: Name):
	
class Person:			pass
	
	# instance attribute id					: str			unique person identifier
	# instance attribute name				: Name			person's name
	# instance attribute sex				: str			person's sex: "m", "f", or "u"
	# instance attribute birth_date			: Date			person's birthdate
	# instance attribute birth_place		: str			person's birthplace
	# instance attribute deathDate			: Date			person's deathdate
	# instance attribute death_place		: str			person's deathplace
	# instance attribute father				: Person		person's father: may be None
	# instance attribute mother				: Person		person's mother: may be None
	# instance attribute child_of_family	: Family		family this person is a child of: may be None
	# instance attribute family_list		: [Family]		list of families this person is a spouse of: may be None
	#
	# dunder  method __init__			( self: Person):
	# dunder  method __eq__				( self: Person, other: Person) -> bool:
	# dunder  method __hash__			( self: Person):
	# dunder  method __repr__			( self: Person):
	#
	# private method _walk				( self: Person, ancestor_list:[Ancestor], person: Person, distance: int, path: [Person], visited: (bool)):
	# private method _is_ancestor_of	( self: Person, other: Person) -> bool:
	#
	# public  method find_ancestors		( self: Person) -> [Ancestor]:
	
class Family:			pass
	# instance attribute id					: str				family identifier
	# instance attribute husband			: Person			husband of family
	# instance attribute wife				: Person			wife    of family
	# instance attribute marriage_date		: str				marriage date
	# instance attribute marriage_place		: str				marriage place
	# instance attribute child_dictionary	: dict[Person]		children in family indexed by person identifier (pid)
	# instance attribute child_list			: list[Person]		children in family sorted  by birth date	
	
	# method __init__( self: Family):
	
	# dunder method __eq__  ( self: Family, other: Family) ->	 bool:
	# dunder method __hash__( self: Family):
	# dunder method __repr__( self: Family):
	
class People:			pass
	# instance attribute person_dictionary: {Person}		all persons
	# instance attribute family_dictionary: {Family}		all families
	
	# dunder  method __init__						( self: People):
	
	# private method _echo							( self: People) -> bool:
	# private method _person_by_id					( self: People, person_id: str):
	# private method _family_by_id					( self: People, family_id: str):
	# private method_find_distance_and_path 		( self: People, person_a: Person, person_b: Person)  -> [CommonAncestor]:
	# private method _get_common_ancestor_list		( self: People, person_a: Person, person_b: Person)  -> [CommonAncestor]:
	# private method _get_mrca_list					( self: People, person_a: Person, person_b: Person)  -> [CommonAncestor]:
	
	# public  method import_GEDCOM					( self: People, file):
	# public  method find_person					( self: People, search_terms: str) -> [Person]:
	# public  method get_mrca_relationships_list	( self: People, person_a: Person, person_b: Person) -> [Relationships]:

class Ancestor:			pass

	# class attribute visited: set( bool)
	
	# instance attribute person		: Person			ancestor
	# instance attribute distance	: int				number of hops from ancestor to person
	# instance attribute path		: [Person]			path from ancestor to person
	
	# dunder method __init__( self: Ancestor, person: Person, distance: int, path: [Person]):
	# dunder method __eq__  ( self: Ancestor, other: Ancestor) -> bool:
	# dunder method __hash__( self: Ancestor):
	# dunder method __repr__( self: Ancestor):
	
class CommonAncestor:	pass
	# instance attribute person			: Person		common ancestor
	# instance attribute spouse			: Person		spouse of ancestor if also a common ancestor
	# instance attribute person_a		: Person		first person
	# instance attribute distance_a		: int			number of hops from ancestor to 1st person
	# instance attribute path_a			: [Person]		path from ancestor to 1st person
	# instance attribute person_b		: Person		second person
	# instance attribute distance_b		: int			number of hops from ancestor to 2nd person
	# instance attribute path_b			: [Person]		path from ancestor to 2nd person
	
	# dunder method __init__						( self: CommonAncestor, ancestor: Person, person_a: Person, path_a: [Person], distance_a: int, person_b: Person, path_b: [Person], distance_b: int):
	# dunder method __eq__							( self: CommonAncestor, other: CommonAncestor) ->  bool:
	# dunder method __hash__						( self: CommonAncestor):
	
	# private method _get_mrca_relationships_list	( self: CommonAncestor) -> [Relationships]:
	
# module functions

#	_get_standard_relationship_name( sex_a: str, distance_a: int, sex_b: str, distance_b: int) -> (str, str)
#	_massage_relationship( sex: str, relationship: str) -> str

class Relationships:	pass

#==================
# public class Name
#==================

class Name():
	
	def __init__( self: Name):
		self.fullname: str	= ""
		self.givenname: str	= ""
		self.surname: str	= ""
	#end def
	
#end class

#====================
# public class Person
#====================

class Person():
	
	count = 0
	
	def __init__( self: Person):
		
		Person.count		+= 1
		
		self.id	: str						= ""		#  person identifier
		self.name: Name						= Name()
		self.sex: str						= ""
		self.birth_date: Date				= None
		self.birth_place: str				= ""
		self.deathDate: Date				= None
		self.death_place: str				= ""
		self.father	: Person				= None
		self.mother	: Person				= None
		self.child_of_family: Family		= None		# family this person is a child of
		self.family_list: [Family]			= []		# list of families this person is a spouse of
	
	def __eq__( self: Person, other: Person):
		return self.id == other.id
	#end def
	
	def __hash__( self: Person):
		return hash( self.id)
	#end def
	
	def __repr__( self: Person):
		return self.name.fullname
	#end def

	def find_ancestors( self: Person) -> [Ancestor]:
		
		#============================================================
		# Returns a list of ancestors
		#
		# Each entry contains:
		#
		# person      Person object (an ancestor)
		# distance    number of generations above starting person
		# paths       list of shortest paths from ancestor to person
		#
		# The starting person is included with distance 0
		#===========================================================
		
		#============================================
		# walk recursively through person's ancestors
		#============================================
		
		ancestors = []
		
		self._walk( ancestors, self, distance=0, path=[], visited=set())
		
		return ancestors
		
	#end def

	#========================================
	# Is person an ancestor of another person
	#========================================

	def _is_ancestor_of( person: Person, other_person: Person) -> bool:
		
		if person == other_person:
			return False
		# end if
		
		ancestor_list: [Ancestor] = other_person.find_ancestors()
		
		for possible_ancestor in ancestor_list:
			if possible_ancestor.person == person:
				return True
			#end if
		#end if
		
		return False
		
	#end def

	def _walk( self, ancestor_list, person: Person, distance: int, path: [Person], visited: (bool)):
		
		if person is None:
			return
		#end if
		
		#================================
		# Prevent loops cause by bad data
		#================================
		
		if person in visited:
			return
		#end if
		
		visited.add( person)
		
		#==================================================
		# Path is stored ancestor -> ... -> starting person
		#==================================================
		
		ancestor_path = [person] + path	
		
		found = None
		for ancestor in ancestor_list:
			if person.id == ancestor.person.id:
				found = ancestor
				break
			#end if
		#end for
		
		if not found:
		
			#====================================
			# First time we've seen this ancestor
			#====================================
			
			ancestor = Ancestor( person, distance, ancestor_path)
			ancestor_list.append( ancestor)
			
		else:
			
			#===============
			# Not first time
			#===============

			if distance < ancestor.distance:
				
				#=====================
				# Found a shorter path
				#=====================
			
				ancestor.distance = distance
				ancestor.path = [ancestor_path]
				
			elif distance == ancestor.distance:
				
				#===========================
				# Found an even shorter path
				#===========================
				
				ancestor.path.append(ancestor_path)
			#end if
			
		#end if
		
		self._walk( ancestor_list, person.father, distance + 1, ancestor_path, visited)
		self._walk( ancestor_list, person.mother, distance + 1, ancestor_path, visited)
		
	#end def
	
#end class

#====================
# public class Family
#====================

class Family():
	
	count: int = 0
	
	def __init__( self: Family):
		
		Family.count			+= 1
		
		self.id	: str							= ""		# family identifier
		self.husband: Person					= None
		self.wife: Person						= None
		self.marriage_date:str					= None
		self.marriage_place	: str				= ""
		self.child_dictionary: dict[Person]		= {}		# children in family indexed by person identifier (pid)
		self.child_list: list[Person]			= []		# children in family sorted by birth date
		
	#end def
	
	def __eq__( self: Family, other: Family):
		return self.id == other.id
	#end def
	
	def __hash__( self: Family):
		return hash( self.id)
	#end def
	
	def __repr__( self: Family):
		return self.id + " " + self.husband.name.fullname + " " + self.wife.name.fullname
	#end def
	
#end class
	
#====================
# public class People
#====================

class People():
	
	def __init__( self: People):
		self.person_dictionary	= {}
		self.family_dictionary	= {}
	#end def
	
	def import_GEDCOM( self: People, file):
		
		person_dictionary		= self.person_dictionary
		family_dictionary		= self.family_dictionary
		
		GEDCOM_file = GEDCOM_File()
		if not GEDCOM_file.import_GEDCOM( file):
			return False
		#end if
		
		for INDI_id, INDI_record in GEDCOM_file.INDI_records.items():
			
			#=================================================
			# Create Person and Family instances, if necessary
			#=================================================
			
			FAMC_id = INDI_record.FAMC_id
			if FAMC_id == "":
				HUSB_id			= ""
				WIFE_id			= ""
			else:
				FAM_record		= GEDCOM_file.FAM_records[FAMC_id]
				HUSB_id			= FAM_record.HUSB_id
				WIFE_id			= FAM_record.WIFE_id
			#end if
			
			person			= self._person_by_id( INDI_id)
			family			= self._family_by_id( FAMC_id)
			father			= self._person_by_id( HUSB_id)
			mother			= self._person_by_id( WIFE_id)
			
			#=======================
			# Populate Person fields
			#=======================
			
			person.name.fullname		= INDI_record.NAME
			person.name.givenname		= INDI_record.GIVN
			person.name.surname			= INDI_record.SURN
			person.sex					= INDI_record.SEX
			person.birthDate			= INDI_record.BIRT_DATE
			person.birth_date			= Date( INDI_record.BIRT_DATE)
			person.birth_place			= INDI_record.BIRT_PLAC
			person.death_date			= INDI_record.DEAT_DATE
			person.deathDate			= Date( INDI_record.DEAT_DATE)
			person.death_place			= INDI_record.DEAT_PLAC
			person.father				= father
			person.mother				= mother
			person.child_of_family		= family
			for FAMS_id in INDI_record.FAMS_ids:
				family = self._family_by_id( FAMS_id)
				if person.sex == "M":
					family.husband	= person
				else:
					family.wife		= person
				#end if
				person.family_list.append( family)
			#end for
			
		#end for
		
		for FAM_id, FAM_record in GEDCOM_file.FAM_records.items():
			HUSB_id = FAM_record.HUSB_id
			WIFE_id = FAM_record.WIFE_id
			
			#=================================================
			# create Family and Person instances, if necessary
			#=================================================
			
			family		= self._family_by_id( FAM_id)
			husband		= self._person_by_id( HUSB_id)
			wife		= self._person_by_id( WIFE_id)
			child_list	= []
			for CHIL_id in FAM_record.CHIL_ids:
				child_list.append( self._person_by_id( CHIL_id))
			#end for
			
			#=======================
			# Populate Family fields
			#=======================
			
			family.husband						= husband
			family.wife							= wife
			person.marriage_date				= Date( FAM_record.MARR_DATE)
			family.marriage_place				= FAM_record.MARR_PLAC
			for child in child_list:
				family.child_dictionary[child.id]	= child
				family.child_list.append( child)
			#end for
		#end for
		
		#============================
		# sort children by birth_date
		#============================
		
		for family_id, family in self.family_dictionary.items():
			family.child_list.sort(key = lambda child: child.birth_date.end_date_integer)
		#end for
		
		print( "\nPeople import successful:", len( self.person_dictionary), "persons", len( self.family_dictionary), "families")
		
		return True
		
	#end def
	
	def find_person( self: People, search_terms: str) -> [Person]:
		
		candidates: [Person] = []
		
		if len( search_terms) < 1:
			return candidates
		#end if
		
		if search_terms == "everyone":
			for id, person in self.person_dictionary.items():
				candidates.append( person)
			#end for
			return candidates
		#end if
		
		for id, person in self.person_dictionary.items():
			name_and_date = str(person.name.fullname + " " + person.birth_date.date_string_original).lower()
			match = True
			for term in search_terms.split():
				if term not in name_and_date:
					match = False
					break
				#end if
			#end for
			if match:
				candidates.append( person)
			#end if
		#end for
		
		return candidates
		
	#end def
	
	def _echo( self: People):
		
		echo_individuals	= False
		echo_families		= False
		
		if echo_individuals:
			print( "\n")
			for person_id, person in self.person_dict.items():
				print( "Person", person.id, "\"" + person.name.fullname + "\"", "\"" + person.birth_date.date_string_original + "\"", "\"" + person.deathDate.date_string_original + "\"")
				if len( person.family_list) > 0:
					family = person.family_list[0]
				#end if
				for family in person.family_list:
					if person.sex == "M":
						spouse = family.wife
					else:
						spouse = family.husband
					#end if
					print( "   Family", family.id)
					if spouse == None:
						print( "      Spouse None")
					else:
						print( "      Spouse", spouse.id, "\"" + spouse.name.fullname + "\"", "\"" + spouse.birth_date.date_string_original + "\"", "\"" + spouse.deathDate.date_string_original + "\"")
					#end if
					for child in family.child_list:
						print( "         Child", child.id, "\"" + child.name.fullname + "\"", "\"" + child.birth_date.date_string_original + "\"", "\"" + child.deathDate.date_string_original + "\"")
					#end for
				#end for
		#end if
		
		if echo_families:
			print( "\n")
			for family_id, family in self.family_dict.items():
				print( "Family", family.id)
				
				if family.husband == None:
					print( "   Husband None")
				else:
					print( "   Husband", family.husband.id, "\"" + family.husband.name.fullname + "\"", "\"" + family.husband.birth_date.date_string_original + "\"", "\"" + family.husband.deathDate.date_string_original + "\"")
				#end if
				
				if family.wife == None:
					print( "   Wife None")
				else:
					print( "   Wife", family.wife.id, "\"" + family.wife.name.fullname + "\"", "\"" + family.wife.birth_date.date_string_original + "\"", "\"" + family.wife.deathDate.date_string_original + "\"")
				#end if
				
				for child in family.child_list:
					print( "      Child", child.id, "\"" + child.name.fullname + "\"", "\"" + child.birth_date.date_string_original + "\"", "\"" + child.deathDate.date_string_original + "\"")
				#end if
		#end if	
		
	#end def
	
	def _person_by_id( self: People, person_id: str):
		
		if person_id == "":
			return None
		#end if
		
		if person_id in self.person_dictionary.keys():
			return self.person_dictionary[person_id]
		#end if
		
		person								= Person()
		person.id							= person_id
		self.person_dictionary[person_id]	= person
		
		return person
		
	#end def
	
	def _family_by_id( people: People, family_id: str):
		
		if family_id == "":
			return None
		#end if
		
		if family_id in people.family_dictionary.keys():
			family = people.family_dictionary[family_id]
			return family
		#end if
		
		family								= Family()
		family.id							= family_id
		people.family_dictionary[family_id]	= family
		
		return family
		
	#end def
	
	def _get_common_ancestor_list( self: People, person_a: Person, person_b: Person) -> [CommonAncestor]:
		
		ancestors_of_a_list: list[Ancestor] = person_a.find_ancestors()
		ancestors_of_b_list: list[Ancestor] = person_b.find_ancestors()
		
		set_a: set[Ancestor] = set( ancestors_of_a_list)
		set_b: set[Ancestor] = set( ancestors_of_b_list)
		
		common_ancestor_list: list[CommonAncestor] = []
		
		common_ancestor_set: set[Ancestor] = set_a.intersection( set_b)
		
		for ancestor in common_ancestor_set:
			
			(distance_a, path_a) = self._find_distance_and_path( ancestor, ancestors_of_a_list, person_a)
			(distance_b, path_b) = self._find_distance_and_path( ancestor, ancestors_of_b_list, person_b)
			
			common_ancestor = CommonAncestor( ancestor, person_a, distance_a, path_a, person_b, distance_b, path_b)
			
			common_ancestor_list.append( common_ancestor)
			
		#end if
		
		return common_ancestor_list
		
	#end def
	
	def _find_distance_and_path( self, ancestor, ancestor_list, person):
		for person in ancestor_list:
			if person.person.id == ancestor.person.id:
				return (person.distance, person.path)
			#end if
		#end for
	#end def
	
#================================================================
# Find most recent common ancestors in a list of common ancestors
#================================================================
	
	def _get_mrca_list( self: People, person_a: Person, person_b: Person) -> [CommonAncestor]:
		
		#================================
		# First find all common ancestors
		#================================
		
		common_ancestor_list: [CommonAncestor] = self._get_common_ancestor_list( person_a, person_b)
		
		#===========================================================================
		# Eliminate common ancestors that are ancestors of any other common ancestor
		#===========================================================================
		
		mrca_list: [CommonAncestor] = []
		
		for candidate_ancestor in common_ancestor_list:
			candidate_is_mrca = True
			
			#=========================================================
			# For each candidate ancestor, see if it is an ancestor of
			# any other common ancestor. If so, it is not a mrca.
			#=========================================================
			
			for other_common_ancestor in common_ancestor_list:
				if other_common_ancestor.ancestor == candidate_ancestor.ancestor:
					continue
				#end if
				if candidate_ancestor.ancestor.person._is_ancestor_of( other_common_ancestor.ancestor.person):
					candidate_is_mrca = False
					break
				#end if
			#end for
			

			if candidate_is_mrca:
				ancestor	= candidate_ancestor.ancestor
				person_a	= candidate_ancestor.person_a
				distance_a	= candidate_ancestor.distance_a
				path_a		= candidate_ancestor.path_a
				person_b	= candidate_ancestor.person_b
				distance_b	= candidate_ancestor.distance_b
				path_b		= candidate_ancestor.path_b
				
				mrca = CommonAncestor( ancestor, person_a, distance_a, path_a, person_b, distance_b, path_b)
				
				mrca_list.append(mrca)
			#end if
			
		#end for
		
		return mrca_list
		
	#end def
	
	def get_mrca_relationships_list( self: People, person_a: Person, person_b: Person) -> [Relationships]:
	
		Ancestor.visited = set()
		
		mrca_relationships_list = []
	
		mrca_list = self._get_mrca_list( person_a, person_b)
		
		for mrca in mrca_list:
			
			#====================================================================
			# if mrca has not already been processed as a spouse of another mrca,
			# determine mrca relationships and append to list
			#====================================================================
			
			if not mrca.ancestor.person in Ancestor.visited:
				mrca_relationships_list.append( mrca._get_mrca_relationships())
			#end if
		#end for
		
		return mrca_relationships_list
		
	#end def
	
#end class

class Ancestor():
	
	visited = None
	
	def __init__( self: Ancestor, person: Person, distance: int, path: [Person]):
		self.person: Person			= person			#ancester
		self.distance: int			= distance			#distance from ancestor to person
		self.path: [Person]			= path				#path from ancestor to person
	#end def
	
	def __eq__( self: Ancestor, other: Ancestor):
		return self.person.id == other.person.id
	#end def
	
	def __hash__( self: Ancestor):
		return hash( self.person.id)
	#end def
	
	def __repr__( self: Ancestor):
		repr = self.person.name.fullname.replace("/","")
		repr = repr + " " + str(self.distance) + " "
		joined_path = " -> ".join(person.name.fullname.replace("/","") for person in self.path)
		repr = repr + "[" + joined_path + "]"
		return repr
	#end if
	
#end class

class CommonAncestor():
	def __init__(self: CommonAncestor, ancestor: Person, person_a: Person, path_a: [Person], distance_a: int, person_b: Person, path_b: [Person], distance_b: int):
		
		self.ancestor: Person		= ancestor
		self.person_a: Person		= person_a
		self.path_a: [Person]		= path_a
		self.distance_a: int		= distance_a
		self.person_b: Person		= person_b
		self.path_b: [Person]		= path_b
		self.distance_b	: int		= distance_b
		
	#end def
	
	def __eq__( self: CommonAncestor, other: CommonAncestor):

		if self.ancestor.id != other.ancestor.id:
			return False
		elif self.person_a.id != other.person_a.id:
			return False
		elif self.person_b.id != other.person_b.id:
			return False
		else:
			return True
		#end if
	#end def
	
	def __hash__( self: CommonAncestor):
		return hash( self.ancestor.id + self.person_a.id + self.person_b.id)
	#end def
	
	def __repr__( self: CommonAncestor):
		repr_a = self.person_a.name.fullname.replace("/","")
		repr_a = repr_a + " " + str(self.distance_a) + " "
		joined_path_a = " -> ".join(person.name.fullname.replace("/","") for person in self.path_a)
		repr_a = repr_a + "[" + joined_path_a + "]"
		
		repr_b = self.person_b.name.fullname.replace("/","")
		repr_b = repr_b + " " + str(self.distance_b) + " "
		joined_path_b = " -> ".join(person.name.fullname.replace("/","") for person in self.path_b)
		repr_b = repr_b + "[" + joined_path_b + "]"
		
		repr = self.ancestor.person.name.fullname.replace("/","") + " " + repr_a + "\n" + self.ancestor.person.name.fullname.replace("/","") + " " + repr_b
	
		return repr
	#end if
	
	def _get_mrca_relationships( common_ancestor: CommonAncestor) -> Relationships:
		
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
			child_a			= common_ancestor.path_a[1]		# child  of person_a
			father_a		= child_a.father				# father of child_a
			mother_a		= child_a.mother				# mother of child_a
		else:
			child_a			= None
			father_a		= None
			mother_a		= None
		#end if
		
		if distance_b > 0:
			child_b			= common_ancestor.path_b[1]		# child  of person_b
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
		else:
			if father_a is not None and mother_a is not None and father_b is not None and mother_b is not None:
				if father_a == father_b and mother_a == mother_b:
					half_status = "f"
				else:
					half_status = "h" 
				#end if
			#end if
		#end if
		
		#============================================================================
		# if half status is full, spouse of common ancestor is also a common ancestor
		# add spouse to set of common ancestors already processed
		#============================================================================
		
		if half_status == "f":
			Ancestor.visited.add( father_a)
			Ancestor.visited.add( mother_a)
			Ancestor.visited.add( father_b)
			Ancestor.visited.add( mother_b)
		#end if
		
		name_a	= person_a.name.fullname
		sex_a	= person_a.sex.lower()
		
		name_b	= person_b.name.fullname
		sex_b	= person_b.sex.lower()
		
		relationship_a_to_b = _get_standard_relationship_name( sex_a, distance_a, sex_b, distance_b)
		relationship_b_to_a = _get_standard_relationship_name( sex_b, distance_b, sex_a, distance_a)
		
		massaged_relationship_a_to_b = _massage_relationship( sex_b, relationship_a_to_b)
		massaged_relationship_b_to_a = _massage_relationship( sex_b, relationship_b_to_a)
		
		verbose_a_to_b	= f"\n{name_b} is {name_a}'s {massaged_relationship_a_to_b}"
		verbose_b_to_a	= f"\n{name_a} is {name_b}'s {massaged_relationship_b_to_a}" 
		
		relationships = Relationships( common_ancestor)
		
		relationships.person_a						: Person	= person_a
		relationships.person_b						: Person	= person_b
		relationships.male_mrca						: Person	= father_a
		relationships.female_mrca					: Person	= mother_b
		relationships.half_status					: str		= half_status
		
		relationships.a_to_b_relationship			: str		= relationship_a_to_b
		relationships.b_to_a_relationship			: str		= relationship_b_to_a
		
		relationships.a_to_b_relationship_verbose	: str		= verbose_a_to_b
		relationships.b_to_a_relationship_verbose	: str		= verbose_b_to_a
		
		return relationships
	#end def
	
#end class

class Relationships():
	
	visited = None		# used in full relationship situations to prevent redundant relationships
	
	def __init__(self: Relationships, common_ancestor: CommonAncestor):
		
		self.person_a						: Person		= None
		self.person_b						: Person		= None
		self.male_mrca						: Person		= None			# male   most recent common ancestor, possibly None if half relationship
		self.female_mrca					: Person		= None			# female most recent common ancestor, possibly None if half relationship
		self.half_status					: str			= "u"			#"f" (ful), "h" (half, or "u" (unknown)
		self.a_and_b_relationship			: str			= ""			# person a and person b are ...
		self.a_to_b_relationship			: str			= ""			# person b is person a's ...
		self.b_to_a_relationship			: str			= ""			# person a is person b's ...
		self.a_and_b_relationship_verbose	: str			= ""			# person a and person b are ...
		self.a_to_b_relationship_verbose	: str			= ""			# person b is person a's ...
		self.b_to_a_relationship_verbose	: str			= ""			# person a is person b's ...
		self.relationship_verbose			: str			= ""			# all three relationships
		
	#end def
	
	def __eq__( self: CommonAncestor, other: CommonAncestor):
		if self.person_a.id != other.person_a.id:
			return False
		elif self.person_b.id != other.person_b.id:
			return False
		elif self.male_mrca.id != other.male_mrca.id:
			return False
		elif self.female_mrca.id != other.female_mrca.id:
			return False
		else:
			return True
		#end if
	#end def
	
	def __hash__( self: CommonAncestor):
		return hash( self.person_a.id + self.person_b.id + self.male_mrca.id + self.female_mrca.id)
	#end def
	
#end class

_standard_relationship_names = {
	  0:  ( "self",								"SELF"   ),
	  1:  ( "son/daughter",						"S/D"    ),
	  2:  ( "grandson/daughter",				"GS/D"   ),
	  3:  ( "great-grandson/daughter",			"GGS/D"  ),
	  4:  ( "2nd great--grandson/daughter",		"2GGS/D" ),
	  5:  ( "3rd great-grandson/daughter",		"3GGS/D "),
	  6:  ( "4th great-grandson/daughter",		"4GGS/D" ),
	  7:  ( "5th great-grandson/daughter",		"5GGS/D" ),
	  8:  ( "6th great-grandson/daughter",		"6GGS/D" ),
	  9:  ( "7th great-grandson/daughter",		"7GGS/D" ),
	  10: ( "8th great-grandson/daughter",		"8GGS/D" ),
	  11: ( "9th great-grandson/daughter",		"9GGS/D" ),
	  12: ( "10th great-grandson/daughter",		"10GGS/D"),
	 100: ( "father/mother",					"F/M"    ),	
	 200: ( "grandfather/mother",				"GF/M"   ),
	 300: ( "great-grandfather/mother",			"GGF/M"  ),
	 400: ( "2nd great-grandfather/mother",		"2GGF/M" ),
	 500: ( "3rd great-grandfather/mother",		"3GGF/M" ),
	 600: ( "4th great-grandfather/mother",		"4GGF/M" ),
	 700: ( "5th great-grandfather/mother",		"5GGF/M" ),
	 800: ( "6th great-grandfather/mother",		"6GGF/M" ),
	 900: ( "7th great-grandfather/mother",		"7GGF/M" ),
	1000: ( "8th great-grandfather/mother",		"8GGF/M" ),
	1100: ( "9th great-grandfather/mother",		"9GGF/M" ),
	1200: ( "10th great-grandfather/mother",	"10GGF/M"),
	 101: ( "brother/sister",					"B/S"    ),	
	 102: ( "nephew/niece",						"N/N"    ),
	 103: ( "great-nephew/niece",				"GN/N"   ),
	 104: ( "2nd great-nephew/niece",			"2GN/N"  ),
	 105: ( "3rd great-nephew/niece",			"3GN/N"  ),
	 106: ( "4th great-nephew/niece",			"4GN/N"  ),
	 107: ( "5th great-nephew/niece",			"5GN/N"  ),
	 108: ( "6th great-nephew/niece",			"6GN/N"  ),
	 109: ( "7th great-nephew/niece",			"7GN/N"  ),
	1010: ( "8th great-nephew/niece",			"8GN/N"  ),
	1011: ( "9th great-nephew/niece",			"9GN/N"  ),
	1012: ( "10th great-nephew/niece",			"10GN/N" ),
	 201: ( "uncle/aunt",						"U/A"    ),
	 301: ( "great-uncle/aunt",					"GU/A"   ),
	 401: ( "2nd great-uncle/aunt",				"2GU/A"  ),
	 501: ( "3rd great-uncle/aunt",				"3GU/A"  ),
	 601: ( "4th great-uncle/aunt",				"4GU/A"  ),
	 701: ( "5th great-uncle/aunt",				"5GU/A"  ),
	 801: ( "6th great-uncle/aunt",				"6GU/A"  ),
	 901: ( "7th great-uncle/aunt",				"7GU/A"  ),
	1001: ( "8th great-uncle/aunt",				"8GU/A"  ),
	1101: ( "9th great-uncle/aunt",				"9GU/A"  ),
	1201: ( "10th great-uncle/aunt",			"10GU/A" ),
	 202: ( "1st cousin",						"1C"     ),
	 203: ( "1st cousin once removed",			"1C1R"   ),
	 204: ( "1st cousin twice removed",			"1C2R"   ),
	 205: ( "1st cousin 3 times removed",		"1C3R"   ),
	 206: ( "1st cousin 4 times removed",		"1C4R"   ),
	 207: ( "1st cousin 5 times removed",		"1C5R"   ),
	 208: ( "1st cousin 6 times removed",		"1C6R"   ),
	 209: ( "1st cousin 7 times removed",		"1C7R"   ),
	 210: ( "1st cousin 8 times removed",		"1C8R"   ),
	 211: ( "1st cousin 9 times removed",		"1C9R"   ),
	 212: ( "1st cousin 10 times removed",		"1C10R"  ),
	 302: ( "1st cousin once removed",			"1C1R"   ),
	 402: ( "1st cousin twice removed",			"1C2R"   ),
	 502: ( "1st cousin 3 times removed",		"1C3R"   ),
	 602: ( "1st cousin 4 times removed",		"1C4R"   ),
	 702: ( "1st cousin 5 times removed",		"1C5R"   ),
	 802: ( "1st cousin 6 times removed",		"1C6R"   ),
	 902: ( "1st cousin 7 times removed",		"1C7R"   ),
	1002: ( "1st cousin 8 times removed",		"1C8R"   ),
	1102: ( "1st cousin 9 times removed",		"1C9R"   ),
	1202: ( "1st cousin 10 times removed",		"1C10R"  ),
	 303: ( "2nd cousin",						"2C"     ),
	 304: ( "2nd cousin once removed",			"2C1R"   ),
	 305: ( "2nd cousin twice removed",			"2C2R"   ),
	 306: ( "2nd cousin 3 times removed",		"2C3R"   ),
	 307: ( "2nd cousin 4 times removed",		"2C4R"   ),
	 308: ( "2nd cousin 5 times removed",		"2C5R"   ),
	 309: ( "2nd cousin 6 times removed",		"2C6R"   ),
	 310: ( "2nd cousin 7 times removed",		"2C7R"   ),
	 311: ( "2nd cousin 8 times removed",		"2C8R"   ),
	 312: ( "2nd cousin 9 times removed",		"2C9R"   ),
	 403: ( "2nd cousin once removed",			"2C1R"   ),
	 503: ( "2nd cousin twice removed",			"2C2R"   ),
	 603: ( "2nd cousin 3 times removed",		"2C3R"   ),
	 703: ( "2nd cousin 4 times removed",		"2C4R"   ),
	 803: ( "2nd cousin 5 times removed",		"2C5R"   ),
	 903: ( "2nd cousin 6 times removed",		"2C6R"   ),
	1003: ( "2nd cousin 7 times removed",		"2C7R"   ),
	1103: ( "2nd cousin 8 times removed",		"2C8R"   ),
	1203: ( "2nd cousin 9 times removed",		"2C9R"   ),
	}

alternate_relationship_names  = {
	  0:  ( "self",								"SELF"),
	  1:  ( "son/daughter",						"S/D"),
	  2:  ( "grandson/daughter",				"GS/D"),
	  3:  ( "great-grandson/daughter",			"GGS/D"),
	  4:  ( "2nd great-grandson/daughter",		"2GGS/D"),
	  5:  ( "3rd great-grandson/daughter",		"3GGS/D"),
	  6:  ( "4th great-grandson/daughter",		"4GGS/D"),
	  7:  ( "5th great-grandson/daughter",		"5GGS/D"),
	  8:  ( "6th great-grandson/daughter",		"6GGS/D"),
	  9:  ( "7th great-grandson/daughter",		"7GGS/D"),
	  10: ( "8th great-grandson/daughter",		"8GGS/D"),
	  11: ( "9th great-grandson/daughter",		"9GGS/D"),
	  12: ( "10th great-grandson/daughter",		"10GGS/D"),
	 100: ( "father/mother",					"F/M"),
	 200: ( "grandfather/mother",				"GF/M"),
	 300: ( "great-grandfather/mother",			"GGF/M"),
	 400: ( "2nd great-grandfather/mother",		"2GGF/M"),
	 500: ( "3rd great-grandfather/mother",		"3GGF/M"),
	 600: ( "4th great-grandfather/mother",		"4GGF/M"),
	 700: ( "5th great-grandfather/mother",		"5GGF/M"),
	 800: ( "6th great-grandfather/mother",		"6GGF/M"),
	 900: ( "7th great-grandfather/mother",		"7GGF/M"),
	1000: ( "8th great-grandfather/mother",		"8GGF/M"),
	1100: ( "9th great-grandfather/mother",		"9GGF/M"),
	1200: ( "10th great-grandfather/mother",	"10GGF/M"),
	 101: ( "bother/sister",					"0C"),
	 102: ( "nephew/niece",						"0C+1G"),
	 103: ( "great-nephew/niece",				"0C+2G"),
	 104: ( "2nd great-nephew/niece",			"0C+3G"),
	 105: ( "3rd great-nephew/niece",			"0C+4G"),
	 106: ( "4th great-nephew/niece",			"0C+5G"),
	 107: ( "5th great-nephew/niece",			"0C+6G"),
	 108: ( "6th great-nephew/niece",			"0C+7G"),
	 109: ( "7th great-nephew/niece",			"0C+8G"),
	1010: ( "8th great-nephew/niece",			"0C+9G"),
	1011: ( "9th great-nephew/niece",			"0C+10G"),
	1012: ( "10th great-nephew/niece",			"0C+11G"),
	 201: ( "uncle/aunt",						"0C-1G"),
	 301: ( "great-uncle/aunt",					"0C-2G"),
	 401: ( "2nd great-uncle/aunt",				"0C-3G"),
	 501: ( "3rd great-uncle/aunt",				"0C-4G"),
	 601: ( "4th great-uncle/aunt",				"0C-5G"),
	 701: ( "5th great-uncle/aunt",				"0C-6G"),
	 801: ( "6th great-uncle/aunt",				"0C-7G"),
	 901: ( "7th great-uncle/aunt",				"0C-8G"),
	1001: ( "8th great-uncle/aunt",				"0C-9G"),
	1101: ( "9th great-uncle/aunt",				"0C-10G"),
	1201: ( "10th great-uncle/aunt",			"0C-11G"),
	 202: ( "1st cousin",						"1C"),
	 203: ( "1st cousin plus 1 generation",		"1C+1G"),
	 204: ( "1st cousin plus 2 generations",	"1C+2G"),
	 205: ( "1st cousin plus 3 generations",	"1C+3G"),
	 206: ( "1st cousin plus 4 generations",	"1C+4G"),
	 207: ( "1st cousin plus 5 generations",	"1C+5G"),
	 208: ( "1st cousin plus 6 generations",	"1C+6G"),
	 209: ( "1st cousin plus 7 generations",	"1C+7C"),
	 210: ( "1st cousin plus 8 generations",	"1C+8G"),
	 211: ( "1st cousin plus 9 generations",	"1C+9G"),
	 212: ( "1st cousin plus 10 generations",	"1C+10G"),
	 302: ( "1st cousin minus 1 generation",	"2C-1G"),
	 402: ( "1st cousin minus 2 generations",	"3C-2G"),
	 502: ( "1st cousin minus 3 generations",	"4C-3G"),
	 602: ( "1st cousin minus 4 generations",	"5C-4G"),
	 702: ( "1st cousin minus 5 generations",	"6C-5G"),
	 802: ( "1st cousin minus 6 generations",	"7C-6G"),
	 902: ( "1st cousin minus 7 generations",	"8C-7G"),
	1002: ( "1st cousin minus 8 generations",	"10C-8G"),
	1102: ( "1st cousin minus 9 generations",	"11C-9G"),
	1202: ( "1st cousin minus 10 generations",	"12C-10G")
}

#=======================
# Module level functions
#=======================
#
#==========================================================================================
# _get_standard_relationship_name()
#
#		gets relationship from relationship names dictionary and
#		massages them for certain relationships, e.g. "son/daughter" -> "son" or "daughter"
#==========================================================================================

def _get_standard_relationship_name( sex_a: str, distance_a: int, sex_b: str, distance_b: int) -> str:
	
	key = distance_a * 100 + distance_b
	
	relationship = f"{_standard_relationship_names[key][0]} ({_standard_relationship_names[key][1]})"
	
	massaged_relationship = _massage_relationship(  sex_b, relationship)
	
	return massaged_relationship
	
#end def

#===============================================+=============================================
# _massage_relationship
#
#	massages relationship for certain relationships, e.g. "son/daughter" -> "son" or "daughter
#=============================================================================================

def _massage_relationship( sex: str, relationship: str) -> str:
	if sex == "m":
		relationship = relationship.replace( "son/daughter",    "son")
		relationship = relationship.replace( "father/mother",   "father")
		relationship = relationship.replace( "brother/sister",  "brother")
		relationship = relationship.replace( "uncle/aunt",      "uncle")
		relationship = relationship.replace( "nephew/niece",    "nephew")
		
		relationship = relationship.replace( "S/D",  "S")
		relationship = relationship.replace( "F/M",  "F")
		relationship = relationship.replace( "B/S",  "BR")
		relationship = relationship.replace( "U/A",  "U")
		relationship = relationship.replace( "N/N",  "NE")
	elif sex == "f":
		relationship = relationship.replace( "son/daughter",    "daughter")
		relationship = relationship.replace( "father/mother",   "mother")
		relationship = relationship.replace( "brother/sister",  "sister")
		relationship = relationship.replace( "uncle/aunt",      "aunt")
		relationship = relationship.replace( "nephew/niece",    "niece")
		
		relationship = relationship.replace( "S/D",  "D")
		relationship = relationship.replace( "F/M",  "M")
		relationship = relationship.replace( "B/S",  "SI")
		relationship = relationship.replace( "U/A",  "A")
		relationship = relationship.replace( "N/N",  "NI")
	#end if
	
	return relationship
	
#end def

def _print_standard_relationship_descriptions( name_a: str, sex_a: str, distance_a: int, name_b: str, sex_b: str, distance_b: int, half_status: str):
	
	relationship_a_to_b = _get_standard_relationship_name( sex_a, distance_a, sex_b, distance_b)
	relationship_b_to_a = _get_standard_relationship_name( sex_b, distance_b, sex_a, distance_a)
	
	print( f"\n{name_b} is {name_a}'s {relationship_a_to_b}")
	print( f"\n{name_a} is {name_b}'s {relationship_b_to_a}")
	
	if distance_a == 0 or distance_b == 0:												# direct ancestor/descendant
		relationship = relationship_b_to_a + " & " + relationship_a_to_b
	else:
		if distance_a == 1 and distance_b == 1:											# siblings
			relationship = "siblings (SIB)"
		elif distance_a == 1 and distance_b == 2:										# uncle/aunt/nephew/niece
			relationship = relationship_b_to_a + " & " + relationship_a_to_b
		elif distance_a == 2 and distance_b == 1:
			relationship = relationship_b_to_a
		elif  distance_a > 1 and distance_b > 1:										# cousins
			relationship = relationship_a_to_b.replace( "cousin", "cousins")
		#end if
		if half_status == "h":
			relationship = "half " + relationship
		#end if
	#end if

	print( f"\n{name_a} and {name_b} are {relationship}")
		
#end def
"""

#================================
# _get_undirected_relationships()
#================================

def _get_undirected_relationship( distance_a: int, distance_b: int, relationship_b_to_a: str, relationship_a_to_b: str) -> str:
	
	if distance_a == 0 or distance_b == 0:												# direct ancestor/descendant
		relationship = relationship_b_to_a + "/" + relationship_a_to_b
		abbreviation = abbreviation_b_to_a + "/" + abbreviation_a_to_b
	else:
		if distance_a == 1 and distance_b == 1:											# siblings
			relationship = "siblings"
			abbreviation = "SIB"
		elif distance_a == 1 and distance_b == 2:										# uncle/aunt/nephew/niece
			relationship = relationship_b_to_a + "/" + relationship_a_to_b
			abbreviation = abbreviation_b_to_a + "/" + abbreviation_a_to_b
		elif distance_a == 2 and distance_b == 1:
			relationship = relationship_b_to_a
			abbreviation = abbreviation_b_to_a
		elif  distance_a > 1 and distance_b > 1:										# cousins
			relationship = relationship_a_to_b.replace( "cousin", "cousins")
			abbreviation = abbreviation_a_to_b
		#end if
		if half_status == "h":
			relationship = "half " + relationship
			abbreviation = "H" + abbreviation
		#end if
	#end if

	return f"\n{name_a} and {name_b} are {relationship} ({abbreviation})"
	
#end if

"""




