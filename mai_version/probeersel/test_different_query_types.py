import statistics
import timeit

import gc
import problog
from problog import get_evaluatable
from problog.program import PrologString
from problog.engine import DefaultEngine
from problog.logic import Term

p = PrologString("""
solve(Sol) :-
	generate(Sol),
	test(Sol),
	write(Sol), nl.


generate([]).
generate([H|T]) :-
	% generate a value from 1 to 9 for the element H:
	member(H,[1,2,3,4,5,6,7,8,9]),
	% generate the rest:
	generate(T).

test(Sol) :-
        % test all row constraints:
	test2([r1,r2,r3,r4,r5,r6,r7,r8,r9],Sol), % r1= first row, ...
        % test all column constraints:
	test2([c1,c2,c3,c4,c5,c6,c7,c8,c9],Sol), % c1= first column, ...
        % test all block constraints:
	test2([b1,b2,b3,b4,b5,b6,b7,b8,b9],Sol). % b1= first block, ...


test2([],_). % no rows/blocks/columns left to check
test2([H|T],Sol) :-
	% 1) check the first row/column/block:
	% 1a) get the involved positions:
	group(H,Positions),
	% 1b) get the values at those positions:
	get_values(Positions,Sol,Values),
	% 1c) check whether these values are all different: 
	all_different(Values),
	% 2) check the remaining rows/blocks/columns:
	test2(T,Sol).

get_values([],_,[]).
get_values([Pos|T],Sol,[Val|T2]) :-
	nth_element(Pos,Sol,Val), % get the value at Pos
	get_values(T,Sol,T2).

all_different([]).
all_different([H|T]) :-
	% H should not occur in T:
	not(member(H,T)),
	% all elements of T should be different:
	all_different(T).



% the rows:
group(r1,[1,2,3,4,5,6,7,8,9]). % first row
group(r2,[10,11,12,13,14,15,16,17,18]). % second row
group(r3,[19,20,21,22,23,24,25,26,27]). % ...
group(r4,[28,29,30,31,32,33,34,35,36]).
group(r5,[37,38,39,40,41,42,43,44,45]).
group(r6,[46,47,48,49,50,51,52,53,54]).
group(r7,[55,56,57,58,59,60,61,62,63]).
group(r8,[64,65,66,67,68,69,70,71,72]).
group(r9,[73,74,75,76,77,78,79,80,81]).

% the columns:
group(c1,[1,10,19,28,37,46,55,64,73]).
group(c2,[2,11,20,29,38,47,56,65,74]).
group(c3,[3,12,21,30,39,48,57,66,75]).
group(c4,[4,13,22,31,40,49,58,67,76]).
group(c5,[5,14,23,32,41,50,59,68,77]).
group(c6,[6,15,24,33,42,51,60,69,78]).
group(c7,[7,16,25,34,43,52,61,70,79]).
group(c8,[8,17,26,35,44,53,62,71,80]).
group(c9,[9,18,27,36,45,54,63,72,81]).

% the blocks:
group(b1,[1,2,3,10,11,12,19,20,21]).
group(b2,[4,5,6,13,14,15,22,23,24]).
group(b3,[7,8,9,16,17,18,25,26,27]).
group(b4,[28,29,30,37,38,39,46,47,48]).
group(b5,[31,32,33,40,41,42,49,50,51]).
group(b6,[34,35,36,43,44,45,52,53,54]).
group(b7,[55,56,57,64,65,66,73,74,75]).
group(b8,[58,59,60,67,68,69,76,77,78]).
group(b9,[61,62,63,70,71,72,79,80,81]).


member(X,[X|_]).
member(X,[_|T]) :-
	member(X,T).

nth_element(N,[H|_],H) :-
	N=1.
nth_element(N,[_|T],E) :-
	N>1,
	N1 is N-1,
	nth_element(N1,T,E).


""")

query = PrologString("solve([_,_,_,2,3,_,_,_,5,_,4,2,_,9,_,_,_,3,3,_,_,_,_,8,7,_,_,_,_,7,_,_,_,_,5,6,_,9,_,7,2,_,_,1,4,5,_,_,9,_,_,_,_,_,6,_,_,_,_,2,8,4,9,_,_,8,_,_,1,_,_,7,2,5,_,_,_,9,6,_,_]).")
query1 = None

for item in query:
    query1 = item


engine = DefaultEngine()

times_query = []
times_query_extended = []

db = engine.prepare(p)  # This compiles the Prolog model into an internal format.
# This step is optional, but it might be worthwhile if you
#  want to query the same model multiple times.

db2 = db.extend()
db2 += Term('query')(query1)

for i in range(0, 100):
    start = timeit.default_timer()
    results = engine.query(db, query1)
    end = timeit.default_timer()
    gc.collect()
    times_query.append(end - start)
    # print([query1(*args) for args in results])
    print(results)

for i in range(0, 100):
    start = timeit.default_timer()
    query_result = problog.get_evaluatable().create_from(db, engine=engine).evaluate()
    end = timeit.default_timer()
    gc.collect()
    times_query_extended.append(end - start)
    print(query_result)

print("average duration query:", statistics.mean(times_query), "seconds")
print("average duration query:", statistics.mean(times_query_extended), "seconds")
# for statement in p:
#     print(statement)
#
# knowledge = get_evaluatable().create_from(p)
#
# print(knowledge.evaluate())