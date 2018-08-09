from typing import Sequence

from tilde.representation.TILDE_query import TILDEQuery
from tilde.representation.example import ExampleWrapper


def seq_to_flgg_clause_string(seq:Sequence) -> str:
    flgg_clause_string = ""
    for i, lit in enumerate(seq, 0):
        flgg_clause_string += str(lit)
        if i < len(seq) - 1:
            flgg_clause_string += ", "
        elif i == len(seq) - 1:
            flgg_clause_string += "."

    return flgg_clause_string


def build_clause(example: ExampleWrapper) -> str:
    return seq_to_flgg_clause_string(example.logic_program)


def build_hypothesis(tilde_query:  TILDEQuery) -> str:
    return seq_to_flgg_clause_string(tilde_query.get_literals())


