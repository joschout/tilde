from representation.language import TypeModeLanguage
from representation.rule import TILDEQuery

import trees.scoring

lang = TypeModeLanguage(False)

# manually adding the types
worn_type_sign = 'worn'
worn_type_args = ['part']
lang.add_types(worn_type_sign, worn_type_args)

replaceable_type_sign = 'replaceable'
replaceable_type_args = ['part']
lang.add_types(replaceable_type_sign, replaceable_type_args)

not_replaceable_type_sign = 'not_replaceable'
not_replaceable_type_args = ['part']
lang.add_types(not_replaceable_type_sign, not_replaceable_type_args)

# manually adding the constants
part_value_type_name = 'part'
part_values = ['gear', 'chain', 'engine', 'wheel']
lang.add_values(part_value_type_name, *part_values)

# manually adding modes
lang.add_modes(replaceable_type_sign, ['-'])
lang.add_modes(worn_type_sign, ['-'])
lang.add_modes(not_replaceable_type_sign, ['-'])


tilde_query = TILDEQuery(None, None)

refinement_generator = lang.refine_conjunction_one_literal(tilde_query)

from trees.tilde_paper_machines_example import examples, background_knowledge, possible_targets, worn

refined_queries = []
for refinement in refinement_generator:
    refined_queries.append(TILDEQuery(tilde_query, refinement))
for q in refined_queries:
    # compute the score of the queries
    examples_set = set(examples)
    conj_ofQuery = q.to_conjunction()
    examples_satisfying_query = trees.scoring.get_examples_satisfying_query(examples, conj_ofQuery, background_knowledge)
    score = trees.scoring.information_gain(examples_set, examples_satisfying_query, examples_set - examples_satisfying_query, possible_targets)
    print(score)

refinement_generator2 =  lang.refine_conjunction_one_literal(refined_queries[1])
refined_queries = []
for refinement in refinement_generator2:
    print(refinement)

