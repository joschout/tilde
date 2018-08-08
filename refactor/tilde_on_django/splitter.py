from typing import Optional

from refactor.tilde_essentials.split_criterion import SplitCriterionBuilder
from refactor.tilde_essentials.splitter import Splitter, SplitInfo
from refactor.tilde_essentials.tree_node import TreeNode


class DjangoSplitter(Splitter):

    def get_split(self, examples, current_node: TreeNode) -> Optional[SplitInfo]:
        current_best_split_info = None
        split_criterion = SplitCriterionBuilder.get_split_criterion(
            self.split_criterion_str,
            examples, current_node.get_labels(examples))

        generator = self.test_generator_builder.generate_possible_tests(examples, current_node)
        for candidate_test in generator:
            print(candidate_test)
            examples_satisfying_test, examples_not_satisfying_test = self._split_examples(candidate_test, examples)

            candidate_test_score = split_criterion.calculate(examples_satisfying_test,
                                                             examples_not_satisfying_test
                                                             )
            if current_best_split_info is None or candidate_test_score > current_best_split_info.score:
                current_best_split_info = SplitInfo(test=candidate_test,
                                                    examples_left=examples_satisfying_test,
                                                    examples_right=examples_not_satisfying_test,
                                                    score=candidate_test_score,
                                                    threshold=split_criterion.get_threshold(),
                                                    split_criterion=split_criterion.get_name())
            else:
                # if we do not keep the query, destruct it
                candidate_test.destruct()
        return current_best_split_info

