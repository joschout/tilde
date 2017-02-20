from classification import get_label_single_example
from mach_tests.mach_definitions_TILDE_paper import labeled_examples, background_knowledge, possible_targets, language_machines
from mach_tests.mach_definitions_examples_ACE import ex1
from mach_tests.mach_definitions_logic import sendback, fix, ok
from trees.TreeBuilder import TreeBuilder
from trees.tree_converter import convert_tree_to_simple_program

tree_builder = TreeBuilder(language_machines, background_knowledge, possible_targets)

tree_builder.build_tree(labeled_examples)
tree = tree_builder.get_tree()
print(tree)


program = convert_tree_to_simple_program(tree, language_machines)

labels_ex1 = get_label_single_example(ex1, program, [sendback, fix, ok])
print(labels_ex1)
