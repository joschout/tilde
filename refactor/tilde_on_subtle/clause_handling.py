from typing import Iterable

from tilde.representation.TILDE_query import TILDEQuery
from tilde.representation.example import ExampleWrapper


def literals_to_clause_string(iterable_literals: Iterable, init_string="") -> str:
    for i, lit in enumerate(iterable_literals, 0):
        init_string += str(lit) + ", "

    if init_string != "":
        init_string = init_string[:-2]

    return init_string


def build_clause(example: ExampleWrapper) -> str:

    example_string = ""
    # TODO: remove ugly hack
    has_classification_term = False
    if hasattr(example, 'classification_term'):
        has_classification_term = True
        example_string += str(example.classification_term)

    # TODO: remove double iteration over list
    first_lit = None
    for lit in example.logic_program:
        first_lit = lit
        break
    if first_lit is not None:
        if has_classification_term:
            example_string += ", "
        example_string =  literals_to_clause_string(example.logic_program, init_string=example_string)

    return "[" + example_string + "]"


def build_hypothesis(tilde_query:  TILDEQuery) -> str:
    return "[" + literals_to_clause_string(tilde_query.get_literals()) + "]"
