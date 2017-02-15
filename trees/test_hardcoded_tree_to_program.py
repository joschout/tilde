# Hardcoded example to start with
#                           n0: worn(X)
#                   ________/   \_______
#                  /                    \
#         n1: not_replaceable(X)         n2: class(ok)
#        _______/   \_______
#       /                   \
# n3: class(sendback)       n4: class(fix)
#


from classification import get_label_single_example, get_label
from trees.TreeNode import *
from mach_tests.mach_definitions_examples_ACE import examples
from mach_tests.mach_definitions_logic import *
from mach_tests.mach_definitions_TILDE_paper import language_machines


# === creating the decision tree ===============
tree_node_n3 = TreeNode()
tree_node_n3.classification = sendback

tree_node_n4 = TreeNode()
tree_node_n4.classification = fix

tree_node_n1 = TreeNode()
tree_node_n1.left_subtree = tree_node_n3
tree_node_n1.right_subtree = tree_node_n4
tree_node_n1.conj = not_replaceable(X)

tree_node_n2 = TreeNode()
tree_node_n2.classification = ok

tree_node_n0 = TreeNode()
tree_node_n0.left_subtree = tree_node_n1
tree_node_n0.right_subtree = tree_node_n2
tree_node_n0.conj = worn(X)

# === converting the decision tree to prolog ==========
program = SimpleProgram()

decision_tree_to_simple_program(tree_node_n0, program)

possible_labels =[sendback, fix, ok]

ex1 = examples[0]
labels = get_label([ex1], program, possible_labels)
print(labels)

result2 = get_label_single_example(ex1, program, possible_labels)
print(result2)




