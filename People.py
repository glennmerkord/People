"""
-------------------------------------------------------
People.py

	2026 09 24		version 1.0.0
	2026 09 26		rewrote show_person and show_family
-------------------------------------------------------
"""

from GEDCOM.GEDCOM_File			import GEDCOM_File
from GEDCOM.GEDCOM_Date			import Date
from GEDCOM.GEDCOM_Individual	import GEDCOM_Individual, no_gedcom_individual
from GEDCOM.GEDCOM_Family		import GEDCOM_Family, no_gedcom_family

from CommandLine.CommandLine	import Framework

from Utilities.Utilities		import is_integer, match_first_in_list, caller_info

import	os

#
# class Name
#
class Name():
	
	def __init__( self):
		self.fullname		: str	= ""
		self.givenname		: str	= ""
		self.surname		: str	= ""
#
# end class Name
#
# class Person
#
class Person():
	
	def __init__( self, initialize_relationships = True):		
		self.id					: str			= ""			# person identifier
		self.fullname			: str			= ""
		self.givenname			: str			= ""
		self.surname			: str			= ""
		self.sex				: str			= "Unknown"		# Male, Female, or Unknown			
		self.birth_date			: Date			= Date( "")
		self.birth_place		: str			= ""
		self.death_date			: Date			= Date( "")
		self.death_place		: str			= ""
		if initialize_relationships:
			self.father			: Person		= no_person
			self.mother			: Person		= no_person
			self.child_of		: Family		= no_family		# family this person is a child of
		self.families			: [Family]		= []			# list of families this person is a spouse of
		self.number_of_children	: int			= 0				# total number of children from all families

	def __format__( self, format_string):

		def format_name( name: str, width: int):
			if len( name) > width:
				return name[:width-3] + "..."
			elif len( name) < max_length:
				return name.ljust( width)
			else:
				return name
			# end if
		#end def

		if format_string == "full":
			format_string = f"id:name:birth-death:parents:#_of_spouses:#_of_children"
		# end if

		items = format_string.strip().lower().split(":")
		return_string = []
		max_length = 30

		for item in items:
			if item == "id":
				return_string.append( self.id)
			elif item == "name":
				name = format_name( self.fullname, max_length)
				return_string.append( name)
			elif item == "birth-death":
				birth_death_string = self.birth_death( format = "long")
				return_string.append( f"{birth_death_string:13}")
			elif item == "parents":
				father = format_name( self.father.fullname, max_length)
				mother = format_name( self.mother.fullname, max_length)
				if self.sex == "Male":
					parents_string = f"son of {father} & {mother}"
				elif self.sex == "Female":
					parents_string = f"dau of {father} & {mother}"
				else:
					parents_string = f"chi of {father} & {mother}"					
				# end if
				return_string.append( f"{parents_string}")
			elif item == "#_of_spouses":
				number_of_spouses = len( self.families)
				if number_of_spouses == 1:
					return_string.append( f"{number_of_spouses} spouse ")
				else:
					return_string.append( f"{number_of_spouses} spouses")
				# end if
			elif item == "#_of_children":
				if self.number_of_children == 1:
					return_string.append( f"{self.number_of_children} child")
				else:
					return_string.append( f"{self.number_of_children} children")
					# end if					
			# end if
		# end for
		return "  ".join( return_string)
	
	def birth_death( self, format = "short"):
		birth_year = self.birth_date.begin_year
		death_year = self.death_date.end_year

		if format == "short":
			if birth_year == "0000": birth_year = ""
			if death_year == "9999": death_year = ""
		else:
			if birth_year == "0000": birth_year = "    "
			if death_year == "9999": death_year = "    "
		# end if

		return f"({birth_year} - {death_year})"
	# end def	
	def __eq__( self: Person, other: Person):
		return self.id == other.id
	
	def __hash__( self: Person):
		return hash( self.id)
	
	def __str__( self: Person):
		return self.name.fullname
#
# end class Person
#
# class Family
#
class Family():

	def __init__( self: Family, initialize_relationships = True):
		self.id					: str				= ""		# family identifier
		if initialize_relationships:
			self.husband		: Person			= no_person
			self.wife			: Person			= no_person
		self.marriage_date		: Date				= Date( "")
		self.marriage_place		: str				= ""
		self.children			: list[Person]		= []		# sorted by birth date	

	def __format__( self, format_string):

		def format_name( name: str, width: int):
			if len( name) > width:
				return name[:width-3] + "..."
			elif len( name) < max_length:
				return name.ljust( width)
			else:
				return name
			# end if
		#end def

		items = format_string.strip().lower().split(":")
		return_string = []
		max_length = 30

		for item in items:
			if item == "id":
				return_string.append( self.id)
			elif item == "spouses":
				husband		= format_name( self.husband.fullname, max_length)
				wife		= format_name( self.wife.fullname, max_length)
				return_string.append( f"{husband} & {wife}")
			elif item == "#_of_children":
				number_of_children = len( self.children)
				if number_of_children == 1:
					return_string.append( f"& 1 child")
				else:
					return_string.append( f"& {number_of_children} children")
			elif item == "children":
				for child in self.children:
					name = format_name( child.fullname, max_length)
					return_string.append( f"\n\t{name}")
		# end for
		return "  ".join( return_string)
	# end def
	
	def birth_death( self, format = "short"):
		birth_year = self.birth_date.begin_year
		death_year = self.death_date.end_year

		if format == "short":
			if birth_year == "0000": birth_year = ""
			if death_year == "9999": death_year = ""
		else:
			if birth_year == "0000": birth_year = "    "
			if death_year == "9999": death_year = "    "
		# end if

		return f"({birth_year} - {death_year})"
	# end def
		
	def __eq__( self: Family, other: Family):
		return self.id == other.id
	
	def __hash__( self: Family):
		return hash( self.id)
	
	def __str__( self: Family):
		return f"{self.id} {self.husband.name.fullname} {self.wife.name.fullname}"
#	
# end class Family
#	
# class People
#
class People():
	
	def __init__( self: People, gedcom_file: GEDCOM_File):
		self.gedcom_file			= gedcom_file
		self.persons				= {}		# keyed by person id
		self.families				= {}		# keyed by family id
		self.person_xref_letter		= ""
		self.family_xref_letter		= ""

		self._get_people_and_families_from_gedcom_file( gedcom_file)

		if len( self.persons) > 0:
			first_id = next(iter(self.persons))
			self.person_xref_letter = first_id[1]

		if len( self.families) > 0:
			first_id = next(iter(self.families))
			self.family_xref_letter = first_id[1]

	def find_person( self, search_term: str) -> [Person]:
		candidates: list[Person] = []

		if not search_term:
			return candidates

		search_terms = search_term.lower().split()

		for person in self.persons.values():	
			name_and_date = str(person.fullname + " " + person.birth_date.begin_date).lower()
			match = True
			for term in search_terms:
				if term not in name_and_date:
					match = False
					break
			
			if match:
				candidates.append( person)
		
		return candidates

	def find_family( self, search_term: str) -> [Family]:
	
		candidate_families: list[Family] = []

		if not search_term:
			return candidate_families
		# end if

		search_terms 								= search_term.split()
		candidate_people: list[GEDCOM_Individual]	= []

		for person in self.persons.values():
			# date 			= persons.birth_date.begin_date if type( person.birth_date) == Date else person.birth_date
			date			= person.birth_date.begin_date
			name_and_date	= str(person.name + " " + date).lower()
			match			= True

			for term in search_terms:
				if term not in name_and_date:
					match = False
					break
			
			if match:
				candidate_people.append( person)	
		# end for
	
		for person in candidate_people:
			for family in person.families_a_spouse_in:
				candidate_families.append( family)

		return candidate_families
		
	# end def find_family
#
# create persons and families from gedcom individuals and families
# and generated linkages between persons and families
#
	def _get_people_and_families_from_gedcom_file( self, file: GEDCOM_File) -> bool:
#
# create persons and famlies from gedcom individuals and families
#
		for gedcom_individual in file.individuals.values():
			self.persons[gedcom_individual.id]	= self._new_person_from_gedcom_individual( gedcom_individual)

		for gedcom_family in file.families.values():
			self.families[gedcom_family.id]		= self._new_family_from_gedcom_family( gedcom_family)
#
# generate linkages between persons and famlies
#
		for person in self.persons.values():
			gedcom_individual				= file.individuals[person.id]
			gedcom_father					= gedcom_individual.father_of()
			gedcom_mother					= gedcom_individual.mother_of()
			gedcom_family_a_child_of		= gedcom_individual.family_a_child_of
			gedcom_families_a_spouse_in		= gedcom_individual.families_a_spouse_in
			if gedcom_father            != no_gedcom_individual:
				person.father				= self.persons[gedcom_father.id]
			if gedcom_mother            != no_gedcom_individual:
				person.mother				= self.persons[gedcom_mother.id]
			if gedcom_family_a_child_of != no_gedcom_family:
				person.child_of				= self.families[gedcom_family_a_child_of.id]
			person.families					= []
			for gedcom_family in gedcom_families_a_spouse_in:
				person.families.append( self.families[gedcom_family.id])
	
		for family in self.families.values():
			gedcom_family					= file.families[family.id]
			gedcom_husband					= gedcom_family.husband
			gedcom_wife						= gedcom_family.wife
			gedcom_children					= gedcom_family.children
			if gedcom_husband != no_gedcom_individual:
				family.husband				= self.persons[gedcom_husband.id]
			if gedcom_wife    != no_gedcom_individual:
				family.wife					= self.persons[gedcom_wife.id]
			family.children					= []
			for gedcom_child in gedcom_children:
				family.children.append( self.persons[gedcom_child.id])
#
# sort children by birth_date
#
		for family in self.families.values():
			family.children.sort(key = lambda child: child.birth_date.end_date_integer)
		#end for

#
# create person from gedcom individual
#
	def _new_person_from_gedcom_individual( self, gedcom_individual: GEDCOM_Individual) -> Person:
		new_person							= Person()
		new_person.id						= gedcom_individual.id
		new_person.fullname					= gedcom_individual.name
		new_person.givenname				= gedcom_individual.given_name
		new_person.surname					= gedcom_individual.sur_name
		new_person.sex						= gedcom_individual.sex
		new_person.birth_date				= gedcom_individual.birth_date
		new_person.birth_place				= gedcom_individual.birth_place
		new_person.death_date				= gedcom_individual.death_date
		new_person.death_place				= gedcom_individual.death_place
		new_person.child_of					= gedcom_individual.family_a_child_of
		return new_person
#
# create family from gedcom family
#
	def _new_family_from_gedcom_family( self, gedcom_family: GEDCOM_Family) -> Family:
		new_family							= Family()
		new_family.id						= gedcom_family.id
		new_family.marriage_date			= gedcom_family.marriage_date
		new_family.marriage_place			= gedcom_family.marriage_place
		return new_family
#
# end class People
#
class No_Person( Person) :
	def __init__( self):
		super().__init__( initialize_relationships = False)

no_person = No_Person()

class No_Family( Family) :
	def __init__( self):
		super().__init__( initialize_relationships = False)

no_family = No_Family()

#------------------------------------------------------------------------------------------------------------------#

def main():
	
	import sys

	gedcom_file: GEDCOM_File	= None
	people: People.People		= None

	def error_handler( status, command, sub_command, arguments):
		print( f"\n{status}:  {command} {sub_command} {arguments}")
	# end def
#
# open
#
	def open( arguments: str):
		if not arguments:
			print()
			print( "Open: You must provide a file name!")
			return
	
		script_dir	= os.path.dirname(os.path.abspath(__file__))
		file_name	= arguments
		file_path	= os.path.join(script_dir, file_name)
	
		nonlocal gedcom_file
	
		gedcom_file = GEDCOM_File()
	
		(nl, ni, nf, ng) = gedcom_file.open_file( file_path)
		if  nl == 0:
			print( "\nop: There was a problem opening file", repr( file_name))
			return
		else:
			print()
			print( f"GEDCOM import successful: {nl} lines {ni} individuals and {nf} families in {ng} group(s) of related individuals")

		nonlocal people
		people = People( gedcom_file)
	
	def show_person( arguments: str):
		nonlocal gedcom_file
		if not gedcom_file:
			print( f"\nYou must open a gedcom file first!")
			return
		
		nonlocal people

		print( f"{len( people.persons)} people!")

		if len( arguments) == 0:
			print()
			for person in people.persons.values():
				print( f"{person:full}")
			return

		person_list = people.find_person( arguments)
		if len( person_list) == 0:
			print( f"\nli: No person found! {arguments}")
		elif len( person_list) == 1:
			person = person_list[0]
			print( f"\n{person:full}")
		else:
			print()
			for person in person_list:
				print( f"{person:full}")

	def show_family( arguments: str):
		nonlocal gedcom_file
		if not gedcom_file:
			print( f"\nYou must open a gedcom file first!")
			return

		nonlocal people

		
		print( f"{len( people.families)} families!")

		if len( arguments) == 0:
			print()
			for family in people.families.values():
				print( f"{family:id:spouses:#_of_children}")
			return

		family_list = people.find_family( arguments)
		if len( family_list) == 0:
			print( f"\nNo family found! {arguments}")
		elif len( family_list) == 1:
			family = family_list[0]
			print( f"{family:id:spouses:#_of_children:children}")
		else:
			print()
			for family in family_list:
				print( f"{family:id:spouses:#_of_children}")

	def show_commands( arguments: str):
		print( f"\nShow Commands {arguments}")

	def exit( arguments: str):
		print( f"\nExit {arguments}")

	registry =	{
		"Open"				: open,
		"Show Person"		: show_person,
		"Show Family"		: show_family,
		"Show Commands"		: show_commands,
		"Exit"				: exit
	}
	
	framework = Framework()

	framework.register_commands( registry)

	framework.run( prompt = "Command: ", error_handler = error_handler)

	sys.exit()
# end def
	
if __name__ == "__main__":
	main()
# end if