"""
---------------------------------------------------------
Descendants.py

	2026 09 28		created
---------------------------------------------------------
"""
from __future__			import annotations
from People.Person		import Person
from People.Family		import Family, no_family

def get_descendants( person: Person, number_of_generations: int) -> list[tuple[int,Person,Family]]:

	max_generation	= number_of_generations - 1

	# max_generation: the highest generation number to include

	result: list[tuple[int,Person,Family]] = []

	_collect( person, 0, result, frozenset(), max_generation)

	return result

def _collect( person, generation: int, result: list[tuple[int, Person]], path: FrozenSet[int], max_generation: int) -> None:
	if person.id in path:
		print( f"Cycle detected: {person.fullname} appears as their own descendant; skipping this branch")
		return

	path = path | {person.id}

	families_with_children = [family for family in person.families if family.children]
	at_depth_limit = max_generation is not None and generation >= max_generation

	if not families_with_children or at_depth_limit:
		result.append((generation, person, no_family))
		return

	for family in families_with_children:
		result.append((generation, person, family))
		for child in family.children:
			_collect( child, generation + 1, result, path, max_generation)