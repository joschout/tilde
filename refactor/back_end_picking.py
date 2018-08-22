from enum import Enum

import refactor
import refactor.query_testing_back_end.problog.defaults
import refactor.query_testing_back_end.django.defaults
import refactor.query_testing_back_end.flgg_py4j.defaults
import refactor.query_testing_back_end.subtle.defaults

from refactor.default_interface import DefaultHandler


class QueryBackEnd(Enum):
    SIMPLE_PROGRAM = 1
    PROBLOG = 2
    CLAUSEDB = 3

    DJANGO = 4
    SUBTLE = 5
    FLGG = 6


def get_back_end_default(description) -> DefaultHandler:
    if description == QueryBackEnd.SIMPLE_PROGRAM:
        return refactor.query_testing_back_end.problog.defaults.ProblogDefaultHandler(QueryBackEnd.SIMPLE_PROGRAM.name)
    if description == QueryBackEnd.PROBLOG or \
            description == QueryBackEnd.CLAUSEDB:
        return None
    if description == QueryBackEnd.DJANGO:
        return refactor.query_testing_back_end.django.defaults.DjangoDefaultHandler(QueryBackEnd.DJANGO.name)
    if description == QueryBackEnd.FLGG:
        return refactor.query_testing_back_end.flgg_py4j.defaults.FLGGDefaultHandler(QueryBackEnd.FLGG.name)
    if description == QueryBackEnd.SUBTLE:
        return refactor.query_testing_back_end.subtle.defaults.SubtleDefaultHandler(QueryBackEnd.SUBTLE.name)
    else:
        return None


if __name__ == '__main__':
    print(QueryBackEnd.SIMPLE_PROGRAM.name)