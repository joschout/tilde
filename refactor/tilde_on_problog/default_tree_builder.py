from refactor.tilde_essentials.leaf_strategy import LeafBuilder
from refactor.tilde_essentials.splitter import Splitter
from refactor.tilde_essentials.stop_criterion import StopCriterion
from refactor.tilde_essentials.tree_builder import TreeBuilder
from refactor.tilde_on_problog.evaluation import SimpleProgramQueryEvaluator
from refactor.tilde_on_problog.test_generation import ProbLogTestGeneratorBuilder

from problog.engine import DefaultEngine

from tilde_config import split_criterion


def get_default_decision_tree_builder(language, prediction_goal) -> TreeBuilder:
    engine = DefaultEngine()
    engine.unknown = 1

    test_evaluator = SimpleProgramQueryEvaluator(engine=engine)

    test_generator_builder = ProbLogTestGeneratorBuilder(language=language,
                                                         query_head_if_keys_format=prediction_goal)
    splitter = Splitter(split_criterion_str=split_criterion(), test_evaluator=test_evaluator,
                        test_generator_builder=test_generator_builder)
    # splitter = ProblogSplitter(language=language,split_criterion_str='entropy', test_evaluator=test_evaluator,
    #                            query_head_if_keys_format=prediction_goal)
    leaf_builder = LeafBuilder()
    stop_criterion = StopCriterion()
    tree_builder = TreeBuilder(splitter=splitter, leaf_builder=leaf_builder, stop_criterion=stop_criterion)
    return tree_builder
