from typing import Optional, Iterator, Dict

from problog.logic import *
# class PredicateGenerator:
#     count = 0
#
#     def __init__(self, language):
#         self.language = language
from representation.language import TypeModeLanguage

from tilde.representation.TILDE_query import TILDEQuery


def get_predicate_generator(language: TypeModeLanguage) -> Iterator[Term]:
    count = 0  # type: int
    while True:
        new_name_found = False
        while not new_name_found:
            name = 'pred%d' % count
            count += 1
            if not language.does_predicate_exist(name, 1):
                new_name_found = True
        yield Term(name)


class LeafStrategy:
    def to_string(self, node_indentation) -> str:
        raise NotImplementedError('abstract method')

    def can_classify(self) -> object:
        raise NotImplementedError('abstract method')

    # def get_leaf_clause(self, previous_conjunction) -> Clause:
    #     raise NotImplementedError('abstract method')


class TreeNode:
    """A node in a First-Order Logical Decision Tree.

    There are two kinds of nodes: decision nodes and leaf nodes"""
    left_subtree = None  # type: Optional[TreeNode]
    right_subtree = None  # type: Optional[TreeNode]
    nb_of_examples_with_label = None  # type: Optional[int]
    nb_of_examples_in_this_node = None  # type: Optional[int]

    strategy = None  # type: Optional[LeafStrategy]

    query = None  # type: Optional[TILDEQuery]

    def get_left_child_node(self) -> 'TreeNode':
        return self.left_subtree

    def get_right_child_node(self) -> 'TreeNode':
        return self.right_subtree

    def has_both_children(self) -> bool:
        return self.left_subtree is not None and self.right_subtree is not None

    def is_leaf_node(self) -> bool:
        return self.left_subtree is None and self.right_subtree is None

    def to_string(self, indentation='', current_node_number=0):
        """
        Represents the tree as a string using some layouting
        :param indentation:
        :param current_node_number:
        :return:
        """
        node_indentation = indentation
        child_indentation = indentation

        if current_node_number == 0:
            child_indentation = '\t'
        elif current_node_number == 1:
            node_indentation += '|-'
            child_indentation += '|\t'
        else:
            node_indentation += '\-'
            child_indentation += '\t'

        if self.is_leaf_node():
            result = self.strategy.to_string(node_indentation)
            # result = node_indentation + "Leaf, class label: " + str(self.classification) + ", [" + str(
            #     self.nb_of_examples_with_label) + "/" + str(self.nb_of_examples_in_this_node) + "]" + '\n'
            return result
        else:
            result = node_indentation + 'INode, query: ' + str(self.query) + '\n'

            if self.get_left_child_node() is not None:
                result = result + self.get_left_child_node().to_string(child_indentation, 1)
            if self.get_right_child_node() is not None:
                result = result + self.get_right_child_node().to_string(child_indentation, 2)
            return result

    def can_classify(self) -> object:
        if self.strategy is None:
            raise AttributeError('TreeNode has no Strategy')
        else:
            return self.strategy.can_classify()


class DeterministicLeafMergeException(Exception):
    pass


class DeterministicLeafStrategy(LeafStrategy):
    def __init__(self, classification: Term, nb_of_examples_with_label: int, nb_of_examples_in_this_node: int):
        self.classification = classification  # type: Term
        self.nb_of_examples_with_label = nb_of_examples_with_label  # type: int
        self.nb_of_examples_in_this_node = nb_of_examples_in_this_node  # type: int

    def can_classify(self) -> object:
        return isinstance(self.classification, Term)

    def to_string(self, node_indentation) -> str:
        result = node_indentation + "Leaf, class label: " + str(self.classification) + ", [" + str(
            self.nb_of_examples_with_label) + "/" + str(self.nb_of_examples_in_this_node) + "]" + '\n'
        return result

    def merge(self, other: 'DeterministicLeafStrategy'):
        if other.classification is not self.classification:
            raise DeterministicLeafMergeException('2 DeterministicLeafStrategy cannot be merged, one has '
                                                  'classification:' + str(self.classification) + ", the other has "
                                                                                                 "classification: " +
                                                  str(other.classification))
        self.nb_of_examples_with_label += other.nb_of_examples_with_label
        self.nb_of_examples_in_this_node += other.nb_of_examples_in_this_node

    # def get_leaf_clause(self, previous_conjunction):
    #     return self.classification << previous_conjunction


class MLEDeterministicLeafStrategy(LeafStrategy):
    def __init__(self, label_frequencies: Dict[Term, float], label_absolute_counts: Dict[Term, float]):
        self.label_frequencies = label_frequencies  # type: Dict[Term, float]
        self.label_absolute_counts = label_absolute_counts  # type: Dict[Term, float]
        self.nb_of_examples_in_this_node = sum(self.label_absolute_counts.values())  # type: int

    def can_classify(self) -> bool:
        return isinstance(self.label_frequencies, dict)

    def to_string(self, node_indentation) -> str:
        result = node_indentation + "Leaf, class label frequencies: " + str(
            self.label_frequencies) + ", class label counts" + str(
            self.label_absolute_counts) + "/" + str(self.nb_of_examples_in_this_node) + "]" + '\n'
        return result

    # def get_leaf_clause(self,  previous_conjunction: Term):
    #     var = self.prediction_goal.args[self.index]  # type: Var
    #     label_frequencies = node.label_frequencies  # type: Optional[Dict[Label, float]]
    #
    #     goals_with_probabilities = []
    #
    #     for label in label_frequencies.keys():
    #         substitution = {var.name: label}  # type: Dict[str, Term]
    #         goal_with_label = apply_substitution_to_term(self.prediction_goal, substitution)  # type: Term
    #         probability_of_goal = Constant(label_frequencies[label])
    #         goal_with_label.probability = probability_of_goal
    #         goals_with_probabilities.append(goal_with_label)
    #
    #     return AnnotatedDisjunction(goals_with_probabilities, previous_conjunction)
