"""
PySWIP usage example. See also:
    https://github.com/yuce/pyswip
"""

from pyswip import Prolog

subtle_path = "/home/joschout/Repos/tilde/libs/subtle-2.2.pl"


subsumer_string = '[p(X),q(X)]'
subsubsumee_string = '[p(a),p(b),q(c),q(a)]'

prolog = Prolog()
prolog.consult(subtle_path)


query_results_list = list(prolog.query("subsumes(" + subsumer_string + ", " + subsubsumee_string + ")"))

if query_results_list: # dictionary is False if empty
    print("Does subsume: ", str(query_results_list))
else:
    print("Does NOT subsume: ", str(query_results_list))


print(query_results_list)
