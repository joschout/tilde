from typing import Optional, Tuple

from problog.engine import ClauseDB
from problog.logic import And
from problog.logic import Term
from problog.program import SimpleProgram

from representation.example import Example
from representation.language import TypeModeLanguage
from representation.TILDE_query import TILDEQuery, TILDEQueryHiddenLiteral
import trees.scoring
from classification.classification import ExamplePartitioner
import math

from trees.TreeNode import TreeNode
from typing import Iterable, Set, List

from trees.stop_criterion import StopCriterionHandler, StopCriterionMinimalCoverage


class TreeBuilder:
    """
    Builds a tree out of Examples using a Typed Mode Language and a background knowledge

    """
    possible_targets = None  # type: List[str]
    tree_root = TreeNode()  # type: TreeNode
    DEBUG_PRINTING = False
    stop_criterion_handler = None  # type: StopCriterionHandler

    def __init__(self, language: TypeModeLanguage, background_knowledge: SimpleProgram, possible_targets: List[str],
                 stop_criterion_handler: StopCriterionHandler = StopCriterionMinimalCoverage()):
        self.language = language
        self.example_partitioner = ExamplePartitioner()
        self.possible_targets = possible_targets
        self. stop_criterion_handler = stop_criterion_handler

    def debug_printing(self, should_print: bool):
        self.DEBUG_PRINTING = should_print

    def build_tree(self, examples: Iterable[ClauseDB], query_head_if_keys_format: Optional[Term] = None):

        if query_head_if_keys_format is not None:
            initial_tilde_query = TILDEQueryHiddenLiteral(query_head_if_keys_format)
        else:
            initial_tilde_query = TILDEQuery(None, None)

        if self.DEBUG_PRINTING:
            print("\n=== START recursive tree building ===")
            print('total number of examples: ', len(examples))
        self.build_tree_recursive(set(examples), initial_tilde_query, self.tree_root)
        if self.DEBUG_PRINTING:
            print("=== END recursive tree building ===\n")

    def build_tree_recursive(self, examples: Set[ClauseDB], tilde_query: TILDEQuery, tree_node: TreeNode,
                             recursion_level=0):
        """"
        MAKE SURE EXAMPLES IS A SET
        """
        if self.DEBUG_PRINTING:
            print('\nrecursion level', recursion_level)
        # generating the refined queries to test
        refined_queries = get_refined_queries_of(tilde_query, self.language)  # type: Iterable[TILDEQuery]:
        if self.DEBUG_PRINTING:
            print('generating refined queries of: ', str(tilde_query))
            print('refined queries:', list(map(str, refined_queries)))

        # computing which query provides the optimal split

        best_query, score_best_query, examples_satisfying_best_query, examples_not_satisfying_best_query \
            = get_best_refined_query(refined_queries, examples, self.example_partitioner, self.possible_targets)
        if self.DEBUG_PRINTING:
            print('best query: ', str(best_query))
            print('# examples satisfying best query: ', len(examples_satisfying_best_query))
            if examples_satisfying_best_query is not None:
                label_counts_sat = {}
                for example in examples_satisfying_best_query:
                    if example.label in label_counts_sat:
                        label_counts_sat[example.label] += 1
                    else:
                        label_counts_sat[example.label] = 1
                print('\tlabel counts:' + str(label_counts_sat))

            print('# examples not satisfying best query: ', len(examples_not_satisfying_best_query))
            if examples_not_satisfying_best_query is not None:
                label_counts_not_sat = {}
                for example in examples_not_satisfying_best_query:
                    if example.label in label_counts_not_sat:
                        label_counts_not_sat[example.label] += 1
                    else:
                        label_counts_not_sat[example.label] = 1
                print('\tlabel counts:' + str(label_counts_not_sat))

        # check whether to turn a node into a leaf
        # a node has to be turned into a leaf node when the set of current examples is sufficiently homogeneous
        # The set of current examples is sufficiently homogeneous when:
        if self.stop_criterion_handler.is_stop_criterion_reached(score_best_query, examples_satisfying_best_query, examples_not_satisfying_best_query):
            # make a leaf node
            # calculate the majority class in the set of examples
            label_with_max_count, nb_of_examples_with_label = self.calculate_majority_class(examples)
            tree_node.classification = label_with_max_count
            tree_node.nb_of_examples_with_label = nb_of_examples_with_label
            tree_node.nb_of_examples_in_this_node = len(examples)
        else:
            tree_node.query = best_query
            # left child node
            tree_node.left_subtree = TreeNode()
            self.build_tree_recursive(examples_satisfying_best_query, best_query, tree_node.left_subtree,
                                      recursion_level + 1)
            if self.DEBUG_PRINTING:
                print(self.tree_root.to_string2())

            # right child node
            tree_node.right_subtree = TreeNode()
            self.build_tree_recursive(examples_not_satisfying_best_query, tilde_query, tree_node.right_subtree,
                                      recursion_level + 1)
            if self.DEBUG_PRINTING:
                print(self.tree_root.to_string2())

    def get_tree(self) -> TreeNode:
        return self.tree_root

    @staticmethod
    def calculate_majority_class(examples: Iterable[Example]) -> Tuple[Term, int]:
        """Calculate the majority class label in the given set of examples.
        """
        label_counts = {}
        for example in examples:
            if example.label in label_counts:
                label_counts[example.label] += 1
            else:
                label_counts[example.label] = 1
        label_with_max_count = max(label_counts, key=(lambda key: label_counts[key]))  # type: Term
        count = label_counts[label_with_max_count]  # type: int
        return label_with_max_count, count


def get_refined_queries_of(tilde_query: TILDEQuery, language: TypeModeLanguage) -> Iterable[TILDEQuery]:
    # generating the refined queries to test
    refinement_generator = language.refine_conjunction_one_literal(tilde_query)
    refined_queries = []  # type: List[TILDEQuery]
    for refinement in refinement_generator:  # type: Term
        refined_query = TILDEQuery(tilde_query, refinement)
        refined_queries.append(refined_query)
    return refined_queries


def get_best_refined_query(refined_queries: Iterable[TILDEQuery], examples: Set[Example],
                           example_partitioner: ExamplePartitioner, possible_targets: List[str]) -> Tuple[
                            Optional[TILDEQuery], float, Optional[Set[Example]], Optional[Set[Example]]]:
    best_query = None  # type: Optional[TILDEQuery]
    score_best_query = - math.inf  # type: float
    examples_satisfying_best_query = set()  # type: Optional[Set[Example]]
    examples_not_satisfying_best_query = set()  # type: Optional[Set[Example]]

    for q in refined_queries:  # type: TILDEQuery
        # compute the score of the queries
        conj_of_tilde_query = q.to_conjunction()  # type: And

        examples_satisfying_q = example_partitioner.get_examples_satisfying_query(examples, conj_of_tilde_query)  # type: Set[Example]
        examples_not_satisfying_q = examples - examples_satisfying_q  # type: Set[Example]
        score = trees.scoring.information_gain(examples, examples_satisfying_q,
                                               examples_not_satisfying_q, possible_targets)

        if score > score_best_query:
            best_query = q
            score_best_query = score
            examples_satisfying_best_query = examples_satisfying_q
            examples_not_satisfying_best_query = examples_not_satisfying_q

    if '21'in str(best_query):
        print("breakpoint here")
    return best_query, score_best_query, examples_satisfying_best_query, examples_not_satisfying_best_query
