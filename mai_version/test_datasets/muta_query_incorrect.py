from problog.program import PrologString
from problog.engine import DefaultEngine
from problog.logic import *


engine = DefaultEngine()
to_query = Term('to_query')

# ==== MANIER 1: alles in een PrologString ====#
p = PrologString("""
equals(V_0,V_0) :- true.
dmuta(V_0,pos) :- logmutag(V_0,V_1), V_1>0.
dmuta(V_0,neg) :- logmutag(V_0,V_1), V_1=<0.
sbond(V_0,V_1,V_2,V_3) :- bond(V_0,V_1,V_2,V_3); bond(V_0,V_2,V_1,V_3).
allnum(V_0,V_1,V_2,V_3) :- logmutag(V_0,V_1), logp(V_0,V_2), lumo(V_0,V_3).

to_query :- dmuta(V_0,V_1), atom(V_0,V_2,V_3,27,V_4).

molecule(1).
logmutag(1,2.11).
pos(1).
testnr(1,1).
lumo(1,-1.246).
logp(1,4.23).
nitro(1,[d1_19, d1_24, d1_25, d1_26]).
benzene(1,[d1_6, d1_1, d1_2, d1_3, d1_4, d1_5]).
benzene(1,[d1_5, d1_14, d1_13, d1_12, d1_11, d1_4]).
benzene(1,[d1_20, d1_12, d1_11, d1_17, d1_18, d1_19]).
ring_size_6(1,[d1_6, d1_1, d1_2, d1_3, d1_4, d1_5]).
ring_size_6(1,[d1_5, d1_14, d1_13, d1_12, d1_11, d1_4]).
ring_size_6(1,[d1_20, d1_12, d1_11, d1_17, d1_18, d1_19]).
phenanthrene(1,[[d1_6, d1_1, d1_2, d1_3, d1_4, d1_5], [d1_5, d1_14, d1_13, d1_12, d1_11, d1_4], [d1_20, d1_12, d1_11, d1_17, d1_18, d1_19]]).
atom(1,d1_1,c,22,-0.117).
atom(1,d1_2,c,22,-0.117).
atom(1,d1_3,c,22,-0.117).
atom(1,d1_4,c,195,-0.087).
atom(1,d1_5,c,195,0.013).
atom(1,d1_6,c,22,-0.117).
atom(1,d1_7,h,3,0.142).
atom(1,d1_8,h,3,0.143).
atom(1,d1_9,h,3,0.142).
atom(1,d1_10,h,3,0.142).
atom(1,d1_11,c,27,-0.087).
atom(1,d1_12,c,27,0.013).
atom(1,d1_13,c,22,-0.117).
atom(1,d1_14,c,22,-0.117).
atom(1,d1_15,h,3,0.143).
atom(1,d1_16,h,3,0.143).
atom(1,d1_17,c,22,-0.117).
atom(1,d1_18,c,22,-0.117).
atom(1,d1_19,c,22,-0.117).
atom(1,d1_20,c,22,-0.117).
atom(1,d1_21,h,3,0.142).
atom(1,d1_22,h,3,0.143).
atom(1,d1_23,h,3,0.142).
atom(1,d1_24,n,38,0.812).
atom(1,d1_25,o,40,-0.388).
atom(1,d1_26,o,40,-0.388).
bond(1,d1_1,d1_2,7).
bond(1,d1_2,d1_3,7).
bond(1,d1_3,d1_4,7).
bond(1,d1_4,d1_5,7).
bond(1,d1_5,d1_6,7).
bond(1,d1_6,d1_1,7).
bond(1,d1_1,d1_7,1).
bond(1,d1_2,d1_8,1).
bond(1,d1_3,d1_9,1).
bond(1,d1_6,d1_10,1).
bond(1,d1_4,d1_11,7).
bond(1,d1_11,d1_12,7).
bond(1,d1_12,d1_13,7).
bond(1,d1_13,d1_14,7).
bond(1,d1_14,d1_5,7).
bond(1,d1_13,d1_15,1).
bond(1,d1_14,d1_16,1).
bond(1,d1_11,d1_17,7).
bond(1,d1_17,d1_18,7).
bond(1,d1_18,d1_19,7).
bond(1,d1_19,d1_20,7).
bond(1,d1_20,d1_12,7).
bond(1,d1_17,d1_21,1).
bond(1,d1_18,d1_22,1).
bond(1,d1_20,d1_23,1).
bond(1,d1_24,d1_19,1).
bond(1,d1_24,d1_25,2).
bond(1,d1_24,d1_26,2).
""")

db = engine.prepare(p)
results = engine.query(db, to_query)
print(results)
# ==== EINDE MANIER 1

# ==== MANIER 2: in stukken opgedeeld ====#
background_knowledge = PrologString(
"""
equals(V_0,V_0) :- true.
dmuta(V_0,pos) :- logmutag(V_0,V_1), V_1>0.
dmuta(V_0,neg) :- logmutag(V_0,V_1), V_1=<0.
sbond(V_0,V_1,V_2,V_3) :- bond(V_0,V_1,V_2,V_3); bond(V_0,V_2,V_1,V_3).
allnum(V_0,V_1,V_2,V_3) :- logmutag(V_0,V_1), logp(V_0,V_2), lumo(V_0,V_3).
"""
)

query = Term('dmuta')(Var('V_0'), Var('V_1')) & Term('atom')(Var('V_0'),Var('V_2'),Var('V_3'),Constant('27'),Var('V_4'))

example = PrologString(
"""
molecule(1).
logmutag(1,2.11).
pos(1).
testnr(1,1).
lumo(1,-1.246).
logp(1,4.23).
nitro(1,[d1_19, d1_24, d1_25, d1_26]).
benzene(1,[d1_6, d1_1, d1_2, d1_3, d1_4, d1_5]).
benzene(1,[d1_5, d1_14, d1_13, d1_12, d1_11, d1_4]).
benzene(1,[d1_20, d1_12, d1_11, d1_17, d1_18, d1_19]).
ring_size_6(1,[d1_6, d1_1, d1_2, d1_3, d1_4, d1_5]).
ring_size_6(1,[d1_5, d1_14, d1_13, d1_12, d1_11, d1_4]).
ring_size_6(1,[d1_20, d1_12, d1_11, d1_17, d1_18, d1_19]).
phenanthrene(1,[[d1_6, d1_1, d1_2, d1_3, d1_4, d1_5], [d1_5, d1_14, d1_13, d1_12, d1_11, d1_4], [d1_20, d1_12, d1_11, d1_17, d1_18, d1_19]]).
atom(1,d1_1,c,22,-0.117).
atom(1,d1_2,c,22,-0.117).
atom(1,d1_3,c,22,-0.117).
atom(1,d1_4,c,195,-0.087).
atom(1,d1_5,c,195,0.013).
atom(1,d1_6,c,22,-0.117).
atom(1,d1_7,h,3,0.142).
atom(1,d1_8,h,3,0.143).
atom(1,d1_9,h,3,0.142).
atom(1,d1_10,h,3,0.142).
atom(1,d1_11,c,27,-0.087).
atom(1,d1_12,c,27,0.013).
atom(1,d1_13,c,22,-0.117).
atom(1,d1_14,c,22,-0.117).
atom(1,d1_15,h,3,0.143).
atom(1,d1_16,h,3,0.143).
atom(1,d1_17,c,22,-0.117).
atom(1,d1_18,c,22,-0.117).
atom(1,d1_19,c,22,-0.117).
atom(1,d1_20,c,22,-0.117).
atom(1,d1_21,h,3,0.142).
atom(1,d1_22,h,3,0.143).
atom(1,d1_23,h,3,0.142).
atom(1,d1_24,n,38,0.812).
atom(1,d1_25,o,40,-0.388).
atom(1,d1_26,o,40,-0.388).
bond(1,d1_1,d1_2,7).
bond(1,d1_2,d1_3,7).
bond(1,d1_3,d1_4,7).
bond(1,d1_4,d1_5,7).
bond(1,d1_5,d1_6,7).
bond(1,d1_6,d1_1,7).
bond(1,d1_1,d1_7,1).
bond(1,d1_2,d1_8,1).
bond(1,d1_3,d1_9,1).
bond(1,d1_6,d1_10,1).
bond(1,d1_4,d1_11,7).
bond(1,d1_11,d1_12,7).
bond(1,d1_12,d1_13,7).
bond(1,d1_13,d1_14,7).
bond(1,d1_14,d1_5,7).
bond(1,d1_13,d1_15,1).
bond(1,d1_14,d1_16,1).
bond(1,d1_11,d1_17,7).
bond(1,d1_17,d1_18,7).
bond(1,d1_18,d1_19,7).
bond(1,d1_19,d1_20,7).
bond(1,d1_20,d1_12,7).
bond(1,d1_17,d1_21,1).
bond(1,d1_18,d1_22,1).
bond(1,d1_20,d1_23,1).
bond(1,d1_24,d1_19,1).
bond(1,d1_24,d1_25,2).
bond(1,d1_24,d1_26,2).
"""
)

db = engine.prepare(background_knowledge)

db += (to_query << query)
for statement in example:
    db += statement

results = engine.query(db, to_query)
print(results)
# ==== EINDE MANIER 2 ====#

# === MANIER 3: manier 2 naar string omzetten, concateneren en dan als PrologString ====#
prolog_string = ""
for statement in db:
    prolog_string = prolog_string + str(statement) + ".\n"

example = PrologString(prolog_string)
db = engine.prepare(example)
results = engine.query(db, to_query)
print(results)
# ==== EINDE MANIER 3 ====#
