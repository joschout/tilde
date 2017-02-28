from typing import Optional, Iterator

from problog.logic import *

# class PredicateGenerator:
#     count = 0
#
#     def __init__(self, language):
#         self.language = language
from representation.language import TypeModeLanguage
from representation.TILDE_query import TILDEQuery


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


class FOLDecisitionTree:
    """A First-Order Logical Decision Tree"""
    root_node = None  # type: TreeNode

    def __init__(self, example_list) -> None:
        root_node = TreeNode()
        query = True
        root_node.build_tree(example_list, query)


class TreeNode:
    """A node in a First-Order Logical Decision Tree.

    There are two kinds of nodes: decision nodes and leaf nodes"""
    left_subtree = None  # type: Optional(TreeNode)
    right_subtree = None  # type: Optional(TreeNode)

    # conj = True  # DEPRECATED

    query = None  # type: Optional(TILDEQuery)
    classification = None

    def get_left_child_node(self) -> 'TreeNode':
        return self.left_subtree

    def get_right_child_node(self) -> 'TreeNode':
        return self.right_subtree

        # def build_tree(self, example_list):
        #     # check if the tree is homogeneous
        #     homogeneous_check =\
        #         is_current_example_set_sufficiently_homogenous(example_list)
        #     if homogeneous_check:
        #         return
        #     else:
        #         refined_query = get_best_refined_query(self.query, example_list)

    def to_string(self, level=0):
        """
        Represents the tree as a string without fancy layouting
        :param level:
        :return:
        """
        if self.get_left_child_node() is None and self.get_right_child_node() is None:
            result = '\t' * level + "Leaf, classlabel: " + str(self.classification) + '\n'
            return result
        else:
            result = '\t' * level + 'INode\n'
            if self.get_left_child_node() is not None:
                result = result + self.get_left_child_node().to_string(level + 1)
            if self.get_right_child_node() is not None:
                result = result + self.get_right_child_node().to_string(level + 1)
            return result

    def to_string2(self, indentation='', currentNodeNumber=0):
        """
        Represents the tree as a string using some layouting
        :param indentation:
        :param currentNodeNumber:
        :return:
        """
        node_indentation = indentation
        child_indentation = indentation

        if currentNodeNumber == 0:
            child_indentation = '\t'
        elif currentNodeNumber == 1:
            node_indentation += '|-'
            child_indentation += '|\t'
        else:
            node_indentation += '\-'
            child_indentation += '\t'

        if self.get_left_child_node() is None and self.get_right_child_node() is None:
            result = node_indentation + "Leaf, class label: " + str(self.classification) + '\n'
            return result
        else:
            result = node_indentation + 'INode, query: ' + str(self.query) + '\n'

            if self.get_left_child_node() is not None:
                result = result + self.get_left_child_node().to_string2(child_indentation, 1)
            if self.get_right_child_node() is not None:
                result = result + self.get_right_child_node().to_string2(child_indentation, 2)
            return result
