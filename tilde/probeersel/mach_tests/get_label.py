"""
Simple ProbLog code for a classifying a machine example using Problog code to encode the rules
"""
from problog.program import SimpleProgram
from tilde.representation.example import SimpleProgramExampleWrapper
from tilde.probeersel.mach_tests.mach_definitions_logic import *
from tilde.classification.classification import  get_labels_single_example_models

ex1 = SimpleProgram()

ex1 += worn(gear)
ex1 += worn(engine)
ex1 += replaceable(gear)

rules = SimpleProgram()
rules += (p0 << worn(X))
rules += (p1 << (worn(X) & ~replaceable(X)))
rules += (sendback << (worn(X) & ~replaceable(X)))
rules += (fix << (worn(X) & ~p1))
rules += (ok << ~p0)

possible_labels = [sendback, fix, ok]

labels = get_labels_single_example_models(ex1, rules, possible_labels)
print(labels)
