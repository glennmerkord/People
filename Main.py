"""
-------------------------------------------------------
Main.py

	2026 09 24		version 1.0.0
	2026 09 26		rewrote show_person and show_family
	2026 09 26		split off from People.py
-------------------------------------------------------
"""
from __future__					import annotations

from GEDCOM.GEDCOM_File			import GEDCOM_File

from People.Population			import Population

from CommandLine.CommandLine	import Framework

from Utilities.Utilities		import is_integer

from People.Ancestors			import get_ancestors

from People.Descendants			import get_descendants

import	os
import	shlex

def main():
	
	import sys

	gedcom_file: GEDCOM_File	= None
	people: People.Population	= None

	def error_handler( status, command, sub_command, argument_string):
		print( f"\n{status}:  {command} {sub_command} {argument_string}")
	# end def
#
# open
#
	def open( argument_string: str):
		if not argument_string:
			print()
			print( "Open: You must provide a file name!")
			return
	
		script_dir	= os.path.dirname(os.path.abspath(__file__))
		file_name	= argument_string
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
		people = Population( gedcom_file)
	
	def show_person( argument_string: str):
		nonlocal gedcom_file
		if not gedcom_file:
			print( f"\nYou must open a gedcom file first!")
			return
		
		nonlocal people

		if len( argument_string) == 0:
			print()
			for person in people.persons.values():
				print( f"{person:full}")
			return

		person_list = people.find_person( argument_string)
		if len( person_list) == 0:
			print( f"\nli: No person found! {argument_string}")
		elif len( person_list) == 1:
			person = person_list[0]
			print( f"\n{person:full}")
		else:
			print()
			for person in person_list:
				print( f"{person:full}")

	def show_ancestors( argument_string: str):
		nonlocal gedcom_file
		if not gedcom_file:
			print( f"\nYou must open a gedcom file first!")
			return
		
		nonlocal people

		if len( argument_string) == 0:
			items = []
		else:
			items = argument_string.split( ",", 1)
		if len( items) == 2:
			if is_integer( items[1]):
				name					= items[0]
				number_of_generations	= int(items[1])
			else:
				items = []
		if len (items) != 2:
			print( f"\nYou must enter a name and number of generations (separated by a comma)!")
			return

		person_list = people.find_person( name)
		if len( person_list) == 0:
			print( f"\nNo person found! {name}")
		elif len( person_list) == 1:
			person			= person_list[0]
			ancestor_list	= get_ancestors( person, number_of_generations)
			print()
			for (position, ahnentafel_number, ancestor) in ancestor_list:
				print(f"Ancestor {ahnentafel_number} is {ancestor.fullname} at position {position}")
		else:
			print()
			for person in person_list:
				print( f"{person:full}")
			print (f"\nAmbigous person, be more specific!")

	def show_descendants( argument_string: str):
		nonlocal gedcom_file
		if not gedcom_file:
			print( f"\nYou must open a gedcom file first!")
			return
		
		nonlocal people

		if len( argument_string) == 0:
			items = []
		else:
			items = argument_string.split( ",", 1)
		if len( items) == 2:
			if is_integer( items[1]):
				name					= items[0]
				number_of_generations	= int(items[1])
			else:
				items = []
		if len (items) != 2:
			print( f"\nYou must enter a name and number of generations (separated by a comma)!")
			return

		person_list = people.find_person( name)
		if len( person_list) == 0:
			print( f"\nNo person found! {name}")
		elif len( person_list) == 1:
			person = person_list[0]
			descendants =  get_descendants( person, number_of_generations)
			for (generation, descendant) in descendants:
				tabs = "\t"*generation
				print( f"\n{tabs} {generation} {descendant.fullname}")
		else:
			print()
			for person in person_list:
				print( f"{person:full}")
			print (f"\nAmbigous person, be more specific!")

	def show_family( argument_string: str):
		nonlocal gedcom_file
		if not gedcom_file:
			print( f"\nYou must open a gedcom file first!")
			return

		nonlocal people

		print( f"{len( people.families)} families!")

		if len( argument_string) == 0:
			print()
			for family in people.families.values():
				print( f"{family:id:spouses:#_of_children}")
			return

		family_list = people.find_family( argument_string)
		if len( family_list) == 0:
			print( f"\nNo family found! {argument_string}")
		elif len( family_list) == 1:
			family = family_list[0]
			print( f"{family:id:spouses:#_of_children:children}")
		else:
			print()
			for family in family_list:
				print( f"{family:id:spouses:#_of_children}")

	def show_commands( argument_string: str):
		print( f"\nShow Commands {argument_string}")

	def exit( argument_string: str):
		print( f"\nExit {argument_string}")

	registry =	{
		"Open"				: open,
		"Show Person"		: show_person,
		"Show Ancestors"	: show_ancestors,
		"Show Descendants"	: show_descendants,
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