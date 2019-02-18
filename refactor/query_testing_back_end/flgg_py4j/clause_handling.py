from typing import Iterable

from refactor.representation.TILDE_query import TILDEQuery
from refactor.representation.example import ExampleWrapper


def literals_to_flgg_clause_string(iterable_literals: Iterable, init_string="") -> str:

    for i, lit in enumerate(iterable_literals, 0):
        init_string += str(lit) + ", "
    if init_string != "":
        init_string = init_string[:-2] + "."

    return init_string


def build_clause(example: ExampleWrapper, training=True) -> str:

    example_string = ""
    has_classification_term = False

    if training:
        # TODO: remove ugly hack
        # has_classification_term = False
        if hasattr(example, 'classification_term'):
            has_classification_term = True
            example_string += 'not(' + str(example.classification_term) + ")"

    # TODO: remove double iteration over list
    first_lit = None
    for lit in example.logic_program:
        first_lit = lit
        break
    if first_lit is not None:
        if has_classification_term:
            example_string += ", "
        return literals_to_flgg_clause_string(example.logic_program, init_string=example_string)
    else:
        return example_string


def build_hypothesis(tilde_query:  TILDEQuery) -> str:
    return literals_to_flgg_clause_string(tilde_query.get_literals_as_subsumption_list())


