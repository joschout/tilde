"""
Definition of Terms, Constants and Vars used in the machine parts examples.
"""
from problog.logic import Term, Constant, Var

# defining the terms
sendback, fix, ok = \
    Term('sendback'), Term('fix'), Term('ok')

worn, replaceable, not_replaceable  = \
    Term('worn'), Term('replaceable'), Term('not_replaceable')

p0, p1, class_ = \
    Term('p0'), Term('p1'), Term('class')

# defining the constants
gear, engine, chain, wheel, control_unit = \
    Constant('gear'), Constant('engine'), Constant('chain'), Constant('wheel'), Constant('control_unit')

# defining the vars
X = Var('X')
Y = Var('Y')
Z = Var('Z')