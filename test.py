from problog.program import SimpleProgram
from problog.logic import *
from problog.engine import DefaultEngine
from problog.program import PrologString

example1_prolog_string = PrologString("""
worn(gear).
worn(engine).
replaceable(gear).
"""
)


backgroung_knowledge = PrologString("""
replaceable(gear).
replaceable(wheel).
replaceable(chain).
not_replaceable(engine).
not_replaceable(control_unit).
""")

logic_program = PrologString("""
p0 :- worn(X).
p1 :- worn(X), \+ replaceable(X).
sendback :- worn(X), \+ replaceable(X).
fix :- worn(X), \+ p1.
ok :- \+ p0.
"""
)


engine = DefaultEngine()

db = engine.prepare(example1_prolog_string)
db2 = db.extend()
for statement in logic_program:
    db2 += statement

query = Term('sendback')

results = engine.query(db2, query)

print(bool(results))