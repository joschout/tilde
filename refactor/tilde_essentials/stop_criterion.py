from refactor.tilde_essentials.splitter import SplitInfo
import math


class StopCriterion:
    # def should_investigate_node(self):
    #     raise NotImplementedError('abstract method')

    def __init__(self, max_depth: int = math.inf,
                 min_samples_split: int = 2,
                 min_samples_leaf: int = 1
                 ):
        self.max_depth = max_depth
        self.min_samples_split = min_samples_split
        self.min_samples_leaf = min_samples_leaf

    def cannot_split_before_test(self, examples, depth):
        """
        If we already know we cannot split without having to calculate possible tests,
        report True here.

        :param depth:
        :param examples:
        :return:
        """
        if depth >= self.max_depth:
            return True

        if len(examples) < self.min_samples_split:
            return True

    def _not_enough_examples_in_leaves(self, split_info: SplitInfo) -> bool:
        """
        Return true if the smallest of the two subsets has NOT enough examples to be acceptable as a leaf.

        # NOTE: I changed it back to min, this explanation isn't true anymore
        # REASON: setting:
        #     minimal_cases(n).
        #           the minimal nb of examples that a leaf in the tree should cover
        #
        # (De Raedt: a good heuristic:
        # stop expanding nodes
        #   WHEN the number of examples in the nodes falls below a certain (user-defined threshold)
        # NOTE:
        #   the nodes get split into two children
        #   --> possible case:
        #       only for 1 of the children, the nb of examples falls below the threshold
        # IF by splitting,
        #       ONE of the nodes falls below a certain user-defined threshold
        #           (i.e. the MIN of their nbs < threshold)
        #       THEN we don't split this node

        :param split_info:
        :return:
        """
        return min(
            len(split_info.examples_left), len(split_info.examples_right)
        ) < self.min_samples_leaf

    def cannot_split_on_test(self, split_info: SplitInfo):
        if not split_info.passing_score():
            return True

        if self._not_enough_examples_in_leaves(split_info):
            return True

        return False


