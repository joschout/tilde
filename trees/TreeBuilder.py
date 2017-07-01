from problog.logic import Term

from representation.TILDE_query import TILDEQueryHiddenLiteral
from representation.example import calculate_majority_class
from trees.RefinementController import *
from trees.TILDEQueryScorer import *
from trees.TreeBuilder_helper import print_partition_subset_sizes
from trees.TreeBuilder_helper_probabilistic import print_partition_statistics_prob, \
    create_probabilistic_leaf_node
from trees.TreeNode import TreeNode
from trees.stop_criterion import StopCriterionHandler, StopCriterionMinimalCoverage


class TreeBuilder:
    """
    Builds a tree out of Examples using a Typed Mode Language and a background knowledge

    """
    possible_targets = None  # type: List[Label]
    tree_root = TreeNode()  # type: TreeNode
    DEBUG_PRINTING = False  # type: bool
    stop_criterion_handler = None  # type: StopCriterionHandler

    probabilistic_tree_building = False  # type: bool
    DEBUG_PRINTING_PROBABILISTIC = True  # type: bool

    def __init__(self, language: TypeModeLanguage, possible_targets: List[Label],
                 example_partitioner: ExamplePartitioner,
                 stop_criterion_handler: StopCriterionHandler = StopCriterionMinimalCoverage(),
                 probabilistic_tree_building: Optional[bool] = False):
        self.language = language
        self.example_partitioner = example_partitioner
        self.possible_targets = possible_targets
        self.stop_criterion_handler = stop_criterion_handler
        self.probabilistic_tree_building = probabilistic_tree_building

    def debug_printing(self, should_print: bool):
        self.DEBUG_PRINTING = should_print

    def build_tree(self, examples: Iterable[Example], query_head_if_keys_format: Optional[Term] = None):

        if query_head_if_keys_format is not None:
            initial_tilde_query = TILDEQueryHiddenLiteral(query_head_if_keys_format)
        else:
            initial_tilde_query = TILDEQuery(None, None)

        if self.DEBUG_PRINTING:
            print("\n=== START recursive tree building ===")
            print('total number of examples: ', len(examples))
        self._build_tree_recursive(set(examples), initial_tilde_query, self.tree_root)
        if self.DEBUG_PRINTING:
            print("=== END recursive tree building ===\n")

    def _build_tree_recursive(self, examples: Set[Example], tilde_query: TILDEQuery, tree_node: TreeNode,
                              recursion_level=0):
        """"
        MAKE SURE EXAMPLES IS A SET
        """
        if self.DEBUG_PRINTING:
            print('\nrecursion level', recursion_level)
        # generating the refined queries to test
        refined_queries = RefinementController.get_refined_queries_of(tilde_query,
                                                                      self.language)  # type: Iterable[TILDEQuery]:
        # computing which query provides the optimal split

        best_query, score_best_query, examples_satisfying_best_query, examples_not_satisfying_best_query \
            = TILDEQueryScorer.get_best_refined_query(refined_queries, examples, self.example_partitioner,
                                                      self.possible_targets, self.probabilistic_tree_building)
        if self.DEBUG_PRINTING:
            print('best query: ', str(best_query))
            if self.probabilistic_tree_building:
                print_partition_statistics_prob(examples_satisfying_best_query, examples_not_satisfying_best_query,
                                                self.possible_targets, "\t")
            else:
                print_partition_subset_sizes(examples_satisfying_best_query, examples_not_satisfying_best_query)

        # check whether to turn a node into a leaf
        # a node has to be turned into a leaf node when the set of current examples is sufficiently homogeneous
        # The set of current examples is sufficiently homogeneous when:
        if self.stop_criterion_handler.is_stop_criterion_reached(score_best_query, examples_satisfying_best_query,
                                                                 examples_not_satisfying_best_query):
            self._turn_node_into_leaf(tree_node, examples)
        else:
            self._turn_into_inner_node(tree_node, best_query, tilde_query, examples_satisfying_best_query, examples_not_satisfying_best_query, recursion_level + 1)

    def _turn_node_into_leaf(self, tree_node: TreeNode, examples: Set[Example]):

        # make a leaf node
        # calculate the majority class in the set of examples
        if not self.probabilistic_tree_building:
            label_with_max_count, nb_of_examples_with_label = calculate_majority_class(examples)
            tree_node.classification = label_with_max_count
            tree_node.nb_of_examples_with_label = nb_of_examples_with_label
            tree_node.nb_of_examples_in_this_node = len(examples)
        else:
            # TODO
            create_probabilistic_leaf_node(tree_node, examples, self.possible_targets)
            tree_node.nb_of_examples_in_this_node = len(examples)

    def _turn_into_inner_node(self, tree_node: TreeNode, refined_query: TILDEQuery, parent_query: TILDEQuery,
                              examples_satisfying_best_query: Set[Example],
                              examples_not_satisfying_best_query: Set[Example],
                              recursion_level_of_node):
        tree_node.query = refined_query
        # left child node
        tree_node.left_subtree = TreeNode()
        self._build_tree_recursive(examples_satisfying_best_query, refined_query, tree_node.left_subtree,
                                   recursion_level_of_node)
        if self.DEBUG_PRINTING:
            print(self.tree_root.to_string2())

        # right child node
        tree_node.right_subtree = TreeNode()
        self._build_tree_recursive(examples_not_satisfying_best_query, parent_query, tree_node.right_subtree,
                                   recursion_level_of_node)
        if self.DEBUG_PRINTING:
            print(self.tree_root.to_string2())

    def get_tree(self) -> TreeNode:
        return self.tree_root
