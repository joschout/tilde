from problog.engine import DefaultEngine
from problog.logic import *

from problog.program import PrologString

pl = PrologString("""
mother_child(trude, sally).

father_child(tom, sally).
father_child(tom, erica).
father_child(mike, tom).

sibling(X, Y) :- parent_child(Z, X), parent_child(Z, Y).

parent_child(X, Y) :- father_child(X, Y).
parent_child(X, Y) :- mother_child(X, Y).
""")

from problog.program import SimpleProgram

# Define the language of terms
mother_child = Term('mother_child')
father_child = Term('father_child')
sibling = Term('sibling')
parent_child = Term('parent_child')
X, Y, Z = map(Var, 'XYZ')
trude, sally, tom, erica, mike = map(Term, ['trude', 'sally', 'tom', 'erica', 'mike'])

# Define the program
pl = SimpleProgram()
pl += mother_child(trude, sally)
pl += father_child(tom, sally)
pl += father_child(tom, erica)
pl += father_child(mike, tom)
pl += sibling(X, Y) << (parent_child(Z, X) & parent_child(Z, Y))
pl += parent_child(X, Y) << father_child(X, Y)
pl += parent_child(X, Y) << mother_child(X, Y)

engine = DefaultEngine()
db = engine.prepare(pl)


print(db)
query_term = sibling(tom, sally)
res = engine.query(db, query_term)
print ('%s? %s' % (query_term, bool(res)))

query_term = sibling(sally, erica)
res = engine.query(db, query_term)
print(res)
print ('%s? %s' % (query_term, bool(res)))

# NOTE: variables can be replaced by None of a negative number
# the difference is that each None is a different variable,
# while each variable with the same negative number is the same variable
query_term = sibling(None, None)
res = engine.query(db, query_term)

for args in res:
    print(query_term(*args))

print('siblings of sally:')
query_term = Term('sibling', Term('sally'), None)
res = engine.query(db, query_term)

for args in res:
    print(query_term(*args))

print(engine.ground_all(db, queries=[query_term]))