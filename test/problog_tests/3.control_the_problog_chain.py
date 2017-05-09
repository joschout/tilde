from problog.program import PrologString
from problog.engine import DefaultEngine
from problog.logic import Term

p = PrologString("""
coin(c1). coin(c2).
0.4::heads(C); 0.6::tails(C) :- coin(C).
win :- heads(C).
evidence(heads(c1), false).
query(win).
""")

engine = DefaultEngine()

db = engine.prepare(p)    # This compiles the Prolog model into an internal format.
                          # This step is optional, but it might be worthwhile if you
                          #  want to query the same model multiple times.
query1 = Term('heads', None)   # query for 'heads(_)'
results = engine.query(db, query1)
print([query1(*args) for args in results])