from refactor.tilde_essentials.tree_builder import TreeBuilder
from mai_version.representation.example_collection import ExampleCollection


class DefaultHandler:

    def __init__(self, back_end_name: str):
        self.back_end_name = back_end_name

    @staticmethod
    def get_default_decision_tree_builder(language, prediction_goal) -> TreeBuilder:
        raise NotImplementedError('abstract method')

    @staticmethod
    def get_transformed_example_list(training_examples_collection: ExampleCollection, training=False):
        raise NotImplementedError('abstract method')

    @staticmethod
    def get_transformed_test_example_list(simple_example_wrapper_list, training=True):
        raise NotImplementedError('abstract method')


