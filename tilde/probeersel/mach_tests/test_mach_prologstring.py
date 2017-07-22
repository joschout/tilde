""""
Simple ProbLog code for the machine example encoded as PrologStrings.

1. Encode as a PrologString (subclass of LogicProgram):
    a. one example
    b. the background knowledge
    c. the logic program encoding the decision tree
2.

"""
from problog.engine import ClauseDB
from problog.logic import *
from problog.engine import DefaultEngine
from problog.program import PrologString


example1_prolog_string = PrologString("""
worn(gear).
worn(engine).
replaceable(gear).
""")

logic_program = PrologString("""
p0 :- worn(X).
p1 :- worn(X), \+ replaceable(X).
sendback :- worn(X), \+ replaceable(X).
fix :- worn(X), \+ p1.
ok :- \+ p0.
""")

engine = DefaultEngine()

db = engine.prepare(logic_program)  # type: ClauseDB
db2 = db.extend()  # type: ClauseDB
for statement in example1_prolog_string:
    db2 += statement

query = Term('sendback')

results = engine.query(db2, query)

print('Is example 1 of class', query, ' ? :', bool(results))
