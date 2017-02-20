# def decision_tree_to_simple_program(node: TreeNode, simple_program: SimpleProgram, previous_conjunction=Term('true')):
#     # if the current node is a leaf
#     if node.left_subtree is None and node.right_subtree is None:
#         if node.classification is not None:
#             clause = (node.classification << previous_conjunction)
#             simple_program += clause
#             return [node.classification]
#         else:
#             raise InvalidTreeNodeError()
#     else:
#         # for the left subnode
#         total_conj_left_node = And(previous_conjunction, node.conj)
#         left_class_labels = decision_tree_to_simple_program(node.left_subtree, simple_program, total_conj_left_node)
#
#         # for the right subnode
#         negated_left_class_labels = [~label for label in left_class_labels]
#         conj_of_neg_left_class_ables = And.from_list(negated_left_class_labels)
#         total_conj_right_node = And(conj_of_neg_left_class_ables, previous_conjunction)
#         right_class_labels = decision_tree_to_simple_program(node.right_subtree, simple_program, total_conj_right_node)
#         return left_class_labels + right_class_labels

from problog.logic import Term, And
from problog.program import SimpleProgram

from representation.language import TypeModeLanguage
from trees import TreeNode
from trees.TreeNode import get_predicate_generator


def decision_tree_to_simple_program2(node: TreeNode, simple_program: SimpleProgram,
                                     predicate_generator, previous_conjunction=Term('true')):
    if node.left_subtree is not None and node.left_subtree is not None:
        # assign a new predicate to this node
        p = next(predicate_generator)
        conj_left = And(previous_conjunction, node.query.get_literal())
        conj_right = And(previous_conjunction, ~p)
        clause = (p << conj_left)
        simple_program += clause

        # recurse on left subtree
        decision_tree_to_simple_program2(node.left_subtree, simple_program, predicate_generator, conj_left)
        # recurse on right subtree
        decision_tree_to_simple_program2(node.right_subtree, simple_program, predicate_generator, conj_right)
    else:
        if node.classification is not None:
            clause = (node.classification << previous_conjunction)
            simple_program += clause
        else:
            raise InvalidTreeNodeError()


def convert_tree_to_simple_program(tree: TreeNode, language: TypeModeLanguage) -> SimpleProgram:
    predicate_generator = get_predicate_generator(language)
    program = SimpleProgram()
    decision_tree_to_simple_program2(tree, program, predicate_generator)
    return program


class InvalidTreeNodeError(Exception):
    pass

