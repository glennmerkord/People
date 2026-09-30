"""
---------------------------------------------------------
Population.py

	2026 09 24		version 1.0.0
	2026 09 26		rewrote show_person and show_family
	2026 09 26		renamed from People.py
	2026 09 26		split off Main, Person, and Family
	2026 09 28		corrected import of Person and Family
	2026 09 28		fixed person.name to person.fullname
---------------------------------------------------------
"""

from GEDCOM.GEDCOM_File				import GEDCOM_File
from GEDCOM.GEDCOM_Date				import Date
from GEDCOM.GEDCOM_Individual		import no_gedcom_individual
from GEDCOM.GEDCOM_Family			import no_gedcom_family

from People.Person					import Person
from People.Family					import Family

#	
# class Population
#
class Population():
	
	def __init__( self: Population, gedcom_file: GEDCOM_File):
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
			name_and_date	= str(person.fullname + " " + date).lower()
			match			= True

			for term in search_terms:
				if term not in name_and_date:
					match = False
					break
			
			if match:
				candidate_people.append( person)	
		# end for
	
		for person in candidate_people:
			for family in person.families:
				candidate_families.append( family)

		return candidate_families
		
	# end def find_family
#
# create persons and families from gedcom individuals and families
# and generated linkages between persons and families
#
	def _get_people_and_families_from_gedcom_file( self, file: GEDCOM_File) -> bool:
#
# create persons and families from gedcom individuals and families
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
# end class Population