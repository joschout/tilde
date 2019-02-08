from typing import Iterable, List

from problog.logic import Term
from refactor.representation.language import TypeModeLanguage

from refactor.representation.TILDE_query import TILDEQuery


class RefinementController:
    @staticmethod
    def get_refined_queries_of(tilde_query: TILDEQuery, language: TypeModeLanguage, debug_printing: bool = False) -> \
            Iterable[TILDEQuery]:

        # generating the refined queries to test
        refinement_generator = language.refine_conjunction_one_literal(tilde_query)
        refined_queries = []  # type: List[TILDEQuery]
        for refinement in refinement_generator:  # type: Term
            refined_query = TILDEQuery(tilde_query, refinement)
            refined_queries.append(refined_query)

        if debug_printing:
            print('generated refined queries of: ', str(tilde_query))
            print('refined queries:', list(map(str, refined_queries)))
        return refined_queries

    @staticmethod
    def get_refined_query_generator(tilde_query: TILDEQuery, language: TypeModeLanguage, debug_printing: bool = False):

        # generating the refined queries to test
        refinement_generator = language.refine_conjunction_one_literal(tilde_query)
        for refinement in refinement_generator:  # type: Term
            refined_query = TILDEQuery(tilde_query, refinement)
            yield refined_query

    @staticmethod
    def get_refined_query_generator2(tilde_query: TILDEQuery, language: TypeModeLanguage, debug_printing: bool = False):
        refined_queries = RefinementController.get_refined_queries_of(tilde_query, language, debug_printing)
        for refined_query in refined_queries:
            yield refined_query