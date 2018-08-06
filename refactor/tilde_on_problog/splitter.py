from refactor.tilde_essentials.splitter import Splitter, SplitInfo
from refactor.tilde_essentials.tree_node import TreeNode
from tilde.representation.language import TypeModeLanguage
from tilde.trees.RefinementController import RefinementController


class ProblogSplitter(Splitter):

    def __init__(self, language: TypeModeLanguage):
        self.language = language

    def _generate_possible_tests(self, examples, current_node):
        query = current_node.test
        return RefinementController.get_refined_query_generator(
            query, self.language)  # type: Iterable[TILDEQuery]
