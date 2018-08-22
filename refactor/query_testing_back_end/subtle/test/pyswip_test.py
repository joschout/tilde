"""
PySWIP usage example. See also:
    https://github.com/yuce/pyswip
"""

from pyswip import Prolog


prolog = Prolog()
prolog.assertz("father(michael,john)")
prolog.assertz("father(michael,gina)")
query_results = list(prolog.query("father(michael,X)"))\

# check if results are correct:
if query_results == [{'X': 'john'}, {'X': 'gina'}]:
    print("Correct results")
else:
    print("Incorrect results")
for soln in prolog.query("father(X,Y)"):
    print(soln["X"], "is the father of", soln["Y"])

# michael is the father of john
# michael is the father of gina
