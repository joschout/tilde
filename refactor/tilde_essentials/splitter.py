from typing import Optional

from refactor.tilde_essentials.evaluation import TestEvaluator
from refactor.tilde_essentials.split_criterion import SplitCriterionBuilder
from refactor.tilde_essentials.test_generation import TestGeneratorBuilder
from refactor.tilde_essentials.tree_node import TreeNode


class SplitInfo:
    """
    Contains the information about a split using a test on a set of training examples.

    """

    def __init__(self,
                 test,
                 examples_left,
                 examples_right,
                 score,
                 threshold,
                 split_criterion):
        self.test = test
        self.examples_left = examples_left
        self.examples_right = examples_right
        self.score = score
        self.threshold = threshold
        self.split_criterion = split_criterion

    # def get_test(self):
    #     return self.test
    #
    # @property
    # def get_examples_left(self):
    #     return self.examples_left
    #
    # def get_examples_right(self):
    #     raise NotImplementedError('abstract method')
    #
    # def get_score(self) -> float:
    #     raise NotImplementedError('abstract method')

    def get_split_criterion(self) -> str:
        """
        Returns 'gini' for Gini index, 'entropy' for information gain,
        'MSE' for mean squared error and 'MSA' for Mean Absolute Error
        :return:
        """
        raise NotImplementedError('abstract method')

    def passing_score(self) -> bool:
        return self.score >= self.threshold


class Splitter:
    """
    Finds the best test for splitting a node based on the node's training examples.
    It must be initialized with a SplitCriterion and TestEvaluator.
    Reports the split info using a SplitInfo object.
    """

    def __init__(self, split_criterion_str, test_evaluator: TestEvaluator,
                 test_generator_builder: TestGeneratorBuilder, verbose=False):
        self.split_criterion_str = split_criterion_str
        self.test_evaluator = test_evaluator
        self.test_generator_builder = test_generator_builder
        self.verbose=verbose

    def get_split(self, examples, current_node: TreeNode) -> Optional[SplitInfo]:
        current_best_split_info = None
        split_criterion = SplitCriterionBuilder.get_split_criterion(
            self.split_criterion_str,
            examples, current_node.get_labels(examples))

        generator = self.test_generator_builder.generate_possible_tests(examples, current_node)
        for candidate_test in generator:
            if self.verbose:
                print(candidate_test)
            examples_satisfying_test, examples_not_satisfying_test = self._split_examples(candidate_test, examples)

            candidate_test_score = split_criterion.calculate(examples_satisfying_test,
                                                             examples_not_satisfying_test
                                                             )
            if current_best_split_info is None or candidate_test_score > current_best_split_info.score:
                current_best_split_info = SplitInfo(test=candidate_test,
                                                    examples_left=examples_satisfying_test,
                                                    examples_right=examples_not_satisfying_test,
                                                    score=candidate_test_score,
                                                    threshold=split_criterion.get_threshold(),
                                                    split_criterion=split_criterion.get_name())
            # elif candidate_test_score > current_best_split_info.score:
            #     current_best_split_info = SplitInfo(test=can)
            #     current_best_split_info.test = candidate_test
            #     current_best_split_info.examples_left = examples_satisfying_test
            #     current_best_split_info.examples_right = examples_not_satisfying_test

        return current_best_split_info

    def _split_examples(self, test, examples):
        examples_satisfying_test = set()
        examples_not_satifying_test = set()

        for example in examples:
            succeeds_test = self.test_evaluator.evaluate(example, test)
            if succeeds_test:
                examples_satisfying_test.add(example)
            else:
                examples_not_satifying_test.add(example)
        return examples_satisfying_test, examples_not_satifying_test

