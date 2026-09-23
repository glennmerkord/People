from GEDCOM.GEDCOM_File			import GEDCOM_File
from GEDCOM.GEDCOM_Individual	import GEDCOM_Individual, no_gedcom_individual
from GEDCOM.GEDCOM_Family		import GEDCOM_Family, no_gedcom_family

from Date						import Date

from Command_Line_Framework		import Framework

from Utilities					import is_integer, match_first_in_list, caller_info

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
		self.person_xref_letter		= "P"
		self.family_xref_letter		= "F"

		self._get_people_and_families_from_gedcom_file( gedcom_file)

		if len( self.persons) > 0:
			first_id = next(iter(self.persons))
			self.person_xref_letter = first_id[1]

		if len( self.families) > 0:
			first_id = next(iter(self.families))
			self.family_xref_letter = first_id[1]			
#
# find person by 1) full xref, 2) integer identifier, 3) name and birthdate
# search by name and birthdate may return multiple matches
#
	def find_person( self, search_term: str) -> [Person]:
		candidates: list[Person] = []
		
		if not search_term:
			return candidates

		if "@" in search_term:
			id = search_term
		elif is_integer( search_term):
			id = f"@{self.person_xref_letter}{search_term}@"
		else:
			id = ""
	
		if id:
			if id in self.persons.keys():
				candidates.append( self.persons[id])
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

	people: People.People	= None

	def error_handler( status, command, sub_command, arguments):
		print( f"\n{status}:  {command} {sub_command} {arguments}")
	# end def
#
# open
#
	def open( filename: str):
		print( f"open {filename}")
		gedcom_file = GEDCOM_File()
		( nl, ni, nf, ng) = gedcom_file.open_file( filename)
		if nl == 0:
			print(f"\nOops, something went wrong opening file {filename}")
		else:
			nonlocal people
			people = People( gedcom_file)
	#
	# show all
	#
	def show_all( argument: str):
		if not people:
			print( f"\nError: You must open a GEDCOM file first!")
			return
		words = argument.strip().split( maxsplit = 1)
		if len( words) == 0:
			print( f"\nError: Argument missing for Show All!")
			return
		match = match_first_in_list( words[0], ["Persons", "Families"])
		if match == None:
			print( f"\nError: Invalid argument '{words[0]}' for Show All!")
			return
		if len( words) > 1:
			print( f"\nWarning: Extraneous argument '{words[1]}' for Show All ignored!")
		if match == "Persons":
			print()
			for person in people.persons.values():
				print( f"{person.fullname}")
		elif match == "Families":
			print()
			for family in people.families.values():
				print( f"{family.husband.fullname } {family.wife.fullname}")

	def show_person( arguments: str):
		nonlocal people
		persons = people.find_person( arguments)
		if len( persons) == 0:
			print( f"\nNo person matching '{arguments}' found")
		for person in persons:
			print( f"{person.fullname}")

	def show_family( arguments: str):
		print( f"\nShow Family {arguments}")

	def show_group( arguments: str):
		print( f"\nShow Group {arguments}")

	def show_commands( arguments: str):
		print( f"\nShow Commands {arguments}")

	def export( arguments: str):
		print( f"\nExport {arguments}")

	def exit( arguments: str):
		print( f"\nExit {arguments}")

	registry =	{
		"Open"				: open,
		"Show All"			: show_all,
		"Show Person"		: show_person,
		"Show Family"		: show_family,
		"Show Group"		: show_group,
		"Show Commands"		: show_commands,
		"Export"			: export,
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