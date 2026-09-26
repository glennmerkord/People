"""
-------------------------------------------------------
Person.py

	2026 09 24		version 1.0.0
	2026 09 26		rewrote show_person and show_family
	2026 09 26		split off from People.py
-------------------------------------------------------
"""
from GEDCOM.GEDCOM_Date		import Date

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
			from Person import no_person
			from Family import no_family
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

class No_Person( Person) :
	def __init__( self):
		super().__init__( initialize_relationships = False)

no_person = No_Person()