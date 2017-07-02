from trees.TreeNode import TreeNode


def prune_leaf_nodes_with_same_label(node: TreeNode):
    """"
    Case: node = leaf node
        --> return
        
    Case: BOTH child nodes of this node are leaf node
        --> case: both have the same label
                --> prune the children
            case: they don't have the same label
                --> return
    Case: one or both of the child nodes are inner nodes
        --> go into the children
            AND MAYBE PRUNE
            --> if it has become a child node
                --> prune    
    """

    # TODO: fails when given None
    if node is None:
        return

    left_child_node = node.get_left_child_node()
    right_child_node = node.get_right_child_node()

    if left_child_node is None or right_child_node is None:
        return

    left_is_leaf = left_child_node.is_leaf_node()
    right_is_leaf = right_child_node.is_leaf_node()

    if not left_is_leaf:
        prune_leaf_nodes_with_same_label(left_child_node)
    if not right_is_leaf:
        prune_leaf_nodes_with_same_label(right_child_node)

    # check again
    left_is_leaf = left_child_node.is_leaf_node()
    right_is_leaf = right_child_node.is_leaf_node()

    # if both children are leaf node
    if left_is_leaf and right_is_leaf:
        if left_child_node.classification == right_child_node.classification:
            node.classification = left_child_node.classification
            node.nb_of_examples_with_label = left_child_node.nb_of_examples_with_label + right_child_node.nb_of_examples_with_label
            node.nb_of_examples_in_this_node = left_child_node.nb_of_examples_in_this_node + right_child_node.nb_of_examples_in_this_node
            node.left_subtree = None
            node.right_subtree = None


