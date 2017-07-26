""""
Simple ProbLog code for the machine example encoded as PrologStrings.

1. Encode as a PrologString (subclass of LogicProgram):
    a. one example
    b. the background knowledge
    c. the logic program encoding the decision tree
2.

"""
import problog
from problog.engine import ClauseDB
from problog.logic import *
from problog.engine import DefaultEngine
from problog.program import PrologString


eng = DefaultEngine()
eng.unknown = 1

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

possible_labels = [Term('sendback'), Term('fix'), Term('ok')]
query_terms = [Term('query')(label) for label in possible_labels]


# db logic program
db_lp = eng.prepare(logic_program)  # type: ClauseDB

# ========================================================
# db logic program + example + queries
db_lp_q = db_lp.extend()
for q in query_terms:
    db_lp_q += q
# ========================================================
# db logic program + example
db_lp_q_ex = db_lp_q.extend()  # type: ClauseDB
for e in example1_prolog_string:
    db_lp_q_ex += e

# printing
for s in db_lp:
    print(s)
for s in db_lp_q:
    print(s)
for s in db_lp_q_ex:
    print(s)


query_results = problog.get_evaluatable().create_from(db_lp_q_ex, engine=eng).evaluate()
for key in query_results:
    value = query_results[key]
    print(value)

print(query_results)

query = Term('sendback')
results = eng.query(db_lp_q_ex, query)

print('Is example 1 of class', query, ' ? :', bool(results))
