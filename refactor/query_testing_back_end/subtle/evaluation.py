from typing import Optional

from pyswip import Prolog

from refactor.tilde_essentials.evaluation import TestEvaluator
from refactor.tilde_essentials.example import Example
from refactor.tilde_essentials.query_wrapping import QueryWrapper


class SubtleQueryEvaluator(TestEvaluator):
    @staticmethod
    def build(subtle_path: str)-> 'SubtleQueryEvaluator':
            prolog = Prolog()
            prolog.consult(subtle_path)
            return SubtleQueryEvaluator(prolog)

    def __init__(self, prolog:Prolog):
        self.prolog=prolog

        self.subsumes_str = "subsumes({subsumer},{subsumee})"

    def _subsumes(self, test_str, example_str):
        query_results_list = list(self.prolog.query(
            self.subsumes_str.format(
                subsumer=test_str, subsumee=example_str)))
        if query_results_list:  # dictionary is False if empty
            return True
        else:
            return False

    def evaluate(self, example: Example, test: QueryWrapper) -> bool:
        example_string = example.data  # type: str
        query_string = test.external_representation  # type: str

        does_subsume = self._subsumes(query_string, example_string)
        return does_subsume


def _main():
    subsumer_string = '[p(X),q(X)]'
    subsubsumee_string = '[p(a),p(b),q(c),q(a)]'

    query_str = "subsumes({subsumer},{subsumee})".format(
        subsumer=subsumer_string, subsumee=subsubsumee_string)

    print(query_str)
