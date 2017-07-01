
from problog.logic import *

functor = 'foo'
first_arg = 'bar'

deterministic_term = Term(functor)(first_arg)
probabilistic_term = Term(functor)(first_arg, p=0.5)


print(deterministic_term)
print(probabilistic_term)

deterministic_hash = deterministic_term.__hash__()
print(deterministic_hash)
probabilistic_hash = probabilistic_term.__hash__()
print(probabilistic_hash)

are_they_equal = deterministic_term == probabilistic_term
print("do they equate? ", are_they_equal)




