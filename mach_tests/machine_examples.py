from problog.logic import *
from problog.program import SimpleProgram
from mach_tests.test_get_label import get_label

# defining the terms
sendback, fix, ok, worn, replaceable = \
    Term('sendback'), Term('fix'), Term('ok'), Term('worn'), Term('replaceable')
p0, p1, class_ = \
    Term('p0'), Term('p1'), Term('class')

# defining the constants
gear, engine, chain, wheel, control_unit = \
    Constant('gear'), Constant('engine'), Constant('chain'), Constant('wheel'), Constant('control_unit')

X = Var('X')

# defining clauses, TILDE paper page 289 figure 4
rules = SimpleProgram()
rules += (p0 << worn(X))
rules += (p1 << (worn(X) & ~replaceable(X)))
rules += (sendback << (worn(X) & ~replaceable(X)))
rules += (fix << (worn(X) & ~p1))
rules += (ok << ~p0)

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


def test_get_labels():
    labels = get_label(examples, rules)
    print(labels)
