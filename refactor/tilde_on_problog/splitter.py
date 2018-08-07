from typing import Optional

from problog.logic import Term

from refactor.tilde_essentials.evaluation import TestEvaluator
from refactor.tilde_essentials.splitter import Splitter, SplitInfo
from refactor.tilde_essentials.tree_node import TreeNode
from tilde.representation.TILDE_query import TILDEQuery, TILDEQueryHiddenLiteral
from tilde.representation.language import TypeModeLanguage
from tilde.trees.RefinementController import RefinementController


class ProblogSplitter(Splitter):

    def __init__(self, language: TypeModeLanguage,
                 split_criterion_str,
                 test_evaluator: TestEvaluator,
                 query_head_if_keys_format: Optional[Term] = None):
        super().__init__(split_criterion_str, test_evaluator)
        self.language = language

        if query_head_if_keys_format is not None:
            self.initial_query = TILDEQueryHiddenLiteral(query_head_if_keys_format)
        else:
            self.initial_query = TILDEQuery(None, None)

    def _generate_possible_tests(self, examples, current_node: TreeNode):

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

        return RefinementController.get_refined_query_generator(
            query_to_refine, self.language)
