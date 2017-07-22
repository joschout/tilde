from problog.program import SimpleProgram

from tilde.probeersel.mach_tests.mach_definitions_logic import worn, replaceable, gear, engine, chain, control_unit, wheel


ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8, ex9, ex10 = SimpleProgram(), SimpleProgram(), SimpleProgram(), SimpleProgram(), SimpleProgram(), SimpleProgram(), SimpleProgram(), SimpleProgram(), SimpleProgram(), SimpleProgram()
ex1 += worn(gear)
ex1 += worn(engine)
ex1 += replaceable(gear)

ex3 += worn(gear)

ex4 += worn(engine)

ex5 += worn(gear)
ex5 += worn(chain)

ex6 += worn(wheel)

ex7 += worn(wheel)
ex7 += worn(control_unit)

ex9 += worn(wheel)
ex9 += worn(chain)

ex10 += worn(engine)
ex10 += worn(chain)

examples = [ex1, ex2, ex3, ex4, ex5, ex6, ex7, ex8, ex9, ex10]
