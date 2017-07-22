""""
Definitions of labeled Examples, a background knowledge and a TypeModeLanguage
"""
from problog.program import SimpleProgram

from tilde.representation.language import TypeModeLanguage
from tilde.representation.example import Example

from tilde.probeersel.mach_tests.mach_definitions_logic import *
ex1, ex2, ex3, ex4 = Example(), Example(), Example(), Example()

ex1 += worn(gear)
ex1 += worn(chain)
ex1.label = fix

ex2 += worn(engine)
ex2 += worn(chain)
ex2.label = sendback

ex3 += worn(wheel)
ex3.label = sendback

ex4.label = ok

labeled_examples = [ex1, ex2, ex3, ex4]

possible_targets = [fix, sendback, ok]

background_knowledge = SimpleProgram()
background_knowledge += replaceable(gear)
background_knowledge += replaceable(chain)
background_knowledge += not_replaceable(engine)
background_knowledge += not_replaceable(wheel)

# Machine language

language_machines = TypeModeLanguage(False)

# manually adding the types
worn_type_sign = 'worn'
worn_type_args = ['part']  # type: TypeArguments
language_machines.add_types(worn_type_sign, worn_type_args)

replaceable_type_sign = 'replaceable'
replaceable_type_args = ['part']
language_machines.add_types(replaceable_type_sign, replaceable_type_args)

not_replaceable_type_sign = 'not_replaceable'
not_replaceable_type_args = ['part']
language_machines.add_types(not_replaceable_type_sign, not_replaceable_type_args)

# manually adding the constants
part_value_type_name = 'part'
part_values = ['gear', 'chain', 'engine', 'wheel']
language_machines.add_values(part_value_type_name, *part_values)

# manually adding modes
language_machines.add_modes(replaceable_type_sign, ['-'])
language_machines.add_modes(worn_type_sign, ['-'])
language_machines.add_modes(not_replaceable_type_sign, ['-'])

language_machines.add_modes(replaceable_type_sign, ['+'])
language_machines.add_modes(worn_type_sign, ['+'])
language_machines.add_modes(not_replaceable_type_sign, ['+'])
