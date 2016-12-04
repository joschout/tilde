# Hardcoded example to start with
#                           n0: worn(X)
#                   ________/   \_______
#                  /                    \
#         n1: not_replaceable(X)         n2: class(ok)
#        _______/   \_______
#       /                   \
# n3: class(sendback)       n4: class(fix)
#

from problog.logic import Var, Term
from trees.TreeNode import *

X = Var('X')
Y = Var('Y')
Z = Var('Z')

sendback, fix, ok, worn, replaceable = \
    Term('sendback'), Term('fix'), Term('ok'), Term('worn'), Term('replaceable')

not_replaceable = Term('not_replaceable')

worn_X = worn(X)
not_replaceable_X = not_replaceable(X)

tree_node_n3 = TreeNode()
tree_node_n3.classification = sendback

tree_node_n4 = TreeNode()
tree_node_n4.classification = fix

tree_node_n1 = TreeNode()
tree_node_n1.left_subtree = tree_node_n3
tree_node_n1.right_subtree = tree_node_n4
tree_node_n1.conj = not_replaceable_X

tree_node_n2 = TreeNode()
tree_node_n2.classification = ok

tree_node_n0 = TreeNode()
tree_node_n0.left_subtree = tree_node_n1
tree_node_n0.right_subtree = tree_node_n2
tree_node_n0.conj = worn_X

program = SimpleProgram()
decision_tree_to_SimpleProgram(tree_node_n0, program)

print(program)