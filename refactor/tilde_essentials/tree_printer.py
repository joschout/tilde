
class TreeNodePrinter:

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
