from typing import Optional

from problog.logic import Term

from refactor.tilde_essentials.test_generation import FOLTestGeneratorBuilder
from refactor.query_testing_back_end.django.clause_handling import build_hypothesis
try:
    from src.ClauseWrapper import HypothesisWrapper
except ImportError as err:
    from refactor.query_testing_back_end.django.django_wrapper.ClauseWrapper import HypothesisWrapper

from refactor.representation.TILDE_query import TILDEQuery, TILDEQueryHiddenLiteral
from refactor.representation.language import TypeModeLanguage
from refactor.tilde_essentials.refinement_controller import RefinementController


class DjangoTestGeneratorBuilder(FOLTestGeneratorBuilder):
    def __init__(self, language: TypeModeLanguage,
                 query_head_if_keys_format: Optional[Term] = None):
        super().__init__(DjangoTestGeneratorBuilder.get_initial_query(query_head_if_keys_format))
        self.language = language

    def generate_possible_tests(self, examples, current_node):
        hypothesis_wrapper_query_to_refine = self._get_associated_query(current_node)  # type: HypothesisWrapper
        query_to_refine = hypothesis_wrapper_query_to_refine._prolog_hypothesis
        generator = RefinementController.get_refined_query_generator(
            query_to_refine, self.language)
        for tilde_query in generator:
            # turn TILDEQuery into a HypothesisWrapper
            hypothesis_wrapper = build_hypothesis(tilde_query)
            yield hypothesis_wrapper

    @staticmethod
    def get_initial_query(query_head_if_keys_format: Optional[Term] = None):
        if query_head_if_keys_format is not None:
            initial_tilde_query = TILDEQueryHiddenLiteral(query_head_if_keys_format)
        else:
            initial_tilde_query = TILDEQuery(None, None)

        hypothesis_wrapper_initial_query = build_hypothesis(initial_tilde_query)

        return hypothesis_wrapper_initial_query
