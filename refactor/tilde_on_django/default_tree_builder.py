from refactor.tilde_essentials.leaf_strategy import LeafBuilder
from refactor.tilde_essentials.stop_criterion import StopCriterion
from refactor.tilde_essentials.tree_builder import TreeBuilder
from refactor.tilde_on_django.evaluation import DjangoQueryEvaluator
from refactor.tilde_on_django.splitter import DjangoSplitter
from refactor.tilde_on_django.test_generation import DjangoTestGeneratorBuilder
from tilde_config import split_criterion


def get_default_decision_tree_builder(language, prediction_goal) -> TreeBuilder:
    test_evaluator = DjangoQueryEvaluator()
    test_generator_builder = DjangoTestGeneratorBuilder(language=language,
                                                        query_head_if_keys_format=prediction_goal)

    splitter = DjangoSplitter(split_criterion_str=split_criterion(), test_evaluator=test_evaluator,
                              test_generator_builder=test_generator_builder)
    leaf_builder = LeafBuilder()
    stop_criterion = StopCriterion()
    tree_builder = TreeBuilder(splitter=splitter, leaf_builder=leaf_builder, stop_criterion=stop_criterion)
    return tree_builder
