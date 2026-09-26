"""
-------------------------------------------------------
Main.py

	2026 09 24		version 1.0.0
	2026 09 26		rewrote show_person and show_family
	2026 09 26		split off from People.py
-------------------------------------------------------
"""

from GEDCOM.GEDCOM_File			import GEDCOM_File

from Population					import Population

from CommandLine.CommandLine	import Framework

import	os

def main():
	
	import sys

	gedcom_file: GEDCOM_File	= None
	people: People.Population	= None

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
		people = Population( gedcom_file)
	
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