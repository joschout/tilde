from mai_version.trees.TreeNode import TreeNode
from mai_version.trees.leaf_strategy import DeterministicLeafStrategy


def prune_leaf_nodes_with_same_label(node: TreeNode):
    """"
    NOTE: assumes Deterministic leaf nodes with ONE class label


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
        if not isinstance(left_child_node.strategy, DeterministicLeafStrategy):
            print("can only prune leaves with DeterministicLeafStrategy")
            return

        if not isinstance(right_child_node.strategy, DeterministicLeafStrategy):
            print("can only prune leaves with DeterministicLeafStrategy")
            return

        if left_child_node.strategy.classification == right_child_node.strategy.classification:
            left_child_node.strategy.merge(right_child_node.strategy)
            node.strategy = left_child_node.strategy
            node.left_subtree = None
            node.right_subtree = None


