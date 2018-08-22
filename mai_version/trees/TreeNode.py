from typing import Optional

from mai_version.representation.TILDE_query import TILDEQuery, TILDEQueryHiddenLiteral
from mai_version.trees.leaf_strategy import LeafStrategy


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

    def to_string_full_query(self, indentation='', current_node_number=0):
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
                result = result + self.get_left_child_node().to_string_full_query(child_indentation, 1)
            if self.get_right_child_node() is not None:
                result = result + self.get_right_child_node().to_string_full_query(child_indentation, 2)
            return result

    def to_string_compact(self, indentation='', current_node_number=0):
        """
        Represents the tree as a string using some layouting
        :param indentation:
        :param current_node_number:
        :return:
        """
        node_indentation = indentation
        child_indentation = indentation

        if current_node_number == 0:  # root node
            child_indentation = ''
        elif current_node_number == 1:  # this node is the LEFT child node of its parent
            node_indentation += '+--'
            child_indentation += '|       '
        else:  # this node is the RIGHT child node of its parent
            node_indentation += '+--'
            child_indentation += '        '

        if self.is_leaf_node():
            if current_node_number == 0:
                result = self.strategy.to_string_compact()
            elif current_node_number == 1:
                result = node_indentation + 'yes: ' + self.strategy.to_string_compact()
            else:
                result = node_indentation + 'no: ' + self.strategy.to_string_compact()

            # result = self.strategy.to_string(node_indentation)

            # result = node_indentation + "Leaf, class label: " + str(self.classification) + ", [" + str(
            #     self.nb_of_examples_with_label) + "/" + str(self.nb_of_examples_in_this_node) + "]" + '\n'
            return result
        else:
            if current_node_number == 0:
                if self.query.parent is not None and isinstance(self.query.parent, TILDEQueryHiddenLiteral):
                    result = str(self.query.parent.literal) + '\n'
                else:
                    result = ""

                result = result + str(self.query.get_literal()) + ' ?\n'

            elif current_node_number == 1:
                result = node_indentation + 'yes: ' + str(self.query.get_literal()) + ' ?\n'
            else:
                result = node_indentation + 'no: ' + str(self.query.get_literal()) + ' ?\n'

            # result = node_indentation + 'INode, query: ' + str(self.query) + '\n'

            if self.get_left_child_node() is not None:
                result = result + self.get_left_child_node().to_string_compact(child_indentation, 1)
            if self.get_right_child_node() is not None:
                result = result + self.get_right_child_node().to_string_compact(child_indentation, 2)
            return result

    def __str__(self):
        return self.to_string_compact()

    def get_nb_of_nodes(self) -> int:
        return TreeNode._count_nb_of_nodes(self)

    @staticmethod
    def _count_nb_of_nodes(node:Optional['TreeNode'] = None) -> int:

        if node is None:
            return 0
        else:
            count = 1  # count the node itself
            count += TreeNode._count_nb_of_nodes(node.left_subtree)
            count += TreeNode._count_nb_of_nodes(node.right_subtree)

            return count

    def get_nb_of_inner_nodes(self):
        return TreeNode._count_nb_of_inner_nodes(self)

    @staticmethod
    def _count_nb_of_inner_nodes(node:Optional['TreeNode'] = None) -> int:

        if node.is_leaf_node():
            return 0
        else:
            count = 1
            count += TreeNode._count_nb_of_inner_nodes(node.left_subtree)
            count += TreeNode._count_nb_of_inner_nodes(node.right_subtree)
            return count

    def can_classify(self) -> object:
        if self.strategy is None:
            raise AttributeError('TreeNode has no Strategy')
        else:
            return self.strategy.can_classify()


