from refactor.tilde_essentials.example import get_labels

#
# class TreeBuildInfo:
#     def __init__(self):
#         self.labels = None
#         self.n_examples = None
from refactor.tilde_essentials.tree_printer import TreeNodePrinter


class TreeNode:
    def __init__(self, parent=None, depth=0):
        self.parent = parent
        self.depth = depth

        self.left_child = None
        self.right_child = None

        self.test = None

        self.labels = None

        self.leaf_strategy = None

    def get_labels(self, examples):
        if self.labels is not None:
            return self.labels
        else:
            self.labels = get_labels(examples)

    def is_leaf_node(self) -> bool:
        return self.left_child is None and self.right_child is None

    def __str__(self):
        return TreeNodePrinter.to_string(self)
