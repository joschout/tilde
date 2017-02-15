from typing import Optional

from problog.program import SimpleProgram

from representation.example import Example
from representation.language import TypeModeLanguage
from representation.rule import TILDEQuery
import trees.scoring
import classification
import math
from trees.TreeNode import TreeNode
from typing import Iterable, Set, List


class TreeBuilder:
    """
    Builds a tree out of Examples using a Typed Mode Language and a background knowledge

    """
    background_knowledge = None  # type: Optional[SimpleProgram]
    possible_targets = None  # type: List[str]
    tree_root = TreeNode()  # type: TreeNode

    def __init__(self, language: TypeModeLanguage, background_knowledge: SimpleProgram, possible_targets: List[str]):
        self.language = language
        self.background_knowledge = background_knowledge
        self.possible_targets = possible_targets

    def build_tree(self, examples: Iterable[Example]):
        initial_tilde_query = TILDEQuery(None, None)
        self.build_tree_recursive(set(examples), initial_tilde_query, self.tree_root)

    def build_tree_recursive(self, examples: Set[Example], tilde_query: TILDEQuery, tree_node: TreeNode):
        """"
        MAKE SURE EXAMPLES IS A SET

        """

        # generating the refined queries to test
        refinement_generator = self.language.refine_conjunction_one_literal(tilde_query)
        refined_queries = []
        for refinement in refinement_generator:
            refined_queries.append(TILDEQuery(tilde_query, refinement))

        # computing which query provides the optimal split

        best_query = None
        score_best_query = - math.inf
        examples_satisfying_best_query = None
        examples_not_satisfying_best_query = None

        for q in refined_queries:
            # compute the score of the queries
            conj_of_tilde_query = q.to_conjunction()
            examples_satisfying_q = classification.get_examples_satisfying_query(examples, conj_of_tilde_query,
                                                                                self.background_knowledge)
            examples_not_satisfying_q = examples - examples_satisfying_q
            score = trees.scoring.information_gain(examples, examples_satisfying_q,
                                                   examples_not_satisfying_q, self.possible_targets)
            if score > score_best_query:
                best_query = q
                score_best_query = score
                examples_satisfying_best_query = examples_satisfying_q
                examples_not_satisfying_best_query = examples_not_satisfying_q

        # check whether to turn a node into a leaf
        # a node has to be turned into a leaf node when the set of current examples is sufficiently homogeneous
        # The set of current examples is sufficiently homogeneous when:
        stop_criterium = False
        if score_best_query < 0.001:
            stop_criterium = True

        if stop_criterium:
            # make a leaf node
            # calculate the majority class in the set of examples
            tree_node.classification = self.calculate_majority_class(examples)
        else:
            tree_node.query = best_query
            # left child node
            tree_node.left_subtree = TreeNode()
            self.build_tree_recursive(examples_satisfying_best_query, best_query, tree_node.left_subtree)

            # right child node
            tree_node.right_subtree = TreeNode()
            self.build_tree_recursive(examples_not_satisfying_best_query, tilde_query, tree_node.right_subtree)

    def get_tree(self) -> TreeNode:
        return self.tree_root

    @staticmethod
    def calculate_majority_class(examples: Iterable[Example]) -> str:
        """Calculate the majority class label in the given set of examples.
        """
        label_counts = {}
        for example in examples:
            if example.label in label_counts:
                label_counts[example.label] += 1
            else:
                label_counts[example.label] = 1
        label_with_max_count = max(label_counts, key=(lambda key: label_counts[key]))
        return label_with_max_count
