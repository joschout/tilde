from typing import Optional

from problog.logic import Term

from refactor.tilde_essentials.test_generation import FOLTestGeneratorBuilder
from refactor.query_testing_back_end.subtle.clause_handling import build_hypothesis
from refactor.query_testing_back_end.subtle.query_wrapping import SubtleQueryWrapper
from refactor.representation.TILDE_query import TILDEQueryHiddenLiteral, TILDEQuery
from refactor.representation.language import TypeModeLanguage
from refactor.tilde_essentials.refinement_controller import RefinementController


class SubtleTestGeneratorBuilder(FOLTestGeneratorBuilder):
    def __init__(self, language: TypeModeLanguage,
                 query_head_if_keys_format: Optional[Term] = None):
        super().__init__(SubtleTestGeneratorBuilder.get_initial_query(query_head_if_keys_format))
        self.language = language

    def generate_possible_tests(self, examples, current_node):
        query_wrapper = self._get_associated_query(current_node)  # type: SubtleQueryWrapper
        query_to_refine = query_wrapper.tilde_query  # type: TILDEQuery
        generator = RefinementController.get_refined_query_generator(
            query_to_refine, self.language)
        for tilde_query in generator:
            tilde_query_str = build_hypothesis(tilde_query)  # type: str
            yield SubtleQueryWrapper(tilde_query, tilde_query_str)

    @staticmethod
    def get_initial_query(query_head_if_keys_format: Optional[Term] = None):
        if query_head_if_keys_format is not None:
            initial_tilde_query = TILDEQueryHiddenLiteral(query_head_if_keys_format)
        else:
            initial_tilde_query = TILDEQuery(None, None)

        wrapper_initial_tilde_query = SubtleQueryWrapper(initial_tilde_query, build_hypothesis(initial_tilde_query))

        return wrapper_initial_tilde_query
