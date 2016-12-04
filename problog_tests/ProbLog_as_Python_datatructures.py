from problog.program import SimpleProgram
from problog.logic import Constant,Var,Term,AnnotatedDisjunction
from problog import get_evaluatable

coin,heads,tails,win,query =\
    Term('coin'),Term('heads'),Term('tails'),Term('win'),Term('query')
C = Var('C')
p = SimpleProgram()
p += coin(Constant('c1'))
p += coin(Constant('c2'))
p += AnnotatedDisjunction([heads(C,p=0.4), tails(C,p=0.6)], coin(C))
p += (win << heads(C))
p += query(win)

print(get_evaluatable().create_from(p).evaluate())