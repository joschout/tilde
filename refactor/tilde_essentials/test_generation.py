from refactor.tilde_essentials.tree_node import TreeNode


class TestGeneratorBuilder:
    """
    Builds a generator to produce possible tests in a node to be split.

    """
    def generate_possible_tests(self, examples, current_node):
        raise NotImplementedError('abstract method')


class FOLTestGeneratorBuilder(TestGeneratorBuilder):
    """
    Builds a generator to produce possible tests in a node to be split.
    Finds the associated test of the node, which is the test of the ancestor of the current node whose test should be refined.

    """

    def generate_possible_tests(self, examples, current_node):
        raise NotImplementedError('abstract method')

    def __init__(self, initial_query):
        self.initial_query = initial_query  # the associated query of the root node

    def _get_associated_query(self, current_node: TreeNode):

        query_to_refine = None
        ancestor = current_node

        while query_to_refine is None:
            if ancestor.parent is None:
                query_to_refine = self.initial_query
            else:
                # NOTE: this depends on whether the current node is the LEFT or RIGHT subtree
                # IF it is the left subtree:
                #       use the query of the parent
                # ELSE (if it is the right subtree:
                #       go higher up in the tree
                #          until a node is found that is the left subtree of a node
                #           OR the root is reached

                parent_of_ancestor = ancestor.parent
                if ancestor is parent_of_ancestor.left_child:
                    query_to_refine = parent_of_ancestor.test
                else:
                    ancestor = parent_of_ancestor
        return query_to_refine


