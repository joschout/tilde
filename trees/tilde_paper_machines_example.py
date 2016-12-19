from problog.logic import *
from problog.program import SimpleProgram

from representation.example import Example

# defining the terms
worn, replaceable, not_replaceable =\
    Term('worn'), Term('replaceable'), Term('not_replaceable')

# defining the constants
gear, engine, chain, wheel = \
    Constant('gear'), Constant('engine'), Constant('chain'), Constant('wheel')
fix, sendback, ok = Constant('fix'), Constant('sendback'), Constant('ok')

target  = Term('target')

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

examples = [ex1, ex2, ex3, ex4]

possible_targets = [fix, sendback, ok]

background_knowledge = SimpleProgram()
background_knowledge += replaceable(gear)
background_knowledge += replaceable(chain)
background_knowledge += not_replaceable(engine)
background_knowledge += not_replaceable(wheel)