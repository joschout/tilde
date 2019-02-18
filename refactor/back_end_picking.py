from enum import Enum

from refactor.default_interface import DefaultHandler


class QueryBackEnd(Enum):
    SIMPLE_PROGRAM = 1
    PROBLOG = 2
    CLAUSEDB = 3

    DJANGO = 4
    SUBTLE = 5
    FLGG = 6


class UnavailableBackEndException(Exception):
    pass


def get_back_end_default(description) -> DefaultHandler:
    if description == QueryBackEnd.SIMPLE_PROGRAM:
        try:
            import refactor.query_testing_back_end.problog.defaults
            return refactor.query_testing_back_end.problog.defaults.ProblogDefaultHandler(
                QueryBackEnd.SIMPLE_PROGRAM.name)
        except ImportError as err:
            raise UnavailableBackEndException(description.name + " backend not available, " + str(err))
    if description == QueryBackEnd.PROBLOG or \
            description == QueryBackEnd.CLAUSEDB:
        return None
    if description == QueryBackEnd.DJANGO:
        try:
            import refactor.query_testing_back_end.django.defaults
            return refactor.query_testing_back_end.django.defaults.DjangoDefaultHandler(QueryBackEnd.DJANGO.name)
        except ImportError as err:
            raise UnavailableBackEndException(description.name + " backend not available, " + str(err))
    if description == QueryBackEnd.FLGG:
        try:
            import refactor.query_testing_back_end.flgg_py4j.defaults
            return refactor.query_testing_back_end.flgg_py4j.defaults.FLGGDefaultHandler(QueryBackEnd.FLGG.name)
        except ImportError as err:
            raise UnavailableBackEndException(description.name + " backend not available, " + str(err))
    if description == QueryBackEnd.SUBTLE:
        try:
            import refactor.query_testing_back_end.subtle.defaults
            return refactor.query_testing_back_end.subtle.defaults.SubtleDefaultHandler(QueryBackEnd.SUBTLE.name)
        except ImportError as err:
            raise UnavailableBackEndException(description.name + " backend not available, " + str(err))
    else:
        return None


if __name__ == '__main__':
    print(QueryBackEnd.SIMPLE_PROGRAM.name)
