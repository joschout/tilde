from typing import Optional

from refactor.tilde_essentials.evaluation import TestEvaluator
from refactor.tilde_essentials.tree_builder import TreeBuilder
from refactor.tilde_essentials.tree_node import TreeNode


class DecisionTree:
    """
    Decision tree used for making predictions. Initially empty.
    An internal TreeNode tree is fitted on training examples using a TreeBuilder.

    """

    def __init__(self):
        self.tree = None  # type: Optional[TreeNode]
        self.tree_builder = None  # type: Optional[TreeBuilder]
        self.test_evaluator = None  # type: Optional[TestEvaluator]
        self.tree_pruner = None

    def fit(self, examples, tree_builder: TreeBuilder):
        self.tree_builder = tree_builder
        self.tree_builder.build(examples)
        self.test_evaluator = self.tree_builder.splitter.test_evaluator
        self.tree = tree_builder.tree_root

        if self.tree_pruner is not None:
            self.tree = self.tree_pruner.prune(self.tree)

    def predict(self, example):
        return self._predict_recursive(example, self.tree)

    def _predict_recursive(self, example, tree_node: TreeNode):
        if tree_node.is_leaf_node():
            return tree_node.leaf_strategy.predict(example)
        else:
            succeeds_test = self.test_evaluator.evaluate(example, tree_node.test)
            if succeeds_test:
                self._predict_recursive(example, tree_node.left_child)
            else:
                self._predict_recursive(example, tree_node.right_child)

    def __str__(self):
        return self.tree.__str__()
