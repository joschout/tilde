from enum import Enum
from typing import Iterable, List, Optional, Set

from problog.logic import Term

from tilde.classification.example_partitioning import ExamplePartitioner
from tilde.representation.language import TypeModeLanguage
from tilde.trees.RefinementController import RefinementController

from tilde.trees.TILDEQueryScorer import QueryScoreInfo, TILDEQueryScorer

# python 3.6
try:
    from typing import Collection
except ImportError:
    Collection = Iterable

from tilde.representation.TILDE_query import TILDEQueryHiddenLiteral, TILDEQuery
from tilde.representation.example import calculate_majority_class, calculate_label_frequencies_and_absolute_counts, \
    ExampleWrapper, Label

from tilde.trees.TreeBuilder_helper import print_partition_subset_sizes
from tilde.trees.TreeBuilder_helper_probabilistic import print_partition_statistics_prob, \
    create_probabilistic_leaf_node
from tilde.trees.TreeNode import TreeNode
from tilde.trees.leaf_strategy import DeterministicLeafStrategy, MLEDeterministicLeafStrategy
from tilde.trees.stop_criterion import StopCriterionHandler, StopCriterionMinimalCoverage


class TreeBuilder:
    """
    Builds a tree out of Examples using a Typed Mode Language and a background knowledge

    """
    possible_targets = None  # type: List[Label]
    tree_root = TreeNode()  # type: TreeNode
    DEBUG_PRINTING = False  # type: bool
    stop_criterion_handler = None  # type: StopCriterionHandler

    def __init__(self, language: TypeModeLanguage, possible_targets: List[Label],
                 example_partitioner: ExamplePartitioner,
                 stop_criterion_handler: StopCriterionHandler = StopCriterionMinimalCoverage()):
        self.language = language
        self.example_partitioner = example_partitioner
        self.possible_targets = possible_targets
        self.stop_criterion_handler = stop_criterion_handler

    def debug_printing(self, should_print: bool):
        self.DEBUG_PRINTING = should_print

    def build_tree(self, examples: Collection[ExampleWrapper], query_head_if_keys_format: Optional[Term] = None):

        initial_tilde_query = self.__get_initial_query(query_head_if_keys_format)

        if self.DEBUG_PRINTING:
            print("\n=== START recursive tree building ===")
            print('total number of examples: ', len(examples))
        self._build_tree_recursive(set(examples), initial_tilde_query, self.tree_root)
        if self.DEBUG_PRINTING:
            print("=== END recursive tree building ===\n")

    @staticmethod
    def __get_initial_query(query_head_if_keys_format: Optional[Term] = None) -> TILDEQuery:
        if query_head_if_keys_format is not None:
            return TILDEQueryHiddenLiteral(query_head_if_keys_format)
        else:
            return TILDEQuery(None, None)

    def _build_tree_recursive(self, examples: Set[ExampleWrapper], tilde_query: TILDEQuery, tree_node: TreeNode,
                              recursion_level=0):
        # MAKE SURE EXAMPLES IS A SET
        if self.DEBUG_PRINTING:
            print('\nrecursion level', recursion_level)

        # generating the refined queries to test
        refined_queries = self._get_refined_queries_of(tilde_query)  # type: Iterable[TILDEQuery]
        score_info = self._score_queries(refined_queries, examples)  # type: QueryScoreInfo

        # check whether to turn a node into a leaf
        # a node has to be turned into a leaf node when the set of current examples is sufficiently homogeneous
        if self._stop_criterion(score_info):
            self._turn_node_into_leaf(tree_node, examples)
        else:
            self._turn_into_inner_node(tree_node, tilde_query, score_info, recursion_level + 1)

    def _get_refined_queries_of(self, query: TILDEQuery) -> Iterable[TILDEQuery]:
        return RefinementController.get_refined_queries_of(query, self.language)

    def _turn_node_into_leaf(self, tree_node: TreeNode, examples: Set[ExampleWrapper]):
        raise NotImplementedError('abstract method')

    def _turn_into_inner_node(self, tree_node: TreeNode, parent_query: TILDEQuery, score_info: QueryScoreInfo,
                              recursion_level_of_node):
        tree_node.query = score_info.best_query  # type: TILDEQuery
        # left child node
        tree_node.left_subtree = TreeNode()
        self._build_tree_recursive(score_info.examples_satisfying_best_query, score_info.best_query,
                                   tree_node.left_subtree,
                                   recursion_level_of_node)
        if self.DEBUG_PRINTING:
            print(str(self.tree_root))

        # right child node
        tree_node.right_subtree = TreeNode()
        self._build_tree_recursive(score_info.examples_not_satisfying_best_query, parent_query, tree_node.right_subtree,
                                   recursion_level_of_node)
        if self.DEBUG_PRINTING:
            print(str(self.tree_root))

    def _score_queries(self, refined_queries: Iterable[TILDEQuery], examples: Set[ExampleWrapper]) -> QueryScoreInfo:
        # computing which query provides the optimal split
        raise NotImplementedError('abstract method')

    def _stop_criterion(self, score: QueryScoreInfo) -> bool:
        return self.stop_criterion_handler.is_stop_criterion_reached(score.score_of_best_query,
                                                                     score.examples_satisfying_best_query,
                                                                     score.examples_not_satisfying_best_query)

    def get_tree(self) -> TreeNode:
        return self.tree_root


class DeterministicTreeBuilder(TreeBuilder):
    """
    Builds a regular relational decision tree for classification,
    where each leaf has one class label.
    """

    def __init__(self, language: TypeModeLanguage, possible_targets: List[Label],
                 example_partitioner: ExamplePartitioner,
                 stop_criterion_handler: StopCriterionHandler = StopCriterionMinimalCoverage()):
        super().__init__(language, possible_targets, example_partitioner, stop_criterion_handler)

    def _turn_node_into_leaf(self, tree_node: TreeNode, examples: Set[ExampleWrapper]):
        # make a leaf node
        # calculate the majority class in the set of examples
        label_with_max_count, nb_of_examples_with_label = calculate_majority_class(examples)
        tree_node.strategy = DeterministicLeafStrategy(label_with_max_count, nb_of_examples_with_label, len(examples))

    def _score_queries(self, refined_queries: Iterable[TILDEQuery], examples: Set[ExampleWrapper]) -> QueryScoreInfo:
        # computing which query provides the optimal split
        score_info = TILDEQueryScorer.get_best_refined_query(refined_queries, examples, self.example_partitioner,
                                                             self.possible_targets)
        if self.DEBUG_PRINTING:
            print('best query: ', str(score_info.best_query))
            print_partition_subset_sizes(score_info.examples_satisfying_best_query,
                                         score_info.examples_not_satisfying_best_query)

        return score_info


class MLEDeterministicTreeBuilder(TreeBuilder):
    def __init__(self, language: TypeModeLanguage, possible_targets: List[Label],
                 example_partitioner: ExamplePartitioner,
                 stop_criterion_handler: StopCriterionHandler = StopCriterionMinimalCoverage()):
        super().__init__(language, possible_targets, example_partitioner, stop_criterion_handler)

    def _turn_node_into_leaf(self, tree_node: TreeNode, examples: Set[ExampleWrapper]):
        # make a leaf node
        # calculate the majority class in the set of examples
        label_frequencies, label_absolute_counts = calculate_label_frequencies_and_absolute_counts(examples)
        tree_node.strategy = MLEDeterministicLeafStrategy(label_frequencies, label_absolute_counts)

    def _score_queries(self, refined_queries: Iterable[TILDEQuery], examples: Set[ExampleWrapper]) -> QueryScoreInfo:
        # computing which query provides the optimal split
        score_info = TILDEQueryScorer.get_best_refined_query(refined_queries, examples, self.example_partitioner,
                                                             self.possible_targets)
        if self.DEBUG_PRINTING:
            print('best query: ', str(score_info.best_query))
            print_partition_subset_sizes(score_info.examples_satisfying_best_query,
                                         score_info.examples_not_satisfying_best_query)

        return score_info


class ProbabilisticTreeBuilder(TreeBuilder):
    def __init__(self, language: TypeModeLanguage, possible_targets: List[Label],
                 example_partitioner: ExamplePartitioner,
                 stop_criterion_handler: StopCriterionHandler = StopCriterionMinimalCoverage()):
        super().__init__(language, possible_targets, example_partitioner, stop_criterion_handler)

    def _turn_node_into_leaf(self, tree_node: TreeNode, examples: Set[ExampleWrapper]):
        # make a leaf node
        # TODO
        create_probabilistic_leaf_node(tree_node, examples, self.possible_targets)
        tree_node.nb_of_examples_in_this_node = len(examples)

    def _score_queries(self, refined_queries: Iterable[TILDEQuery], examples: Set[ExampleWrapper]) -> QueryScoreInfo:
        # computing which query provides the optimal split
        score_info = TILDEQueryScorer.get_best_refined_query(refined_queries, examples, self.example_partitioner,
                                                             self.possible_targets, probabilistic=True)

        if self.DEBUG_PRINTING:
            print('best query: ', str(score_info.best_query))
            print_partition_statistics_prob(score_info.examples_satisfying_best_query,
                                            score_info.examples_not_satisfying_best_query,
                                            self.possible_targets, "\t")
        return score_info


class TreeBuilderType(Enum):
    DETERMINISTIC = 1
    MLEDETERMINISTIC = 2
    PROBABILISITC = 3


class TreeBuilderBuilder:
    # TODO: misschien heeft het voordeel om het type al bij init mee te geven

    def build_treebuilder(self, tree_builder_type: TreeBuilderType,
                          language: TypeModeLanguage, possible_labels: List[Label],
                          example_partitioner: ExamplePartitioner,
                          stop_criterion_handler: StopCriterionHandler = StopCriterionMinimalCoverage()
                          ) -> TreeBuilder:
        if tree_builder_type is TreeBuilderType.DETERMINISTIC:
            return DeterministicTreeBuilder(language, possible_labels, example_partitioner, stop_criterion_handler)
        elif tree_builder_type is TreeBuilderType.MLEDETERMINISTIC:
            return MLEDeterministicTreeBuilder(language, possible_labels, example_partitioner, stop_criterion_handler)
        elif tree_builder_type is TreeBuilderType.PROBABILISITC:
            raise NotImplementedError('No defined treebuilder choice for: ' + str(tree_builder_type))
        else:
            raise NotImplementedError('No defined treebuilder choice for: ' + str(tree_builder_type))
