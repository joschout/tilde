from problog import get_evaluatable
from problog.program import PrologString
from problog.engine import DefaultEngine
from problog.logic import Term, Constant

p = PrologString("""
mother_child(trude, sally).

father_child(tom, sally).
father_child(tom, erica).
father_child(mike, tom).

sibling(X, Y) :- parent_child(Z, X), parent_child(Z, Y).

parent_child(X, Y) :- father_child(X, Y).
parent_child(X, Y) :- mother_child(X, Y).
""")

engine = DefaultEngine()

db = engine.prepare(p)

c1 = Constant('sally')
c2 = Constant('erica')

query1 = Term('sibling')(c1, c2)   # query for 'heads(_)'
results = engine.query(db, query1)
print([query1(*args) for args in results])