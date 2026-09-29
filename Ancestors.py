"""
---------------------------------------------------------
Ancestors.py

	2026 09 26		created
---------------------------------------------------------
"""

from People.Person		import no_person

def get_ancestors( person: Person, number_of_generations: int) -> list[tuple[float, int, int, Person]]:
	
	""" Returns a list of a person's ancestors, each list item being a tuple containing			"""
	""" vertical position in an ahnentafel chart, ahnentafel_number, generation, and person		"""
	""" for a given number of generations														"""
	
	ancestors: dict[int, Person] = {}

	def traverse( current_person: Person, current_ahnentafel: int, current_gen: int) -> None:

		""" Recursively traverse a person's ancestor tree,             """
		""" stop if it is 'no_person' or exceeds requested generations """
		
		if current_person is no_person or current_gen > number_of_generations:
			return

		# Add person to the dictionary

		ancestors[current_ahnentafel] = current_person

		# Traverse father (2N) and mother (2N + 1), incrementing the generation count

		traverse( current_person.father, current_ahnentafel * 2,     current_gen + 1)
		traverse( current_person.mother, current_ahnentafel * 2 + 1, current_gen + 1)

		# begin traversal with root person, by definition ahnentafel number 1 and generation 0

	traverse( person, current_ahnentafel=1, current_gen=0)

	ancestor_list: list[tuple[float, int, int, Person]]	= []
	for ahnentafel, person in ancestors.items():
		generation	= ahnentafel.bit_length() - 1
		first		= 1 << generation
		position	= 1. - (2 * (ahnentafel - first) + 1) / (2 * first)	
		ancestor_list.append( (position, ahnentafel, generation, person))
	
	ancestor_list.sort( key=lambda x: x[0], reverse=True)
	
	return ancestor_list