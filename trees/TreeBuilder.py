from typing import Optional, Tuple

from problog.logic import And
from problog.logic import Term
from problog.program import SimpleProgram

from representation.example import Example
from representation.language import TypeModeLanguage
from representation.TILDE_query import TILDEQuery
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
        refined_queries = get_refined_queries_of(tilde_query, self.language)

        # computing which query provides the optimal split

        best_query, score_best_query, examples_satisfying_best_query, examples_not_satisfying_best_query \
            = get_best_refined_query(refined_queries, examples, self.background_knowledge, self.possible_targets)

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


def get_refined_queries_of(tilde_query: TILDEQuery, language: TypeModeLanguage) -> Iterable[TILDEQuery]:
    # generating the refined queries to test
    refinement_generator = language.refine_conjunction_one_literal(tilde_query)
    refined_queries = []  # type: List[TILDEQuery]
    for refinement in refinement_generator:  # type: Term
        refined_query = TILDEQuery(tilde_query, refinement)
        refined_queries.append(refined_query)
    return refined_queries


def get_best_refined_query(refined_queries: Iterable[TILDEQuery], examples: Set[Example],
                           background_knowledge: SimpleProgram, possible_targets: List[str]) -> Tuple[Optional[TILDEQuery], float, Optional[Set[Example]], Optional[Set[Example]]]:
    best_query = None  # type: Optional[TILDEQuery]
    score_best_query = - math.inf  # type: float
    examples_satisfying_best_query = None  # type: Optional[Set[Example]]
    examples_not_satisfying_best_query = None  # type: Optional[Set[Example]]

    for q in refined_queries:  # type: TILDEQuery
        # compute the score of the queries
        conj_of_tilde_query = q.to_conjunction()  # type: And
        examples_satisfying_q = classification.get_examples_satisfying_query(examples, conj_of_tilde_query,
                                                                             background_knowledge)  # type: Set[Example]
        examples_not_satisfying_q = examples - examples_satisfying_q
        score = trees.scoring.information_gain(examples, examples_satisfying_q,
                                               examples_not_satisfying_q, possible_targets)
        if score > score_best_query:
            best_query = q
            score_best_query = score
            examples_satisfying_best_query = examples_satisfying_q
            examples_not_satisfying_best_query = examples_not_satisfying_q

    return best_query, score_best_query, examples_satisfying_best_query, examples_not_satisfying_best_query
