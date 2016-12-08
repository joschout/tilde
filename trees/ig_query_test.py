from problog.logic import *
from problog.program import SimpleProgram
from problog.engine import DefaultEngine

from language.example import Example
# Testing the four examples from the problog paper using the following queries:
# <- replaceable(X)
# <- not_replaceable(X)
# <- worn(X)


# defining the terms
worn, replaceable, not_replaceable =\
    Term('worn'), Term('replaceable'), Term('not_replaceable')

# defining the constants
gear, engine, chain, wheel = \
    Constant('gear'), Constant('engine'), Constant('chain'), Constant('wheel')
fix, sendback, ok = Constant('fix'), Constant('sendback'), Constant('ok')

target  = Term('target')

ex1, ex2, ex3, ex4 = Example(), Example(), Example(), Example()

ex1 += worn(gear)
ex1 += worn(chain)
ex1.label = fix

ex2 += worn(engine)
ex2 += worn(chain)
ex2.label = sendback

ex3 += worn(wheel)
ex3.label = sendback

ex4.label = ok

examples = [ex1, ex2, ex3, ex4]

possible_targets = [fix, sendback, ok]

background_knowledge = SimpleProgram()
background_knowledge += replaceable(gear)
background_knowledge += replaceable(chain)
background_knowledge += not_replaceable(engine)
background_knowledge += not_replaceable(wheel)

X = Var('X')
query1 = replaceable(X)
query2 = not_replaceable(X)
query3 = worn(X)

queries = [query1, query2, query3]

# a list of sets, one for each query
results_of_queries = {}


engine = DefaultEngine()
engine.unknown = 1

for query in queries:
    query_results = set()
    for example in examples:
        db = engine.prepare(example)
        for knowledge in background_knowledge:
            db += knowledge
        example_satisfies_query = engine.query(db, query)
        if bool(example_satisfies_query):
            query_results.add(example)
    results_of_queries[query] = query_results

print(results_of_queries)


def entropy_binary(list_of_bools):
    """Calculate the entropy of a list of booleans.

        entropy([]) = 0
        entropy([True, True]) = 0
        entropy([False, False]) = 0
        entropy( [True, True, False, False]) = 1
    """
    if len(list_of_bools) == 0:
        return 0

    nb_of_positives = list_of_bools.count(True)
    nb_of_negatives = list_of_bools.count(False)

    if nb_of_positives == 0 or nb_of_negatives == 0:
        return 0

    return - nb_of_positives / len(list_of_bools) * math.log2(nb_of_positives / len(list_of_bools))\
           - nb_of_negatives / len(list_of_bools) * math.log2(nb_of_negatives / len(list_of_bools))


def entropy(list_of_examples, list_of_possible_labels):
    if len(list_of_examples) == 0:
        return 0
    entropy_value = 0

    nb_of_examples = len(list_of_examples)

    for label in list_of_possible_labels:
        nb_of_elements_with_label = len([example for example in list_of_examples if example.label == label])
        if nb_of_elements_with_label != 0:
            entropy_value -= nb_of_elements_with_label / nb_of_examples * math.log2(nb_of_elements_with_label / nb_of_examples)
    return entropy_value

# entropy test
l1 = [ex2, ex3]
l2 = [ex1, ex2]
print("Entropy of 2 examples labeled 'sendback' : ", entropy(l1, possible_targets), ", should be 0.0")
print("Entropy of one example labeled 'fix', another labeled 'sendback' : ", entropy(l2, possible_targets), ", should be 1.0")


def information_gain(list_of_bools, sublist_left, sublist_right):
    if len(list_of_bools) == 0:
        return 0

    ig = entropy(list_of_bools, possible_targets)

    ig -= len(sublist_left) / len(list_of_bools) * entropy(sublist_left, possible_targets)
    ig -= len(sublist_right) / len(list_of_bools) * entropy(sublist_right, possible_targets)
    return ig

# information gain tests like in the TILDE paper on page 293
l_q1_l, l_q1_r = [ex1, ex2, ex3], [ex4]
l_q2_l, l_q2_r = [ex1, ex2, ex3, ex4], []
l_q3_l, l_q3_r = [ex1, ex2, ex3, ex4], []

print(information_gain(examples, l_q1_l, l_q1_r))
print(information_gain(examples, l_q2_l, l_q2_r))
print(information_gain(examples, l_q3_l, l_q3_r))