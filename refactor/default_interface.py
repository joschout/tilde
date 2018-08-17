from refactor.tilde_essentials.tree_builder import TreeBuilder
from tilde.representation.example_collection import ExampleCollection


class DefaultHandler:
    @staticmethod
    def get_default_decision_tree_builder(language, prediction_goal) -> TreeBuilder:
        raise NotImplementedError('abstract method')

    @staticmethod
    def get_transformed_example_list(training_examples_collection: ExampleCollection):
        raise NotImplementedError('abstract method')