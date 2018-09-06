from refactor.tilde_essentials.evaluation import TestEvaluator
from refactor.tilde_essentials.example import Example
try:
    from src.ClauseWrapper import ClauseWrapper, HypothesisWrapper
    from src.subsumption_checking import check_subsumption
except ImportError as err:
    from refactor.query_testing_back_end.django.django_wrapper.ClauseWrapper import ClauseWrapper, HypothesisWrapper
    from refactor.query_testing_back_end.django.django_wrapper.subsumption_checking import check_subsumption


class DjangoQueryEvaluator(TestEvaluator):
    def evaluate(self, example: Example, test: HypothesisWrapper) -> bool:
        example_clause_wrapper = example.data  # type: ClauseWrapper

        does_subsume, run_time_ms = check_subsumption(test, example_clause_wrapper)
        return does_subsume
