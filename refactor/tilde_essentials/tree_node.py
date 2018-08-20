from typing import Optional

from refactor.tilde_essentials.destuctable import Destructible
from refactor.tilde_essentials.example import get_labels

#
# class TreeBuildInfo:
#     def __init__(self):
#         self.labels = None
#         self.n_examples = None
# from refactor.tilde_essentials.tree_printer import TreeNodePrinter


class TreeNode(Destructible):
    """

    """
    def __init__(self, parent=None, depth=0):
        self.parent = parent  # type: Optional['TreeNode']
        self.depth = depth  # type: int

        self.left_child = None  # type: Optional['TreeNode']
        self.right_child = None  # type: Optional['TreeNode']

        self.test = None

        # the set of labels occurring in this node
        self.labels = None

        self.leaf_strategy = None

    def get_labels(self, examples):
        if self.labels is None:
            self.labels = get_labels(examples)
        return self.labels

    def is_leaf_node(self) -> bool:
        return self.left_child is None and self.right_child is None

    def __str__(self):
        return TreeNodePrinter.to_string(self)

    def destruct(self):
        destruct_method = getattr(self.test, 'destruct', None)
        if callable(destruct_method):
            self.test.destruct()
        if self.left_child is not None:
            self.left_child.destruct()
        if self.right_child is not None:
            self.right_child.destruct()


def count_nb_of_nodes(node: Optional['TreeNode'] = None) -> int:

    if node is None:
        return 0
    else:
        count = 1  # count the node itself
        count += count_nb_of_nodes(node.left_child)
        count += count_nb_of_nodes(node.right_child)

        return count


def count_nb_of_inner_nodes(node: Optional['TreeNode'] = None) -> int:

    if node.is_leaf_node():
        return 0
    else:
        count = 1
        count += count_nb_of_inner_nodes(node.left_child)
        count += count_nb_of_inner_nodes(node.right_child)
        return count


class TreeNodePrinter:
    """
    Pretty prints a TreeNode tree structure.
    """

    setting = "full"

    @staticmethod
    def to_string(tree_node: TreeNode) -> str:
        if TreeNodePrinter.setting == "full":
            return TreeNodePrinter.to_string_full_query(tree_node)
        if TreeNodePrinter.setting == "compact":
            TreeNodePrinter.to_string_compact(tree_node)

    @staticmethod
    def to_string_full_query(tree_node: TreeNode, indentation='', current_node_number=0) -> str:
        """
        Represents the tree as a string using some layouting
        :param tree_node:
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

        if tree_node.is_leaf_node():
            result = tree_node.leaf_strategy.to_string(node_indentation)
            # result = node_indentation + "Leaf, class label: " + str(self.classification) + ", [" + str(
            #     self.nb_of_examples_with_label) + "/" + str(self.nb_of_examples_in_this_node) + "]" + '\n'
            return result
        else:
            result = node_indentation + 'INode, query: ' + str(tree_node.test) + '\n'

            if tree_node.left_child is not None:
                result = result + TreeNodePrinter.to_string_full_query(tree_node.left_child, child_indentation, 1)
            if tree_node.right_child is not None:
                result = result + TreeNodePrinter.to_string_full_query(tree_node.right_child, child_indentation, 2)
            return result

    @staticmethod
    def to_string_compact(tree_node: TreeNode, indentation='', current_node_number=0):
        """
        Represents the tree as a string using some layouting
        :param tree_node:
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

        if tree_node.is_leaf_node():
            if current_node_number == 0:
                result = tree_node.leaf_strategy.to_string_compact()
            elif current_node_number == 1:
                result = node_indentation + 'yes: ' + tree_node.leaf_strategy.to_string_compact()
            else:
                result = node_indentation + 'no: ' + tree_node.leaf_strategy.to_string_compact()

            # result = self.strategy.to_string(node_indentation)

            # result = node_indentation + "Leaf, class label: " + str(self.classification) + ", [" + str(
            #     self.nb_of_examples_with_label) + "/" + str(self.nb_of_examples_in_this_node) + "]" + '\n'
            return result
        else:
            if current_node_number == 0:
                # TODO: remove dependency from TILDEQueryHiddenLiteral
                if tree_node.test.parent is not None:
                # if tree_node.test.parent is not None and isinstance(tree_node.test.parent, TILDEQueryHiddenLiteral):
                    result = str(tree_node.test.parent.literal) + '\n'
                else:
                    result = ""

                result = result + str(tree_node.test.get_literal()) + ' ?\n'

            elif current_node_number == 1:
                result = node_indentation + 'yes: ' + str(tree_node.test.get_literal()) + ' ?\n'
            else:
                result = node_indentation + 'no: ' + str(tree_node.test.get_literal()) + ' ?\n'

            # result = node_indentation + 'INode, query: ' + str(self.query) + '\n'

            if tree_node.left_child is not None:
                result = result + TreeNodePrinter.to_string_compact(tree_node.left_child, child_indentation, 1)
            if tree_node.right_child is not None:
                result = result + TreeNodePrinter.to_string_compact(tree_node.right_child, child_indentation, 2)
            return result
