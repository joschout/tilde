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

from problog.logic import Term, And, Var
from problog.program import SimpleProgram

from problog_helper.problog_helper import apply_substitution_to_term
from representation.language import TypeModeLanguage
from trees import TreeNode
from trees.TreeNode import get_predicate_generator


def decision_tree_to_simple_program2(node: TreeNode, simple_program: SimpleProgram,
                                     predicate_generator, previous_conjunction=Term('true'),
                                     debug_printing=False):
    if node.has_both_children():
        # assign a new predicate to this node
        p = next(predicate_generator)

        # the following if-else is only necessary to remove an unnecessary 'true' term in the head
        if previous_conjunction.functor == 'true':
            conj_left = node.query.get_literal()
            conj_right = ~p
        else:
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


def convert_tree_to_simple_program(tree_root: TreeNode, language: TypeModeLanguage, debug_printing=False) -> SimpleProgram:
    if debug_printing:
        print('\n=== START conversion of tree to program ===')
        print('tree to be converted:')
        print(tree_root.to_string2())
    predicate_generator = get_predicate_generator(language)
    program = SimpleProgram()
    decision_tree_to_simple_program2(tree_root, program, predicate_generator, debug_printing=debug_printing)
    if debug_printing:
        print('resulting program:')
        for statement in program:
            print(statement)
        print('=== END conversion of tree to program ===\n')
    return program


class InvalidTreeNodeError(Exception):
    pass


class TreeToProgramConverter:
    def __init__(self, debug_printing=False):
        self.debug_printing = debug_printing
        self.predicate_generator = None
        self.program = None

    def convert_tree_to_simple_program(self, tree_root: TreeNode, language: TypeModeLanguage) -> SimpleProgram:
        if self.debug_printing:
            print('\n=== START conversion of tree to program ===')
            print('tree to be converted:')
            print(tree_root.to_string2())
        self.predicate_generator = get_predicate_generator(language)
        self.program = SimpleProgram()
        self._decision_tree_to_simple_program(tree_root)
        if self.debug_printing:
            print('resulting program:')
            for statement in self.program:
                print(statement)
            print('=== END conversion of tree to program ===\n')
        return self.program

    def _decision_tree_to_simple_program(self, node: TreeNode, previous_conjunction=Term('true')):
        if node.has_both_children():
            self._handle_inner_node(node, previous_conjunction)
        elif node.classification is not None:
            self._handle_leaf_node(node, previous_conjunction)
        else:
            raise InvalidTreeNodeError()

    def _handle_inner_node(self, node: TreeNode, previous_conjunction: Term):
        # assign a new predicate to this node
        p = next(self.predicate_generator)

        # the following if-else is only necessary to remove an unnecessary 'true' term in the head
        if previous_conjunction.functor == 'true':
            conj_left = node.query.get_literal()
            conj_right = ~p
        else:
            conj_left = And(previous_conjunction, node.query.get_literal())
            conj_right = And(previous_conjunction, ~p)
        clause = (p << conj_left)
        self.program += clause

        # recurse on left subtree
        self._decision_tree_to_simple_program(node.left_subtree, conj_left)
        # recurse on right subtree
        self._decision_tree_to_simple_program(node.right_subtree, conj_right)

    def _handle_leaf_node(self, node: TreeNode, previous_conjunction: Term):
        clause = self.get_leaf_node_clause(node, previous_conjunction)
        self.program += clause

    def get_leaf_node_clause(self, node: TreeNode, previous_conjunction: Term):
        raise NotImplementedError('abstract method')


class ModelsTreeToProgramConverter(TreeToProgramConverter):
    def get_leaf_node_clause(self, node, previous_conjunction):
        return node.classification << previous_conjunction


class KeyTreeToProgramConverter(TreeToProgramConverter):
    def __init__(self, prediction_goal, index, debug_printing=False):
        super().__init__(debug_printing)
        self.prediction_goal = prediction_goal
        self.index = index

    def get_leaf_node_clause(self, node, previous_conjunction):
        var = self.prediction_goal.args[self.index]  # type: Var
        label = node.classification  # type: Term
        substitution = {var.name: label}
        goal_with_label = apply_substitution_to_term(self.prediction_goal, substitution)  # type: Term
        return goal_with_label << previous_conjunction






