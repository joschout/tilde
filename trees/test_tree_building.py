from problog.program import SimpleProgram

from mach_tests.mach_definitions_logic import sendback, fix, ok
from mach_tests.mach_definitions_TILDE_paper import labeled_examples, background_knowledge, possible_targets, language_machines
from trees.TreeNode import get_predicate_generator, decision_tree_to_simple_program2
from trees.TreeBuilder import TreeBuilder
from mach_tests.mach_definitions_examples_ACE import ex1
from classification import get_label_single_example

tree_builder = TreeBuilder(language_machines, background_knowledge, possible_targets)

tree_builder.build_tree(labeled_examples)
tree = tree_builder.get_tree()
print(tree)

predicate_generator = get_predicate_generator(language_machines)

program = SimpleProgram()
decision_tree_to_simple_program2(tree, program, predicate_generator)

labels_ex1 = get_label_single_example(ex1, program, [sendback, fix, ok])
print(labels_ex1)
