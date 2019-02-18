from py4j.java_gateway import JavaGateway

from refactor.default_interface import DefaultHandler
from refactor.tilde_essentials.example import Example
from refactor.tilde_essentials.leaf_strategy import LeafBuilder
from refactor.tilde_essentials.splitter import Splitter
from refactor.tilde_essentials.stop_criterion import StopCriterion
from refactor.tilde_essentials.tree_builder import TreeBuilder
from refactor.query_testing_back_end.flgg_py4j.clause_handling import build_clause
from refactor.query_testing_back_end.flgg_py4j.evaluation import FLGGQueryEvaluator
from refactor.query_testing_back_end.flgg_py4j.test_generation import FLGGTestGeneratorBuilder
from refactor.representation.example_collection import ExampleCollection
from tilde_config import split_criterion


class FLGGDefaultHandler(DefaultHandler):
    @staticmethod
    def get_default_decision_tree_builder(language, prediction_goal) -> TreeBuilder:
        java_gateway = JavaGateway()
        test_evaluator = FLGGQueryEvaluator(java_gateway)
        test_generator_builder = FLGGTestGeneratorBuilder(language=language,
                                                          query_head_if_keys_format=prediction_goal)

        splitter = Splitter(split_criterion_str=split_criterion(), test_evaluator=test_evaluator,
                            test_generator_builder=test_generator_builder)
        leaf_builder = LeafBuilder()
        stop_criterion = StopCriterion()
        tree_builder = TreeBuilder(splitter=splitter, leaf_builder=leaf_builder, stop_criterion=stop_criterion)
        return tree_builder

    @staticmethod
    def get_transformed_example_list(training_examples_collection: ExampleCollection, training=False):
        examples = []
        for ex_wr_sp in training_examples_collection.get_example_wrappers_sp():
            example_clause = build_clause(ex_wr_sp, training=False)
            example = Example(data=example_clause, label=ex_wr_sp.label)
            example.classification_term = ex_wr_sp.classification_term
            examples.append(example)
        return examples

    @staticmethod
    def get_transformed_test_example_list(simple_example_wrapper_list, training=False):
        test_examples_reformed = []
        for ex_wr_sp in simple_example_wrapper_list:
            example_clause = build_clause(ex_wr_sp, training=False)
            example = Example(data=example_clause, label=ex_wr_sp.label)
            example.classification_term = ex_wr_sp.classification_term
            test_examples_reformed.append(example)
        return test_examples_reformed

