from typing import Iterable

from problog.logic import Term
from problog.program import LogicProgram

from refactor.tilde_essentials.tree_node import TreeNode
from src.ClauseWrapper import ClauseWrapper, HypothesisWrapper
from tilde.representation.TILDE_query import TILDEQuery
from tilde.representation.example import ExampleWrapper


def build_clause(example: ExampleWrapper) -> ClauseWrapper:

    clause = ClauseWrapper(clause_id=None)

    for fact_statement in example.logic_program:  # type: Term
        clause.add_literal_to_body(fact_statement)

    # TODO: remove ugly hack
    if hasattr(example, 'classification_term'):
        clause.add_literal_to_body(example.classification_term)

    clause.lock_adding_to_clause()
    clause.add_problog_clause(example)
    return clause


def build_hypothesis(tilde_query: TILDEQuery) -> HypothesisWrapper:
    clause = ClauseWrapper(clause_id=None)

    literals = tilde_query.get_literals()
    for literal in literals:
        clause.add_literal_to_body(literal)

    clause.lock_adding_to_clause()
    clause.add_problog_clause(tilde_query)

    hypothesis = HypothesisWrapper(clause)
    return hypothesis


def destruct_tree_tests(tree_node: TreeNode):
    if tree_node.test is not None:
        tree_node.test.destruct()

    if tree_node.left_child is not None:
        destruct_tree_tests(tree_node.left_child)

    if tree_node.right_child is not None:
        destruct_tree_tests(tree_node.right_child)
