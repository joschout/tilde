import math

from tilde.probeersel.mach_tests import labeled_examples, background_knowledge, possible_targets, language_machines

import tilde.classification
from tilde.representation.TILDE_query import TILDEQuery

tilde_query = TILDEQuery(None, None)

refinement_generator = language_machines.refine_conjunction_one_literal(tilde_query)

# =================================

refined_queries = []
for refinement in refinement_generator:
    refined_queries.append(TILDEQuery(tilde_query, refinement))

best_query = None
score_best_query = - math.inf


for q in refined_queries:
    # compute the score of the queries
    examples_set = set(labeled_examples)
    conj_ofQuery = q.to_conjunction()
    examples_satisfying_query = classification.get_examples_satisfying_query(labeled_examples, conj_ofQuery, background_knowledge)
    score = tilde.trees.scoring.information_gain(examples_set, examples_satisfying_query, examples_set - examples_satisfying_query, possible_targets)
    if score > score_best_query:
        best_query = q
        score_best_query = score
    print(score)
# =========================================

refinement_generator2 = language_machines.refine_conjunction_one_literal(best_query)
refined_queries2 = []
for refinement in refinement_generator2:
    refined_queries2.append(TILDEQuery(best_query, refinement))

for q in refined_queries2:
    print(q)