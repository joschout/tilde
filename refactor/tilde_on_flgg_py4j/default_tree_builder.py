from py4j.java_gateway import JavaGateway

from refactor.tilde_essentials.leaf_strategy import LeafBuilder
from refactor.tilde_essentials.splitter import Splitter
from refactor.tilde_essentials.stop_criterion import StopCriterion
from refactor.tilde_essentials.tree_builder import TreeBuilder
from refactor.tilde_on_flgg_py4j.evaluation import FLGGQueryEvaluator
from refactor.tilde_on_flgg_py4j.test_generation import FLGGTestGeneratorBuilder
from tilde_config import split_criterion


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
