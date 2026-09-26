"""
-------------------------------------------------------
Family.py

	2026 09 24		version 1.0.0
	2026 09 26		rewrote show_person and show_family
	2026 09 26		split off from People.py
-------------------------------------------------------
"""

from GEDCOM.GEDCOM_Date		import Date

class Family():

	def __init__( self: Family, initialize_relationships = True):
		self.id					: str				= ""		# family identifier
		if initialize_relationships:
			from Person import no_person
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

class No_Family( Family) :
	def __init__( self):
		super().__init__( initialize_relationships = False)

no_family = No_Family()