from problog.logic import And

import tilde.classification
import tilde.trees.scoring

from tilde.probeersel.mach_tests.mach_definitions_logic import *
from tilde.probeersel.mach_tests.mach_definitions_TILDE_paper import *

# Testing the four examples from the problog paper using the following queries:
# <- replaceable(X)
# <- not_replaceable(X)
# <- worn(X)
# <- worn(X), replacable(X)

X = Var('X')
query1 = replaceable(X)
query2 = not_replaceable(X)
query3 = worn(X)
query4 = And(worn(X), not_replaceable(X))
queries = [query1, query2, query3, query4]

# a dictionary of sets, one for each query
results_of_queries = {}

for query in queries:
    examples_satisfying_query = classification.get_examples_satisfying_query(labeled_examples, query, background_knowledge)
    results_of_queries[query] = examples_satisfying_query

print(results_of_queries)

# entropy test
l1 = [ex2, ex3]
l2 = [ex1, ex2]
print("Entropy of 2 examples labeled 'sendback' : ", tilde.trees.scoring.entropy(l1, possible_targets), ", should be 0.0")
print("Entropy of one example labeled 'fix', another labeled 'sendback' : ", tilde.trees.scoring.entropy(l2, possible_targets), ", should be 1.0")


# information gain tests like in the TILDE paper on page 293
l_q1_l, l_q1_r = [ex1, ex2, ex3], [ex4]
l_q2_l, l_q2_r = [ex1, ex2, ex3, ex4], []
l_q3_l, l_q3_r = [ex1, ex2, ex3, ex4], []

print(tilde.trees.scoring.information_gain(labeled_examples, l_q1_l, l_q1_r, possible_targets))
print(tilde.trees.scoring.information_gain(labeled_examples, l_q2_l, l_q2_r, possible_targets))
print(tilde.trees.scoring.information_gain(labeled_examples, l_q3_l, l_q3_r, possible_targets))

