from refactor.default_interface import DefaultHandler
from refactor.tilde_essentials.example import Example
from refactor.tilde_essentials.leaf_strategy import LeafBuilder
from refactor.tilde_essentials.splitter import Splitter
from refactor.tilde_essentials.stop_criterion import StopCriterion
from refactor.tilde_essentials.tree_builder import TreeBuilder
from refactor.tilde_on_subtle.clause_handling import build_clause
from refactor.tilde_on_subtle.evaluation import SubtleQueryEvaluator
from refactor.tilde_on_subtle.test_generation import SubtleTestGeneratorBuilder
from tilde.representation.example_collection import ExampleCollection
from tilde_config import subtle_path, split_criterion


class SubtleDefaultHandler(DefaultHandler):
    @staticmethod
    def get_default_decision_tree_builder(language, prediction_goal) -> TreeBuilder:
        test_evaluator = SubtleQueryEvaluator(subtle_path())
        test_generator_builder = SubtleTestGeneratorBuilder(language=language,
                                                            query_head_if_keys_format=prediction_goal)

        splitter = Splitter(split_criterion_str=split_criterion(), test_evaluator=test_evaluator,
                            test_generator_builder=test_generator_builder)
        leaf_builder = LeafBuilder()
        stop_criterion = StopCriterion()
        tree_builder = TreeBuilder(splitter=splitter, leaf_builder=leaf_builder, stop_criterion=stop_criterion)
        return tree_builder

    @staticmethod
    def get_transformed_example_list(training_examples_collection: ExampleCollection):
        examples = []
        for ex_wr_sp in training_examples_collection.get_example_wrappers_sp():
            example_clause = build_clause(ex_wr_sp)
            example = Example(data=example_clause, label=ex_wr_sp.label)
            example.classification_term = ex_wr_sp.classification_term
            examples.append(example)
        return examples