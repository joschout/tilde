from py4j.java_gateway import JavaGateway

from refactor.tilde_essentials.evaluation import TestEvaluator
from refactor.tilde_essentials.example import Example
from refactor.tilde_essentials.query_wrapping import QueryWrapper


class FLGGQueryEvaluator(TestEvaluator):
    def __init__(self, gateway: JavaGateway):
        self.subsumption_engine = gateway.entry_point

    def evaluate(self, example: Example, test: QueryWrapper) -> bool:
        example_string = example.data
        query_string = test.external_representation

        does_subsume = self.subsumption_engine.subsumes(query_string, example_string)
        return does_subsume
