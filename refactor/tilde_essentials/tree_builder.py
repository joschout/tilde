from refactor.tilde_essentials.splitter import Splitter
from refactor.tilde_essentials.stop_criterion import StopCriterion
from refactor.tilde_essentials.tree_node import TreeNode


class TreeBuilder:

    def __init__(self,
                 splitter: Splitter,
                 leaf_builder,
                 stop_criterion: StopCriterion = StopCriterion()
                 ):
        self.splitter = splitter
        self.leaf_builder = leaf_builder
        self.stop_criterion = stop_criterion
        self.tree_root = None  # type: TreeNode

    def build(self, examples):
        if self._builder_check:
            self.tree_root = TreeNode(depth=0, parent=None)

            self._build_recursive(examples, self.tree_root)
            return
        # recurse

    def _build_recursive(self, examples, current_node):

        if self.stop_criterion.cannot_split_before_test(examples, current_node.depth):
            self.leaf_builder.build(current_node, split_info=None)
        else:

            split_info = self.splitter.get_split(examples, current_node)

            if self.stop_criterion.cannot_split_on_test(split_info):
                self.leaf_builder.build(current_node, split_info)
            else:
                current_node.test = split_info.test

                child_depth = current_node.depth + 1
                # left_child
                current_node.left_child = TreeNode(child_depth, current_node)
                left_examples = split_info.examples_left
                self._build_recursive(left_examples, current_node.left_child)

                current_node.right_child = TreeNode(child_depth, current_node)
                right_examples = split_info.examples_right
                self._build_recursive(right_examples, current_node.right_child)

    @property
    def _builder_check(self):
        """
        Returns True if the builder has been initialized correctly

        :return:
        """
        if (
                self.splitter is None or
                self.leaf_builder is None or
                self.stop_criterion is None
        ):
            return False
        else:
            return True
