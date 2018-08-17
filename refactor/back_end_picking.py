from enum import Enum

import refactor
import refactor.tilde_on_problog.defaults
import refactor.tilde_on_django.defaults
import refactor.tilde_on_flgg_py4j.defaults
import refactor.tilde_on_subtle.defaults

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
        return refactor.tilde_on_problog.defaults.ProblogDefaultHandler()
    if description == QueryBackEnd.PROBLOG or \
            description == QueryBackEnd.CLAUSEDB:
        return None
    if description == QueryBackEnd.DJANGO:
        return refactor.tilde_on_django.defaults.DjangoDefaultHandler()
    if description == QueryBackEnd.FLGG:
        return refactor.tilde_on_flgg_py4j.defaults.FLGGDefaultHandler()
    if description == QueryBackEnd.SUBTLE:
        return refactor.tilde_on_subtle.defaults.SubtleDefaultHandler()
    else:
        return None
