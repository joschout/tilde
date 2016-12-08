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
from mach_tests.machine_examples import examples
from mach_tests.test_get_label import get_label
from problog.engine import DefaultEngine

X = Var('X')
Y = Var('Y')
Z = Var('Z')

sendback, fix, ok, worn, replaceable = \
    Term('sendback'), Term('fix'), Term('ok'), Term('worn'), Term('replaceable')

not_replaceable = Term('not_replaceable')

worn_X = worn(X)
not_replaceable_X = not_replaceable(X)

def get_label_machines(example, rules):
    eng = DefaultEngine()
    eng.unknown = 1
    db = eng.prepare(example)
    for rule in rules:
        db += rule
    possible_labels = [sendback, fix, ok]
    result_list = [eng.query(db, x) for x in possible_labels]
    zipped = zip(result_list, possible_labels)
    labels_ex = []
    for result_ex, label in zipped:
        if result_ex == [()]:
            labels_ex.append(label)
    return labels_ex


# === creating the decision tree ===============
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

# === converting the decision tree to prolog ==========
program = SimpleProgram()
decision_tree_to_simple_program(tree_node_n0, program)


ex1 = examples[0]
labels = get_label([ex1], program)
print(labels)

engine = DefaultEngine()
engine.unknown = 1
db = engine.prepare(ex1)
for clause in program:
    db += clause
result = engine.query(db, sendback)
print(result)

result2 = get_label_machines(ex1, program)
print(result2)




