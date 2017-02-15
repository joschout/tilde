"""
Simple ProbLog code for a classifying a machine example using Problog code to encode the rules
"""
from problog.program import SimpleProgram

from classification import get_label_old, get_label, get_label_single_example
from representation.example import Example

from mach_tests.mach_definitions_logic import *


ex1 = Example()

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


print(get_label_old([ex1], rules, possible_labels))
print(get_label([ex1], rules, possible_labels))
print(get_label_single_example(ex1, rules, possible_labels))
